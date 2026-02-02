"""Tests for ContentNode rotation methods."""

import pytest
from kodexa_document import Document, ContentNode


def test_get_rotate_without_rotation():
    """Test get_rotate returns None when no rotation is set."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    assert root.get_rotate() is None


def test_set_and_get_rotate():
    """Test set_rotate stores rotation correctly."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set rotation
    root.set_rotate(90.0)
    
    # Get rotation
    assert root.get_rotate() == 90.0


def test_set_rotate_with_integer():
    """Test set_rotate converts integer to float."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set with integer
    root.set_rotate(180)
    
    # Should return as float
    assert root.get_rotate() == 180.0
    assert isinstance(root.get_rotate(), float)


def test_set_rotate_with_string():
    """Test set_rotate converts string to float."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set with string
    root.set_rotate("270.5")
    
    # Should return as float
    assert root.get_rotate() == 270.5
    assert isinstance(root.get_rotate(), float)


def test_set_rotate_negative_value():
    """Test set_rotate handles negative rotation."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Negative rotation is valid
    root.set_rotate(-45.0)
    assert root.get_rotate() == -45.0


def test_set_rotate_large_value():
    """Test set_rotate handles rotations > 360."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Rotation > 360 is valid (no normalization)
    root.set_rotate(720.0)
    assert root.get_rotate() == 720.0


def test_set_rotate_zero():
    """Test set_rotate with zero rotation."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    root.set_rotate(0.0)
    assert root.get_rotate() == 0.0


def test_set_rotate_multiple_times():
    """Test set_rotate behavior when called multiple times."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set first rotation
    root.set_rotate(90.0)
    assert root.get_rotate() == 90.0
    
    # Set second rotation - using set_feature, this replaces the previous value
    root.set_rotate(180.0)
    
    # Should only have the latest value
    assert root.get_rotate() == 180.0


def test_rotate_with_bbox():
    """Test rotation can coexist with bbox."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set both bbox and rotation
    root.set_bbox([10.0, 20.0, 110.0, 170.0])
    root.set_rotate(45.0)
    
    # Both should be accessible
    assert root.get_bbox() == [10.0, 20.0, 110.0, 170.0]
    assert root.get_rotate() == 45.0
    
    # And individual bbox accessors should still work
    assert root.get_x() == 10.0
    assert root.get_y() == 20.0


def test_rotate_on_child_nodes():
    """Test rotation works on child nodes."""
    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root
    
    # Create children with different rotations
    page1 = doc.create_node("page")
    page1.set_rotate(0.0)
    root.add_child(page1)
    
    page2 = doc.create_node("page")
    page2.set_rotate(90.0)
    root.add_child(page2)
    
    text = doc.create_node("text")
    text.set_rotate(45.0)
    page1.add_child(text)
    
    # Verify each node's rotation
    assert page1.get_rotate() == 0.0
    assert page2.get_rotate() == 90.0
    assert text.get_rotate() == 45.0
    assert root.get_rotate() is None  # Root has no rotation


def test_get_rotate_with_non_numeric_stored_value():
    """Test get_rotate handles non-numeric values gracefully."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Manually set a non-numeric value (shouldn't happen normally)
    root.add_feature("spatial", "rotate", "not-a-number")
    
    # Should raise an error when trying to convert
    with pytest.raises(ValueError):
        root.get_rotate()


def test_rotate_decimal_precision():
    """Test rotation maintains decimal precision."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root
    
    # Set rotation with many decimals
    root.set_rotate(123.456789)
    
    # Should maintain precision
    assert root.get_rotate() == 123.456789