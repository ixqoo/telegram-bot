import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        playlist TEXT,
        text TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT
    )
    """)
    conn.commit()

def add_user(user_id, username):
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", (user_id, username))
    conn.commit()

def add_track(user_id, playlist, text):
    cursor.execute("INSERT INTO tracks (user_id, playlist, text) VALUES (?, ?, ?)",
                   (user_id, playlist, text))
    conn.commit()

def add_question(user_id, text):
    cursor.execute("INSERT INTO questions (user_id, text) VALUES (?, ?)",
                   (user_id, text))
    conn.commit()

def get_tracks():
    return cursor.execute("SELECT * FROM tracks").fetchall()

def get_questions():
    return cursor.execute("SELECT * FROM questions").fetchall()

def get_users():
    return cursor.execute("SELECT * FROM users").fetchall()
