"""An old ``local_windows_ps`` call on a Matrx 2 computer runs as desktop_windows_admin / desktop_automation.

Same harness as test_legacy_local_routes_to_matrx2.py (the REAL executor, aidream's local proxy faked).
One test per mapped action (its op and params on the wire), one per refused input (named, nothing sent),
the pre-turn tool filter keeping the old name, and a red half that empties the router's table.
Action list = the live row's actions (apps/matrx-desktop/test/fixtures/legacy-contracts/local-tools.json).
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
ROW_ACTIONS = {
    "event_log", "get_env", "registry_read", "registry_write", "run",
    "service_control", "service_list", "set_env", "windows_features",
}  # fmt: skip
PARAMETERS: dict[str, Any] = {
    "action": {"type": "string", "required": True, "enum": sorted(ROW_ACTIONS)},
}


class _Silent:
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
            "sandbox_id": "pc-1",
            "base_url": BASE,
            "access_token": "user-jwt",
            "root_path": "C:\\Users\\person",
            "target_kind": target_kind,
            "device_id": "5b0c3a9e-8a51-4c2c-9d0e-1f2a3b4c5d6e",
        }
    }


async def _call(
    monkeypatch: pytest.MonkeyPatch, arguments: dict[str, Any], *, target_kind: str | None
) -> ToolResult:
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.registry import ToolRegistry

    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="local_windows_ps",
            description="Matrx Local's Windows administration.",
            parameters=PARAMETERS,
            tool_type=ToolType.LOCAL,
        )
    )
    executor = ToolExecutor(registry=registry, execution_logger=_Silent())
    token = set_app_context(
        AppContext(
            emitter=None, user_id="u", request_id="run-1", token="t", is_authenticated=True,
            metadata=_metadata(target_kind),
        )  # type: ignore[arg-type]
    )
    try:
        _, result = await executor.execute(
            "local_windows_ps", arguments,
            ToolContext(call_id="legacy-ps-1", tool_name="local_windows_ps"),
        )
    finally:
        clear_app_context(token)
    return result


MAPPED: list[tuple[dict[str, Any], str, dict[str, Any]]] = [
    (
        {"action": "run", "script": "Get-Date", "timeout": 20},
        "automation.script",
        {"language": "powershell", "script": "Get-Date", "timeout_s": 20},
    ),
    (
        {"action": "registry_read", "key_path": "HKCU:\\Software\\Example", "value_name": "V"},
        "windows.registry_read",
        {"key": "HKCU\\Software\\Example", "name": "V"},
    ),
    (
        {
            "action": "registry_write", "key_path": "HKCU:\\Software\\Example",
            "value_name": "V", "value": 5, "value_type": "DWord",
        },
        "windows.registry_write",
        {"key": "HKCU\\Software\\Example", "name": "V", "data": "5", "type": "REG_DWORD"},
    ),
    (
        {"action": "service_list", "filter": "spool", "status": "running"},
        "windows.services",
        {"filter": "spool", "status": "running"},
    ),
    (
        {"action": "service_control", "name": "Spooler", "service_action": "restart"},
        "windows.service_control",
        {"name": "Spooler", "action": "restart"},
    ),
    (
        {"action": "event_log", "log_name": "Application", "level": "Warning", "count": 5, "source": "X"},
        "windows.event_log",
        {"log": "Application", "levels": ["warning"], "limit": 5, "source": "X"},
    ),
    (
        {"action": "event_log"},  # Matrx Local's default filter was Error
        "windows.event_log",
        {"levels": ["error"]},
    ),
    (
        {"action": "event_log", "level": "All"},
        "windows.event_log",
        {},
    ),
    (
        {"action": "windows_features", "filter": "Hyper", "installed_only": True},
        "windows.features",
        {"filter": "Hyper", "installed_only": True},
    ),
]


@pytest.mark.parametrize(("old", "op", "params"), MAPPED, ids=[m[0]["action"] + str(i) for i, m in enumerate(MAPPED)])
async def test_each_mapped_action_lands_on_its_op_with_its_params(
    monkeypatch, old: dict[str, Any], op: str, params: dict[str, Any]
) -> None:
    seen = _aidream(monkeypatch, {"client_instance": "pc", "result": {"ok": True}, "duration_ms": 3})
    result = await _call(monkeypatch, old, target_kind="local_machine")
    assert result.success, result.error
    assert seen and seen[0].url.path.endswith(f"/op/{op}")
    sent = json.loads(seen[0].content)
    for k, v in params.items():
        assert sent.get(k) == v, (k, sent)
    if not params.get("levels"):
        assert "levels" not in sent or sent["levels"] is None
    assert result.tool_name == "local_windows_ps"
    expected = "desktop_automation" if op == "automation.script" else "desktop_windows_admin"
    assert any(f"ran as {expected}" in n for n in result.model_notices)


async def test_every_mapped_action_of_the_live_row_is_covered_or_refused() -> None:
    covered = {m[0]["action"] for m in MAPPED} | {r[0]["action"] for r in REFUSED}
    assert covered - {"reboot"} == ROW_ACTIONS


REFUSED: list[tuple[dict[str, Any], str]] = [
    ({"action": "get_env", "name": "PATH"}, "get_env"),
    ({"action": "set_env", "name": "X", "value": "1", "scope": "User"}, "set_env"),
    (
        {"action": "registry_write", "key_path": "HKCU:\\S", "value_name": "V", "value": "1", "value_type": "Nope"},
        "value_type=Nope",
    ),
    ({"action": "event_log", "level": "Verbose"}, "level=Verbose"),
    ({"action": "reboot"}, "no action 'reboot'"),
]


@pytest.mark.parametrize(("old", "named"), REFUSED, ids=[r[1] for r in REFUSED])
async def test_an_input_matrx2_cannot_take_is_refused_in_words_and_sends_nothing(
    monkeypatch, old: dict[str, Any], named: str
) -> None:
    seen = _aidream(monkeypatch, {"result": {"ok": True}})
    result = await _call(monkeypatch, old, target_kind="local_machine")
    assert not result.success and seen == []
    assert named in result.error.message
    assert "desktop_windows_admin" in result.error.suggested_action


async def test_red_without_the_router_the_matrx2_call_fails(monkeypatch) -> None:
    monkeypatch.setattr(legacy_local, "LEGACY_LOCAL_SUCCESSORS", {})
    seen = _aidream(monkeypatch, {"result": {"ok": True}})
    result = await _call(monkeypatch, {"action": "service_list"}, target_kind="local_machine")
    assert not result.success and seen == []
    assert result.error.error_type == "no_viable_executor"


def _merged_tools(target_kind: str | None, *, routed: bool = True) -> list[str]:
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.tools.merge import merge_request_tools
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.load_from_definitions(
        [
            ToolDefinition(
                name="local_windows_ps", description="Matrx Local's Windows administration.",
                parameters=PARAMETERS, tool_type=ToolType.LOCAL, function_path="",
            )
        ]
    )
    registry._bindings_by_tool = {"local_windows_ps": {"matrx-local"}}
    config = UnifiedConfig(model="test-model", messages=[], tools=["local_windows_ps"])
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


async def test_the_pre_turn_filter_keeps_the_old_name_on_a_matrx2_computer() -> None:
    assert _merged_tools("local_machine") == ["local_windows_ps"]


async def test_the_filter_drops_it_with_no_computer_or_a_cloud_sandbox() -> None:
    assert _merged_tools(None) == []
    assert _merged_tools("sandbox") == []


async def test_red_without_the_router_the_filter_drops_the_old_name() -> None:
    assert _merged_tools("local_machine", routed=False) == []
