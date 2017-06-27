import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import matplotlib.dates as mdates
import dateutil as du
from datetime import datetime
from datetime import timedelta


<<<<<<< Updated upstream
INeph1Linux = '/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-19-2017/NL170619Frame.csv'
INeph1Windows = 'C:/Users/sm2/Documents/Github Repository Clone/TSI-3563-INeph/Data/06-19-2017/NL170619Frame.csv'
=======
INeph1 = '/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-20-2017/NL170620Frame.csv'
>>>>>>> Stashed changes


INEPH = pd.read_csv(INeph1Windows, delimiter=',', header=0)

def SAE_function(sigma1, sigma2, lambda1, lambda2):
    return -1.0*(np.log(sigma1/sigma2)/np.log(lambda1/lambda2))


def SAE(data):
    df = pd.DataFrame()
    saebg = []
    saegr = []
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
        saevalbg = SAE_function(float(blue[counter]), float(green[counter]), 450.0E-9, 550.0E-9)
        saevalgr = SAE_function(float(green[counter]), float(red[counter]), 550.0E-9, 700.0E-9)
        cfblueval = 1.165 + (-.046 * sp.exp(-1.0 * saevalbg))
        cfgreenval = 1.152 + (-.044 * sp.exp(-1.0 * saevalbg))
        cfredval = 1.120 + (-.035 * sp.exp(-1.0 * saevalgr))
        correctedblueval = cfblueval * 1.0E6 * blue[counter]
        correctedgreenval = cfgreenval * 1.0E6 * green[counter]
        correctedredval = cfredval * 1.0E6 * red[counter]
        saebg.append(saevalbg)
        saegr.append(saevalgr)
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
    df['S.A.E. (Blue:Green)'] = saebg
    df['S.A.E. (Green:Red)'] = saegr
    df['Blue Correction Factor'] = cfblue
    df['Green Correction Factor'] = cfgreen
    df['Red Correction Factor'] = cfred
    df['Corrected Blue Data'] = correctedblue
    df['Corrected Green Data'] = correctedgreen
    df['Corrected Red Data'] = correctedred
    myFmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
    ax = plt.subplot(211)
    ax.plot(timearray, saebg, label='SAE Blue:Green')
    ax.plot(timearray, saegr, label='SAE Green:Red')
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

#SAE(INEPH)
NephDat = SAE(INEPH)
path = '/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-20-2017/CorrectedData.csv'
NephDat.to_csv(path, sep=',', index=True, header=True)



times = NephDat['Time Stamp'].tolist()
[str(i) for i in times]
time_axis = [du.parser.parse(i) for i in times]


f, axx = plt.subplots(2, 1, sharex=True)
xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
axx[0].xaxis.set_major_formatter(xfmt)
axx[0].plot(time_axis, NephDat['Raw Blue Data'] * 1.0E6, 'b-', label='Raw Blue Coefficients')
axx[0].plot(time_axis, NephDat['Raw Green Data'] * 1.0E6, 'g-', label='Raw Green Coefficients')
axx[0].plot(time_axis, NephDat['Raw Red Data'] * 1.0E6, 'r-', label='Raw Red Coefficients')
axx[0].legend(loc=1)
axx[0].set_title('Blue, Green, and Red Raw Scattering Coefficients as a Function of Time')
axx[0].set_xlabel('Time (H:M:S)')
axx[0].set_ylabel('b ${(Mm^-1)}$')
axx[1].xaxis.set_major_formatter(xfmt)
axx[1].plot(time_axis, NephDat['Corrected Blue Data'], 'b--', label='Corrected Blue Coefficients')
axx[1].plot(time_axis, NephDat['Corrected Green Data'], 'g--', label='Corrected Green Coefficients')
axx[1].plot(time_axis, NephDat['Corrected Red Data'], 'r--', label='Corrected Red Coefficients')
axx[1].legend(loc=1)
axx[1].set_title('Blue, Green, and Red Corrected Scattering Coefficients as a Function of Time')
axx[1].set_xlabel('Time (H:M:S)')
axx[1].set_ylabel('Corrected b ${(Mm^-1)}$')
plt.xticks(rotation=80)
plt.tight_layout()
plt.show()


