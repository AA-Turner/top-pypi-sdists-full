"""
Debug remaining feature test failures.
"""

import json
import tempfile
import pytest
from kodexa_document import Document, ContentNode


def test_get_all_features():
    """Debug test_get_all_features failure."""
    doc = Document(inmemory=True)
    
    try:
        node = doc.create_node("paragraph", "Test content")
        
        # Add multiple features
        node.add_feature("style", "font", {"family": "Arial"})
        node.add_feature("style", "color", "blue")
        node.add_feature("layout", "margin", {"top": 10, "bottom": 10})
        
        # Get all features
        features = node.get_features()
        assert features is not None, "Features should not be None"
        assert isinstance(features, list), f"Features should be list, got {type(features)}"
        assert len(features) >= 3, f"Expected at least 3 features, got {len(features)}"
        
    finally:
        doc.close()


def test_get_features_of_type():
    """Debug test_get_features_of_type failure."""
    doc = Document(inmemory=True)
    
    try:
        node = doc.create_node("paragraph", "Test content")
        
        # Add features of different types
        node.add_feature("style", "font", "Arial")
        node.add_feature("style", "color", "blue")
        node.add_feature("layout", "margin", 10)
        
        # Get only style features
        style_features = node.get_features_of_type("style")
        assert style_features is not None, "Style features should not be None"
        assert len(style_features) == 2, f"Expected 2 style features, got {len(style_features)}"
        
        # Get only layout features
        layout_features = node.get_features_of_type("layout")
        assert layout_features is not None, "Layout features should not be None"
        assert len(layout_features) == 1, f"Expected 1 layout feature, got {len(layout_features)}"
        
    finally:
        doc.close()


def test_tag_persistence():
    """Debug test_tag_persistence failure."""
    import os

    # Create document and use auto-created root node
    doc1 = Document(inmemory=True)
    root = doc1.content_node
    root.content = "Root"

    child = doc1.create_node("paragraph", "Tagged paragraph")
    root.add_child(child)
    
    # Add tags
    child.tag("important", confidence=0.9, value="high")
    child.tag("category/business")
    
    initial_tags = child.get_tags()
    assert initial_tags is not None, "Tags should not be None before save"
    
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
        assert loaded_root is not None, "Loaded root should not be None"
        
        loaded_children = loaded_root.get_children()
        assert len(loaded_children) == 1, f"Expected 1 child, got {len(loaded_children)}"
        
        loaded_child = loaded_children[0]
        assert loaded_child.content == "Tagged paragraph", "Child content should match"
        
        # Check tags persisted
        has_important = loaded_child.has_tag("important")
        has_category = loaded_child.has_tag("category/business")
        
        assert has_important, "'important' tag not persisted"
        assert has_category, "'category/business' tag not persisted"
        
        doc2.close()
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_node_with_complex_metadata():
    """Debug test_node_with_complex_metadata failure."""
    doc = Document(inmemory=True)
    
    try:
        node = doc.create_node("paragraph", "Complex node")
        
        # Add multiple features
        node.add_feature("style", "font", {"family": "Arial", "size": 12})
        node.add_feature("style", "color", "#FF0000")
        node.add_feature("layout", "position", {"x": 100, "y": 200})
        
        # Add multiple tags
        node.tag("important", confidence=0.95)
        node.tag("reviewed", value="approved")
        node.tag("category/technical")
        
        # Verify all metadata
        features = node.get_features()
        tags = node.get_tags()
        
        assert features is not None, "Features should not be None"
        assert tags is not None, "Tags should not be None"
        
        assert len(features) >= 3, f"Expected at least 3 features, got {len(features)}"
        assert len(tags) >= 3, f"Expected at least 3 tags, got {len(tags)}"
        
        has_important = node.has_tag("important")
        font_feature = node.get_feature("style", "font")
        
        assert has_important, "Should have 'important' tag"
        assert font_feature is not None, "Should have font feature"
        
    finally:
        doc.close()


# Tests are now pytest-compatible - no main execution needed