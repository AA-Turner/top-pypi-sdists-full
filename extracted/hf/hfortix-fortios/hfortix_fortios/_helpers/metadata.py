"""
Shared metadata accessor functions for all validation helpers.

These functions are used by all endpoint-specific validator modules to access
field metadata (descriptions, types, constraints, defaults, options, etc.).

Instead of duplicating these ~8KB of code in every helper file, they're centralized here.
"""

from typing import Any


def get_field_description(
    field_descriptions: dict[str, str],
    field_name: str,
) -> str | None:
    """
    Get description/help text for a field.

    Args:
        field_descriptions: FIELD_DESCRIPTIONS dict from validator module
        field_name: Name of the field

    Returns:
        Description text or None if field doesn't exist

    Example:
        >>> desc = get_field_description(FIELD_DESCRIPTIONS, "name")
        >>> print(desc)
    """
    return field_descriptions.get(field_name)


def get_field_type(
    field_types: dict[str, str],
    field_name: str,
) -> str | None:
    """
    Get the type of a field.

    Args:
        field_types: FIELD_TYPES dict from validator module
        field_name: Name of the field

    Returns:
        Field type (e.g., "string", "integer", "option") or None

    Example:
        >>> field_type = get_field_type(FIELD_TYPES, "status")
        >>> print(field_type)  # "option"
    """
    return field_types.get(field_name)


def get_field_constraints(
    field_constraints: dict[str, dict[str, Any]],
    field_name: str,
) -> dict[str, Any] | None:
    """
    Get constraints for a field (min/max values, string length).

    Args:
        field_constraints: FIELD_CONSTRAINTS dict from validator module
        field_name: Name of the field

    Returns:
        Constraint dict or None

    Example:
        >>> constraints = get_field_constraints(FIELD_CONSTRAINTS, "port")
        >>> print(constraints)  # {"type": "integer", "min": 1, "max": 65535}
    """
    return field_constraints.get(field_name)


def get_field_default(
    fields_with_defaults: dict[str, Any],
    field_name: str,
) -> Any | None:
    """
    Get default value for a field.

    Args:
        fields_with_defaults: FIELDS_WITH_DEFAULTS dict from validator module
        field_name: Name of the field

    Returns:
        Default value or None if no default

    Example:
        >>> default = get_field_default(FIELDS_WITH_DEFAULTS, "status")
        >>> print(default)  # "enable"
    """
    return fields_with_defaults.get(field_name)


def get_field_options(
    globals_dict: dict[str, Any],
    field_name: str,
) -> list[str] | None:
    """
    Get valid enum options for a field.

    Args:
        globals_dict: globals() dict from validator module
        field_name: Name of the field

    Returns:
        List of valid values or None if not an enum field

    Example:
        >>> options = get_field_options(globals(), "status")
        >>> print(options)  # ["enable", "disable"]
    """
    # Construct the constant name from field name
    # Replace all non-alphanumeric characters with underscores for valid Python identifiers
    import re

    safe_name = re.sub(r"[^a-zA-Z0-9]", "_", field_name)
    constant_name = f"VALID_BODY_{safe_name.upper()}"
    return globals_dict.get(constant_name)


def get_nested_schema(
    nested_schemas: dict[str, dict[str, Any]],
    field_name: str,
) -> dict[str, Any] | None:
    """
    Get schema for nested table/list fields.

    Args:
        nested_schemas: NESTED_SCHEMAS dict from validator module
        field_name: Name of the parent field

    Returns:
        Dict mapping child field names to their metadata

    Example:
        >>> nested = get_nested_schema(NESTED_SCHEMAS, "members")
        >>> if nested:
        ...     for child_field, child_meta in nested.items():
        ...         print(f"{child_field}: {child_meta['type']}")
    """
    return nested_schemas.get(field_name)


def get_all_fields(
    field_types: dict[str, str],
) -> list[str]:
    """
    Get list of all field names.

    Args:
        field_types: FIELD_TYPES dict from validator module

    Returns:
        List of all field names in the schema

    Example:
        >>> fields = get_all_fields(FIELD_TYPES)
        >>> print(len(fields))
    """
    return list(field_types.keys())


def get_field_metadata(
    field_types: dict[str, str],
    field_descriptions: dict[str, str],
    field_constraints: dict[str, dict[str, Any]],
    fields_with_defaults: dict[str, Any],
    required_fields: list[str],
    nested_schemas: dict[str, dict[str, Any]],
    globals_dict: dict[str, Any],
    field_name: str,
) -> dict[str, Any] | None:
    """
    Get complete metadata for a field (type, description, constraints, defaults, options).

    Args:
        field_types: FIELD_TYPES dict from validator module
        field_descriptions: FIELD_DESCRIPTIONS dict from validator module
        field_constraints: FIELD_CONSTRAINTS dict from validator module
        fields_with_defaults: FIELDS_WITH_DEFAULTS dict from validator module
        required_fields: REQUIRED_FIELDS list from validator module
        nested_schemas: NESTED_SCHEMAS dict from validator module
        globals_dict: globals() dict from validator module
        field_name: Name of the field

    Returns:
        Dict with all available metadata or None if field doesn't exist

    Example:
        >>> meta = get_field_metadata(
        ...     FIELD_TYPES, FIELD_DESCRIPTIONS, FIELD_CONSTRAINTS,
        ...     FIELDS_WITH_DEFAULTS, REQUIRED_FIELDS, NESTED_SCHEMAS,
        ...     globals(), "status"
        ... )
        >>> print(meta)
        >>> # {
        >>> #   "type": "option",
        >>> #   "description": "Enable/disable this feature",
        >>> #   "default": "enable",
        >>> #   "options": ["enable", "disable"]
        >>> # }
    """
    if field_name not in field_types:
        return None

    metadata: dict[str, Any] = {
        "name": field_name,
        "type": field_types[field_name],
    }

    # Add description if available
    if field_name in field_descriptions:
        metadata["description"] = field_descriptions[field_name]

    # Add constraints if available
    if field_name in field_constraints:
        metadata["constraints"] = field_constraints[field_name]

    # Add default if available
    if field_name in fields_with_defaults:
        metadata["default"] = fields_with_defaults[field_name]

    # Add required flag
    metadata["required"] = field_name in required_fields

    # Add options if available
    options = get_field_options(globals_dict, field_name)
    if options:
        metadata["options"] = options

    # Add nested schema if available
    nested = get_nested_schema(nested_schemas, field_name)
    if nested:
        metadata["nested_schema"] = nested

    return metadata


def validate_field_value(
    field_types: dict[str, str],
    field_descriptions: dict[str, str],
    field_constraints: dict[str, dict[str, Any]],
    globals_dict: dict[str, Any],
    field_name: str,
    value: Any,
) -> tuple[bool, str | None]:
    """
    Validate a single field value against its constraints.

    Args:
        field_types: FIELD_TYPES dict from validator module
        field_descriptions: FIELD_DESCRIPTIONS dict from validator module
        field_constraints: FIELD_CONSTRAINTS dict from validator module
        globals_dict: globals() dict from validator module
        field_name: Name of the field
        value: Value to validate

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> is_valid, error = validate_field_value(
        ...     FIELD_TYPES, FIELD_DESCRIPTIONS, FIELD_CONSTRAINTS,
        ...     globals(), "status", "enable"
        ... )
        >>> if not is_valid:
        ...     print(error)
    """
    # Get field metadata
    field_type = get_field_type(field_types, field_name)
    if field_type is None:
        return (
            False,
            f"Unknown field: '{field_name}' (not defined in schema)",
        )

    # Get field description for better error context
    description = get_field_description(field_descriptions, field_name)

    # Validate enum values
    options = get_field_options(globals_dict, field_name)
    if options and value not in options:
        error_msg = f"Invalid value for '{field_name}': {repr(value)}"
        if description:
            error_msg += f"\n  → Description: {description}"
        error_msg += (
            f"\n  → Valid options: {', '.join(repr(v) for v in options)}"
        )
        if options:
            error_msg += f"\n  → Example: {field_name}={repr(options[0])}"
        return (False, error_msg)

    # Validate constraints
    constraints = get_field_constraints(field_constraints, field_name)
    if constraints:
        constraint_type = constraints.get("type")

        if constraint_type == "integer":
            if not isinstance(value, int):
                error_msg = f"Field '{field_name}' must be an integer"
                if description:
                    error_msg += f"\n  → Description: {description}"
                error_msg += f"\n  → You provided: {type(value).__name__} = {repr(value)}"
                return (False, error_msg)

            min_val = constraints.get("min")
            max_val = constraints.get("max")

            if min_val is not None and value < min_val:
                error_msg = f"Field '{field_name}' value {value} is below minimum {min_val}"
                if description:
                    error_msg += f"\n  → Description: {description}"
                if max_val is not None:
                    error_msg += f"\n  → Valid range: {min_val} to {max_val}"
                return (False, error_msg)

            if max_val is not None and value > max_val:
                error_msg = f"Field '{field_name}' value {value} exceeds maximum {max_val}"
                if description:
                    error_msg += f"\n  → Description: {description}"
                if min_val is not None:
                    error_msg += f"\n  → Valid range: {min_val} to {max_val}"
                return (False, error_msg)

        elif constraint_type == "string":
            if not isinstance(value, str):
                error_msg = f"Field '{field_name}' must be a string"
                if description:
                    error_msg += f"\n  → Description: {description}"
                error_msg += f"\n  → You provided: {type(value).__name__} = {repr(value)}"
                return (False, error_msg)

            max_length = constraints.get("max_length")
            if max_length and len(value) > max_length:
                error_msg = f"Field '{field_name}' length {len(value)} exceeds maximum {max_length}"
                if description:
                    error_msg += f"\n  → Description: {description}"
                error_msg += f"\n  → Your value: {repr(value[:50])}{'...' if len(value) > 50 else ''}"
                return (False, error_msg)

    return (True, None)
