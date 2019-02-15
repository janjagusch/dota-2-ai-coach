import pandas as pd
import json

match = pd.read_csv("data/match_4063266100.csv", index_col=0)
match_replay = pd.read_csv("data/match_replay_4063266100.csv", index_col=0)
#movement_data = match_replay['']

pd.set_option('display.max_columns', None)


# create damage log
damage_log = pd.concat([match[(match.type == "DOTA_COMBATLOG_DAMAGE")],
                       match[(match.type == "DOTA_COMBATLOG_CRITICAL_DAMAGE")]])


def first_blood():
    first_blood = match[(match.type == "DOTA_COMBATLOG_FIRST_BLOOD")].reset_index()
    fb_tick = int(first_blood['tick'])

    first_death = match[(match.type == "DOTA_COMBATLOG_DEATH") & (match.tick == fb_tick)].reset_index()
    target_id = int(first_death['targetNameIdx'])

    #match_replay[(match_replay.targetNameIdx == target_id)]

    # add 3 seconds before and after in actual timestamps
    fb_log = damage_log[(damage_log.tick >= fb_tick - 450) & (damage_log.tick < fb_tick) & (damage_log.targetNameIdx == target_id)].sort_values(by=['timestamp'])

    fb_output = pd.DataFrame(index=None)
    fb_output['type'] = first_blood['type']
    fb_output['attacker'] = first_death['attackerName']
    fb_output['target'] = first_death['targetName']
    fb_output['start_time'] = fb_log['timestamp'].iloc[0]
    fb_output['end_time'] = fb_log['timestamp'].iloc[-1]

    return fb_output


fb = first_blood().to_json(orient="records")

print(fb)
# & (damage.inflictorNameIdx == inflictor_id) & (damage.targetNameIdx == target_id)
