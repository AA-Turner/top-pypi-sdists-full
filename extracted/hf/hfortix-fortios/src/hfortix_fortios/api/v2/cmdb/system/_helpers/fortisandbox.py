"""Validation helpers for system/fortisandbox - Auto-generated"""

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
    "server",  # Server IP address or FQDN of the remote FortiSandbox.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disable",
    "forticloud": "disable",
    "inline-scan": "disable",
    "server": "",
    "source-ip": "",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
    "enc-algorithm": "default",
    "ssl-min-proto-version": "default",
    "email": "",
    "ca": "",
    "cn": "",
    "certificate-verification": "disable",
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
    "status": "option",  # Enable/disable FortiSandbox.
    "forticloud": "option",  # Enable/disable FortiSandbox Cloud.
    "inline-scan": "option",  # Enable/disable FortiSandbox inline scan.
    "server": "string",  # Server IP address or FQDN of the remote FortiSandbox.
    "source-ip": "string",  # Source IP address for communications to FortiSandbox.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
    "enc-algorithm": "option",  # Configure the level of SSL protection for secure communication with FortiSandbox
    "ssl-min-proto-version": "option",  # Minimum supported protocol version for SSL/TLS connections (default is to follow
    "email": "string",  # Notifier email address.
    "ca": "string",  # The CA that signs remote FortiSandbox certificate, empty for no check.
    "cn": "string",  # The CN of remote server certificate, case sensitive, empty for no check.
    "certificate-verification": "option",  # Enable/disable identity verification of FortiSandbox by use of certificate.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable FortiSandbox.",
    "forticloud": "Enable/disable FortiSandbox Cloud.",
    "inline-scan": "Enable/disable FortiSandbox inline scan.",
    "server": "Server IP address or FQDN of the remote FortiSandbox.",
    "source-ip": "Source IP address for communications to FortiSandbox.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
    "enc-algorithm": "Configure the level of SSL protection for secure communication with FortiSandbox.",
    "ssl-min-proto-version": "Minimum supported protocol version for SSL/TLS connections (default is to follow system global setting).",
    "email": "Notifier email address.",
    "ca": "The CA that signs remote FortiSandbox certificate, empty for no check.",
    "cn": "The CN of remote server certificate, case sensitive, empty for no check.",
    "certificate-verification": "Enable/disable identity verification of FortiSandbox by use of certificate.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "server": {"type": "string", "max_length": 63},
    "source-ip": {"type": "string", "max_length": 63},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
    "email": {"type": "string", "max_length": 63},
    "ca": {"type": "string", "max_length": 79},
    "cn": {"type": "string", "max_length": 127},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_FORTICLOUD = [
    "enable",
    "disable",
]
VALID_BODY_INLINE_SCAN = [
    "enable",
    "disable",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_ENC_ALGORITHM = [
    "default",
    "high",
    "low",
]
VALID_BODY_SSL_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_CERTIFICATE_VERIFICATION = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_fortisandbox_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/fortisandbox."""
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


def validate_system_fortisandbox_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/fortisandbox object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticloud" in payload:
        is_valid, error = _validate_enum_field(
            "forticloud",
            payload["forticloud"],
            VALID_BODY_FORTICLOUD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "inline-scan" in payload:
        is_valid, error = _validate_enum_field(
            "inline-scan",
            payload["inline-scan"],
            VALID_BODY_INLINE_SCAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enc-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "enc-algorithm",
            payload["enc-algorithm"],
            VALID_BODY_ENC_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "certificate-verification" in payload:
        is_valid, error = _validate_enum_field(
            "certificate-verification",
            payload["certificate-verification"],
            VALID_BODY_CERTIFICATE_VERIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_fortisandbox_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/fortisandbox."""
    # Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticloud" in payload:
        is_valid, error = _validate_enum_field(
            "forticloud",
            payload["forticloud"],
            VALID_BODY_FORTICLOUD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "inline-scan" in payload:
        is_valid, error = _validate_enum_field(
            "inline-scan",
            payload["inline-scan"],
            VALID_BODY_INLINE_SCAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enc-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "enc-algorithm",
            payload["enc-algorithm"],
            VALID_BODY_ENC_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "certificate-verification" in payload:
        is_valid, error = _validate_enum_field(
            "certificate-verification",
            payload["certificate-verification"],
            VALID_BODY_CERTIFICATE_VERIFICATION,
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
    "endpoint": "system/fortisandbox",
    "category": "cmdb",
    "api_path": "system/fortisandbox",
    "help": "Configure FortiSandbox.",
    "total_fields": 14,
    "required_fields_count": 2,
    "fields_with_defaults_count": 14,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
