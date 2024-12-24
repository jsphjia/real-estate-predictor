#########################
# This file implements gradient descent to determine optimal solution.
#########################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def import_data(city):
    file_name = city + "-sold.txt"
    cols = ['beds', 'baths', 'sq', 'area', 'sold_date', 'sold_price']
    file_info = pd.read_csv(file_name, sep=',', names=cols)
    plot_data(file_info)
    return

def create_batches():
    return

def gradient_descent():
    return

def plot_data(data):
    plt.scatter(data['beds'], data['sold_price'])
    plt.xlim([0, 10])
    plt.ylim([0, 10000000])
    plt.xlabel('Bedrooms')
    plt.ylabel('Sold Price')
    plt.title('Bedrooms v. Sold Price')
    plt.show()
    return