"""Run once per key: an agent step's ``result_version`` must move whenever its answer can.

Ruling 2026-10-26: what an agent row POINTS AT (its tools, its bindings, the source a following
copy runs) changes without the row's own version moving, so it is folded in; what resolves by
name or outside our database (prompt blocks, listed skills, MCP servers) refuses reuse.
Each test was red on the first build, which hashed only the row's own version.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db import _registry
from matrx_ai.graph_nodes import agent_action
from matrx_ai.tools import agent_projection

AGENT = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
SOURCE = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
TOOL = "cccccccc-cccc-4ccc-8ccc-cccccccccccc"


class _World:
    def __init__(self) -> None:
        self.rows: dict[str, Any] = {
            AGENT: SimpleNamespace(id=AGENT, version=3, updated_at="t3", tools=[TOOL], prompt_blocks=[],
                                   skill_config={}, mcp_servers=[], follows_source=False, source_agent_id=None),
            SOURCE: SimpleNamespace(id=SOURCE, version=7, updated_at="s7", tools=[TOOL], prompt_blocks=[],
                                    skill_config={}, mcp_servers=[], follows_source=False, source_agent_id=None),
        }
        self.tools = {TOOL: {"id": TOOL, "version": 1, "updated_at": "u1"}}
        self.assocs: list[Any] = []


@pytest.fixture
def world(monkeypatch) -> _World:
    w = _World()

    async def _resolve(inputs: Any, **kw: Any) -> Any:
        return SimpleNamespace(agent_id=AGENT, is_version=False, config_overrides={})

    async def _load(agent_id: str, *, is_version: bool) -> Any:
        return w.rows[agent_id]

    class _Q:
        def __init__(self, ids: list[str]) -> None:
            self.ids = ids

        async def values(self, *cols: str) -> list[dict[str, Any]]:
            return [dict(w.tools[i]) for i in self.ids if i in w.tools]

    class _ToolModel:
        @staticmethod
        def filter(id__in: list[str]) -> _Q:
            return _Q(id__in)

    class _Assoc:
        async def filter_items(self, **kw: Any) -> list[Any]:
            return [a for a in w.assocs if all(getattr(a, k) == v for k, v in kw.items())]

    monkeypatch.setattr(agent_action, "resolve_step_agent_full", _resolve)
    monkeypatch.setattr(agent_projection, "_load_agent_row", _load)
    monkeypatch.setattr(_registry, "get_model", lambda name: _ToolModel)
    monkeypatch.setattr(_registry, "get_instance", lambda name: _Assoc())
    return w


async def _version() -> str:
    return await agent_action.step_result_version(None, None, None)


async def test_a_tool_edit_moves_the_version(world):
    before = await _version()
    world.tools[TOOL]["updated_at"] = "u2"
    assert await _version() != before


async def test_a_new_binding_moves_the_version_and_a_tag_does_not(world):
    before = await _version()
    world.assocs.append(SimpleNamespace(id="t1", source_type="agent", source_id=AGENT, target_type="tag",
                                        target_id="x", role=None, version=1, updated_at="a", deleted_at=None))
    assert await _version() == before
    world.assocs.append(SimpleNamespace(id="a1", source_type="agent", source_id=AGENT, target_type="agent",
                                        target_id=SOURCE, role="member", version=1, updated_at="a", deleted_at=None))
    assert await _version() != before


async def test_a_following_copy_moves_with_its_source(world):
    world.rows[AGENT].follows_source = True
    world.rows[AGENT].source_agent_id = SOURCE
    before = await _version()
    world.rows[SOURCE].version = 8  # a fix to the platform agent the copy follows
    assert await _version() != before


async def test_what_has_no_version_refuses_reuse(world):
    world.rows[AGENT].prompt_blocks = [{"name": "house_rules"}]
    with pytest.raises(agent_action.StepAnswerUnversioned):
        await _version()
    world.rows[AGENT].prompt_blocks = []
    world.rows[AGENT].mcp_servers = ["srv"]
    with pytest.raises(agent_action.StepAnswerUnversioned):
        await _version()
