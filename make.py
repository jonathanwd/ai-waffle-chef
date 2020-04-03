from parts.simple import generate_recipe, ingredientClass, recipeClass
from parts.classify import classify
from parts.w2vChef import ingredientIdeas, wordcheck
from parts.amount import get_amount
from parts.parings import pair
from parts.evaluators import waffleness_estimator
from parts.surprise import surprise_score
from parts.food_pair_probability import pair_score
import gensim
import json
import sys
import random
import logging
import itertools
import copy

DEBUG = False

def cook(inspiration, model):
    new_ingredients = []
    print("You want me to make a " + inspiration + " waffle?")
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
    possibilities = []
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
    possibilities = set(possibilities)
    if DEBUG:print(possibilities)
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
                if DEBUG:print(possibility)
                new_ingredient = ingredientClass()
                new_ingredient.define_me(possibility, a, classed)
                new_ingredients.append(new_ingredient)
        else:
            pass
            #print("no")
    return new_ingredients

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

def select_all_possible_pair(new_ingredients):
    result = []
    upper_limit = min(6, len(new_ingredients))
    for n in range(5,upper_limit):
        for conb in itertools.combinations(new_ingredients, n):
            temp_list = []
            for c in conb:
                temp = copy.copy(c)
                temp_list.append(temp)
            result.append(temp_list)
            del temp_list
    print("Number of inspired additional ingredient:        " + str(len(new_ingredients)))
    print("Number of possible combination of recipes:       " + str(len(result)))
    return result

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# model = gensim.models.KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', binary=True)
model = gensim.models.KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', limit=1600000, binary=True)
# f = open('data/layer1.json', 'r')
# all_recipes = f.read().splitlines()
# f.close()

surprise_rating = 9 
foodpair_rating = 5
surprise_percentiles = [0.412, 0.490, 0.512, 0.528, 0.545, 0.565, 0.580, 0.601, 0.624, 0.654, 0.748]
foodpair_percentiles = [11.0, 15.4, 16.8, 17.6, 18.3, 19.0, 19.8, 20.7, 21.7, 23.1, 27.1]
cups = 4
multiplier = cups / 2.3
while True:
    print("What kinds of waffle would you like to eat?")
    while True:
        inspiration = input(">> ")
        if inspiration.lower() == "no":
            print("OK, see you!")
            sys.exit()
        if wordcheck(model,inspiration):
            break
    new_ingredients = cook(inspiration, model)
    #selected_ingredients = select(new_ingredients)
    list_of_selected_ingredients = select_all_possible_pair(new_ingredients)
    for selected_ingredients in list_of_selected_ingredients:
        initial_ingredients = generate_recipe()
        ingredient_strings = []
        for ingredient in selected_ingredients:
            ingredient_strings.extend(ingredient.get_name().split())
        score = surprise_score(ingredient_strings)
        p_score = pair_score(initial_ingredients + selected_ingredients)

        recipe = recipeClass()
        for i in initial_ingredients:
            i.multiply(multiplier)
            recipe.add_ingredient(i)
        for i in selected_ingredients:
            i.multiply(multiplier)
            recipe.add_ingredient(i)
        recipe.update_amounts()

        if(score > surprise_percentiles[surprise_rating] and p_score > foodpair_percentiles[foodpair_rating]):
            print("")
            print("///////////////////////////////////////")
            print(inspiration + " waffle recipe")
            print("///////////////////////////////////////")
            print("Surprise score:" + str(round(score * 100, 1)))
            print("Food Pair score:" + str(round(p_score, 1)))
            isWaffle = 'Yes' if waffleness_estimator(R=recipe) else 'No'
            print('Is this a waffle recipe? {}.'.format(isWaffle))
            print("---------------------------------------")
            recipe.print_ingredients()
            print('')
            print(recipe.print_recipe())
            del initial_ingredients
            del recipe
