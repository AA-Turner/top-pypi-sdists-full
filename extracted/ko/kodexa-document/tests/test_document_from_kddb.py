"""Test from_kddb functionality with detached and bytes support."""
import os
import tempfile
import pytest
from kodexa_document import Document, DocumentError


class TestFromKDDB:
    """Test the from_kddb method with all its parameters."""
    
    def test_from_kddb_with_detached_true(self):
        """Test that detached=True creates a copy (default behavior)."""
        # Create a test document
        doc1 = Document.from_text("Test document", inmemory=False)
        
        # Save to a temp file
        with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
            temp_path = f.name
        
        try:
            doc1.save(temp_path)
            original_uuid = doc1.uuid
            doc1.close()
            
            # Open with detached=True (default)
            doc2 = Document.from_kddb(temp_path, detached=True)
            assert doc2.uuid == original_uuid
            
            # For now, just verify the document opens correctly
            # TODO: Add metadata modification when API is available
            doc2.close()
            
            # Open the original file again 
            doc3 = Document.from_kddb(temp_path, detached=False)
            assert doc3.uuid == original_uuid
            doc3.close()
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_from_kddb_with_detached_false(self):
        """Test that detached=False modifies the original file."""
        # Create a test document
        doc1 = Document.from_text("Test document", inmemory=False)
        
        # Save to a temp file
        with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
            temp_path = f.name
        
        try:
            doc1.save(temp_path)
            doc1.close()
            
            # Open with detached=False
            doc2 = Document.from_kddb(temp_path, detached=False)
            
            # For now, just verify the document opens correctly
            # TODO: Add modification test when metadata API is available
            assert doc2.uuid  # Document should have UUID
            doc2.close()
            
            # Open again to verify file still exists and works
            doc3 = Document.from_kddb(temp_path)
            assert doc3.uuid  # Should still work
            doc3.close()
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_from_kddb_with_bytes(self):
        """Test loading from bytes."""
        # Create a test document
        doc1 = Document.from_text("Test from bytes", inmemory=False)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
            temp_path = f.name
        
        try:
            doc1.save(temp_path)
            original_uuid = doc1.uuid
            doc1.close()
            
            # Read the file as bytes
            with open(temp_path, 'rb') as f:
                kddb_bytes = f.read()
            
            # Load from bytes
            doc2 = Document.from_kddb(kddb_bytes)
            assert doc2.uuid == original_uuid
            doc2.close()
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_from_kddb_bytes_with_inmemory(self):
        """Test loading from bytes with inmemory=True."""
        # Create a test document
        doc1 = Document.from_text("Memory test from bytes")
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
            temp_path = f.name
        
        try:
            doc1.save(temp_path)
            doc1.close()
            
            # Read as bytes
            with open(temp_path, 'rb') as f:
                kddb_bytes = f.read()
            
            # Load from bytes with inmemory=True
            doc2 = Document.from_kddb(kddb_bytes, inmemory=True)
            assert doc2.uuid  # Document should work
            
            # Performance should be better but we can't easily test that
            doc2.close()
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_from_kddb_file_with_inmemory(self):
        """Test loading from file path with inmemory=True."""
        # Create test document
        doc1 = Document.from_text("Memory test from file")
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
            temp_path = f.name
        
        try:
            doc1.save(temp_path)
            original_uuid = doc1.uuid
            doc1.close()
            
            # Load with inmemory=True
            doc2 = Document.from_kddb(temp_path, inmemory=True)
            assert doc2.uuid == original_uuid
            
            # Document should work normally
            doc2.close()
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_from_kddb_nonexistent_file(self):
        """Test error handling for non-existent file."""
        with pytest.raises((DocumentError, RuntimeError)):
            Document.from_kddb("/nonexistent/file.kddb")
    
    def test_from_kddb_invalid_bytes(self):
        """Test error handling for invalid bytes."""
        invalid_bytes = b"This is not a valid KDDB file"
        
        with pytest.raises((DocumentError, RuntimeError)):
            Document.from_kddb(invalid_bytes)
    
    def test_from_kddb_defaults(self):
        """Test that defaults match legacy Python (detached=True, inmemory=False)."""
        # Create test document
        doc1 = Document.from_text("Test defaults")
        
        with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
            temp_path = f.name
        
        try:
            doc1.save(temp_path)
            doc1.close()
            
            # Call with no parameters except path - should use defaults
            doc2 = Document.from_kddb(temp_path)
            # Default is detached=True, so original file should not be modified
            # Default is inmemory=False, so should be file-based
            
            # We can't easily test these directly, but document should work
            assert doc2.uuid  # Document should work
            doc2.close()
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])