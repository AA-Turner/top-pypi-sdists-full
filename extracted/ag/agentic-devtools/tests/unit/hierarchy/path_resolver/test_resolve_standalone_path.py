"""Tests for standalone path resolution."""

from pathlib import Path

from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata
from agentic_devtools.hierarchy.path_resolver import resolve_spec_path


class TestResolveStandalonePath:
    """Tests for standalone (flat) path resolution."""

    def test_standalone_with_short_name(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        path = resolve_spec_path(200, meta, specs_root, short_name="user-auth")
        assert path == specs_root / "200-user-auth"

    def test_standalone_without_short_name(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        path = resolve_spec_path(200, meta, specs_root)
        assert path == specs_root / "200-spec"

    def test_standalone_with_special_characters(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        path = resolve_spec_path(200, meta, specs_root, short_name="User Auth Feature!")
        expected = specs_root / "200-user-auth-feature"
        assert path == expected

    def test_standalone_with_only_punctuation_uses_placeholder(self, tmp_path: Path) -> None:
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        path = resolve_spec_path(200, meta, specs_root, short_name="!!!")
        assert path == specs_root / "200-spec"

    def test_title_alias_for_short_name(self, tmp_path: Path) -> None:
        """title= is an accepted alias for short_name= and produces the same path."""
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        path = resolve_spec_path(200, meta, specs_root, title="auth-handler")
        assert path == specs_root / "200-auth-handler"

    def test_short_name_takes_precedence_over_title(self, tmp_path: Path) -> None:
        """When both short_name and title are given, short_name wins."""
        specs_root = tmp_path / "specs"
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        path = resolve_spec_path(200, meta, specs_root, short_name="primary", title="secondary")
        assert path == specs_root / "200-primary"
