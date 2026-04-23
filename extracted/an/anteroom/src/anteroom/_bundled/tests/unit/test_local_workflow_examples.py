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
