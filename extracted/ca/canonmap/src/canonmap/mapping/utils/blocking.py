import logging
import re
from typing import Callable, Dict, Iterable, Optional

from metaphone import doublemetaphone

# logger = logging.getLogger(__name__)


# --- Strategy helpers and registry -----------------------------------------------------------

def _execute_and_collect_names(db_connection_manager, sql: str, params: Iterable) -> set:
    rows = db_connection_manager.execute_query(sql, params)
    return {row["name"] for row in rows}


def _prepare_phonetic_param(entity_name: str) -> Optional[str]:
    p1, p2 = doublemetaphone(entity_name)
    return p1 or p2


def _prepare_initialism_param(entity_name: str) -> Optional[str]:
    if not entity_name:
        return None
    entity_clean = entity_name.strip().upper()
    if entity_clean.isalpha() and 2 <= len(entity_clean) <= 6 and " " not in entity_clean:
        return entity_clean
    parts = re.findall(r"[A-Za-z]+", entity_name)
    return "".join(p[0].upper() for p in parts) if parts else None


def _prepare_exact_param(entity_name: str) -> Optional[str]:
    if not entity_name:
        return None
    return entity_name.strip().lower()


def _sql_phonetic(table_name: str, field_name: str) -> str:
    return f"""
        SELECT DISTINCT `{field_name}` AS name
        FROM `{table_name}`
        WHERE `__{field_name}_phonetic__` LIKE %s
    """


def _sql_initialism(table_name: str, field_name: str) -> str:
    return f"""
        SELECT DISTINCT `{field_name}` AS name
        FROM `{table_name}`
        WHERE `__{field_name}_initialism__` = %s
    """


def _sql_exact(table_name: str, field_name: str) -> str:
    return f"""
        SELECT DISTINCT `{field_name}` AS name
        FROM `{table_name}`
        WHERE LOWER(TRIM(`{field_name}`)) LIKE %s
    """


def _simple_handler(
    db_connection_manager,
    entity_name: str,
    table_name: str,
    field_name: str,
    prepare_param: Callable[[str], Optional[str]],
    sql_builder: Callable[[str, str], str],
) -> set:
    param = prepare_param(entity_name)
    if not param:
        return set()
    sql = sql_builder(table_name, field_name)
    return _execute_and_collect_names(db_connection_manager, sql, (param,))


def _soundex_handler(db_connection_manager, entity_name: str, table_name: str, field_name: str) -> set:
    """
    Block candidates using MySQL's SOUNDEX function, with fallback to helper table.
    """
    primary_sql = f"""
        SELECT DISTINCT `{field_name}` AS name
        FROM `{table_name}`
        WHERE SOUNDEX(`{field_name}`) = SOUNDEX(%s)
    """
    rows = db_connection_manager.execute_query(primary_sql, [entity_name])
    candidates = {r["name"] for r in rows}
    if candidates:
        return candidates

    fallback_sql = """
        SELECT DISTINCT name
        FROM soundex_helper
        WHERE code = SOUNDEX(%s)
    """
    helper_rows = db_connection_manager.execute_query(fallback_sql, [entity_name])
    return {r["name"] for r in helper_rows}


# Public registry mapping block type to handler callable
BLOCKING_HANDLERS: Dict[str, Callable[[object, str, str, str], set]] = {
    "phonetic": lambda db, e, t, f: _simple_handler(db, e, t, f, _prepare_phonetic_param, _sql_phonetic),
    "initialism": lambda db, e, t, f: _simple_handler(db, e, t, f, _prepare_initialism_param, _sql_initialism),
    "exact": lambda db, e, t, f: _simple_handler(db, e, t, f, _prepare_exact_param, _sql_exact),
    "soundex": _soundex_handler,
}


def block_candidates(
    db_connection_manager,
    entity_name: str,
    table_name: str,
    field_name: str,
    block_type: str,
) -> set:
    """
    General blocking function using a strategy map.
    Valid block_type values: "phonetic", "soundex", "initialism", "exact".
    """
    handler = BLOCKING_HANDLERS.get(block_type)
    if handler is None:
        raise ValueError(f"Unknown block_type '{block_type}'")
    return handler(db_connection_manager, entity_name, table_name, field_name)


# --- Backward-compatible wrappers -------------------------------------------------------------

def block_by_phonetic(db_connection_manager, entity_name: str, table_name: str, field_name: str) -> set:
    return block_candidates(db_connection_manager, entity_name, table_name, field_name, "phonetic")


def block_by_soundex(db_connection_manager, entity_name: str, table_name: str, field_name: str) -> set:
    return block_candidates(db_connection_manager, entity_name, table_name, field_name, "soundex")


def block_by_initialism(db_connection_manager, entity_name: str, table_name: str, field_name: str) -> set:
    return block_candidates(db_connection_manager, entity_name, table_name, field_name, "initialism")


def block_by_exact_match(db_connection_manager, entity_name: str, table_name: str, field_name: str) -> set:
    return block_candidates(db_connection_manager, entity_name, table_name, field_name, "exact")
