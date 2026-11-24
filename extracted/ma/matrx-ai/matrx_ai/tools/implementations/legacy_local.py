"""Old ``local_*`` tool names, answered by Matrx 2's core when the person's computer runs Matrx 2.

Matrx Local's sidecar served the ``local_*`` dispatchers; Matrx 2 serves the same capabilities as
``desktop_*`` ops through the device relay. An agent that still lists an old name keeps working on
both kinds of computer through ONE router at the executor's dispatch edge:

* Matrx Local attached (the request declares ``desktop-native``): the call is delegated to it,
  exactly as before — delegation runs first and this module is never consulted.
* Matrx 2 attached (the run is bound to a ``local_machine`` target): the call is translated to its
  successor tool's arguments and run by that tool's own handler (``device_op`` → relay → core).
* Neither: the executor's ``no_viable_executor`` refusal stands.

Only dispatchers whose successor is PROVEN on every platform it ran on are translated (the gate is
``apps/matrx-desktop/test/unit/matrx-local-still-live.test.ts``). An old input the successor cannot
take in one call is refused by name, with the successor call that does it — never dropped.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import Any

from matrx_ai.tools._sandbox_proxy import get_active_sandbox, sandbox_binding_of
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

#: A translation: the successor's arguments, or the sentence saying what it cannot take.
Translation = dict[str, Any] | str


def _browser(args: dict[str, Any]) -> Translation:
    """local_browser (Matrx Local's Playwright browser) → desktop_browser (the person's own browser
    through the AI Matrx extension). The extension tools named in refusals are the ones
    ``apps/matrx-desktop/test/live/extension-matrx2-only-live.mjs`` proves carry each input."""
    action = args.get("action")
    selector = args.get("selector")
    if action == "navigate":
        if args.get("wait_for"):
            return (
                "wait_for is a second call on Matrx 2: navigate first, then call desktop_browser "
                "with action='call', tool='wait_for', tool_args={'condition': 'element', "
                "'target': <selector>}"
            )
        return {"action": "navigate", "url": args.get("url")}
    if action == "click":
        return {"action": "click", "selector": selector}
    if action == "type_text":
        if args.get("press_enter"):
            return (
                "press_enter is a second call on Matrx 2: type first, then call desktop_browser "
                "with action='call', tool='press_keys', tool_args={'keys': 'Enter'}"
            )
        if args.get("clear_first") is False:
            return "clear_first=false is not carried: desktop_browser's type replaces the field's value"
        return {"action": "type", "selector": selector, "text": args.get("text")}
    if action == "extract":
        extract_type = args.get("extract_type") or "text"
        if extract_type in ("html", "value"):
            return f"extract_type={extract_type} is not carried by desktop_browser"
        if not selector and extract_type == "text" and not args.get("all_matches"):
            return {"action": "read"}
        if not selector:
            return "extract with an attribute or all_matches needs a selector on Matrx 2"
        tool_args: dict[str, Any] = {
            "selector": selector,
            "limit": 50 if args.get("all_matches") else 1,
        }
        if args.get("attribute"):
            tool_args["attributes"] = [args["attribute"]]
        return {"action": "call", "tool": "query_elements", "tool_args": tool_args}
    if action == "screenshot":
        if args.get("full_page"):
            return "full_page is not carried: desktop_browser takes a picture of the visible tab"
        if selector:
            return {
                "action": "call",
                "tool": "screenshot_region",
                "tool_args": {"selector": selector},
            }
        return {"action": "screenshot"}
    if action == "tabs":
        tab_action = args.get("tab_action") or "list"
        if tab_action == "list":
            return {"action": "tabs"}
        if tab_action == "new":
            return {"action": "call", "tool": "open_new_tab", "tool_args": {"url": args.get("url")}}
        return (
            f"tab_action={tab_action} takes a tab id on Matrx 2, not an index: call desktop_browser "
            "with action='tabs', then action='close' with tab_ids or action='call', "
            "tool='switch_to_tab', tool_args={'tab_id': <id>}"
        )
    if action == "close":
        return (
            "close is not carried: Matrx 2 drives the person's own browser, which it never closes"
        )
    if action == "eval":
        return (
            "eval is not carried: the extension runs no page script for Matrx 2; use "
            "desktop_browser read, click or type"
        )
    return f"local_browser has no action {action!r}"


#: Matrx Local's registry value types (PowerShell's) → the registry's own names.
_REG_TYPES = {
    "String": "REG_SZ",
    "ExpandString": "REG_EXPAND_SZ",
    "MultiString": "REG_MULTI_SZ",
    "DWord": "REG_DWORD",
    "QWord": "REG_QWORD",
    "Binary": "REG_BINARY",
}
_EVENT_LEVELS = {
    "Critical": "critical",
    "Error": "error",
    "Warning": "warning",
    "Information": "information",
}


def _hive_key(key_path: Any) -> Any:
    """``HKCU:\\Software\\X`` (PowerShell's drive form) → ``HKCU\\Software\\X`` (reg.exe's)."""
    if isinstance(key_path, str):
        head, sep, rest = key_path.partition(":")
        if sep and head.upper() in {"HKLM", "HKCU", "HKCR", "HKU", "HKCC"}:
            return head + rest
    return key_path


def _windows_ps(args: dict[str, Any]) -> Translation:
    """local_windows_ps (Matrx Local's PowerShell dispatcher) → desktop_automation / desktop_windows_admin.

    The ``_tool`` key names the successor tool for this action (``run`` is desktop_automation, the
    rest are desktop_windows_admin). Mapping follows apps/matrx-desktop/test/unit/legacy-contract-parity
    .test.ts (PARITY) and the protocol's LEGACY_ACTIONS.
    """
    action = args.get("action")
    admin = "desktop_windows_admin"
    if action == "run":
        return {
            "_tool": "desktop_automation",
            "language": "powershell",
            "script": args.get("script"),
            "timeout_s": args.get("timeout"),
        }
    if action == "get_env":
        return "get_env is not carried: read an environment variable with shell_execute"
    if action == "set_env":
        return (
            "set_env is not carried: changing the person's persistent environment is not an agent "
            "tool; a per-command variable rides shell_execute"
        )
    if action == "registry_read":
        return {
            "_tool": admin,
            "action": "registry_read",
            "key": _hive_key(args.get("key_path")),
            "name": args.get("value_name"),
        }
    if action == "registry_write":
        value_type = args.get("value_type") or "String"
        if value_type not in _REG_TYPES:
            return f"value_type={value_type} is not one of {', '.join(sorted(_REG_TYPES))}"
        return {
            "_tool": admin,
            "action": "registry_write",
            "key": _hive_key(args.get("key_path")),
            "name": args.get("value_name"),
            "type": _REG_TYPES[value_type],
            "data": None if args.get("value") is None else str(args["value"]),
        }
    if action == "service_list":
        return {
            "_tool": admin,
            "action": "services",
            "filter": args.get("filter"),
            "status": args.get("status"),
        }
    if action == "service_control":
        return {
            "_tool": admin,
            "action": "service_control",
            "name": args.get("name"),
            "service_action": args.get("service_action"),
        }
    if action == "event_log":
        level = args.get("level") or "Error"  # Matrx Local's default filter was Error
        if level != "All" and level not in _EVENT_LEVELS:
            return f"level={level} is not one of All, {', '.join(_EVENT_LEVELS)}"
        return {
            "_tool": admin,
            "action": "event_log",
            "log": args.get("log_name"),
            "levels": None if level == "All" else [_EVENT_LEVELS[level]],
            "source": args.get("source"),
            "limit": args.get("count"),
        }
    if action == "windows_features":
        return {
            "_tool": admin,
            "action": "features",
            "filter": args.get("filter"),
            "installed_only": args.get("installed_only"),
        }
    return f"local_windows_ps has no action {action!r}"


async def _desktop_windows_ps(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools.implementations import desktop

    tool = args.pop("_tool")
    handler = desktop.desktop_automation if tool == "desktop_automation" else desktop.desktop_windows_admin
    return await handler(args, ctx)


async def _desktop_browser(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools.implementations.desktop import desktop_browser

    return await desktop_browser(args, ctx)


#: Old dispatcher → (successor tool, translator, successor handler). Add a dispatcher here only when
#: its successor is proven and every one of its inputs either translates or is refused by name.
LEGACY_LOCAL_SUCCESSORS: dict[
    str,
    tuple[
        str,
        Callable[[dict[str, Any]], Translation],
        Callable[[dict[str, Any], ToolContext], Awaitable[ToolResult]],
    ],
] = {
    "local_browser": ("desktop_browser", _browser, _desktop_browser),
    "local_windows_ps": ("desktop_windows_admin", _windows_ps, _desktop_windows_ps),
}


def routes_to_matrx2(tool_name: str, app_ctx: Any = None) -> bool:
    """True when this old name has a successor AND the run is bound to a Matrx 2 computer.

    ``app_ctx``: the context being built (the tool merge's viability gate, which must keep an old
    name the router will run, or the model never sees it); default the request's own context.
    """
    if tool_name not in LEGACY_LOCAL_SUCCESSORS:
        return False
    binding = get_active_sandbox() if app_ctx is None else sandbox_binding_of(app_ctx)
    return binding is not None and binding.target_kind == "local_machine"


async def run_on_matrx2(tool_name: str, args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Run an old ``local_*`` call as its Matrx 2 successor (caller checked ``routes_to_matrx2``)."""
    successor, translate, handler = LEGACY_LOCAL_SUCCESSORS[tool_name]
    started_at = time.time()
    translated = translate(dict(args or {}))
    if isinstance(translated, str):
        return ToolResult(
            success=False,
            error=ToolError(
                refusal=True,
                error_type="validation",
                message=f"{tool_name} on Matrx 2: {translated}.",
                suggested_action=f"Call {successor} directly; {tool_name} is its old name.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=ctx.call_id,
        )
    # A dispatcher with several successors names the one for this call in "_tool".
    successor = translated.get("_tool", successor)
    result = await handler({k: v for k, v in translated.items() if v is not None}, ctx)
    result.tool_name = tool_name
    result.model_notices.append(
        f"{tool_name} ran as {successor} on Matrx 2; call {successor} next time."
    )
    return result
