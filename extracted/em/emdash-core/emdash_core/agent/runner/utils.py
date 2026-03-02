"""Utility classes and functions for the agent runner."""

import json
from datetime import datetime, date
from typing import Any


class SafeJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles Neo4j types and other non-serializable objects."""

    def default(self, obj: Any) -> Any:
        # Handle datetime objects
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        # Handle Neo4j DateTime
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()

        # Handle Neo4j Date, Time, etc.
        if hasattr(obj, 'to_native'):
            return str(obj.to_native())

        # Handle sets
        if isinstance(obj, set):
            return list(obj)

        # Handle bytes
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')

        # Fallback to string representation
        try:
            return str(obj)
        except Exception:
            return f"<non-serializable: {type(obj).__name__}>"


def summarize_tool_result(result: Any) -> str:
    """Create a brief summary of a tool result.

    Args:
        result: ToolResult object with success, error, and data attributes.

    Returns:
        Brief summary string.
    """
    if not result.success:
        return f"Error: {result.error}"

    if not result.data:
        return "Empty result"

    data = result.data

    # Ensure data is a dict before accessing keys
    if not isinstance(data, dict):
        return str(data)[:200] if data else "Completed"

    if "results" in data:
        return f"{len(data['results'])} results"
    elif "root_node" in data:
        node = data["root_node"]
        if isinstance(node, dict):
            name = node.get("qualified_name") or node.get("file_path", "unknown")
        else:
            name = str(node)
        return f"Expanded: {name}"
    elif "callers" in data:
        return f"{len(data['callers'])} callers"
    elif "callees" in data:
        return f"{len(data['callees'])} callees"
    elif "message" in data:
        return str(data["message"])[:200]

    return "Completed"
