from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os

resourcesPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/resources/'

#Class to work with the user input to build queries
class FilterSelection():
    def __init__(self, searchButton):
        #Create the main user input frame
        self.mainFrame = QFrame()
        #Create the user input layout to be inside the frame
        mainLayout = QVBoxLayout()
        self.mainFrame.setLayout(mainLayout)

        userInputTopL = QHBoxLayout()
        userInputTopF = QFrame()
        userInputTopF.setLayout(userInputTopL)

        #Add the position select box
        userInputTopL.addWidget(self.createPositionBox())
        #Add the FA/Waiver select box
        userInputTopL.addWidget(self.createAvailabilityTypeBox())

        mainLayout.addWidget(userInputTopF)
        #Add the team select box
        mainLayout.addWidget(self.createTeamSelectBox())
        #Add the sort algorithm
        mainLayout.addWidget(self.createAlgorithmBox())

        pictureFrame = QFrame()
        pictureLayout = QHBoxLayout(pictureFrame)
        pictureLayout.addStretch()
        pictureLayout.addWidget(self.preparePremIcon())
        pictureLayout.addStretch()
        pictureLayout.addWidget(searchButton)
        pictureLayout.addStretch()
        #Insert premier league icon
        mainLayout.addWidget(pictureFrame)

    #Returns the widget which will be used by the GUI
    def returnWidget(self):
        return self.mainFrame

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



    def decodeComboBox(self):
        teams = ["Any", "AFC Bournemouth", "Arsenal", "Brighton and Hove Albion", "Burnley", "Cardiff City", "Chelsea", "Crystal Palace",
                 "Everton", "Fulham", "Huddersfield Town", "Leicester City", "Liverpool", "Manchester City",
                 "Manchester United", "Newcastle United", "Southampton", "Tottenham Hotspur", "Watford",
                 "West Ham United", "Wolverhampton Wanderers"]
        if (teams.index(self.teamSelectComboBox.currentText()) == 0):
            return ""
        else:
            return " and club_id = " + str(teams.index(self.teamSelectComboBox.currentText()))

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

    def buildQuery(self):
        queryString = "select name, game_played, club_id, goal, assist, " + self.decodeSortAlgo() + " as algo from player"
        if (self.defButton.isChecked()):
            queryString = queryString + "\nwhere position = 'D'"
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

        return queryString

