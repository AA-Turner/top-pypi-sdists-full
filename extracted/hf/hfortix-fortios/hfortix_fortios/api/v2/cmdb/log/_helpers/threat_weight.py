"""Validation helpers for log/threat_weight - Auto-generated"""

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
    "status": "enable",
    "blocked-connection": "high",
    "failed-connection": "low",
    "url-block-detected": "high",
    "botnet-connection-detected": "critical",
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
    "status": "option",  # Enable/disable the threat weight feature.
    "level": "string",  # Score mapping for threat weight levels.
    "blocked-connection": "option",  # Threat weight score for blocked connections.
    "failed-connection": "option",  # Threat weight score for failed connections.
    "url-block-detected": "option",  # Threat weight score for URL blocking.
    "botnet-connection-detected": "option",  # Threat weight score for detected botnet connections.
    "malware": "string",  # Anti-virus malware threat weight settings.
    "ips": "string",  # IPS threat weight settings.
    "web": "string",  # Web filtering threat weight settings.
    "geolocation": "string",  # Geolocation-based threat weight settings.
    "application": "string",  # Application-control threat weight settings.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable the threat weight feature.",
    "level": "Score mapping for threat weight levels.",
    "blocked-connection": "Threat weight score for blocked connections.",
    "failed-connection": "Threat weight score for failed connections.",
    "url-block-detected": "Threat weight score for URL blocking.",
    "botnet-connection-detected": "Threat weight score for detected botnet connections.",
    "malware": "Anti-virus malware threat weight settings.",
    "ips": "IPS threat weight settings.",
    "web": "Web filtering threat weight settings.",
    "geolocation": "Geolocation-based threat weight settings.",
    "application": "Application-control threat weight settings.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "level": {
        "low": {
            "type": "integer",
            "help": "Low level score value (1 - 100).",
            "default": 5,
            "min_value": 1,
            "max_value": 100,
        },
        "medium": {
            "type": "integer",
            "help": "Medium level score value (1 - 100).",
            "default": 10,
            "min_value": 1,
            "max_value": 100,
        },
        "high": {
            "type": "integer",
            "help": "High level score value (1 - 100).",
            "default": 30,
            "min_value": 1,
            "max_value": 100,
        },
        "critical": {
            "type": "integer",
            "help": "Critical level score value (1 - 100).",
            "default": 50,
            "min_value": 1,
            "max_value": 100,
        },
    },
    "malware": {
        "virus-infected": {
            "type": "option",
            "help": "Threat weight score for virus (infected) detected.",
            "default": "critical",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "inline-block": {
            "type": "option",
            "help": "Threat weight score for malware detected by inline block.",
            "default": "critical",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "file-blocked": {
            "type": "option",
            "help": "Threat weight score for blocked file detected.",
            "default": "low",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "command-blocked": {
            "type": "option",
            "help": "Threat weight score for blocked command detected.",
            "default": "disable",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "oversized": {
            "type": "option",
            "help": "Threat weight score for oversized file detected.",
            "default": "disable",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "virus-scan-error": {
            "type": "option",
            "help": "Threat weight score for virus (scan error) detected.",
            "default": "high",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "switch-proto": {
            "type": "option",
            "help": "Threat weight score for switch proto detected.",
            "default": "disable",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "mimefragmented": {
            "type": "option",
            "help": "Threat weight score for mimefragmented detected.",
            "default": "disable",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "virus-file-type-executable": {
            "type": "option",
            "help": "Threat weight score for virus (file type executable) detected.",
            "default": "medium",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "virus-outbreak-prevention": {
            "type": "option",
            "help": "Threat weight score for virus (outbreak prevention) event.",
            "default": "critical",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "content-disarm": {
            "type": "option",
            "help": "Threat weight score for virus (content disarm) detected.",
            "default": "medium",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "malware-list": {
            "type": "option",
            "help": "Threat weight score for virus (malware list) detected.",
            "default": "medium",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "ems-threat-feed": {
            "type": "option",
            "help": "Threat weight score for virus (EMS threat feed) detected.",
            "default": "medium",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "fsa-malicious": {
            "type": "option",
            "help": "Threat weight score for FortiSandbox malicious malware detected.",
            "default": "critical",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "fsa-high-risk": {
            "type": "option",
            "help": "Threat weight score for FortiSandbox high risk malware detected.",
            "default": "high",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "fsa-medium-risk": {
            "type": "option",
            "help": "Threat weight score for FortiSandbox medium risk malware detected.",
            "default": "medium",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
    },
    "ips": {
        "info-severity": {
            "type": "option",
            "help": "Threat weight score for IPS info severity events.",
            "default": "disable",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "low-severity": {
            "type": "option",
            "help": "Threat weight score for IPS low severity events.",
            "default": "low",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "medium-severity": {
            "type": "option",
            "help": "Threat weight score for IPS medium severity events.",
            "default": "medium",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "high-severity": {
            "type": "option",
            "help": "Threat weight score for IPS high severity events.",
            "default": "high",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
        "critical-severity": {
            "type": "option",
            "help": "Threat weight score for IPS critical severity events.",
            "default": "critical",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
    },
    "web": {
        "id": {
            "type": "integer",
            "help": "Entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "category": {
            "type": "integer",
            "help": "Threat weight score for web category filtering matches.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "level": {
            "type": "option",
            "help": "Threat weight score for web category filtering matches.",
            "default": "low",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
    },
    "geolocation": {
        "id": {
            "type": "integer",
            "help": "Entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "country": {
            "type": "string",
            "help": "Country code.",
            "required": True,
            "default": "",
            "max_length": 2,
        },
        "level": {
            "type": "option",
            "help": "Threat weight score for Geolocation-based events.",
            "default": "low",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
    },
    "application": {
        "id": {
            "type": "integer",
            "help": "Entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "category": {
            "type": "integer",
            "help": "Application category.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "level": {
            "type": "option",
            "help": "Threat weight score for Application events.",
            "default": "low",
            "options": ["disable", "low", "medium", "high", "critical"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_BLOCKED_CONNECTION = [
    "disable",
    "low",
    "medium",
    "high",
    "critical",
]
VALID_BODY_FAILED_CONNECTION = [
    "disable",
    "low",
    "medium",
    "high",
    "critical",
]
VALID_BODY_URL_BLOCK_DETECTED = [
    "disable",
    "low",
    "medium",
    "high",
    "critical",
]
VALID_BODY_BOTNET_CONNECTION_DETECTED = [
    "disable",
    "low",
    "medium",
    "high",
    "critical",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_log_threat_weight_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for log/threat_weight."""
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


def validate_log_threat_weight_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new log/threat_weight object."""
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
    if "blocked-connection" in payload:
        is_valid, error = _validate_enum_field(
            "blocked-connection",
            payload["blocked-connection"],
            VALID_BODY_BLOCKED_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "failed-connection" in payload:
        is_valid, error = _validate_enum_field(
            "failed-connection",
            payload["failed-connection"],
            VALID_BODY_FAILED_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "url-block-detected" in payload:
        is_valid, error = _validate_enum_field(
            "url-block-detected",
            payload["url-block-detected"],
            VALID_BODY_URL_BLOCK_DETECTED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "botnet-connection-detected" in payload:
        is_valid, error = _validate_enum_field(
            "botnet-connection-detected",
            payload["botnet-connection-detected"],
            VALID_BODY_BOTNET_CONNECTION_DETECTED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_log_threat_weight_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update log/threat_weight."""
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
    if "blocked-connection" in payload:
        is_valid, error = _validate_enum_field(
            "blocked-connection",
            payload["blocked-connection"],
            VALID_BODY_BLOCKED_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "failed-connection" in payload:
        is_valid, error = _validate_enum_field(
            "failed-connection",
            payload["failed-connection"],
            VALID_BODY_FAILED_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "url-block-detected" in payload:
        is_valid, error = _validate_enum_field(
            "url-block-detected",
            payload["url-block-detected"],
            VALID_BODY_URL_BLOCK_DETECTED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "botnet-connection-detected" in payload:
        is_valid, error = _validate_enum_field(
            "botnet-connection-detected",
            payload["botnet-connection-detected"],
            VALID_BODY_BOTNET_CONNECTION_DETECTED,
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
    "endpoint": "log/threat_weight",
    "category": "cmdb",
    "api_path": "log/threat-weight",
    "help": "Configure threat weight settings.",
    "total_fields": 11,
    "required_fields_count": 0,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
