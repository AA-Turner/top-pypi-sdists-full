"""SQL WHERE clause and JOIN builders for navigation filters.

Pure functions — no side effects, no DuckDB execution.
Used by nav/filters.py for both simple (level=0) and cascade (level>0) filters.

Functions:
    build_bbox_where: Spatial ST_Intersects WHERE clause
    build_datetime_where: Temporal WHERE clause with TRY_CAST
    build_parent_child_join: Parent-child JOIN condition by format
"""

from datetime import datetime, timezone

from tacoreader._constants import (
    METADATA_CURRENT_ID,
    METADATA_PARENT_ID,
    METADATA_SOURCE_FILE,
)


def build_bbox_where(
    geometry_col: str,
    minx: float,
    miny: float,
    maxx: float,
    maxy: float,
) -> str:
    """Build spatial WHERE clause using ST_Intersects.

    Args:
        geometry_col: Name of WKB-encoded geometry column
        minx, miny, maxx, maxy: Bounding box coordinates

    Returns:
        SQL WHERE clause string (without WHERE keyword)

    Example:
        >>> build_bbox_where("istac:geometry", -10, 35, 5, 45)
        'ST_Intersects(ST_GeomFromWKB("istac:geometry"), ST_MakeEnvelope(-10.0, 35.0, 5.0, 45.0))'
    """
    return (
        f'ST_Intersects('
        f'ST_GeomFromWKB("{geometry_col}"), '
        f'ST_MakeEnvelope({float(minx)}, {float(miny)}, {float(maxx)}, {float(maxy)})'
        f')'
    )


def build_datetime_where(
    time_col: str,
    start_epoch: int,
    end_epoch: int | None,
) -> str:
    """Build temporal WHERE clause with TRY_CAST.

    Handles both TIMESTAMP and STRING date columns via TRY_CAST to DATE.

    Args:
        time_col: Name of time column
        start_epoch: Start timestamp as Unix epoch (seconds)
        end_epoch: End timestamp as Unix epoch (seconds), or None for point query

    Returns:
        SQL WHERE clause string (without WHERE keyword)
    """
    col_cast = f'TRY_CAST("{time_col}" AS DATE)'
    start_dt = datetime.fromtimestamp(start_epoch, tz=timezone.utc)
    start_str = start_dt.strftime("%Y-%m-%d")

    if end_epoch is None:
        return f"({col_cast} = DATE '{start_str}')"

    end_dt = datetime.fromtimestamp(end_epoch, tz=timezone.utc)
    end_str = end_dt.strftime("%Y-%m-%d")

    return f"({col_cast} BETWEEN DATE '{start_str}' AND DATE '{end_str}')"


def build_parent_child_join(
    format_type: str,
    parent_alias: str,
    child_alias: str,
) -> str:
    """Build parent-child JOIN condition based on dataset format.

    TacoCat requires additional source_file matching because consolidated
    datasets contain rows from multiple source ZIPs.

    Args:
        format_type: "zip", "folder", or "tacocat"
        parent_alias: SQL alias for parent table
        child_alias: SQL alias for child table

    Returns:
        SQL JOIN condition string (without ON keyword)

    Example:
        >>> build_parent_child_join("folder", "l0", "l1")
        'l1."internal:parent_id" = l0."internal:current_id"'
    """
    base = (
        f'{child_alias}."{METADATA_PARENT_ID}" = '
        f'{parent_alias}."{METADATA_CURRENT_ID}"'
    )

    if format_type == "tacocat":
        return (
            f'{base} AND '
            f'{child_alias}."{METADATA_SOURCE_FILE}" = '
            f'{parent_alias}."{METADATA_SOURCE_FILE}"'
        )

    return base