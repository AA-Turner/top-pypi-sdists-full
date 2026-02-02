"""Tests to improve coverage for ContentFeature class."""

import json
import pytest
from kodexa_document import ContentFeature


class TestContentFeatureCoverage:
    """Test cases to improve ContentFeature coverage."""

    def test_init_with_none_value(self):
        """Test initialization with None value (covers line 30)."""
        feature = ContentFeature("type", "name", None)
        assert feature.value == []
        assert feature.get_value() == []

    def test_get_value_empty_list(self):
        """Test get_value with empty value list (covers line 42)."""
        feature = ContentFeature("type", "name", [])
        assert feature.get_value() == []

        # Also test manually setting empty value
        feature2 = ContentFeature("type", "name", "test")
        feature2.value = []
        assert feature2.get_value() == []

    def test_to_dict_method(self):
        """Test to_dict method (covers lines 56-61)."""
        feature = ContentFeature("style", "font", "Arial")
        result = feature.to_dict()

        assert result == {
            "name": "style:font",
            "value": ["Arial"],
            "featureType": "style"
        }

        # Test with multiple values
        feature2 = ContentFeature("tag", "labels", ["important", "urgent"])
        result2 = feature2.to_dict()

        assert result2 == {
            "name": "tag:labels",
            "value": ["important", "urgent"],
            "featureType": "tag"
        }

    def test_repr_method(self):
        """Test __repr__ method (covers line 67)."""
        feature = ContentFeature("style", "font", "Arial")
        repr_str = repr(feature)

        assert repr_str == "ContentFeature(feature_type='style', name='font', value=['Arial'])"

        # Test with complex values
        feature2 = ContentFeature("data", "complex", {"key": "value"})
        repr_str2 = repr(feature2)

        assert "ContentFeature(feature_type='data', name='complex'" in repr_str2
        assert "{'key': 'value'}" in repr_str2

    def test_from_dict_legacy_format(self):
        """Test from_dict with legacy name format (covers lines 87-89)."""
        # Legacy format without feature_type field
        data = {
            "name": "style:font",
            "value": ["Arial"]
        }

        feature = ContentFeature.from_dict(data)
        assert feature.feature_type == "style"
        assert feature.name == "font"
        assert feature.value == ["Arial"]

        # Test with missing colon in name (edge case)
        data2 = {
            "name": "justname",
            "value": ["test"]
        }

        feature2 = ContentFeature.from_dict(data2)
        assert feature2.feature_type == "justname"
        assert feature2.name == ""
        assert feature2.value == ["test"]

        # Test with empty name
        data3 = {
            "name": "",
            "value": ["test"]
        }

        feature3 = ContentFeature.from_dict(data3)
        assert feature3.feature_type == ""
        assert feature3.name == ""

    def test_from_dict_with_data_field(self):
        """Test from_dict with data field containing JSON (covers lines 94-100)."""
        # Test with valid JSON in data field
        data = {
            "name": "metadata",
            "value": [],
            "data": json.dumps({"key": "value", "number": 123}),
            "featureType": "metadata"
        }

        feature = ContentFeature.from_dict(data)
        assert feature.feature_type == "metadata"
        assert feature.name == "metadata"
        # Value wrapped in list because ContentFeature stores all values as lists
        assert feature.value == [{"key": "value", "number": 123}]

        # Test with invalid JSON in data field (should use raw data)
        data2 = {
            "name": "raw",
            "value": [],
            "data": "not-json-{invalid}",
            "featureType": "raw"
        }

        feature2 = ContentFeature.from_dict(data2)
        assert feature2.feature_type == "raw"
        assert feature2.name == "raw"
        # Even invalid JSON gets wrapped in a list
        assert feature2.value == ["not-json-{invalid}"]

        # Test with None data field (should fall through)
        data3 = {
            "name": "test",
            "value": ["original"],
            "data": None,
            "featureType": "test"
        }

        feature3 = ContentFeature.from_dict(data3)
        assert feature3.value == ["original"]

    def test_from_dict_edge_cases(self):
        """Test from_dict with various edge cases."""
        # Empty featureType field - falls back to legacy parsing
        data = {
            "name": "test",
            "value": ["val"],
            "featureType": ""
        }

        feature = ContentFeature.from_dict(data)
        # When featureType is empty, it falls back to parsing from name
        assert feature.feature_type == "test"
        assert feature.name == ""

        # Missing optional fields
        data2 = {
            "name": "minimal"
        }

        feature2 = ContentFeature.from_dict(data2)
        assert feature2.value == []
