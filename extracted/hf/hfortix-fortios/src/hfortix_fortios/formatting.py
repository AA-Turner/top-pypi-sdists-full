"""
Data formatting utilities for FortiOS objects and data structures.

Provides simple, type-agnostic conversion functions that handle any input gracefully.
Never raises exceptions - returns sensible defaults for edge cases.

"""

from __future__ import annotations

import json
from typing import Any

__all__ = [
    "to_json",
    "to_csv",
    "to_dict",
    "to_multiline",
    "to_list",
    "to_quoted",
    "to_table",
    "to_yaml",
    "to_xml",
    "to_key_value",
    "to_markdown_table",
    "to_dictlist",
    "to_listdict",
]


def to_json(data: Any, indent: int = 2, **kwargs: Any) -> str:
    """
    Convert any data to formatted JSON string.

    Handles objects with __dict__, converts sets/tuples to lists,
    and uses str() fallback for non-serializable types.

    Args:
        data: Any Python object to convert to JSON
        indent: Number of spaces for indentation (default: 2)
        **kwargs: Additional arguments passed to json.dumps()

    Returns:
        Formatted JSON string

    """

    def default_handler(obj: Any) -> Any:
        """Handle non-serializable objects."""
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        if isinstance(obj, (set, tuple)):
            return list(obj)
        return str(obj)

    return json.dumps(data, indent=indent, default=default_handler, **kwargs)


def to_csv(data: Any, separator: str = ", ") -> str:
    """
    Convert any data to comma-separated string.

    Args:
        data: Any Python object to convert
        separator: String to use between items (default: ', ')

    Returns:
        Comma-separated string

    Examples:
        >>> to_csv(['port1', 'port2', 'port3'])
        'port1, port2, port3'

        >>> to_csv({'x': 1, 'y': 2, 'z': 3})
        'x=1, y=2, z=3'

        >>> to_csv('already a string')
        'already a string'

        >>> to_csv(None)
        ''

        >>> to_csv([1, 2, 3], separator=' | ')
        '1 | 2 | 3'

        >>> class Interface:
        ...     def __init__(self):
        ...         self.name = "port1"
        ...         self.ip = "10.0.0.1"
        >>> to_csv(Interface())
        'name=port1, ip=10.0.0.1'
    """
    if data is None:
        return ""

    if isinstance(data, str):
        return data

    if isinstance(data, (int, float, bool)):
        return str(data)

    if isinstance(data, (list, tuple, set)):
        return separator.join(str(item) for item in data)

    if isinstance(data, dict):
        return separator.join(f"{k}={v}" for k, v in data.items())

    if hasattr(data, "__dict__"):
        return to_csv(data.__dict__, separator)

    return str(data)


def to_dict(data: Any) -> dict[str, Any] | dict[int, Any]:
    """
    Convert any data to dictionary.

    Args:
        data: Any Python object to convert

    Returns:
        Dictionary representation of the data

    Examples:
        >>> class Policy:
        ...     def __init__(self):
        ...         self.name = "Allow-All"
        ...         self.action = "accept"
        >>> to_dict(Policy())
        {'name': 'Allow-All', 'action': 'accept'}

        >>> to_dict({'already': 'a dict'})
        {'already': 'a dict'}

        >>> to_dict([('a', 1), ('b', 2)])
        {'a': 1, 'b': 2}

        >>> to_dict(['x', 'y', 'z'])
        {0: 'x', 1: 'y', 2: 'z'}

        >>> to_dict('simple string')
        {'value': 'simple string'}

        >>> to_dict(None)
        {'value': None}
    """
    if isinstance(data, dict):
        return data

    if hasattr(data, "__dict__"):
        return data.__dict__

    if isinstance(data, (list, tuple)):
        # Check if it's a list of tuples (can be converted to dict)
        if data and all(
            isinstance(item, (list, tuple)) and len(item) == 2 for item in data
        ):
            try:
                return dict(data)
            except (TypeError, ValueError):
                pass
        # Otherwise convert to indexed dict
        return {i: v for i, v in enumerate(data)}

    # For primitives, wrap in value key
    return {"value": data}


def to_multiline(data: Any, separator: str = "\n") -> str:
    """
    Convert any data to newline-separated string.

    Args:
        data: Any Python object to convert
        separator: String to use between lines (default: '\\n')

    Returns:
        Newline-separated string

    Examples:
        >>> print(to_multiline(['port1', 'port2', 'port3']))
        port1
        port2
        port3

        >>> print(to_multiline({'name': 'policy1', 'action': 'accept'}))
        name: policy1
        action: accept

        >>> to_multiline('already a string')
        'already a string'

        >>> to_multiline(None)
        ''

        >>> class Policy:
        ...     def __init__(self):
        ...         self.name = "Allow-All"
        ...         self.policyid = 1
        >>> print(to_multiline(Policy()))
        name: Allow-All
        policyid: 1
    """
    if data is None:
        return ""

    if isinstance(data, str):
        return data

    if isinstance(data, (int, float, bool)):
        return str(data)

    if isinstance(data, (list, tuple, set)):
        return separator.join(str(item) for item in data)

    if isinstance(data, dict):
        return separator.join(f"{k}: {v}" for k, v in data.items())

    if hasattr(data, "__dict__"):
        return to_multiline(data.__dict__, separator)

    return str(data)


def to_list(data: Any, delimiter: str | None = None) -> list[Any]:
    """
    Convert any data to list.

    Args:
        data: Any Python object to convert
        delimiter: If data is a string, split by this delimiter.
                  If None and data is string with spaces, auto-splits by space.
                  Common delimiters: ',', ' ', '|', ';', etc.

    Returns:
        List representation of the data

    Examples:
        >>> to_list(['already', 'a', 'list'])
        ['already', 'a', 'list']

        >>> to_list(('tuple', 'to', 'list'))
        ['tuple', 'to', 'list']

        >>> to_list({'a', 'b', 'c'})  # set to list
        ['a', 'b', 'c']

        >>> to_list('port1,port2,port3', delimiter=',')
        ['port1', 'port2', 'port3']

        >>> to_list('port1 port2 port3')  # auto-splits on space
        ['port1', 'port2', 'port3']

        >>> to_list('80 443 8080')  # works with numbers as strings
        ['80', '443', '8080']

        >>> to_list('port1 | port2 | port3', delimiter=' | ')
        ['port1', 'port2', 'port3']

        >>> to_list('single_string')  # no spaces, returns as-is
        ['single_string']

        >>> to_list({'name': 'policy1', 'action': 'accept'})
        ['policy1', 'accept']

        >>> to_list(None)
        []

        >>> to_list(42)
        [42]

        >>> class Policy:
        ...     def __init__(self):
        ...         self.name = "Allow-All"
        ...         self.policyid = 1
        >>> to_list(Policy())
        ['Allow-All', 1]
    """
    if data is None:
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, (tuple, set)):
        return list(data)

    if isinstance(data, str):
        if delimiter is not None:
            # Explicit delimiter provided
            return [item.strip() for item in data.split(delimiter)]
        elif " " in data:
            # Auto-split on space if no delimiter specified and string contains spaces
            return data.split()
        else:
            # Single item string with no spaces
            return [data]

    if isinstance(data, dict):
        return list(data.values())

    if hasattr(data, "__dict__"):
        return list(data.__dict__.values())

    # For primitives, return single-item list
    return [data]


def to_quoted(data: Any, quote: str = '"', separator: str = ", ") -> str:
    """
    Convert any data to quoted string representation.

    Args:
        data: Any Python object to convert
        quote: Quote character to use (default: '"')
        separator: String to use between quoted items (default: ', ')

    Returns:
        Quoted string representation

    Examples:
        >>> to_quoted(['port1', 'port2', 'port3'])
        '"port1", "port2", "port3"'

        >>> to_quoted({'x': 1, 'y': 2})
        '"x", "y"'

        >>> to_quoted('hello')
        '"hello"'

        >>> to_quoted(None)
        '""'

        >>> to_quoted([1, 2, 3], quote="'")
        "'1', '2', '3'"

        >>> class Interface:
        ...     def __init__(self):
        ...         self.name = "port1"
        ...         self.vlan = 10
        >>> to_quoted(Interface())
        '"name", "vlan"'
    """
    if data is None:
        return f"{quote}{quote}"

    if isinstance(data, str):
        return f"{quote}{data}{quote}"

    if isinstance(data, (int, float, bool)):
        return f"{quote}{data}{quote}"

    if isinstance(data, (list, tuple, set)):
        return separator.join(f"{quote}{item}{quote}" for item in data)

    if isinstance(data, dict):
        # Quote the keys
        return separator.join(f"{quote}{k}{quote}" for k in data.keys())

    if hasattr(data, "__dict__"):
        return to_quoted(data.__dict__, quote, separator)

    return f"{quote}{data}{quote}"


def to_table(data: Any, headers: bool = True, delimiter: str = " | ") -> str:
    """
    Convert data to table format.

    Args:
        data: Any Python object to convert (list of dicts, list of objects, etc.)
        headers: Whether to include headers (default: True)
        delimiter: Column delimiter (default: ' | ')

    Returns:
        Table-formatted string

    Examples:
        >>> policies = [
        ...     {'name': 'Allow-Web', 'action': 'accept', 'policyid': 1},
        ...     {'name': 'Block-All', 'action': 'deny', 'policyid': 2}
        ... ]
        >>> print(to_table(policies))
        name | action | policyid
        Allow-Web | accept | 1
        Block-All | deny | 2

        >>> to_table(policies, headers=False)
        'Allow-Web | accept | 1\\nBlock-All | deny | 2'

        >>> to_table(policies, delimiter=' || ')
        'name || action || policyid\\nAllow-Web || accept || 1\\nBlock-All || deny || 2'
    """
    if data is None:
        return ""

    if isinstance(data, str):
        return data

    # Convert single dict to list
    if isinstance(data, dict):
        data = [data]

    # Convert objects with __dict__ to dicts
    if not isinstance(data, (list, tuple)):
        if hasattr(data, "__dict__"):
            data = [data]
        else:
            return str(data)

    # Convert list of objects to list of dicts
    processed_data = []
    for item in data:
        if hasattr(item, "__dict__"):
            processed_data.append(item.__dict__)
        elif isinstance(item, dict):
            processed_data.append(item)
        else:
            processed_data.append({"value": item})

    if not processed_data:
        return ""

    # Get all unique keys
    all_keys = []
    for item in processed_data:
        for key in item.keys():
            if key not in all_keys:
                all_keys.append(key)

    lines = []

    # Add headers
    if headers:
        lines.append(delimiter.join(str(k) for k in all_keys))

    # Add rows
    for item in processed_data:
        row = delimiter.join(str(item.get(k, "")) for k in all_keys)
        lines.append(row)

    return "\n".join(lines)


def to_yaml(data: Any, indent: int = 2) -> str:
    """
    Convert data to YAML-like format (simple, no external dependencies).

    Args:
        data: Any Python object to convert
        indent: Number of spaces for indentation (default: 2)

    Returns:
        YAML-style string

    Examples:
        >>> policy = {'name': 'Allow-Web', 'action': 'accept', 'srcintf': ['port1', 'port2']}
        >>> print(to_yaml(policy))
        name: Allow-Web
        action: accept
        srcintf:
          - port1
          - port2

        >>> print(to_yaml({'nested': {'key': 'value'}}))
        nested:
          key: value
    """

    def _format_yaml(obj: Any, level: int = 0) -> str:
        indent_str = " " * (indent * level)

        if obj is None:
            return "null"

        if isinstance(obj, bool):
            return "true" if obj else "false"

        if isinstance(obj, (int, float)):
            return str(obj)

        if isinstance(obj, str):
            # Quote if contains special chars
            if ":" in obj or "#" in obj or obj.startswith((" ", "-")):
                return f"'{obj}'"
            return obj

        if isinstance(obj, (list, tuple)):
            if not obj:
                return "[]"
            lines = []
            for item in obj:
                if isinstance(item, (dict, list)):
                    # Complex item
                    lines.append(f"{indent_str}- ")
                    lines.append(_format_yaml(item, level + 1))
                else:
                    # Simple item
                    lines.append(f"{indent_str}- {_format_yaml(item, 0)}")
            return "\n".join(lines)

        if isinstance(obj, dict):
            if not obj:
                return "{}"
            lines = []
            for key, value in obj.items():
                if isinstance(value, dict):
                    lines.append(f"{indent_str}{key}:")
                    lines.append(_format_yaml(value, level + 1))
                elif isinstance(value, (list, tuple)):
                    lines.append(f"{indent_str}{key}:")
                    lines.append(_format_yaml(value, level + 1))
                else:
                    lines.append(
                        f"{indent_str}{key}: {_format_yaml(value, 0)}"
                    )
            return "\n".join(lines)

        if hasattr(obj, "__dict__"):
            return _format_yaml(obj.__dict__, level)

        return str(obj)

    return _format_yaml(data)


def to_xml(data: Any, root: str = "data", indent: int = 2) -> str:
    """
    Convert data to simple XML format (no external dependencies).

    Args:
        data: Any Python object to convert
        root: Root element name (default: 'data')
        indent: Number of spaces for indentation (default: 2)

    Returns:
        XML string

    Examples:
        >>> policy = {'name': 'Allow-Web', 'policyid': 1}
        >>> print(to_xml(policy, root='policy'))
        <policy>
          <name>Allow-Web</name>
          <policyid>1</policyid>
        </policy>

        >>> policies = [{'name': 'p1'}, {'name': 'p2'}]
        >>> print(to_xml(policies, root='policies'))
        <policies>
          <item>
            <name>p1</name>
          </item>
          <item>
            <name>p2</name>
          </item>
        </policies>
    """

    def _escape_xml(text: str) -> str:
        """Escape special XML characters."""
        # Order matters: & must be first to avoid double-escaping
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&apos;")
        return text

    def _format_xml(obj: Any, tag: str, level: int = 0) -> str:
        indent_str = " " * (indent * level)

        if obj is None:
            return f"{indent_str}<{tag}/>"

        if isinstance(obj, (str, int, float, bool)):
            value = _escape_xml(str(obj)) if isinstance(obj, str) else obj
            return f"{indent_str}<{tag}>{value}</{tag}>"

        if isinstance(obj, (list, tuple)):
            lines = [f"{indent_str}<{tag}>"]
            for item in obj:
                lines.append(_format_xml(item, "item", level + 1))
            lines.append(f"{indent_str}</{tag}>")
            return "\n".join(lines)

        if isinstance(obj, dict):
            lines = [f"{indent_str}<{tag}>"]
            for key, value in obj.items():
                # Sanitize key for XML
                safe_key = key.replace(" ", "_").replace("-", "_")
                lines.append(_format_xml(value, safe_key, level + 1))
            lines.append(f"{indent_str}</{tag}>")
            return "\n".join(lines)

        if hasattr(obj, "__dict__"):
            return _format_xml(obj.__dict__, tag, level)

        return f"{indent_str}<{tag}>{obj}</{tag}>"

    return _format_xml(data, root)


def to_key_value(
    data: Any, separator: str = "=", delimiter: str = "\n"
) -> str:
    """
    Convert data to key=value pairs format.

    Args:
        data: Any Python object to convert
        separator: Separator between key and value (default: '=')
        delimiter: Delimiter between pairs (default: '\\n')

    Returns:
        Key-value pairs string

    Examples:
        >>> config = {'host': '192.168.1.1', 'port': 443, 'verify': False}
        >>> print(to_key_value(config))
        host=192.168.1.1
        port=443
        verify=False

        >>> to_key_value(config, separator=': ', delimiter='; ')
        'host: 192.168.1.1; port: 443; verify: False'
    """
    if data is None:
        return ""

    if isinstance(data, str):
        return data

    if isinstance(data, dict):
        return delimiter.join(f"{k}{separator}{v}" for k, v in data.items())

    if hasattr(data, "__dict__"):
        return to_key_value(data.__dict__, separator, delimiter)

    if isinstance(data, (list, tuple)):
        # For lists, use index as key
        return delimiter.join(f"{i}{separator}{v}" for i, v in enumerate(data))

    return str(data)


def to_markdown_table(data: Any) -> str:
    """
    Convert data to Markdown table format.

    Args:
        data: List of dicts or list of objects

    Returns:
        Markdown table string

    Examples:
        >>> policies = [
        ...     {'name': 'Allow-Web', 'action': 'accept'},
        ...     {'name': 'Block-All', 'action': 'deny'}
        ... ]
        >>> print(to_markdown_table(policies))
        | name | action |
        | --- | --- |
        | Allow-Web | accept |
        | Block-All | deny |
    """
    if data is None:
        return ""

    if isinstance(data, str):
        return data

    # Convert single dict to list
    if isinstance(data, dict):
        data = [data]

    # Convert objects with __dict__ to dicts
    if not isinstance(data, (list, tuple)):
        if hasattr(data, "__dict__"):
            data = [data]
        else:
            return str(data)

    # Convert list of objects to list of dicts
    processed_data = []
    for item in data:
        if hasattr(item, "__dict__"):
            processed_data.append(item.__dict__)
        elif isinstance(item, dict):
            processed_data.append(item)
        else:
            processed_data.append({"value": item})

    if not processed_data:
        return ""

    # Get all unique keys
    all_keys = []
    for item in processed_data:
        for key in item.keys():
            if key not in all_keys:
                all_keys.append(key)

    lines = []

    # Add header
    lines.append("| " + " | ".join(str(k) for k in all_keys) + " |")
    lines.append("| " + " | ".join("---" for _ in all_keys) + " |")

    # Add rows
    for item in processed_data:
        row = "| " + " | ".join(str(item.get(k, "")) for k in all_keys) + " |"
        lines.append(row)

    return "\n".join(lines)


def to_dictlist(data: Any) -> list[dict[str, Any]]:
    """
    Convert dict of lists to list of dicts (columnar to row format).

    Useful for transforming columnar data into row-based records.

    Args:
        data: Dict where values are lists, or any convertible data

    Returns:
        List of dicts where each dict is one row

    Examples:
        >>> columnar = {'name': ['p1', 'p2'], 'action': ['accept', 'deny']}
        >>> to_dictlist(columnar)
        [{'name': 'p1', 'action': 'accept'}, {'name': 'p2', 'action': 'deny'}]

        >>> to_dictlist({'ports': ['80', '443', '8080']})
        [{'ports': '80'}, {'ports': '443'}, {'ports': '8080'}]

        >>> # Already list of dicts - returns as-is
        >>> to_dictlist([{'name': 'p1'}, {'name': 'p2'}])
        [{'name': 'p1'}, {'name': 'p2'}]

        >>> to_dictlist(None)
        []
    """
    if data is None:
        return []

    # Already list of dicts
    if isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            return data
        # List of objects with __dict__
        if all(hasattr(item, "__dict__") for item in data):
            return [item.__dict__ for item in data]
        # Convert simple list to list of value dicts
        return [{"value": item} for item in data]

    # Convert object to dict first
    if hasattr(data, "__dict__"):
        data = data.__dict__

    if not isinstance(data, dict):
        return [{"value": data}]

    # Dict of lists - convert to list of dicts
    # Get all keys
    keys = list(data.keys())
    if not keys:
        return []

    # Check if all values are lists/tuples
    values = [
        data[k] if isinstance(data[k], (list, tuple)) else [data[k]]
        for k in keys
    ]

    # Find max length
    max_len = max(len(v) for v in values) if values else 0

    # Pad lists to same length with None
    padded_values = []
    for v in values:
        if len(v) < max_len:
            padded_values.append(list(v) + [None] * (max_len - len(v)))
        else:
            padded_values.append(list(v))

    # Transpose to list of dicts
    result = []
    for i in range(max_len):
        row = {keys[j]: padded_values[j][i] for j in range(len(keys))}
        result.append(row)

    return result


def to_listdict(data: Any) -> dict[str, list[Any]]:
    """
    Convert list of dicts to dict of lists (row to columnar format).

    Useful for transforming row-based records into columnar data.

    Args:
        data: List of dicts, list of objects, or any convertible data

    Returns:
        Dict where keys are field names and values are lists

    Examples:
        >>> rows = [{'name': 'p1', 'action': 'accept'}, {'name': 'p2', 'action': 'deny'}]
        >>> to_listdict(rows)
        {'name': ['p1', 'p2'], 'action': ['accept', 'deny']}

        >>> to_listdict([{'ports': '80'}, {'ports': '443'}, {'ports': '8080'}])
        {'ports': ['80', '443', '8080']}

        >>> # Single dict becomes dict of single-item lists
        >>> to_listdict({'name': 'p1', 'action': 'accept'})
        {'name': ['p1'], 'action': ['accept']}

        >>> to_listdict(None)
        {}
    """
    if data is None:
        return {}

    # Already dict of lists
    if isinstance(data, dict):
        # Check if it's already dict of lists
        if all(isinstance(v, (list, tuple)) for v in data.values()):
            return {k: list(v) for k, v in data.items()}
        # Convert single values to lists
        return {k: [v] for k, v in data.items()}

    # Convert object to dict first
    if hasattr(data, "__dict__"):
        data = data.__dict__
        return {k: [v] for k, v in data.items()}

    if not isinstance(data, (list, tuple)):
        return {"value": [data]}

    # List of dicts - convert to dict of lists
    if not data:
        return {}

    # Convert objects to dicts
    processed_data = []
    for item in data:
        if hasattr(item, "__dict__"):
            processed_data.append(item.__dict__)
        elif isinstance(item, dict):
            processed_data.append(item)
        else:
            processed_data.append({"value": item})

    # Get all unique keys
    all_keys = []
    for item in processed_data:
        for key in item.keys():
            if key not in all_keys:
                all_keys.append(key)

    # Build dict of lists
    result = {key: [] for key in all_keys}
    for item in processed_data:
        for key in all_keys:
            result[key].append(item.get(key, None))

    return result
