"""A tool that accepts a field shows it back — in the create result and in every read.

2026-11-18, stranger proof of the default assistant: the task tool saved ``due_time`` but its readback left it
out (and the create result left out ``due_date`` too), so both models told people a saved time had not saved.
These tests derive the accepted fields from the WIRE arg models themselves, so a field added to a write later is
covered without editing this file.
"""

from __future__ import annotations

import datetime as dt
from contextlib import asynccontextmanager
from typing import Any
from unittest.mock import AsyncMock

import pytest

from matrx_ai import _ext
from matrx_ai.tools.arg_models.dispatcher_args import (
    ProjectCreateWire,
    ProjectUpdateWire,
    TaskCreateWire,
    TaskUpdateWire,
)
from matrx_ai.tools.models import ToolContext

# Wire inputs that are not row fields: the dispatcher's action word, the target id, and ``because`` (the source
# pointer + the person's exact words, carried on the action run, never on the row). The access words
# (published_to_web, shown_to) are row fields and must be shown back like any other.
_NOT_A_FIELD = {"action", "task_id", "because"}

SAVED_TASK = {
    "id": "t1",
    "title": "Call the dentist",
    "description": "Ask about the cleaning",
    "status": "incomplete",
    "priority": "high",
    "due_date": dt.date(2026, 11, 20),
    "due_time": dt.time(15, 30),
    "project_id": "p1",
    "parent_task_id": "t0",
    "assignee_id": "u2",
    "published_to_web": False,
    "shown_to": "everyone",
    "organization_id": "org-1",
    "created_at": "2026-11-18T10:00:00Z",
    "updated_at": "2026-11-18T10:00:00Z",
    "version": 1,
}

SAVED_PROJECT = {
    "id": "p1",
    "name": "Move house",
    "description": "Everything for the move",
    "status": "active",
    "priority": "medium",
    "start_date": dt.date(2026, 11, 1),
    "target_date": dt.date(2026, 12, 1),
    "organization_id": "org-1",
    "created_at": "2026-11-18T10:00:00Z",
    "updated_at": "2026-11-18T10:00:00Z",
    "version": 1,
}


def _accepted(model: type) -> set[str]:
    return set(model.model_fields) - _NOT_A_FIELD


@pytest.fixture
def wired(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.db.content_types import tasks as tasks_mod

    class _Tasks:
        get_task = AsyncMock(return_value={"success": True, "task": dict(SAVED_TASK)})
        update_task = AsyncMock(return_value={"success": True, "task": {**SAVED_TASK, "version": 2}})
        create_task = AsyncMock(return_value={"success": True, "task": dict(SAVED_TASK)})
        list_tasks_for_project = AsyncMock(return_value={"success": True, "tasks": [dict(SAVED_TASK)]})

    class _Projects:
        create_project = AsyncMock(return_value={"success": True, "project": dict(SAVED_PROJECT)})
        update_project = AsyncMock(
            return_value={"success": True, "project": {**SAVED_PROJECT, "version": 2}, "prior": dict(SAVED_PROJECT)}
        )
        get_project = AsyncMock(return_value={"success": True, "project": dict(SAVED_PROJECT)})

    monkeypatch.setattr(tasks_mod, "tasks_manager_instance", _Tasks(), raising=False)
    from matrx_ai.tools.implementations import projects as projects_mod

    monkeypatch.setattr(projects_mod, "_manager", lambda: _Projects())
    monkeypatch.setattr(projects_mod, "_tasks_manager", lambda: _Tasks())
    monkeypatch.setattr(ToolContext, "organization_id", property(lambda self: "org-1"))

    @asynccontextmanager
    async def _as_the_person():
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _as_the_person)


def _shown(output: dict[str, Any], fields: set[str]) -> set[str]:
    return {f for f in fields if f not in output}


@pytest.mark.asyncio
async def test_task_create_shows_back_every_field_it_accepted(wired: None) -> None:
    from matrx_ai.tools.implementations.tasks import task_create

    result = await task_create({"title": "Call the dentist"}, ToolContext(call_id="c1"))
    assert result.success, result.error
    assert _shown(result.output, _accepted(TaskCreateWire)) == set()
    assert result.output["due_date"] == "2026-11-20"
    assert result.output["due_time"] == "15:30"


@pytest.mark.asyncio
async def test_task_get_shows_back_every_field_a_write_accepts(wired: None) -> None:
    from matrx_ai.tools.implementations.tasks import task_get

    result = await task_get({"task_id": "t1"}, ToolContext(call_id="c2"))
    assert result.success, result.error
    assert _shown(result.output, _accepted(TaskCreateWire) | _accepted(TaskUpdateWire)) == set()
    assert result.output["due_time"] == "15:30"


@pytest.mark.asyncio
async def test_task_update_shows_back_every_field_it_accepted(wired: None) -> None:
    from matrx_ai.tools.implementations.tasks import task_update

    result = await task_update({"task_id": "t1", "due_time": "15:30"}, ToolContext(call_id="c3"))
    assert result.success, result.error
    assert _shown(result.output, _accepted(TaskUpdateWire)) == set()
    assert result.output["due_time"] == "15:30"


@pytest.mark.asyncio
async def test_a_project_read_shows_each_task_due_time(wired: None) -> None:
    from matrx_ai.tools.implementations.projects import project_get

    result = await project_get({"project_id": "p1"}, ToolContext(call_id="c4"))
    assert result.success, result.error
    assert result.output["tasks"][0]["due_time"] == "15:30"


@pytest.mark.asyncio
async def test_project_writes_show_back_every_field_they_accepted(wired: None) -> None:
    from matrx_ai.tools.implementations.projects import project_create, project_update

    created = await project_create({"name": "Move house"}, ToolContext(call_id="c5"))
    assert created.success, created.error
    assert _shown(created.output, _accepted(ProjectCreateWire)) == set()
    updated = await project_update({"project_id": "p1", "name": "Move house"}, ToolContext(call_id="c6"))
    assert updated.success, updated.error
    assert _shown(updated.output, _accepted(ProjectUpdateWire) - {"project_id"}) == set()
