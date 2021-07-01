import pandas as pd

pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_columns", 10)
pd.set_option('display.width', 1000)
df = pd.read_csv('sensors_sample_data.csv', delimiter=';')

sorted_df = pd.DataFrame({'sensor_id': df.sensor_id, 'sensor_direction': df.sensor_direction,
                          'sub_direction_number': df.sub_direction_number, 'range_end': df.range_end})

sorted_df['range_end'] = pd.to_datetime(sorted_df.range_end)

sorted_df.sort_values(by=['sensor_id', 'range_end'], inplace=True, ascending=True)
print(sorted_df.head(1000))

