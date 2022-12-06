# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 15:27:49 2022
@author: Aayush Jha
Assignment : Statistics and trend
"""
#Imports
import numpy as np
import pandas as pd
import scipy as sci
import matplotlib.pyplot as plt

""""""


def read_Data(fileName):
    df_Data1 = pd.read_csv(fileName)
    df_Data = trimData(df_Data1)
    df_dataTransposed = df_Data.T
    df_dataTransposed = cleanDataTrans(df_dataTransposed)
    return df_Data, df_dataTransposed

""""""

def cleanDataTrans(dataframe):
    dataframe.rename(columns=dataframe.loc["Country Name"], inplace=True)
    dataframe = dataframe.drop([ "Country Name"], axis=0)
    dataframe.index.name = "Year"
    return dataframe


""""""


def trimData(DatasetName):
    Countries = ['China', 'India', 'United States', 'United Kingdom', 'Germany',
                 'Brazil', 'Australia', 'South Africa']

    Indicators = ['CO2 emissions (kt)', 'Methane emissions (kt of CO2 equivalent)', 'Nitrous oxide emissions (thousand metric tons of CO2 equivalent)', 'Nitrous oxide emissions (% change from 1990)', 'Methane emissions (% change from 1990)',
                  'Population, total', 'Electricity production from renewable sources, excluding hydroelectric (% of total)', 'Electricity production from coal sources (% of total)', 'Forest area (sq. km)']

    trimmed_data = DatasetName[DatasetName['Country Name'].isin(Countries)]
    trimmed_data = trimmed_data[trimmed_data['Indicator Name'].isin(
        Indicators)]
    trimmed_data = trimmed_data.drop(
        ['Country Code', 'Indicator Code'], axis=1)
    trimmed_data = trimmed_data.drop(trimmed_data.iloc[:, trimmed_data.columns.get_loc(
        "1960"):trimmed_data.columns.get_loc("1989")], axis=1)
    return trimmed_data


""""""


def dataIndicator(Name):
   Dataframe = df_climateChange.loc[df_climateChange['Indicator Name']
                                    == Name]
   Dataframe = Dataframe.transpose()
   Dataframe.rename(columns=Dataframe.loc["Country Name"], inplace=True)
   Dataframe = Dataframe.drop(["Indicator Name", "Country Name"], axis=0)
   Dataframe["Year"] = Dataframe.index
   Dataframe.index.name = "Year"
   return Dataframe


""""""


def barPlotDataManp():

   Dataframe = dataIndicator(
       'Electricity production from coal sources (% of total)')
   Dataframe = Dataframe.iloc[:-6]
   Dataframe = Dataframe[::6]
   return Dataframe


""""""


def pieChartdatManu():
    Dataframe = dataIndicator('Population, total')
    Dataframe = Dataframe.iloc[[-1]].iloc[0:1, :-1]
    myLabels = np.array(Dataframe.columns)
    myExplode = [0.08,0.08 ,0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    Dataframe = np.array(Dataframe[:1].iloc[0])
    return Dataframe, myLabels, myExplode

""""""


def Scatterdatamanu():
    Dataframe =  df_climateChange.groupby(by=['Indicator Name']).mean()
    nitrous_change =np.array(Dataframe.iloc[6,2:24])
    methane_change = np.array(Dataframe.iloc[4,2:24])
    yearSeries = np.linspace(1991, 2012,22)
    return Dataframe,nitrous_change,methane_change,yearSeries

""""""


def plotdatamanu():
    Dataframe = dataIndicator('CO2 emissions (kt)')
    Dataframe = Dataframe.iloc[:-2].iloc[1:-1, 0:9]
    Dataframe = Dataframe[::3]
    return Dataframe


df_climateChange, df_climateChange_trans = read_Data('Data.csv')

#Barplot
df_elec = barPlotDataManp()
ax = df_elec.plot.bar(width=0.8)
ax.plot(rot=45, title="Consumption of coal in different country for electricity production(%)")
ax.legend(loc='center left', bbox_to_anchor=(1.0, .7))
plt.ylabel("Percentage of coal consumption")
plt.show()


#plot
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


#Piechart
plt.Figure()
df_pop, myLabels, myExplode = pieChartdatManu()
plt.pie(df_pop, shadow = True, labels=myLabels, explode=myExplode)
plt.show()

#Scatter
Dataframe,nitrous_change,methane_change,yearSeries = Scatterdatamanu()
plt.figure()
plt.scatter(yearSeries,nitrous_change,label='new', alpha=0.3, edgecolors='none')
plt.scatter(yearSeries,methane_change,label='old',alpha=0.9, edgecolors='none')
plt.legend(
           ('Nitrous Oxide', 'Methane'),
           scatterpoints=1,
           loc='upper right',
           ncol=3,
           fontsize=8)
plt.show()
