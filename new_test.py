import numpy as np
import pandas as pd
import time
start_time = time.time()

def main():
    pd.set_option("display.max_rows", 24000)
    pd.set_option('display.width', 10000)

    df = pd.read_csv('sensors_sample_data.csv', delimiter=';')

# 9105 - 16.���  были подобные записи в стобце velocity, заменяем на нули
    num_of_strange_sign = 0
    lines_with_strange_sign = []  # индексы строк с неопознанными знаками
    for i in df.velocity:
        for j in i:
            if j == '�':
                df.velocity[num_of_strange_sign] = str(df.velocity[num_of_strange_sign]).replace('�', '0')
                lines_with_strange_sign.append(num_of_strange_sign)
                break
        num_of_strange_sign += 1

    dens_df = pd.DataFrame({'intensity': df.intensity, 'velocity': df.velocity}).astype('float64')

    for i in lines_with_strange_sign:
        dens_df.velocity[i] = int(dens_df['velocity'].mean())

    dens_df['density'] = dens_df.intensity / dens_df.velocity
    dens_df = dens_df.replace([-np.inf, np.inf], [0, 0])

    dens_df['time'] = df.range_end
    dens_df['time'] = pd.to_datetime(dens_df.time)
    #dens_df.sort_values(by=['time'], inplace=True, ascending=True)

    dens_df['prev_value'] = df['velocity'].shift()

    print(dens_df.head(100))
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
