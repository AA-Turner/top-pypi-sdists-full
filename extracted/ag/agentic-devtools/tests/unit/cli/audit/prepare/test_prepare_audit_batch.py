"""Tests for prepare_audit_batch() with mocked provider."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.audit.models import ClaimResult, ClosedPRInfo
from agentic_devtools.cli.audit.prepare import prepare_audit_batch
from agentic_devtools.cli.ci.models import ReviewCommentInfo


class TestPrepareAuditBatch:
    """Tests for prepare_audit_batch() covering claim loop and skip-on-ALREADY_CLAIMED."""

    def _make_provider(self, prs: list[ClosedPRInfo], comments: list[ReviewCommentInfo] | None = None) -> MagicMock:
        provider = MagicMock()
        provider.list_closed_prs.return_value = prs
        provider.claim_pr_for_audit.return_value = ClaimResult.CLAIMED
        provider.list_all_review_comments.return_value = comments or []
        provider.remove_label = MagicMock()
        provider.add_label = MagicMock()
        return provider

    def _make_prs(self, count: int) -> list[ClosedPRInfo]:
        return [
            ClosedPRInfo(
                number=i + 1,
                title=f"PR #{i + 1}",
                url=f"https://github.com/org/repo/pull/{i + 1}",
                state="closed",
                closed_at=f"2024-01-{15 - i:02d}T10:00:00Z",
                merged=True,
            )
            for i in range(count)
        ]

    @patch("agentic_devtools.state.get_state_dir")
    def test_successful_preparation(self, mock_state_dir, tmp_path) -> None:
        mock_state_dir.return_value = tmp_path
        prs = self._make_prs(3)
        comments = [
            ReviewCommentInfo(
                id=1,
                path="src/main.py",
                body="Fix validation",
                html_url="",
                diff_hunk="@@ hunk",
                author_login="reviewer1",
            ),
        ]
        provider = self._make_provider(prs, comments)

        batch = prepare_audit_batch(provider, 3, str(tmp_path))

        assert batch.status == "ready"
        assert len(batch.pr_numbers) == 3
        assert batch.batch_id != ""

    @patch("agentic_devtools.state.get_state_dir")
    def test_skips_already_claimed(self, mock_state_dir, tmp_path) -> None:
        mock_state_dir.return_value = tmp_path
        prs = self._make_prs(5)
        provider = self._make_provider(prs)
        # First 2 already claimed, next 3 succeed
        provider.claim_pr_for_audit.side_effect = [
            ClaimResult.ALREADY_CLAIMED,
            ClaimResult.ALREADY_CLAIMED,
            ClaimResult.CLAIMED,
            ClaimResult.CLAIMED,
            ClaimResult.CLAIMED,
        ]

        batch = prepare_audit_batch(provider, 3, str(tmp_path))

        assert batch.status == "ready"
        assert len(batch.pr_numbers) == 3
        # PRs 1 and 2 were skipped
        assert 1 not in batch.pr_numbers
        assert 2 not in batch.pr_numbers

    @patch("agentic_devtools.state.get_state_dir")
    def test_empty_batch_when_no_eligible(self, mock_state_dir, tmp_path) -> None:
        mock_state_dir.return_value = tmp_path
        provider = self._make_provider([])

        batch = prepare_audit_batch(provider, 10, str(tmp_path))

        assert batch.status == "empty"
        assert batch.pr_numbers == []

    @patch("agentic_devtools.state.get_state_dir")
    def test_claim_loop_breaks_at_batch_size(self, mock_state_dir, tmp_path) -> None:
        mock_state_dir.return_value = tmp_path
        prs = self._make_prs(10)
        provider = self._make_provider(prs)

        batch = prepare_audit_batch(provider, 3, str(tmp_path))

        assert batch.status == "ready"
        assert len(batch.pr_numbers) == 3
        assert provider.claim_pr_for_audit.call_count == 3

    @patch("agentic_devtools.state.get_state_dir")
    def test_collects_comments_with_empty_path(self, mock_state_dir, tmp_path) -> None:
        mock_state_dir.return_value = tmp_path
        prs = self._make_prs(1)
        comments = [
            ReviewCommentInfo(
                id=1,
                path="",
                body="General feedback",
                html_url="",
                diff_hunk="",
                author_login="reviewer1",
            ),
        ]
        provider = self._make_provider(prs, comments)

        batch = prepare_audit_batch(provider, 1, str(tmp_path))

        assert batch.status == "ready"
        assert batch.pr_numbers == [1]

    @patch("agentic_devtools.state.get_state_dir")
    @patch("agentic_devtools.cli.audit.prepare.cleanup_failed_batch")
    @patch(
        "agentic_devtools.cli.audit.prepare.detect_stale_comments",
        side_effect=RuntimeError("staleness failure"),
    )
    def test_cleanup_on_exception_after_claims(
        self,
        mock_detect_stale,
        mock_cleanup,
        mock_state_dir,
        tmp_path,
    ) -> None:
        mock_state_dir.return_value = tmp_path
        prs = self._make_prs(3)
        provider = self._make_provider(prs)

        with pytest.raises(RuntimeError, match="staleness failure"):
            prepare_audit_batch(provider, 3, str(tmp_path))

        mock_cleanup.assert_called_once_with(provider, [1, 2, 3], [1, 2, 3])
        assert mock_detect_stale.called is True

    @patch("agentic_devtools.state.get_state_dir")
    def test_cleanup_on_failure(self, mock_state_dir, tmp_path) -> None:
        mock_state_dir.return_value = tmp_path
        prs = self._make_prs(3)
        provider = self._make_provider(prs)
        provider.list_all_review_comments.side_effect = RuntimeError("API Error")

        batch = prepare_audit_batch(provider, 3, str(tmp_path))

        # All PRs failed data collection, so batch should be empty of processed PRs
        assert batch.status == "ready"
        assert batch.pr_numbers == []
        # In-progress labels should have been removed from the failed PRs
        assert provider.remove_label.called
