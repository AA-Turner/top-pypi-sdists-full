"""Tests for build_dependency_graph function."""

import pytest

from agentic_devtools.epic_tree.dependencies import build_dependency_graph
from agentic_devtools.epic_tree.errors import UnresolvedRefError
from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, SubtaskNode


class TestBuildDependencyGraph:
    """Tests for dependency graph construction."""

    def test_blocks_creates_edge(self):
        """A.blocks = [B] creates edge A -> B."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        graph = build_dependency_graph(tree)
        assert "f2" in graph["f1"]

    def test_blocked_by_creates_edge(self):
        """B.blockedBy = [A] creates edge A -> B."""
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", blockedBy=("f1",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        graph = build_dependency_graph(tree)
        assert "f2" in graph["f1"]

    def test_complementary_blocks_blocked_by(self):
        """blocks and blockedBy are complementary - same edge not duplicated."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", blockedBy=("f1",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        graph = build_dependency_graph(tree)
        assert graph["f1"] == {"f2"}

    def test_cross_depth_relationships(self):
        """Dependencies can cross depth levels."""
        s1 = SubtaskNode(ref="s1", title="S1", body="", blockedBy=("f1",))
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1,))
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        graph = build_dependency_graph(tree)
        assert "s1" in graph["f1"]

    def test_unresolved_ref_raises_key_error(self):
        """Reference to non-existent ref in blocks raises KeyError."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("nonexistent",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        with pytest.raises(KeyError, match="nonexistent"):
            build_dependency_graph(tree)

    def test_unresolved_ref_in_blocked_by_raises_key_error(self):
        """Reference to non-existent ref in blockedBy raises KeyError."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blockedBy=("nonexistent",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        with pytest.raises(KeyError, match="nonexistent"):
            build_dependency_graph(tree)

    def test_no_dependencies_empty_edges(self):
        """Tree without dependencies has empty edge sets."""
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        graph = build_dependency_graph(tree)
        assert graph["e1"] == set()
        assert graph["f1"] == set()

    def test_all_nodes_in_graph(self):
        """All tree nodes appear as keys in the graph."""
        s1 = SubtaskNode(ref="s1", title="S1", body="")
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1,))
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        graph = build_dependency_graph(tree)
        assert set(graph.keys()) == {"e1", "f1", "s1"}


class TestBuildDependencyGraphUnresolvedRefError:
    """Tests for UnresolvedRefError in build_dependency_graph."""

    def test_blocks_raises_unresolved_ref_error(self):
        """blocks direction raises UnresolvedRefError with correct error_payload."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("missing",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        with pytest.raises(UnresolvedRefError) as exc_info:
            build_dependency_graph(tree)
        err = exc_info.value
        assert err.error_payload["unresolved_ref"] == "missing"
        assert err.error_payload["declaring_ref"] == "f1"
        assert err.error_payload["direction"] == "blocks"
        assert err.error_payload["scope"] == "intra_epic_v1"
        assert err.error_payload["category"] == "unresolved_reference"

    def test_blocked_by_raises_unresolved_ref_error(self):
        """blockedBy direction raises UnresolvedRefError with correct error_payload."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blockedBy=("missing",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        with pytest.raises(UnresolvedRefError) as exc_info:
            build_dependency_graph(tree)
        err = exc_info.value
        assert err.error_payload["unresolved_ref"] == "missing"
        assert err.error_payload["declaring_ref"] == "f1"
        assert err.error_payload["direction"] == "blockedBy"
        assert err.error_payload["scope"] == "intra_epic_v1"
        assert err.error_payload["category"] == "unresolved_reference"

    def test_str_contains_direction_and_refs(self):
        """str(e) contains unresolved ref, declaring ref, and direction word."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("bad-ref",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        with pytest.raises(UnresolvedRefError) as exc_info:
            build_dependency_graph(tree)
        msg = str(exc_info.value)
        assert "bad-ref" in msg
        assert "f1" in msg
        assert "blocks" in msg

    def test_backward_compat_catchable_as_key_error(self):
        """UnresolvedRefError is still catchable as KeyError."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("nope",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        with pytest.raises(KeyError):
            build_dependency_graph(tree)

    def test_duplicate_entries_no_duplicate_edges(self):
        """Duplicate entries in blocks arrays produce no duplicate edges."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2", "f2"), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        graph = build_dependency_graph(tree)
        assert graph["f1"] == {"f2"}

    def test_contradictory_declarations_produce_distinct_edges(self):
        """A blocks B AND A blockedBy B produces two distinct edges (A→B and B→A)."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2",), blockedBy=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        graph = build_dependency_graph(tree)
        assert "f2" in graph["f1"]  # A→B from blocks
        assert "f1" in graph["f2"]  # B→A from blockedBy
