import pandas as pd
import os

resourcesPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/lib/resources/'

df = pd.read_csv(resourcesPath + 'FantraxScrape.csv')

print(df.head())

teamToId = {
    'BOUR' : 1,
    'ARS' : 2,
    'BRIGHT' : 3,
    'BURN' : 4,
    'CAR' : 5,
    'CHE' : 6,
    'CRY' : 7,
    'EVE' : 8,
    'FUL' : 9,
    'HUD' : 10,
    'LEIC' : 11,
    'LIV' : 12,
    'MCI' : 13,
    'MUN' : 14,
    'NEW' : 15,
    'SOU' : 16,
    'TOT' : 17,
    'WAT' : 18,
    'WHU' : 19,
    'WOLVES' : 20
}

#Things that need to be changed
#   TEAM -> TEAM_ID
#   STATUS -> WW, FA, OWNED ONLY

for i in range(0, len(df.index)):
    df.iloc[i, df.columns.get_loc('Team')] = teamToId[df.iloc[i, df.columns.get_loc('Team')]]
    if (df.iloc[i, df.columns.get_loc('Status')] != 'FA' and df.iloc[i, df.columns.get_loc('Status')] != 'WW'):
        df.iloc[i, df.columns.get_loc('Status')] = 'OWNDED'
    if (len(df.iloc[i, df.columns.get_loc('Position')]) != 1):
        df.iloc[i, df.columns.get_loc('Position')] = df.iloc[i, df.columns.get_loc('Position')][0:1]

df.to_csv(resourcesPath + 'CleanedFantraxScrape.csv')