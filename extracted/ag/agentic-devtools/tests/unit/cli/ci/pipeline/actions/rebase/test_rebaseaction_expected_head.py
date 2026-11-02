"""Tests for expected-head checks and results in RebaseAction."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.actions.rebase import RebaseAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot


def _make_provider(*, head_sha: str = "abc123") -> MagicMock:
    """Create a provider with PR metadata matching the default snapshot."""
    provider = MagicMock()
    provider.get_pr_metadata.return_value = PRMetadata(
        number=42,
        title="",
        head_branch="feature/foo",
        head_sha=head_sha,
        base_branch="main",
    )
    return provider


def _make_snapshot(**kwargs: object) -> PRStateSnapshot:
    """Create a behind PR snapshot with the expected repair head."""
    values: dict[str, object] = {
        "pr_number": 42,
        "head_sha": "abc123",
        "base_branch": "main",
        "head_branch": "feature/foo",
        "commit_count": 1,
        "commits_behind": 2,
        "base_repo_full_name": "owner/repo",
    }
    values.update(kwargs)
    return PRStateSnapshot(**values)  # type: ignore[arg-type]


class TestRebaseActionExpectedHead:
    """Expected-head comparison and post-rebase reporting cases."""

    def test_execute_reports_new_head_on_success(self) -> None:
        """Successful rebase reports the returned HEAD for the refreshed snapshot."""
        snapshot = _make_snapshot(base_branch="develop")
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="",
            head_branch="feature/foo",
            head_sha="abc123",
            base_branch="develop",
        )
        provider.rebase_onto_base.return_value = "new-head"

        result = RebaseAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.invalidates_snapshot is True
        assert "expected head abc123" in result.details
        assert "new head new-head" in result.details
        provider.rebase_onto_base.assert_called_once_with(
            pr_number=42,
            base_branch="develop",
            head_branch="feature/foo",
            head_sha="abc123",
        )

    def test_execute_skips_and_reports_mismatched_live_head(self) -> None:
        """A stale expected head skips without asking the provider to rebase."""
        snapshot = _make_snapshot()
        provider = _make_provider(head_sha="def456")

        result = RebaseAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert "abc123" in result.details
        assert "def456" in result.details
        provider.rebase_onto_base.assert_not_called()

    def test_execute_reports_when_branch_is_no_longer_behind(self) -> None:
        """An unchanged head and no-op provider result report no update needed."""
        snapshot = _make_snapshot()
        provider = _make_provider()
        provider.rebase_onto_base.return_value = None

        result = RebaseAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert "no update was needed" in result.details.lower()
        assert result.preconditions["branch_still_behind"] is False
        assert provider.get_pr_metadata.call_count == 2

    def test_execute_reports_head_mismatch_after_provider_refetch(self) -> None:
        """A head changed during provider preflight is reported as a non-mutating skip."""
        snapshot = _make_snapshot()
        provider = _make_provider()
        provider.get_pr_metadata.side_effect = [
            PRMetadata(number=42, title="", head_branch="feature/foo", head_sha="abc123", base_branch="main"),
            PRMetadata(number=42, title="", head_branch="feature/foo", head_sha="def456", base_branch="main"),
        ]
        provider.rebase_onto_base.return_value = None

        result = RebaseAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert "abc123" in result.details
        assert "def456" in result.details
