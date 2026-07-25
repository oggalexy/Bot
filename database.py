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
        type TEXT NOT NULL,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        used INTEGER DEFAULT 0
    )
    """)

    db.commit()
    db.close()


def add_account(account_type, login, password):
    db = connect()
    c = db.cursor()

    c.execute(
        """
        INSERT INTO accounts(type, login, password)
        VALUES (?, ?, ?)
        """,
        (account_type, login, password)
    )

    db.commit()
    db.close()


def get_accounts(account_type, amount):
    db = connect()
    c = db.cursor()

    c.execute(
        """
        SELECT id, login, password
        FROM accounts
        WHERE type=? AND used=0
        LIMIT ?
        """,
        (account_type, amount)
    )

    accounts = c.fetchall()

    for account in accounts:
        c.execute(
            """
            UPDATE accounts
            SET used=1
            WHERE id=?
            """,
            (account[0],)
        )

    db.commit()
    db.close()

    return accounts


def get_stock(account_type):
    db = connect()
    c = db.cursor()

    c.execute(
        """
        SELECT COUNT(*)
        FROM accounts
        WHERE type=? AND used=0
        """,
        (account_type,)
    )

    amount = c.fetchone()[0]

    db.close()

    return amount


def add_many(accounts):
    db = connect()
    c = db.cursor()

    for account in accounts:
        c.execute(
            """
            INSERT INTO accounts(type, login, password)
            VALUES (?, ?, ?)
            """,
            (
                account["type"],
                account["login"],
                account["password"]
            )
        )

    db.commit()
    db.close()
