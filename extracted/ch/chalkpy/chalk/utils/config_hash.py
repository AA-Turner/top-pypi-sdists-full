"""
Utilities for generating consistent hashes from configuration objects.
"""

import hashlib
import json
from typing import Any, Dict


def generate_config_hash(config_dict: Dict[str, Any]) -> str:
    """
    Generate a consistent hash from configuration parameters.

    This function ensures that the same configuration inputs always produce
    the same hash, regardless of ordering in collections or future additions
    to the config structure.
    """

    def _normalize_value(value: Any) -> Any:
        """Recursively normalize values for consistent hashing."""
        if isinstance(value, dict):
            # Sort dictionary by keys to ensure consistent ordering
            return {k: _normalize_value(v) for k, v in sorted(value.items())}
        elif isinstance(value, (list, tuple)):
            # Sort lists/tuples if they contain comparable items
            try:
                return sorted([_normalize_value(item) for item in value])
            except TypeError:
                # If items aren't comparable, convert to strings and sort
                return sorted([str(_normalize_value(item)) for item in value])
        elif isinstance(value, set):
            # Convert sets to sorted lists
            try:
                return sorted([_normalize_value(item) for item in value])
            except TypeError:
                return sorted([str(_normalize_value(item)) for item in value])
        elif hasattr(value, "total_seconds"):
            # Handle timedelta objects
            return value.total_seconds()
        elif hasattr(value, "__dict__"):
            # Handle objects with attributes by converting to dict
            obj_dict = {}
            for attr_name in sorted(dir(value)):
                if not attr_name.startswith("_"):
                    try:
                        attr_value = getattr(value, attr_name)
                        if not callable(attr_value):
                            obj_dict[attr_name] = _normalize_value(attr_value)
                    except (AttributeError, TypeError):
                        pass
            return obj_dict
        else:
            return value

    # Normalize the entire config dict
    normalized_config = _normalize_value(config_dict)

    # Convert to JSON string with sorted keys for consistent serialization
    json_str = json.dumps(normalized_config, sort_keys=True, separators=(",", ":"))

    # Generate SHA-256 hash
    hash_obj = hashlib.sha256(json_str.encode("utf-8"))
    return hash_obj.hexdigest()[:16]  # Use first 16 characters for brevity
