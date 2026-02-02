#!/usr/bin/env python3
"""
Test script to verify ContentFeature implementation works correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up environment to use local library
os.environ['LD_LIBRARY_PATH'] = os.path.join(os.path.dirname(__file__), 'kodexa_document', '_native')

def test_content_feature():
    """Test that ContentFeature works correctly."""
    from kodexa_document import Document, ContentFeature

    print("Testing ContentFeature implementation...")

    # Create document and node
    doc = Document(inmemory=True)
    node = doc.create_node("paragraph", "Test content")

    # Test 1: add_feature returns ContentFeature
    print("1. Testing add_feature returns ContentFeature...")
    feature = node.add_feature("style", "font", "Arial")
    assert feature is not None, "add_feature should return ContentFeature"
    assert isinstance(feature, ContentFeature), f"Should be ContentFeature, got {type(feature)}"
    assert feature.value == ["Arial"], f"Value should be ['Arial'], got {feature.value}"
    assert feature.feature_type == "style", f"Type should be 'style', got {feature.feature_type}"
    assert feature.name == "font", f"Name should be 'font', got {feature.name}"
    print("   ✓ add_feature returns ContentFeature correctly")

    # Test 2: get_feature returns ContentFeature
    print("2. Testing get_feature returns ContentFeature...")
    retrieved = node.get_feature("style", "font")
    assert retrieved is not None, "get_feature should return ContentFeature"
    assert isinstance(retrieved, ContentFeature), f"Should be ContentFeature, got {type(retrieved)}"
    assert retrieved.value == ["Arial"], f"Value should be ['Arial'], got {retrieved.value}"
    print("   ✓ get_feature returns ContentFeature correctly")

    # Test 3: get_value() method works
    print("3. Testing ContentFeature.get_value() method...")
    value = retrieved.get_value()
    # get_value() now always returns the full array
    assert value == ["Arial"], f"get_value() should return ['Arial'], got {value}"
    print("   ✓ get_value() returns array of values")

    # Test 4: Appending to existing feature
    print("4. Testing appending to existing feature...")
    feature2 = node.add_feature("style", "font", "Helvetica")
    assert feature2 is not None
    assert feature2.value == ["Arial", "Helvetica"], f"Should have both values, got {feature2.value}"
    print("   ✓ Appending values works correctly")

    # Test 5: Feature with dict value
    print("5. Testing feature with dict value...")
    dict_feature = node.add_feature("style", "color", {"r": 255, "g": 0, "b": 0})
    assert dict_feature is not None
    assert dict_feature.value == [{"r": 255, "g": 0, "b": 0}], f"Dict should be in array, got {dict_feature.value}"
    # get_value() returns the full array
    value = dict_feature.get_value()
    assert value == [{"r": 255, "g": 0, "b": 0}], f"get_value() should return array, got {value}"
    print("   ✓ Dict values work correctly")

    # Test 6: Feature with array value
    print("6. Testing feature with array value...")
    multi_feature = node.add_feature("tags", "keywords", ["python", "test"])
    assert multi_feature is not None
    # Values are wrapped in array
    assert multi_feature.value == [["python", "test"]], f"Value should be wrapped, got {multi_feature.value}"
    print("   ✓ Array values work correctly")

    doc.close()
    print("\n✅ All ContentFeature tests passed!")

if __name__ == "__main__":
    try:
        test_content_feature()
        print("\n🎉 SUCCESS: ContentFeature implementation is working correctly!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
