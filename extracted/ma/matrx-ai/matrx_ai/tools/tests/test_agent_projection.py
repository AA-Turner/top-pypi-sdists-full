"""Phase E tests — AgentToolSpec projection.

Covers ``resolve_agent_specs`` (rewrites AgentToolSpec to RegisteredToolSpec
with opaque names + builds the projection map) and ``lookup_projected_tool``
(executor-side lookup that takes precedence over the global registry).
"""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from matrx_ai.tools.agent_projection import (
    PROJECTED_AGENT_TOOLS_KEY,
    lookup_projected_tool,
    resolve_agent_specs,
)
from matrx_ai.tools.models import ToolDefinition, ToolType
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


class _FakeAgentRow:
    def __init__(
        self,
        name: str = "Test agent",
        description: str = "",
        variable_definitions: list[dict[str, Any]] | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.variable_definitions = variable_definitions or []


@pytest.fixture
def fake_load_agent():
    """Patch the manager's load_by_id to return canned rows keyed by agent_id."""
    rows: dict[str, _FakeAgentRow] = {}

    async def _load(agent_id: str):
        if agent_id not in rows:
            raise ValueError(f"agent not found: {agent_id}")
        return rows[agent_id]

    with patch(
        "matrx_ai.db.agx_manager.agx_agent_manager_instance.load_by_id",
        new=AsyncMock(side_effect=_load),
    ), patch(
        "matrx_ai.db.agx_manager.agx_version_manager_instance.load_by_id",
        new=AsyncMock(side_effect=_load),
    ):
        yield rows


# ---------------------------------------------------------------------------
# resolve_agent_specs
# ---------------------------------------------------------------------------

class TestResolveAgentSpecs:
    async def test_no_agent_specs_passthrough(self, fake_load_agent) -> None:
        ctx = _make_ctx()
        specs = [
            RegisteredToolSpec(name="fs_read"),
            InlineToolSpec(name="weather", description="x"),
        ]
        rewritten, projections = await resolve_agent_specs(specs, ctx)
        assert rewritten == specs
        assert projections == {}

    async def test_single_agent_spec_projects_to_custom_tool_1(
        self, fake_load_agent
    ) -> None:
        fake_load_agent["abc-123"] = _FakeAgentRow(
            name="SEO keywords",
            description="Returns the best SEO keywords for a target audience.",
            variable_definitions=[
                {"name": "topic", "required": True, "helpText": "What to research"},
                {"name": "audience", "required": False, "helpText": "Target market"},
            ],
        )
        ctx = _make_ctx()
        rewritten, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="abc-123")], ctx
        )

        # The agent spec is replaced with an opaque RegisteredToolSpec.
        assert len(rewritten) == 1
        assert isinstance(rewritten[0], RegisteredToolSpec)
        assert rewritten[0].name == "custom_tool_1"

        # The projection map carries a synthetic ToolDefinition.
        assert "custom_tool_1" in projections
        dumped = projections["custom_tool_1"]
        assert dumped["tool_type"] == ToolType.AGENT.value
        assert dumped["function_path"] == "agent:abc-123"
        assert dumped["prompt_id"] == "abc-123"
        # Description comes from the agent record.
        assert "SEO keywords" in dumped["description"] or "best SEO" in dumped["description"]
        # Variables show up as JSON Schema-shaped parameters.
        assert "topic" in dumped["parameters"]
        assert dumped["parameters"]["topic"]["required"] is True

    async def test_multiple_agents_get_sequential_names(self, fake_load_agent) -> None:
        fake_load_agent["a-1"] = _FakeAgentRow(name="agent-A")
        fake_load_agent["b-2"] = _FakeAgentRow(name="agent-B")
        fake_load_agent["c-3"] = _FakeAgentRow(name="agent-C")
        ctx = _make_ctx()
        rewritten, projections = await resolve_agent_specs(
            [
                AgentToolSpec(agent_id="a-1"),
                AgentToolSpec(agent_id="b-2"),
                AgentToolSpec(agent_id="c-3"),
            ],
            ctx,
        )
        assert [s.name for s in rewritten] == [
            "custom_tool_1",
            "custom_tool_2",
            "custom_tool_3",
        ]
        assert projections["custom_tool_1"]["prompt_id"] == "a-1"
        assert projections["custom_tool_2"]["prompt_id"] == "b-2"
        assert projections["custom_tool_3"]["prompt_id"] == "c-3"

    async def test_duplicate_agent_id_dedupes(self, fake_load_agent) -> None:
        fake_load_agent["a-1"] = _FakeAgentRow(name="agent-A")
        ctx = _make_ctx()
        rewritten, projections = await resolve_agent_specs(
            [
                AgentToolSpec(agent_id="a-1"),
                AgentToolSpec(agent_id="a-1"),
            ],
            ctx,
        )
        # Both spec entries point to the same projected name.
        assert rewritten[0].name == "custom_tool_1"
        assert rewritten[1].name == "custom_tool_1"
        # Only one projection allocated.
        assert len(projections) == 1

    async def test_description_override_takes_precedence(self, fake_load_agent) -> None:
        fake_load_agent["a-1"] = _FakeAgentRow(
            name="Default name", description="Default description"
        )
        ctx = _make_ctx()
        _, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="a-1", description_override="My explicit description")],
            ctx,
        )
        assert projections["custom_tool_1"]["description"] == "My explicit description"

    async def test_agent_lookup_failure_raises_value_error(
        self, fake_load_agent
    ) -> None:
        ctx = _make_ctx()
        with pytest.raises(ValueError, match="resolution failed"):
            await resolve_agent_specs(
                [AgentToolSpec(agent_id="missing")], ctx
            )

    async def test_continues_existing_projection_indexing(
        self, fake_load_agent
    ) -> None:
        # When ctx.metadata already has a projection map (e.g. from a prior
        # merge call), new projections continue numbering from where it
        # left off, not start back at 1.
        fake_load_agent["a-1"] = _FakeAgentRow(name="agent-A")
        ctx = _make_ctx(metadata={
            PROJECTED_AGENT_TOOLS_KEY: {
                "custom_tool_1": {"prompt_id": "old", "name": "custom_tool_1"},
                "custom_tool_2": {"prompt_id": "older", "name": "custom_tool_2"},
            }
        })
        _, projections = await resolve_agent_specs(
            [AgentToolSpec(agent_id="a-1")], ctx
        )
        assert "custom_tool_3" in projections


# ---------------------------------------------------------------------------
# lookup_projected_tool — executor-side
# ---------------------------------------------------------------------------

class TestLookupProjectedTool:
    def test_returns_none_without_app_context(self) -> None:
        # Ensure no contextvar is set.
        from matrx_connect.context.app_context import _app_context

        sentinel = object()
        token = _app_context.set(None) if False else None
        # No active context — lookup is a safe no-op.
        result = lookup_projected_tool("custom_tool_1")
        assert result is None

    def test_returns_none_when_no_projections(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        ctx = _make_ctx(metadata={})
        token = set_app_context(ctx)
        try:
            assert lookup_projected_tool("custom_tool_1") is None
        finally:
            clear_app_context(token)

    def test_returns_tool_definition_when_projected(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        synthetic = ToolDefinition(
            name="custom_tool_1",
            description="Test agent",
            tool_type=ToolType.AGENT,
            function_path="agent:abc-123",
            prompt_id="abc-123",
        )
        ctx = _make_ctx(metadata={
            PROJECTED_AGENT_TOOLS_KEY: {
                "custom_tool_1": synthetic.model_dump(exclude={"_callable"}),
            }
        })
        token = set_app_context(ctx)
        try:
            result = lookup_projected_tool("custom_tool_1")
            assert result is not None
            assert result.name == "custom_tool_1"
            assert result.tool_type == ToolType.AGENT
            assert result.prompt_id == "abc-123"
        finally:
            clear_app_context(token)

    def test_returns_none_for_unknown_name(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        ctx = _make_ctx(metadata={
            PROJECTED_AGENT_TOOLS_KEY: {"custom_tool_1": {"name": "custom_tool_1"}},
        })
        token = set_app_context(ctx)
        try:
            assert lookup_projected_tool("custom_tool_999") is None
        finally:
            clear_app_context(token)
