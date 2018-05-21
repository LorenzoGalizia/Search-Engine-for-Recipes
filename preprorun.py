import pandas as pd
import preprolib as pplib

file = open('recipes.csv', errors='replace')
dataframe = pd.read_csv(file)

dataframe = dataframe[dataframe['name'] != 'name']# Removes the rows that contains the keys. After that We have as index even numbers.
dataframe.fillna('None', inplace=True)
dataframe = dataframe[dataframe['name'] != 'None']
dataframe = dataframe.reset_index(drop=True)
dataframe.to_csv('recipes.csv', index=False)

dataframe = pplib.pre_basic(dataframe)
dataframe = pplib.stopword(dataframe)
dataframe = pplib.stemming(dataframe)
dataframe = pplib.replace_char(dataframe)
dataframe = pplib.normalization(dataframe)

dataframe.to_csv('recstem.csv', index=False)
file.close()

invd = dataframe.T

inv_index = pplib.inverted_index(invd)
pplib.index_to_csv(inv_index)
