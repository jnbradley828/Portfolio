import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

def draw_plot():
    # Read data from file
    data = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10,6))
    plt.scatter(x=data['Year'], y=data['CSIRO Adjusted Sea Level'])

    # Create first line of best fit
    regLine = linregress(x=data['Year'], y = data['CSIRO Adjusted Sea Level'])
    yearsExtended = np.arange(1880, 2051)
    bfLine1 = regLine.slope * yearsExtended + regLine.intercept
    plt.plot(yearsExtended, bfLine1, color='red')

    # Create second line of best fit
    dataSince2000 = data.loc[data['Year'] >= 2000]
    regLine2 = linregress(x=dataSince2000['Year'], y = dataSince2000['CSIRO Adjusted Sea Level'])
    years2 = np.arange(2000, 2051)
    bfLine2 = regLine2.slope * years2 + regLine2.intercept
    plt.plot(years2, bfLine2, color='green')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()