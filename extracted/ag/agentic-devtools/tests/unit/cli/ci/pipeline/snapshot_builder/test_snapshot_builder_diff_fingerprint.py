"""Tests for build_pr_state_snapshot."""

import logging
from types import MethodType
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _current_review_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_diff_fingerprint_failure_is_non_blocking(self) -> None:
        """A fingerprint lookup failure leaves the optional fingerprint empty."""
        provider = _current_review_provider([], {})
        provider.compute_diff_hash.side_effect = RuntimeError("git unavailable")
        snapshot = build_pr_state_snapshot(provider, 1)
        assert snapshot.diff_hash == ""
        assert snapshot.diff_hash_supported is True
        assert snapshot.diff_hash_available is False

    def test_diff_fingerprint_unavailable_when_capable_provider_returns_none(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A capable provider returning None means the fingerprint is unavailable."""
        provider = _current_review_provider([], {})
        provider.compute_diff_hash.return_value = None
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.pipeline.snapshot_builder"):
            snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.diff_hash == ""
        assert snapshot.diff_hash_supported is True
        assert snapshot.diff_hash_available is False
        assert "PR #1" in caplog.text
        assert "Provider returned None" in caplog.text

    def test_diff_fingerprint_unavailable_when_capable_provider_returns_empty_string(self) -> None:
        """A capable provider returning an empty string is treated as unavailable."""
        provider = _current_review_provider([], {})
        provider.compute_diff_hash.return_value = ""
        snapshot = build_pr_state_snapshot(provider, 1)
        assert snapshot.diff_hash == ""
        assert snapshot.diff_hash_supported is True
        assert snapshot.diff_hash_available is False

    def test_prefers_pinned_diff_files_for_snapshot_baseline(self) -> None:
        """When available, file inventory should be collected for the same HEAD SHA."""
        provider = _current_review_provider([], {})
        provider.compute_diff_files = MagicMock(return_value=["pinned.py"])
        provider.list_pr_files.side_effect = AssertionError(
            "list_pr_files should not be used when diff files are pinned"
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.files == ["pinned.py"]
        provider.compute_diff_files.assert_called_once_with(base_branch="main", sha="head-sha")

    def test_pins_base_sha_for_diff_inventory_and_fingerprint(self) -> None:
        """Diff inventory and fingerprint use one resolved base commit."""
        provider = _current_review_provider([], {})
        provider.get_ref_sha.return_value = "base-sha"
        provider.compute_diff_files = MagicMock(return_value=["pinned.py"])
        provider.compute_diff_hash.return_value = "patch-id:hash"

        build_pr_state_snapshot(provider, 1)

        provider.compute_diff_files.assert_called_once_with(base_branch="main", sha="head-sha", base_sha="base-sha")
        provider.compute_diff_hash.assert_called_once_with(base_branch="main", sha="head-sha", base_sha="base-sha")
        provider.get_ref_sha.assert_called_once_with("main")

    def test_fails_closed_when_pinned_base_sha_is_unavailable(self) -> None:
        """A pin-capable provider must not fall back to independently resolved bases."""
        provider = _current_review_provider([], {})

        def _get_ref_sha(_provider: object, _ref: str) -> str:
            return ""

        provider.get_ref_sha = MethodType(_get_ref_sha, provider)

        with pytest.raises(RuntimeError, match="base branch SHA unavailable"):
            build_pr_state_snapshot(provider, 1)

        provider.compute_diff_hash.assert_not_called()

    def test_falls_back_to_live_pr_files_when_pinned_diff_files_are_unsupported(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A provider without pinned inventory support falls back to PR files."""
        provider = _current_review_provider([], {})
        provider.compute_diff_files = None
        provider.list_pr_files.return_value = ["fallback.py"]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.files == ["fallback.py"]

    def test_pinned_diff_files_failure_is_fatal(self, caplog: pytest.LogCaptureFixture) -> None:
        """An overridden exact-HEAD inventory failure must not mix snapshot heads."""
        provider = _current_review_provider([], {})
        provider.compute_diff_files = MagicMock(side_effect=RuntimeError("git unavailable"))
        provider.list_pr_files.return_value = ["fallback.py"]

        with pytest.raises(RuntimeError, match="git unavailable"):
            build_pr_state_snapshot(provider, 1)

        provider.list_pr_files.assert_not_called()
        assert "Failed to compute diff files for HEAD head-sha" in caplog.text

    def test_missing_pinned_diff_files_is_fatal(self) -> None:
        """An overridden exact-HEAD inventory returning None fails closed."""
        provider = _current_review_provider([], {})
        provider.compute_diff_files = MagicMock(return_value=None)
        provider.list_pr_files.return_value = ["fallback.py"]

        with pytest.raises(RuntimeError, match="exact-HEAD file inventory unavailable"):
            build_pr_state_snapshot(provider, 1)

        provider.list_pr_files.assert_not_called()

    def test_diff_fingerprint_unsupported_when_provider_uses_default_method(self) -> None:
        """The inherited base-provider default still counts as unsupported."""
        provider = _current_review_provider([], {})
        provider.compute_diff_hash = CIPlatformProvider.compute_diff_hash.__get__(provider, MagicMock)
        snapshot = build_pr_state_snapshot(provider, 1)
        assert snapshot.diff_hash == ""
        assert snapshot.diff_hash_supported is False
        assert snapshot.diff_hash_available is False
