"""Tests for reclaim_one_eval_pr()."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.cli.audit.takeover import reclaim_one_eval_pr


class TestReclaimOneEvalPr:
    """Tests for the squash-preferred / takeover-fallback reclaim of one eval PR."""

    def test_returns_squashed_when_squash_succeeds(self) -> None:
        provider = MagicMock()
        outcome = reclaim_one_eval_pr(
            provider,
            pr_number=1,
            base_branch="main",
            head_branch="copilot/x",
            head_sha="sha1",
        )
        assert outcome == "squashed"
        provider.squash_before_publish.assert_called_once_with(
            pr_number=1, base_branch="main", head_branch="copilot/x", head_sha="sha1"
        )
        provider.reclaim_copilot_commit.assert_not_called()

    def test_falls_back_to_takeover_when_squash_raises(self) -> None:
        provider = MagicMock()
        provider.squash_before_publish.side_effect = RuntimeError("lease race")
        outcome = reclaim_one_eval_pr(
            provider,
            pr_number=2,
            base_branch="main",
            head_branch="copilot/y",
            head_sha="sha2",
        )
        assert outcome == "takeover"
        provider.reclaim_copilot_commit.assert_called_once_with(pr_number=2, head_branch="copilot/y", head_sha="sha2")

    def test_returns_failed_when_both_raise(self) -> None:
        provider = MagicMock()
        provider.squash_before_publish.side_effect = RuntimeError("boom")
        provider.reclaim_copilot_commit.side_effect = RuntimeError("nope")
        outcome = reclaim_one_eval_pr(
            provider,
            pr_number=3,
            base_branch="main",
            head_branch="copilot/z",
            head_sha="sha3",
        )
        assert outcome == "failed"
