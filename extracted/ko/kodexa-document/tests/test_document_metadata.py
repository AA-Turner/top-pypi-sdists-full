#!/usr/bin/env python
"""
Test DocumentMetadata implementation to verify legacy_python compatibility.
"""

from kodexa_document import Document, DocumentMetadata


def test_basic_metadata():
    """Test basic metadata operations."""
    print("Testing basic metadata operations...")
    
    # Create document with DocumentMetadata
    meta = DocumentMetadata()
    meta.author = 'John Doe'
    meta.date = '2024-12-24'
    doc = Document(metadata=meta)
    
    # Verify metadata was set
    assert doc.metadata.author == 'John Doe'
    assert doc.metadata.date == '2024-12-24'
    print("✓ Created document with DocumentMetadata")
    
    # Test dot notation write
    doc.metadata.title = 'Test Document'
    assert doc.metadata.title == 'Test Document'
    print("✓ Dot notation write works")
    
    # Test dict notation write
    doc.metadata['version'] = '1.0.0'
    assert doc.metadata['version'] == '1.0.0'
    print("✓ Dict notation write works")
    
    # Test that cached approach returns same instance
    meta1 = doc.metadata
    meta2 = doc.metadata
    assert meta1 is meta2
    print("✓ Same cached instance returned (efficient)")
    
    # And they have the expected data
    assert dict(meta1) == dict(meta2)
    print("✓ Both references point to same data")
    
    doc.close()
    print("✓ Basic metadata operations passed\n")


def test_metadata_persistence():
    """Test that metadata changes persist in Go."""
    print("Testing metadata persistence...")
    
    doc = Document()
    
    # Set some metadata
    doc.metadata.author = 'Jane Smith'
    doc.metadata.project = 'Kodexa'
    
    # Access again and verify it persisted
    fresh_meta = doc.metadata
    assert fresh_meta.author == 'Jane Smith'
    assert fresh_meta.project == 'Kodexa'
    print("✓ Metadata persists across accesses")
    
    doc.close()
    print("✓ Metadata persistence passed\n")


def test_legacy_patterns():
    """Test patterns commonly used in legacy_python."""
    print("Testing legacy_python patterns...")
    
    # Pattern 1: Create with empty DocumentMetadata
    doc = Document(DocumentMetadata())
    # Metadata contains uuid/version but no user metadata
    user_metadata = {k: v for k, v in doc.metadata.items() if k not in ('uuid', 'version')}
    assert user_metadata == {}
    print("✓ Document(DocumentMetadata()) works")
    
    # Pattern 2: Create with initialized DocumentMetadata
    doc2 = Document(DocumentMetadata({"key": "value"}))
    assert doc2.metadata.key == "value"
    print("✓ DocumentMetadata({...}) initialization works")
    
    # Pattern 3: Dot notation assignment (like doc.metadata.cheese = "value")
    doc.metadata.cheese = "cheddar"
    assert doc.metadata.cheese == "cheddar"
    print("✓ Legacy dot notation pattern works")
    
    doc.close()
    doc2.close()
    print("✓ Legacy patterns passed\n")


def test_deep_nested_assignments():
    """Test that deep nested dot notation works correctly with parent-child tracking."""
    print("Testing deep nested assignments...")
    
    doc = Document()
    
    # Test creating deeply nested structure through dot notation
    doc.metadata.config.theme.name = "dark"
    doc.metadata.config.theme.primary = "blue"
    doc.metadata.config.locale = "en_US"
    
    # Verify all values are preserved
    meta = doc.metadata
    assert meta.config.theme.name == "dark"
    assert meta.config.theme.primary == "blue"
    assert meta.config.locale == "en_US"
    print("✓ Deep nested dot notation (a.b.c = value) works correctly")
    
    # Test that sequential assignments preserve previous values
    doc.metadata.deeply.nested.field = "value1"
    doc.metadata.deeply.nested.another = "value2"
    doc.metadata.deeply.other = "value3"
    
    # Verify all values preserved
    meta2 = doc.metadata
    assert meta2.deeply.nested.field == "value1"
    assert meta2.deeply.nested.another == "value2"
    assert meta2.deeply.other == "value3"
    print("✓ Sequential nested assignments preserve all values")
    
    # Test mixed dict and dot notation
    doc.metadata.mixed = {"initial": "value"}
    doc.metadata.mixed.added = "new_value"
    
    meta3 = doc.metadata
    assert meta3.mixed.initial == "value"
    assert meta3.mixed.added == "new_value"
    print("✓ Mixed dict/dot notation works correctly")
    
    doc.close()
    print("✓ Deep nested assignments fully functional\n")


def test_json_serialization():
    """Test that metadata values are properly JSON serialized."""
    print("Testing JSON serialization...")
    
    doc = Document()
    
    # Test various types
    doc.metadata.string = "text"
    doc.metadata.number = 42
    doc.metadata.float_val = 3.14
    doc.metadata.bool_val = True
    doc.metadata.null_val = None
    doc.metadata.list_val = [1, 2, 3]
    doc.metadata.dict_val = {"nested": "object"}
    
    # Verify all types preserved
    meta = doc.metadata
    assert meta.string == "text"
    assert meta.number == 42
    assert meta.float_val == 3.14
    assert meta.bool_val is True
    assert meta.null_val is None
    assert meta.list_val == [1, 2, 3]
    assert meta.dict_val == {"nested": "object"}
    print("✓ All JSON types preserved correctly")
    
    doc.close()
    print("✓ JSON serialization passed\n")


if __name__ == "__main__":
    print("=" * 60)
    print("DocumentMetadata Implementation Test Suite")
    print("Using Cached Approach: Simple and Efficient")
    print("=" * 60 + "\n")
    
    test_basic_metadata()
    test_metadata_persistence()
    test_legacy_patterns()
    test_deep_nested_assignments()
    test_json_serialization()
    
    print("=" * 60)
    print("✅ All tests completed successfully!")
    print("=" * 60)