"""Tests for discover_relationships in shared/github_api.py."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.speckit.shared.github_api import discover_relationships


class TestDiscoverRelationships:
    """Tests for the discover_relationships function."""

    def test_returns_parent_and_children(self) -> None:
        """Test that both parent and children are returned from a single API call."""
        mock_meta = MagicMock()
        mock_meta.parent = 100
        mock_child = MagicMock()
        mock_child.number = 201
        mock_meta.children = [mock_child]
        mock_meta.informational_children = []

        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.return_value = mock_meta
            parent, children = discover_relationships("owner", "repo", 200)

        assert parent == 100
        assert children == [201]

    def test_single_api_call(self) -> None:
        """Test that only one build_metadata call is made (not two)."""
        mock_meta = MagicMock()
        mock_meta.parent = None
        mock_meta.children = []
        mock_meta.informational_children = []

        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_instance = mock_detector_cls.return_value
            mock_instance.build_metadata.return_value = mock_meta
            discover_relationships("owner", "repo", 50)

        mock_instance.build_metadata.assert_called_once_with(50)

    def test_403_error_exits_with_guidance(self) -> None:
        """Test that 403 errors produce actionable error messages."""
        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.side_effect = Exception("HTTP 403 Forbidden")
            with pytest.raises(SystemExit) as exc_info:
                discover_relationships("owner", "repo", 50)
            assert exc_info.value.code == 1

    def test_unreachable_error_exits_with_guidance(self) -> None:
        """Test that network errors produce actionable error messages."""
        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.side_effect = Exception("Could not resolve host")
            with pytest.raises(SystemExit) as exc_info:
                discover_relationships("owner", "repo", 50)
            assert exc_info.value.code == 1

    def test_includes_informational_children(self) -> None:
        """Test that informational children are included alongside direct children."""
        mock_meta = MagicMock()
        mock_meta.parent = 100
        mock_child = MagicMock()
        mock_child.number = 201
        mock_info_child = MagicMock()
        mock_info_child.number = 202
        mock_meta.children = [mock_child]
        mock_meta.informational_children = [mock_info_child]

        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.return_value = mock_meta
            parent, children = discover_relationships("owner", "repo", 200)

        assert parent == 100
        assert children == [201, 202]

    def test_reraises_unknown_errors(self) -> None:
        """Test that unexpected errors are re-raised."""
        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.side_effect = RuntimeError("unexpected boom")
            with pytest.raises(RuntimeError, match="unexpected boom"):
                discover_relationships("owner", "repo", 50)

    def test_validation_errors_exit_cleanly(self) -> None:
        """Test that detector ValueError failures exit with a clean user-facing message."""
        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.side_effect = ValueError("GitHub CLI (`gh`) is not installed")
            with pytest.raises(SystemExit) as exc_info:
                discover_relationships("owner", "repo", 50)
            assert exc_info.value.code == 1

    def test_deduplicates_children_preserving_first_occurrence_order(self) -> None:
        """Test duplicate children across lists are deduplicated in stable order."""
        mock_meta = MagicMock()
        mock_meta.parent = 100
        child_201 = MagicMock()
        child_201.number = 201
        child_202 = MagicMock()
        child_202.number = 202
        info_202 = MagicMock()
        info_202.number = 202
        info_203 = MagicMock()
        info_203.number = 203
        info_201 = MagicMock()
        info_201.number = 201
        mock_meta.children = [child_201, child_202]
        mock_meta.informational_children = [info_202, info_203, info_201]

        with patch("agentic_devtools.cli.speckit.shared.github_api.GitHubHierarchyDetector") as mock_detector_cls:
            mock_detector_cls.return_value.build_metadata.return_value = mock_meta
            parent, children = discover_relationships("owner", "repo", 200)

        assert parent == 100
        assert children == [201, 202, 203]
