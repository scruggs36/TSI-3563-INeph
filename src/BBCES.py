import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import matplotlib.dates as mdates
import dateutil as du
from datetime import datetime
from datetime import timedelta
from datetime import date

BBCES1Windows = 'C:/Users/sm2/Documents/Github Repository Clone/TSI-3563-INeph/Data/06-19-2017/BBCES Data/ext_data2.txt'
BBCES2Windows = 'C:/Users/sm2/Documents/Github Repository Clone/TSI-3563-INeph/Data/06-19-2017/BBCES Data/time_data.txt'
INEPH1Windows = 'C:/Users/sm2/Documents/Github Repository Clone/TSI-3563-INeph/Data/06-19-2017/CorrectedData.csv'
INEPH2Windows = 'C:/Users/sm2/Documents/Github Repository Clone/TSI-3563-INeph/Data/06-20-2017/CorrectedData.csv'


BBCES1Linux = '/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-19-2017/BBCES Data/ext_data2.txt'
BBCES2Linux = '/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-19-2017/BBCES Data/time_data.txt'
INEPH1Linux = '/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-19-2017/CorrectedData.csv'
INEPH2Linux = '/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-20-2017/CorrectedData.csv'


INEPH1 = pd.read_csv(INEPH1Linux, delimiter=',', header=0)
INEPH2 = pd.read_csv(INEPH2Linux, delimiter=',', header=0)
INEPH = pd.concat([INEPH1, INEPH2])

BBCES_ts = pd.read_csv(BBCES2Linux, delimiter='\t', header=0)


BBCES = pd.read_csv(BBCES1Linux, delimiter='\t', header=0, engine='python')


BBCES['Time String'] = np.asarray(BBCES_ts)[:,0]


# Interpret time stamps with datetime and re-append as new column in data frame
INeph_py_time = []

for element in INEPH['Time Stamp']:
    t = datetime.strptime(element, "%Y-%m-%d %H:%M:%S")
    t.replace(second=0)
    INeph_py_time.append(t)

INEPH['PY Time'] = INeph_py_time

# Function to plot raw data obtained from BBCES and Line up time stamps from INEPH and BBCES

def n_point_average(number, data):
    # creating a new dataframe because of issues with mikes txt file
    matlab_time_points = np.asarray(data['Time String'])
    data1 = np.asarray(data['550_nm'])
    data2 = np.asarray(data['680_nm'])
    new_data = pd.DataFrame()
    new_data['Time String'] = matlab_time_points
    new_data['550nm'] = data1
    new_data['680nm'] = data2

    # dropping NaN data from dataframe rows
    new_data = new_data.dropna()

    # declaring some empty arrays for later use
    python_time_points = []
    time_bins = []
    mean_data_550nm = []
    mean_data_680nm = []

    # this is gets the date time string into datetime.datetime format
    for element in new_data['Time String']:
        the_times = datetime.strptime(element, "%Y-%m-%d %H:%M:%S")
        the_times.replace(microsecond=0)
        python_time_points.append(the_times)
    new_data['Python Time'] = python_time_points

    # this creates a plot of the BBCES data
    f0, ax = plt.subplots()
    ax.plot(new_data['Python Time'], new_data['550nm'], 'g.', label='550nm Extinction')
    ax.plot(new_data['Python Time'], new_data['680nm'], 'r.', label='680nm Extinction')
    ax.set_title('Raw BBCES Extinction as a Function of Time')
    ax.set_ylabel('Extinction Coefficient')
    ax.set_xlabel('Time (H:M:S)')
    ax.legend(loc=1)
    xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=80)
    plt.tight_layout()
    plt.show()

    # preparing for some loops to match times and data points
    neph_times = INEPH['PY Time'].tolist()
    bbces_times = new_data['Python Time'].tolist()
    bbces_550nm = new_data['550nm'].tolist()
    bbces_680nm = new_data['680nm'].tolist()
    ineph_overlap_bbces = []
    bbces_overlap_ineph = []
    INeph_rgd = []
    INeph_cgd = []
    INeph_rrd = []
    INeph_crd = []

    # this double for loop finds where the bbces and INEPH times match exactly
    for element1 in neph_times:
        for element2 in bbces_times:
            if element1 == element2:
                ineph_overlap_bbces.append(neph_times.index(element1))
                bbces_overlap_ineph.append(bbces_times.index(element2))
                time_bins.append(element1)
                print([element1, neph_times.index(element1), element2, bbces_times.index(element2)])



    # we have to delete the first point because there is not enough data to average prior to the matching of the times for the bbces to average
    del bbces_overlap_ineph[0]
    del ineph_overlap_bbces[0]
    del time_bins[0]

    # here we are averaging the data prior to the matched times for the bbces and appending to array
    for element3 in bbces_overlap_ineph:
        mean_data_550nm.append(np.mean(bbces_550nm[element3 - number:element3]))
        mean_data_680nm.append(np.mean(bbces_680nm[element3 - number:element3]))

    # creating a plot of the averaged data from BBCES and overlaying INEPH data
    f1, ax = plt.subplots()
    ax.set_title('300 Second Averaged BBCES and INEPH Data Plotted as a Function of Time')
    ax.set_xlabel('Time (H:M:S)')
    ax.set_ylabel('Extinction or Scattering Coefficient')
    ax.plot(time_bins, mean_data_550nm, 'g.', label='BBCES 300s Mean 550nm Ext. Coef.')
    ax.plot(time_bins, mean_data_680nm, 'r.', label='BBCES 300s Mean 680nm Ext. Coef.')
    ax.plot(INEPH['PY Time'], INEPH['Raw Green Data'] * 1.0E6, 'g--', label='Raw INeph 550nm Sca. Coef.')
    ax.plot(INEPH['PY Time'], INEPH['Raw Red Data'] * 1.0E6, 'r--', label='Raw INeph 700nm Sca. Coef.')
    ax.plot(INEPH['PY Time'], INEPH['Corrected Green Data'], 'g*', label='Corrected INeph 550nm Sca. Coef.')
    ax.plot(INEPH['PY Time'], INEPH['Corrected Red Data'], 'r*', label='Corrected INeph 700nm Sca. Coef.')
    ax.legend(loc=1)
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=80)
    plt.tight_layout()
    plt.show()

    # collecting raw and corrected INeph data at the selected times
    for element4 in ineph_overlap_bbces:
        INeph_rgd.append(np.asarray(INEPH['Raw Green Data'])[element4] * 1.0E6)
        INeph_cgd.append(np.asarray(INEPH['Corrected Green Data'])[element4])
        INeph_rrd.append(np.asarray(INEPH['Raw Red Data'])[element4] * 1.0E6)
        INeph_crd.append(np.asarray(INEPH['Corrected Red Data'])[element4])


    ratio_raw_550nm = np.divide(INeph_rgd, mean_data_550nm,)
    ratio_corrected_550nm = np.divide(INeph_cgd, mean_data_550nm)
    ratio_raw_680nm = np.divide(INeph_rrd, mean_data_680nm)
    ratio_corrected_680nm = np.divide(INeph_crd, mean_data_680nm)

    # Plot INeph to BBCES ratio vs time
    f2, ax = plt.subplots()
    ax.plot(time_bins, ratio_raw_550nm, 'g-', label='550nm Raw INeph:BBCES ratio')
    ax.plot(time_bins, ratio_corrected_550nm, 'g--', label='550nm Corrected INeph:BBCES ratio')
    ax.plot(time_bins, ratio_raw_680nm, 'r-', label='680nm Raw INeph:BBCES ratio')
    ax.plot(time_bins, ratio_corrected_680nm, 'r--', label='680nm Corrected INeph:BBCES ratio')
    ax.set_title('Integrating Nephelometer to BBCES Ratio as a Function of Time')
    ax.set_ylabel('Scattering:Extinction Ratio (SSA)')
    ax.set_xlabel('Time (H:M:S)')
    ax.legend(loc=1)
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=80)
    plt.tight_layout()
    plt.show()


    return [time_bins, mean_data_550nm, mean_data_680nm]


n_point_average(300, BBCES)