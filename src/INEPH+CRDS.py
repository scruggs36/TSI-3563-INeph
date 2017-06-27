import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime


INeph1 = '/home/austen/PycharmProjects/Integrating Nephelometer/Data/Neph Data/NL170409Frame.csv'
INeph2 = '/home/austen/PycharmProjects/Integrating Nephelometer/Data/Neph Data/NL170410Frame.csv'
INeph3 = '/home/austen/PycharmProjects/Integrating Nephelometer/Data/Neph Data/NL170411Frame.csv'
INeph4 = '/home/austen/PycharmProjects/Integrating Nephelometer/Data/Neph Data/NL170412Frame.csv'
INeph5 = '/home/austen/PycharmProjects/Integrating Nephelometer/Data/Neph Data/NL170413Frame.csv'
INeph6 = '/home/austen/PycharmProjects/Integrating Nephelometer/Data/Neph Data/NL170414Frame.csv'
# processed data for 2017-04-09 is not present; ask Al if he has it...
# crds1 = '/home/austen/PycharmProjects/Integrating Nephelometer/Data/CRDS Data/20170409/pas_processed.txt'
crds2 = '/home/austen/PycharmProjects/Integrating Nephelometer/Data/CRDS Data/20170410/pas_processed.txt'
crds3 = '/home/austen/PycharmProjects/Integrating Nephelometer/Data/CRDS Data/20170411/pas_processed.txt'


INEPH1 = pd.read_csv(INeph1, delimiter=',', header=0)
INEPH2 = pd.read_csv(INeph2, delimiter=',', header=0)
INEPH3 = pd.read_csv(INeph3, delimiter=',', header=0)
INEPH4 = pd.read_csv(INeph4, delimiter=',', header=0)
INEPH5 = pd.read_csv(INeph5, delimiter=',', header=0)
INEPH6 = pd.read_csv(INeph6, delimiter=',', header=0)
# CRDS1 = pd.read_csv(crds1, delimiter='\t', header=0)
CRDS2 = pd.read_csv(crds2, delimiter='\t', header=0)
CRDS3 = pd.read_csv(crds3, delimiter='\t', header=0)

INEPH1 = pd.DataFrame(INEPH1)
INEPH2 = pd.DataFrame(INEPH2)
INEPH3 = pd.DataFrame(INEPH3)
INEPH4 = pd.DataFrame(INEPH4)
INEPH5 = pd.DataFrame(INEPH5)
INEPH6 = pd.DataFrame(INEPH6)
# CRDS1 = pd.DataFrame(CRDS1)
CRDS2 = pd.DataFrame(CRDS2)
CRDS3 = pd.DataFrame(CRDS3)
INEPH = pd.concat([INEPH2, INEPH3, INEPH4, INEPH5])
CRDS = pd.concat([CRDS2, CRDS3])



def SAE_function(sigma1, sigma2, lambda1, lambda2):
    return -1.0*(np.log(sigma1/sigma2)/np.log(lambda1/lambda2))


def SAE(data):
    df = pd.DataFrame()
    sae = []
    cfblue = []
    cfgreen = []
    cfred = []
    timearray = []
    correctedblue = []
    correctedgreen = []
    correctedred = []
    blue = np.asarray(data.loc[:, 'Blue'])
    green = np.asarray(data.loc[:, 'Green'])
    red = np.asarray(data.loc[:, 'Red'])
    timestamps = np.asarray(data.loc[:, 'Date_Hr'])
    for counter, element in enumerate(timestamps):
        time = datetime.strptime(timestamps[counter], "%Y-%m-%d %H:%M:%S")
        timearray.append(time)
    timearray = mdates.date2num(timearray)
    for counter, element in enumerate(timestamps):
        saeval = SAE_function(1.0E5 * float(blue[counter]), 1.0E5 * float(red[counter]), 450.0E-9, 700.0E-9)
        cfblueval = 1.365 + (-.156 * sp.exp(-1.0 * saeval))
        cfgreenval = 1.337 + (-.138 * sp.exp(-1.0 * saeval))
        cfredval = 1.297 + (-.113 * sp.exp(-1.0 * saeval))
        correctedblueval = cfblueval * 1.0E5 * blue[counter]
        correctedgreenval = cfgreenval * 1.0E5 * green[counter]
        correctedredval = cfredval * 1.0E5 * red[counter]
        sae.append(saeval)
        cfblue.append(cfblueval)
        cfgreen.append(cfgreenval)
        cfred.append(cfredval)
        correctedblue.append(correctedblueval)
        correctedgreen.append(correctedgreenval)
        correctedred.append(correctedredval)
    df['Time Stamp'] = timestamps
    df['Raw Blue Data'] = blue
    df['Raw Green Data'] = green
    df['Raw Red Data'] = red
    df['S.A.E. (Blue:Red)'] = sae
    df['Blue Correction Factor'] = cfblue
    df['Green Correction Factor'] = cfgreen
    df['Red Correction Factor'] = cfred
    df['Corrected Blue Data'] = correctedblue
    df['Corrected Green Data'] = correctedgreen
    df['Corrected Red Data'] = correctedred
    myFmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
    ax = plt.subplot(211)
    ax.plot(timearray, sae, label='SAE')
    ax.set_title('Scattering Angstrom Exponent as a Function of Time')
    ax.set_ylabel('S.A.E.')
    ax.legend(loc=1)
    ax.xaxis.set_major_formatter(myFmt)
    ax1 = plt.subplot(212, sharex=ax)
    ax1.plot(timearray, correctedblue, 'b-', label='blue wavelength')
    ax1.plot(timearray, correctedgreen, 'g-', label='green wavelength')
    ax1.plot(timearray, correctedred, 'r-', label='red wavelength')
    ax1.set_title('Corrected Scattering Coefficients as a Function of Time')
    ax1.set_ylabel('Corrected Scattering Coefficient')
    ax1.tick_params(axis='x', pad=30)
    ax1.legend(loc=1)
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.xticks(rotation=89)
    plt.gcf().subplots_adjust(bottom=0.30)
    plt.tight_layout()
    plt.show()
    return df

def CRDS_Time(timelist):
    timearray2 = []
    for element in timelist:
        time = datetime.strptime(element, "%Y-%m-%d %H:%M:%S")
        timearray2.append(time)
    return timearray2

# This at some point could be turned into a function
CRD_Time_Stamps = CRDS_Time(np.asarray(CRDS.loc[:, 'Time']))
date_times = mdates.date2num(CRD_Time_Stamps)

f, ax = plt.subplots()
ax.plot_date(date_times, CRDS.loc[:,'ext662_Mm'], 'b-', label='662 nm CRDS Extinction')
ax.set_title('CRDS Extinction vs Time')
ax.set_xlabel('Time')
ax.set_ylabel('Extinction $Mm^{-1}$')
xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.xticks(rotation=90)
plt.legend(loc=1)
plt.tight_layout()
plt.show()


def window_average(arr, n):
    end =  n * int(len(arr)/n)
    return np.mean(arr[:end].reshape(-1, n), 1)

def window_date_times_array(dates, n):
    return dates[0::n]


# CRDS Data collection start 2017-04-11 14:15:00
# We need to use 2017-04-12 00:00:00 data, because both the CRDS and Neph are running here
# We need to average every 60 seconds of the CRDS data because it produces data at 1Hz and the Neph produces data every 60 seconds
Extinction_Array = np.asarray(CRDS.loc[:,'ext662_Mm'])
Window_Averaged_Extinction = window_average(Extinction_Array, 60)
Window_Date_Time = window_date_times_array(date_times, 60)
Window_Date_Time_Strings = window_date_times_array(np.asarray(CRDS.loc[:, 'Time']), 60)


# this function does work and it removes the second unit from the time, but it is still carried over when plotting and such
def Remove_Seconds(timelist):
    TimeArray = []
    for counter, element in enumerate(timelist):
        time = datetime.strptime(timelist[counter], "%Y-%m-%d %H:%M:%S")
        time = time.strftime("%Y-%m-%d %H:%M")
        TimeArray.append(time)
    return TimeArray


# Defining some data frames
DF = SAE(INEPH)
DF3 = pd.DataFrame()
DF3['CRDS Time'] = Window_Date_Time_Strings
DF3['Averaged Extinction'] = Window_Averaged_Extinction
# the below is a neat way of filtering out NaN data
# DF3 = DF3[np.isfinite(DF3['CRDS Extinction'])]


# AA=str.format(Remove_Seconds(np.asarray(INEPH.loc[:, 'Date_Hr']))[115])

# this forces the time stamps in the array to be strings
def Make_Str(array):
    appendable=[]
    for element in array:
        a = str.format(element)
        appendable.append(a)
    return appendable

A = Make_Str(Remove_Seconds(np.asarray(INEPH.loc[:, 'Date_Hr'])))
B = Make_Str(Remove_Seconds(Window_Date_Time_Strings))

# Quick_Test(B, A, -1)
# this simple test is working!
def Simple_Test(X, TestVal):
    appendable = []
    for counter, element in enumerate(X):
        if element == TestVal:
            print(element, counter)
            appendable.append(counter)
    return appendable


# Simple_Test(B, AA)


# Next Test
def Next_Test(X, TestArray):
    appendable = []
    for counter1, element1 in enumerate(TestArray):
        for counter2, element2 in enumerate(X):
            if element1 == element2:
                print(element2, counter2)
                appendable.append(counter2)
    return appendable

# This part of the code is all post processing stuff that utilizes CRD data, I intend on eliminating it as this should
# Only look at Integrating Nephelometer Data

# Example is below this finds where elements in k are located in j
# j = ['rat','cat', 'dog', 'bird','hog', 'frog', 'fox']
# k = ['bird', 'cat', 'dog', 'goat']
# Next_Test(j,  k)

# this finds where elements in A (INEPH) are located in B(CRDS Data)
#CRDS_OVERLAP = np.asarray(Next_Test(B, A))

# this finds where elements in B (CRDS) are loctated in A(INEPH)
#INEPH_OVERLAP = np.asarray(Next_Test(A, B))

# Here we are making the arrays into lists
#CRDS_OVERLAP_ROWS = CRDS_OVERLAP.tolist()
#INEPH_OVERLAP_ROWS = INEPH_OVERLAP.tolist()

# Here we select the rows with the timestamps that overlap between INEPH data and CRDS data
# Finally the Data Frames are bound by the right time start and end points, but they are still not the same size
#DF = pd.DataFrame(DF.ix[INEPH_OVERLAP_ROWS])
#DF3 = pd.DataFrame(DF3.ix[CRDS_OVERLAP_ROWS])

#AVG_EXTINCTION = np.asarray(DF3[['Averaged Extinction']])
#RED_CORRECTED_SCATTER = np.asarray(DF[['Corrected Red Data']])
#SCATTERING_EXTINCTION_RATIO = np.divide(RED_CORRECTED_SCATTER, AVG_EXTINCTION)
# found out the last element in the time array was a 'nan' had to do this to make arrays same size, this value was also 'nan',
# using del and [-1] eliminates the last element in the list
#SCATTERING_EXTINCTION_RATIO = np.delete(SCATTERING_EXTINCTION_RATIO, len(SCATTERING_EXTINCTION_RATIO)-1)
#ratio_time = np.asarray(DF[['Time Stamp']])
#ratio_time = ratio_time.flatten()
#ratio_time = ratio_time.tolist()
# found out the last element in the time array was a 'nan',
#  using del and [-1] eliminates the last element in the list
#del ratio_time[-1]

# this is how I found out the last element in the list was 'nan'
# this preventing CRDS_Time function from working properly
# for element in ratio_time:
#    print(type(element))

#RATIO_TIME = mdates.date2num(CRDS_Time(ratio_time))

#f3, ax3 = plt.subplots()
#ax3Fmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
#ax3.plot(RATIO_TIME, SCATTERING_EXTINCTION_RATIO,'r-', label='Scattering to Extinction Ratio' )
#ax3.set_title('Scattering at 632 nm to Extinction Ratio at 662 nm as a Function of Time')
#ax3.set_xlabel('Time')
#ax3.set_ylabel('Scattering:Extinction Ratio')
#ax3.tick_params(axis='x', pad=30)
#ax3.legend(loc=1)
#ax3.xaxis.set_major_formatter(ax3Fmt)
#plt.xticks(rotation=89)
#plt.gcf().subplots_adjust(bottom=0.30)
#plt.tight_layout()
#plt.show()

#f4, ax4 = plt.subplots()
#ax4.plot(AVG_EXTINCTION, RED_CORRECTED_SCATTER, 'ro', label='correlation')
#ax4.set_title('Correlation Plot Scattering vs. Extinction')
#ax4.set_ylabel('Scattering')
#ax4.set_xlabel('Extinction')
#ax4.legend(loc=1)
#ax4.tick_params(axis='x', pad=30)
#plt.tight_layout()
#plt.show()
#DF.to_csv('/home/austen/PycharmProjects/Integrating Nephelometer/Data/INEPHDATA.csv', sep=',')
#DF3.to_csv('/home/austen/PycharmProjects/Integrating Nephelometer/Data/CRDDATA.csv', sep=',')