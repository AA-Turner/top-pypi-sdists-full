"""Tests for CommitResult."""

from agentic_devtools.models.git_results import BlockedState, CommitResult


class TestCommitResult:
    """Tests for CommitResult dataclass."""

    def test_defaults_represent_unpushed_non_noop_result(self):
        """CommitResult defaults optional commit fields and booleans."""
        result = CommitResult()

        assert result.commit_sha is None
        assert result.commit_message_title is None
        assert result.is_amend is None
        assert result.push_succeeded is False
        assert result.no_op is False
        assert result.error is None

    def test_stores_success_fields(self):
        """CommitResult stores commit success details."""
        result = CommitResult(
            commit_sha="abc123",
            commit_message_title="test(#1900): add coverage",
            is_amend=True,
            push_succeeded=True,
            no_op=False,
        )

        assert result.commit_sha == "abc123"
        assert result.commit_message_title == "test(#1900): add coverage"
        assert result.is_amend is True
        assert result.push_succeeded is True
        assert result.no_op is False

    def test_stores_noop_and_error_outcomes(self):
        """CommitResult can represent no-op and structured error outcomes."""
        noop = CommitResult(no_op=True)
        error = BlockedState(category="protection", message="push rejected")
        failed = CommitResult(error=error)

        assert noop.no_op is True
        assert failed.error is error
