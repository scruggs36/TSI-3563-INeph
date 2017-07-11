import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates


path = "/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-20-2017/NL170620.dat"
DatFile = open(path, "r")
Lines = DatFile.readlines()

time_array = []
blue_tot_scatter = []
green_tot_scatter = []
red_tot_scatter = []
blue_bak_scatter = []
green_bak_scatter = []
red_bak_scatter = []
z_blue_tot_scatter = []
z_green_tot_scatter = []
z_red_tot_scatter = []
z_blue_bak_scatter = []
z_green_bak_scatter = []
z_red_bak_scatter = []
z_blue_rayleigh_scatter = []
z_green_rayleigh_scatter = []
z_red_rayleigh_scatter = []
pressure = []
sample_temp = []
inlet_temp = []
RH = []
Lamp_Volts = []
Lamp_Amps = []
BNC_Volts = []

# the asterik in the first if statement in the for loop before time tuple is important and is indicative
# of accepting other parameters

# also, all dates, whether strings or tuples, the goal is to convert them into datetime objects
# such that they are interpreted by python, then use num2dates for plots

# the second if statement in the for loop really should be
# if Line.split(',')[0] == 'D'and Line.split(',')[1][0] == 'N':
# as the N implies normal operation, outside of Z for zero, and B for blanking mode!
# however, if I do this the data frame will not be of the right dimensions!
# this really needs to be fixed which may require more thought

for Line in Lines:
    if Line.split(',')[0] == 'T':
        time_tuple = (Line.split(',')[1], Line.split(',')[2], Line.split(',')[3], Line.split(',')[4], Line.split(',')[5], Line.split(',')[6])
        time_tuple = tuple(int(x) for x in time_tuple)
        date_str = datetime(*time_tuple)
        time_array.append(date_str)
    #if Line.split(',')[0] == 'D'and Line.split(',')[1][0] == 'N':
    if Line.split(',')[0] == 'D':
        blue_tot_scatter.append(Line.split(',')[3])
        green_tot_scatter.append(Line.split(',')[4])
        red_tot_scatter.append(Line.split(',')[5])
        blue_bak_scatter.append(Line.split(',')[6])
        green_bak_scatter.append(Line.split(',')[7])
        red_bak_scatter.append(Line.split(',')[8])
    if Line.split(',')[0] == 'Y':
        pressure.append(Line.split(',')[2])
        sample_temp.append(Line.split(',')[3])
        inlet_temp.append(Line.split(',')[4])
        RH.append(Line.split(',')[5])
        Lamp_Volts.append(Line.split(',')[6])
        Lamp_Amps.append(Line.split(',')[7])
        BNC_Volts.append(Line.split(',')[8])
    if Line.split(',')[0] == 'Z':
        z_blue_tot_scatter.append(Line.split(',')[1])
        z_green_tot_scatter.append(Line.split(',')[2])
        z_red_tot_scatter.append(Line.split(',')[3])
        z_blue_bak_scatter.append(Line.split(',')[4])
        z_green_bak_scatter.append(Line.split(',')[5])
        z_red_bak_scatter.append(Line.split(',')[6])
        z_blue_rayleigh_scatter.append(Line.split(',')[7])
        z_green_rayleigh_scatter.append(Line.split(',')[8])
        z_red_rayleigh_scatter.append(Line.split(',')[9])

# convert date time objects to a usable format for matplotlib.pyplot
dates_and_times = matplotlib.dates.date2num(time_array)
xfmt = matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S')

'''
# make sure arrays are same length
print(len(dates_and_times))
print(len(blue_tot_scatter))
print(len(green_tot_scatter))
print(len(red_tot_scatter))
print(len(blue_bak_scatter))
print(len(green_bak_scatter))
print(len(red_bak_scatter))
print(len(pressure))
print(len(sample_temp))
print(len(inlet_temp))
print(len(RH))
print(len(Lamp_Amps))
print(len(Lamp_Volts))
print(len(BNC_Volts))
'''
blue_tot_scatter = [float(i) * 1E6 for i in blue_tot_scatter]
green_tot_scatter = [float(i) * 1E6 for i in green_tot_scatter]
red_tot_scatter = [float(i) * 1E6 for i in red_tot_scatter]
blue_bak_scatter = [float(i) * 1E6 for i in blue_bak_scatter]
green_bak_scatter = [float(i) * 1E6 for i in green_bak_scatter]
red_bak_scatter = [float(i) * 1E6 for i in red_bak_scatter]
pressure = [float(i) for i in pressure]
sample_temp = [float(i) for i in sample_temp]
inlet_temp = [float(i) for i in inlet_temp]
RH = [float(i) for i in RH]
Lamp_Amps = [float(i) for i in Lamp_Amps]
Lamp_Volts = [float(i) for i in Lamp_Volts]
BNC_Volts = [float(i) for i in BNC_Volts]

# create data frame for saving a text file
DF = pd.DataFrame()
DF['Date Times'] = dates_and_times
DF['Blue Total Scattering Coefficient'] = blue_tot_scatter
DF['Green Total Scattering Coefficient'] = green_tot_scatter
DF['Red Total Scattering Coefficient'] = red_tot_scatter
DF['Blue Back Scattering Coefficient'] = blue_bak_scatter
DF['Green Back Scattering Coefficient'] = green_bak_scatter
DF['Red Back Scattering Coefficient'] = red_bak_scatter
DF['Barometric Pressure (mBar)'] = pressure
DF['Sample Temperature (K)'] = sample_temp
DF['Inlet Temperature (K)'] = inlet_temp
DF['Relative Humidity (%)'] = RH
DF['Lamp Current'] = Lamp_Amps
DF['Lamp Voltage'] = Lamp_Volts
DF['BNC Input Voltage (mV)'] = BNC_Volts


# creating plots from data frame
f0, ax0 = plt.subplots()
ax0.plot(DF['Date Times'], DF['Blue Total Scattering Coefficient'], 'b-', label='Blue Total Scattering')
ax0.plot(DF['Date Times'], DF['Green Total Scattering Coefficient'], 'g-', label='Green Total Scattering')
ax0.plot(DF['Date Times'], DF['Red Total Scattering Coefficient'], 'r-', label='Red Total Scattering')
ax0.set_title('Scattering Coefficients as a Function of Time')
ax0.set_xlabel('Time')
ax0.set_ylabel('Scattering Coefficient (Mm^-1)')
ax0.xaxis.set_major_formatter(xfmt)
plt.legend(loc=1)
plt.xticks(rotation=80)
plt.tight_layout()
plt.show()


f1, ax1 = plt.subplots()
ax1.plot(DF['Date Times'], DF['Blue Back Scattering Coefficient'], 'b-', label='Blue Back Scattering')
ax1.plot(DF['Date Times'], DF['Green Back Scattering Coefficient'], 'g-', label='Green Back Scattering')
ax1.plot(DF['Date Times'], DF['Red Back Scattering Coefficient'], 'r-', label='Red Back Scattering')
ax1.set_title('Back Scattering Coefficients as a Function of Time')
ax1.set_xlabel('Time')
ax1.set_ylabel('Scattering Coefficient (Mm^-1)')
ax1.xaxis.set_major_formatter(xfmt)
plt.legend(loc=1)
plt.xticks(rotation=80)
plt.tight_layout()
plt.show()


# This is how you rotate axes on subplots, but it becomes far too congested
# I ended up splitting up the plots for clarity
'''
f2, ax2 = plt.subplots(1, 3)
ax2[0].plot(DF['Date Times'], DF['Barometric Pressure (mBar)'], 'g-', label='Barometric Pressure (mBar)')
ax2[1].plot(DF['Date Times'], DF['Sample Temperature (K)'], 'r-', label='Sample Temperature (K)')
ax2[1].plot(DF['Date Times'], DF['Inlet Temperature (K)'], 'r--', label='Inlet Temperature (K)')
ax2[2].plot(DF['Date Times'], DF['Relative Humidity (%)'], 'b-', label='RH (%)')
ax2[0].set_title('Barometric Pressure as a Function of Time')
ax2[0].set_xlabel('Time')
ax2[0].set_ylabel('mBar')
ax2[1].set_title('Temperature as a Function of Time')
ax2[1].set_xlabel('Time')
ax2[1].set_ylabel('Kelvin')
ax2[2].set_title('Percent Relative Humidity as a Function of Time')
ax2[2].set_xlabel('Time')
ax2[2].set_ylabel('% RH')
ax2[0].xaxis.set_major_formatter(xfmt)
ax2[1].xaxis.set_major_formatter(xfmt)
ax2[2].xaxis.set_major_formatter(xfmt)
ax2[0].legend(loc=1)
ax2[1].legend(loc=1)
ax2[2].legend(loc=1)
plt.setp(ax2[0].xaxis.get_majorticklabels(), rotation=80)
plt.setp(ax2[1].xaxis.get_majorticklabels(), rotation=80)
plt.setp(ax2[2].xaxis.get_majorticklabels(), rotation=80)
plt.tight_layout()
plt.show()


f3, ax3 = plt.subplots(1, 3)
ax3[0].plot(DF['Date Times'], DF['Lamp Current'], 'b-', label='Lamp Current')
ax3[1].plot(DF['Date Times'], DF['Lamp Voltage'], 'g-', label='Lamp Voltage')
ax3[2].plot(DF['Date Times'], DF['BNC Input Voltage (mV)'], 'r-', label='BNC Voltage')
ax3[0].set_title('Lamp Current as a Function of Time')
ax3[0].set_xlabel('Time')
ax3[0].set_ylabel('Amperes?')
ax3[1].set_title('Lamp Voltage as a Function of Time')
ax3[1].set_xlabel('Time')
ax3[1].set_ylabel('Volts?')
ax3[2].set_title('BNC Input Voltage as a Function of Time')
ax3[2].set_xlabel('Time')
ax3[2].set_ylabel('mV')
ax3[0].xaxis.set_major_formatter(xfmt)
ax3[1].xaxis.set_major_formatter(xfmt)
ax3[2].xaxis.set_major_formatter(xfmt)
ax3[0].legend(loc=1)
ax3[1].legend(loc=1)
ax3[2].legend(loc=1)
plt.setp(ax3[0].xaxis.get_majorticklabels(), rotation=80)
plt.setp(ax3[1].xaxis.get_majorticklabels(), rotation=80)
plt.setp(ax3[2].xaxis.get_majorticklabels(), rotation=80)
plt.tight_layout()
plt.show()
'''

f2, ax2 = plt.subplots()
ax2.plot(DF['Date Times'], DF['Barometric Pressure (mBar)'], 'g-', label='Barometric Pressure (mBar)')
ax2.set_title('Barometric Pressure as a Function of Time')
ax2.set_xlabel('Time')
ax2.set_ylabel('mBar')
ax2.xaxis.set_major_formatter(xfmt)
ax2.legend(loc=1)
plt.xticks(rotation=80)
plt.tight_layout()
plt.show()

f3, ax3 = plt.subplots()
ax3.plot(DF['Date Times'], DF['Sample Temperature (K)'], 'r-', label='Sample Temperature (K)')
ax3.legend(loc=1)
ax3.set_title('Sample Temperature as a Function of Time')
ax3.set_xlabel('Time')
ax3.set_ylabel('Kelvin')
ax3.xaxis.set_major_formatter(xfmt)
ax3.legend(loc=1)
plt.xticks(rotation = 80)
plt.tight_layout()
plt.show()


f4, ax4 = plt.subplots()
ax4.plot(DF['Date Times'], DF['Inlet Temperature (K)'], 'r--', label='Inlet Temperature (K)')
ax4.set_title('Inlet Temperature as a Function of Time')
ax4.set_xlabel('Time')
ax4.set_ylabel('Kelvin')
ax4.xaxis.set_major_formatter(xfmt)
ax4.legend(loc=1)
plt.xticks(rotation = 80)
plt.tight_layout()
plt.show()


f5, ax5 = plt.subplots()
ax5.plot(DF['Date Times'], DF['Relative Humidity (%)'], 'b-', label='RH (%)')
ax5.set_title('Percent Relative Humidity as a Function of Time')
ax5.set_xlabel('Time')
ax5.set_ylabel('% RH')
ax5.xaxis.set_major_formatter(xfmt)
ax5.legend(loc=1)
plt.xticks(rotation = 80)
plt.tight_layout()
plt.show()


f6, ax6 = plt.subplots()
ax6.plot(DF['Date Times'], DF['Lamp Current'], 'b-', label='Lamp Current')
ax6.set_title('Lamp Current as a Function of Time')
ax6.set_xlabel('Time')
ax6.set_ylabel('Amperes?')
ax6.xaxis.set_major_formatter(xfmt)
ax6.legend(loc=1)
plt.xticks(rotation=80)
plt.tight_layout()
plt.show()


f7, ax7 = plt.subplots()
ax7.plot(DF['Date Times'], DF['Lamp Voltage'], 'g-', label='Lamp Voltage')
ax7.set_title('Lamp Voltage as a Function of Time')
ax7.set_xlabel('Time')
ax7.set_ylabel('Volts?')
ax7.xaxis.set_major_formatter(xfmt)
ax7.legend(loc=1)
plt.xticks(rotation=80)
plt.tight_layout()
plt.show()


f8, ax8 = plt.subplots()
ax8.plot(DF['Date Times'], DF['BNC Input Voltage (mV)'], 'r-', label='BNC Voltage')
ax8.set_title('BNC Input Voltage as a Function of Time')
ax8.set_xlabel('Time')
ax8.set_ylabel('mV')
ax8.xaxis.set_major_formatter(xfmt)
ax8.legend(loc=1)
plt.xticks(rotation=80)
plt.tight_layout()
plt.show()