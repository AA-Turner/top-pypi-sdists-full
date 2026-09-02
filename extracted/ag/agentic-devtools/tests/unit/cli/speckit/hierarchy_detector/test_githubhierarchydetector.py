"""Tests for GitHubHierarchyDetector class."""

from __future__ import annotations

import json
import re
import subprocess
import time
from datetime import datetime
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyDetector,
    HierarchyLevel,
    HierarchyNode,
    HierarchyValidationError,
)
from agentic_devtools.cli.speckit.hierarchy_detector import (
    GitHubHierarchyDetector,
)


def _make_rest_response(items: list | dict, status: int = 200) -> str:
    """Build a fake gh api --include response with headers + JSON body."""
    headers = (
        f"HTTP/2 {status}\ncontent-type: application/json\nx-ratelimit-remaining: 4990\nx-ratelimit-reset: 9999999999\n"
    )
    body = json.dumps(items)
    return f"{headers}\n{body}"


def _make_graphql_response(data: dict, status: int = 200) -> str:
    """Build a fake gh api graphql --include response."""
    headers = (
        f"HTTP/2 {status}\ncontent-type: application/json\nx-ratelimit-remaining: 4990\nx-ratelimit-reset: 9999999999\n"
    )
    body = json.dumps(data)
    return f"{headers}\n{body}"


def _mock_run_safe(stdout: str = "", stderr: str = "", returncode: int = 0):
    """Create a mock run_safe result."""
    result = MagicMock(spec=subprocess.CompletedProcess)
    result.stdout = stdout
    result.stderr = stderr
    result.returncode = returncode
    return result


class TestGetChildren:
    """Tests for GitHubHierarchyDetector.get_children."""

    def test_returns_entries(self) -> None:
        """Happy path: returns ChildEntry list from REST API."""
        items = [
            {"number": 101, "title": "Child 1", "position": 0},
            {"number": 102, "title": "Child 2", "position": 1},
            {"number": 103, "title": "Child 3", "position": 2},
        ]
        response = _make_rest_response(items)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector.get_children("owner", "repo", 100)

        assert len(children) == 3
        assert children[0] == ChildEntry(key="101", title="Child 1", order=1)
        assert children[1] == ChildEntry(key="102", title="Child 2", order=2)
        assert children[2] == ChildEntry(key="103", title="Child 3", order=3)

    def test_empty_list(self) -> None:
        """Returns empty list when no sub-issues."""
        response = _make_rest_response([])

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector.get_children("owner", "repo", 200)

        assert children == []

    def test_advisory_order_ignored_uses_position_index(self) -> None:
        """advisory_order and position are ignored; 1-based index is always used."""
        items = [
            {"number": 101, "title": "Child", "advisory_order": 5, "position": 0},
        ]
        response = _make_rest_response(items)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector.get_children("owner", "repo", 100)

        assert children[0].order == 1

    def test_position_ignored(self) -> None:
        """position is ignored; 1-based index is always used."""
        items = [
            {"number": 101, "title": "Child", "position": 3},
        ]
        response = _make_rest_response(items)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector.get_children("owner", "repo", 100)

        assert children[0].order == 1

    def test_index_based_order(self) -> None:
        """1-based index used for order assignment."""
        items = [
            {"number": 101, "title": "Child"},
        ]
        response = _make_rest_response(items)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector.get_children("owner", "repo", 100)

        assert children[0].order == 1

    def test_order_always_one_based(self) -> None:
        """Order is always 1-based regardless of advisory_order or position fields."""
        items = [
            {"number": 101, "title": "Child", "advisory_order": 0, "position": 5},
        ]
        response = _make_rest_response(items)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector.get_children("owner", "repo", 100)

        assert children[0].order == 1

    def test_graphql_fallback_on_rest_failure(self) -> None:
        """Falls back to GraphQL when REST fails (non-404)."""
        graphql_data = {
            "data": {
                "repository": {
                    "issue": {
                        "subIssues": {
                            "nodes": [
                                {"number": 201, "title": "GQL Child 1"},
                                {"number": 202, "title": "GQL Child 2"},
                            ]
                        }
                    }
                }
            }
        }
        graphql_response = _make_graphql_response(graphql_data)

        call_count = [0]

        def mock_run(cmd, **kwargs):
            call_count[0] += 1
            if "graphql" not in cmd:
                # REST fails
                return _mock_run_safe(stderr="403 rate limited", returncode=1)
            # GraphQL succeeds
            return _mock_run_safe(stdout=graphql_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector.get_children("owner", "repo", 100)

        assert len(children) == 2
        assert children[0].key == "201"
        assert children[1].key == "202"
        # GraphQL fallback uses 1-based index for order
        assert children[0].order == 1
        assert children[1].order == 2

    def test_cross_repo_child(self) -> None:
        """Cross-repo children use qualified key format."""
        items = [
            {
                "number": 101,
                "title": "Cross-repo child",
                "repository": {
                    "owner": {"login": "other-org"},
                    "name": "other-repo",
                },
            },
        ]
        response = _make_rest_response(items)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector.get_children("owner", "repo", 100)

        assert len(children) == 1
        assert children[0].key == "other-org/other-repo#101"

    def test_graphql_null_issue_raises_validation_error(self) -> None:
        """GraphQL fallback with issue=null raises HierarchyValidationError."""
        graphql_data = {"data": {"repository": {"issue": None}}}
        graphql_response = _make_graphql_response(graphql_data)

        def mock_run(cmd, **kwargs):
            if "graphql" not in cmd:
                return _mock_run_safe(stderr="500 upstream error", returncode=1)
            return _mock_run_safe(stdout=graphql_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="missing issue"):
                detector.get_children("owner", "repo", 100)

    def test_graphql_missing_repository_raises_validation_error(self) -> None:
        """GraphQL fallback with repository=null raises HierarchyValidationError."""
        graphql_data = {"data": {"repository": None}}
        graphql_response = _make_graphql_response(graphql_data)

        def mock_run(cmd, **kwargs):
            if "graphql" not in cmd:
                return _mock_run_safe(stderr="500 upstream error", returncode=1)
            return _mock_run_safe(stdout=graphql_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="missing repository"):
                detector.get_children("owner", "repo", 100)

    def test_graphql_nodes_non_list_returns_empty(self) -> None:
        """GraphQL subIssues.nodes as non-list is normalized to empty."""
        graphql_data = {"data": {"repository": {"issue": {"subIssues": {"nodes": {"number": 101}}}}}}
        graphql_response = _make_graphql_response(graphql_data)

        def mock_run(cmd, **kwargs):
            if "graphql" not in cmd:
                return _mock_run_safe(stderr="500 upstream error", returncode=1)
            return _mock_run_safe(stdout=graphql_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector.get_children("owner", "repo", 100)

        assert children == []


class TestGetParent:
    """Tests for GitHubHierarchyDetector.get_parent."""

    def test_returns_parent_number(self) -> None:
        """Returns parent issue number as string when parent exists."""
        graphql_data = {"data": {"repository": {"issue": {"parent": {"number": 100}}}}}
        response = _make_graphql_response(graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            parent = detector.get_parent("owner", "repo", 102)

        assert parent == "100"

    def test_no_parent_returns_none(self) -> None:
        """Returns None when issue has no parent."""
        graphql_data = {"data": {"repository": {"issue": {"parent": None}}}}
        response = _make_graphql_response(graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            parent = detector.get_parent("owner", "repo", 500)

        assert parent is None

    def test_non_dict_parent_returns_none(self) -> None:
        """Returns None when GraphQL parent payload has unexpected shape."""
        graphql_data = {"data": {"repository": {"issue": {"parent": "unexpected-parent"}}}}
        response = _make_graphql_response(graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            parent = detector.get_parent("owner", "repo", 500)

        assert parent is None

    def test_api_error_raises(self) -> None:
        """Raises HierarchyValidationError on API failure."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stderr="server error", returncode=1),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="GraphQL API failed"):
                detector.get_parent("owner", "repo", 999)

    def test_null_issue_raises_validation_error(self) -> None:
        """GraphQL issue=null raises HierarchyValidationError."""
        graphql_data = {"data": {"repository": {"issue": None}}}
        response = _make_graphql_response(graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="missing issue"):
                detector.get_parent("owner", "repo", 999)

    def test_missing_repository_raises_validation_error(self) -> None:
        """GraphQL repository=null raises HierarchyValidationError."""
        graphql_data = {"data": {"repository": None}}
        response = _make_graphql_response(graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="missing repository"):
                detector.get_parent("owner", "repo", 999)


class TestGetLevel:
    """Tests for GitHubHierarchyDetector.get_level."""

    def test_epic_has_grandchildren(self) -> None:
        """Issue with children that have children → EPIC."""
        children_data = [
            {"number": 20, "title": "Feature 1", "position": 0},
            {"number": 21, "title": "Feature 2", "position": 1},
        ]
        rest_response = _make_rest_response(children_data)

        batch_graphql_data = {
            "data": {
                "repository": {
                    "issue_20": {"subIssues": {"totalCount": 3}},
                    "issue_21": {"subIssues": {"totalCount": 0}},
                }
            }
        }
        graphql_response = _make_graphql_response(batch_graphql_data)
        parent_none_response = _make_graphql_response({"data": {"repository": {"issue": {"parent": None}}}})

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                if "parent { number }" in cmd_str:
                    return _mock_run_safe(stdout=parent_none_response)
                return _mock_run_safe(stdout=graphql_response)
            return _mock_run_safe(stdout=rest_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 10)

        assert level == HierarchyLevel.EPIC

    def test_feature_children_all_leaves(self) -> None:
        """Issue with children that are all leaves → FEATURE."""
        children_data = [
            {"number": 30, "title": "Task 1", "position": 0},
            {"number": 31, "title": "Task 2", "position": 1},
        ]
        rest_response = _make_rest_response(children_data)

        batch_graphql_data = {
            "data": {
                "repository": {
                    "issue_30": {"subIssues": {"totalCount": 0}},
                    "issue_31": {"subIssues": {"totalCount": 0}},
                }
            }
        }
        graphql_response = _make_graphql_response(batch_graphql_data)
        parent_none_response = _make_graphql_response({"data": {"repository": {"issue": {"parent": None}}}})

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                if "parent { number }" in cmd_str:
                    return _mock_run_safe(stdout=parent_none_response)
                return _mock_run_safe(stdout=graphql_response)
            return _mock_run_safe(stdout=rest_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 20)

        assert level == HierarchyLevel.FEATURE

    def test_task_no_children_no_parent(self) -> None:
        """Standalone issue with no children and no parent → TASK."""
        rest_response = _make_rest_response([])
        graphql_no_parent = _make_graphql_response({"data": {"repository": {"issue": {"parent": None}}}})

        def mock_run(cmd, **kwargs):
            if "graphql" in cmd:
                return _mock_run_safe(stdout=graphql_no_parent)
            return _mock_run_safe(stdout=rest_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 999)

        assert level == HierarchyLevel.TASK

    def test_batch_query_failure_fallback_to_feature(self) -> None:
        """Batch query failure falls back to FEATURE with warning."""
        children_data = [
            {"number": 30, "title": "Task 1", "position": 0},
        ]
        rest_response = _make_rest_response(children_data)

        call_count = [0]
        parent_none_response = _make_graphql_response({"data": {"repository": {"issue": {"parent": None}}}})

        def mock_run(cmd, **kwargs):
            call_count[0] += 1
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                if "parent { number }" in cmd_str:
                    return _mock_run_safe(stdout=parent_none_response)
                # Batch query fails
                return _mock_run_safe(stderr="server error", returncode=1)
            return _mock_run_safe(stdout=rest_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 10)

        assert level == HierarchyLevel.FEATURE

    def test_depth_cap_returns_task(self) -> None:
        """Issues at depth >= MAX_DEPTH are classified as TASK without further classification."""
        children_response = _make_rest_response([])
        parent_graphql = {"data": {"repository": {"issue": {"parent": None}}}}
        parent_response = _make_graphql_response(parent_graphql)

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                return _mock_run_safe(stdout=parent_response)
            return _mock_run_safe(stdout=children_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42, _depth=3)

        assert level == HierarchyLevel.TASK

    def test_depth_cap_with_children_returns_task(self) -> None:
        """Depth cap is enforced before child classification — TASK even when children exist."""
        # Children are present, which would normally trigger batch-check and return
        # EPIC or FEATURE; depth cap in _classify_level must short-circuit first.
        children_data = [{"number": 10, "title": "Child", "position": 0}]
        children_response = _make_rest_response(children_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=children_response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42, _depth=3)

        # Must be TASK from depth cap, not FEATURE/EPIC from child classification
        assert level == HierarchyLevel.TASK

    def test_batch_query_null_repository_raises(self) -> None:
        """Batch query with repository=null raises HierarchyValidationError."""
        batch_graphql_data = {"data": {"repository": None}}
        graphql_response = _make_graphql_response(batch_graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=graphql_response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="missing repository"):
                detector._batch_check_children_have_children("owner", "repo", [20])


class TestBuildHierarchyTree:
    """Tests for GitHubHierarchyDetector.build_hierarchy_tree."""

    def test_full_node_construction(self) -> None:
        """Builds complete HierarchyNode with all fields."""
        # Mock: title fetch, parent query, children query, batch level check
        issue_detail = {"number": 20, "title": "Add login feature"}
        issue_response = _make_rest_response(issue_detail)

        children_data = [
            {"number": 30, "title": "Implement form", "position": 0},
            {"number": 31, "title": "Add tests", "position": 1},
        ]
        children_response = _make_rest_response(children_data)

        parent_response_by_number = {
            "20": _make_graphql_response({"data": {"repository": {"issue": {"parent": {"number": 10}}}}}),
            "10": _make_graphql_response({"data": {"repository": {"issue": {"parent": None}}}}),
        }

        batch_graphql = {
            "data": {
                "repository": {
                    "issue_30": {"subIssues": {"totalCount": 0}},
                    "issue_31": {"subIssues": {"totalCount": 0}},
                }
            }
        }
        batch_response = _make_graphql_response(batch_graphql)

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                if "issue_" in cmd_str:
                    return _mock_run_safe(stdout=batch_response)
                if "parent { number }" in cmd_str:
                    if "number=20" in cmd_str:
                        return _mock_run_safe(stdout=parent_response_by_number["20"])
                    if "number=10" in cmd_str:
                        return _mock_run_safe(stdout=parent_response_by_number["10"])
                    return _mock_run_safe(stdout=parent_response_by_number["10"])
                return _mock_run_safe(stdout=batch_response)
            # REST calls
            if "sub_issues" in cmd_str:
                return _mock_run_safe(stdout=children_response)
            return _mock_run_safe(stdout=issue_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            node = detector.build_hierarchy_tree("owner", "repo", 20)

        assert node.title == "Add login feature"
        assert node.level == HierarchyLevel.FEATURE
        assert node.parent == "10"
        assert len(node.children) == 2
        assert node.children[0].key == "30"
        assert node.children[1].key == "31"
        assert node.processed_at is not None
        assert isinstance(node.processed_at, datetime)

    def test_circular_reference_detected(self) -> None:
        """Circular references raise HierarchyValidationError."""
        detector = GitHubHierarchyDetector("owner", "repo")
        visited = {"owner/repo#42"}
        with pytest.raises(HierarchyValidationError, match="Circular reference"):
            detector.build_hierarchy_tree("owner", "repo", 42, _visited=visited)

    def test_yaml_roundtrip(self) -> None:
        """Returned node is serializable via to_dict()."""
        issue_detail = {"number": 50, "title": "Test Issue"}
        issue_response = _make_rest_response(issue_detail)

        children_response = _make_rest_response([])
        parent_graphql = {"data": {"repository": {"issue": {"parent": None}}}}
        parent_response = _make_graphql_response(parent_graphql)

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                return _mock_run_safe(stdout=parent_response)
            if "sub_issues" in cmd_str:
                return _mock_run_safe(stdout=children_response)
            return _mock_run_safe(stdout=issue_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            node = detector.build_hierarchy_tree("owner", "repo", 50)

        # Verify to_dict() works and has expected structure
        data = node.to_dict()
        assert data["title"] == "Test Issue"
        assert data["level"] == "task"
        assert data["parent"] is None
        assert data["children"] == []
        assert data["processed_at"] is not None


class TestDetectHierarchy:
    """Tests for GitHubHierarchyDetector.detect_hierarchy."""

    def test_bare_number_uses_constructor_defaults(self) -> None:
        """Bare number issue key uses constructor owner/repo."""
        issue_detail = {"number": 42, "title": "My Issue"}
        issue_response = _make_rest_response(issue_detail)
        children_response = _make_rest_response([])
        parent_graphql = {"data": {"repository": {"issue": {"parent": None}}}}
        parent_response = _make_graphql_response(parent_graphql)

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                return _mock_run_safe(stdout=parent_response)
            if "sub_issues" in cmd_str:
                return _mock_run_safe(stdout=children_response)
            return _mock_run_safe(stdout=issue_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("my-org", "my-repo")
            node = detector.detect_hierarchy("42")

        assert node.title == "My Issue"
        assert isinstance(node, HierarchyNode)

    def test_qualified_reference_overrides(self) -> None:
        """Qualified reference overrides constructor defaults."""
        issue_detail = {"number": 99, "title": "Other Issue"}
        issue_response = _make_rest_response(issue_detail)
        children_response = _make_rest_response([])
        parent_graphql = {"data": {"repository": {"issue": {"parent": None}}}}
        parent_response = _make_graphql_response(parent_graphql)

        called_with_endpoints = []

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            called_with_endpoints.append(cmd_str)
            if "graphql" in cmd_str:
                return _mock_run_safe(stdout=parent_response)
            if "sub_issues" in cmd_str:
                return _mock_run_safe(stdout=children_response)
            return _mock_run_safe(stdout=issue_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("default-org", "default-repo")
            node = detector.detect_hierarchy("other-org/other-repo#99")

        assert node.title == "Other Issue"
        # Verify the REST calls used the parsed owner/repo
        rest_calls = [c for c in called_with_endpoints if "other-org/other-repo" in c]
        assert len(rest_calls) > 0

    def test_protocol_compliance(self) -> None:
        """GitHubHierarchyDetector satisfies HierarchyDetector protocol."""
        detector = GitHubHierarchyDetector("owner", "repo")
        assert isinstance(detector, HierarchyDetector)

    def test_invalid_issue_key_raises_validation_error(self) -> None:
        """Invalid issue references are wrapped in HierarchyValidationError."""
        detector = GitHubHierarchyDetector("owner", "repo")

        with pytest.raises(HierarchyValidationError, match="Invalid issue reference format"):
            detector.detect_hierarchy("not-a-valid-issue-key")


class TestRateLimit:
    """Tests for rate-limit awareness."""

    def test_pause_when_below_threshold(self) -> None:
        """Pauses when remaining is below threshold."""
        detector = GitHubHierarchyDetector("owner", "repo", rate_limit_threshold=10)
        detector._rate_limit_remaining = 5
        detector._rate_limit_reset = time.time() + 2

        with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
            detector._check_rate_limit()
            mock_sleep.assert_called_once()
            # Duration should be between 1 and 120
            call_args = mock_sleep.call_args[0][0]
            assert 1.0 <= call_args <= 120.0

    def test_no_pause_above_threshold(self) -> None:
        """No pause when remaining is above threshold."""
        detector = GitHubHierarchyDetector("owner", "repo", rate_limit_threshold=10)
        detector._rate_limit_remaining = 100
        detector._rate_limit_reset = time.time() + 60

        with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
            detector._check_rate_limit()
            mock_sleep.assert_not_called()

    def test_custom_threshold(self) -> None:
        """Custom threshold value changes pause trigger point."""
        detector = GitHubHierarchyDetector("owner", "repo", rate_limit_threshold=50)
        detector._rate_limit_remaining = 45
        detector._rate_limit_reset = time.time() + 5

        with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
            detector._check_rate_limit()
            mock_sleep.assert_called_once()

    def test_pause_duration_bounded(self) -> None:
        """Pause duration is bounded between 1 and 120 seconds."""
        detector = GitHubHierarchyDetector("owner", "repo", rate_limit_threshold=10)
        detector._rate_limit_remaining = 5

        # Test minimum bound (reset time in the past)
        detector._rate_limit_reset = time.time() - 100
        with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
            detector._check_rate_limit()
            call_args = mock_sleep.call_args[0][0]
            assert call_args == 1.0

        # Test maximum bound (reset time far in the future)
        detector._rate_limit_reset = time.time() + 500
        with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
            detector._check_rate_limit()
            call_args = mock_sleep.call_args[0][0]
            assert call_args == 120.0


class TestExponentialBackoff:
    """Tests for exponential backoff retry logic."""

    def test_retries_with_backoff(self) -> None:
        """Retries with exponential backoff on failure."""
        call_count = [0]

        def mock_run(cmd, **kwargs):
            call_count[0] += 1
            return _mock_run_safe(stderr="server error", returncode=1)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="REST API failed"):
                    detector._run_gh_rest("repos/owner/repo/issues/42/sub_issues")

        assert call_count[0] == 5  # _MAX_RETRIES

    def test_404_fails_fast_no_retry(self) -> None:
        """404 errors fail fast without retrying."""
        call_count = [0]

        def mock_run(cmd, **kwargs):
            call_count[0] += 1
            return _mock_run_safe(stderr="404 Not Found", returncode=1)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="404"):
                detector._run_gh_rest("repos/owner/repo/issues/999/sub_issues")

        assert call_count[0] == 1  # No retries for 404


class TestMalformedResponses:
    """Tests for handling malformed/unexpected responses."""

    def test_malformed_json_raises(self) -> None:
        """Malformed JSON raises HierarchyValidationError after exhausting retries."""
        bad_response = "HTTP/2 200\ncontent-type: application/json\n\nnot valid json"

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=bad_response),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="Malformed JSON"):
                    detector._run_gh_rest("repos/owner/repo/issues/42/sub_issues")

    def test_malformed_json_retries_then_succeeds(self) -> None:
        """Transient malformed JSON is retried; a later valid response succeeds."""
        bad_response = "HTTP/2 200\ncontent-type: application/json\n\nnot valid json"
        good_items = [{"number": 1, "title": "Child", "position": 0}]
        good_response = _make_rest_response(good_items)

        mock_run = MagicMock(
            side_effect=[
                _mock_run_safe(stdout=bad_response),
                _mock_run_safe(stdout=bad_response),
                _mock_run_safe(stdout=good_response),
            ]
        )

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            new=mock_run,
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                data, _ = detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

        assert data == good_items
        assert mock_run.call_count == 3


class TestRunGhRestEdgeCases:
    """Edge-case tests for _run_gh_rest method."""

    def test_gh_cli_missing_raises_validation_error(self) -> None:
        """Missing gh binary raises HierarchyValidationError."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=FileNotFoundError("gh not found"),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="`gh`"):
                detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

    def test_no_blocks_fallback_json_parse(self) -> None:
        """When _split_header_body_blocks returns no blocks, falls back to direct JSON parse."""
        # Simulate stdout that has no HTTP/ prefix (so _split_header_body_blocks returns [])
        raw_json = json.dumps([{"number": 1}])

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=raw_json),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            data, headers = detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

        assert data == [{"number": 1}]
        assert headers == ""

    def test_no_blocks_invalid_json_raises(self) -> None:
        """When blocks is empty and direct JSON parse also fails, raises error after retries."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout="not json at all"),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="Empty or unparseable"):
                    detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

    def test_no_blocks_invalid_json_retries_then_succeeds(self) -> None:
        """No-blocks fallback retries on JSONDecodeError; succeeds on a later attempt."""
        good_items = [{"number": 2, "title": "Child", "position": 0}]
        good_raw = json.dumps(good_items)  # no HTTP/ prefix → no-blocks path

        mock_run = MagicMock(
            side_effect=[
                _mock_run_safe(stdout="not json at all"),
                _mock_run_safe(stdout=good_raw),
            ]
        )

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            new=mock_run,
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                data, headers = detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

        assert data == good_items
        assert headers == ""
        assert mock_run.call_count == 2

    def test_empty_body_in_block_skipped(self) -> None:
        """Blocks with empty body parts are handled — only non-empty bodies parsed."""
        # Two pages: first has an empty body, second has content
        response = (
            "HTTP/2 200\ncontent-type: application/json\n"
            "x-ratelimit-remaining: 100\nx-ratelimit-reset: 9999999999\n\n"
            "   \n"
            "HTTP/2 200\ncontent-type: application/json\n"
            "x-ratelimit-remaining: 99\nx-ratelimit-reset: 9999999999\n\n"
            '[{"number": 1}]'
        )

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            data, _headers = detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

        assert data == [{"number": 1}]

    def test_all_blocks_headers_only_raises_after_retries(self) -> None:
        """All blocks with whitespace-only bodies are treated as retryable error, not empty list."""
        # Both pages return headers but no JSON body — this is a malformed/partial response
        response = (
            "HTTP/2 200\ncontent-type: application/json\n"
            "x-ratelimit-remaining: 100\nx-ratelimit-reset: 9999999999\n\n"
            "   \n"
            "HTTP/2 200\ncontent-type: application/json\n"
            "x-ratelimit-remaining: 99\nx-ratelimit-reset: 9999999999\n\n"
            "   "
        )

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="no JSON body"):
                    detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

    def test_empty_stdout_with_zero_exit_raises_empty_response_error(self) -> None:
        """Empty stdout with returncode=0 reports explicit empty-response failure."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout="", stderr="", returncode=0),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="empty response"):
                    detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")


class TestRunGhGraphqlEdgeCases:
    """Edge-case tests for _run_gh_graphql method."""

    def test_gh_cli_missing_raises_validation_error(self) -> None:
        """Missing gh binary raises HierarchyValidationError."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=FileNotFoundError("gh not found"),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="`gh`"):
                detector._run_gh_graphql("query { viewer { login } }", {})

    def test_query_sent_via_raw_field(self) -> None:
        """String GraphQL inputs are passed via --raw-field to avoid YAML parsing."""
        query = (
            "query($owner: String!, $repo: String!, $number: Int!) { "
            "repository(owner: $owner, name: $repo) { issue(number: $number) { number } } }"
        )
        response = _make_graphql_response({"data": {"repository": {"issue": {"number": 42}}}})
        captured: dict[str, list[str]] = {}

        def mock_run(cmd, **_kwargs):
            captured["cmd"] = cmd
            return _mock_run_safe(stdout=response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            data, _headers = detector._run_gh_graphql(
                query,
                {"owner": "owner", "repo": "repo", "number": 42},
            )

        cmd = captured["cmd"]
        assert data["data"]["repository"]["issue"]["number"] == 42
        raw_fields = [cmd[i + 1] for i, token in enumerate(cmd[:-1]) if token == "--raw-field"]
        assert f"query={query}" in raw_fields
        assert "owner=owner" in raw_fields
        assert "repo=repo" in raw_fields
        assert "--field" in cmd
        assert "number=42" in cmd

    def test_no_blocks_fallback_find_json(self) -> None:
        """When no blocks found, falls back to finding JSON in raw output."""
        # No HTTP/ prefix → _split_header_body_blocks returns []
        raw_with_json = '{"data": {"repository": {"issue": {"parent": null}}}}'

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=raw_with_json),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            data, headers = detector._run_gh_graphql("query { viewer { login } }", {})

        assert data == {"data": {"repository": {"issue": {"parent": None}}}}

    def test_blocks_empty_body_fallback_find_json(self) -> None:
        """When blocks exist but body is empty, falls back to finding JSON in raw output."""
        # HTTP response with headers but empty body after the double newline
        # The body is whitespace-only, so body.strip() is falsy → falls to fallback
        raw = (
            "HTTP/2 200\n"
            "content-type: application/json\n"
            "X-RateLimit-Remaining: 3\n"
            "X-RateLimit-Reset: 1234\n"
            "\n   \n"
            '{"data": {"viewer": {"login": "test"}}}'
        )

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=raw),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            data, headers = detector._run_gh_graphql("query { viewer { login } }", {})

        assert data["data"]["viewer"]["login"] == "test"
        assert "HTTP/2 200" in headers
        assert "content-type: application/json" in headers
        assert "X-RateLimit-Remaining: 3" in headers
        assert detector._rate_limit_remaining == 3
        assert detector._rate_limit_reset == 1234.0

    def test_fallback_preserves_headers_and_updates_rate_limit(self) -> None:
        """Fallback JSON parsing keeps last headers and updates rate-limit state."""
        raw = '{"data": {"viewer": {"login": "test"}}}'
        headers = "HTTP/2 200\ncontent-type: application/json\nX-RateLimit-Remaining: 2\nX-RateLimit-Reset: 5678\n"

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                return_value=_mock_run_safe(stdout=raw),
            ),
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector._split_header_body_blocks",
                return_value=[(headers, "")],
            ),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            data, returned_headers = detector._run_gh_graphql("query { viewer { login } }", {})

        assert data["data"]["viewer"]["login"] == "test"
        assert "HTTP/2 200" in returned_headers
        assert "content-type: application/json" in returned_headers
        assert "X-RateLimit-Remaining: 2" in returned_headers
        assert detector._rate_limit_remaining == 2
        assert detector._rate_limit_reset == 5678.0

    def test_blocks_empty_body_fallback_json_decode_error(self) -> None:
        """When blocks body is empty and fallback JSON also fails, raises error after retries."""
        # Headers present (blocks found) but body is empty; fallback finds no '{'
        raw = "HTTP/2 200\ncontent-type: application/json\n\n   "

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=raw),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="GraphQL API failed"):
                    detector._run_gh_graphql("query { viewer { login } }", {})

    def test_fallback_json_decode_error(self) -> None:
        """When fallback path finds '{' but JSON is invalid, retries then raises."""
        # No HTTP/ prefix → blocks is empty, fallback finds '{' but can't parse
        raw = "some prefix {not valid json at all"

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=raw),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="GraphQL API failed"):
                    detector._run_gh_graphql("query { viewer { login } }", {})

    def test_completely_unparseable_graphql_raises(self) -> None:
        """Completely unparseable GraphQL response raises error."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout="no json anywhere"),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="GraphQL API failed"):
                    detector._run_gh_graphql("query { viewer { login } }", {})

    def test_malformed_json_in_graphql_body_raises(self) -> None:
        """Malformed JSON in GraphQL body raises error after exhausting retries."""
        bad_response = "HTTP/2 200\ncontent-type: application/json\n\n{not valid json"

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=bad_response),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="GraphQL API failed"):
                    detector._run_gh_graphql("query { viewer { login } }", {})

    def test_malformed_graphql_body_retries_then_succeeds(self) -> None:
        """Transient malformed GraphQL body is retried; a later valid response succeeds."""
        bad_response = "HTTP/2 200\ncontent-type: application/json\n\n{not valid json"
        good_data = {"data": {"repository": {"issue": {"number": 42}}}}
        good_response = _make_graphql_response(good_data)

        mock_run = MagicMock(
            side_effect=[
                _mock_run_safe(stdout=bad_response),
                _mock_run_safe(stdout=bad_response),
                _mock_run_safe(stdout=good_response),
            ]
        )

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            new=mock_run,
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                data, _ = detector._run_gh_graphql("query { viewer { login } }", {})

        assert data == good_data
        assert mock_run.call_count == 3

    def test_graphql_errors_in_body_raise(self) -> None:
        """GraphQL body with errors retries until exhausted then raises."""
        from agentic_devtools.cli.speckit.hierarchy_detector import _MAX_RETRIES

        response = _make_graphql_response({"errors": [{"message": "boom"}]})

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="boom"):
                    detector._run_gh_graphql("query { viewer { login } }", {})
        # Sleep is called between each attempt (not after the last one)
        assert mock_sleep.call_count == _MAX_RETRIES - 1

    def test_graphql_errors_in_body_retried(self) -> None:
        """GraphQL body errors are retried; the method succeeds on a later attempt."""
        error_response = _make_graphql_response({"errors": [{"message": "transient"}]})
        good_data = {"data": {"viewer": {"login": "alice"}}}
        good_response = _make_graphql_response(good_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=[
                _mock_run_safe(stdout=error_response),
                _mock_run_safe(stdout=good_response),
            ],
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                data, _ = detector._run_gh_graphql("query { viewer { login } }", {})

        assert data == good_data

    def test_graphql_errors_in_fallback_raise(self) -> None:
        """Fallback JSON discovery retries GraphQL errors until exhausted then raises."""
        from agentic_devtools.cli.speckit.hierarchy_detector import _MAX_RETRIES

        raw = 'prefix {"errors": [{"message": "fallback boom"}]}'

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=raw),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="fallback boom"):
                    detector._run_gh_graphql("query { viewer { login } }", {})
        # Sleep is called between each attempt (not after the last one)
        assert mock_sleep.call_count == _MAX_RETRIES - 1

    def test_empty_stdout_with_zero_exit_raises_empty_response_error(self) -> None:
        """Empty GraphQL stdout with returncode=0 reports explicit empty-response failure."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout="", stderr="", returncode=0),
        ):
            with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep"):
                detector = GitHubHierarchyDetector("owner", "repo")
                with pytest.raises(HierarchyValidationError, match="empty response"):
                    detector._run_gh_graphql("query { viewer { login } }", {})


class TestCheckGraphqlErrorsRetryable:
    """Unit tests for _check_graphql_errors_retryable helper."""

    def test_no_errors_returns_none_and_unchanged_backoff(self) -> None:
        """Clean response returns (None, backoff) — no sleep, no error."""
        detector = GitHubHierarchyDetector("owner", "repo")
        data = {"data": {"viewer": {"login": "alice"}}}
        with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
            err_msg, returned_backoff = detector._check_graphql_errors_retryable(data, attempt=0, backoff=2.0)
        assert err_msg is None
        assert returned_backoff == 2.0
        mock_sleep.assert_not_called()

    def test_graphql_errors_mid_retries_sleeps_and_doubles_backoff(self) -> None:
        """Errors before final attempt trigger sleep and return doubled backoff."""
        detector = GitHubHierarchyDetector("owner", "repo")
        data = {"errors": [{"message": "transient failure"}]}
        with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
            err_msg, returned_backoff = detector._check_graphql_errors_retryable(data, attempt=0, backoff=1.0)
        assert err_msg is not None
        assert "transient failure" in err_msg
        mock_sleep.assert_called_once_with(1.0)
        assert returned_backoff == 2.0

    def test_graphql_errors_on_last_attempt_no_sleep(self) -> None:
        """Errors on the last attempt do not trigger sleep."""
        from agentic_devtools.cli.speckit.hierarchy_detector import _MAX_RETRIES

        detector = GitHubHierarchyDetector("owner", "repo")
        data = {"errors": [{"message": "last attempt error"}]}
        with patch("agentic_devtools.cli.speckit.hierarchy_detector.time.sleep") as mock_sleep:
            err_msg, _ = detector._check_graphql_errors_retryable(data, attempt=_MAX_RETRIES - 1, backoff=16.0)
        assert err_msg is not None
        mock_sleep.assert_not_called()


class TestFetchIssueTitleEdgeCases:
    """Edge-case tests for _fetch_issue_title."""

    def test_missing_title_raises(self) -> None:
        """Raises HierarchyValidationError when title field is absent."""
        response = _make_rest_response({"number": 42, "body": "no title here"})

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="Could not retrieve title"):
                detector._fetch_issue_title("owner", "repo", 42)

    def test_null_title_falls_back_to_issue_label(self) -> None:
        """Null title field is normalized to 'Issue #N' rather than the string 'None'."""
        response = _make_rest_response({"number": 42, "title": None})

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            title = detector._fetch_issue_title("owner", "repo", 42)

        assert title == "Issue #42"
        assert title != "None"


class TestGetChildrenEdgeCases:
    """Edge-case tests for get_children and _get_children_rest."""

    def test_404_not_retried_and_reraised(self) -> None:
        """404 errors from REST are re-raised without GraphQL fallback."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stderr="404 Not Found", returncode=1),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="404"):
                detector.get_children("owner", "repo", 999)

    def test_data_not_list_returns_empty(self) -> None:
        """Non-list REST data returns empty children list."""
        response = _make_rest_response({"message": "not a list"})

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_rest("owner", "repo", 42)

        assert children == []

    def test_non_dict_items_skipped(self) -> None:
        """Non-dict items in the children list are skipped."""
        response = _make_rest_response(["not a dict", {"number": 10, "title": "Valid"}])

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_rest("owner", "repo", 42)

        assert len(children) == 1
        assert children[0].key == "10"

    def test_missing_number_skipped(self) -> None:
        """Items without 'number' field are skipped."""
        response = _make_rest_response([{"title": "No number"}, {"number": 5, "title": "Valid"}])

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_rest("owner", "repo", 42)

        assert len(children) == 1
        assert children[0].key == "5"

    def test_null_title_falls_back_to_issue_label(self) -> None:
        """REST children with null title are normalized to Issue #N."""
        response = _make_rest_response([{"number": 8, "title": None}])

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_rest("owner", "repo", 42)

        assert children[0].title == "Issue #8"

    def test_non_string_title_falls_back_to_issue_label(self) -> None:
        """REST children with non-string title are normalized to Issue #N."""
        response = _make_rest_response([{"number": 9, "title": 1234}])

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_rest("owner", "repo", 42)

        assert children[0].title == "Issue #9"

    def test_blank_string_title_falls_back_to_issue_label(self) -> None:
        """REST children with blank-string title are normalized to Issue #N."""
        response = _make_rest_response([{"number": 13, "title": "   "}])

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_rest("owner", "repo", 42)

        assert children[0].title == "Issue #13"

    def test_cross_repo_child_qualified_key(self) -> None:
        """Cross-repo children get qualified keys and same-repo children follow."""
        items = [
            {
                "number": 101,
                "title": "Cross-repo issue",
                "repository": {
                    "owner": {"login": "other-org"},
                    "name": "other-repo",
                },
            },
            {
                "number": 102,
                "title": "Same-repo with repo info",
                "repository": {
                    "owner": {"login": "owner"},
                    "name": "repo",
                },
            },
        ]
        response = _make_rest_response(items)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_rest("owner", "repo", 42)

        assert len(children) == 2
        assert children[0].key == "other-org/other-repo#101"
        assert children[1].key == "102"

    def test_owner_as_string_falls_back_to_current_repo(self) -> None:
        """When 'owner' field in repository is a non-dict (e.g. string), falls back to current owner."""
        items = [
            {
                "number": 55,
                "title": "Issue with malformed owner",
                "repository": {
                    "owner": "not-a-dict",
                    "name": "repo",
                },
            }
        ]
        response = _make_rest_response(items)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_rest("owner", "repo", 42)

        # Malformed owner falls back to current owner → same repo, plain key
        assert len(children) == 1
        assert children[0].key == "55"

    def test_name_as_non_string_falls_back_to_current_repo(self) -> None:
        """When 'name' field in repository is a non-string, falls back to current repo name."""
        items = [
            {
                "number": 66,
                "title": "Issue with non-string name",
                "repository": {
                    "owner": {"login": "owner"},
                    "name": 12345,
                },
            }
        ]
        response = _make_rest_response(items)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_rest("owner", "repo", 42)

        # Non-string name falls back to current repo → same repo, plain key
        assert len(children) == 1
        assert children[0].key == "66"


class TestGetChildrenGraphqlEdgeCases:
    """Edge-case tests for _get_children_graphql."""

    def test_non_dict_nodes_skipped(self) -> None:
        """Non-dict nodes in GraphQL response are skipped."""
        data = {"data": {"repository": {"issue": {"subIssues": {"nodes": [None, {"number": 5, "title": "Valid"}]}}}}}
        response = _make_graphql_response(data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_graphql("owner", "repo", 42)

        assert len(children) == 1
        assert children[0].key == "5"

    def test_missing_number_in_node_skipped(self) -> None:
        """Nodes without 'number' field are skipped."""
        data = {
            "data": {
                "repository": {
                    "issue": {"subIssues": {"nodes": [{"title": "No number"}, {"number": 7, "title": "Valid"}]}}
                }
            }
        }
        response = _make_graphql_response(data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_graphql("owner", "repo", 42)

        assert len(children) == 1
        assert children[0].key == "7"

    def test_null_title_falls_back_to_issue_label(self) -> None:
        """GraphQL children with null title are normalized to Issue #N."""
        data = {"data": {"repository": {"issue": {"subIssues": {"nodes": [{"number": 11, "title": None}]}}}}}
        response = _make_graphql_response(data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_graphql("owner", "repo", 42)

        assert children[0].title == "Issue #11"

    def test_non_string_title_falls_back_to_issue_label(self) -> None:
        """GraphQL children with non-string title are normalized to Issue #N."""
        data = {"data": {"repository": {"issue": {"subIssues": {"nodes": [{"number": 12, "title": 99}]}}}}}
        response = _make_graphql_response(data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_graphql("owner", "repo", 42)

        assert children[0].title == "Issue #12"

    def test_full_page_with_next_page_emits_warning(self, capsys: pytest.CaptureFixture[str]) -> None:
        """100-node response with hasNextPage=True emits a truncation warning to stderr."""
        nodes = [{"number": i, "title": f"Issue {i}"} for i in range(1, 101)]
        data = {
            "data": {
                "repository": {
                    "issue": {
                        "subIssues": {
                            "pageInfo": {"hasNextPage": True},
                            "nodes": nodes,
                        }
                    }
                }
            }
        }
        response = _make_graphql_response(data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_graphql("owner", "repo", 42)

        assert len(children) == 100
        captured = capsys.readouterr()
        assert "more than" in captured.err
        assert "incomplete" in captured.err

    def test_full_page_no_next_page_no_warning(self, capsys: pytest.CaptureFixture[str]) -> None:
        """100-node response with hasNextPage=False does not emit a truncation warning."""
        nodes = [{"number": i, "title": f"Issue {i}"} for i in range(1, 101)]
        data = {
            "data": {
                "repository": {
                    "issue": {
                        "subIssues": {
                            "pageInfo": {"hasNextPage": False},
                            "nodes": nodes,
                        }
                    }
                }
            }
        }
        response = _make_graphql_response(data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            children = detector._get_children_graphql("owner", "repo", 42)

        assert len(children) == 100
        captured = capsys.readouterr()
        assert "incomplete" not in captured.err


class TestGetParentEdgeCases:
    """Edge-case tests for get_parent."""

    def test_parent_number_none(self) -> None:
        """Parent data with no number returns None."""
        data = {"data": {"repository": {"issue": {"parent": {"title": "No number"}}}}}
        response = _make_graphql_response(data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            result = detector.get_parent("owner", "repo", 42)

        assert result is None

    def test_non_dict_parent_returns_none(self) -> None:
        """Non-dict parent payload is treated as no parent."""
        data = {"data": {"repository": {"issue": {"parent": "unexpected"}}}}
        response = _make_graphql_response(data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            result = detector.get_parent("owner", "repo", 42)

        assert result is None


class TestBatchCheckEdgeCases:
    """Edge-case tests for _batch_check_children_have_children."""

    def test_empty_child_numbers_returns_empty(self) -> None:
        """Empty child_numbers list returns empty dict without API call."""
        detector = GitHubHierarchyDetector("owner", "repo")
        result = detector._batch_check_children_have_children("owner", "repo", [])
        assert result == {}

    def test_null_alias_value_treated_as_no_children(self) -> None:
        """When GraphQL returns null for an aliased issue (None in Python), result is False."""
        batch_graphql_data = {
            "data": {
                "repository": {
                    "issue_10": None,
                }
            }
        }
        response = _make_graphql_response(batch_graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            result = detector._batch_check_children_have_children("owner", "repo", [10])

        assert result == {10: False}

    def test_non_dict_alias_value_treated_as_no_children(self) -> None:
        """When GraphQL returns a non-dict truthy value for an alias, result is False."""
        batch_graphql_data = {
            "data": {
                "repository": {
                    "issue_20": "unexpected-string",
                }
            }
        }
        response = _make_graphql_response(batch_graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            result = detector._batch_check_children_have_children("owner", "repo", [20])

        assert result == {20: False}

    def test_null_sub_issues_treated_as_no_children(self) -> None:
        """When subIssues is null, result defaults to False."""
        batch_graphql_data = {
            "data": {
                "repository": {
                    "issue_30": {"subIssues": None},
                }
            }
        }
        response = _make_graphql_response(batch_graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            result = detector._batch_check_children_have_children("owner", "repo", [30])

        assert result == {30: False}

    def test_non_integer_total_count_treated_as_no_children(self) -> None:
        """Non-integer subIssues.totalCount values are treated as no children."""
        batch_graphql_data = {
            "data": {
                "repository": {
                    "issue_40": {"subIssues": {"totalCount": "2"}},
                    "issue_41": {"subIssues": {"totalCount": None}},
                }
            }
        }
        response = _make_graphql_response(batch_graphql_data)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            result = detector._batch_check_children_have_children("owner", "repo", [40, 41])

        assert result == {40: False, 41: False}

    def test_large_child_numbers_split_into_chunks(self) -> None:
        """Large child lists are queried in multiple GraphQL chunks."""
        child_numbers = list(range(1, 106))
        expected = {num: num % 2 == 0 for num in child_numbers}
        detector = GitHubHierarchyDetector("owner", "repo")
        calls: list[list[int]] = []

        def mock_run_gh_graphql(query: str, _variables: dict[str, Any]) -> tuple[dict[str, Any], str]:
            chunk_numbers = [int(match) for match in re.findall(r"issue_(\d+)\s*:\s*issue", query)]
            calls.append(chunk_numbers)
            repository = {
                f"issue_{num}": {"subIssues": {"totalCount": 1 if num % 2 == 0 else 0}} for num in chunk_numbers
            }
            return ({"data": {"repository": repository}}, "")

        with patch.object(detector, "_run_gh_graphql", side_effect=mock_run_gh_graphql):
            result = detector._batch_check_children_have_children("owner", "repo", child_numbers)

        assert result == expected
        assert len(calls) == 3
        assert [len(chunk) for chunk in calls] == [50, 50, 5]


class TestGetLevelEdgeCases:
    """Edge-case tests for get_level."""

    def test_all_cross_repo_children_returns_feature(self) -> None:
        """When all children are cross-repo, classify as FEATURE."""
        children_data = [
            {
                "number": 101,
                "title": "Cross-repo",
                "repository": {"owner": {"login": "other"}, "name": "other-repo"},
            }
        ]
        children_response = _make_rest_response(children_data)
        parent_none_response = _make_graphql_response({"data": {"repository": {"issue": {"parent": None}}}})

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                return _mock_run_safe(stdout=parent_none_response)
            return _mock_run_safe(stdout=children_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42)

        assert level == HierarchyLevel.FEATURE

    def test_cross_repo_with_non_numeric_key_skipped(self) -> None:
        """Children with non-numeric keys (no '/') that fail int conversion are skipped."""
        # This tests line 592-593 where ValueError is caught
        # We mock get_children directly to return a ChildEntry with non-numeric key
        from agentic_devtools.cli.speckit.hierarchy import ChildEntry

        children_response = _make_rest_response([])
        parent_graphql = {"data": {"repository": {"issue": {"parent": None}}}}
        parent_response = _make_graphql_response(parent_graphql)

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                return _mock_run_safe(stdout=parent_response)
            return _mock_run_safe(stdout=children_response)

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                side_effect=mock_run,
            ),
            patch.object(
                GitHubHierarchyDetector,
                "get_children",
                return_value=[ChildEntry(key="abc", title="Non-numeric key", order=0)],
            ),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42)

        # All children have non-numeric keys → same_repo_numbers is empty → FEATURE
        assert level == HierarchyLevel.FEATURE

    def test_depth_1_with_parent_returns_feature(self) -> None:
        """Issue at depth 1 with a parent and no children returns FEATURE."""
        # No children
        children_response = _make_rest_response([])
        parent_graphql = {"data": {"repository": {"issue": {"parent": {"number": 10}}}}}
        parent_response = _make_graphql_response(parent_graphql)

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                return _mock_run_safe(stdout=parent_response)
            return _mock_run_safe(stdout=children_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42, _depth=1)

        assert level == HierarchyLevel.FEATURE

    def test_depth_2_with_parent_returns_task(self) -> None:
        """Issue at depth 2 with a parent and no children returns TASK."""
        children_response = _make_rest_response([])
        parent_graphql = {"data": {"repository": {"issue": {"parent": {"number": 10}}}}}
        parent_response = _make_graphql_response(parent_graphql)

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                return _mock_run_safe(stdout=parent_response)
            return _mock_run_safe(stdout=children_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42, _depth=2)

        assert level == HierarchyLevel.TASK

    def test_leaf_with_parent_and_no_grandparent_infers_feature(self) -> None:
        """Leaf nodes infer FEATURE when their parent has no parent."""
        children_response = _make_rest_response([])
        parent_response = _make_graphql_response({"data": {"repository": {"issue": {"parent": {"number": 10}}}}})
        root_response = _make_graphql_response({"data": {"repository": {"issue": {"parent": None}}}})

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                if "number=42" in cmd_str:
                    return _mock_run_safe(stdout=parent_response)
                return _mock_run_safe(stdout=root_response)
            return _mock_run_safe(stdout=children_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42)

        assert level == HierarchyLevel.FEATURE

    def test_leaf_with_grandparent_infers_task(self) -> None:
        """Leaf nodes infer TASK when their parent also has a parent."""
        children_response = _make_rest_response([])
        parent_response = _make_graphql_response({"data": {"repository": {"issue": {"parent": {"number": 10}}}}})
        grandparent_response = _make_graphql_response({"data": {"repository": {"issue": {"parent": {"number": 1}}}}})

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                if "number=42" in cmd_str:
                    return _mock_run_safe(stdout=parent_response)
                return _mock_run_safe(stdout=grandparent_response)
            return _mock_run_safe(stdout=children_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42)

        assert level == HierarchyLevel.TASK

    def test_leaf_with_great_grandparent_warns_depth_cap(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Leaf nodes deeper than supported hierarchy depth emit a cap warning."""
        with (
            patch.object(GitHubHierarchyDetector, "get_children", return_value=[]),
            patch.object(
                GitHubHierarchyDetector,
                "get_parent",
                side_effect=["10", "5", "1"],
            ),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42)

        assert level == HierarchyLevel.TASK
        assert (
            "Warning: Hierarchy depth exceeds 3 levels for owner/repo#42. Classifying as TASK (depth=3)."
        ) in capsys.readouterr().err

    def test_non_leaf_depth_cap_is_inferred_from_parent_chain(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Non-leaf nodes beyond depth cap short-circuit to TASK before child checks."""
        with (
            patch.object(
                GitHubHierarchyDetector,
                "get_children",
                return_value=[ChildEntry(key="99", title="Child", order=0)],
            ),
            patch.object(
                GitHubHierarchyDetector,
                "get_parent",
                side_effect=["10", "5", "1"],
            ) as mock_get_parent,
            patch.object(
                GitHubHierarchyDetector,
                "_batch_check_children_have_children",
            ) as mock_batch,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42)

        assert level == HierarchyLevel.TASK
        assert mock_get_parent.call_count == 3
        mock_batch.assert_not_called()
        assert (
            "Warning: Hierarchy depth exceeds 3 levels for owner/repo#42. Classifying as TASK (depth=3)."
        ) in capsys.readouterr().err

    def test_leaf_with_non_numeric_parent_defaults_to_feature(self) -> None:
        """Leaf nodes with non-numeric parent IDs conservatively classify as FEATURE."""
        with (
            patch.object(GitHubHierarchyDetector, "get_children", return_value=[]),
            patch.object(GitHubHierarchyDetector, "get_parent", return_value="abc"),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42)

        assert level == HierarchyLevel.FEATURE

    def test_leaf_with_non_numeric_grandparent_defaults_to_task(self) -> None:
        """Leaf nodes with non-numeric grandparent IDs conservatively classify as TASK."""
        with (
            patch.object(GitHubHierarchyDetector, "get_children", return_value=[]),
            patch.object(
                GitHubHierarchyDetector,
                "get_parent",
                side_effect=["10", "abc"],
            ),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42)

        assert level == HierarchyLevel.TASK

    def test_leaf_with_grandparent_and_no_great_grandparent_infers_task(self) -> None:
        """Leaf nodes infer TASK when parent has a parent but no great-grandparent exists."""
        with (
            patch.object(GitHubHierarchyDetector, "get_children", return_value=[]),
            patch.object(
                GitHubHierarchyDetector,
                "get_parent",
                side_effect=["10", "1", None],
            ),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            level = detector.get_level("owner", "repo", 42)

        assert level == HierarchyLevel.TASK

    def test_leaf_grandparent_lookup_error_has_context(self) -> None:
        """Grandparent lookup failures include depth-inference context."""
        with (
            patch.object(GitHubHierarchyDetector, "get_children", return_value=[]),
            patch.object(
                GitHubHierarchyDetector,
                "get_parent",
                side_effect=[
                    "10",
                    HierarchyValidationError("api", "upstream failure"),
                ],
            ),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(
                HierarchyValidationError,
                match="Failed to determine grandparent",
            ):
                detector.get_level("owner", "repo", 42)

    def test_leaf_great_grandparent_lookup_error_has_context(self) -> None:
        """Great-grandparent lookup failures include depth-inference context."""
        with (
            patch.object(GitHubHierarchyDetector, "get_children", return_value=[]),
            patch.object(
                GitHubHierarchyDetector,
                "get_parent",
                side_effect=[
                    "10",
                    "1",
                    HierarchyValidationError("api", "upstream failure"),
                ],
            ),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(
                HierarchyValidationError,
                match="Failed to determine great-grandparent",
            ):
                detector.get_level("owner", "repo", 42)


class TestBuildHierarchyTreeEdgeCases:
    """Edge-case tests for build_hierarchy_tree."""

    def test_depth_cap_classifies_as_task(self) -> None:
        """Issues exceeding depth cap are classified with warning."""
        issue_detail = {"number": 99, "title": "Deep Issue"}
        issue_response = _make_rest_response(issue_detail)
        children_response = _make_rest_response([])
        parent_graphql = {"data": {"repository": {"issue": {"parent": None}}}}
        parent_response = _make_graphql_response(parent_graphql)

        def mock_run(cmd, **kwargs):
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            if "graphql" in cmd_str:
                return _mock_run_safe(stdout=parent_response)
            if "sub_issues" in cmd_str:
                return _mock_run_safe(stdout=children_response)
            return _mock_run_safe(stdout=issue_response)

        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            side_effect=mock_run,
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            node = detector.build_hierarchy_tree("owner", "repo", 99, _depth=3)

        assert node.level == HierarchyLevel.TASK


class TestRunGhRestForbiddenHandling:
    """Tests for HTTP 403 handling in _run_gh_rest (NFR-003)."""

    def test_non_rate_limit_403_fails_fast_no_retry(self) -> None:
        """Non-rate-limit 403 raises immediately without retrying."""
        bad_auth_response = _mock_run_safe(
            stdout="",
            stderr="HTTP 403: Resource not accessible by integration",
            returncode=1,
        )

        sleep_calls: list[float] = []
        run_safe_calls: list[int] = []

        def counting_run_safe(cmd, **kwargs):
            run_safe_calls.append(1)
            return bad_auth_response

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                side_effect=counting_run_safe,
            ),
            patch("time.sleep", side_effect=lambda s: sleep_calls.append(s)),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="403"):
                detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

        assert len(run_safe_calls) == 1, "Should not retry on non-rate-limit 403"
        assert sleep_calls == [], "Should not sleep on non-rate-limit 403"

    def test_rate_limit_403_retries_with_backoff(self) -> None:
        """Rate-limit 403 retries and uses rate-limit helpers."""
        rate_limit_response = _mock_run_safe(
            stdout="",
            stderr="HTTP 403: API rate limit exceeded for user",
            returncode=1,
        )

        sleep_calls: list[float] = []

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                return_value=rate_limit_response,
            ),
            patch("time.sleep", side_effect=lambda s: sleep_calls.append(s)),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="rate limit|REST API failed"):
                detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

        # Should have retried (_MAX_RETRIES - 1) times with sleep
        assert len(sleep_calls) > 0, "Should sleep between retries on rate-limit 403"

    def test_rate_limit_403_calls_update_rate_limit(self) -> None:
        """Rate-limit 403 calls _update_rate_limit as part of retry flow."""
        rate_limit_response = _mock_run_safe(
            stdout="",
            stderr="HTTP 403: API rate limit exceeded for user",
            returncode=1,
        )

        update_calls: list[int] = []

        def fake_update(headers: str) -> None:
            update_calls.append(1)

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                return_value=rate_limit_response,
            ),
            patch("time.sleep"),
            patch.object(GitHubHierarchyDetector, "_update_rate_limit", side_effect=fake_update),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError):
                detector._run_gh_rest("repos/owner/repo/issues/1/sub_issues")

        assert len(update_calls) > 0, "_update_rate_limit should be called on rate-limit 403"

    def test_issue_number_in_url_is_not_treated_as_http_403(self) -> None:
        """A /issues/403 URL token does not trigger auth-failure handling."""
        url_token_response = _mock_run_safe(
            stdout="",
            stderr="gh: GET https://api.github.com/repos/owner/repo/issues/403/sub_issues: connection reset",
            returncode=1,
        )

        run_safe_calls: list[int] = []

        def counting_run_safe(cmd, **kwargs):
            run_safe_calls.append(1)
            return url_token_response

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                side_effect=counting_run_safe,
            ),
            patch("time.sleep"),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="REST API failed after"):
                detector._run_gh_rest("repos/owner/repo/issues/403/sub_issues")

        assert len(run_safe_calls) == 5, "Unstructured 403 tokens should follow normal retry handling"


class TestRunGhGraphqlForbiddenHandling:
    """Tests for HTTP 403 handling in _run_gh_graphql (NFR-003)."""

    def test_non_rate_limit_403_fails_fast_no_retry(self) -> None:
        """Non-rate-limit 403 raises immediately without retrying."""
        bad_auth_response = _mock_run_safe(
            stdout="",
            stderr="HTTP 403: Resource not accessible by integration",
            returncode=1,
        )

        sleep_calls: list[float] = []
        run_safe_calls: list[int] = []

        def counting_run_safe(cmd, **kwargs):
            run_safe_calls.append(1)
            return bad_auth_response

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                side_effect=counting_run_safe,
            ),
            patch("time.sleep", side_effect=lambda s: sleep_calls.append(s)),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="403"):
                detector._run_gh_graphql("{ viewer { login } }", {})

        assert len(run_safe_calls) == 1, "Should not retry on non-rate-limit 403"
        assert sleep_calls == [], "Should not sleep on non-rate-limit 403"

    def test_rate_limit_403_retries_with_backoff(self) -> None:
        """Rate-limit 403 retries and uses rate-limit helpers."""
        rate_limit_response = _mock_run_safe(
            stdout="",
            stderr="HTTP 403: API rate limit exceeded for user",
            returncode=1,
        )

        sleep_calls: list[float] = []

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                return_value=rate_limit_response,
            ),
            patch("time.sleep", side_effect=lambda s: sleep_calls.append(s)),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="rate limit|GraphQL API failed"):
                detector._run_gh_graphql("{ viewer { login } }", {})

        assert len(sleep_calls) > 0, "Should sleep between retries on rate-limit 403"

    def test_rate_limit_403_calls_update_rate_limit(self) -> None:
        """Rate-limit 403 calls _update_rate_limit as part of retry flow."""
        rate_limit_response = _mock_run_safe(
            stdout="",
            stderr="HTTP 403: API rate limit exceeded for user",
            returncode=1,
        )

        update_calls: list[int] = []

        def fake_update(headers: str) -> None:
            update_calls.append(1)

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                return_value=rate_limit_response,
            ),
            patch("time.sleep"),
            patch.object(GitHubHierarchyDetector, "_update_rate_limit", side_effect=fake_update),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError):
                detector._run_gh_graphql("{ viewer { login } }", {})

        assert len(update_calls) > 0, "_update_rate_limit should be called on rate-limit 403"

    def test_issue_number_in_graphql_error_text_is_not_treated_as_http_403(self) -> None:
        """A /issues/403 token in stderr does not trigger GraphQL auth-failure handling."""
        url_token_response = _mock_run_safe(
            stdout="",
            stderr="GraphQL request for https://api.github.com/repos/owner/repo/issues/403 failed",
            returncode=1,
        )

        run_safe_calls: list[int] = []

        def counting_run_safe(cmd, **kwargs):
            run_safe_calls.append(1)
            return url_token_response

        with (
            patch(
                "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
                side_effect=counting_run_safe,
            ),
            patch("time.sleep"),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            with pytest.raises(HierarchyValidationError, match="GraphQL API failed after"):
                detector._run_gh_graphql("{ viewer { login } }", {})

        assert len(run_safe_calls) == 5, "Unstructured 403 tokens should follow normal retry handling"


class TestValidateRepositoryAccess:
    """Tests for GitHubHierarchyDetector.validate_repository_access."""

    def test_succeeds_when_repo_exists(self) -> None:
        """Returns normally when the repository is accessible."""
        response = _make_rest_response({"id": 1, "full_name": "owner/repo"})
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stdout=response, returncode=0),
        ):
            detector = GitHubHierarchyDetector("owner", "repo")
            # Should not raise.
            detector.validate_repository_access()

    def test_raises_on_404(self) -> None:
        """Raises HierarchyValidationError wrapping the 404 with context."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stderr="HTTP/2 404\n\nNot Found", returncode=1),
        ):
            detector = GitHubHierarchyDetector("owner", "nonexistent")
            with pytest.raises(HierarchyValidationError, match="inaccessible or does not exist"):
                detector.validate_repository_access()

    def test_raises_on_403(self) -> None:
        """Raises HierarchyValidationError wrapping a 403 with context."""
        with patch(
            "agentic_devtools.cli.speckit.hierarchy_detector.run_safe",
            return_value=_mock_run_safe(stderr="HTTP 403 Forbidden", returncode=1),
        ):
            detector = GitHubHierarchyDetector("owner", "private-repo")
            with pytest.raises(HierarchyValidationError, match="inaccessible or does not exist"):
                detector.validate_repository_access()
