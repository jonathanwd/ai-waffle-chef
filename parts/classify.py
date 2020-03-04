import json
from io import StringIO
from contextlib import redirect_stdout

def class_it(json_input, ingredient, prepath = ()):
    to_return = ""
    for k, v in json_input.items():
        path = prepath + (k,)
        if isinstance(v, list):
            for item in v:
                if item == ingredient:
                    to_return = str(path)
                    print(to_return)
        else:
            class_it(v, ingredient, path)

def classify(ingredient):
    f = open('data/classed.json', 'r')
    data = json.load(f)
    f.close()
    to_return = ""
    with StringIO() as buf, redirect_stdout(buf):
        class_it(data, ingredient)
        to_return = buf.getvalue()
        to_return = to_return.replace('(', '')
        to_return = to_return.replace(')', '')
        to_return = to_return.replace('\'', '')
        to_return = to_return.replace('\n', '')
        to_return = to_return.split(', ')
        print(to_return)
    return(to_return)
