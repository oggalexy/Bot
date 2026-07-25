import sqlite3

DB = "accounts.db"


def connect():
    return sqlite3.connect(DB)


def setup():
    db = connect()
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        login TEXT,
        password TEXT,
        used INTEGER DEFAULT 0
    )
    """)

    db.commit()
    db.close()


def add_account(type, login, password):
    db = connect()
    c = db.cursor()

    c.execute(
        "INSERT INTO accounts(type,login,password) VALUES(?,?,?)",
        (type, login, password)
    )

    db.commit()
    db.close()


def get_accounts(type, amount):

    db = connect()
    c = db.cursor()

    c.execute(
        """
        SELECT id,login,password 
        FROM accounts
        WHERE type=? AND used=0
        LIMIT ?
        """,
        (type, amount)
    )

    accounts = c.fetchall()

    for acc in accounts:
        c.execute(
            "UPDATE accounts SET used=1 WHERE id=?",
            (acc[0],)
        )

    db.commit()
    db.close()

    return accounts


def stock(type):

    db = connect()
    c = db.cursor()

    c.execute(
        "SELECT COUNT(*) FROM accounts WHERE type=? AND used=0",
        (type,)
    )

    result = c.fetchone()[0]

    db.close()

    return result
