"""Tests for ContentNode spatial methods."""

import pytest
from kodexa_document import Document, ContentNode


def test_spatial_methods_with_bbox():
    """Test get_x, get_y, get_width, get_height with valid bbox."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set a bounding box using features [x1, y1, x2, y2]
    root.add_feature("spatial", "bbox", [10.0, 20.0, 110.0, 170.0])
    
    # Test get_x (should return x1)
    assert root.get_x() == 10.0
    
    # Test get_y (should return y1)
    assert root.get_y() == 20.0
    
    # Test get_width (should return x2 - x1)
    assert root.get_width() == 100.0  # 110 - 10
    
    # Test get_height (should return y2 - y1)
    assert root.get_height() == 150.0  # 170 - 20


def test_spatial_methods_without_bbox():
    """Test spatial methods return None when no bbox exists."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # No bbox set, all methods should return None
    assert root.get_x() is None
    assert root.get_y() is None
    assert root.get_width() is None
    assert root.get_height() is None


def test_spatial_methods_with_invalid_bbox():
    """Test that setting invalid bbox data raises errors."""
    from kodexa_document import DocumentError
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Test with bbox that's too short - should raise error
    with pytest.raises(DocumentError):
        root.add_feature("spatial", "bbox", [10.0, 20.0])  # Only 2 values

    # Test with non-list bbox - should raise error
    with pytest.raises(DocumentError):
        root.set_feature("spatial", "bbox", "invalid")

    # Test with None bbox - should raise error
    with pytest.raises(DocumentError):
        root.set_feature("spatial", "bbox", None)

    # No bbox set, so accessors should return None
    assert root.get_x() is None
    assert root.get_y() is None
    assert root.get_width() is None
    assert root.get_height() is None


def test_spatial_methods_with_string_numbers():
    """Test spatial methods handle string numbers in bbox."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set bbox with string numbers (sometimes happens in real data)
    root.add_feature("spatial", "bbox", ["10.5", "20.5", "110.5", "170.5"])
    
    # Should convert strings to floats
    assert root.get_x() == 10.5
    assert root.get_y() == 20.5
    assert root.get_width() == 100.0  # 110.5 - 10.5
    assert root.get_height() == 150.0  # 170.5 - 20.5


def test_spatial_methods_with_integer_bbox():
    """Test spatial methods work with integer bbox values."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set bbox with integers
    root.add_feature("spatial", "bbox", [10, 20, 110, 170])
    
    # Should work with integers and return floats
    assert root.get_x() == 10.0
    assert root.get_y() == 20.0
    assert root.get_width() == 100.0
    assert root.get_height() == 150.0


def test_spatial_methods_with_negative_coordinates():
    """Test spatial methods handle negative coordinates correctly."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Negative coordinates are valid in some coordinate systems
    root.add_feature("spatial", "bbox", [-10.0, -20.0, 50.0, 80.0])
    
    assert root.get_x() == -10.0
    assert root.get_y() == -20.0
    assert root.get_width() == 60.0  # 50 - (-10)
    assert root.get_height() == 100.0  # 80 - (-20)


def test_spatial_methods_with_zero_dimensions():
    """Test spatial methods handle zero-width or zero-height bbox."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Zero width (x1 == x2)
    root.add_feature("spatial", "bbox", [10.0, 20.0, 10.0, 50.0])
    assert root.get_x() == 10.0
    assert root.get_y() == 20.0
    assert root.get_width() == 0.0
    assert root.get_height() == 30.0
    
    # Zero height (y1 == y2)
    root.set_feature("spatial", "bbox", [10.0, 20.0, 50.0, 20.0])
    assert root.get_x() == 10.0
    assert root.get_y() == 20.0
    assert root.get_width() == 40.0
    assert root.get_height() == 0.0


def test_spatial_methods_on_child_nodes():
    """Test spatial methods work on child nodes."""
    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root
    
    # Create a child with bbox
    page = doc.create_node("page")
    page.add_feature("spatial", "bbox", [0.0, 0.0, 595.0, 842.0])  # A4 page
    root.add_child(page)
    
    # Create another child with different bbox
    text = doc.create_node("text")
    text.add_feature("spatial", "bbox", [100.0, 200.0, 300.0, 250.0])
    page.add_child(text)
    
    # Test page bbox
    assert page.get_x() == 0.0
    assert page.get_y() == 0.0
    assert page.get_width() == 595.0
    assert page.get_height() == 842.0
    
    # Test text bbox
    assert text.get_x() == 100.0
    assert text.get_y() == 200.0
    assert text.get_width() == 200.0  # 300 - 100
    assert text.get_height() == 50.0  # 250 - 200


def test_get_bbox():
    """Test get_bbox returns the full bbox array."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set bbox using feature
    root.add_feature("spatial", "bbox", [10.0, 20.0, 110.0, 170.0])
    
    # get_bbox should return the full array as floats
    bbox = root.get_bbox()
    assert bbox == [10.0, 20.0, 110.0, 170.0]
    assert all(isinstance(v, float) for v in bbox)


def test_get_bbox_without_bbox():
    """Test get_bbox returns None when no bbox exists."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    assert root.get_bbox() is None


def test_get_bbox_with_string_values():
    """Test get_bbox converts string values to floats."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set bbox with string values
    root.add_feature("spatial", "bbox", ["10.5", "20.5", "110.5", "170.5"])
    
    # Should return floats
    bbox = root.get_bbox()
    assert bbox == [10.5, 20.5, 110.5, 170.5]
    assert all(isinstance(v, float) for v in bbox)


def test_set_bbox():
    """Test set_bbox stores the bbox correctly."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set bbox using the method
    root.set_bbox([10.0, 20.0, 110.0, 170.0])
    
    # Verify it was stored
    bbox = root.get_bbox()
    assert bbox == [10.0, 20.0, 110.0, 170.0]
    
    # Also verify through individual accessors
    assert root.get_x() == 10.0
    assert root.get_y() == 20.0
    assert root.get_width() == 100.0
    assert root.get_height() == 150.0


def test_set_bbox_with_integers():
    """Test set_bbox converts integers to floats."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set bbox with integers
    root.set_bbox([10, 20, 110, 170])
    
    # Should be stored as floats
    bbox = root.get_bbox()
    assert bbox == [10.0, 20.0, 110.0, 170.0]
    assert all(isinstance(v, float) for v in bbox)


def test_set_bbox_overwrites_existing():
    """Test set_bbox overwrites an existing bbox."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set initial bbox
    root.set_bbox([10.0, 20.0, 110.0, 170.0])
    assert root.get_bbox() == [10.0, 20.0, 110.0, 170.0]
    
    # Overwrite with new bbox
    root.set_bbox([5.0, 15.0, 55.0, 85.0])
    assert root.get_bbox() == [5.0, 15.0, 55.0, 85.0]
    
    # Verify through accessors
    assert root.get_x() == 5.0
    assert root.get_y() == 15.0
    assert root.get_width() == 50.0
    assert root.get_height() == 70.0


def test_set_bbox_invalid_input():
    """Test set_bbox raises error for invalid input."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Too few values
    with pytest.raises(ValueError, match="must be a list/tuple of 4 values"):
        root.set_bbox([10.0, 20.0])
    
    # Too many values
    with pytest.raises(ValueError, match="must be a list/tuple of 4 values"):
        root.set_bbox([10.0, 20.0, 110.0, 170.0, 200.0])
    
    # Not a list/tuple
    with pytest.raises(ValueError, match="must be a list/tuple of 4 values"):
        root.set_bbox("invalid")
    
    # None
    with pytest.raises(ValueError, match="must be a list/tuple of 4 values"):
        root.set_bbox(None)


def test_set_bbox_with_negative_values():
    """Test set_bbox handles negative coordinates."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Negative coordinates are valid
    root.set_bbox([-10.0, -20.0, 50.0, 80.0])
    assert root.get_bbox() == [-10.0, -20.0, 50.0, 80.0]
    assert root.get_x() == -10.0
    assert root.get_y() == -20.0