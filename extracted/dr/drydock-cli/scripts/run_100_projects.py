#!/usr/bin/env python3
"""Drive the real drydock TUI against a random project from
/data3/100-python-projects/, capture the session output, and grep for
bug patterns the operator hit before.

The point is NOT to score the run. The point is to make drydock chew on
realistic user code so I (Claude, on the 30-min wakeup) can read the log
and find the next show-stopper.

One run per invocation. A bash loop wraps this for continuous chewing.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

import pexpect

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shakedown_interactive import (  # noqa: E402
    DRYDOCK_BIN,
    SessionWatcher,
    drain_pty,
    send_prompt_and_confirm,
)


PROJECTS_ROOT = Path("/data3/100-python-projects")
SCRATCH_ROOT = Path("/tmp/drydock_100")
LOG_ROOT = Path("/data3/drydock/.100_projects/runs")

# Conversation prompts. Designed to mirror real iterative use:
# read → edit → run → diagnose → edit again → run again. The operator's
# 2026-05-19 critique was correct — the prior 2-prompt sessions never
# pushed drydock into compaction, multi-edit chains, or test-debug
# cycles, so all the real bugs they hit (truncated-history templates,
# search_replace cascades, malformed JSON on long writes) were invisible
# to my testing.
#
# Each session sends ALL 5 of these in sequence. That's ~10-15 turns
# minimum and forces drydock into the long-session failure modes.
PROMPT_SEQUENCE = [
    # 1. Open + understand
    "Read main.py and the README. Tell me what this project does and "
    "what the main entry point is. Brief.",

    # 2. Make an additive edit — exercises write_file with full content
    "Add a top-of-file docstring to main.py describing what it does. "
    "Three sentences. Keep all existing code intact.",

    # 3. Run + see what happens — exercises bash on user code
    "Now run `python3 main.py` and tell me what you see. If it crashes "
    "or has missing dependencies, tell me the exact error.",

    # 4. Debugging cycle — search_replace on a real symbol, multi-step
    "Pick one function in main.py and add a `--verbose` print "
    "statement at the start of it that says 'entering <funcname>'. "
    "Use search_replace, not write_file. Then run main.py again to "
    "verify your edit didn't break anything.",

    # 5. Iteration — re-edit after a previous edit (the cascade case)
    "Now revert the verbose print statement you added (search_replace "
    "again). Confirm by reading main.py and showing me the line where "
    "your function starts.",
]


# Bug-pattern signatures the operator has hit. Each one means
# "drydock surfaced a user-visible error in the TUI."
BUG_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("mcp_args_truncation", re.compile(r"Input should be a valid list.*'ython", re.I)),
    ("name_error", re.compile(r"\bNameError: name '[\w_]+' is not defined")),
    ("attribute_error", re.compile(r"\bAttributeError:")),
    ("pydantic_validation", re.compile(r"\bpydantic\.[\w_]*[Ee]rror|validation error for ")),
    ("search_replace_cascade", re.compile(
        r"(SEARCH/REPLACE blocks? failed.*?\n.*?){2,}", re.S
    )),
    ("syntax_error_after_edit", re.compile(r"SYNTAX ERROR after edit")),
    ("read_file_dedup_red_x", re.compile(r"✕\s+read_file:\s*(?:error|Invalid)")),
    ("hung_thrusting", re.compile(r"Thrusting.*?\(\s*([6-9]m\d+s|\d{2,}m\d+s)")),
    ("hung_running", re.compile(r"Running.*?\(\s*([6-9]m\d+s|\d{2,}m\d+s)")),
    ("hung_parsing", re.compile(r"Parsing.*?\(\s*([3-9]m\d+s|\d{2,}m\d+s)")),
    ("hallucinated_tool", re.compile(r"(exit_plan_mode|enter_plan_mode|ralph_repo_index)")),
    ("approval_modal_block", re.compile(r"Trust this folder.*?modal", re.I | re.S)),
    ("traceback", re.compile(r"^Traceback \(most recent call last\):", re.M)),
    ("api_400", re.compile(r"\bAPI error 400\b|context window exceeded")),
    ("unhandled_exception", re.compile(r"unhandled exception|Internal error", re.I)),
]


def _pick_project() -> Path | None:
    projects = sorted([p for p in PROJECTS_ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")])
    if not projects:
        return None
    return random.choice(projects)


def _prep_scratch(project: Path) -> Path:
    """Copy project into a clean scratch dir. We don't want the model
    editing the read-only corpus."""
    SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", project.name)
    dest = SCRATCH_ROOT / safe
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(project, dest)
    # Pre-trust so the trust modal doesn't block input.
    trusted = Path.home() / ".drydock" / "trusted_folders.toml"
    trusted.parent.mkdir(parents=True, exist_ok=True)
    text = trusted.read_text() if trusted.exists() else ""
    line = f'"{dest}" = true'
    if line not in text:
        with trusted.open("a") as f:
            f.write(f"\n{line}\n")
    return dest


def _scan_session_jsonl(jsonl_path: Path) -> list[tuple[str, str]]:
    """Walk messages.jsonl and surface real tool errors / failure
    patterns from the STRUCTURED tool result content. This catches
    errors the pty log obscures behind ANSI escape sequences.

    Returns [(pattern_name, snippet)].
    """
    if not jsonl_path.exists():
        return []
    hits: list[tuple[str, str]] = []
    # Tool-result content patterns. Each line in messages.jsonl is a
    # message; tool results have role="tool" and a stringified content
    # block that includes the actual error text.
    error_markers = [
        ("tool_error_tag", re.compile(r"<tool_error>")),
        ("mcp_args_truncation", re.compile(r"Input should be a valid list.*'ython", re.I)),
        ("validation_error", re.compile(r"\bvalidation error for ")),
        ("search_replace_not_found", re.compile(r"SEARCH/REPLACE block \d+ failed")),
        ("search_replace_rejected", re.compile(r"edit REJECTED|would break syntax")),
        ("syntax_error_after_edit", re.compile(r"SYNTAX ERROR after edit")),
        ("fuzzy_auto_apply", re.compile(r"auto-applied via fuzzy match")),
        ("tool_returned_error", re.compile(r"\berror:\s*\w|Error:\s*\w")),
        ("read_file_dedup", re.compile(r"this exact call to .read_file.")),
        ("write_file_dedup", re.compile(r"identical-content write|dedup")),
        ("python_traceback", re.compile(r"^Traceback \(most recent call last\):", re.M)),
        ("name_error", re.compile(r"\bNameError:")),
        ("attribute_error", re.compile(r"\bAttributeError:")),
        ("hallucinated_tool", re.compile(r"\b(exit_plan_mode|enter_plan_mode|ralph_repo_index)\b")),
        ("api_400", re.compile(r"API error 400|context window exceeded")),
        ("model_thrashing", re.compile(r"ALREADY CORRECT|ALREADY APPLIED")),
    ]
    try:
        with jsonl_path.open() as f:
            for lineno, line in enumerate(f, 1):
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("role") != "tool":
                    continue
                content = d.get("content", "")
                if not isinstance(content, str):
                    content = json.dumps(content)
                for name, pat in error_markers:
                    m = pat.search(content)
                    if m:
                        start = max(0, m.start() - 60)
                        end = min(len(content), m.end() + 200)
                        snippet = content[start:end].replace("\n", "\\n")[:400]
                        hits.append((name, f"L{lineno} [{d.get('name')}]: {snippet}"))
                        break  # one finding per message
    except Exception:
        pass
    return hits


def _scan_for_bugs(log_text: str) -> list[tuple[str, str]]:
    """Return [(pattern_name, sample_snippet), ...].

    Backstop pattern set used on the pty log when no session_dir is
    available. Most bugs surface more reliably via _scan_session_jsonl.
    """
    hits: list[tuple[str, str]] = []
    for name, pat in BUG_PATTERNS:
        m = pat.search(log_text)
        if m:
            start = max(0, m.start() - 80)
            end = min(len(log_text), m.end() + 200)
            snippet = log_text[start:end].replace("\n", "\\n")[:400]
            hits.append((name, snippet))
    return hits


def run_one(timeout_sec: int = 720) -> dict:
    project = _pick_project()
    if not project:
        return {"ok": False, "reason": "no_projects_found"}

    scratch = _prep_scratch(project)
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", project.name)
    pty_log = LOG_ROOT / f"{stamp}_{safe}.log"
    meta = {
        "project": project.name,
        "scratch": str(scratch),
        "pty_log": str(pty_log),
        "started_at": stamp,
        "bugs": [],
        "session_dir": None,
        "exit_reason": None,
    }
    meta_path = LOG_ROOT / f"{stamp}_{safe}.json"

    # Real read→edit→run→debug→re-edit sequence (5 prompts). Mirrors
    # actual operator usage; pushes drydock into compaction, multi-edit
    # chains, search_replace cascades, and the long-session failure
    # modes the prior 2-prompt benign sessions never touched.
    prompts = list(PROMPT_SEQUENCE)

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    pty_log_fh = pty_log.open("w", encoding="utf-8", errors="replace")
    child: pexpect.spawn | None = None
    try:
        child = pexpect.spawn(
            DRYDOCK_BIN,
            cwd=str(scratch),
            encoding="utf-8",
            timeout=5,
            dimensions=(40, 140),
            env=env,
        )
        child.logfile_read = pty_log_fh  # type: ignore[assignment]

        spawned_at = time.time()
        watcher = SessionWatcher(scratch, since=spawned_at)

        # Wait for TUI ready; tolerate the trust dialog auto-dismissal
        # that send_prompt_and_confirm handles.
        time.sleep(6)
        drain_pty(child, seconds=2.0)

        # Find the session. CLAUDE.md learning #36: drydock can take
        # up to 4 MINUTES to create a session_dir when the GPU is busy.
        # The previous 60s poll window was the #1 reason this harness
        # was blind to TUI errors — when session_dir was null we fell
        # back to ANSI-laden pty grep and missed every structured tool
        # error. Poll for up to 300s before giving up.
        for _ in range(300):
            try:
                if watcher.find_session():
                    break
            except Exception:
                pass
            time.sleep(1)
        if watcher.session_dir:
            meta["session_dir"] = str(watcher.session_dir)

        end_at = time.time() + timeout_sec
        for prompt in prompts:
            if time.time() >= end_at:
                meta["exit_reason"] = "timeout_before_prompt"
                break
            try:
                accepted = send_prompt_and_confirm(
                    child, prompt, watcher,
                    max_retries=2, wait_per_retry=30.0,
                )
            except Exception as e:
                meta["exit_reason"] = f"prompt_send_error: {e!r}"
                break
            if not accepted:
                meta["exit_reason"] = "prompt_not_accepted"
                break
            # Let the model work for up to N seconds, watching for new
            # messages. End early if quiet for 25s.
            quiet_since = time.time()
            try:
                watcher.refresh()
            except Exception:
                pass
            last_count = len(watcher.messages)
            while time.time() < end_at:
                time.sleep(3)
                drain_pty(child, seconds=0.5)
                # Late-bind: session_dir may have appeared after the
                # initial poll window. Keep trying.
                if watcher.session_dir is None:
                    try:
                        watcher.find_session()
                    except Exception:
                        pass
                try:
                    watcher.refresh()
                    now_count = len(watcher.messages)
                except Exception:
                    now_count = last_count
                if now_count > last_count:
                    last_count = now_count
                    quiet_since = time.time()
                if time.time() - quiet_since > 25:
                    break

        # One more late-bind attempt after the prompt loop ends, in
        # case the session_dir only materialised during the last turn.
        if watcher.session_dir is None:
            try:
                watcher.find_session()
            except Exception:
                pass
        if watcher.session_dir and not meta.get("session_dir"):
            meta["session_dir"] = str(watcher.session_dir)

        if not meta["exit_reason"]:
            meta["exit_reason"] = "completed"

    except pexpect.exceptions.EOF:
        meta["exit_reason"] = "drydock_died"
    except Exception as e:
        meta["exit_reason"] = f"harness_error: {e!r}"
    finally:
        if child and child.isalive():
            try:
                child.sendcontrol("c")
                time.sleep(0.5)
                child.terminate(force=True)
            except Exception:
                pass
        pty_log_fh.close()

    # Scan the pty log + the session log (if found) for bug signatures.
    # Read the raw pty log for fallback scanning + visible-only patterns
    # (e.g. spinner-hangs that only show up in the rendered TUI).
    log_text = ""
    try:
        log_text = pty_log.read_text(errors="replace")
    except Exception:
        pass

    # Structured scan: walk the session's messages.jsonl tool results.
    # This is the PRIMARY bug-detection path. Real tool errors are
    # captured verbatim in the JSON content, with no ANSI escape codes
    # to dodge. The pty-log grep was the source of historic blindness.
    structured_hits: list[tuple[str, str]] = []
    if meta.get("session_dir"):
        try:
            sdir = Path(str(meta["session_dir"]))
            structured_hits = _scan_session_jsonl(sdir / "messages.jsonl")
        except Exception as e:
            structured_hits.append(("scan_error", repr(e)))

    pty_hits = _scan_for_bugs(log_text)

    # Dedup by name — prefer the structured hit, then pty.
    seen: dict[str, str] = {}
    for name, snippet in structured_hits + pty_hits:
        seen.setdefault(name, snippet)
    meta["bugs"] = [{"name": n, "snippet": s} for n, s in seen.items()]
    meta["bugs_structured_count"] = len(structured_hits)
    meta["bugs_pty_count"] = len(pty_hits)
    meta["log_bytes"] = len(log_text)
    meta_path.write_text(json.dumps(meta, indent=2))
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout-sec", type=int, default=240)
    args = ap.parse_args()
    meta = run_one(timeout_sec=args.timeout_sec)
    print(json.dumps({
        "project": meta.get("project"),
        "bugs_found": [b["name"] for b in meta.get("bugs", [])],
        "exit_reason": meta.get("exit_reason"),
        "session_dir": meta.get("session_dir"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
