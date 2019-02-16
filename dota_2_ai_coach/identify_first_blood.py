import pandas as pd
import json
import hana_connector

#match = pd.read_csv("data/match_4063266100.csv", index_col=0)
#match_replay = pd.read_csv("data/match_replay_4063266100.csv", index_col=0)
#movement_data = match_replay['']

pd.set_option('display.max_columns', None)


# create damage log
#damage_log = pd.concat([match[(match.type == "DOTA_COMBATLOG_DAMAGE")],
#                      match[(match.type == "DOTA_COMBATLOG_CRITICAL_DAMAGE")]])


def first_blood(matchID):
    hana = hana_connector.HanaConnector()
    connection = hana.connect()
    first_blood = pd.read_sql("""
    SELECT
        "tick", "type"
    FROM 
        "DOTA2_TI8"."combatlog"
    WHERE
        "match_id" = {matchID}
    AND
        "type" = 'DOTA_COMBATLOG_FIRST_BLOOD'
    """.format(matchID=matchID), connection)
    if first_blood.empty:
        return first_blood
    
    print(first_blood)
    # first_blood = pd.DataFrame(data, columns=columns)

    # print(first_blood['tick'].values[0][0], "asgggg")
    #first_blood = match[(match.type == "DOTA_COMBATLOG_FIRST_BLOOD")].reset_index()
    fb_tick = int(first_blood['tick'])
    print(fb_tick)
    first_death = pd.read_sql("""
        SELECT
            *
        FROM 
            "DOTA2_TI8"."combatlog"
        WHERE
            "match_id" = {matchID}
        AND
            "type" = 'DOTA_COMBATLOG_DEATH'
            AND
            "tick" = {tick}
        """.format(tick=fb_tick, matchID=matchID), connection)
    #first_death = pd.DataFrame(data, columns=columns)
    # first_death = match[(match.type == "DOTA_COMBATLOG_DEATH") & (match.tick == fb_tick)].reset_index()
    target_id = int(first_death['targetNameIdx'])

    #match_replay[(match_replay.targetNameIdx == target_id)]
    damage_log = pd.read_sql("""
        SELECT
            *
        FROM 
            "DOTA2_TI8"."combatlog"
        WHERE
            "match_id" = {matchID}
            AND
            (
                "type" = 'DOTA_COMBATLOG_DAMAGE'
                OR
                "type" = 'DOTA_COMBATLOG_CRITICAL_DAMAGE'
            )
            AND
            "tick" < {tick}
            AND
            "tick" >= {tick} - 450
            AND
            "targetNameIdx" = {target_id}
            ORDER BY
            "timestamp"
            ASC
        """.format(tick=fb_tick, target_id=target_id, matchID=matchID), connection)
    print(fb_tick, target_id)
    # damage_log = pd.DataFrame(data, columns=columns)   
    print(damage_log.shape) 
    # add 3 seconds before and after in actual timestamps
    # fb_log = damage_log[(damage_log.tick >= fb_tick - 450) & (damage_log.tick < fb_tick) & (damage_log.targetNameIdx == target_id)].sort_values(by=['timestamp'])

    fb_output = pd.DataFrame(index=None)
    print(first_blood['type'])
    fb_output['type'] = first_blood['type']
    fb_output['attacker'] = first_death['attackerName']
    fb_output['target'] = first_death['targetName']
    fb_output['start_time'] = damage_log['timestamp'].iloc[0]
    fb_output['end_time'] = damage_log['timestamp'].iloc[-1]
    # fb_output['start_time'] = fb_log['timestamp'].iloc[0]
    # fb_output['end_time'] = fb_log['timestamp'].iloc[-1]

    return fb_output


# fb = first_blood().to_json(orient="records")

# print(fb)
# & (damage.inflictorNameIdx == inflictor_id) & (damage.targetNameIdx == target_id)
