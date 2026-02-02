"""
Test script for document statistics functionality.
"""

from kodexa_document import Document


def test_document_statistics():
    """Test the get_statistics functionality."""
    # Create a document and use auto-created root node
    doc = Document(inmemory=True)

    # Use auto-created root node
    root = doc.content_node
    root.content = "Test Document"
    section = doc.create_node("section", "Section 1")
    para1 = doc.create_node("paragraph", "First paragraph")
    para2 = doc.create_node("paragraph", "Second paragraph")

    # Build hierarchy
    root.add_child(section)
    section.add_child(para1)
    section.add_child(para2)
    
    # Add some features and tags
    para1.add_feature("spatial", "bbox", [1.0, 2.0, 3.0, 4.0])
    para1.tag("important", value="high", confidence=0.9)
    para2.add_feature("text", "label", "summary")
    
    # Get statistics
    stats = doc.get_statistics()
    
    # Verify statistics structure
    assert stats is not None, "Statistics should not be None"
    assert isinstance(stats, dict), "Statistics should be a dictionary"
    
    # Verify required fields exist
    assert 'uuid' in stats, "Statistics should contain UUID"
    assert 'version' in stats, "Statistics should contain version"
    assert 'total_nodes' in stats, "Statistics should contain total_nodes"
    assert 'total_tags' in stats, "Statistics should contain total_tags"
    assert 'total_features' in stats, "Statistics should contain total_features"
    assert 'total_exceptions' in stats, "Statistics should contain total_exceptions"
    assert 'generated_at' in stats, "Statistics should contain generated_at"
    assert 'node_type_count' in stats, "Statistics should contain node_type_count"
    
    # Verify expected values
    expected_nodes = 4  # root, section, paragraph, paragraph
    actual_nodes = stats.get('total_nodes', 0)
    assert actual_nodes == expected_nodes, f"Expected {expected_nodes} nodes, got {actual_nodes}"
    
    # Verify node types
    node_types = stats.get('node_type_count', {})
    assert isinstance(node_types, dict), "node_type_count should be a dictionary"
    
    expected_paragraphs = 2
    actual_paragraphs = node_types.get('paragraph', 0)
    assert actual_paragraphs == expected_paragraphs, f"Expected {expected_paragraphs} paragraphs, got {actual_paragraphs}"
    
    # Verify root type count
    assert node_types.get('root', 0) == 1, "Should have exactly 1 root node"
    assert node_types.get('section', 0) == 1, "Should have exactly 1 section node"
    
    # Check that we have some features and tags
    # Note: spatial:bbox is now stored in separate bbox table, not features table
    # So we only count the text:label feature
    assert stats.get('total_features', 0) == 1, "Expected 1 feature (bbox stored separately)"
    
    assert stats.get('total_tags', 0) > 0, "No tags detected"
    assert stats.get('total_tags', 0) == 1, "Expected 1 tag"
    
    doc.close()


# Tests are now pytest-compatible - no main execution needed