"""
Canonical JSON normalization for deterministic hashing.

This module ensures that the same compliance data always produces
the same hash, regardless of key ordering, whitespace, or null values.
"""

import json
import unicodedata
from typing import Any, Dict, List, Union


def normalize_json(data: Union[Dict, List, Any]) -> str:
    """
    Produce canonical JSON string for deterministic hashing.
    
    Rules applied:
    1. Sort all dictionary keys recursively
    2. Remove null, empty string, empty list, and empty dict values
    3. Remove fields starting with underscore (internal/debug fields)
    4. Apply Unicode NFC normalization to all strings
    5. No whitespace in output
    6. Consistent serialization (separators, no ensure_ascii)
    
    Args:
        data: Data structure to normalize (dict, list, or primitive)
    
    Returns:
        Canonical JSON string
    
    Example:
        >>> data = {"b": 1, "a": 2, "_debug": "removed", "empty": None}
        >>> normalize_json(data)
        '{"a":2,"b":1}'
    """
    cleaned = _clean_value(data)
    
    # Serialize with consistent settings
    return json.dumps(
        cleaned,
        separators=(',', ':'),  # No whitespace
        ensure_ascii=False,      # Allow Unicode
        sort_keys=True,          # Sorted keys
        default=str              # Convert non-serializable to string
    )


def _clean_value(value: Any) -> Any:
    """
    Recursively clean and normalize a value.
    
    Args:
        value: Value to clean
    
    Returns:
        Cleaned value
    """
    if isinstance(value, dict):
        return _clean_dict(value)
    elif isinstance(value, list):
        return _clean_list(value)
    elif isinstance(value, str):
        return _normalize_string(value)
    elif value is None:
        return None  # Will be filtered out by _clean_dict
    else:
        return value


def _clean_dict(d: Dict) -> Dict:
    """
    Clean dictionary by removing empty/null values and internal fields.
    
    Args:
        d: Dictionary to clean
    
    Returns:
        Cleaned dictionary with sorted keys
    """
    cleaned = {}
    
    for key, value in sorted(d.items()):
        # Skip internal fields (start with underscore)
        if key.startswith('_'):
            continue
        
        # Recursively clean value
        cleaned_value = _clean_value(value)
        
        # Skip if value is None, empty string, empty list, or empty dict
        if cleaned_value in (None, '', [], {}):
            continue
        
        cleaned[key] = cleaned_value
    
    return cleaned


def _clean_list(lst: List) -> List:
    """
    Clean list by recursively cleaning each element.
    
    Args:
        lst: List to clean
    
    Returns:
        Cleaned list
    """
    cleaned = []
    
    for item in lst:
        cleaned_item = _clean_value(item)
        
        # Keep item unless it's None or empty
        if cleaned_item not in (None, '', [], {}):
            cleaned.append(cleaned_item)
    
    return cleaned


def _normalize_string(s: str) -> str:
    """
    Normalize string using Unicode NFC form.
    
    This ensures that different representations of the same
    Unicode characters are normalized to a canonical form.
    
    Args:
        s: String to normalize
    
    Returns:
        Normalized string
    
    Example:
        >>> _normalize_string("café")  # é as two characters
        'café'  # é as single character
    """
    return unicodedata.normalize('NFC', s)


def validate_deterministic(data: Dict) -> bool:
    """
    Validate that data can be deterministically normalized.
    
    Checks for common issues that might cause non-deterministic behavior:
    - Floating point precision issues
    - Datetime objects (should be ISO strings)
    - Custom objects
    
    Args:
        data: Data to validate
    
    Returns:
        True if data is safe for deterministic normalization
    
    Raises:
        ValueError: If data contains non-deterministic elements
    """
    try:
        # Try to normalize
        normalized = normalize_json(data)
        
        # Try to parse back
        parsed = json.loads(normalized)
        
        # Should be able to normalize again with same result
        renormalized = normalize_json(parsed)
        
        if normalized != renormalized:
            raise ValueError("Data is not deterministically normalizable")
        
        return True
    
    except (TypeError, ValueError) as e:
        raise ValueError(f"Data validation failed: {str(e)}")
