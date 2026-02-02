"""Tests for the inmemory parameter in Document class."""

import pytest
from kodexa_document import Document


class TestDocumentInMemory:
    """Test the inmemory parameter functionality."""
    
    def test_create_inmemory_default(self):
        """Test creating a document with inmemory=True (default)."""
        doc = Document(inmemory=True)
        assert doc.uuid is not None
        assert len(doc.uuid) > 0
        doc.close()
    
    def test_create_file_based(self):
        """Test creating a file-based document."""
        doc = Document(inmemory=False)
        assert doc.uuid is not None
        assert len(doc.uuid) > 0
        doc.close()
    
    def test_from_text_inmemory(self):
        """Test creating document from text with inmemory=True."""
        text = "This is a test document"
        doc = Document.from_text(text, inmemory=True)
        assert doc.uuid is not None
        assert len(doc.uuid) > 0
        doc.close()
    
    def test_from_text_file_based(self):
        """Test creating document from text with inmemory=False."""
        text = "This is another test document"
        doc = Document.from_text(text, inmemory=False)
        assert doc.uuid is not None
        assert len(doc.uuid) > 0
        doc.close()
    
    def test_from_text_with_separator_inmemory(self):
        """Test creating document from text with separator and inmemory=True."""
        text = "Line 1\nLine 2\nLine 3"
        doc = Document.from_text(text, separator="\n", inmemory=True)
        assert doc.uuid is not None
        assert len(doc.uuid) > 0
        doc.close()
    
    def test_create_in_memory_factory(self):
        """Test the create_in_memory factory method."""
        doc = Document.create_in_memory()
        assert doc.uuid is not None
        assert len(doc.uuid) > 0
        doc.close()
    
    def test_from_kddb_with_inmemory(self):
        """Test that from_kddb passes through inmemory parameter."""
        # This would require an actual KDDB file to test properly
        # For now, we just verify the parameter is accepted
        from kodexa_document.errors import DocumentError
        
        with pytest.raises(DocumentError) as exc_info:
            doc = Document.from_kddb("nonexistent.kddb", inmemory=True)
        
        # Verify the error message indicates it tried to open the file
        assert "document not found" in str(exc_info.value).lower()
    
    def test_multiple_inmemory_documents_independent(self):
        """Test that multiple in-memory documents are independent."""
        doc1 = Document(inmemory=True)
        doc2 = Document(inmemory=True)
        
        # They should have different UUIDs
        assert doc1.uuid != doc2.uuid
        
        doc1.close()
        doc2.close()
    
    def test_context_manager_with_inmemory(self):
        """Test using Document as context manager with inmemory parameter."""
        with Document(inmemory=True) as doc:
            assert doc.uuid is not None
            assert len(doc.uuid) > 0
        
        # Document should be closed after context
        assert doc._closed is True
    
    @pytest.mark.parametrize("inmemory", [True, False])
    def test_inmemory_parameter_variations(self, inmemory):
        """Test both inmemory values work correctly."""
        doc = Document(inmemory=inmemory)
        assert doc.uuid is not None
        assert len(doc.uuid) > 0
        doc.close()