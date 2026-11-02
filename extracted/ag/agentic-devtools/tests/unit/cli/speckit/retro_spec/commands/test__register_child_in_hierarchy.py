"""Tests for _register_child_in_hierarchy in retro_spec/commands.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.retro_spec.commands import _register_child_in_hierarchy


class TestRegisterChildInHierarchy:
    """Tests for the _register_child_in_hierarchy helper."""

    def test_creates_new_hierarchy_file_when_absent(self, tmp_path: Path) -> None:
        """Creates a minimal hierarchy.yml when the parent file does not exist."""
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        hierarchy_path = parent_dir / "hierarchy.yml"

        written = _register_child_in_hierarchy(
            hierarchy_path=hierarchy_path,
            parent_dir=parent_dir,
            specs_root=tmp_path,
            issue_number=42,
            issue_title="My feature",
        )

        assert written is True
        assert hierarchy_path.exists()
        content = hierarchy_path.read_text(encoding="utf-8")
        assert "42" in content
        assert "My feature" in content

    def test_appends_child_to_existing_hierarchy_file(self, tmp_path: Path) -> None:
        """Appends a new child entry to an existing hierarchy.yml."""
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        hierarchy_path = parent_dir / "hierarchy.yml"
        hierarchy_path.write_text(
            "title: 'Issue #100'\nlevel: epic\nchildren: []\n",
            encoding="utf-8",
        )

        written = _register_child_in_hierarchy(
            hierarchy_path=hierarchy_path,
            parent_dir=parent_dir,
            specs_root=tmp_path,
            issue_number=42,
            issue_title="Child feature",
        )

        assert written is True
        content = hierarchy_path.read_text(encoding="utf-8")
        assert "42" in content
        assert "Child feature" in content

    def test_returns_false_when_child_already_registered_with_same_title(self, tmp_path: Path) -> None:
        """Returns False without rewriting when child is already present with identical title."""
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        hierarchy_path = parent_dir / "hierarchy.yml"
        hierarchy_path.write_text(
            "title: 'Issue #100'\nlevel: epic\nchildren:\n  - key: '42'\n    title: Child feature\n    order: 0\n",
            encoding="utf-8",
        )
        original_mtime = hierarchy_path.stat().st_mtime

        written = _register_child_in_hierarchy(
            hierarchy_path=hierarchy_path,
            parent_dir=parent_dir,
            specs_root=tmp_path,
            issue_number=42,
            issue_title="Child feature",
        )

        assert written is False
        assert hierarchy_path.stat().st_mtime == original_mtime

    def test_raises_value_error_on_conflicting_child_title(self, tmp_path: Path) -> None:
        """Raises ValueError when an existing child entry has a different title."""
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        hierarchy_path = parent_dir / "hierarchy.yml"
        hierarchy_path.write_text(
            "title: 'Issue #100'\nlevel: epic\nchildren:\n  - key: '42'\n    title: Old title\n    order: 0\n",
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="Conflicting child definition"):
            _register_child_in_hierarchy(
                hierarchy_path=hierarchy_path,
                parent_dir=parent_dir,
                specs_root=tmp_path,
                issue_number=42,
                issue_title="New title",
            )

    def test_sets_parent_key_when_grandparent_is_numeric(self, tmp_path: Path) -> None:
        """Sets parent key when the grandparent directory name is a plain number."""
        grandparent_dir = tmp_path / "100"
        grandparent_dir.mkdir()
        parent_dir = grandparent_dir / "200"
        parent_dir.mkdir()
        hierarchy_path = parent_dir / "hierarchy.yml"

        _register_child_in_hierarchy(
            hierarchy_path=hierarchy_path,
            parent_dir=parent_dir,
            specs_root=tmp_path,
            issue_number=42,
            issue_title="Grandchild",
        )

        content = hierarchy_path.read_text(encoding="utf-8")
        assert "100" in content  # parent key set from numeric grandparent dir name
        assert "parent:" in content  # parent field is present in the YAML output
