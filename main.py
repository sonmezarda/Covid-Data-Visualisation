from __future__ import annotations

import matplotlib.pyplot as plt
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as QtCore

from modules.covid_helper import test as covidTest
from modules.plot_helper import test as pltTest

from modules.covid_helper import CovidHelper
from modules.plot_helper import PlotHelper

from modules.pyqt_helper import SearchWidget, CountryScroll,  MPushButton, GraphSettingForm


def main():
    app = qt.QApplication([])
    covid = CovidHelper()
    window = MainWindow()
    countryScroll = CountryScroll(covid.getCountryList(True, True))

    sw = SearchWidget("Country Name: ")
    sw.lineEdit.textChanged.connect(lambda: countryScroll.filterCountries(sw.lineEdit.text()))

    testButton = MPushButton("Test Button")
    gsettings = GraphSettingForm()


    window.main_layout.addWidget(sw, 1, 1)
    window.main_layout.addWidget(countryScroll, 2, 1)
    window.main_layout.addWidget(gsettings, 2,2)

    window.main_layout.addWidget(testButton, 3,2)
    gsettings.showGraphButton.clicked.connect(lambda: 
                                              showGraphButtonClick(gsettings.getSettings(), countryScroll.getCheckedCountries()))

    window.show()
    app.exec()

def showGraphButtonClick(settings, countries):
    covid = CovidHelper()
    plotter = PlotHelper()
    covid.loadGlobalData()

    if not settings["splitByCountry"]:
        df = covid.getDateIntervalbyCountry(settings["startDate"], settings["endDate"], countries, dropIndex=True)
        fig, ax = plt.subplots(1,1)
        fig.autofmt_xdate()
        plotter.plotBasic(ax, df, plotType=settings["column"], dayTextInterval=settings["dateInterval"], linewidth=settings["lineWidth"], marker=settings["marker"], ms=settings["markerSize"])
        plt.show()

class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Covid 19 Data Visualisation")
        self.central_widget = qt.QWidget()
        self.main_layout = qt.QGridLayout()

        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)

if __name__ == "__main__":
    main()
    