import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
start_time = time.time()


# визуализация графиков
def show_graphs(plot, x, y, name, color):
    plot.scatter(range(len(y)), y, c=color)
    plot.set_title(name)
    plot.set_xlim(0, len(y) - 1)
    plot.set_xticks(range(len(x)))
    plot.set_xticklabels(x)


# нахождение индекса начала нового часа в отсортированном по времени датафрейме
def hop_to_next_hour(func_df_series, starting_point):

    hop = 0
    prev_hour = func_df_series[starting_point].hour
    for i in func_df_series[starting_point:]:
        if i != func_df_series[len(func_df_series) - 1]:
            if i.hour == prev_hour:
                hop += 1
                prev_hour = i.hour
            else:
                return hop, starting_point
        else:
            return hop, starting_point
        starting_point += 1


# для подсчета кол-ва выбросов данных каждой связкой сенсор-направление-участок делю список на подсписки таких связок
def split_list(alist, wanted_parts):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts)]


def main():
    pd.set_option("display.max_rows", 44000)
    pd.set_option("display.max_columns", 8)
    pd.set_option('display.width', 500)

    df = pd.read_csv('sensors_sample_data.csv', delimiter=';')

# 9105 - 16.���  были подобные записи в стобце velocity, заменяем на нули (далее значения будут заменены на среднее)
    num_of_strange_sign = 0
    lines_with_strange_sign = []  # индексы строк с неопознанными знаками
    for i in df.velocity:
        for j in i:
            if j == '�':
                df.velocity[num_of_strange_sign] = str(df.velocity[num_of_strange_sign]).replace('�', '0')
                lines_with_strange_sign.append(num_of_strange_sign)
                break
        num_of_strange_sign += 1


# создаем новый датафрейм c добавлением чуть далее столбца плотности потока
    dens_df = pd.DataFrame({'intensity': df.intensity, 'velocity': df.velocity}).astype('float64')

# заменяем значения в тех строках где раньше были � на среднеезначение всего столбца
    for i in lines_with_strange_sign:
        dens_df.velocity[i] = int(dens_df['velocity'].mean())

#  добавляем столбцы плотности и времени, сортируя по времени
    dens_df['density'] = dens_df.intensity / dens_df.velocity
# создание резервного датафрейма, не сортированного по времени (на всякий случай)
    # unsorted_dens_df = dens_df.copy()

    dens_df['time'] = df.range_end
    dens_df['time'] = pd.to_datetime(dens_df.time)
    dens_df.sort_values(by=['time'], inplace=True, ascending=True)


# аномалия 1, когда машины были, но скорость зафиксирована 0
    zero_velocity_rows = dens_df[(dens_df['velocity'] != 0) & (dens_df['intensity'] == 0)].index.tolist()

# аномалия 2, когда машин не было, но скорость зафиксированная не равна 0
    inf_rows = dens_df[dens_df['density'] == np.inf].index.tolist()

# просто так нашел индексы строк где не было ни машин ни скорости
    nan_rows = dens_df[dens_df['density'].isnull()].index.tolist()

# заменяем все значения inf и NaN на нули и затем на среднее значение столбца
    average_dens = dens_df.density.replace([-np.inf, np.inf, np.nan], 0).mean()
    dens_df = dens_df.replace([-np.inf, np.inf, np.nan], [average_dens, average_dens, 0])

# визуализация с помощью графиков плотности, скорости и интенсивности по времени
    time_list = list(dens_df.time[::500])  # для отображения всех точек, убрать 500, но оооочень долго будет запускаться
    plt.figure(figsize=(17, 8))
    show_graphs(plt.subplot(221), time_list, list(dens_df.intensity[::500]), 'Intensity', 'b')
    show_graphs(plt.subplot(222), time_list, list(dens_df.velocity[::500]), 'Velocity', 'r')
    show_graphs(plt.subplot(212), time_list, list(dens_df.density[::500]), 'Density', 'g')

# создаемм датафрейм отсортированны по времени но с новыми индексами с нуля, для нахождения далее индексов новых часов
    df_by_hours = dens_df.copy().reset_index(drop=True)

# анализ по каждому часу
    list_of_new_hours = [0]  # индексы начала нового часа (для определения тренда по часам)
    new_hour = 0
    for i in range(1000):
        hop, new_hour = hop_to_next_hour(df_by_hours.time, new_hour)
        if hop == 0:
            break
        list_of_new_hours.append(new_hour)

# датафрейм со стобцом тренда
    trending_df = pd.DataFrame({'hour': list(np.arange(24)) *
                                (len(list_of_new_hours) // 24) + list(np.arange(len(list_of_new_hours) % 24)),
                                'intensity': df_by_hours.intensity.iloc[list_of_new_hours],
                                'velocity': df_by_hours.velocity.iloc[list_of_new_hours],
                                'density': df_by_hours.density.iloc[list_of_new_hours]})

    trending_df['trend intensity'] = np.where(trending_df['intensity'] < trending_df['intensity'].shift(), 'DOWN',
                                              np.where(trending_df['intensity'] > trending_df['intensity'].shift(),
                                                       'UP', 'FLAT'))

    trending_df['trend velocity'] = np.where(trending_df['velocity'] < trending_df['velocity'].shift(), 'DOWN',
                                             np.where(trending_df['velocity'] > trending_df['velocity'].shift(),
                                                      'UP', 'FLAT'))

    trending_df['trend density'] = np.where(trending_df['density'] < trending_df['density'].shift(), 'DOWN',
                                            np.where(trending_df['density'] > trending_df['density'].shift(),
                                                     'UP', 'FLAT'))

# датафрейм для анализа количества выбросов данных каждой тройкой сенсор-направление-участок на протяжении суток
    sorted_df = pd.DataFrame({'sensor_id': df.sensor_id, 'sensor_direction': df.sensor_direction,
                              'sub_direction_number': df.sub_direction_number, 'range_end': df.range_end})

    sorted_df['range_end'] = pd.to_datetime(sorted_df.range_end)

    sorted_df.sort_values(by=['sensor_id', 'sub_direction_number'], inplace=True, ascending=True)

# датафрейм чисто с тройками сенсор-направление-участок
    new_df = pd.DataFrame({'sensor_id': sorted_df.sensor_id, 'sensor_direction': sorted_df.sensor_direction,
                           'sub_direction_number': sorted_df.sub_direction_number})
# датафрейм с тройками в список
    data_frame_list = new_df.values.reshape(-1).tolist()
    splited_list = split_list(data_frame_list, len(data_frame_list) // 3)

    count_of_data_list = []
    counter = 0
    prev_x, prev_y, prev_z = splited_list[0][0], splited_list[0][1], splited_list[0][2]
    for i in splited_list:
        if i[0] == prev_x:
            if i[1] == prev_y:
                if i[2] == prev_z:
                    counter += 1
                else:
                    prev_z = i[2]
                    count_of_data_list.append(counter)
                    counter = 0
            else:
                prev_y = i[1]
                count_of_data_list.append(counter)
                counter = 0
        else:
            prev_x = i[0]
            count_of_data_list.append(counter)
            counter = 0
# удаление лишних нулей
    count_of_data_list = list(filter(lambda num: num != 0, count_of_data_list))

# вывод всей информации
    '''Предварительный анализ  исходного csv файла (много приколов и аномалий)
    '''
    print(len(lines_with_strange_sign), 'lines with � sign instead of number: ', *lines_with_strange_sign)
    print("\nAmount of 1st type issues (velocity is 0 while intensity is not 0):", len(zero_velocity_rows),
          ". Indexes are:", *zero_velocity_rows)
    print("\nAmount of 2nd type issues (velocity is not 0 while intensity is 0), dividing by 0 = inf:", len(inf_rows),
          ". Indexes are:", *inf_rows)
    print("\nAmount of NaN (0 velocity and 0 intensity):", len(nan_rows), ". Indexes are:", *nan_rows)

    '''1ый пункт ТЗ, значения плотности потока но в хронологическом порядке,
        в порядке данном в начальном csv - unsorted_dens_df.density.head()'''
    print(dens_df.density.head(10))

    '''2ой пункт ТЗ, датафрейм со столбцами тренда интенсивности, скорости и плотности по часам ,
     индексы этого датафрейма найденны функцией и означают начало каждого нового часа, т.е записи 0 - 632 были с нулевым 
     часом, 632 - 1397 c 1 часом, и так далее, на протяжении около 2ух суток'''
    print(trending_df.head(30))

    '''
    3ий пункт ТЗ, список количества выбросов данных каждой тройкой сенсор-направление-участок. для нахождения того 
    или иного сенсора (допустим с минимальным или максимальным количеством выбросом данных за промежуток времени, 
    сложить суммы предыдущих троек и получится индекс искомой тройки с интересующим нас количестовм выбросов'''
    print('Amount of data ejections:', *count_of_data_list)

    '''
    4ый пункт ТЗ, графики интенсивности, скорости от времени ( за одно плотность от времени, для красоты)
    '''
    plt.show()

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
