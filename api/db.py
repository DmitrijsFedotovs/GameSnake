"""Database operations for the Metal Snake Solid API."""
import sqlite3
from pathlib import Path
from typing import Any
DB_PATH = Path(__file__).resolve().parent.parent / "records.db"
def get_connection() -> sqlite3.Connection:
    """Open a connection to the existing SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
def init_db() -> None:
    """Create the scores table if it does not exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
def save_score(player_name: str, score: int) -> None:
    """Save a single game result."""
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO scores (player_name, score)
            VALUES (?, ?)
            """,
            (player_name, score),
        )
def get_top_scores(limit: int = 10) -> list[dict[str, Any]]:
    """Return the highest scores."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT player_name, score, created_at
            FROM scores
            ORDER BY score DESC, id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]
def get_player_stats(player_name: str) -> dict[str, Any] | None:
    """Return game count and best score for a player."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS games_played,
                MAX(score) AS best_score
            FROM scores
            WHERE player_name = ?
            """,
            (player_name,),
        ).fetchone()
    if row is None or row["games_played"] == 0:
        return None
    return {
        "player_name": player_name,
        "games_played": row["games_played"],
        "best_score": row["best_score"],
    }
init_db()