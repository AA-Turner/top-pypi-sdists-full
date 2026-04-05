"""Contract tests for local workflow example definitions."""

from __future__ import annotations

from pathlib import Path

from anteroom.services.workflow_engine import load_definition

_ROOT = Path(__file__).resolve().parents[2]


def test_local_lifecycle_workflow_examples_load() -> None:
    examples = {
        "examples/workflows/local_work_item_router.yaml": "local_work_item_router",
        "examples/workflows/local_claude_codex_issue_delivery.yaml": "local_claude_codex_issue_delivery",
        "examples/workflows/local_claude_codex_pr_repair.yaml": "local_claude_codex_pr_repair",
        "examples/workflows/local_claude_pr_refresh.yaml": "local_claude_pr_refresh",
        "examples/workflows/local_codex_pr_review_only.yaml": "local_codex_pr_review_only",
    }

    for relative_path, expected_id in examples.items():
        path = _ROOT / relative_path
        definition = load_definition(path.read_text(encoding="utf-8"))
        assert definition.id == expected_id
        assert "issue_number" in definition.inputs


def test_issue_delivery_reference_workflow_uses_current_features() -> None:
    path = _ROOT / "examples" / "workflows" / "issue_delivery.yaml"
    definition = load_definition(path.read_text(encoding="utf-8"))
    steps = {step.id: step for step in definition.steps}
    fast_checks_loop = steps["fast_checks_loop"]
    review_loop = steps["review_loop"]
    open_pr = steps["open_pr"]

    assert definition.id == "issue_delivery"
    assert definition.policies["inject_rules"] is True
    assert definition.policies["inject_conventions"] is True
    assert definition.policies["budget"]["max_steps"] == 30
    assert {"start_work", "fast_checks_loop", "sync_for_pr", "open_pr", "review_loop", "final_checks"} <= steps.keys()
    assert fast_checks_loop.until == {"step": "run_checks", "field": "result_status", "equals": "success"}
    assert fast_checks_loop.stop_after_unchanged == 2
    assert review_loop.until == {"step": "review", "field": "result_findings", "is_empty": True}
    assert review_loop.stop_after_unchanged == 2
    assert open_pr.outputs == [{"name": "pr_url", "from": "result_summary"}]
