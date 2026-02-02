"""Validation helpers for application/list - Auto-generated"""

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
    "name",  # List name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "replacemsg-group": "",
    "extended-log": "disable",
    "other-application-action": "pass",
    "app-replacemsg": "enable",
    "other-application-log": "disable",
    "enforce-default-app-port": "disable",
    "force-inclusion-ssl-di-sigs": "disable",
    "unknown-application-action": "pass",
    "unknown-application-log": "disable",
    "p2p-block-list": "",
    "deep-app-inspection": "enable",
    "options": "allow-dns",
    "control-default-network-services": "disable",
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
    "name": "string",  # List name.
    "comment": "var-string",  # Comments.
    "replacemsg-group": "string",  # Replacement message group.
    "extended-log": "option",  # Enable/disable extended logging.
    "other-application-action": "option",  # Action for other applications.
    "app-replacemsg": "option",  # Enable/disable replacement messages for blocked applications
    "other-application-log": "option",  # Enable/disable logging for other applications.
    "enforce-default-app-port": "option",  # Enable/disable default application port enforcement for allo
    "force-inclusion-ssl-di-sigs": "option",  # Enable/disable forced inclusion of SSL deep inspection signa
    "unknown-application-action": "option",  # Pass or block traffic from unknown applications.
    "unknown-application-log": "option",  # Enable/disable logging for unknown applications.
    "p2p-block-list": "option",  # P2P applications to be block listed.
    "deep-app-inspection": "option",  # Enable/disable deep application inspection.
    "options": "option",  # Basic application protocol signatures allowed by default.
    "entries": "string",  # Application list entries.
    "control-default-network-services": "option",  # Enable/disable enforcement of protocols over selected ports.
    "default-network-services": "string",  # Default network service entries.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "List name.",
    "comment": "Comments.",
    "replacemsg-group": "Replacement message group.",
    "extended-log": "Enable/disable extended logging.",
    "other-application-action": "Action for other applications.",
    "app-replacemsg": "Enable/disable replacement messages for blocked applications.",
    "other-application-log": "Enable/disable logging for other applications.",
    "enforce-default-app-port": "Enable/disable default application port enforcement for allowed applications.",
    "force-inclusion-ssl-di-sigs": "Enable/disable forced inclusion of SSL deep inspection signatures.",
    "unknown-application-action": "Pass or block traffic from unknown applications.",
    "unknown-application-log": "Enable/disable logging for unknown applications.",
    "p2p-block-list": "P2P applications to be block listed.",
    "deep-app-inspection": "Enable/disable deep application inspection.",
    "options": "Basic application protocol signatures allowed by default.",
    "entries": "Application list entries.",
    "control-default-network-services": "Enable/disable enforcement of protocols over selected ports.",
    "default-network-services": "Default network service entries.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
    "replacemsg-group": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "entries": {
        "id": {
            "type": "integer",
            "help": "Entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "risk": {
            "type": "string",
            "help": "Risk, or impact, of allowing traffic from this application to occur (1 - 5; Low, Elevated, Medium, High, and Critical).",
        },
        "category": {
            "type": "string",
            "help": "Category ID list.",
        },
        "application": {
            "type": "string",
            "help": "ID of allowed applications.",
        },
        "protocols": {
            "type": "user",
            "help": "Application protocol filter.",
            "default": "all",
        },
        "vendor": {
            "type": "user",
            "help": "Application vendor filter.",
            "default": "all",
        },
        "technology": {
            "type": "user",
            "help": "Application technology filter.",
            "default": "all",
        },
        "behavior": {
            "type": "user",
            "help": "Application behavior filter.",
            "default": "all",
        },
        "popularity": {
            "type": "option",
            "help": "Application popularity filter (1 - 5, from least to most popular).",
            "default": "1 2 3 4 5",
            "options": ["1", "2", "3", "4", "5"],
        },
        "exclusion": {
            "type": "string",
            "help": "ID of excluded applications.",
        },
        "parameters": {
            "type": "string",
            "help": "Application parameters.",
        },
        "action": {
            "type": "option",
            "help": "Pass or block traffic, or reset connection for traffic from this application.",
            "default": "block",
            "options": ["pass", "block", "reset"],
        },
        "log": {
            "type": "option",
            "help": "Enable/disable logging for this application list.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "log-packet": {
            "type": "option",
            "help": "Enable/disable packet logging.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "rate-count": {
            "type": "integer",
            "help": "Count of the rate.",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "rate-duration": {
            "type": "integer",
            "help": "Duration (sec) of the rate.",
            "default": 60,
            "min_value": 1,
            "max_value": 65535,
        },
        "rate-mode": {
            "type": "option",
            "help": "Rate limit mode.",
            "default": "continuous",
            "options": ["periodical", "continuous"],
        },
        "rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip", "dhcp-client-mac", "dns-domain"],
        },
        "session-ttl": {
            "type": "integer",
            "help": "Session TTL (0 = default).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "shaper": {
            "type": "string",
            "help": "Traffic shaper.",
            "default": "",
            "max_length": 35,
        },
        "shaper-reverse": {
            "type": "string",
            "help": "Reverse traffic shaper.",
            "default": "",
            "max_length": 35,
        },
        "per-ip-shaper": {
            "type": "string",
            "help": "Per-IP traffic shaper.",
            "default": "",
            "max_length": 35,
        },
        "quarantine": {
            "type": "option",
            "help": "Quarantine method.",
            "default": "none",
            "options": ["none", "attacker"],
        },
        "quarantine-expiry": {
            "type": "user",
            "help": "Duration of quarantine. (Format ###d##h##m, minimum 1m, maximum 364d23h59m, default = 5m). Requires quarantine set to attacker.",
            "default": "5m",
        },
        "quarantine-log": {
            "type": "option",
            "help": "Enable/disable quarantine logging.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
    },
    "default-network-services": {
        "id": {
            "type": "integer",
            "help": "Entry ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "port": {
            "type": "integer",
            "help": "Port number.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "services": {
            "type": "option",
            "help": "Network protocols.",
            "default": "",
            "options": ["http", "ssh", "telnet", "ftp", "dns", "smtp", "pop3", "imap", "snmp", "nntp", "https"],
        },
        "violation-action": {
            "type": "option",
            "help": "Action for protocols not in the allowlist for selected port.",
            "default": "block",
            "options": ["pass", "monitor", "block"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_EXTENDED_LOG = [
    "enable",
    "disable",
]
VALID_BODY_OTHER_APPLICATION_ACTION = [
    "pass",
    "block",
]
VALID_BODY_APP_REPLACEMSG = [
    "disable",
    "enable",
]
VALID_BODY_OTHER_APPLICATION_LOG = [
    "disable",
    "enable",
]
VALID_BODY_ENFORCE_DEFAULT_APP_PORT = [
    "disable",
    "enable",
]
VALID_BODY_FORCE_INCLUSION_SSL_DI_SIGS = [
    "disable",
    "enable",
]
VALID_BODY_UNKNOWN_APPLICATION_ACTION = [
    "pass",
    "block",
]
VALID_BODY_UNKNOWN_APPLICATION_LOG = [
    "disable",
    "enable",
]
VALID_BODY_P2P_BLOCK_LIST = [
    "skype",
    "edonkey",
    "bittorrent",
]
VALID_BODY_DEEP_APP_INSPECTION = [
    "disable",
    "enable",
]
VALID_BODY_OPTIONS = [
    "allow-dns",
    "allow-icmp",
    "allow-http",
    "allow-ssl",
]
VALID_BODY_CONTROL_DEFAULT_NETWORK_SERVICES = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_application_list_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for application/list."""
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


def validate_application_list_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new application/list object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "extended-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-log",
            payload["extended-log"],
            VALID_BODY_EXTENDED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "other-application-action" in payload:
        is_valid, error = _validate_enum_field(
            "other-application-action",
            payload["other-application-action"],
            VALID_BODY_OTHER_APPLICATION_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "app-replacemsg" in payload:
        is_valid, error = _validate_enum_field(
            "app-replacemsg",
            payload["app-replacemsg"],
            VALID_BODY_APP_REPLACEMSG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "other-application-log" in payload:
        is_valid, error = _validate_enum_field(
            "other-application-log",
            payload["other-application-log"],
            VALID_BODY_OTHER_APPLICATION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enforce-default-app-port" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-default-app-port",
            payload["enforce-default-app-port"],
            VALID_BODY_ENFORCE_DEFAULT_APP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "force-inclusion-ssl-di-sigs" in payload:
        is_valid, error = _validate_enum_field(
            "force-inclusion-ssl-di-sigs",
            payload["force-inclusion-ssl-di-sigs"],
            VALID_BODY_FORCE_INCLUSION_SSL_DI_SIGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unknown-application-action" in payload:
        is_valid, error = _validate_enum_field(
            "unknown-application-action",
            payload["unknown-application-action"],
            VALID_BODY_UNKNOWN_APPLICATION_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unknown-application-log" in payload:
        is_valid, error = _validate_enum_field(
            "unknown-application-log",
            payload["unknown-application-log"],
            VALID_BODY_UNKNOWN_APPLICATION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "p2p-block-list" in payload:
        is_valid, error = _validate_enum_field(
            "p2p-block-list",
            payload["p2p-block-list"],
            VALID_BODY_P2P_BLOCK_LIST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "deep-app-inspection" in payload:
        is_valid, error = _validate_enum_field(
            "deep-app-inspection",
            payload["deep-app-inspection"],
            VALID_BODY_DEEP_APP_INSPECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "options" in payload:
        is_valid, error = _validate_enum_field(
            "options",
            payload["options"],
            VALID_BODY_OPTIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "control-default-network-services" in payload:
        is_valid, error = _validate_enum_field(
            "control-default-network-services",
            payload["control-default-network-services"],
            VALID_BODY_CONTROL_DEFAULT_NETWORK_SERVICES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_application_list_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update application/list."""
    # Validate enum values using central function
    if "extended-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-log",
            payload["extended-log"],
            VALID_BODY_EXTENDED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "other-application-action" in payload:
        is_valid, error = _validate_enum_field(
            "other-application-action",
            payload["other-application-action"],
            VALID_BODY_OTHER_APPLICATION_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "app-replacemsg" in payload:
        is_valid, error = _validate_enum_field(
            "app-replacemsg",
            payload["app-replacemsg"],
            VALID_BODY_APP_REPLACEMSG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "other-application-log" in payload:
        is_valid, error = _validate_enum_field(
            "other-application-log",
            payload["other-application-log"],
            VALID_BODY_OTHER_APPLICATION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enforce-default-app-port" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-default-app-port",
            payload["enforce-default-app-port"],
            VALID_BODY_ENFORCE_DEFAULT_APP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "force-inclusion-ssl-di-sigs" in payload:
        is_valid, error = _validate_enum_field(
            "force-inclusion-ssl-di-sigs",
            payload["force-inclusion-ssl-di-sigs"],
            VALID_BODY_FORCE_INCLUSION_SSL_DI_SIGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unknown-application-action" in payload:
        is_valid, error = _validate_enum_field(
            "unknown-application-action",
            payload["unknown-application-action"],
            VALID_BODY_UNKNOWN_APPLICATION_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unknown-application-log" in payload:
        is_valid, error = _validate_enum_field(
            "unknown-application-log",
            payload["unknown-application-log"],
            VALID_BODY_UNKNOWN_APPLICATION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "p2p-block-list" in payload:
        is_valid, error = _validate_enum_field(
            "p2p-block-list",
            payload["p2p-block-list"],
            VALID_BODY_P2P_BLOCK_LIST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "deep-app-inspection" in payload:
        is_valid, error = _validate_enum_field(
            "deep-app-inspection",
            payload["deep-app-inspection"],
            VALID_BODY_DEEP_APP_INSPECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "options" in payload:
        is_valid, error = _validate_enum_field(
            "options",
            payload["options"],
            VALID_BODY_OPTIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "control-default-network-services" in payload:
        is_valid, error = _validate_enum_field(
            "control-default-network-services",
            payload["control-default-network-services"],
            VALID_BODY_CONTROL_DEFAULT_NETWORK_SERVICES,
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
    "endpoint": "application/list",
    "category": "cmdb",
    "api_path": "application/list",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure application control lists.",
    "total_fields": 17,
    "required_fields_count": 1,
    "fields_with_defaults_count": 14,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
