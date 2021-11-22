import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from env import api_key
import time
import re
from time import sleep
import os

def acquire():
    df = pd.read_csv("final.csv")
    return df

def extract(timeline_data, other_game_data, time):
    #columns = ['assistsplayer_10', 'assistsplayer_2', 'assistsplayer_3', 'assistsplayer_4', 'assistsplayer_5', 'assistsplayer_8', 'assistsplayer_9', 'assistsplayer_1' 'currentGold_1', 'currentGold_10', 'currentGold_2', 'currentGold_3', 'currentGold_4', 'currentGold_5', 'currentGold_6', 'currentGold_7', 'currentGold_8', 'currentGold_9', 'deathsplayer_1', 'deathsplayer_10', 'deathsplayer_2', 'deathsplayer_3', 'deathsplayer_4', 'deathsplayer_5', 'deathsplayer_6', 'deathsplayer_7', 'deathsplayer_8', 'deathsplayer_9', 'dragon_team100', 'dragon_team200', 'firedragon_team100', 'firedragon_team200', 'gameDuration', 'gameEndTimestamp', 'gameId', 'gameMode', 'gameName', 'gameStartTimestamp', 'gameType', 'gameVersion', 'goldPerSecond_1', 'goldPerSecond_10', 'goldPerSecond_2', 'goldPerSecond_3', 'goldPerSecond_4', 'goldPerSecond_5', 'goldPerSecond_6', 'goldPerSecond_7', 'goldPerSecond_8', 'goldPerSecond_9', 'hextechdragon_team200', 'inhibs_lost_team200', 'jungleMinionsKilled_1', 'jungleMinionsKilled_10', 'jungleMinionsKilled_2', 'jungleMinionsKilled_3', 'jungleMinionsKilled_4', 'jungleMinionsKilled_5', 'jungleMinionsKilled_6', 'jungleMinionsKilled_7', 'jungleMinionsKilled_8', 'jungleMinionsKilled_9', 'killsplayer_1', 'killsplayer_2', 'killsplayer_3', 'killsplayer_4', 'killsplayer_5', 'killsplayer_6', 'killsplayer_7', 'killsplayer_8', 'killsplayer_9', 'killsplayer_10', 'level_1', 'level_10', 'level_2', 'level_3', 'level_4', 'level_5', 'level_6', 'level_7', 'level_8', 'level_9', 'magicDamageDoneToChampions_1', 'magicDamageDoneToChampions_10', 'magicDamageDoneToChampions_2', 'magicDamageDoneToChampions_3', 'magicDamageDoneToChampions_4', 'magicDamageDoneToChampions_5', 'magicDamageDoneToChampions_6', 'magicDamageDoneToChampions_7', 'magicDamageDoneToChampions_8', 'magicDamageDoneToChampions_9', 'matchId', 'minionsKilled_1', 'minionsKilled_10', 'minionsKilled_2', 'minionsKilled_3', 'minionsKilled_4', 'minionsKilled_5', 'minionsKilled_6', 'minionsKilled_7', 'minionsKilled_8', 'minionsKilled_9', 'physicalDamageDoneToChampions_1', 'physicalDamageDoneToChampions_10', 'physicalDamageDoneToChampions_2', 'physicalDamageDoneToChampions_3', 'physicalDamageDoneToChampions_4', 'physicalDamageDoneToChampions_5', 'physicalDamageDoneToChampions_6', 'physicalDamageDoneToChampions_7', 'physicalDamageDoneToChampions_8', 'physicalDamageDoneToChampions_9', 'queueId', 'riftherald_team100', 'timeEnemySpentControlled_1', 'timeEnemySpentControlled_10', 'timeEnemySpentControlled_2', 'timeEnemySpentControlled_3', 'timeEnemySpentControlled_4', 'timeEnemySpentControlled_5', 'timeEnemySpentControlled_6', 'timeEnemySpentControlled_7', 'timeEnemySpentControlled_8', 'timeEnemySpentControlled_9', 'timestamp', 'totalDamageDoneToChampions_1', 'totalDamageDoneToChampions_10', 'totalDamageDoneToChampions_2', 'totalDamageDoneToChampions_3', 'totalDamageDoneToChampions_4', 'totalDamageDoneToChampions_5', 'totalDamageDoneToChampions_6', 'totalDamageDoneToChampions_7', 'totalDamageDoneToChampions_8', 'totalDamageDoneToChampions_9', 'totalGold_1', 'totalGold_10', 'totalGold_2', 'totalGold_3', 'totalGold_4', 'totalGold_5', 'totalGold_6', 'totalGold_7', 'totalGold_8', 'totalGold_9', 'towers_lost_team100', 'towers_lost_team200', 'trueDamageDoneToChampions_1', 'trueDamageDoneToChampions_10', 'trueDamageDoneToChampions_2', 'trueDamageDoneToChampions_3', 'trueDamageDoneToChampions_4', 'trueDamageDoneToChampions_5', 'trueDamageDoneToChampions_6', 'trueDamageDoneToChampions_7', 'trueDamageDoneToChampions_8', 'trueDamageDoneToChampions_9', 'ward_player_1', 'ward_player_10', 'ward_player_2', 'ward_player_3', 'ward_player_4', 'ward_player_5', 'ward_player_6', 'ward_player_7', 'ward_player_8', 'ward_player_9', 'waterdragon_team100', 'winningTeam', 'xp_1', 'xp_10', 'xp_2', 'xp_3', 'xp_4', 'xp_5', 'xp_6', 'xp_7', 'xp_8', 'xp_9', 'airdragon_team100', 'assistsplayer_7', 'chemtechdragon_team100', 'earthdragon_team100', 'killsplayer_10', 'killsplayer_6', 'killsplayer_8', 'riftherald_team300', 'assistsplayer_1', 'baron_team100', 'earthdragon_team200', 'ward_player_0']
    df = pd.DataFrame()
    
    for index, timedata in enumerate(timeline_data):
        
        # Grabbing Game Duration and Game Mode
        game_duration = other_game_data[index]['info']['gameDuration']
        game_mode = str(other_game_data[index]['info']['gameMode'])
                        
        # Checking if game is a classic game and more than 15 min
        if (int(game_duration) >= 1500) & (game_mode == 'CLASSIC'): 
            
            # Creating an empty dictionary
            final_d = {}
            
            # Using timeline data to extract events, up to a specific time, and add them up to create totals
            kda = get_player_kda(timedata, time)
            
            # Saving totals (kda) to final_d
            final_d.update(kda)
            
            # Using timeline data to extract player stats at a specific time
            final_d.update(get_player_stats(timedata, time))
            
            # Using other_game_data to grab additional overall game data
            final_d.update(get_more_info(other_game_data[index], time))
            
            # Save to DataFrame
            df = df.append(final_d, ignore_index=True)
            
            print(f"Finished with: {index} of {len(timeline_data)-1}")
            
        else:
            print(f"Skipping: {index} due to <{time} min or not classic")
    print("Done! now lets get some korean bbq, more chicken plz! haha....follow suit")
    return df

def get_more_info(data, time):

    d = {}
    d['time_cutoff'] = time
    d["gameMode"] = str(data['info']['gameMode'])
    d["gameType"] = str(data['info']['gameType'])
    d['gameVersion'] = str(data['info']['gameVersion'])
    d['gameDuration'] = str(data['info']['gameDuration'])
    d['matchId'] = str(data['metadata']['matchId'])
    d['gameId'] = str(data['info']['gameId'])
    d['gameName'] = str(data['info']['gameName'])
    d['gameStartTimestamp'] = str(data['info']['gameStartTimestamp'])
    d['gameEndTimestamp'] = str(data['info']['gameEndTimestamp'])
    d['queueId'] = str(data['info']['queueId'])
    
    return d

def get_player_kda(data, time):
    
    df = pd.DataFrame()
    for index in range(len(data['info']['frames'])):
        for event in data['info']['frames'][index]['events']:
            if event['type'] == 'CHAMPION_KILL':
                df = df.append(event, ignore_index =True)
            

    df.timestamp = df.timestamp / 60_000

    kills_df = df[(df.type== 'CHAMPION_KILL') & (df.timestamp <= time)]

    d= {'assistsplayer_10':0, 'assistsplayer_2':0, 'assistsplayer_6':0,'assistsplayer_7':0,'assistsplayer_3':0, 'assistsplayer_4':0, 'assistsplayer_5':0, 'assistsplayer_8':0, 'assistsplayer_9':0, 'assistsplayer_1':0, 'currentGold_1':0, 'currentGold_10':0, 'currentGold_2':0, 'currentGold_3':0, 'currentGold_4':0, 'currentGold_5':0, 'currentGold_6':0, 'currentGold_7':0, 'currentGold_8':0, 'currentGold_9':0, 'deathsplayer_1':0, 'deathsplayer_10':0, 'deathsplayer_2':0, 'deathsplayer_3':0, 'deathsplayer_4':0, 'deathsplayer_5':0, 'deathsplayer_6':0, 'deathsplayer_7':0, 'deathsplayer_8':0, 'deathsplayer_9':0, 'dragon_team100':0, 'dragon_team200':0, 'firedragon_team100':0, 'firedragon_team200':0, 'gameDuration':0, 'gameEndTimestamp':0, 'gameId':0, 'gameMode':0, 'gameName':0, 'gameStartTimestamp':0, 'gameType':0, 'gameVersion':0, 'goldPerSecond_1':0, 'goldPerSecond_10':0, 'goldPerSecond_2':0, 'goldPerSecond_3':0, 'goldPerSecond_4':0, 'goldPerSecond_5':0, 'goldPerSecond_6':0, 'goldPerSecond_7':0, 'goldPerSecond_8':0, 'goldPerSecond_9':0, 'hextechdragon_team200':0, 'inhibs_lost_team200':0, 'jungleMinionsKilled_1':0, 'jungleMinionsKilled_10':0, 'jungleMinionsKilled_2':0, 'jungleMinionsKilled_3':0, 'jungleMinionsKilled_4':0, 'jungleMinionsKilled_5':0, 'jungleMinionsKilled_6':0, 'jungleMinionsKilled_7':0, 'jungleMinionsKilled_8':0, 'jungleMinionsKilled_9':0, 'killsplayer_1':0, 'killsplayer_2':0, 'killsplayer_3':0, 'killsplayer_4':0, 'killsplayer_5':0, 'killsplayer_6':0, 'killsplayer_0':0,'killsplayer_7':0, 'killsplayer_8':0, 'killsplayer_9':0, 'killsplayer_10':0, 'level_1':0, 'level_10':0, 'level_2':0, 'level_3':0, 'level_4':0, 'level_5':0, 'level_6':0, 'level_7':0, 'level_8':0, 'level_9':0, 'magicDamageDoneToChampions_1':0, 'magicDamageDoneToChampions_10':0, 'magicDamageDoneToChampions_2':0, 'magicDamageDoneToChampions_3':0, 'magicDamageDoneToChampions_4':0, 'magicDamageDoneToChampions_5':0, 'magicDamageDoneToChampions_6':0, 'magicDamageDoneToChampions_7':0, 'magicDamageDoneToChampions_8':0, 'magicDamageDoneToChampions_9':0, 'matchId':0, 'minionsKilled_1':0, 'minionsKilled_10':0, 'minionsKilled_2':0, 'minionsKilled_3':0, 'minionsKilled_4':0, 'minionsKilled_5':0, 'minionsKilled_6':0, 'minionsKilled_7':0, 'minionsKilled_8':0, 'minionsKilled_9':0, 'physicalDamageDoneToChampions_1':0, 'physicalDamageDoneToChampions_10':0, 'physicalDamageDoneToChampions_2':0, 'physicalDamageDoneToChampions_3':0, 'physicalDamageDoneToChampions_4':0, 'physicalDamageDoneToChampions_5':0, 'physicalDamageDoneToChampions_6':0, 'physicalDamageDoneToChampions_7':0, 'physicalDamageDoneToChampions_8':0, 'physicalDamageDoneToChampions_9':0, 'queueId':0, 'riftherald_team100':0, 'timeEnemySpentControlled_1':0, 'timeEnemySpentControlled_10':0, 'timeEnemySpentControlled_2':0, 'timeEnemySpentControlled_3':0, 'timeEnemySpentControlled_4':0, 'timeEnemySpentControlled_5':0, 'timeEnemySpentControlled_6':0, 'timeEnemySpentControlled_7':0, 'timeEnemySpentControlled_8':0, 'timeEnemySpentControlled_9':0, 'timestamp':0, 'totalDamageDoneToChampions_1':0, 'totalDamageDoneToChampions_10':0, 'totalDamageDoneToChampions_2':0, 'totalDamageDoneToChampions_3':0, 'totalDamageDoneToChampions_4':0, 'totalDamageDoneToChampions_5':0, 'totalDamageDoneToChampions_6':0, 'totalDamageDoneToChampions_7':0, 'totalDamageDoneToChampions_8':0, 'totalDamageDoneToChampions_9':0, 'totalGold_1':0, 'totalGold_10':0, 'totalGold_2':0, 'totalGold_3':0, 'totalGold_4':0, 'totalGold_5':0, 'totalGold_6':0, 'totalGold_7':0, 'totalGold_8':0, 'totalGold_9':0, 'towers_lost_team100':0, 'towers_lost_team200':0, 'trueDamageDoneToChampions_1':0, 'trueDamageDoneToChampions_10':0, 'trueDamageDoneToChampions_2':0, 'trueDamageDoneToChampions_3':0, 'trueDamageDoneToChampions_4':0, 'trueDamageDoneToChampions_5':0, 'trueDamageDoneToChampions_6':0, 'trueDamageDoneToChampions_7':0, 'trueDamageDoneToChampions_8':0, 'trueDamageDoneToChampions_9':0, 'ward_player_1':0, 'ward_player_10':0, 'ward_player_2':0, 'ward_player_3':0, 'ward_player_4':0, 'ward_player_5':0, 'ward_player_6':0, 'ward_player_7':0, 'ward_player_8':0, 'ward_player_9':0, 'waterdragon_team100':0, 'winningTeam':0, 'xp_1':0, 'xp_10':0, 'xp_2':0, 'xp_3':0, 'xp_4':0, 'xp_5':0, 'xp_6':0, 'xp_7':0, 'xp_8':0, 'xp_9':0, 'airdragon_team100':0, 'assistsplayer_7':0, 'chemtechdragon_team100':0, 'earthdragon_team100':0, 'killsplayer_10':0, 'killsplayer_6':0, 'killsplayer_8':0, 'riftherald_team300':0, 'assistsplayer_1':0, 'baron_team100':0, 'earthdragon_team200':0, 'ward_player_0':0}

    mylist = []
    for value in kills_df.assistingParticipantIds:
        if type(value) == list:
            for assist in value:
                mylist.append(assist)
    temp = pd.DataFrame(mylist)

    for index, player in enumerate(kills_df.killerId.value_counts().sort_index()):

        # Grabbing kills and saving values to same dictionary
        d['killsplayer_'+str(int(kills_df.killerId.value_counts().sort_index().index[index]))] =\
        kills_df.killerId.value_counts().sort_index().iloc[index]

        # Grabbing deaths and saving values to same dictionary
    for index, player in enumerate(kills_df.victimId.value_counts().sort_index()):
        d['deathsplayer_'+str(int(kills_df.victimId.value_counts().sort_index().index[index]))] =\
        kills_df.victimId.value_counts().sort_index().iloc[index]

        # Grabbing assists and saving values to same dictionary
    if temp.empty:
        print("")# Do nothing
    else:
        for index, player in enumerate(temp[0].value_counts().sort_index()):
            d['assistsplayer_'+str(temp[0].value_counts().sort_index().index[index])] = temp.value_counts().sort_index().iloc[index]

    df = pd.DataFrame()
    for index in range(len(data['info']['frames'])):
        for event in data['info']['frames'][index]['events']:
            if event['type'] == 'ELITE_MONSTER_KILL':
                df = df.append(event, ignore_index =True)
            elif event['type']== 'GAME_END':
                df = df.append(event, ignore_index =True)
    
    df.timestamp = df.timestamp / 60_000

    kills_df = df[(df.type == 'ELITE_MONSTER_KILL')  & (df.timestamp <= time)]

    for index, player in enumerate(kills_df[kills_df.monsterType=='DRAGON'].killerTeamId.value_counts().sort_index()):

        # Grabbing dragons and saving values to same dictionary
        d['dragon_team'+str(int(kills_df[kills_df.monsterType=='DRAGON'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterType=='DRAGON'].killerTeamId.value_counts().sort_index().iloc[index]

    for index, player in enumerate(kills_df[kills_df.monsterSubType=='CHEMTECH_DRAGON'].killerTeamId.value_counts().sort_index()):

        # Grabbing dragons and saving values to same dictionary
        d['chemtechdragon_team'+str(int(kills_df[kills_df.monsterSubType=='CHEMTECH_DRAGON'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterSubType=='CHEMTECH_DRAGON'].killerTeamId.value_counts().sort_index().iloc[index]

    for index, player in enumerate(kills_df[kills_df.monsterSubType=='HEXTECH_DRAGON'].killerTeamId.value_counts().sort_index()):

        # Grabbing dragons and saving values to same dictionary
        d['hextechdragon_team'+str(int(kills_df[kills_df.monsterSubType=='HEXTECH_DRAGON'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterSubType=='HEXTECH_DRAGON'].killerTeamId.value_counts().sort_index().iloc[index]

    for index, player in enumerate(kills_df[kills_df.monsterSubType=='WATER_DRAGON'].killerTeamId.value_counts().sort_index()):

        # Grabbing dragons and saving values to same dictionary
        d['waterdragon_team'+str(int(kills_df[kills_df.monsterSubType=='WATER_DRAGON'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterSubType=='WATER_DRAGON'].killerTeamId.value_counts().sort_index().iloc[index]

    for index, player in enumerate(kills_df[kills_df.monsterSubType=='FIRE_DRAGON'].killerTeamId.value_counts().sort_index()):

        # Grabbing dragons and saving values to same dictionary
        d['firedragon_team'+str(int(kills_df[kills_df.monsterSubType=='FIRE_DRAGON'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterSubType=='FIRE_DRAGON'].killerTeamId.value_counts().sort_index().iloc[index]

    for index, player in enumerate(kills_df[kills_df.monsterSubType=='EARTH_DRAGON'].killerTeamId.value_counts().sort_index()):

        # Grabbing dragons and saving values to same dictionary
        d['earthdragon_team'+str(int(kills_df[kills_df.monsterSubType=='EARTH_DRAGON'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterSubType=='EARTH_DRAGON'].killerTeamId.value_counts().sort_index().iloc[index]

    for index, player in enumerate(kills_df[kills_df.monsterSubType=='AIR_DRAGON'].killerTeamId.value_counts().sort_index()):

        # Grabbing dragons and saving values to same dictionary
        d['airdragon_team'+str(int(kills_df[kills_df.monsterSubType=='AIR_DRAGON'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterSubType=='AIR_DRAGON'].killerTeamId.value_counts().sort_index().iloc[index]
        
    for index, player in enumerate(kills_df[kills_df.monsterType=='RIFTHERALD'].killerTeamId.value_counts().sort_index()):

        # Grabbing riftherald and saving values to same dictionary
        d['riftherald_team'+str(int(kills_df[kills_df.monsterType=='RIFTHERALD'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterType=='RIFTHERALD'].killerTeamId.value_counts().sort_index().iloc[index]

    for index, player in enumerate(kills_df[kills_df.monsterType=='BARON_NASHOR'].killerTeamId.value_counts().sort_index()):

        # Grabbing baron and saving values to same dictionary
        d['baron_team'+str(int(kills_df[kills_df.monsterType=='BARON_NASHOR'].killerTeamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.monsterType=='BARON_NASHOR'].killerTeamId.value_counts().sort_index().iloc[index]

    # Grabbing target, winning team
    d['winningTeam'] = int(df[df.type == 'GAME_END'].winningTeam)

    df = pd.DataFrame()
    for index in range(len(data['info']['frames'])):
        for event in data['info']['frames'][index]['events']:
            if event['type'] == 'WARD_PLACED':
                df = df.append(event, ignore_index =True)
    
    df.timestamp = df.timestamp / 60_000

    kills_df = df[(df.type == 'WARD_PLACED')  & (df.timestamp <= time)]

    for index, player in enumerate(kills_df[kills_df.type=='WARD_PLACED'].creatorId.value_counts().sort_index()):

        # Grabbing baron and saving values to same dictionary
        d['ward_player_'+str(int(kills_df[kills_df.type=='WARD_PLACED'].creatorId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.type=='WARD_PLACED'].creatorId.value_counts().sort_index().iloc[index]
    df = pd.DataFrame()
    
    for index in range(len(data['info']['frames'])):
        for event in data['info']['frames'][index]['events']:
            if event['type'] == 'BUILDING_KILL':
                df = df.append(event, ignore_index =True)

    df.timestamp = df.timestamp / 60_000

    kills_df = df[(df.type == 'BUILDING_KILL')  & (df.timestamp <= time)]

    for index, player in enumerate(kills_df[kills_df.buildingType =='TOWER_BUILDING'].teamId.value_counts().sort_index()):

        # Grabbing baron and saving values to same dictionary
        d['towers_lost_team'+str(int(kills_df[kills_df.buildingType =='TOWER_BUILDING'].teamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.buildingType =='TOWER_BUILDING'].teamId.value_counts().sort_index().iloc[index]
    
    for index, player in enumerate(kills_df[kills_df.buildingType =='INHIBITOR_BUILDING'].teamId.value_counts().sort_index()):

        # Grabbing baron and saving values to same dictionary
        d['inhibs_lost_team'+str(int(kills_df[kills_df.buildingType =='INHIBITOR_BUILDING'].teamId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.buildingType =='INHIBITOR_BUILDING'].teamId.value_counts().sort_index().iloc[index]


    return d

def get_player_stats(data, time):
    player_stats = []

    #Here, each timeframe represents about one minute
    timeframe = data['info']['frames'][time]
    players = timeframe['participantFrames']
    #Now create a dicitonary to hold the players' stats from this timeframe
    players_dict = {}
    for i in range(1, len(players) + 1):
        #Now create a temp dict to store the current players stats
        #Use formatted strings to automatically increment the player label
        temp_dict = {
            f'currentGold_{i}': players[str(i)]['currentGold'],
            f'magicDamageDoneToChampions_{i}': players[str(i)]['damageStats']['magicDamageDoneToChampions'],
            f'physicalDamageDoneToChampions_{i}': players[str(i)]['damageStats']['physicalDamageDoneToChampions'],
            f'trueDamageDoneToChampions_{i}': players[str(i)]['damageStats']['trueDamageDoneToChampions'],
            f'totalDamageDoneToChampions_{i}': players[str(i)]['damageStats']['totalDamageDoneToChampions'],
            f'goldPerSecond_{i}': players[str(i)]['goldPerSecond'],
            f'jungleMinionsKilled_{i}': players[str(i)]['jungleMinionsKilled'],
            f'level_{i}': players[str(i)]['level'],
            f'minionsKilled_{i}': players[str(i)]['minionsKilled'],
            f'timeEnemySpentControlled_{i}': players[str(i)]['timeEnemySpentControlled'],
            f'totalGold_{i}': players[str(i)]['totalGold'],
            f'xp_{i}': players[str(i)]['xp']
            }
        #Now that I have the current players stats, extend it to the overall players_dict
        players_dict.update(temp_dict)
    #Update the players_dict one more time with the timestamp for the timeframe
    players_dict.update({'timestamp' : timeframe['timestamp']})
    #Append the players_dict to the overall player_stats list of dicts
    player_stats.append(players_dict)
    return player_stats[0]

def get_new_patch_data(name_list, api_key):
    """
    This function takes in a list of usernames that are in the same tier and iterates 
    through them to find their puuids.
    It will then use those puuids to grab all of their match ids that are in the newest patch.
    From there, the function will iterate through all of the match ids and grab the timeline
    data for each match as well as the other game data. 
    Finally, this function will incrementally save the returned json information every 10 times.
    This prevents the loss of all data if the function errors out at some point.
    This function returns nothing.
    """
    
    #Set up the basegame number. Any match_ids below this number are part of the old patch
    #and will not be included. We will use the basegame var for comparisons in the loop
    basegame = 4107000001
    
    #Set up the base url for grabbing match_ids
    match_url = 'https://americas.api.riotgames.com/'
    
    #Set up the base url for grabbing puuids
    puuid_base_url = 'https://na1.api.riotgames.com/'
    
    #Set up another counter to keep track of how many users have been completed
    n = 0
    
    #Set up a counter to keep track of how many json files have been completed in total
    num_json = 0
    
    #Set up one more counter to keep track of how many pulls we have made.
    #Can't go over 100 pulls every 2 minutes.
    num_pulls = 0
    
    #Set up empty lists to store timeline and other game data
    timeline_data = []
    game_data = []
    
    #Loop through each name in the given name_list
    #First grab the puuid, then grab the match_ids, then actual match json info
    for name in name_list:
        
        #for testing
        print(f'Beginning Loop for user {name}')
        
        #Update n var
        n += 1
        
        #Leave a status update after every 100 users
        if n % 100 == 0:
            print(f'Completed {n} users of {len(name_list)}!\n')
        
        ########################## Get puuids ##########################
        
        #Set up the query
        query = f'lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}'
        
        #Get the response
        response = requests.get(puuid_base_url + query)
        
        #Update pull count and sleep for 150 seconds if necessary
        num_pulls += 1
        
        if num_pulls % 100 == 0:
            print('\nHit 100 pulls! Sleeping for 150 seconds.')
            sleep(150)
            print('Continuing!\n')
        
        #Check the response code and leave message if something goes wrong
        if response.status_code != 200:
            print(f'Something went wrong! Status Code: {response.status_code}. Did not get puuid for user: {name}')
            print(f'Skipping this user. There are {len(name_list) - n} users left.\n')
            continue
        
        #Grab the user's puuid
        puuid = response.json()['puuid']
        
        #For testing
        print(f'\t-Got the puuid for user {name}.')
        
        ########################## Get Match IDs #########################
        
        #Now that we have a single puuid, grab all the match ids for that user that are greater
        #than the basegame value. These match_ids will be for the newest patch.
        
        #Set up a counter
        i = 0
        
        #This loop will be set up to run indefinitely. Be sure to break out of it when 
        #Done with the current user
        while i >= 0:
            #Set up the query to get a match_id
            query = f'lol/match/v5/matches/by-puuid/{puuid}/ids?start={i}&count=1&api_key={api_key}'
            
            #Get the response
            response = requests.get(match_url + query)
            
            #Update pull count and sleep for 150 seconds if necessary
            num_pulls += 1

            if num_pulls % 100 == 0:
                print('\nHit 100 pulls! Sleeping for 150 seconds.')
                sleep(150)
                print('Continuing!\n')
            
            #Check response status code and leave message if something went wrong
            if response.status_code != 200:
                print(f'Something went wrong! Status Code: {response.status_code}. Did not get Match_ID for user: {name}')
                print(f'Skipping this user. There are {len(name_list) - n} users left.\n')
                break
                
            #Grab the match_id
            match = response.json()
            
            #Verify there's something in it
            if len(match) == 0:
                print(f'\t-No match ID for user {name}. Skipping this user!')
                break
            
            #Convert match_id to integer
            match_num = int(match[0].strip('NA1_'))
            
            #Compare current match_id to basegame var.
            #Skip if match_id is less than basegame
            if match_num < basegame:
                print(f'\t-Completed getting all current patch Match IDs for user {name}')
                print(f'\t-There are {len(name_list) - n} users left.')
                break

            ####################### Get Match Info ##########################
            
            #Now that we know the current match_id is part of the newest patch,
            #We can retrieve the actual match info. Keep in mind this is still part
            #of the while loop above
                
            #Every 250 entries, save the lists as json files and reset the lists
            if len(timeline_data) % 250 == 0:    
                #Save timeline data.
                #First, convert it to a df
                timeline_df = pd.DataFrame(timeline_data)

                #Save as json file. Use username string to identify whose file it is
                timeline_df.to_json(f'timeline_data_user_{name}_end_{num_json}.json')

                #Print status message
                print(f'\t-Created timeline_data_user_{name}_end_{num_json}.json')

                #Save other game data
                #First, convert it to a df
                game_df = pd.DataFrame(game_data)

                #Save as json file. Use username string to identify whose file it is
                game_df.to_json(f'other_game_data_user_{name}_end_{num_json}.json')

                #Print status message
                print(f'\t-Created other_game_data_user_{name}_end_{num_json}.json\n')
                
                #Now reset the temp lists
                timeline_data = []
                game_data = []
            
        
            ############################# TIMELINE DATA #######################
            #Set up timeline url
            timeline_query = f'lol/match/v5/matches/{match[0]}/timeline/?api_key={api_key}'

            #Grab timeline json data
            timeline_response = requests.get(match_url + timeline_query)

            #Update pull count and sleep for 150 seconds if necessary
            num_pulls += 1

            if num_pulls % 100 == 0:
                print('\nHit 100 pulls! Sleeping for 150 seconds.')
                sleep(150)
                print('Continuing!\n')
            
            #Check response and leave a status message
            if timeline_response.status_code != 200:
                print(f'Something went wrong getting TIMELINE DATA! Status Code {timeline_response.status_code} for match ID: {match}.')
                print(f'Skipping this match ID.\n')
                continue

            #Turn it into json format
            timeline_json = timeline_response.json()

            #Append this data to the timeline_data list
            timeline_data.append(timeline_json)
            
            ############################# OTHER GAME DATA #######################
            #Set up game data url
            game_query = f'lol/match/v5/matches/{match[0]}?api_key={api_key}'

            #Grab game json data
            game_response = requests.get(match_url + game_query)

            #Update pull count and sleep for 150 seconds if necessary
            num_pulls += 1

            if num_pulls % 100 == 0:
                print('\nHit 100 pulls! Sleeping for 150 seconds.')
                sleep(150)
                print('Continuing!\n')
            
            #Check response and leave a status message.
            if game_response.status_code != 200:
                print(f'Something went wrong getting OTHER GAME DATA! Status Code {game_response.status_code} for match ID: {match}.')
                print(f'Skipping this match ID and REMOVING PREVIOUS TIMELINE ENTRY.\n')

                #Remove the last entry in the timeline_data list
                timeline_data.pop()
                continue

            #Turn it into json format
            game_json = game_response.json()

            #Append this data to the game_data list
            game_data.append(game_json)
            
            #Update num_json
            num_json += 1
            
            #Update i
            i += 1
            
        #Tell the user how many match_ids were used for the current user
        print(f'\t-Completed {i} Match IDs for user {name}\n')
    
    #Save any json data that was not saved at the end of the for loop
    
    #Save timeline data.
    #First, convert it to a df
    timeline_df = pd.DataFrame(timeline_data)

    #Save as json file. Use username string to identify whose file it is
    timeline_df.to_json(f'timeline_data_user_{name}_end_{num_json}.json')

    #Print status message
    print(f'Created timeline_data_user_{name}_end_{num_json}.json')

    #Save other game data
    #First, convert it to a df
    game_df = pd.DataFrame(game_data)

    #Save as json file. Use username string to identify whose file it is
    game_df.to_json(f'other_game_data_user_{name}_end_{num_json}.json')

    #Print status message
    print(f'Created other_game_data_user_{name}_end_{num_json}.json')
    
    #Complete! Leave a message
    print('All users completed! Follow suit.')


def build_extracted_df(username, path = './', time = 15):
    """
    This function will take in a path for the json files stored in your directory. 
    It will then read all of them into a list, convert them to lists of dicts, and feed
    them into the extract function. The time variable is for the extract function and determines
    at what timeframe the data will be acquired for. The username is only used for naming the
    .csv file at the end. Please use your last name to avoid confusion.
    
    This function returns a dataframe with data extracted for the specified time. 
    It also automatically saves this dataframe as a .csv.
    
    The path variable defaults to the current directory.
    The time variable defaults to the 15 minute mark.
    
    You will need to have os imported to run this function.
    """
    
    #Gather the names of the timeline json files and sort them
    #This will pull all files that start with 'timeline'
    timeline_files = [ x for x in os.listdir(path) if x.startswith("timeline") ]
    timeline_files.sort()
    
    #Gather the names of the other game data json files and sort them
    #This will pull all files that start with 'other'
    other_data_files = [ x for x in os.listdir(path) if x.startswith("other") ]
    other_data_files.sort()
    
    #Will need an empty df to store the final df
    extracted_df = pd.DataFrame()
    
    #Verify that the lists are the same length
    if len(timeline_files) != len(other_data_files):
        print('Something went wrong! The json lists are not equal!')
        print('Stopping function.')
        return

    for i in range(0, len(timeline_files)):
        #Need to read both of them into dataframes and then convert to list of dicts
        timeline_list = pd.read_json(path + timeline_files[i])
        game_list = pd.read_json(path + other_data_files[i])

        #Convert to list of dicts
        timeline_list = timeline_list.to_dict(orient = 'records')
        game_list = game_list.to_dict(orient = 'records')

        #Now feed them into Joshua C's prepare file. Extract data for the specified timeframe
        temp_df = extract(timeline_list, game_list, time)

        #Now append the temp_df to the complete_df
        extracted_df = extracted_df.append(temp_df, ignore_index = True)
            
    #Drop duplicates and return the prepared df
    extracted_df = extracted_df.drop_duplicates()
    
    #Now save the extracted_df as a .csv
    extracted_df.to_csv(f'new_extracted_data_{username}_time_{time}.csv', index = False)
    
    return extracted_df

def get_players(start=0, end=2640):
    '''
    start where you want to start the list from
    end is where you want to end the list
    default setting is all of them
    '''
    df = pd.read_csv("2640_players.csv")
    list_of_players = list(df.players)
    return list_of_players[start:end]