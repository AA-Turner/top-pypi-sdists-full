"""Integration tests for skip mechanism and sibling cascade (US-3).

Verifies skip bypasses child and labels next, sibling-to-sibling cascade,
all-children-skipped behavior, and failed-takes-precedence-over-skip.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import (
    CascadeDirection,
    ChildInfo,
    HierarchyLevel,
    HierarchyMetadata,
)

from .conftest import (
    assert_comment_posted,
    assert_label_applied,
    assert_label_not_applied,
    make_issue_state,
)


class TestSkipBypassesChildAndLabelsNext:
    """T018: Child with speckit:skip is skipped, next child labeled."""

    def test_skip_to_next_child(
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

        mock_state.side_effect = lambda n: make_issue_state(n, labels=["speckit:skip"] if n == 103 else [])

        result = processor.trigger_first_child(101, yml_path)
        assert result.action == CascadeAction.TRIGGERED
        assert result.event is not None
        assert result.event.target_issue == 104
        assert 103 in result.skipped_issues

        assert_label_applied(mock_label, 104)
        assert_label_not_applied(mock_label, 103)
        assert_comment_posted(mock_comment, 101, "Skip Notice")


class TestSiblingToSiblingCascade:
    """T019: Sibling-to-sibling cascade after completion."""

    def test_triggers_next_sibling(
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

        mock_state.side_effect = lambda n: make_issue_state(n)

        result = processor.trigger_next_sibling(103, yml_path)
        assert result.action == CascadeAction.TRIGGERED
        assert result.event is not None
        assert result.event.direction == CascadeDirection.SIBLING_TO_SIBLING
        assert result.event.target_issue == 104

        assert_label_applied(mock_label, 104)


class TestAllChildrenSkippedReturnsCascadeComplete:
    """T020: All children skipped returns CASCADE_COMPLETE."""

    def test_all_skipped_cascade_complete(
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

        mock_state.side_effect = lambda n: make_issue_state(n, labels=["speckit:skip"])

        result = processor.trigger_first_child(101, yml_path)
        assert result.action == CascadeAction.CASCADE_COMPLETE
        assert result.event is None
        assert result.skipped_issues == [103, 104]
        assert mock_label.call_args_list == []

        assert_comment_posted(mock_comment, 101, "No further cascade target remains.")
        assert_comment_posted(mock_comment, 101, "No further sub-issues to process.")


class TestFailedTakesPrecedenceOverSkip:
    """T021: speckit:failed takes precedence over speckit:skip."""

    def test_failed_halts_even_with_skip(
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

        mock_state.side_effect = lambda n: make_issue_state(
            n,
            labels=["speckit:skip", "speckit:failed"] if n == 103 else [],
        )

        result = processor.trigger_first_child(101, yml_path)
        assert result.action == CascadeAction.HALTED
        assert result.skipped_issues == []
        assert mock_label.call_args_list == []
        assert_comment_posted(mock_comment, 101, "speckit:failed")
