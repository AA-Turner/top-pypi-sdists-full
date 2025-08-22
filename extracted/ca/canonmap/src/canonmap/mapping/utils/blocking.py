import logging
import re
from typing import Callable, Dict, Iterable, Optional

from metaphone import doublemetaphone
from canonmap.connectors.mysql_connector.utils.db_metadata import (
    column_exists as _column_exists,
)
from canonmap.connectors.mysql_connector.utils.transforms import (
    to_soundex as _to_soundex,
)

# logger = logging.getLogger(__name__)


# --- Strategy helpers and registry -----------------------------------------------------------

def _execute_and_collect_names(db_connection_manager, sql: str, params: Iterable, limit: Optional[int] = None) -> set:
    resp = db_connection_manager.execute_query(sql, list(params), allow_writes=False, limit=limit)
    rows = resp.get("data") or []
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


def _sql_phonetic(connector, table_name: str, field_name: str, prefilter_subquery: Optional[str] = None) -> Optional[str]:
    primary = f"__{field_name}_phonetic__"
    fallback = f"{field_name}_phonetic__"
    helper_col = None
    try:
        if _column_exists(connector, table_name, primary):
            helper_col = primary
        elif _column_exists(connector, table_name, fallback):
            helper_col = fallback
    except Exception:
        # If metadata lookup fails for any reason, do not build SQL
        helper_col = None
    if not helper_col:
        return None
    
    from_clause = f"`{table_name}`"
    if prefilter_subquery:
        from_clause = f"{prefilter_subquery} AS `{table_name}`"
    
    return f"""
        SELECT DISTINCT `{field_name}` AS name
        FROM {from_clause}
        WHERE `{helper_col}` LIKE %s
    """


def _sql_initialism(connector, table_name: str, field_name: str, prefilter_subquery: Optional[str] = None) -> Optional[str]:
    primary = f"__{field_name}_initialism__"
    fallback = f"{field_name}_initialism__"
    helper_col = None
    try:
        if _column_exists(connector, table_name, primary):
            helper_col = primary
        elif _column_exists(connector, table_name, fallback):
            helper_col = fallback
    except Exception:
        helper_col = None
    if not helper_col:
        return None
    
    from_clause = f"`{table_name}`"
    if prefilter_subquery:
        from_clause = f"{prefilter_subquery} AS `{table_name}`"
    
    return f"""
        SELECT DISTINCT `{field_name}` AS name
        FROM {from_clause}
        WHERE `{helper_col}` = %s
    """


def _sql_exact(connector, table_name: str, field_name: str, prefilter_subquery: Optional[str] = None) -> str:
    from_clause = f"`{table_name}`"
    if prefilter_subquery:
        from_clause = f"{prefilter_subquery} AS `{table_name}`"
    
    return f"""
        SELECT DISTINCT `{field_name}` AS name
        FROM {from_clause}
        WHERE LOWER(TRIM(`{field_name}`)) LIKE %s
    """


def _simple_handler(
    db_connection_manager,
    entity_name: str,
    table_name: str,
    field_name: str,
    prepare_param: Callable[[str], Optional[str]],
    sql_builder: Callable[[object, str, str, Optional[str]], Optional[str]],
    limit: Optional[int] = None,
    prefilter_subquery: Optional[str] = None,
) -> set:
    param = prepare_param(entity_name)
    if not param:
        return set()
    sql = sql_builder(db_connection_manager, table_name, field_name, prefilter_subquery)
    if not sql:
        return set()
    return _execute_and_collect_names(db_connection_manager, sql, (param,), limit=limit)


def _soundex_handler(db_connection_manager, entity_name: str, table_name: str, field_name: str, limit: Optional[int] = None, prefilter_subquery: Optional[str] = None) -> set:
    """
    Block candidates using helper field if available; otherwise use MySQL's SOUNDEX.
    """
    from_clause = f"`{table_name}`"
    if prefilter_subquery:
        from_clause = f"{prefilter_subquery} AS `{table_name}`"
    
    # Prefer helper field column if present: __<field>_soundex__
    try:
        primary = f"__{field_name}_soundex__"
        fallback = f"{field_name}_soundex__"
        helper_col_name = None
        if _column_exists(db_connection_manager, table_name, primary):
            helper_col_name = primary
        elif _column_exists(db_connection_manager, table_name, fallback):
            helper_col_name = fallback
        if helper_col_name:
            code = _to_soundex(entity_name)
            if not code:
                return set()
            helper_sql = f"""
                SELECT DISTINCT `{field_name}` AS name
                FROM {from_clause}
                WHERE `{helper_col_name}` = %s
            """
            resp = db_connection_manager.execute_query(helper_sql, [code], allow_writes=False, limit=limit)
            rows = resp.get("data") or []
            return {r["name"] for r in rows}
    except Exception:
        # Ignore helper column issues and fall back to SOUNDEX function
        pass

    primary_sql = f"""
        SELECT DISTINCT `{field_name}` AS name
        FROM {from_clause}
        WHERE SOUNDEX(`{field_name}`) = SOUNDEX(%s)
    """
    resp = db_connection_manager.execute_query(primary_sql, [entity_name], allow_writes=False, limit=limit)
    rows = resp.get("data") or []
    return {r["name"] for r in rows}


# Public registry mapping block type to handler callable
BLOCKING_HANDLERS: Dict[str, Callable[[object, str, str, str, Optional[int], Optional[str]], set]] = {
    "phonetic": lambda db, e, t, f, lim=None, prefilter=None: _simple_handler(db, e, t, f, _prepare_phonetic_param, _sql_phonetic, lim, prefilter),
    "initialism": lambda db, e, t, f, lim=None, prefilter=None: _simple_handler(db, e, t, f, _prepare_initialism_param, _sql_initialism, lim, prefilter),
    "exact": lambda db, e, t, f, lim=None, prefilter=None: _simple_handler(db, e, t, f, _prepare_exact_param, _sql_exact, lim, prefilter),
    "soundex": _soundex_handler,
}


def block_candidates(
    db_connection_manager,
    entity_name: str,
    table_name: str,
    field_name: str,
    block_type: str,
    limit: Optional[int] = None,
    prefilter_subquery: Optional[str] = None,
) -> set:
    """
    General blocking function using a strategy map.
    Valid block_type values: "phonetic", "soundex", "initialism", "exact".
    """
    handler = BLOCKING_HANDLERS.get(block_type)
    if handler is None:
        raise ValueError(f"Unknown block_type '{block_type}'")
    return handler(db_connection_manager, entity_name, table_name, field_name, limit, prefilter_subquery)


# --- Backward-compatible wrappers -------------------------------------------------------------

def block_by_phonetic(db_connection_manager, entity_name: str, table_name: str, field_name: str, limit: Optional[int] = None) -> set:
    return block_candidates(db_connection_manager, entity_name, table_name, field_name, "phonetic", limit)


def block_by_soundex(db_connection_manager, entity_name: str, table_name: str, field_name: str, limit: Optional[int] = None) -> set:
    return block_candidates(db_connection_manager, entity_name, table_name, field_name, "soundex", limit)


def block_by_initialism(db_connection_manager, entity_name: str, table_name: str, field_name: str, limit: Optional[int] = None) -> set:
    return block_candidates(db_connection_manager, entity_name, table_name, field_name, "initialism", limit)


def block_by_exact_match(db_connection_manager, entity_name: str, table_name: str, field_name: str, limit: Optional[int] = None) -> set:
    return block_candidates(db_connection_manager, entity_name, table_name, field_name, "exact", limit)
