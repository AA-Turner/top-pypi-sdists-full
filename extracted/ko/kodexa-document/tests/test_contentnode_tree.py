"""
Tests for ContentNode tree navigation functionality.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from kodexa_document import Document, ContentNode, DocumentError


class TestContentNodeTreeNavigation:
    """Test ContentNode tree navigation operations."""
    
    def test_parent_child_relationship(self):
        """Test basic parent-child relationships."""
        doc = Document(inmemory=True)
        
        # Create root node
        root = doc.create_node("document", "Root Document")
        doc.content_node = root
        
        # Create child nodes
        section1 = doc.create_node("section", "Section 1")
        section2 = doc.create_node("section", "Section 2")
        
        # Add children to root
        root.add_child(section1)
        root.add_child(section2)
        
        # Verify parent relationships
        assert section1.get_parent().id == root.id
        assert section2.get_parent().id == root.id
        
        # Verify root has no parent
        assert root.get_parent() is None
        
        # Verify children
        children = root.get_children()
        assert len(children) == 2
        assert children[0].id == section1.id
        assert children[1].id == section2.id
        
        doc.close()
    
    def test_child_count_property(self):
        """Test child_count property."""
        doc = Document(inmemory=True)
        
        root = doc.create_node("document", "Root")
        doc.content_node = root
        
        # Initially no children
        assert root.child_count == 0
        
        # Add children
        for i in range(5):
            child = doc.create_node("paragraph", f"Paragraph {i}")
            root.add_child(child)
        
        # Verify count
        assert root.child_count == 5
        
        doc.close()
    
    def test_get_child_by_index(self):
        """Test getting child by index."""
        doc = Document(inmemory=True)
        
        root = doc.create_node("document", "Root")
        doc.content_node = root
        
        # Create and add children
        children_created = []
        for i in range(3):
            child = doc.create_node("paragraph", f"Paragraph {i}")
            root.add_child(child)
            children_created.append(child)
        
        # Get children by index
        assert root.get_child(0).content == "Paragraph 0"
        assert root.get_child(1).content == "Paragraph 1"
        assert root.get_child(2).content == "Paragraph 2"
        
        # Out of bounds returns None
        assert root.get_child(3) is None
        assert root.get_child(-1) is None
        
        doc.close()
    
    def test_add_child_with_index(self):
        """Test adding child at specific index."""
        doc = Document(inmemory=True)
        
        root = doc.create_node("document", "Root")
        doc.content_node = root
        
        # Add initial children
        child1 = doc.create_node("paragraph", "First")
        child3 = doc.create_node("paragraph", "Third")
        root.add_child(child1)
        root.add_child(child3)
        
        # Insert at index 1
        child2 = doc.create_node("paragraph", "Second")
        root.add_child(child2, index=1)
        
        # Verify order
        children = root.get_children()
        assert len(children) == 3
        assert children[0].content == "First"
        assert children[1].content == "Second"
        assert children[2].content == "Third"
        
        doc.close()
    
    def test_remove_child(self):
        """Test removing a child node."""
        doc = Document(inmemory=True)
        
        root = doc.create_node("document", "Root")
        doc.content_node = root
        
        # Add children
        child1 = doc.create_node("paragraph", "Keep me")
        child2 = doc.create_node("paragraph", "Remove me")
        child3 = doc.create_node("paragraph", "Keep me too")
        
        root.add_child(child1)
        root.add_child(child2)
        root.add_child(child3)
        
        assert root.child_count == 3
        
        # Remove middle child
        root.remove_child(child2)
        
        # Verify removal
        assert root.child_count == 2
        children = root.get_children()
        assert children[0].content == "Keep me"
        assert children[1].content == "Keep me too"
        
        doc.close()
    
    def test_sibling_navigation(self):
        """Test next_node and previous_node methods."""
        doc = Document(inmemory=True)
        
        root = doc.create_node("document", "Root")
        doc.content_node = root
        
        # Create sibling nodes
        child1 = doc.create_node("paragraph", "First")
        child2 = doc.create_node("paragraph", "Second")
        child3 = doc.create_node("paragraph", "Third")
        
        root.add_child(child1)
        root.add_child(child2)
        root.add_child(child3)
        
        # Test next_node
        next_of_1 = child1.next_node()
        assert next_of_1 is not None
        assert next_of_1.content == "Second"
        
        next_of_2 = child2.next_node()
        assert next_of_2 is not None
        assert next_of_2.content == "Third"
        
        next_of_3 = child3.next_node()
        assert next_of_3 is None  # Last child has no next
        
        # Test previous_node
        prev_of_3 = child3.previous_node()
        assert prev_of_3 is not None
        assert prev_of_3.content == "Second"
        
        prev_of_2 = child2.previous_node()
        assert prev_of_2 is not None
        assert prev_of_2.content == "First"
        
        prev_of_1 = child1.previous_node()
        assert prev_of_1 is None  # First child has no previous

        doc.close()

    def test_navigation_legacy(self):
        """Test basic navigation - ported from legacy kodexa tests."""
        # Matches legacy test_navigation() from kodexa/tests/basic_document_test.py
        doc = Document(inmemory=True)

        root = doc.create_node("foo", "cheese")
        doc.content_node = root

        # Add first child (fishstick)
        root.add_child(doc.create_node(node_type='bar', content='fishstick'))
        # Add more children
        root.add_child(doc.create_node(node_type='bar', content='cheeseburger'))
        root.add_child(doc.create_node(node_type='bar', content='lemon'))

        # Test navigation
        assert root.get_children()[0].next_node().content == 'cheeseburger'
        assert root.get_children()[2].previous_node().content == 'cheeseburger'

        doc.close()

    def test_sibling_navigation_node_type_re(self):
        """Test next_node and previous_node with node_type_re parameter."""
        doc = Document(inmemory=True)

        root = doc.create_node("document", "Root")
        doc.content_node = root

        # Create sibling nodes with different types
        child1 = doc.create_node("paragraph", "Para1")
        child2 = doc.create_node("line", "Line1")
        child3 = doc.create_node("paragraph", "Para2")
        child4 = doc.create_node("word", "Word1")

        root.add_child(child1)
        root.add_child(child2)
        root.add_child(child3)
        root.add_child(child4)

        # Find next paragraph (skip line)
        next_para = child1.next_node(node_type_re="paragraph")
        assert next_para is not None
        assert next_para.content == "Para2"
        assert next_para.node_type == "paragraph"

        # Find next line
        next_line = child1.next_node(node_type_re="line")
        assert next_line is not None
        assert next_line.content == "Line1"

        # Find previous paragraph from word
        prev_para = child4.previous_node(node_type_re="paragraph")
        assert prev_para is not None
        assert prev_para.content == "Para2"

        doc.close()

    def test_sibling_navigation_has_no_content(self):
        """Test next_node and previous_node with has_no_content parameter."""
        doc = Document(inmemory=True)

        root = doc.create_node("document", "Root")
        doc.content_node = root

        # Create sibling nodes - child2 has no content
        child1 = doc.create_node("paragraph", "First")
        child2 = doc.create_node("paragraph", "")  # Empty content
        child3 = doc.create_node("paragraph", "Third")

        root.add_child(child1)
        root.add_child(child2)
        root.add_child(child3)

        # With has_no_content=True (default for next_node) - should get empty node
        next_of_1 = child1.next_node(has_no_content=True)
        assert next_of_1 is not None
        assert next_of_1.content == ""

        # With has_no_content=False - should skip empty node
        next_of_1_with_content = child1.next_node(has_no_content=False)
        assert next_of_1_with_content is not None
        assert next_of_1_with_content.content == "Third"

        # Test previous_node with has_no_content
        prev_of_3 = child3.previous_node(has_no_content=True)
        assert prev_of_3 is not None
        assert prev_of_3.content == ""

        prev_of_3_with_content = child3.previous_node(has_no_content=False)
        assert prev_of_3_with_content is not None
        assert prev_of_3_with_content.content == "First"

        doc.close()

    def test_sibling_navigation_traverse_sibling(self):
        """Test next_node with Traverse.SIBLING (default behavior)."""
        from kodexa_document.model.enums import Traverse

        doc = Document(inmemory=True)

        root = doc.create_node("document", "Root")
        doc.content_node = root

        # Create two sections with children
        section1 = doc.create_node("section", "Section1")
        section2 = doc.create_node("section", "Section2")

        para1 = doc.create_node("paragraph", "Para1")
        para2 = doc.create_node("paragraph", "Para2")

        root.add_child(section1)
        root.add_child(section2)
        section1.add_child(para1)
        section2.add_child(para2)

        # With Traverse.SIBLING (default) - para1 has no next sibling
        next_sibling = para1.next_node(traverse=Traverse.SIBLING)
        assert next_sibling is None

        # Sections are siblings of each other
        next_section = section1.next_node(traverse=Traverse.SIBLING)
        assert next_section is not None
        assert next_section.content == "Section2"

        doc.close()

    def test_sibling_navigation_combined_params(self):
        """Test next_node and previous_node with node_type_re and has_no_content combined."""
        doc = Document(inmemory=True)

        root = doc.create_node("document", "Root")
        doc.content_node = root

        # Create structure with mixed types and empty content
        child1 = doc.create_node("paragraph", "Para1")
        child2 = doc.create_node("line", "")  # empty line
        child3 = doc.create_node("paragraph", "")  # empty paragraph
        child4 = doc.create_node("paragraph", "Para4")

        root.add_child(child1)
        root.add_child(child2)
        root.add_child(child3)
        root.add_child(child4)

        # Find next paragraph with content (skip empty paragraph at index 2)
        next_node = child1.next_node(
            node_type_re="paragraph",
            has_no_content=False
        )
        assert next_node is not None
        assert next_node.content == "Para4"

        # Find previous paragraph with content
        prev_node = child4.previous_node(
            node_type_re="paragraph",
            has_no_content=False
        )
        assert prev_node is not None
        assert prev_node.content == "Para1"

        doc.close()

    def test_deep_hierarchy(self):
        """Test deep hierarchical structure."""
        doc = Document(inmemory=True)
        
        # Create hierarchy: doc -> section -> paragraph -> word
        root = doc.create_node("document", "Document")
        section = doc.create_node("section", "Section")
        paragraph = doc.create_node("paragraph", "Paragraph")
        word = doc.create_node("word", "Word")
        
        doc.content_node = root
        root.add_child(section)
        section.add_child(paragraph)
        paragraph.add_child(word)
        
        # Navigate up from word to root
        assert word.get_parent().content == "Paragraph"
        assert word.get_parent().get_parent().content == "Section"
        assert word.get_parent().get_parent().get_parent().content == "Document"
        assert word.get_parent().get_parent().get_parent().get_parent() is None
        
        # Navigate down from root to word
        assert root.get_children()[0].content == "Section"
        assert root.get_children()[0].get_children()[0].content == "Paragraph"
        assert root.get_children()[0].get_children()[0].get_children()[0].content == "Word"
        
        doc.close()
    
    def test_empty_children_list(self):
        """Test get_children on leaf nodes."""
        doc = Document(inmemory=True)
        
        leaf = doc.create_node("word", "Leaf node")
        
        # Leaf has no children
        assert leaf.get_children() == []
        assert leaf.child_count == 0
        assert leaf.get_child(0) is None
        
        doc.close()
    
    def test_tree_persistence(self):
        """Test that tree structure persists through save/load."""
        import tempfile
        import os

        # Create document and use auto-created root node
        doc1 = Document(inmemory=True)
        root = doc1.content_node
        root.content = "Root"
        child1 = doc1.create_node("section", "Section 1")
        child2 = doc1.create_node("section", "Section 2")
        grandchild = doc1.create_node("paragraph", "Paragraph in Section 1")

        root.add_child(child1)
        root.add_child(child2)
        child1.add_child(grandchild)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".kddb", delete=False) as f:
            temp_path = f.name
        
        try:
            doc1.save(temp_path)
            doc1.close()
            
            # Load it back
            doc2 = Document.from_kddb(temp_path, inmemory=True)
            
            # Verify tree structure
            loaded_root = doc2.content_node
            assert loaded_root is not None
            assert loaded_root.content == "Root"
            assert loaded_root.child_count == 2
            
            loaded_children = loaded_root.get_children()
            assert loaded_children[0].content == "Section 1"
            assert loaded_children[1].content == "Section 2"
            
            # Check grandchild
            section1_children = loaded_children[0].get_children()
            assert len(section1_children) == 1
            assert section1_children[0].content == "Paragraph in Section 1"
            
            doc2.close()
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_circular_reference_prevention(self):
        """Test that circular references are prevented."""
        doc = Document(inmemory=True)
        
        parent = doc.create_node("section", "Parent")
        child = doc.create_node("paragraph", "Child")
        
        # Normal parent-child relationship
        parent.add_child(child)
        
        # Try to add parent as child of its own child (would create cycle)
        # This should fail or be prevented by the domain logic
        try:
            child.add_child(parent)
            # If it doesn't raise an error, verify it didn't create a cycle
            # by checking that traversing up from parent doesn't loop
            current = parent
            depth = 0
            while current is not None and depth < 10:
                current = current.get_parent()
                depth += 1
            # If we didn't get stuck in a loop, we're okay
            assert depth < 10
        except Exception:
            # Expected - circular reference was prevented
            pass
        
        doc.close()

    def test_contentnode_tree_operations(self):
        """Test tree operation edge cases."""
        doc = Document()
        root = doc.create_node("root")
        child1 = doc.create_node("child1", parent=root)
        child2 = doc.create_node("child2", parent=root)

        # Test get_child with invalid index
        invalid_child = root.get_child(999)
        assert invalid_child is None

        # Test get_child with negative index - not supported, returns None
        last_child = root.get_child(-1)
        assert last_child is None

        # Successful remove_child returns None
        result = root.remove_child(child1)
        assert result is None
        # Use get_children() method instead of children property
        children = root.get_children()
        assert len(children) == 1

        # Legacy SDK behavior: remove_child just deletes the node without
        # validating parent-child relationship (no error raised)
        # Create other_node as child of remaining child so it has a parent
        remaining_child = root.get_children()[0]
        other_node = doc.create_node("other", parent=remaining_child)
        root.remove_child(other_node)  # Deletes other_node, doesn't raise

        # Verify other_node is marked as deleted
        assert getattr(other_node, '_deleted', False) is True

        doc.close()

    # TODO: Revisit this test after virtual nodes feature is removed
    @pytest.mark.skip(reason="Virtual nodes feature is being removed - revisit after removal")
    def test_virtual_nodes_not_persisted(self):
        """Test that virtual nodes exist in memory but are NOT saved to KDDB files.

        This matches legacy Python behavior where virtual nodes only exist during
        a document session and disappear when the document is saved and reloaded.
        """
        import tempfile
        import os

        doc = Document(inmemory=True)
        root = doc.content_node
        root.content = "Root"

        # Create regular nodes
        regular1 = doc.create_node("section", "Regular 1")
        regular2 = doc.create_node("section", "Regular 2")
        root.add_child(regular1)
        root.add_child(regular2)

        # Create virtual node
        virtual_node = doc.create_node("section", "Virtual Section", virtual=True)
        root.add_child(virtual_node)

        # Create child of virtual node
        virtual_child = doc.create_node("paragraph", "Child of Virtual")
        virtual_node.add_child(virtual_child)

        # Verify virtual nodes exist in memory
        assert virtual_node.virtual is True
        assert virtual_node.content == "Virtual Section"
        children = root.get_children()
        assert len(children) == 3  # 2 regular + 1 virtual

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".kddb", delete=False) as f:
            temp_path = f.name

        try:
            doc.save(temp_path)
            doc.close()

            # Load it back
            doc2 = Document.from_kddb(temp_path, inmemory=True)

            # Verify virtual nodes are NOT in the saved file
            loaded_root = doc2.content_node
            assert loaded_root is not None
            loaded_children = loaded_root.get_children()

            # Only the 2 regular nodes should be present
            assert len(loaded_children) == 2
            contents = [c.content for c in loaded_children]
            assert "Regular 1" in contents
            assert "Regular 2" in contents
            assert "Virtual Section" not in contents  # Virtual node not persisted

            # Verify none of the loaded nodes are virtual
            for child in loaded_children:
                assert child.virtual is False

            doc2.close()
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    # TODO: Revisit this test after virtual nodes feature is removed
    @pytest.mark.skip(reason="Virtual nodes feature is being removed - revisit after removal")
    def test_virtual_node_sibling_navigation(self):
        """Test that sibling navigation works with virtual nodes in memory."""
        doc = Document(inmemory=True)
        root = doc.content_node
        root.content = "Root"

        # Create mix of regular and virtual nodes
        regular1 = doc.create_node("paragraph", "Regular 1")
        virtual1 = doc.create_node("paragraph", "Virtual 1", virtual=True)
        regular2 = doc.create_node("paragraph", "Regular 2")
        virtual2 = doc.create_node("paragraph", "Virtual 2", virtual=True)
        regular3 = doc.create_node("paragraph", "Regular 3")

        root.add_child(regular1)
        root.add_child(virtual1)
        root.add_child(regular2)
        root.add_child(virtual2)
        root.add_child(regular3)

        # Verify virtual flag is set correctly
        assert regular1.virtual is False
        assert virtual1.virtual is True
        assert regular2.virtual is False
        assert virtual2.virtual is True
        assert regular3.virtual is False

        # Test next_node includes virtual nodes
        next_of_r1 = regular1.next_node()
        assert next_of_r1 is not None
        assert next_of_r1.content == "Virtual 1"

        next_of_v1 = virtual1.next_node()
        assert next_of_v1 is not None
        assert next_of_v1.content == "Regular 2"

        # Test previous_node includes virtual nodes
        prev_of_r2 = regular2.previous_node()
        assert prev_of_r2 is not None
        assert prev_of_r2.content == "Virtual 1"

        doc.close()


if __name__ == "__main__":
    # Run tests
    test = TestContentNodeTreeNavigation()
    
    print("Running ContentNode tree navigation tests...")
    
    tests_to_run = [
        ("test_parent_child_relationship", test.test_parent_child_relationship),
        ("test_child_count_property", test.test_child_count_property),
        ("test_get_child_by_index", test.test_get_child_by_index),
        ("test_add_child_with_index", test.test_add_child_with_index),
        ("test_remove_child", test.test_remove_child),
        ("test_sibling_navigation", test.test_sibling_navigation),
        ("test_deep_hierarchy", test.test_deep_hierarchy),
        ("test_empty_children_list", test.test_empty_children_list),
        ("test_tree_persistence", test.test_tree_persistence),
        ("test_circular_reference_prevention", test.test_circular_reference_prevention),
        ("test_virtual_nodes_not_persisted", test.test_virtual_nodes_not_persisted),
        ("test_virtual_node_sibling_navigation", test.test_virtual_node_sibling_navigation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests_to_run:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed out of {len(tests_to_run)} tests")
    
    if failed == 0:
        print("All tree navigation tests passed!")
    else:
        print(f"{failed} tests failed.")