"""Arguments of the Matrx 2 desktop tools (ops of ``@ai-matrx/desktop-protocol``).

Each field mirrors the op's params schema; the tool's ``tool.definition.parameters`` row is this
model, held equal by the drift gate and by test_desktop_tools.py.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from matrx_ai.tools.declared import ToolArgs


class DesktopTranscribeArgs(ToolArgs):
    path: str = Field(
        description="The audio or video file on the user's computer (absolute, or relative to its home folder)."
    )
    model: Literal["tiny", "base", "small", "large-v3-turbo"] | None = Field(
        default=None,
        description="Whisper size: tiny is fastest, large-v3-turbo most accurate. Omit for the computer's default.",
    )
    language: str | None = Field(
        default=None,
        description="Spoken language as an ISO 639-1 code such as en or es. Omit to detect it.",
    )
    task: Literal["transcribe", "translate"] = Field(
        default="transcribe",
        description="transcribe keeps the spoken language; translate writes English.",
    )


class DesktopProcessArgs(ToolArgs):
    action: Literal["list", "ports", "kill"] = Field(
        description="list: running processes; ports: listening ports and the process on each; kill: stop one by pid.",
    )
    name: str | None = Field(
        default=None,
        description="list: only processes whose name or command line contains this text.",
    )
    sort: Literal["cpu", "memory", "pid", "name"] = Field(
        default="cpu", description="list: order, busiest first for cpu and memory."
    )
    limit: int = Field(default=25, ge=1, le=200, description="list: at most this many processes.")
    port: int | None = Field(default=None, ge=1, le=65535, description="ports: only this port.")
    pid: int | None = Field(
        default=None, ge=1, description="kill: the process id, from list or ports."
    )
    force: bool = Field(
        default=False,
        description="kill: end it at once instead of asking it to quit (it cannot save its work).",
    )


class DesktopClipboardArgs(ToolArgs):
    action: Literal["read", "write"] = Field(
        description="read: the clipboard's text; write: replace the clipboard's text."
    )
    text: str | None = Field(default=None, description="write: the text to put on the clipboard.")


class ShellJobArgs(ToolArgs):
    action: Literal["start", "output", "stop", "list"] = Field(
        description=(
            "start: run a command in the background (a dev server, a long build) and get its job_id; "
            "output: read what it printed since `offset`; stop: end it; list: every job."
        ),
    )
    command: str | None = Field(default=None, description="start: the shell command.")
    cwd: str | None = Field(
        default=None,
        description="start: the folder it runs in (absolute, or relative to the home folder).",
    )
    job_id: str | None = Field(
        default=None, description="output, stop: the job (from start or list)."
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="output: read from this byte (next_offset of the last read; 0 = from the start).",
    )
    wait_seconds: int = Field(
        default=0,
        ge=0,
        le=25,
        description="output: wait up to this long for new output or the exit when none is waiting.",
    )
    force: bool = Field(
        default=False, description="stop: end it at once instead of asking it to quit."
    )


class DesktopAppsArgs(ToolArgs):
    action: Literal["list", "open"] = Field(
        description="list: the apps Matrx 2 knows and whether each is installed; open: open one or bring it forward.",
    )
    app_key: str | None = Field(default=None, description="open: the app (its app_key from list).")
    profile_id: str | None = Field(
        default=None,
        description="open: one of the app's saved profiles (from list); the default profile when omitted.",
    )


class DesktopSystemArgs(ToolArgs):
    action: Literal["info", "open_url", "open_path", "notify"] = Field(
        description=(
            "info: the computer (OS, user, folders, CPU, memory, battery); open_url: open a link in the "
            "default browser or mail app; open_path: open a file or folder with its default app; notify: "
            "show a notification."
        ),
    )
    url: str | None = Field(default=None, description="open_url: an http, https or mailto link.")
    path: str | None = Field(
        default=None,
        description="open_path: the file or folder (absolute, or relative to the home folder).",
    )
    reveal: bool = Field(
        default=False, description="open_path: show it in Finder or Explorer instead of opening it."
    )
    title: str | None = Field(default=None, description="notify: the notification's title.")
    body: str = Field(default="", description="notify: the notification's text.")


class DesktopScreenArgs(ToolArgs):
    action: Literal["list", "capture"] = Field(
        description="list: the displays; capture: a picture of one display (you see the image).",
    )
    display_id: int | None = Field(
        default=None,
        ge=0,
        description="capture: the display (from list); the main display when omitted.",
    )
    format: Literal["jpeg", "png"] = Field(
        default="jpeg", description="capture: jpeg is smaller; png is exact."
    )
    max_width: int = Field(
        default=1600,
        ge=160,
        le=7680,
        description="capture: scale the picture down to at most this many pixels wide.",
    )


class DesktopWindowArgs(ToolArgs):
    action: Literal["list", "focus", "move", "minimize"] = Field(
        description="list: open windows; focus: bring one to the front; move: move or resize one; minimize: minimize one.",
    )
    title: str | None = Field(
        default=None, description="list: only windows whose title contains this text."
    )
    id: int | None = Field(
        default=None, ge=0, description="focus, move, minimize: the window (its id from list)."
    )
    x: int | None = Field(default=None, description="move: new left edge, in screen points.")
    y: int | None = Field(default=None, description="move: new top edge, in screen points.")
    width: int | None = Field(
        default=None, ge=50, le=16384, description="move: new width, in points."
    )
    height: int | None = Field(
        default=None, ge=50, le=16384, description="move: new height, in points."
    )
    limit: int = Field(default=50, ge=1, le=500, description="list: at most this many windows.")


InputKeyName = Literal[
    "cmd", "ctrl", "alt", "shift", "meta",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
    "enter", "tab", "escape", "space", "backspace", "delete",
    "up", "down", "left", "right", "home", "end", "pageup", "pagedown",
    "minus", "equal", "comma", "period", "slash", "semicolon", "quote", "bracketleft", "bracketright", "backslash", "grave",
]  # fmt: skip


class DesktopInputArgs(ToolArgs):
    action: Literal["type_text", "hotkey", "mouse_move", "mouse_click"] = Field(
        description=(
            "type_text: type text into whatever has focus; hotkey: press keys together (cmd is Command on a "
            "Mac, Ctrl elsewhere); mouse_move: move the pointer; mouse_click: click (at x, y when given)."
        ),
    )
    text: str | None = Field(default=None, description="type_text: the text to type.")
    keys: list[InputKeyName] | None = Field(
        default=None,
        description='hotkey: the keys pressed together, modifiers first, such as ["cmd", "shift", "t"].',
    )
    x: int | None = Field(
        default=None,
        description="mouse_move, mouse_click: screen x in points (from desktop_screen or desktop_window).",
    )
    y: int | None = Field(default=None, description="mouse_move, mouse_click: screen y in points.")
    button: Literal["left", "right", "middle"] = Field(
        default="left", description="mouse_click: which button."
    )
    double: bool = Field(default=False, description="mouse_click: a double click.")


class DesktopPowerArgs(ToolArgs):
    action: Literal["status", "prevent_sleep"] = Field(
        description="status: battery, charging, and whether Matrx 2 is keeping it awake; prevent_sleep: keep it awake for a while.",
    )
    seconds: int | None = Field(
        default=None,
        ge=0,
        le=86400,
        description="prevent_sleep: how long to keep it awake; 0 lets it sleep again now.",
    )
    reason: str = Field(
        default="Matrx 2 is working",
        description="prevent_sleep: shown where the OS lists what keeps it awake.",
    )


class DesktopResourcesArgs(ToolArgs):
    action: Literal["snapshot"] = Field(
        default="snapshot",
        description="snapshot: CPU use, memory, swap and disk space now (the busiest processes are desktop_process list).",
    )


class FsWatchArgs(ToolArgs):
    action: Literal["start", "events", "stop"] = Field(
        description="start: watch a folder; events: what changed since the last read; stop: end the watch.",
    )
    path: str | None = Field(
        default=None, description="start: the folder (absolute, or relative to the home folder)."
    )
    recursive: bool = Field(default=True, description="start: include every subfolder.")
    ignore: list[str] | None = Field(
        default=None,
        description='start: globs not to report, such as [".git/**", "node_modules/**"].',
    )
    watch_id: str | None = Field(default=None, description="events, stop: the watch (from start).")
    wait_seconds: int = Field(
        default=0,
        ge=0,
        le=25,
        description="events: wait up to this long for a change when none is waiting.",
    )
