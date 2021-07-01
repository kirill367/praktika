import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
start_time = time.time()


def show_graphs(plot, X, Y, name, color):
    plot.scatter(range(len(Y)), Y, c=color)
    plot.set_title(name)
    plot.set_xlim(0, len(Y) - 1)
    plot.set_xticks(range(len(X)))
    plot.set_xticklabels(X)


def main():
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

# аномалия 1, когда машины были, но скорость зафиксирована 0
    counterOfIssues1 = 0  # счетчик аномалий такого типа
    numOfLine = 0
    numNanLines = []  # индексы строк с NaN значением ( 0 / 0 )
    lines_with_issues1 = []  # индексы строк с аномалией 1 (с значением inf, (1 / 0))
    for i in dens_df.density:
        if np.isnan(i):
           numNanLines.append(numOfLine)

        elif np.isinf(i):
           counterOfIssues1 += 1
           lines_with_issues1.append(numOfLine)
        numOfLine += 1

# аномалия 2, когда машин не было, но скорость зафиксированная не равна 0
    counterOfIssues2 = 0  # счетчик аномалий такого типа
    lines_with_issues2 = []
    newnumOfLine = 0
    for j in dens_df.intensity:
        if int(dens_df.intensity[newnumOfLine]) == 0 and dens_df.velocity[newnumOfLine] != 0:
            counterOfIssues2 += 1
            lines_with_issues2.append(newnumOfLine)
        newnumOfLine += 1


# визуализация с помощью графиков плотности по времени и скорости по времени
    time_list = list(dens_df.time[::100])
    fig = plt.figure(figsize=(17, 8))
    show_graphs(plt.subplot(221), time_list, list(dens_df.intensity[::100]), 'Intensity', 'b')
    show_graphs(plt.subplot(222), time_list, list(dens_df.velocity[::100]), 'Velocity', 'r')
    show_graphs(plt.subplot(212), time_list, list(dens_df.density[::100]), 'Density', 'g')
    #plt.show()

    print('lines with �-signs are: ', lineswithstrangesign)
    print("The amount of 1st type - issues (intensity != 0 and velocity == 0 ) is", counterOfIssues1, '. lines are',
          lines_with_issues1)
    print("The amount of 2nd type - issues (intensity == 0 and velocity != 0 ) is", counterOfIssues2, '. lines are',
          lines_with_issues2)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
