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

class MSpinBox(qt.QSpinBox):
    def __init__(self, min:int=0, max:int=0, start:int=0):
        super().__init__()
        self.setMinimum(min)
        self.setMaximum(max)
        self.setValue(start)

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
            if(type(country) != str): continue
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
        checkedCountries = [country.countryName.split(' - ')[0] for country in self.checkBoxList if country.isChecked()]

        return checkedCountries

class GraphSettingForm(qt.QWidget):
    def __init__(self):
        super().__init__()

        formLayout = qt.QFormLayout()
        self.formLayout = formLayout
        self.startDate = MDateEdit(QtCore.QDate(2021,6,1))
        self.endDate = MDateEdit(QtCore.QDate(2022,1,1))
        self.dataMetric = MCombobox(["Confirmed Cases","Confirmed Deaths"])
        self.dataInterval = MCombobox(["New Per Day","Cumulative", "Weekly"])
        self.splitByCountry = MCheckBox("")
        self.alignAxisScales = MCheckBox("")
        self.markerType = MCombobox(["Circle - o","None","Star - *", "Point - .", "Pixel - ,", "X - x", "Plus - +", "Plus (Filled) - P", "Square - s", "Hexagon - H"])
        self.markerSize = MSpinBox(0,10,3)
        self.showGraphButton = MPushButton('Show Graph')
        self.dateTextInterval = MSpinBox(1,30,7)

        pltSettingsLbl = MLabel('Plot Settings')
        pltSettingsLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        formLayout.addRow(MLabel('Start Date: '), self.startDate)
        formLayout.addRow(MLabel('End Date: '), self.endDate)
        formLayout.addRow(MLabel('Metric: '), self.dataMetric)
        formLayout.addRow(MLabel('Interval: '), self.dataInterval)
        formLayout.addRow(MLabel('Split by Country: '), self.splitByCountry)
        formLayout.addRow(MLabel('Align Axis Scales: '), self.alignAxisScales)
        
        formLayout.addRow(pltSettingsLbl)
        formLayout.addRow(MLabel('Marker Type: '), self.markerType)
        formLayout.addRow(MLabel('Marker Size: '), self.markerSize)
        formLayout.addRow(MLabel('X axis Date Interval: '), self.dateTextInterval)
        
        formLayout.addRow(self.showGraphButton)

        self.setLayout(self.formLayout)

    def getSettings(self):
        settings={}
        startDate = self.startDate.date()
        endDate = self.endDate.date()

        settings["startDate"] = f"{startDate.year()}-{startDate.month():02d}-{startDate.day():02d}" 
        settings["endDate"] = f"{endDate.year()}-{endDate.month():02d}-{endDate.day():02d}"
        settings["splitByCountry"] = self.splitByCountry.isChecked()

        settings["column"] = ""
        if self.dataInterval.currentText() == "New Per Day":
            settings["column"] = "New"
        elif self.dataInterval.currentText() == "Cumulative":
            settings["column"] = "Cumulative"
        elif self.dataInterval.currentText() == "Weekly":
            settings["column"] = "Weekly_New"

        if self.dataMetric.currentText() == "Confirmed Cases":
            settings["column"]+="_cases"
        elif self.dataMetric.currentText() == "Confirmed Deaths":
            settings["column"]+="_deaths"

        
        if self.markerType.currentText() == "None":
            settings["marker"] = None
        else:
            settings["marker"] = self.markerType.currentText()[-1]

        settings["markerSize"] = self.markerSize.value()
        settings["dateInterval"] = self.dateTextInterval.value()
        
        print(settings)
        return settings
    
### Errors

def showError(errormsg):
    dialog = qt.QDialog()
    dialog.setWindowTitle("ERROR")
    dialog.exec()

