"""
Test ContentNode spatial/migration compatibility methods:
- adopt_children()
- set_bbox_from_children()
- set_statistics()
"""

import pytest
from kodexa_document import Document


class TestAdoptChildren:
    """Test ContentNode.adopt_children() method."""

    def test_adopt_children_from_same_parent(self):
        """Test adopting children that are already under the same parent (reordering)."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        # Create children under root
        child_a = doc.create_node("word", "A")
        child_b = doc.create_node("word", "B")
        child_c = doc.create_node("word", "C")
        root.add_child(child_a)
        root.add_child(child_b)
        root.add_child(child_c)

        # Adopt in different order (should reorder)
        root.adopt_children([child_c, child_a, child_b])

        # Verify children still exist
        children = root.get_children()
        assert len(children) == 3

        doc.close()

    def test_adopt_children_replace_removes_others(self):
        """Test adopt_children with replace=True removes non-adopted children."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        # Create children
        keep1 = doc.create_node("word", "keep1")
        keep2 = doc.create_node("word", "keep2")
        remove = doc.create_node("word", "remove")
        root.add_child(keep1)
        root.add_child(keep2)
        root.add_child(remove)

        # Adopt only keep1 and keep2 with replace
        root.adopt_children([keep1, keep2], replace=True)

        children = root.get_children()
        assert len(children) == 2
        contents = [c.content for c in children]
        assert "keep1" in contents
        assert "keep2" in contents
        assert "remove" not in contents

        doc.close()

    def test_adopt_children_from_different_parent(self):
        """Test adopting children from a different parent (re-parenting)."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        # Create source node with children
        source = doc.create_node("source")
        child1 = doc.create_node("word", "hello")
        child2 = doc.create_node("word", "world")
        root.add_child(source)
        source.add_child(child1)
        source.add_child(child2)

        # Create target node
        target = doc.create_node("target")
        root.add_child(target)

        # Adopt children from source to target
        children_to_adopt = source.get_children()
        target.adopt_children(children_to_adopt)

        # Verify children moved to target
        target_children = target.get_children()
        assert len(target_children) == 2
        assert target_children[0].content == "hello"
        assert target_children[1].content == "world"

        doc.close()


class TestSetBboxFromChildren:
    """Test ContentNode.set_bbox_from_children() method."""

    def test_set_bbox_from_children_basic(self):
        """Test basic bbox calculation from children."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        parent = doc.create_node("line")
        root.add_child(parent)

        # Add children with bboxes
        child1 = doc.create_node("word", "hello")
        child1.set_bbox([10, 20, 50, 40])
        parent.add_child(child1)

        child2 = doc.create_node("word", "world")
        child2.set_bbox([60, 15, 100, 45])
        parent.add_child(child2)

        # Calculate bbox from children
        parent.set_bbox_from_children()

        # Verify bbox is union of children
        bbox = parent.get_bbox()
        assert bbox[0] == 10   # min x
        assert bbox[1] == 15   # min y
        assert bbox[2] == 100  # max x
        assert bbox[3] == 45   # max y

        doc.close()

    def test_set_bbox_from_children_no_children(self):
        """Test set_bbox_from_children with no children does nothing."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        parent = doc.create_node("line")
        parent.set_bbox([1, 2, 3, 4])
        root.add_child(parent)

        # Should not change existing bbox when no children
        parent.set_bbox_from_children()

        # Bbox should be unchanged
        bbox = parent.get_bbox()
        assert bbox == [1, 2, 3, 4]

        doc.close()

    def test_set_bbox_from_children_with_zero_coordinates(self):
        """Test set_bbox_from_children handles zero coordinates correctly."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        parent = doc.create_node("line")
        root.add_child(parent)

        # Add children with zero coordinates
        child1 = doc.create_node("word", "at origin")
        child1.set_bbox([0, 0, 50, 30])
        parent.add_child(child1)

        child2 = doc.create_node("word", "offset")
        child2.set_bbox([100, 100, 150, 130])
        parent.add_child(child2)

        parent.set_bbox_from_children()

        bbox = parent.get_bbox()
        assert bbox[0] == 0    # min x should be 0, not skipped
        assert bbox[1] == 0    # min y should be 0, not skipped
        assert bbox[2] == 150  # max x
        assert bbox[3] == 130  # max y

        doc.close()

    def test_set_bbox_from_children_some_without_bbox(self):
        """Test set_bbox_from_children ignores children without bboxes."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        parent = doc.create_node("line")
        root.add_child(parent)

        # Child with bbox
        child1 = doc.create_node("word", "has bbox")
        child1.set_bbox([10, 20, 50, 40])
        parent.add_child(child1)

        # Child without bbox
        child2 = doc.create_node("word", "no bbox")
        parent.add_child(child2)

        parent.set_bbox_from_children()

        # Should only use child1's bbox
        bbox = parent.get_bbox()
        assert bbox == [10, 20, 50, 40]

        doc.close()


class TestSetStatistics:
    """Test ContentNode.set_statistics() method."""

    def test_set_statistics_basic(self):
        """Test basic statistics setting."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        node = doc.create_node("line", "test line")
        root.add_child(node)

        # Set statistics
        stats = {"mean_width": 12.5, "char_count": 100}
        node.set_statistics(stats)

        # Verify statistics stored as feature
        # Note: get_feature_value returns the value(s) - may be wrapped in list
        stored = node.get_feature_value("spatial", "statistics")

        # Handle both unwrapped (dict) and wrapped (list with dict) cases
        if isinstance(stored, list):
            assert len(stored) >= 1
            assert stored[0] == stats
        else:
            assert stored == stats

        doc.close()

    def test_set_statistics_persists(self):
        """Test that statistics persist through serialization."""
        # Use Document.from_text which is known to persist correctly
        doc = Document.from_text("test content")

        stats = {"updated_mean_width": 15.0}
        doc.content_node.set_statistics(stats)

        # Serialize and deserialize
        kddb_bytes = doc.to_kddb()
        doc.close()

        doc2 = Document.from_kddb(kddb_bytes)

        stored = doc2.content_node.get_feature_value("spatial", "statistics")

        # Handle both unwrapped and wrapped cases
        if isinstance(stored, list):
            assert stats in stored
        else:
            assert stored == stats

        doc2.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
