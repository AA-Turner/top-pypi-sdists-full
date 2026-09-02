"""Integration tests for happy-path cascade flow (US-1).

Verifies end-to-end: hierarchy.yml creation, child labeling order,
completion comments, filesystem structure, and ordering determinism.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import yaml

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml, write_hierarchy_yml
from agentic_devtools.hierarchy.models import (
    CascadeDirection,
    ChildInfo,
    HierarchyLevel,
    HierarchyMetadata,
)

from .conftest import (
    assert_comment_posted,
    assert_label_applied,
    make_issue_state,
)


class TestEpicDetectionWritesHierarchyYml:
    """T008: Detect epic and write hierarchy.yml."""

    def test_writes_hierarchy_yml_with_correct_content(self, specs_root: Path) -> None:
        metadata = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[
                ChildInfo(number=101, title="Feature: Authentication", order=1),
                ChildInfo(number=102, title="Feature: Authorization", order=2),
            ],
        )
        yml_path = specs_root / "100" / "hierarchy.yml"
        result = write_hierarchy_yml(yml_path, metadata)

        assert result is True
        assert yml_path.exists()
        data = yaml.safe_load(yml_path.read_text())
        assert data["level"] == "epic"
        assert data["parent"] is None
        assert len(data["children"]) == 2
        assert data["children"][0]["number"] == 101
        assert data["children"][1]["number"] == 102

    def test_only_epic_dir_created(self, specs_root: Path) -> None:
        metadata = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[
                ChildInfo(number=101, title="Feature A"),
                ChildInfo(number=102, title="Feature B"),
            ],
        )
        write_hierarchy_yml(specs_root / "100" / "hierarchy.yml", metadata)

        assert (specs_root / "100").is_dir()
        assert not (specs_root / "100" / "101").exists()
        assert not (specs_root / "100" / "102").exists()


class TestFullCascadeLabelsChildrenInOrder:
    """T009: Cascade labels children in API order."""

    def test_labels_first_child_then_next(
        self,
        specs_root: Path,
        mock_cascade_api: tuple[CascadeProcessor, MagicMock, MagicMock, MagicMock],
    ) -> None:
        processor, mock_state, mock_label, mock_comment = mock_cascade_api

        metadata = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[
                ChildInfo(number=101, title="Feature A", order=1),
                ChildInfo(number=102, title="Feature B", order=2),
            ],
        )
        yml_path = specs_root / "100" / "hierarchy.yml"
        write_hierarchy_yml(yml_path, metadata)

        mock_state.side_effect = lambda n: make_issue_state(n)

        result1 = processor.trigger_first_child(100, yml_path)
        assert result1.action == CascadeAction.TRIGGERED
        assert result1.event is not None
        assert result1.event.target_issue == 101
        assert result1.event.direction == CascadeDirection.PARENT_TO_CHILD
        assert_label_applied(mock_label, 101)

        mock_label.reset_mock()
        result2 = processor.trigger_next_sibling(101, yml_path)
        assert result2.action == CascadeAction.TRIGGERED
        assert result2.event is not None
        assert result2.event.target_issue == 102
        assert result2.event.direction == CascadeDirection.SIBLING_TO_SIBLING
        assert_label_applied(mock_label, 102)


class TestCompletionCommentAfterLastTask:
    """T010: Completion comment on child + parent notification after last child."""

    def test_cascade_complete_posts_comment_on_parent(
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

        processor.trigger_first_child(101, yml_path)
        processor.trigger_next_sibling(103, yml_path)

        result = processor.trigger_next_sibling(104, yml_path)
        assert result.action == CascadeAction.CASCADE_COMPLETE

        assert_comment_posted(mock_comment, 104, "cascade complete")
        assert_comment_posted(mock_comment, 101, "All subtasks have completed")


class TestFullEpicToTaskCascadeFilesystem:
    """T011: End-to-end filesystem structure verification."""

    def test_nested_hierarchy_yml_files(self, specs_root: Path) -> None:
        epic_meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[
                ChildInfo(number=101, title="Feature: Authentication", order=1),
                ChildInfo(number=102, title="Feature: Authorization", order=2),
            ],
        )
        write_hierarchy_yml(specs_root / "100" / "hierarchy.yml", epic_meta)

        feat101_meta = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=100,
            children=[
                ChildInfo(number=103, title="Task: Login form", order=1),
                ChildInfo(number=104, title="Task: Password reset", order=2),
            ],
        )
        (specs_root / "100" / "101").mkdir(parents=True, exist_ok=True)
        write_hierarchy_yml(specs_root / "100" / "101" / "hierarchy.yml", feat101_meta)

        task103_meta = HierarchyMetadata(
            level=HierarchyLevel.TASK,
            parent=101,
        )
        (specs_root / "100" / "101" / "103").mkdir(parents=True, exist_ok=True)
        write_hierarchy_yml(specs_root / "100" / "101" / "103" / "hierarchy.yml", task103_meta)

        assert (specs_root / "100" / "hierarchy.yml").exists()
        assert (specs_root / "100" / "101" / "hierarchy.yml").exists()
        assert (specs_root / "100" / "101" / "103" / "hierarchy.yml").exists()

        epic_data = read_hierarchy_yml(specs_root / "100" / "hierarchy.yml")
        assert epic_data.level == HierarchyLevel.EPIC
        assert len(epic_data.children) == 2

        feat_data = read_hierarchy_yml(specs_root / "100" / "101" / "hierarchy.yml")
        assert feat_data.level == HierarchyLevel.FEATURE
        assert feat_data.parent == 100

        task_data = read_hierarchy_yml(specs_root / "100" / "101" / "103" / "hierarchy.yml")
        assert task_data.level == HierarchyLevel.TASK
        assert task_data.parent == 101


class TestOrderingDeterminism:
    """T012: Children order preserved from API response."""

    def test_non_canonical_order_preserved(
        self,
        specs_root: Path,
        mock_cascade_api: tuple[CascadeProcessor, MagicMock, MagicMock, MagicMock],
    ) -> None:
        processor, mock_state, mock_label, mock_comment = mock_cascade_api

        metadata = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[
                ChildInfo(number=104, title="Task B", order=1),
                ChildInfo(number=103, title="Task A", order=2),
            ],
        )
        yml_path = specs_root / "100" / "hierarchy.yml"
        write_hierarchy_yml(yml_path, metadata)

        data = yaml.safe_load(yml_path.read_text())
        assert data["children"][0]["number"] == 104
        assert data["children"][1]["number"] == 103

        mock_state.side_effect = lambda n: make_issue_state(n)

        result = processor.trigger_first_child(100, yml_path)
        assert result.action == CascadeAction.TRIGGERED
        assert result.event is not None
        assert result.event.target_issue == 104
