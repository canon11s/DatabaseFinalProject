# GUI for Fantasy Premier League Toolkit

#Necessary libraries
import sys
import FilterSelection, PlayerDisplay
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import mysql.connector
import os.path

resourcesPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/resources/'

#Class for the main window
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        #Properties of the window
        self.title = "Fantasy Premier League Toolkit"
        self.setGeometry(100, 100, 1200, 600)

        #Establish connection to database
        self.database = mysql.connector.connect(
            host="localhost",
            user="databaseProject",
            passwd="password",
            database="soccer"
        )
        self.cursor = self.database.cursor()

        #Initialize UI
        self.initUI()
        self.show()

    #Method to initialize components of the main window UI
    def initUI(self):
        #Create the main frame - this will be the focus of the application - set as central widget
        self.mainF = QFrame(self)
        self.setCentralWidget(self.mainF)
        #Create a HBoxLayout to separate user input and player tables
        self.mainL = QHBoxLayout(self.mainF)


        #Search button to run search and find players
        searchButton = QPushButton(text="Search")
        searchButton.clicked.connect(self.searchClick)

        #Create an instance of a 'FilterSelection' object - this will handle the user writing a query to DB
        self.userInput = FilterSelection.FilterSelection(searchButton)

        #Create an instance of 'PlayerDisplay' object - this will handle populating display tables
        self.tableDisplay = PlayerDisplay.PlayerDisplay()

        #Add the frames to the main layout
        self.mainL.addWidget(self.userInput.returnWidget(), 1)
        self.mainL.addWidget(self.tableDisplay.returnWidget(), 4)
        #Show!
        self.show()

    def searchClick(self):
        queryString = self.userInput.buildQuery()
        self.cursor.execute(queryString)
        self.tableDisplay.fillTable(self.cursor)


#A function to set up the color scheme of the window
def createDarkPalette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(75, 78, 109))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(34, 34, 34))
    palette.setColor(QPalette.AlternateBase, QColor(75, 78, 109))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(75, 78, 109))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    palette.setColor(QPalette.ButtonText, Qt.black)
    return palette


if __name__ == '__main__':
    app = QApplication([])
    app.setPalette(createDarkPalette())
    app.setWindowIcon(QIcon(resourcesPath + 'newIcon.png'))
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
