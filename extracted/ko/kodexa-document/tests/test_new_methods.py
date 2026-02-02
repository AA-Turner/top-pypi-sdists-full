#!/usr/bin/env python3
"""
Test script for new legacy_python compatibility methods:
- Document.get_all_tags()
- Document.get_nodes_by_type()
"""

import sys
from pathlib import Path

# Add the kodexa_document module to the path
sys.path.insert(0, str(Path(__file__).parent / "kodexa_document"))

from kodexa_document import Document

def test_get_all_tags():
    """Test Document.get_all_tags() method."""
    print("Testing Document.get_all_tags()...")
    
    doc = Document(inmemory=True)
    
    # Create nodes with various tags
    root = doc.create_node("document")
    doc.content_node = root
    
    para1 = doc.create_node("paragraph", "First paragraph")
    para2 = doc.create_node("paragraph", "Second paragraph") 
    section1 = doc.create_node("section", "A section")
    
    root.add_child(para1)
    root.add_child(para2)
    root.add_child(section1)
    
    # Tag the nodes
    para1.tag("important")
    para1.tag("reviewed")
    para2.tag("draft")
    section1.tag("important")
    section1.tag("header")
    
    # Test get_all_tags
    all_tags = doc.get_all_tags()
    print(f"All tags: {all_tags}")
    
    # Verify we have the expected tags
    expected_tags = {"important", "reviewed", "draft", "header"}
    actual_tags = set(all_tags)
    
    assert expected_tags.issubset(actual_tags), f"Expected {expected_tags} to be subset of {actual_tags}"
    print("✓ get_all_tags() works correctly")
    
    doc.close()


def test_get_nodes_by_type():
    """Test Document.get_nodes_by_type() method."""
    print("\nTesting Document.get_nodes_by_type()...")
    
    doc = Document(inmemory=True)
    
    # Create nodes of different types
    root = doc.create_node("document")
    doc.content_node = root
    
    para1 = doc.create_node("paragraph", "First paragraph")
    para2 = doc.create_node("paragraph", "Second paragraph")
    section1 = doc.create_node("section", "A section")
    header1 = doc.create_node("header", "A header")
    
    root.add_child(para1)
    root.add_child(para2)
    root.add_child(section1)
    root.add_child(header1)
    
    # Test get_nodes_by_type for paragraphs
    paragraphs = doc.get_nodes_by_type("paragraph")
    print(f"Found {len(paragraphs)} paragraphs")
    
    assert len(paragraphs) == 2, f"Expected 2 paragraphs, got {len(paragraphs)}"
    
    # Verify they are the right nodes
    para_contents = [node.content for node in paragraphs]
    assert "First paragraph" in para_contents
    assert "Second paragraph" in para_contents
    
    # Test get_nodes_by_type for sections
    sections = doc.get_nodes_by_type("section")
    print(f"Found {len(sections)} sections")
    
    assert len(sections) == 1, f"Expected 1 section, got {len(sections)}"
    assert sections[0].content == "A section"
    
    # Test get_nodes_by_type for headers
    headers = doc.get_nodes_by_type("header")
    print(f"Found {len(headers)} headers")
    
    assert len(headers) == 1, f"Expected 1 header, got {len(headers)}"
    assert headers[0].content == "A header"
    
    # Test get_nodes_by_type for non-existent type
    nonexistent = doc.get_nodes_by_type("nonexistent")
    print(f"Found {len(nonexistent)} nonexistent nodes")
    
    assert len(nonexistent) == 0, f"Expected 0 nonexistent nodes, got {len(nonexistent)}"
    
    print("✓ get_nodes_by_type() works correctly")
    
    doc.close()


if __name__ == "__main__":
    try:
        test_get_all_tags()
        test_get_nodes_by_type()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)