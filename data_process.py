import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('data/I_vel_pow.csv')
data = data[np.logical_and(data['time_(s)'] > 1.07, data['time_(s)'] < 1.1)]

coeff = np.polyfit(data['time_(s)'], data['velocity_(turn/s)']*2*np.pi, 1)
print(coeff)