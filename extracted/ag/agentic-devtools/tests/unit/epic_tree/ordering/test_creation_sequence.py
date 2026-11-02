"""Tests for creation_sequence function."""

from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, SubtaskNode
from agentic_devtools.epic_tree.ordering import creation_sequence


class TestCreationSequence:
    """Tests for depth-first pre-order traversal with resolved sibling order."""

    def test_depth_first_pre_order(self):
        """Returns all nodes in depth-first pre-order."""
        s1 = SubtaskNode(ref="s1", title="S1", body="")
        s2 = SubtaskNode(ref="s2", title="S2", body="")
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1, s2))
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = creation_sequence(tree)
        refs = [n.ref for n in result]
        assert refs == ["e1", "f1", "s1", "s2", "f2"]

    def test_respects_explicit_order(self):
        """Features/subtasks with explicit order are visited in resolved order."""
        s1 = SubtaskNode(ref="s1", title="S1", body="", order=2)
        s2 = SubtaskNode(ref="s2", title="S2", body="", order=1)
        f1 = FeatureNode(ref="f1", title="F1", body="", order=2, subtasks=(s1, s2))
        f2 = FeatureNode(ref="f2", title="F2", body="", order=1, subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = creation_sequence(tree)
        refs = [n.ref for n in result]
        assert refs == ["e1", "f2", "f1", "s2", "s1"]

    def test_all_nodes_included(self):
        """All nodes appear exactly once."""
        s1 = SubtaskNode(ref="s1", title="S1", body="")
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1,))
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = creation_sequence(tree)
        refs = [n.ref for n in result]
        assert len(refs) == 3
        assert set(refs) == {"e1", "f1", "s1"}

    def test_empty_epic(self):
        """Epic with no features returns just the epic node."""
        epic = EpicNode(ref="e1", title="E1", body="", features=())
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = creation_sequence(tree)
        assert [n.ref for n in result] == ["e1"]

    def test_raises_type_error_for_non_feature_node(self):
        """Raises TypeError if features list contains non-FeatureNode."""
        import pytest

        from agentic_devtools.epic_tree.ordering import _visit_epic

        s1 = SubtaskNode(ref="s1", title="S1", body="")
        # Use model_construct to bypass Pydantic validation
        epic = EpicNode.model_construct(
            ref="e1",
            title="E1",
            body="",
            features=(s1,),
            labels=(),
            issueType=None,
            order=None,
            blockedBy=(),
            blocks=(),
        )
        result: list = []
        with pytest.raises(TypeError, match="Expected FeatureNode"):
            _visit_epic(epic, result)

    def test_raises_type_error_for_non_subtask_node(self):
        """Raises TypeError if subtasks list contains non-SubtaskNode."""
        import pytest

        from agentic_devtools.epic_tree.ordering import _visit_feature

        epic_node = EpicNode(ref="e1", title="E1", body="", features=())
        # Use model_construct to bypass Pydantic validation
        feature = FeatureNode.model_construct(
            ref="f1",
            title="F1",
            body="",
            subtasks=(epic_node,),
            labels=(),
            issueType=None,
            order=None,
            blockedBy=(),
            blocks=(),
        )
        result: list = []
        with pytest.raises(TypeError, match="Expected SubtaskNode"):
            _visit_feature(feature, result)

    def test_us5_full_tree_with_explicit_order(self):
        """US-5 AS-1: epic with [f1(order:2), f2(order:1)], f1->[s1, s2], f2->[s3(order:2), s4(order:1)]."""
        s1 = SubtaskNode(ref="s1", title="S1", body="")
        s2 = SubtaskNode(ref="s2", title="S2", body="")
        s3 = SubtaskNode(ref="s3", title="S3", body="", order=2)
        s4 = SubtaskNode(ref="s4", title="S4", body="", order=1)
        f1 = FeatureNode(ref="f1", title="F1", body="", order=2, subtasks=(s1, s2))
        f2 = FeatureNode(ref="f2", title="F2", body="", order=1, subtasks=(s3, s4))
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = creation_sequence(tree)
        refs = [n.ref for n in result]
        assert refs == ["e1", "f2", "s4", "s3", "f1", "s1", "s2"]

    def test_determinism_identical_output(self):
        """Same input produces identical output across multiple invocations."""
        s1 = SubtaskNode(ref="s1", title="S1", body="", order=2)
        s2 = SubtaskNode(ref="s2", title="S2", body="", order=1)
        f1 = FeatureNode(ref="f1", title="F1", body="", order=2, subtasks=(s1, s2))
        f2 = FeatureNode(ref="f2", title="F2", body="", order=1, subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        first = [n.ref for n in creation_sequence(tree)]
        for _ in range(50):
            assert [n.ref for n in creation_sequence(tree)] == first

    def test_no_features_returns_only_epic(self):
        """Epic with no features returns single-element list."""
        epic = EpicNode(ref="e1", title="E1", body="", features=())
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = creation_sequence(tree)
        assert len(result) == 1
        assert result[0].ref == "e1"

    def test_all_document_order_depth_first(self):
        """All document-order nodes produce standard depth-first pre-order."""
        s1 = SubtaskNode(ref="s1", title="S1", body="")
        s2 = SubtaskNode(ref="s2", title="S2", body="")
        s3 = SubtaskNode(ref="s3", title="S3", body="")
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1, s2))
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=(s3,))
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = creation_sequence(tree)
        refs = [n.ref for n in result]
        assert refs == ["e1", "f1", "s1", "s2", "f2", "s3"]


class TestCreationSequenceDeterministicPositions:
    """Deterministic positional ordering for pipeline tie-breaking (FR-003/014/015)."""

    def test_stable_position_index_across_calls(self):
        s1 = SubtaskNode(ref="s1", title="S1", body="")
        s2 = SubtaskNode(ref="s2", title="S2", body="")
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1, s2))
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        first = [n.ref for n in creation_sequence(tree)]
        second = [n.ref for n in creation_sequence(tree)]
        assert first == second == ["e1", "f1", "s1", "s2"]

    def test_empty_feature_and_subtask_positions(self):
        f_empty = FeatureNode(ref="f0", title="F0", body="", subtasks=())
        s1 = SubtaskNode(ref="s1", title="S1", body="")
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1,))
        epic = EpicNode(ref="e1", title="E1", body="", features=(f_empty, f1))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        refs = [n.ref for n in creation_sequence(tree)]
        assert refs == ["e1", "f0", "f1", "s1"]
        # Positions are unique and contiguous.
        assert len(refs) == len(set(refs))
