"""Shared helper: stream new messages.jsonl entries to stdout as the
drydock-under-test produces them. Used by lifecycle_runner and
gauntlet_runner so the operator's `tail -f live.log` shows the
actual prompts, tool calls, and error responses — not just a
high-level pass/fail summary.

If the runner sees an explicit `<tool_error>`, REJECTED, ALREADY
CORRECT, or other failure marker, it prefixes the line with a
visible `‼ NOTICED:` tag so the operator can verify the runner's
eyes are working.
"""
from __future__ import annotations

import json
from pathlib import Path


def _truncate(s: str, n: int = 220) -> str:
    s = s.replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


def render_message(msg: dict) -> str | None:
    role = msg.get("role")
    if role == "user":
        c = msg.get("content", "")
        if isinstance(c, str):
            return f"  USER: {_truncate(c, 400)}"
        return None
    if role == "assistant":
        text = msg.get("content", "") if isinstance(msg.get("content"), str) else ""
        reasoning = msg.get("reasoning_content", "") if isinstance(msg.get("reasoning_content"), str) else ""
        tool_calls = msg.get("tool_calls") or []
        lines: list[str] = []
        if reasoning.strip():
            lines.append(f"  thinking ({len(reasoning)}c): {_truncate(reasoning, 220)}")
        if text.strip():
            lines.append(f"  MODEL: {_truncate(text, 400)}")
        for tc in tool_calls:
            fn = tc.get("function", {}) or {}
            name = fn.get("name", "?")
            args = fn.get("arguments", "")
            if not isinstance(args, str):
                args = json.dumps(args)
            lines.append(f"  → {name}({_truncate(args, 280)})")
        return "\n".join(lines) if lines else None
    if role == "tool":
        name = msg.get("name", "?")
        c = msg.get("content", "")
        if not isinstance(c, str):
            c = json.dumps(c)
        # Detect failure markers — operator wants to verify the runner
        # notices these. Prefix with ‼ NOTICED: for visibility.
        failure_signals = (
            "<tool_error>",
            "REJECTED",
            "ALREADY CORRECT",
            "ALREADY APPLIED",
            "Malformed JSON",
            "truncated history entry",
            "SEARCH/REPLACE block",
            "max_tokens mid-emission",
            "[Exit code 1]",
            "[Exit code 124]",
            "Traceback (most recent call last)",
            "validation error for",
        )
        for sig in failure_signals:
            if sig in c:
                return f"  ‼ NOTICED ({sig}): {name} → {_truncate(c, 320)}"
        return f"  ✓ {name}: {_truncate(c, 240)}"
    if role == "system":
        c = msg.get("content", "")
        if isinstance(c, str):
            return f"  SYSTEM-NOTE: {_truncate(c, 240)}"
    return None


def stream_new_messages(
    session_dir: Path | None,
    last_index: int,
    out=None,
) -> int:
    """Read any new lines from session_dir/messages.jsonl past
    last_index, format + print to `out` (default stdout), return the
    new line count.
    """
    import sys
    if out is None:
        out = sys.stdout
    if session_dir is None:
        return last_index
    msgs = session_dir / "messages.jsonl"
    if not msgs.is_file():
        return last_index
    try:
        with msgs.open() as f:
            lines = f.readlines()
    except OSError:
        return last_index
    for i, line in enumerate(lines[last_index:], start=last_index + 1):
        try:
            msg = json.loads(line)
        except Exception:
            continue
        rendered = render_message(msg)
        if rendered:
            print(f"[#{i:3d}] {rendered}", file=out, flush=True)
    return len(lines)
