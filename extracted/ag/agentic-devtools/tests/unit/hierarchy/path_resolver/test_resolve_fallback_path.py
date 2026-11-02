"""Tests for fallback flat path in resolve_spec_path."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata
from agentic_devtools.hierarchy.path_resolver import resolve_spec_path


class TestResolveFallbackPath:
    """Cover fallback flat path when FEATURE/TASK has no parent."""

    def test_feature_no_parent_uses_flat_path(self):
        meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=None)
        result = resolve_spec_path(42, meta, Path("specs"), short_name="My Feature")
        assert result == Path("specs/42-my-feature")

    def test_task_no_parent_uses_flat_path(self):
        meta = HierarchyMetadata(level=HierarchyLevel.TASK, parent=None)
        result = resolve_spec_path(99, meta, Path("specs"), short_name="Some Task")
        assert result == Path("specs/99-some-task")

    def test_fallback_no_title_uses_spec(self):
        meta = HierarchyMetadata(level=HierarchyLevel.TASK, parent=None)
        result = resolve_spec_path(5, meta, Path("specs"), short_name="")
        assert result == Path("specs/5-spec")
