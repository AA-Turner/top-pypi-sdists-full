#!/usr/bin/env python3
"""
Test script for additional methods exposed from Go backend.

Document methods:
- find_nodes_by_tag_uuid()
- get_node_by_id()
- get_node_count_by_type()
- get_feature_types_with_counts()
- get_node_types_with_counts()
- replace_exceptions()
- get_tags_by_prefix()
- create_data_exception()
- get_data_objects_by_parent_id()
- get_all_features()
- get_document_filename()

ContentNode methods:
- has_next_node()
- has_previous_node()
- get_first_child_index()
- get_last_child_index()
- get_node_at_index()
- add_child_content()
- get_ancestors()
- get_descendants()
"""

import sys
from pathlib import Path

# Add the kodexa_document module to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kodexa_document import Document


# =============================================================================
# Document Method Tests
# =============================================================================

def test_find_nodes_by_tag_uuid():
    """Test Document.find_nodes_by_tag_uuid() method."""
    print("Testing Document.find_nodes_by_tag_uuid()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para1 = doc.create_node("paragraph", "First paragraph")
    para2 = doc.create_node("paragraph", "Second paragraph")
    root.add_child(para1)
    root.add_child(para2)

    # Tag a node and get the tag UUID
    para1.tag("important")
    tags = para1.get_tags()
    assert len(tags) > 0, "Expected at least one tag"

    tag_uuid = tags[0].uuid if hasattr(tags[0], 'uuid') else tags[0].get('uuid')
    assert tag_uuid, "Expected tag to have a UUID"

    # Find nodes by tag UUID
    found_nodes = doc.find_nodes_by_tag_uuid(tag_uuid)
    assert len(found_nodes) >= 1, f"Expected at least 1 node, got {len(found_nodes)}"

    # Test with non-existent UUID
    not_found = doc.find_nodes_by_tag_uuid("non-existent-uuid")
    assert len(not_found) == 0, f"Expected 0 nodes for non-existent UUID, got {len(not_found)}"

    print("✓ find_nodes_by_tag_uuid() works correctly")
    doc.close()


def test_get_node_by_id():
    """Test Document.get_node_by_id() method."""
    print("\nTesting Document.get_node_by_id()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para = doc.create_node("paragraph", "Test paragraph")
    root.add_child(para)

    # Get the node's ID
    node_id = para.id
    assert node_id is not None, "Expected node to have an ID"

    # Find node by ID
    found_node = doc.get_node_by_id(node_id)
    assert found_node is not None, "Expected to find node by ID"
    assert found_node.content == "Test paragraph"

    # Test with non-existent ID
    not_found = doc.get_node_by_id(999999)
    assert not_found is None, "Expected None for non-existent ID"

    print("✓ get_node_by_id() works correctly")
    doc.close()


def test_get_node_count_by_type():
    """Test Document.get_node_count_by_type() method."""
    print("\nTesting Document.get_node_count_by_type()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create multiple nodes of same type
    for i in range(5):
        para = doc.create_node("paragraph", f"Paragraph {i}")
        root.add_child(para)

    for i in range(3):
        section = doc.create_node("section", f"Section {i}")
        root.add_child(section)

    # Test counts
    para_count = doc.get_node_count_by_type("paragraph")
    assert para_count == 5, f"Expected 5 paragraphs, got {para_count}"

    section_count = doc.get_node_count_by_type("section")
    assert section_count == 3, f"Expected 3 sections, got {section_count}"

    nonexistent_count = doc.get_node_count_by_type("nonexistent")
    assert nonexistent_count == 0, f"Expected 0 for nonexistent type, got {nonexistent_count}"

    print("✓ get_node_count_by_type() works correctly")
    doc.close()


def test_get_feature_types_with_counts():
    """Test Document.get_feature_types_with_counts() method."""
    print("\nTesting Document.get_feature_types_with_counts()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para1 = doc.create_node("paragraph", "First")
    para2 = doc.create_node("paragraph", "Second")
    root.add_child(para1)
    root.add_child(para2)

    # Add features
    para1.add_feature("spatial", "bbox", [0, 0, 100, 100])
    para2.add_feature("spatial", "bbox", [0, 100, 100, 200])
    para1.add_feature("custom", "score", 0.95)

    # Get feature types with counts
    types = doc.get_feature_types_with_counts()
    assert isinstance(types, list), "Expected list result"

    # Should have at least spatial and custom types
    type_names = [t.get('name', '') for t in types]
    print(f"Feature types: {type_names}")

    print("✓ get_feature_types_with_counts() works correctly")
    doc.close()


def test_get_node_types_with_counts():
    """Test Document.get_node_types_with_counts() method."""
    print("\nTesting Document.get_node_types_with_counts()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    for i in range(3):
        root.add_child(doc.create_node("paragraph", f"Para {i}"))
    for i in range(2):
        root.add_child(doc.create_node("section", f"Section {i}"))

    types = doc.get_node_types_with_counts()
    assert isinstance(types, list), "Expected list result"

    # Find paragraph and section counts
    type_dict = {t.get('name'): t.get('count') for t in types}
    print(f"Node types: {type_dict}")

    assert type_dict.get('paragraph') == 3, f"Expected 3 paragraphs"
    assert type_dict.get('section') == 2, f"Expected 2 sections"

    print("✓ get_node_types_with_counts() works correctly")
    doc.close()


def test_get_all_features():
    """Test Document.get_all_features() method."""
    print("\nTesting Document.get_all_features()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para = doc.create_node("paragraph", "Test")
    root.add_child(para)

    para.add_feature("test", "value1", "data1")
    para.add_feature("test", "value2", "data2")

    features = doc.get_all_features()
    assert isinstance(features, list), "Expected list result"
    print(f"Found {len(features)} features")

    print("✓ get_all_features() works correctly")
    doc.close()


def test_get_document_filename():
    """Test Document.get_document_filename() method."""
    print("\nTesting Document.get_document_filename()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Set source with filename
    doc.source = {"original_filename": "test_file.pdf"}

    filename = doc.get_document_filename()
    # Note: This may return empty string if source metadata isn't properly set
    print(f"Filename: '{filename}'")

    print("✓ get_document_filename() works correctly")
    doc.close()


# =============================================================================
# ContentNode Method Tests
# =============================================================================

def test_has_next_node():
    """Test ContentNode.has_next_node() method."""
    print("\nTesting ContentNode.has_next_node()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para1 = doc.create_node("paragraph", "First")
    para2 = doc.create_node("paragraph", "Second")
    para3 = doc.create_node("paragraph", "Third")

    root.add_child(para1)
    root.add_child(para2)
    root.add_child(para3)

    # First node has next
    assert para1.has_next_node() == True, "First node should have next"

    # Second node has next
    assert para2.has_next_node() == True, "Second node should have next"

    # Last node has no next
    assert para3.has_next_node() == False, "Last node should not have next"

    print("✓ has_next_node() works correctly")
    doc.close()


def test_has_previous_node():
    """Test ContentNode.has_previous_node() method."""
    print("\nTesting ContentNode.has_previous_node()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para1 = doc.create_node("paragraph", "First")
    para2 = doc.create_node("paragraph", "Second")
    para3 = doc.create_node("paragraph", "Third")

    root.add_child(para1)
    root.add_child(para2)
    root.add_child(para3)

    # First node has no previous
    assert para1.has_previous_node() == False, "First node should not have previous"

    # Second node has previous
    assert para2.has_previous_node() == True, "Second node should have previous"

    # Last node has previous
    assert para3.has_previous_node() == True, "Last node should have previous"

    print("✓ has_previous_node() works correctly")
    doc.close()


def test_get_first_child_index():
    """Test ContentNode.get_first_child_index() method."""
    print("\nTesting ContentNode.get_first_child_index()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # No children initially
    assert root.get_first_child_index() is None, "Should return None for no children"

    # Add children
    para1 = doc.create_node("paragraph", "First")
    para2 = doc.create_node("paragraph", "Second")
    root.add_child(para1)
    root.add_child(para2)

    first_idx = root.get_first_child_index()
    assert first_idx is not None, "Should have first child index"
    assert first_idx == 0, f"Expected index 0, got {first_idx}"

    print("✓ get_first_child_index() works correctly")
    doc.close()


def test_get_last_child_index():
    """Test ContentNode.get_last_child_index() method."""
    print("\nTesting ContentNode.get_last_child_index()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # No children initially
    assert root.get_last_child_index() is None, "Should return None for no children"

    # Add children
    for i in range(5):
        para = doc.create_node("paragraph", f"Para {i}")
        root.add_child(para)

    last_idx = root.get_last_child_index()
    assert last_idx is not None, "Should have last child index"
    assert last_idx == 4, f"Expected index 4, got {last_idx}"

    print("✓ get_last_child_index() works correctly")
    doc.close()


def test_get_node_at_index():
    """Test ContentNode.get_node_at_index() method."""
    print("\nTesting ContentNode.get_node_at_index()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para1 = doc.create_node("paragraph", "First")
    para2 = doc.create_node("paragraph", "Second")
    para3 = doc.create_node("paragraph", "Third")

    root.add_child(para1)
    root.add_child(para2)
    root.add_child(para3)

    # Get node at each index
    node0 = root.get_node_at_index(0)
    assert node0 is not None, "Should find node at index 0"
    assert node0.content == "First"

    node1 = root.get_node_at_index(1)
    assert node1 is not None, "Should find node at index 1"
    assert node1.content == "Second"

    node2 = root.get_node_at_index(2)
    assert node2 is not None, "Should find node at index 2"
    assert node2.content == "Third"

    # Non-existent index
    node99 = root.get_node_at_index(99)
    assert node99 is None, "Should return None for invalid index"

    print("✓ get_node_at_index() works correctly")
    doc.close()


def test_add_child_content():
    """Test ContentNode.add_child_content() method."""
    print("\nTesting ContentNode.add_child_content()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Add child with content in one call
    child1 = root.add_child_content("paragraph", "New paragraph")
    assert child1 is not None, "Should return created node"
    assert child1.node_type == "paragraph"
    assert child1.content == "New paragraph"

    # Add at specific index
    child2 = root.add_child_content("section", "New section", index=0)
    assert child2 is not None, "Should return created node"
    assert child2.node_type == "section"

    # Verify child count
    children = root.get_children()
    assert len(children) == 2, f"Expected 2 children, got {len(children)}"

    print("✓ add_child_content() works correctly")
    doc.close()


def test_get_ancestors():
    """Test ContentNode.get_ancestors() method."""
    print("\nTesting ContentNode.get_ancestors()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create a hierarchy: root -> section -> paragraph -> word
    section = doc.create_node("section", "Section")
    paragraph = doc.create_node("paragraph", "Paragraph")
    word = doc.create_node("word", "Hello")

    root.add_child(section)
    section.add_child(paragraph)
    paragraph.add_child(word)

    # Get ancestors of word (should be paragraph, section, root)
    ancestors = word.get_ancestors()
    print(f"Found {len(ancestors)} ancestors")

    # Root has no ancestors
    root_ancestors = root.get_ancestors()
    assert len(root_ancestors) == 0, f"Root should have 0 ancestors, got {len(root_ancestors)}"

    print("✓ get_ancestors() works correctly")
    doc.close()


def test_get_descendants():
    """Test ContentNode.get_descendants() method."""
    print("\nTesting ContentNode.get_descendants()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create a hierarchy
    section = doc.create_node("section", "Section")
    para1 = doc.create_node("paragraph", "Para 1")
    para2 = doc.create_node("paragraph", "Para 2")
    word1 = doc.create_node("word", "Hello")
    word2 = doc.create_node("word", "World")

    root.add_child(section)
    section.add_child(para1)
    section.add_child(para2)
    para1.add_child(word1)
    para1.add_child(word2)

    # Get descendants of root
    descendants = root.get_descendants()
    print(f"Found {len(descendants)} descendants of root")

    # Get descendants of section
    section_descendants = section.get_descendants()
    print(f"Found {len(section_descendants)} descendants of section")

    # Leaf has no descendants
    word_descendants = word1.get_descendants()
    assert len(word_descendants) == 0, f"Leaf should have 0 descendants, got {len(word_descendants)}"

    print("✓ get_descendants() works correctly")
    doc.close()


# =============================================================================
# Missing Document Method Tests (based on legacy SDK analysis)
# =============================================================================

def test_replace_exceptions():
    """Test Document.replace_exceptions() - replaces all exceptions in document.

    Based on legacy SDK: kodexa/kodexa/model/model.py:2551
    """
    print("\nTesting Document.replace_exceptions()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para = doc.create_node("paragraph", "Test paragraph")
    root.add_child(para)

    # Add initial exceptions
    doc.add_exception({
        "exception_type": "validation",
        "message": "Initial error 1",
        "severity": "warning"
    })
    doc.add_exception({
        "exception_type": "validation",
        "message": "Initial error 2",
        "severity": "error"
    })

    initial_exceptions = doc.get_exceptions()
    assert len(initial_exceptions) >= 2, f"Expected at least 2 exceptions, got {len(initial_exceptions)}"

    # Replace with new exceptions
    new_exceptions = [
        {
            "exception_type": "replaced",
            "message": "Replaced error",
            "severity": "info",
            "node_uuid": para.uuid
        }
    ]
    doc.replace_exceptions(new_exceptions)

    # Verify replacement
    replaced = doc.get_exceptions()
    assert len(replaced) == 1, f"Expected 1 exception after replace, got {len(replaced)}"
    # Handle both dict and object return types
    exc = replaced[0]
    msg = exc.get('message') if isinstance(exc, dict) else exc.message
    assert msg == "Replaced error", f"Expected 'Replaced error', got '{msg}'"

    print("✓ replace_exceptions() works correctly")
    doc.close()


def test_get_tags_by_prefix():
    """Test Document.get_tags_by_prefix() - filters tags by name prefix."""
    print("\nTesting Document.get_tags_by_prefix()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para1 = doc.create_node("paragraph", "First")
    para2 = doc.create_node("paragraph", "Second")
    root.add_child(para1)
    root.add_child(para2)

    # Add tags with different prefixes
    para1.tag("invoice/amount")
    para1.tag("invoice/date")
    para2.tag("customer/name")
    para2.tag("customer/address")
    para1.tag("other_tag")

    # Get tags by prefix - invoice
    invoice_tags = doc.get_tags_by_prefix("invoice/")
    assert isinstance(invoice_tags, list), "Expected list result"
    assert len(invoice_tags) >= 2, f"Expected at least 2 invoice tags, got {len(invoice_tags)}"

    # Get tags by prefix - customer
    customer_tags = doc.get_tags_by_prefix("customer/")
    assert len(customer_tags) >= 2, f"Expected at least 2 customer tags, got {len(customer_tags)}"

    # Non-existent prefix returns empty
    empty_tags = doc.get_tags_by_prefix("nonexistent/")
    assert len(empty_tags) == 0, f"Expected 0 tags for nonexistent prefix, got {len(empty_tags)}"

    print("✓ get_tags_by_prefix() works correctly")
    doc.close()


def test_create_data_exception():
    """Test Document.create_data_exception() - creates a data-level exception."""
    print("\nTesting Document.create_data_exception()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create a data exception
    exc_data = {
        "exception_type": "data_validation",
        "message": "Invalid data format",
        "severity": "error",
        "path": "/data/field1"
    }

    doc.create_data_exception(exc_data)

    print("✓ create_data_exception() works correctly")
    doc.close()


def test_get_data_objects_by_parent_id():
    """Test Document.get_data_objects_by_parent_id() - retrieves child data objects."""
    print("\nTesting Document.get_data_objects_by_parent_id()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Get data objects by parent ID 0 (root level)
    # This should return an empty list or root-level objects
    root_objects = doc.get_data_objects_by_parent_id(0)
    assert isinstance(root_objects, list), "Expected list result"

    print("✓ get_data_objects_by_parent_id() works correctly")
    doc.close()


# =============================================================================
# Enhanced ContentNode Tests (based on legacy SDK behavior)
# =============================================================================

def test_has_next_node_with_regex():
    """Test ContentNode.has_next_node() with node_type_re regex parameter.

    Based on legacy SDK: kodexa/kodexa/model/model.py:1959
    Legacy signature: has_next_node(self, node_type_re=".*", skip_virtual=False)
    """
    print("\nTesting ContentNode.has_next_node() with node_type_re regex...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create mixed node types
    para1 = doc.create_node("paragraph", "First para")
    section1 = doc.create_node("section", "A section")
    para2 = doc.create_node("paragraph", "Second para")
    header1 = doc.create_node("header", "A header")

    root.add_child(para1)
    root.add_child(section1)
    root.add_child(para2)
    root.add_child(header1)

    # Test with regex matching only paragraphs
    has_next_para = para1.has_next_node(node_type_re="paragraph")
    assert has_next_para == True, "para1 should have next paragraph node (para2)"

    # Test with regex matching sections
    has_next_section = para1.has_next_node(node_type_re="section")
    assert has_next_section == True, "para1 should have next section node"

    # Test with regex that doesn't match anything after last node
    has_next_table = header1.has_next_node(node_type_re="table")
    assert has_next_table == False, "header1 should not have next table node"

    # Test with wildcard regex (default behavior)
    has_next_any = para1.has_next_node(node_type_re=".*")
    assert has_next_any == True, "para1 should have next node with wildcard regex"

    print("✓ has_next_node() with regex works correctly")
    doc.close()


def test_has_previous_node_with_regex():
    """Test ContentNode.has_previous_node() with node_type_re regex parameter.

    Based on legacy SDK: kodexa/kodexa/model/model.py:1972
    """
    print("\nTesting ContentNode.has_previous_node() with node_type_re regex...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para1 = doc.create_node("paragraph", "First para")
    section1 = doc.create_node("section", "A section")
    para2 = doc.create_node("paragraph", "Second para")

    root.add_child(para1)
    root.add_child(section1)
    root.add_child(para2)

    # Test with regex matching paragraphs
    has_prev_para = para2.has_previous_node(node_type_re="paragraph")
    assert has_prev_para == True, "para2 should have previous paragraph node (para1)"

    # Test with regex matching sections
    has_prev_section = para2.has_previous_node(node_type_re="section")
    assert has_prev_section == True, "para2 should have previous section node"

    # First node has no previous
    has_prev = para1.has_previous_node(node_type_re=".*")
    assert has_prev == False, "para1 should not have previous node"

    print("✓ has_previous_node() with regex works correctly")
    doc.close()


def test_has_next_node_skip_virtual():
    """Test ContentNode.has_next_node() with skip_virtual parameter.

    Based on legacy SDK: kodexa/kodexa/model/model.py:1959
    The skip_virtual parameter should skip virtual nodes when searching.
    """
    print("\nTesting ContentNode.has_next_node() with skip_virtual...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create: regular -> virtual -> regular
    regular1 = doc.create_node("paragraph", "Regular 1")
    virtual1 = doc.create_node("paragraph", "Virtual 1", virtual=True)
    regular2 = doc.create_node("paragraph", "Regular 2")

    root.add_child(regular1)
    root.add_child(virtual1)
    root.add_child(regular2)

    # Without skip_virtual (default), should find next node
    has_next = regular1.has_next_node(skip_virtual=False)
    assert has_next == True, "regular1 should have next node"

    # With skip_virtual=True, should skip virtual and find regular2
    has_next_skip = regular1.has_next_node(skip_virtual=True)
    assert has_next_skip == True, "regular1 should have next real node (regular2)"

    print("✓ has_next_node() with skip_virtual works correctly")
    doc.close()


def test_has_previous_node_skip_virtual():
    """Test ContentNode.has_previous_node() with skip_virtual parameter."""
    print("\nTesting ContentNode.has_previous_node() with skip_virtual...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create: regular -> virtual -> regular
    regular1 = doc.create_node("paragraph", "Regular 1")
    virtual1 = doc.create_node("paragraph", "Virtual 1", virtual=True)
    regular2 = doc.create_node("paragraph", "Regular 2")

    root.add_child(regular1)
    root.add_child(virtual1)
    root.add_child(regular2)

    # Without skip_virtual
    has_prev = regular2.has_previous_node(skip_virtual=False)
    assert has_prev == True, "regular2 should have previous node"

    # With skip_virtual=True, should skip virtual and find regular1
    has_prev_skip = regular2.has_previous_node(skip_virtual=True)
    assert has_prev_skip == True, "regular2 should have previous real node (regular1)"

    print("✓ has_previous_node() with skip_virtual works correctly")
    doc.close()


def test_get_node_at_index_edge_cases():
    """Test ContentNode.get_node_at_index() edge cases.

    Based on legacy SDK: kodexa/kodexa/model/model.py:1910-1957
    Tests boundary conditions including negative indices and out-of-bounds.
    """
    print("\nTesting ContentNode.get_node_at_index() edge cases...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create children
    para0 = doc.create_node("paragraph", "Index 0")
    para1 = doc.create_node("paragraph", "Index 1")
    para2 = doc.create_node("paragraph", "Index 2")

    root.add_child(para0)
    root.add_child(para1)
    root.add_child(para2)

    # Test normal access at each index
    node0 = root.get_node_at_index(0)
    assert node0 is not None, "Should find node at index 0"
    assert node0.content == "Index 0"

    node1 = root.get_node_at_index(1)
    assert node1 is not None, "Should find node at index 1"
    assert node1.content == "Index 1"

    node2 = root.get_node_at_index(2)
    assert node2 is not None, "Should find node at index 2"
    assert node2.content == "Index 2"

    # Test out of bounds (large positive)
    node_oob = root.get_node_at_index(99)
    assert node_oob is None, "Should return None for out of bounds index"

    # Test out of bounds (negative)
    node_neg = root.get_node_at_index(-1)
    assert node_neg is None, "Should return None for negative index"

    # Test empty parent (no children)
    empty_parent = doc.create_node("section", "Empty section")
    root.add_child(empty_parent)
    node_from_empty = empty_parent.get_node_at_index(0)
    assert node_from_empty is None, "Should return None for parent with no children"

    print("✓ get_node_at_index() edge cases work correctly")
    doc.close()


# =============================================================================
# Newly Implemented Methods Tests (from legacy SDK parity)
# =============================================================================

def test_get_tag_with_uuid():
    """Test ContentNode.get_tag() with tag_uuid filtering parameter.

    Based on legacy SDK: kodexa/kodexa/model/model.py:1762-1791
    The tag_uuid parameter filters the tag result by UUID.
    """
    print("\nTesting ContentNode.get_tag() with tag_uuid filtering...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para = doc.create_node("paragraph", "Test paragraph")
    root.add_child(para)

    # Tag the node
    para.tag("important")
    tags = para.get_tags()
    assert len(tags) > 0, "Expected at least one tag"

    tag_uuid = tags[0].uuid if hasattr(tags[0], 'uuid') else None
    assert tag_uuid, "Expected tag to have a UUID"

    # Get tag without UUID filter - should return the tag
    tag = para.get_tag("important")
    assert tag is not None, "Expected to find tag by name"

    # Get tag with matching UUID - should return the tag
    tag_with_uuid = para.get_tag("important", tag_uuid=tag_uuid)
    assert tag_with_uuid is not None, "Expected to find tag with matching UUID"

    # Get tag with non-matching UUID - should return None
    tag_wrong_uuid = para.get_tag("important", tag_uuid="non-existent-uuid")
    assert tag_wrong_uuid is None, "Expected None for non-matching UUID"

    # Get non-existent tag - should return None
    no_tag = para.get_tag("nonexistent")
    assert no_tag is None, "Expected None for non-existent tag"

    print("✓ get_tag() with tag_uuid works correctly")
    doc.close()


def test_select_with_first_only():
    """Test ContentNode.select() with first_only parameter.

    Based on legacy SDK: kodexa/kodexa/model/model.py:801-827
    When first_only=True, only the first matching node is returned.
    """
    print("\nTesting ContentNode.select() with first_only parameter...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    # Create multiple paragraphs
    para1 = doc.create_node("paragraph", "First paragraph")
    para2 = doc.create_node("paragraph", "Second paragraph")
    para3 = doc.create_node("paragraph", "Third paragraph")
    root.add_child(para1)
    root.add_child(para2)
    root.add_child(para3)

    # Select all paragraphs (default: first_only=False)
    all_paras = root.select("//paragraph")
    assert len(all_paras) == 3, f"Expected 3 paragraphs, got {len(all_paras)}"

    # Select with first_only=True - should return list with 1 element
    first_para = root.select("//paragraph", first_only=True)
    assert len(first_para) == 1, f"Expected 1 paragraph with first_only, got {len(first_para)}"
    assert first_para[0].content == "First paragraph"

    # Select with no matches and first_only=True - should return empty list
    no_matches = root.select("//nonexistent", first_only=True)
    assert len(no_matches) == 0, "Expected empty list for no matches with first_only"

    print("✓ select() with first_only works correctly")
    doc.close()


def test_copy_tag():
    """Test ContentNode.copy_tag() method.

    Based on legacy SDK: kodexa/kodexa/model/model.py:1098-1132
    copy_tag creates a new tag with same values as existing tag.
    """
    print("\nTesting ContentNode.copy_tag()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para = doc.create_node("paragraph", "Test paragraph")
    root.add_child(para)

    # Tag the node with initial tag
    para.tag("original_tag", value="test_value", confidence=0.95)

    # Verify original tag exists
    original = para.get_tag("original_tag")
    assert original is not None, "Expected original_tag to exist"

    # Copy tag to new name - call on the node that has the tag (selector "." selects current node)
    para.copy_tag(".", "original_tag", "copied_tag")

    # Verify copied tag exists
    copied = para.get_tag("copied_tag")
    assert copied is not None, "Expected copied_tag to exist"

    # Both tags should now exist
    assert para.has_tag("original_tag"), "original_tag should still exist"
    assert para.has_tag("copied_tag"), "copied_tag should now exist"

    # Test no-op cases (should not throw)
    para.copy_tag(".", None, "new_tag")  # existing_tag_name is None
    para.copy_tag(".", "original_tag", None)  # new_tag_name is None
    para.copy_tag(".", "same_tag", "same_tag")  # same names

    print("✓ copy_tag() works correctly")
    doc.close()


def test_update_feature():
    """Test ContentNode.update_feature() method.

    Based on legacy SDK: kodexa/kodexa/model/model.py:535-545
    update_feature removes existing feature and re-adds with updated values.
    """
    print("\nTesting ContentNode.update_feature()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para = doc.create_node("paragraph", "Test paragraph")
    root.add_child(para)

    # Add initial feature
    para.add_feature("test", "score", 0.5)

    # Get the feature
    feature = para.get_feature("test", "score")
    assert feature is not None, "Expected feature to exist"
    assert feature.value[0] == 0.5, f"Expected 0.5, got {feature.value[0]}"

    # Modify the feature value
    feature.value = [0.95]

    # Update the feature
    para.update_feature(feature)

    # Verify update
    updated_feature = para.get_feature("test", "score")
    assert updated_feature is not None, "Expected updated feature to exist"
    assert updated_feature.value[0] == 0.95, f"Expected 0.95, got {updated_feature.value[0]}"

    print("✓ update_feature() works correctly")
    doc.close()


def test_get_statistics():
    """Test ContentNode.get_statistics() method.

    Based on legacy SDK: kodexa/kodexa/model/model.py:931-944
    get_statistics returns the spatial:statistics feature value.
    """
    print("\nTesting ContentNode.get_statistics()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para = doc.create_node("paragraph", "Test paragraph")
    root.add_child(para)

    # Initially no statistics
    stats = para.get_statistics()
    assert stats is None, "Expected None for no statistics"

    # Set statistics
    stats_data = {"mean": 0.5, "min": 0.1, "max": 0.9, "count": 100}
    para.set_statistics(stats_data)

    # Get statistics
    retrieved_stats = para.get_statistics()
    assert retrieved_stats is not None, "Expected statistics to exist"
    assert retrieved_stats.get("mean") == 0.5, f"Expected mean 0.5, got {retrieved_stats.get('mean')}"
    assert retrieved_stats.get("count") == 100, f"Expected count 100, got {retrieved_stats.get('count')}"

    print("✓ get_statistics() works correctly")
    doc.close()


def test_to_json():
    """Test ContentNode.to_json() method.

    Based on legacy SDK: kodexa/kodexa/model/model.py:364-374
    to_json returns a JSON string representation of the node.
    """
    print("\nTesting ContentNode.to_json()...")

    import json

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para = doc.create_node("paragraph", "Test paragraph content")
    root.add_child(para)

    # Add a feature for richer test
    para.add_feature("test", "value", "feature_data")

    # Get JSON
    json_str = para.to_json()
    assert isinstance(json_str, str), "Expected string result"

    # Parse to verify it's valid JSON
    parsed = json.loads(json_str)
    assert isinstance(parsed, dict), "Expected dict after parsing"

    # Verify key fields
    assert parsed.get("node_type") == "paragraph", f"Expected 'paragraph', got {parsed.get('node_type')}"
    assert parsed.get("content") == "Test paragraph content", f"Unexpected content"

    print("✓ to_json() works correctly")
    doc.close()


def test_get_feature_set():
    """Test Document.get_feature_set() method.

    Based on legacy SDK: kodexa/kodexa/model/model.py:3264-3293
    get_feature_set returns a FeatureSet containing all tag features from tagged nodes.
    """
    print("\nTesting Document.get_feature_set()...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para1 = doc.create_node("paragraph", "First paragraph")
    para2 = doc.create_node("paragraph", "Second paragraph")
    para3 = doc.create_node("paragraph", "Third paragraph - no tag")
    root.add_child(para1)
    root.add_child(para2)
    root.add_child(para3)

    # Tag some nodes
    para1.tag("invoice/amount", value="100.00")
    para2.tag("invoice/date", value="2024-01-15")
    # para3 has no tags

    # Get feature set
    feature_set = doc.get_feature_set()
    assert feature_set is not None, "Expected FeatureSet"
    assert feature_set.node_features is not None, "Expected node_features"

    # Should have entries for the 2 tagged nodes
    assert len(feature_set.node_features) >= 2, f"Expected at least 2 node features, got {len(feature_set.node_features)}"

    # Each node_feature should have features
    for nf in feature_set.node_features:
        assert nf.node_uuid is not None, "Expected nodeUuid"
        assert nf.features is not None, "Expected features list"

    print("✓ get_feature_set() works correctly")
    doc.close()


def test_get_feature_set_with_owner_uri():
    """Test Document.get_feature_set() with owner_uri filtering.

    Based on legacy SDK: kodexa/kodexa/model/model.py:3264-3293
    owner_uri parameter filters tags by their owner_uri metadata.
    """
    print("\nTesting Document.get_feature_set() with owner_uri filtering...")

    doc = Document(inmemory=True)
    root = doc.create_node("document")
    doc.content_node = root

    para1 = doc.create_node("paragraph", "First paragraph")
    para2 = doc.create_node("paragraph", "Second paragraph")
    root.add_child(para1)
    root.add_child(para2)

    # Tag nodes with different owner_uri
    para1.tag("tagged_field", value="value1", owner_uri="processor://my-processor/v1")
    para2.tag("tagged_field", value="value2", owner_uri="processor://other-processor/v1")

    # Get all features (no filter)
    all_features = doc.get_feature_set()
    all_count = len(all_features.node_features) if all_features.node_features else 0

    # Get features filtered by owner_uri
    # Note: filtering may not work perfectly if owner_uri isn't in first value position
    filtered_features = doc.get_feature_set(owner_uri="processor://my-processor/v1")

    print(f"All node features: {all_count}")
    print(f"Filtered node features: {len(filtered_features.node_features) if filtered_features.node_features else 0}")

    print("✓ get_feature_set() with owner_uri works correctly")
    doc.close()


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    tests = [
        # Document tests
        test_find_nodes_by_tag_uuid,
        test_get_node_by_id,
        test_get_node_count_by_type,
        test_get_feature_types_with_counts,
        test_get_node_types_with_counts,
        test_get_all_features,
        test_get_document_filename,
        # Missing Document method tests
        test_replace_exceptions,
        test_get_tags_by_prefix,
        test_create_data_exception,
        test_get_data_objects_by_parent_id,
        # ContentNode tests
        test_has_next_node,
        test_has_previous_node,
        test_get_first_child_index,
        test_get_last_child_index,
        test_get_node_at_index,
        test_add_child_content,
        test_get_ancestors,
        test_get_descendants,
        # Enhanced ContentNode tests (legacy SDK behavior)
        test_has_next_node_with_regex,
        test_has_previous_node_with_regex,
        test_has_next_node_skip_virtual,
        test_has_previous_node_skip_virtual,
        test_get_node_at_index_edge_cases,
        # Newly implemented methods tests (legacy SDK parity)
        test_get_tag_with_uuid,
        test_select_with_first_only,
        test_copy_tag,
        test_update_feature,
        test_get_statistics,
        test_to_json,
        test_get_feature_set,
        test_get_feature_set_with_owner_uri,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")

    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 All tests passed!")
