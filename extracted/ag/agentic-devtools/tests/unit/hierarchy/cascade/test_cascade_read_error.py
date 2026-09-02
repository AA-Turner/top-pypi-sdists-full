"""Tests for cascade when hierarchy.yml cannot be read."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor


class TestCascadeReadError:
    """Cover exception paths when read_hierarchy_yml fails."""

    def test_trigger_first_child_file_not_found(self, tmp_path: Path):
        """Non-existent YAML path returns HALTED (not NO_CHILDREN — an unreadable file is an error path)."""
        proc = CascadeProcessor("o", "r")
        with patch.object(proc, "_post_comment") as mock_comment:
            result = proc.trigger_first_child(42, tmp_path / "nonexistent.yml")
        assert result.action == CascadeAction.HALTED
        assert "Could not read" in result.comment
        mock_comment.assert_called_once_with(42, result.comment)

    def test_trigger_next_sibling_file_not_found(self, tmp_path: Path):
        """Non-existent YAML path returns HALTED (not NO_CHILDREN — an unreadable file is an error path)."""
        proc = CascadeProcessor("o", "r")
        parent_dir = tmp_path / "50-parent"
        parent_dir.mkdir()
        with patch.object(proc, "_post_comment") as mock_comment:
            result = proc.trigger_next_sibling(42, parent_dir / "nonexistent.yml")
        assert result.action == CascadeAction.HALTED
        assert "Could not read" in result.comment
        mock_comment.assert_called_once_with(50, result.comment)

    def test_trigger_next_sibling_file_not_found_without_numeric_parent_prefix(self, tmp_path: Path):
        """Unparseable parent directory skips comment posting gracefully."""
        proc = CascadeProcessor("o", "r")
        parent_dir = tmp_path / "parent-dir"
        parent_dir.mkdir()
        with patch.object(proc, "_post_comment") as mock_comment:
            result = proc.trigger_next_sibling(42, parent_dir / "nonexistent.yml")
        assert result.action == CascadeAction.HALTED
        assert "Could not read" in result.comment
        mock_comment.assert_not_called()

    def test_trigger_first_child_invalid_yml(self, tmp_path: Path):
        """Invalid YAML content returns HALTED (not NO_CHILDREN — a parse error is an error path)."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text("level: INVALID_LEVEL\n")
        proc = CascadeProcessor("o", "r")
        result = proc.trigger_first_child(42, yml)
        assert result.action == CascadeAction.HALTED
        assert "Could not read" in result.comment

    def test_trigger_first_child_malformed_yaml(self, tmp_path: Path):
        """Malformed YAML (yaml.YAMLError) returns HALTED — not an unhandled crash."""
        yml = tmp_path / "hierarchy.yml"
        yml.write_text("level: epic\nchildren:\n\t- number: 1\n")
        proc = CascadeProcessor("o", "r")
        with patch.object(proc, "_post_comment") as mock_comment:
            result = proc.trigger_first_child(42, yml)
        assert result.action == CascadeAction.HALTED
        assert "Could not read" in result.comment
        mock_comment.assert_called_once_with(42, result.comment)

    def test_trigger_next_sibling_malformed_yaml(self, tmp_path: Path):
        """Malformed YAML (yaml.YAMLError) in trigger_next_sibling returns HALTED."""
        parent_dir = tmp_path / "50-parent"
        parent_dir.mkdir()
        yml = parent_dir / "hierarchy.yml"
        yml.write_text("level: feature\nchildren:\n\t- number: 1\n")
        proc = CascadeProcessor("o", "r")
        with patch.object(proc, "_post_comment") as mock_comment:
            result = proc.trigger_next_sibling(42, yml)
        assert result.action == CascadeAction.HALTED
        assert "Could not read" in result.comment
        mock_comment.assert_called_once_with(50, result.comment)
