"""Tests for round-trip fidelity of load/save hierarchy operations."""

from datetime import UTC, datetime

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyLevel,
    HierarchyNode,
    load_hierarchy,
    save_hierarchy,
)


class TestRoundTrip:
    """Tests for round-trip fidelity."""

    def test_save_then_load_equality(self, tmp_path):
        """Test that save + load produces equal node."""
        ts = datetime(2024, 6, 15, 10, 0, 0, tzinfo=UTC)
        original = HierarchyNode(
            title="Feature",
            level=HierarchyLevel.FEATURE,
            parent="42",
            children=[
                ChildEntry(key="100", title="First", order=1),
                ChildEntry(key="101", title="Second", order=2),
            ],
            processed_at=ts,
        )
        path = tmp_path / "hierarchy.yml"
        save_hierarchy(original, path)
        loaded = load_hierarchy(path)

        assert loaded.title == original.title
        assert loaded.level == original.level
        assert loaded.parent == original.parent
        assert loaded.processed_at == original.processed_at
        assert len(loaded.children) == len(original.children)
        for orig, load in zip(original.children, loaded.children):
            assert orig.key == load.key
            assert orig.title == load.title
            assert orig.order == load.order

    def test_byte_identical_resave(self, tmp_path):
        """Test that save → load → save produces identical bytes."""
        node = HierarchyNode(
            title="Epic",
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[ChildEntry(key="1", title="Child", order=0)],
            processed_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC),
        )
        path = tmp_path / "hierarchy.yml"
        save_hierarchy(node, path)
        content1 = path.read_bytes()

        loaded = load_hierarchy(path)
        save_hierarchy(loaded, path)
        content2 = path.read_bytes()

        assert content1 == content2

    def test_ten_cycle_stability(self, tmp_path):
        """Test that 10 save/load cycles produce stable output."""
        node = HierarchyNode(
            title="Task",
            level=HierarchyLevel.TASK,
            parent="5",
            children=[ChildEntry(key=str(i), title=f"Child {i}", order=i) for i in range(10)],
            processed_at=datetime(2024, 12, 31, 23, 59, 59, tzinfo=UTC),
        )
        path = tmp_path / "hierarchy.yml"
        save_hierarchy(node, path)
        reference = path.read_bytes()

        for _ in range(10):
            loaded = load_hierarchy(path)
            save_hierarchy(loaded, path)

        assert path.read_bytes() == reference

    def test_ordering_preserved_25_children(self, tmp_path):
        """Test that ordering is preserved with 25 children."""
        children = [ChildEntry(key=str(i), title=f"Item {i}", order=25 - i) for i in range(25)]
        node = HierarchyNode(
            title="Big Feature",
            level=HierarchyLevel.FEATURE,
            parent="1",
            children=children,
        )
        path = tmp_path / "hierarchy.yml"
        save_hierarchy(node, path)
        loaded = load_hierarchy(path)

        assert [c.key for c in loaded.children] == [str(i) for i in range(25)]

    def test_duplicate_order_values_accepted(self, tmp_path):
        """Test that duplicate order values are accepted."""
        children = [
            ChildEntry(key="1", title="A", order=1),
            ChildEntry(key="2", title="B", order=1),
            ChildEntry(key="3", title="C", order=1),
        ]
        node = HierarchyNode(title="X", level=HierarchyLevel.EPIC, children=children)
        path = tmp_path / "hierarchy.yml"
        save_hierarchy(node, path)
        loaded = load_hierarchy(path)

        assert [c.key for c in loaded.children] == ["1", "2", "3"]

    def test_empty_children_round_trip(self, tmp_path):
        """Test round-trip with empty children."""
        node = HierarchyNode(
            title="Leaf Task",
            level=HierarchyLevel.TASK,
            parent="99",
            children=[],
            processed_at=None,
        )
        path = tmp_path / "hierarchy.yml"
        save_hierarchy(node, path)
        loaded = load_hierarchy(path)

        assert loaded.children == []
        assert loaded.parent == "99"
        assert loaded.processed_at is None

    def test_naive_processed_at_is_stable_after_resave(self, tmp_path):
        """Test that naive processed_at input is canonicalized on first save."""
        node = HierarchyNode(
            title="Task",
            level=HierarchyLevel.TASK,
            parent="9",
            children=[],
            processed_at=datetime(2024, 1, 1, 0, 0, 0),
        )
        path = tmp_path / "hierarchy.yml"
        save_hierarchy(node, path)
        content1 = path.read_bytes()

        loaded = load_hierarchy(path)
        save_hierarchy(loaded, path)
        content2 = path.read_bytes()

        assert content1 == content2
