import json
from quantulum3 import parser
from pint import UnitRegistry
import statistics

def amount(reference_ingredient, new_ingredient, data):
    filtered = []
    values = []
    ureg = UnitRegistry()
    for line in data:
        try:
            if reference_ingredient in line and new_ingredient in line:
                reference_q = []
                test_q = []
                recipe = json.loads(line[:-1]) # Don't include the ending comma
                ingredients = recipe["ingredients"]
                for ingredient in ingredients:
                    text = ingredient["text"]
                    if reference_ingredient in text:
                        reference_q = parser.parse(text)
                    if new_ingredient in text:
                        test_q = parser.parse(text)
                if reference_q and test_q:
                    fq = str(reference_q[0].value) + " " + str(reference_q[0].unit)
                    tq = str(test_q[0].value) + " " + str(test_q[0].unit)
                    reference_volume = ureg.parse_expression(fq)
                    reference_volume = reference_volume.to(ureg.cup)
                    if reference_volume.magnitude < 1:
                        pass
                    test_volume = ureg.parse_expression(tq)
                    test_volume = test_volume.to(ureg.cup)
                    score = test_volume.magnitude/reference_volume.magnitude * 1000
                    score = round(score)
                    values.append(score)
        except:
            pass
    if values:
        return round(statistics.median(values))
    else:
        return -1

def list_builder(json_input, list_b):
    for k, v in json_input.items():
        if isinstance(v, list):
            list_b.extend(v)
        else:
            list_builder(v, list_b)

def add_amounts(reference_ingredient, all_recipes):
    f = open('data/classed.json', 'r')
    classed_data = json.load(f)
    f.close()
    ingredients = []
    list_builder(classed_data, ingredients)
    f = open('data/amount.txt', 'r')
    amounts = f.read().splitlines()
    f.close()
    f=open("data/amount.txt", "a")
    for ingredient in ingredients:
        not_found = True
        for am in amounts:
            if ingredient in am:
                # i = amount.split()
                # print(i[0])
                # print(i[1])
                not_found = False
        if not_found:
            print("Calculating amount for " + ingredient + "...")
            a = amount(reference_ingredient, ingredient, all_recipes)
            print(a)
            f.write(ingredient)
            f.write(" ")
            f.write(str(a))
            f.write("\n")
    f.close()

def get_amount(item):
    f = open('data/amount.txt', 'r')
    lines = f.readlines()
    for line in lines:
        if item in line:
            split = line.rsplit(' ', 1)
            if split[0] == item:
                return split[1]
    return -1

f = open('data/layer1.json', 'r')
all_recipies = f.read().splitlines()
f.close()
add_amounts('flour', all_recipies)