"""
Where English Step-Up keeps its data.

On your own computer it uses a simple file (data/english-step-up.db).
Online, it uses the Postgres database named by the DATABASE_URL setting (for example Neon),
so student accounts and scores survive every restart.

Nothing here needs to change when you add lessons.
"""

import os
import re
import sqlite3

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
SQLITE_PATH = os.path.join(DATA_DIR, "english-step-up.db")

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
USING_POSTGRES = bool(DATABASE_URL)

if USING_POSTGRES:
    import psycopg2
    from psycopg2.extras import RealDictCursor
else:
    os.makedirs(DATA_DIR, exist_ok=True)


def describe():
    return "Postgres (online database)" if USING_POSTGRES else f"file {SQLITE_PATH}"


def _to_postgres(sql, params):
    """The app writes SQLite-style SQL; Postgres needs %s placeholders instead of ?."""
    if params:
        sql = sql.replace("%", "%%")   # keep any literal % intact (must happen first)
    return sql.replace("?", "%s")


class Connection:
    """One database connection, used the same way for both databases."""

    def __init__(self):
        if USING_POSTGRES:
            self._raw = psycopg2.connect(
                DATABASE_URL,
                cursor_factory=RealDictCursor,
                connect_timeout=20,      # Neon's free database may need a moment to wake up
                keepalives=1,
                keepalives_idle=30,
            )
        else:
            self._raw = sqlite3.connect(SQLITE_PATH, timeout=10)
            self._raw.row_factory = sqlite3.Row
            self._raw.execute("PRAGMA foreign_keys = ON")

    def execute(self, sql, params=()):
        """Run one statement. Rows come back as row["column_name"] either way."""
        if USING_POSTGRES:
            cursor = self._raw.cursor()
            cursor.execute(_to_postgres(sql, params), tuple(params) or None)
            return cursor
        return self._raw.execute(sql, params)

    def insert(self, sql, params=()):
        """Run an INSERT and return the new row's id."""
        if USING_POSTGRES:
            return self.execute(sql + " RETURNING id", params).fetchone()["id"]
        return self.execute(sql, params).lastrowid

    def commit(self):
        self._raw.commit()

    def rollback(self):
        self._raw.rollback()

    def close(self):
        self._raw.close()


def connect():
    return Connection()


def init(schema_sql):
    """Create the tables the first time, for whichever database is in use."""
    conn = Connection()
    try:
        if USING_POSTGRES:
            # SQLite's auto-numbering and float types have different names in Postgres.
            schema_sql = re.sub(r"\bINTEGER PRIMARY KEY\b", "SERIAL PRIMARY KEY", schema_sql)
            schema_sql = re.sub(r"\bREAL\b", "DOUBLE PRECISION", schema_sql)
            conn.execute(schema_sql)
        else:
            conn._raw.execute("PRAGMA journal_mode = WAL")
            conn._raw.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()
