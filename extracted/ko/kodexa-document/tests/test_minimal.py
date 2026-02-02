"""
Minimal test of the Python wrapper with Go bindings.
"""

import tempfile
import pytest
from kodexa_document import Document


def test_create_in_memory_document():
    """Test creating an in-memory document."""
    doc = Document.create_in_memory()
    
    assert doc.uuid is not None
    assert len(doc.uuid) > 0
    assert doc.version is not None
    
    doc.close()


def test_document_json_serialization():
    """Test JSON serialization of documents."""
    doc = Document.create_in_memory()
    
    json_str = doc.to_json()
    assert isinstance(json_str, str)
    assert len(json_str) > 0
    assert '"uuid"' in json_str
    
    doc.close()


def test_document_from_text():
    """Test creating document from text."""
    text_doc = Document.from_text("Line 1\nLine 2\nLine 3", separator="\n")
    
    assert text_doc.uuid is not None
    assert len(text_doc.uuid) > 0
    
    text_doc.close()


def test_document_save_and_load():
    """Test saving and loading documents."""
    # Create document from text
    text_doc = Document.from_text("Line 1\nLine 2\nLine 3", separator="\n")
    original_uuid = text_doc.uuid
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".kddb", delete=False) as f:
        temp_path = f.name
    
    try:
        text_doc.save(temp_path)
        text_doc.close()
        
        # Load it back
        loaded_doc = Document.from_kddb(temp_path)
        
        assert loaded_doc.uuid == original_uuid
        loaded_doc.close()
        
    finally:
        import os
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_context_manager():
    """Test document context manager."""
    with Document.create_in_memory() as doc:
        assert doc.uuid is not None
        uuid = doc.uuid
        assert len(uuid) > 0
    
    # Document should be closed after context


def test_invalid_file_path():
    """Test error handling with invalid file path."""
    with pytest.raises(Exception):
        Document.from_kddb("/nonexistent/file.kddb")


def test_closed_document_access():
    """Test error handling when accessing closed document."""
    doc = Document.create_in_memory()
    doc.close()
    
    with pytest.raises(RuntimeError):
        _ = doc.uuid