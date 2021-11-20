import pandas as pd
import requests
from bs4 import BeautifulSoup
from env import api_key
import re

# Use prep to alter the dataframe
def prep(df):
    df = df.rename(columns={ 'team_deathsplayer_100':'BlueTeamDeaths', 'team_deathsplayer_200':'RedTeamDeaths', 'team_goldPerSecond_100':'BlueTeamGoldPerSec', 'team_goldPerSecond_200':'RedTeamGoldPerSec', 'team_jungleMinionsKilled_100':'BlueTeamJungleMinionsKilled', 'team_jungleMinionsKilled_200':'RedTeamJungleMinionsKilled', 'team_killsplayer_100':'BlueTeamKills', 'team_killsplayer_200':'RedTeamKills', 'team_level_100':'BlueTeamLevel', 'team_level_200':'RedTeamLevel', 'team_magicDamageDoneToChampions_100':'BlueTeamMagicDamageDoneToChampions', 'team_magicDamageDoneToChampions_200':'RedTeamMagicDamageDoneToChampions', 'team_minionsKilled_100':'BlueTeamMinionsKilled', 'team_minionsKilled_200':'RedTeamMinionsKilled', 'team_physicalDamageDoneToChampions_100':'BlueTeamPhysicalDamageDoneToChampions', 'team_physicalDamageDoneToChampions_200':'RedTeamPhysicalDamageDoneToChampions', 'team_timeEnemySpentControlled_100':'BlueTeamTimeEnemySpentControlled', 'team_timeEnemySpentControlled_200':'RedTeamTimeEnemySpentControlled', 'team_totalDamageDoneToChampions_100':'BlueTeamTotalDamageDoneToChampions', 'team_totalDamageDoneToChampions_200':'RedTeamTotalDamageDoneToChampions', 'team_totalGold_100':'BlueTeamTotalGold', 'team_totalGold_200':'RedTeamTotalGold', 'team_trueDamageDoneToChampions_100':'BlueTeamTrueDamageDoneToChampions', 'team_trueDamageDoneToChampions_200':'RedTeamTrueDamageDoneToChampions', 'team_ward_player_100':'BlueTeamWards', 'team_ward_player_200':'RedTeamWards', 'team_assistsplayer_100':'BlueTeamAssists', 'team_assistsplayer_200':'RedTeamAssists', 'team_xp_100':'BlueTeamXp', 'team_xp_200':'RedTeamXp'})
    return df

def prepare(jsonList, jsonList2,t):
    df = pd.DataFrame()
    
    for index, data in enumerate(jsonList):
        if ((data['info']['frames'][-1]['events'][-1]['timestamp']/60000) >= 20) & (str(jsonList2[index]['info']['gameMode'])=='CLASSIC'):
            final_d = {}
            kda = get_player_kda(data, t)
            final_d.update(kda)
            final_d.update(get_player_stats(data, t))
            final_d["gameMode"] = str(jsonList2[index]['info']['gameMode'])
            final_d["gameType"] = str(jsonList2[index]['info']['gameType'])
            final_d['gameVersion'] = str(jsonList2[index]['info']['gameVersion'])
            df = df.append(final_d, ignore_index=True)
            
            print(f"Finished with: {index} of {len(jsonList)}")
        else:
            print(f"Skipping: {index} due to <20 min or not classic")
    
    df = clean(df)
    return df

def clean(df):
    df = df.fillna(0)
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

    for col in columns:
        df[f'team_{col}100'] = 0
        df[f'team_{col}200'] = 0

    for index, value in enumerate(df.iterrows()):
        for col in columns:
            
            total = 0
            
            for i in range(1, 6):
                total += int(df.iloc[index][f'{col}{i}'])
            
            df.at[index, f'team_{col}100'] = total
        
            total = 0
            
            for i in range(6, 11):
                total += int(df.iloc[index][f'{col}{i}'])
            
            df.at[index, f'team_{col}200'] = total
    return df
    
def get_player_kda(data, t):
    
    
    df = pd.DataFrame()
    for index in range(len(data['info']['frames'])):
        for event in data['info']['frames'][index]['events']:
            if event['type'] == 'CHAMPION_KILL':
                df = df.append(event, ignore_index =True)
            

    df.timestamp = df.timestamp / 60_000

    kills_df = df[(df.type== 'CHAMPION_KILL') & (df.timestamp <= t)]

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

def get_player_stats(data, t):
    player_stats = []

    #Here, each timeframe represents about one minute
    timeframe = data['info']['frames'][t]
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
    #Update the players_dict one more t with the timestamp for the timeframe
    players_dict.update({'timestamp' : timeframe['timestamp']})
    #Append the players_dict to the overall player_stats list of dicts
    player_stats.append(players_dict)
    return player_stats[0]