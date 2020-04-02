import json
import numpy as np

def pair_score(ingredients):
    f = open('data/amount.txt', 'r')
    lines2 = f.readlines()
    f.close()
    food_list = []
    for line in lines2:
        l_list = line.rsplit(" ",1)
        food_list.append(l_list[0])

    correlation_matrix = np.load('data/food_pair_matrix.npy')
    score = 0
    for i in ingredients:
        for i2 in ingredients:
            score += correlation_matrix[food_list.index(i.name), food_list.index(i2.name)]

    return score


