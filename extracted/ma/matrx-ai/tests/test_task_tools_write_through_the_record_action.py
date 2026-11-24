"""The `task` and `project` tools write through the host's record Action, never around it.

A task's rules (a new task lands in the inbox or is planned; a timed task takes the person's zone;
completing a repeating task rolls it forward) live in the server's one record writer. A tool that
writes through its own manager skips every one of them and writes no action run. With the host's
``record_writer`` seam configured, every create / update / delete of a task or a project goes
through it; the manager only reads and writes the access columns the tool reconciles. Without the
seam (a CLIENT host) the manager writes, as before.

Each test fails if the tool writes the record around the seam: the manager's record-writing methods
raise, and the fake writer records exactly what reached it.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from unittest.mock import AsyncMock

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations import projects as projects_tool
from matrx_ai.tools.implementations.tasks import task_create, task_delete, task_update
from matrx_ai.tools.models import ToolContext
from matrx_ai.tools.record_writer import RecordWriteRefused

ORG = "11111111-1111-1111-1111-111111111111"
USER = "22222222-2222-2222-2222-222222222222"
TASK = "33333333-3333-3333-3333-333333333333"
PROJECT = "44444444-4444-4444-4444-444444444444"
ROW = {"id": TASK, "title": "Call the plumber", "status": "inbox", "version": 1, "organization_id": ORG}


def _around(*_a: Any, **_k: Any) -> Any:
    raise AssertionError("the tool wrote the record around the record Action")


class _Writer:
    """The host's record writer, faked: records each call and answers like the Action."""

    def __init__(self, refuse: RecordWriteRefused | None = None) -> None:
        self.calls: list[dict[str, Any]] = []
        self.refuse = refuse

    async def __call__(
        self, *, operation: str, noun: str, data: dict, organization_id: str | None = None, trusted: dict | None = None
    ):
        self.calls.append({"operation": operation, "noun": noun, "data": dict(data), "organization_id": organization_id})
        self.trusted = trusted
        if self.refuse is not None:
            raise self.refuse
        return None if operation == "delete" else {"id": data.get("id") or (TASK if noun == "task" else PROJECT), **data}


@pytest.fixture(autouse=True)
def _person() -> Any:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.tools.tests.test_agent_projection import _NullEmitter

    token = set_app_context(AppContext(emitter=_NullEmitter(), user_id=USER, organization_id=ORG))
    yield
    clear_app_context(token)


@pytest.fixture
def mgr(monkeypatch: pytest.MonkeyPatch) -> Any:
    from matrx_ai.db.content_types import tasks as tasks_mod

    class _Mgr:
        get_task = AsyncMock(return_value={"success": True, "task": dict(ROW)})
        update_task = AsyncMock(return_value={"success": True, "task": {**ROW, "version": 2}})
        create_task = AsyncMock(side_effect=_around)
        delete_task = AsyncMock(side_effect=_around)

    m = _Mgr()
    monkeypatch.setattr(tasks_mod, "tasks_manager_instance", m, raising=False)

    @asynccontextmanager
    async def _as_the_person(*_a: Any):
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _as_the_person)
    return m


def _wire(monkeypatch: pytest.MonkeyPatch, writer: _Writer) -> _Writer:
    monkeypatch.setitem(_ext._registry, "record_writer", writer)
    return writer


@pytest.mark.asyncio
async def test_a_created_task_is_one_write_through_task_create(mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    mgr.update_task.side_effect = _around
    writer = _wire(monkeypatch, _Writer())
    result = await task_create({"title": "Call the plumber", "shown_to": "my_team"}, ToolContext(call_id="c1"))
    assert result.success, result.error
    # ONE write: the Action's. The access the tool reconciled rides it as trusted columns.
    assert writer.calls == [
        {"operation": "create", "noun": "task", "data": {"title": "Call the plumber"}, "organization_id": ORG}
    ]
    assert writer.trusted["published_to_web"] is False
    assert writer.trusted["shown_to"] == "my_team"
    # The rule decides the starting status; the tool no longer sends the retired "incomplete".
    assert "status" not in writer.calls[0]["data"]
    mgr.update_task.assert_not_awaited()
    assert result.output["status"] == "inbox"


@pytest.mark.asyncio
async def test_an_updated_task_goes_through_task_update(mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    mgr.update_task.side_effect = _around
    writer = _wire(monkeypatch, _Writer())
    result = await task_update({"task_id": TASK, "status": "completed"}, ToolContext(call_id="c2"))
    assert result.success, result.error
    assert writer.calls == [
        {"operation": "update", "noun": "task", "data": {"status": "completed", "id": TASK}, "organization_id": None}
    ]
    mgr.update_task.assert_not_awaited()


@pytest.mark.asyncio
async def test_publishing_rides_the_same_update(mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    writer = _wire(monkeypatch, _Writer())
    mgr.get_task.return_value = {"success": True, "task": {**ROW, "published_to_web": True}}
    result = await task_update(
        {"task_id": TASK, "title": "Call the plumber today", "published_to_web": True}, ToolContext(call_id="c3")
    )
    assert result.success, result.error
    assert writer.calls[0]["data"] == {"title": "Call the plumber today", "id": TASK}
    assert writer.trusted["published_to_web"] is True
    mgr.update_task.assert_not_awaited()


@pytest.mark.asyncio
async def test_publishing_alone_is_one_write(mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    writer = _wire(monkeypatch, _Writer())
    result = await task_update({"task_id": TASK, "published_to_web": True}, ToolContext(call_id="c3b"))
    assert result.success, result.error
    assert writer.calls == []
    (access_call,) = mgr.update_task.await_args_list
    assert access_call.kwargs["published_to_web"] is True


@pytest.mark.asyncio
async def test_a_deleted_task_goes_through_task_delete(mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    writer = _wire(monkeypatch, _Writer())
    result = await task_delete({"task_id": TASK}, ToolContext(call_id="c4"))
    assert result.success, result.error
    assert writer.calls == [{"operation": "delete", "noun": "task", "data": {"id": TASK}, "organization_id": None}]
    assert result.output == {"deleted": True, "archived": True, "task_id": TASK, "previous_version": 1}


@pytest.mark.asyncio
async def test_a_task_the_person_sees_but_cannot_change_is_no_access(mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    _wire(monkeypatch, _Writer(refuse=RecordWriteRefused("task not found or not editable", error_type="not_found")))
    result = await task_update({"task_id": TASK, "title": "x"}, ToolContext(call_id="c5"))
    assert not result.success
    assert result.error.error_type == "no_access"


@pytest.mark.asyncio
async def test_a_rule_refusal_reaches_the_model_in_its_words(mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    words = "This task repeats on a rule that cannot be read (FREQ=NEVER), so it was not completed."
    _wire(monkeypatch, _Writer(refuse=RecordWriteRefused(words, error_type="validation")))
    result = await task_update({"task_id": TASK, "status": "completed"}, ToolContext(call_id="c6"))
    assert not result.success
    assert (result.error.error_type, result.error.message) == ("validation", words)


@pytest.mark.asyncio
async def test_a_client_host_without_the_seam_writes_through_its_manager(mgr: Any) -> None:
    assert _ext._registry.get("record_writer") is None
    mgr.create_task.side_effect = None
    mgr.create_task.return_value = {"success": True, "task": dict(ROW)}
    result = await task_create({"title": "Call the plumber"}, ToolContext(call_id="c7"))
    assert result.success, result.error
    assert "status" not in mgr.create_task.await_args.kwargs


# ── project ──────────────────────────────────────────────────────────────────

PROJECT_ROW = {"id": PROJECT, "name": "Kitchen", "status": "active", "version": 3, "organization_id": ORG}


@pytest.fixture
def project_mgr(monkeypatch: pytest.MonkeyPatch) -> Any:
    class _Mgr:
        get_project = AsyncMock(return_value={"success": True, "project": dict(PROJECT_ROW)})
        create_project = AsyncMock(side_effect=_around)
        update_project = AsyncMock(side_effect=_around)
        _unique_slug = AsyncMock(return_value="kitchen")

    m = _Mgr()
    monkeypatch.setattr(projects_tool, "_manager", lambda: m)

    @asynccontextmanager
    async def _as_the_person(*_a: Any):
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _as_the_person)
    return m


@pytest.mark.asyncio
async def test_a_created_project_goes_through_project_create(project_mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    writer = _wire(monkeypatch, _Writer())
    result = await projects_tool.project_create({"name": "Kitchen"}, ToolContext(call_id="p1"))
    assert result.success, result.error
    assert writer.calls == [
        {"operation": "create", "noun": "project", "data": {"name": "Kitchen", "slug": "kitchen"}, "organization_id": ORG}
    ]
    assert result.output["id"] == PROJECT


@pytest.mark.asyncio
async def test_an_updated_project_goes_through_project_update(project_mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    writer = _wire(monkeypatch, _Writer())
    result = await projects_tool.project_update({"project_id": PROJECT, "status": "completed"}, ToolContext(call_id="p2"))
    assert result.success, result.error
    assert writer.calls == [
        {"operation": "update", "noun": "project", "data": {"status": "completed", "id": PROJECT}, "organization_id": None}
    ]
    assert result.output["previous_version"] == 3
