import os
from typing import Optional

import duckdb


class DuckDBClient:
    """Client for managing DuckDB connection and local scouting data."""

    def __init__(self, db_path: str = "data/scouting.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = duckdb.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        """Initializes the database schema if it doesn't exist."""
        # This would typically read from src/db/schema.sql
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS matches (
                match_id VARCHAR PRIMARY KEY,
                team_id VARCHAR,
                opponent_id VARCHAR,
                map_name VARCHAR,
                score VARCHAR,
                start_time TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS rounds (
                match_id VARCHAR,
                round_number INTEGER,
                winning_side VARCHAR,
                win_type VARCHAR,
                team_a_econ VARCHAR,
                team_b_econ VARCHAR,
                PRIMARY KEY (match_id, round_number)
            );

            CREATE TABLE IF NOT EXISTS player_stats (
                match_id VARCHAR,
                player_id VARCHAR,
                kills INTEGER,
                deaths INTEGER,
                assists INTEGER,
                adr FLOAT,
                PRIMARY KEY (match_id, player_id)
            );
        """
        )

    def query(self, sql: str, params: Optional[list] = None):
        """Executes a query and returns the results as a DataFrame."""
        if params:
            return self.conn.execute(sql, params).df()
        return self.conn.execute(sql).df()

    def insert_match(self, match_data: dict):
        # Implementation for inserting match data
        pass
