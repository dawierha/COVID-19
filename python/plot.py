import numpy as np
import matplotlib.pyplot as plt

from read import CV19_data

def plot_data(cv19_object):
    plt.plot(cv19_object.confirmed_cases)
    plt.plot(cv19_object.deaths)
    plt.show()