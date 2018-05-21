from nltk.corpus import stopwords
from nltk.stem.porter import *
import unicodedata as ucd
import collections
import csv


### Return all the info in lowercase and replace all the non-alphanumeric digit with a space. ###
def pre_basic(dataframe):
    dataframe['name'] = dataframe['name'].str.lower().str.replace('[^0-9a-z]+', ' ').str.split()
    dataframe['recipeInstructions'] = dataframe['recipeInstructions'].str.lower().str.replace('[^0-9a-z]+', ' ').str.split()
    dataframe['ingredients'] = dataframe['ingredients'].str.lower().str.replace('[^0-9a-z]+', ' ').str.split()
    dataframe['recipeYield'] = dataframe['recipeYield'].str.lower().str.replace('[^0-9a-z]+', ' ').str.split()
    return dataframe

### Removes from the dataframe all the stopwords. ###
def stopword(dataframe):
    stop = stopwords.words('english')
    dataframe['name'] = dataframe['name'].apply(lambda word: [char for char in word if char not in stop])
    dataframe['ingredients'] = dataframe['ingredients'].apply(lambda word: [char for char in word if char not in stop])
    dataframe['recipeInstructions'] = dataframe['recipeInstructions'].apply(lambda word: [char for char in word if char not in stop])
    dataframe['recipeYield'] = dataframe['recipeYield'].apply(lambda word: [char for char in word if char not in stop])
    return dataframe

### Stems all the datframe's word. ###
def stemming(dataframe):
    stemmer = PorterStemmer()
    dataframe['name'] = dataframe['name'].apply(lambda x: [stemmer.stem(y) for y in x])
    dataframe['ingredients'] = dataframe['ingredients'].apply(lambda x: [stemmer.stem(y) for y in x])
    dataframe['recipeInstructions'] = dataframe['recipeInstructions'].apply(lambda x: [stemmer.stem(y) for y in x])
    dataframe['recipeYield'] = dataframe['recipeYield'].apply(lambda x: [stemmer.stem(y) for y in x])
    return dataframe

### Joins the words and creates the strings. ###
def replace_char(dataframe):
    dataframe['name'] = dataframe['name'].apply(' '.join)
    dataframe['recipeInstructions'] = dataframe['recipeInstructions'].apply(' '.join)
    dataframe['ingredients'] = dataframe['ingredients'].apply(' '.join)
    dataframe['recipeYield'] = dataframe['recipeYield'].apply(' '.join)
    return dataframe

### Normalize all the dataframe's strings. ###
def normalization(dataframe):
    dataframe['name'] = dataframe['name'].map(lambda x: ucd.normalize('NFKD', x))
    dataframe['author'] = dataframe['author'].map(lambda x: ucd.normalize('NFKD', x))
    dataframe['Dietary'] = dataframe['Dietary'].map(lambda x: ucd.normalize('NFKD', x))
    dataframe['prepTime'] = dataframe['prepTime'].map(lambda x: ucd.normalize('NFKD', x))
    dataframe['cookTime'] = dataframe['cookTime'].map(lambda x: ucd.normalize('NFKD', x))
    dataframe['recipeInstructions'] = dataframe['recipeInstructions'].map(lambda x: ucd.normalize('NFKD', x))
    dataframe['ingredients'] = dataframe['ingredients'].map(lambda x: ucd.normalize('NFKD', x))
    dataframe['recipeYield'] = dataframe['recipeYield'].map(lambda x: ucd.normalize('NFKD', x))
    return dataframe

### Create the inverted index as a dictionary that has all the words in the dataframe as keys
### and as values for each keys the list of document where is present the words ###
def inverted_index(dataframe):
    ndf = {}
    s = set()
    inv_index = collections.defaultdict(list)
    for i in dataframe.keys():
        str = ''
        for j in dataframe[i].values:
            str += j + ' '
        ndf[i] = str.split(' ')
    for i in ndf.values():
        for j in i:
            if j != '':
                s.add(j)
    for i in s:
        for j in ndf.keys():
            if i in ndf[j]:
                inv_index[i].append(j)
    return inv_index


### Save the inverted index to a csv ###
def index_to_csv(dict):
    inverted_ind = csv.writer(open('inverted.csv', 'w', newline='', encoding='utf-8'))
    inverted_ind.writerow(['doc'])
    with open('inverted.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        for k, v in dict.items():
            writer.writerow([k, v])
    return
