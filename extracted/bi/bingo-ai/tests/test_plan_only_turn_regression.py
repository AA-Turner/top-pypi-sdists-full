"""Regression tests for the "plan-only turn stops the mission" bug.

Symptom (v7.4.6 and earlier): a text-mode model (no native function calling,
e.g. a `custom` PackyCode aggregator serving `deepseek-v4-pro`) emits a
`<THINK>` plan with Step 1..N but no ```code block``` / TOOL_CALL. The loop
called ``_current_action_candidate`` which returned ``None`` because the task
graph had never been loaded (``load_template`` only ran on the target-detection
branch). ``reduce_mission(candidates=[])`` then reported an exhausted frontier
and the mission terminated on the very first planning turn — appearing to
"stall / go idle" with only the plan printed.

Root-cause fix (v7.4.7):
  1. ``_current_action_candidate`` self-loads the standard web-pentest template
     from the objective when the task graph is empty, so the action frontier is
     never *spuriously* empty.
  2. The text/TOOL_CALL execution path grants the same plan->execute nudge
     budget the FC path already had, instead of terminating immediately.

These tests exercise the state-owning pieces directly (no live model / network).
"""

from __future__ import annotations

from types import SimpleNamespace

from bingo.core.execution_runtime import (
    MissionRuntime,
    RuntimeDecision,
    reduce_mission,
)
from bingo.core.intelligence import TaskGraph
from bingo.ui.terminal import BingoTerminal


def test_task_graph_seeded_from_objective_exposes_recon_node() -> None:
    """An empty graph loaded from a mission objective must expose a ready node."""
    graph = TaskGraph()
    assert graph.ready_nodes() == []  # empty until seeded

    graph.load_template("https://www.example.test SQL injection, dump admin")
    ready = graph.ready_nodes()

    assert ready, "seeded graph must expose at least one ready node"
    # recon has no dependencies, so it is the first eligible frontier action.
    assert any(node.node_id == "recon" for node in ready)


def test_current_action_candidate_self_loads_empty_task_graph() -> None:
    """v7.4.7: candidate lookup seeds an empty graph from the objective.

    Before the fix this returned ``None`` (graph never loaded on the text-mode
    path) which collapsed the action frontier and ended the mission on the first
    planning turn.
    """
    stub = SimpleNamespace(
        _intel_ready=True,
        _task_graph=TaskGraph(),
        _agent_state={"target": "https://www.example.test"},
        _mission_runtime=MissionRuntime(
            objective="https://www.example.test SQLi -> admin password",
            target="https://www.example.test",
        ),
    )

    candidate = BingoTerminal._current_action_candidate(stub, "<THINK>Step 1..6 plan</THINK>")

    assert candidate is not None, "empty graph must self-seed and yield a candidate"
    assert candidate.node_id == "recon"
    assert candidate.target == "https://www.example.test"


def test_seeded_frontier_makes_reduce_mission_continue() -> None:
    """With a seeded frontier, reduce_mission must NOT report on the first turn."""
    stub = SimpleNamespace(
        _intel_ready=True,
        _task_graph=TaskGraph(),
        _agent_state={"target": "https://www.example.test"},
        _mission_runtime=MissionRuntime(
            objective="https://www.example.test SQLi",
            target="https://www.example.test",
        ),
    )

    candidate = BingoTerminal._current_action_candidate(stub, "plan only, no code")
    decision = reduce_mission(
        stub._mission_runtime,
        candidates=[candidate] if candidate else [],
    )

    assert decision in {RuntimeDecision.CONTINUE, RuntimeDecision.PIVOT}


def test_candidate_is_none_only_when_intel_engine_unavailable() -> None:
    """Without the intelligence engine the candidate is None (nudge path handles it)."""
    stub = SimpleNamespace(
        _intel_ready=False,
        _task_graph=TaskGraph(),
        _agent_state={"target": "https://www.example.test"},
        _mission_runtime=MissionRuntime(
            objective="anything",
            target="https://www.example.test",
        ),
    )

    assert BingoTerminal._current_action_candidate(stub, "plan") is None
