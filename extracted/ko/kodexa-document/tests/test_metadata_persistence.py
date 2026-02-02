"""
Test metadata persistence through save/load operations.
"""

import tempfile
import os
from pathlib import Path
from kodexa_document import Document


def test_metadata_persistence_to_file():
    """Test that metadata persists when saving to and loading from a file."""
    # Create document with metadata
    metadata = {
        "title": "Test Document",
        "author": "Test Author",
        "tags": ["test", "metadata", "persistence"],
        "count": 42,
        "active": True
    }
    
    doc1 = Document(metadata=metadata, inmemory=True)
    doc1_uuid = doc1.uuid
    
    # Verify metadata is set correctly
    doc1_metadata = doc1.metadata
    print(f"Original metadata: {doc1_metadata}")
    assert doc1_metadata.get("title") == "Test Document"
    assert doc1_metadata.get("author") == "Test Author"
    assert doc1_metadata.get("tags") == ["test", "metadata", "persistence"]
    assert doc1_metadata.get("count") == 42
    assert doc1_metadata.get("active") == True
    
    # Save to file
    with tempfile.NamedTemporaryFile(suffix='.kddb', delete=False) as f:
        temp_path = f.name
    
    try:
        doc1.save(temp_path)
        doc1.close()
        
        # Load from file
        doc2 = Document.from_kddb(temp_path, inmemory=True)
        assert doc2.uuid == doc1_uuid
        
        # Check metadata after loading
        doc2_metadata = doc2.metadata
        print(f"Loaded metadata: {doc2_metadata}")
        
        # These assertions will likely fail if metadata isn't persisted
        assert doc2_metadata.get("title") == "Test Document", f"Expected 'Test Document', got {doc2_metadata.get('title')}"
        assert doc2_metadata.get("author") == "Test Author", f"Expected 'Test Author', got {doc2_metadata.get('author')}"
        assert doc2_metadata.get("tags") == ["test", "metadata", "persistence"], f"Expected tags list, got {doc2_metadata.get('tags')}"
        assert doc2_metadata.get("count") == 42, f"Expected 42, got {doc2_metadata.get('count')}"
        assert doc2_metadata.get("active") == True, f"Expected True, got {doc2_metadata.get('active')}"
        
        doc2.close()
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_metadata_persistence_to_bytes():
    """Test that metadata persists when converting to bytes and back."""
    # Create document with metadata
    metadata = {
        "project": "Kodexa",
        "module": "Document",
        "test": "persistence"
    }
    
    doc1 = Document(metadata=metadata, inmemory=True)
    doc1_uuid = doc1.uuid
    
    # Verify metadata is set
    print(f"Original metadata: {doc1.metadata}")
    assert doc1.metadata.get("project") == "Kodexa"
    assert doc1.metadata.get("module") == "Document"
    assert doc1.metadata.get("test") == "persistence"
    
    # Convert to bytes
    kddb_bytes = doc1.to_kddb()
    doc1.close()
    
    # Load from bytes
    doc2 = Document.from_kddb(kddb_bytes, inmemory=True)
    assert doc2.uuid == doc1_uuid
    
    # Check metadata after loading
    doc2_metadata = doc2.metadata
    print(f"Loaded metadata: {doc2_metadata}")
    
    # These assertions will likely fail if metadata isn't persisted
    assert doc2_metadata.get("project") == "Kodexa", f"Expected 'Kodexa', got {doc2_metadata.get('project')}"
    assert doc2_metadata.get("module") == "Document", f"Expected 'Document', got {doc2_metadata.get('module')}"
    assert doc2_metadata.get("test") == "persistence", f"Expected 'persistence', got {doc2_metadata.get('test')}"
    
    doc2.close()


def test_empty_metadata_after_load():
    """Test what happens when a document with no metadata is saved and loaded."""
    # Create document without metadata
    doc1 = Document(inmemory=True)
    doc1_uuid = doc1.uuid
    
    # Save and load
    kddb_bytes = doc1.to_kddb()
    doc1.close()
    
    doc2 = Document.from_kddb(kddb_bytes, inmemory=True)
    assert doc2.uuid == doc1_uuid
    
    # Check metadata - should be empty dict or similar
    doc2_metadata = doc2.metadata
    print(f"Empty document metadata after load: {doc2_metadata}")
    assert isinstance(doc2_metadata, dict)
    
    doc2.close()


if __name__ == "__main__":
    print("Testing metadata persistence to file...")
    try:
        test_metadata_persistence_to_file()
        print("✓ Metadata persistence to file PASSED")
    except AssertionError as e:
        print(f"✗ Metadata persistence to file FAILED: {e}")
    
    print("\nTesting metadata persistence to bytes...")
    try:
        test_metadata_persistence_to_bytes()
        print("✓ Metadata persistence to bytes PASSED")
    except AssertionError as e:
        print(f"✗ Metadata persistence to bytes FAILED: {e}")
    
    print("\nTesting empty metadata after load...")
    try:
        test_empty_metadata_after_load()
        print("✓ Empty metadata test PASSED")
    except AssertionError as e:
        print(f"✗ Empty metadata test FAILED: {e}")