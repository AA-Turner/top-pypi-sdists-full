"""A lean dispatcher row (``$envelope``) advertises ``action`` + one object, and still works.

2026-10-02: the ``records`` tool cost ~7,200 Anthropic tokens per run because a provider
was shown the flattened union of 25 actions' arguments. A row that declares
``"$envelope": "args"`` is shown only its root map (``action`` + ``args``); the executor
lifts ``args`` back into the flat call before the declared model validates it, so the
full per-action contract still decides — and a flat call keeps working.

These tests run the REAL executor pipeline on a small two-action tool. The red half
swaps the unwrap for a pass-through (in memory, no file touched) and requires that the
same envelope call is then refused — so the passing half is about the unwrap, not luck.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

import pytest
from pydantic import Field, RootModel

from matrx_ai.tools.declared import ToolArgs, tool
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType

TOOL = "envelope_probe_crew_log"


class _AddVisit(ToolArgs):
    action: Literal["add_visit"]
    patient: str = Field(description="Who was seen.")
    minutes: int = Field(default=45, description="Session length.")


class _ListVisits(ToolArgs):
    action: Literal["list_visits"]
    limit: int = Field(default=20, description="How many.")


class _ProbeArgs(
    RootModel[Annotated[_AddVisit | _ListVisits, Field(discriminator="action")]]
):
    pass


SEEN: list[dict[str, Any]] = []


@tool(name=TOOL, source_kind="native", args=_ProbeArgs)
async def envelope_probe_crew_log(args: dict[str, Any], ctx: Any) -> ToolResult:
    SEEN.append(dict(args))
    return ToolResult(success=True, output={"ok": True}, tool_name=TOOL, call_id=ctx.call_id)


def _definition(*, envelope: bool = True) -> ToolDefinition:
    variants = {
        "add_visit": {
            "patient": {"type": "string", "required": True, "description": "Who was seen."},
            "minutes": {"type": "integer", "default": 45, "description": "Session length."},
        },
        "list_visits": {"limit": {"type": "integer", "default": 20, "description": "How many."}},
    }
    params: dict[str, Any] = {
        "action": {"type": "string", "enum": ["add_visit", "list_visits"], "required": True},
        "$variants": variants,
    }
    if envelope:
        params["args"] = {"type": "object", "description": "That action's arguments."}
        params["$envelope"] = "args"
    return ToolDefinition(
        name=TOOL,
        description="Cedar Ridge visit log.",
        parameters=params,
        tool_type=ToolType.LOCAL,
        function_path=f"{__name__}.envelope_probe_crew_log",
    )


def test_the_provider_is_shown_the_root_and_the_contract_keeps_every_field() -> None:
    lean = _definition()
    for fmt in (lean.to_anthropic_format()["input_schema"], lean.to_mcp_format()["input_schema"]):
        assert set(fmt["properties"]) == {"action", "args"}
    assert set(lean.to_openai_format()["function"]["parameters"]["properties"]) == {"action", "args"}
    assert set(lean.to_google_format()["parameters"]["properties"]) == {"action", "args"}
    assert set(lean._build_json_schema(contract=True)["properties"]) == {
        "action",
        "patient",
        "minutes",
        "limit",
    }


def test_the_google_sdk_accepts_the_lean_declaration() -> None:
    from google.genai import types

    types.Tool(function_declarations=[_definition().to_google_format()])


def test_a_row_without_an_envelope_is_unchanged() -> None:
    flat = _definition(envelope=False)
    assert flat.args_envelope is None
    assert flat._build_json_schema() == flat._build_json_schema(contract=True)


def test_the_delegated_precheck_validates_the_unwrapped_call_per_action() -> None:
    from matrx_ai.tools.executor import _validate_against_declared_schema

    lean = _definition()
    assert _validate_against_declared_schema(lean, {"action": "add_visit", "patient": "R. Ortiz"}) is None
    refused = _validate_against_declared_schema(lean, {"action": "add_visit", "minutes": 30})
    assert refused and "patient" in refused


class _Silent:
    """Stands in for the execution logger: these tests are about arguments, not rows."""

    def prepare_metadata(self, *a: Any, **k: Any) -> None:
        return None

    def __getattr__(self, _name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


async def _run(monkeypatch: pytest.MonkeyPatch, arguments: dict[str, Any]) -> ToolResult:
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.persistence import queue_helpers
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.registry import ToolRegistry

    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    registry = ToolRegistry()
    registry.register(_definition())
    executor = ToolExecutor(registry=registry, execution_logger=_Silent())

    async def _dispatch(tool_def, args, ctx, *a: Any, **k: Any) -> ToolResult:
        # What the tool BODY would be handed — the pipeline up to here is real.
        return await envelope_probe_crew_log(args, ctx)

    monkeypatch.setattr(executor, "_dispatch", _dispatch)
    token = set_app_context(AppContext(emitter=None))
    try:
        _, result = await executor.execute(
            TOOL, arguments, ToolContext(call_id="envelope-1", tool_name=TOOL)
        )
    finally:
        clear_app_context(token)
    return result


async def test_an_envelope_call_runs_flat_through_the_executor(monkeypatch) -> None:
    SEEN.clear()
    result = await _run(
        monkeypatch, {"action": "add_visit", "args": {"patient": "R. Ortiz", "minutes": 30}}
    )
    assert result.success, result.error
    assert SEEN[-1] == {"action": "add_visit", "patient": "R. Ortiz", "minutes": 30}


async def test_a_flat_call_still_runs(monkeypatch) -> None:
    SEEN.clear()
    result = await _run(monkeypatch, {"action": "list_visits", "limit": 5})
    assert result.success, result.error
    assert SEEN[-1] == {"action": "list_visits", "limit": 5}


async def test_a_bad_envelope_call_is_refused_naming_the_fields(monkeypatch) -> None:
    result = await _run(monkeypatch, {"action": "add_visit", "args": {"patiant": "R. Ortiz"}})
    assert not result.success
    message = result.error.message
    assert "`add_visit` takes, inside `args`: minutes, patient" in message, message
    assert "required: patient" in message, message


async def test_red_without_the_unwrap_the_same_call_is_refused(monkeypatch) -> None:
    from matrx_ai.tools import _dispatch_util

    monkeypatch.setattr(_dispatch_util, "unwrap_args_envelope", lambda a, e: (a, None))
    SEEN.clear()
    result = await _run(
        monkeypatch, {"action": "add_visit", "args": {"patient": "R. Ortiz", "minutes": 30}}
    )
    assert not result.success and SEEN == []


async def test_a_double_envelope_is_refused_by_the_executor(monkeypatch) -> None:
    """RED before 2026-10-02: the executor lifted one `args`, the body lifted the second,
    and the call ran as if it had been sent once — silently."""
    SEEN.clear()
    result = await _run(
        monkeypatch, {"action": "add_visit", "args": {"args": {"patient": "R. Ortiz"}}}
    )
    assert not result.success and SEEN == []
    assert "holds another `args`" in result.error.message, result.error.message


async def test_browser_inline_merge_delegates_flat_arguments(monkeypatch) -> None:
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    import matrx_ai.capabilities.browser_dom as browser_dom
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.merge import merge_request_tools
    from matrx_ai.tools.models import ToolType
    from matrx_ai.tools.registry import ToolRegistry

    class Emitter:
        def __init__(self) -> None:
            self.delegated: list[dict[str, Any]] = []

        async def send_tool_event(self, event: Any) -> None:
            if event.event == "tool_delegated":
                self.delegated.append(event.data["arguments"])

        async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...

    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    registry = ToolRegistry.get_instance()
    registry.clear()
    definition = _definition()
    definition.tool_type = ToolType.EXTERNAL_HANDLER
    registry.load_from_definitions([definition])
    registry._bindings_by_tool = {TOOL: {"chrome-extension"}}
    browser_dom._specs_cache = None
    try:
        spec = browser_dom._build_auto_load_specs()[1]
        emitter = Emitter()
        ctx = AppContext(emitter=emitter, client_tools=[])
        config = UnifiedConfig(model="test-model", messages=[], tools=[], custom_tools=[])
        ctx = merge_request_tools(
            config, ctx, [spec], active_executors=frozenset({"chrome-extension"})
        )
        executor = ToolExecutor(registry=registry, execution_logger=_Silent())
        token = set_app_context(ctx)
        try:
            _, result = await executor.execute(
                TOOL,
                {"action": "add_visit", "args": {"patient": "R. Ortiz", "minutes": 30}},
                ToolContext(call_id="browser-envelope-1", tool_name=TOOL),
                client_tools=frozenset(ctx.client_tools or []),
            )
        finally:
            clear_app_context(token)
        assert emitter.delegated == [
            {"action": "add_visit", "patient": "R. Ortiz", "minutes": 30}
        ], (ctx.client_tools, result.error)
    finally:
        browser_dom._specs_cache = None
        registry.clear()
