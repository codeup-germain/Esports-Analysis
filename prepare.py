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

    # Drop Duplicates
    df = df.drop_duplicates()
    
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
    #for index, value in enumerate(df.iterrows()):
    #    col='killsplayer_'
    #            
    #    # Blue Team MVP
    #    total = 0
#
    #    for i in range(1, 6):
    #        value = int(df.iloc[index][f'{col}{i}'])
    #        if (value>total):
    #            total = value
    #
    #    df.at[index, 'BlueTeamMVPKills'] = total
    #    
    #    # Red Team MVP
    #    total = 0
#
    #    for i in range(6, 11):
    #        value = int(df.iloc[index][f'{col}{i}'])
    #        if (value>total):
    #            total = value
     #       
    #    df.at[index, 'RedTeamMVPKills'] = total

    df = team_difference_stats(df)
    df = main_rename(df)
    return df

def team_difference_stats(df):
    '''
    Added a bunch of new columns to try out, (alot of difference columns) KDA columns
    '''
    df['BlueTeamLevelDifference'] = df.BlueTeamLevel - df.RedTeamLevel
    df['BlueTeamXpDifference'] = df.BlueTeamXp - df.RedTeamXp
    df['BlueTeamWardDifference'] = df.BlueTeamWards - df.RedTeamWards
    df['BlueTeamminionKillDifference'] = df.BlueTeamJungleMinionsKilled - df.RedTeamJungleMinionsKilled
    df['BlueTeamDeathsDifference'] = df.BlueTeamDeaths - df.RedTeamDeaths
    df['BlueTeamMagicDmgDifference'] = df.BlueTeamMagicDamageDoneToChampions - df.RedTeamMagicDamageDoneToChampions
    df['BlueTeamPhysicalDmgDifference'] = df.BlueTeamPhysicalDamageDoneToChampions - df.RedTeamPhysicalDamageDoneToChampions
    df['BlueTeamTrueDmgDifference'] = df.BlueTeamTrueDamageDoneToChampions - df.RedTeamTrueDamageDoneToChampions
    df['BlueTeamTotalDmgDifference'] = df.BlueTeamTotalDamageDoneToChampions - df.RedTeamTotalDamageDoneToChampions
    df['BlueTeamTotalMinionsMonstersDifference'] = ((df.BlueTeamMinionsKilled + df.BlueTeamJungleMinionsKilled) - 
                                    (df.RedTeamMinionsKilled + df.RedTeamJungleMinionsKilled))
    df['BlueTeamTimeCCingDifference'] = df.BlueTeamTimeEnemySpentControlled - df.RedTeamTimeEnemySpentControlled
    df['BlueteamWardDifference'] = df.BlueTeamWards - df.RedTeamWards
    df['BlueteamAssistDifference'] = df.BlueTeamAssists - df.RedTeamAssists
    df['BlueBotLaneKillDifference'] = (df.killsplayer_4 + df.killsplayer_5) - (df.killsplayer_9 + df.killsplayer_10)
    df['BlueJungTopkillDifference'] = (df.killsplayer_1 + df.killsplayer_2) - (df.killsplayer_6 + df.killsplayer_7)
    df['BlueTeamWaterDragonDifference'] = df.waterdragon_team100 - df.waterdragon_team200
    df['BlueTeamAirDragonDifference'] = df.airdragon_team100 - df.airdragon_team200
    df['BlueTeamChemtechDragonDifference'] = df.chemtechdragon_team100 - df.waterdragon_team200
    df['BlueTeamFireDragonDifference'] = df.firedragon_team100 - df.firedragon_team200
    df['BlueTeamHextechDragonDifference'] = df.hextechdragon_team100 - df.hextechdragon_team200
    df['BlueTeamEarthDragonDifference'] = df.earthdragon_team100 - df.earthdragon_team200
    df['BlueSupportStats'] = df.assistsplayer_5 - (df.deathsplayer_5 * 2)
    df['RedSupportStats'] = df.assistsplayer_10 - (df.deathsplayer_10 * 2)
    df['BlueSupportDifference'] = df.BlueSupportStats - df.RedSupportStats
    df['BlueTopKda'] = df.killsplayer_1 * 1.25 + (df.assistsplayer_1 * .75) - df.deathsplayer_1
    df['BlueJungleKda'] = df.killsplayer_2 * 1.25 + (df.assistsplayer_2 * .75) - df.deathsplayer_2
    df['BlueMidKda'] = df.killsplayer_3 * 1.25 + (df.assistsplayer_3 * .75) - df.deathsplayer_3
    df['BlueBotKda'] = df.killsplayer_4 * 1.25 + (df.assistsplayer_4 * .75) - df.deathsplayer_4
    df['BlueSupportKda'] = df.killsplayer_5 * 1.25 + (df.assistsplayer_5 * .75) - df.deathsplayer_5
    df['RedTopKda'] = df.killsplayer_6 * 1.25 + (df.assistsplayer_6 * .75) - df.deathsplayer_6
    df['RedJungleKda'] = df.killsplayer_7 * 1.25 + (df.assistsplayer_7 * .75) - df.deathsplayer_7
    df['RedMidKda'] = df.killsplayer_8 * 1.25 + (df.assistsplayer_8 * .75) - df.deathsplayer_8
    df['RedBotKda'] = df.killsplayer_9 * 1.25 + (df.assistsplayer_9 * .75) - df.deathsplayer_9
    df['RedSupportKda'] = (df.killsplayer_10 * 1.25 + (df.assistsplayer_10 * .75)) - df.deathsplayer_10
    df['BlueTeamKdaDifference'] = (((df.BlueTeamKills * 1.25 + (df.BlueTeamAssists * .75)) - df.BlueTeamDeaths) - 
                                   (df.RedTeamKills * 1.25 + (df.RedTeamAssists * .75) - df.RedTeamDeaths))
    df['BlueJungleGankHeavy'] = (df.killsplayer_2 * 100) - (df.jungleMinionsKilled_2)
    df['RedJungleGankHeavy'] = (df.killsplayer_7 * 100) - (df.jungleMinionsKilled_7)
    df['BlueTeamJungleDiffy'] = df.BlueJungleGankHeavy - df.RedJungleGankHeavy
    return df

def main_rename(df):
    '''
    This function renames columns, makes them easier to read.
    '''
    # Rename Kills
    df = df.rename(columns={'killsplayer_1': 'BlueTopKills'})
    df = df.rename(columns={'killsplayer_2': 'BlueJungleKills'})
    df = df.rename(columns={'killsplayer_3': 'BlueMidKills'})
    df = df.rename(columns={'killsplayer_4': 'BlueADCKills'})
    df = df.rename(columns={'killsplayer_5': 'BlueSupportKills'})
    df = df.rename(columns={'killsplayer_6': 'RedTopKills'})
    df = df.rename(columns={'killsplayer_7': 'RedJungleKills'})
    df = df.rename(columns={'killsplayer_8': 'RedMidKills'})
    df = df.rename(columns={'killsplayer_9': 'RedADCKills'})
    df = df.rename(columns={'killsplayer_10':'RedSupportKills'})

    # Rename Assists
    df = df.rename(columns={'assistsplayer_1': 'BlueTopAssists'})
    df = df.rename(columns={'assistsplayer_2': 'BlueJungleAssists'})
    df = df.rename(columns={'assistsplayer_3': 'BlueMidAssists'})
    df = df.rename(columns={'assistsplayer_4': 'BlueADCAssists'})
    df = df.rename(columns={'assistsplayer_5': 'BlueSupportAssists'})
    df = df.rename(columns={'assistsplayer_6': 'RedTopAssists'})
    df = df.rename(columns={'assistsplayer_7': 'RedJungleAssists'})
    df = df.rename(columns={'assistsplayer_8': 'RedMidAssists'})
    df = df.rename(columns={'assistsplayer_9': 'RedADCAssists'})
    df = df.rename(columns={'assistsplayer_10':'RedSupportAssists'})

    # Rename Deaths
    df = df.rename(columns={'deathsplayer_1': 'BlueTopDeaths'})
    df = df.rename(columns={'deathsplayer_2': 'BlueJungleDeaths'})
    df = df.rename(columns={'deathsplayer_3': 'BlueMidDeaths'})
    df = df.rename(columns={'deathsplayer_4': 'BlueADCDeaths'})
    df = df.rename(columns={'deathsplayer_5': 'BlueSupportDeaths'})
    df = df.rename(columns={'deathsplayer_6': 'RedTopDeaths'})
    df = df.rename(columns={'deathsplayer_7': 'RedJungleDeaths'})
    df = df.rename(columns={'deathsplayer_8': 'RedMidDeaths'})
    df = df.rename(columns={'deathsplayer_9': 'RedADCDeaths'})
    df = df.rename(columns={'deathsplayer_10':'RedSupportDeaths'})

    # Rename Current Gold
    df = df.rename(columns={'currentGold_1' :'BlueTopCurrentGold'})
    df = df.rename(columns={'currentGold_2' :'BlueJungleCurrentGold'})
    df = df.rename(columns={'currentGold_3' :'BlueMidCurrentGold'})
    df = df.rename(columns={'currentGold_4' :'BlueADCCurrentGold'})
    df = df.rename(columns={'currentGold_5' :'BlueSupportCurrentGold'})
    df = df.rename(columns={'currentGold_6' :'RedTopCurrentGold'})
    df = df.rename(columns={'currentGold_7' :'RedJungleCurrentGold'})
    df = df.rename(columns={'currentGold_8' :'RedMidCurrentGold'})
    df = df.rename(columns={'currentGold_9' :'RedADCCurrentGold'})
    df = df.rename(columns={'currentGold_10' :'RedSupportCurrentGold'})

    # Rename Gold Per Sec
    df = df.rename(columns={'goldPerSecond_1': 'BlueTopgoldPerSecond'})
    df = df.rename(columns={'goldPerSecond_2': 'BlueJunglegoldPerSecond'})
    df = df.rename(columns={'goldPerSecond_3': 'BlueMidgoldPerSecond'})
    df = df.rename(columns={'goldPerSecond_4': 'BlueADCgoldPerSecond'})
    df = df.rename(columns={'goldPerSecond_5': 'BlueSupportgoldPerSecond'})
    df = df.rename(columns={'goldPerSecond_6': 'RedTopgoldPerSecond'})
    df = df.rename(columns={'goldPerSecond_7': 'RedJunglegoldPerSecond'})
    df = df.rename(columns={'goldPerSecond_8': 'RedMidgoldPerSecond'})
    df = df.rename(columns={'goldPerSecond_9': 'RedADCgoldPerSecond'})
    df = df.rename(columns={'goldPerSecond_10':'RedSupportgoldPerSecond'})

    # Rename Jungle Minions Killed
    df = df.rename(columns={'jungleMinionsKilled_1': 'BlueTopJungleMinionsKilled'})
    df = df.rename(columns={'jungleMinionsKilled_2': 'BlueJungleJungleMinionsKilled'})
    df = df.rename(columns={'jungleMinionsKilled_3': 'BlueMidJungleMinionsKilled'})
    df = df.rename(columns={'jungleMinionsKilled_4': 'BlueADCJungleMinionsKilled'})
    df = df.rename(columns={'jungleMinionsKilled_5': 'BlueSupportJungleMinionsKilled'})
    df = df.rename(columns={'jungleMinionsKilled_6': 'RedTopJungleMinionsKilled'})
    df = df.rename(columns={'jungleMinionsKilled_7': 'RedJungleJungleMinionsKilled'})
    df = df.rename(columns={'jungleMinionsKilled_8': 'RedMidJungleMinionsKilled'})
    df = df.rename(columns={'jungleMinionsKilled_9': 'RedADCJungleMinionsKilled'})
    df = df.rename(columns={'jungleMinionsKilled_10':'RedSupportJungleMinionsKilled'})

    # Rename Level
    df = df.rename(columns={'level_1': 'BlueTopLevel'})
    df = df.rename(columns={'level_2': 'BlueJungleLevel'})
    df = df.rename(columns={'level_3': 'BlueMidLevel'})
    df = df.rename(columns={'level_4': 'BlueADCLevel'})
    df = df.rename(columns={'level_5': 'BlueSupportLevel'})
    df = df.rename(columns={'level_6': 'RedTopLevel'})
    df = df.rename(columns={'level_7': 'RedJungleLevel'})
    df = df.rename(columns={'level_8': 'RedMidLevel'})
    df = df.rename(columns={'level_9': 'RedADCLevel'})
    df = df.rename(columns={'level_10':'RedSupportLevel'})

    # Rename Minions Killed
    df = df.rename(columns={'minionsKilled_1': 'BlueTopMinionsKilled'})
    df = df.rename(columns={'minionsKilled_2': 'BlueJungleMinionsKilled'})
    df = df.rename(columns={'minionsKilled_3': 'BlueMidMinionsKilled'})
    df = df.rename(columns={'minionsKilled_4': 'BlueADCMinionsKilled'})
    df = df.rename(columns={'minionsKilled_5': 'BlueSupportMinionsKilled'})
    df = df.rename(columns={'minionsKilled_6': 'RedTopMinionsKilled'})
    df = df.rename(columns={'minionsKilled_7': 'RedJungleMinionsKilled'})
    df = df.rename(columns={'minionsKilled_8': 'RedMidMinionsKilled'})
    df = df.rename(columns={'minionsKilled_9': 'RedADCMinionsKilled'})
    df = df.rename(columns={'minionsKilled_10':'RedSupportMinionsKilled'})

    # Rename Physical Damage Doen To Champions
    df = df.rename(columns={'physicalDamageDoneToChampions_1': 'BlueTopPhysicalDamageDoneToChampions'})
    df = df.rename(columns={'physicalDamageDoneToChampions_2': 'BlueJunglePhysicalDamageDoneToChampions'})
    df = df.rename(columns={'physicalDamageDoneToChampions_3': 'BlueMidPhysicalDamageDoneToChampions'})
    df = df.rename(columns={'physicalDamageDoneToChampions_4': 'BlueADCPhysicalDamageDoneToChampions'})
    df = df.rename(columns={'physicalDamageDoneToChampions_5': 'BlueSupportPhysicalDamageDoneToChampions'})
    df = df.rename(columns={'physicalDamageDoneToChampions_6': 'RedTopPhysicalDamageDoneToChampions'})
    df = df.rename(columns={'physicalDamageDoneToChampions_7': 'RedJunglePhysicalDamageDoneToChampions'})
    df = df.rename(columns={'physicalDamageDoneToChampions_8': 'RedMidPhysicalDamageDoneToChampions'})
    df = df.rename(columns={'physicalDamageDoneToChampions_9': 'RedADCPhysicalDamageDoneToChampions'})
    df = df.rename(columns={'physicalDamageDoneToChampions_10':'RedSupportPhysicalDamageDoneToChampions'})

    # Rename Time Enemy Spent Controlled
    df = df.rename(columns={'timeEnemySpentControlled_1': 'BlueTopTimeEnemySpentControlled'})
    df = df.rename(columns={'timeEnemySpentControlled_2': 'BlueJungleTimeEnemySpentControlled'})
    df = df.rename(columns={'timeEnemySpentControlled_3': 'BlueMidTimeEnemySpentControlled'})
    df = df.rename(columns={'timeEnemySpentControlled_4': 'BlueADCTimeEnemySpentControlled'})
    df = df.rename(columns={'timeEnemySpentControlled_5': 'BlueSupportTimeEnemySpentControlled'})
    df = df.rename(columns={'timeEnemySpentControlled_6': 'RedTopTimeEnemySpentControlled'})
    df = df.rename(columns={'timeEnemySpentControlled_7': 'RedJungleTimeEnemySpentControlled'})
    df = df.rename(columns={'timeEnemySpentControlled_8': 'RedMidTimeEnemySpentControlled'})
    df = df.rename(columns={'timeEnemySpentControlled_9': 'RedADCTimeEnemySpentControlled'})
    df = df.rename(columns={'timeEnemySpentControlled_10':'RedSupportTimeEnemySpentControlled'})

    # Rename Total Damage Done to Champions
    df = df.rename(columns={'totalDamageDoneToChampions_1': 'BlueTopTotalDamageDoneToChampions'})
    df = df.rename(columns={'totalDamageDoneToChampions_2': 'BlueJungleTotalDamageDoneToChampions'})
    df = df.rename(columns={'totalDamageDoneToChampions_3': 'BlueMidTotalDamageDoneToChampions'})
    df = df.rename(columns={'totalDamageDoneToChampions_4': 'BlueADCTotalDamageDoneToChampions'})
    df = df.rename(columns={'totalDamageDoneToChampions_5': 'BlueSupportTotalDamageDoneToChampions'})
    df = df.rename(columns={'totalDamageDoneToChampions_6': 'RedTopTotalDamageDoneToChampions'})
    df = df.rename(columns={'totalDamageDoneToChampions_7': 'RedJungleTotalDamageDoneToChampions'})
    df = df.rename(columns={'totalDamageDoneToChampions_8': 'RedMidTotalDamageDoneToChampions'})
    df = df.rename(columns={'totalDamageDoneToChampions_9': 'RedADCTotalDamageDoneToChampions'})
    df = df.rename(columns={'totalDamageDoneToChampions_10':'RedSupportTotalDamageDoneToChampions'})

    # Rename Total Gold
    df = df.rename(columns={'totalGold_1': 'BlueTopTotalGold'})
    df = df.rename(columns={'totalGold_2': 'BlueJungleTotalGold'})
    df = df.rename(columns={'totalGold_3': 'BlueMidTotalGold'})
    df = df.rename(columns={'totalGold_4': 'BlueADCTotalGold'})
    df = df.rename(columns={'totalGold_5': 'BlueSupportTotalGold'})
    df = df.rename(columns={'totalGold_6': 'RedTopTotalGold'})
    df = df.rename(columns={'totalGold_7': 'RedJungleTotalGold'})
    df = df.rename(columns={'totalGold_8': 'RedMidTotalGold'})
    df = df.rename(columns={'totalGold_9': 'RedADCTotalGold'})
    df = df.rename(columns={'totalGold_10':'RedSupportTotalGold'})

    # Rename True Damage Done To Champions
    df = df.rename(columns={'trueDamageDoneToChampions_1': 'BlueTopTrueDamageDoneToChampions'})
    df = df.rename(columns={'trueDamageDoneToChampions_2': 'BlueJungleTrueDamageDoneToChampions'})
    df = df.rename(columns={'trueDamageDoneToChampions_3': 'BlueMidTrueDamageDoneToChampions'})
    df = df.rename(columns={'trueDamageDoneToChampions_4': 'BlueADCTrueDamageDoneToChampions'})
    df = df.rename(columns={'trueDamageDoneToChampions_5': 'BlueSupportTrueDamageDoneToChampions'})
    df = df.rename(columns={'trueDamageDoneToChampions_6': 'RedTopTrueDamageDoneToChampions'})
    df = df.rename(columns={'trueDamageDoneToChampions_7': 'RedJungleTrueDamageDoneToChampions'})
    df = df.rename(columns={'trueDamageDoneToChampions_8': 'RedMidTrueDamageDoneToChampions'})
    df = df.rename(columns={'trueDamageDoneToChampions_9': 'RedADCTrueDamageDoneToChampions'})
    df = df.rename(columns={'trueDamageDoneToChampions_10':'RedSupportTrueDamageDoneToChampions'})

    # Rename Magic Damage Done To Champions 
    df = df.rename(columns={'magicDamageDoneToChampions_1': 'BlueTopMagicDamageDoneToChampions'})
    df = df.rename(columns={'magicDamageDoneToChampions_2': 'BlueJungleMagicDamageDoneToChampions'})
    df = df.rename(columns={'magicDamageDoneToChampions_3': 'BlueMidMagicDamageDoneToChampions'})
    df = df.rename(columns={'magicDamageDoneToChampions_4': 'BlueADCMagicDamageDoneToChampions'})
    df = df.rename(columns={'magicDamageDoneToChampions_5': 'BlueSupportMagicDamageDoneToChampions'})
    df = df.rename(columns={'magicDamageDoneToChampions_6': 'RedTopMagicDamageDoneToChampions'})
    df = df.rename(columns={'magicDamageDoneToChampions_7': 'RedJungleMagicDamageDoneToChampions'})
    df = df.rename(columns={'magicDamageDoneToChampions_8': 'RedMidMagicDamageDoneToChampions'})
    df = df.rename(columns={'magicDamageDoneToChampions_9': 'RedADCMagicDamageDoneToChampions'})
    df = df.rename(columns={'magicDamageDoneToChampions_10':'RedSupportMagicDamageDoneToChampions'})

    # Rename Wards
    df = df.rename(columns={'ward_player_1': 'BlueTopWard'})
    df = df.rename(columns={'ward_player_2': 'BlueJungleWard'})
    df = df.rename(columns={'ward_player_3': 'BlueMidWard'})
    df = df.rename(columns={'ward_player_4': 'BlueADCWard'})
    df = df.rename(columns={'ward_player_5': 'BlueSupportWard'})
    df = df.rename(columns={'ward_player_6': 'RedTopWard'})
    df = df.rename(columns={'ward_player_7': 'RedJungleWard'})
    df = df.rename(columns={'ward_player_8': 'RedMidWard'})
    df = df.rename(columns={'ward_player_9': 'RedADCWard'})
    df = df.rename(columns={'ward_player_10':'RedSupportWard'})

    # Rename Xp
    df = df.rename(columns={'xp_1': 'BlueTopXp'})
    df = df.rename(columns={'xp_2': 'BlueJungleXp'})
    df = df.rename(columns={'xp_3': 'BlueMidXp'})
    df = df.rename(columns={'xp_4': 'BlueADCXp'})
    df = df.rename(columns={'xp_5': 'BlueSupportXp'})
    df = df.rename(columns={'xp_6': 'RedTopXp'})
    df = df.rename(columns={'xp_7': 'RedJungleXp'})
    df = df.rename(columns={'xp_8': 'RedMidXp'})
    df = df.rename(columns={'xp_9': 'RedADCXp'})
    df = df.rename(columns={'xp_10':'RedSupportXp'})

    # Rename Inhibs Lost
    df = df.rename(columns={'inhibs_lost_team100': 'BlueTeamInhibsLost'})
    df = df.rename(columns={'inhibs_lost_team200': 'RedTeamInhibsLost'})

    # Rename Rift Heralds
    df = df.rename(columns={'riftherald_team100': 'BlueTeamRiftHeralds'})
    df = df.rename(columns={'riftherald_team200': 'RedTeamRiftHeralds'})

    # Rename Kills Towers Lost
    df = df.rename(columns={'towers_lost_team100': 'BlueTeamTowersLost'})
    df = df.rename(columns={'towers_lost_team200': 'RedTeamTowersLost'})

    # Rename Individual Dragons
    df = df.rename(columns={'chemtechdragon_team100':'BlueTeamChemtechDragon'})
    df = df.rename(columns={'chemtechdragon_team200':'RedTeamChemtechDragon'})
    df = df.rename(columns={'airdragon_team100':'BlueTeamAirDragon'})
    df = df.rename(columns={'airdragon_team200':'RedTeamAirDragon'})
    df = df.rename(columns={'waterdragon_team100':'BlueTeamWaterDragon'})
    df = df.rename(columns={'waterdragon_team200':'RedTeamWaterDragon'})
    df = df.rename(columns={'hextechdragon_team100':'BlueTeamHextechDragonDragon'})
    df = df.rename(columns={'hextechdragon_team200':'RedTeamHextechDragonDragon'})
    df = df.rename(columns={'earthdragon_team100':'BlueTeamEarthDragon'})
    df = df.rename(columns={'earthdragon_team200':'RedTeamEarthDragon'})
    df = df.rename(columns={'firedragon_team100':'BlueTeamFireDragon'})
    df = df.rename(columns={'firedragon_team200':'RedTeamFireDragon'})

    # Rename Barons
    df = df.rename(columns={'baron_team100':'BlueTeamBarons'})
    df = df.rename(columns={'baron_team200':'RedTeamBarons'})

    # Rename totalDragons
    df = df.rename(columns={'dragon_team100':'BlueTeamDragons'})
    df = df.rename(columns={'dragon_team200':'RedTeamDragons'})
    
    return df