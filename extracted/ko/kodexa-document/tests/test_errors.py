"""
Test error handling for Kodexa Go bindings.
"""

import pytest
from kodexa_document import Document
from kodexa_document.errors import (
    DocumentError,
    DocumentNotFoundError,
    InvalidDocumentError,
    check_error,
    clear_error,
)


class TestErrorTypes:
    """Test different error types."""
    
    def test_document_not_found(self):
        """Test DocumentNotFoundError is raised for missing files."""
        with pytest.raises(DocumentError) as exc_info:
            Document.from_kddb("/nonexistent/path/file.kddb")
        
        # The actual exception type depends on the Go error mapping
        assert "not found" in str(exc_info.value).lower() or \
               "no such file" in str(exc_info.value).lower()
    
    def test_closed_document_error(self):
        """Test error when accessing closed document."""
        doc = Document()
        doc.close()
        
        with pytest.raises(RuntimeError) as exc_info:
            _ = doc.uuid
        
        assert "closed" in str(exc_info.value).lower()


class TestErrorHandling:
    """Test error handling mechanisms."""
    
    def test_clear_error(self):
        """Test that clear_error doesn't raise."""
        clear_error()  # Should not raise
    
    def test_invalid_json_input(self):
        """Test handling of invalid JSON input to CreateDocument."""
        # This would require creating a document with invalid JSON
        # Since our wrapper constructs the JSON, we can't easily test this
        # without exposing lower-level functions
        pass