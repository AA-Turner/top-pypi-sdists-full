#!/usr/bin/env python
"""
Test ContentException implementation to verify legacy_python compatibility.
"""

from kodexa_document import ContentException


def test_basic_content_exception():
    """Test basic ContentException creation with required fields."""
    print("Testing basic ContentException creation...")
    
    # Create with just required fields
    exc = ContentException("VALIDATION_ERROR", "Missing required field")
    
    assert exc['exception_type'] == "VALIDATION_ERROR"
    assert exc['message'] == "Missing required field"
    assert exc['severity'] == "ERROR"  # Default value
    
    # Test dot notation access
    assert exc.exception_type == "VALIDATION_ERROR"
    assert exc.message == "Missing required field"
    assert exc.severity == "ERROR"
    
    print("✓ Basic ContentException created successfully")


def test_content_exception_with_all_fields():
    """Test ContentException with all optional fields."""
    print("Testing ContentException with all fields...")
    
    exc = ContentException(
        exception_type="EXTRACTION_ERROR",
        message="Failed to extract value",
        severity="WARNING",
        tag="entity/person",
        group_uuid="group-123",
        tag_uuid="tag-456",
        exception_type_id="EXT001",
        exception_details="Detailed error information here",
        node_uuid="node-789",
        value="John Doe",
        boolean_value=True
    )
    
    # Verify all fields are stored
    assert exc.exception_type == "EXTRACTION_ERROR"
    assert exc.message == "Failed to extract value"
    assert exc.severity == "WARNING"
    assert exc.tag == "entity/person"
    assert exc.group_uuid == "group-123"
    assert exc.tag_uuid == "tag-456"
    assert exc.exception_type_id == "EXT001"
    assert exc.exception_details == "Detailed error information here"
    assert exc.node_uuid == "node-789"
    assert exc.value == "John Doe"
    assert exc.boolean_value is True
    
    print("✓ All fields stored correctly")


def test_dict_behavior():
    """Test that ContentException behaves like a dictionary."""
    print("Testing dict-like behavior...")
    
    exc = ContentException("TEST_ERROR", "Test message")
    
    # Dict-style access
    assert exc['exception_type'] == "TEST_ERROR"
    assert exc['message'] == "Test message"
    
    # Dict-style assignment
    exc['custom_field'] = "custom_value"
    assert exc['custom_field'] == "custom_value"
    
    # Check keys
    assert 'exception_type' in exc
    assert 'message' in exc
    assert 'severity' in exc
    assert 'custom_field' in exc
    
    # Iteration
    keys = list(exc.keys())
    assert 'exception_type' in keys
    assert 'message' in keys
    
    print("✓ Dict-like behavior works correctly")


def test_dot_notation():
    """Test dot notation access and assignment."""
    print("Testing dot notation...")
    
    exc = ContentException("ERROR", "Initial message")
    
    # Dot notation read
    assert exc.exception_type == "ERROR"
    assert exc.message == "Initial message"
    
    # Dot notation write
    exc.severity = "CRITICAL"
    exc.node_uuid = "node-123"
    
    assert exc.severity == "CRITICAL"
    assert exc.node_uuid == "node-123"
    
    # Verify also accessible via dict
    assert exc['severity'] == "CRITICAL"
    assert exc['node_uuid'] == "node-123"
    
    print("✓ Dot notation works correctly")


def test_from_go_dict():
    """Test creating ContentException from Go backend data."""
    print("Testing from_go_dict conversion...")
    
    # Simulate data from Go backend
    go_data = {
        'exception_type': 'VALIDATION_ERROR',
        'message': 'Invalid data format',
        'severity': 'ERROR',
        'tag': 'validation/format',
        'group_uuid': 'group-abc',
        'tag_uuid': 'tag-def',
        'exception_type_id': 'VAL001',
        'exception_details': 'Expected JSON, got XML',
        'node_uuid': 'node-ghi',
        'id': 1,
        'path': '/document/body',
        'open': True,
        'created_at': '2024-12-25T10:00:00Z'
    }
    
    exc = ContentException.from_go_dict(go_data)
    
    # Verify conversion
    assert exc.exception_type == 'VALIDATION_ERROR'
    assert exc.message == 'Invalid data format'
    assert exc.severity == 'ERROR'
    assert exc.tag == 'validation/format'
    assert exc.group_uuid == 'group-abc'
    assert exc.tag_uuid == 'tag-def'
    assert exc.exception_type_id == 'VAL001'
    assert exc.exception_details == 'Expected JSON, got XML'
    assert exc.node_uuid == 'node-ghi'
    
    # Additional Go fields should also be present
    assert exc.id == 1
    assert exc.path == '/document/body'
    assert exc.open is True
    assert exc.created_at == '2024-12-25T10:00:00Z'
    
    print("✓ from_go_dict conversion works correctly")


def test_to_go_dict():
    """Test converting ContentException to Go backend format."""
    print("Testing to_go_dict conversion...")

    exc = ContentException(
        exception_type="PROCESSING_ERROR",
        message="Processing failed",
        severity="ERROR",
        tag="processing/failed",
        node_uuid="node-123"
    )

    go_dict = exc.to_go_dict()

    # Verify conversion - to_go_dict converts to camelCase for Go backend
    assert go_dict['exceptionType'] == "PROCESSING_ERROR"
    assert go_dict['message'] == "Processing failed"
    assert go_dict['severity'] == "ERROR"
    assert go_dict['tag'] == "processing/failed"
    assert go_dict['nodeUuid'] == "node-123"

    # Should not include None values (check camelCase keys)
    assert 'groupUuid' not in go_dict
    assert 'tagUuid' not in go_dict
    assert 'value' not in go_dict

    print("✓ to_go_dict conversion works correctly")


def test_legacy_compatibility():
    """Test patterns used in legacy_python."""
    print("Testing legacy_python compatibility patterns...")
    
    # Legacy pattern 1: Direct instantiation with positional args
    exc = ContentException("TEST_ERROR", "Test message")
    assert exc.exception_type == "TEST_ERROR"
    assert exc.message == "Test message"
    
    # Legacy pattern 2: Using kwargs
    exc2 = ContentException(
        exception_type="VALIDATION",
        message="Validation failed",
        severity="WARNING",
        node_uuid="node-456"
    )
    assert exc2.exception_type == "VALIDATION"
    assert exc2.severity == "WARNING"
    assert exc2.node_uuid == "node-456"
    
    # Legacy pattern 3: Adding fields after creation
    exc3 = ContentException("ERROR", "Error occurred")
    exc3.custom_data = {"key": "value"}
    assert exc3.custom_data == {"key": "value"}
    
    print("✓ Legacy compatibility patterns work")


def test_string_representations():
    """Test __str__ and __repr__ methods."""
    print("Testing string representations...")
    
    exc = ContentException(
        exception_type="DATA_ERROR",
        message="Invalid data",
        severity="WARNING"
    )
    
    # Test __repr__
    repr_str = repr(exc)
    assert "ContentException" in repr_str
    assert "DATA_ERROR" in repr_str
    assert "Invalid data" in repr_str
    assert "WARNING" in repr_str
    
    # Test __str__
    str_repr = str(exc)
    assert "WARNING" in str_repr
    assert "DATA_ERROR" in str_repr
    assert "Invalid data" in str_repr
    
    print(f"✓ String representations work: {str_repr}")


def test_empty_data_handling():
    """Test handling of empty or None data."""
    print("Testing empty data handling...")
    
    # from_go_dict with empty dict
    exc = ContentException.from_go_dict({})
    assert exc.exception_type == "UNKNOWN"
    assert exc.message == ""
    assert exc.severity == "ERROR"
    
    # from_go_dict with None (shouldn't crash)
    exc2 = ContentException.from_go_dict(None)
    assert exc2.exception_type == "UNKNOWN"
    assert exc2.message == ""
    
    print("✓ Empty data handling works correctly")


if __name__ == "__main__":
    print("=" * 60)
    print("ContentException Implementation Test Suite")
    print("=" * 60 + "\n")
    
    test_basic_content_exception()
    test_content_exception_with_all_fields()
    test_dict_behavior()
    test_dot_notation()
    test_from_go_dict()
    test_to_go_dict()
    test_legacy_compatibility()
    test_string_representations()
    test_empty_data_handling()
    
    print("\n" + "=" * 60)
    print("✅ All ContentException tests completed successfully!")
    print("=" * 60)