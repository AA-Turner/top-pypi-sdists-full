"""
Comprehensive tests for feature appending behavior.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from kodexa_document import Document, ContentNode


def test_feature_value_appends():
    """Test that values append when adding to same feature."""
    doc = Document(inmemory=True)

    # Create a node
    node = doc.create_node("paragraph", "Test content")

    # Add a feature
    node.add_feature("style", "font", "Arial")

    # Get all features and check the first one
    features = node.get_features()
    assert len(features) == 1
    first_feature = features[0]

    # Check initial value
    feature = node.get_feature("style", "font")
    assert feature.value == ["Arial"]

    # Add the same feature again - should append
    node.add_feature("style", "font", "Helvetica")

    # Get the feature again
    feature = node.get_feature("style", "font")
    font_values = feature.value
    assert font_values == ["Arial", "Helvetica"]

    # Get all features - still just one feature
    features = node.get_features()
    assert len(features) == 1

    # Verify we have multiple values
    assert isinstance(font_values, list)
    assert len(font_values) == 2

    doc.close()
    print("✓ test_feature_value_appends passed")


def test_feature_append_with_different_types():
    """Test appending features with different value types."""
    doc = Document(inmemory=True)

    node = doc.create_node("paragraph", "Test content")

    # Add a string value
    node.add_feature("metadata", "tag", "first")

    # Add a dict value to the same feature
    node.add_feature("metadata", "tag", {"type": "second"})

    # Add a number value
    node.add_feature("metadata", "tag", 42)

    # Check all values are in the array
    feature = node.get_feature("metadata", "tag")
    tag_values = feature.value
    assert isinstance(tag_values, list)
    assert len(tag_values) == 3
    assert tag_values[0] == "first"
    assert tag_values[1] == {"type": "second"}
    assert tag_values[2] == 42

    doc.close()
    print("✓ test_feature_append_with_different_types passed")


def test_feature_stores_values_in_arrays():
    """Test that values are stored in arrays."""
    doc = Document(inmemory=True)

    node = doc.create_node("paragraph", "Test content")

    # Add a feature with a dict value
    node.add_feature("style", "color", {"r": 255, "g": 0, "b": 0})

    # Get the feature - values are stored in arrays
    feature = node.get_feature("style", "color")
    color_value = feature.value
    assert isinstance(color_value, list)
    assert len(color_value) == 1
    assert color_value[0] == {"r": 255, "g": 0, "b": 0}

    # Add another feature
    node.add_feature("style", "background", "white")

    # Values are stored in arrays
    feature = node.get_feature("style", "background")
    bg_value = feature.value
    assert isinstance(bg_value, list)
    assert len(bg_value) == 1
    assert bg_value[0] == "white"

    doc.close()
    print("✓ test_feature_stores_values_in_arrays passed")


def test_feature_persistence_through_save_load():
    """Test that appended features persist correctly through save/load."""
    import tempfile
    import os

    # Create document and use auto-created root node
    doc1 = Document(inmemory=True)
    root = doc1.content_node
    root.content = "Root"

    child = doc1.create_node("paragraph", "Test paragraph")
    root.add_child(child)

    # Add multiple values to same feature
    child.add_feature("style", "class", "header")
    child.add_feature("style", "class", "bold")
    child.add_feature("style", "class", "italic")

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".kddb", delete=False) as f:
        temp_path = f.name

    try:
        doc1.save(temp_path)
        doc1.close()

        # Load it back
        doc2 = Document.from_kddb(temp_path, inmemory=True)

        # Navigate to the child node
        loaded_root = doc2.content_node
        loaded_children = loaded_root.get_children()
        assert len(loaded_children) == 1

        loaded_child = loaded_children[0]

        # Check the feature has all values
        feature = loaded_child.get_feature("style", "class")

        # If get_feature returns None, try getting all features as a workaround
        if feature is None:
            all_features = loaded_child.get_features()
            print(f"DEBUG: All features = {all_features}")

            # Find the feature in the list format
            if isinstance(all_features, list):
                for feature in all_features:
                    if feature.get('type') == 'style' and feature.get('name') == 'class':
                        class_values = feature.get('value')
                        break

            if feature is None:
                assert False, "Feature not found after loading"

        class_values = feature.value if feature else None
        print(f"DEBUG: class_values = {class_values}, type = {type(class_values)}")
        assert isinstance(class_values, list), f"Expected list but got {type(class_values)}: {class_values}"
        assert len(class_values) == 3
        assert "header" in class_values
        assert "bold" in class_values
        assert "italic" in class_values

        doc2.close()
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    print("✓ test_feature_persistence_through_save_load passed")


def test_multiple_features_same_type_different_names():
    """Test that features with same type but different names are independent."""
    doc = Document(inmemory=True)

    node = doc.create_node("paragraph", "Test content")

    # Add features with same type but different names
    node.add_feature("style", "font", "Arial")
    node.add_feature("style", "font", "Helvetica")  # Appends to style:font

    node.add_feature("style", "color", "red")
    node.add_feature("style", "color", "blue")  # Appends to style:color

    node.add_feature("style", "size", "12pt")  # New feature style:size

    # Check each feature independently
    font_feature = node.get_feature("style", "font")
    assert font_feature.value == ["Arial", "Helvetica"]

    color_feature = node.get_feature("style", "color")
    assert color_feature.value == ["red", "blue"]

    size_feature = node.get_feature("style", "size")
    assert size_feature is not None
    assert size_feature.value == ["12pt"]

    # Get all features - should have 3 distinct features
    features = node.get_features()
    assert len(features) >= 3

    # Get features of type "style" - should get all 3
    style_features = node.get_features_of_type("style")
    assert len(style_features) == 3

    doc.close()
    print("✓ test_multiple_features_same_type_different_names passed")


if __name__ == "__main__":
    print("Running comprehensive feature append behavior tests...")

    try:
        test_feature_value_appends()
        test_feature_append_with_different_types()
        test_feature_stores_values_in_arrays()
        test_feature_persistence_through_save_load()
        test_multiple_features_same_type_different_names()

        print("\n✅ All comprehensive feature tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
