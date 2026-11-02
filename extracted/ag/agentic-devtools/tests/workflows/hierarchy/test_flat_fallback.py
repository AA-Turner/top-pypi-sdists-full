"""Integration tests for flat fallback and flat-spec preservation (US-5).

Verifies standalone issues create flat directories without hierarchy.yml,
and existing flat specs remain unchanged when a separate hierarchy.yml is written.
"""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import (
    ChildInfo,
    HierarchyLevel,
    HierarchyMetadata,
)
from agentic_devtools.hierarchy.path_resolver import resolve_spec_path


class TestStandaloneCreatesFlatDirNoHierarchyYml:
    """T025: Standalone issue creates flat dir, no hierarchy.yml."""

    def test_standalone_flat_path(self, specs_root: Path) -> None:
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        path = resolve_spec_path(42, meta, specs_root, title="fix-typo")

        assert str(path).endswith("42-fix-typo")
        assert "hierarchy.yml" not in str(path)

    def test_standalone_no_hierarchy_yml(self, specs_root: Path) -> None:
        meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        result = write_hierarchy_yml(specs_root / "42-fix-typo" / "hierarchy.yml", meta)

        assert result is False
        assert not (specs_root / "42-fix-typo" / "hierarchy.yml").exists()


class TestExistingFlatSpecNotModified:
    """T026: Existing flat specs are unchanged by separate hierarchy.yml writes."""

    def test_existing_flat_spec_unchanged(self, specs_root: Path) -> None:
        legacy_dir = specs_root / "50-old-feature"
        legacy_dir.mkdir()
        existing_file = legacy_dir / "existing.md"
        original_content = "# Existing Spec\n\nThis should not be modified.\n"
        existing_file.write_text(original_content)

        hierarchical_meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[ChildInfo(number=101, title="Feature A")],
        )
        write_hierarchy_yml(specs_root / "100" / "hierarchy.yml", hierarchical_meta)

        assert existing_file.read_text() == original_content
        assert (specs_root / "50-old-feature" / "existing.md").exists()
