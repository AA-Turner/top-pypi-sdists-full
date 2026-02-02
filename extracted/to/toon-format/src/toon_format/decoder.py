"""TOON decoder implementation."""

from toon_format.types import DecodeOptions, JsonValue


def decode(input: str, options: DecodeOptions | None = None) -> JsonValue:
    """Convert a TOON-formatted string to a Python value.

    Args:
        input: A TOON-formatted string to parse
        options: Optional decoding options:
            - indent: Expected number of spaces per indentation level (default: 2)
            - strict: Enable strict validation (default: True)

    Returns:
        A Python value (dict, list, or primitive) representing the parsed TOON data.

    Raises:
        ValueError: If the input is malformed (when strict=True)

    Examples:
        >>> decode('items[2]{sku,qty}:\\n  A1,2\\n  B2,1')
        {'items': [{'sku': 'A1', 'qty': 2}, {'sku': 'B2', 'qty': 1}]}

        >>> decode('tags[2]: foo,bar')
        {'tags': ['foo', 'bar']}

        >>> decode('[3]: 1,2,3')
        [1, 2, 3]
    """
    raise NotImplementedError("TOON decoder is not yet implemented")
