"""`pysae-ai-tools usage statusline` — a Claude Code status line that doubles as the usage feed.

Claude Code pipes its session JSON on stdin on every render. We pull the ``rate_limits`` block
(5H + weekly plan windows — Pro/Max only, present after the first API response of the session)
into the shared usage cache, so every other consumer (hook, ``show``, ``prime``) reads it
instead of the aggressively rate-limited ``/api/oauth/usage`` endpoint. Then we render a line.

With ``--exec <cmd>`` (wired by ``usage setup install`` when a status line already exists), the
same stdin is forwarded to ``<cmd>`` and its output is displayed — so an existing status line
(e.g. ccstatusline) keeps rendering while we silently feed the cache. Without it we print our
own compact line.

Must never fail: a crashing status line pollutes the UI. Bad/empty stdin, and a failing or slow
wrapped command, all degrade to our minimal line; cache-write errors are swallowed.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

from .client import record_statusline_usage

_WRAP_TIMEOUT = 10.0


def _num(value: object) -> float | None:
    return float(value) if isinstance(value, (int, float)) else None


def _window(rate: dict[str, object], key: str) -> tuple[float | None, float | None]:
    block = rate.get(key)
    if not isinstance(block, dict):
        return None, None
    return _num(block.get("used_percentage")), _num(block.get("resets_at"))


def _str_field(container: object, *path: str) -> str | None:
    node: object = container
    for key in path:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node if isinstance(node, str) and node else None


def _render(payload: dict[str, object], five_pct: float | None, week_pct: float | None) -> str:
    parts: list[str] = []
    model = _str_field(payload, "model", "display_name")
    if model:
        parts.append(model)
    current_dir = _str_field(payload, "workspace", "current_dir")
    if current_dir:
        parts.append(Path(current_dir).name)
    windows = [f"{label} {pct:.0f}%" for label, pct in (("5h", five_pct), ("7j", week_pct)) if pct is not None]
    if windows:
        parts.append(" ".join(windows))
    return " · ".join(parts)


def _exec_from_args(args: list[str]) -> str | None:
    """The wrapped command from ``--exec <cmd…>`` / ``--exec=<cmd>``.

    Everything after ``--exec`` is the command: Claude Code runs the configured status-line
    string through a shell, which splits it on spaces before we see it, so a wrapped command
    with its own args (``ccstatusline --theme dark``) arrives as several argv tokens — join
    them back into the single shell string ``_delegate`` re-runs."""
    for i, arg in enumerate(args):
        if arg == "--exec":
            return " ".join(args[i + 1 :]) or None
        if arg.startswith("--exec="):
            return arg[len("--exec=") :] or None
    return None


def _read_stdin() -> str:
    try:
        return sys.stdin.read()
    except (OSError, ValueError):
        return ""


def _parse_payload(raw_in: str) -> dict[str, object]:
    try:
        payload = json.loads(raw_in or "{}")
    except (json.JSONDecodeError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _delegate(command: str, stdin_text: str) -> str | None:
    """Run the wrapped status-line command with the same stdin and return its stdout.

    ``shell=True`` faithfully reproduces how Claude Code itself runs a configured status line
    (which may carry args/pipes); the command comes from the user's own settings.json, not from
    untrusted input. Returns None on any failure so the caller falls back to our own line."""
    try:
        result = subprocess.run(  # noqa: S602 - command is the user's own statusLine config
            command,
            shell=True,
            input=stdin_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=_WRAP_TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout if result.returncode == 0 else None


def statusline(args: list[str] | None = None) -> None:
    """Feed the usage cache from Claude Code's stdin JSON, then render the status line."""
    exec_cmd = _exec_from_args(args or [])
    raw_in = _read_stdin()
    payload = _parse_payload(raw_in)

    rate = payload.get("rate_limits")
    rate = rate if isinstance(rate, dict) else {}
    five_pct, five_reset = _window(rate, "five_hour")
    week_pct, week_reset = _window(rate, "seven_day")

    if five_pct is not None or week_pct is not None:
        try:
            record_statusline_usage(five_pct, five_reset, week_pct, week_reset, time.time())
        except (OSError, ValueError, OverflowError):
            pass

    if exec_cmd:
        delegated = _delegate(exec_cmd, raw_in)
        if delegated is not None:
            sys.stdout.write(delegated)
            return

    print(_render(payload, five_pct, week_pct))
