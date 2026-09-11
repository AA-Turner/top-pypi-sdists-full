"""Agent projection — saved agents as opaque ``custom_tool_N`` tools.

SUTs: ``resolve_agent_specs`` (AgentToolSpec → RegisteredToolSpec with opaque
names + the synthetic ToolDefinition map) and ``lookup_projected_tool`` (the
executor-side per-request lookup). The only doubles are the two DB managers'
``load_by_id`` — separate tables for agents and pinned versions, so routing a
load to the wrong table is observable.

Breaks these tests name:
* the agent's own description is ignored (model sees a generic label);
* a pinned version is loaded from the agents table (floating master runs);
* a floating and a pinned reference to the same id collapse into one tool;
* a projection already on the request is re-allocated instead of reused, or
  numbering restarts and clobbers it;
* the recursion ceiling / handoff inline mode / reference result params drop;
* lookup ignores the name, or the request's map, or returns a stale shape.
"""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from matrx_connect.context.app_context import clear_app_context, set_app_context

from matrx_ai.tools.agent_projection import (
    AUTO_INPUT_DESCRIPTION,
    PROJECTED_AGENT_TOOLS_KEY,
    lookup_projected_tool,
    resolve_agent_specs,
)
from matrx_ai.tools.models import ToolType
from matrx_ai.tools.specs import (
    AgentToolSpec,
    InlineToolSpec,
    RegisteredToolSpec,
)


class _NullEmitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


def _make_ctx(metadata: dict | None = None):
    from matrx_connect import AppContext

    return AppContext(emitter=_NullEmitter(), metadata=dict(metadata or {}))


class _AgentRow:
    """The columns ``resolve_agent_specs`` reads off an agx agent/version row."""

    def __init__(
        self,
        name: str,
        description: str = "",
        variable_definitions: list[dict[str, Any]] | None = None,
        output_schema: dict[str, Any] | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.variable_definitions = variable_definitions or []
        self.output_schema = output_schema


class _Tables:
    def __init__(self) -> None:
        self.agents: dict[str, _AgentRow] = {}
        self.versions: dict[str, _AgentRow] = {}


@pytest.fixture
def tables():
    t = _Tables()

    def _loader(table: dict[str, _AgentRow]):
        async def _load(agent_id: str) -> _AgentRow:
            if agent_id not in table:
                raise ValueError(f"row not found: {agent_id}")
            return table[agent_id]

        return AsyncMock(side_effect=_load)

    with patch(
        "matrx_ai.db.agx_manager.agx_agent_manager_instance.load_by_id",
        new=_loader(t.agents),
    ), patch(
        "matrx_ai.db.agx_manager.agx_version_manager_instance.load_by_id",
        new=_loader(t.versions),
    ):
        yield t


# ---------------------------------------------------------------------------
# resolve_agent_specs
# ---------------------------------------------------------------------------

class TestResolveAgentSpecs:
    async def test_no_agent_specs_passthrough(self, tables) -> None:
        ctx = _make_ctx()
        specs = [
            RegisteredToolSpec(name="fs_read"),
            InlineToolSpec(name="weather", description="x"),
        ]
        rewritten, projections = await resolve_agent_specs(specs, ctx)
        assert rewritten == specs
        assert projections == {}

    async def test_single_agent_spec_projects_to_custom_tool_1(self, tables) -> None:
        tables.agents["abc-123"] = _AgentRow(
            name="SEO keywords",
            description="Returns the best SEO keywords for a target audience.",
            variable_definitions=[
                {"name": "topic", "required": True, "helpText": "What to research"},
                {"name": "audience", "required": False, "helpText": "Target market"},
            ],
        )
        rewritten, projections = await resolve_agent_specs(
            [RegisteredToolSpec(name="fs_read"), AgentToolSpec(agent_id="abc-123")],
            _make_ctx(),
        )

        assert rewritten == [
            RegisteredToolSpec(name="fs_read"),
            RegisteredToolSpec(name="custom_tool_1"),
        ]
        assert list(projections) == ["custom_tool_1"]
        dumped = projections["custom_tool_1"]
        assert dumped["name"] == "custom_tool_1"
        assert dumped["tool_type"] == ToolType.AGENT.value
        assert dumped["function_path"] == "agent:abc-123"
        assert dumped["prompt_id"] == "abc-123"
        assert dumped["prompt_is_version"] is False
        assert dumped["description"] == "Returns the best SEO keywords for a target audience."
        assert dumped["max_recursion_depth"] == 2
        assert dumped["must_complete"] is True
        assert dumped["result_mode"] == "inline"
        assert dumped["handoff_terminal"] is False
        assert set(dumped["parameters"]) == {"input", "topic", "audience"}
        assert dumped["parameters"]["input"] == {
            "type": "string",
            "description": AUTO_INPUT_DESCRIPTION,
            "required": False,
        }
        assert dumped["parameters"]["topic"]["required"] is True
        assert dumped["parameters"]["topic"]["description"] == "What to research"
        assert dumped["parameters"]["audience"]["required"] is False

    async def test_agent_without_description_gets_named_fallback(self, tables) -> None:
        tables.agents["a-1"] = _AgentRow(name="Invoice extractor", description="")
        _, projections = await resolve_agent_specs([AgentToolSpec(agent_id="a-1")], _make_ctx())
        assert projections["custom_tool_1"]["description"] == "Specialised tool: Invoice extractor"

    async def test_description_override_takes_precedence(self, tables) -> None:
        tables.agents["a-1"] = _AgentRow(name="Default name", description="Default description")
        _, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="a-1", description_override="My explicit description")],
            _make_ctx(),
        )
        assert projections["custom_tool_1"]["description"] == "My explicit description"

    async def test_pinned_version_loads_from_the_versions_table(self, tables) -> None:
        tables.agents["shared-id"] = _AgentRow(name="Floating", description="floating master")
        tables.versions["shared-id"] = _AgentRow(name="Pinned", description="pinned v7")
        _, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="shared-id", is_version=True)], _make_ctx()
        )
        dumped = projections["custom_tool_1"]
        assert dumped["description"] == "pinned v7"
        assert dumped["prompt_is_version"] is True

    async def test_multiple_agents_get_sequential_names(self, tables) -> None:
        tables.agents["a-1"] = _AgentRow(name="agent-A")
        tables.agents["b-2"] = _AgentRow(name="agent-B")
        tables.agents["c-3"] = _AgentRow(name="agent-C")
        rewritten, projections = await resolve_agent_specs(
            [
                AgentToolSpec(agent_id="a-1"),
                AgentToolSpec(agent_id="b-2"),
                AgentToolSpec(agent_id="c-3"),
            ],
            _make_ctx(),
        )
        assert [s.name for s in rewritten] == ["custom_tool_1", "custom_tool_2", "custom_tool_3"]
        assert {k: v["prompt_id"] for k, v in projections.items()} == {
            "custom_tool_1": "a-1",
            "custom_tool_2": "b-2",
            "custom_tool_3": "c-3",
        }

    async def test_duplicate_agent_id_dedupes(self, tables) -> None:
        tables.agents["a-1"] = _AgentRow(name="agent-A")
        rewritten, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="a-1"), AgentToolSpec(agent_id="a-1")],
            _make_ctx(),
        )
        assert [s.name for s in rewritten] == ["custom_tool_1", "custom_tool_1"]
        assert list(projections) == ["custom_tool_1"]

    async def test_floating_and_pinned_references_to_one_id_are_distinct_tools(
        self, tables
    ) -> None:
        tables.agents["a-1"] = _AgentRow(name="agent-A", description="floating")
        tables.versions["a-1"] = _AgentRow(name="agent-A", description="pinned")
        rewritten, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="a-1"), AgentToolSpec(agent_id="a-1", is_version=True)],
            _make_ctx(),
        )
        assert [s.name for s in rewritten] == ["custom_tool_1", "custom_tool_2"]
        assert projections["custom_tool_1"]["description"] == "floating"
        assert projections["custom_tool_2"]["description"] == "pinned"

    async def test_agent_lookup_failure_raises_value_error(self, tables) -> None:
        with pytest.raises(
            ValueError,
            match=r"AgentToolSpec resolution failed for agent_id='missing' \(is_version=False\)",
        ):
            await resolve_agent_specs([AgentToolSpec(agent_id="missing")], _make_ctx())

    async def test_continues_existing_projection_indexing(self, tables) -> None:
        tables.agents["a-1"] = _AgentRow(name="agent-A")
        ctx = _make_ctx(metadata={
            PROJECTED_AGENT_TOOLS_KEY: {
                "custom_tool_1": {"prompt_id": "old", "name": "custom_tool_1"},
                "custom_tool_2": {"prompt_id": "older", "name": "custom_tool_2"},
            }
        })
        rewritten, projections = await resolve_agent_specs([AgentToolSpec(agent_id="a-1")], ctx)
        assert [s.name for s in rewritten] == ["custom_tool_3"]
        assert list(projections) == ["custom_tool_3"]

    async def test_agent_already_projected_on_the_request_is_reused(self, tables) -> None:
        tables.agents["a-1"] = _AgentRow(name="agent-A")
        ctx = _make_ctx(metadata={
            PROJECTED_AGENT_TOOLS_KEY: {
                "custom_tool_1": {"prompt_id": "a-1", "prompt_is_version": False},
            }
        })
        rewritten, projections = await resolve_agent_specs([AgentToolSpec(agent_id="a-1")], ctx)
        assert rewritten == [RegisteredToolSpec(name="custom_tool_1")]
        assert projections == {}

    async def test_declared_recursion_budget_overrides_the_default(self, tables) -> None:
        tables.agents["a-1"] = _AgentRow(name="agent-A")
        _, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="a-1", max_recursion_depth=5)], _make_ctx()
        )
        assert projections["custom_tool_1"]["max_recursion_depth"] == 5

    async def test_handoff_target_is_always_inline(self, tables) -> None:
        tables.agents["a-1"] = _AgentRow(name="agent-A")
        _, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="a-1", handoff=True, result_mode="reference")], _make_ctx()
        )
        dumped = projections["custom_tool_1"]
        assert dumped["handoff_terminal"] is True
        assert dumped["result_mode"] == "inline"

    async def test_reference_result_mode_adds_caller_naming_params(self, tables) -> None:
        tables.agents["a-1"] = _AgentRow(name="agent-A")
        _, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="a-1", result_mode="reference")], _make_ctx()
        )
        dumped = projections["custom_tool_1"]
        assert dumped["result_mode"] == "reference"
        assert set(dumped["parameters"]) == {"input", "result_key", "result_description"}
        assert dumped["parameters"]["result_key"]["required"] is False


# ---------------------------------------------------------------------------
# lookup_projected_tool — executor-side
# ---------------------------------------------------------------------------

class TestLookupProjectedTool:
    def test_returns_none_without_app_context(self) -> None:
        assert lookup_projected_tool("custom_tool_1") is None

    def test_returns_none_when_no_projections(self) -> None:
        token = set_app_context(_make_ctx(metadata={}))
        try:
            assert lookup_projected_tool("custom_tool_1") is None
        finally:
            clear_app_context(token)

    async def test_resolves_the_projection_resolve_agent_specs_stashed(self, tables) -> None:
        tables.agents["abc-123"] = _AgentRow(name="SEO keywords", description="SEO research")
        tables.agents["def-456"] = _AgentRow(name="Summarizer", description="Summaries")
        ctx = _make_ctx()
        _, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="abc-123"), AgentToolSpec(agent_id="def-456")], ctx
        )
        ctx.metadata[PROJECTED_AGENT_TOOLS_KEY] = projections

        token = set_app_context(ctx)
        try:
            second = lookup_projected_tool("custom_tool_2")
            first = lookup_projected_tool("custom_tool_1")
            unknown = lookup_projected_tool("custom_tool_999")
        finally:
            clear_app_context(token)

        assert second is not None and first is not None
        assert (second.name, second.tool_type, second.prompt_id, second.function_path) == (
            "custom_tool_2",
            ToolType.AGENT,
            "def-456",
            "agent:def-456",
        )
        assert (first.name, first.prompt_id, first.description) == (
            "custom_tool_1",
            "abc-123",
            "SEO research",
        )
        assert unknown is None
