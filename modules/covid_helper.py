from __future__ import annotations
from typing import Any
import numpy
import pandas as pd
import requests
import asyncio
import datetime
import os
import time

class CovidConstants:
    allDataUrl = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    allDataName = "data/WHO-COVID-19-global-data.csv"
    tableDataUrl = "https://covid19.who.int/WHO-COVID-19-global-table-data.csv"
    vaccinationDataUrl = "https://covid19.who.int/who-data/vaccination-metadata.csv"

class CovidHelper:
    def __init__(self):
        self.global_data = pd.DataFrame()

    @staticmethod
    def checkGlobalData(function):
        def wrapper(self:CovidHelper, *args, **kwargs):
            if self.global_data.empty:
                self.loadGlobalData()
            return function(self, *args, **kwargs)
        return wrapper

    def loadGlobalData(self, reDownload=False) -> None:
        if not reDownload:
            self.global_data = CovidHelper.getCSV(CovidConstants.allDataName)
        else:
            CovidHelper.downloadData(CovidConstants.allDataUrl, CovidConstants.allDataName)
            self.loadGlobalData()

    @checkGlobalData
    def getGlobalData(self) -> pd.DataFrame:
        return self.global_data

    @checkGlobalData
    def getCountryList(self, dropIndex:bool=True) -> pd.DataFrame:
        return self.global_data["Country"].drop_duplicates().reset_index(drop=dropIndex)

    @checkGlobalData
    def getCountryData(self, country:str, dropIndex:bool=True) -> pd.DataFrame:
        return self.global_data[self.global_data["Country"]==country].reset_index(drop=dropIndex)

    @checkGlobalData
    def getDateData(self, date:str|datetime.date, dropIndex:bool=True) -> pd.DataFrame:
        if type(date) == datetime.date:
            return self.global_data[self.global_data["Date_reported"] == str(date)].reset_index(drop=dropIndex)
        elif type(date) == str:
            return self.global_data[self.global_data["Date_reported"] == date].reset_index(drop=dropIndex)

    @checkGlobalData
    def getCountryDateData(self, date:str|datetime.date, country:str, dropIndex:bool=True) -> pd.DataFrame:
        global_data = self.global_data
        return global_data[
            (global_data["Date_reported"] == str(date))&(global_data["Country"] == country)
            ].reset_index(drop=dropIndex)

    @checkGlobalData
    def getDateIntervalbyCountry(self, startDate:str|datetime.date, endDate:str|datetime.date, country:str|list[str]="ALL", dropIndex:bool=True):
        if type(country) == str and country == "ALL":
            return self.global_data.query(f"Date_reported >= '{str(startDate)}'").query(f"Date_reported <= '{str(endDate)}'")

        if type(country) == str:
            countryData = self.getCountryData(country, dropIndex=False)
            if countryData.empty:
                return countryData
            
            return countryData.query(f"Date_reported >= '{str(startDate)}'").query(f"Date_reported <= '{str(endDate)}'").reset_index(drop=dropIndex)
        
        if type(country) == list:
            df = pd.DataFrame()
            for c in country:
                countryData = self.getCountryData(c, dropIndex=False)
                if countryData.empty:
                    continue
                firstDateIndex = countryData[countryData["Date_reported"] == str(startDate)].iloc[0]["index"]
                lastDateIndex = countryData[countryData["Date_reported"] == str(endDate)].iloc[0]["index"]
                frames = [df, self.global_data.loc[firstDateIndex:lastDateIndex]]
                df = pd.concat(frames)
            return df


    @staticmethod
    def downloadData(url:str, path:str) -> bool:
        query_parameters = {"downloadformat":"csv"}
        print("Downloading...")
        response = requests.get(url, params=query_parameters)
        if not response.ok:
            print("Download Failed")
            return False
        print("Download Successful. File Saving...")
        with open(path, mode="wb") as file:
            file.write(response.content)

        return True

    @staticmethod
    def getCSV(path, url=CovidConstants.allDataUrl) -> pd.DataFrame:
        if os.path.exists(path):
            return pd.read_csv(path)

        res = CovidHelper.downloadData(url, path)
        if res:
            return pd.read_csv(path)
        else:
            raise FileNotFoundError("CSV File Not Found and Could Not be Downloaded")

    def buf():
        pass



def test():
    CovC = CovidConstants
    cHelper = CovidHelper()
    print("Loading...")
    st = time.time()
    df = cHelper.getDateIntervalbyCountry(datetime.date(2022, 10, 1), datetime.date(2022, 11, 1), "Yemen")
    ft = time.time()
    print(f"Time1: {ft-st}")
    print(df)


    #print(d)


if __name__ == "__main__":
    test()