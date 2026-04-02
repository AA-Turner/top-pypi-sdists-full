"""Navigation filters — return TacoDataset, never DataFrame.

This is the nav/ branch of tacoreader:
    nav/   → ds.filter_*() → TacoDataset  (this module)
    sql/   → ds.sql(query) → DataFrame

Two filter modes:
    simple (level=0)   → WHERE on current view, no JOINs
    cascade (level>0)  → hierarchical JOINs, propagates upward

Both modes create TEMP VIEWs and return TacoDataset via build_filtered_dataset.
Neither mode calls .sql() — that would break the branch separation.

Functions:
    apply_bbox_filter: Spatial filtering entry point
    apply_datetime_filter: Temporal filtering entry point
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from tacoreader._constants import LEVEL_VIEW_PREFIX
from tacoreader._exceptions import TacoQueryError
from tacoreader.nav._sql_builders import (
    build_bbox_where,
    build_datetime_where,
    build_parent_child_join,
)
from tacoreader.nav._view_builder import build_filtered_dataset

if TYPE_CHECKING:
    from tacoreader.dataset import TacoDataset


_GEOMETRY_PRIORITY = ["istac:geometry", "stac:centroid", "istac:centroid"]
_TIME_PRIORITY = ["istac:time_start", "stac:time_start"]


def apply_bbox_filter(
    dataset: "TacoDataset",
    minx: float,
    miny: float,
    maxx: float,
    maxy: float,
    geometry_col: str,
    level: int,
) -> "TacoDataset":
    """Filter by bounding box at any hierarchy level.

    level=0: WHERE on current view, no JOINs.
    level>0: hierarchical JOINs propagating upward to level0.

    Args:
        dataset: TacoDataset to filter
        minx, miny, maxx, maxy: Bounding box coordinates
        geometry_col: Geometry column name ("auto" for detection)
        level: Hierarchy level to filter at

    Returns:
        Filtered TacoDataset
    """
    _validate_level(dataset, level)
    cols = _get_columns(dataset, level)
    geometry_col = _resolve_geometry_col(geometry_col, cols, level)
    where = build_bbox_where(geometry_col, minx, miny, maxx, maxy)

    if level == 0:
        return _simple_filter(dataset, where)
    return _cascade_filter(dataset, level, where)


def apply_datetime_filter(
    dataset: "TacoDataset",
    datetime_range: str | datetime | tuple[datetime, datetime],
    time_col: str,
    level: int,
) -> "TacoDataset":
    """Filter by datetime range at any hierarchy level.

    level=0: WHERE on current view, no JOINs.
    level>0: hierarchical JOINs propagating upward to level0.

    Args:
        dataset: TacoDataset to filter
        datetime_range: String range, single datetime, or tuple
        time_col: Time column name ("auto" for detection)
        level: Hierarchy level to filter at

    Returns:
        Filtered TacoDataset
    """
    _validate_level(dataset, level)
    cols = _get_columns(dataset, level)
    time_col = _resolve_time_col(time_col, cols, level)
    start, end = _parse_datetime(datetime_range)
    where = build_datetime_where(time_col, start, end)

    if level == 0:
        return _simple_filter(dataset, where)
    return _cascade_filter(dataset, level, where)


def _simple_filter(dataset: "TacoDataset", where_clause: str) -> "TacoDataset":
    """Apply WHERE on current view. No JOINs, no cascade."""
    db = dataset._duckdb
    view = f"view_{uuid.uuid4().hex[:8]}"

    db.execute(
        f"CREATE TEMP VIEW {view} AS "
        f"SELECT * FROM {dataset._query.view_name} WHERE {where_clause}"
    )
    n = db.execute(f"SELECT COUNT(*) FROM {view}").fetchone()[0]

    return build_filtered_dataset(
        dataset=dataset,
        final_view=view,
        new_n=n,
        rsut_compliant=dataset._query.rsut_compliant,
        filtered_level_views={},
        joined_levels=dataset._query.joined_levels.copy(),
    )


def _cascade_filter(
    dataset: "TacoDataset",
    target_level: int,
    where_clause: str,
) -> "TacoDataset":
    """Filter at target level and propagate upward to level0.

    Strategy:
        1. Filter target level by where_clause → filtered_level{N}
        2. For each level from target-1 down to 0:
           keep only parents that have surviving children
        3. Create final view from filtered level0
        4. Check RSUT compliance
    """
    db = dataset._duckdb
    suffix = uuid.uuid4().hex[:8]
    format_type = dataset._origin.format
    filtered_views: dict[int, str] = {}

    target_view = f"{LEVEL_VIEW_PREFIX}{target_level}"
    filtered_target = f"filtered_{target_level}_{suffix}"
    db.execute(
        f"CREATE TEMP VIEW {filtered_target} AS "
        f"SELECT * FROM {target_view} WHERE {where_clause}"
    )
    filtered_views[target_level] = filtered_target

    for lvl in range(target_level - 1, -1, -1):
        child_view = filtered_views[lvl + 1]
        current_view = dataset._query.view_name if lvl == 0 else f"{LEVEL_VIEW_PREFIX}{lvl}"
        filtered_current = f"filtered_{lvl}_{suffix}"
        join_cond = build_parent_child_join(format_type, "parent", "child")

        db.execute(
            f"""
            CREATE TEMP VIEW {filtered_current} AS
            SELECT DISTINCT parent.*
            FROM {current_view} parent
            INNER JOIN {child_view} child ON {join_cond}
            """
        )
        filtered_views[lvl] = filtered_current

    final_view = f"view_{suffix}"
    db.execute(
        f"CREATE TEMP VIEW {final_view} AS "
        f"SELECT * FROM {filtered_views[0]}"
    )
    n = db.execute(f"SELECT COUNT(*) FROM {final_view}").fetchone()[0]

    rsut = _check_cascade_rsut(db, filtered_views, format_type)

    joined_levels = dataset._query.joined_levels.copy()
    for lvl in range(1, target_level + 1):
        joined_levels.add(f"{LEVEL_VIEW_PREFIX}{lvl}")

    return build_filtered_dataset(
        dataset=dataset,
        final_view=final_view,
        new_n=n,
        rsut_compliant=rsut,
        filtered_level_views=filtered_views,
        joined_levels=joined_levels,
    )


def _check_cascade_rsut(
    db,
    filtered_views: dict[int, str],
    format_type: str,
) -> bool:
    """Check structural homogeneity after cascade filter."""
    if 0 not in filtered_views or 1 not in filtered_views:
        return True

    join_cond = build_parent_child_join(format_type, "l0", "l1")
    query = f"""
        WITH parent_children AS (
            SELECT
                l0."internal:current_id" as parent_id,
                COALESCE(STRING_AGG(l1.id, '|' ORDER BY l1.id), '') as children_sig
            FROM {filtered_views[0]} l0
            LEFT JOIN {filtered_views[1]} l1 ON {join_cond}
            GROUP BY l0."internal:current_id"
        )
        SELECT COUNT(DISTINCT children_sig) = 1 as is_homogeneous
        FROM parent_children
    """
    try:
        result = db.execute(query).fetchone()
        return bool(result[0]) if result else True
    except Exception:
        return False


def _validate_level(dataset: "TacoDataset", level: int) -> None:
    max_level = dataset.pit_schema.max_depth()
    if level < 0 or level > max_level:
        raise TacoQueryError(
            f"Level {level} does not exist.\nAvailable levels: 0 to {max_level}"
        )


def _get_columns(dataset: "TacoDataset", level: int) -> list[str]:
    if level == 0:
        return dataset.data.columns
    view = f"{LEVEL_VIEW_PREFIX}{level}"
    return [row[0] for row in dataset._duckdb.execute(f"DESCRIBE {view}").fetchall()]


def _resolve_geometry_col(col: str, columns: list[str], level: int) -> str:
    if col != "auto":
        if col not in columns:
            raise TacoQueryError(
                f"Column '{col}' not found at level {level}.\n"
                f"Available columns: {columns}"
            )
        return col
    for candidate in _GEOMETRY_PRIORITY:
        if candidate in columns:
            return candidate
    raise TacoQueryError(
        f"No geometry column found at level {level}.\n"
        f"Expected one of: {', '.join(_GEOMETRY_PRIORITY)}\n"
        f"Available columns: {columns}"
    )


def _resolve_time_col(col: str, columns: list[str], level: int) -> str:
    if col != "auto":
        if col not in columns:
            raise TacoQueryError(
                f"Column '{col}' not found at level {level}.\n"
                f"Available columns: {columns}"
            )
        return col
    for candidate in _TIME_PRIORITY:
        if candidate in columns:
            return candidate
    raise TacoQueryError(
        f"No time column found at level {level}.\n"
        f"Expected one of: {', '.join(_TIME_PRIORITY)}\n"
        f"Available columns: {columns}"
    )


def _parse_datetime(
    dt_input: str | datetime | tuple[datetime, datetime],
) -> tuple[int, int | None]:
    """Parse datetime input to (start_epoch, end_epoch)."""
    from datetime import timezone

    def _to_utc(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    def _parse_str(s: str) -> datetime:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return _to_utc(dt)

    if isinstance(dt_input, str):
        if "/" in dt_input:
            start_str, end_str = dt_input.split("/", 1)
            s = int(_parse_str(start_str).timestamp())
            e = int(_parse_str(end_str).timestamp())
            if s > e:
                raise TacoQueryError(f"Invalid range: start ({start_str}) > end ({end_str})")
            return s, e
        return int(_parse_str(dt_input).timestamp()), None

    elif isinstance(dt_input, datetime):
        return int(_to_utc(dt_input).timestamp()), None

    elif isinstance(dt_input, tuple) and len(dt_input) == 2:
        s = int(_to_utc(dt_input[0]).timestamp())
        e = int(_to_utc(dt_input[1]).timestamp())
        if s > e:
            raise TacoQueryError("Invalid range: start > end")
        return s, e

    raise TacoQueryError(
        f"Invalid datetime input: {dt_input}\n"
        f"Expected: string range, datetime object, or tuple of datetime objects"
    )