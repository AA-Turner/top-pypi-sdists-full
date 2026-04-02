"""Flatten operation — returns all FILE rows with full ancestral metadata.

Two code paths:
    - No active filters: query flat view lN directly (fast)
    - Active cascade filters or simple view filter: rebuild JOINs over filtered views

Functions:
    execute_flatten: Build and execute the flatten query
"""

from typing import Any

import duckdb

from tacoreader._constants import DEFAULT_VIEW_NAME
from tacoreader.schema import PITSchema


def execute_flatten(
    db: duckdb.DuckDBPyConnection,
    backend: str,
    pit_schema: PITSchema,
    format_type: str,
    filtered_level_views: dict[int, str],
    view_name: str,
    level: int | None,
    sort_by: str | None = None,
    sort_descending: bool = False,
    limit_n: int | None = None,
) -> Any:
    """Return FILE rows from target level with full ancestral metadata.

    Args:
        db: DuckDB connection with flat views registered
        backend: One of "pyarrow", "polars", "pandas"
        pit_schema: PITSchema for max_depth resolution
        format_type: "zip", "folder", or "tacocat"
        filtered_level_views: Active cascade filter views keyed by level
        view_name: Current level0 view name (for simple filters)
        level: Target level (None = max_depth)
        sort_by: Column name to sort by (flat view prefixed, e.g. "l0:stac:time_start")
        sort_descending: True for DESC, False for ASC
        limit_n: Maximum number of rows to return

    Returns:
        Native DataFrame with all user columns + 'gdal_vsi' column
    """
    if level is None:
        level = pit_schema.max_depth()

    # Use filtered path if cascade filters are active OR if view_name was
    # changed by a simple filter (filter_datetime / filter_bbox at level=0).
    # _build_filtered_query already handles view_name via the _view(0) fallback.
    if filtered_level_views or view_name != DEFAULT_VIEW_NAME:
        query = _build_filtered_query(db, filtered_level_views, format_type, view_name, level)
    else:
        query = _build_flat_query(db, level)

    query = _apply_sort_limit(query, sort_by, sort_descending, limit_n)

    from tacoreader.sql.executor import execute_sql
    return execute_sql(db, query, backend)


def _apply_sort_limit(
    query: str,
    sort_by: str | None,
    sort_descending: bool,
    limit_n: int | None,
) -> str:
    """Append ORDER BY and LIMIT clauses to query if set."""
    if sort_by:
        direction = "DESC" if sort_descending else "ASC"
        query = f'{query.rstrip()}\n        ORDER BY "{sort_by}" {direction}'
    if limit_n is not None:
        query = f"{query.rstrip()}\n        LIMIT {limit_n}"
    return query


def _build_flat_query(db: duckdb.DuckDBPyConnection, level: int) -> str:
    """Build query over global flat view lN — no active filters."""
    columns = _get_flat_columns(db, level)
    select_clause = _build_select(columns, level)
    return f"""
        SELECT {select_clause}
        FROM l{level}
        WHERE "l{level}:type" = 'FILE'
    """


def _build_filtered_query(
    db: duckdb.DuckDBPyConnection,
    filtered_level_views: dict[int, str],
    format_type: str,
    view_name: str,
    level: int,
) -> str:
    """Build query with JOINs over filtered_level_views.

    Replicates flat view logic but using the cascade-filtered tables
    so results respect active filter state.
    """
    from tacoreader.nav._sql_builders import build_parent_child_join

    # Collect columns per level from the actual level views (not flat)
    level_columns: dict[int, list[str]] = {}
    for lvl in range(level + 1):
        rows = db.execute(
            f"SELECT column_name FROM information_schema.columns "
            f"WHERE table_name = 'level{lvl}' "
            f"ORDER BY ordinal_position"
        ).fetchall()
        exclude = {"internal:parent_id", "internal:current_id"}
        level_columns[lvl] = [col for (col,) in rows if col not in exclude]

    # Build SELECT with level prefixes
    select_parts = []
    for lvl in range(level, -1, -1):
        for col in level_columns[lvl]:
            if col.startswith("internal:"):
                continue
            prefixed = f"l{lvl}:{col}"
            select_parts.append(f'_l{lvl}."{col}" AS "{prefixed}"')

    # gdal_vsi always last
    select_parts.append(f'_l{level}."internal:gdal_vsi" AS gdal_vsi')

    select_clause = ", ".join(select_parts)

    # Determine which view to use per level
    def _view(lvl: int) -> str:
        if lvl in filtered_level_views:
            return filtered_level_views[lvl]
        if lvl == 0:
            return view_name
        return f"level{lvl}"

    # FROM + JOINs
    from_clause = f"{_view(level)} AS _l{level}"
    join_clauses = []
    for lvl in range(level - 1, -1, -1):
        join_cond = build_parent_child_join(format_type, f"_l{lvl}", f"_l{lvl + 1}")
        join_clauses.append(f"JOIN {_view(lvl)} AS _l{lvl} ON {join_cond}")

    joins = "\n        ".join(join_clauses)

    return f"""
        SELECT {select_clause}
        FROM {from_clause}
        {joins}
        WHERE _l{level}."type" = 'FILE'
    """


def _get_flat_columns(db: duckdb.DuckDBPyConnection, level: int) -> list[str]:
    """Get all columns from flat view lN via introspection."""
    rows = db.execute(
        f"SELECT column_name FROM information_schema.columns "
        f"WHERE table_name = 'l{level}' "
        f"ORDER BY ordinal_position"
    ).fetchall()
    return [col for (col,) in rows]


def _build_select(columns: list[str], level: int) -> str:
    """Build SELECT clause from flat view columns.

    Rules:
        - lN:internal:gdal_vsi → renamed to 'gdal_vsi'
        - All other internal:* → excluded
        - Everything else → kept as-is
    """
    by_level: dict[int, list[str]] = {lvl: [] for lvl in range(level, -1, -1)}

    for col in columns:
        if ":internal:" in col and col != f"l{level}:internal:gdal_vsi":
            continue
        for lvl in range(level, -1, -1):
            if col.startswith(f"l{lvl}:"):
                by_level[lvl].append(col)
                break

    parts = []
    for lvl in range(level, -1, -1):
        for col in by_level[lvl]:
            if col == f"l{level}:internal:gdal_vsi":
                continue  # gdal_vsi goes last
            parts.append(f'"{col}"')

    # gdal_vsi always last
    parts.append(f'"l{level}:internal:gdal_vsi" AS gdal_vsi')

    return ", ".join(parts)