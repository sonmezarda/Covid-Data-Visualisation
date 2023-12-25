from __future__ import annotations

import PyQt5.QtWidgets as qt
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QWidget

import pandas as pd

### My Qt Widgets
class MLabel(qt.QLabel):
    def __init__(self, text):
        super().__init__(text)

class MLineEdit(qt.QLineEdit):
    def __init__(self):
        super().__init__()

class MCheckBox(qt.QCheckBox):
    def __init__(self, text:str="checkbox"):
        super().__init__(text)

class MScrollArea(qt.QScrollArea):
    def __init__(self):
        super().__init__()

class MDateEdit(qt.QDateEdit):
    def __init__(self, currentdate=QtCore.QDateTime.currentDateTime()):
        super().__init__(calendarPopup=True)
        if type(currentdate) == QtCore.QDateTime:
            self.setDateTime(currentdate)
        elif type(currentdate) == QtCore.QDate:
            self.setDateTime(QtCore.QDateTime(currentdate))

class MPushButton(qt.QPushButton):
    def __init__(self, text:str="PUSH BUTTON"):
        super().__init__(text)

class MCombobox(qt.QComboBox):
    def __init__(self, selections:list[str]=None):
        super().__init__()
        if selections != None:
            self.addItems(selections)

# My custom QT Widgets
class SearchWidget(qt.QWidget):
    def __init__(self,lbltext:str):
        super().__init__()
        self.main_layout = qt.QHBoxLayout()
        self.label = MLabel(lbltext)
        self.lineEdit = MLineEdit()

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.lineEdit)
        self.setLayout(self.main_layout)
    
    def setSearchScroll(self):
        pass
        
class CountryCheckBox(MCheckBox):
    def __init__(self, countryName):
        super().__init__()
        self.countryName = countryName

        self.setText(countryName)

class CountryScroll(MScrollArea):
    def __init__(self, countries:list[str]|pd.DataFrame):
        super().__init__()
        self.countries = countries
        self.main_widget = qt.QWidget()
        self.main_layout = qt.QVBoxLayout()
        

        self.main_widget.setLayout(self.main_layout)

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        
        self.createCountryList()
        self.main_layout.addStretch()
    
    def reloadCountries(self, countries):
        self. countries = countries
        self.main_layout = qt.QVBoxLayout()
        self.createCountryList()
        
    def createCountryList(self):
        self.checkBoxList:list[CountryCheckBox] = list()
        
        for country in self.countries:
            Cbox = CountryCheckBox(country)
            self.checkBoxList.append(Cbox)
            self.main_layout.addWidget(Cbox)

    def filterCountries(self, countryName:str):
        for country in self.checkBoxList:
            if countryName.upper() in country.countryName.upper():
                country.setVisible(True)
            else:
                country.setVisible(False)
    
    def getCheckedCountries(self)->list[str]:
        checkedCountries = [country.countryName for country in self.checkBoxList if country.isChecked()]

        return checkedCountries

class GraphSettingForm(qt.QWidget):
    def __init__(self):
        super().__init__()

        formLayout = qt.QFormLayout()
        self.formLayout = formLayout
        self.startDate = MDateEdit(QtCore.QDate(2022,1,1))
        self.endDate = MDateEdit(QtCore.QDate(2022,1,1))
        self.dataMetric = MCombobox(["Confirmed Cases","Confirmed Deaths"])
        self.dataInterval = MCombobox(["New Per Day","Cumulative"])
        self.splitByCountry = MCheckBox()

        formLayout.addRow(MLabel('Start Date: '), self.startDate)
        formLayout.addRow(MLabel('End Date: '), self.endDate)
        formLayout.addRow(MLabel('Metric: '), self.dataMetric)
        formLayout.addRow(MLabel('Interval: '), self.dataInterval)
        formLayout.addRow(MLabel('Split by Country: '), self.splitByCountry)

        formLayout.addRow(MPushButton('Show Graph'))

        self.setLayout(self.formLayout)

    def getSettings(self):
        settings={}
        startDate = self.startDate.date()
        endDate = self.endDate.date()

        settings["startDate"] = f"{startDate.year()}-{startDate.month()}-{startDate.day()}" 
        settings["endDate"] = f"{endDate.year()}-{endDate.month()}-{endDate.day()}"
        settings["splitByCountry"] = self.splitByCountry.isChecked()

        if self.dataMetric.currentText() == "Confirmed Cases":
            if self.dataInterval.currentText() == "New Per Day":
                settings["column"] = "New_cases"
            elif self.dataInterval.currentText() == "Cumulative":
                settings["column"] = "Cumulative_cases"
        elif self.dataMetric.currentText() == "Confirmed Deaths":
            if self.dataInterval.currentText() == "New Per Day":
                settings["column"] = "New_deaths"
            elif self.dataInterval.currentText() == "Cumulative":
                settings["column"] = "Cumulative_deaths"
        else:
            settings["column"] = "error"
        
        return settings
