import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
start_time = time.time()
global flag
flag = True

def show_graphs(plot, x, y, name, color):
    plot.scatter(range(len(y)), y, c=color)
    plot.set_title(name)
    plot.set_xlim(0, len(y) - 1)
    plot.set_xticks(range(len(x)))
    plot.set_xticklabels(x)

def hop_to_next_hour(func_df):
    global starting_point, prev_hour, flag
    if flag:
        starting_point = 0
        flag = False

    hop = 0
    prev_hour = func_df.time[starting_point]
    for i in func_df.time[starting_point: ]:
        if i.hour == prev_hour.hour:
            hop += 1
            prev_hour = i.hour
        else:

            return hop
        starting_point += 1


def main():
    pd.set_option("display.max_rows", 24000)
    pd.set_option('display.width', 5000)

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


# создаем новый датафрейм с столбцом плотности потока
    dens_df = pd.DataFrame({'intensity': df.intensity, 'velocity': df.velocity}).astype('float64')

# заменяем значения в тех строках где раньше были � на среднеезначение всего столбца
    for i in lines_with_strange_sign:
        dens_df.velocity[i] = int(dens_df['velocity'].mean())
# создание резервного датафрейма, не сортированного по времени (на всякий случай)
    # unsorted_dens_df = dens_df.copy()
#  добавляем столбцы плотности и времени, сортируя по времени
    dens_df['density'] = dens_df.intensity / dens_df.velocity

    dens_df['time'] = df.range_end
    dens_df['time'] = pd.to_datetime(dens_df.time)
    dens_df.sort_values(by=['time'], inplace=True, ascending=True)


# аномалия 1, когда машины были, но скорость зафиксирована 0
    zero_velocity_rows = dens_df[(dens_df['velocity'] != 0) & (dens_df['intensity'] == 0)].index.tolist()

# аномалия 2, когда машин не было, но скорость зафиксированная не равна 0
    inf_rows = dens_df[dens_df['density'] == np.inf].index.tolist()

# просто так нашел индексы строк где не было ни машин ни скорости
    nan_rows = dens_df[dens_df['density'].isnull()].index.tolist()

#
    avarege_dens = dens_df.density.replace([-np.inf, np.inf, np.nan], 0).mean()
    dens_df = dens_df.replace([-np.inf, np.inf, np.nan], [avarege_dens, avarege_dens, 0])

# создаемм датафрейм с трендами
    trending_df = dens_df.copy().reset_index(drop=True)
    to_another_hour = 100
    trending_df['next_value'] = trending_df['velocity'].shift(- to_another_hour)
# визуализация с помощью графиков плотности по времени и скорости по времени
    time_list = list(dens_df.time[::100])
    plt.figure(figsize=(17, 8))
    show_graphs(plt.subplot(221), time_list, list(dens_df.intensity[::100]), 'Intensity', 'b')
    show_graphs(plt.subplot(222), time_list, list(dens_df.velocity[::100]), 'Velocity', 'r')
    show_graphs(plt.subplot(212), time_list, list(dens_df.density[::100]), 'Density', 'g')
    # plt.show()

    print("Amount of 1st type issues (velocity is 0 while intensity is not 0):", len(zero_velocity_rows),
          ". Indexes are:", zero_velocity_rows)
    print("Amount of 2nd type issues (velocity is not 0 while intensity is 0), dividing by 0 = inf:", len(inf_rows),
          ". Indexes are:", inf_rows)
    print("Amount of NaN (0 velocity and 0 intensity):", len(nan_rows), ". Indexes are:", nan_rows)

    print("--- %s seconds ---" % (time.time() - start_time))
    print(trending_df.head(650))
    print(hop_to_next_hour(trending_df))
    print(hop_to_next_hour(trending_df))



if __name__ == "__main__":
    main()
