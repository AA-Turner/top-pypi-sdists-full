"""Validation helpers for firewall/local_in_policy - Auto-generated"""

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
    "intf",  # Incoming interface name from available options.
    "srcaddr",  # Source address object from available options.
    "dstaddr",  # Destination address object from available options.
    "service",  # Service object from available options.
    "schedule",  # Schedule object from available options.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "policyid": 0,
    "uuid": "00000000-0000-0000-0000-000000000000",
    "ha-mgmt-intf-only": "disable",
    "srcaddr-negate": "disable",
    "internet-service-src": "disable",
    "dstaddr-negate": "disable",
    "action": "deny",
    "service-negate": "disable",
    "internet-service-src-negate": "disable",
    "schedule": "",
    "status": "enable",
    "virtual-patch": "disable",
    "logtraffic": "disable",
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
    "policyid": "integer",  # User defined local in policy ID.
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "ha-mgmt-intf-only": "option",  # Enable/disable dedicating the HA management interface only for local-in policy.
    "intf": "string",  # Incoming interface name from available options.
    "srcaddr": "string",  # Source address object from available options.
    "srcaddr-negate": "option",  # When enabled srcaddr specifies what the source address must NOT be.
    "dstaddr": "string",  # Destination address object from available options.
    "internet-service-src": "option",  # Enable/disable use of Internet Services in source for this local-in policy. If e
    "internet-service-src-name": "string",  # Internet Service source name.
    "internet-service-src-group": "string",  # Internet Service source group name.
    "internet-service-src-custom": "string",  # Custom Internet Service source name.
    "internet-service-src-custom-group": "string",  # Custom Internet Service source group name.
    "internet-service-src-fortiguard": "string",  # FortiGuard Internet Service source name.
    "dstaddr-negate": "option",  # When enabled dstaddr specifies what the destination address must NOT be.
    "action": "option",  # Action performed on traffic matching the policy (default = deny).
    "service": "string",  # Service object from available options.
    "service-negate": "option",  # When enabled service specifies what the service must NOT be.
    "internet-service-src-negate": "option",  # When enabled internet-service-src specifies what the service must NOT be.
    "schedule": "string",  # Schedule object from available options.
    "status": "option",  # Enable/disable this local-in policy.
    "virtual-patch": "option",  # Enable/disable virtual patching.
    "logtraffic": "option",  # Enable/disable local-in traffic logging.
    "comments": "var-string",  # Comment.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "policyid": "User defined local in policy ID.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "ha-mgmt-intf-only": "Enable/disable dedicating the HA management interface only for local-in policy.",
    "intf": "Incoming interface name from available options.",
    "srcaddr": "Source address object from available options.",
    "srcaddr-negate": "When enabled srcaddr specifies what the source address must NOT be.",
    "dstaddr": "Destination address object from available options.",
    "internet-service-src": "Enable/disable use of Internet Services in source for this local-in policy. If enabled, source address is not used.",
    "internet-service-src-name": "Internet Service source name.",
    "internet-service-src-group": "Internet Service source group name.",
    "internet-service-src-custom": "Custom Internet Service source name.",
    "internet-service-src-custom-group": "Custom Internet Service source group name.",
    "internet-service-src-fortiguard": "FortiGuard Internet Service source name.",
    "dstaddr-negate": "When enabled dstaddr specifies what the destination address must NOT be.",
    "action": "Action performed on traffic matching the policy (default = deny).",
    "service": "Service object from available options.",
    "service-negate": "When enabled service specifies what the service must NOT be.",
    "internet-service-src-negate": "When enabled internet-service-src specifies what the service must NOT be.",
    "schedule": "Schedule object from available options.",
    "status": "Enable/disable this local-in policy.",
    "virtual-patch": "Enable/disable virtual patching.",
    "logtraffic": "Enable/disable local-in traffic logging.",
    "comments": "Comment.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "policyid": {"type": "integer", "min": 0, "max": 4294967295},
    "schedule": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "intf": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "srcaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-name": {
        "name": {
            "type": "string",
            "help": "Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "service": {
        "name": {
            "type": "string",
            "help": "Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_HA_MGMT_INTF_ONLY = [
    "enable",
    "disable",
]
VALID_BODY_SRCADDR_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_SRC = [
    "enable",
    "disable",
]
VALID_BODY_DSTADDR_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_ACTION = [
    "accept",
    "deny",
]
VALID_BODY_SERVICE_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_SRC_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_VIRTUAL_PATCH = [
    "enable",
    "disable",
]
VALID_BODY_LOGTRAFFIC = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_local_in_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/local_in_policy."""
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


def validate_firewall_local_in_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/local_in_policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ha-mgmt-intf-only" in payload:
        is_valid, error = _validate_enum_field(
            "ha-mgmt-intf-only",
            payload["ha-mgmt-intf-only"],
            VALID_BODY_HA_MGMT_INTF_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "srcaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr-negate",
            payload["srcaddr-negate"],
            VALID_BODY_SRCADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src",
            payload["internet-service-src"],
            VALID_BODY_INTERNET_SERVICE_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr-negate",
            payload["dstaddr-negate"],
            VALID_BODY_DSTADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "service-negate",
            payload["service-negate"],
            VALID_BODY_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src-negate",
            payload["internet-service-src-negate"],
            VALID_BODY_INTERNET_SERVICE_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "virtual-patch" in payload:
        is_valid, error = _validate_enum_field(
            "virtual-patch",
            payload["virtual-patch"],
            VALID_BODY_VIRTUAL_PATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_local_in_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/local_in_policy."""
    # Validate enum values using central function
    if "ha-mgmt-intf-only" in payload:
        is_valid, error = _validate_enum_field(
            "ha-mgmt-intf-only",
            payload["ha-mgmt-intf-only"],
            VALID_BODY_HA_MGMT_INTF_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "srcaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr-negate",
            payload["srcaddr-negate"],
            VALID_BODY_SRCADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src",
            payload["internet-service-src"],
            VALID_BODY_INTERNET_SERVICE_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr-negate",
            payload["dstaddr-negate"],
            VALID_BODY_DSTADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "service-negate",
            payload["service-negate"],
            VALID_BODY_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src-negate",
            payload["internet-service-src-negate"],
            VALID_BODY_INTERNET_SERVICE_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "virtual-patch" in payload:
        is_valid, error = _validate_enum_field(
            "virtual-patch",
            payload["virtual-patch"],
            VALID_BODY_VIRTUAL_PATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
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
    "endpoint": "firewall/local_in_policy",
    "category": "cmdb",
    "api_path": "firewall/local-in-policy",
    "mkey": "policyid",
    "mkey_type": "integer",
    "help": "Configure user defined IPv4 local-in policies.",
    "total_fields": 23,
    "required_fields_count": 5,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
