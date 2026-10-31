import sqlite3
from pathlib import Path


class ConversationStore:
    def __init__(self, path: str):
        self.path = str(Path(path))
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.path, timeout=10)

    def _init_db(self):
        with self._connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'model')),
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            con.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_user_id_id
                ON messages(user_id, id)
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS daily_usage (
                    user_id INTEGER NOT NULL,
                    usage_date TEXT NOT NULL,
                    count INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY (user_id, usage_date)
                )
            """)

    def get_history(self, user_id: int, limit: int = 10):
        with self._connect() as con:
            rows = con.execute(
                "SELECT role, content FROM messages WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
        rows.reverse()
        # Ensure history begins with a user message and alternates cleanly enough for API input.
        while rows and rows[0][0] != "user":
            rows.pop(0)
        return rows

    def add_exchange(self, user_id: int, prompt: str, answer: str):
        with self._connect() as con:
            con.execute(
                "INSERT INTO messages (user_id, role, content) VALUES (?, 'user', ?)",
                (user_id, prompt),
            )
            con.execute(
                "INSERT INTO messages (user_id, role, content) VALUES (?, 'model', ?)",
                (user_id, answer),
            )

    def clear_user(self, user_id: int):
        with self._connect() as con:
            con.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))

    def get_daily_usage(self, user_id: int, usage_date: str) -> int:
        with self._connect() as con:
            row = con.execute(
                "SELECT count FROM daily_usage WHERE user_id = ? AND usage_date = ?",
                (user_id, usage_date),
            ).fetchone()
        return int(row[0]) if row else 0

    def add_daily_usage(self, user_id: int, usage_date: str):
        with self._connect() as con:
            con.execute("""
                INSERT INTO daily_usage (user_id, usage_date, count) VALUES (?, ?, 1)
                ON CONFLICT(user_id, usage_date) DO UPDATE SET count = count + 1
            """, (user_id, usage_date))
