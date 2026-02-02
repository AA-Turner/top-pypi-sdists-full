"""
Central validation functions for endpoint validators.

These functions are used by all auto-generated endpoint validator modules
to avoid code duplication across 1,062+ helper files.

Each function is generic and works with any endpoint by accepting the
endpoint-specific constants as parameters.
"""

from typing import Any


def validate_required_fields(
    payload: dict,
    required_fields: list[str],
    field_descriptions: dict[str, str],
) -> tuple[bool, str | None]:
    """
    Validate that all required fields are present in payload.

    Generic validator used by all POST endpoints to check required fields.

    Args:
        payload: The request payload to validate
        required_fields: List of field names that must be present
        field_descriptions: Dict mapping field names to their descriptions

    Returns:
        Tuple of (is_valid, error_message)
        - (True, None) if all required fields present
        - (False, error_msg) with detailed error if fields missing
    """
    missing_fields = []
    for field in required_fields:
        if field not in payload:
            missing_fields.append(field)

    if missing_fields:
        # Build enhanced error message
        error_parts = [
            f"Missing required field(s): {', '.join(missing_fields)}"
        ]

        # Add descriptions for first few missing fields
        for field in missing_fields[:3]:
            desc = field_descriptions.get(field)
            if desc:
                error_parts.append(f"  • {field}: {desc}")

        if len(missing_fields) > 3:
            error_parts.append(f"  ... and {len(missing_fields) - 3} more")

        return (False, "\n".join(error_parts))

    return (True, None)


def validate_enum_field(
    field_name: str,
    value: Any,
    valid_values: list[str],
    field_descriptions: dict[str, str],
) -> tuple[bool, str | None]:
    """
    Validate that a field value is one of the allowed enum values.

    Generic enum validator used by POST/PUT endpoints for option fields.

    Args:
        field_name: Name of the field being validated
        value: The value to validate
        valid_values: List of valid enum values
        field_descriptions: Dict mapping field names to descriptions

    Returns:
        Tuple of (is_valid, error_message)
        - (True, None) if value is valid
        - (False, error_msg) with detailed error if invalid

    Example:
        >>> is_valid, error = validate_enum_field(
        ...     field_name="status",
        ...     value="invalid",
        ...     valid_values=["enable", "disable"],
        ...     field_descriptions={"status": "Enable/disable entry"}
        ... )
        >>> print(error)
        Invalid value for 'status': 'invalid'
          → Description: Enable/disable entry
          → Valid options: 'enable', 'disable'
          → Example: status='enable'
    """
    if value not in valid_values:
        desc = field_descriptions.get(field_name, "")
        error_msg = f"Invalid value for '{field_name}': '{value}'"

        if desc:
            error_msg += f"\n  → Description: {desc}"

        error_msg += (
            f"\n  → Valid options: {', '.join(repr(v) for v in valid_values)}"
        )

        if valid_values:
            error_msg += f"\n  → Example: {field_name}='{valid_values[0]}'"

        return (False, error_msg)

    return (True, None)


def validate_query_parameter(
    param_name: str,
    value: Any,
    valid_values: list[str],
) -> tuple[bool, str | None]:
    """
    Validate that a query parameter value is allowed.

    Generic query param validator used by GET endpoints.

    Args:
        param_name: Name of the query parameter
        value: The value to validate
        valid_values: List of valid parameter values

    Returns:
        Tuple of (is_valid, error_message)
        - (True, None) if value is valid
        - (False, error_msg) if invalid

    Example:
        >>> is_valid, error = validate_query_parameter(
        ...     param_name="action",
        ...     value="invalid",
        ...     valid_values=["default", "schema"]
        ... )
        >>> print(error)
        Invalid query parameter 'action'='invalid'. Must be one of: default, schema
    """
    if value and value not in valid_values:
        return (
            False,
            f"Invalid query parameter '{param_name}'='{value}'. "
            f"Must be one of: {', '.join(valid_values)}",
        )

    return (True, None)


def validate_multiple_enums(
    payload: dict,
    enum_fields: dict[str, list[str]],
    field_descriptions: dict[str, str],
) -> tuple[bool, str | None]:
    """
    Validate multiple enum fields at once.

    Convenience function to validate several enum fields in a single call.
    Used by POST/PUT validators to reduce boilerplate.

    Args:
        payload: The request payload
        enum_fields: Dict mapping field names to their valid values
        field_descriptions: Dict mapping field names to descriptions

    Returns:
        Tuple of (is_valid, error_message)
        - (True, None) if all enum fields valid
        - (False, error_msg) on first validation failure

    Example:
        >>> is_valid, error = validate_multiple_enums(
        ...     payload={"status": "enable", "type": "invalid"},
        ...     enum_fields={
        ...         "status": ["enable", "disable"],
        ...         "type": ["type1", "type2"]
        ...     },
        ...     field_descriptions={"status": "Status", "type": "Type"}
        ... )
    """
    for field_name, valid_values in enum_fields.items():
        if field_name in payload:
            is_valid, error = validate_enum_field(
                field_name,
                payload[field_name],
                valid_values,
                field_descriptions,
            )
            if not is_valid:
                return (False, error)

    return (True, None)


def validate_multiple_query_params(
    params: dict[str, Any],
    valid_params: dict[str, list[str]],
) -> tuple[bool, str | None]:
    """
    Validate multiple query parameters at once.

    Convenience function to validate several query params in a single call.
    Used by GET validators to reduce boilerplate.

    Args:
        params: Dict of query parameters to validate
        valid_params: Dict mapping param names to their valid values

    Returns:
        Tuple of (is_valid, error_message)
        - (True, None) if all params valid
        - (False, error_msg) on first validation failure

    Example:
        >>> is_valid, error = validate_multiple_query_params(
        ...     params={"action": "schema", "format": "invalid"},
        ...     valid_params={
        ...         "action": ["default", "schema"],
        ...         "format": ["json", "xml"]
        ...     }
        ... )
    """
    for param_name, valid_values in valid_params.items():
        if param_name in params:
            is_valid, error = validate_query_parameter(
                param_name,
                params[param_name],
                valid_values,
            )
            if not is_valid:
                return (False, error)

    return (True, None)
