import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from env import api_key
import re

# Use prep to alter the dataframe

def prepare(df):

    df = clean(df)

    train, test = split(df)

    return train, test


def split(df):
    
    train, test = train_test_split(df, test_size = 0.2, random_state = 123)

    return train, test


def clean(df):
    '''
    This Function, fills NA with zero, creates team total columns & gold difference, drops killplayers_0
    '''
    # Replace all nulls with 0
    df = df.fillna(0)

    # Setting the features we want to add up for team totals to 'columns'
    columns=['deathsplayer_',
                'goldPerSecond_',
                'jungleMinionsKilled_',
                'killsplayer_',
                'level_',
                'magicDamageDoneToChampions_',
                'minionsKilled_',
                'physicalDamageDoneToChampions_',
                'timeEnemySpentControlled_',
                'totalDamageDoneToChampions_',
                'totalGold_',
                'trueDamageDoneToChampions_',
                'ward_player_',
                'assistsplayer_',
                'xp_']

    # Initializing/Set up the names based on columns above
    for col in columns:
        df[f'team_{col}100'] = 0
        df[f'team_{col}200'] = 0

    # Calculate values for blue team totals and read team totals
    for index, value in enumerate(df.iterrows()):
        for col in columns:
            
            total = 0
            # Blue Team
            for i in range(1, 6):
                total += int(df.iloc[index][f'{col}{i}'])
            
            df.at[index, f'team_{col}100'] = total
        
            total = 0
            # Red Team
            for i in range(6, 11):
                total += int(df.iloc[index][f'{col}{i}'])
            
            df.at[index, f'team_{col}200'] = total

    # Drop killsplayer_0, not needed
    df.drop(columns = ['killsplayer_0'], inplace = True)

    # Rename team stats 100 = Blue Team, 200 Red Team
    df = df.rename(columns={ 'team_deathsplayer_100':'BlueTeamDeaths', 'team_deathsplayer_200':'RedTeamDeaths', 'team_goldPerSecond_100':'BlueTeamGoldPerSec', 'team_goldPerSecond_200':'RedTeamGoldPerSec', 'team_jungleMinionsKilled_100':'BlueTeamJungleMinionsKilled', 'team_jungleMinionsKilled_200':'RedTeamJungleMinionsKilled', 'team_killsplayer_100':'BlueTeamKills', 'team_killsplayer_200':'RedTeamKills', 'team_level_100':'BlueTeamLevel', 'team_level_200':'RedTeamLevel', 'team_magicDamageDoneToChampions_100':'BlueTeamMagicDamageDoneToChampions', 'team_magicDamageDoneToChampions_200':'RedTeamMagicDamageDoneToChampions', 'team_minionsKilled_100':'BlueTeamMinionsKilled', 'team_minionsKilled_200':'RedTeamMinionsKilled', 'team_physicalDamageDoneToChampions_100':'BlueTeamPhysicalDamageDoneToChampions', 'team_physicalDamageDoneToChampions_200':'RedTeamPhysicalDamageDoneToChampions', 'team_timeEnemySpentControlled_100':'BlueTeamTimeEnemySpentControlled', 'team_timeEnemySpentControlled_200':'RedTeamTimeEnemySpentControlled', 'team_totalDamageDoneToChampions_100':'BlueTeamTotalDamageDoneToChampions', 'team_totalDamageDoneToChampions_200':'RedTeamTotalDamageDoneToChampions', 'team_totalGold_100':'BlueTeamTotalGold', 'team_totalGold_200':'RedTeamTotalGold', 'team_trueDamageDoneToChampions_100':'BlueTeamTrueDamageDoneToChampions', 'team_trueDamageDoneToChampions_200':'RedTeamTrueDamageDoneToChampions', 'team_ward_player_100':'BlueTeamWards', 'team_ward_player_200':'RedTeamWards', 'team_assistsplayer_100':'BlueTeamAssists', 'team_assistsplayer_200':'RedTeamAssists', 'team_xp_100':'BlueTeamXp', 'team_xp_200':'RedTeamXp'})
    
    # Create Gold Difference
    df['BlueTeamTotalGoldDifference'] = df.BlueTeamTotalGold - df.RedTeamTotalGold
    df['RedTeamTotalGoldDifference'] =  df.RedTeamTotalGold - df.BlueTeamTotalGold

    # Creating BlueTeamMVPKills
    for index, value in enumerate(df.iterrows()):
        col='killsplayer_'
                
        # Blue Team MVP
        total = 0

        for i in range(1, 6):
            value = int(df.iloc[index][f'{col}{i}'])
            if (value>total):
                total = value
    
        df.at[index, 'BlueTeamMVPKills'] = total
        
        # Red Team MVP
        total = 0

        for i in range(6, 11):
            value = int(df.iloc[index][f'{col}{i}'])
            if (value>total):
                total = value
            
        df.at[index, 'RedTeamMVPKills'] = total

    return df