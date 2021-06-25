import numpy as np
import pandas as pd

#9105 - 16.&&&
def main():
    pd.set_option("display.max_rows", 10000)
    df = pd.read_csv('sensors_sample_data.csv', delimiter=';')

    counter = 0
    for i in df.velocity:
        for j in i:
            if j == '�':
                df.velocity[counter] = str(df.velocity[counter]).replace('�', '0')
        counter += 1

    result_df = pd.DataFrame({'intensity':df.intensity, 'velocity': df.velocity }).astype('float64')
    result_df['density'] = result_df.intensity / result_df.velocity

   #for i in result_df.density:
       # if i == "inf" or ""
    print(result_df.tail(9999))

if __name__ == "__main__":
    main()