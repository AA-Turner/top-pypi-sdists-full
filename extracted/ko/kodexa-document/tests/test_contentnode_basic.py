"""
Basic tests for ContentNode functionality.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from kodexa_document import Document, ContentNode, DocumentError


class TestContentNodeBasic:
    """Test basic ContentNode operations."""
    
    def test_create_node_through_document(self):
        """Test creating a node through document."""
        doc = Document(inmemory=True)
        
        # Create a node
        node = doc.create_node("paragraph", "Hello World")
        assert node is not None
        assert node.node_type == "paragraph"
        assert node.content == "Hello World"
        assert node.id > 0  # Should have a database ID
        assert node.uuid != ""  # Should have a UUID
        assert node.virtual == False
        assert node.index is None  # No index specified
        
        doc.close()
    
    def test_create_node_with_index(self):
        """Test creating a node with an index."""
        doc = Document(inmemory=True)
        
        # Create nodes with indices
        node1 = doc.create_node("paragraph", "First", index=0)
        node2 = doc.create_node("paragraph", "Second", index=1)
        
        assert node1.index == 0
        assert node2.index == 1
        
        doc.close()
    
    def test_get_set_content_node(self):
        """Test getting and setting document's root node."""
        doc = Document(inmemory=True)

        # New documents have a default root node with type "root"
        root = doc.content_node
        assert root is not None
        assert root.node_type == "root"

        # Update the root node's content
        root.content = "Root Content"

        # Get it back
        retrieved = doc.content_node
        assert retrieved is not None
        assert retrieved.node_type == "root"
        assert retrieved.content == "Root Content"
        assert retrieved.id == root.id

        # Clear the content node
        doc.content_node = None
        assert doc.content_node is None

        doc.close()
    
    def test_node_properties(self):
        """Test node property access."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Test Content")
        
        # Test read-only properties
        assert node.node_type == "paragraph"
        assert node.id > 0
        assert node.uuid != ""
        assert node.virtual == False
        
        # Test read/write properties
        assert node.content == "Test Content"
        node.content = "Modified Content"
        assert node.content == "Modified Content"
        
        assert node.index is None
        node.index = 5
        assert node.index == 5
        
        # Clear index
        node.index = None
        assert node.index is None
        
        doc.close()
    
    def test_node_aliases(self):
        """Test Document aliases for content_node."""
        doc = Document(inmemory=True)
        
        root = doc.create_node("document", "Root")
        
        # Test set_root alias
        doc.set_root(root)
        
        # Test get_root alias
        retrieved = doc.get_root()
        assert retrieved is not None
        assert retrieved.id == root.id
        
        doc.close()
    
    def test_node_context_manager(self):
        """Test ContentNode context manager."""
        doc = Document(inmemory=True)
        
        with doc.create_node("paragraph", "Test") as node:
            assert node.content == "Test"
            # Node should be valid inside context
            assert node.node_type == "paragraph"
        
        # After context, node should be closed
        with pytest.raises(ValueError, match="ContentNode has been closed"):
            _ = node.content
        
        doc.close()
    
    def test_node_repr_str(self):
        """Test ContentNode string representations."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Short content")
        
        # Test __repr__
        repr_str = repr(node)
        assert "ContentNode" in repr_str
        assert "paragraph" in repr_str
        assert "Short content" in repr_str
        
        # Test __str__
        str_repr = str(node)
        assert "paragraph" in str_repr
        assert "Short content" in str_repr
        
        # Test with long content
        long_node = doc.create_node("paragraph", "A" * 100)
        repr_long = repr(long_node)
        assert "..." in repr_long  # Should be truncated
        
        # Test closed node
        node.close()
        assert repr(node) == "ContentNode(closed)"
        assert str(node) == "[Closed ContentNode]"
        
        doc.close()
    
    def test_memory_cleanup(self):
        """Test that nodes are properly cleaned up."""
        doc = Document(inmemory=True)
        
        # Create multiple nodes
        nodes = []
        for i in range(10):
            node = doc.create_node("paragraph", f"Content {i}")
            nodes.append(node)
        
        # Clear references
        nodes.clear()
        
        # Nodes should be garbage collected (finalizers will free handles)
        # This is automatic in Python
        
        doc.close()
    
    def test_document_persistence_with_nodes(self):
        """Test saving and loading document with nodes."""
        import tempfile
        import os

        # Create document and use auto-created root node
        doc1 = Document(inmemory=True)
        root = doc1.content_node
        root.content = "Root"

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".kddb", delete=False) as f:
            temp_path = f.name
        
        try:
            doc1.save(temp_path)
            doc1.close()
            
            # Load it back
            doc2 = Document.from_kddb(temp_path, inmemory=True)
            
            # Check content node was persisted
            loaded_root = doc2.content_node
            assert loaded_root is not None
            assert loaded_root.node_type == "root"
            assert loaded_root.content == "Root"
            
            doc2.close()
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_contentnode_error_paths(self):
        """Test error handling in ContentNode."""
        doc = Document()
        node = doc.create_node("test")

        # Test that node operations properly detect closed document
        doc.close()

        # All database operations should now return "document is closed" error
        with pytest.raises(DocumentError) as exc_info:
            node.get_children()
        assert "document is closed" in str(exc_info.value).lower()

        with pytest.raises(DocumentError) as exc_info:
            node.add_feature("test", "name", "value")
        assert "document is closed" in str(exc_info.value).lower()

        with pytest.raises(DocumentError) as exc_info:
            node.tag("test_tag")
        assert "document is closed" in str(exc_info.value).lower()

    def test_contentnode_properties_on_closed(self):
        """Test ContentNode property access on closed document."""
        doc = Document()
        node = doc.create_node("test")
        doc.close()

        # Property access should still work (these are cached values)
        # But database operations should fail with proper error
        assert node.content == ""  # This works (cached)
        assert node.node_type == "test"  # This works (cached)

        # Database operations should fail with "document is closed"
        with pytest.raises(DocumentError) as exc_info:
            node.get_tags()
        assert "document is closed" in str(exc_info.value).lower()

        with pytest.raises(DocumentError) as exc_info:
            node.get_features()
        assert "document is closed" in str(exc_info.value).lower()

    def test_contentnode_content_parts_errors(self):
        """Test content parts error cases."""
        doc = Document()
        node = doc.create_node("test")

        # Test set_content_parts with invalid type - raises ValueError
        with pytest.raises(ValueError):
            node.set_content_parts("not a list")

        # Note: [1, 2, 3] is now valid - integers represent child node references
        # (matching kodexa/kodexa behavior for rollup operations)

        doc.close()

    def test_contentnode_bbox_errors(self):
        """Test bbox error cases."""
        doc = Document()
        node = doc.create_node("test")

        # Test set_bbox with invalid types
        with pytest.raises(TypeError):
            node.set_bbox("not", "valid", "bbox", "values")

        # Test set_bbox with wrong number of args
        with pytest.raises(TypeError):
            node.set_bbox(1.0, 2.0)  # Too few args

        doc.close()


if __name__ == "__main__":
    # Run tests
    test = TestContentNodeBasic()
    
    print("Running ContentNode basic tests...")
    
    try:
        test.test_create_node_through_document()
        print("✓ test_create_node_through_document")
    except Exception as e:
        print(f"✗ test_create_node_through_document: {e}")
    
    try:
        test.test_create_node_with_index()
        print("✓ test_create_node_with_index")
    except Exception as e:
        print(f"✗ test_create_node_with_index: {e}")
    
    try:
        test.test_get_set_content_node()
        print("✓ test_get_set_content_node")
    except Exception as e:
        print(f"✗ test_get_set_content_node: {e}")
    
    try:
        test.test_node_properties()
        print("✓ test_node_properties")
    except Exception as e:
        print(f"✗ test_node_properties: {e}")
    
    try:
        test.test_node_aliases()
        print("✓ test_node_aliases")
    except Exception as e:
        print(f"✗ test_node_aliases: {e}")
    
    try:
        test.test_node_context_manager()
        print("✓ test_node_context_manager")
    except Exception as e:
        print(f"✗ test_node_context_manager: {e}")
    
    try:
        test.test_node_repr_str()
        print("✓ test_node_repr_str")
    except Exception as e:
        print(f"✗ test_node_repr_str: {e}")
    
    try:
        test.test_memory_cleanup()
        print("✓ test_memory_cleanup")
    except Exception as e:
        print(f"✗ test_memory_cleanup: {e}")
    
    try:
        test.test_document_persistence_with_nodes()
        print("✓ test_document_persistence_with_nodes")
    except Exception as e:
        print(f"✗ test_document_persistence_with_nodes: {e}")
    
    print("\nAll basic ContentNode tests completed!")