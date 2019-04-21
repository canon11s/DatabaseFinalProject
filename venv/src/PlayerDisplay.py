#Necessary imports
from PyQt5.QtWidgets import *

#File constants
teams = ["Any", "AFC Bournemouth", "Arsenal", "Brighton and Hove Albion", "Burnley", "Cardiff City", "Chelsea",
                 "Crystal Palace",
                 "Everton", "Fulham", "Huddersfield Town", "Leicester City", "Liverpool", "Manchester City",
                 "Manchester United", "Newcastle United", "Southampton", "Tottenham Hotspur", "Watford",
                 "West Ham United", "Wolverhampton Wanderers"]

#Class to represent the table component of the application
class PlayerDisplay():
    def __init__(self):
        #Declare tables to be filled by database
        self.mainTable = QTableWidget()
        # Create the table frame
        self.mainFrame = QFrame()
        # Create a layout to fit inside the frame
        self.mainLayout = QVBoxLayout(self.mainFrame)
        #Table of available players in the league
        self.mainLayout.addWidget(self.createFantraxBox())

    # Returns the widget which will be used by the GUI
    def returnWidget(self):
        return self.mainFrame

    def fillTable(self, resultSet):
        self.mainTable.clear()
        self.mainTable.setRowCount(50)

        i = 0
        for name, game_played, club_id, goal, assist, algo in resultSet:
            self.mainTable.setItem(i, 0, QTableWidgetItem(name))
            self.mainTable.setItem(i, 1, QTableWidgetItem(str(algo)))
            if (game_played > 5):
                self.mainTable.setItem(i, 2, QTableWidgetItem(str(algo/game_played)))
            else:
                self.mainTable.setItem(i, 2, QTableWidgetItem('N/A'))
            self.mainTable.setItem(i, 3, QTableWidgetItem(teams[int(club_id)]))
            self.mainTable.setItem(i, 4, QTableWidgetItem(str(goal)))
            self.mainTable.setItem(i, 5, QTableWidgetItem(str(assist)))
            i = i + 1
        self.mainTable.setHorizontalHeaderItem(0, QTableWidgetItem('Name'))
        self.mainTable.setHorizontalHeaderItem(1, QTableWidgetItem('Algorithm'))
        self.mainTable.setHorizontalHeaderItem(2, QTableWidgetItem('Algo/Game'))
        self.mainTable.setHorizontalHeaderItem(3, QTableWidgetItem('Club'))
        self.mainTable.setHorizontalHeaderItem(4, QTableWidgetItem('Goals'))
        self.mainTable.setHorizontalHeaderItem(5, QTableWidgetItem('Assists'))

    #Method called in the constructor to set up the table and surrounding labels
    def createFantraxBox(self):
        fantraxGroup = QGroupBox("Available players based on set parameters")
        fantraxHolderLayout = QVBoxLayout()
        self.mainTable.setColumnCount(6)
        fantraxHeader = self.mainTable.horizontalHeader()
        fantraxHeader.setSectionResizeMode(0, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(1, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(2, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(3, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(4, QHeaderView.Stretch)
        fantraxHeader.setSectionResizeMode(5, QHeaderView.Stretch)
        self.mainTable.setHorizontalHeaderLabels(["Name", "Algorithm", "Algo/Game", "Club", "Goals", "Assists"])
        fantraxHolderLayout.addWidget(self.mainTable)
        fantraxGroup.setLayout(fantraxHolderLayout)
        return fantraxGroup