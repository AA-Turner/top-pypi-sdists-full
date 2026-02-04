"""Validation helpers for firewall/shaping_policy - Auto-generated"""

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
    "srcaddr",  # IPv4 source address and address group names.
    "dstaddr",  # IPv4 destination address and address group names.
    "srcaddr6",  # IPv6 source address and address group names.
    "dstaddr6",  # IPv6 destination address and address group names.
    "service",  # Service and service group names.
    "dstintf",  # One or more outgoing (egress) interfaces.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "id": 0,
    "uuid": "00000000-0000-0000-0000-000000000000",
    "name": "",
    "status": "enable",
    "ip-version": "4",
    "traffic-type": "forwarding",
    "internet-service": "disable",
    "internet-service-src": "disable",
    "schedule": "",
    "tos-mask": "",
    "tos": "",
    "tos-negate": "disable",
    "traffic-shaper": "",
    "traffic-shaper-reverse": "",
    "per-ip-shaper": "",
    "class-id": 0,
    "diffserv-forward": "disable",
    "diffserv-reverse": "disable",
    "diffservcode-forward": "",
    "diffservcode-rev": "",
    "cos-mask": "",
    "cos": "",
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
    "id": "integer",  # Shaping policy ID (0 - 4294967295).
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "name": "string",  # Shaping policy name.
    "comment": "var-string",  # Comments.
    "status": "option",  # Enable/disable this traffic shaping policy.
    "ip-version": "option",  # Apply this traffic shaping policy to IPv4 or IPv6 traffic.
    "traffic-type": "option",  # Traffic type.
    "srcaddr": "string",  # IPv4 source address and address group names.
    "dstaddr": "string",  # IPv4 destination address and address group names.
    "srcaddr6": "string",  # IPv6 source address and address group names.
    "dstaddr6": "string",  # IPv6 destination address and address group names.
    "internet-service": "option",  # Enable/disable use of Internet Services for this policy. If enabled, destination
    "internet-service-name": "string",  # Internet Service ID.
    "internet-service-group": "string",  # Internet Service group name.
    "internet-service-custom": "string",  # Custom Internet Service name.
    "internet-service-custom-group": "string",  # Custom Internet Service group name.
    "internet-service-fortiguard": "string",  # FortiGuard Internet Service name.
    "internet-service-src": "option",  # Enable/disable use of Internet Services in source for this policy. If enabled, s
    "internet-service-src-name": "string",  # Internet Service source name.
    "internet-service-src-group": "string",  # Internet Service source group name.
    "internet-service-src-custom": "string",  # Custom Internet Service source name.
    "internet-service-src-custom-group": "string",  # Custom Internet Service source group name.
    "internet-service-src-fortiguard": "string",  # FortiGuard Internet Service source name.
    "service": "string",  # Service and service group names.
    "schedule": "string",  # Schedule name.
    "users": "string",  # Apply this traffic shaping policy to individual users that have authenticated wi
    "groups": "string",  # Apply this traffic shaping policy to user groups that have authenticated with th
    "application": "string",  # IDs of one or more applications that this shaper applies application control tra
    "app-category": "string",  # IDs of one or more application categories that this shaper applies application c
    "app-group": "string",  # One or more application group names.
    "url-category": "string",  # IDs of one or more FortiGuard Web Filtering categories that this shaper applies 
    "srcintf": "string",  # One or more incoming (ingress) interfaces.
    "dstintf": "string",  # One or more outgoing (egress) interfaces.
    "tos-mask": "user",  # Non-zero bit positions are used for comparison while zero bit positions are igno
    "tos": "user",  # ToS (Type of Service) value used for comparison.
    "tos-negate": "option",  # Enable negated TOS match.
    "traffic-shaper": "string",  # Traffic shaper to apply to traffic forwarded by the firewall policy.
    "traffic-shaper-reverse": "string",  # Traffic shaper to apply to response traffic received by the firewall policy.
    "per-ip-shaper": "string",  # Per-IP traffic shaper to apply with this policy.
    "class-id": "integer",  # Traffic class ID.
    "diffserv-forward": "option",  # Enable to change packet's DiffServ values to the specified diffservcode-forward 
    "diffserv-reverse": "option",  # Enable to change packet's reverse (reply) DiffServ values to the specified diffs
    "diffservcode-forward": "user",  # Change packet's DiffServ to this value.
    "diffservcode-rev": "user",  # Change packet's reverse (reply) DiffServ to this value.
    "cos-mask": "user",  # VLAN CoS evaluated bits.
    "cos": "user",  # VLAN CoS bit pattern.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "id": "Shaping policy ID (0 - 4294967295).",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "name": "Shaping policy name.",
    "comment": "Comments.",
    "status": "Enable/disable this traffic shaping policy.",
    "ip-version": "Apply this traffic shaping policy to IPv4 or IPv6 traffic.",
    "traffic-type": "Traffic type.",
    "srcaddr": "IPv4 source address and address group names.",
    "dstaddr": "IPv4 destination address and address group names.",
    "srcaddr6": "IPv6 source address and address group names.",
    "dstaddr6": "IPv6 destination address and address group names.",
    "internet-service": "Enable/disable use of Internet Services for this policy. If enabled, destination address and service are not used.",
    "internet-service-name": "Internet Service ID.",
    "internet-service-group": "Internet Service group name.",
    "internet-service-custom": "Custom Internet Service name.",
    "internet-service-custom-group": "Custom Internet Service group name.",
    "internet-service-fortiguard": "FortiGuard Internet Service name.",
    "internet-service-src": "Enable/disable use of Internet Services in source for this policy. If enabled, source address is not used.",
    "internet-service-src-name": "Internet Service source name.",
    "internet-service-src-group": "Internet Service source group name.",
    "internet-service-src-custom": "Custom Internet Service source name.",
    "internet-service-src-custom-group": "Custom Internet Service source group name.",
    "internet-service-src-fortiguard": "FortiGuard Internet Service source name.",
    "service": "Service and service group names.",
    "schedule": "Schedule name.",
    "users": "Apply this traffic shaping policy to individual users that have authenticated with the FortiGate.",
    "groups": "Apply this traffic shaping policy to user groups that have authenticated with the FortiGate.",
    "application": "IDs of one or more applications that this shaper applies application control traffic shaping to.",
    "app-category": "IDs of one or more application categories that this shaper applies application control traffic shaping to.",
    "app-group": "One or more application group names.",
    "url-category": "IDs of one or more FortiGuard Web Filtering categories that this shaper applies traffic shaping to.",
    "srcintf": "One or more incoming (ingress) interfaces.",
    "dstintf": "One or more outgoing (egress) interfaces.",
    "tos-mask": "Non-zero bit positions are used for comparison while zero bit positions are ignored.",
    "tos": "ToS (Type of Service) value used for comparison.",
    "tos-negate": "Enable negated TOS match.",
    "traffic-shaper": "Traffic shaper to apply to traffic forwarded by the firewall policy.",
    "traffic-shaper-reverse": "Traffic shaper to apply to response traffic received by the firewall policy.",
    "per-ip-shaper": "Per-IP traffic shaper to apply with this policy.",
    "class-id": "Traffic class ID.",
    "diffserv-forward": "Enable to change packet's DiffServ values to the specified diffservcode-forward value.",
    "diffserv-reverse": "Enable to change packet's reverse (reply) DiffServ values to the specified diffservcode-rev value.",
    "diffservcode-forward": "Change packet's DiffServ to this value.",
    "diffservcode-rev": "Change packet's reverse (reply) DiffServ to this value.",
    "cos-mask": "VLAN CoS evaluated bits.",
    "cos": "VLAN CoS bit pattern.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "name": {"type": "string", "max_length": 35},
    "schedule": {"type": "string", "max_length": 35},
    "traffic-shaper": {"type": "string", "max_length": 35},
    "traffic-shaper-reverse": {"type": "string", "max_length": 35},
    "per-ip-shaper": {"type": "string", "max_length": 35},
    "class-id": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
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
    "srcaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-name": {
        "name": {
            "type": "string",
            "help": "Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
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
    "users": {
        "name": {
            "type": "string",
            "help": "User name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "groups": {
        "name": {
            "type": "string",
            "help": "Group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "application": {
        "id": {
            "type": "integer",
            "help": "Application IDs.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "app-category": {
        "id": {
            "type": "integer",
            "help": "Category IDs.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "app-group": {
        "name": {
            "type": "string",
            "help": "Application group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "url-category": {
        "id": {
            "type": "integer",
            "help": "URL category ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "srcintf": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstintf": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_IP_VERSION = [
    "4",
    "6",
]
VALID_BODY_TRAFFIC_TYPE = [
    "forwarding",
    "local-in",
    "local-out",
]
VALID_BODY_INTERNET_SERVICE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_SRC = [
    "enable",
    "disable",
]
VALID_BODY_TOS_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_DIFFSERV_FORWARD = [
    "enable",
    "disable",
]
VALID_BODY_DIFFSERV_REVERSE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_shaping_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/shaping_policy."""
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


def validate_firewall_shaping_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/shaping_policy object."""
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
    if "ip-version" in payload:
        is_valid, error = _validate_enum_field(
            "ip-version",
            payload["ip-version"],
            VALID_BODY_IP_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-type" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-type",
            payload["traffic-type"],
            VALID_BODY_TRAFFIC_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service",
            payload["internet-service"],
            VALID_BODY_INTERNET_SERVICE,
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
    if "tos-negate" in payload:
        is_valid, error = _validate_enum_field(
            "tos-negate",
            payload["tos-negate"],
            VALID_BODY_TOS_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-forward" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-forward",
            payload["diffserv-forward"],
            VALID_BODY_DIFFSERV_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-reverse" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-reverse",
            payload["diffserv-reverse"],
            VALID_BODY_DIFFSERV_REVERSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_shaping_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/shaping_policy."""
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
    if "ip-version" in payload:
        is_valid, error = _validate_enum_field(
            "ip-version",
            payload["ip-version"],
            VALID_BODY_IP_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-type" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-type",
            payload["traffic-type"],
            VALID_BODY_TRAFFIC_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service",
            payload["internet-service"],
            VALID_BODY_INTERNET_SERVICE,
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
    if "tos-negate" in payload:
        is_valid, error = _validate_enum_field(
            "tos-negate",
            payload["tos-negate"],
            VALID_BODY_TOS_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-forward" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-forward",
            payload["diffserv-forward"],
            VALID_BODY_DIFFSERV_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-reverse" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-reverse",
            payload["diffserv-reverse"],
            VALID_BODY_DIFFSERV_REVERSE,
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
    "endpoint": "firewall/shaping_policy",
    "category": "cmdb",
    "api_path": "firewall/shaping-policy",
    "mkey": "id",
    "mkey_type": "integer",
    "help": "Configure shaping policies.",
    "total_fields": 46,
    "required_fields_count": 6,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
