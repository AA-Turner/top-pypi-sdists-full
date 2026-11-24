"""An agent's call by an OLD Matrx Local name lands on Matrx 2's op and returns its typed result.

The REAL executor pipeline runs a ``local_browser`` call whose definition is the live
``tool.definition`` row (read 2026-11-01: LOCAL, no function_path, bound only to ``matrx-local``).
aidream's local proxy is faked exactly as ``test_desktop_tools.py`` fakes it. Three computers:

* Matrx 2 bound (``local_machine``): the call is translated and sent as ``browser.call``.
* Matrx Local attached (the name is in ``client_tools``): it is delegated, the router untouched.
* Nothing attached: ``no_viable_executor``, as before.

The red half empties the router's table (in memory) and requires the Matrx 2 call to fail again.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.tools import _sandbox_proxy as proxy
from matrx_ai.tools.implementations import legacy_local
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType

pytestmark = pytest.mark.asyncio

BASE = "https://aidream.invalid/api/local-proxy/5b0c3a9e-8a51-4c2c-9d0e-1f2a3b4c5d6e"

#: The live local_browser row's contract (tool.definition 5703e56e-…, 2026-11-01), trimmed of descriptions.
LOCAL_BROWSER_PARAMETERS: dict[str, Any] = {
    "action": {
        "type": "string",
        "required": True,
        "enum": [
            "click",
            "close",
            "eval",
            "extract",
            "navigate",
            "screenshot",
            "tabs",
            "type_text",
        ],
    },
    "url": {"type": "string"},
    "text": {"type": "string"},
    "browser": {"type": "string"},
    "timeout": {"type": "integer", "default": 10, "minimum": 1, "maximum": 60},
    "selector": {"type": "string"},
    "wait_for": {"type": "string", "default": None},
    "attribute": {"type": "string", "default": None},
    "full_page": {"type": "boolean", "default": False},
    "tab_index": {"type": "integer", "default": None},
    "javascript": {"type": "string"},
    "tab_action": {"type": "string", "enum": ["list", "new", "close", "switch"], "default": "list"},
    "all_matches": {"type": "boolean", "default": False},
    "clear_first": {"type": "boolean", "default": True},
    "press_enter": {"type": "boolean", "default": False},
    "extract_type": {
        "type": "string",
        "enum": ["text", "html", "attribute", "value"],
        "default": "text",
    },
}


class _Silent:
    """Stands in for the execution logger: these tests are about routing, not rows."""

    def prepare_metadata(self, *a: Any, **k: Any) -> None:
        return None

    def __getattr__(self, _name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


def _aidream(monkeypatch: pytest.MonkeyPatch, body: Any) -> list[httpx.Request]:
    seen: list[httpx.Request] = []
    real = httpx.AsyncClient

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=body)

    monkeypatch.setattr(
        proxy.httpx, "AsyncClient", lambda **kw: real(transport=httpx.MockTransport(handler), **kw)
    )
    return seen


def _metadata(target_kind: str | None) -> dict[str, Any]:
    if target_kind is None:
        return {}
    return {
        "active_sandbox": {
            "sandbox_id": "mac-1",
            "base_url": BASE,
            "access_token": "user-jwt",
            "root_path": "/Users/person",
            "target_kind": target_kind,
            "device_id": "5b0c3a9e-8a51-4c2c-9d0e-1f2a3b4c5d6e",
        }
    }


async def _call(
    monkeypatch: pytest.MonkeyPatch,
    arguments: dict[str, Any],
    *,
    target_kind: str | None,
    client_tools: frozenset[str] | None = None,
) -> ToolResult:
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.registry import ToolRegistry

    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="local_browser",
            description="Matrx Local's browser.",
            parameters=LOCAL_BROWSER_PARAMETERS,
            tool_type=ToolType.LOCAL,
        )
    )
    executor = ToolExecutor(registry=registry, execution_logger=_Silent())
    token = set_app_context(
        AppContext(
            emitter=None,
            user_id="u",
            request_id="run-1",
            token="t",
            is_authenticated=True,
            metadata=_metadata(target_kind),
        )  # type: ignore[arg-type]
    )
    try:
        _, result = await executor.execute(
            "local_browser",
            arguments,
            ToolContext(call_id="legacy-1", tool_name="local_browser"),
            client_tools=client_tools,
        )
    finally:
        clear_app_context(token)
    return result


async def test_an_old_name_on_matrx2_lands_on_its_op_and_returns_the_typed_result(
    monkeypatch,
) -> None:
    tabs = {"tabs": [{"id": 7, "title": "Cedar Ridge Clinic", "url": "https://example.com/"}]}
    seen = _aidream(monkeypatch, {"client_instance": "ext_a", "result": tabs, "duration_ms": 9})
    result = await _call(monkeypatch, {"action": "tabs"}, target_kind="local_machine")
    assert result.success, result.error
    assert seen and seen[0].url.path.endswith("/op/browser.call")
    assert json.loads(seen[0].content) == {
        "tool": "list_open_tabs",
        "args": {},
        "timeout_ms": 120_000,
    }
    assert result.output["action"] == "tabs"
    assert result.output["result"] == tabs
    assert result.tool_name == "local_browser"
    assert any("ran as desktop_browser" in n for n in result.model_notices)


@pytest.mark.parametrize(
    ("old", "tool", "tool_args"),
    [
        (
            {"action": "navigate", "url": "https://example.com"},
            "navigate_active_tab",
            {"url": "https://example.com"},
        ),
        ({"action": "click", "selector": "#go"}, "click_element", {"selector": "#go"}),
        (
            {"action": "type_text", "selector": "#q", "text": "hi"},
            "type_into_element",
            {"selector": "#q", "text": "hi"},
        ),
        ({"action": "extract"}, "get_page_text", {"max_chars": 8000}),
        (
            {"action": "extract", "selector": "a", "attribute": "href", "all_matches": True},
            "query_elements",
            {"selector": "a", "limit": 50, "attributes": ["href"]},
        ),
        ({"action": "screenshot", "selector": "#go"}, "screenshot_region", {"selector": "#go"}),
        (
            {"action": "tabs", "tab_action": "new", "url": "https://example.com"},
            "open_new_tab",
            {"url": "https://example.com"},
        ),
    ],
)
async def test_each_carried_action_becomes_the_extension_tool_the_live_walk_proved(
    monkeypatch, old: dict[str, Any], tool: str, tool_args: dict[str, Any]
) -> None:
    seen = _aidream(
        monkeypatch, {"client_instance": "ext_a", "result": {"ok": True}, "duration_ms": 9}
    )
    result = await _call(monkeypatch, old, target_kind="local_machine")
    assert result.success, result.error
    sent = json.loads(seen[0].content)
    assert (sent["tool"], sent["args"]) == (tool, tool_args)


@pytest.mark.parametrize(
    ("old", "named"),
    [
        ({"action": "navigate", "url": "https://example.com", "wait_for": "#go"}, "wait_for"),
        (
            {"action": "type_text", "selector": "#q", "text": "hi", "press_enter": True},
            "press_enter",
        ),
        ({"action": "screenshot", "full_page": True}, "full_page"),
        ({"action": "eval", "javascript": "1+1"}, "eval"),
        ({"action": "tabs", "tab_action": "switch", "tab_index": 1}, "tab_action=switch"),
        ({"action": "close"}, "close"),
    ],
)
async def test_an_input_matrx2_cannot_take_in_one_call_is_refused_by_name(
    monkeypatch, old: dict[str, Any], named: str
) -> None:
    seen = _aidream(monkeypatch, {"result": {"ok": True}})
    result = await _call(monkeypatch, old, target_kind="local_machine")
    assert not result.success and seen == []
    assert named in result.error.message and "desktop_browser" in result.error.suggested_action


async def test_on_matrx_local_the_call_is_still_delegated(monkeypatch) -> None:
    from matrx_ai.tools.executor import ToolExecutor

    delegated: list[str] = []

    async def _delegate(self, tool_def, args, ctx, *a: Any, **k: Any) -> ToolResult:
        delegated.append(tool_def.name)
        return ToolResult(
            success=True, output={"delegated": True}, tool_name=tool_def.name, call_id=ctx.call_id
        )

    monkeypatch.setattr(ToolExecutor, "_execute_delegated", _delegate)
    seen = _aidream(monkeypatch, {"result": {"ok": True}})
    result = await _call(
        monkeypatch,
        {"action": "tabs"},
        target_kind="local_machine",
        client_tools=frozenset({"local_browser"}),
    )
    assert result.success and delegated == ["local_browser"] and seen == []


async def test_with_no_computer_attached_it_has_no_viable_executor(monkeypatch) -> None:
    result = await _call(monkeypatch, {"action": "tabs"}, target_kind=None)
    assert not result.success and result.error.error_type == "no_viable_executor"


async def test_red_without_the_router_the_matrx2_call_fails(monkeypatch) -> None:
    monkeypatch.setattr(legacy_local, "LEGACY_LOCAL_SUCCESSORS", {})
    seen = _aidream(monkeypatch, {"result": {"ok": True}})
    result = await _call(monkeypatch, {"action": "tabs"}, target_kind="local_machine")
    assert not result.success and seen == []
    assert result.error.error_type == "no_viable_executor"


def _merged_tools(target_kind: str | None, *, routed: bool = True) -> list[str]:
    """The tools the MODEL is handed for an agent listing local_browser (the merge's viability gate).

    The live failure this guards (2026-11-01): the dispatch edge could route local_browser, but the
    merge dropped it first ("needs one of ['matrx-local']"), so an agent on a Matrx 2 computer never
    saw the tool and called something else.
    """
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.tools.merge import merge_request_tools
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.load_from_definitions(
        [
            ToolDefinition(
                name="local_browser",
                description="Matrx Local's browser.",
                parameters=LOCAL_BROWSER_PARAMETERS,
                tool_type=ToolType.LOCAL,
                function_path="",
            )
        ]
    )
    registry._bindings_by_tool = {"local_browser": {"matrx-local"}}
    config = UnifiedConfig(model="test-model", messages=[], tools=["local_browser"])
    ctx = AppContext(emitter=None, client_tools=[], metadata=_metadata(target_kind))  # type: ignore[arg-type]
    saved = dict(legacy_local.LEGACY_LOCAL_SUCCESSORS)
    if not routed:
        legacy_local.LEGACY_LOCAL_SUCCESSORS.clear()
    try:
        merge_request_tools(config, ctx, [], active_executors=frozenset())
    finally:
        legacy_local.LEGACY_LOCAL_SUCCESSORS.update(saved)
        registry.clear()
    return list(config.tools)


async def test_the_model_is_handed_the_old_name_on_a_matrx2_computer() -> None:
    assert _merged_tools("local_machine") == ["local_browser"]


async def test_the_model_is_not_handed_the_old_name_with_no_computer_or_a_cloud_sandbox() -> None:
    assert _merged_tools(None) == []
    assert _merged_tools("sandbox") == []


async def test_red_without_the_router_the_merge_drops_the_old_name_again() -> None:
    assert _merged_tools("local_machine", routed=False) == []
