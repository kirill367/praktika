import pandas as pd
import numpy as np
import datetime

pd.set_option("display.max_rows", 15000)
pd.set_option("display.max_columns", 10)

def split_list(alist, wanted_parts):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts)]


pd.set_option('display.width', 1000)
df = pd.read_csv('sensors_sample_data.csv', delimiter=';')

sorted_df = pd.DataFrame({'sensor_id': df.sensor_id, 'sensor_direction': df.sensor_direction,
                          'sub_direction_number': df.sub_direction_number, 'range_end': df.range_end})

sorted_df['range_end'] = pd.to_datetime(sorted_df.range_end)

sorted_df.sort_values(by=['sensor_id', 'sub_direction_number'], inplace=True, ascending=True)

new_df = pd.DataFrame({'sensor_id': sorted_df.sensor_id, 'sensor_direction': sorted_df.sensor_direction,
                       'sub_direction_number': sorted_df.sub_direction_number})

data_frame_list = new_df.values.reshape(-1).tolist()
splited_list = split_list(data_frame_list, len(data_frame_list) // 3)

count_list = []
counter = 0
prev_x, prev_y, prev_z = splited_list[0][0], splited_list[0][1], splited_list[0][2]
for i in splited_list:
    if i[0] == prev_x:
        if i[1] == prev_y:
            if i[2] == prev_z:
                counter += 1
            else:
                prev_z = i[2]
                count_list.append(counter)
                counter = 0
        else:
            prev_y = i[1]
            count_list.append(counter)
            counter = 0
    else:
        prev_x = i[0]
        count_list.append(counter)
        counter = 0



count_list = list(filter(lambda num: num != 0, count_list))
print(count_list)
