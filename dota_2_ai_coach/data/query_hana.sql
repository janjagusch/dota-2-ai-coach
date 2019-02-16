
SELECT
t."game_tick_interval",
t."team_name",
gold_gained."value" as "gold_gained",
xp_gained."value" as "xp_gained",
damage_dealt."value" as "damage_dealt",
damage_received."value" as "damage_received",
enemy_heroes_killed."value" as "enemy_heroes-´_killed",
friendly_heroes_killed."value" as "friendly_heroes_killed",
creeps_killed."value" as "creeps_killed",
enemy_buildings_killed."value" as "enemy_buildings_killed",
friendly_buildings_killed."value" as "friendly_buildings_killed"
FROM
(
SELECT
*,
CASE WHEN t."team" = 2 THEN 'Radiant' ELSE 'Dire' END AS "team_name"
FROM
(
SELECT
DISTINCT
t1."game_tick_interval",
t2."target_team" as "team"
from
(
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
) as t1,
(
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
) as t2
WHERE
t2."target_team" IN (2, 3)
) AS t
) AS t
LEFT JOIN
(
SELECT "game_tick_interval", "target_team" AS "team", "sum_value" AS "value" FROM (
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
) WHERE "type" = 'DOTA_COMBATLOG_GOLD'
) as gold_gained
ON
gold_gained."game_tick_interval" = t."game_tick_interval" AND
gold_gained."team" = t."team"
LEFT JOIN
(
SELECT "game_tick_interval", "target_team" AS "team", "sum_value" AS "value" FROM (
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
) WHERE "type" = 'DOTA_COMBATLOG_XP'
) as xp_gained
ON
xp_gained."game_tick_interval" = t."game_tick_interval" AND
xp_gained."team" = t."team"
LEFT JOIN
(
SELECT
"game_tick_interval",
"target_team" AS "team",
SUM("sum_value") AS "value"
FROM
(
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
)
WHERE "type" = 'DOTA_COMBATLOG_DAMAGE'
GROUP BY
"game_tick_interval",
"target_team"
) AS damage_received
ON
damage_received."game_tick_interval" = t."game_tick_interval" AND
damage_received."team" = t."team"
LEFT JOIN
(
SELECT
"game_tick_interval",
"attacker_team" AS "team",
SUM("sum_value") AS "value"
FROM
(
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
)
WHERE "type" = 'DOTA_COMBATLOG_DAMAGE'
GROUP BY
"game_tick_interval",
"attacker_team"
) AS damage_dealt
ON
damage_dealt."game_tick_interval" = t."game_tick_interval" AND
damage_dealt."team" = t."team"
LEFT JOIN(
SELECT
"game_tick_interval",
"attacker_team" AS "team",
SUM("is_target_hero") AS "value"
FROM
(
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
)
WHERE
"type" = 'DOTA_COMBATLOG_DEATH'
GROUP BY
"game_tick_interval",
"attacker_team"
) as enemy_heroes_killed
ON
enemy_heroes_killed."game_tick_interval" = damage_received."game_tick_interval" AND
enemy_heroes_killed."team" = damage_received."team"
LEFT JOIN(
SELECT
"game_tick_interval",
"target_team" AS "team",
SUM("is_target_hero") AS "value"
FROM
(
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
)
WHERE
"type" = 'DOTA_COMBATLOG_DEATH'
GROUP BY
"game_tick_interval",
"target_team"
) as friendly_heroes_killed
ON
friendly_heroes_killed."game_tick_interval" = damage_received."game_tick_interval" AND
friendly_heroes_killed."team" = damage_received."team"
LEFT JOIN(
SELECT
"game_tick_interval",
"attacker_team" AS "team",
SUM(- 1 * "is_target_hero" + 1) AS "value"
FROM
(
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
)
WHERE
"type" = 'DOTA_COMBATLOG_DEATH'
GROUP BY
"game_tick_interval",
"attacker_team"
) as creeps_killed
ON
creeps_killed."game_tick_interval" = damage_received."game_tick_interval" AND
creeps_killed."team" = damage_received."team"
LEFT JOIN(
SELECT
"game_tick_interval",
"attacker_team" AS "team",
SUM("sum_value") AS "value"
FROM
(
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
)
WHERE
"type" = 'DOTA_COMBATLOG_TEAM_BUILDING_KILL'
GROUP BY
"game_tick_interval",
"attacker_team"
) as enemy_buildings_killed
ON
enemy_buildings_killed."game_tick_interval" = damage_received."game_tick_interval" AND
enemy_buildings_killed."team" = damage_received."team"
LEFT JOIN(
SELECT
"game_tick_interval",
"target_team" AS "team",
SUM("sum_value") AS "value"
FROM
(
SELECT
"game_tick_interval",
"type",
"attacker_team",
"target_team",
COUNT("value") AS "count_events",
SUM("value") AS "sum_value",
"is_target_hero"

FROM
(

SELECT
c."game_tick" / (m."duration" * 30) AS "game_tick_relative",
c."game_tick_interval" / (m."duration"  / 10) AS "game_tick_interval_relative",
c."game_tick_adjusted" / 30 AS "timestep_adjusted",
c.*

FROM
(

SELECT
c."match_id",
c."game_tick",
c."game_tick" + 2700 AS "game_tick_adjusted",
/* Calculate 10 second interval based on game tick */
CAST(c."game_tick" / 300 AS INT) AS "game_tick_interval",
c."type",
c."value",
c."attackerName" AS "attacker_name",
c."attackerTeam" AS "attacker_team",
c."inflictorName" AS "inflictor_name",
c."targetName" AS "target_name",
entity_team."team" AS "target_team",
CASE WHEN c."isAttackerHero" = True THEN 1 ELSE 0 END AS "is_attacker_hero",
CASE WHEN c."isTargetHero" = True THEN 1 ELSE 0 END AS "is_target_hero"

FROM
"DOTA2_TI8"."combatlog" as c

LEFT JOIN
(

SELECT
"targetName" AS "name",
"targetTeam" AS "team"

FROM
"DOTA2_TI8"."combatlog"

WHERE
"match_id" = 4063266100 AND
"targetTeam" != 0

GROUP BY
"targetName",
"targetTeam"

ORDER BY
"targetTeam",
"targetName"

)
AS entity_team
ON c."targetName" = entity_team."name"

WHERE
c."match_id" = 4063266100 AND
"type" IN (
'DOTA_COMBATLOG_DAMAGE',
'DOTA_COMBATLOG_XP',
'DOTA_COMBATLOG_DEATH',
'DOTA_COMBATLOG_GOLD',
'DOTA_COMBATLOG_HEAL',
'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
'DOTA_COMBATLOG_KILLSTREAK',
'DOTA_COMBATLOG_CRITICAL_DAMAGE',
'DOTA_COMBATLOG_MULTIKILL',
'DOTA_COMBATLOG_FIRST_BLOOD'
)

) AS c

LEFT JOIN "DOTA2_TI8"."matches" as m
ON c."match_id" = m."match_id"

)

GROUP BY
"game_tick_interval",
"type",
"attacker_team",
"target_team",
"is_target_hero"

ORDER BY
"game_tick_interval",
"attacker_team",
"target_team",
"type",
"is_target_hero"
ASC
)
WHERE
"type" = 'DOTA_COMBATLOG_TEAM_BUILDING_KILL'
GROUP BY
"game_tick_interval",
"target_team"
) as friendly_buildings_killed
ON
friendly_buildings_killed."game_tick_interval" = damage_received."game_tick_interval" AND
friendly_buildings_killed."team" = damage_received."team"
WHERE
t."game_tick_interval" IS NOT NULL
ORDER BY
t."game_tick_interval", "team_name"
;
;