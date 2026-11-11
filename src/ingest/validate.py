import duckdb
from pathlib import Path

from src.ingest.load_raw import DB_PATH


def check_schedules(db_path: Path = DB_PATH) -> None:

    con = duckdb.connect(str(db_path), read_only = True)
    con.sql("""
    SELECT
        season,
        COUNT(*) AS games,
        ROUND(100.0 * (COUNT(*) - COUNT(spread_line)) / COUNT(*), 1) AS pct_missing_spread,
        ROUND(100.0 * (COUNT(*) - COUNT(total_line))/ COUNT(*), 1) AS pct_missing_total,
        ROUND(100.0 * (COUNT(*) - COUNT(home_moneyline)) / COUNT(*), 1) AS pct_missing_ml
    FROM raw_schedules
    GROUP BY season
    ORDER BY season
    """).show()
    con.close()

# There is a missing moneyline for the Bears at Packers, 2017 week 4.
# The data looks normal, just a gap no need to fix just exclude game.

if __name__ == "__main__":
    check_schedules()