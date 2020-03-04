import requests
import re
from bs4 import BeautifulSoup

def pair(ingredient):
    page = requests.get("http://www.ingredientpairings.com/?i=" + ingredient)
    soup = BeautifulSoup(page.content, 'html.parser')

    matches = []
    knowledge = soup.find(class_='main')
    ingredients = knowledge.findChild().find_all('a')
    for i in ingredients:
        matches.append(i.text)
    return(matches)

# print(pair("beef"))

