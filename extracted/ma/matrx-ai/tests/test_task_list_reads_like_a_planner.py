"""The ``task`` tool's list reads like a planner view (Matrx Planner chat, 2026-11-13).

Found live: asked "move everything from Friday to Monday", the Planner chat could not tell which tasks were due
Friday — the list returned only id/title/status/priority — and it showed project ids instead of names. A list now
carries each task's due date and time, priority, project id AND name and parent, and narrows to a day, a range or
overdue (``due_on`` / ``due_from`` / ``due_to`` / ``overdue_as_of``; a date filter leaves out finished tasks).
Splitting a task into steps makes sub-tasks (``parent_task_id``), which the description says.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from unittest.mock import AsyncMock

import pytest

from matrx_ai import _ext
from matrx_ai.tools.arg_models.dispatcher_args import TaskArgs
from matrx_ai.tools.implementations.tasks import task_list
from matrx_ai.tools.models import ToolContext

ROWS = [
    {"id": "t1", "title": "Ring Delphine", "status": "planned", "priority": "high", "project_id": None,
     "parent_task_id": None, "due_date": "2026-11-13", "due_time": "15:00:00"},
    {"id": "t2", "title": "Fix the header", "status": "planned", "priority": "medium", "project_id": "p1",
     "parent_task_id": None, "due_date": "2026-11-13", "due_time": None},
    {"id": "t3", "title": "Studio database decision", "status": "planned", "priority": "low", "project_id": "p2",
     "parent_task_id": None, "due_date": "2026-11-12", "due_time": None},
    {"id": "t4", "title": "Rain boots", "status": "planned", "priority": None, "project_id": None,
     "parent_task_id": None, "due_date": "2026-11-16", "due_time": "08:00:00"},
    {"id": "t5", "title": "Done already", "status": "completed", "priority": None, "project_id": None,
     "parent_task_id": None, "due_date": "2026-11-13", "due_time": None},
    {"id": "t6", "title": "No date", "status": "inbox", "priority": None, "project_id": None,
     "parent_task_id": None, "due_date": None, "due_time": None},
]


@pytest.fixture
def mgr(monkeypatch: pytest.MonkeyPatch) -> Any:
    from matrx_ai.db.content_types import tasks as tasks_mod

    class _Mgr:
        list_tasks_for_user = AsyncMock(return_value={"success": True, "tasks": [dict(r) for r in ROWS]})
        project_names = AsyncMock(return_value={"p1": "Website Relaunch", "p2": "Website Relaunch Three"})

    m = _Mgr()
    monkeypatch.setattr(tasks_mod, "tasks_manager_instance", m, raising=False)

    @asynccontextmanager
    async def _as_the_person():
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _as_the_person)
    return m


async def _ids(args: dict[str, Any]) -> list[str]:
    result = await task_list(args, ToolContext(call_id="c1"))
    assert result.success, result.error
    return [t["id"] for t in result.output["tasks"]]


@pytest.mark.asyncio
async def test_a_row_carries_dates_priority_project_name_and_parent(mgr: Any) -> None:
    result = await task_list({}, ToolContext(call_id="c1"))
    row = next(t for t in result.output["tasks"] if t["id"] == "t2")
    assert row == {"id": "t2", "title": "Fix the header", "status": "planned", "priority": "medium",
                   "due_date": "2026-11-13", "due_time": None, "project_id": "p1",
                   "project_name": "Website Relaunch", "parent_task_id": None}
    assert next(t for t in result.output["tasks"] if t["id"] == "t1")["due_time"] == "15:00"


@pytest.mark.asyncio
async def test_one_day_leaves_out_finished_tasks(mgr: Any) -> None:
    assert await _ids({"due_on": "2026-11-13"}) == ["t1", "t2"]


@pytest.mark.asyncio
async def test_a_range_and_overdue(mgr: Any) -> None:
    assert await _ids({"due_from": "2026-11-13", "due_to": "2026-11-16"}) == ["t1", "t2", "t4"]
    assert await _ids({"overdue_as_of": "2026-11-13"}) == ["t3"]


@pytest.mark.asyncio
async def test_a_bad_date_is_refused_by_name(mgr: Any) -> None:
    result = await task_list({"due_on": "Friday"}, ToolContext(call_id="c1"))
    assert not result.success and "due_on" in result.error.message


def test_the_wire_accepts_the_filters_and_a_due_time() -> None:
    TaskArgs.model_validate({"action": "list", "due_on": "2026-11-13"})
    TaskArgs.model_validate({"action": "list", "overdue_as_of": "2026-11-13", "due_from": "2026-11-01"})
    TaskArgs.model_validate({"action": "create", "title": "x", "due_time": "15:30", "parent_task_id": "t1"})
    TaskArgs.model_validate({"action": "update", "task_id": "t1", "due_time": "09:00"})
