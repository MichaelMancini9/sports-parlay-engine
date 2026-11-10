import nflreadpy as nfl
import polars as pl
import duckdb
from pathlib import Path

current_season = nfl.get_current_season()
schedules = nfl.load_schedules([current_season])


game = schedules.filter(
    (pl.col("away_team") == "BUF") & (pl.col("home_team") == "MIN")
)

print(game.select(["gameday", "away_team", "home_team",
                   "away_score", "home_score", "result", "spread_line"]))



# spread_line and result are from the home team's perspective (spread_line > 0 = home is favoured) 
# result = home_score - away_score 
# home covers when result > spread_line

Path("data").mkdir(exist_ok=True)
con = duckdb.connect("data/nfl.duckdb")

con.execute("CREATE OR REPLACE TABLE raw_schedules AS SELECT * FROM schedules")

con.sql("SELECT COUNT(*) FROM raw_schedules").show()

con.sql("""
    SELECT game_type, COUNT(*) AS games
    FROM raw_schedules
    GROUP BY game_type
    ORDER BY games DESC
""").show()

con.close()

