"""Type stubs for formatting utilities."""

from __future__ import annotations

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

    Args:
        data: Any Python object to convert to JSON
        indent: Number of spaces for indentation (default: 2)
        **kwargs: Additional arguments passed to json.dumps()

    Returns:
        Formatted JSON string
    """
    ...

def to_csv(data: Any, separator: str = ", ") -> str:
    """
    Convert any data to comma-separated string.

    Args:
        data: Any Python object to convert
        separator: String to use between items (default: ', ')

    Returns:
        Comma-separated string
    """
    ...

def to_dict(data: Any) -> dict[str, Any] | dict[int, Any]:
    """
    Convert any data to dictionary.

    Args:
        data: Any Python object to convert

    Returns:
        Dictionary representation of the data
    """
    ...

def to_multiline(data: Any, separator: str = "\n") -> str:
    """
    Convert any data to newline-separated string.

    Args:
        data: Any Python object to convert
        separator: String to use between lines (default: '\\n')

    Returns:
        Newline-separated string
    """
    ...

def to_list(data: Any, delimiter: str | None = None) -> list[Any]:
    """
    Convert any data to a list.

    Args:
        data: Any Python object to convert
        delimiter: Optional delimiter to split strings (default: None, auto-detect spaces)

    Returns:
        List representation of the data
    """
    ...

def to_quoted(data: Any, quote: str = '"', separator: str = ", ") -> str:
    """
    Convert any data to quoted string representation.

    Args:
        data: Any Python object to convert
        quote: Quote character to use (default: '"')
        separator: String to use between quoted items (default: ', ')

    Returns:
        Quoted string representation
    """
    ...

def to_table(data: Any, headers: bool = True, delimiter: str = " | ") -> str:
    """
    Convert data to ASCII table format.

    Args:
        data: Any Python object to convert
        headers: Whether to include headers (default: True)
        delimiter: Column delimiter (default: ' | ')

    Returns:
        ASCII table string
    """
    ...

def to_yaml(data: Any, indent: int = 2) -> str:
    """
    Convert data to YAML-like format (no external dependencies).

    Args:
        data: Any Python object to convert
        indent: Number of spaces for indentation (default: 2)

    Returns:
        YAML-like formatted string
    """
    ...

def to_xml(data: Any, root: str = "data", indent: int = 2) -> str:
    """
    Convert data to simple XML format (no external dependencies).

    Args:
        data: Any Python object to convert
        root: Root element name (default: 'data')
        indent: Number of spaces for indentation (default: 2)

    Returns:
        XML formatted string
    """
    ...

def to_key_value(data: Any, separator: str = "=", delimiter: str = "\n") -> str:
    """
    Convert data to key=value pairs format.

    Args:
        data: Any Python object to convert
        separator: Separator between key and value (default: '=')
        delimiter: Delimiter between pairs (default: '\\n')

    Returns:
        Key-value pairs string
    """
    ...

def to_markdown_table(data: Any) -> str:
    """
    Convert data to Markdown table format.

    Args:
        data: Any Python object to convert

    Returns:
        Markdown table string
    """
    ...

def to_dictlist(data: Any) -> list[dict[str, Any]]:
    """
    Convert columnar data to list of dictionaries (row format).

    Transforms {'col1': [a, b], 'col2': [x, y]} to [{'col1': a, 'col2': x}, {'col1': b, 'col2': y}]

    Args:
        data: Columnar data (dict of lists)

    Returns:
        List of dictionaries
    """
    ...

def to_listdict(data: Any) -> dict[str, list[Any]]:
    """
    Convert list of dictionaries to columnar format.

    Transforms [{'col1': a, 'col2': x}, {'col1': b, 'col2': y}] to {'col1': [a, b], 'col2': [x, y]}

    Args:
        data: List of dictionaries (row format)

    Returns:
        Dictionary of lists (columnar format)
    """
    ...
