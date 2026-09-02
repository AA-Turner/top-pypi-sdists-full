"""Tests for run_tree_mode (spawned tree-mode task target, issue #2117)."""

from unittest.mock import patch

from agentic_devtools.cli.jira import create_epic_router
from agentic_devtools.cli.jira.create_epic_router import run_tree_mode


def test_emits_routing_record_then_forwards(capsys):
    with patch("agentic_devtools.cli.jira.tree_mode_commands.create_epic_tree") as tree:
        run_tree_mode(
            "plan.json",
            start_from="feat-1",
            provider="github",
            dry_run=True,
            basis=create_epic_router.BASIS_FILE_OVERRIDES_LEGACY,
        )

    out = capsys.readouterr().out
    assert '"event": "create_epic.routing"' in out
    assert '"basis": "file_overrides_legacy_state"' in out
    tree.assert_called_once_with("plan.json", start_from="feat-1", provider="github", dry_run=True)


def test_defaults_use_file_present_basis(capsys):
    with patch("agentic_devtools.cli.jira.tree_mode_commands.create_epic_tree") as tree:
        run_tree_mode("plan.json")
    assert '"basis": "file_present"' in capsys.readouterr().out
    tree.assert_called_once_with("plan.json", start_from=None, provider=None, dry_run=False)


class TestRunTreeModeDelegationSemantics:
    """T058 — routing record precedes delegation; pipeline errors propagate (FR-010)."""

    def test_record_emitted_before_delegation(self, capsys):
        import pytest

        # create_epic_tree raises; the routing record must already be emitted.
        with patch(
            "agentic_devtools.cli.jira.tree_mode_commands.create_epic_tree",
            side_effect=RuntimeError("boom"),
        ):
            with pytest.raises(RuntimeError):
                run_tree_mode("plan.json")
        assert '"event": "create_epic.routing"' in capsys.readouterr().out

    def test_pipeline_validation_error_propagates(self):
        import pytest

        from agentic_devtools.cli.jira.creation_pipeline import PipelineValidationError

        with patch(
            "agentic_devtools.cli.jira.tree_mode_commands.create_epic_tree",
            side_effect=PipelineValidationError("bad tree"),
        ):
            with pytest.raises(PipelineValidationError):
                run_tree_mode("plan.json")

    def test_pipeline_execution_error_propagates(self):
        import pytest

        from agentic_devtools.adapters.operation_plan import OperationPlan
        from agentic_devtools.cli.jira.creation_pipeline import PipelineExecutionError

        err = PipelineExecutionError(
            cause=RuntimeError("adapter down"),
            operation_type="create_issue",
            refs=("e1",),
            stage="create_issue",
            created_result=None,
            partial_plan=OperationPlan(operations=(), dry_run=False, check_existing=False),
        )
        with patch("agentic_devtools.cli.jira.tree_mode_commands.create_epic_tree", side_effect=err):
            with pytest.raises(PipelineExecutionError):
                run_tree_mode("plan.json")
