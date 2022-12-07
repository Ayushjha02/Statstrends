# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 15:27:49 2022.

@author: Ayush Jha
@Student Id: 21063203
Assignment : Statistics and trend
"""
# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sci


# Function to read and transpose the file
def read_Data(fileName):
    """
    Read,Clean and Transpose.

    function read the data from the csv file,Clean the data to make
    it usable and transpose the data.transposed data further get cleaned to
    include header as needed
    """
    df_Data1 = pd.read_csv(fileName)
# using trimData function to remove unwanted data
    df_Data = trimData(df_Data1)
    df_dataTransposed = df_Data.T
    df_dataTransposed = cleanDataTrans(df_dataTransposed)
    return df_Data, df_dataTransposed


# Function to  clean the transposed data
def cleanDataTrans(dataframe):
    """
    Clean the transposed data.

    function clean the data by removing unwanted header
    and change it to use country name and use year as index
    """
    dataframe.rename(columns=dataframe.loc["Country Name"], inplace=True)
    dataframe = dataframe.drop(["Country Name"], axis=0)
    dataframe.index.name = "Year"
    return dataframe


# Function to trim the data in a good format
def trimData(DatasetName):
    """
    Remove the unwanted data.

    return only usable countries and indicators
    """
    Countries = ['China', 'India', 'United States', 'United Kingdom',
                 'Germany',
                 'Brazil', 'Australia', 'South Africa']

    Indicators = ['CO2 emissions (kt)',
                  'Nitrous oxide emissions (% change from 1990)',
                  'Methane emissions (% change from 1990)',
                  'Population, total',
                  'Electricity production from coal sources (% of total)',
                  'Forest area (sq. km)']

    trimmed_data = DatasetName[DatasetName['Country Name'].isin(Countries)]
    trimmed_data = trimmed_data[trimmed_data['Indicator Name'].isin(
        Indicators)]
    trimmed_data = trimmed_data.drop(
        ['Country Code', 'Indicator Code'], axis=1)
    drop_data = trimmed_data.iloc[:, trimmed_data.columns.get_loc(
        "1960"):trimmed_data.columns.get_loc("1989")]
    trimmed_data = trimmed_data.drop(drop_data, axis=1)
    return trimmed_data


# Function to fetch data besad on data indicator
def dataIndicator(Name):
    """Return the data besad on the indicator name."""
    Dataframe = df_climateChange.loc[df_climateChange['Indicator Name']
                                     == Name]
    Dataframe = Dataframe.transpose()
    Dataframe.rename(columns=Dataframe.loc["Country Name"], inplace=True)
    Dataframe = Dataframe.drop(["Indicator Name", "Country Name"], axis=0)
    Dataframe["Year"] = Dataframe.index
    Dataframe.index.name = "Year"
    return Dataframe


# Function used for bar graph
def barPlotDataManp():
    """
    Manupulates the data for appropriate graph.

    Function used to get all the parameters require to plot bar graphs
    """
    Dataframe = dataIndicator(
        'Electricity production from coal sources (% of total)')
    Dataframe = Dataframe.iloc[:-6]
    Dataframe = Dataframe[::6]
    return Dataframe


# Function used for Pie graph
def pieChartdatManu():
    """
    Manupulates the data for appropriate graph.

    Function used to fetch all the data for Pie Chart graphs.
    """
    Dataframe = dataIndicator('Population, total')
    Dataframe = Dataframe.iloc[[-1]].iloc[0:1, :-1]
    myLabels = np.array(Dataframe.columns)
    myExplode = [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    Dataframe = np.array(Dataframe[:1].iloc[0])
    return Dataframe, myLabels, myExplode


# Function used for scatter plot
def Scatterdatamanu():
    """
    Manupulates the data for appropriate graph.

    function uses mean method to get the mean for all indicator grouped
    by and then return the data useful to plot scatter
    """
    Dataframe = df_climateChange.groupby(by=['Indicator Name']).mean()
    nitrous_change = np.array(Dataframe.iloc[4, 2:24])
    methane_change = np.array(Dataframe.iloc[3, 2:24])
    yearSeries = np.linspace(1991, 2012, 22)
    return Dataframe, nitrous_change, methane_change, yearSeries


# Function used for plot
def plotdatamanu():
    """
    Manupulates the data for appropriate graph.

    Function to manupulate the data used to plot graph
    """
    Dataframe = dataIndicator('CO2 emissions (kt)')
    Dataframe = Dataframe.iloc[:-2].iloc[1:-1, 0:9]
    Dataframe = Dataframe[::3]
    return Dataframe


# Reading the data by using read data function
df_climateChange, df_climateChange_trans = read_Data('Data.csv')


# Barplot(using pandas dataframe method)
# Using pandas bar plot method to get all the required data for bar plot
df_elec = barPlotDataManp()
ax = df_elec.plot.bar(width=0.8)
title = 'coal Consumption in different country for electricity production(%)'
ax.plot(rot=45, title=title)
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.7))
plt.ylabel("Percentage of coal consumption")
plt.show()


# plot
# Using plotdatamanu method to get all the required data for plot
df_co2 = plotdatamanu()
plt.Figure(figsize=(12, 12))
plt.plot(df_co2["Year"], df_co2["India"], label="India")
plt.plot(df_co2["Year"], df_co2["China"], label="China")
plt.plot(df_co2["Year"], df_co2["United States"], label="US")
plt.plot(df_co2["Year"], df_co2["United Kingdom"], label="UK")
plt.plot(df_co2["Year"], df_co2["Brazil"], label="Brazil")
plt.plot(df_co2["Year"], df_co2["Australia"], label="Australia")
plt.plot(df_co2["Year"], df_co2["South Africa"], label="South Africa")
plt.plot(df_co2["Year"], df_co2["Germany"], label="Germany")
plt.xlabel("Year")
plt.ylabel("CO2 Consumption")
plt.title("CO2 emissions (kt) by countries for period of 1989-2017")
plt.legend(loc=2, prop={'size': 7})
plt.show()


# PiePlot
# Using pieChartdatManu function which returns data useful for pie chart
df_pop, myLabels, myExplode = pieChartdatManu()
plt.Figure()
plt.pie(df_pop, shadow=True, labels=myLabels, explode=myExplode)
plt.title("Population of each country in year 2021")
plt.show()


# Scatter
# Using Scatterdatamanu function which returns data useful for scatters
Dataframe, nitrous_change, methane_change, yearSeries = Scatterdatamanu()
plt.figure()
plt.scatter(yearSeries, nitrous_change,
            alpha=0.5, edgecolors='none')
plt.scatter(yearSeries, methane_change,
            alpha=0.9, edgecolors='none')
plt.title('Mean of changes in emissions of nitrous oxide and methane over the'
          ' period of 1991-2012(%)')
plt.ylabel('Change in Percentage -->')
plt.xlabel('Year -->')
plt.legend(
    ('Nitrous Oxide', 'Methane'),
    scatterpoints=1,
    loc='upper right',
    ncol=3,
    fontsize=8)
plt.show()


# heatmap
df_frame = df_climateChange[df_climateChange['Country Name']=='China']
df_frame = df_frame.iloc[:,4:26]
