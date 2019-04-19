# Canon Sawrey
# Created: Jan. 6 2018
# Updated: Feb. 11 2019
# GUI for Fantasy Premier League Toolkit

#Necessary libraries
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import mysql.connector
import os.path

resourcesPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/lib/resources/'

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
            database="prem"
        )

        self.cursor = self.database.cursor()

        #Declare tables to be filled by database
        self.fantraxTable = QTableWidget()

        #Initialize UI
        self.initUI()
        self.show()


    def initUI(self):

        #Create the main frame
        self.mainF = QFrame(self)
        self.setCentralWidget(self.mainF)

        #Create a HBoxLayout to separate user input and player tables
        self.mainL = QHBoxLayout(self.mainF)

        #Create the user input frame
        userInputF = QFrame(self.mainF)
        #Create the user input layout to be inside the frame
        userInputL = QVBoxLayout(userInputF)
        #Add the position select box
        userInputL.addWidget(self.createPositionBox())
        #Add the FA/Waiver select box
        userInputL.addWidget(self.createAvailabilityTypeBox())
        #Add the team select box
        userInputL.addWidget(self.createTeamSelectBox())
        #Add the sort algorithm
        userInputL.addWidget(self.createAlgorithmBox())
        #Search button to run search and find players
        searchButton = QPushButton(text="Search")
        userInputL.addWidget(searchButton)
        #Connect search button with clicked command
        searchButton.clicked.connect(self.searchClick)

        #Insert premier league icon
        userInputL.addWidget(self.preparePremIcon())

        # Create the table frame
        tableF = QFrame(self.mainF)
        #Create a layout to fit inside the frame
        tableL = QVBoxLayout(tableF)
        #Table of available players in the league
        tableL.addWidget(self.createFantraxBox())

        #Add the frames to the main layout
        self.mainL.addWidget(userInputF)
        self.mainL.addWidget(tableF)
        #Set the layout to the layout just generated
        self.mainF.setLayout(self.mainL)
        #Show!
        self.show()

    def searchClick(self):
        queryString = "select player_name, " + self.decodeSortAlgo() + " as algo from player"
        '''if (self.defButton.isChecked()):
            queryString = queryString + "\nwhere pos_id = 0"
        elif (self.midButton.isChecked()):
            queryString = queryString + "\nwhere pos_id = 1"
        elif (self.fwdButton.isChecked()):
            queryString = queryString + "\nwhere pos_id = 2"

        if (self.freeAgentOnlyButton.isChecked()):
            queryString = queryString + '\nwhere availability = "FA"'
            '''

        queryString = queryString + self.decodeComboBox()

        queryString = queryString + "\norder by " + self.decodeSortAlgo() + " desc"

        self.cursor.execute(queryString)

        self.fantraxTable.setRowCount(50)

        i = 0
        for player_name, algo in self.cursor:
            self.fantraxTable.setItem(i, 0, QTableWidgetItem(player_name))
            self.fantraxTable.setItem(i, 1, QTableWidgetItem(str(algo)))
            i = i + 1


    def decodeSortAlgo(self):
        try:
            float(self.goalWeight.text())
            float(self.assistWeight.text())
            float(self.sotWeight.text())
            float(self.yellowWeight.text())
            float(self.redWeight.text())
            float(self.tackleWeight.text())
            float(self.keyPassesWeight.text())
            float(self.interceptionWeight.text())
        except:
            error = QMessageBox(text="All algorithm values must be numbers.")
            error.exec()
            self.resetAlgoClick()

        retString = "goals * " + self.goalWeight.text() + " + assists * " + self.assistWeight.text()\
                    + " + shots_on_target * " + self.sotWeight.text() + " + yellow_cards * " + self.yellowWeight.text()
        return retString


    def decodeComboBox(self):
        teams = ["Any", "AFC Bournemouth", "Arsenal", "Brighton", "Burnley", "Cardiff City", "Chelsea", "Crystal Palace",
                 "Everton", "Fulham", "Huddersfield", "Leicester City", "Liverpool", "Manchester City",
                 "Manchester United", "Newcastle United", "Southampton", "Tottenham Hotspur", "Watford",
                 "West Ham United", "Wolverhampton Wanderers"]
        if (teams.index(self.teamSelectComboBox.currentText()) == 0):
            return ""
        else:
            return "\nwhere club_id = " + str(teams.index(self.teamSelectComboBox.currentText()) - 1)

    def resetAlgoClick(self):
        self.goalWeight.setText("8")
        self.assistWeight.setText("6")
        self.sotWeight.setText("2")
        self.yellowWeight.setText("-3")
        self.redWeight.setText("-7")
        self.tackleWeight.setText("1")
        self.keyPassesWeight.setText("2")
        self.interceptionWeight.setText("0.5")
        notification = QMessageBox(text="Resetting to standard weights.")
        notification.exec()


    def createFantraxBox(self):
        fantraxGroup = QGroupBox("Available players based on set parameters")
        fantraxHolderLayout = QVBoxLayout()
        self.fantraxTable.setColumnCount(5)
        fantraxHeader = self.fantraxTable.horizontalHeader()
        fantraxHeader.setSectionResizeMode(0, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        fantraxHeader.setSectionResizeMode(2, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(3, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(4, QHeaderView.Stretch)
        self.fantraxTable.setHorizontalHeaderLabels(["Name", "CScore", "Club", "Games", "Points per Game"])
        fantraxHolderLayout.addWidget(self.fantraxTable)
        fantraxGroup.setLayout(fantraxHolderLayout)
        return fantraxGroup

    def createPositionBox(self):
        # Create radio button group box + populate
        positionGroup = QGroupBox("Position")
        positionVBox = QVBoxLayout()
        self.fwdButton = QRadioButton(text="Forward")
        self.midButton = QRadioButton(text="Midfielder")
        self.defButton = QRadioButton(text="Defender")
        positionVBox.addWidget(self.fwdButton)
        positionVBox.addWidget(self.midButton)
        positionVBox.addWidget(self.defButton)
        positionGroup.setLayout(positionVBox)
        return positionGroup

    def createAvailabilityTypeBox(self):
        availabilityTypeGroup = QGroupBox("Availability")
        availabilityTypeVBox = QVBoxLayout()
        self.waiverOkButton = QRadioButton(text="Waivers OK")
        self.freeAgentOnlyButton = QRadioButton(text="Restrict to Free Agents")
        availabilityTypeVBox.addWidget(self.waiverOkButton)
        availabilityTypeVBox.addWidget(self.freeAgentOnlyButton)
        availabilityTypeGroup.setLayout(availabilityTypeVBox)
        return availabilityTypeGroup

    def createAlgorithmBox(self):
        algorithmBox = QGroupBox("Sort algorithm")

        algorithmVBox = QVBoxLayout()

        algorithmHBox = QHBoxLayout()
        algorithmHBoxF = QFrame()

        algorithmLabels1 = QVBoxLayout()
        algorithmLabelsF1 = QFrame()
        algorithmLabels2 = QVBoxLayout()
        algorithmLabelsF2 = QFrame()

        algorithmTextboxes1 = QVBoxLayout()
        algorithmTextboxesF1 = QFrame()
        algorithmTextboxes2 = QVBoxLayout()
        algorithmTextboxesF2 = QFrame()

        lineEditWidth = 50

        algorithmLabels1.addWidget(QLabel(text="Goals:"))
        self.goalWeight = QLineEdit()
        self.goalWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes1.addWidget(self.goalWeight)
        algorithmLabels1.addWidget(QLabel(text="Assists:"))
        self.assistWeight = QLineEdit()
        self.assistWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes1.addWidget(self.assistWeight)
        algorithmLabels1.addWidget(QLabel(text="SoT:"))
        self.sotWeight = QLineEdit()
        self.sotWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes1.addWidget(self.sotWeight)
        algorithmLabels1.addWidget(QLabel(text="Yellows:"))
        self.yellowWeight = QLineEdit()
        self.yellowWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes1.addWidget(self.yellowWeight)
        algorithmLabels2.addWidget(QLabel(text="Reds:"))
        self.redWeight = QLineEdit()
        self.redWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.redWeight)
        algorithmLabels2.addWidget(QLabel(text="Tackles:"))
        self.tackleWeight = QLineEdit()
        self.tackleWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.tackleWeight)
        algorithmLabels2.addWidget(QLabel(text="Key Passes:"))
        self.keyPassesWeight = QLineEdit()
        self.keyPassesWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.keyPassesWeight)
        algorithmLabels2.addWidget(QLabel(text="Interceptions:"))
        self.interceptionWeight = QLineEdit()
        self.interceptionWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.interceptionWeight)

        algorithmLabelsF1.setLayout(algorithmLabels1)
        algorithmTextboxesF1.setLayout(algorithmTextboxes1)

        algorithmLabelsF2.setLayout(algorithmLabels2)
        algorithmTextboxesF2.setLayout(algorithmTextboxes2)

        algorithmHBox.addWidget(algorithmLabelsF1)
        algorithmHBox.addWidget(algorithmTextboxesF1)
        algorithmHBox.addWidget(algorithmLabelsF2)
        algorithmHBox.addWidget(algorithmTextboxesF2)

        algorithmHBoxF.setLayout(algorithmHBox)

        algorithmVBox.addWidget(algorithmHBoxF)

        self.resetButton = QPushButton(text="Reset Algorithm")
        algorithmVBox.addWidget(self.resetButton)
        self.resetButton.clicked.connect(self.resetAlgoClick)

        algorithmBox.setLayout(algorithmVBox)

        return algorithmBox

    def createTeamSelectBox(self):
        teamSelectBox = QGroupBox("Club")
        teamSelectBoxVBox = QVBoxLayout()
        self.teamSelectComboBox = QComboBox()
        self.teamSelectComboBox.setCurrentText("Any")
        self.teamSelectComboBox.addItem("Any")
        self.teamSelectComboBox.addItem("AFC Bournemouth")
        self.teamSelectComboBox.addItem("Arsenal")
        self.teamSelectComboBox.addItem("Brighton")
        self.teamSelectComboBox.addItem("Burnley")
        self.teamSelectComboBox.addItem("Cardiff City")
        self.teamSelectComboBox.addItem("Chelsea")
        self.teamSelectComboBox.addItem("Crystal Palace")
        self.teamSelectComboBox.addItem("Everton")
        self.teamSelectComboBox.addItem("Fulham")
        self.teamSelectComboBox.addItem("Huddersfield")
        self.teamSelectComboBox.addItem("Leicester City")
        self.teamSelectComboBox.addItem("Liverpool")
        self.teamSelectComboBox.addItem("Manchester City")
        self.teamSelectComboBox.addItem("Manchester United")
        self.teamSelectComboBox.addItem("Newcastle United")
        self.teamSelectComboBox.addItem("Southampton")
        self.teamSelectComboBox.addItem("Tottenham Hotspur")
        self.teamSelectComboBox.addItem("Watford")
        self.teamSelectComboBox.addItem("West Ham United")
        self.teamSelectComboBox.addItem("Wolverhampton Wanderers")
        teamSelectBoxVBox.addWidget(self.teamSelectComboBox)
        self.teamSelectComboBox.setStyleSheet("QComboBox {color: black} ")
        teamSelectBox.setLayout(teamSelectBoxVBox)
        return teamSelectBox

    def preparePremIcon(self):
        premIcon = QLabel()
        pixmap = QPixmap(resourcesPath + 'PremierLeagueIcon.png')
        premIcon.setPixmap(pixmap)
        return premIcon


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
    app.setWindowIcon(QIcon(resourcesPath + 'PremierLeagueIcon.png'))
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())