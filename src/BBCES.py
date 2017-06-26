import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import matplotlib.dates as mdates
import dateutil as du
from datetime import datetime
from datetime import timedelta

BBCES1Windows ='C:/Users/sm2/Documents/Github Repository Clone/TSI-3563-INeph/Data/06-19-2017/BBCES Data/ext_data2.txt'

BBCES = pd.read_csv(BBCES1Windows, delimiter='\t', header=0, engine='python')


def n_point_average(number, data):
    matlab_time_points = np.asarray(data['serial_time'])
    data1 = np.asarray(data['550_nm'])
    data2 = np.asarray(data['680_nm'])
    new_data = pd.DataFrame()
    new_data['Matlab Time'] = matlab_time_points
    new_data['550nm'] = data1
    new_data['680nm'] = data2
    no_nan_data = new_data.dropna()
    python_time_points = []
    time_bins = []
    mean_data1 = []
    mean_data2 = []
    for element in matlab_time_points:
        py_time = datetime.fromordinal(int(element)) + timedelta(days=element%1) - timedelta(days = 366)
        python_time_points.append(py_time)
    new_data['Python Time'] = python_time_points
    f, axxx = plt.subplots(2, 1, sharex=True)
    axxx[0].plot(new_data['Python Time'], new_data['550nm'], 'g-', label='550nm Extinction')
    axxx[0].plot(new_data['Python Time'], new_data['680nm'], 'r-', label='680nm Extinction')
    axxx[0].set_title('Raw BBCES Extinction as a Function of Time')
    axxx[0].set_ylabel('Extinction Coefficient')
    axxx[0].set_xlabel('Time (H:M:S)')
    axxx[0].legend(loc=1)
    axxx[1].set_title('300 Second Averaged BBCES Extinction as a Function of Time')
    axxx[1].set_xlabel('Time (H:M:S)')
    axxx[1].set_ylabel('Extinction Coefficient')
    xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    axxx[1].xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=80)
    plt.tight_layout()
    plt.show()
    '''
    for counter, element in enumerate(time_points):
        a = counter * number
        b = (counter + 1) * number
        avg1 = np.mean(data1[a:b])
        avg2 = np.mean(data2[a:b])
        mean_data1.append(avg1)
        mean_data2.append(avg2)
        time_bins.append(time_points[b])
    '''
    return [time_bins, mean_data1, mean_data2]








n_point_average(300, BBCES)