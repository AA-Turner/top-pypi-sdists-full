"""Tests for the TakeOverAutomationCommitAction pipeline action."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.pipeline.actions.takeover import (
    TakeOverAutomationCommitAction,
    TakeOverCopilotCommitAction,
)
from agentic_devtools.cli.ci.pipeline.exceptions import ForceWithLeaseError
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.retry import ProviderRateLimitError

_SESSION_PATH = "agentic_devtools.cli.ci.pipeline.actions.takeover.is_copilot_session_active_via_agent_task"


class TestTakeOverAutomationCommitAction:
    """Tests for take-over action evaluation and execution."""

    def _make_snapshot(self, **kwargs: object) -> PRStateSnapshot:
        """Create a PRStateSnapshot with sensible defaults."""
        defaults: dict[str, object] = {
            "pr_number": 42,
            "head_sha": "abc123def456",
            "base_branch": "main",
            "head_branch": "feature/foo",
            "base_repo_full_name": "owner/repo",
            "head_author_login": "Copilot",
            "files": ["specs/1878/spec.md"],
        }
        defaults.update(kwargs)
        return PRStateSnapshot(**defaults)  # type: ignore[arg-type]

    def test_name_property(self) -> None:
        """name returns 'takeover'."""
        assert TakeOverAutomationCommitAction().name == "takeover"

    def test_does_not_set_runs_after_invalidation(self) -> None:
        """TakeOver is an early action and must not run after invalidation."""
        action = TakeOverAutomationCommitAction()
        assert not getattr(action, "runs_after_invalidation", False)

    @patch(_SESSION_PATH, return_value=False)
    def test_evaluate_skip_when_head_not_copilot_authored(self, _mock_session) -> None:
        """evaluate() SKIPs when HEAD author is a human login."""
        snapshot = self._make_snapshot(head_author_login="AMARSNIK_swica")
        result = TakeOverAutomationCommitAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["head_authored_by_takeover_author"] is False
        assert "AMARSNIK_swica" in result.details

    @patch(_SESSION_PATH, return_value=False)
    def test_evaluate_skip_when_head_author_unknown(self, _mock_session) -> None:
        """evaluate() SKIPs and labels an empty author as 'unknown'."""
        snapshot = self._make_snapshot(head_author_login="")
        result = TakeOverAutomationCommitAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert "unknown" in result.details

    @pytest.mark.parametrize(
        "files",
        [
            [".github/workflows/ai-pr-loop.yml"],
            ["agentic_devtools/cli/ci/pipeline/actions/takeover.py"],
            [".github/workflows/ai-pr-loop.yml", "agentic_devtools/cli/ci/pipeline/actions/takeover.py"],
        ],
    )
    @patch(_SESSION_PATH, return_value=False)
    def test_evaluate_execute_regardless_of_files_involved(self, _mock_session, files: list[str]) -> None:
        """evaluate() EXECUTEs regardless of which files changed in the PR."""
        snapshot = self._make_snapshot(files=files)
        result = TakeOverAutomationCommitAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert "no_workflow_file_changes" not in result.preconditions
        assert result.preconditions["no_active_session"] is True
        assert "workflow files changed" not in result.details.lower()

    @patch(_SESSION_PATH, return_value=True)
    def test_evaluate_skip_when_active_session(self, _mock_session) -> None:
        """evaluate() SKIPs when a Copilot coding session is active."""
        snapshot = self._make_snapshot()
        result = TakeOverAutomationCommitAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_active_session"] is False

    @patch(_SESSION_PATH, return_value=False)
    @pytest.mark.parametrize("head_author_login", ["copilot[bot]", "copilot-swe-agent[bot]", "github-actions[bot]"])
    def test_evaluate_execute_when_takeover_author_head_and_idle(self, _mock_session, head_author_login: str) -> None:
        """evaluate() EXECUTEs for an idle automation/Copilot-authored HEAD."""
        snapshot = self._make_snapshot(head_author_login=head_author_login)
        result = TakeOverAutomationCommitAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["head_authored_by_takeover_author"] is True
        assert head_author_login in result.details

    def test_execute_success_invalidates_snapshot(self) -> None:
        """execute() reclaims the commit and invalidates the snapshot."""
        snapshot = self._make_snapshot(files=[".github/workflows/ai-pr-loop.yml"])
        derived = DerivedState(snapshot)
        provider = MagicMock()

        result = TakeOverAutomationCommitAction().execute(provider, snapshot, derived)

        provider.reclaim_copilot_commit.assert_called_once_with(
            pr_number=42, head_branch="feature/foo", head_sha="abc123def456"
        )
        assert result.decision == ActionDecision.EXECUTE
        assert result.invalidates_snapshot is True
        assert derived.get("head_author_login") == ""

    def test_execute_force_with_lease_error_returns_failed(self) -> None:
        """execute() maps ForceWithLeaseError to FAILED with a concurrency hint."""
        snapshot = self._make_snapshot()
        provider = MagicMock()
        provider.reclaim_copilot_commit.side_effect = ForceWithLeaseError("lease rejected")

        result = TakeOverAutomationCommitAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.FAILED
        assert "concurrent update" in result.details.lower()
        assert result.error == "lease rejected"

    def test_execute_generic_error_returns_failed(self) -> None:
        """execute() maps unexpected errors to FAILED."""
        snapshot = self._make_snapshot()
        provider = MagicMock()
        provider.reclaim_copilot_commit.side_effect = RuntimeError("head moved")

        result = TakeOverAutomationCommitAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.FAILED
        assert result.details == "reclaim_copilot_commit failed"
        assert result.error == "head moved"

    def test_legacy_class_name_aliases_new_takeover_action(self) -> None:
        """The legacy takeover class name remains as a backwards-compatible alias."""
        assert TakeOverCopilotCommitAction is TakeOverAutomationCommitAction

    def test_execute_re_raises_rate_limit_error(self) -> None:
        snapshot = self._make_snapshot()
        provider = MagicMock()
        provider.reclaim_copilot_commit.side_effect = ProviderRateLimitError(is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            TakeOverAutomationCommitAction().execute(provider, snapshot, DerivedState(snapshot))
