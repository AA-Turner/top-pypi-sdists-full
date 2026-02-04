"""Validation helpers for ips/global_ - Auto-generated"""

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
    "fail-open": "disable",
    "database": "extended",
    "traffic-submit": "disable",
    "anomaly-mode": "continuous",
    "session-limit-mode": "heuristic",
    "socket-size": 256,
    "engine-count": 0,
    "sync-session-ttl": "enable",
    "deep-app-insp-timeout": 0,
    "deep-app-insp-db-limit": 0,
    "exclude-signatures": "ot",
    "packet-log-queue-depth": 128,
    "ngfw-max-scan-range": 4096,
    "av-mem-limit": 0,
    "machine-learning-detection": "enable",
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
    "fail-open": "option",  # Enable to allow traffic if the IPS buffer is full. Default is disable and IPS tr
    "database": "option",  # Regular or extended IPS database. Regular protects against the latest common and
    "traffic-submit": "option",  # Enable/disable submitting attack data found by this FortiGate to FortiGuard.
    "anomaly-mode": "option",  # Global blocking mode for rate-based anomalies.
    "session-limit-mode": "option",  # Method of counting concurrent sessions used by session limit anomalies. Choose b
    "socket-size": "integer",  # IPS socket buffer size. Max and default value depend on available memory. Can be
    "engine-count": "integer",  # Number of IPS engines running. If set to the default value of 0, FortiOS sets th
    "sync-session-ttl": "option",  # Enable/disable use of kernel session TTL for IPS sessions.
    "deep-app-insp-timeout": "integer",  # Timeout for Deep application inspection (1 - 2147483647 sec., 0 = use recommende
    "deep-app-insp-db-limit": "integer",  # Limit on number of entries in deep application inspection database (1 - 21474836
    "exclude-signatures": "option",  # Excluded signatures.
    "packet-log-queue-depth": "integer",  # Packet/pcap log queue depth per IPS engine.
    "ngfw-max-scan-range": "integer",  # NGFW policy-mode app detection threshold.
    "av-mem-limit": "integer",  # Maximum percentage of system memory allowed for use on AV scanning (10 - 50, def
    "machine-learning-detection": "option",  # Enable/disable machine learning detection.
    "tls-active-probe": "string",  # TLS active probe configuration.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "fail-open": "Enable to allow traffic if the IPS buffer is full. Default is disable and IPS traffic is blocked when the IPS buffer is full.",
    "database": "Regular or extended IPS database. Regular protects against the latest common and in-the-wild attacks. Extended includes protection from legacy attacks.",
    "traffic-submit": "Enable/disable submitting attack data found by this FortiGate to FortiGuard.",
    "anomaly-mode": "Global blocking mode for rate-based anomalies.",
    "session-limit-mode": "Method of counting concurrent sessions used by session limit anomalies. Choose between greater accuracy (accurate) or improved performance (heuristics).",
    "socket-size": "IPS socket buffer size. Max and default value depend on available memory. Can be changed to tune performance.",
    "engine-count": "Number of IPS engines running. If set to the default value of 0, FortiOS sets the number to optimize performance depending on the number of CPU cores.",
    "sync-session-ttl": "Enable/disable use of kernel session TTL for IPS sessions.",
    "deep-app-insp-timeout": "Timeout for Deep application inspection (1 - 2147483647 sec., 0 = use recommended setting).",
    "deep-app-insp-db-limit": "Limit on number of entries in deep application inspection database (1 - 2147483647, use recommended setting = 0).",
    "exclude-signatures": "Excluded signatures.",
    "packet-log-queue-depth": "Packet/pcap log queue depth per IPS engine.",
    "ngfw-max-scan-range": "NGFW policy-mode app detection threshold.",
    "av-mem-limit": "Maximum percentage of system memory allowed for use on AV scanning (10 - 50, default = zero). To disable set to zero. When disabled, there is no limit on the AV memory usage.",
    "machine-learning-detection": "Enable/disable machine learning detection.",
    "tls-active-probe": "TLS active probe configuration.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "socket-size": {"type": "integer", "min": 0, "max": 512},
    "engine-count": {"type": "integer", "min": 0, "max": 255},
    "deep-app-insp-timeout": {"type": "integer", "min": 0, "max": 2147483647},
    "deep-app-insp-db-limit": {"type": "integer", "min": 0, "max": 2147483647},
    "packet-log-queue-depth": {"type": "integer", "min": 128, "max": 4096},
    "ngfw-max-scan-range": {"type": "integer", "min": 0, "max": 4294967295},
    "av-mem-limit": {"type": "integer", "min": 10, "max": 50},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "tls-active-probe": {
        "interface-select-method": {
            "type": "option",
            "help": "Specify how to select outgoing interface to reach server.",
            "default": "auto",
            "options": ["auto", "sdwan", "specify"],
        },
        "interface": {
            "type": "string",
            "help": "Specify outgoing interface to reach server.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "vdom": {
            "type": "string",
            "help": "Virtual domain name for TLS active probe.",
            "required": True,
            "default": "",
            "max_length": 31,
        },
        "source-ip": {
            "type": "ipv4-address",
            "help": "Source IP address used for TLS active probe.",
            "default": "0.0.0.0",
        },
        "source-ip6": {
            "type": "ipv6-address",
            "help": "Source IPv6 address used for TLS active probe.",
            "default": "::",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_FAIL_OPEN = [
    "enable",
    "disable",
]
VALID_BODY_DATABASE = [
    "regular",
    "extended",
]
VALID_BODY_TRAFFIC_SUBMIT = [
    "enable",
    "disable",
]
VALID_BODY_ANOMALY_MODE = [
    "periodical",
    "continuous",
]
VALID_BODY_SESSION_LIMIT_MODE = [
    "accurate",
    "heuristic",
]
VALID_BODY_SYNC_SESSION_TTL = [
    "enable",
    "disable",
]
VALID_BODY_EXCLUDE_SIGNATURES = [
    "none",
    "ot",
]
VALID_BODY_MACHINE_LEARNING_DETECTION = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_ips_global_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for ips/global_."""
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


def validate_ips_global_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new ips/global_ object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "fail-open" in payload:
        is_valid, error = _validate_enum_field(
            "fail-open",
            payload["fail-open"],
            VALID_BODY_FAIL_OPEN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "database" in payload:
        is_valid, error = _validate_enum_field(
            "database",
            payload["database"],
            VALID_BODY_DATABASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-submit" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-submit",
            payload["traffic-submit"],
            VALID_BODY_TRAFFIC_SUBMIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "anomaly-mode" in payload:
        is_valid, error = _validate_enum_field(
            "anomaly-mode",
            payload["anomaly-mode"],
            VALID_BODY_ANOMALY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-limit-mode" in payload:
        is_valid, error = _validate_enum_field(
            "session-limit-mode",
            payload["session-limit-mode"],
            VALID_BODY_SESSION_LIMIT_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sync-session-ttl" in payload:
        is_valid, error = _validate_enum_field(
            "sync-session-ttl",
            payload["sync-session-ttl"],
            VALID_BODY_SYNC_SESSION_TTL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "exclude-signatures" in payload:
        is_valid, error = _validate_enum_field(
            "exclude-signatures",
            payload["exclude-signatures"],
            VALID_BODY_EXCLUDE_SIGNATURES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "machine-learning-detection" in payload:
        is_valid, error = _validate_enum_field(
            "machine-learning-detection",
            payload["machine-learning-detection"],
            VALID_BODY_MACHINE_LEARNING_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_ips_global_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update ips/global_."""
    # Validate enum values using central function
    if "fail-open" in payload:
        is_valid, error = _validate_enum_field(
            "fail-open",
            payload["fail-open"],
            VALID_BODY_FAIL_OPEN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "database" in payload:
        is_valid, error = _validate_enum_field(
            "database",
            payload["database"],
            VALID_BODY_DATABASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-submit" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-submit",
            payload["traffic-submit"],
            VALID_BODY_TRAFFIC_SUBMIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "anomaly-mode" in payload:
        is_valid, error = _validate_enum_field(
            "anomaly-mode",
            payload["anomaly-mode"],
            VALID_BODY_ANOMALY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-limit-mode" in payload:
        is_valid, error = _validate_enum_field(
            "session-limit-mode",
            payload["session-limit-mode"],
            VALID_BODY_SESSION_LIMIT_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sync-session-ttl" in payload:
        is_valid, error = _validate_enum_field(
            "sync-session-ttl",
            payload["sync-session-ttl"],
            VALID_BODY_SYNC_SESSION_TTL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "exclude-signatures" in payload:
        is_valid, error = _validate_enum_field(
            "exclude-signatures",
            payload["exclude-signatures"],
            VALID_BODY_EXCLUDE_SIGNATURES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "machine-learning-detection" in payload:
        is_valid, error = _validate_enum_field(
            "machine-learning-detection",
            payload["machine-learning-detection"],
            VALID_BODY_MACHINE_LEARNING_DETECTION,
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
    "endpoint": "ips/global_",
    "category": "cmdb",
    "api_path": "ips/global",
    "help": "Configure IPS global parameter.",
    "total_fields": 16,
    "required_fields_count": 0,
    "fields_with_defaults_count": 15,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
