# src/canonmap/connectors/mysql_connector/matching/blocking.py

import re
from metaphone import doublemetaphone

def block_by_phonetic(conn, entity_name: str, table_name: str, field_name: str) -> set:
    """
    Block candidates using Double Metaphone phonetic encoding.
    Returns a set of unique candidate names from the database whose phonetic code matches.
    """
    p1, p2 = doublemetaphone(entity_name)
    search_code = p1 or p2
    if not search_code:
        return set()
    sql = f"""SELECT DISTINCT `{field_name}` AS name
              FROM `{table_name}`
              WHERE `__{field_name}_phonetic__` = %s"""
    with conn.cursor() as cur:
        cur.execute(sql, (search_code,))
        return {r[0] for r in cur.fetchall()}

def block_by_soundex(conn, entity_name: str, table_name: str, field_name: str) -> set:
    """
    Block candidates using MySQL's SOUNDEX function.
    """
    sql = f"""SELECT DISTINCT `{field_name}` AS name
              FROM `{table_name}`
              WHERE `__{field_name}_soundex__` = SOUNDEX(%s)"""
    with conn.cursor() as cur:
        cur.execute(sql, (entity_name,))
        return {r[0] for r in cur.fetchall()}

def block_by_initialism(conn, entity_name: str, table_name: str, field_name: str) -> set:
    """
    Block candidates using initialism matching.
    """
    if not entity_name:
        return set()
    entity_clean = entity_name.strip().upper()
    if (entity_clean.isalpha() and 2 <= len(entity_clean) <= 6 and ' ' not in entity_clean):
        search_initialism = entity_clean
    else:
        parts = re.findall(r"[A-Za-z]+", entity_name)
        search_initialism = "".join(p[0].upper() for p in parts) if parts else None
    if not search_initialism:
        return set()
    sql = f"""SELECT DISTINCT `{field_name}` AS name
              FROM `{table_name}`
              WHERE `__{field_name}_initialism__` = %s"""
    with conn.cursor() as cur:
        cur.execute(sql, (search_initialism,))
        return {r[0] for r in cur.fetchall()}

def block_by_exact_match(conn, entity_name: str, table_name: str, field_name: str) -> set:
    """
    Block candidates by exact (case-insensitive) substring match.
    """
    if not entity_name:
        return set()
    search_term = entity_name.strip().lower()
    sql = f"""SELECT DISTINCT `{field_name}` AS name
              FROM `{table_name}`
              WHERE LOWER(TRIM(`{field_name}`)) LIKE %s"""
    with conn.cursor() as cur:
        cur.execute(sql, (f"%{search_term}%",))
        return {r[0] for r in cur.fetchall()}

def get_more_candidates(conn, entity_name: str, table_name: str, field_name: str, min_candidates: int) -> set:
    """
    Broaden search for candidates if initial blocks are too narrow.
    Includes partial name match and fallback to random sampling.
    """
    additional_candidates = set()
    # Partial match on first and last name, if possible
    parts = entity_name.split()
    if len(parts) > 1:
        first_name = parts[0]
        last_name = parts[-1]
        sql = f"""SELECT DISTINCT `{field_name}` AS name
                  FROM `{table_name}`
                  WHERE LOWER(TRIM(`{field_name}`)) LIKE %s OR LOWER(TRIM(`{field_name}`)) LIKE %s
                  LIMIT %s"""
        with conn.cursor() as cur:
            cur.execute(sql, (f"%{first_name}%", f"%{last_name}%", min_candidates * 2))
            additional_candidates.update(r[0] for r in cur.fetchall())
    # If still not enough, sample random non-empty candidates
    if len(additional_candidates) < min_candidates:
        sql = f"""SELECT DISTINCT `{field_name}` AS name
                  FROM `{table_name}`
                  WHERE `{field_name}` IS NOT NULL AND `{field_name}` != ''
                  ORDER BY RAND()
                  LIMIT %s"""
        with conn.cursor() as cur:
            cur.execute(sql, (min_candidates,))
            additional_candidates.update(r[0] for r in cur.fetchall())
    return additional_candidates