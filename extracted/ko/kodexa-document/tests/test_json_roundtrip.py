"""
Test JSON serialization roundtrip to identify what data is being lost.
"""

import json
from kodexa_document import Document


def test_feature_roundtrip():
    """Test that features survive JSON roundtrip operations."""
    # Create document with features
    doc1 = Document(inmemory=True)
    root = doc1.create_node("document", "Test document")
    para = doc1.create_node("paragraph", "Test paragraph")

    # Add child
    root.add_child(para)
    doc1.content_node = root

    # Add bbox feature to paragraph (stored in separate bbox table)
    bbox_value = [1.0, 2.0, 3.0, 4.0]
    para.add_feature("spatial", "bbox", bbox_value)

    # Verify bbox was stored - get_features() includes bbox as synthetic feature
    features_before = para.get_features()
    assert len(features_before) > 0, "Feature should have been added"
    # Find the spatial:bbox feature
    bbox_feature_before = None
    for f in features_before:
        if f.feature_type == "spatial" and f.name == "bbox":
            bbox_feature_before = f
            break
    assert bbox_feature_before is not None, "spatial:bbox should be in features"
    # Value is wrapped: [[x1, y1, x2, y2]] so GetValue returns the array
    assert bbox_feature_before.value == [bbox_value], f"Expected {[bbox_value]}, got {bbox_feature_before.value}"

    # Export to JSON
    json_str = doc1.to_json()
    assert len(json_str) > 0, "JSON export should not be empty"

    # Check if bbox is in the JSON features array (as spatial:bbox feature)
    json_data = json.loads(json_str)
    content_node = json_data.get('content_node', {})
    children = content_node.get('children', [])
    assert len(children) > 0, "Children should exist in JSON"

    para_json = children[0]
    # BBox is now exported in the features array as featureType="spatial", name="bbox"
    json_features = para_json.get('features', [])
    bbox_feature = None
    for f in json_features:
        if f.get('featureType') == 'spatial' and f.get('name') == 'bbox':
            bbox_feature = f
            break
    assert bbox_feature is not None, "BBox feature should be in JSON features array"
    # Value is wrapped: [[x1, y1, x2, y2]]
    assert bbox_feature['value'] == [bbox_value], f"Expected bbox {[bbox_value]}, got {bbox_feature['value']}"

    # Import from JSON
    doc2 = Document.from_json(json_str, inmemory=True)

    # Check features in imported document
    root2 = doc2.content_node
    assert root2 is not None, "Root node should exist after import"

    children2 = root2.get_children()
    assert len(children2) > 0, "Children should exist after import"

    para2 = children2[0]

    # Verify bbox can be retrieved via get_bbox()
    imported_bbox = para2.get_bbox()
    assert imported_bbox == bbox_value, f"Expected bbox {bbox_value}, got {imported_bbox}"

    # Verify bbox is also available via get_features() as synthetic feature
    features_after = para2.get_features()
    assert len(features_after) > 0, "Features should survive JSON roundtrip"
    bbox_feature_after = None
    for f in features_after:
        if f.feature_type == "spatial" and f.name == "bbox":
            bbox_feature_after = f
            break
    assert bbox_feature_after is not None, "spatial:bbox should be in features after import"

    # Test feature retrieval methods
    spatial_features = para2.get_features_of_type("spatial")
    assert len(spatial_features) == 1, "Should have one spatial feature"

    bbox_feature = para2.get_feature("spatial", "bbox")
    assert bbox_feature is not None, "Should be able to retrieve specific feature"
    # get_value() now returns full array: [[x1, y1, x2, y2]]
    # Values may be integers after JSON roundtrip (1 vs 1.0)
    bbox_result = bbox_feature.get_value()
    # Unwrap outer array if needed
    if len(bbox_result) == 1 and isinstance(bbox_result[0], list):
        bbox_result = bbox_result[0]
    assert len(bbox_result) == 4, f"Expected 4 coordinates, got {len(bbox_result)}"
    assert [float(v) for v in bbox_result] == bbox_value, f"Expected {bbox_value}, got {bbox_result}"

    doc1.close()
    doc2.close()


def test_tag_roundtrip():
    """Test that tags survive JSON roundtrip operations."""
    # Create document with tags
    doc1 = Document(inmemory=True)
    root = doc1.create_node("document", "Test document")
    para = doc1.create_node("paragraph", "Important content")
    
    # Add child
    root.add_child(para)
    doc1.content_node = root
    
    # Add tag to paragraph
    para.tag("important", value="high_priority", confidence=0.95)
    
    # Verify tag was added - get_tags() now returns tag names (strings)
    tags_before = para.get_tags()
    assert len(tags_before) > 0, "Tag should have been added"
    assert "important" in tags_before
    
    # For rich tag data, use get_tag() method
    tag_data = para.get_tag("important")
    assert tag_data is not None
    assert tag_data['name'] == "important"
    assert tag_data['value'] == "high_priority"
    assert tag_data['confidence'] == 0.95
    
    # Export to JSON
    json_str = doc1.to_json()

    # Check if tags are in the JSON features array (as type="tag" features)
    json_data = json.loads(json_str)
    content_node = json_data.get('content_node', {})
    children = content_node.get('children', [])
    assert len(children) > 0, "Children should exist in JSON"

    para_json = children[0]
    # Tags are now exported in the features array as featureType="tag"
    json_features = para_json.get('features', [])
    tag_feature = None
    for f in json_features:
        if f.get('featureType') == 'tag' and f.get('name') == 'important':
            tag_feature = f
            break
    assert tag_feature is not None, "Tag feature should be in JSON features array"
    # Tag value is an array of tag data objects
    tag_value = tag_feature.get('value', [])
    assert len(tag_value) > 0, "Tag should have value data"
    tag_data = tag_value[0]
    assert tag_data.get('value') == "high_priority", f"Expected value 'high_priority', got {tag_data.get('value')}"
    assert tag_data.get('confidence') == 0.95, f"Expected confidence 0.95, got {tag_data.get('confidence')}"

    # Import from JSON
    doc2 = Document.from_json(json_str, inmemory=True)
    
    # Check tags in imported document
    root2 = doc2.content_node
    assert root2 is not None, "Root node should exist after import"
    
    children2 = root2.get_children()
    assert len(children2) > 0, "Children should exist after import"
    
    para2 = children2[0]
    tags_after = para2.get_tags()
    assert len(tags_after) > 0, "Tags should survive JSON roundtrip"
    assert "important" in tags_after
    
    # Check rich tag data survived roundtrip
    tag_data_after = para2.get_tag("important")
    assert tag_data_after is not None
    assert tag_data_after['name'] == "important"
    assert tag_data_after['value'] == "high_priority"
    assert tag_data_after['confidence'] == 0.95
    
    # Test tag query methods
    assert para2.has_tag("important"), "Should have the important tag"
    important_tag = para2.get_tag("important")
    assert important_tag is not None, "Should be able to retrieve specific tag"
    assert important_tag['value'] == "high_priority"
    
    doc1.close()
    doc2.close()


def test_document_validations_roundtrip():
    """Test that document validations survive JSON roundtrip."""
    # Note: Document validations are extraction-related and may not be 
    # directly settable in the current API. This test checks if the 
    # JSON structure includes them.
    
    doc1 = Document(inmemory=True)
    root = doc1.create_node("document", "Test document")
    doc1.content_node = root
    
    # Export to JSON to see structure
    json_str = doc1.to_json()
    json_data = json.loads(json_str)
    
    # Verify expected JSON structure keys
    expected_keys = {'uuid', 'version', 'content_node'}
    actual_keys = set(json_data.keys())
    assert expected_keys.issubset(actual_keys), f"Missing expected keys. Got: {actual_keys}"
    
    # Check if validation-related fields exist (they may be empty or absent)
    # These fields are optional and depend on extraction processing
    optional_fields = ['validations', 'document_validations', 'exceptions', 'content_exceptions']
    
    # Document that these fields are either absent or empty in basic documents
    for field in optional_fields:
        value = json_data.get(field)
        if value is not None:
            # If present, should be a list or empty
            assert isinstance(value, (list, type(None))), f"{field} should be a list or None"
    
    # Import from JSON and verify structure is preserved
    doc2 = Document.from_json(json_str, inmemory=True)
    json_str2 = doc2.to_json()
    json_data2 = json.loads(json_str2)
    
    # Verify roundtrip preserves structure
    assert json_data2['uuid'] == json_data['uuid'], "UUID should be preserved"
    assert json_data2['version'] == json_data['version'], "Version should be preserved"
    
    doc1.close()
    doc2.close()


# Tests are now pytest-compatible - no main execution needed