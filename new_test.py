import pandas as pd
import numpy as np

df = pd.read_csv('zoo.csv', delimiter=',')
counter = 0
my_list = []
for i in df.animal:
    if df.animal[counter] == 'zebra' and df.uniq_id[counter] == 1011:
        my_list.append(counter)
    counter += 1
print(my_list)

