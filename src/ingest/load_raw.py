import duckdb
import nflreadpy as nfl
from pathlib import Path

DB_PATH = Path("data/nfl.duckdb")


def load_schedules(seasons: list[int], db_path: Path = DB_PATH) -> None:

    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    schedules = nfl.load_schedules(seasons)

    con = duckdb.connect(db_path)

    con.execute("CREATE TABLE IF NOT EXISTS raw_schedules AS SELECT * FROM schedules WHERE 1=0")
    con.execute("DELETE FROM raw_schedules WHERE season = ANY(?)", [seasons])
    con.execute("INSERT INTO raw_schedules SELECT * FROM schedules")
    con.sql("SELECT season, COUNT(*) FROM raw_schedules GROUP BY season ORDER BY season").show()
    con.close()


if __name__ == "__main__":
    load_schedules([2023, 2024, 2025, 2026])