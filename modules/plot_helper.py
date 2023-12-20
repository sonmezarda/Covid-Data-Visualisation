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
        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        for country in df["Country"].drop_duplicates():
            print(df)
            countryData = df[df["Country"] == country]
            lenght = countryData.shape[0]
            #x = np.arange(0, lenght, 1)
            y = countryData[plotType]
            ax.plot(countryData["Date_reported"], y, label=country,**kwargs)
            ax.legend()
            yLabel = ' '.join(plotType.split('_')).capitalize() + " (Per Day)"
            ax.set(xlabel="Date", ylabel=yLabel, title=f"New Cases (From {countryData['Date_reported'].iloc[0]} to {countryData['Date_reported'].iloc[-1]})")

        return ax


def test():
    pltHelper = PlotHelper()
    cHelper = CovidHelper()
    df = cHelper.getbyCountry(["Türkiye", "Iran (Islamic Republic of)"], dropIndex=True)
    fig, axs = plt.subplots(1,1)
    fig.autofmt_xdate()
    #pltHelper.plotBasic(axs[0],df,"Cumulative_cases")
    pltHelper.plotBasic(axs, df, "New_cases")

    plt.show()


