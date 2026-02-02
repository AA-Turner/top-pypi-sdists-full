"""Tests for ContentNode content parts methods.

Content parts can be either strings or integers. Integer values represent
child node indices (for rollup operations where parent content references
child nodes).
"""

import pytest
from kodexa_document import Document, ContentNode


def test_get_content_parts_empty():
    """Test get_content_parts returns empty list for node with no parts."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Set empty parts explicitly
    root.set_content_parts([])

    parts = root.get_content_parts()
    assert parts == []


def test_get_content_parts_single():
    """Test get_content_parts returns single part."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Set single part
    root.set_content_parts(["Hello World"])

    parts = root.get_content_parts()
    assert parts == ["Hello World"]


def test_content_parts_preserved():
    """Test that content parts are preserved, not joined."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Set multiple parts
    parts = ["Part 1", " Part 2", " Part 3"]
    root.set_content_parts(parts)

    # Get parts back - should be preserved separately
    retrieved_parts = root.get_content_parts()
    assert retrieved_parts == ["Part 1", " Part 2", " Part 3"]
    assert len(retrieved_parts) == 3


def test_set_content_parts_empty_list():
    """Test setting empty content parts list."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Set some content first
    root.set_content_parts(["Initial content"])

    # Set empty parts
    root.set_content_parts([])

    # Should clear content parts
    assert root.get_content_parts() == []


def test_set_content_parts_single():
    """Test setting a single content part."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Set single part
    root.set_content_parts(["Single part"])

    # Should return single part
    assert root.get_content_parts() == ["Single part"]


def test_set_content_parts_invalid_type():
    """Test set_content_parts raises error for invalid type."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Should raise ValueError for non-list
    with pytest.raises(ValueError, match="must be a list"):
        root.set_content_parts("not a list")

    with pytest.raises(ValueError, match="must be a list"):
        root.set_content_parts(None)


def test_content_parts_with_integers():
    """Test content parts with integer child node references."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Set parts with integers (child node references)
    parts = ["Prefix: ", 0, " Middle: ", 1, " Suffix"]
    root.set_content_parts(parts)

    # Get parts back - should preserve types
    retrieved_parts = root.get_content_parts()
    assert retrieved_parts == ["Prefix: ", 0, " Middle: ", 1, " Suffix"]
    assert len(retrieved_parts) == 5
    assert isinstance(retrieved_parts[0], str)
    assert isinstance(retrieved_parts[1], int)
    assert isinstance(retrieved_parts[2], str)
    assert isinstance(retrieved_parts[3], int)
    assert isinstance(retrieved_parts[4], str)


def test_content_parts_invalid_part_type():
    """Test set_content_parts raises error for invalid part types."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Should raise ValueError for invalid part types (not string or int)
    with pytest.raises(ValueError, match="must be a string or integer"):
        root.set_content_parts(["valid", 1.5])  # float not allowed

    with pytest.raises(ValueError, match="must be a string or integer"):
        root.set_content_parts(["valid", {"key": "value"}])  # dict not allowed


def test_content_parts_with_special_characters():
    """Test content parts with special characters are preserved."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Set parts with special characters
    parts = ["Part with 'quotes'", 'Part with "double quotes"', "Part with\nnewline"]
    root.set_content_parts(parts)

    # Parts should be preserved separately with special characters intact
    retrieved_parts = root.get_content_parts()
    assert retrieved_parts == ["Part with 'quotes'", 'Part with "double quotes"', "Part with\nnewline"]


def test_content_parts_with_unicode():
    """Test content parts with Unicode characters are preserved."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Set parts with Unicode
    parts = ["Hello 世界", "Emoji 🌍", "Math ∑∏∫"]
    root.set_content_parts(parts)

    # Parts should be preserved separately with Unicode intact
    retrieved_parts = root.get_content_parts()
    assert retrieved_parts == ["Hello 世界", "Emoji 🌍", "Math ∑∏∫"]


def test_content_parts_on_child_nodes():
    """Test content parts work on child nodes."""
    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create child with content parts
    child = doc.create_node("paragraph")
    root.add_child(child)
    child.set_content_parts(["First sentence.", " Second sentence."])

    # Verify child's content parts are preserved
    assert child.get_content_parts() == ["First sentence.", " Second sentence."]


def test_content_parts_empty_strings():
    """Test content parts with empty strings are preserved."""
    doc = Document(inmemory=True)
    root = doc.create_node("page")
    doc.content_node = root

    # Set parts with empty strings
    parts = ["", "Non-empty", "", "Another", ""]
    root.set_content_parts(parts)

    # Empty strings should be preserved
    retrieved_parts = root.get_content_parts()
    assert retrieved_parts == ["", "Non-empty", "", "Another", ""]


def test_content_parts_rollup_with_child_references():
    """Test rollup operation with child node references."""
    doc = Document(inmemory=True)
    root = doc.create_node("paragraph")
    doc.content_node = root

    # Simulate rollup by setting parts with child node references (integers)
    # This matches kodexa/kodexa behavior where parent content references children
    rolled_up_parts = [
        "The London-headquartered bank is a heavyweight component of the ",
        0,  # Reference to child node 0
        ". HSBC shares in Hong Kong closed 2.78% lower."
    ]
    root.set_content_parts(rolled_up_parts)

    # Parts should be preserved with mixed types
    retrieved_parts = root.get_content_parts()
    assert len(retrieved_parts) == 3
    assert retrieved_parts[0] == "The London-headquartered bank is a heavyweight component of the "
    assert retrieved_parts[1] == 0  # integer preserved
    assert isinstance(retrieved_parts[1], int)
    assert retrieved_parts[2] == ". HSBC shares in Hong Kong closed 2.78% lower."


def test_content_parts_multiple_child_references():
    """Test content parts with multiple child node references."""
    doc = Document(inmemory=True)
    root = doc.create_node("table")
    doc.content_node = root

    # Simulate table cell references
    parts = [0, " | ", 1, " | ", 2]  # Three cell references with separators
    root.set_content_parts(parts)

    # Parts should be preserved
    retrieved_parts = root.get_content_parts()
    assert retrieved_parts == [0, " | ", 1, " | ", 2]
    assert isinstance(retrieved_parts[0], int)
    assert isinstance(retrieved_parts[2], int)
    assert isinstance(retrieved_parts[4], int)