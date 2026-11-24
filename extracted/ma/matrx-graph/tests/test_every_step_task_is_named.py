"""Every step invocation runs in a NAMED asyncio task, so a frozen loop names the step.

2026-11-02 run f2bf5df1: the ``voice`` step held the worker's loop 10.8 s; the loop watchdog files the
task holding the loop, and an unnamed ``Task-8812`` names nothing.
"""

from __future__ import annotations

import ast
from pathlib import Path

from matrx_graph.executor.scheduler import step_task_name

_SCHEDULER = Path(__file__).parents[1] / "matrx_graph" / "executor" / "scheduler.py"


def test_every_invocation_task_carries_a_name() -> None:
    tree = ast.parse(_SCHEDULER.read_text())
    spawns = [
        call
        for call in ast.walk(tree)
        if isinstance(call, ast.Call)
        and getattr(call.func, "attr", "") == "create_task"
        and call.args
        and isinstance(call.args[0], ast.Call)
        and getattr(call.args[0].func, "attr", "") == "_run_invocation"
    ]
    assert spawns, "no step spawn found — the guard lost its target"
    unnamed = [c.lineno for c in spawns if not any(k.arg == "name" for k in c.keywords)]
    assert not unnamed, f"step tasks spawned without a name at lines {unnamed}"


def test_the_name_says_step_and_run() -> None:
    assert step_task_name("f2bf5df1-bad9-4a6c", "voice") == "workflow_step:voice:run=f2bf5df1"
