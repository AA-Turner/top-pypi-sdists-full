"""Test Document.to_json() method for coverage."""

import json
import pytest
from kodexa_document import Document


class TestDocumentToJSON:
    """Test Document.to_json() method."""
    
    def test_to_json_basic(self):
        """Test basic to_json functionality."""
        doc = Document()
        root = doc.create_node("document", content="test content")
        doc.content_node = root
        
        # Get JSON string
        json_str = doc.to_json()
        assert isinstance(json_str, str)
        
        # Verify it's valid JSON
        json_data = json.loads(json_str)
        assert isinstance(json_data, dict)
        
        # Should have basic document structure
        assert "uuid" in json_data
        assert "content_node" in json_data
        
        doc.close()
    
    def test_to_json_with_metadata(self):
        """Test to_json with document metadata."""
        doc = Document()
        doc.metadata = {"key": "value", "number": 123}
        root = doc.create_node("root")
        doc.content_node = root
        
        json_str = doc.to_json()
        json_data = json.loads(json_str)
        
        # Check metadata is included
        assert "metadata" in json_data
        assert json_data["metadata"]["key"] == "value"
        assert json_data["metadata"]["number"] == 123
        
        doc.close()
    
    def test_to_json_with_complex_tree(self):
        """Test to_json with complex node tree."""
        doc = Document()
        root = doc.create_node("root", content="root content")
        doc.content_node = root
        
        # Create complex tree
        child1 = doc.create_node("child1", content="child1 content", parent=root)
        child2 = doc.create_node("child2", content="child2 content", parent=root)
        grandchild = doc.create_node("grandchild", content="grandchild content", parent=child1)
        
        # Add features and tags
        child1.add_feature("type", "name", "value")
        child2.tag("important", value="test")
        
        json_str = doc.to_json()
        json_data = json.loads(json_str)
        
        # Verify structure is present
        assert json_data["content_node"]["type"] == "root"
        assert json_data["content_node"]["content"] == "root content"
        
        # Should have children
        assert "children" in json_data["content_node"]
        children = json_data["content_node"]["children"]
        assert len(children) == 2
        
        doc.close()
    
    def test_to_json_inmemory_vs_file(self):
        """Test to_json works for both inmemory and file-based documents."""
        # In-memory document
        doc_mem = Document(inmemory=True)
        root_mem = doc_mem.create_node("test", content="memory")
        doc_mem.content_node = root_mem
        json_mem = doc_mem.to_json()
        
        # File-based document
        doc_file = Document(inmemory=False)
        root_file = doc_file.create_node("test", content="file")
        doc_file.content_node = root_file
        json_file = doc_file.to_json()
        
        # Both should produce valid JSON
        data_mem = json.loads(json_mem)
        data_file = json.loads(json_file)
        
        assert data_mem["content_node"]["content"] == "memory"
        assert data_file["content_node"]["content"] == "file"
        
        doc_mem.close()
        doc_file.close()
    
    def test_to_json_closed_document_error(self):
        """Test to_json raises error on closed document."""
        doc = Document()
        doc.close()
        
        with pytest.raises((RuntimeError, Exception)):
            doc.to_json()