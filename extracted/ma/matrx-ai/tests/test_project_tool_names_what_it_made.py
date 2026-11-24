"""The `project` tool: an agent can make and change a project, and the result names what the card needs.

Use case: a person asks the chat "set up a project for the spring launch with these six steps"; the agent
creates the project, then the tasks with ``project_id``. The turn's card strip reads ``id`` + ``name`` off
the create result (``@ai-matrx/tool-cards`` ``toolOutputs.ts``); a create with no carried organization is
refused, never written into a default one.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from unittest.mock import AsyncMock

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations.projects import project
from matrx_ai.tools.models import ToolContext

PID = "5b0c7a1e-2d3f-4a5b-9c6d-7e8f9a0b1c2d"
ORG = "11111111-2222-4333-8444-555555555555"
ROW = {"id": PID, "name": "Spring launch", "status": "active", "organization_id": ORG, "version": 1}


@pytest.fixture
def mgr(monkeypatch: pytest.MonkeyPatch) -> Any:
    from matrx_ai.db.content_types import projects as projects_mod

    class _Mgr:
        create_project = AsyncMock(return_value={"success": True, "project": dict(ROW)})
        update_project = AsyncMock(return_value={
            "success": True, "project": {**ROW, "status": "paused", "version": 2}, "prior": dict(ROW),
        })
        get_project = AsyncMock(return_value={"success": False, "error_type": "not_found", "error": f"Project {PID} was not found, or you do not have access to it."})

    m = _Mgr()
    monkeypatch.setattr(projects_mod, "projects_manager_instance", m, raising=False)

    @asynccontextmanager
    async def _as_the_person():
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _as_the_person)
    return m


@pytest.mark.asyncio
async def test_a_create_writes_into_the_carried_organization_and_names_the_project(
    mgr: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_ai.tools import organization_hold

    monkeypatch.setattr(organization_hold, "carried_organization_id", lambda ctx: ORG)
    result = await project({"action": "create", "name": "Spring launch"}, ToolContext(call_id="c1"))
    assert result.success, result.error
    assert result.tool_name == "project"
    assert result.output["id"] == PID and result.output["name"] == "Spring launch"
    assert mgr.create_project.await_args.kwargs["organization_id"] == ORG


@pytest.mark.asyncio
async def test_a_create_with_no_organization_is_refused(mgr: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.tools import organization_hold

    monkeypatch.setattr(organization_hold, "carried_organization_id", lambda ctx: None)
    result = await project({"action": "create", "name": "Spring launch"}, ToolContext(call_id="c2"))
    assert not result.success
    mgr.create_project.assert_not_awaited()


@pytest.mark.asyncio
async def test_an_update_names_the_version_it_replaced(mgr: Any) -> None:
    result = await project({"action": "update", "project_id": PID, "status": "paused"}, ToolContext(call_id="c3"))
    assert result.success, result.error
    assert result.output["previous_version"] == 1 and result.output["version"] == 2
    assert result.output["previous"] == {"status": "active"}


@pytest.mark.asyncio
async def test_an_unseen_project_answers_not_found_naming_it(mgr: Any) -> None:
    result = await project({"action": "get", "project_id": PID}, ToolContext(call_id="c4"))
    assert not result.success
    assert result.error.error_type == "not_found" and PID in result.error.message


@pytest.mark.asyncio
async def test_an_unknown_action_is_a_validation_error() -> None:
    result = await project({"action": "delete", "project_id": PID}, ToolContext(call_id="c5"))
    assert not result.success and result.error.error_type == "validation"
