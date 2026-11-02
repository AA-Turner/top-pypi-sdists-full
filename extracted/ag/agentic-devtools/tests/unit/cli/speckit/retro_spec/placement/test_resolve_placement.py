"""Tests for resolve_placement in retro_spec/placement.py."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.retro_spec.placement import resolve_placement


class TestResolvePlacement:
    """Tests for the resolve_placement function."""

    def test_no_parent_places_at_root(self, tmp_path: Path) -> None:
        """Test that issues without parents are placed at root level."""
        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (None, [])
            result = resolve_placement("owner", "repo", 142, tmp_path)

        assert result.target_path == tmp_path / "142"
        assert result.parent_issue is None
        assert result.needs_hierarchy_update is False

    def test_no_parent_uses_issue_title_for_flat_directory(self, tmp_path: Path) -> None:
        """Standalone generated specs use the established issue-slug directory convention."""
        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships", return_value=(None, [])):
            result = resolve_placement("owner", "repo", 142, tmp_path, issue_title="Add API [v2]")

        assert result.target_path == tmp_path / "142-add-api-v2"

    def test_parent_with_canonical_path(self, tmp_path: Path) -> None:
        """Test placement beneath a canonical parent directory."""
        (tmp_path / "100").mkdir()

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (100, [])
            result = resolve_placement("owner", "repo", 142, tmp_path)

        assert result.target_path == tmp_path / "100" / "142"
        assert result.parent_issue == 100
        assert result.needs_hierarchy_update is True

    def test_parent_at_legacy_flat_path_aborts(self, tmp_path: Path) -> None:
        """Test that legacy flat parent path causes abort with guidance."""
        (tmp_path / "100-my-epic").mkdir()

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (100, [])
            with pytest.raises(SystemExit) as exc_info:
                resolve_placement("owner", "repo", 142, tmp_path)
            assert exc_info.value.code == 1

    def test_nested_legacy_parent_path_aborts(self, tmp_path: Path) -> None:
        """Nested legacy parent paths require migration before child placement."""
        (tmp_path / "10" / "20-feature").mkdir(parents=True)

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships", return_value=(20, [])):
            with pytest.raises(SystemExit) as exc_info:
                resolve_placement("owner", "repo", 142, tmp_path)

        assert exc_info.value.code == 1

    def test_rejects_parent_under_non_numeric_ancestor(self, tmp_path: Path) -> None:
        """Parent directories with non-canonical ancestors are rejected."""
        (tmp_path / "legacy" / "100").mkdir(parents=True)

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships", return_value=(100, [])):
            with pytest.raises(SystemExit) as exc_info:
                resolve_placement("owner", "repo", 142, tmp_path)

        assert exc_info.value.code == 1

    def test_parent_not_in_specs_places_at_root(self, tmp_path: Path) -> None:
        """Test that missing parent dir results in root placement."""
        (tmp_path / "some-other-dir").mkdir()
        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (999, [])
            result = resolve_placement("owner", "repo", 142, tmp_path)

        assert result.target_path == tmp_path / "142"
        assert result.parent_issue == 999
        assert result.needs_hierarchy_update is False

    def test_parent_at_nested_path_is_found(self, tmp_path: Path) -> None:
        """Test placement beneath a parent that is already nested under another directory."""
        # Parent 100 lives at specs/50/100/ (already nested, not at root)
        nested_parent = tmp_path / "50" / "100"
        nested_parent.mkdir(parents=True)

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (100, [])
            result = resolve_placement("owner", "repo", 142, tmp_path)

        assert result.target_path == tmp_path / "50" / "100" / "142"
        assert result.parent_issue == 100
        assert result.needs_hierarchy_update is True

    def test_does_not_raise_when_specs_root_missing_and_parent_not_found(self, tmp_path: Path) -> None:
        """Test that a non-existent specs_root does not raise when checking legacy paths."""
        missing_specs = tmp_path / "specs"  # does not exist

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (100, [])
            # Should return root placement without raising FileNotFoundError
            result = resolve_placement("owner", "repo", 142, missing_specs)

        assert result.target_path == missing_specs / "142"
        assert result.parent_issue == 100
        assert result.needs_hierarchy_update is False

    def test_does_not_raise_when_specs_root_is_a_file(self, tmp_path: Path) -> None:
        """Test that a specs_root path that is a file (not a directory) does not raise."""
        specs_file = tmp_path / "specs"
        specs_file.write_text("not a directory", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (100, [])
            # Should return root placement without raising NotADirectoryError
            result = resolve_placement("owner", "repo", 142, specs_file)

        assert result.target_path == specs_file / "142"
        assert result.parent_issue == 100
        assert result.needs_hierarchy_update is False

    def test_skips_file_entry_with_parent_name_and_falls_back_to_root(self, tmp_path: Path) -> None:
        """Test that a file (not directory) named after the parent is not used as placement path."""
        # Create a FILE named "100", not a directory — should not be treated as the parent path
        (tmp_path / "100").write_text("not a dir", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (100, [])
            result = resolve_placement("owner", "repo", 142, tmp_path)

        # File named "100" does not qualify; no legacy flat dir either → root placement
        assert result.target_path == tmp_path / "142"
        assert result.parent_issue == 100
        assert result.needs_hierarchy_update is False

    def test_depth_cap_places_child_at_flat_path(self, tmp_path: Path) -> None:
        """Test that a mocked depth-cap overflow falls back to a flat path."""
        (tmp_path / "100").mkdir()
        fake_relative = SimpleNamespace(parts=("100", "141", "142", "143"))

        with (
            patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships", return_value=(100, [])),
            patch.object(Path, "relative_to", return_value=fake_relative),
        ):
            result = resolve_placement("owner", "repo", 142, tmp_path)

        assert result.target_path == tmp_path / "142"
        assert result.parent_issue == 100
        assert result.needs_hierarchy_update is False

    def test_prefers_sorted_nested_parent_candidate(self, tmp_path: Path) -> None:
        """Test nested parent resolution is deterministic via sorted first-level dirs."""
        (tmp_path / "30" / "100").mkdir(parents=True)
        (tmp_path / "20" / "100").mkdir(parents=True)

        with (
            patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships", return_value=(100, [])),
            patch.object(Path, "iterdir", return_value=iter([tmp_path / "30", tmp_path / "20"])),
        ):
            result = resolve_placement("owner", "repo", 142, tmp_path)

        assert result.target_path == tmp_path / "20" / "100" / "142"
        assert result.parent_issue == 100
        assert result.needs_hierarchy_update is True

    def test_rejects_symlinked_level0_parent(self, tmp_path: Path) -> None:
        """A symlinked level-0 parent directory is not used as a canonical parent path."""
        real_dir = tmp_path / "real_100"
        real_dir.mkdir()
        symlink_parent = tmp_path / "100"
        symlink_parent.symlink_to(real_dir)

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (100, [])
            result = resolve_placement("owner", "repo", 142, tmp_path)

        # Symlinked parent must not be accepted — placement should fall back to root
        assert result.target_path == tmp_path / "142"
        assert result.needs_hierarchy_update is False

    def test_rejects_symlinked_level1_candidate(self, tmp_path: Path) -> None:
        """A symlinked level-1 candidate directory is not used as a canonical parent path."""
        numeric_dir = tmp_path / "50"
        numeric_dir.mkdir()
        real_target = tmp_path / "real_100"
        real_target.mkdir()
        symlink_candidate = numeric_dir / "100"
        symlink_candidate.symlink_to(real_target)

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships") as mock_discover:
            mock_discover.return_value = (100, [])
            result = resolve_placement("owner", "repo", 142, tmp_path)

        # Symlinked candidate must not be accepted — placement should fall back to root
        assert result.target_path == tmp_path / "142"
        assert result.needs_hierarchy_update is False

    def test_rejects_symlinked_parent_hierarchy_file(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """A symlinked hierarchy file is rejected before nested placement is returned."""
        parent_dir = tmp_path / "100"
        parent_dir.mkdir()
        outside_hierarchy = tmp_path / "outside.yml"
        outside_hierarchy.write_text("title: outside\nlevel: epic\nchildren: []\n", encoding="utf-8")
        (parent_dir / "hierarchy.yml").symlink_to(outside_hierarchy)

        with patch("agentic_devtools.cli.speckit.retro_spec.placement.discover_relationships", return_value=(100, [])):
            with pytest.raises(SystemExit) as exc_info:
                resolve_placement("owner", "repo", 142, tmp_path)

        assert exc_info.value.code == 1
        assert "symlinked hierarchy.yml" in capsys.readouterr().err
