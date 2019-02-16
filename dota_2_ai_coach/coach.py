import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dota_2_ai_coach.hana_connector import HanaConnector
import dota_2_ai_coach.hana_queries as queries


match_id = 4063266100
# match_id = 4061660411


def query_highligths(match_id):

    hana_connector = HanaConnector()
    hana_connector.connect()


    queries.create_alter_view(queries.query_entity_team(match_id),
                              hana_connector.connection.cursor(), "entity_team")


    queries.create_alter_view(queries.query_combat_cleaned(match_id),
                              hana_connector.connection.cursor(), "combat_cleaned")


    queries.create_alter_view(queries.query_combat_joined(),
                              hana_connector.connection.cursor(), "combat_joined")


    queries.create_alter_view(queries.query_combat_aggregated(),
                              hana_connector.connection.cursor(), "combat_aggregated")


    queries.create_alter_view(queries.query_combat_pivot(),
                              hana_connector.connection.cursor(), "combat_pivot")


    highlights = pd.read_sql("SELECT * FROM combat_pivot;",
                             hana_connector.connection)
    highlights = highlights.fillna(0)
    highlights["intensity"] = highlights.drop(["game_tick_interval", "team_name",
                                               "gold_gained", "xp_gained"], axis=1).apply(
        lambda x: (x - x.mean()) / x.std(), axis=0).apply(lambda x: x.sum(), axis=1)
    highlights["intensity"] = (highlights["intensity"] - highlights["intensity"].min()) / \
        (highlights["intensity"].max() - highlights["intensity"].min())
    intensity_smoothed = highlights.groupby(
        "team_name", as_index=False)["intensity"]
    intensity_smoothed = intensity_smoothed.rolling(window=12).mean().\
        fillna(0)
    intensity_smoothed = intensity_smoothed.reset_index()
    intensity_smoothed = intensity_smoothed.set_index("level_1", drop=True)
    highlights["seconds_interval"] = highlights["game_tick_interval"] * 10 + 90
    highlights["intensity_smoothed"] = intensity_smoothed["intensity"]


    # highlights.set_index('seconds_interval').groupby('team_name')['intensity_smoothed'].plot(legend=True)
    # plt.show()

    # plt.plot(highlights["seconds_interval"], highlights["intensity_smoothed"])
    # plt.show()


    queries.drop_view_if_exists(hana_connector.connection.cursor(), "entity_team")
    queries.drop_view_if_exists(
        hana_connector.connection.cursor(), "combat_cleaned")
    queries.drop_view_if_exists(
        hana_connector.connection.cursor(), "combat_joined")
    queries.drop_view_if_exists(
        hana_connector.connection.cursor(), "combat_aggregated")
    queries.drop_view_if_exists(hana_connector.connection.cursor(), "combat_pivot")


    hana_connector.close()

    return highlights
