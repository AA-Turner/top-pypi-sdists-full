"""Integration tests for edge cases.

Covers closed/deleted children, empty children list,
and enforcement allow at legacy flat path stage-2.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.enforcement import (
    check_parent_specked,
)
from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import (
    ChildInfo,
    HierarchyLevel,
    HierarchyMetadata,
)

from .conftest import assert_comment_posted, assert_label_applied, assert_label_not_applied, make_issue_state


class TestClosedChildSkipped:
    """T029: Closed child is skipped and skip notice posted."""

    def test_closed_child_skipped(
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

        def side_effect(n: int) -> dict | None:
            if n == 103:
                return make_issue_state(n, state="closed")
            return make_issue_state(n)

        mock_state.side_effect = side_effect

        result = processor.trigger_first_child(101, yml_path)
        assert result.action == CascadeAction.TRIGGERED
        assert result.event is not None
        assert result.event.target_issue == 104
        assert 103 in result.skipped_issues

        assert_label_applied(mock_label, 104)
        assert_label_not_applied(mock_label, 103)
        assert_comment_posted(mock_comment, 101, "#103")


class TestDeletedChildSkipped:
    """T030: Deleted child (404) is skipped."""

    def test_deleted_child_skipped(
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

        def side_effect(n: int) -> dict | None:
            if n == 103:
                return None  # 404
            return make_issue_state(n)

        mock_state.side_effect = side_effect

        result = processor.trigger_first_child(101, yml_path)
        assert result.action == CascadeAction.TRIGGERED
        assert result.event is not None
        assert result.event.target_issue == 104
        assert 103 in result.skipped_issues

        assert_label_applied(mock_label, 104)
        assert_label_not_applied(mock_label, 103)
        assert_comment_posted(mock_comment, 101, "#103")


class TestEmptyChildrenList:
    """T031: Empty children list returns NO_CHILDREN."""

    def test_no_children(
        self,
        specs_root: Path,
        mock_cascade_api: tuple[CascadeProcessor, MagicMock, MagicMock, MagicMock],
    ) -> None:
        processor, mock_state, mock_label, mock_comment = mock_cascade_api

        metadata = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=100,
            children=[],
        )
        yml_path = specs_root / "101" / "hierarchy.yml"
        write_hierarchy_yml(yml_path, metadata)

        result = processor.trigger_first_child(101, yml_path)
        assert result.action == CascadeAction.NO_CHILDREN

        mock_label.assert_not_called()
        assert_comment_posted(mock_comment, 101, "No further sub-issues to process.")


class TestEnforcementAllowAtLegacyFlatPathStage2:
    """T032: Enforcement stage-2 finds legacy flat path and allows."""

    def test_allow_via_legacy_path(self, specs_root: Path) -> None:
        (specs_root / "101-my-feature").mkdir()

        is_specked, found_path = check_parent_specked(101, specs_root)

        assert is_specked is True
        assert found_path is not None
        assert found_path.name.startswith("101-")
