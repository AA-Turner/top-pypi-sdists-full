"""
Tests for JSON normalization (deterministic canonical form).
"""
import pytest
from compz.normalize import normalize_json


def test_normalize_same_dict_different_order():
    """Test that dict key order doesn't affect normalized output."""
    dict1 = {"b": 2, "a": 1, "c": 3}
    dict2 = {"a": 1, "c": 3, "b": 2}
    
    norm1 = normalize_json(dict1)
    norm2 = normalize_json(dict2)
    
    assert norm1 == norm2, "Same dict with different key order should normalize identically"


def test_normalize_different_dicts():
    """Test that different dicts produce different normalized output."""
    dict1 = {"a": 1, "b": 2}
    dict2 = {"a": 1, "b": 3}
    
    norm1 = normalize_json(dict1)
    norm2 = normalize_json(dict2)
    
    assert norm1 != norm2, "Different dicts should produce different normalized output"


def test_normalize_nested_dict():
    """Test normalization of nested dictionaries."""
    nested = {
        "outer": {
            "z": 3,
            "a": 1,
            "m": 2
        },
        "top": "value"
    }
    
    # Should not raise exception
    normalized = normalize_json(nested)
    assert isinstance(normalized, str)
    assert len(normalized) > 0


def test_normalize_with_list():
    """Test normalization handles lists correctly."""
    data = {
        "items": [3, 1, 2],
        "name": "test"
    }
    
    normalized = normalize_json(data)
    assert isinstance(normalized, str)
    # List order should be preserved (not sorted)
    assert "3" in normalized


def test_normalize_empty_dict():
    """Test normalization of empty dict."""
    normalized = normalize_json({})
    assert normalized == "{}"
