from gensim.models import Word2Vec
import math

# Here we will load and use our custom word2vec model.
def surprise_score(new_ingredients):
    scores = []
    model = Word2Vec.load("data/food.model")
    for i in range(len(new_ingredients)):
        for i2 in range(len(new_ingredients)):
            if i < i2:
                try:
                    scores.append(model.similarity(new_ingredients[i], new_ingredients[i2]))
                except KeyError as e:
                    print(e.args[0])
                    pass
    mean = sum(scores) / len(scores) 
    score = 1/(1+pow(math.e, -5 * mean))
    return score

# new_ingredients = ["ginger", "beans", "orange", "candy", "strawberry"]
# print(surprise_score(new_ingredients))

