import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import sys

from read import read_cvs, CV19_data
from plot import plot_data

#TODO
#Read cvs files
#plot confirmed cases and total deaths
#predict confirmed cases based on total deaths

def create_cv19_objects(filename_conf, filename_deaths, countries=[], provinces=[], ig_provinces=[]):
    confirmed_cases = read_cvs(filename_conf, countries, provinces, ig_provinces)
    print(confirmed_cases)
    deaths = read_cvs(filename_deaths, countries, provinces, ig_provinces)
    i = 0
    for obj in confirmed_cases:
        obj.add_cases_death(deaths[i])
        i += 1

    return confirmed_cases

def func(t, a, b, c):
    return a*np.exp(t/b)+c

def doubling_cases(cv19_object):
    x_data = np.arange(np.size(cv19_object.confirmed_cases))
    popt, pcov = curve_fit(func, x_data, cv19_object.confirmed_cases, p0=[0.5, 2, 0])
    print(popt)
    d_time = popt[1]*np.log(2)
    return func(x_data, *popt), d_time

    #Fit exponential curve to data
    #From exponential function calculate days until the number of cases have doubled


def plot_death_percentage(cv19_object):
    where_array = cv19_object.deaths.astype(np.bool)
    percentage = np.divide(cv19_object.deaths, cv19_object.confirmed_cases, where=where_array)
    percentage = percentage*where_array*100

    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    plt1 = ax1.plot(range(0, np.size(cv19_object.confirmed_cases)), cv19_object.confirmed_cases, '*', color='tab:red')
    plt2 = ax1.plot(cv19_object.deaths, '*', color='tab:blue')
    
    plt.xticks(np.arange(np.size(cv19_object.time_stamps)), cv19_object.time_stamps, rotation=60, ha='right')
    plt.grid()
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    plt3 = ax2.plot(percentage, color='tab:green')
    fig.tight_layout()
    plt.legend([plt1, plt2, plt3], ['Confirmed cases', 'Confirmed deaths', 'Percentage of deaths and confirmed'], loc=2)
    plt.title('Percentage of deaths and confirmed cases for ' + cv19_object.country)
    plt.show()


def plot_double_days(obj_list):
    fig = plt.figure(figsize=(14, 8))
    for obj in obj_list:
        fit_curve, dtime = doubling_cases(obj)

        where_array = obj.deaths.astype(np.bool)
        plt.bar(obj.country, dtime)

        # plt.plot(fit_curve)
        
    #plt.legend([plt1, plt2, plt3], ['Confirmed cases', 'Confirmed deaths', 'Percentage of deaths and confirmed'], loc=2)
    
    plt.title('Number of days until confirmed cases have doubled')
    plt.show()


def plot_curve_fit(cv19_objects):
    fig = plt.figure(figsize=(14, 8))
    for obj in cv19_objects:
        fit_curve, dtime = doubling_cases(obj)
        c=np.random.rand(3,)
        where_array = obj.deaths.astype(np.bool)
        plt.plot(range(0, np.size(obj.confirmed_cases)), obj.confirmed_cases, '*', label=obj.country, c=c)
        plt.plot(fit_curve)
        
    #plt.legend([plt1, plt2, plt3], ['Confirmed cases', 'Confirmed deaths', 'Percentage of deaths and confirmed'], loc=2)
    plt.grid()
    # plt.yscale('log')
    plt.legend(loc=2)
    plt.xticks(np.arange(np.size(cv19_objects[0].time_stamps)), cv19_objects[0].time_stamps, rotation=60, ha='right')
    plt.title('Exponential curve fitted on confirmed cases')
    plt.show()


countries = ['Sweden', 'Norway', 'Denmark', 'Iceland']
# countries = ['US']
provinces = []
path = '../csse_covid_19_data/csse_covid_19_time_series/'
obj_list = create_cv19_objects(path+'time_series_covid19_confirmed_global.csv', path+'/time_series_covid19_deaths_global.csv', countries=countries, provinces=provinces)

#plot_death_percentage(obj_list[0])
# plot_double_days(obj_list)
plot_curve_fit(obj_list)