"""
Test script for ContentNode lifecycle operations.
"""

import uuid
import pytest
from kodexa_document import Document, ContentNode


def test_get_node_by_uuid():
    """Test get_node_by_uuid functionality."""
    # Create a document with some content
    doc = Document.from_text("This is a test document with multiple paragraphs.\n\nSecond paragraph here.", inmemory=True)
    
    try:
        # Get the content node and navigate to find nodes with UUIDs
        root = doc.content_node
        assert root is not None, "No content node found"
        
        # Get some child nodes to test with
        children = root.get_children()
        if not children:
            # Create some test nodes
            child1 = doc.create_node("paragraph", "Test paragraph 1")
            child2 = doc.create_node("paragraph", "Test paragraph 2")
            root.add_child(child1)
            root.add_child(child2)
            children = [child1, child2]
        
        # Test getting node by UUID
        first_child = children[0]
        node_uuid = first_child.uuid
        assert node_uuid is not None, "Node UUID should not be None"
        
        # Test get_node_by_uuid
        found_node = doc.get_node_by_uuid(node_uuid)
        assert found_node is not None, "get_node_by_uuid returned None"
        
        # Verify it's the same node
        assert found_node.uuid == node_uuid, "Found node has different UUID"
        
    finally:
        doc.close()


def test_node_deletion():
    """Test node deletion functionality using remove_child."""
    doc = Document.create_in_memory()
    
    try:
        # Create a node structure
        root = doc.create_node("document", "Root document")
        child1 = doc.create_node("paragraph", "First paragraph")
        child2 = doc.create_node("paragraph", "Second paragraph")
        
        root.add_child(child1)
        root.add_child(child2)
        doc.content_node = root
        
        # Verify initial state
        children = root.get_children()
        assert len(children) == 2, f"Expected 2 children, got {len(children)}"
        
        # Delete one child using remove_child
        child1_uuid = child1.uuid
        root.remove_child(child1)
        
        # Verify node was deleted
        remaining_children = root.get_children()
        assert len(remaining_children) == 1, f"Expected 1 child after deletion, got {len(remaining_children)}"
        assert remaining_children[0].uuid == child2.uuid, "Wrong child remained"
        
        # Note: Document.delete_node() method is not implemented in lib/python
        # This test uses parent.remove_child() as the available deletion method
        
    finally:
        doc.close()


def test_node_hierarchy_operations():
    """Test basic node hierarchy operations."""
    doc = Document.create_in_memory()
    
    try:
        # Create a complex hierarchy
        root = doc.create_node("document", "Root")
        section1 = doc.create_node("section", "Section 1")
        section2 = doc.create_node("section", "Section 2")
        para1 = doc.create_node("paragraph", "Paragraph 1")
        para2 = doc.create_node("paragraph", "Paragraph 2")
        
        # Build tree structure
        root.add_child(section1)
        root.add_child(section2)
        section1.add_child(para1)
        section2.add_child(para2)
        doc.content_node = root
        
        # Test basic parent-child relationships
        para1_parent = para1.get_parent()
        para2_parent = para2.get_parent()
        assert para1_parent is not None, "para1 should have a parent"
        assert para2_parent is not None, "para2 should have a parent"
        assert para1_parent.uuid == section1.uuid, "para1 parent should be section1"
        assert para2_parent.uuid == section2.uuid, "para2 parent should be section2"
        
        # Test child count
        assert root.child_count == 2, f"Root should have 2 children, got {root.child_count}"
        assert section1.child_count == 1, f"Section1 should have 1 child, got {section1.child_count}"
        
    finally:
        doc.close()


def test_node_content_updates():
    """Test updating node content."""
    doc = Document.create_in_memory()
    
    try:
        # Create a node
        node = doc.create_node("paragraph", "Original content")
        
        # Test content update
        new_content = "Updated content"
        node.content = new_content
        assert node.content == new_content, f"Content should be '{new_content}', got '{node.content}'"
        
        # Test node type update
        new_type = "heading"
        node.node_type = new_type
        assert node.node_type == new_type, f"Node type should be '{new_type}', got '{node.node_type}'"
        
    finally:
        doc.close()


def test_node_tree_navigation():
    """Test basic tree navigation using available methods."""
    doc = Document.create_in_memory()
    
    try:
        # Create a tree structure
        root = doc.create_node("document", "Root")
        child1 = doc.create_node("section", "Child 1")
        child2 = doc.create_node("section", "Child 2")
        child3 = doc.create_node("section", "Child 3")
        grandchild = doc.create_node("paragraph", "Grandchild")
        
        # Build structure
        root.add_child(child1)
        root.add_child(child2)
        root.add_child(child3)
        child2.add_child(grandchild)
        doc.content_node = root
        
        # Test basic child access
        children = root.get_children()
        assert len(children) == 3, f"Root should have 3 children, got {len(children)}"
        
        # Test indexed child access
        first_child = root.get_child(0)
        last_child = root.get_child(2)
        assert first_child is not None, "Root should have first child"
        assert last_child is not None, "Root should have last child"
        assert first_child.uuid == child1.uuid, "First child should be child1"
        assert last_child.uuid == child3.uuid, "Last child should be child3"
        
        # Test parent relationship
        grandchild_parent = grandchild.get_parent()
        assert grandchild_parent is not None, "grandchild should have parent"
        assert grandchild_parent.uuid == child2.uuid, "grandchild parent should be child2"
        
    finally:
        doc.close()


def test_node_uuid_operations():
    """Test UUID-based node operations."""
    doc = Document.create_in_memory()
    
    try:
        # Create nodes with UUIDs and properly attach them to document
        root = doc.create_node("document", "Root")
        doc.content_node = root  # Set root first to ensure it's in the document
        
        child = doc.create_node("paragraph", "Child")
        root.add_child(child)
        
        # Test UUID properties
        root_uuid = root.uuid
        child_uuid = child.uuid
        
        assert root_uuid is not None, "Root UUID should not be None"
        assert child_uuid is not None, "Child UUID should not be None"
        assert root_uuid != child_uuid, "UUIDs should be unique"
        
        # Test finding nodes by UUID
        found_root = doc.get_node_by_uuid(root_uuid)
        found_child = doc.get_node_by_uuid(child_uuid)
        
        assert found_root is not None, "Should find root by UUID"
        assert found_child is not None, "Should find child by UUID"
        assert found_root.uuid == root_uuid, "Found root should have correct UUID"
        assert found_child.uuid == child_uuid, "Found child should have correct UUID"
        
        # Test with non-existent UUID
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        not_found = doc.get_node_by_uuid(fake_uuid)
        assert not_found is None, "Should return None for non-existent UUID"
        
    finally:
        doc.close()


def test_node_property_setters():
    """Test node property setters (node_type, virtual)."""
    doc = Document.create_in_memory()
    
    try:
        # Create a test node
        node = doc.create_node("original_type", "Test content")
        doc.content_node = node
        
        # Test original values
        assert node.node_type == "original_type", "Original node type should be 'original_type'"
        original_virtual = node.virtual
        assert isinstance(original_virtual, bool), "Virtual should be a boolean"
        
        # Test node_type property setter
        node.node_type = "property_type"
        assert node.node_type == "property_type", "Property setter should update node type"
        
        # Test virtual property setter
        node.virtual = True
        assert node.virtual is True, "Property setter should set virtual to True"
        
        node.virtual = False
        assert node.virtual is False, "Property setter should set virtual to False"
        
    finally:
        doc.close()




def test_content_property_updates():
    """Test content property updates beyond basic node_type."""
    doc = Document.create_in_memory()
    
    try:
        # Create a node
        node = doc.create_node("paragraph", "Original content")
        doc.content_node = node
        
        # Test content property (already covered in other tests, but be explicit)
        new_content = "Updated content via property"
        node.content = new_content
        assert node.content == new_content, f"Content property should be '{new_content}', got '{node.content}'"
        
        # Test setting content to empty string
        node.content = ""
        assert node.content == "", "Content should be empty string"
        
        # Test setting content to None (if supported)
        try:
            node.content = None
            # If this doesn't raise an exception, verify the behavior
            assert node.content is None or node.content == "", "Content set to None should be None or empty"
        except (TypeError, ValueError):
            # This is acceptable - None might not be a valid content value
            pass
        
    finally:
        doc.close()