import sqlite3
from typing import Sequence, Optional

from .github_api import fetch_languages

def populate_language_db(
    db_path: str = "system_io.db", languages: Optional[Sequence[str]] = None
) -> int:
    """Populate a SQLite DB with GitHub languages.

    Parameters
    ----------
    db_path: str
        Path to the SQLite database file.
    languages: Sequence[str] | None
        Languages to store. If None, fetch from GitHub.

    Returns
    -------
    int
        Total number of languages stored in the database.
    """
    if languages is None:
        languages = fetch_languages()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS languages (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)"
    )
    cur.executemany(
        "INSERT OR IGNORE INTO languages (name) VALUES (?)",
        [(lang,) for lang in languages],
    )
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM languages").fetchone()[0]
    conn.close()
    return count

def main(argv: Optional[Sequence[str]] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Populate local language database from GitHub linguist"
    )
    parser.add_argument(
        "--db", default="system_io.db", help="Path to SQLite database"
    )
    args = parser.parse_args(argv)

    count = populate_language_db(args.db)
    print(f"{count} languages stored in {args.db}")

if __name__ == "__main__":
    main()
