
import sqlite3
import pandas as pd

DB_NAME = "job_verification.db"


def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS verification_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                job_title TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                verdict TEXT NOT NULL,
                warnings TEXT,
                checked_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_result(company, title, result):
    warnings = " | ".join(result["warnings"])

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            INSERT INTO verification_history
            (company, job_title, risk_score, verdict, warnings)
            VALUES (?, ?, ?, ?, ?)
        """, (
            company,
            title,
            result["risk_score"],
            result["verdict"],
            warnings
        ))


def get_history():
    with sqlite3.connect(DB_NAME) as conn:
        return pd.read_sql_query(
            "SELECT * FROM verification_history ORDER BY id DESC",
            conn
        )


def clear_history():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM verification_history")
