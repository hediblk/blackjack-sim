import sqlite3
import datetime


class DatabaseManager:
    def __init__(self, db_path="blackjack.db"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()

        # single row table for balance
        # would be cool to add multiple players later
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                balance REAL
            )
        """)

        cursor.execute(
            "INSERT OR IGNORE INTO player (id, balance) VALUES (1, 1000.0)")

        # game tble (from starting the game session to ending it)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_balance REAL,
                end_balance REAL,
                cards_dealt INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP
            )
        """)

        # records every hand played in a session
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                player_cards TEXT,
                dealer_cards TEXT,
                actions TEXT,
                winnings REAL,
                FOREIGN KEY(session_id) REFERENCES sessions(id)
            )
        """)

        conn.commit()
        conn.close()

    def get_balance(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM player WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 1000.0

    def update_balance(self, amount):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE player SET balance = ? WHERE id = 1", (amount,))
        conn.commit()
        conn.close()

    def start_session(self, start_balance):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (start_balance, end_balance, cards_dealt, start_time)
            VALUES (?, ?, 0, ?)
        """, (start_balance, start_balance, datetime.datetime.now()))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id

    def end_session(self, session_id, end_balance, cards_dealt):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sessions 
            SET end_balance = ?, cards_dealt = ?, end_time = ?
            WHERE id = ?
        """, (end_balance, cards_dealt, datetime.datetime.now(), session_id))
        conn.commit()
        conn.close()

    def log_hand(self, session_id, player_cards, dealer_cards, actions, winnings):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO hands (session_id, player_cards, dealer_cards, actions, winnings)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, player_cards, dealer_cards, actions, winnings))
        conn.commit()
        conn.close()
