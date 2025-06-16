import sqlite3

def init_db():
    conn = sqlite3.connect("app/db/data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS config (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # default_config = {
    #     "POSTGRES_USER": None,
    #     "POSTGRES_PASSWORD": None,
    #     "POSTGRES_DB": None,
    #     "POSTGRES_HOST": None,
    #     "POSTGRES_PORT": None,
    #     "REDIS_HOST": None,
    #     "REDIS_PORT": None,
    #     "CHROMADB_HOST": None,
    #     "CHROMADB_PORT": None,
    #     "CHROMADB_API_KEY": None
    # }

    # for key, value in default_config.items():
    #     cursor.execute("INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)", (key, value))

    conn.commit()
    conn.close()
