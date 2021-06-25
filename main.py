import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    pd.set_option("display.max_rows", 10000)
    df = pd.read_csv('sensors_sample_data.csv', delimiter=';')

# 9105 - 16.���  были подоюные записи
    numOfSrtangeSign = 0
    for i in df.velocity:
        for j in i:
            if j == '�':
                df.velocity[numOfSrtangeSign] = str(df.velocity[numOfSrtangeSign]).replace('�', '0')
        numOfSrtangeSign += 1

    result_df = pd.DataFrame({'intensity':df.intensity, 'velocity': df.velocity }).astype('float64')
    result_df['density'] = result_df.intensity / result_df.velocity

    counterOfIssues1 = 0
    numOfLine = 0
    numNanLines = []
    lines_with_issues1 = []
    for i in result_df.density:
        if np.isnan(i):
           numNanLines.append(numOfLine)

        elif np.isinf(i):
           counterOfIssues1 += 1
           lines_with_issues1.append(numOfLine)
        numOfLine += 1
        
    counterOfIssues2 = 0
    lines_with_issues2 = []
    newnumOfLine = 0
    for i in result_df.intensity:
        if int(result_df.intensity[newnumOfLine]) == 0: #and result_df.velocity[newnumOfLine] != 0.0:
            counterOfIssues2 += 1
            lines_with_issues2.append(newnumOfLine)
    numOfLine += 1


    print("The amount of 1st type - issues (intensity != 0 and velocity == 0 ) is", counterOfIssues1,'. lines are', lines_with_issues1)
    print("The amount of 2nd type - issues  (intensity == 0 and velocity != 0 ) is", counterOfIssues2,'. lines are', lines_with_issues2)

    print(result_df.tail(1000))
if __name__ == "__main__":
    main()