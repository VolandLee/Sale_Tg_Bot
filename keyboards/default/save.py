import pickle, catalog
with open('catalog/Wildberries/brands.pickle', 'rb') as f:
    catawild = pickle.load(f)
print(catawild)
