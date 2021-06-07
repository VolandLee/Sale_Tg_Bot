# -*- coding: cp1251 -*-
import pickle
import copy

with open('catalog/Wildberries/brands.pickle', 'rb') as f:
    data = pickle.load(f)

data1 = {}
for i in data:

    data1[i.replace("Страница ", "")] = copy.deepcopy(data[i])
print(data1)
with open('catalog/Wildberries/brands.pickle', 'wb') as f:
    pickle.dump(data1, f)





