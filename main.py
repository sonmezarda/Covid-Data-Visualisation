from __future__ import annotations

from modules.covid_helper import test as covidTest
from modules.covid_helper import CovidHelper
from modules.plot_helper import test as pltTest
from modules.pyqt_helper import SearchWidget, CountryScroll, MDateEdit, MPushButton, MCombobox, GraphSettingForm
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as QtCore

def main():
    app = qt.QApplication([])
    covid = CovidHelper()
    #window = qt.QWidget()#MainWindow()
    window = MainWindow()
    #window.setLayout(ly)
    countryScroll = CountryScroll(covid.getCountryList())

    sw = SearchWidget("Country Name: ")
    sw.lineEdit.textChanged.connect(lambda: countryScroll.filterCountries(sw.lineEdit.text()))

    testButton = MPushButton("Test Button")
    gsettings = GraphSettingForm()


    window.main_layout.addWidget(sw, 1, 1)
    window.main_layout.addWidget(countryScroll, 2, 1)
    window.main_layout.addWidget(gsettings, 2,2)
    #window.main_layout.addWidget(startDate, 1, 2)

    window.main_layout.addWidget(testButton, 3,2)
    #window.main_layout.addWidget(caseSetting, 2,3) 
    testButton.clicked.connect(lambda: print(gsettings.getSettings()))

    window.show()
    app.exec()

class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Covid 19 Data Visualisation")
        self.central_widget = qt.QWidget()
        self.main_layout = qt.QGridLayout()

        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)
        
        # self.dateedit = qt.QDateEdit(calendarPopup=True)
        # self.menuBar().setCornerWidget(self.dateedit, QtCore.Qt.Corner.TopLeftCorner)
        # self.dateedit.setDateTime(QtCore.QDateTime.currentDateTime())


    def buttonClicked(self):
        print("Clicked!")



if __name__ == "__main__":
    main()
    