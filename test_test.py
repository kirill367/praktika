import pandas as pd
import numpy as np



pd.set_option("display.max_rows", 24000)
df = pd.read_csv('sensors_sample_data.csv', delimiter=';')

# 9105 - 16.���  были подобные записи в стобце velocity, заменяем на нули
numOfSrtangeSign = 0
lineswithstrangesign = []  # индексы строк с неопознанными знаками
for i in df.velocity:
    for j in i:
        if j == '�':
            df.velocity[numOfSrtangeSign] = str(df.velocity[numOfSrtangeSign]).replace('�', '0')
            lineswithstrangesign.append(numOfSrtangeSign)
            break
    numOfSrtangeSign += 1


# создаем новый датафрейм с столбцом плотности потока
dens_df = pd.DataFrame({'intensity':df.intensity, 'velocity': df.velocity}).astype('float64')

# заменяем значения в тех строках где раньше были � на среднеезначение всего столбца
for i in lineswithstrangesign:
    dens_df.velocity[i] = int(dens_df['velocity'].mean())
# создание резервного датафрейма, не сортированного по времени (на всякий случай)
unsorted_dens_df = dens_df.copy()
#  добавляем столбцы плотности и времени, сортируя по времени
dens_df['density'] = dens_df.intensity / dens_df.velocity
dens_df['time'] = df.range_end
dens_df['time'] = pd.to_datetime(dens_df.time)
dens_df.sort_values(by=['time'], inplace=True, ascending=True)






