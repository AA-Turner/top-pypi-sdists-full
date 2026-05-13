"""Tests for the autonomous loop primitives used by /autopolit, /autofleet, /autoorg.

Every test uses a stub iteration callback so the loop completes in
milliseconds. The point is to pin the loop semantics — iteration count,
cancel behaviour, stop-file detection, parallelism, role assignment,
stagnation detection — not the LLM behaviour itself.
"""

from __future__ import annotations

import threading
import time
from pathlib import Path

import pytest

from sage.core.autonomous import (
    DEFAULT_ORG_ROLES,
    LoopState,
    run_autofleet_loop,
    run_autoorg_loop,
    run_autopolit_loop,
)


# ---------------------------------------------------------------------------
# /autopolit
# ---------------------------------------------------------------------------


class TestAutopolitLoop:
    def test_runs_n_iterations_with_user_message(self, tmp_path: Path) -> None:
        calls: list[str] = []

        def step(prompt: str, state: LoopState) -> dict:
            calls.append(prompt)
            return {"iteration": state.iteration, "response_hash": str(state.iteration)}

        result = run_autopolit_loop(
            task="improve test coverage",
            project_root=tmp_path,
            run_one_iteration=step,
            max_iterations=5,
            iteration_delay_seconds=0,
        )
        assert result.iteration == 5
        # User-supplied focus appears in every iteration prompt
        for prompt in calls:
            assert "improve test coverage" in prompt
            assert "Autonomous iteration" in prompt

    def test_runs_with_no_message_uses_self_directed_prompt(self, tmp_path: Path) -> None:
        calls: list[str] = []

        def step(prompt: str, state: LoopState) -> dict:
            calls.append(prompt)
            return {"iteration": state.iteration, "response_hash": str(state.iteration)}

        run_autopolit_loop(
            task=None,
            project_root=tmp_path,
            run_one_iteration=step,
            max_iterations=3,
            iteration_delay_seconds=0,
        )
        # The self-directed prompt asks sage to pick its own focus + use TDD
        for prompt in calls:
            assert "No specific focus" in prompt
            assert "TDD" in prompt
            assert "Analyse the codebase" in prompt or "Analyse" in prompt

    def test_cancel_event_stops_loop_cleanly(self, tmp_path: Path) -> None:
        state_ref: dict = {}

        def step(prompt: str, state: LoopState) -> dict:
            state_ref["state"] = state
            if state.iteration == 2:
                state.cancel_event.set()
            return {"response_hash": str(state.iteration)}

        result = run_autopolit_loop(
            task=None,
            project_root=tmp_path,
            run_one_iteration=step,
            max_iterations=100,  # would run forever otherwise
            iteration_delay_seconds=0,
        )
        # Cancel-event set during iteration 2 → loop exits at top of iteration 3
        assert result.iteration == 2

    def test_stop_file_stops_loop(self, tmp_path: Path) -> None:
        def step(prompt: str, state: LoopState) -> dict:
            if state.iteration == 1:
                # Create the stop file mid-run from this thread
                state.stop_file.parent.mkdir(parents=True, exist_ok=True)
                state.stop_file.touch()
            return {"response_hash": str(state.iteration)}

        result = run_autopolit_loop(
            task=None,
            project_root=tmp_path,
            run_one_iteration=step,
            max_iterations=100,
            iteration_delay_seconds=0,
        )
        assert result.iteration == 1
        # Stop file is detected on the NEXT iteration's pre-check

    def test_keyboard_interrupt_exits_gracefully(self, tmp_path: Path) -> None:
        def step(prompt: str, state: LoopState) -> dict:
            if state.iteration == 2:
                raise KeyboardInterrupt
            return {"response_hash": str(state.iteration)}

        result = run_autopolit_loop(
            task="fix bugs",
            project_root=tmp_path,
            run_one_iteration=step,
            max_iterations=100,
            iteration_delay_seconds=0,
        )
        # KeyboardInterrupt during iteration 2 → loop exits; iteration counter
        # reflects the iteration where it was raised.
        assert result.iteration == 2

    def test_stagnation_detection_stops_repetition(self, tmp_path: Path) -> None:
        def step(prompt: str, state: LoopState) -> dict:
            return {"response_hash": "same-hash-every-time"}

        result = run_autopolit_loop(
            task=None,
            project_root=tmp_path,
            run_one_iteration=step,
            max_iterations=100,
            stagnation_window=3,
            iteration_delay_seconds=0,
        )
        # First 3 iterations record identical fingerprints → stagnation detected
        assert result.iteration == 3

    def test_stale_stop_file_is_cleared_on_start(self, tmp_path: Path) -> None:
        # Pre-existing stop file from a previous run
        stop_path = tmp_path / ".sage" / "AUTO-STOP"
        stop_path.parent.mkdir(parents=True)
        stop_path.touch()

        ran_at_least_once = {"flag": False}

        def step(prompt: str, state: LoopState) -> dict:
            ran_at_least_once["flag"] = True
            return {"response_hash": "x"}

        run_autopolit_loop(
            task=None,
            project_root=tmp_path,
            run_one_iteration=step,
            max_iterations=1,
            iteration_delay_seconds=0,
        )
        assert ran_at_least_once["flag"], "loop exited before any iteration"


# ---------------------------------------------------------------------------
# /autofleet
# ---------------------------------------------------------------------------


class TestAutofleetLoop:
    def test_decomposes_then_runs_subtasks_in_parallel(self, tmp_path: Path) -> None:
        active = {"count": 0, "max": 0}
        lock = threading.Lock()

        def decompose(task: str | None, state: LoopState) -> list[str]:
            return [f"subtask-{i}" for i in range(4)]

        def run_subtask(sub: str, state: LoopState) -> dict:
            with lock:
                active["count"] += 1
                active["max"] = max(active["max"], active["count"])
            time.sleep(0.02)
            with lock:
                active["count"] -= 1
            return {"subtask": sub, "ok": True}

        run_autofleet_loop(
            task=None,
            project_root=tmp_path,
            decompose=decompose,
            run_one_subtask=run_subtask,
            max_iterations=1,
            max_workers=4,
            iteration_delay_seconds=0,
        )
        # Parallelism actually used — multiple subtasks ran simultaneously
        assert active["max"] >= 2, (
            f"subtasks did not run in parallel; max concurrent={active['max']}"
        )

    def test_runs_indefinitely_until_cancelled(self, tmp_path: Path) -> None:
        iterations_done = {"n": 0}

        def decompose(task: str | None, state: LoopState) -> list[str]:
            return ["a", "b"]

        def run_subtask(sub: str, state: LoopState) -> dict:
            return {"subtask": sub}

        # Cancel from a background thread after ~50ms
        def cancel_soon(state_box: dict) -> None:
            time.sleep(0.05)
            if "state" in state_box:
                state_box["state"].cancel_event.set()

        state_box: dict = {}

        def decompose_track(task: str | None, state: LoopState) -> list[str]:
            state_box["state"] = state
            iterations_done["n"] += 1
            return ["a", "b"]

        thread = threading.Thread(target=cancel_soon, args=(state_box,), daemon=True)
        thread.start()

        result = run_autofleet_loop(
            task=None,
            project_root=tmp_path,
            decompose=decompose_track,
            run_one_subtask=run_subtask,
            max_iterations=None,  # truly indefinite — cancel is the only exit
            max_workers=2,
            iteration_delay_seconds=0,
        )
        thread.join()
        assert iterations_done["n"] >= 1
        assert result.iteration >= 1

    def test_subtask_exception_does_not_break_loop(self, tmp_path: Path) -> None:
        def decompose(task: str | None, state: LoopState) -> list[str]:
            return ["good", "bad", "also-good"]

        def run_subtask(sub: str, state: LoopState) -> dict:
            if sub == "bad":
                raise RuntimeError("oh no")
            return {"subtask": sub}

        result = run_autofleet_loop(
            task=None,
            project_root=tmp_path,
            decompose=decompose,
            run_one_subtask=run_subtask,
            max_iterations=1,
            iteration_delay_seconds=0,
        )
        # All three subtasks were recorded — the bad one as error, not crash
        results = result.history[0]["results"]
        assert len(results) == 3
        bad = next(r for r in results if r.get("subtask") == "bad")
        assert "error" in bad

    def test_user_message_propagates_to_decompose(self, tmp_path: Path) -> None:
        captured: list[str | None] = []

        def decompose(task: str | None, state: LoopState) -> list[str]:
            captured.append(task)
            return ["sub"]

        def run_subtask(sub: str, state: LoopState) -> dict:
            return {"subtask": sub}

        run_autofleet_loop(
            task="rebuild the auth layer",
            project_root=tmp_path,
            decompose=decompose,
            run_one_subtask=run_subtask,
            max_iterations=2,
            iteration_delay_seconds=0,
        )
        assert captured == ["rebuild the auth layer", "rebuild the auth layer"]


# ---------------------------------------------------------------------------
# /autoorg
# ---------------------------------------------------------------------------


class TestAutoorgLoop:
    def test_runs_each_role_per_iteration(self, tmp_path: Path) -> None:
        roles_seen: list[str] = []
        lock = threading.Lock()

        def run_role(role: str, prompt: str, state: LoopState) -> dict:
            with lock:
                roles_seen.append(role)
            return {"role": role}

        run_autoorg_loop(
            task="ship the dashboard MVP",
            project_root=tmp_path,
            run_one_role=run_role,
            max_iterations=1,
            iteration_delay_seconds=0,
        )
        for role, _ in DEFAULT_ORG_ROLES:
            assert role in roles_seen, f"role {role!r} did not run"

    def test_role_prompts_include_role_perspective_and_user_message(
        self, tmp_path: Path
    ) -> None:
        prompts_by_role: dict[str, str] = {}
        lock = threading.Lock()

        def run_role(role: str, prompt: str, state: LoopState) -> dict:
            with lock:
                prompts_by_role[role] = prompt
            return {"role": role}

        run_autoorg_loop(
            task="ship the dashboard MVP",
            project_root=tmp_path,
            run_one_role=run_role,
            max_iterations=1,
            iteration_delay_seconds=0,
        )
        for role, _ in DEFAULT_ORG_ROLES:
            prompt = prompts_by_role[role]
            assert role in prompt
            assert "ship the dashboard MVP" in prompt

    def test_runs_with_no_message_self_directed(self, tmp_path: Path) -> None:
        prompts: list[str] = []
        lock = threading.Lock()

        def run_role(role: str, prompt: str, state: LoopState) -> dict:
            with lock:
                prompts.append(prompt)
            return {"role": role}

        run_autoorg_loop(
            task=None,
            project_root=tmp_path,
            run_one_role=run_role,
            max_iterations=1,
            iteration_delay_seconds=0,
        )
        # Each role gets its own brief, no user focus injected
        assert len(prompts) == len(DEFAULT_ORG_ROLES)
        for p in prompts:
            assert "User focus" not in p

    def test_cancel_stops_after_current_iteration(self, tmp_path: Path) -> None:
        iter_count = {"n": 0}
        lock = threading.Lock()

        def run_role(role: str, prompt: str, state: LoopState) -> dict:
            with lock:
                iter_count["n"] += 1
            # Cancel after the very first role completes
            state.cancel_event.set()
            return {"role": role}

        result = run_autoorg_loop(
            task=None,
            project_root=tmp_path,
            run_one_role=run_role,
            max_iterations=100,
            iteration_delay_seconds=0,
        )
        # The first iteration completes (all roles in parallel), then the loop
        # checks cancel and exits.
        assert result.iteration == 1
        assert iter_count["n"] >= 1

    def test_roles_run_in_parallel(self, tmp_path: Path) -> None:
        active = {"count": 0, "max": 0}
        lock = threading.Lock()

        def run_role(role: str, prompt: str, state: LoopState) -> dict:
            with lock:
                active["count"] += 1
                active["max"] = max(active["max"], active["count"])
            time.sleep(0.02)
            with lock:
                active["count"] -= 1
            return {"role": role}

        run_autoorg_loop(
            task=None,
            project_root=tmp_path,
            run_one_role=run_role,
            max_iterations=1,
            max_workers=6,
            iteration_delay_seconds=0,
        )
        assert active["max"] >= 2, (
            f"org roles did not run in parallel; max concurrent={active['max']}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
