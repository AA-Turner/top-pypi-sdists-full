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
    DesktopClipboardArgs,
    DesktopInputArgs,
    DesktopPowerArgs,
    DesktopProcessArgs,
    DesktopResourcesArgs,
    DesktopScreenArgs,
    DesktopSystemArgs,
    DesktopTranscribeArgs,
    DesktopWindowArgs,
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
