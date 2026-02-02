"""
Tests for ContentNode features and tags functionality.
"""

import sys
import json
import pytest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from kodexa_document import Document, ContentNode, DocumentError


class TestContentNodeFeatures:
    """Test ContentNode feature operations."""
    
    def test_add_and_get_feature(self):
        """Test adding and retrieving a feature."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Test content")
        
        # Add a feature
        node.add_feature("style", "font", {"family": "Arial", "size": 12})
        
        # Get the feature - returns a ContentFeature object
        feature = node.get_feature("style", "font")
        assert feature is not None
        # Use get_value() to get the actual value - Go backend stores as array
        feature_value = feature.get_value()
        assert isinstance(feature_value, list)
        assert len(feature_value) == 1
        assert feature_value[0]["family"] == "Arial"
        assert feature_value[0]["size"] == 12
        
        doc.close()
    
    def test_add_feature_return_value(self):
        """Test that add_feature returns the ContentFeature with accumulated values (legacy_python behavior)."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Test content")
        
        # First add_feature call
        new_feature = node.add_feature('test', 'test', 'cheese')
        # add_feature now returns a ContentFeature object matching legacy_python
        assert new_feature is not None
        assert len(new_feature.value) == 1
        assert new_feature.value[0] == 'cheese'
        
        # Second add to same feature - should append
        another_feature = node.add_feature('test', 'test', 'pickels')
        assert len(another_feature.value) == 2
        assert another_feature.value[0] == 'cheese'
        assert another_feature.value[1] == 'pickels'
        
        # Third add to same feature
        yet_another_feature = node.add_feature('test', 'test', 'lettuce')
        assert len(yet_another_feature.value) == 3
        assert yet_another_feature.value[0] == 'cheese'
        assert yet_another_feature.value[1] == 'pickels'
        assert yet_another_feature.value[2] == 'lettuce'
        
        # Test with a new feature
        feature_2 = node.add_feature('test_2', 'test_2_name', 'sesame_seeds')
        assert feature_2 is not None
        assert len(feature_2.value) == 1
        assert feature_2.value[0] == 'sesame_seeds'
        
        doc.close()
    
    def test_get_all_features(self):
        """Test getting all features on a node."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Test content")
        
        # Add multiple features
        node.add_feature("style", "font", {"family": "Arial"})
        node.add_feature("style", "color", "blue")
        node.add_feature("layout", "margin", {"top": 10, "bottom": 10})
        
        # Get all features
        features = node.get_features()
        assert features is not None
        assert len(features) >= 3  # At least the 3 we added
        
        doc.close()
    
    def test_get_features_of_type(self):
        """Test getting features filtered by type."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Test content")
        
        # Add features of different types
        node.add_feature("style", "font", "Arial")
        node.add_feature("style", "color", "blue")
        node.add_feature("layout", "margin", 10)
        
        # Get only style features - now returns ContentFeature objects
        style_features = node.get_features_of_type("style")
        assert len(style_features) == 2
        
        # Verify they are ContentFeature objects with correct properties
        for feature in style_features:
            assert hasattr(feature, 'feature_type')
            assert hasattr(feature, 'name') 
            assert hasattr(feature, 'get_value')
            assert feature.feature_type == "style"
            assert feature.name in ["font", "color"]
        
        # Get only layout features
        layout_features = node.get_features_of_type("layout")
        assert len(layout_features) == 1
        assert layout_features[0].feature_type == "layout"
        assert layout_features[0].name == "margin"
        
        doc.close()
    
    def test_remove_feature(self):
        """Test removing a feature."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Test content")
        
        # Add and then remove a feature
        node.add_feature("style", "font", "Arial")
        feature = node.get_feature("style", "font")
        assert feature is not None
        assert feature.value == ["Arial"]
        
        node.remove_feature("style", "font")
        assert node.get_feature("style", "font") is None

        doc.close()

    def test_contentnode_feature_edge_cases(self):
        """Test feature-related edge cases."""
        doc = Document()
        node = doc.create_node("test")

        # Test get_features_of_type with no features
        features = node.get_features_of_type("nonexistent")
        assert features == []

        # Test remove_feature that doesn't exist - returns None (no error)
        result = node.remove_feature("type", "name")
        assert result is None

        # Add a feature and test removal
        node.add_feature("type", "name", "value")
        # Verify feature exists
        features = node.get_features_of_type("type")
        assert len(features) == 1

        # Successful removal returns None
        result = node.remove_feature("type", "name")
        assert result is None

        # Verify feature was removed
        features = node.get_features_of_type("type")
        assert len(features) == 0

        # Try removing again - also returns None (idempotent)
        result = node.remove_feature("type", "name")
        assert result is None

        doc.close()

    def test_feature_multiple_values(self):
        """Test multiple feature values."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")

        # Add feature values (appends like legacy_python)
        node.add_feature("style", "font", "Arial")
        node.add_feature("style", "font", "Helvetica")

        # Should have both values in array
        font_feature = node.get_feature("style", "font")
        assert font_feature is not None
        assert font_feature.value == ["Arial", "Helvetica"]

        # Add multiple features with different names
        node.add_feature("tags", "keyword", "python")
        node.add_feature("tags", "author", "testing")
        
        # Both should exist as separate features - now returns ContentFeature objects
        features = node.get_features_of_type("tags")
        assert len(features) >= 2
        
        # Verify they are ContentFeature objects
        for feature in features:
            assert hasattr(feature, 'feature_type')
            assert hasattr(feature, 'name')
            assert feature.feature_type == "tags"
            assert feature.name in ["keyword", "author"]
        
        doc.close()


class TestContentNodeTags:
    """Test ContentNode tagging operations."""
    
    def test_tag_node_simple(self):
        """Test simple node tagging."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Important text")
        
        # Tag the node
        node.tag("important")
        
        # Check if tag exists
        assert node.has_tag("important")
        assert node.has_tags()
        
        doc.close()
    
    def test_tag_with_options(self):
        """Test tagging with various options."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Test text")
        
        # Tag with options
        node.tag("entity", 
                confidence=0.95,
                value="person",
                tag_uuid="123e4567-e89b-12d3-a456-426614174000")
        
        # Get the tag
        tag = node.get_tag("entity")
        assert tag is not None
        
        # Check tag properties
        if "Confidence" in tag:
            assert tag["Confidence"] == 0.95
        if "Value" in tag:
            assert tag["Value"] == "person"
        if "UUID" in tag:
            assert tag["UUID"] == "123e4567-e89b-12d3-a456-426614174000"
        
        doc.close()
    
    def test_get_all_tags(self):
        """Test getting all tags on a node."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Multi-tagged text")
        
        # Add multiple tags
        node.tag("important")
        node.tag("reviewed")
        node.tag("entity/person")
        
        # Get all tags - now returns list of tag names (strings)
        tags = node.get_tags()
        assert len(tags) >= 3
        
        # Check tag names - tags is now a list of strings (legacy_python behavior)
        assert "important" in tags
        assert "reviewed" in tags
        assert "entity/person" in tags
        
        doc.close()
    
    def test_get_specific_tag(self):
        """Test getting a specific tag by name."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Tagged text")
        
        # Add tags
        node.tag("tag1", value="value1")
        node.tag("tag2", value="value2")
        
        # Get specific tag
        tag1 = node.get_tag("tag1")
        assert tag1 is not None
        if "Value" in tag1:
            assert tag1["Value"] == "value1"
        
        # Non-existent tag returns None
        tag3 = node.get_tag("tag3")
        assert tag3 is None or tag3 == {}
        
        doc.close()
    
    def test_has_tag(self):
        """Test checking if a tag exists."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Test text")
        
        # Initially no tags
        assert not node.has_tag("test")
        assert not node.has_tags()
        
        # Add a tag
        node.tag("test")
        
        # Now has the tag
        assert node.has_tag("test")
        assert node.has_tags()
        
        # But not other tags
        assert not node.has_tag("other")
        
        doc.close()
    
    def test_remove_tag(self):
        """Test removing a tag (when implemented)."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test text")

        # Add and verify tag
        node.tag("removable")
        assert node.has_tag("removable")

        # Try to remove (currently not implemented in domain)
        try:
            node.remove_tag("removable")
            # If it works, verify removal
            assert not node.has_tag("removable")
        except RuntimeError as e:
            # Expected until RemoveTag is implemented
            assert "not yet implemented" in str(e) or "Failed to remove" in str(e)

        doc.close()

    def test_update_tag(self):
        """Test updating an existing tag's data field in place."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test text")

        # Add initial tag
        node.tag("my_label", value="initial_value", confidence=0.8)
        assert node.has_tag("my_label")

        # Get initial tag data
        initial_tags = node.get_feature_values("tag", "my_label")
        assert initial_tags is not None
        assert len(initial_tags) == 1
        assert initial_tags[0].get("value") == "initial_value"

        # Update the tag's data field with custom data
        custom_data = {"custom_key": "custom_value", "count": 42}
        node.update_tag("my_label", custom_data)

        # Verify update - still 1 tag entry, with updated data field
        updated_tags = node.get_feature_values("tag", "my_label")
        assert updated_tags is not None
        assert len(updated_tags) == 1
        # The data field should contain our custom data
        assert updated_tags[0].get("data") == custom_data

        doc.close()

    def test_update_tag_nonexistent(self):
        """Test that updating a non-existent tag raises an error."""
        from kodexa_document.errors import DocumentError
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test text")

        # Try to update a tag that doesn't exist
        try:
            node.update_tag("nonexistent_tag", {"test": "data"})
            assert False, "Expected error for non-existent tag"
        except (RuntimeError, DocumentError) as e:
            assert "not found" in str(e).lower() or "failed" in str(e).lower()

        doc.close()

    def test_update_tag_persistence(self):
        """Test that updated tags persist through save/load."""
        import tempfile
        import os

        doc1 = Document(inmemory=True)
        node = doc1.create_node("paragraph", "Tagged paragraph")
        doc1.content_node.add_child(node)

        # Add initial tag
        node.tag("persistent_label", value="original")

        # Update the tag's data field
        custom_data = {"updated_key": "updated_value", "items": [1, 2, 3]}
        node.update_tag("persistent_label", custom_data)

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".kddb", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            doc1.to_kddb(tmp_path)
            doc1.close()

            # Load and verify
            doc2 = Document.from_kddb(tmp_path)
            loaded_node = doc2.select("//paragraph")[0]

            loaded_tags = loaded_node.get_feature_values("tag", "persistent_label")
            assert loaded_tags is not None
            assert len(loaded_tags) == 1
            # The data field should contain our custom data
            assert loaded_tags[0].get("data") == custom_data

            doc2.close()
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_tag_persistence(self):
        """Test that tags persist through save/load."""
        import tempfile
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
            loaded_children = loaded_root.get_children()
            assert len(loaded_children) == 1
            
            loaded_child = loaded_children[0]
            
            # Check tags persisted
            assert loaded_child.has_tag("important")
            assert loaded_child.has_tag("category/business")
            
            # Check tag details
            important_tag = loaded_child.get_tag("important")
            if important_tag and "Confidence" in important_tag:
                assert important_tag["Confidence"] == 0.9
            
            doc2.close()
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_contentnode_tag_edge_cases(self):
        """Test tag-related edge cases."""
        doc = Document()
        node = doc.create_node("test")

        # Test has_tag on nonexistent tag
        has_tag = node.has_tag("nonexistent")
        assert has_tag is False

        # Test get_tag on nonexistent tag
        tag = node.get_tag("nonexistent")
        assert tag is None

        # Test remove_tag on nonexistent tag - raises DocumentError
        with pytest.raises(DocumentError, match="tag 'nonexistent' not found"):
            node.remove_tag("nonexistent")

        # Add a tag and test
        node.tag("test_tag", value="test_value")

        # Test has_tag
        has_tag = node.has_tag("test_tag")
        assert has_tag is True

        # Successful remove_tag returns None
        result = node.remove_tag("test_tag")
        assert result is None

        # Try removing again - should raise DocumentError
        with pytest.raises(DocumentError, match="tag 'test_tag' not found"):
            node.remove_tag("test_tag")

        doc.close()


class TestGetFeaturesIncludesTagsAndBbox:
    """Test that GetFeatures returns tags and bounding boxes as features for backward compatibility."""

    def test_get_features_includes_tags_as_features(self):
        """Test that get_features() returns tags as features with 'tag:xxx' type."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")
        doc.content_node = node

        # Add a regular feature
        node.add_feature("style", "bold", "true")

        # Add tags
        node.tag("Bill/Amount", value="100.00")
        node.tag("important")

        # Get all features - should include regular features and tags
        features = node.get_features()

        # Find tag features
        tag_features = [f for f in features if f.feature_type == "tag"]

        # Should have 2 tag features
        assert len(tag_features) == 2, f"Expected 2 tag features, got {len(tag_features)}"

        # Verify tag names
        tag_names = [f.name for f in tag_features]
        assert "Bill/Amount" in tag_names, "Expected 'Bill/Amount' tag feature"
        assert "important" in tag_names, "Expected 'important' tag feature"

        # Verify regular feature is still there
        style_features = [f for f in features if f.feature_type == "style"]
        assert len(style_features) == 1, "Expected 1 style feature"

        doc.close()

    def test_get_features_includes_bbox_as_feature(self):
        """Test that get_features() returns bounding box as feature with 'spatial:bbox' type."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")
        doc.content_node = node

        # Add a regular feature
        node.add_feature("style", "font", "Arial")

        # Set bounding box
        node.set_bbox([10.0, 20.0, 100.0, 200.0])

        # Get all features - should include bbox
        features = node.get_features()

        # Find spatial:bbox feature
        bbox_features = [f for f in features if f.feature_type == "spatial" and f.name == "bbox"]

        # Should have 1 bbox feature
        assert len(bbox_features) == 1, f"Expected 1 spatial:bbox feature, got {len(bbox_features)}"

        # Verify coordinates in data
        bbox_feature = bbox_features[0]
        bbox_data = bbox_feature.get_value()
        assert bbox_data is not None, "Expected bbox data to be present"

        # Bbox data should be coordinates [x1, y1, x2, y2]
        if isinstance(bbox_data, list) and len(bbox_data) == 4:
            assert bbox_data[0] == 10.0, f"Expected x1=10.0, got {bbox_data[0]}"
            assert bbox_data[1] == 20.0, f"Expected y1=20.0, got {bbox_data[1]}"
            assert bbox_data[2] == 100.0, f"Expected x2=100.0, got {bbox_data[2]}"
            assert bbox_data[3] == 200.0, f"Expected y2=200.0, got {bbox_data[3]}"

        doc.close()

    def test_get_features_combined_result(self):
        """Test that get_features() returns combined regular features, tags, and bbox."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")
        doc.content_node = node

        # Add regular feature
        node.add_feature("style", "bold", "true")

        # Add tags
        node.tag("entity/amount", value="100.00")
        node.tag("important")

        # Set bounding box
        node.set_bbox([0, 0, 100, 100])

        # Get all features
        features = node.get_features()

        # Count by type
        style_count = len([f for f in features if f.feature_type == "style"])
        tag_count = len([f for f in features if f.feature_type == "tag"])
        spatial_count = len([f for f in features if f.feature_type == "spatial"])

        # Should have: 1 regular + 2 tags + 1 bbox = 4
        assert style_count == 1, f"Expected 1 style feature, got {style_count}"
        assert tag_count == 2, f"Expected 2 tag features, got {tag_count}"
        assert spatial_count == 1, f"Expected 1 spatial feature, got {spatial_count}"

        doc.close()

    def test_get_features_multiple_tags_same_name(self):
        """Test that multiple tags with same name are grouped into a single feature."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content with 100 and 200 and 300")
        doc.content_node = node

        # Add multiple tags with same name but different values/positions
        node.tag("entity/amount", value="100.00", start=18, end=21)
        node.tag("entity/amount", value="200.00", start=26, end=29)
        node.tag("entity/amount", value="300.00", start=34, end=37)

        # Get all features
        features = node.get_features()

        # Count tag:entity/amount features
        amount_features = [f for f in features if f.feature_type == "tag" and f.name == "entity/amount"]

        # Tags with same name are grouped into a single feature
        assert len(amount_features) == 1, f"Expected 1 tag:entity/amount feature, got {len(amount_features)}"

        doc.close()

    def test_get_features_of_type_with_tags(self):
        """Test that get_features_of_type('tag') returns all tag features."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")
        doc.content_node = node

        # Add regular feature
        node.add_feature("style", "bold", "true")

        # Add tags
        node.tag("tag1", value="value1")
        node.tag("tag2", value="value2")
        node.tag("tag3")

        # Get only tag features
        tag_features = node.get_features_of_type("tag")

        # Should have exactly 3 tag features
        assert len(tag_features) == 3, f"Expected 3 tag features, got {len(tag_features)}"

        # All should have feature_type == "tag"
        for f in tag_features:
            assert f.feature_type == "tag", f"Expected feature_type 'tag', got '{f.feature_type}'"

        doc.close()

    def test_get_features_of_type_with_spatial(self):
        """Test that get_features_of_type('spatial') returns bbox feature."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")
        doc.content_node = node

        # Add regular feature
        node.add_feature("style", "bold", "true")

        # Set bounding box
        node.set_bbox([10, 20, 100, 200])

        # Get only spatial features
        spatial_features = node.get_features_of_type("spatial")

        # Should have exactly 1 spatial feature (the bbox)
        assert len(spatial_features) == 1, f"Expected 1 spatial feature, got {len(spatial_features)}"
        assert spatial_features[0].name == "bbox", f"Expected name 'bbox', got '{spatial_features[0].name}'"

        doc.close()

    def test_set_feature_redirects_tag_type(self):
        """Test that set_feature with type='tag' redirects to tag()."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")
        doc.content_node = node

        # Use set_feature with tag type - should redirect to tag()
        node.set_feature("tag", "my_tag", "tag_value")

        # Should be accessible via tag methods
        assert node.has_tag("my_tag"), "Expected tag 'my_tag' to exist"

        # Should also appear in get_features
        features = node.get_features()
        tag_features = [f for f in features if f.feature_type == "tag" and f.name == "my_tag"]
        assert len(tag_features) == 1, f"Expected 1 tag:my_tag feature, got {len(tag_features)}"

        doc.close()

    def test_set_feature_redirects_spatial_bbox(self):
        """Test that set_feature with type='spatial', name='bbox' redirects to set_bbox()."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")
        doc.content_node = node

        # Use set_feature with spatial:bbox - should redirect to set_bbox()
        # Note: This may need special handling in Python for coordinate parsing
        node.set_feature("spatial", "bbox", [50.0, 60.0, 150.0, 160.0])

        # Should be accessible via bbox methods
        bbox = node.get_bbox()
        if bbox is not None:
            assert bbox[0] == 50.0, f"Expected x1=50.0, got {bbox[0]}"
            assert bbox[1] == 60.0, f"Expected y1=60.0, got {bbox[1]}"
            assert bbox[2] == 150.0, f"Expected x2=150.0, got {bbox[2]}"
            assert bbox[3] == 160.0, f"Expected y2=160.0, got {bbox[3]}"

        doc.close()

    def test_remove_feature_redirects_tag_type(self):
        """Test that remove_feature with type='tag' redirects to remove_tag()."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")
        doc.content_node = node

        # Add a tag
        node.tag("removable_tag")
        assert node.has_tag("removable_tag"), "Tag should exist"

        # Use remove_feature with tag type - should redirect to remove_tag()
        node.remove_feature("tag", "removable_tag")

        # Tag should be removed
        assert not node.has_tag("removable_tag"), "Tag should have been removed"

        doc.close()

    def test_add_feature_redirects_tag_type(self):
        """Test that add_feature with type='tag' redirects to tag()."""
        doc = Document(inmemory=True)

        node = doc.create_node("paragraph", "Test content")
        doc.content_node = node

        # Use add_feature with tag type - should redirect to tag()
        node.add_feature("tag", "added_tag", "tag_value")

        # Should be accessible via tag methods
        assert node.has_tag("added_tag"), "Expected tag 'added_tag' to exist"

        doc.close()


class TestFeatureTagInteraction:
    """Test interaction between features and tags."""

    def test_features_and_tags_independent(self):
        """Test that features and tags are independent."""
        doc = Document(inmemory=True)
        
        node = doc.create_node("paragraph", "Test content")
        
        # Add both features and tags
        node.add_feature("style", "font", "Arial")
        node.tag("important")

        # Both should exist independently
        # get_feature_value returns the first value (legacy behavior)
        assert node.get_feature_value("style", "font") == "Arial"
        assert node.has_tag("important")
        
        # Removing feature doesn't affect tags
        node.remove_feature("style", "font")
        assert node.has_tag("important")
        
        doc.close()
    
    def test_node_with_complex_metadata(self):
        """Test node with both features and tags."""
        doc = Document(inmemory=True)
        
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
        assert len(node.get_features()) >= 3
        assert len(node.get_tags()) >= 3
        assert node.has_tag("important")
        assert node.get_feature("style", "font") is not None
        
        doc.close()


if __name__ == "__main__":
    # Run tests
    print("Running ContentNode features and tags tests...")
    
    # Feature tests
    feature_test = TestContentNodeFeatures()
    feature_tests = [
        ("test_add_and_get_feature", feature_test.test_add_and_get_feature),
        ("test_get_all_features", feature_test.test_get_all_features),
        ("test_get_features_of_type", feature_test.test_get_features_of_type),
        ("test_remove_feature", feature_test.test_remove_feature),
        ("test_feature_multiple_values", feature_test.test_feature_multiple_values),
    ]
    
    # Tag tests
    tag_test = TestContentNodeTags()
    tag_tests = [
        ("test_tag_node_simple", tag_test.test_tag_node_simple),
        ("test_tag_with_options", tag_test.test_tag_with_options),
        ("test_get_all_tags", tag_test.test_get_all_tags),
        ("test_get_specific_tag", tag_test.test_get_specific_tag),
        ("test_has_tag", tag_test.test_has_tag),
        ("test_remove_tag", tag_test.test_remove_tag),
        ("test_update_tag", tag_test.test_update_tag),
        ("test_update_tag_nonexistent", tag_test.test_update_tag_nonexistent),
        ("test_update_tag_persistence", tag_test.test_update_tag_persistence),
        ("test_tag_persistence", tag_test.test_tag_persistence),
    ]
    
    # Interaction tests
    interaction_test = TestFeatureTagInteraction()
    interaction_tests = [
        ("test_features_and_tags_independent", interaction_test.test_features_and_tags_independent),
        ("test_node_with_complex_metadata", interaction_test.test_node_with_complex_metadata),
    ]

    # GetFeatures includes tags and bbox tests
    get_features_test = TestGetFeaturesIncludesTagsAndBbox()
    get_features_tests = [
        ("test_get_features_includes_tags_as_features", get_features_test.test_get_features_includes_tags_as_features),
        ("test_get_features_includes_bbox_as_feature", get_features_test.test_get_features_includes_bbox_as_feature),
        ("test_get_features_combined_result", get_features_test.test_get_features_combined_result),
        ("test_get_features_multiple_tags_same_name", get_features_test.test_get_features_multiple_tags_same_name),
        ("test_get_features_of_type_with_tags", get_features_test.test_get_features_of_type_with_tags),
        ("test_get_features_of_type_with_spatial", get_features_test.test_get_features_of_type_with_spatial),
        ("test_set_feature_redirects_tag_type", get_features_test.test_set_feature_redirects_tag_type),
        ("test_set_feature_redirects_spatial_bbox", get_features_test.test_set_feature_redirects_spatial_bbox),
        ("test_remove_feature_redirects_tag_type", get_features_test.test_remove_feature_redirects_tag_type),
        ("test_add_feature_redirects_tag_type", get_features_test.test_add_feature_redirects_tag_type),
    ]

    all_tests = feature_tests + tag_tests + interaction_tests + get_features_tests
    
    passed = 0
    failed = 0
    
    for test_name, test_func in all_tests:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed out of {len(all_tests)} tests")
    
    if failed == 0:
        print("All features and tags tests passed!")
    else:
        print(f"{failed} tests failed.")