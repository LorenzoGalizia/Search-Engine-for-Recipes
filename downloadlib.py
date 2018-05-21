import requests
from bs4 import BeautifulSoup
import time
import csv


### Saves all the links that start with a particular path ,from the input 'url' in a file .txt ###
def get_links(url):
    cnt = requests.get(url)
    soup = BeautifulSoup(cnt.text, 'lxml')
    f = open('recipes.txt', 'w')
    for link in soup.find_all('loc'):
        a = link.text
        if a.startswith('http://www.bbc.co.uk/food/recipes/'):
            f.write(a + '\n')
    f.close()
    return

### Extracts particular information. Take in input the type of the tag and the BeautifulSoup file ###
def ext_info(soup, type):
    info = []
    for tag in soup.find_all(itemprop=type):
        cleantag = tag.text
        if cleantag == '\n\n':
            pass
        else:
            cleantag = cleantag.replace('\n', '')
            cleantag = cleantag.replace('\r', '')
            info.append(cleantag)
    if soup.find_all(href=type):
        info.append('Vegetarian')
    return info

### Extracts the simplest information from the itemprop tags. It takes in input the BeutifulSoup file and the type of the tag ###
def ext_basicinfo(soup, type):
    result = ""
    for tag in soup.find_all(itemprop=type):
        result = tag.contents[0]
    return result

### Reads the file .txt with all the urls and stores all the recipes' info into a dictionary. Between each download it waits 1sec ###
def read_urls(txt):
    recipes = {}
    file = open(txt, 'r')
    for url in file:
        for attempt in range(1, 4):
            r_url = requests.get(url)
        try:
            dict = {}
            recipe = BeautifulSoup(r_url.text, 'lxml')
            dict['name'] = recipe.title.contents[0][21:]
            dict['prepTime'] = ext_basicinfo(recipe, 'prepTime')
            dict['cookTime'] = ext_basicinfo(recipe, 'cookTime')
            dict['author'] = ext_basicinfo(recipe, 'author')
            dict['recipeYield'] = ext_basicinfo(recipe, 'recipeYield')
            dict['ingredients'] = ext_info(recipe, 'ingredients')
            dict['recipeInstructions'] = ext_info(recipe, 'recipeInstructions')
            if (ext_info(recipe, '/food/diets/vegetarian') == ['Vegetarian']):
                dict['Dietary'] = 'Vegetarian'
            else:
                dict['Dietary'] = 'None'
            recipes[dict['name']] = dict
        except requests.RequestException:
            time.sleep(attempt * 10)

    return recipes

### Creates a file CSV from the recipes's dictionary. ###
def dict_to_csv(dict):
    keys = list(dict.keys())
    columns = ['name', 'author','Dietary','prepTime','cookTime','recipeInstructions', 'ingredients', 'recipeYield']
    with open('recipes.csv', 'w', encoding = 'utf-8') as f:
        for i in keys:
            dic = dict[i]
            d_writer = csv.DictWriter(f, fieldnames=columns, delimiter = ',')
            d_writer.writeheader()
            data = {key: value for key, value in dic.items() if key in columns}
            d_writer.writerow(data)
    return
