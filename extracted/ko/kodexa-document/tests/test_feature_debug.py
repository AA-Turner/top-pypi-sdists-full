"""
Debug feature creation to understand what's happening.
"""

from kodexa_document import Document


def test_feature_creation():
    """Debug feature creation step by step."""
    doc = Document(inmemory=True)
    
    node = doc.create_node("paragraph", "Test content")
    assert node._handle is not None
    
    # Add first feature
    node.add_feature("style", "font", {"family": "Arial"})
    features = node.get_features()
    assert features is not None
    assert len(features) >= 1
    
    # Add second feature
    node.add_feature("style", "color", "blue")
    features = node.get_features()
    assert len(features) >= 2
    
    # Add third feature
    node.add_feature("layout", "margin", {"top": 10, "bottom": 10})
    features = node.get_features()
    assert len(features) >= 3
    
    # Verify feature structure - now returns ContentFeature objects
    for feature in features:
        assert hasattr(feature, 'feature_type')
        assert hasattr(feature, 'name')
        assert hasattr(feature, 'value')
        assert hasattr(feature, 'get_value')
        # ContentFeature objects have the expected properties
    
    doc.close()
