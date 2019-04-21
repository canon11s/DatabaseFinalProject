#The purpose of this file is to create a list of all active players in the premier league from the official
#league website. Note: no statistics are scraped, only the list of players

from lxml import html
import requests
import pandas as pd
import ftfy

# URLs to be used #
premierLeagueURL = "https://www.premierleague.com"
premierLeagueClubsURL = "https://www.premierleague.com/clubs"


# # # # # Collect a list of all premier league players # # # # # #

#Grab and format HTML from official website
page = requests.get(premierLeagueClubsURL)
tree = html.fromstring(page.content)

#Find all links to clubs on the page - use css classses
teamLinkLocation = tree.cssselect('.indexItem')

#Send edited team links here
teamLinks = []

for i in range(0, 20):
    # Find the page location
    temp = teamLinkLocation[i].attrib['href']
    #Add link to website domain
    temp = premierLeagueURL + temp
    #Point link to the squad list, not the overview
    temp = temp.replace("overview", "squad")
    #Add to teamLinks list
    teamLinks.append(temp)
    #We now havea list of all premier league clubs!

#We now need to get all the PLAYER links from the club links
#Define an empty list to hold the player links - and one to hold their stats location
playerHomeLinks = []
playerStatLinks = []

for i in range(0, 20):
    #Same process as before for clubs, just looped
    squadPage = requests.get(teamLinks[i])
    squadTree = html.fromstring(squadPage.content)

    playerLinkLocation = squadTree.cssselect('.playerOverviewCard')
    #This number needs to be flexible - no idea how many players each team has
    for j in range(len(playerLinkLocation)):
        temp = playerLinkLocation[j].attrib['href']
        temp = premierLeagueURL + temp
        playerHomeLinks.append(temp)
        playerStatLinks.append(playerHomeLinks[j].replace("overview", "stats"))

#We now must get the relevant player data
#Create lists to hold each type of data - these will later be put into a pandas dataframe
names = []
clubs = []
nationalities = []
positions = []
numbers = []
ages = []


#Populate lists!
for i in range(len(playerHomeLinks)):
    playerPage = requests.get(playerHomeLinks[i])
    playerTree = html.fromstring(playerPage.content)

    #There should always be a name associated with a player
    #NOTE: the ftfy library is used to keep names with accents from coming out ugly - due to Unicode mismatches
    playerName = ftfy.fix_text(str(playerTree.cssselect('.playerDetails')[0].cssselect('.name')[0].text_content()))
    names.append(playerName)

    #Players on lona will often not have a number assigned
    try:
        playerNumber = str(playerTree.cssselect('.playerDetails')[0].cssselect('.number')[0].text_content())
    except IndexError:
        playerNumber = "No number"
        print(playerName + " does not have a number assigned.")
    numbers.append(playerNumber)

    #Players should always have nationality
    playerNationality = str(playerTree.cssselect('.pdcol1')[0].cssselect('.info')[0].text_content())
    nationalities.append(playerNationality)

    #Players may or may not have aa position
    try:
        playerPosition = str(playerTree.cssselect('.fixedSidebar')[0].cssselect('.info')[1].text_content())
    except IndexError:
        playerPosition = "No position"
        print(playerName + " does not have a position assigned.")
    positions.append(playerPosition)

    #Players should always have an age
    playerAge = str(playerTree.cssselect('.pdcol2')[0].cssselect('.info')[0].text_content())
    ages.append(playerAge)

    #Players may or may not have a club
    try:
        playerClub = str(playerTree.cssselect('.fixedSidebar')[0].cssselect('.info')[0].text_content())
    except IndexError:
        playerClub = "No club"
        print(playerName + " does not have a club assigned.")
    clubs.append(playerClub)

#We now must create a data frame to hold all of the details about the players
playerDataFrame = pd.DataFrame(
    {'Name': names,
     "Club": clubs,
     "Nationality": nationalities,
     "Age": ages,
     "Position": positions,
     "Number": numbers
     }
)

print(playerDataFrame.head())

playerDataFrame.to_csv('completePremierLeaguePlayers.csv', encoding='utf-8', index=False)