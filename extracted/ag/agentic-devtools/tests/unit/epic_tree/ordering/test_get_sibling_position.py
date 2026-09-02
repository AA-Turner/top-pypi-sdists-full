"""Tests for get_sibling_position function."""

import pytest

from agentic_devtools.epic_tree.models import IssueNode
from agentic_devtools.epic_tree.ordering import get_sibling_position


class TestGetSiblingPosition:
    """Tests for identity-based position lookup."""

    def test_first_node_returns_one(self):
        """First node in list returns (1, N)."""
        nodes = [
            IssueNode(ref="a", title="A", body=""),
            IssueNode(ref="b", title="B", body=""),
            IssueNode(ref="c", title="C", body=""),
        ]
        assert get_sibling_position(nodes[0], nodes) == (1, 3)

    def test_middle_node_returns_correct_position(self):
        """Middle node returns correct (position, N)."""
        nodes = [
            IssueNode(ref="a", title="A", body=""),
            IssueNode(ref="b", title="B", body=""),
            IssueNode(ref="c", title="C", body=""),
            IssueNode(ref="d", title="D", body=""),
        ]
        assert get_sibling_position(nodes[1], nodes) == (2, 4)
        assert get_sibling_position(nodes[2], nodes) == (3, 4)

    def test_last_node_returns_n_n(self):
        """Last node returns (N, N)."""
        nodes = [
            IssueNode(ref="a", title="A", body=""),
            IssueNode(ref="b", title="B", body=""),
            IssueNode(ref="c", title="C", body=""),
        ]
        assert get_sibling_position(nodes[2], nodes) == (3, 3)

    def test_node_not_in_list_raises_value_error(self):
        """Node not in list raises ValueError."""
        nodes = [
            IssueNode(ref="a", title="A", body=""),
            IssueNode(ref="b", title="B", body=""),
        ]
        other = IssueNode(ref="c", title="C", body="")
        with pytest.raises(ValueError, match="not present in the sibling list"):
            get_sibling_position(other, nodes)

    def test_empty_list_raises_value_error(self):
        """Empty list raises ValueError."""
        node = IssueNode(ref="a", title="A", body="")
        with pytest.raises(ValueError, match="not present in the sibling list"):
            get_sibling_position(node, [])

    def test_identity_semantics_same_values_different_object(self):
        """Same-valued but distinct object raises ValueError (identity-based)."""
        node_a = IssueNode(ref="a", title="A", body="")
        node_a_clone = IssueNode(ref="a", title="A", body="")
        nodes = [node_a]
        with pytest.raises(ValueError, match="not present in the sibling list"):
            get_sibling_position(node_a_clone, nodes)

    def test_not_found_error_uses_ref_not_full_repr(self):
        """Error message includes node ref without leaking full node body content."""
        nodes = [IssueNode(ref="a", title="A", body="")]
        other = IssueNode(ref="x", title="X", body="secret body text")

        with pytest.raises(ValueError) as exc_info:
            get_sibling_position(other, nodes)

        message = str(exc_info.value)
        assert "Node ref 'x'" in message
        assert "secret body text" not in message

    def test_single_element_list(self):
        """Single-element list returns (1, 1)."""
        node = IssueNode(ref="x", title="X", body="")
        assert get_sibling_position(node, [node]) == (1, 1)

    def test_accepts_tuple_input(self):
        """Accepts a tuple as the resolved_siblings argument."""
        nodes = (
            IssueNode(ref="a", title="A", body=""),
            IssueNode(ref="b", title="B", body=""),
        )
        assert get_sibling_position(nodes[1], nodes) == (2, 2)
