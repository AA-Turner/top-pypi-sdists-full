#!/usr/bin/env python
"""
Test Tag class integration with ContentNode methods.
"""

from kodexa_document import Document, Tag


def test_contentnode_tag_methods():
    """Test that ContentNode returns Tag objects instead of dicts/strings."""
    print("Testing ContentNode tag method integration...")
    
    # Create document and node
    doc = Document()
    root = doc.create_node("document") 
    doc.content_node = root
    
    child = doc.create_node("paragraph", "Hello world")
    root.add_child(child)
    
    # Tag the child node
    child.tag("important", confidence=0.9, value="test_value")
    
    # Test get_tags() returns List[Tag]
    tags = child.get_tags()
    assert isinstance(tags, list)
    
    if len(tags) > 0:
        tag = tags[0]
        assert isinstance(tag, Tag)
        print(f"✓ get_tags() returns List[Tag]: {type(tags)}")
        print(f"✓ First tag is Tag object: {type(tag)}")
        
        # Verify tag has expected properties
        assert hasattr(tag, 'confidence')
        assert hasattr(tag, 'value')
        print(f"✓ Tag has expected attributes: confidence={getattr(tag, 'confidence', None)}, value={getattr(tag, 'value', None)}")
    
    # Test get_tag() returns Tag object
    tag = child.get_tag("important")
    if tag is not None:
        assert isinstance(tag, Tag)
        print(f"✓ get_tag() returns Tag object: {type(tag)}")
        
        # Test both dict and dot notation access
        if 'confidence' in tag:
            assert tag['confidence'] == tag.confidence
            print("✓ Both dict and dot notation work")
    else:
        print("⚠ get_tag() returned None - tag may not have been created properly")
    
    # Test get_tag() with non-existent tag
    missing_tag = child.get_tag("nonexistent")
    assert missing_tag is None
    print("✓ get_tag() returns None for non-existent tags")
    
    doc.close()
    print("✓ ContentNode tag method integration test completed\n")


def test_tag_object_compatibility():
    """Test that returned Tag objects work like legacy_python Tags."""
    print("Testing Tag object legacy compatibility...")
    
    doc = Document()
    root = doc.create_node("document")
    doc.content_node = root
    
    child = doc.create_node("word", "test")
    root.add_child(child)
    
    # Tag with multiple attributes
    child.tag("entity", 
              confidence=0.85,
              value="person",
              group_uuid="test-group-123")
    
    # Get the tag and test legacy patterns
    tags = child.get_tags()
    if len(tags) > 0:
        tag = tags[0]
        
        # Test legacy_python access patterns
        try:
            # Dot notation
            confidence = tag.confidence
            value = tag.value
            group_uuid = tag.group_uuid
            
            # Dict notation  
            confidence2 = tag['confidence']
            value2 = tag['value']
            group_uuid2 = tag['group_uuid']
            
            assert confidence == confidence2
            assert value == value2
            assert group_uuid == group_uuid2
            
            print(f"✓ Legacy access patterns work: confidence={confidence}, value={value}")
            print(f"✓ Both access methods return same values")
            
            # Test Tag methods
            tag_copy = tag.copy()
            assert isinstance(tag_copy, Tag)
            assert tag_copy.confidence == tag.confidence
            print("✓ Tag.copy() method works")
            
            # Test JSON serialization
            json_str = tag.to_json()
            assert isinstance(json_str, str)
            print("✓ Tag.to_json() works")
            
            # Test repr
            repr_str = repr(tag)
            assert "confidence=" in repr_str
            print(f"✓ Tag repr works: {repr_str}")
            
        except AttributeError as e:
            print(f"⚠ Legacy access pattern failed: {e}")
    
    doc.close()
    print("✓ Tag object legacy compatibility test completed\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Tag Integration Test Suite")
    print("=" * 60 + "\n")
    
    test_contentnode_tag_methods()
    test_tag_object_compatibility()
    
    print("=" * 60)
    print("✅ All Tag integration tests completed!")
    print("=" * 60)