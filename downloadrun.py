import downloadlib as dlib

dlib.get_links("https://www.bbc.co.uk/food/sitemap.xml")

dict_rec = dlib.read_urls('recipes.txt')

dlib.dict_to_csv(dict_rec)



