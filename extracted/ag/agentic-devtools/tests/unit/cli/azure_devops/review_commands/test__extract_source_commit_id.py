"""Tests for _extract_source_commit_id."""

from agentic_devtools.cli.azure_devops.review_commands import _extract_source_commit_id


class TestExtractSourceCommitId:
    """Tests for _extract_source_commit_id."""

    def test_returns_none_when_last_merge_source_commit_not_dict(self) -> None:
        """Non-dict lastMergeSourceCommit is treated as missing."""
        details = {"pullRequest": {"lastMergeSourceCommit": None}}

        assert _extract_source_commit_id(details) is None

    def test_returns_none_when_commit_id_not_string(self) -> None:
        """Non-string commitId is rejected."""
        details = {"pullRequest": {"lastMergeSourceCommit": {"commitId": 123}}}

        assert _extract_source_commit_id(details) is None

    def test_returns_none_when_commit_id_is_blank(self) -> None:
        """Whitespace-only commitId is rejected."""
        details = {"pullRequest": {"lastMergeSourceCommit": {"commitId": "   "}}}

        assert _extract_source_commit_id(details) is None
