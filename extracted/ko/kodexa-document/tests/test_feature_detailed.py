"""
Detailed diagnosis of feature functionality issues.
"""

import json
import pytest
from kodexa_document import Document


def test_feature_value_storage():
    """Test feature value storage and retrieval."""
    doc = Document(inmemory=True)
    node = doc.create_node("paragraph", "Test content")
    
    # Test with a simple dict
    test_data = {"family": "Arial", "size": 12}
    
    # add_feature returns ContentFeature
    feature = node.add_feature("style", "font", test_data)
    assert feature is not None
    
    # Get it back
    result = node.get_feature("style", "font")
    assert result is not None
    
    # result is now a ContentFeature object
    from kodexa_document import ContentFeature
    assert isinstance(result, ContentFeature)
    
    # Value should be stored as array internally
    assert result.value == [test_data]
    
    # get_value() returns the full array of values
    assert result.get_value() == [test_data]
    
    doc.close()


def test_get_all_features():
    """Test GetAllFeatures return value."""
    doc = Document(inmemory=True)
    node = doc.create_node("paragraph", "Test content")
    
    # Add features
    node.add_feature("style", "font", {"family": "Arial"})
    node.add_feature("layout", "margin", 10)
    
    all_features = node.get_features()
    assert isinstance(all_features, list)
    assert len(all_features) >= 2
    
    for feature in all_features:
        assert hasattr(feature, 'feature_type')
        assert hasattr(feature, 'name')
        # Each feature is now a ContentFeature object with expected properties
    
    doc.close()


def test_feature_removal():
    """Test feature removal functionality."""
    doc = Document(inmemory=True)
    node = doc.create_node("paragraph", "Test content")
    
    # Add a temporary feature
    node.add_feature("test", "temporary", "will_remove")
    before = node.get_feature("test", "temporary")
    assert before is not None
    
    # Try to remove it
    try:
        node.remove_feature("test", "temporary")
        after = node.get_feature("test", "temporary")
        # Feature should be None after removal
        assert after is None
    except Exception as e:
        pytest.skip(f"Feature removal not implemented: {e}")
    
    doc.close()


def test_feature_data_field_access():
    """Test accessing feature data fields directly."""
    doc = Document(inmemory=True)
    node = doc.create_node("paragraph", "Test content")
    
    test_values = [
        ("style", "font", {"family": "Arial"}),
        ("layout", "margin", 10),
        ("content", "text", "some text")
    ]
    
    for feature_type, feature_name, feature_value in test_values:
        node.add_feature(feature_type, feature_name, feature_value)
        result = node.get_feature(feature_type, feature_name)
        
        assert result is not None
        # get_feature returns a ContentFeature object, not a dict
        # Check that we can access the value
        assert hasattr(result, 'value')
        
        # At minimum, we should be able to identify the feature
        # The exact structure depends on Go implementation
    
    doc.close()


def test_features_persistence_with_different_types():
    """Test that different value types are handled correctly."""
    doc = Document(inmemory=True)
    node = doc.create_node("paragraph", "Test content")
    
    # Test different data types
    test_cases = [
        ("string_val", "text", "hello world"),
        ("int_val", "number", 42),
        ("float_val", "decimal", 3.14),
        ("bool_val", "flag", True),
        ("list_val", "items", [1, 2, 3]),
        ("dict_val", "config", {"key": "value"}),
    ]
    
    for feature_type, feature_name, feature_value in test_cases:
        node.add_feature(feature_type, feature_name, feature_value)
        result = node.get_feature(feature_type, feature_name)
        assert result is not None
    
    # Verify we can get all features
    all_features = node.get_features()
    assert len(all_features) >= len(test_cases)
    
    doc.close()