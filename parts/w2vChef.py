def ingredientIdeas(model, positives, negatives):
    thoughts = model.most_similar(positive=positives, negative=negatives)
    return thoughts

def wordcheck(model, word):
    try:
        model[word]
        return True
    except KeyError as e:
        print(e.args[0])
        return False