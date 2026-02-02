"""
Tests for Document.from_json functionality.
"""

import pytest
import json
from kodexa_document import Document


class TestDocumentFromJSON:
    """Test Document.from_json functionality."""
    
    def test_from_json_basic(self):
        """Test basic from_json functionality."""
        # Create original document
        doc1 = Document(inmemory=True)
        root = doc1.create_node("document", "Test content")
        doc1.content_node = root
        doc1.set_metadata("author", "Test Author")
        
        # Export to JSON
        json_str = doc1.to_json()
        
        # Create new document from JSON
        doc2 = Document.from_json(json_str, inmemory=True)
        
        # Verify properties
        assert doc2.uuid == doc1.uuid
        assert doc2.version == doc1.version
        assert doc2.metadata == doc1.metadata
        
        # Verify content node
        assert doc2.content_node is not None
        assert doc2.content_node.node_type == "document"
        assert doc2.content_node.content == "Test content"
        
        doc1.close()
        doc2.close()
    
    def test_from_json_roundtrip(self):
        """Test JSON roundtrip (export -> import -> export)."""
        # Create complex document
        doc1 = Document(inmemory=True)
        root = doc1.create_node("document", "Root content")
        child1 = doc1.create_node("paragraph", "Paragraph 1")
        child2 = doc1.create_node("paragraph", "Paragraph 2")
        
        # Build hierarchy
        root.add_child(child1)
        root.add_child(child2)
        doc1.content_node = root
        
        # Set metadata
        doc1.set_metadata("title", "Test Document")
        doc1.set_metadata("tags", ["test", "roundtrip"])
        doc1.set_metadata("number", 42)
        doc1.set_metadata("boolean", True)
        
        # First JSON export
        json_str1 = doc1.to_json()
        
        # Import from JSON
        doc2 = Document.from_json(json_str1, inmemory=True)
        
        # Second JSON export
        json_str2 = doc2.to_json()
        
        # Parse both JSON strings and compare (order may differ)
        data1 = json.loads(json_str1)
        data2 = json.loads(json_str2)
        
        # Key properties should match
        assert data1["uuid"] == data2["uuid"]
        assert data1["version"] == data2["version"]
        assert data1["metadata"] == data2["metadata"]
        
        # Content structure should match (if contentNode exists)
        if "contentNode" in data1 and "contentNode" in data2:
            assert data1["contentNode"]["nodeType"] == data2["contentNode"]["nodeType"]
            assert data1["contentNode"]["content"] == data2["contentNode"]["content"]
            if "children" in data1["contentNode"] and "children" in data2["contentNode"]:
                assert len(data1["contentNode"]["children"]) == len(data2["contentNode"]["children"])
        
        doc1.close()
        doc2.close()
    
    def test_from_json_inmemory_parameter(self):
        """Test inmemory parameter."""
        # Create test document
        doc1 = Document(inmemory=True)
        root = doc1.create_node("document", "Test")
        doc1.content_node = root
        json_str = doc1.to_json()
        
        # Test inmemory=True
        doc2 = Document.from_json(json_str, inmemory=True)
        assert doc2 is not None
        assert doc2.content_node.content == "Test"
        
        # Test inmemory=False (default)
        doc3 = Document.from_json(json_str, inmemory=False)
        assert doc3 is not None
        assert doc3.content_node.content == "Test"
        
        # Test default (should be False)
        doc4 = Document.from_json(json_str)
        assert doc4 is not None
        assert doc4.content_node.content == "Test"
        
        doc1.close()
        doc2.close()
        doc3.close()
        doc4.close()
    
    def test_from_json_empty_document(self):
        """Test from_json with minimal document."""
        # Create minimal document
        doc1 = Document(inmemory=True)
        json_str = doc1.to_json()
        
        # Import from JSON
        doc2 = Document.from_json(json_str, inmemory=True)
        
        # Should have basic properties
        assert doc2.uuid == doc1.uuid
        assert doc2.version == doc1.version
        # Metadata contains uuid/version but no user metadata
        user_metadata = {k: v for k, v in doc2.metadata.items() if k not in ('uuid', 'version')}
        assert user_metadata == {}
        
        doc1.close()
        doc2.close()
    
    def test_from_json_with_metadata_only(self):
        """Test from_json with document containing only metadata."""
        # Create document with only metadata
        doc1 = Document(inmemory=True)
        doc1.set_metadata("key1", "value1")
        doc1.set_metadata("key2", 123)
        doc1.set_metadata("key3", ["a", "b", "c"])
        
        json_str = doc1.to_json()
        
        # Import from JSON
        doc2 = Document.from_json(json_str, inmemory=True)
        
        # Verify metadata was preserved
        assert doc2.metadata["key1"] == "value1"
        assert doc2.metadata["key2"] == 123
        assert doc2.metadata["key3"] == ["a", "b", "c"]
        
        doc1.close()
        doc2.close()
    
    def test_from_json_invalid_input(self):
        """Test from_json with invalid inputs."""
        # Test with None
        with pytest.raises(TypeError):
            Document.from_json(None)
        
        # Test with non-string
        with pytest.raises(TypeError):
            Document.from_json(123)
        
        # Test with invalid JSON
        with pytest.raises(Exception):  # Could be RuntimeError or DocumentError
            Document.from_json("invalid json {")
        
        # Test with empty string
        with pytest.raises(Exception):  # Could be RuntimeError or DocumentError
            Document.from_json("")
    
    def test_from_json_complex_content_tree(self):
        """Test from_json with complex content tree."""
        # Create complex document structure
        doc1 = Document(inmemory=True)
        
        # Create hierarchy: document -> section -> paragraph -> word
        root = doc1.create_node("document", "Document")
        section = doc1.create_node("section", "Section 1")
        para1 = doc1.create_node("paragraph", "First paragraph")
        para2 = doc1.create_node("paragraph", "Second paragraph")
        word1 = doc1.create_node("word", "First")
        word2 = doc1.create_node("word", "paragraph")
        
        # Build tree
        root.add_child(section)
        section.add_child(para1)
        section.add_child(para2)
        para1.add_child(word1)
        para1.add_child(word2)
        doc1.content_node = root
        
        # Add tags (features are not serialized to JSON currently, so we test tags)
        word1.tag("important", confidence=0.95, value="key_word")
        word2.tag("secondary", confidence=0.8, value="other_word")
        
        # Export and import
        json_str = doc1.to_json()
        doc2 = Document.from_json(json_str, inmemory=True)
        
        # Verify structure
        assert doc2.content_node.node_type == "document"
        assert doc2.content_node.child_count == 1
        
        section2 = doc2.content_node.get_child(0)
        assert section2.node_type == "section"
        assert section2.child_count == 2
        
        para1_2 = section2.get_child(0)
        assert para1_2.node_type == "paragraph"
        assert para1_2.content == "First paragraph"
        assert para1_2.child_count == 2
        
        # Check tags (repository initialization should be working now)
        word1_2 = para1_2.get_child(0)
        assert word1_2.content == "First"
        tags = word1_2.get_tags()
        assert len(tags) > 0
        assert "important" in tags  # tags is now a list of strings
        
        word2_2 = para1_2.get_child(1)
        assert word2_2.content == "paragraph"
        tags2 = word2_2.get_tags()
        assert len(tags2) > 0  
        assert "secondary" in tags2  # tags is now a list of strings
        
        doc1.close()
        doc2.close()
    
    def test_from_json_preserves_uuids(self):
        """Test that from_json preserves document UUID."""
        # Create document with known UUID
        doc1 = Document(inmemory=True)
        original_uuid = doc1.uuid
        
        # Export and import
        json_str = doc1.to_json()
        doc2 = Document.from_json(json_str, inmemory=True)
        
        # UUID should be preserved
        assert doc2.uuid == original_uuid
        
        doc1.close()
        doc2.close()
    
    def test_from_json_context_manager(self):
        """Test from_json with context manager."""
        # Create test document
        with Document(inmemory=True) as doc1:
            root = doc1.create_node("document", "Test content")
            doc1.content_node = root
            doc1.set_metadata("test", "value")
            json_str = doc1.to_json()
        
        # Import with context manager
        with Document.from_json(json_str, inmemory=True) as doc2:
            assert doc2.content_node.content == "Test content"
            assert doc2.metadata["test"] == "value"
    
    def test_from_json_kwargs_compatibility(self):
        """Test that from_json accepts additional kwargs for compatibility."""
        # Create test document
        doc1 = Document(inmemory=True)
        root = doc1.create_node("document", "Test")
        doc1.content_node = root
        json_str = doc1.to_json()
        
        # Should accept additional kwargs without error
        doc2 = Document.from_json(json_str, inmemory=True, unused_param="ignored")
        assert doc2.content_node.content == "Test"
        
        doc1.close()
        doc2.close()