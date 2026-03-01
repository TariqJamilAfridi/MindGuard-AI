import sqlite3
import hashlib
import re
from datetime import datetime

DB_PATH = "mindguard.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER DEFAULT NULL,
            text       TEXT    NOT NULL,
            sentiment  TEXT    NOT NULL,
            score      REAL    NOT NULL,
            emotions   TEXT    NOT NULL,
            response   TEXT    NOT NULL,
            tip        TEXT    NOT NULL,
            created_at TEXT    NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            created_at  TEXT    NOT NULL,
            last_email  TEXT    DEFAULT NULL,
            entry_count INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database ready.")

# ── Entries ────────────────────────────────────────────────
def save_entry(text, sentiment, score, emotions, response, tip, user_id=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO entries (user_id,text,sentiment,score,emotions,response,tip,created_at)
        VALUES (?,?,?,?,?,?,?,?)
    """, (user_id, text, sentiment, score, ", ".join(emotions),
          response, tip, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    eid = c.lastrowid
    conn.close()
    if user_id:
        _bump_count(user_id)
    return eid

def get_all_entries(user_id=None):
    conn = get_connection()
    c = conn.cursor()
    if user_id:
        c.execute("SELECT * FROM entries WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    else:
        c.execute("SELECT * FROM entries ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_recent_entries(days=30, user_id=None):
    conn = get_connection()
    c = conn.cursor()
    if user_id:
        c.execute("""
            SELECT DATE(created_at) as day, AVG(score) as avg_score, COUNT(*) as count
            FROM entries WHERE user_id=? AND created_at >= DATE('now',?)
            GROUP BY DATE(created_at) ORDER BY day ASC
        """, (user_id, f"-{days} days"))
    else:
        c.execute("""
            SELECT DATE(created_at) as day, AVG(score) as avg_score, COUNT(*) as count
            FROM entries WHERE created_at >= DATE('now',?)
            GROUP BY DATE(created_at) ORDER BY day ASC
        """, (f"-{days} days",))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_emotion_counts(user_id=None):
    conn = get_connection()
    c = conn.cursor()
    if user_id:
        c.execute("SELECT emotions FROM entries WHERE user_id=?", (user_id,))
    else:
        c.execute("SELECT emotions FROM entries")
    rows = c.fetchall()
    conn.close()
    counts = {}
    for row in rows:
        for em in row["emotions"].split(", "):
            em = em.strip()
            if em:
                counts[em] = counts.get(em, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

# ── Users ──────────────────────────────────────────────────
def _hash(pw): return hashlib.sha256(pw.encode()).hexdigest()

def register_user(name, email, password):
    email = email.strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return None, "Invalid email address."
    if len(password) < 6:
        return None, "Password must be at least 6 characters."
    if len(name.strip()) < 2:
        return None, "Please enter your name."
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO users (name,email,password,created_at)
                     VALUES (?,?,?,?)""",
                  (name.strip(), email, _hash(password),
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        uid = c.lastrowid
        conn.close()
        return get_user_by_id(uid), None
    except sqlite3.IntegrityError:
        conn.close()
        return None, "This email is already registered."

def login_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (email.strip().lower(), _hash(password)))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(uid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (uid,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def _bump_count(uid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET entry_count=entry_count+1 WHERE id=?", (uid,))
    conn.commit()
    conn.close()

def get_users_for_digest():
    """Users with entries who haven't received a digest in 7 days."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE entry_count>0
                 AND (last_email IS NULL OR last_email<=DATE('now','-7 days'))""")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def mark_email_sent(uid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET last_email=? WHERE id=?",
              (datetime.now().strftime("%Y-%m-%d"), uid))
    conn.commit()
    conn.close()
