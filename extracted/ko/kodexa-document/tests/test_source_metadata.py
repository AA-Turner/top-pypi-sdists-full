#!/usr/bin/env python
"""
Test SourceMetadata implementation to verify legacy_python compatibility.
"""

from kodexa_document import Document, SourceMetadata


def test_basic_source_operations():
    """Test basic source metadata operations."""
    print("Testing basic source operations...")
    
    # Create document with SourceMetadata
    source = SourceMetadata()
    source.original_filename = 'test.pdf'
    source.original_path = '/path/to/test.pdf'
    source.mime_type = 'application/pdf'
    
    # Create document with source (need to convert to dict for Document constructor)
    doc = Document(source={'originalFilename': 'test.pdf', 
                          'originalPath': '/path/to/test.pdf',
                          'mimeType': 'application/pdf'})
    
    # Verify source was set
    assert doc.source.original_filename == 'test.pdf'
    assert doc.source.original_path == '/path/to/test.pdf'
    assert doc.source.mime_type == 'application/pdf'
    print("✓ Created document with source metadata")
    
    # Test dot notation write
    doc.source.checksum = 'abc123'
    assert doc.source.checksum == 'abc123'
    print("✓ Dot notation write works")
    
    # Test that cached approach returns same instance
    source1 = doc.source
    source2 = doc.source
    assert source1 is source2
    print("✓ Same cached instance returned (efficient)")
    
    doc.close()
    print("✓ Basic source operations passed\n")


def test_source_persistence():
    """Test that source changes persist in Go."""
    print("Testing source persistence...")
    
    doc = Document()
    
    # Set some source metadata
    doc.source.original_filename = 'document.docx'
    doc.source.connector = 'SharePoint'
    doc.source.created = '2024-12-25'
    
    # Access again and verify it persisted
    fresh_source = doc.source
    assert fresh_source.original_filename == 'document.docx'
    assert fresh_source.connector == 'SharePoint'
    assert fresh_source.created == '2024-12-25'
    print("✓ Source metadata persists across accesses")
    
    doc.close()
    print("✓ Source persistence passed\n")


def test_legacy_patterns():
    """Test patterns commonly used in legacy_python."""
    print("Testing legacy_python patterns...")
    
    # Pattern 1: Direct field assignment
    doc = Document()
    doc.source.original_filename = "test.doc"
    assert doc.source.original_filename == "test.doc"
    print("✓ Direct field assignment works")
    
    # Pattern 2: Multiple field assignments
    doc.source.original_path = "/path/to/file"
    doc.source.mime_type = "application/msword"
    doc.source.checksum = "xyz789"
    
    # Verify all fields preserved
    assert doc.source.original_filename == "test.doc"
    assert doc.source.original_path == "/path/to/file"
    assert doc.source.mime_type == "application/msword"
    assert doc.source.checksum == "xyz789"
    print("✓ Multiple field assignments preserved")
    
    # Pattern 3: Headers dict field
    doc.source.headers = {"Content-Type": "text/plain", "X-Custom": "value"}
    assert doc.source.headers == {"Content-Type": "text/plain", "X-Custom": "value"}
    print("✓ Headers dict field works")
    
    doc.close()
    print("✓ Legacy patterns passed\n")


def test_all_source_fields():
    """Test all SourceMetadata fields."""
    print("Testing all source fields...")
    
    doc = Document()
    
    # Set all fields
    doc.source.original_filename = "test.pdf"
    doc.source.original_path = "/docs/test.pdf"
    doc.source.checksum = "sha256:abcdef"
    doc.source.cid = "cache-id-123"
    doc.source.last_modified = "2024-12-24T10:00:00Z"
    doc.source.created = "2024-12-01T09:00:00Z"
    doc.source.connector = "FileSystem"
    doc.source.mime_type = "application/pdf"
    doc.source.headers = {"X-Version": "1.0"}
    doc.source.lineage_document_uuid = "uuid-lineage"
    doc.source.source_document_uuid = "uuid-source"
    doc.source.pdf_document_uuid = "uuid-pdf"
    
    # Verify all fields
    source = doc.source
    assert source.original_filename == "test.pdf"
    assert source.original_path == "/docs/test.pdf"
    assert source.checksum == "sha256:abcdef"
    assert source.cid == "cache-id-123"
    assert source.last_modified == "2024-12-24T10:00:00Z"
    assert source.created == "2024-12-01T09:00:00Z"
    assert source.connector == "FileSystem"
    assert source.mime_type == "application/pdf"
    assert source.headers == {"X-Version": "1.0"}
    assert source.lineage_document_uuid == "uuid-lineage"
    assert source.source_document_uuid == "uuid-source"
    assert source.pdf_document_uuid == "uuid-pdf"
    print("✓ All source fields work correctly")
    
    doc.close()
    print("✓ All fields test passed\n")


def test_source_setter():
    """Test setting source via setter."""
    print("Testing source setter...")
    
    doc = Document()
    
    # Set source via setter with dict
    doc.source = {
        'originalFilename': 'new.txt',
        'mimeType': 'text/plain'
    }
    
    # Verify it was set
    assert doc.source.original_filename == 'new.txt'
    assert doc.source.mime_type == 'text/plain'
    print("✓ Source setter with dict works")
    
    # Set source via setter with SourceMetadata object
    new_source = SourceMetadata()
    new_source.original_filename = 'updated.pdf'
    new_source.original_path = '/updated/path'
    doc.source = new_source
    
    # Verify it was set
    assert doc.source.original_filename == 'updated.pdf'
    assert doc.source.original_path == '/updated/path'
    print("✓ Source setter with SourceMetadata works")
    
    doc.close()
    print("✓ Source setter test passed\n")


def test_null_values():
    """Test handling of None/null values."""
    print("Testing null value handling...")
    
    doc = Document()
    
    # All fields should start as None
    source = doc.source
    assert source.original_filename is None
    assert source.checksum is None
    assert source.mime_type is None
    print("✓ Fields initialize as None")
    
    # Set some fields
    doc.source.original_filename = "test.txt"
    doc.source.mime_type = "text/plain"
    
    # Other fields should still be None
    assert doc.source.checksum is None
    assert doc.source.cid is None
    print("✓ Unset fields remain None")
    
    # Can set fields back to None
    doc.source.mime_type = None
    assert doc.source.mime_type is None
    assert doc.source.original_filename == "test.txt"  # Other fields preserved
    print("✓ Can set fields to None")
    
    doc.close()
    print("✓ Null value handling passed\n")


if __name__ == "__main__":
    print("=" * 60)
    print("SourceMetadata Implementation Test Suite")
    print("=" * 60 + "\n")
    
    test_basic_source_operations()
    test_source_persistence()
    test_legacy_patterns()
    test_all_source_fields()
    test_source_setter()
    test_null_values()
    
    print("=" * 60)
    print("✅ All SourceMetadata tests completed successfully!")
    print("=" * 60)