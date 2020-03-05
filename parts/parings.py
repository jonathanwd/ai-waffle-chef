import requests
import re
from bs4 import BeautifulSoup

def pair(ingredient):
    page = requests.get("http://www.ingredientpairings.com/?i=" + ingredient)
    soup = BeautifulSoup(page.content, 'html.parser')

    matches = {}
    tier_one = []
    tier_two = []
    tier_three = []
    tier_four = []

    knowledge = soup.find(class_='main')
    ingredients = knowledge.findChild().find_all('a')
    for i in ingredients:
        if "<b>" in str(i):
            if(i.text[0].isupper()):
                tier_one.append(i.text)
            else:
                tier_two.append(i.text)
        elif "<i>" in str(i):
            tier_four.append(i.text)
        else:
            tier_three.append(i.text)
    matches["one"] = tier_one
    matches["two"] = tier_two
    matches["three"] = tier_three
    matches["four"] = tier_four
    return matches

# print(pair("cornmeal"))

