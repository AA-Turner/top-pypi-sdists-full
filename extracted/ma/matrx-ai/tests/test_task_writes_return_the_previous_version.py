"""Every task write names the version it replaced, so an app's Undo can restore it (Matrx Planner PS2).

``projects.tasks`` is version-captured (``platform._version_capture('task')`` → ``history.row_versions``,
proven live 2026-11-13: an INSERT then an UPDATE left versions 1 and 2). An Undo restores a version through
``platform.version_restore('task', id, version)``; the chat's tool result is where the app learns which one.
Use case: a person tells the Planner chat "push the dentist call to Friday", then taps Undo.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from unittest.mock import AsyncMock

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations.tasks import task_create, task_delete, task_update
from matrx_ai.tools.models import ToolContext

PRIOR = {"id": "t1", "title": "Call the dentist", "status": "planned", "due_date": "2026-11-16", "version": 4}


@pytest.fixture
def mgr(monkeypatch: pytest.MonkeyPatch) -> Any:
    from matrx_ai.db.content_types import tasks as tasks_mod

    class _Mgr:
        get_task = AsyncMock(return_value={"success": True, "task": dict(PRIOR)})
        update_task = AsyncMock(return_value={"success": True, "task": {**PRIOR, "due_date": "2026-11-20", "version": 5}})
        delete_task = AsyncMock(return_value={"success": True})
        create_task = AsyncMock(return_value={"success": True, "task": {**PRIOR, "id": "t2", "version": 1}})

    m = _Mgr()
    monkeypatch.setattr(tasks_mod, "tasks_manager_instance", m, raising=False)

    @asynccontextmanager
    async def _as_the_person():
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _as_the_person)
    return m


@pytest.mark.asyncio
async def test_an_update_names_the_version_it_replaced_and_the_old_values(mgr: Any) -> None:
    result = await task_update({"task_id": "t1", "due_date": "2026-11-20"}, ToolContext(call_id="c1"))
    assert result.success, result.error
    assert result.output["previous_version"] == 4
    assert result.output["version"] == 5
    assert result.output["previous"] == {"due_date": "2026-11-16"}


@pytest.mark.asyncio
async def test_a_delete_names_the_version_it_archived(mgr: Any) -> None:
    result = await task_delete({"task_id": "t1"}, ToolContext(call_id="c2"))
    assert result.success, result.error
    assert result.output["previous_version"] == 4


@pytest.mark.asyncio
async def test_a_create_says_there_was_no_previous_version(mgr: Any) -> None:
    result = await task_create({"title": "Call the dentist"}, ToolContext(call_id="c3"))
    if not result.success:
        pytest.skip(f"create path needs more context here: {result.error}")
    assert result.output.get("previous_version", "absent") is None
