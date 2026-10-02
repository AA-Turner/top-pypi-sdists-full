"""A tool component saved by name is linked to its tool, and lives in the tool's organization.

Defect (2026-10-01): ``tool.ui`` is a component of ``tool.definition`` — its RLS read
(``std_select``) answers only through ``tool_id``. ``toolcomp_create_component`` given a
``tool_name`` alone wrote ``tool_id = NULL`` even when that tool exists, so the renderer
was invisible to every person outside the admin lane and chat always fell back to the
generic card (14 of 17 ``matrx-default/default`` renderers, ``memory`` among them). It
also stamped the request's active organization on a tool's child, which the DB trigger
``_1_refuse_foreign_org`` refuses once the parent is named.

Scenario: Riley, working in her own organization, asks her agent to give the platform's
``memory`` tool a card. A workflow emit card (no tool behind it) still saves unlinked in
her organization.
"""

from __future__ import annotations

import contextlib
from typing import Any

import pytest

SYSTEM_ORG = "39c38960-d30c-4840-b0c1-c9960de95582"
RILEY_ORG = "0a0a0a0a-0000-4000-8000-00000000b001"
MEMORY_TOOL = "3c121dff-1df9-47e7-9894-a5693e89a7d5"
CODE = "export default function MemoryCard({ data }) { return <div>{data.key}</div>; }"


class _Row:
    def __init__(self, **data: Any) -> None:
        self.__dict__.update(data)


class _Query:
    async def all(self) -> list[Any]:
        return []

    def limit(self, _n: int) -> _Query:
        return self


class FakeToolDefinition:
    rows = {
        MEMORY_TOOL: _Row(id=MEMORY_TOOL, name="memory", organization_id=SYSTEM_ORG, deleted_at=None),
    }

    async def get_or_none(self, use_cache: bool = True, **where: Any) -> _Row | None:
        for row in self.rows.values():
            if all(getattr(row, k) == v for k, v in where.items()):
                return row
        return None


class FakeToolUi:
    def __init__(self) -> None:
        self.created: list[dict[str, Any]] = []

    def filter(self, **_where: Any) -> _Query:
        return _Query()

    async def create_item(self, **payload: Any) -> _Row:
        self.created.append(payload)
        return _Row(id="c0de0000-0000-4000-8000-0000000000aa", created_at=None, **payload)


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai import _ext
    from matrx_ai.tools import models
    from matrx_ai.tools.implementations import tool_component

    ui = FakeToolUi()
    models_by_name = {"ToolDefinition": FakeToolDefinition(), "ToolUi": ui}
    monkeypatch.setattr(tool_component, "get_db_model", lambda name: models_by_name[name])
    monkeypatch.setattr(models.ToolContext, "organization_id", property(lambda self: RILEY_ORG))

    @contextlib.asynccontextmanager
    async def acting_as_caller():
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)
    return ui


def _ctx():
    from matrx_ai.tools.models import ToolContext

    return ToolContext(call_id="call-memory-card", tool_name="toolcomp_create_component")


@pytest.mark.asyncio
async def test_a_card_saved_by_tool_name_points_at_its_tool_and_its_tools_organization(world):
    from matrx_ai.tools.implementations.tool_component import toolcomp_create_component

    result = await toolcomp_create_component(
        {"tool_name": "memory", "display_name": "Memory", "inline_code": CODE}, _ctx()
    )

    assert result.success, result.error
    (row,) = world.created
    assert row["tool_id"] == MEMORY_TOOL
    assert row["organization_id"] == SYSTEM_ORG


@pytest.mark.asyncio
async def test_a_workflow_card_with_no_tool_behind_it_stays_unlinked_in_the_callers_organization(world):
    from matrx_ai.tools.implementations.tool_component import toolcomp_create_component

    result = await toolcomp_create_component(
        {
            "tool_name": "weekly_digest_card",
            "surface_name": "matrx-user/workflow",
            "display_name": "Weekly digest",
            "inline_code": CODE,
        },
        _ctx(),
    )

    assert result.success, result.error
    (row,) = world.created
    assert row["tool_id"] is None
    assert row["organization_id"] == RILEY_ORG
