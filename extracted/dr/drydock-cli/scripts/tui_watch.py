#!/usr/bin/env python3
"""Tail `~/.drydock/all_tui.jsonl` (produced by tui_capture.py) and
print every drydock TUI error / failure pattern, with structured
metadata, as it happens.

Findings are appended to `~/.drydock/tui_findings.jsonl` so wakeup
ticks can read the recent set quickly.

Run as:
    nohup python3 scripts/tui_watch.py >/dev/null 2>&1 &
"""
from __future__ import annotations

import json
import os
import re
import signal
import sys
import time
from pathlib import Path

INPUT_PATH = Path.home() / ".drydock" / "all_tui.jsonl"
FINDINGS_PATH = Path.home() / ".drydock" / "tui_findings.jsonl"
OFFSET_PATH = Path.home() / ".drydock" / "tui_watch_offset.txt"

# These patterns are calibrated to real drydock tool-result content
# (NOT the rendered TUI). Each one corresponds to a real user-visible
# pain point. Add new ones here as you spot them.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("tool_error_tag", re.compile(r"<tool_error>")),
    ("mcp_args_truncation", re.compile(r"Input should be a valid list.*'ython", re.I)),
    ("validation_error", re.compile(r"\bvalidation error for ")),
    ("search_replace_not_found", re.compile(r"SEARCH/REPLACE block \d+ failed: Search text not found")),
    ("search_replace_rejected_syntax", re.compile(r"edit REJECTED.*would (?:introduce|break) (?:SyntaxError|syntax)")),
    ("syntax_error_after_edit", re.compile(r"SYNTAX ERROR after edit")),
    ("fuzzy_auto_apply", re.compile(r"auto-applied via fuzzy match")),
    ("read_file_dedup", re.compile(r"this exact call to .read_file.")),
    ("bash_dedup", re.compile(r"this exact call to .bash.")),
    ("write_file_dedup", re.compile(r"identical-content write|3rd identical write")),
    ("read_mcp_args_truncation", re.compile(r"read_mcp_resource failed.*Could not read")),
    ("python_traceback", re.compile(r"Traceback \(most recent call last\):")),
    ("name_error", re.compile(r"\bNameError:")),
    ("attribute_error", re.compile(r"\bAttributeError:")),
    ("api_400", re.compile(r"API error 400|context window exceeded")),
    ("hallucinated_tool", re.compile(r"\b(exit_plan_mode|enter_plan_mode|ralph_repo_index|list_mcp_resources_local)\b")),
    ("model_thrashing_already_correct", re.compile(r"ALREADY CORRECT|ALREADY APPLIED")),
    ("permission_denied", re.compile(r"Permission denied|tool was denied")),
    # Require an exception-call shape (`ToolError(` or `raise ToolError`)
    # so this doesn't match prose/documentation that simply mentions the
    # word "ToolError". Caught false-positive 2026-05-18 23:23 when
    # retrieve returned CLAUDE.md text that documented the term.
    ("tool_panic_retry", re.compile(r"raise ToolError|ToolError\(|panic[ -]retry")),

    # 2026-05-19: caught from operator's /data3/slides session — model
    # output a write_file call with 8K-char content that exceeded
    # max_tokens=2048 and got truncated mid-JSON. Format handler emits
    # "Your tool call arguments were malformed JSON ... max_tokens
    # mid-emission". Worth a dedicated pattern because it's the
    # canonical "model output got cut off" signature — independent
    # of which tool, independent of the file path.
    ("tool_args_malformed_json", re.compile(
        r"tool call arguments were malformed JSON|Malformed JSON:",
        re.I,
    )),
    ("tool_args_truncated_mid_emission", re.compile(
        r"exceeded the model's max_tokens mid-emission", re.I,
    )),

    # 2026-05-19: model copies drydock's history-compaction markers
    # ('_truncated' / '_original_bytes') back into a tool call as if
    # they were the real args. Drydock detects + refuses. Surface this
    # — it's a thrashing signature where the model is going in circles
    # because it's lost track of the actual file content.
    ("tool_args_truncated_history_template", re.compile(
        r"truncated history entry as a template|"
        r"_truncated'/'_original_bytes'", re.I,
    )),

    # Softer signals — broaden coverage when hard errors aren't surfacing.
    # Added 2026-05-18 22:50 after a 60-min stretch with zero findings;
    # the operator's heuristic is "if you don't see issues every 15 min
    # the testing is wrong." These catch the symptoms without requiring
    # an exception.
    ("loop_retrospection", re.compile(r"RETROSPECTION — Your last \d+ tool calls")),
    ("loop_guidance", re.compile(r"you are repeating a pattern that is not making progress", re.I)),
    ("compaction_triggered", re.compile(r"\[compact\]|context.compact|auto_compact|emergency compact", re.I)),
    ("api_error_recovery", re.compile(r"API error \d+|backend.*retry|will retry", re.I)),
    ("ghost_tool_call", re.compile(r"tool .* does not exist|unknown tool|not a registered tool", re.I)),
    ("subagent_failed", re.compile(r"subagent (?:failed|errored|timed out)|task tool failure", re.I)),
    ("model_empty_response", re.compile(r"empty response from model|no content.*no tool_calls|Continue working\.")),
    ("file_too_large_skip", re.compile(r"file too large|truncated.*\d+ lines|max_read_bytes exceeded", re.I)),
]

_stop = False


def _emit_finding(record: dict) -> None:
    FINDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with FINDINGS_PATH.open("a") as f:
        f.write(json.dumps(record, default=str) + "\n")
    # Also echo to stdout so a curious tail -f /var/log/... user sees
    # it immediately.
    print(json.dumps({
        "ts": record.get("captured_at"),
        "session": (record.get("session_id") or "")[:24],
        "pat": record.get("pattern"),
        "tool": record.get("tool_name"),
        "snippet": (record.get("snippet") or "")[:160],
    }, default=str), flush=True)


def _handle(_sig, _frame) -> None:
    global _stop
    _stop = True


def _scan(line: str) -> None:
    """Scan a single all_tui.jsonl line and emit findings."""
    try:
        rec = json.loads(line)
    except Exception:
        return
    if "event" in rec and "msg" not in rec:
        # Lifecycle events — log session_attached so wakeups see new
        # sessions starting, but don't pattern-scan them.
        if rec.get("event") in ("session_attached", "capture_started"):
            _emit_finding({**rec, "pattern": rec["event"]})
        return
    msg = rec.get("msg") or {}
    role = msg.get("role")
    if role != "tool":
        return
    content = msg.get("content", "")
    if not isinstance(content, str):
        content = json.dumps(content, default=str)
    tool_name = msg.get("name") or ""
    for pat_name, pat in PATTERNS:
        m = pat.search(content)
        if m:
            start = max(0, m.start() - 60)
            end = min(len(content), m.end() + 200)
            snippet = content[start:end].replace("\n", "\\n")[:400]
            _emit_finding({
                "captured_at": rec.get("captured_at"),
                "session_id": rec.get("session_id"),
                "session_dir": rec.get("session_dir"),
                "tool_name": tool_name,
                "pattern": pat_name,
                "snippet": snippet,
            })
            return  # one finding per tool result


def _load_offset() -> int:
    try:
        return int(OFFSET_PATH.read_text().strip())
    except (FileNotFoundError, ValueError):
        return 0


def _save_offset(offset: int) -> None:
    try:
        OFFSET_PATH.write_text(str(offset))
    except OSError:
        pass


def _tail() -> None:
    INPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not INPUT_PATH.exists():
        INPUT_PATH.touch()
    f = INPUT_PATH.open()
    # Resume from the last offset (idempotent restart). If the file
    # was truncated, rewind. If we've never run, start at 0 to
    # backfill everything currently sitting in all_tui.jsonl.
    start_offset = _load_offset()
    try:
        size = INPUT_PATH.stat().st_size
    except OSError:
        size = 0
    if start_offset > size:
        start_offset = 0  # truncated
    f.seek(start_offset)
    last_save = 0.0
    while not _stop:
        line = f.readline()
        if not line:
            time.sleep(0.5)
            continue
        line = line.rstrip("\n")
        if line:
            try:
                _scan(line)
            except Exception as e:
                _emit_finding({
                    "captured_at": time.time(),
                    "pattern": "watcher_error",
                    "snippet": repr(e),
                })
        now = time.time()
        if now - last_save >= 2.0:
            _save_offset(f.tell())
            last_save = now


def main() -> int:
    signal.signal(signal.SIGTERM, _handle)
    signal.signal(signal.SIGINT, _handle)
    _tail()
    return 0


if __name__ == "__main__":
    sys.exit(main())
