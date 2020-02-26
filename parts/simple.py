import json
import random
import numpy as np
from pint import UnitRegistry
from fractions import Fraction

class recipeClass:
    def __init__(self):
        self.flour = []
        self.dry = []
        self.wet = []
        self.mix = []
        self.toppings = []
        self.flour_options = ['Flour','Mixes']
        self.dry_options = ['Spices', 'Dry', 'Salt and Pepper', 'Corn and Wheat', 'Chips, Crumbs, and Grits', 'Rice', 'Other Grain', 'Pasta', 'Seeds']
        self.wet_options = ['Creams and Eggs', 'Wet', 'Sauces', 'Liquids', 'Grease and Fat', 'Nut butter']
        self.mix_options = ['Meats', 'Fruits', 'Vegetables', 'Cheese', 'Mix', 'Nut', 'Bread', 'Weird Spices']
        self.toppings_options = []
    def add_ingredient(self, ingredient):
        for i in range(len(ingredient.get_class())):
            i_class = ingredient.get_class()[i]
            if i_class in self.flour_options:
                self.flour.append(ingredient)
            elif i_class in self.dry_options:
                self.dry.append(ingredient)
            elif i_class in self.wet_options:
                self.wet.append(ingredient)
            elif i_class in self.mix_options:
                self.mix.append(ingredient)
            elif i_class in self.toppings_options:
                self.toppings.append(ingredient)
            # print(i_class)
    def print_recipe(self):
        dry = "In a large bowl mix the " + ', '.join([i.get_name() for i in self.flour]) + ', ' + ', '.join([self.dry[i].get_name() for i in range(len(self.dry) - 1)]) + ', and ' + self.dry[-1].get_name() + '.\n'
        wet = "In another bowl, mix the " + ', '.join([self.wet[i].get_name() for i in range(len(self.wet) - 1)]) + ', and ' + self.wet[-1].get_name() + '.\n'
        mix = "Pour the wet ingredients into the flour mixture and mix until smooth.\n"
        if(self.mix):
            if len(self.mix) > 1:
                mix = mix + "Mix in the " + ', '.join([self.mix[i].get_name() for i in range(len(self.mix) - 1)]) + ', and ' + self.mix[-1].get_name() + '.\n'
            else:
                mix = mix + "Mix in the " + self.mix[0].get_name() + '.\n'
        cook = "Pour the batter into the waffle iron and bake until toasty.\n"
        toppings = ""
        if(self.toppings):
            if len(self.toppings) > 1:
                toppings = "Serve with " + ', '.join([self.toppings[i].get_name() for i in range(len(self.toppings) - 1)]) + ', and ' + self.toppings[-1].get_name() + '.\n'
            else:
                toppings = "Serve with " +  self.toppings[0].get_name() + '.\n'
        toppings = toppings + "Enjoy!\n"
        return ''.join([dry,wet,mix,cook,toppings])
class ingredientClass:
    def __init__(self, ingredient_object = None):
        if ingredient_object:
            ps = ingredient_object["probabilities"]
            probabilities =[float(i) for i in ps]
            ingr = np.random.choice(len(ps), 1, p=probabilities)[0]
            self.name = ingredient_object["options"][ingr]
            self.amount = ingredient_object["values"][ingr]
            self.classes = ingredient_object["class"][ingr]
    def define_me(self, n, a, c):
        self.name = n
        self.amount = a
        self.classes = c
    def fraction_time(self, frac):
        mixed = ""
        m = frac.numerator // frac.denominator
        if m > 0:
            mixed = str(m) + " "
            new_frac = Fraction(frac.numerator%frac.denominator, frac.denominator)
            if new_frac == 0:
                frac = ""
            else:
                frac = str(new_frac) + " "
        else:
            frac = str(frac) + " "
        return str(mixed) + str(frac)
    def value_to_measurement(self):
        if self.name == 'egg':
            return str(round(self.amount / 250))
        elif self.amount >= 250:    
            measurement = self.amount / 1000 * self.ureg.cup
            frac = Fraction(int(round(4*measurement.magnitude)),4)
            return self.fraction_time(frac) + str(measurement.units)
        elif self.amount >= 62:
            measurement = self.amount / 62.5 * self.ureg.tablespoon
            frac = Fraction(int(round(2*measurement.magnitude)),2)
            return self.fraction_time(frac) + str(measurement.units)
        elif self.amount >= 20:
            measurement = self.amount / 20.8 * self.ureg.teaspoon
            frac = Fraction(int(round(2*measurement.magnitude)),2)
            return self.fraction_time(frac) + str(measurement.units)
        else:
            measurement = self.amount / 20.8 * self.ureg.teaspoon
            frac = Fraction(int(round(4*measurement.magnitude)),4)
            return self.fraction_time(frac) + str(measurement.units)
    def multiply(self, percentage):
        self.amount = self.amount * percentage
    def get_class(self):
        return self.classes
    def get_name(self):
        return self.name
    def __str__(self):
        measurement = self.value_to_measurement()
        return measurement + " " + str(self.name)
    @classmethod
    def initialize_unit_registry(cls, ureg):
        cls.ureg = ureg

def generate_recipe():
    # multiplier = cups / 2.3
    f = open('data/basics.json', 'r')
    data = json.load(f)
    ureg = UnitRegistry()
    ingredientClass.initialize_unit_registry(ureg)
    basics = data['basics']
    ingredients = []
    for basic in basics:
        ingredients.append(ingredientClass(basic))
    return ingredients
    # for ingredient in ingredients:
    #     ingredient.multiply(multiplier)
    #     print(ingredient)
    
generate_recipe()
# battersize = 4
# mixin_to_dry = 1
# wet_to_dry = 1.2
