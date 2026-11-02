"""Tests for resolve_sibling_order function."""

from agentic_devtools.epic_tree.models import IssueNode
from agentic_devtools.epic_tree.ordering import resolve_sibling_order


class TestResolveSiblingOrder:
    """Tests for deterministic sibling ordering."""

    def test_explicit_order_ascending(self):
        """Nodes with explicit order are sorted ascending."""
        nodes = [
            IssueNode(ref="a", title="A", body="", order=3),
            IssueNode(ref="b", title="B", body="", order=1),
            IssueNode(ref="c", title="C", body="", order=2),
        ]
        result = resolve_sibling_order(nodes)
        assert [n.ref for n in result] == ["b", "c", "a"]

    def test_implicit_after_explicit(self):
        """Nodes without order follow those with explicit order, in document order."""
        nodes = [
            IssueNode(ref="a", title="A", body=""),
            IssueNode(ref="b", title="B", body="", order=1),
            IssueNode(ref="c", title="C", body=""),
        ]
        result = resolve_sibling_order(nodes)
        assert [n.ref for n in result] == ["b", "a", "c"]

    def test_same_explicit_order_tiebreak_by_document_order(self):
        """Same explicit order uses document order as tiebreak."""
        nodes = [
            IssueNode(ref="a", title="A", body="", order=1),
            IssueNode(ref="b", title="B", body="", order=1),
            IssueNode(ref="c", title="C", body="", order=1),
        ]
        result = resolve_sibling_order(nodes)
        assert [n.ref for n in result] == ["a", "b", "c"]

    def test_all_implicit_preserves_document_order(self):
        """When all nodes lack explicit order, document order is preserved."""
        nodes = [
            IssueNode(ref="x", title="X", body=""),
            IssueNode(ref="y", title="Y", body=""),
            IssueNode(ref="z", title="Z", body=""),
        ]
        result = resolve_sibling_order(nodes)
        assert [n.ref for n in result] == ["x", "y", "z"]

    def test_determinism_across_invocations(self):
        """Same input produces same output across 100 invocations."""
        nodes = [
            IssueNode(ref="a", title="A", body="", order=2),
            IssueNode(ref="b", title="B", body=""),
            IssueNode(ref="c", title="C", body="", order=1),
        ]
        expected = [n.ref for n in resolve_sibling_order(nodes)]
        for _ in range(100):
            result = [n.ref for n in resolve_sibling_order(nodes)]
            assert result == expected

    def test_empty_list(self):
        """Empty input returns empty output."""
        assert resolve_sibling_order([]) == []

    def test_accepts_tuple_input(self):
        """Accepts a tuple (Sequence) as input without error."""
        nodes = (
            IssueNode(ref="a", title="A", body=""),
            IssueNode(ref="b", title="B", body="", order=1),
            IssueNode(ref="c", title="C", body=""),
        )
        result = resolve_sibling_order(nodes)
        assert [n.ref for n in result] == ["b", "a", "c"]

    def test_returns_same_object_references(self):
        """Returned list contains the same object references as input."""
        nodes = [
            IssueNode(ref="a", title="A", body="", order=2),
            IssueNode(ref="b", title="B", body="", order=1),
        ]
        result = resolve_sibling_order(nodes)
        assert result[0] is nodes[1]
        assert result[1] is nodes[0]

    def test_mixed_explicit_implicit_four_nodes(self):
        """Mixed explicit/implicit: [a(1), b(none), c(2), d(none)] -> [a, c, b, d]."""
        nodes = [
            IssueNode(ref="a", title="A", body="", order=1),
            IssueNode(ref="b", title="B", body=""),
            IssueNode(ref="c", title="C", body="", order=2),
            IssueNode(ref="d", title="D", body=""),
        ]
        result = resolve_sibling_order(nodes)
        assert [n.ref for n in result] == ["a", "c", "b", "d"]

    def test_large_order_gaps(self):
        """Large order gaps sort correctly by value."""
        nodes = [
            IssueNode(ref="a", title="A", body="", order=999),
            IssueNode(ref="b", title="B", body="", order=1),
            IssueNode(ref="c", title="C", body="", order=50),
        ]
        result = resolve_sibling_order(nodes)
        assert [n.ref for n in result] == ["b", "c", "a"]

    def test_single_element(self):
        """Single-element list returns [node]."""
        node = IssueNode(ref="x", title="X", body="")
        result = resolve_sibling_order([node])
        assert result == [node]
        assert result[0] is node

    def test_four_subtasks_no_order_document_order(self):
        """Four subtasks with no order field return document order."""
        nodes = [
            IssueNode(ref="s1", title="S1", body=""),
            IssueNode(ref="s2", title="S2", body=""),
            IssueNode(ref="s3", title="S3", body=""),
            IssueNode(ref="s4", title="S4", body=""),
        ]
        result = resolve_sibling_order(nodes)
        assert [n.ref for n in result] == ["s1", "s2", "s3", "s4"]

    def test_duplicate_order_two_values(self):
        """[a(order:2), b(order:1), c(order:2)] -> [b, a, c] tiebreak by document position."""
        nodes = [
            IssueNode(ref="a", title="A", body="", order=2),
            IssueNode(ref="b", title="B", body="", order=1),
            IssueNode(ref="c", title="C", body="", order=2),
        ]
        result = resolve_sibling_order(nodes)
        assert [n.ref for n in result] == ["b", "a", "c"]
