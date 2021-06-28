import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    pd.set_option("display.max_rows", 10000)
    df = pd.read_csv('sensors_sample_data.csv', delimiter=';')

# 9105 - 16.���  были подобные записи в стобце velocity, заменяем на нули
    numOfSrtangeSign = 0
    lineswithstrangesign = []
    for i in df.velocity:
        for j in i:
            if j == '�':
                df.velocity[numOfSrtangeSign] = str(df.velocity[numOfSrtangeSign]).replace('�', '0')
                lineswithstrangesign.append(numOfSrtangeSign)
        numOfSrtangeSign += 1


    print( 'lines with �-signs are: ', lineswithstrangesign)

# создаем новый датафрейм с столбцом плотности потока
    dens_df = pd.DataFrame({'intensity':df.intensity, 'velocity': df.velocity}).astype('float64')
    dens_df['density'] = dens_df.intensity / dens_df.velocity

    for i in lineswithstrangesign:
        dens_df.velocity[i] = int(dens_df['velocity'].mean())

# аномалии

# аномалия, когда машины были, но скорость зафиксирована 0
    counterOfIssues1 = 0
    numOfLine = 0
    numNanLines = []
    lines_with_issues1 = []
    for i in dens_df.density:
        if np.isnan(i):
           numNanLines.append(numOfLine)

        elif np.isinf(i):
           counterOfIssues1 += 1
           lines_with_issues1.append(numOfLine)
        numOfLine += 1

# аномалия, когда машин не было, но скорость зафиксированная не равна 0
    counterOfIssues2 = 0
    lines_with_issues2 = []
    newnumOfLine = 0
    for j in dens_df.intensity:
        if int(dens_df.intensity[newnumOfLine]) == 0:
            counterOfIssues2 += 1
            lines_with_issues2.append(newnumOfLine)
        newnumOfLine += 1


    print("The amount of 1st type - issues (intensity != 0 and velocity == 0 ) is", counterOfIssues1, '. lines are', lines_with_issues1)
    print("The amount of 2nd type - issues  (intensity == 0 and velocity != 0 ) is", counterOfIssues2, '. lines are', lines_with_issues2)
    print(dens_df['velocity'].head(9106))


if __name__ == "__main__":
    main()