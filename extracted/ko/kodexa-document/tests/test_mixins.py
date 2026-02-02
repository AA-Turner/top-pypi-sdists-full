"""
Test mixin functionality matching legacy_python behavior.
"""

import pytest
from kodexa_document import Document


class TestMixins:
    """Test document mixin methods."""
    
    def test_initial_mixins_empty(self):
        """Test that new documents have empty mixins."""
        document = Document(inmemory=True)
        
        # Test get_mixins method
        assert document.get_mixins() == []
        
        document.close()
    
    def test_add_mixin_single(self):
        """Test adding a single mixin."""
        document = Document(inmemory=True)
        
        # Add a mixin and verify it returns self for chaining
        result = document.add_mixin("test-mixin")
        assert result is document  # Method chaining
        
        # Verify mixin was added
        assert document.get_mixins() == ["test-mixin"]
        
        document.close()
    
    def test_add_multiple_mixins(self):
        """Test adding multiple mixins."""
        document = Document(inmemory=True)
        
        # Add multiple mixins
        document.add_mixin("mixin1")
        document.add_mixin("mixin2")  
        document.add_mixin("mixin3")
        
        # Verify all mixins are present
        mixins = document.get_mixins()
        assert len(mixins) == 3
        assert "mixin1" in mixins
        assert "mixin2" in mixins
        assert "mixin3" in mixins
        
        document.close()
    
    def test_add_duplicate_mixins(self):
        """Test that duplicate mixins are ignored."""
        document = Document(inmemory=True)
        
        # Add same mixin multiple times
        document.add_mixin("duplicate")
        document.add_mixin("duplicate")
        document.add_mixin("unique")
        document.add_mixin("duplicate")
        
        # Should have only two unique mixins
        mixins = document.get_mixins()
        assert len(mixins) == 2
        assert "duplicate" in mixins
        assert "unique" in mixins
        
        document.close()
    
    def test_mixin_type_validation(self):
        """Test that mixin methods validate input types."""
        document = Document(inmemory=True)
        
        # add_mixin should only accept strings
        with pytest.raises(TypeError, match="mixin must be a string"):
            document.add_mixin(123)
        
        with pytest.raises(TypeError, match="mixin must be a string"):
            document.add_mixin(["not", "a", "string"])
        
        with pytest.raises(TypeError, match="mixin must be a string"):
            document.add_mixin(None)
        
        document.close()
    
    def test_mixins_with_special_characters(self):
        """Test mixins with special characters and unicode."""
        document = Document(inmemory=True)
        
        # Test various special characters
        special_mixins = [
            "mixin with spaces",
            "mixin-with-dashes", 
            "mixin_with_underscores",
            "mixin.with.dots",
            "mixin/with/slashes",
            "mixin:with:colons",
            "unicode: 中文 русский العربية",
            "emoji: 🚀 📄 ✨",
            "",  # empty string
            "very-long-mixin-" + "x" * 100
        ]
        
        # Add all special mixins
        for mixin in special_mixins:
            document.add_mixin(mixin)
        
        # Verify all were added
        doc_mixins = document.get_mixins()
        assert len(doc_mixins) == len(special_mixins)
        for mixin in special_mixins:
            assert mixin in doc_mixins
        
        document.close()
    
    def test_mixins_persistence_across_operations(self):
        """Test that mixins persist across other document operations."""
        document = Document(inmemory=True)
        
        # Add mixins
        document.add_mixin("persistent1")
        document.add_mixin("persistent2")
        
        # Perform other document operations
        root = document.create_node("document")
        document.content_node = root
        
        child = document.create_node("paragraph", content="Test content")
        root.add_child(child)
        
        # Set metadata
        document.set_metadata("test_key", "test_value")
        
        # Mixins should still be there
        mixins = document.get_mixins()
        assert len(mixins) == 2
        assert "persistent1" in mixins
        assert "persistent2" in mixins
        
        document.close()
    
    def test_multiple_documents_independent_mixins(self):
        """Test that different documents have independent mixins."""
        doc1 = Document(inmemory=True)
        doc2 = Document(inmemory=True)
        
        # Add different mixins to each document
        doc1.add_mixin("doc1-mixin1")
        doc1.add_mixin("doc1-mixin2")
        
        doc2.add_mixin("doc2-mixin1")
        doc2.add_mixin("doc2-mixin2")
        doc2.add_mixin("doc2-mixin3")
        
        # Verify each document has its own mixins
        assert len(doc1.get_mixins()) == 2
        assert len(doc2.get_mixins()) == 3
        
        assert "doc1-mixin1" in doc1.get_mixins()
        assert "doc1-mixin2" in doc1.get_mixins()
        assert "doc1-mixin1" not in doc2.get_mixins()
        assert "doc1-mixin2" not in doc2.get_mixins()
        
        assert "doc2-mixin1" in doc2.get_mixins()
        assert "doc2-mixin2" in doc2.get_mixins()
        assert "doc2-mixin3" in doc2.get_mixins()
        assert "doc2-mixin1" not in doc1.get_mixins()
        
        doc1.close()
        doc2.close()
    
    def test_method_chaining(self):
        """Test that add_mixin supports method chaining."""
        document = Document(inmemory=True)
        
        # Test method chaining
        result = (document
                  .add_mixin("chain1")
                  .add_mixin("chain2")
                  .add_mixin("chain3"))
        
        # Should return the same document object
        assert result is document
        
        # Verify final state
        mixins = document.get_mixins()
        assert len(mixins) == 3
        assert "chain1" in mixins
        assert "chain2" in mixins
        assert "chain3" in mixins
        
        document.close()
    
    def test_mixins_with_json_round_trip(self):
        """Test that mixins survive JSON serialization/deserialization."""
        document = Document(inmemory=True)
        
        # Add some mixins
        document.add_mixin("spatial")
        document.add_mixin("navigation")
        
        # Convert to JSON and back
        json_str = document.to_json()
        document2 = Document.from_json(json_str, inmemory=True)
        
        # Verify mixins are preserved
        mixins = document2.get_mixins()
        assert len(mixins) == 2
        assert "spatial" in mixins
        assert "navigation" in mixins
        
        document.close()
        document2.close()
    
    def test_mixins_after_document_close(self):
        """Test that accessing mixins after close raises an error."""
        document = Document(inmemory=True)
        
        # Add a mixin
        document.add_mixin("test")
        
        # Close the document
        document.close()
        
        # Accessing mixins should raise an error
        with pytest.raises(RuntimeError, match="Document has been closed"):
            document.get_mixins()
        
        with pytest.raises(RuntimeError, match="Document has been closed"):
            document.add_mixin("another")