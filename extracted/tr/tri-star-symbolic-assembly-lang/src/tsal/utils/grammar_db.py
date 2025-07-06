import sqlite3
from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

DB_PATH = Path("system_io.db")

DEFAULT_GRAMMARS = [
    ("Python", "syntax", "Indent with spaces"),
    ("Python", "style", "PEP8"),
    ("Python", "block", "Colons start blocks"),
    ("JavaScript", "syntax", "Semicolons optional"),
    ("JavaScript", "block", "{} for code blocks"),
    ("Universal", "part_of_speech", "noun"),
    ("Universal", "part_of_speech", "verb"),
]
DEFAULT_POS_RULES = ["noun", "verb", "adjective", "adverb", "preposition", "conjunction", "interjection"]
DEFAULT_LANGUAGE_GRAMMARS = [
    ("Python", "Indent with spaces"),
    ("JavaScript", "Semicolons optional"),
]

def create_grammar_table(
    db_path: Union[Path, str] = DB_PATH, *, reset: bool = False
) -> None:
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    if reset:
        cur.execute("DROP TABLE IF EXISTS grammar")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS grammar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            context TEXT,
            lens TEXT,
            rule TEXT,
            UNIQUE(context, lens, rule)
        )
        """
    )
    conn.commit()
    conn.close()

def populate_grammar_db(
    db_path: Union[Path, str] = DB_PATH,
    grammars: Optional[Sequence[Tuple[str, str, str]]] = None,
    *,
    reset: bool = False,
) -> int:
    create_grammar_table(db_path, reset=reset)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    grammars = grammars or DEFAULT_GRAMMARS
    cur.executemany(
        "INSERT OR IGNORE INTO grammar (context, lens, rule) VALUES (?, ?, ?)",
        grammars,
    )
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM grammar").fetchone()[0]
    conn.close()
    return count

def get_grammar_by_context(
    db_path: Union[Path, str] = DB_PATH,
    context: Optional[str] = None,
    lens: Optional[str] = None,
) -> list[Tuple[str, str, str]]:
    create_grammar_table(db_path)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    sql = "SELECT context, lens, rule FROM grammar WHERE 1=1"
    params = []
    if context:
        sql += " AND context=?"
        params.append(context)
    if lens:
        sql += " AND lens=?"
        params.append(lens)
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def populate_language_grammar_db(
    db_path: Path = DB_PATH, examples: Optional[Sequence[Tuple[str, str]]] = None
) -> int:
    grammars = examples or DEFAULT_LANGUAGE_GRAMMARS
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS grammar_language (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT,
            rules TEXT,
            UNIQUE(language, rules)
        )
        """
    )
    cur.executemany(
        "INSERT OR IGNORE INTO grammar_language (language, rules) VALUES (?, ?)",
        grammars,
    )
    if grammars:
        cur.executemany(
            "INSERT OR IGNORE INTO grammar (context, lens, rule) VALUES (?, ?, ?)",
            list(grammars),
        )
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM grammar_language").fetchone()[0]
    conn.close()
    return count

def populate_pos_grammar_db(
    db_path: Path = DB_PATH, rules: Optional[Sequence[str]] = None
) -> int:
    rules = rules or DEFAULT_POS_RULES
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS grammar_pos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule TEXT UNIQUE
        )
        """
    )
    cur.executemany(
        "INSERT OR IGNORE INTO grammar_pos (rule) VALUES (?)",
        [(r,) for r in rules],
    )
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM grammar_pos").fetchone()[0]
    conn.close()
    return count

def main(argv: Optional[Sequence[str]] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Populate or query the grammar database")
    parser.add_argument("--db", default="system_io.db", help="Path to SQLite database")
    parser.add_argument("--context", help="Filter by context when querying")
    parser.add_argument("--lens", help="Filter by lens when querying")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate tables before populating")
    args = parser.parse_args(argv)

    if args.context or args.lens:
        rows = get_grammar_by_context(args.db, context=args.context, lens=args.lens)
        for row in rows:
            print("|".join(row))
    else:
        count = populate_grammar_db(args.db, reset=args.reset)
        print(f"{count} entries stored in {args.db}")

if __name__ == "__main__":
    main()
