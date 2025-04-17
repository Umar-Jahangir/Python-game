import sqlite3
from contextlib import contextmanager

class GameDatabase:
    def __init__(self, db_name='game_scores.db'):
        self.db_name = db_name
        self._initialize_database()

    @contextmanager
    def _get_cursor(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            conn.close()

    def _initialize_database(self):
        with self._get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS high_score (
                    game_name TEXT PRIMARY KEY,
                    score INTEGER NOT NULL
                )
            ''')

    def get_high_score(self, game_name: str) -> int:
        with self._get_cursor() as cursor:
            cursor.execute('SELECT score FROM high_score WHERE game_name = ?', (game_name,))
            result = cursor.fetchone()
            return result[0] if result else 0

    def set_high_score(self, game_name: str, score: int):
        with self._get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO high_score (game_name, score)
                VALUES (?, ?)
                ON CONFLICT(game_name) DO UPDATE SET score = excluded.score
            ''', (game_name, score))
