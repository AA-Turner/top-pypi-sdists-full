from typing import Any

import msgspec

from exponent.core.remote_execution.cli_rpc_types import ToolResult


def to_mostly_xml(tool_result: ToolResult) -> str:
    """
    This provides a default textual representation of the tool result. Override it as needed for your tool."""
    d = msgspec.to_builtins(tool_result)
    del d["tool_name"]
    return to_mostly_xml_helper(d)


def to_mostly_xml_helper(
    d: Any,
) -> str:
    if isinstance(d, dict):
        # No outer wrapper at top level, each field gets XML tags
        parts = []
        for key, value in d.items():
            if isinstance(value, list):
                # Handle lists with item tags
                list_items = "\n".join(
                    f"<item>\n{to_mostly_xml_helper(item)}\n</item>" for item in value
                )
                parts.append(f"<{key}>\n{list_items}\n</{key}>")
            elif isinstance(value, dict):
                # Nested dict
                parts.append(f"<{key}>\n{to_mostly_xml_helper(value)}\n</{key}>")
            else:
                # Scalar value
                parts.append(f"<{key}>\n{value!s}\n</{key}>")
        return "\n".join(parts)
    elif isinstance(d, list):
        raise ValueError("Lists are not allowed at the top level")
    else:
        return str(d)
