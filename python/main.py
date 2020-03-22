import numpy as np
import matplotlib.pyplot as plt
import os
import sys

from read import read_cvs, CV19_data
from plot import plot_data

#TODO
#Read cvs files
#plot confirmed cases and total deaths
#predict confirmed cases based on total deaths

path = '../csse_covid_19_data/csse_covid_19_time_series/'
confirmed_cases = read_cvs(path+'time_series_19-covid-Confirmed.csv', countries=['Sweden'])[0]
deaths = read_cvs(path+'/time_series_19-covid-Deaths.csv', countries=['Sweden'])[0]

confirmed_cases.add_cases_death(deaths)

where_array = confirmed_cases.deaths.astype(np.bool)

percentage = np.divide(confirmed_cases.deaths, confirmed_cases.confirmed_cases, where=where_array)
percentage = percentage*where_array*100

fig, ax1 = plt.subplots()

# ax1.set_ylim(bottom=0, top=1700)

ax1.plot(range(0, np.size(confirmed_cases.confirmed_cases)), confirmed_cases.confirmed_cases, '*', color='tab:red')
ax1.plot(confirmed_cases.deaths, color='tab:blue')

x_left, x_right = ax1.get_xlim()
# ax1.set_xlim([35, x_right])
ax1.xlabels(confirmed_cases.time_stamps)
# ax1.set_xticklabels(confirmed_cases.time_stamps, rotation=60, ha='right')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
# ax2.set_xlim(left=35)
# ax2.set_ylim([-0.5, 10])
# ax2.set_ylim(top=10)

ax2.plot(percentage, color='tab:green')
fig.tight_layout()
plt.show()
