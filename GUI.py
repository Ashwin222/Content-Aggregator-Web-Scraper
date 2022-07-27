import sqlite3
import sys
import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QLabel
from PyQt5.uic import loadUi

from IBM_Blockchain import *
from Hacker_News import *
from KD_Nuggets import *
from Brookings_Research import *
from CIO import *
from Motley_Fool import *
from IT_Security_Guru import *
from TechCrunch import *
from Gartner_Research import *
from AQR_Capital import *

class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setParent(parent)
        self.link_string = None

    def mouseDoubleClickEvent(self, event):
        webbrowser.open(self.link_string)


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("article_table.ui", self)
        self.tableWidget.setColumnWidth(0, 400)
        self.tableWidget.setColumnWidth(1, 600)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 140)
        self.loaddata()

    def loaddata(self):
        # define connection to the SQLite database
        connection = sqlite3.connect('articles.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM articles")
        results = cursor.fetchall()
        linkTemplate = '<a href={0}>{1}</a>'
        row = 0
        self.tableWidget.setRowCount(len(results))
        for article in results:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(article[0]))
            label = HyperlinkLabel(self)
            label.link_string = article[1]
            label.setText(linkTemplate.format(article[1], article[1]))
            self.tableWidget.setCellWidget(row, 1, label)
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(article[2]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(article[3]))
            row = row + 1
        connection.close()


# main

# run the web scrapers
IBM_Blockchain()
Hacker_News()
KD_Nuggets()
Brookings_Research()
CIO()
Motley_Fool()
IT_Security_Guru()
TechCrunch()
Gartner_Research()
AQR_Capital()

# run the UI

app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(900)
widget.setFixedWidth(1800)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
