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

def create_cv19_objects(filename_conf, filename_deaths, countries=[], provinces=[]):
    confirmed_cases = read_cvs(path+'time_series_19-covid-Confirmed.csv', countries, provinces)
    print(confirmed_cases)
    deaths = read_cvs(path+'/time_series_19-covid-Deaths.csv', countries, provinces)
    i = 0
    for obj in confirmed_cases:
        obj.add_cases_death(deaths[i])
        i += 1

    return confirmed_cases

path = '../csse_covid_19_data/csse_covid_19_time_series/'
obj_list = create_cv19_objects(path+'time_series_19-covid-Confirmed.csv', path+'/time_series_19-covid-Deaths.csv', countries=['Spain'])[0]

where_array = obj_list.deaths.astype(np.bool)

percentage = np.divide(obj_list.deaths, obj_list.confirmed_cases, where=where_array)
percentage = percentage*where_array*100

fig, ax1 = plt.subplots(figsize=(16, 12))

# ax1.set_ylim(bottom=0, top=1700)

ax1.plot(range(0, np.size(obj_list.confirmed_cases)), obj_list.confirmed_cases, '*', color='tab:red')
ax1.plot(obj_list.deaths, '*', color='tab:blue')

x_left, x_right = ax1.get_xlim()
# ax1.set_xlim([35, x_right])
plt.xticks(np.arange(np.size(obj_list.time_stamps)), obj_list.time_stamps, rotation=60, ha='right')
plt.grid()
# ax1.xlabels(confirmed_cases.time_stamps)
# ax1.set_xticklabels(confirmed_cases.time_stamps, rotation=60, ha='right')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
# ax2.set_xlim(left=35)
# ax2.set_ylim([-0.5, 10])
# ax2.set_ylim(top=1.5)

ax2.plot(percentage, color='tab:green')
fig.tight_layout()
plt.show()
