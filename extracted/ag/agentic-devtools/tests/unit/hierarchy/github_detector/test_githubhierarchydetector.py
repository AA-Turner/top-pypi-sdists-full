"""Tests for GitHubHierarchyDetector."""

from __future__ import annotations

from dataclasses import dataclass, field
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.hierarchy import HierarchyValidationError
from agentic_devtools.hierarchy.github_detector import GitHubHierarchyDetector
from agentic_devtools.hierarchy.models import HierarchyLevel


# Lightweight mock node that mimics speckit HierarchyNode without validation
@dataclass
class _MockNode:
    title: str = "Issue"
    level: object = None
    parent: str | None = None
    children: list = field(default_factory=list)


@dataclass
class _MockChild:
    key: str = "1"
    title: str = "Child"
    order: int | None = None


class TestDetectParent:
    """Cover detect_parent method."""

    def test_returns_parent_number(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(parent="42", level=SL.FEATURE)
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            assert det.detect_parent(10) == 42

    def test_returns_none_no_parent(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(parent=None, level=SL.EPIC)
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            assert det.detect_parent(10) is None

    def test_returns_none_invalid_parent(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(parent="not-a-number", level=SL.EPIC)
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            assert det.detect_parent(10) is None


class TestDetectChildren:
    """Cover detect_children method."""

    def test_returns_children_list(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(
            level=SL.EPIC,
            children=[_MockChild(key="20", title="Child A"), _MockChild(key="30", title="Child B")],
        )
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            result = det.detect_children(10)
            assert result == [(20, "Child A"), (30, "Child B")]

    def test_skips_invalid_child_keys(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(
            level=SL.EPIC,
            children=[_MockChild(key="abc", title="Bad"), _MockChild(key="5", title="Good")],
        )
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            result = det.detect_children(10)
            assert result == [(5, "Good")]


class TestClassify:
    """Cover classify method."""

    def test_standalone_no_parent_no_children(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(parent=None, children=[], level=SL.TASK)
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            assert det.classify(10) == HierarchyLevel.STANDALONE

    def test_epic_with_children(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(parent=None, children=[_MockChild(key="2", title="C")], level=SL.EPIC)
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            assert det.classify(10) == HierarchyLevel.EPIC

    def test_feature_with_parent(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(parent="1", children=[_MockChild(key="3", title="C")], level=SL.FEATURE)
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            assert det.classify(10) == HierarchyLevel.FEATURE

    def test_unknown_level_defaults_to_task(self):

        # Use a level that's not in the map - need to get one that differs
        # Actually all 3 are mapped, so let's set an invalid level to test default
        node = _MockNode(parent="1", children=[], level="unknown_level")
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            assert det.classify(10) == HierarchyLevel.TASK


class TestBuildMetadata:
    """Cover build_metadata method."""

    def test_standalone(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(parent=None, children=[], level=SL.TASK)
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            meta = det.build_metadata(10)
            assert meta.level == HierarchyLevel.STANDALONE
            assert meta.parent is None
            assert meta.children == []

    def test_with_parent_and_children(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(
            parent="5",
            children=[_MockChild(key="20", title="A"), _MockChild(key="30", title="B")],
            level=SL.FEATURE,
        )
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            meta = det.build_metadata(10)
            assert meta.level == HierarchyLevel.FEATURE
            assert meta.parent == 5
            assert len(meta.children) == 2
            assert meta.children[0].number == 20

    def test_invalid_parent_becomes_none(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(parent="not-a-number", children=[], level=SL.TASK)
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            meta = det.build_metadata(10)
            assert meta.parent is None

    def test_invalid_child_key_skipped(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(
            parent=None,
            children=[_MockChild(key="abc", title="Bad"), _MockChild(key="7", title="Good")],
            level=SL.EPIC,
        )
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            meta = det.build_metadata(10)
            assert len(meta.children) == 1
            assert meta.children[0].number == 7

    def test_unknown_level_in_build_metadata(self):
        """Level not in map defaults to TASK."""
        node = _MockNode(parent="1", children=[], level="unknown_level")
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            meta = det.build_metadata(10)
            assert meta.level == HierarchyLevel.TASK

    def test_depth_capped_children_become_informational(self):
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(
            parent="5",
            children=[_MockChild(key="20", title="Too Deep")],
            level=SL.TASK,
        )
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            meta = det.build_metadata(10)
            assert meta.level == HierarchyLevel.TASK
            assert meta.children == []
            assert len(meta.informational_children) == 1
            assert meta.informational_children[0].number == 20

    def test_child_order_is_preserved_from_child_entry(self):
        """build_metadata preserves ChildEntry.order in the ChildInfo it produces.

        Without this the adapter would always set order=None, causing every
        parent with multiple children to be flagged as ordering-ambiguous by
        the nest discovery layer.
        """
        from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SL

        node = _MockNode(
            parent=None,
            children=[
                _MockChild(key="20", title="A", order=3),
                _MockChild(key="30", title="B", order=7),
                _MockChild(key="40", title="C", order=None),
            ],
            level=SL.EPIC,
        )
        with patch(
            "agentic_devtools.hierarchy.github_detector.SpeckitGitHubDetector.build_hierarchy_tree",
            return_value=node,
        ):
            det = GitHubHierarchyDetector("owner", "repo")
            meta = det.build_metadata(10)
            assert meta.children[0].order == 3
            assert meta.children[1].order == 7
            assert meta.children[2].order is None


class TestValidateRepositoryAccess:
    """Cover validate_repository_access delegation."""

    def test_delegates_to_speckit_detector(self) -> None:
        """validate_repository_access delegates to the underlying speckit detector."""
        det = GitHubHierarchyDetector("owner", "repo")
        with patch.object(det._detector, "validate_repository_access") as mock_validate:
            det.validate_repository_access()
            mock_validate.assert_called_once_with()

    def test_propagates_exception_from_speckit_detector(self) -> None:
        """Exceptions from the speckit detector propagate unchanged."""
        det = GitHubHierarchyDetector("owner", "nonexistent")
        with patch.object(
            det._detector,
            "validate_repository_access",
            side_effect=HierarchyValidationError("api", "inaccessible"),
        ):
            with pytest.raises(HierarchyValidationError, match="inaccessible"):
                det.validate_repository_access()
