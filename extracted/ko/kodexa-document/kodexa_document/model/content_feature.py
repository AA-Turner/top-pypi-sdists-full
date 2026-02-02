"""
ContentFeature class matching legacy_python behavior.
"""
from typing import Any, Optional


class ContentFeature:
    """
    A feature allows you to capture almost any additional data or metadata and associate it with a ContentNode.
    This class matches the legacy_python ContentFeature API.
    """

    def __init__(self, feature_type: str, name: str, value: Any):
        """
        Initialize a ContentFeature.

        Args:
            feature_type: The type of feature (e.g., "style", "tag")
            name: The name of the feature (e.g., "font", "important")
            value: The feature value (always stored as array internally)
        """
        self.feature_type: str = feature_type
        self.name: str = name

        # Value is always an array internally
        if isinstance(value, list):
            self.value = value
        else:
            self.value = [value] if value is not None else []

    def get_value(self) -> Any:
        """
        Get the value from the feature.

        Returns:
            The value of the feature as an array
        """
        return self.value

    def to_dict(self) -> dict:
        """
        Create a dictionary representing this ContentFeature's structure and content.

        Returns:
            The properties of this ContentFeature structured as a dictionary.
        """
        return {
            "name": f"{self.feature_type}:{self.name}",
            "value": self.value,
            "featureType": self.feature_type,
        }

    def __str__(self) -> str:
        return f"Feature [type='{self.feature_type}' name='{self.name}' value='{self.value}']"

    def __repr__(self) -> str:
        return f"ContentFeature(feature_type='{self.feature_type}', name='{self.name}', value={self.value!r})"

    @classmethod
    def from_dict(cls, data: dict) -> 'ContentFeature':
        """
        Create a ContentFeature from a dictionary (as returned by C binding).

        Args:
            data: Dictionary with 'name', 'value', and optionally 'featureType'

        Returns:
            ContentFeature instance
        """
        # New C binding returns featureType and name separately
        if 'featureType' in data and data['featureType']:
            # Use direct values from new C binding format
            feature_type = data['featureType']
            name = data.get('name', '')
        else:
            # Fallback: Extract type and name from the "type:name" format (legacy)
            name_parts = data.get('name', ':').split(':', 1)
            feature_type = name_parts[0] if len(name_parts) > 0 else ''
            name = name_parts[1] if len(name_parts) > 1 else ''

        # For value, use 'data' field if available (contains actual value), otherwise 'value'
        feature_value = data.get('value', [])
        if 'data' in data and data['data']:
            import json
            try:
                # Parse the data field which contains the actual feature values
                feature_value = json.loads(data['data'])
            except (json.JSONDecodeError, TypeError):
                # If parsing fails, use the raw data
                feature_value = data['data']

        return cls(
            feature_type=feature_type,
            name=name,
            value=feature_value,
        )
