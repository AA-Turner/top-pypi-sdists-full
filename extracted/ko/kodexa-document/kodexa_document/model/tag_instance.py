"""
TagInstance - Groups ContentNodes by tag UUID (legacy_python parity).
"""

from typing import List, Dict, Any, Optional


class TagInstance:
    """
    Represents a group of ContentNodes that share the same tag UUID.

    This class provides an organizational abstraction for working with
    related tagged content, matching the legacy_python implementation.
    """

    def __init__(self, tag_name: str, tag_uuid: str, nodes: List['ContentNode'],
                 value: Optional[str] = None, data: Optional[Dict[str, Any]] = None):
        """
        Initialize a TagInstance.

        Args:
            tag_name: Name of the tag
            tag_uuid: UUID that groups these nodes together
            nodes: List of ContentNodes sharing this tag UUID
            value: Combined content from all nodes (optional, computed if not provided)
            data: Tag metadata dictionary (optional)
        """
        self.tag_name = tag_name
        self.tag_uuid = tag_uuid
        self.nodes = nodes if nodes is not None else []
        self._value = value
        self._data = data if data is not None else {}

    def get_value(self) -> str:
        """
        Get the combined content value from all nodes in this instance.

        Returns:
            String with all node content joined by spaces
        """
        if self._value is not None:
            return self._value

        # Compute value by combining content from all nodes
        content_parts = []
        for node in self.nodes:
            if hasattr(node, 'get_all_content'):
                content = node.get_all_content()
                if content:
                    content_parts.append(content)
            elif hasattr(node, 'content') and node.content:
                content_parts.append(node.content)

        return " ".join(content_parts)

    def get_data(self) -> Dict[str, Any]:
        """
        Get the tag metadata/data dictionary.

        Returns:
            Dictionary containing tag metadata
        """
        return self._data

    @property
    def tag(self):
        """Get tag name (legacy_python compatibility)."""
        return self.tag_name

    @property
    def uuid(self):
        """Get tag UUID (legacy_python compatibility)."""
        return self.tag_uuid

    def __repr__(self):
        """String representation."""
        return f"TagInstance(tag_name='{self.tag_name}', tag_uuid='{self.tag_uuid}', nodes={len(self.nodes)})"
