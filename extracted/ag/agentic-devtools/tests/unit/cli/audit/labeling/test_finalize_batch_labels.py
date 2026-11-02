"""Tests for label lifecycle management."""

from unittest.mock import MagicMock

from agentic_devtools.cli.audit.config import LABEL_AUDITED, LABEL_IN_PROGRESS
from agentic_devtools.cli.audit.labeling import cleanup_failed_batch, finalize_batch_labels


class TestFinalizeBatchLabels:
    """Tests for finalize_batch_labels() — FR-003 label lifecycle."""

    def test_removes_in_progress_adds_audited(self) -> None:
        provider = MagicMock()
        finalize_batch_labels(provider, [1, 2, 3])

        assert provider.remove_label.call_count == 3
        assert provider.add_label.call_count == 3
        provider.remove_label.assert_any_call(1, LABEL_IN_PROGRESS)
        provider.add_label.assert_any_call(1, LABEL_AUDITED)

    def test_continues_on_individual_failure(self) -> None:
        provider = MagicMock()
        provider.remove_label.side_effect = [RuntimeError("fail"), None, None]

        # Should not raise
        finalize_batch_labels(provider, [1, 2, 3])
        # Still tries all PRs
        assert provider.add_label.call_count == 3

    def test_continues_when_add_label_fails(self) -> None:
        provider = MagicMock()
        provider.add_label.side_effect = RuntimeError("fail")

        finalize_batch_labels(provider, [1, 2])

        assert provider.remove_label.call_count == 2
        assert provider.add_label.call_count == 2

    def test_empty_pr_list(self) -> None:
        provider = MagicMock()
        finalize_batch_labels(provider, [])
        provider.remove_label.assert_not_called()
        provider.add_label.assert_not_called()


class TestCleanupFailedBatch:
    """Tests for cleanup_failed_batch() — FR-003 failure cleanup."""

    def test_removes_in_progress_from_unprocessed(self) -> None:
        provider = MagicMock()
        cleanup_failed_batch(provider, claimed_prs=[1, 2, 3], processed_prs=[1])

        # Should remove in-progress from PRs 2 and 3 only
        calls = provider.remove_label.call_args_list
        removed_prs = {c[0][0] for c in calls}
        assert removed_prs == {2, 3}

    def test_all_processed_no_cleanup(self) -> None:
        provider = MagicMock()
        cleanup_failed_batch(provider, claimed_prs=[1, 2], processed_prs=[1, 2])
        provider.remove_label.assert_not_called()

    def test_continues_on_failure(self) -> None:
        provider = MagicMock()
        provider.remove_label.side_effect = RuntimeError("fail")
        # Should not raise
        cleanup_failed_batch(provider, claimed_prs=[1, 2], processed_prs=[])
