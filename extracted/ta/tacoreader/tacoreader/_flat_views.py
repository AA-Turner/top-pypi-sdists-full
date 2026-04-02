"""Flat view builder for user-facing SQL interface.

Builds l0, l1, l2, ... views on top of internal level0, level1, level2 views.
Each column is prefixed with its level of origin (l0:, l1:, l2:) to guarantee
zero collisions regardless of what columns each level contains.

These views are READ-ONLY and intended for user SQL queries via dataset.sql().
Internal navigation (cascade filters, .read(), RSUT checks) continues to use
level0, level1, level2 views directly.

Functions:
    build_flat_views: Create lN views for all available levels
"""

import duckdb

from tacoreader._constants import FLAT_VIEW_PREFIX, LEVEL_VIEW_PREFIX


def build_flat_views(
    db: duckdb.DuckDBPyConnection,
    level_ids: list[int],
) -> None:
    """Build flat user-facing views (l0, l1, l2, ...) over internal level views.

    Each flat view exposes columns from all levels up to and including the
    target level, with each column prefixed by its source level (l0:, l1:, ...).
    internal:* columns are excluded — they are navigation artifacts not needed
    in user SQL.

    View structure:
        l0 → all level0 columns prefixed "l0:"
        l1 → all level1 columns prefixed "l1:" + all level0 columns prefixed "l0:"
        l2 → all level2 columns prefixed "l2:" + l1 + l0 columns

    JOINs use internal:current_id / internal:parent_id from the raw level views.
    DuckDB predicate pushdown ensures filters are applied before joining.

    Args:
        db: DuckDB connection with level0, level1, ... views already registered
        level_ids: List of available level IDs, e.g. [0, 1, 2]

    Example:
        # After backends register level0/level1/level2:
        build_flat_views(db, [0, 1, 2])

        # User can now write:
        # SELECT "l0:stac:time_start", "l2:internal:gdal_vsi"
        # FROM l2
        # WHERE "l0:stac:time_start" LIKE '2020%'
    """
    for target_level in level_ids:
        _build_single_flat_view(db, target_level, level_ids)


def _get_level_columns(
    db: duckdb.DuckDBPyConnection,
    level_id: int,
) -> list[str]:
    """Get non-internal columns from a level view.

    Excludes internal:parent_id and internal:current_id (JOIN navigation artifacts).
    Keeps internal:gdal_vsi and other internal:* that may be useful to the user
    (e.g. internal:gdal_vsi for direct raster access).

    Args:
        db: DuckDB connection
        level_id: Level number

    Returns:
        List of column names to expose in flat view
    """
    view_name = f"{LEVEL_VIEW_PREFIX}{level_id}"
    rows = db.execute(
        f"SELECT column_name FROM information_schema.columns "
        f"WHERE table_name = '{view_name}' "
        f"ORDER BY ordinal_position"
    ).fetchall()

    exclude = {"internal:parent_id", "internal:current_id"}
    return [col for (col,) in rows if col not in exclude]


def _build_single_flat_view(
    db: duckdb.DuckDBPyConnection,
    target_level: int,
    level_ids: list[int],
) -> None:
    """Build a single flat view for the given target level.

    Args:
        db: DuckDB connection
        target_level: The level this view is for (0, 1, 2, ...)
        level_ids: All available level IDs (used to validate JOIN chain)
    """
    flat_name = f"{FLAT_VIEW_PREFIX}{target_level}"
    select_parts = []
    join_parts = []

    # Build SELECT: target level columns first, then parent levels descending
    for src_level in range(target_level, -1, -1):
        src_view = f"{LEVEL_VIEW_PREFIX}{src_level}"
        src_alias = f"_l{src_level}"
        prefix = f"{FLAT_VIEW_PREFIX}{src_level}"

        cols = _get_level_columns(db, src_level)
        for col in cols:
            select_parts.append(f'{src_alias}."{col}" AS "{prefix}:{col}"')

    # Build JOINs from target level up to l0
    # _lN JOIN levelN-1 ON levelN-1.current_id = _lN.parent_id
    for src_level in range(target_level - 1, -1, -1):
        child_alias = f"_l{src_level + 1}"
        parent_view = f"{LEVEL_VIEW_PREFIX}{src_level}"
        parent_alias = f"_l{src_level}"
        join_parts.append(
            f'JOIN {parent_view} {parent_alias} '
            f'ON {parent_alias}."internal:current_id" = {child_alias}."internal:parent_id"'
        )

    target_view = f"{LEVEL_VIEW_PREFIX}{target_level}"
    target_alias = f"_l{target_level}"

    sql = (
        f"CREATE OR REPLACE VIEW {flat_name} AS\n"
        f"SELECT {', '.join(select_parts)}\n"
        f"FROM {target_view} {target_alias}\n"
        + ("\n".join(join_parts) if join_parts else "")
    )

    db.execute(sql)