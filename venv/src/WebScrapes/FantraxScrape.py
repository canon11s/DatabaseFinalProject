#The purpose of this file is to scrape all statistics of the desired players from the fantrax fantasy website
#The file will then save all the statistics as a CSV, which can be further cleaned and parsed before being added to
#the DB

#import necessary libraries
import requests
from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

#URLS needed
homePageURL = "https://www.fantrax.com"
signInPageURL = "https://www.fantrax.com/login"
freeAgentURL = "https://www.fantrax.com/fantasy/league/dyfj23bmjjr64sw4/players?view=STATS&positionOrGroup=" \
               "SOCCER_NON_GOALIE&seasonOrProjection=SEASON_918_YEAR_TO_DATE&timeframeTypeCode=YEAR_TO_DATE&" \
               "transactionPeriod=21&miscDisplayType=1&sortType=SCORE&maxResultsPerPage=500&statusOrTeamFilter" \
               "=ALL_AVAILABLE&scoringCategoryType=5&timeStartType=PERIOD_ONLY&pageNumber=1&schedulePageAdj=0&" \
               "startDate=2018-08-10&endDate=2019-05-12&searchName=&txs=false&teamId=h4r7feqjjjyi1c01"

def validLogin(UN, PW):
    #driver = webdriver.Chrome()
    #driver.get(signInPageURL)
    #driver.find_element_by_id("mat-input-0").send_keys(UN)
    #driver.find_element_by_id("mat-input-1").send_keys(PW)
    #driver.find_element_by_class_name("form").find_element_by_class_name("mat-button-wrapper").click()
    if True:
        return True
    else:
        return False

def fantraxScrape(UN, PW):
    # set up Slenium web driver
    driver = webdriver.Chrome()
    driver.get(signInPageURL)
    time.sleep(1)
    driver.find_element_by_id("mat-input-0").send_keys(UN)
    driver.find_element_by_id("mat-input-1").send_keys(PW)
    driver.find_element_by_class_name("form").find_element_by_class_name("mat-button-wrapper").click()
    time.sleep(1)
    driver.get(freeAgentURL)
    #Give the page some time to load to find all the players
    time.sleep(3)

    #Capture all instances of players on the page
    players = driver.find_elements_by_xpath('/html/body/app-root/div/div/div/app-league-players/div/section/ultimate-table/div/section/aside/td')
    stats = driver.find_elements_by_xpath('/html/body/app-root/div/div/div/app-league-players/div/section/ultimate-table/div/section/div/table/tr')

    playerDetails, playerNames, playerPositions, playerTeams = [], [], [], []

    for i in range(0, 60):
        playerDetails.append(players[i].text)
        playerNames.append(playerDetails[i].split('\n')[0])
        playerPositions.append(playerDetails[i].split('\n')[1])
        playerTeams.append(playerDetails[i].split('\n')[2][2:])

    status, totalPoints, pointsPerGame, gamesPlayed, goals, assists, keyPasses, shotsOnTarget, tackles, \
    dispossessed, foulsSuffered, yellows, reds, accurateCrosses, interceptions, clearances, aerials, gad = \
        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []



    for i in range(0, 60):
        status.append(stats[i].text.split('\n')[3].split()[1])
        stats[i] = stats[i].text.split('\n')[4]

        #Adjust for when things are thrown off by free agency/ waivers
        adjustment = 0
        if "%" in stats[i].split()[3]:
            adjustment = -2

        totalPoints.append(stats[i].split()[3 + adjustment])
        pointsPerGame.append(stats[i].split()[4 + adjustment])
        gamesPlayed.append(stats[i].split()[7 + adjustment])
        goals.append(stats[i].split()[8 + adjustment])
        assists.append(stats[i].split()[9 + adjustment])
        keyPasses.append(stats[i].split()[10 + adjustment])
        shotsOnTarget.append(stats[i].split()[12 + adjustment])
        tackles.append(stats[i].split()[13 + adjustment])
        dispossessed.append(stats[i].split()[14 + adjustment])
        foulsSuffered.append(stats[i].split()[15 + adjustment])
        yellows.append(stats[i].split()[16 + adjustment])
        reds.append(stats[i].split()[18 + adjustment])
        accurateCrosses.append(stats[i].split()[19 + adjustment])
        interceptions.append(stats[i].split()[20 + adjustment])
        clearances.append(stats[i].split()[21 + adjustment])
        aerials.append(stats[i].split()[22 + adjustment])
        gad.append(stats[i].split()[24 + adjustment])

    # We now must create a data frame to hold all of the details about the players
    statsDataFrame = pd.DataFrame(
        {'Name' : playerNames,
         "Club" : playerTeams,
         "Position" : playerPositions,
         "Status" : status,
         "Total Points" : totalPoints,
         "PPG" : pointsPerGame,
         "Games played" : gamesPlayed,
         "Goals" : goals,
         "Assists" : assists,
         "Key Passes" : keyPasses,
         "SOT" : shotsOnTarget,
         "Tackles" : tackles,
         "Dispossessed" : dispossessed,
         "Fouls suffered" : foulsSuffered,
         "Yellows" : yellows,
         "Reds" : reds,
         "Accurate Crosses" : accurateCrosses,
         "Interceptions": interceptions,
         "Clearances": clearances,
         "Aerials": aerials,
         "Goals Agnst Def": gad
         }
    )

    print(statsDataFrame.to_string())

    driver.close()

    return statsDataFrame