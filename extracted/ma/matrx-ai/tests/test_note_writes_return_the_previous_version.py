"""Every note write names the version it replaced, so an app's Undo can restore it (Matrx Planner PS2).

``workbench.notes`` is version-captured (``_history`` → ``history.row_versions``); Undo restores with
``platform.version_restore('note', id, previous_version)``. The receipts are the registered ``note_tool_result``
kind, whose schema declares ``version`` / ``previous_version`` / ``previous``.
Use case: a person tells the Planner chat "add the gate code to my Trip note", then taps Undo.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from unittest.mock import AsyncMock

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations.notes import note_delete, note_update
from matrx_ai.tools.kinds.personal_content import NoteToolResult
from matrx_ai.tools.models import ToolContext

PRIOR = {"id": "n1", "label": "Trip", "content": "Flight at 9", "home_scope_id": None, "version": 7}


@pytest.fixture
def mgr(monkeypatch: pytest.MonkeyPatch) -> Any:
    from matrx_ai.db.content_types import notes as notes_mod

    class _Mgr:
        get_note = AsyncMock(return_value={"success": True, "note": dict(PRIOR)})
        update_note = AsyncMock(
            return_value={"success": True, "note": {**PRIOR, "content": "Flight at 9. Gate code 4411", "version": 8}}
        )
        delete_note = AsyncMock(return_value={"success": True})

    m = _Mgr()
    monkeypatch.setattr(notes_mod, "notes_manager_instance", m, raising=False)

    @asynccontextmanager
    async def _as_the_person():
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _as_the_person)
    return m


@pytest.mark.asyncio
async def test_a_note_update_names_the_version_it_replaced(mgr: Any) -> None:
    result = await note_update({"note_id": "n1", "content": "Flight at 9. Gate code 4411"}, ToolContext(call_id="c1"))
    assert result.success, result.error
    assert result.output["previous_version"] == 7
    assert result.output["version"] == 8
    assert result.output["previous"] == {"content": "Flight at 9"}


@pytest.mark.asyncio
async def test_a_note_delete_names_the_version_it_archived(mgr: Any) -> None:
    result = await note_delete({"note_id": "n1"}, ToolContext(call_id="c2"))
    assert result.success, result.error
    assert result.output["previous_version"] == 7


def test_the_receipt_kind_declares_the_undo_keys() -> None:
    fields = NoteToolResult.model_fields
    assert {"version", "previous_version", "previous"} <= set(fields)
    NoteToolResult.model_validate({"deleted": True, "note_id": "n1", "previous_version": 7})
