import numpy as np

print(*list((np.arange(24))) * 5)

print(list(map(int,(8 * str(*np.arange(24))))))