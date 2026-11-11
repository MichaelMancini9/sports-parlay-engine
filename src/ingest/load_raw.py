import duckdb
import nflreadpy as nfl
from pathlib import Path

DB_PATH = Path("data/nfl.duckdb")

# spread_line and result are from the home team's perspective (spread_line > 0 = home is favoured) 
# result = home_score - away_score 
# home covers when result > spread_line

def load_schedules(seasons: list[int], db_path: Path = DB_PATH) -> None:

    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    schedules = nfl.load_schedules(seasons)

    con = duckdb.connect(db_path)
    con.execute("CREATE TABLE IF NOT EXISTS raw_schedules AS SELECT * FROM schedules WHERE 1=0")
    con.execute("DELETE FROM raw_schedules WHERE season = ANY(?)", [seasons])
    con.execute("INSERT INTO raw_schedules BY NAME SELECT * FROM schedules")
    con.close()

def load_pbp(seasons: list[int], db_path: Path = DB_PATH) -> None:

    db_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(db_path)
    for season in seasons:
        pbp = nfl.load_pbp(season)
        con.execute("CREATE TABLE IF NOT EXISTS raw_pbp AS SELECT * FROM pbp WHERE 1=0")
        con.execute("DELETE FROM raw_pbp WHERE season = ?", [season])
        con.execute("INSERT INTO raw_pbp BY NAME SELECT * FROM pbp")
    con.close()

def load_player_stats(seasons: list[int], db_path: Path = DB_PATH) -> None:

    db_path.parent.mkdir(parents=True, exist_ok=True)
    player_stats = nfl.load_player_stats(seasons)

    con = duckdb.connect(db_path)
    con.execute("CREATE TABLE IF NOT EXISTS raw_player_stats AS SELECT * FROM player_stats WHERE 1=0")
    con.execute("DELETE FROM raw_player_stats WHERE season = ANY(?)", [seasons])
    con.execute("INSERT INTO raw_player_stats BY NAME SELECT * FROM player_stats")
    con.close()


if __name__ == "__main__":
    seasons = list(range(2010, nfl.get_current_season() + 1))
    load_schedules(seasons)
    load_pbp(seasons)
    load_player_stats(seasons)