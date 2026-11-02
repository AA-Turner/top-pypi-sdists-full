"""Tests for check_parent_specked (two-stage directory lookup)."""

from pathlib import Path

from agentic_devtools.hierarchy.enforcement import check_parent_specked


class TestCheckParentSpecked:
    """Tests for the two-stage parent spec directory lookup."""

    def test_finds_hierarchical_path(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        parent_dir = specs_root / "100"
        parent_dir.mkdir(parents=True)

        is_specked, found_path = check_parent_specked(100, specs_root)
        assert is_specked is True
        assert found_path == parent_dir

    def test_finds_legacy_flat_path(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        legacy_dir = specs_root / "100-user-auth"
        legacy_dir.mkdir(parents=True)

        is_specked, found_path = check_parent_specked(100, specs_root)
        assert is_specked is True
        assert found_path == legacy_dir

    def test_not_found_returns_false(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        specs_root.mkdir(parents=True)

        is_specked, found_path = check_parent_specked(100, specs_root)
        assert is_specked is False
        assert found_path is None

    def test_hierarchical_path_with_ancestors(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        nested_dir = specs_root / "50" / "100"
        nested_dir.mkdir(parents=True)

        is_specked, found_path = check_parent_specked(100, specs_root, ancestors=[50])
        assert is_specked is True
        assert found_path == nested_dir

    def test_prefers_hierarchical_over_legacy(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        hierarchical_dir = specs_root / "100"
        hierarchical_dir.mkdir(parents=True)
        legacy_dir = specs_root / "100-old-name"
        legacy_dir.mkdir(parents=True)

        is_specked, found_path = check_parent_specked(100, specs_root)
        assert is_specked is True
        assert found_path == hierarchical_dir

    def test_finds_slugged_hierarchical_path_with_ancestors(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        nested_slugged_dir = specs_root / "50" / "100-user-auth"
        nested_slugged_dir.mkdir(parents=True)

        is_specked, found_path = check_parent_specked(100, specs_root, ancestors=[50])
        assert is_specked is True
        assert found_path == nested_slugged_dir

    def test_ignores_slugged_file_match_with_ancestors(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        nested_slugged_file = specs_root / "50" / "100-user-auth"
        nested_slugged_file.parent.mkdir(parents=True)
        nested_slugged_file.write_text("not-a-directory")

        is_specked, found_path = check_parent_specked(100, specs_root, ancestors=[50])
        assert is_specked is False
        assert found_path is None
