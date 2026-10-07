"""A tool the caller names that cannot run is TOLD to the caller, never silently dropped.

Feedback 119846df: a run's replacement tool list named ``fetch_url_as_markdown`` (a
``tool.definition`` row with no implementation); the pre-flight gate removed it and the
run went on without it — the only trace was a server log line and a system_error row.
The caller must get a stream ``warning`` naming the tool, and the same for a name that
is not a known tool at all.
"""

from __future__ import annotations

import asyncio

import pytest
from matrx_connect.context.app_context import AppContext

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.tools import merge as merge_module
from matrx_ai.tools.merge import TOOLS_NOT_AVAILABLE_WARNING_CODE, merge_request_tools
from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry
from matrx_ai.tools.specs import RegisteredToolSpec


class _Recorder:
    def __init__(self) -> None:
        self.warnings: list = []

    async def send_warning(self, payload) -> None:  # noqa: ANN001
        self.warnings.append(payload)


def _registry() -> ToolRegistry:
    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.load_from_definitions(
        [
            ToolDefinition(
                name="no_impl_tool",
                description="fixture: a definition row with no implementation",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="",
            ),
            ToolDefinition(
                name="real_tool",
                description="fixture",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="os.path.join",
            ),
        ]
    )
    registry._bindings_by_tool = {}
    return registry


@pytest.fixture(autouse=True)
def _no_incident_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(merge_module, "_schedule_unrunnable_tool_configuration_capture", lambda **_: None)


@pytest.mark.asyncio
async def test_unimplemented_requested_tool_is_announced() -> None:
    _registry()
    emitter = _Recorder()
    config = UnifiedConfig(model="test-model", messages=[], tools=[])
    merge_request_tools(
        config,
        AppContext(emitter=emitter, client_tools=[]),
        [RegisteredToolSpec(name="no_impl_tool"), RegisteredToolSpec(name="real_tool")],
        active_executors=frozenset(),
    )
    await asyncio.sleep(0)
    await asyncio.sleep(0)

    assert "no_impl_tool" not in config.tools
    assert len(emitter.warnings) == 1
    warning = emitter.warnings[0]
    assert warning.code == TOOLS_NOT_AVAILABLE_WARNING_CODE
    assert warning.metadata["unrunnable"] == ["no_impl_tool"]
    assert "no_impl_tool" in (warning.user_message or "")


@pytest.mark.asyncio
async def test_unknown_requested_tool_is_announced() -> None:
    _registry()
    emitter = _Recorder()
    config = UnifiedConfig(model="test-model", messages=[], tools=[])
    merge_request_tools(
        config,
        AppContext(emitter=emitter, client_tools=[]),
        [RegisteredToolSpec(name="tool_that_does_not_exist"), RegisteredToolSpec(name="real_tool")],
        active_executors=frozenset(),
    )
    await asyncio.sleep(0)
    await asyncio.sleep(0)

    assert len(emitter.warnings) == 1
    assert emitter.warnings[0].metadata["unknown"] == ["tool_that_does_not_exist"]


@pytest.mark.asyncio
async def test_a_runnable_request_is_quiet() -> None:
    _registry()
    emitter = _Recorder()
    config = UnifiedConfig(model="test-model", messages=[], tools=[])
    merge_request_tools(
        config,
        AppContext(emitter=emitter, client_tools=[]),
        [RegisteredToolSpec(name="real_tool")],
        active_executors=frozenset(),
    )
    await asyncio.sleep(0)
    assert emitter.warnings == []
