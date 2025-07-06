import sqlite3
from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

DB_PATH = Path("system_io.db")

DEFAULT_JOKES = [
    ("Python", "Why do Python devs prefer dark mode? Because light attracts bugs."),
    ("General", "Why do programmers hate nature? It has too many bugs."),
]
DEFAULT_ONE_LINERS = [
    "Why did the chicken cross the road? To get to the other side.",
    "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'",
]

def create_humour_table(db_path: Union[Path, str] = DB_PATH, *, reset: bool = False) -> None:
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    if reset:
        cur.execute("DROP TABLE IF EXISTS humour")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS humour (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            context TEXT,
            joke TEXT UNIQUE
        )
        """
    )
    conn.commit()
    conn.close()

def populate_humour_db(
    db_path: Union[Path, str] = DB_PATH,
    jokes: Optional[Sequence[Union[Tuple[str, str], str]]] = None,
    *,
    reset: bool = False,
) -> int:
    create_humour_table(db_path, reset=reset)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # Prepare list of (context, joke) tuples
    combined: list[Tuple[str, str]] = []
    jokes = jokes or []
    for entry in jokes:
        if isinstance(entry, tuple) and len(entry) == 2:
            combined.append(entry)
        elif isinstance(entry, str):
            combined.append(("General", entry))
    if not combined:
        combined = DEFAULT_JOKES + [("General", j) for j in DEFAULT_ONE_LINERS]

    cur.executemany(
        "INSERT OR IGNORE INTO humour (context, joke) VALUES (?, ?)",
        combined,
    )
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM humour").fetchone()[0]
    conn.close()
    return count

def main(argv: Optional[Sequence[str]] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Populate humour database")
    parser.add_argument("--db", default="system_io.db", help="Path to SQLite DB")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate the humour table before populating")
    args = parser.parse_args(argv)

    count = populate_humour_db(args.db, reset=args.reset)
    print(f"{count} jokes stored in {args.db}")

if __name__ == "__main__":
    main()
