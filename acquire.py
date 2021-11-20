import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from env import api_key
import time
import re

def acquire():
    df = pd.read_csv("final.csv")
    return df

def extract(timeline_data, other_game_data, time):
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
            print(f"Skipping: {index} due to <20 min or not classic")
    return df

def get_more_info(data, time):

    d = {}
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

    d = {}
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
    for index, player in enumerate(temp[0].value_counts().sort_index()):
        d['assistsplayer_'+str(temp[0].value_counts().sort_index().index[index])] = temp.value_counts().sort_index().iloc[index]

    df = pd.DataFrame()
    for index in range(len(data['info']['frames'])):
        for event in data['info']['frames'][index]['events']:
            if event['type'] == 'ELITE_MONSTER_KILL':
                df = df.append(event, ignore_index =True)
            elif event['type']== 'GAME_END':
                df = df.append(event, ignore_index =True)

    kills_df = df[df.type == 'ELITE_MONSTER_KILL']
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

    kills_df = df[df.type == 'WARD_PLACED']
    for index, player in enumerate(kills_df[kills_df.type=='WARD_PLACED'].creatorId.value_counts().sort_index()):

        # Grabbing baron and saving values to same dictionary
        d['ward_player_'+str(int(kills_df[kills_df.type=='WARD_PLACED'].creatorId.value_counts().sort_index().index[index]))] =\
        kills_df[kills_df.type=='WARD_PLACED'].creatorId.value_counts().sort_index().iloc[index]
    df = pd.DataFrame()
    
    for index in range(len(data['info']['frames'])):
        for event in data['info']['frames'][index]['events']:
            if event['type'] == 'BUILDING_KILL':
                df = df.append(event, ignore_index =True)

    kills_df = df[df.type == 'BUILDING_KILL']

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