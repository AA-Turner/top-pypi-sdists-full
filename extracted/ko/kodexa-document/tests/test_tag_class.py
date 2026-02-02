#!/usr/bin/env python
"""
Test Tag class implementation to verify legacy_python compatibility.
"""

from kodexa_document import Tag


def test_tag_creation_basic():
    """Test basic Tag creation with constructor."""
    print("Testing basic Tag creation...")
    
    # Test empty tag
    tag = Tag()
    assert 'uuid' in tag  # UUID should be auto-generated
    print("✓ Empty tag created with auto-generated UUID")
    
    # Test tag with basic fields
    tag = Tag(
        start=10,
        end=20,
        value="test value",
        confidence=0.95
    )
    assert tag['start'] == 10
    assert tag['end'] == 20  
    assert tag['value'] == "test value"
    assert tag['confidence'] == 0.95
    assert 'uuid' in tag
    print("✓ Tag created with basic fields")


def test_tag_dict_behavior():
    """Test that Tag behaves like a dictionary."""
    print("Testing Tag dict behavior...")
    
    tag = Tag(value="test", confidence=0.8)
    
    # Dict-style access
    assert tag['value'] == "test"
    assert tag['confidence'] == 0.8
    
    # Dict-style assignment
    tag['start'] = 5
    tag['end'] = 15
    assert tag['start'] == 5
    assert tag['end'] == 15
    
    # Dict-style iteration
    keys = list(tag.keys())
    assert 'value' in keys
    assert 'confidence' in keys
    assert 'uuid' in keys
    print("✓ Dict-style access, assignment, and iteration work")


def test_tag_dot_notation():
    """Test dot notation access and assignment."""
    print("Testing Tag dot notation...")
    
    tag = Tag(value="original")
    
    # Dot notation access
    assert tag.value == "original"
    
    # Dot notation assignment
    tag.start = 100
    tag.end = 200
    tag.confidence = 0.75
    
    assert tag.start == 100
    assert tag.end == 200
    assert tag.confidence == 0.75
    
    # Verify it's also accessible via dict
    assert tag['start'] == 100
    assert tag['end'] == 200
    assert tag['confidence'] == 0.75
    print("✓ Dot notation access and assignment work")


def test_tag_all_fields():
    """Test Tag with all possible legacy_python fields."""
    print("Testing Tag with all fields...")
    
    tag = Tag(
        start=0,
        end=10,
        value="test_value",
        uuid_val="custom-uuid-123",
        data={"key": "value"},
        confidence=0.9,
        group_uuid="group-uuid-456", 
        parent_group_uuid="parent-group-789",
        cell_index=2,
        index=1,
        bbox=[10, 20, 30, 40],  # Should be ignored
        note="test note",
        status="active",
        owner_uri="model://test:1.0.0",
        is_dirty=True
    )
    
    # Verify all fields except bbox
    assert tag.start == 0
    assert tag.end == 10
    assert tag.value == "test_value" 
    assert tag.uuid == "custom-uuid-123"
    assert tag.data == {"key": "value"}
    assert tag.confidence == 0.9
    assert tag.group_uuid == "group-uuid-456"
    assert tag.parent_group_uuid == "parent-group-789"
    assert tag.cell_index == 2
    assert tag.index == 1
    assert tag.note == "test note"
    assert tag.status == "active"
    assert tag.owner_uri == "model://test:1.0.0"
    assert tag.is_dirty is True
    
    # Verify bbox was ignored (not stored)
    assert 'bbox' not in tag
    print("✓ All fields stored correctly, bbox ignored as expected")


def test_tag_go_conversion():
    """Test conversion to/from Go backend format."""
    print("Testing Tag Go conversion...")
    
    # Create tag with Python field names
    tag = Tag(
        start=5,
        end=15,
        value="test",
        confidence=0.85,
        group_uuid="group-123",
        parent_group_uuid="parent-456",
        cell_index=1,
        owner_uri="model://test:1.0"
    )
    
    # Convert to Go format
    go_dict = tag.to_go_dict()
    
    # Verify field name conversion
    assert go_dict['startPos'] == 5
    assert go_dict['endPos'] == 15
    assert go_dict['value'] == "test"
    assert go_dict['confidence'] == 0.85
    assert go_dict['groupUuid'] == "group-123"
    assert go_dict['parentGroupUuid'] == "parent-456"
    assert go_dict['cellIndex'] == 1
    assert go_dict['ownerUri'] == "model://test:1.0"
    
    # Convert back from Go format
    tag2 = Tag.from_go_dict(go_dict)
    
    # Verify round-trip conversion
    assert tag2.start == 5
    assert tag2.end == 15
    assert tag2.value == "test"
    assert tag2.confidence == 0.85
    assert tag2.group_uuid == "group-123"
    assert tag2.parent_group_uuid == "parent-456"
    assert tag2.cell_index == 1
    assert tag2.owner_uri == "model://test:1.0"
    print("✓ Go format conversion works correctly")


def test_tag_json_serialization():
    """Test JSON serialization and deserialization."""
    print("Testing Tag JSON serialization...")
    
    tag = Tag(
        start=1,
        end=5,
        value="json_test",
        confidence=0.7
    )
    
    # Serialize to JSON
    json_str = tag.to_json()
    assert isinstance(json_str, str)
    
    # Deserialize from JSON
    tag2 = Tag.from_json(json_str)
    
    # Verify values
    assert tag2.start == 1
    assert tag2.end == 5
    assert tag2.value == "json_test"
    assert tag2.confidence == 0.7
    print("✓ JSON serialization works correctly")


def test_tag_copy():
    """Test Tag copying functionality."""
    print("Testing Tag copying...")
    
    tag1 = Tag(value="original", confidence=0.8, start=10)
    tag2 = tag1.copy()
    
    # Verify copy has same values
    assert tag2.value == "original"
    assert tag2.confidence == 0.8
    assert tag2.start == 10
    assert tag2.uuid == tag1.uuid  # Same UUID
    
    # Verify they're different objects
    assert tag1 is not tag2
    
    # Verify modifying copy doesn't affect original
    tag2.value = "modified"
    assert tag1.value == "original"
    assert tag2.value == "modified"
    print("✓ Tag copying works correctly")


def test_tag_repr():
    """Test Tag string representation."""
    print("Testing Tag repr...")
    
    tag = Tag(value="test_repr", confidence=0.6, start=0, end=4)
    repr_str = repr(tag)
    
    # Should contain key fields
    assert "value='test_repr'" in repr_str
    assert "confidence=0.6" in repr_str
    assert "start=0" in repr_str
    assert "end=4" in repr_str
    assert "uuid=" in repr_str  # UUID should be abbreviated
    
    print(f"✓ Tag repr works: {repr_str}")


if __name__ == "__main__":
    print("=" * 60)
    print("Tag Class Implementation Test Suite")
    print("=" * 60 + "\n")
    
    test_tag_creation_basic()
    test_tag_dict_behavior()
    test_tag_dot_notation()
    test_tag_all_fields()
    test_tag_go_conversion()
    test_tag_json_serialization()
    test_tag_copy()
    test_tag_repr()
    
    print("\n" + "=" * 60)
    print("✅ All Tag class tests completed successfully!")
    print("=" * 60)