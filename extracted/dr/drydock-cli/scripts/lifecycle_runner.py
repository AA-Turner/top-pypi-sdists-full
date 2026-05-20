#!/usr/bin/env python3
"""Full-lifecycle drydock test runner.

Drives a single drydock TUI through the 6-phase autonomous-AI-engineer
workflow per the operator's 2026-05-19 spec:

  1. PRD Review       — refine a deliberately-vague spec, surface conflicts
  2. Scaffold         — initialize the workspace from PRD
  3. Implement        — write the feature
  4. Modify           — cross-cutting change to the data shape
  5. Troubleshoot     — diagnose + patch an injected runtime error
  6. Expand           — add a secondary subsystem cleanly

Per-phase pass/fail assertion is recorded so we can score how far the
model got. Anything past the read+edit+run cycle in the operator's
real /data3/slides usage is fair game for surfacing real bugs.

One run per invocation. JSON + pty log + per-phase outcomes under
/data3/drydock/.lifecycle_runs/. The 30-min Claude wakeup reads the
results and fixes whatever broke.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import sys
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable

import pexpect

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shakedown_interactive import (  # noqa: E402
    DRYDOCK_BIN,
    SessionWatcher,
    drain_pty,
    send_prompt_and_confirm,
)
from _eval_live_printer import stream_new_messages  # noqa: E402


SCRATCH_ROOT = Path("/tmp/drydock_lifecycle")
LOG_ROOT = Path("/data3/drydock/.lifecycle_runs")


# ───────────────────────────────────────────────────────────────────────
# Project specs. Each is a tiny but real CLI tool the model can build
# in 5-10 minutes. Picked at random per run so we get coverage across
# styles. Each phase prompt is parameterized by `{name}` / `{verb}`.
# ───────────────────────────────────────────────────────────────────────

@dataclass
class ProjectSpec:
    safe_name: str          # filesystem-safe scratch dir
    pkg: str                # python package name
    short: str              # one-liner for the model
    vague_brief: str        # phase 1 input — has at least one contradiction
    # The cross-cutting modification in phase 4: model must touch ≥2 files
    modify_to: str          # one-line description of the change
    modify_check: str       # marker that must appear in the codebase after
    # The error to inject in phase 5
    inject_error: tuple[str, str]   # (file relative to pkg/, content snippet to break)
    error_signature: str    # what should appear in the traceback if injection worked
    # The expansion subsystem in phase 6
    expand_to: str          # one-line description
    expand_check: str       # marker that should appear in the codebase after


SPECS = [
    ProjectSpec(
        safe_name="csv_to_json",
        pkg="csv_to_json",
        short="A CLI that reads a CSV file and writes JSON.",
        vague_brief=(
            "I want a tool that takes a CSV file and produces JSON. "
            "It should be fast but also handle huge files that don't fit "
            "in memory. The output should be one JSON document per file "
            "AND also a JSON-lines stream per row. The CLI flag for the "
            "input is --in, OR --input, OR positional — whichever you think "
            "is best. Be sure to add tests."
        ),
        modify_to="Switch the input from CSV to TSV (tab-separated) everywhere.",
        modify_check=r"\btsv\b|\\t|csv\.reader.*delimiter",
        inject_error=("__main__.py", "import json"),  # replaced with broken import
        error_signature="ModuleNotFoundError|ImportError",
        expand_to=(
            "Add a `--validate` flag that, when set, checks every row "
            "has the same number of columns and aborts with a clear "
            "error if not."
        ),
        expand_check=r"--validate|args\.validate|validate_columns",
    ),
    ProjectSpec(
        safe_name="word_count",
        pkg="word_count",
        short="A CLI that counts words and lines in a text file.",
        vague_brief=(
            "Build me a word-count CLI. It should count words, lines, "
            "and characters. Make sure it works on UTF-8. The output "
            "format should be 'tab-separated' but also 'human-readable' "
            "by default. Pick whichever is sensible. Make it fast on "
            "1GB files but also work without reading the whole file."
        ),
        modify_to="Add a --top N flag that prints the N most-frequent words.",
        modify_check=r"--top\b|top_n|Counter\(",
        inject_error=("__main__.py", "import collections"),
        error_signature="ModuleNotFoundError|ImportError",
        expand_to=(
            "Add a stopwords subsystem: a `--stopwords` flag accepting "
            "a file of words to ignore. Use it in the --top counting "
            "but leave the basic counts unaffected."
        ),
        expand_check=r"--stopwords|stopwords|stop_words",
    ),
]


# ───────────────────────────────────────────────────────────────────────
# Phase definitions.
# Each phase contributes one user prompt + one post-condition check.
# The check runs after the model's turn(s) settle and returns
# (passed: bool, detail: str).
# ───────────────────────────────────────────────────────────────────────

@dataclass
class Phase:
    name: str
    prompt: Callable[[ProjectSpec], str]
    check: Callable[[ProjectSpec, Path], tuple[bool, str]]
    settle_seconds: int = 25       # max idle time after model stops emitting
    deadline_seconds: int = 180    # hard wall-clock per phase


def _ph1_check(spec: ProjectSpec, cwd: Path) -> tuple[bool, str]:
    """PRD.md must exist and contain at least 2 of: Goals, Non-goals,
    Constraints, Open Questions, Ambiguities."""
    prd = cwd / "PRD.md"
    if not prd.is_file():
        return False, "PRD.md missing"
    text = prd.read_text(errors="replace").lower()
    markers = ["goal", "non-goal", "constraint", "open question",
               "ambiguit", "assumption"]
    hits = sum(1 for m in markers if m in text)
    if hits < 2:
        return False, f"PRD.md present but only {hits} structural markers found"
    return True, f"PRD.md has {hits} structural markers"


def _ph2_check(spec: ProjectSpec, cwd: Path) -> tuple[bool, str]:
    """Package dir + __init__.py + __main__.py exist."""
    pkg = cwd / spec.pkg
    if not pkg.is_dir():
        # also accept a flat layout where main.py is at root
        if (cwd / "main.py").is_file():
            return True, "flat main.py layout (no package dir)"
        return False, f"no {spec.pkg}/ dir and no main.py"
    init = pkg / "__init__.py"
    main = pkg / "__main__.py"
    if not init.is_file():
        return False, f"{spec.pkg}/__init__.py missing"
    if not main.is_file():
        # accept main.py as fallback
        if not (pkg / "main.py").is_file():
            return False, f"{spec.pkg}/__main__.py and main.py both missing"
    return True, f"package skeleton present at {spec.pkg}/"


def _ph3_check(spec: ProjectSpec, cwd: Path) -> tuple[bool, str]:
    """`python3 -m pkg --help` must exit 0."""
    import subprocess
    try:
        r = subprocess.run(
            ["python3", "-m", spec.pkg, "--help"],
            cwd=cwd, capture_output=True, timeout=20, text=True,
        )
    except subprocess.TimeoutExpired:
        return False, "python3 -m pkg --help timed out"
    except Exception as e:
        return False, f"subprocess error: {e!r}"
    if r.returncode != 0:
        return False, f"--help exit={r.returncode}: {r.stderr[:200]}"
    return True, "python3 -m pkg --help ran"


def _ph4_check(spec: ProjectSpec, cwd: Path) -> tuple[bool, str]:
    """Modification marker present in any .py file under cwd."""
    pat = re.compile(spec.modify_check, re.I)
    for p in cwd.rglob("*.py"):
        if pat.search(p.read_text(errors="replace")):
            return True, f"modify marker found in {p.relative_to(cwd)}"
    return False, f"no .py file matches /{spec.modify_check}/"


def _ph5_check(spec: ProjectSpec, cwd: Path) -> tuple[bool, str]:
    """After phase 5 the import error we injected should be GONE —
    `python3 -m pkg --help` should run again."""
    import subprocess
    try:
        r = subprocess.run(
            ["python3", "-m", spec.pkg, "--help"],
            cwd=cwd, capture_output=True, timeout=20, text=True,
        )
    except Exception as e:
        return False, f"subprocess error: {e!r}"
    if r.returncode != 0:
        return False, f"still broken: exit={r.returncode} stderr={r.stderr[:200]}"
    return True, "package recovered (--help works)"


def _ph6_check(spec: ProjectSpec, cwd: Path) -> tuple[bool, str]:
    """Expansion marker present in any .py file under cwd."""
    pat = re.compile(spec.expand_check, re.I)
    for p in cwd.rglob("*.py"):
        if pat.search(p.read_text(errors="replace")):
            return True, f"expand marker found in {p.relative_to(cwd)}"
    return False, f"no .py file matches /{spec.expand_check}/"


PHASES: list[Phase] = [
    Phase(
        name="1_prd",
        prompt=lambda s: (
            f"I want you to build me a small Python CLI tool. Here is my "
            f"raw brief — it has at least one ambiguity or contradiction. "
            f"Read it, then write a PRD.md to /tmp/drydock_lifecycle/"
            f"{s.safe_name}/PRD.md with these sections: ## Goals, "
            f"## Non-goals, ## Constraints, ## Open Questions (any "
            f"ambiguities you noticed — DO NOT make stuff up to resolve "
            f"them, leave them open).\n\nBrief:\n{s.vague_brief}"
        ),
        check=_ph1_check,
        deadline_seconds=180,
    ),
    Phase(
        name="2_scaffold",
        prompt=lambda s: (
            f"Now scaffold the package from PRD.md. Create the directory "
            f"structure: `{s.pkg}/__init__.py` and `{s.pkg}/__main__.py` "
            f"with an argparse-based CLI skeleton. Do NOT implement the "
            f"logic yet — just the package skeleton + argparse entry "
            f"point. `python3 -m {s.pkg} --help` must work."
        ),
        check=_ph2_check,
        deadline_seconds=180,
    ),
    Phase(
        name="3_implement",
        prompt=lambda s: (
            f"Now implement the core feature inside `{s.pkg}/`. "
            f"Goal: {s.short}. Use stdlib only. After writing the code, "
            f"run `python3 -m {s.pkg} --help` to confirm it still works."
        ),
        check=_ph3_check,
        deadline_seconds=240,
    ),
    Phase(
        name="4_modify",
        prompt=lambda s: (
            f"Make this cross-cutting change: {s.modify_to} Update all "
            f"the affected files (could be CLI, the core handler, "
            f"docstrings, README — wherever the old behavior is "
            f"referenced). When done, confirm by re-reading 2 of the "
            f"files you changed."
        ),
        check=_ph4_check,
        deadline_seconds=240,
    ),
    Phase(
        name="5_debug",
        # Before this phase runs, the orchestrator will inject a broken
        # import into __main__.py to simulate a real bug.
        prompt=lambda s: (
            f"I just tried to run `python3 -m {s.pkg} --help` and got "
            f"an error. Find the cause and fix it. Run the command "
            f"again after your fix to verify."
        ),
        check=_ph5_check,
        deadline_seconds=180,
    ),
    Phase(
        name="6_expand",
        prompt=lambda s: (
            f"Add this expansion cleanly: {s.expand_to} Keep the existing "
            f"behavior unchanged when the new flag isn't used."
        ),
        check=_ph6_check,
        deadline_seconds=240,
    ),
]


# ───────────────────────────────────────────────────────────────────────


def _prep_scratch(spec: ProjectSpec) -> Path:
    SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
    dest = SCRATCH_ROOT / spec.safe_name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    # Pre-trust so the trust modal doesn't block input.
    trusted = Path.home() / ".drydock" / "trusted_folders.toml"
    trusted.parent.mkdir(parents=True, exist_ok=True)
    text = trusted.read_text() if trusted.exists() else ""
    line = f'"{dest}" = true'
    if line not in text:
        with trusted.open("a") as f:
            f.write(f"\n{line}\n")
    return dest


def _inject_phase5_break(spec: ProjectSpec, cwd: Path) -> bool:
    """Pre-phase-5: break the __main__.py import line so the package
    can't load. Returns True if injection succeeded."""
    target = cwd / spec.pkg / spec.inject_error[0]
    if not target.is_file():
        # Try common alternative
        alt = cwd / spec.pkg / "main.py"
        if alt.is_file():
            target = alt
        else:
            return False
    txt = target.read_text(errors="replace")
    line = spec.inject_error[1]
    if line not in txt:
        return False
    broken = txt.replace(line, "import nonexistent_module_for_lifecycle_test", 1)
    target.write_text(broken)
    return True


def _phase_runtime_settle(child: pexpect.spawn, watcher: SessionWatcher,
                         deadline: float, idle_seconds: int,
                         live_index: int) -> tuple[int, int]:
    """After typing a prompt, wait until: (a) deadline hits, OR (b)
    messages.jsonl is idle for idle_seconds. Stream each new message
    to stdout so `tail -f live.log` shows the actual drydock TUI
    activity. Returns (new_message_count, live_index)."""
    quiet_since = time.time()
    try:
        watcher.refresh()
    except Exception:
        pass
    last = len(watcher.messages)
    while time.time() < deadline:
        time.sleep(3)
        drain_pty(child, seconds=0.5)
        if watcher.session_dir is None:
            try:
                watcher.find_session()
            except Exception:
                pass
        try:
            watcher.refresh()
            now = len(watcher.messages)
        except Exception:
            now = last
        # Stream any newly-arrived messages.
        live_index = stream_new_messages(watcher.session_dir, live_index)
        if now > last:
            last = now
            quiet_since = time.time()
        if time.time() - quiet_since > idle_seconds:
            break
    # Final flush in case lines arrived between watcher.refresh and exit
    live_index = stream_new_messages(watcher.session_dir, live_index)
    return last, live_index


def run_one(spec_idx: int | None = None) -> dict:
    import random
    spec = SPECS[spec_idx] if spec_idx is not None else random.choice(SPECS)
    cwd = _prep_scratch(spec)

    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    pty_log_path = LOG_ROOT / f"{stamp}_{spec.safe_name}.log"
    meta_path = LOG_ROOT / f"{stamp}_{spec.safe_name}.json"

    meta = {
        "spec": spec.safe_name,
        "cwd": str(cwd),
        "pty_log": str(pty_log_path),
        "started_at": stamp,
        "session_dir": None,
        "phases": [],
        "exit_reason": None,
    }

    pty_log = pty_log_path.open("w", encoding="utf-8", errors="replace")
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    child: pexpect.spawn | None = None
    try:
        print(f"[{time.strftime('%H:%M:%S')}] spawning drydock in {cwd}")
        child = pexpect.spawn(
            DRYDOCK_BIN, cwd=str(cwd), encoding="utf-8", timeout=5,
            dimensions=(40, 140), env=env,
        )
        child.logfile_read = pty_log  # type: ignore[assignment]
        spawned = time.time()
        watcher = SessionWatcher(cwd, since=spawned)

        time.sleep(6)
        drain_pty(child, seconds=2.0)
        # Find session (up to 5 min as drydock can lag)
        for _ in range(300):
            try:
                if watcher.find_session():
                    break
            except Exception:
                pass
            time.sleep(1)
        if watcher.session_dir:
            meta["session_dir"] = str(watcher.session_dir)

        live_index = 0  # how many messages we've already streamed

        # Run each phase in sequence.
        for phase in PHASES:
            phase_started = time.time()
            phase_record: dict = {
                "name": phase.name,
                "started_at": time.strftime("%H:%M:%S"),
            }

            # Pre-phase hook: phase 5 needs an injected break before
            # we ask the model to debug.
            if phase.name == "5_debug":
                injected = _inject_phase5_break(spec, cwd)
                phase_record["pre_injection_ok"] = injected
                if not injected:
                    phase_record["passed"] = False
                    phase_record["detail"] = "could not inject break"
                    meta["phases"].append(phase_record)
                    continue

            prompt_text = phase.prompt(spec)
            # Echo the prompt to stdout BEFORE sending — so the operator
            # can see what we're asking drydock to do.
            print(f"\n=== {phase.name} ===")
            for line in prompt_text.splitlines():
                print(f"  PROMPT: {line}")
            try:
                accepted = send_prompt_and_confirm(
                    child, prompt_text, watcher,
                    max_retries=2, wait_per_retry=45.0,
                )
            except Exception as e:
                phase_record["passed"] = False
                phase_record["detail"] = f"prompt_send_error: {e!r}"
                meta["phases"].append(phase_record)
                continue
            phase_record["prompt_accepted"] = accepted
            if not accepted:
                phase_record["passed"] = False
                phase_record["detail"] = "prompt not accepted"
                meta["phases"].append(phase_record)
                continue

            deadline = phase_started + phase.deadline_seconds
            _, live_index = _phase_runtime_settle(
                child, watcher, deadline, phase.settle_seconds, live_index,
            )

            try:
                passed, detail = phase.check(spec, cwd)
            except Exception as e:
                passed, detail = False, f"check raised: {e!r}"
            phase_record["passed"] = passed
            phase_record["detail"] = detail
            phase_record["duration_sec"] = round(time.time() - phase_started, 1)
            meta["phases"].append(phase_record)
            print(f"[{time.strftime('%H:%M:%S')}] phase {phase.name}: "
                  f"{'PASS' if passed else 'FAIL'} ({detail})")

            # If a foundational phase fails, abort further phases — they
            # depend on the workspace being valid.
            if phase.name in {"2_scaffold", "3_implement"} and not passed:
                meta["exit_reason"] = f"abort_after_failed_{phase.name}"
                break

        if not meta["exit_reason"]:
            meta["exit_reason"] = "completed"
    except pexpect.exceptions.EOF:
        meta["exit_reason"] = "drydock_died"
    except Exception as e:  # noqa: BLE001
        meta["exit_reason"] = f"harness_error: {e!r}"
    finally:
        if child and child.isalive():
            try:
                child.sendcontrol("c")
                time.sleep(0.5)
                child.terminate(force=True)
            except Exception:
                pass
        pty_log.close()

    # Summary scoring
    passed = sum(1 for p in meta["phases"] if p.get("passed"))
    total = len(meta["phases"])
    meta["score"] = f"{passed}/{total}"

    meta_path.write_text(json.dumps(meta, indent=2))
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", type=int, default=None,
                    help="0-indexed spec to use (else random)")
    args = ap.parse_args()
    meta = run_one(spec_idx=args.spec)
    print(json.dumps({
        "spec": meta.get("spec"),
        "score": meta.get("score"),
        "exit_reason": meta.get("exit_reason"),
        "session_dir": meta.get("session_dir"),
        "phases": [{"name": p.get("name"), "passed": p.get("passed"),
                    "detail": (p.get("detail") or "")[:120]}
                   for p in meta.get("phases", [])],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
