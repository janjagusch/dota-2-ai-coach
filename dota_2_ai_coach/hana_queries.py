"""
This module provides basic queries for SAP HANA SQL.
"""
from pyhdb.exceptions import DatabaseError


def drop_view_if_exists(cursor, view_name):
    """
    Tries to drop a view and catches error, in case the view does not exist.
    Args:
        cursor: a database connection cursor
        view_name: name of a view
    Returns:
        None
    """
    try:
        cursor.execute("DROP VIEW {0}".format(view_name))
    except DatabaseError:
        print("DatabaseError: VIEW {0} does not exist.".format(view_name))


def create_alter_view(sql, cursor, view_name):
    """
    Checks if a view exists, if so drops it and creates it again. Equivalent to a CREATE OR ALTER.
    Args:
        sql: a SQL query in str format
        cursor: a database connection cursor
        view_name: name of a view
    Returns:
        None
    """
    drop_view_if_exists(cursor, view_name)
    cursor.execute("CREATE VIEW {0} AS {1}".format(view_name, sql))


# This query generates a 1:1 relationship between entities (heroes, creeps, ...)
# and their team (2: radiant, 3: dire, 4: nature). This is critical, since in
# the original table, entities are also related to an abritrary team 0.
entity_team = \
"""
SELECT "targetName" AS "name",
       "targetTeam" AS "team"
FROM "DOTA2_TI8"."combatlog"
WHERE "match_id" = 4063266100
  AND "targetTeam" != 0
GROUP BY "targetName",
         "targetTeam"
ORDER BY "targetTeam",
         "targetName"
"""


def query_entity_team(match_id):
    """
    Compiles the entity team query, provided the match id.
    """
    return entity_team.format(match_id)


# This query generates a cleaned version of the combat log for one match.
# This process involves adjusting the game tick, generating time intervals,
# selecting only meaningful columns (where the type is relevant) and adding
# a correct team label.
combat_cleaned = \
"""
SELECT c."match_id",
       c."game_tick",
       c."game_tick" + 2700 AS "game_tick_adjusted",
       CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
       c."type",
       c."value",
       c."attackerName" AS "attacker_name",
       c."attackerTeam" AS "attacker_team",
       c."inflictorName" AS "inflictor_name",
       c."targetName" AS "target_name",
       entity_team."team" AS "target_team",
       CASE
           WHEN c."isAttackerHero" = TRUE THEN 1
           ELSE 0
       END AS "is_attacker_hero",
       CASE
           WHEN c."isTargetHero" = TRUE THEN 1
           ELSE 0
       END AS "is_target_hero"
FROM "DOTA2_TI8"."combatlog" AS c
LEFT JOIN entity_team ON c."targetName" = entity_team."name"
WHERE c."match_id" = {0}
  AND "type" IN ( 'DOTA_COMBATLOG_DAMAGE',
                  'DOTA_COMBATLOG_XP',
                  'DOTA_COMBATLOG_DEATH',
                  'DOTA_COMBATLOG_GOLD',
                  'DOTA_COMBATLOG_HEAL',
                  'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
                  'DOTA_COMBATLOG_KILLSTREAK',
                  'DOTA_COMBATLOG_CRITICAL_DAMAGE',
                  'DOTA_COMBATLOG_MULTIKILL',
                  'DOTA_COMBATLOG_FIRST_BLOOD' )
"""


def query_combat_cleaned(match_id):
    """
    Compiles the combat cleaned query, provided the match id.
    """
    return combat_cleaned.format(match_id)



# This query geneates a joined table between combat_cleaned and matches.
# It allows us to generate the relative time passed, taking into account the total
# duration of the match.
combat_joined = \
"""
SELECT c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
       c."game_tick_interval" / (m."duration" / 10) AS "game_tick_interval_relative",
       c."game_tick_adjusted" / 30 AS "timestep_adjusted",
       c.*
FROM combat_cleaned AS c
LEFT JOIN "DOTA2_TI8"."matches" AS m ON c."match_id" = m."match_id"
"""


def query_combat_joined():
    """
    Compiles the combat joined query.
    """
    return combat_joined


# This query aggregates data by the game tick intervals.
combat_aggregated = \
"""
SELECT "game_tick_interval",
       "type",
       "attacker_team",
       "target_team",
       COUNT("value") AS "count_events",
       SUM("value") AS "sum_value",
       "is_target_hero"
FROM combat_joined
GROUP BY "game_tick_interval",
         "type",
         "attacker_team",
         "target_team",
         "is_target_hero"
ORDER BY "game_tick_interval",
         "attacker_team",
         "target_team",
         "type",
         "is_target_hero"
"""


def query_combat_aggregated():
    """
    Compiles the combat aggregated query.
    """
    return combat_aggregated


# This query calculates aggreated in game information for each team and time interval.
combat_pivot = \
"""
SELECT t."game_tick_interval",
       t."team_name",
       gold_gained."value" AS "gold_gained",
       xp_gained."value" AS "xp_gained",
       damage_dealt."value" AS "damage_dealt",
       damage_received."value" AS "damage_received",
       enemy_heroes_killed."value" AS "enemy_heroes_killed",
       friendly_heroes_killed."value" AS "friendly_heroes_killed",
       creeps_killed."value" AS "creeps_killed",
       enemy_buildings_killed."value" AS "enemy_buildings_killed",
       friendly_buildings_killed."value" AS "friendly_buildings_killed"
FROM
  ( SELECT *,
           CASE
               WHEN t."team" = 2 THEN 'Radiant'
               ELSE 'Dire'
           END AS "team_name"
   FROM
     ( SELECT DISTINCT t1."game_tick_interval",
                       t2."target_team" AS "team"
      FROM combat_aggregated AS t1,
           combat_aggregated AS t2
      WHERE t2."target_team" IN (2,
                                 3) ) AS t) AS t
LEFT JOIN
  ( SELECT "game_tick_interval",
           "target_team" AS "team",
           "sum_value" AS "value"
   FROM combat_aggregated
   WHERE "type" = 'DOTA_COMBATLOG_GOLD' ) AS gold_gained ON gold_gained."game_tick_interval" = t."game_tick_interval"
AND gold_gained."team" = t."team"
LEFT JOIN
  ( SELECT "game_tick_interval",
           "target_team" AS "team",
           "sum_value" AS "value"
   FROM combat_aggregated
   WHERE "type" = 'DOTA_COMBATLOG_XP' ) AS xp_gained ON xp_gained."game_tick_interval" = t."game_tick_interval"
AND xp_gained."team" = t."team"
LEFT JOIN
  ( SELECT "game_tick_interval",
           "target_team" AS "team",
           SUM("sum_value") AS "value"
   FROM combat_aggregated
   WHERE "type" = 'DOTA_COMBATLOG_DAMAGE'
   GROUP BY "game_tick_interval",
            "target_team" ) AS damage_received ON damage_received."game_tick_interval" = t."game_tick_interval"
AND damage_received."team" = t."team"
LEFT JOIN
  ( SELECT "game_tick_interval",
           "attacker_team" AS "team",
           SUM("sum_value") AS "value"
   FROM combat_aggregated
   WHERE "type" = 'DOTA_COMBATLOG_DAMAGE'
   GROUP BY "game_tick_interval",
            "attacker_team" ) AS damage_dealt ON damage_dealt."game_tick_interval" = t."game_tick_interval"
AND damage_dealt."team" = t."team"
LEFT JOIN
  ( SELECT "game_tick_interval",
           "attacker_team" AS "team",
           SUM("is_target_hero") AS "value"
   FROM combat_aggregated
   WHERE "type" = 'DOTA_COMBATLOG_DEATH'
   GROUP BY "game_tick_interval",
            "attacker_team" ) AS enemy_heroes_killed ON enemy_heroes_killed."game_tick_interval" = damage_received."game_tick_interval"
AND enemy_heroes_killed."team" = damage_received."team"
LEFT JOIN
  ( SELECT "game_tick_interval",
           "target_team" AS "team",
           SUM("is_target_hero") AS "value"
   FROM combat_aggregated
   WHERE "type" = 'DOTA_COMBATLOG_DEATH'
   GROUP BY "game_tick_interval",
            "target_team") AS friendly_heroes_killed ON friendly_heroes_killed."game_tick_interval" = damage_received."game_tick_interval"
AND friendly_heroes_killed."team" = damage_received."team"
LEFT JOIN
  ( SELECT "game_tick_interval",
          "attacker_team" AS "team",
          SUM(- 1 * "is_target_hero" + 1) AS "value"
   FROM combat_aggregated
   WHERE "type" = 'DOTA_COMBATLOG_DEATH'
   GROUP BY "game_tick_interval",
            "attacker_team") AS creeps_killed ON creeps_killed."game_tick_interval" = damage_received."game_tick_interval"
AND creeps_killed."team" = damage_received."team"
LEFT JOIN
  ( SELECT "game_tick_interval",
          "attacker_team" AS "team",
          SUM("sum_value") AS "value"
   FROM combat_aggregated
   WHERE "type" = 'DOTA_COMBATLOG_TEAM_BUILDING_KILL'
   GROUP BY "game_tick_interval",
            "attacker_team") AS enemy_buildings_killed ON enemy_buildings_killed."game_tick_interval" = damage_received."game_tick_interval"
AND enemy_buildings_killed."team" = damage_received."team"
LEFT JOIN
  ( SELECT "game_tick_interval",
          "target_team" AS "team",
          SUM("sum_value") AS "value"
   FROM combat_aggregated
   WHERE "type" = 'DOTA_COMBATLOG_TEAM_BUILDING_KILL'
   GROUP BY "game_tick_interval",
            "target_team") AS friendly_buildings_killed ON friendly_buildings_killed."game_tick_interval" = damage_received."game_tick_interval"
AND friendly_buildings_killed."team" = damage_received."team"
WHERE t."game_tick_interval" IS NOT NULL
ORDER BY t."game_tick_interval",
         "team_name"
"""


def query_combat_pivot():
    """
    Compiles the combat pivot query.
    """
    return combat_pivot
