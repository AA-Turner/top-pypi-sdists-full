"""``dataset:delete_row`` on an older Data table ARCHIVES the row; it never removes it.

Arman's law (chair rule 2026-09-26): every tool delete archives through the table's
soft-delete column, and an archived row is restorable from /trash. ``workbench.udt_dataset_rows``
carries ``deleted_at``, so ``usertable_delete_row`` must stamp it through
``matrx_ai.tools.soft_delete.archive_where`` — scoped to the row, its table and its owner, and
only while the row is still live — and must never call a hard delete.

The model is a stand-in with the generated model's column shape: ``update_where`` records what it
was asked to write, ``delete_where`` fails the test if anything reaches it.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.db._registry as db_registry
from matrx_ai.tools.implementations import datasets_tools
from matrx_ai.tools.models import ToolContext

_TABLE_ID = "11111111-1111-4111-8111-111111111111"
_ROW_ID = "44444444-4444-4444-8444-444444444444"
_USER_ID = "33333333-3333-4333-8333-333333333333"


class _Ctx(ToolContext):
    @property
    def user_id(self) -> str:
        return _USER_ID


class _Rows:
    """The UdtDatasetRows columns that matter here, and a record of every write."""

    _fields = {"id": None, "table_id": None, "user_id": None, "data": None, "deleted_at": None}
    updates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    rows_affected = 1

    @classmethod
    async def update_where(cls, filters: dict[str, Any], **values: Any) -> Any:
        cls.updates.append((filters, values))
        return SimpleNamespace(rows_affected=cls.rows_affected)

    @classmethod
    async def delete_where(cls, **_: Any) -> int:
        raise AssertionError("usertable_delete_row removed the row — it must archive it")


@pytest.fixture(autouse=True)
def _older_table(monkeypatch):
    _Rows.updates = []
    _Rows.rows_affected = 1

    async def _not_moved(_table_id: str):
        return None  # an older table: the body under test, not the record-store arm

    monkeypatch.setattr(datasets_tools, "_moved", _not_moved)
    monkeypatch.setattr(
        db_registry, "get_model", lambda name: _Rows if name == "UdtDatasetRows" else None
    )


async def _delete() -> Any:
    return await datasets_tools.usertable_delete_row(
        {"table_id": _TABLE_ID, "row_id": _ROW_ID},
        _Ctx(call_id="call-1", tool_name="usertable_delete_row"),
    )


@pytest.mark.asyncio
async def test_delete_row_stamps_deleted_at_on_the_live_row_only():
    result = await _delete()

    assert result.success, result.error
    assert result.output == {"deleted_row_id": _ROW_ID, "archived": True}
    assert len(_Rows.updates) == 1, "exactly one archive write"
    filters, values = _Rows.updates[0]
    assert filters == {
        "id": _ROW_ID,
        "table_id": _TABLE_ID,
        "user_id": _USER_ID,
        "deleted_at__isnull": True,
    }, "the archive is scoped to this row, its table and its owner, and leaves an archived row alone"
    assert set(values) == {"deleted_at"} and values["deleted_at"] is not None


@pytest.mark.asyncio
async def test_nothing_live_to_archive_is_not_found():
    _Rows.rows_affected = 0

    result = await _delete()

    assert not result.success
    assert result.error.error_type == "not_found"
