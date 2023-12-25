from __future__ import annotations

from modules.covid_helper import test as covidTest
from modules.covid_helper import CovidHelper
from modules.plot_helper import test as pltTest
from modules.pyqt_helper import SearchWidget, CountryCheckBox
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as QtCore

def main():
    app = qt.QApplication([])
    covid = CovidHelper()
    #window = qt.QWidget()#MainWindow()
    window = MainWindow()
    #window.setLayout(ly)
    countryScroll = getCountryScroll(["a","b","c","d"])


    sw = SearchWidget("Country Name: ")

    window.main_layout.addWidget(sw, 1, 1)
    window.main_layout.addWidget(countryScroll, 2, 1)
    # window.setLayout(layout)

    window.show()
    app.exec()
    #pltTest()


def createCountryList(countries) -> list[CountryCheckBox]:
    checkBoxList = list()
    formLayout = qt.QFormLayout()
    for country in countries:
        Cbox = CountryCheckBox(country)
        checkBoxList.append(Cbox)
        formLayout.addRow(Cbox)
    
    return formLayout

def getCountryScroll(countries):
    formLayout = createCountryList(countries)
    scroll = qt.QScrollArea()
    
    w = qt.QWidget()
    w.setLayout(formLayout)
    scroll.setWidget(w)
    scroll.setWidgetResizable(True)
    scroll.main_layout = formLayout
    return scroll



class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Covid 19 Data Visualisation")
        self.central_widget = qt.QWidget()
        self.main_layout = qt.QGridLayout()

        self.main_layout.addWidget(qt.QPushButton("test2"),2,2)
        self.main_layout.addWidget(qt.QPushButton("test3"),1,3)
        

        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)
        
        # self.dateedit = qt.QDateEdit(calendarPopup=True)
        # self.menuBar().setCornerWidget(self.dateedit, QtCore.Qt.Corner.TopLeftCorner)
        # self.dateedit.setDateTime(QtCore.QDateTime.currentDateTime())


    def buttonClicked(self):
        print("Clicked!")



if __name__ == "__main__":
    main()
    