from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from modules.covid_helper import CovidHelper

class PlotHelper:
    def __init__(self):
        pass

    def plotBasic(self,ax:plt.Axes, df:pd.DataFrame, plotType:str="New_cases", dayTextInterval:int=10, **kwargs):
        #fig.autofmt_xdate()
        ax.grid()
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=dayTextInterval))
        intervalStr = "Per Day"
        for country in df["Country"].drop_duplicates():
            countryData = df[df["Country"] == country]
            if "Weekly" in plotType: 
                plotType=plotType.replace("Weekly_","")
                intervalStr = "Rolling Week"
                #countryData = countryData.set_index('Date_reported')
                y = countryData[plotType].rolling(7, min_periods=1).mean().round()

            else:
                y = countryData[plotType]
            ax.plot(countryData["Date_reported"], y, label=country,**kwargs)
            ax.set_xlim(0,len(y))
            ax.legend()
            yLabel = ' '.join(plotType.split('_')).capitalize() + f" ({intervalStr})"
            ax.set(xlabel="Date", ylabel=yLabel, title=f"{plotType.replace('_',' ').capitalize()} (From {countryData['Date_reported'].iloc[0]} to {countryData['Date_reported'].iloc[-1]})")

        return ax


def test():
    pltHelper = PlotHelper()
    cHelper = CovidHelper()
    df1 = cHelper.getDateIntervalbyCountry("2022-01-01", "2022-05-01", ["Türkiye","Germany"], dropIndex=True)

    fig, axs = plt.subplots(1,1)
    fig.autofmt_xdate()
    #pltHelper.plotBasic(axs[0],df,"Cumulative_cases")
    pltHelper.plotBasic(axs, df1, "Cumulative_cases")

    plt.show()


