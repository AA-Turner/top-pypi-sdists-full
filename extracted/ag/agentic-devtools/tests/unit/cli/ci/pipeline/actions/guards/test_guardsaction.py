"""Tests for GuardsAction."""

from typing import Any, cast
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.pipeline.actions.guards import GuardsAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot

MODULE = "agentic_devtools.cli.ci.pipeline.actions.guards"


class TestGuardsAction:
    """Tests for guard evaluation."""

    def test_rejects_unknown_guard_phase(self) -> None:
        with pytest.raises(ValueError, match="phase must be"):
            GuardsAction(phase=cast(Any, "invalid"))

    def test_safety_phase_does_not_block_failed_wip_recovery(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            is_draft=True,
            files=["src/main.py"],
            title="[WIP] work in progress",
        )

        result = GuardsAction(phase="safety").evaluate(snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.EXECUTE
        assert result.preconditions["not_fork"] is True

    def test_safety_phase_blocks_fork_before_progression_checks(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="attacker/repo",
            base_repo_full_name="org/repo",
            files=[],
            title="[WIP] work in progress",
        )

        result = GuardsAction(phase="safety").evaluate(snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.BLOCKED
        assert result.details == "PR is from a fork"

    def test_progression_phase_blocks_empty_pr(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=[],
            title="Normal title",
        )

        result = GuardsAction(phase="progression").evaluate(snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.BLOCKED
        assert result.details == "PR has no file changes"

    def test_progression_phase_leaves_safety_checks_to_safety_phase(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="attacker/repo",
            base_repo_full_name="org/repo",
            files=[".github/workflows/ci.yml"],
            title="Normal title",
        )

        result = GuardsAction(phase="progression").evaluate(snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.EXECUTE

    def test_all_guards_pass(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            labels=[],
            files=["src/main.py"],
            title="My PR",
        )
        derived = DerivedState(snapshot)
        action = GuardsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["not_fork"] is True
        assert result.preconditions["no_exclusion_label"] is True
        assert result.preconditions["not_wip"] is True
        assert result.preconditions["has_changes"] is True

    def test_wip_title_blocked(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=["src/main.py"],
            title="[WIP] work in progress",
        )
        derived = DerivedState(snapshot)
        action = GuardsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.BLOCKED
        assert "wip" in result.details.lower()

    def test_wip_title_blocked_case_insensitive(self) -> None:
        """[wip] in any case is also blocked."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=["src/main.py"],
            title="[wip] lowercase wip title",
        )
        derived = DerivedState(snapshot)
        action = GuardsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.BLOCKED

    def test_finished_nonempty_wip_draft_is_allowed_for_publish(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            is_draft=True,
            files=["src/main.py"],
            title="[WIP] completed work",
        )
        derived = DerivedState(snapshot)
        derived.set("latest_session_state", SessionState(SessionOutcome.FINISHED))
        result = GuardsAction().evaluate(snapshot, derived)
        assert result.decision is ActionDecision.EXECUTE
        assert result.preconditions["not_wip"] is True

    def test_wip_guard_resolves_latest_session_when_not_prepopulated(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            base_repo_full_name="org/repo",
            head_repo_full_name="org/repo",
            is_draft=True,
            files=["src/main.py"],
            title="[WIP] completed work",
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        derived.set("provider", provider)
        session_state = SessionState(SessionOutcome.FINISHED)
        with patch(f"{MODULE}.get_latest_session_state", return_value=session_state) as get_latest:
            result = GuardsAction().evaluate(snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert derived.get("latest_session_state") == session_state
        get_latest.assert_called_once_with(
            provider,
            1,
            repo="org/repo",
            head_branch="",
            pr_id=None,
            head_sha="",
        )

    def test_no_changes_blocked(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=[],
            title="Normal title",
        )
        derived = DerivedState(snapshot)
        action = GuardsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.BLOCKED
        assert "no file changes" in result.details.lower()

    def test_fork_pr_blocked(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="attacker/repo",
            base_repo_full_name="org/repo",
            files=["src/main.py"],
            title="Normal",
        )
        derived = DerivedState(snapshot)
        action = GuardsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.BLOCKED
        assert "fork" in result.details.lower()

    def test_exclusion_label_blocked(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            labels=["ai-pr-loop-ignore"],
            files=["src/main.py"],
            title="Normal",
        )
        derived = DerivedState(snapshot)
        action = GuardsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.BLOCKED
        assert "exclusion" in result.details.lower()

    def test_privileged_paths_blocked(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=[".github/workflows/ci.yml"],
            title="Normal",
        )
        derived = DerivedState(snapshot)
        action = GuardsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.BLOCKED
        assert "privileged" in result.details.lower()

    def test_docker_files_blocked(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            files=["Dockerfile"],
            title="Normal",
        )
        derived = DerivedState(snapshot)
        action = GuardsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.BLOCKED
        assert "docker" in result.details.lower()

    def test_execute_is_a_noop_success(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1)
        result = GuardsAction().execute(MagicMock(), snapshot, DerivedState(snapshot))
        assert result.decision is ActionDecision.EXECUTE
