# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 15:27:49 2022
@author: Aayush Jha
Assignment : Statistics and trend
"""
# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Function to read and transpose the file
def read_Data(fileName):
    """This Function read the data from the csv file,Clean the data to make
    it usable and transpose the data,transposed data further get cleaned to
    include as needed"""
    df_Data1 = pd.read_csv(fileName)
# using trimData function to remove unwanted data
    df_Data = trimData(df_Data1)
    df_dataTransposed = df_Data.T
    df_dataTransposed = cleanDataTrans(df_dataTransposed)
    return df_Data, df_dataTransposed


# Function to  clean the transposed data
def cleanDataTrans(dataframe):
    """This Function cleans the transposed data by removing unwanted header
    and change it to use country name and use year as index"""
    dataframe.rename(columns=dataframe.loc["Country Name"], inplace=True)
    dataframe = dataframe.drop(["Country Name"], axis=0)
    dataframe.index.name = "Year"
    return dataframe


# Function to trim the data in a good format
def trimData(DatasetName):
    """This function removes the unwanted data from the dataframe and return
    only usable countries and indicators"""
    Countries = ['China', 'India', 'United States', 'United Kingdom',
                 'Germany',
                 'Brazil', 'Australia', 'South Africa']

    Indicators = ['CO2 emissions (kt)',
                  'Methane emissions (kt of CO2 equivalent)',
                  'Nitrous oxide emissions (thousand metric tons of CO2 equivalent)',
                  'Nitrous oxide emissions (% change from 1990)',
                  'Methane emissions (% change from 1990)',
                  'Population, total', 'Electricity production from renewable sources, excluding hydroelectric (% of total)',
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
    """This Function return the data besad on the indicator name
    passed"""
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
    """This Function manupulates the data used to plot bar graphs"""
    Dataframe = dataIndicator(
       'Electricity production from coal sources (% of total)')
    Dataframe = Dataframe.iloc[:-6]
    Dataframe = Dataframe[::6]
    return Dataframe


# Function used for Pie graph
def pieChartdatManu():
    """This function manupulates the data used to Pie Chart graphs"""
    Dataframe = dataIndicator('Population, total')
    Dataframe = Dataframe.iloc[[-1]].iloc[0:1, :-1]
    myLabels = np.array(Dataframe.columns)
    myExplode = [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    Dataframe = np.array(Dataframe[:1].iloc[0])
    return Dataframe, myLabels, myExplode


# Function used for scatter plot
def Scatterdatamanu():
    Dataframe = df_climateChange.groupby(by=['Indicator Name']).mean()
    nitrous_change = np.array(Dataframe.iloc[6, 2:24])
    methane_change = np.array(Dataframe.iloc[4, 2:24])
    yearSeries = np.linspace(1991, 2012, 22)
    return Dataframe, nitrous_change, methane_change, yearSeries


# Function used for plot
def plotdatamanu():
    """This function manupulates the data used to plot"""
    Dataframe = dataIndicator('CO2 emissions (kt)')
    Dataframe = Dataframe.iloc[:-2].iloc[1:-1, 0:9]
    Dataframe = Dataframe[::3]
    return Dataframe


# Reading the data by using read data function
df_climateChange, df_climateChange_trans = read_Data('Data.csv')


# Barplot
# Using bar plot method to get all the required data for bar plot
df_elec = barPlotDataManp()
ax = df_elec.plot.bar(width=0.8)
title = 'coal Consumption in different country for electricity production(%)'
ax.plot(rot=45, title=title)
ax.legend(loc='center left', bbox_to_anchor=(1.0, .7))
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
plt.title("C02 consumption by countries for period of 1989-2017")
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
plt.scatter(yearSeries, nitrous_change, label='new',
            alpha=0.3, edgecolors='none')
plt.scatter(yearSeries, methane_change, label='old',
            alpha=0.9, edgecolors='none')
plt.title("Mean of changes in use of nitrous oxide and methane over the period of 1991-2012(%)")
plt.ylabel('Change in Percentage')
plt.xlabel('Year')
plt.legend(
    ('Nitrous Oxide', 'Methane'),
    scatterpoints=1,
    loc='upper right',
    ncol=3,
    fontsize=8)
plt.show()
