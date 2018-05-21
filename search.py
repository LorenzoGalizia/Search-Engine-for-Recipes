import pandas as pd
import searchlib as slib
import numpy as np

f = open('inverted.csv', errors='replace')
file = pd.read_csv(f)
f.close()
recip = open('recipes.csv', errors='replace')
df = pd.read_csv(recip)
recip.close()
stem = open('recstem.csv', errors='replace')
dfstem = pd.read_csv(stem)
stem.close()

tr_df = df.T
quest = 'y'
while quest == 'y':
    query = slib.answer_to_user()

    list_all_query = slib.preprocessing_query(query)
    list_q = [i for i in list_all_query if i in file.index]

    if list_q:
        fr_query = np.ones((len(list_q)))

        docs = slib.intersect(list_q, file)

        df['recipeInstructions'] = df['recipeInstructions'].str.replace('[^0-9a-z]+', ' ')
        df['ingredients'] = df['ingredients'].str.replace('[^0-9a-z]+', ' ')

        tr_dfstem = dfstem.T

        ndf = slib.create_ndf(tr_dfstem)

        freq = slib.score(list_q, ndf, file, df, dfstem)

        vec = slib.take_freqs(freq, docs, list_q)

        fr_int = slib.vec_freq(vec, docs, list_q)

        cos_simil = slib.cosine_similarity(fr_int, docs, fr_query)

        slib.output(cos_simil, tr_df)
    else:
        print('Not results found!')
    quest = input('Would you like to make another search? (y/n) ')
