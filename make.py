from parts.simple import generate_recipe, ingredientClass, recipeClass
from parts.classify import classify
from parts.w2vChef import ingredientIdeas, wordcheck
from parts.amount import get_amount
from parts.parings import pair
from parts.evaluators import waffleness_estimator, get_micronutrient_info
from parts.surprise import surprise_score
from parts.food_pair_probability import pair_score
from parts.gpt2Chef import ingredientIdeas_gpt2, find_ingredients
from random import randint
import gensim
import json
import sys
import random
import logging
import itertools
import copy

DEBUG = False

def generate_recipe_objects(possibilities):
    new_ingredients = []
    for possibility in possibilities:
        classed = classify(possibility)
        if not classed:
            classed = classify(possibility + "s")
        if not classed:
            classed = classify(possibility[:-1])
        if classed:
            a = int(get_amount(possibility))
            if a > 0:
                if DEBUG:print(classed)
                print(possibility)
                new_ingredient = ingredientClass()
                new_ingredient.define_me(possibility, a, classed)
                new_ingredients.append(new_ingredient)
        else:
            pass
            #print("no")
    return new_ingredients

def cook(inspiration, model, model_sel):
    possibilities = []
    print("You want me to make a " + inspiration + " waffle?")
    key_ingredients = []
    ESSENCIAL_INGREDIENT = False
    key_ingredients = find_ingredients(inspiration)
    if len(key_ingredients) >0:
        ESSENCIAL_INGREDIENT = True

    if model_sel == 0:
        # additional_keywd = random.choice(["butter","meal","bake", "ingredients", "flour"])
        flour_ideas = ingredientIdeas(model, [inspiration, "flour"], [])
        butter_ideas = ingredientIdeas(model, [inspiration, "butter"], [])
        sugar_ideas = ingredientIdeas(model, [inspiration, "sugar"], [])
        ingredient_ideas = ingredientIdeas(model, [inspiration, "ingredient"], [])
        meal_ideas = ingredientIdeas(model, [inspiration, "meal"], [])
        bake_ideas = ingredientIdeas(model, [inspiration, "bake"], [])
        spice_ideas = ingredientIdeas(model, [inspiration, "spice"], [])
        topping_ideas = ingredientIdeas(model, [inspiration, "topping"], [])
        ideas = flour_ideas + butter_ideas + sugar_ideas + ingredient_ideas + meal_ideas + bake_ideas + spice_ideas + topping_ideas
        ideas = set(ideas)
        # ideas = ingredientIdeas(model, [inspiration, additional_keywd], [])
        for idea in ideas:
            idea = idea[0].replace('_', ' ').lower()
            possibilities.append(idea)
            pieces = idea.split(" ", 1)
            if len(pieces) == 2:
                if pieces[0] not in possibilities:
                    possibilities.append(pieces[0])
                if pieces[1] not in possibilities:
                    possibilities.append(pieces[1])
            if DEBUG:print(idea)
    elif model_sel == 1:
        possibilities = ingredientIdeas_gpt2(inspiration)
    possibilities = set(possibilities)
    key_ingredients_object = []
    if ESSENCIAL_INGREDIENT:
        for i in key_ingredients:
            if i in possibilities:
                possibilities.remove(i)
        key_ingredients_object = generate_recipe_objects(key_ingredients)
    if DEBUG:print(possibilities)
    new_ingredients_object = generate_recipe_objects(possibilities)
    return new_ingredients_object, key_ingredients_object

def select(new_ingredients):
    number = 5
    number = min(number, len(new_ingredients))
    randos = random.sample(new_ingredients, number)
    return(randos)
    # suggestions = []
    # for rando in randos:
    #     ideas = pair(rando.get_name())
    #     random.shuffle(ideas)
    #     for idea in ideas:
    #         classed = classify(idea)
    #         if not classed:
    #             classed = classify(idea + "s")
    #         if not classed:
    #             classed = classify(idea[:-1])
    #         if classed:
    #             a = int(get_amount(idea))
    #             if a > 0:
    #                 new_ingredient = ingredientClass()
    #                 new_ingredient.define_me(idea, a, classed)
    #                 suggestions.append(new_ingredient)
    #                 break
    # return(randos + suggestions)

def select_all_possible_pair(new_ingredients,key_ingredients):
    result = []
    key_num = len(key_ingredients)
    if key_num > 0:
        if key_num > 4:
            lower_limit = 2
        else:
            lower_limit = 5 - key_num
    else:
        lower_limit = 5
    upper_limit = lower_limit + 1
    #upper_limit = min(upper_limit, len(new_ingredients))
    for n in range(lower_limit,upper_limit):
        for conb in itertools.combinations(new_ingredients, n):
            temp_list = []
            for c in conb:
                temp = copy.copy(c)
                temp_list.append(temp)
            if key_num > 0:
                sel_key_ing = random.sample(key_ingredients, min(3, key_num))
                for s in sel_key_ing:
                    temp = copy.copy(s)
                    temp_list.append(temp)
            result.append(temp_list)
            del temp_list
    print("Number of key ingredient:                        " + str(len(key_ingredients)))
    print("Number of inspired additional ingredient:        " + str(len(new_ingredients)))
    print("Number of possible combination of recipes:       " + str(len(result)))
    return result

def surprise_score_to_percentile(score):
    surprise_percentiles = [0.490, 0.512, 0.528, 0.545, 0.565, 0.580, 0.601, 0.624, 0.654, 0.748]
    for i in range(len(surprise_percentiles)):
        if score < surprise_percentiles[i]:
            return i
    return 9

def foodpair_score_to_percentile(score):
    foodpair_percentiles = [15.4, 16.8, 17.6, 18.3, 19.0, 19.8, 20.7, 21.7, 23.1, 27.1]
    for i in range(len(foodpair_percentiles)):
        if score < foodpair_percentiles[i]:
            return i
    return 9

# surprise_percentiles = [0.412, 0.490, 0.512, 0.528, 0.545, 0.565, 0.580, 0.601, 0.624, 0.654, 0.748]
# foodpair_percentiles = [11.0, 15.4, 16.8, 17.6, 18.3, 19.0, 19.8, 20.7, 21.7, 23.1, 27.1]
def one_recipe(model, surprise, foodpair, people, inspiration, model_sel, meat_option, nuts_option, dairy_option):
    if model_sel == 0:
        if not wordcheck(model,inspiration):
            raise Exception("Error: " + inspiration + ' was not found in the model. Please try again.')
    surprise_rating = int((surprise-1)/10)
    foodpair_rating = int((foodpair-1)/10)
    multiplier = people / 2
    new_ingredients, key_ingredients = cook(inspiration, model, model_sel)
    #selected_ingredients = select(new_ingredients)
    list_of_selected_ingredients = select_all_possible_pair(new_ingredients, key_ingredients)
    count = len(list_of_selected_ingredients)
    random_location = randint(0, count-1)
    location = random_location
    # loop through all recipes starting at random location
    while True:
        selected_ingredients = list_of_selected_ingredients[location]
        initial_ingredients = generate_recipe(dairy_option)
        ingredient_strings = []
        for ingredient in selected_ingredients:
            ingredient_strings.extend(ingredient.get_name().split())
        score = surprise_score(ingredient_strings)
        p_score = pair_score(initial_ingredients + selected_ingredients)

        recipe = recipeClass()
        recipe.add_category(meat_option, nuts_option, dairy_option)
        for i in initial_ingredients:
            i.multiply(multiplier)
            recipe.add_ingredient(i)
        for i in selected_ingredients:
            i.multiply(multiplier)
            recipe.add_ingredient(i)
        recipe.update_amounts()

        if surprise_score_to_percentile(score) == surprise_rating and foodpair_score_to_percentile(p_score) >= foodpair_rating:
            print("")
            print("///////////////////////////////////////")
            print(inspiration + " waffle recipe")
            print("///////////////////////////////////////")
            print("Surprise score:" + str(round(score * 100, 1)))
            print("Food Pair score:" + str(round(p_score, 1)))
            mni = get_micronutrient_info(R=recipe)
            print('Contained micronutrients: '+', '.join(mni))
            isWaffle = 'Yes' if waffleness_estimator(R=recipe) else 'No'
            print('Is this a waffle recipe? {}.'.format(isWaffle))
            print("---------------------------------------")
            recipe.print_ingredients()
            print('')
            print(recipe.print_recipe())
            return recipe
        location = location + 1
        location = location % count
        if(location == random_location):
            print("No recipe found for specified inputs.")
            break

def create(model, people, model_sel, meat_option, nuts_option, dairy_option):
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    surprise_percentiles = [0.412, 0.490, 0.512, 0.528, 0.545, 0.565, 0.580, 0.601, 0.624, 0.654, 0.748]
    foodpair_percentiles = [11.0, 15.4, 16.8, 17.6, 18.3, 19.0, 19.8, 20.7, 21.7, 23.1, 27.1]
    surprise_rating = int(surprise/10)
    foodpair_rating = int(foodpair/10)
    multiplier = people / 3

    while True:
        print("What kinds of waffle would you like to eat?")
        while True:
            inspiration = input(">> ")
            if inspiration.lower() == "no":
                print("OK, see you!")
                sys.exit()
            if model_sel == 0:
                if wordcheck(model,inspiration):
                    break
            else:
                break
        new_ingredients, key_ingredients = cook(inspiration, model,model_sel)
        #selected_ingredients = select(new_ingredients)
        list_of_selected_ingredients = select_all_possible_pair(new_ingredients, key_ingredients)
        recipe_list = []
        surprise_list = []
        pair_list = []
        waffleness_list = []
        micronutrients_list = []
        for selected_ingredients in list_of_selected_ingredients:
            initial_ingredients = generate_recipe(dairy_option)
            ingredient_strings = []
            for ingredient in selected_ingredients:
                ingredient_strings.extend(ingredient.get_name().split())
            score = surprise_score(ingredient_strings)
            p_score = pair_score(initial_ingredients + selected_ingredients)

            recipe = recipeClass()
            recipe.add_category(meat_option, nuts_option, dairy_option)

            for i in initial_ingredients:
                i.multiply(multiplier)
                recipe.add_ingredient(i)
            for i in selected_ingredients:
                i.multiply(multiplier)
                recipe.add_ingredient(i)
            recipe.update_amounts()

            mni = get_micronutrient_info(R=recipe)
            isWaffle = 'Yes' if waffleness_estimator(R=recipe) else 'No'

            recipe_list.append(copy.copy(recipe))
            pair_list.append(copy.copy(p_score))
            surprise_list.append(copy.copy(score))
            waffleness_list.append(copy.copy(isWaffle))
            micronutrients_list.append(copy.copy(mni))

            del initial_ingredients
            del recipe

        max_num = len(recipe_list)
        mode_num = len(recipe_list) // 2
        pair_index = sorted(range(len(pair_list)), key=lambda k: pair_list[k])
        surprise_index = sorted(range(len(surprise_list)), key=lambda k: surprise_list[k])
        out_index = [0,1,2,3,4, mode_num - 2, mode_num - 1, mode_num, mode_num + 1, mode_num + 2,max_num-5,max_num-4,max_num-3,max_num-2,max_num-1]
        for i in out_index:
            temp_index = surprise_index[i]
            print("")
            print("///////////////////////////////////////")
            print(inspiration + " waffle recipe : SUPERISE RANK " + str(max_num - i))
            print("///////////////////////////////////////")
            print("Surprise score:" + str(round(surprise_list[temp_index] * 100, 1)))
            print("Food Pair score:" + str(round(pair_index[temp_index], 1)))
            print('Contained micronutrients: '+', '.join(micronutrients_list[temp_index]))
            print('Is this a waffle recipe? {}.'.format(waffleness_list[temp_index]))
            print("---------------------------------------")
            recipe_list[temp_index].print_ingredients()
            print('')
            #print(recipe.print_recipe())
            print("")
        for i in out_index:
            temp_index = pair_index[i]
            print("")
            print("///////////////////////////////////////")
            print(inspiration + " waffle recipe : FOOD PAIR RANK " + str(max_num - i))
            print("///////////////////////////////////////")
            print("Surprise score:" + str(round(surprise_list[temp_index] * 100, 1)))
            print("Food Pair score:" + str(round(pair_index[temp_index], 1)))
            print('Contained micronutrients: '+', '.join(micronutrients_list[temp_index]))
            print('Is this a waffle recipe? {}.'.format(waffleness_list[temp_index]))
            print("---------------------------------------")
            recipe_list[temp_index].print_ingredients()
            print('')

if __name__ == '__main__':
    # # Uncomment this section to run without the GUI
    # # model = gensim.models.KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', binary=True)
    model = gensim.models.KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', limit=1600000, binary=True)
    surprise = 50
    foodpair = 30
    people = 3
    model_sel = 1
    meat_option = True
    nuts_option = True
    dairy_option = True
    create(model, people, model_sel, meat_option, nuts_option, dairy_option)
