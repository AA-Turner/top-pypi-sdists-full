"""Validation helpers for antivirus/quarantine - Auto-generated"""

from typing import Any, TypedDict, Literal
from typing_extensions import NotRequired

# Import common validators from central _helpers module
from hfortix_fortios._helpers import (
    validate_enable_disable,
    validate_integer_range,
    validate_string_length,
    validate_port_number,
    validate_ip_address,
    validate_ipv6_address,
    validate_mac_address,
)

# Import central validation functions (avoid duplication across 1,062 files)
from hfortix_fortios._helpers.validation import (
    validate_required_fields as _validate_required_fields,
    validate_enum_field as _validate_enum_field,
    validate_query_parameter as _validate_query_parameter,
)

# ============================================================================
# Required Fields Validation
# Auto-generated from schema
# ============================================================================

# ⚠️  IMPORTANT: FortiOS schemas have known issues with required field marking:

# Do NOT use this list for strict validation - test with the actual FortiOS API!

# Fields marked as required (after filtering false positives)
REQUIRED_FIELDS = [
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "agelimit": 0,
    "maxfilesize": 0,
    "quarantine-quota": 0,
    "drop-infected": "",
    "store-infected": "imap smtp pop3 http ftp nntp imaps smtps pop3s https ftps mapi cifs ssh",
    "drop-machine-learning": "",
    "store-machine-learning": "imap smtp pop3 http ftp nntp imaps smtps pop3s https ftps mapi cifs ssh",
    "lowspace": "ovrw-old",
    "destination": "disk",
}

# ============================================================================
# Deprecated Fields
# Auto-generated from schema - warns users about deprecated fields
# ============================================================================

# Deprecated fields with migration guidance
DEPRECATED_FIELDS = {
}

# ============================================================================
# Field Metadata (Type Information & Descriptions)
# Auto-generated from schema - use for IDE autocomplete and documentation
# ============================================================================

# Field types mapping
FIELD_TYPES = {
    "agelimit": "integer",  # Age limit for quarantined files (0 - 479 hours, 0 means forever).
    "maxfilesize": "integer",  # Maximum file size to quarantine (0 - 500 Mbytes, 0 means unlimited).
    "quarantine-quota": "integer",  # The amount of disk space to reserve for quarantining files (0 - 4294967295 Mbyte
    "drop-infected": "option",  # Do not quarantine infected files found in sessions using the selected protocols.
    "store-infected": "option",  # Quarantine infected files found in sessions using the selected protocols.
    "drop-machine-learning": "option",  # Do not quarantine files detected by machine learning found in sessions using the
    "store-machine-learning": "option",  # Quarantine files detected by machine learning found in sessions using the select
    "lowspace": "option",  # Select the method for handling additional files when running low on disk space.
    "destination": "option",  # Choose whether to quarantine files to the FortiGate disk or to FortiAnalyzer or 
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "agelimit": "Age limit for quarantined files (0 - 479 hours, 0 means forever).",
    "maxfilesize": "Maximum file size to quarantine (0 - 500 Mbytes, 0 means unlimited).",
    "quarantine-quota": "The amount of disk space to reserve for quarantining files (0 - 4294967295 Mbytes, 0 means unlimited and depends on disk space).",
    "drop-infected": "Do not quarantine infected files found in sessions using the selected protocols. Dropped files are deleted instead of being quarantined.",
    "store-infected": "Quarantine infected files found in sessions using the selected protocols.",
    "drop-machine-learning": "Do not quarantine files detected by machine learning found in sessions using the selected protocols. Dropped files are deleted instead of being quarantined.",
    "store-machine-learning": "Quarantine files detected by machine learning found in sessions using the selected protocols.",
    "lowspace": "Select the method for handling additional files when running low on disk space.",
    "destination": "Choose whether to quarantine files to the FortiGate disk or to FortiAnalyzer or to delete them instead of quarantining them.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "agelimit": {"type": "integer", "min": 0, "max": 479},
    "maxfilesize": {"type": "integer", "min": 0, "max": 500},
    "quarantine-quota": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_DROP_INFECTED = [
    "imap",
    "smtp",
    "pop3",
    "http",
    "ftp",
    "nntp",
    "imaps",
    "smtps",
    "pop3s",
    "https",
    "ftps",
    "mapi",
    "cifs",
    "ssh",
]
VALID_BODY_STORE_INFECTED = [
    "imap",
    "smtp",
    "pop3",
    "http",
    "ftp",
    "nntp",
    "imaps",
    "smtps",
    "pop3s",
    "https",
    "ftps",
    "mapi",
    "cifs",
    "ssh",
]
VALID_BODY_DROP_MACHINE_LEARNING = [
    "imap",
    "smtp",
    "pop3",
    "http",
    "ftp",
    "nntp",
    "imaps",
    "smtps",
    "pop3s",
    "https",
    "ftps",
    "mapi",
    "cifs",
    "ssh",
]
VALID_BODY_STORE_MACHINE_LEARNING = [
    "imap",
    "smtp",
    "pop3",
    "http",
    "ftp",
    "nntp",
    "imaps",
    "smtps",
    "pop3s",
    "https",
    "ftps",
    "mapi",
    "cifs",
    "ssh",
]
VALID_BODY_LOWSPACE = [
    "drop-new",
    "ovrw-old",
]
VALID_BODY_DESTINATION = [
    "NULL",
    "disk",
    "FortiAnalyzer",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_antivirus_quarantine_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for antivirus/quarantine."""
    # Validate query parameters using central function
    if "action" in params:
        is_valid, error = _validate_query_parameter(
            "action",
            params.get("action"),
            VALID_QUERY_ACTION
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# POST Validation
# ============================================================================


def validate_antivirus_quarantine_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new antivirus/quarantine object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "drop-infected" in payload:
        is_valid, error = _validate_enum_field(
            "drop-infected",
            payload["drop-infected"],
            VALID_BODY_DROP_INFECTED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "store-infected" in payload:
        is_valid, error = _validate_enum_field(
            "store-infected",
            payload["store-infected"],
            VALID_BODY_STORE_INFECTED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "drop-machine-learning" in payload:
        is_valid, error = _validate_enum_field(
            "drop-machine-learning",
            payload["drop-machine-learning"],
            VALID_BODY_DROP_MACHINE_LEARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "store-machine-learning" in payload:
        is_valid, error = _validate_enum_field(
            "store-machine-learning",
            payload["store-machine-learning"],
            VALID_BODY_STORE_MACHINE_LEARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lowspace" in payload:
        is_valid, error = _validate_enum_field(
            "lowspace",
            payload["lowspace"],
            VALID_BODY_LOWSPACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "destination" in payload:
        is_valid, error = _validate_enum_field(
            "destination",
            payload["destination"],
            VALID_BODY_DESTINATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_antivirus_quarantine_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update antivirus/quarantine."""
    # Validate enum values using central function
    if "drop-infected" in payload:
        is_valid, error = _validate_enum_field(
            "drop-infected",
            payload["drop-infected"],
            VALID_BODY_DROP_INFECTED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "store-infected" in payload:
        is_valid, error = _validate_enum_field(
            "store-infected",
            payload["store-infected"],
            VALID_BODY_STORE_INFECTED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "drop-machine-learning" in payload:
        is_valid, error = _validate_enum_field(
            "drop-machine-learning",
            payload["drop-machine-learning"],
            VALID_BODY_DROP_MACHINE_LEARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "store-machine-learning" in payload:
        is_valid, error = _validate_enum_field(
            "store-machine-learning",
            payload["store-machine-learning"],
            VALID_BODY_STORE_MACHINE_LEARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lowspace" in payload:
        is_valid, error = _validate_enum_field(
            "lowspace",
            payload["lowspace"],
            VALID_BODY_LOWSPACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "destination" in payload:
        is_valid, error = _validate_enum_field(
            "destination",
            payload["destination"],
            VALID_BODY_DESTINATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# Metadata Access Functions
# Imported from central module to avoid duplication across 1,062 files
# Bound to this endpoint's data using functools.partial (saves ~7KB per file)
# ============================================================================

from functools import partial
from hfortix_fortios._helpers.metadata import (
    get_field_description,
    get_field_type,
    get_field_constraints,
    get_field_default,
    get_field_options,
    get_nested_schema,
    get_all_fields,
    get_field_metadata,
    validate_field_value,
)

# Bind module-specific data to central functions using partial application
get_field_description = partial(get_field_description, FIELD_DESCRIPTIONS)
get_field_type = partial(get_field_type, FIELD_TYPES)
get_field_constraints = partial(get_field_constraints, FIELD_CONSTRAINTS)
get_field_default = partial(get_field_default, FIELDS_WITH_DEFAULTS)
get_field_options = partial(get_field_options, globals())
get_nested_schema = partial(get_nested_schema, NESTED_SCHEMAS)
get_all_fields = partial(get_all_fields, FIELD_TYPES)
get_field_metadata = partial(get_field_metadata, FIELD_TYPES, FIELD_DESCRIPTIONS, 
                             FIELD_CONSTRAINTS, FIELDS_WITH_DEFAULTS, REQUIRED_FIELDS,
                             NESTED_SCHEMAS, globals())
validate_field_value = partial(validate_field_value, FIELD_TYPES, FIELD_DESCRIPTIONS,
                               FIELD_CONSTRAINTS, globals())


# ============================================================================
# Schema Information
# Metadata about this endpoint schema
# ============================================================================

SCHEMA_INFO = {
    "endpoint": "antivirus/quarantine",
    "category": "cmdb",
    "api_path": "antivirus/quarantine",
    "help": "Configure quarantine options.",
    "total_fields": 9,
    "required_fields_count": 0,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
