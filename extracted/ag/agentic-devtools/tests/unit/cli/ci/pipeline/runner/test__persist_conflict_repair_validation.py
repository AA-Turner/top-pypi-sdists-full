"""Tests for _persist_conflict_repair_validation."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.pipeline.runner import _persist_conflict_repair_validation
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestPersistConflictRepairValidation:
    """Unit tests for persisted post-repair validation markers."""

    def test_posts_validated_marker(self) -> None:
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"

        assert _persist_conflict_repair_validation(provider, 12, "feedbeef") is True

        provider.post_comment_as_pr_token.assert_called_once_with(
            12,
            "<!-- agdt:conflict-repair-validated:feedbeef -->",
        )

    def test_logs_and_continues_on_non_rate_limit_error(self, caplog: pytest.LogCaptureFixture) -> None:
        provider = MagicMock()
        provider.post_comment_as_pr_token.side_effect = RuntimeError("post failed")
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"

        assert _persist_conflict_repair_validation(provider, 12, "feedbeef") is False

        assert "Failed to persist validated conflict-repair baseline" in caplog.text

    def test_reraises_rate_limit_error(self) -> None:
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "feedbeef"
        provider.post_comment_as_pr_token.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )

        with pytest.raises(ProviderRateLimitError):
            _persist_conflict_repair_validation(provider, 12, "feedbeef")

    def test_skips_marker_when_live_head_changed(self, caplog: pytest.LogCaptureFixture) -> None:
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = "newhead00"

        _persist_conflict_repair_validation(provider, 12, "feedbeef")

        provider.post_comment_as_pr_token.assert_not_called()
        assert "Skipping validated conflict-repair baseline for stale HEAD" in caplog.text

    def test_metadata_lookup_failure_logs_and_skips_marker(self, caplog: pytest.LogCaptureFixture) -> None:
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = RuntimeError("metadata failed")

        _persist_conflict_repair_validation(provider, 12, "feedbeef")

        provider.post_comment_as_pr_token.assert_not_called()
        assert "Failed to verify live HEAD before persisting validated conflict-repair baseline" in caplog.text

    def test_missing_live_head_logs_and_skips_marker(self, caplog: pytest.LogCaptureFixture) -> None:
        provider = MagicMock()
        provider.get_pr_metadata.return_value.head_sha = ""

        _persist_conflict_repair_validation(provider, 12, "feedbeef")

        provider.post_comment_as_pr_token.assert_not_called()
        assert "live HEAD could not be confirmed" in caplog.text

    def test_reraises_rate_limit_from_metadata_lookup(self) -> None:
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )

        with pytest.raises(ProviderRateLimitError):
            _persist_conflict_repair_validation(provider, 12, "feedbeef")
