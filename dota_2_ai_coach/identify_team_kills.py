import pandas as pd
from datetime import datetime


pd.set_option('display.max_columns', None)

"""
IsTargetHero should be true


>2 ppl killed
Time difference between kills <=18 seconds
The hero which died must get some damage within the range of the previous kill
Teamfight event time range creation:  [-18 seconds before the first death in the teamfight; +18 seconds after the last death]
Determining teamfight map location: the location of the first kill within a fight (?)

"""



combat_log = pd.read_csv("data/match_4063266100.csv", index_col=0).reset_index()
match_replay = pd.read_csv("data/match_replay_4063266100.csv", index_col=0)



#### Needs to be SQL statements!
combat_log_only_kills = combat_log[(combat_log.type == "DOTA_COMBATLOG_DEATH") & (combat_log.isTargetHero == True)].sort_values(by=['tick'])
combat_log_gold = combat_log[(combat_log.type == "DOTA_COMBATLOG_GOLD")].sort_values(by=['tick'])
print(combat_log_only_kills.shape)
combat_log_gold_xy = combat_log_gold[['targetNameIdx', 'tick', 'locationX', 'locationY']]


#match_xy = match_replay[['m_iPlayerID', 'tick', 'CBodyComponent.m_vecX', 'CBodyComponent.m_vecY', 'CBodyComponent.m_cellX', 'CBodyComponent.m_cellY' ]]
#match_xy['locationX'] = ((match_xy['CBodyComponent.m_cellX'] * 128) - 8192.0 + match_xy['CBodyComponent.m_vecX'])
#match_xy['locationY'] = ((match_xy['CBodyComponent.m_cellY'] * 128) - 8192.0 + match_xy['CBodyComponent.m_vecY'])
#match_xy = match_xy.drop(labels=['CBodyComponent.m_vecX', 'CBodyComponent.m_vecY', 'CBodyComponent.m_cellX', 'CBodyComponent.m_cellY'], axis=1)

#combat_log_xy = pd.merge(combat_log_only_kills, combat_log_gold_xy, how='left', left_on=['targetNameIdx','tick'], right_on=['targetNameIdx','tick'])#.drop(labels=['targetNameIdx'], axis=1)
#combat_log_xy = combat_log_xy.rename(index=str, columns={"locationX_y": "locationX_attacker", "locationY_y": "locationY_attacker"})
#combat_log_xy = pd.merge(combat_log_xy, match_xy, how='left', left_on=['targetNameIdx','tick'], right_on=['m_iPlayerID','tick']).drop(labels=['m_iPlayerID'], axis=1)
#combat_log_xy = combat_log_xy.rename(index=str, columns={"locationX_y": "locationX_target", "locationY_y": "locationY_target"}).reset_index()

combat_log_only_kills["adj_tick"] = combat_log_only_kills["tick"] - (combat_log_only_kills["tick"] - combat_log_only_kills["game_tick"])
combat_log_only_kills["adj_tick_prior"] = combat_log_only_kills["adj_tick"].shift(1)
combat_log_only_kills["tick_delta"] = combat_log_only_kills["adj_tick"] - combat_log_only_kills["adj_tick_prior"]

print(combat_log_only_kills["adj_tick"])

# Compute euclidean distances between each kill
#kill_xy = combat_log_xy[["locationX_target", "locationY_target"]].apply(lambda x: x["locationX_target", x["locationY_target"]])
kill_xy = combat_log_only_kills[["locationX_target", "locationY_target"]].apply(lambda x: x.tolist(), axis=1).tolist()

combat_log_only_kills.to_csv("kill_log_xy.csv")

#kill_xy = "[" + combat_log_xy['locationX_target'].astype(str) + "," + combat_log_xy['locationY_target'].astype(str) + "]"

print(kill_xy)
#print(euclidean_distances(kill_xy, kill_xy))

curr_tuple = []
number_kills = 0
kill_sequences = []

for index, kill in combat_log_only_kills.iterrows():
    curr_kill_xy = [kill['locationX_target'], kill['locationY_target']]
    if number_kills == 0:
        curr_tuple.append(kill['adj_tick'])
        number_kills = number_kills + 1
    elif kill['tick_delta'] <= 540:
        number_kills = number_kills + 1
    elif kill['tick_delta'] > 540:
        if number_kills > 2:
            curr_tuple.append(kill['adj_tick_prior'])
            kill_sequences.append(curr_tuple)
            number_kills = 1
            curr_tuple = [kill['adj_tick']]
        else:
            curr_tuple = [kill['adj_tick']]
            number_kills = 1

kill_sequences_sec = pd.DataFrame()
start_times = []
end_times = []
for start, end in kill_sequences:
    start_times.append(start / 30 - 15) # add 3 as buffer
    end_times.append(end / 30 + 5) # add 3 as buffer

kill_sequences_sec['timestamp_start'] = start_times
kill_sequences_sec['datetime_start'] = kill_sequences_sec['timestamp_start'].apply(lambda x: datetime.utcfromtimestamp(x).isoformat())
kill_sequences_sec['timestamp_end'] = end_times
kill_sequences_sec['datetime_end'] = kill_sequences_sec['timestamp_end'].apply(lambda x: datetime.utcfromtimestamp(x).isoformat())
kill_sequences_sec['type'] = "KILL_SEQUENCE"



ks = kill_sequences_sec.to_json(orient="records")


"""
JSON
Type = Teamfight
Start =
End =
"""
