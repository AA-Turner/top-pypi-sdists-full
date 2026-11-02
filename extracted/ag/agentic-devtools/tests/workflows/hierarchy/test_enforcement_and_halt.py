"""Integration tests for parent-first enforcement and failure halting (US-2).

Verifies rejection when parent not specked, halt on speckit:failed label,
and distinction between halt and skip actions.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.enforcement import (
    EnforcementAction,
    check_parent_specked,
    enforce_parent_specked,
)
from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import (
    ChildInfo,
    HierarchyLevel,
    HierarchyMetadata,
)

from .conftest import (
    assert_comment_posted,
    assert_label_not_applied,
    make_issue_state,
)


class TestRejectWhenParentNotSpecked:
    """T013: Reject when parent has no spec directory."""

    def test_reject_without_parent_dir(self, specs_root: Path) -> None:
        meta = HierarchyMetadata(level=HierarchyLevel.TASK, parent=101)
        result = enforce_parent_specked(103, meta, specs_root, ancestors=[100])

        assert result.action == EnforcementAction.REJECT
        assert result.parent_issue == 101
        assert "101" in result.reason


class TestRejectNoSluggedAncestorPath:
    """T014: Reject when slugged ancestor path also doesn't exist."""

    def test_reject_no_slugged_match(self, specs_root: Path) -> None:
        # Create ancestor base dir so stage-1 hierarchical lookup runs,
        # but omit any 101 or 101-* directory under it.
        (specs_root / "100").mkdir()
        meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=101)
        result = enforce_parent_specked(103, meta, specs_root, ancestors=[100])

        assert result.action == EnforcementAction.REJECT
        assert result.parent_issue == 101


class TestAllowWhenLegacyFlatPathExists:
    """T015: Allow when legacy flat path (specs/NNN-*/) exists."""

    def test_allow_via_legacy_flat_path(self, specs_root: Path) -> None:
        (specs_root / "101-my-feature").mkdir()
        is_specked, found_path = check_parent_specked(101, specs_root)

        assert is_specked is True
        assert found_path is not None
        assert "101-my-feature" in str(found_path)


class TestHaltOnFailedLabel:
    """T016: Halt cascade when child has speckit:failed label."""

    def test_halt_on_failed_child(
        self,
        specs_root: Path,
        mock_cascade_api: tuple[CascadeProcessor, MagicMock, MagicMock, MagicMock],
    ) -> None:
        processor, mock_state, mock_label, mock_comment = mock_cascade_api

        metadata = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=100,
            children=[
                ChildInfo(number=103, title="Task A", order=1),
                ChildInfo(number=104, title="Task B", order=2),
            ],
        )
        yml_path = specs_root / "101" / "hierarchy.yml"
        write_hierarchy_yml(yml_path, metadata)

        mock_state.side_effect = lambda n: make_issue_state(n, labels=["speckit:failed"] if n == 103 else [])

        result = processor.trigger_first_child(101, yml_path)
        assert result.action == CascadeAction.HALTED

        assert_label_not_applied(mock_label, 104)
        assert_comment_posted(mock_comment, 101, "failed")


class TestHaltDistinctFromSkip:
    """T017: Halted cascade does NOT advance to next sibling."""

    def test_halt_does_not_trigger_next(
        self,
        specs_root: Path,
        mock_cascade_api: tuple[CascadeProcessor, MagicMock, MagicMock, MagicMock],
    ) -> None:
        processor, mock_state, mock_label, mock_comment = mock_cascade_api

        metadata = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=100,
            children=[
                ChildInfo(number=103, title="Task A", order=1),
                ChildInfo(number=104, title="Task B", order=2),
            ],
        )
        yml_path = specs_root / "101" / "hierarchy.yml"
        write_hierarchy_yml(yml_path, metadata)

        mock_state.side_effect = lambda n: make_issue_state(n, labels=["speckit:failed"] if n == 103 else [])

        result = processor.trigger_first_child(101, yml_path)
        assert result.action == CascadeAction.HALTED

        assert_label_not_applied(mock_label, 103)
        assert_label_not_applied(mock_label, 104)
