"""Tests for discover_children in shared/github_api.py."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.speckit.shared.github_api import discover_children


class TestDiscoverChildren:
    """Tests for the discover_children function."""

    def test_returns_children_from_metadata(self) -> None:
        """Test that children are extracted from metadata.children."""
        mock_meta = MagicMock()
        mock_child_1 = MagicMock()
        mock_child_1.number = 101
        mock_child_2 = MagicMock()
        mock_child_2.number = 102
        mock_meta.children = [mock_child_1, mock_child_2]
        mock_meta.informational_children = []

        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.return_value = mock_meta
            result = discover_children("owner", "repo", 100)

        assert result == [101, 102]

    def test_includes_informational_children(self) -> None:
        """Test that informational_children are included in results."""
        mock_meta = MagicMock()
        mock_child = MagicMock()
        mock_child.number = 201
        mock_info_child = MagicMock()
        mock_info_child.number = 202
        mock_meta.children = [mock_child]
        mock_meta.informational_children = [mock_info_child]

        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.return_value = mock_meta
            result = discover_children("owner", "repo", 200)

        assert result == [201, 202]

    def test_returns_empty_for_no_children(self) -> None:
        """Test that empty list is returned when no children exist."""
        mock_meta = MagicMock()
        mock_meta.children = []
        mock_meta.informational_children = []

        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.return_value = mock_meta
            result = discover_children("owner", "repo", 50)

        assert result == []

    def test_403_error_exits_cleanly(self) -> None:
        """Test that 403 errors produce a clean exit (via discover_relationships)."""
        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.side_effect = Exception("HTTP 403 Forbidden")
            with pytest.raises(SystemExit) as exc_info:
                discover_children("owner", "repo", 100)
            assert exc_info.value.code == 1

    def test_validation_error_exits_cleanly(self) -> None:
        """Test that detector ValueError failures exit with a clean message (via discover_relationships)."""
        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.side_effect = ValueError("gh CLI not installed")
            with pytest.raises(SystemExit) as exc_info:
                discover_children("owner", "repo", 100)
            assert exc_info.value.code == 1
