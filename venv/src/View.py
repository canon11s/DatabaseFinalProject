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
            database="soccer"
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

        userInputTopL = QHBoxLayout()
        userInputTopF = QFrame()
        userInputTopF.setLayout(userInputTopL)

        #Add the position select box
        userInputTopL.addWidget(self.createPositionBox())
        #Add the FA/Waiver select box
        userInputTopL.addWidget(self.createAvailabilityTypeBox())

        userInputL.addWidget(userInputTopF)
        #Add the team select box
        userInputL.addWidget(self.createTeamSelectBox())
        #Add the sort algorithm
        userInputL.addWidget(self.createAlgorithmBox())
        #Search button to run search and find players
        searchButton = QPushButton(text="Search")
        #Connect search button with clicked command
        searchButton.clicked.connect(self.searchClick)

        pictureFrame = QFrame()
        pictureLayout = QHBoxLayout(pictureFrame)
        pictureLayout.addStretch()
        pictureLayout.addWidget(self.preparePremIcon())
        pictureLayout.addStretch()
        pictureLayout.addWidget(searchButton)
        pictureLayout.addStretch()
        #Insert premier league icon
        userInputL.addWidget(pictureFrame)

        # Create the table frame
        tableF = QFrame(self.mainF)
        #Create a layout to fit inside the frame
        tableL = QVBoxLayout(tableF)
        #Table of available players in the league
        tableL.addWidget(self.createFantraxBox())

        #Add the frames to the main layout
        self.mainL.addWidget(userInputF, 1)
        self.mainL.addWidget(tableF, 4)
        #Set the layout to the layout just generated
        self.mainF.setLayout(self.mainL)
        #Show!
        self.show()

    def searchClick(self):
        self.fantraxTable.clear()
        queryString = "select name, game_played, club_id, goal, assist, " + self.decodeSortAlgo() + " as algo from player"
        if (self.defButton.isChecked()):
            queryString = queryString + "\nwhere position = 'F'"
        elif (self.midButton.isChecked()):
            queryString = queryString + "\nwhere position = 'M'"
        elif (self.fwdButton.isChecked()):
            queryString = queryString + "\nwhere position = 'F'"
        else:
            queryString = queryString + "\nwhere player_id < 1000"


        if (self.freeAgentOnlyButton.isChecked()):
            queryString = queryString + ' and status = "FA"'
        elif(self.waiverOkButton.isChecked()):
            queryString = queryString + ' and (status = "WW" or status = "FA")'


        queryString = queryString + self.decodeComboBox()

        queryString = queryString + "\norder by " + self.decodeSortAlgo() + " desc"

        self.cursor.execute(queryString)

        self.fantraxTable.setRowCount(50)

        teams = ["Any", "AFC Bournemouth", "Arsenal", "Brighton and Hove Albion", "Burnley", "Cardiff City", "Chelsea",
                 "Crystal Palace",
                 "Everton", "Fulham", "Huddersfield Town", "Leicester City", "Liverpool", "Manchester City",
                 "Manchester United", "Newcastle United", "Southampton", "Tottenham Hotspur", "Watford",
                 "West Ham United", "Wolverhampton Wanderers"]

        i = 0
        for name, game_played, club_id, goal, assist, algo in self.cursor:
            self.fantraxTable.setItem(i, 0, QTableWidgetItem(name))
            self.fantraxTable.setItem(i, 1, QTableWidgetItem(str(algo)))
            if (game_played > 5):
                self.fantraxTable.setItem(i, 2, QTableWidgetItem(str(algo/game_played)))
            else:
                self.fantraxTable.setItem(i, 2, QTableWidgetItem('N/A'))
            self.fantraxTable.setItem(i, 3, QTableWidgetItem(teams[int(club_id)]))
            self.fantraxTable.setItem(i, 4, QTableWidgetItem(str(goal)))
            self.fantraxTable.setItem(i, 5, QTableWidgetItem(str(assist)))
            i = i + 1
        self.fantraxTable.setHorizontalHeaderItem(0, QTableWidgetItem('Name'))
        self.fantraxTable.setHorizontalHeaderItem(1, QTableWidgetItem('Algorithm'))
        self.fantraxTable.setHorizontalHeaderItem(2, QTableWidgetItem('Algo/Game'))
        self.fantraxTable.setHorizontalHeaderItem(3, QTableWidgetItem('Club'))
        self.fantraxTable.setHorizontalHeaderItem(4, QTableWidgetItem('Goals'))
        self.fantraxTable.setHorizontalHeaderItem(5, QTableWidgetItem('Assists'))


    def decodeSortAlgo(self):
        try:
            float(self.goalWeight.text())
            float(self.assistWeight.text())
            float(self.sotWeight.text())
            float(self.dispossessionWeight.text())
            float(self.accCrossWeight.text())
            float(self.foulsSufferedWeight.text())
            float(self.aerialWeight.text())
            float(self.keyPassesWeight.text())
            float(self.tackleWeight.text())
            float(self.yellowWeight.text())
            float(self.redWeight.text())
            float(self.tackleWeight.text())
            float(self.interceptionWeight.text())
            float(self.clearanceWeight.text())
        except:
            error = QMessageBox(text="All algorithm values must be numbers.")
            error.exec()
            self.resetAlgoClick()

        retString = "goal * " + self.goalWeight.text() + \
                    " + assist * " + self.assistWeight.text() + \
                    " + shot_on_target * " + self.sotWeight.text() + \
                    " + dispossession * " + self.dispossessionWeight.text() + \
                    " + accurate_cross * " + self.accCrossWeight.text() + \
                    " + foul_suffered * " + self.foulsSufferedWeight.text() + \
                    " + aerial_won * " + self.aerialWeight.text() + \
                    " + key_pass * " + self.keyPassesWeight.text() + \
                    " + tackle * " + self.tackleWeight.text() + \
                    " + yellow_card * " + self.yellowWeight.text() + \
                    " + red_card * " + self.redWeight.text() + \
                    " + interception * " + self.interceptionWeight.text() + \
                    " + clearance * " + self.clearanceWeight.text()

        return retString


    def decodeComboBox(self):
        teams = ["Any", "AFC Bournemouth", "Arsenal", "Brighton and Hove Albion", "Burnley", "Cardiff City", "Chelsea", "Crystal Palace",
                 "Everton", "Fulham", "Huddersfield Town", "Leicester City", "Liverpool", "Manchester City",
                 "Manchester United", "Newcastle United", "Southampton", "Tottenham Hotspur", "Watford",
                 "West Ham United", "Wolverhampton Wanderers"]
        if (teams.index(self.teamSelectComboBox.currentText()) == 0):
            return ""
        else:
            return " and club_id = " + str(teams.index(self.teamSelectComboBox.currentText()))

    def resetAlgoClick(self):
        self.goalWeight.setText("8")
        self.assistWeight.setText("6")
        self.sotWeight.setText("2")
        self.yellowWeight.setText("-3")
        self.redWeight.setText("-7")
        self.tackleWeight.setText("1")
        self.keyPassesWeight.setText("2")
        self.interceptionWeight.setText("0.5")
        self.clearanceWeight.setText("0.5")
        self.interceptionWeight.setText("0.5")
        self.aerialWeight.setText("0.5")
        self.accCrossWeight.setText("2")
        self.dispossessionWeight.setText("-0.25")
        self.foulsSufferedWeight.setText("0.5")
        self.goalWeight.repaint()
        self.assistWeight.repaint()
        self.sotWeight.repaint()
        self.yellowWeight.repaint()
        self.redWeight.repaint()
        self.tackleWeight.repaint()
        self.keyPassesWeight.repaint()
        self.interceptionWeight.repaint()
        self.clearanceWeight.repaint()
        self.interceptionWeight.repaint()
        self.aerialWeight.repaint()
        self.accCrossWeight.repaint()
        self.dispossessionWeight.repaint()
        self.foulsSufferedWeight.repaint()
        notification = QMessageBox(text="Resetting to standard weights.")
        notification.exec()


    def createFantraxBox(self):
        fantraxGroup = QGroupBox("Available players based on set parameters")
        fantraxHolderLayout = QVBoxLayout()
        self.fantraxTable.setColumnCount(6)
        fantraxHeader = self.fantraxTable.horizontalHeader()
        fantraxHeader.setSectionResizeMode(0, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(1, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(2, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(3, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(4, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(5, QHeaderView.Stretch)
        self.fantraxTable.setHorizontalHeaderLabels(["Name", "Algorithm", "Algo/Game", "Club", "Goals", "Assists"])
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

        algorithmLabels2.addWidget(QLabel(text="Key Passes:"))
        self.keyPassesWeight = QLineEdit()
        self.keyPassesWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.keyPassesWeight)

        algorithmLabels1.addWidget(QLabel(text="SoT:"))
        self.sotWeight = QLineEdit()
        self.sotWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes1.addWidget(self.sotWeight)

        algorithmLabels1.addWidget(QLabel(text="Dispossessions:"))
        self.dispossessionWeight = QLineEdit()
        self.dispossessionWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes1.addWidget(self.dispossessionWeight)

        algorithmLabels1.addWidget(QLabel(text="Acc. Crosses:"))
        self.accCrossWeight = QLineEdit()
        self.accCrossWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes1.addWidget(self.accCrossWeight)

        algorithmLabels1.addWidget(QLabel(text="Fouls Suf.:"))
        self.foulsSufferedWeight = QLineEdit()
        self.foulsSufferedWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes1.addWidget(self.foulsSufferedWeight)

        algorithmLabels2.addWidget(QLabel(text="Yellows:"))
        self.yellowWeight = QLineEdit()
        self.yellowWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.yellowWeight)

        algorithmLabels2.addWidget(QLabel(text="Reds:"))
        self.redWeight = QLineEdit()
        self.redWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.redWeight)

        algorithmLabels2.addWidget(QLabel(text="Tackles:"))
        self.tackleWeight = QLineEdit()
        self.tackleWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.tackleWeight)

        algorithmLabels2.addWidget(QLabel(text="Interceptions:"))
        self.interceptionWeight = QLineEdit()
        self.interceptionWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.interceptionWeight)

        algorithmLabels1.addWidget(QLabel(text="Aerials:"))
        self.aerialWeight = QLineEdit()
        self.aerialWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes1.addWidget(self.aerialWeight)

        algorithmLabels2.addWidget(QLabel(text="Clearances:"))
        self.clearanceWeight = QLineEdit()
        self.clearanceWeight.setFixedWidth(lineEditWidth)
        algorithmTextboxes2.addWidget(self.clearanceWeight)

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
        teams = {"Any", "AFC Bournemouth", "Arsenal", "Brighton and Hove Albion", "Burnley", "Cardiff City", "Chelsea", "Crystal Palace",
        "Everton", "Fulham", "Huddersfield Town", "Leicester City", "Liverpool", "Manchester City",
        "Manchester United", "Newcastle United", "Southampton", "Tottenham Hotspur", "Watford",
        "West Ham United", "Wolverhampton Wanderers"}
        for i in teams:
            self.teamSelectComboBox.addItem(i)
            self.teamSelectComboBox.setCurrentText("Any")
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