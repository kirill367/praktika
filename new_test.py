import pandas as pd
#���
df = pd.read_csv('zoo.csv', delimiter=',')
print(df)
counter = 0
for i in df.uniq_id[:]:
    for j in i:
        if j == '�':
            df.uniq_id[counter] = str(df.uniq_id[counter]).replace('�', '0')
    counter += 1
print(df)