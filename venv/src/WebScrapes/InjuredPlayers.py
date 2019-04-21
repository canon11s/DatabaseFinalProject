#The purpose of this file is to compile a list of players who are soon returning from injury - this is valuable
#as it is useful for fantasy managers - soon returning polayuers may go unnoticed by everyone in your league, so you can
#grab great players for no cost

import requests
import pandas as pd
from bs4 import BeautifulSoup


injuredPlayersURL = "https://www.fantasyfootballscout.co.uk/fantasy-football-injuries/"

# Create an empty list to hold players who are close to returning
returningPlayers = []
returningPlayersClubs = []
returningPlayersDate = []
players = []
def run():
    #Grab and format HTML from website
    page = requests.get(injuredPlayersURL)
    #pass into Beau Soup constructor
    pageContent = BeautifulSoup(page.content, "html.parser")

    #find players who are returning soon - 75% to full health or better
    players = pageContent.find_all("tr")
    #NOTE: The first will be the header for the table. All others after index = 1 will be good data



# FUNCTIONS THAT WILL LATER BE USED BY OUR FOR LOOP

#Fix the weridly formatted names
def fixName(name):
    #Strip bogus off the string, split into list
    listName = name.strip().split(" ")
    #Remove empty strings that still have not been removed
    cleanListName = list(filter(None, listName))
    #Turn it into a single strign name from a clean list
    if (len(cleanListName) > 1):
        finalName = cleanListName[1][1:len(cleanListName[1]) - 1] + " " + cleanListName[0]
    else:
        finalName = cleanListName[0]
    return finalName

#Takes in the weirldy formatted website dates, returns a nice one
def fixDate(idate):
    if idate == "Unknown":
        return idate
    else:
        retDate = idate[3:5] + " - " + idate[0:2] + " - " + idate[6:10]
        return retDate

#Scrapes and adds data to the arrays declared earlier
def addData(index):
    # Scrape the data based on the passes in index
    scrapedName = players[index].find_all("td")[0].text
    scrapedClub = players[index].find_all("td", class_="team")[0]["title"]
    scrapedDate = players[index].find_all("td")[3].text
    # Add the name
    returningPlayers.append(fixName(scrapedName))
    # Add the team
    returningPlayersClubs.append(scrapedClub)
    # Add return date
    returningPlayersDate.append(fixDate(scrapedDate))

#The main function, which will be called from the main file
def generateReturningCSV():
    #Extract only the players that are returning soon - skip index 0, as it is a table header
    for i in range(1, len(players)):
        if players[i].find_all("td", class_="inj-status")[0].text == "Doubt 75%":
            addData(i)

    #We now must create a data frame to hold all of the details about the players
    returningPlayerDataFrame = pd.DataFrame(
        {'Name': returningPlayers,
         "Club": returningPlayersClubs,
         "Date of Return": returningPlayersDate
         }
    )
    return returningPlayerDataFrame