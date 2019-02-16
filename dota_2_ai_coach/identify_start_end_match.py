import pandas as pd

matches = pd.read_csv("data/matches/matches.csv", index_col=0)
print(matches)

duration = 4912


adj_end_tick = combat_log["tick"].max() - (combat_log["tick"].max() - combat_log["game_tick"].max())
print(adj_end_tick)