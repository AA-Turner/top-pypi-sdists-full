#!/usr/bin/env python3
"""Pretty-print the active eval-loop drydock's tool calls + results.

What this is for: operator wants to see EXACTLY what drydock is doing
during a gauntlet/lifecycle run — the tool calls, the tool results,
the model's text — not just the runner's "PASS / FAIL" summary lines.

What it does:
  1. Find the latest drydock session whose cwd is under
     /tmp/drydock_gauntlet/ or /tmp/drydock_lifecycle/ (the eval-loop
     scratch dirs).
  2. Tail its messages.jsonl in real time.
  3. Format each new message TUI-style: tool calls with their args,
     tool results with truncated content, assistant text with a
     thinking summary.

Usage:
    python3 scripts/watch_eval.py
    # or persistent tail:
    python3 scripts/watch_eval.py --follow

Stop with Ctrl-C. Re-attaches if the active session changes (eval
loop moves on to the next iter).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


SESSION_ROOT = Path.home() / ".drydock" / "logs" / "session"
EVAL_SCRATCH_ROOTS = (
    Path("/tmp/drydock_gauntlet"),
    Path("/tmp/drydock_lifecycle"),
)


def _find_active_eval_session() -> Path | None:
    """Find the active drydock session for the current eval-loop run.

    Strategy: walk the per-project markers under the eval scratch roots
    first — they point at the session_dir BEFORE messages.jsonl is
    materialized. Fall back to scanning SESSION_ROOT for the most
    recently-modified messages.jsonl whose meta.json wd matches.
    """
    # Fast path: per-project marker in any eval scratch dir.
    best_via_marker: tuple[float, Path] | None = None
    for root in EVAL_SCRATCH_ROOTS:
        if not root.is_dir():
            continue
        for marker in root.glob("**/.drydock/current_session.txt"):
            try:
                target = Path(marker.read_text().strip())
            except Exception:
                continue
            mtime = marker.stat().st_mtime
            if best_via_marker is None or mtime > best_via_marker[0]:
                best_via_marker = (mtime, target)
    if best_via_marker is not None:
        return best_via_marker[1]

    # Slow path: scan SESSION_ROOT.
    best: tuple[float, Path] | None = None
    for d in SESSION_ROOT.iterdir():
        if not d.is_dir():
            continue
        meta = d / "meta.json"
        msgs = d / "messages.jsonl"
        if not msgs.exists():
            continue
        wd = ""
        if meta.exists():
            try:
                wd = json.loads(meta.read_text()).get(
                    "environment", {}).get("working_directory", "")
            except Exception:
                pass
        if not any(wd.startswith(str(r)) for r in EVAL_SCRATCH_ROOTS):
            continue
        try:
            mtime = msgs.stat().st_mtime
        except OSError:
            continue
        if best is None or mtime > best[0]:
            best = (mtime, d)
    return best[1] if best else None


def _truncate(s: str, n: int = 160) -> str:
    s = s.replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


def _render(msg: dict) -> str | None:
    role = msg.get("role")
    if role == "user":
        c = msg.get("content", "")
        if isinstance(c, str):
            return f"\033[36mUSER:\033[0m {_truncate(c, 300)}"
        return None
    if role == "assistant":
        text = msg.get("content", "") or ""
        if not isinstance(text, str):
            text = ""
        reasoning = msg.get("reasoning_content", "") or ""
        if not isinstance(reasoning, str):
            reasoning = ""
        tool_calls = msg.get("tool_calls") or []
        lines: list[str] = []
        if reasoning.strip():
            lines.append(f"\033[90m  thinking ({len(reasoning)}c): "
                         f"{_truncate(reasoning, 200)}\033[0m")
        if text.strip():
            lines.append(f"\033[32mASSISTANT:\033[0m {_truncate(text, 300)}")
        for tc in tool_calls:
            fn = tc.get("function", {})
            name = fn.get("name", "?")
            args = fn.get("arguments", "")
            if not isinstance(args, str):
                args = json.dumps(args)
            lines.append(f"\033[33m  → {name}\033[0m({_truncate(args, 220)})")
        return "\n".join(lines) if lines else None
    if role == "tool":
        name = msg.get("name", "?")
        c = msg.get("content", "")
        if not isinstance(c, str):
            c = json.dumps(c)
        marker = "✓"
        color = "\033[32m"
        if "<tool_error>" in c or "Error:" in c[:80] or "ALREADY CORRECT" in c:
            marker = "✕"
            color = "\033[31m"
        elif "warnings" in c and "Block" in c:
            marker = "⚠"
            color = "\033[33m"
        return f"{color}  {marker} {name}:\033[0m {_truncate(c, 240)}"
    if role == "system":
        c = msg.get("content", "")
        if isinstance(c, str):
            return f"\033[35mSYSTEM-NOTE:\033[0m {_truncate(c, 220)}"
    return None


def tail_session(session_dir: Path, follow: bool = True) -> None:
    msgs = session_dir / "messages.jsonl"
    print(f"\033[1;34m== attached: {session_dir.name}\033[0m")
    print(f"\033[34m   cwd: see meta.json\033[0m")
    seen = 0
    while True:
        try:
            with msgs.open() as f:
                lines = f.readlines()
        except FileNotFoundError:
            time.sleep(1)
            continue
        for i, line in enumerate(lines[seen:], start=seen + 1):
            try:
                msg = json.loads(line)
            except Exception:
                continue
            out = _render(msg)
            if out:
                print(f"\033[90m[{i:3d}]\033[0m {out}")
        seen = len(lines)
        if not follow:
            break
        time.sleep(1)
        # Re-check active session — eval loop moves on to next iter
        active = _find_active_eval_session()
        if active and active != session_dir:
            print(f"\033[1;35m== session changed → {active.name}\033[0m")
            session_dir = active
            msgs = session_dir / "messages.jsonl"
            seen = 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--follow", action="store_true", default=True)
    ap.add_argument("--once", action="store_true",
                    help="Print current state and exit (no follow)")
    args = ap.parse_args()
    active = _find_active_eval_session()
    if active is None:
        print("No active eval-loop drydock session found.")
        print("Looked under: " + ", ".join(str(r) for r in EVAL_SCRATCH_ROOTS))
        print("Is the eval loop running? Check:")
        print("  pgrep -f /data3/drydock/scripts/eval_loop.sh")
        return 1
    tail_session(active, follow=not args.once)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nbye")
        sys.exit(0)
