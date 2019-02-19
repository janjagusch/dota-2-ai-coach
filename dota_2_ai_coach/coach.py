"""
This module retrieves aggregated match information from the HANA database, provided the match id.
"""
import numpy as np
import pandas as pd
from hana_connector import HanaConnector
import hana_queries as queries


def query_intensity(match_id):
    """
    Creates several views, retrieves aggregated information and deletes views.
    Args:
        match_id: id of a match in database
    Returns:
        Pandas dataframe with aggregated match information.
    """    
    # Connects to HANA
    hana_connector = HanaConnector()
    hana_connector.connect()
    
    # Creates necessary views
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
    
    # Fetches view data locally
    highlights = pd.read_sql("SELECT * FROM combat_pivot;",
                             hana_connector.connection)
    # Imputes empty values
    highlights = highlights.fillna(0)
    # Calculates intensity as a sum of Z-score normalized game relevant statistics
    highlights["intensity"] = highlights.drop(["game_tick_interval", "team_name",
                                               "gold_gained", "xp_gained",
                                               "damage_received",
                                               "friendly_heroes_killed",
                                               "friendly_buildings_killed"], axis=1).apply(
        lambda x: (x - x.mean()) / x.std(), axis=0).apply(lambda x: x.sum(), axis=1)
    # Min-Max normalizes intensity scores
    highlights["intensity"] = (highlights["intensity"] - highlights["intensity"].min()) / \
        (highlights["intensity"].max() - highlights["intensity"].min())
    # Applies rolling mean to intensity
    intensity_smoothed = highlights.groupby(
        "team_name", as_index=False)["intensity"]
    intensity_smoothed = intensity_smoothed.rolling(window=12).mean().\
        fillna(0)
    intensity_smoothed = intensity_smoothed.reset_index()
    intensity_smoothed = intensity_smoothed.set_index("level_1", drop=True)
    # Calculates time interval in seconds
    highlights["seconds_interval"] = highlights["game_tick_interval"] * 10 + 90
    highlights["intensity_smoothed"] = intensity_smoothed["intensity"]
    # Drops created views
    queries.drop_view_if_exists(
        hana_connector.connection.cursor(), "entity_team")
    queries.drop_view_if_exists(
        hana_connector.connection.cursor(), "combat_cleaned")
    queries.drop_view_if_exists(
        hana_connector.connection.cursor(), "combat_joined")
    queries.drop_view_if_exists(
        hana_connector.connection.cursor(), "combat_aggregated")
    queries.drop_view_if_exists(
        hana_connector.connection.cursor(), "combat_pivot")
    # Close connection, but there seems to be an error with the HANA connector
    # hana_connector.close()
    return highlights
