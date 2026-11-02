"""Tests for discover_parent in shared/github_api.py."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.speckit.shared.github_api import discover_parent


class TestDiscoverParent:
    """Tests for the discover_parent function."""

    def test_returns_parent_from_metadata(self) -> None:
        """Test that parent number is returned from metadata."""
        mock_meta = MagicMock()
        mock_meta.parent = 100
        # discover_parent delegates to discover_relationships(), which also reads
        # children and informational_children — both attributes must be set.
        mock_meta.children = []
        mock_meta.informational_children = []

        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.return_value = mock_meta
            result = discover_parent("owner", "repo", 101)

        assert result == 100

    def test_returns_none_when_no_parent(self) -> None:
        """Test that None is returned when no parent exists."""
        mock_meta = MagicMock()
        mock_meta.parent = None
        # discover_parent delegates to discover_relationships(), which also reads
        # children and informational_children — both attributes must be set.
        mock_meta.children = []
        mock_meta.informational_children = []

        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.return_value = mock_meta
            result = discover_parent("owner", "repo", 50)

        assert result is None

    def test_403_error_exits_cleanly(self) -> None:
        """Test that 403 errors produce a clean exit (via discover_relationships)."""
        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.side_effect = Exception("HTTP 403 Forbidden")
            with pytest.raises(SystemExit) as exc_info:
                discover_parent("owner", "repo", 101)
            assert exc_info.value.code == 1

    def test_validation_error_exits_cleanly(self) -> None:
        """Test that detector ValueError failures exit with a clean message (via discover_relationships)."""
        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.side_effect = ValueError("gh CLI not installed")
            with pytest.raises(SystemExit) as exc_info:
                discover_parent("owner", "repo", 101)
            assert exc_info.value.code == 1
