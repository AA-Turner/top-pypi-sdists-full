"""
List normalization helpers for FortiOS API.

Converts various input formats (strings, lists, dicts) to the standard
FortiOS API format: [{'name': 'value'}, ...]

Note: String values are automatically trimmed (leading/trailing whitespace removed)
to prevent common input errors.
"""

from typing import Any, Dict, List, Union


def normalize_to_name_list(
    value: Union[
        str,
        List[str],
        List[Dict[str, str]],
        List[Union[str, Dict[str, str]]],
        Dict[str, str],
        None,
    ],
) -> List[Dict[str, str]]:
    """
    Normalize various input formats to FortiOS API format: [{'name': 'value'}, ...]

    This is the most common list format used in FortiOS API for fields like:
    - srcintf, dstintf (firewall policy)
    - member (address groups, service groups)
    - interface (router, system)
    - etc.

    Args:
        value: Can be:
            - String: 'port1' → [{'name': 'port1'}]
            - List of strings: ['port1', 'port2'] → [{'name': 'port1'}, {'name': 'port2'}]
            - Dict: {'name': 'port1'} → [{'name': 'port1'}]
            - List of dicts: [{'name': 'port1'}, {'name': 'port2'}] → unchanged
            - None: []

        Note: Leading and trailing whitespace is automatically stripped from strings.

    Returns:
        List of dicts in FortiOS format
    """
    if value is None:
        return []

    # Already a list
    if isinstance(value, list):
        if not value:
            return []
        # Process each item based on its type (handles mixed lists)
        result: list[dict[str, str]] = []
        for item in value:
            if isinstance(item, dict):
                # Keep dict if it has 'name' key
                if item and "name" in item:
                    result.append(item)
            elif item is not None:
                # Convert string/other to dict - strip whitespace
                result.append({"name": str(item).strip()})
        return result

    # Single dict
    if isinstance(value, dict):
        return [value] if value and "name" in value else []

    # Single string - strip whitespace
    return [{"name": str(value).strip()}]


def normalize_member_list(
    value: Union[
        str,
        List[str],
        List[Dict[str, Any]],
        List[Union[str, Dict[str, Any]]],
        Dict[str, Any],
        None,
    ],
) -> List[Dict[str, str]]:
    """
    Normalize various input formats for 'member' fields in groups.

    Used for address groups, service groups, and other grouped resources.
    Similar to normalize_to_name_list but specifically for 'member' fields.

    Args:
        value: Can be:
            - String: 'addr1' → [{'name': 'addr1'}]
            - List of strings: ['addr1', 'addr2'] → [{'name': 'addr1'}, {'name': 'addr2'}]
            - Dict: {'name': 'addr1'} → [{'name': 'addr1'}]
            - List of dicts: [{'name': 'addr1'}, {'name': 'addr2'}] → unchanged
            - None: []

    Returns:
        List of dicts in FortiOS format
    """
    # For now, this is identical to normalize_to_name_list
    # But we keep it separate because member lists might need
    # different handling in the future (e.g., additional fields)
    return normalize_to_name_list(value)


def normalize_table_field(
    value: Union[
        str,
        List[str],
        List[Dict[str, Any]],
        List[Union[str, Dict[str, Any]]],
        Dict[str, Any],
        None,
    ],
    mkey: str = "name",
    required_fields: Union[List[str], None] = None,
    field_name: str = "field",
    example: Union[str, None] = None,
) -> List[Dict[str, Any]]:
    """
    Normalize table fields with schema-aware validation.

    This is the universal normalizer for all FortiOS table fields. It supports:
    - Any mkey (name, interface-name, id, value, etc.)
    - Single-field objects (flexible: string, list, or dict)
    - Multi-field objects (strict: dict only with validation)

    Args:
        value: Input value in any supported format
        mkey: The primary key field name from schema (default: "name")
        required_fields: List of required child field names from schema.
                        If more than 1, string format is NOT allowed.
        field_name: Field name for error messages
        example: Optional example string from schema to show in error messages.
                If None, will auto-generate from required_fields.

    Returns:
        List of dicts in FortiOS API format

    Raises:
        ValueError: If multi-field object receives string/list of strings
    """
    if value is None:
        return []

    # Determine if this is a multi-field object (requires dict format only)
    dict_only_mode = required_fields and len(required_fields) > 1

    # Generate example if not provided
    if not example and required_fields:
        # Build example from required fields
        example_parts = []
        for field in required_fields:
            # Generate appropriate example value based on field name
            if field in ("id", "index", "seq-num", "priority"):
                example_parts.append(f"'{field}': 1")
            elif field in ("ip", "ipaddr", "server"):
                example_parts.append(f"'{field}': '192.168.1.10'")
            elif field in ("port", "port-num"):
                example_parts.append(f"'{field}': 443")
            elif field in ("name", "interface-name", "domain", "address"):
                example_parts.append(f"'{field}': 'value'")
            else:
                # Generic example
                example_parts.append(f"'{field}': '...'")
        example = f"[{{{', '.join(example_parts)}}}]"

    # Handle list input
    if isinstance(value, list):
        if not value:
            return []

        # Process each item based on its actual type (handles mixed lists)
        result: List[Dict[str, Any]] = []
        for item in value:
            if isinstance(item, dict):
                # Dict - include if non-empty
                if item:
                    result.append(item)
            elif dict_only_mode:
                # Multi-field mode doesn't accept strings
                req_fields = required_fields or []
                error_msg = (
                    f"Field '{field_name}' requires dict format with keys: "
                    f"{', '.join(req_fields)}\n"
                    f"Example: {field_name}={example or '[{...}]'}"
                )
                raise ValueError(error_msg)
            else:
                # Single-field mode - convert string/primitive to dict
                result.append({mkey: str(item).strip()})
        return result

    # Single dict - wrap in list
    if isinstance(value, dict):
        return [value] if value else []

    # Single string/primitive
    if dict_only_mode:
        req_fields = required_fields or []
        error_msg = (
            f"Field '{field_name}' requires dict format with keys: "
            f"{', '.join(req_fields)}\n"
            f"Example: {field_name}={example or '[{...}]'}"
        )
        raise ValueError(error_msg)

    # Single required field - convert to dict, strip whitespace
    return [{mkey: str(value).strip()}]


# =============================================================================
# Multi-Value Option Field Normalizers
# =============================================================================

# Valid day names for schedule fields
VALID_DAYS = frozenset({
    "sunday", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "none"
})


def normalize_day_field(value: str | list[str] | None) -> str | None:
    """
    Normalize 'day' field to space-separated string format for FortiOS API.

    FortiOS schedule endpoints (e.g., firewall.schedule/recurring) expect
    day values as space-separated strings like "monday tuesday wednesday",
    not as lists.

    Args:
        value: Can be:
            - str: "monday tuesday" (pass-through, validated)
            - str: "monday, tuesday, wednesday" (comma-separated, converted)
            - list: ["monday", "tuesday", "wednesday"] (converted to space-separated)
            - None: returns None

    Returns:
        Space-separated string like "monday tuesday wednesday", or None

    Raises:
        ValueError: If invalid day names are provided
        TypeError: If value is not str, list, or None

    Examples:
        >>> normalize_day_field("monday tuesday")
        'monday tuesday'

        >>> normalize_day_field(["monday", "tuesday", "wednesday"])
        'monday tuesday wednesday'

        >>> normalize_day_field("monday, tuesday, wednesday")
        'monday tuesday wednesday'

        >>> normalize_day_field(None)
        None

        >>> normalize_day_field("MONDAY Tuesday")  # Case-insensitive
        'monday tuesday'
    """
    if value is None:
        return None

    if isinstance(value, list):
        # ["monday", "tuesday"] -> "monday tuesday"
        days = [str(d).strip().lower() for d in value if d]
    elif isinstance(value, str):
        # Handle comma-separated: "monday, tuesday" -> ["monday", "tuesday"]
        if "," in value:
            days = [d.strip().lower() for d in value.split(",") if d.strip()]
        else:
            # Already space-separated or single day
            days = [d.strip().lower() for d in value.split() if d.strip()]
    else:
        raise TypeError(f"Expected str or list, got {type(value).__name__}")

    if not days:
        return None

    # Validate day names
    invalid = [d for d in days if d not in VALID_DAYS]
    if invalid:
        raise ValueError(
            f"Invalid day(s): {invalid}. "
            f"Valid options: {sorted(VALID_DAYS)}"
        )

    return " ".join(days)


# =============================================================================
# Simple Array Field Normalizers
# =============================================================================


def normalize_to_string_list(
    value: int | str | list[int | str] | None,
) -> list[str] | None:
    """
    Normalize various input formats to a simple list of strings.

    Used for array fields like 'id_list' that accept lists of IDs/values
    but don't use the [{'name': '...'}] dict format.

    Args:
        value: Can be:
            - int: 5 → ['5']
            - str: '5' → ['5']
            - list of ints: [1, 2, 3] → ['1', '2', '3']
            - list of strings: ['1', '2', '3'] → ['1', '2', '3']
            - mixed list: [1, '2', 3] → ['1', '2', '3']
            - None: None

    Returns:
        List of strings, or None if input is None

    Examples:
        >>> normalize_to_string_list(5)
        ['5']

        >>> normalize_to_string_list('5')
        ['5']

        >>> normalize_to_string_list([1, 2, 3])
        ['1', '2', '3']

        >>> normalize_to_string_list(['1', '2', '3'])
        ['1', '2', '3']

        >>> normalize_to_string_list([1, '2', 3])
        ['1', '2', '3']

        >>> normalize_to_string_list(None)
        None
    """
    if value is None:
        return None

    # Already a list - convert all items to strings
    if isinstance(value, list):
        if not value:
            return []
        return [str(item).strip() for item in value if item is not None]

    # Single value (int or str) - convert to list with single string
    return [str(value).strip()]
