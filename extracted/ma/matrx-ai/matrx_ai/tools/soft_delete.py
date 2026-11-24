"""The ONE soft-delete primitive every tool delete path archives through.

Arman's law: soft-delete everything important — archive, never delete; a
person's data is never destroyed by an agent. A tool that "deletes" a row on a
table with a soft-delete column MUST set that column instead of removing the
row. The census of every delete-class tool action, and the guard that holds it,
live in ``matrx_ai.tools.delete_census``.

Column EXISTENCE on the generated model is the authority (the generator stamps
it from the live database) — never a flag that can drift.

Preference order, first present wins:
  ``deleted_at`` (timestamp) · ``is_deleted`` (bool) · ``archived_at`` (timestamp) · ``is_archived`` (bool)
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

SOFT_DELETE_COLUMNS: tuple[str, ...] = ("deleted_at", "is_deleted", "archived_at", "is_archived")


def soft_delete_column_in(names: Any) -> str | None:
    """The soft-delete column among ``names`` (an iterable of column names), or None."""
    present = set(names)
    for col in SOFT_DELETE_COLUMNS:
        if col in present:
            return col
    return None


def soft_delete_column(model: Any) -> str | None:
    """The soft-delete column of an ORM model class, or None when it has none."""
    fields = getattr(model, "_fields", None) or {}
    return soft_delete_column_in(fields.keys() if isinstance(fields, dict) else fields)


def is_flag(col: str) -> bool:
    return col.startswith("is_")


def archived_value(col: str) -> Any:
    """What the column holds once the row is archived."""
    return True if is_flag(col) else datetime.now(UTC)


def live_filter(col: str) -> dict[str, Any]:
    """The lookup that keeps only rows NOT archived through ``col``."""
    return {col: False} if is_flag(col) else {f"{col}__isnull": True}


def is_archived_row(row: dict[str, Any], col: str) -> bool:
    value = row.get(col)
    return bool(value) if is_flag(col) else value is not None


async def archive_where(model: Any, filters: dict[str, Any]) -> int:
    """Archive every LIVE row of ``model`` matching ``filters``; returns rows archived.

    A platform entity (a model with ``archive_where``) archives ``deleted_at`` through
    the entity's own archive, which works as the person on every table; anything else goes through the ORM's
    own ``update_where`` on the caller's connection. Rows already archived are left
    untouched, so their original archive time survives. Raises ValueError when
    the model has no soft-delete column — the caller decides, loudly, what to do.
    """
    col = soft_delete_column(model)
    if col is None:
        raise ValueError(f"{getattr(model, '__name__', model)!r} has no soft-delete column {SOFT_DELETE_COLUMNS}.")
    entity_archive = getattr(model, "archive_where", None)
    if col == "deleted_at" and callable(entity_archive):
        # A platform entity archives through its own archive_where: as the person (a tool's RLS
        # session) a table whose SELECT policy hides archived rows refuses an UPDATE of deleted_at
        # and the refusal aborts the whole transaction; archive_where falls back to
        # platform.entity_soft_delete there (matrx_orm.core.archive).
        return int(await entity_archive(filters))
    result = await model.update_where({**filters, **live_filter(col)}, **{col: archived_value(col)})
    return int(getattr(result, "rows_affected", 0) or 0)
