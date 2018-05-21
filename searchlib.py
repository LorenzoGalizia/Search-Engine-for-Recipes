from nltk.corpus import stopwords
from nltk.stem.porter import *
import collections
import math
import numpy as np
from scipy import spatial


### we ask to the user what he want search ###
def answer_to_user():
    query = input('Search Recipes: ')
    while len(query) == 0:
        print('Please, insert a new search!')
        query = input('Search Recipes: ')
    return query


### with this function we preprocess the query ###
def preprocessing_query(string):
    string = string.lower()
    stop = stopwords.words('english')
    str = [x for x in string.split() if x not in stop]
    stemmer = PorterStemmer()
    str_stem = [stemmer.stem(y) for y in str]
    return str_stem


### This function return a list in which there are the elements that are in both lists###
def intersection(p1, p2):
    answer = []
    i = 0
    j = 0
    while i in range(len(p1)) and j in range(len(p2)):
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i = i + 1
            j = j + 1
        elif p1[i] < p2[j]:
            i = i + 1
        else:
            j = j + 1
    return answer


### This function return the intersect between two or more lists###
def intersect(list_query, inv_index):
    result = eval(inv_index['doc'][list_query[0]])
    i = 1
    terms = list_query[i:]
    while terms and result:
        result = intersection(result, eval(inv_index['doc'][terms[0]]))
        i += 1
        terms = terms[i:]
    return result


### This function create a dictionary that have as keys the label of the documents
### and as values the words in each document.###
def create_ndf(dataframe):
    ndf = {}
    for i in dataframe.keys():
        st = ''
        for p in dataframe[i].values:
            st += str(p) + ' '
        ndf[i] = st.split(' ')
    return ndf


### This function returns a dictionary that has as keys every word in the user query
### and as values as lists as the number of document where each word is. In every list
### is stored the label of the document and the tf-idf score of the word in the document.###
def score(query, ndf, inv_index, df, dstem):
    in_index = collections.defaultdict(list)
    for i in query:
        for j in ndf.keys():
            c = ndf[j].count(i)  # quante volte appare la parola i nel doc j.
            l = len(ndf[j]) 
            l_doc = len(inv_index['doc'][i]) # in quanti docs appare la parola i.
            if i in ndf[j]:
                idf = math.log(len(df) / l_doc)
                tf = c / l
                in_index[i].append([j, tf * idf])

    return in_index


### This function returns a list in which are stored the list doc&if-idf of each words
### in the query if the doc  is present in the doc intersection. ###
def take_freqs(dict, docs, query):
    vec = []
    for i in query:
        for j in dict[i]:
            if j[0] in docs:
                vec.append(j)
    return vec


### This function return a np.array where are stored all the score of all the words in the query ###
def vec_freq(vec, docs, query):
    q = []
    for i in docs:
        x = np.zeros(len(query))
        k = 0
        for j in vec:
            if j[0] == i:
                x[k] = j[1]
                k += 1
        q.append(x)
    return q


### This function return the cosine similarity between the frequence of the words present in the doc and the
### the vector of ones associeted with the query.###
def cosine_similarity(freq, docs, fr_q):
    search = []
    j = 0
    for i in freq:
        y = 1.0 - spatial.distance.cosine(i, fr_q)
        result = (docs[j], y)
        j += 1
        search.append(result)
    search.sort(key=lambda x: x[1], reverse=True)
    return search


### This function return the results of the user's query. It prints the first 20 recipes found###

def output(search, util):
    j = 0
    if search != []:
        for i in search:
            j += 1
            print(util[i[0]]['name'])
            if j == 20:
                print('And More...')
                break
    else:
        print('No results found!')
    return

