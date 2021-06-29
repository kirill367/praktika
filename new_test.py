import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
start_time = time.time()

def main():
    fig = plt.Figure(figsize=(50,100))
    plt.plot()
    plt.show()

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
