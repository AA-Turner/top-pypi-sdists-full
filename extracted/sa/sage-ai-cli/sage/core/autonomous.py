"""Autonomous-loop primitives shared by `/autopolit`, `/autofleet`, `/autoorg`.

All three REPL commands are *fully autonomous* — they run iteration after
iteration with no user input, focused on either a user-supplied message
or, when none is given, on whole-codebase improvements proposed by sage
itself. The user remains in control via two cancel paths:

  1. Press Ctrl-C → the current iteration aborts, the loop exits, and the
     REPL returns. sage itself stays alive.
  2. Create the file `<project_root>/.sage/AUTO-STOP` from another shell.
     The loop polls for this file between iterations and exits cleanly.
     Use this when the running iteration is stuck inside an LLM call and
     Ctrl-C is awkward.

The three loops differ only in what they do per iteration:

  - `run_autopolit_loop()`   — one in-process turn per iteration.
  - `run_autofleet_loop()`   — decompose iteration into N parallel subtasks.
  - `run_autoorg_loop()`     — N parallel subtasks, each one assigned a
                                distinct organisational role (CEO, CTO,
                                engineer, designer, marketer, etc.).

This module deliberately depends only on stdlib + the Sage core
primitives, so it stays unit-testable without spinning up a real LLM.
"""

from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence


@dataclass
class LoopState:
    """Per-loop state that survives across iterations.

    Carries cancel signals + iteration history. The same object is passed
    to every iteration callback so it can adapt based on past results
    (avoid repeating identical work, switch strategy after N failures,
    etc.).
    """

    project_root: Path
    cancel_event: threading.Event = field(default_factory=threading.Event)
    iteration: int = 0
    history: list[dict] = field(default_factory=list)
    started_at: float = field(default_factory=time.time)

    @property
    def stop_file(self) -> Path:
        return self.project_root / ".sage" / "AUTO-STOP"

    def should_stop(self) -> tuple[bool, str]:
        if self.cancel_event.is_set():
            return True, "cancel-event"
        if self.stop_file.exists():
            return True, f"stop-file: {self.stop_file}"
        return False, ""

    def record(self, entry: dict) -> None:
        self.history.append(entry)


def _ensure_stop_file_cleared(state: LoopState) -> None:
    """Remove a stale stop file so a fresh loop doesn't immediately exit."""
    try:
        if state.stop_file.exists():
            state.stop_file.unlink()
    except OSError:
        pass  # best-effort; not fatal


def _default_iteration_prompt(task: str | None, iteration: int) -> str:
    """Build the per-iteration prompt.

    With a user message: focus iteration on it, asking sage to extend or
    refine the work each round.

    Without a user message: ask sage to analyse the codebase, pick one
    impactful improvement, and implement it with TDD.
    """
    if task:
        return (
            f"## Autonomous iteration {iteration}\n\n"
            f"## User-supplied focus\n{task.strip()}\n\n"
            "Make tangible progress on this focus area in THIS iteration.\n"
            "If the work is already done, find a closely related improvement\n"
            "(refactor, test coverage, docs, performance, security) that\n"
            "compounds on previous iterations. Avoid repeating yourself.\n"
            "Use TDD: write or update a failing test first, then implement."
        )
    return (
        f"## Autonomous iteration {iteration}\n\n"
        "No specific focus was provided. Analyse the codebase and pick ONE\n"
        "high-impact improvement for this iteration. Prefer in this order:\n"
        "  1. Failing or missing tests for critical paths\n"
        "  2. Security issues (hardcoded secrets, missing input validation)\n"
        "  3. Reliability gaps (unhandled errors, race conditions)\n"
        "  4. Maintainability (duplicated logic, large untyped functions)\n"
        "  5. Performance hot spots\n"
        "  6. Documentation gaps (public API, READMEs)\n"
        "Use TDD: write or update a failing test first, then implement.\n"
        "Do NOT repeat improvements from previous iterations of this loop."
    )


# Default roles used by /autoorg. Each role gets its own iteration prompt
# so the model adopts the perspective of that function in the org.
DEFAULT_ORG_ROLES: tuple[tuple[str, str], ...] = (
    ("product-manager", "Define the next user-facing improvement worth shipping. Output a one-paragraph spec."),
    ("staff-engineer", "Pick the next technical improvement. Write the code and tests."),
    ("qa-engineer", "Find untested critical paths and add coverage. Report any bugs found."),
    ("security-engineer", "Audit for security issues. Patch any you find."),
    ("devops-engineer", "Tighten Dockerfile / CI / observability. Add health checks if missing."),
    ("technical-writer", "Improve a README or docstring that confuses a newcomer."),
)


def _role_iteration_prompt(role: str, role_brief: str, task: str | None,
                           iteration: int) -> str:
    """Per-role prompt for /autoorg subagents."""
    focus = f"## User focus\n{task.strip()}\n\n" if task else ""
    return (
        f"## /autoorg iteration {iteration} — you are the **{role}**\n\n"
        f"## Your role\n{role_brief}\n\n"
        f"{focus}"
        "Make tangible progress in THIS iteration appropriate for your role.\n"
        "Coordinate via files in the repository — read what the other roles\n"
        "have produced and build on it. Avoid stepping on their work."
    )


# ---------------------------------------------------------------------------
# Public loop runners
# ---------------------------------------------------------------------------


IterationFn = Callable[[str, LoopState], dict]
"""A single-iteration callback. Receives the prompt + loop state, returns
a dict describing what happened (used for history tracking)."""

ProgressFn = Callable[[str], None]


def run_autopolit_loop(
    *,
    task: str | None,
    project_root: Path,
    run_one_iteration: IterationFn,
    progress: ProgressFn | None = None,
    max_iterations: int | None = None,
    iteration_delay_seconds: float = 0.5,
    stagnation_window: int = 3,
) -> LoopState:
    """Single-threaded autonomous loop.

    Repeats forever (or up to `max_iterations` if set for testing) until:
      - User presses Ctrl-C (KeyboardInterrupt caught here, loop exits)
      - `.sage/AUTO-STOP` file appears
      - `state.cancel_event` is set
      - Stagnation: last `stagnation_window` iterations all returned the
        same `response_hash` (model is stuck repeating itself).
    """
    state = LoopState(project_root=project_root.resolve())
    state.project_root.mkdir(parents=True, exist_ok=True)
    (state.project_root / ".sage").mkdir(parents=True, exist_ok=True)
    _ensure_stop_file_cleared(state)

    def _log(msg: str) -> None:
        if progress:
            progress(msg)

    _log(f"/autopolit started — focus: {task or '(self-directed code improvement)'}")
    _log(f"Stop anytime with Ctrl-C, or `touch {state.stop_file}` from another shell.")

    try:
        while True:
            stop, reason = state.should_stop()
            if stop:
                _log(f"/autopolit stopping ({reason})")
                break
            if max_iterations is not None and state.iteration >= max_iterations:
                _log(f"/autopolit reached max_iterations={max_iterations}; stopping")
                break

            state.iteration += 1
            _log(f"── iteration {state.iteration} ──")
            prompt = _default_iteration_prompt(task, state.iteration)
            try:
                entry = run_one_iteration(prompt, state)
            except KeyboardInterrupt:
                _log("/autopolit cancelled by user (Ctrl-C)")
                break
            except Exception as exc:
                entry = {"error": str(exc), "iteration": state.iteration}
                _log(f"iteration error: {exc}")
            state.record(entry)

            if _stagnated(state.history, window=stagnation_window):
                _log(f"/autopolit stopping — last {stagnation_window} iterations were identical")
                break

            # Small breath between iterations so the user can interrupt.
            time.sleep(iteration_delay_seconds)
    except KeyboardInterrupt:
        _log("/autopolit cancelled by user (Ctrl-C)")

    _log(f"/autopolit done: {state.iteration} iterations completed in "
         f"{time.time() - state.started_at:.0f}s")
    return state


def run_autofleet_loop(
    *,
    task: str | None,
    project_root: Path,
    decompose: Callable[[str | None, LoopState], list[str]],
    run_one_subtask: Callable[[str, LoopState], dict],
    progress: ProgressFn | None = None,
    max_iterations: int | None = None,
    max_workers: int = 4,
    iteration_delay_seconds: float = 0.5,
) -> LoopState:
    """Parallel-subagent autonomous loop.

    Per iteration: decompose the focus into N subtasks → run each in its
    own thread via `run_one_subtask` → record all results. Repeats
    indefinitely with the same cancel semantics as /autopolit.
    """
    state = LoopState(project_root=project_root.resolve())
    state.project_root.mkdir(parents=True, exist_ok=True)
    (state.project_root / ".sage").mkdir(parents=True, exist_ok=True)
    _ensure_stop_file_cleared(state)

    def _log(msg: str) -> None:
        if progress:
            progress(msg)

    _log(f"/autofleet started — focus: {task or '(self-directed code improvement)'}")
    _log(f"Stop anytime with Ctrl-C, or `touch {state.stop_file}` from another shell.")

    try:
        while True:
            stop, reason = state.should_stop()
            if stop:
                _log(f"/autofleet stopping ({reason})")
                break
            if max_iterations is not None and state.iteration >= max_iterations:
                _log(f"/autofleet reached max_iterations={max_iterations}; stopping")
                break

            state.iteration += 1
            _log(f"── fleet iteration {state.iteration} ──")
            subtasks = decompose(task, state)
            if not subtasks:
                _log("decompose returned no subtasks; ending fleet loop")
                break

            results: list[dict] = []
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                futures = {
                    pool.submit(_safe_subtask, run_one_subtask, sub, state): sub
                    for sub in subtasks
                }
                for fut in as_completed(futures):
                    sub = futures[fut]
                    try:
                        entry = fut.result()
                    except Exception as exc:
                        entry = {"subtask": sub, "error": str(exc)}
                    results.append(entry)
                    _log(f"  ✓ subtask done: {sub[:60]}")

            state.record({"iteration": state.iteration, "results": results})
            time.sleep(iteration_delay_seconds)
    except KeyboardInterrupt:
        _log("/autofleet cancelled by user (Ctrl-C)")

    _log(f"/autofleet done: {state.iteration} iterations completed in "
         f"{time.time() - state.started_at:.0f}s")
    return state


def run_autoorg_loop(
    *,
    task: str | None,
    project_root: Path,
    run_one_role: Callable[[str, str, LoopState], dict],
    progress: ProgressFn | None = None,
    roles: Sequence[tuple[str, str]] = DEFAULT_ORG_ROLES,
    max_iterations: int | None = None,
    max_workers: int = 4,
    iteration_delay_seconds: float = 0.5,
) -> LoopState:
    """Org-role autonomous loop.

    Per iteration: each role (product, engineering, QA, security, devops,
    docs) runs as a separate subagent IN PARALLEL with a role-specific
    prompt. Stays alive until cancelled.
    """
    state = LoopState(project_root=project_root.resolve())
    state.project_root.mkdir(parents=True, exist_ok=True)
    (state.project_root / ".sage").mkdir(parents=True, exist_ok=True)
    _ensure_stop_file_cleared(state)

    def _log(msg: str) -> None:
        if progress:
            progress(msg)

    role_names = ", ".join(r for r, _ in roles)
    _log(f"/autoorg started — roles: {role_names}")
    _log(f"Focus: {task or '(self-directed organisation-wide improvement)'}")
    _log(f"Stop anytime with Ctrl-C, or `touch {state.stop_file}` from another shell.")

    try:
        while True:
            stop, reason = state.should_stop()
            if stop:
                _log(f"/autoorg stopping ({reason})")
                break
            if max_iterations is not None and state.iteration >= max_iterations:
                _log(f"/autoorg reached max_iterations={max_iterations}; stopping")
                break

            state.iteration += 1
            _log(f"── org iteration {state.iteration} ──")

            role_results: list[dict] = []
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                futures = {}
                for role_name, role_brief in roles:
                    prompt = _role_iteration_prompt(
                        role_name, role_brief, task, state.iteration
                    )
                    futures[pool.submit(_safe_role, run_one_role, role_name,
                                        prompt, state)] = role_name
                for fut in as_completed(futures):
                    role_name = futures[fut]
                    try:
                        entry = fut.result()
                    except Exception as exc:
                        entry = {"role": role_name, "error": str(exc)}
                    role_results.append(entry)
                    _log(f"  ✓ {role_name} done")

            state.record({"iteration": state.iteration, "roles": role_results})
            time.sleep(iteration_delay_seconds)
    except KeyboardInterrupt:
        _log("/autoorg cancelled by user (Ctrl-C)")

    _log(f"/autoorg done: {state.iteration} iterations completed in "
         f"{time.time() - state.started_at:.0f}s")
    return state


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _safe_subtask(fn: Callable[[str, LoopState], dict], sub: str,
                  state: LoopState) -> dict:
    try:
        return fn(sub, state)
    except Exception as exc:
        return {"subtask": sub, "error": str(exc)}


def _safe_role(fn: Callable[[str, str, LoopState], dict], role: str,
               prompt: str, state: LoopState) -> dict:
    try:
        return fn(role, prompt, state)
    except Exception as exc:
        return {"role": role, "error": str(exc)}


def _stagnated(history: Sequence[dict], window: int) -> bool:
    """True when the last `window` iterations all share the same response
    fingerprint — a strong signal the model is stuck."""
    if len(history) < window:
        return False
    recent = history[-window:]
    fingerprints = [
        e.get("response_hash") or e.get("error") or str(sorted(e.items()))[:200]
        for e in recent
    ]
    return len(set(fingerprints)) == 1


__all__ = [
    "DEFAULT_ORG_ROLES",
    "LoopState",
    "run_autofleet_loop",
    "run_autoorg_loop",
    "run_autopolit_loop",
]
