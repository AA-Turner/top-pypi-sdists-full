"""
Test delete_on_close functionality.
"""

import tempfile
import os
import time
from pathlib import Path
import pytest
from kodexa_document import Document


def test_delete_on_close_true():
    """Test that file is deleted when delete_on_close=True."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    # Create and save a document
    doc1 = Document(inmemory=True)
    doc1.save(temp_path)
    doc1.close()
    
    # Verify file exists
    assert os.path.exists(temp_path), "File should exist after initial save"
    
    # Open with delete_on_close=True and detached=False to work on original file
    # Note: Using inmemory=False because with inmemory=True, the file may be deleted immediately after loading
    doc2 = Document(kddb_path=temp_path, delete_on_close=True, inmemory=False, detached=False)
    
    # File should still exist while document is open
    assert os.path.exists(temp_path), "File should exist while document is open"
    
    # Close the document
    doc2.close()
    
    # File should be deleted after close
    assert not os.path.exists(temp_path), "File should be deleted after close with delete_on_close=True"


def test_delete_on_close_false():
    """Test that file is NOT deleted when delete_on_close=False."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    try:
        # Create and save a document
        doc1 = Document(inmemory=True)
        doc1.save(temp_path)
        doc1.close()
        
        # Verify file exists
        assert os.path.exists(temp_path), "File should exist after initial save"
        
        # Open with delete_on_close=False (default) and detached=False
        doc2 = Document(kddb_path=temp_path, delete_on_close=False, inmemory=False, detached=False)
        
        # File should exist while document is open
        assert os.path.exists(temp_path), "File should exist while document is open"
        
        # Close the document
        doc2.close()
        
        # File should still exist after close
        assert os.path.exists(temp_path), "File should NOT be deleted after close with delete_on_close=False"
        
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_from_kddb_delete_on_close():
    """Test delete_on_close with from_kddb method."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    # Create and save initial document
    doc1 = Document(metadata={"test": "data"}, inmemory=True)
    doc1.save(temp_path)
    doc1.close()
    
    assert os.path.exists(temp_path), "File should exist after initial save"
    
    # Open with from_kddb and delete_on_close=True, detached=False
    # This should delete the original file on close
    # Note: Using inmemory=False to avoid immediate deletion
    doc2 = Document.from_kddb(temp_path, detached=False, delete_on_close=True, inmemory=False)
    
    # File should still exist while document is open
    assert os.path.exists(temp_path), "File should exist while document is open"
    
    # Close the document
    doc2.close()
    
    # Original file should be deleted
    assert not os.path.exists(temp_path), "Original file should be deleted with detached=False and delete_on_close=True"


def test_detached_with_delete_on_close():
    """Test interaction between detached and delete_on_close."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    try:
        # Create and save initial document
        doc1 = Document(metadata={"original": "data"}, inmemory=True)
        doc1.save(temp_path)
        doc1.close()
        
        assert os.path.exists(temp_path), "Original file should exist"
        
        # Open with detached=True and delete_on_close=True
        # This creates a temp copy; delete_on_close should delete the temp copy
        # The original should remain
        doc2 = Document.from_kddb(temp_path, detached=True, delete_on_close=True, inmemory=True)
        
        # Original file should still exist
        assert os.path.exists(temp_path), "Original file should exist with detached=True"
        
        # Close the document
        doc2.close()
        
        # Original file should still exist (only temp copy was deleted)
        assert os.path.exists(temp_path), "Original file should still exist after closing detached document"
        
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_new_document_delete_on_close():
    """Test delete_on_close with a new document (not opened from file)."""
    # Create new document with delete_on_close=True but no kddb_path
    doc = Document(metadata={"test": "new"}, delete_on_close=True, inmemory=True)
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    doc.save(temp_path)
    
    # File should exist after save
    assert os.path.exists(temp_path), "File should exist after save"
    
    # Close the document
    doc.close()
    
    # For a new document created with delete_on_close=True but saved later,
    # the saved file should NOT be deleted (delete_on_close applies to the file opened with, not saved to)
    assert os.path.exists(temp_path), "Saved file should not be deleted for new document"
    
    # Clean up
    os.unlink(temp_path)


def test_multiple_saves_delete_on_close():
    """Test delete_on_close behavior with multiple saves."""
    # Create initial file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path1 = f.name
    
    doc = Document(metadata={"test": "multi-save"}, inmemory=True)
    doc.save(temp_path1)
    doc.close()
    
    # Open with delete_on_close=True and detached=False
    doc2 = Document(kddb_path=temp_path1, delete_on_close=True, inmemory=False, detached=False)
    
    # Save to a different file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path2 = f.name
    
    doc2.save(temp_path2)
    
    # Both files should exist
    assert os.path.exists(temp_path1), "Original file should exist"
    assert os.path.exists(temp_path2), "Second file should exist"
    
    # Close the document
    doc2.close()
    
    # Only the file opened with delete_on_close should be deleted
    assert not os.path.exists(temp_path1), "Original file should be deleted"
    assert os.path.exists(temp_path2), "Second file should not be deleted"
    
    # Clean up
    if os.path.exists(temp_path2):
        os.unlink(temp_path2)


def test_context_manager_delete_on_close():
    """Test delete_on_close with context manager."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    # Create and save initial document
    doc1 = Document(inmemory=True)
    doc1.save(temp_path)
    doc1.close()
    
    assert os.path.exists(temp_path), "File should exist"
    
    # Use context manager with delete_on_close and detached=False
    with Document(kddb_path=temp_path, delete_on_close=True, inmemory=False, detached=False) as doc:
        assert os.path.exists(temp_path), "File should exist while in context"
    
    # File should be deleted after exiting context
    assert not os.path.exists(temp_path), "File should be deleted after context exit"


def test_error_handling_delete_on_close():
    """Test that delete_on_close still works even if an error occurs."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    # Create and save initial document
    doc1 = Document(inmemory=True)
    doc1.save(temp_path)
    doc1.close()
    
    assert os.path.exists(temp_path), "File should exist"
    
    # Open with delete_on_close and detached=False
    doc2 = Document(kddb_path=temp_path, delete_on_close=True, inmemory=False, detached=False)
    
    # Simulate an error by closing twice (second close might raise)
    doc2.close()
    try:
        doc2.close()  # This might raise an error
    except:
        pass  # Ignore any error
    
    # File should still be deleted
    assert not os.path.exists(temp_path), "File should be deleted even if error occurs"


if __name__ == "__main__":
    print("Testing delete_on_close functionality...")
    
    test_delete_on_close_true()
    print("✓ test_delete_on_close_true passed")
    
    test_delete_on_close_false()
    print("✓ test_delete_on_close_false passed")
    
    test_from_kddb_delete_on_close()
    print("✓ test_from_kddb_delete_on_close passed")
    
    test_detached_with_delete_on_close()
    print("✓ test_detached_with_delete_on_close passed")
    
    test_new_document_delete_on_close()
    print("✓ test_new_document_delete_on_close passed")
    
    test_multiple_saves_delete_on_close()
    print("✓ test_multiple_saves_delete_on_close passed")
    
    test_context_manager_delete_on_close()
    print("✓ test_context_manager_delete_on_close passed")
    
    test_error_handling_delete_on_close()
    print("✓ test_error_handling_delete_on_close passed")
    
    print("\nAll delete_on_close tests passed!")