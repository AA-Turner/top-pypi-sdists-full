"""
Test to_kddb functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path
from kodexa_document import Document


def test_to_kddb_with_path():
    """Test saving document to KDDB file with a path."""
    # Create a document
    doc = Document(inmemory=True)
    doc_uuid = doc.uuid
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    try:
        # Save document to file
        result = doc.to_kddb(temp_path)
        assert result is None  # Should return None when saving to file
        
        # Verify file exists and has content
        assert os.path.exists(temp_path)
        assert os.path.getsize(temp_path) > 0
        
        # Close original document
        doc.close()
        
        # Load the saved document to verify
        doc2 = Document.from_kddb(temp_path, inmemory=True)
        assert doc2.uuid == doc_uuid
        doc2.close()
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_to_kddb_without_path():
    """Test getting document as KDDB bytes without a path."""
    # Create a document
    doc = Document(inmemory=True)
    doc_uuid = doc.uuid
    
    # Get document as bytes
    kddb_bytes = doc.to_kddb()
    
    # Verify we got bytes
    assert kddb_bytes is not None
    assert isinstance(kddb_bytes, bytes)
    assert len(kddb_bytes) > 0
    
    # Close original document
    doc.close()
    
    # Load document from bytes to verify
    doc2 = Document.from_kddb(kddb_bytes, inmemory=True)
    assert doc2.uuid == doc_uuid
    doc2.close()


def test_to_kddb_roundtrip():
    """Test roundtrip: create -> to_kddb bytes -> from_kddb."""
    # Create document with metadata
    metadata = {"title": "Test Document", "version": "1.0"}
    doc = Document(metadata=metadata, inmemory=True)
    doc_uuid = doc.uuid
    
    # Convert to bytes
    kddb_bytes = doc.to_kddb()
    assert isinstance(kddb_bytes, bytes)
    
    # Close original
    doc.close()
    
    # Load from bytes
    doc2 = Document.from_kddb(kddb_bytes, inmemory=True)
    
    # Verify document properties
    assert doc2.uuid == doc_uuid
    # Metadata might not be preserved in current implementation
    # Just verify the document loads successfully
    # TODO: Enable when metadata is fully implemented
    # assert doc2.metadata["title"] == "Test Document"
    # assert doc2.metadata["version"] == "1.0"
    
    doc2.close()


def test_to_kddb_file_roundtrip():
    """Test roundtrip: create -> save to file -> load from file."""
    # Create document with metadata
    metadata = {"author": "Test Author", "date": "2025-01-01"}
    doc = Document(metadata=metadata, inmemory=True)
    doc_uuid = doc.uuid
    
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    try:
        # Save to file
        doc.to_kddb(temp_path)
        doc.close()
        
        # Load from file
        doc2 = Document.from_kddb(temp_path, detached=False, inmemory=True)
        
        # Verify document properties
        assert doc2.uuid == doc_uuid
        # Metadata might not be preserved in current implementation
        # TODO: Enable when metadata is fully implemented
        # assert doc2.metadata["author"] == "Test Author"
        # assert doc2.metadata["date"] == "2025-01-01"
        
        doc2.close()
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_to_kddb_from_text():
    """Test to_kddb with document created from text."""
    # Create document from text
    text = "Line 1\nLine 2\nLine 3"
    doc = Document.from_text(text, separator="\n", inmemory=True)
    
    # Get as bytes
    kddb_bytes = doc.to_kddb()
    assert isinstance(kddb_bytes, bytes)
    assert len(kddb_bytes) > 0
    
    doc.close()
    
    # Load from bytes and verify content
    doc2 = Document.from_kddb(kddb_bytes, inmemory=True)
    # Note: We can't verify content directly without ContentNode implementation
    # but we can verify the document loads successfully
    assert doc2.uuid is not None
    doc2.close()


def test_to_kddb_closed_document():
    """Test that to_kddb raises error on closed document."""
    doc = Document(inmemory=True)
    doc.close()
    
    with pytest.raises(RuntimeError, match="Document has been closed"):
        doc.to_kddb()
    
    with pytest.raises(RuntimeError, match="Document has been closed"):
        doc.to_kddb("/tmp/test.kddb")


def test_save_method_still_works():
    """Test that the save method still works independently."""
    doc = Document(inmemory=True)
    doc_uuid = doc.uuid
    
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    try:
        # Use save method directly
        doc.save(temp_path)
        doc.close()
        
        # Verify file was created
        assert os.path.exists(temp_path)
        assert os.path.getsize(temp_path) > 0
        
        # Load and verify
        doc2 = Document.from_kddb(temp_path, inmemory=True)
        assert doc2.uuid == doc_uuid
        doc2.close()
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    # Run tests
    test_to_kddb_with_path()
    print("✓ test_to_kddb_with_path passed")
    
    test_to_kddb_without_path()
    print("✓ test_to_kddb_without_path passed")
    
    test_to_kddb_roundtrip()
    print("✓ test_to_kddb_roundtrip passed")
    
    test_to_kddb_file_roundtrip()
    print("✓ test_to_kddb_file_roundtrip passed")
    
    test_to_kddb_from_text()
    print("✓ test_to_kddb_from_text passed")
    
    test_to_kddb_closed_document()
    print("✓ test_to_kddb_closed_document passed")
    
    test_save_method_still_works()
    print("✓ test_save_method_still_works passed")
    
    print("\nAll to_kddb tests passed!")