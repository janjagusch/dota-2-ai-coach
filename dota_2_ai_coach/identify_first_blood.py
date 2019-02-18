import pandas as pd
import json
import hana_connector
from datetime import datetime




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

    
    fb_tick = int(first_blood['tick'])

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
    
    fb_output = pd.DataFrame(index=None)
    
    fb_output['type'] = first_blood['type']
    fb_output['attacker'] = first_death['attackerName']
    fb_output['target'] = first_death['targetName']
    fb_output['start_time'] = datetime.utcfromtimestamp(
        damage_log['timestamp'].iloc[0]).isoformat()
    fb_output['end_time'] = datetime.utcfromtimestamp(
        damage_log['timestamp'].iloc[-1]).isoformat()
    
    return fb_output

