"""Tests for the local work-item router workflow."""

from __future__ import annotations

from pathlib import Path

from anteroom.services.workflow_engine import WorkflowEngine, load_definition

_ROOT = Path(__file__).resolve().parents[2]


def _load_router():
    path = _ROOT / "examples/workflows/local_work_item_router.yaml"
    return load_definition(path.read_text(encoding="utf-8"))


def test_router_workflow_loads_and_routes_all_lifecycle_states() -> None:
    definition = _load_router()
    steps = {step.id: step for step in definition.steps}
    required_steps = {
        "prepare_issue",
        "inspect_pr",
        "route_issue_delivery",
        "route_pr_repair",
        "route_pr_refresh",
        "route_pr_review_only",
    }

    assert definition.id == "local_work_item_router"
    assert required_steps <= set(steps)

    expected = {
        "route_issue_delivery": '"lifecycle": "no_pr"',
        "route_pr_repair": '"lifecycle": "review_repair"',
        "route_pr_refresh": '"lifecycle": "refresh_needed"',
        "route_pr_review_only": '"lifecycle": "review_only"',
    }
    for step_id, substring in expected.items():
        when = steps[step_id].when
        assert when is not None
        assert when["step"] == "inspect_pr"
        assert when["field"] == "result_summary"
        assert when["contains"] == substring


def test_router_when_clauses_dispatch_exclusively() -> None:
    definition = _load_router()
    route_steps = {step.id: step for step in definition.steps if step.id.startswith("route_")}
    lifecycle_to_step = {
        "no_pr": "route_issue_delivery",
        "review_repair": "route_pr_repair",
        "refresh_needed": "route_pr_refresh",
        "review_only": "route_pr_review_only",
    }

    for lifecycle, expected_step in lifecycle_to_step.items():
        summary = f'{{"lifecycle": "{lifecycle}"}}'
        results = {"inspect_pr": {"result_summary": summary}}
        matched = {
            step_id for step_id, step in route_steps.items() if WorkflowEngine._evaluate_when(step.when, results)
        }
        assert matched == {expected_step}


def test_router_routes_to_expected_workflow_paths() -> None:
    definition = _load_router()
    commands = {step.id: step.command for step in definition.steps if step.id.startswith("route_")}

    assert "./examples/workflows/local_claude_codex_issue_delivery.yaml" in commands["route_issue_delivery"]
    assert "./examples/workflows/local_claude_codex_pr_repair.yaml" in commands["route_pr_repair"]
    assert "./examples/workflows/local_claude_pr_refresh.yaml" in commands["route_pr_refresh"]
    assert "./examples/workflows/local_codex_pr_review_only.yaml" in commands["route_pr_review_only"]
