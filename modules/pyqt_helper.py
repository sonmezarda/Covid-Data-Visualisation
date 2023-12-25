from __future__ import annotations

import PyQt5.QtWidgets as qt

### My Qt Widgets

class MLabel(qt.QLabel):
    def __init__(self, text):
        super().__init__(text)

class MLineEdit(qt.QLineEdit):
    def __init__(self):
        super().__init__()

class MCheckBox(qt.QCheckBox):
    def __init__(self):
        super().__init__()

# My custom QT Widgets
        
class SearchWidget(qt.QWidget):
    def __init__(self,lbltext:str):
        super().__init__()
        self.main_layout = qt.QHBoxLayout()
        self.label = MLabel(lbltext)
        self.searchLineEdit = MLineEdit()

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.searchLineEdit)
        self.setLayout(self.main_layout)
        
class CountryCheckBox(MCheckBox):
    def __init__(self, countryName):
        super().__init__()
        self.countryName = countryName

        self.setText(countryName)
