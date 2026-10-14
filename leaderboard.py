import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "records.db"


def init_db():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_score(player_name, score):
    player_name = player_name.strip()[:16]

    if not player_name:
        player_name = "Player"

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO scores (player_name, score)
            VALUES (?, ?)
            """,
            (player_name, max(0, int(score)))
        )

        connection.execute("""
            DELETE FROM scores
            WHERE id NOT IN (
                SELECT id
                FROM scores
                ORDER BY score DESC, id ASC
                LIMIT 5
            )
        """)


def get_top_players():
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute("""
            SELECT player_name, score
            FROM scores
            ORDER BY score DESC, id ASC
            LIMIT 5
        """).fetchall()

        return [dict(row) for row in rows]

init_db()