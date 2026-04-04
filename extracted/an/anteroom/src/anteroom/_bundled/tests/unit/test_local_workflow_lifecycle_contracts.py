"""Contract tests for lifecycle-specific local workflow definitions."""

from __future__ import annotations

from pathlib import Path

from anteroom.services.workflow_engine import WorkflowStepDef, load_definition

_ROOT = Path(__file__).resolve().parents[2]


def _load_workflow(relative_path: str):
    path = _ROOT / relative_path
    return load_definition(path.read_text(encoding="utf-8"))


def _flatten_steps(steps: list[WorkflowStepDef]) -> list[WorkflowStepDef]:
    flat: list[WorkflowStepDef] = []
    for step in steps:
        flat.append(step)
        if step.steps:
            flat.extend(_flatten_steps(step.steps))
        if step.on_failure:
            flat.extend(_flatten_steps(step.on_failure))
    return flat


def test_issue_delivery_keeps_fresh_issue_contract() -> None:
    definition = _load_workflow("examples/workflows/local_claude_codex_issue_delivery.yaml")
    steps = _flatten_steps(definition.steps)
    step_ids = {step.id for step in steps}
    plan_loop = next(step for step in steps if step.id == "plan_loop")
    existing_work_loop = next(step for step in steps if step.id == "existing_work_loop")
    review_plan = next(step for step in steps if step.id == "review_plan")
    review_existing_work = next(step for step in steps if step.id == "review_existing_work")
    initial_checks = next(step for step in steps if step.id == "initial_checks")
    implement_issue = next(step for step in steps if step.id == "implement_issue")

    assert definition.id == "local_claude_codex_issue_delivery"
    assert {
        "assess_existing_work",
        "plan_loop",
        "existing_work_loop",
        "gate_plan_approved",
        "implement_issue",
        "capture_baseline",
        "initial_sync",
        "open_pr",
        "pr_review_loop",
        "assert_pr_fresh",
        "assert_pr_mergeable",
    } <= step_ids
    assert plan_loop.max_rounds == 3
    assert plan_loop.when == {
        "step": "assess_existing_work",
        "field": "result_summary",
        "not_equals": "existing_work_present",
    }
    assert existing_work_loop.when == {
        "step": "assess_existing_work",
        "field": "result_summary",
        "equals": "existing_work_present",
    }
    assert review_plan.timeout == 360
    assert review_existing_work.timeout == 360
    assert implement_issue.when == {
        "step": "assess_existing_work",
        "field": "result_summary",
        "not_equals": "existing_work_present",
    }
    assert "--allow-baseline" in (initial_checks.argv or [])


def test_pr_repair_targets_existing_pr_without_replanning() -> None:
    definition = _load_workflow("examples/workflows/local_claude_codex_pr_repair.yaml")
    steps = _flatten_steps(definition.steps)
    step_ids = {step.id for step in steps}

    assert definition.id == "local_claude_codex_pr_repair"
    assert {"assert_pr_fresh", "assert_pr_mergeable", "pr_review_loop", "assert_pr_approved"} <= step_ids
    assert {"plan_loop", "draft_plan", "gate_plan_approved", "implement_issue", "open_pr"} & step_ids == set()
    assert any(step.id == "fix_pr" and step.runner == "python_script" for step in steps)


def test_pr_refresh_focuses_on_refresh_and_validation_only() -> None:
    definition = _load_workflow("examples/workflows/local_claude_pr_refresh.yaml")
    steps = _flatten_steps(definition.steps)
    step_ids = {step.id for step in steps}

    assert definition.id == "local_claude_pr_refresh"
    assert {"refresh_pr", "refresh_checks_loop", "refresh_sync", "assert_pr_fresh", "assert_pr_mergeable"} <= step_ids
    assert {"review_pr", "fix_pr", "open_pr", "plan_loop", "implement_issue", "assert_pr_approved"} & step_ids == set()
    assert any(step.id == "refresh_pr" and step.runner == "python_script" for step in steps)


def test_pr_review_only_stays_python_review_without_claude_repair() -> None:
    definition = _load_workflow("examples/workflows/local_codex_pr_review_only.yaml")
    steps = _flatten_steps(definition.steps)
    step_ids = {step.id for step in steps}

    assert definition.id == "local_codex_pr_review_only"
    assert {"assert_pr_fresh", "assert_pr_mergeable", "ensure_pr_ready", "review_pr", "assert_pr_approved"} <= step_ids
    assert {"fix_pr", "refresh_pr", "open_pr", "plan_loop", "implement_issue"} & step_ids == set()
    assert all(step.runner != "cli_claude" for step in steps if step.type == "runner")


def test_local_workflows_have_no_agent_runners() -> None:
    """All local_*.yaml workflows must use python_script or shell runners, never cli_claude or cli_codex."""
    examples_dir = _ROOT / "examples" / "workflows"
    agent_runners = {"cli_claude", "cli_codex"}
    violations: list[str] = []

    for yaml_path in sorted(examples_dir.glob("local_*.yaml")):
        definition = load_definition(yaml_path.read_text(encoding="utf-8"))
        for step in _flatten_steps(definition.steps):
            if step.type == "runner" and step.runner in agent_runners:
                violations.append(f"{yaml_path.name}:{step.id} uses runner={step.runner}")

    assert violations == [], f"Agent runners found in local workflows: {violations}"


def test_issue_delivery_check_steps_bind_to_prepared_worktree_contract() -> None:
    definition = _load_workflow("examples/workflows/local_claude_codex_issue_delivery.yaml")
    steps = {step.id: step for step in _flatten_steps(definition.steps)}

    for step_id in {"initial_checks", "autofix_checks"}:
        step = steps[step_id]
        assert step.working_dir == "{prepare_issue.summary}"

    assert steps["initial_sync"].working_dir == "{prepare_issue.summary}"


def test_issue_delivery_capture_baseline_uses_helper_script() -> None:
    definition = _load_workflow("examples/workflows/local_claude_codex_issue_delivery.yaml")
    steps = {step.id: step for step in _flatten_steps(definition.steps)}
    capture = steps["capture_baseline"]

    assert capture.runner == "python_script"
    assert capture.command == "scripts/workflows/local_cli_issue_flow.py"
    assert capture.argv == ["capture-baseline", "--issue", "{issue_number}"]
