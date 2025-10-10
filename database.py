import sqlite3
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

# Define the database name constant.
DB_NAME = "iocs.db"

def init_db():
    # Using 'with' statement ensures the connection is closed automatically
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS iocs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    source TEXT,
                    date_added TEXT
                )''')
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
                )''')
        conn.commit()

def add_user(username, password, role='user'):
    # Using 'with' statement ensures the connection is closed automatically
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        # Ensure password hashing uses UTF-8 decoding for consistency
        hashed_pw = generate_password_hash(password).decode('utf-8')
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pw, role))
        conn.commit()

def verify_user(username, password):
    # Using 'with' statement ensures the connection is closed automatically
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM users WHERE username=?", (username,))
        user = c.fetchone()
    
    # Check if a user was found and verify the password
    if user and check_password_hash(user[2], password):
        return {"id": user[0], "username": user[1], "role": user[3]}
    return None


def add_ioc(url, source="manual"):
    """Add a new IOC (malicious URL) to the database."""
    # Using 'with' statement ensures the connection is closed automatically
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT OR IGNORE INTO iocs (url, source, date_added) VALUES (?, ?, ?)",
                      (url, source, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        except Exception as e:
            print("Error adding IOC:", e)

def get_recent(limit=10):
    """Get recent IOCs."""
    # Using 'with' statement ensures the connection is closed automatically
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT url, source, date_added FROM iocs ORDER BY date_added DESC LIMIT ?", (limit,))
        rows = c.fetchall()
    return rows

def find_ioc(url):
    """Search for a specific IOC."""
    # Using 'with' statement ensures the connection is closed automatically
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM iocs WHERE url=?", (url,))
        result = c.fetchone()
    return result
