"""
Test label functionality matching legacy_python behavior.
"""

import pytest
from kodexa_document import Document


class TestLabels:
    """Test document label methods."""
    
    def test_initial_labels_empty(self):
        """Test that new documents have empty labels."""
        document = Document(inmemory=True)
        
        # Test both property and method access
        assert document.labels == []
        assert document.get_labels() == []
        
        document.close()
    
    def test_add_label_single(self):
        """Test adding a single label."""
        document = Document(inmemory=True)
        
        # Add a label and verify it returns self for chaining
        result = document.add_label("test-label")
        assert result is document  # Method chaining
        
        # Verify label was added
        assert document.labels == ["test-label"]
        assert document.get_labels() == ["test-label"]
        
        document.close()
    
    def test_add_multiple_labels(self):
        """Test adding multiple labels."""
        document = Document(inmemory=True)
        
        # Add multiple labels
        document.add_label("label1")
        document.add_label("label2")  
        document.add_label("label3")
        
        # Verify all labels are present
        labels = document.labels
        assert len(labels) == 3
        assert "label1" in labels
        assert "label2" in labels
        assert "label3" in labels
        
        document.close()
    
    def test_add_duplicate_labels(self):
        """Test that duplicate labels are ignored."""
        document = Document(inmemory=True)
        
        # Add same label multiple times
        document.add_label("duplicate")
        document.add_label("duplicate")
        document.add_label("unique")
        document.add_label("duplicate")
        
        # Should have only two unique labels
        labels = document.labels
        assert len(labels) == 2
        assert "duplicate" in labels
        assert "unique" in labels
        
        document.close()
    
    def test_remove_label(self):
        """Test removing labels."""
        document = Document(inmemory=True)
        
        # Add some labels
        document.add_label("label1")
        document.add_label("label2")
        document.add_label("label3")
        
        # Remove one label and verify it returns self for chaining
        result = document.remove_label("label2")
        assert result is document  # Method chaining
        
        # Verify label was removed
        labels = document.labels
        assert len(labels) == 2
        assert "label1" in labels
        assert "label3" in labels
        assert "label2" not in labels
        
        document.close()
    
    def test_remove_nonexistent_label(self):
        """Test removing a label that doesn't exist raises ValueError."""
        document = Document(inmemory=True)
        
        # Add some labels
        document.add_label("existing")
        
        # Try to remove non-existent label - should raise ValueError
        with pytest.raises(ValueError, match="label not found: nonexistent"):
            document.remove_label("nonexistent")
        
        # Original labels should be unchanged
        assert document.labels == ["existing"]
        
        document.close()
    
    def test_remove_from_empty_document(self):
        """Test removing from empty document raises ValueError."""
        document = Document(inmemory=True)
        
        with pytest.raises(ValueError, match="label not found: anything"):
            document.remove_label("anything")
        
        document.close()
    
    def test_label_type_validation(self):
        """Test that label methods validate input types."""
        document = Document(inmemory=True)
        
        # add_label should only accept strings
        with pytest.raises(TypeError, match="label must be a string"):
            document.add_label(123)
        
        with pytest.raises(TypeError, match="label must be a string"):
            document.add_label(["not", "a", "string"])
        
        with pytest.raises(TypeError, match="label must be a string"):
            document.add_label(None)
        
        # remove_label should only accept strings
        with pytest.raises(TypeError, match="label must be a string"):
            document.remove_label(123)
        
        document.close()
    
    def test_labels_with_special_characters(self):
        """Test labels with special characters and unicode."""
        document = Document(inmemory=True)
        
        # Test various special characters
        special_labels = [
            "label with spaces",
            "label-with-dashes", 
            "label_with_underscores",
            "label.with.dots",
            "label/with/slashes",
            "label:with:colons",
            "unicode: 中文 русский العربية",
            "emoji: 🚀 📄 ✨",
            "",  # empty string
            "very-long-label-" + "x" * 100
        ]
        
        # Add all special labels
        for label in special_labels:
            document.add_label(label)
        
        # Verify all were added
        doc_labels = document.labels
        assert len(doc_labels) == len(special_labels)
        for label in special_labels:
            assert label in doc_labels
        
        document.close()
    
    def test_labels_persistence_across_operations(self):
        """Test that labels persist across other document operations."""
        document = Document(inmemory=True)
        
        # Add labels
        document.add_label("persistent1")
        document.add_label("persistent2")
        
        # Perform other document operations
        root = document.create_node("document")
        document.content_node = root
        
        child = document.create_node("paragraph", content="Test content")
        root.add_child(child)
        
        # Set metadata
        document.set_metadata("test_key", "test_value")
        
        # Labels should still be there
        labels = document.labels
        assert len(labels) == 2
        assert "persistent1" in labels
        assert "persistent2" in labels
        
        document.close()
    
    def test_multiple_documents_independent_labels(self):
        """Test that different documents have independent labels."""
        doc1 = Document(inmemory=True)
        doc2 = Document(inmemory=True)
        
        # Add different labels to each document
        doc1.add_label("doc1-label1")
        doc1.add_label("doc1-label2")
        
        doc2.add_label("doc2-label1")
        doc2.add_label("doc2-label2")
        doc2.add_label("doc2-label3")
        
        # Verify each document has its own labels
        assert len(doc1.labels) == 2
        assert len(doc2.labels) == 3
        
        assert "doc1-label1" in doc1.labels
        assert "doc1-label2" in doc1.labels
        assert "doc1-label1" not in doc2.labels
        assert "doc1-label2" not in doc2.labels
        
        assert "doc2-label1" in doc2.labels
        assert "doc2-label2" in doc2.labels
        assert "doc2-label3" in doc2.labels
        assert "doc2-label1" not in doc1.labels
        
        # Modify one document - other should be unaffected
        doc1.remove_label("doc1-label1")
        assert len(doc1.labels) == 1
        assert len(doc2.labels) == 3  # unchanged
        
        doc1.close()
        doc2.close()
    
    def test_method_chaining(self):
        """Test that add_label and remove_label support method chaining."""
        document = Document(inmemory=True)
        
        # Test method chaining
        result = (document
                  .add_label("chain1")
                  .add_label("chain2")
                  .add_label("chain3")
                  .remove_label("chain2"))
        
        # Should return the same document object
        assert result is document
        
        # Verify final state
        labels = document.labels
        assert len(labels) == 2
        assert "chain1" in labels
        assert "chain3" in labels
        assert "chain2" not in labels
        
        document.close()
    
    def test_property_vs_method_consistency(self):
        """Test that labels property and get_labels() method return the same result."""
        document = Document(inmemory=True)
        
        # Empty document
        assert document.labels == document.get_labels()
        
        # Add some labels
        document.add_label("prop1")
        document.add_label("prop2")
        
        # Both should return the same list
        prop_labels = document.labels
        method_labels = document.get_labels()
        
        assert prop_labels == method_labels
        assert len(prop_labels) == 2
        assert "prop1" in prop_labels
        assert "prop2" in prop_labels
        
        # Remove a label
        document.remove_label("prop1")
        
        # Should still be consistent
        assert document.labels == document.get_labels()
        assert len(document.labels) == 1
        assert "prop2" in document.labels
        
        document.close()