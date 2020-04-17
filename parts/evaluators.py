import json

import joblib
import numpy as np

from parts.simple import recipeClass


# load the model from disk
waffleness_pca = joblib.load('data/waffleness.model')


def get_waffleness(R: recipeClass, model=waffleness_pca):

    selected_ingredients = ('flour', 'water', 'baking', 'butter',
                            'egg', 'milk', 'oil', 'salt', 'sugar', 'vanilla')
    n_selected_ingredients = len(selected_ingredients)

    def _name_mapping(name: str):
        for i in selected_ingredients:
            if i in name.lower():
                return i
        return "unselected"

    ingredients = R.dry + R.wet + R.mix + R.toppings

    features = np.zeros(n_selected_ingredients, dtype=np.float)

    for ingr in R.flour:
        _name = 'flour'
        _amount = ingr.amount
        idx = selected_ingredients.index(_name)
        features[idx] += _amount

    for ingr in ingredients:

        _name = _name_mapping(ingr.name)
        _amount = ingr.amount
        if _name == 'egg':
            _amount /= 250

        if _name != "unselected":
            idx = selected_ingredients.index(_name)
            features[idx] += _amount

    if features[0] == 0:
        return -1
    features /= features[0]

    X = np.expand_dims(features, axis=0)
    score = model.score(X)

    return score


def waffleness_estimator(R: recipeClass, threshold=10):
    score = get_waffleness(R)
    return True if score > threshold else False

with open('data/micronutrients.json') as json_file:
    micronutrient_info = json.load(json_file)


def get_micronutrient_info(R: recipeClass):

    mni = []

    ingredients = R.flour + R.dry + R.wet + R.mix + R.toppings
    for k, v in micronutrient_info.items():
        sign = False
        for ingr in ingredients:
            if sign:
                break
            _name = ingr.name.lower()
            for i in v:
                if _name in i.lower():
                    sign = True
                    mni.append(k)
                    break

    if len(mni) == 0:
        return ['N/A']

    return mni
