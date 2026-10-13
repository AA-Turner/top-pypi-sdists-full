"""Matrx 2 desktop tools: capabilities that exist only on a person's own computer (SPEC §6, §10).

Each tool is ONE op of ``@ai-matrx/desktop-protocol``, sent through the conversation's
``local_machine`` binding: ``_sandbox_proxy.device_op`` → aidream ``POST /api/local-proxy/{device}/op/{cap.op}``
→ the device relay → Matrx 2's Router → the capability owner. Params and result are exactly the
op's schema (the tool ↔ op map is ``TOOL_CATALOG`` in the protocol package).
"""

from __future__ import annotations

import time
from typing import Any

from matrx_ai.tools._sandbox_proxy import (
    DEVICE_OP_MAX_SECONDS,
    SandboxProxyError,
    device_op,
    get_active_sandbox,
)
from matrx_ai.tools.arg_models.desktop_args import (
    DesktopAppsArgs,
    DesktopAudioArgs,
    DesktopAutomationArgs,
    DesktopBrowserArgs,
    DesktopCalendarArgs,
    DesktopClipboardArgs,
    DesktopContactsArgs,
    DesktopDocumentsArgs,
    DesktopEntitiesArgs,
    DesktopGitArgs,
    DesktopInputArgs,
    DesktopLocationArgs,
    DesktopMailArgs,
    DesktopMessagesArgs,
    DesktopNetArgs,
    DesktopNotesArgs,
    DesktopPhotosArgs,
    DesktopPowerArgs,
    DesktopProcessArgs,
    DesktopResourcesArgs,
    DesktopScheduleArgs,
    DesktopScreenArgs,
    DesktopSystemArgs,
    DesktopTranscribeArgs,
    DesktopWebArgs,
    DesktopWindowArgs,
    DesktopWindowsAdminArgs,
    FsWatchArgs,
    ShellJobArgs,
)
from matrx_ai.tools.implementations.filesystem import _proxy_error, _resolve_sandbox_path
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

#: The transcript's segments shown to the model (the full text is always returned).
SEGMENTS_SHOWN = 200


def _no_computer(tool: str, call_id: str, started_at: float) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="no_computer",
            message=f"{tool} runs on the user's computer, and no computer is connected to this conversation.",
            suggested_action="Ask the user to open Matrx 2 on their computer and connect it to this chat.",
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool,
        call_id=call_id,
    )


async def desktop_transcribe(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Speech to text with local Whisper on the user's computer (op ``models.transcribe``). The
    first use installs the speech runtime and the model there, which can take minutes."""
    started_at = time.time()
    parsed = DesktopTranscribeArgs(**args)
    binding = get_active_sandbox()
    if binding is None or binding.target_kind != "local_machine":
        return _no_computer("desktop_transcribe", ctx.call_id, started_at)
    try:
        params: dict[str, Any] = {
            "path": _resolve_sandbox_path(binding, parsed.path),
            "task": parsed.task,
        }
        if parsed.model is not None:
            params["model"] = parsed.model
        if parsed.language is not None:
            params["language"] = parsed.language
        result = await device_op(
            binding, "models.transcribe", params, timeout_s=DEVICE_OP_MAX_SECONDS
        )
    except SandboxProxyError as exc:
        return _proxy_error(
            exc, tool_name="desktop_transcribe", call_id=ctx.call_id, started_at=started_at
        )
    segments = result.get("segments") or []
    return ToolResult(
        success=True,
        output={
            "text": result.get("text", ""),
            "language": result.get("language"),
            "duration_s": result.get("duration_s"),
            "model": result.get("model"),
            "elapsed_ms": result.get("elapsed_ms"),
            "segments": segments[:SEGMENTS_SHOWN],
            "segments_total": len(segments),
            "path": params["path"],
        },
        started_at=started_at,
        completed_at=time.time(),
        tool_name="desktop_transcribe",
        call_id=ctx.call_id,
    )


def _invalid(tool: str, call_id: str, started_at: float, message: str) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="invalid_argument", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool,
        call_id=call_id,
    )


async def desktop_process(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Processes on the user's computer (ops ``proc.list``, ``proc.ports``, ``proc.kill``)."""
    started_at = time.time()
    parsed = DesktopProcessArgs(**args)
    binding = get_active_sandbox()
    if binding is None or binding.target_kind != "local_machine":
        return _no_computer("desktop_process", ctx.call_id, started_at)
    op: str
    params: dict[str, Any]
    if parsed.action == "list":
        op, params = "proc.list", {"sort": parsed.sort, "limit": parsed.limit}
        if parsed.name:
            params["name"] = parsed.name
    elif parsed.action == "ports":
        op, params = "proc.ports", ({"port": parsed.port} if parsed.port is not None else {})
    else:
        if parsed.pid is None:
            return _invalid(
                "desktop_process",
                ctx.call_id,
                started_at,
                "kill needs the pid (from list or ports)",
            )
        op, params = "proc.kill", {"pid": parsed.pid, "force": parsed.force}
    try:
        result = await device_op(binding, op, params, timeout_s=60)
    except SandboxProxyError as exc:
        return _proxy_error(
            exc, tool_name="desktop_process", call_id=ctx.call_id, started_at=started_at
        )
    return ToolResult(
        success=True,
        output={"action": parsed.action, **result},
        started_at=started_at,
        completed_at=time.time(),
        tool_name="desktop_process",
        call_id=ctx.call_id,
    )


async def desktop_clipboard(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The user's clipboard text (ops ``clipboard.read``, ``clipboard.write``)."""
    started_at = time.time()
    parsed = DesktopClipboardArgs(**args)
    binding = get_active_sandbox()
    if binding is None or binding.target_kind != "local_machine":
        return _no_computer("desktop_clipboard", ctx.call_id, started_at)
    if parsed.action == "write" and parsed.text is None:
        return _invalid("desktop_clipboard", ctx.call_id, started_at, "write needs the text")
    try:
        if parsed.action == "read":
            result = await device_op(binding, "clipboard.read", {}, timeout_s=30)
        else:
            result = await device_op(
                binding, "clipboard.write", {"text": parsed.text}, timeout_s=30
            )
    except SandboxProxyError as exc:
        return _proxy_error(
            exc, tool_name="desktop_clipboard", call_id=ctx.call_id, started_at=started_at
        )
    return ToolResult(
        success=True,
        output={"action": parsed.action, **result},
        started_at=started_at,
        completed_at=time.time(),
        tool_name="desktop_clipboard",
        call_id=ctx.call_id,
    )


# ── Group 2: computer control (one op per action; params exactly the op's schema) ───────────────


async def _call_ops(
    tool: str,
    ctx: ToolContext,
    started_at: float,
    plan: tuple[str, dict[str, Any], float] | str,
    *,
    action: str,
    shape: Any = None,
) -> ToolResult:
    """Send one planned op to the bound computer and wrap its result; ``plan`` is the op, its
    params and its timeout, or the refusal text when the arguments do not make a call."""
    binding = get_active_sandbox()
    if binding is None or binding.target_kind != "local_machine":
        return _no_computer(tool, ctx.call_id, started_at)
    if isinstance(plan, str):
        return _invalid(tool, ctx.call_id, started_at, plan)
    op, params, timeout_s = plan
    try:
        result = await device_op(binding, op, params, timeout_s=timeout_s)
    except SandboxProxyError as exc:
        return _proxy_error(exc, tool_name=tool, call_id=ctx.call_id, started_at=started_at)
    output: dict[str, Any] = {"action": action, **result}
    provider_content = None
    if shape is not None:
        output, provider_content = shape(output)
    return ToolResult(
        success=True,
        output=output,
        provider_content=provider_content,
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool,
        call_id=ctx.call_id,
    )


def _path(path: str) -> str:
    binding = get_active_sandbox()
    return _resolve_sandbox_path(binding, path) if binding is not None else path


async def shell_job(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Background commands on the user's computer (ops ``exec.job.*``)."""
    started_at = time.time()
    a = ShellJobArgs(**args)
    plan: tuple[str, dict[str, Any], float] | str
    if a.action == "start":
        if not a.command:
            plan = "start needs the command"
        else:
            params: dict[str, Any] = {"command": a.command}
            if a.cwd:
                params["cwd"] = _path(a.cwd)
            plan = ("exec.job.start", params, 60)
    elif a.action == "list":
        plan = ("exec.job.list", {}, 30)
    elif not a.job_id:
        plan = f"{a.action} needs the job_id (from start or list)"
    elif a.action == "output":
        plan = (
            "exec.job.output",
            {"job_id": a.job_id, "offset": a.offset, "wait_ms": a.wait_seconds * 1000},
            a.wait_seconds + 30,
        )
    else:
        plan = ("exec.job.stop", {"job_id": a.job_id, "force": a.force}, 30)
    return await _call_ops("shell_job", ctx, started_at, plan, action=a.action)


async def desktop_apps(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Apps on the user's computer (ops ``apps.list``, ``apps.open``)."""
    started_at = time.time()
    a = DesktopAppsArgs(**args)
    plan: tuple[str, dict[str, Any], float] | str
    if a.action == "list":
        plan = ("apps.list", {}, 30)
    elif not a.app_key:
        plan = "open needs the app_key (from list)"
    else:
        params: dict[str, Any] = {"app_key": a.app_key}
        if a.profile_id:
            params["profile_id"] = a.profile_id
        plan = ("apps.open", params, 60)
    return await _call_ops("desktop_apps", ctx, started_at, plan, action=a.action)


async def desktop_system(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The user's computer itself (ops ``sysinfo.get``, ``system.*``)."""
    started_at = time.time()
    a = DesktopSystemArgs(**args)
    plan: tuple[str, dict[str, Any], float] | str
    if a.action == "info":
        plan = ("sysinfo.get", {}, 30)
    elif a.action == "open_url":
        plan = ("system.open_url", {"url": a.url}, 30) if a.url else "open_url needs the url"
    elif a.action == "open_path":
        plan = (
            ("system.open_path", {"path": _path(a.path), "reveal": a.reveal}, 30)
            if a.path
            else "open_path needs the path"
        )
    else:
        plan = (
            ("system.notify", {"title": a.title, "body": a.body}, 30)
            if a.title
            else "notify needs a title"
        )
    return await _call_ops("desktop_system", ctx, started_at, plan, action=a.action)


def _screen_image(output: dict[str, Any]) -> tuple[dict[str, Any], Any]:
    """The picture goes to the model as an image; the stored output keeps only its facts."""
    from matrx_ai.config import ImageContent, TextContent

    data = output.pop("data_base64", None)
    if not data:
        return output, None
    output["size_bytes"] = len(data) * 3 // 4
    facts = (
        f"Screenshot of display {output.get('display_id')}: {output.get('width')}x{output.get('height')} "
        f"(display {output.get('source_width')}x{output.get('source_height')} pixels), {output.get('mime_type')}."
    )
    return output, [
        ImageContent(base64_data=data, mime_type=output.get("mime_type") or "image/jpeg"),
        TextContent(text=facts),
    ]


async def desktop_screen(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The user's displays and a picture of one (ops ``screen.list``, ``screen.capture``)."""
    started_at = time.time()
    a = DesktopScreenArgs(**args)
    if a.action == "list":
        return await _call_ops(
            "desktop_screen", ctx, started_at, ("screen.list", {}, 30), action="list"
        )
    params: dict[str, Any] = {"format": a.format, "max_width": a.max_width}
    if a.display_id is not None:
        params["display_id"] = a.display_id
    return await _call_ops(
        "desktop_screen",
        ctx,
        started_at,
        ("screen.capture", params, 60),
        action="capture",
        shape=_screen_image,
    )


async def desktop_window(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Windows on the user's screen (ops ``window.*``)."""
    started_at = time.time()
    a = DesktopWindowArgs(**args)
    plan: tuple[str, dict[str, Any], float] | str
    if a.action == "list":
        params: dict[str, Any] = {"limit": a.limit}
        if a.title:
            params["title"] = a.title
        plan = ("window.list", params, 30)
    elif a.id is None:
        plan = f"{a.action} needs the window id (from list)"
    elif a.action == "move":
        moved = {
            k: v
            for k, v in (("x", a.x), ("y", a.y), ("width", a.width), ("height", a.height))
            if v is not None
        }
        plan = (
            ("window.move", {"id": a.id, **moved}, 30)
            if moved
            else "move needs x and y, width and height, or both"
        )
    else:
        plan = (f"window.{a.action}", {"id": a.id}, 30)
    return await _call_ops("desktop_window", ctx, started_at, plan, action=a.action)


async def desktop_input(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The keyboard and mouse of the user's computer (ops ``input.*``)."""
    started_at = time.time()
    a = DesktopInputArgs(**args)
    plan: tuple[str, dict[str, Any], float] | str
    if a.action == "type_text":
        plan = ("input.type_text", {"text": a.text}, 120) if a.text else "type_text needs the text"
    elif a.action == "hotkey":
        plan = ("input.hotkey", {"keys": list(a.keys)}, 30) if a.keys else "hotkey needs the keys"
    elif a.action == "mouse_move":
        plan = (
            ("input.mouse_move", {"x": a.x, "y": a.y}, 30)
            if a.x is not None and a.y is not None
            else "mouse_move needs x and y"
        )
    elif (a.x is None) != (a.y is None):
        plan = "mouse_click needs both x and y, or neither to click where the pointer is"
    else:
        params: dict[str, Any] = {"button": a.button, "double": a.double}
        if a.x is not None and a.y is not None:
            params.update(x=a.x, y=a.y)
        plan = ("input.mouse_click", params, 30)
    return await _call_ops("desktop_input", ctx, started_at, plan, action=a.action)


async def desktop_power(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Battery and keeping the user's computer awake (ops ``power.*``)."""
    started_at = time.time()
    a = DesktopPowerArgs(**args)
    plan: tuple[str, dict[str, Any], float] | str
    if a.action == "status":
        plan = ("power.status", {}, 30)
    elif a.seconds is None:
        plan = "prevent_sleep needs seconds (0 lets it sleep again)"
    else:
        plan = ("power.prevent_sleep", {"seconds": a.seconds, "reason": a.reason}, 30)
    return await _call_ops("desktop_power", ctx, started_at, plan, action=a.action)


async def desktop_resources(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """CPU, memory and disks of the user's computer (op ``resources.snapshot``)."""
    started_at = time.time()
    a = DesktopResourcesArgs(**args)
    return await _call_ops(
        "desktop_resources", ctx, started_at, ("resources.snapshot", {}, 60), action=a.action
    )


async def fs_watch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Watch a folder on the user's computer (ops ``fs.watch.start/events/stop``)."""
    started_at = time.time()
    a = FsWatchArgs(**args)
    plan: tuple[str, dict[str, Any], float] | str
    if a.action == "start":
        if not a.path:
            plan = "start needs the folder path"
        else:
            params: dict[str, Any] = {"path": _path(a.path), "recursive": a.recursive}
            if a.ignore:
                params["ignore"] = list(a.ignore)
            plan = ("fs.watch.start", params, 30)
    elif not a.watch_id:
        plan = f"{a.action} needs the watch_id (from start)"
    elif a.action == "events":
        plan = (
            "fs.watch.events",
            {"watch_id": a.watch_id, "wait_ms": a.wait_seconds * 1000},
            a.wait_seconds + 30,
        )
    else:
        plan = ("fs.watch.stop", {"watch_id": a.watch_id}, 30)
    return await _call_ops("fs_watch", ctx, started_at, plan, action=a.action)


async def desktop_audio(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Microphones and speakers of the user's computer (ops ``audio.*``)."""
    started_at = time.time()
    a = DesktopAudioArgs(**args)
    plan: tuple[str, dict[str, Any], float] | str
    if a.action == "devices":
        plan = ("audio.devices", {}, 60)
    elif a.action == "record":
        if a.seconds is None:
            plan = "record needs seconds"
        else:
            params: dict[str, Any] = {"seconds": a.seconds}
            if a.device_id:
                params["device_id"] = a.device_id
            if a.path:
                params["path"] = _path(a.path)
            plan = ("audio.record", params, a.seconds + 90)
    else:
        plan = ("audio.play", {"path": _path(a.path)}, 660) if a.path else "play needs the path"
    return await _call_ops("desktop_audio", ctx, started_at, plan, action=a.action)


#: Network actions wait on a remote; the core gives git up to 600 s there.
_GIT_NETWORK_TIMEOUT_S = 660.0


def _git_plan(a: DesktopGitArgs) -> tuple[str, dict[str, Any], float] | str:
    """One desktop_git action as its ``git.*`` op (params exactly the op's schema)."""
    if a.action == "clone":
        if not a.url or not a.dest:
            return "clone needs the url and the dest folder"
        params: dict[str, Any] = {"url": a.url, "dest": _path(a.dest)}
        if a.branch:
            params["branch"] = a.branch
        if a.depth:
            params["depth"] = a.depth
        return ("git.clone", params, _GIT_NETWORK_TIMEOUT_S)
    if not a.cwd:
        return f"{a.action} needs cwd, the repository folder"
    cwd = _path(a.cwd)
    if a.action == "status":
        return ("git.status", {"cwd": cwd}, 150)
    if a.action == "diff":
        diff: dict[str, Any] = {"cwd": cwd, "staged": a.staged}
        if a.path:
            diff["path"] = a.path
        return ("git.diff", diff, 150)
    if a.action == "log":
        return ("git.log", {"cwd": cwd, "limit": a.limit}, 150)
    if a.action == "add":
        if not a.paths:
            return 'add needs paths (["."] stages everything)'
        return ("git.add", {"cwd": cwd, "paths": a.paths}, 150)
    if a.action == "commit":
        if not a.message:
            return "commit needs the message"
        return ("git.commit", {"cwd": cwd, "message": a.message, "amend": a.amend}, 150)
    if a.action in ("push", "pull"):
        net: dict[str, Any] = {"cwd": cwd, "remote": a.remote}
        if a.branch:
            net["branch"] = a.branch
        if a.action == "push":
            net["force_with_lease"] = a.force_with_lease
        else:
            net["rebase"] = a.rebase
        return (f"git.{a.action}", net, _GIT_NETWORK_TIMEOUT_S)
    if a.action == "branch":
        if a.branch_action != "list" and not a.name:
            return f"branch {a.branch_action} needs the name"
        br: dict[str, Any] = {"cwd": cwd, "action": a.branch_action}
        if a.name:
            br["name"] = a.name
        return ("git.branch", br, 150)
    stash: dict[str, Any] = {"cwd": cwd, "action": a.stash_action}
    if a.message and a.stash_action == "push":
        stash["message"] = a.message
    return ("git.stash", stash, 150)


async def desktop_git(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Git on the user's computer, through its own git (ops ``git.*``)."""
    started_at = time.time()
    a = DesktopGitArgs(**args)
    return await _call_ops("desktop_git", ctx, started_at, _git_plan(a), action=a.action)


#: A browser render can wait on the page and on the one shared browser; the core allows it 120 s.
_WEB_BROWSER_TIMEOUT_S = 200.0


def _web_land(organization_id: str | None) -> dict[str, Any]:
    """Where a page the agent reads is saved as a Source (the op's ``land``, protocol 1.40): the
    organization this conversation carries, never the computer's active one. With none carried the
    op names none, and the computer saves it where its person works (its active organization)."""
    if not organization_id:
        return {}
    return {"land": {"organization_id": organization_id, "keep": False, "attach_to": []}}


def _web_plan(
    a: DesktopWebArgs, organization_id: str | None = None
) -> tuple[str, dict[str, Any], float] | str:
    """One device-side desktop_web action as its ``web.*`` op (params exactly the op's schema)."""
    if a.action == "fetch":
        if not a.url:
            return "fetch needs the url"
        params: dict[str, Any] = {
            "url": a.url,
            "method": a.method,
            "headers": [{"name": k, "value": v} for k, v in (a.headers or {}).items()],
            "timeout_s": a.timeout_s,
        }
        if a.body is not None:
            params["body"] = a.body
        return ("web.fetch", params, a.timeout_s + 30)
    if a.action == "scrape":
        if not a.urls:
            return "scrape needs urls (1 to 20)"
        return (
            "web.scrape",
            {
                "urls": a.urls,
                "use_cache": a.use_cache,
                "get_links": a.get_links,
                **_web_land(organization_id),
            },
            300,
        )
    if not a.url:
        return "browser_fetch needs the url"
    browser: dict[str, Any] = {
        "url": a.url,
        "extract_text": a.extract_text,
        **_web_land(organization_id),
    }
    if a.wait_for:
        browser["wait_for"] = a.wait_for
    return ("web.fetch_with_browser", browser, _WEB_BROWSER_TIMEOUT_S)


async def desktop_web(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The web from the user's own computer (ops ``web.*``), and search through AI Matrx.

    fetch, scrape and browser_fetch run ON the computer: its IP, its connection. search never does:
    the computer holds no provider key, so it runs here, on the server's own search provider, as the
    person making this turn (the platform ``web_search`` tool, same context)."""
    started_at = time.time()
    a = DesktopWebArgs(**args)
    if a.action == "search":
        if not a.queries:
            return _invalid("desktop_web", ctx.call_id, started_at, "search needs queries (1 to 5)")
        from matrx_ai.tools.implementations.web import web_search

        query: dict[str, Any] = {"queries": a.queries[:5], "max_results_per_query": a.count}
        if a.freshness:
            query["freshness"] = a.freshness
        result = await web_search(query, ctx)
        result.tool_name = "desktop_web"
        return result
    from matrx_ai.tools.organization_hold import carried_organization_id

    plan = _web_plan(a, carried_organization_id(ctx))
    return await _call_ops("desktop_web", ctx, started_at, plan, action=a.action)


# ── The user's own browser, through Matrx 2 (cap browser: the AI Matrx extension paired with it) ──

#: desktop_browser action → the AI Matrx extension's own tool (matrx-extend src/lib/tools/handlers).
#: Read tools answer at once; action tools ask the person in the browser first (initiator
#: 'desktop'); the extension refuses its privileged tools from Matrx 2 (cdp_*, script injection).
BROWSER_ACTION_TOOLS: dict[str, str] = {
    "tabs": "list_open_tabs",
    "read": "get_page_text",
    "screenshot": "take_screenshot",
    "navigate": "navigate_active_tab",
    "click": "click_element",
    "type": "type_into_element",
    "close": "close_tab",
}

#: What the device may add on top of the person's wait (relay and core hops).
_BROWSER_HEADROOM_S = 30.0


def _browser_plan(a: DesktopBrowserArgs) -> tuple[str, dict[str, Any], float] | str:
    """One desktop_browser action as its ``browser.*`` op (params exactly the op's schema)."""
    if a.action == "sessions":
        return ("browser.sessions", {}, 30)
    if a.action == "call":
        if not a.tool:
            return "call needs tool: the extension tool's name"
        tool, args = a.tool, dict(a.tool_args or {})
    else:
        tool = BROWSER_ACTION_TOOLS[a.action]
        args = {}
        if a.action == "read":
            args = {"max_chars": a.max_chars}
        elif a.action == "screenshot":
            # The picture comes back to this turn; the extension keeps no copy of its own.
            args = {"persist": False}
        elif a.action == "navigate":
            if not a.url:
                return "navigate needs the url"
            args = {"url": a.url}
        elif a.action in ("click", "type"):
            if not a.selector and not a.ref:
                return f"{a.action} needs a selector or a ref (from read)"
            args = {"selector": a.selector} if a.selector else {"ref": a.ref}
            if a.action == "type":
                if a.text is None:
                    return "type needs the text"
                args["text"] = a.text
        elif a.action == "close":
            if not a.tab_ids:
                return "close needs tab_ids (from tabs)"
            args = {"tab_ids": a.tab_ids}
    params: dict[str, Any] = {"tool": tool, "args": args, "timeout_ms": a.timeout_s * 1000}
    if a.browser:
        params["client_instance"] = a.browser
    return ("browser.call", params, a.timeout_s + _BROWSER_HEADROOM_S)


def _browser_shape(output: dict[str, Any]) -> tuple[dict[str, Any], Any]:
    """A screenshot goes to the model as an image; a tool's own refusal stays in its words."""
    from matrx_ai.config import ImageContent, TextContent

    result = output.get("result")
    if not isinstance(result, dict):
        return output, None
    data = result.pop("image_base64", None)
    if not data:
        return output, None
    result["size_bytes"] = len(data) * 3 // 4
    facts = (
        f"Screenshot of the browser tab: {result.get('width')}x{result.get('height')} "
        f"({result.get('media_type') or 'image/jpeg'})."
    )
    return output, [
        ImageContent(base64_data=data, mime_type=result.get("media_type") or "image/jpeg"),
        TextContent(text=facts),
    ]


async def desktop_browser(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The user's own browser, through the AI Matrx extension connected to Matrx 2 (ops
    ``browser.sessions``, ``browser.call``). Only a browser signed in to the same AI Matrx account
    as Matrx 2 is ever driven; the person confirms every action in the browser."""
    started_at = time.time()
    a = DesktopBrowserArgs(**args)
    result = await _call_ops(
        "desktop_browser",
        ctx,
        started_at,
        _browser_plan(a),
        action=a.action,
        shape=_browser_shape,
    )
    # An extension tool that ran but could not do it ({ok: false, reason}) is a failure the model
    # must see as one, not a success carrying a refusal.
    inner = (
        result.output.get("result") if result.success and isinstance(result.output, dict) else None
    )
    if isinstance(inner, dict) and inner.get("ok") is False:
        reason = str(inner.get("reason") or inner.get("error") or "The browser could not do that")
        return ToolResult(
            success=False,
            error=ToolError(error_type="browser_refused", message=reason),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="desktop_browser",
            call_id=ctx.call_id,
        )
    return result


# ── Matrx Local's remaining tools (desktop-protocol 1.37): one op per action, table-driven ───────
#
# Each action names its op, the args that become the op's params (arg name → param name), the ones
# it cannot go without, and its timeout. Times arrive as ISO 8601 and travel as epoch ms; paths are
# resolved against the computer's home like every desktop tool's.


class _Act:
    __slots__ = ("op", "fields", "required", "timeout_s")

    def __init__(
        self,
        op: str,
        fields: dict[str, str] | tuple[str, ...] = (),
        required: tuple[str, ...] = (),
        timeout_s: float = 60,
    ) -> None:
        self.op = op
        self.fields = dict(fields) if isinstance(fields, dict) else {f: f for f in fields}
        self.required = required
        self.timeout_s = timeout_s


#: Args holding a time (ISO 8601 in, epoch ms out).
_TIME_ARGS = frozenset({"start", "end", "due", "since"})

SIDECAR_ACTIONS: dict[str, dict[str, _Act]] = {
    "desktop_net": {
        "info": _Act("net.info", timeout_s=40),
        "wifi": _Act("net.wifi", timeout_s=75),
        "bluetooth": _Act("net.bluetooth", timeout_s=75),
        "devices": _Act("net.devices", timeout_s=40),
        "mdns": _Act("net.mdns", ("service_type", "timeout_s"), timeout_s=60),
        "scan": _Act("net.scan", ("host", "ports", "allow_public"), ("host", "ports"), 300),
        "download": _Act(
            "net.download", ("url", "path", "overwrite", "timeout_s"), ("url", "path"), 3700
        ),
    },
    "desktop_automation": {
        "run": _Act(
            "automation.script", ("language", "script", "timeout_s"), ("language", "script"), 660
        ),
    },
    "desktop_mail": {
        "accounts": _Act("mail.accounts", timeout_s=90),
        "list": _Act("mail.list", ("account", "mailbox", "unread_only", "limit"), timeout_s=150),
        "send": _Act(
            "mail.send",
            {
                "to": "to",
                "cc": "cc",
                "subject": "subject",
                "body": "body",
                "sender": "from",
                "send": "send",
            },
            ("to", "subject", "body"),
            90,
        ),
    },
    "desktop_messages": {
        "chats": _Act("messages.chats", ("limit",), timeout_s=60),
        "list": _Act("messages.list", ("chat_id", "limit"), timeout_s=60),
        "send": _Act("messages.send", ("to", "text"), ("to", "text"), 90),
    },
    "desktop_contacts": {
        "search": _Act("contacts.search", ("query", "limit"), ("query",), 150),
        "get": _Act("contacts.get", ("id",), ("id",), 90),
    },
    "desktop_calendar": {
        "events": _Act(
            "calendar.list",
            {"start": "from_ms", "end": "to_ms", "calendar": "calendar", "limit": "limit"},
            ("start", "end"),
            150,
        ),
        "create_event": _Act(
            "calendar.create",
            {
                "title": "title",
                "start": "start_ms",
                "end": "end_ms",
                "all_day": "all_day",
                "calendar": "calendar",
                "location": "location",
                "notes": "notes",
            },
            ("title", "start", "end"),
            90,
        ),
        "reminders": _Act("reminders.list", ("list", "include_completed", "limit"), timeout_s=120),
        "create_reminder": _Act(
            "reminders.create",
            {"title": "title", "due": "due_ms", "list": "list", "notes": "notes"},
            ("title",),
            90,
        ),
    },
    "desktop_photos": {
        "search": _Act(
            "photos.search",
            {
                "query": "query",
                "start": "from_ms",
                "end": "to_ms",
                "favorites_only": "favorites_only",
                "limit": "limit",
            },
            timeout_s=150,
        ),
        "get": _Act("photos.get", ("id", "export"), ("id",), 210),
    },
    "desktop_location": {
        "get": _Act("location.get", ("timeout_s",), timeout_s=120),
    },
    "desktop_windows_admin": {
        "registry_read": _Act("windows.registry_read", ("key", "name"), ("key",), 90),
        "registry_write": _Act(
            "windows.registry_write", ("key", "name", "type", "data", "delete"), ("key", "name"), 90
        ),
        "services": _Act("windows.services", ("filter", "limit"), timeout_s=90),
        "service_control": _Act(
            "windows.service_control",
            {"name": "name", "service_action": "action"},
            ("name", "service_action"),
            120,
        ),
        "event_log": _Act(
            "windows.event_log",
            {"log": "log", "levels": "levels", "since": "since_ms", "limit": "limit"},
            timeout_s=120,
        ),
        "features": _Act("windows.features", ("filter",), timeout_s=150),
    },
    "desktop_notes": {
        "folders": _Act("notes.folders", timeout_s=60),
        "list": _Act("notes.list", ("folder", "limit"), timeout_s=60),
        "read": _Act("notes.read", ("path",), ("path",), 60),
        "write": _Act(
            "notes.write", ("folder", "label", "content", "if_hash"), ("label", "content"), 60
        ),
        "search": _Act("notes.search", ("query", "limit"), ("query",), 120),
    },
    "desktop_documents": {
        "pdf_text": _Act(
            "documents.pdf_text", ("path", "first_page", "last_page", "max_chars"), ("path",), 150
        ),
        "ocr": _Act("documents.ocr", ("path", "languages", "fast"), ("path",), 210),
        "image_resize": _Act(
            "documents.image_resize",
            ("path", "out_path", "max_size", "format", "overwrite"),
            ("path",),
            150,
        ),
        "office_generate": _Act(
            "documents.office_generate",
            ("kind", "path", "title", "paragraphs", "sheets", "overwrite"),
            ("kind", "path"),
            90,
        ),
    },
    "desktop_entities": {
        "names": _Act("entities.ner", ("text", "labels"), ("text",), 150),
        "private_data": _Act("entities.pii", ("text", "kinds", "redact"), ("text",), 60),
    },
}

#: The protocol param names whose values are file paths (args mapped onto them are resolved).
_PATH_PARAMS = frozenset({"path", "out_path"})
#: Tools whose `path` is relative to their own folder on the computer, never to its home.
_RELATIVE_PATH_TOOLS = frozenset({"desktop_notes"})


def _epoch_ms(value: str) -> int | None:
    """ISO 8601 (a date, or a date and time, with or without a zone: UTC when none) → epoch ms."""
    from datetime import UTC, datetime

    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return int(dt.timestamp() * 1000)


def _sidecar_plan(tool: str, action: str, a: Any) -> tuple[str, dict[str, Any], float] | str:
    """One action of a Matrx Local successor tool as its op, params exactly the op's schema."""
    spec = SIDECAR_ACTIONS[tool].get(action)
    if spec is None:
        return f"{tool} has no action {action}"
    missing = [f for f in spec.required if getattr(a, f, None) in (None, "", [])]
    if missing:
        return f"{action} needs {', '.join(missing)}"
    params: dict[str, Any] = {}
    for arg, param in spec.fields.items():
        value = getattr(a, arg, None)
        if value is None:
            continue
        if arg in _TIME_ARGS:
            ms = _epoch_ms(str(value))
            if ms is None:
                return f"{arg} must be an ISO 8601 date or time, such as 2026-10-12T09:00:00-07:00"
            value = ms
        elif param in _PATH_PARAMS and isinstance(value, str) and tool not in _RELATIVE_PATH_TOOLS:
            value = _path(value)
        params[param] = value
    return (spec.op, params, spec.timeout_s)


async def _sidecar(
    tool: str, model: Any, args: dict[str, Any], ctx: ToolContext, default_action: str | None = None
) -> ToolResult:
    started_at = time.time()
    a = model(**args)
    action = getattr(a, "action", None) or default_action or ""
    return await _call_ops(tool, ctx, started_at, _sidecar_plan(tool, action, a), action=action)


async def desktop_net(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The user's computer's network (ops ``net.*``): interfaces, Wi-Fi, Bluetooth, local devices,
    Bonjour, a port probe of a host on its network, downloads onto it."""
    return await _sidecar("desktop_net", DesktopNetArgs, args, ctx)


async def desktop_automation(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """A script in the computer's own automation language (op ``automation.script``)."""
    return await _sidecar(
        "desktop_automation", DesktopAutomationArgs, args, ctx, default_action="run"
    )


async def desktop_mail(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The Mail app on the user's Mac (ops ``mail.*``)."""
    return await _sidecar("desktop_mail", DesktopMailArgs, args, ctx)


async def desktop_messages(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The Messages app on the user's Mac (ops ``messages.*``)."""
    return await _sidecar("desktop_messages", DesktopMessagesArgs, args, ctx)


async def desktop_contacts(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Contacts on the user's Mac (ops ``contacts.*``)."""
    return await _sidecar("desktop_contacts", DesktopContactsArgs, args, ctx)


async def desktop_calendar(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Calendar and Reminders on the user's Mac (ops ``calendar.*``, ``reminders.*``)."""
    return await _sidecar("desktop_calendar", DesktopCalendarArgs, args, ctx)


async def desktop_photos(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The Photos library on the user's Mac (ops ``photos.*``)."""
    return await _sidecar("desktop_photos", DesktopPhotosArgs, args, ctx)


async def desktop_location(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Where the user's computer is (op ``location.get``)."""
    return await _sidecar("desktop_location", DesktopLocationArgs, args, ctx, default_action="get")


async def desktop_windows_admin(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Windows administration on the user's PC (ops ``windows.*``)."""
    return await _sidecar("desktop_windows_admin", DesktopWindowsAdminArgs, args, ctx)


async def desktop_notes(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """The user's local notes in Documents/Matrx/Notes (ops ``notes.*``)."""
    return await _sidecar("desktop_notes", DesktopNotesArgs, args, ctx)


async def desktop_documents(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """PDF text, OCR, images and Office files on the user's computer (ops ``documents.*``)."""
    return await _sidecar("desktop_documents", DesktopDocumentsArgs, args, ctx)


async def desktop_entities(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Names and private data in a text, found on the user's computer (ops ``entities.*``)."""
    return await _sidecar("desktop_entities", DesktopEntitiesArgs, args, ctx)


#: The tools desktop_schedule can put on an interval (their actions' plans, run by the device).
_SCHEDULABLE: dict[str, Any] = {
    "desktop_net": DesktopNetArgs,
    "desktop_notes": DesktopNotesArgs,
    "desktop_documents": DesktopDocumentsArgs,
    "desktop_entities": DesktopEntitiesArgs,
    "desktop_mail": DesktopMailArgs,
    "desktop_messages": DesktopMessagesArgs,
    "desktop_contacts": DesktopContactsArgs,
    "desktop_calendar": DesktopCalendarArgs,
    "desktop_photos": DesktopPhotosArgs,
    "desktop_location": DesktopLocationArgs,
    "desktop_automation": DesktopAutomationArgs,
    "desktop_windows_admin": DesktopWindowsAdminArgs,
}
_SCHEDULE_DEFAULT_ACTION = {"desktop_automation": "run", "desktop_location": "get"}


def _schedule_plan(a: DesktopScheduleArgs) -> tuple[str, dict[str, Any], float] | str:
    if a.action == "list":
        return ("schedule.list", {"include_finished": bool(a.include_finished)}, 30)
    if a.action == "cancel":
        return (
            ("schedule.cancel", {"id": a.id}, 30)
            if a.id
            else "cancel needs the id (from create or list)"
        )
    if not (a.name and a.tool and a.interval_s):
        return "create needs name, tool and interval_s"
    model = _SCHEDULABLE.get(a.tool)
    if model is None:
        return f"{a.tool} cannot be scheduled; one of: {', '.join(sorted(_SCHEDULABLE))}"
    try:
        inner = model(**(a.tool_args or {}))
    except Exception as exc:  # noqa: BLE001 - the model's own words go back to the agent
        return f"tool_args for {a.tool}: {str(exc)[:300]}"
    action = getattr(inner, "action", None) or _SCHEDULE_DEFAULT_ACTION.get(a.tool, "")
    plan = _sidecar_plan(a.tool, action, inner)
    if isinstance(plan, str):
        return plan
    op, params, _ = plan
    create: dict[str, Any] = {
        "name": a.name,
        "op": op,
        "params": params,
        "interval_s": a.interval_s,
        "run_now": bool(a.run_now),
    }
    if a.max_runs is not None:
        create["max_runs"] = a.max_runs
    return ("schedule.create", create, 60)


async def desktop_schedule(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Run a desktop tool's action on the user's computer on an interval (ops ``schedule.*``)."""
    started_at = time.time()
    a = DesktopScheduleArgs(**args)
    return await _call_ops("desktop_schedule", ctx, started_at, _schedule_plan(a), action=a.action)
