"""
database.py
~~~~~~~~~~~
SQLite handler.  Demonstrates ENCAPSULATION - all SQL is private to the class.
Saves every registered user AND every quiz attempt (score, certificate, time).
"""
import os
import sqlite3
from datetime import datetime
from .config import DB_FILE


class Database:
    """ENCAPSULATION + CONSTRUCTOR/DESTRUCTOR.

    Owns the SQLite connection (private attribute `__conn`) and exposes only
    high-level methods. __del__ closes the connection automatically.
    """

    def __init__(self, db_path: str = DB_FILE):
        self.__conn = sqlite3.connect(db_path)
        self.__conn.row_factory = sqlite3.Row
        self.__create_tables()

    def __create_tables(self):
        cur = self.__conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL UNIQUE,
                dob         TEXT    NOT NULL,
                age         INTEGER NOT NULL,
                phone       TEXT    NOT NULL,
                email       TEXT    NOT NULL,
                password    TEXT    NOT NULL,
                created_at  TEXT    NOT NULL
            );
            CREATE TABLE IF NOT EXISTS attempts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name   TEXT    NOT NULL,
                topic       TEXT    NOT NULL,
                score       INTEGER NOT NULL,
                total       INTEGER NOT NULL,
                certificate TEXT    NOT NULL,
                taken_at    TEXT    NOT NULL
            );
        """)
        self.__conn.commit()

    # ---------- USER CRUD ----------
    def add_user(self, name, dob, age, phone, email, password):
        cur = self.__conn.cursor()
        cur.execute(
            "INSERT INTO users (name,dob,age,phone,email,password,created_at) "
            "VALUES (?,?,?,?,?,?,?)",
            (name, dob, age, phone, email, password,
             datetime.now().isoformat(timespec="seconds")),
        )
        self.__conn.commit()
        return cur.lastrowid

    def user_exists(self, name):
        cur = self.__conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE name = ?", (name,))
        return cur.fetchone() is not None

    def get_user(self, name):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM users WHERE name = ?", (name,))
        row = cur.fetchone()
        return dict(row) if row else None

    def verify_password(self, name, password) -> bool:
        """Case-sensitive password verification."""
        user = self.get_user(name)
        return user is not None and user["password"] == password

    # ---------- ATTEMPT CRUD ----------
    def save_attempt(self, user_name, topic, score, total, certificate):
        cur = self.__conn.cursor()
        cur.execute(
            "INSERT INTO attempts (user_name,topic,score,total,certificate,taken_at) "
            "VALUES (?,?,?,?,?,?)",
            (user_name, topic, score, total, certificate,
             datetime.now().isoformat(timespec="seconds")),
        )
        self.__conn.commit()
        return cur.lastrowid

    def all_attempts(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM attempts ORDER BY taken_at DESC")
        return [dict(r) for r in cur.fetchall()]

    # ---------- DESTRUCTOR ----------
    def __del__(self):
        try:
            self.__conn.close()
        except Exception:
            pass
