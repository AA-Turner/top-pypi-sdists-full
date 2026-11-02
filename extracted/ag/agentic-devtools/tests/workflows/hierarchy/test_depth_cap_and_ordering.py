"""Integration tests for depth cap and ordering determinism (US-6).

Verifies that 4th-level children go to informational_children only,
and ordering from the API response is preserved in hierarchy.yml and cascade.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import yaml

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor
from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import (
    ChildInfo,
    HierarchyLevel,
    HierarchyMetadata,
)

from .conftest import assert_label_applied, make_issue_state


class TestFourthLevelInInformationalChildrenOnly:
    """T027: 4th-level children appear in informational_children, not children."""

    def test_informational_children_no_cascade(
        self,
        specs_root: Path,
        mock_cascade_api: tuple[CascadeProcessor, MagicMock, MagicMock, MagicMock],
    ) -> None:
        processor, mock_state, mock_label, mock_comment = mock_cascade_api

        metadata = HierarchyMetadata(
            level=HierarchyLevel.TASK,
            parent=101,
            children=[],
            informational_children=[
                ChildInfo(number=107, title="Sub-task: Deep child"),
            ],
        )
        yml_path = specs_root / "100" / "101" / "103" / "hierarchy.yml"
        write_hierarchy_yml(yml_path, metadata)

        data = yaml.safe_load(yml_path.read_text())
        assert len(data["children"]) == 0
        assert len(data["informational_children"]) == 1
        assert data["informational_children"][0]["number"] == 107

        mock_state.side_effect = lambda n: make_issue_state(n)
        result = processor.trigger_first_child(103, yml_path)
        assert result.action == CascadeAction.NO_CHILDREN
        mock_label.assert_not_called()


class TestOrderingPreservedFromApiResponse:
    """T028: API order is preserved in hierarchy.yml and cascade triggers."""

    def test_non_numeric_order_preserved(
        self,
        specs_root: Path,
        mock_cascade_api: tuple[CascadeProcessor, MagicMock, MagicMock, MagicMock],
    ) -> None:
        processor, mock_state, mock_label, mock_comment = mock_cascade_api

        metadata = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=100,
            children=[
                ChildInfo(number=104, title="Task B", order=1),
                ChildInfo(number=103, title="Task A", order=2),
            ],
        )
        yml_path = specs_root / "101" / "hierarchy.yml"
        write_hierarchy_yml(yml_path, metadata)

        data = yaml.safe_load(yml_path.read_text())
        assert data["children"][0]["number"] == 104
        assert data["children"][1]["number"] == 103

        mock_state.side_effect = lambda n: make_issue_state(n)

        result = processor.trigger_first_child(101, yml_path)
        assert result.action == CascadeAction.TRIGGERED
        assert result.event is not None
        assert result.event.target_issue == 104
        assert_label_applied(mock_label, 104)
