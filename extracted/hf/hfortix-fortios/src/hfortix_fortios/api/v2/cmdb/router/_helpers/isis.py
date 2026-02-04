"""Validation helpers for router/isis - Auto-generated"""

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
    "is-type": "level-1-2",
    "adv-passive-only": "disable",
    "adv-passive-only6": "disable",
    "auth-mode-l1": "password",
    "auth-mode-l2": "password",
    "auth-keychain-l1": "",
    "auth-keychain-l2": "",
    "auth-sendonly-l1": "disable",
    "auth-sendonly-l2": "disable",
    "ignore-lsp-errors": "disable",
    "lsp-gen-interval-l1": 30,
    "lsp-gen-interval-l2": 30,
    "lsp-refresh-interval": 900,
    "max-lsp-lifetime": 1200,
    "spf-interval-exp-l1": "",
    "spf-interval-exp-l2": "",
    "dynamic-hostname": "disable",
    "adjacency-check": "disable",
    "adjacency-check6": "disable",
    "overload-bit": "disable",
    "overload-bit-suppress": "",
    "overload-bit-on-startup": 0,
    "default-originate": "disable",
    "default-originate6": "disable",
    "metric-style": "narrow",
    "redistribute-l1": "disable",
    "redistribute-l1-list": "",
    "redistribute-l2": "disable",
    "redistribute-l2-list": "",
    "redistribute6-l1": "disable",
    "redistribute6-l1-list": "",
    "redistribute6-l2": "disable",
    "redistribute6-l2-list": "",
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
    "is-type": "option",  # IS type.
    "adv-passive-only": "option",  # Enable/disable IS-IS advertisement of passive interfaces only.
    "adv-passive-only6": "option",  # Enable/disable IPv6 IS-IS advertisement of passive interfaces only.
    "auth-mode-l1": "option",  # Level 1 authentication mode.
    "auth-mode-l2": "option",  # Level 2 authentication mode.
    "auth-password-l1": "password",  # Authentication password for level 1 PDUs.
    "auth-password-l2": "password",  # Authentication password for level 2 PDUs.
    "auth-keychain-l1": "string",  # Authentication key-chain for level 1 PDUs.
    "auth-keychain-l2": "string",  # Authentication key-chain for level 2 PDUs.
    "auth-sendonly-l1": "option",  # Enable/disable level 1 authentication send-only.
    "auth-sendonly-l2": "option",  # Enable/disable level 2 authentication send-only.
    "ignore-lsp-errors": "option",  # Enable/disable ignoring of LSP errors with bad checksums.
    "lsp-gen-interval-l1": "integer",  # Minimum interval for level 1 LSP regenerating.
    "lsp-gen-interval-l2": "integer",  # Minimum interval for level 2 LSP regenerating.
    "lsp-refresh-interval": "integer",  # LSP refresh time in seconds.
    "max-lsp-lifetime": "integer",  # Maximum LSP lifetime in seconds.
    "spf-interval-exp-l1": "user",  # Level 1 SPF calculation delay.
    "spf-interval-exp-l2": "user",  # Level 2 SPF calculation delay.
    "dynamic-hostname": "option",  # Enable/disable dynamic hostname.
    "adjacency-check": "option",  # Enable/disable adjacency check.
    "adjacency-check6": "option",  # Enable/disable IPv6 adjacency check.
    "overload-bit": "option",  # Enable/disable signal other routers not to use us in SPF.
    "overload-bit-suppress": "option",  # Suppress overload-bit for the specific prefixes.
    "overload-bit-on-startup": "integer",  # Overload-bit only temporarily after reboot.
    "default-originate": "option",  # Enable/disable distribution of default route information.
    "default-originate6": "option",  # Enable/disable distribution of default IPv6 route information.
    "metric-style": "option",  # Use old-style (ISO 10589) or new-style packet formats.
    "redistribute-l1": "option",  # Enable/disable redistribution of level 1 routes into level 2.
    "redistribute-l1-list": "string",  # Access-list for route redistribution from l1 to l2.
    "redistribute-l2": "option",  # Enable/disable redistribution of level 2 routes into level 1.
    "redistribute-l2-list": "string",  # Access-list for route redistribution from l2 to l1.
    "redistribute6-l1": "option",  # Enable/disable redistribution of level 1 IPv6 routes into level 2.
    "redistribute6-l1-list": "string",  # Access-list for IPv6 route redistribution from l1 to l2.
    "redistribute6-l2": "option",  # Enable/disable redistribution of level 2 IPv6 routes into level 1.
    "redistribute6-l2-list": "string",  # Access-list for IPv6 route redistribution from l2 to l1.
    "isis-net": "string",  # IS-IS net configuration.
    "isis-interface": "string",  # IS-IS interface configuration.
    "summary-address": "string",  # IS-IS summary addresses.
    "summary-address6": "string",  # IS-IS IPv6 summary address.
    "redistribute": "string",  # IS-IS redistribute protocols.
    "redistribute6": "string",  # IS-IS IPv6 redistribution for routing protocols.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "is-type": "IS type.",
    "adv-passive-only": "Enable/disable IS-IS advertisement of passive interfaces only.",
    "adv-passive-only6": "Enable/disable IPv6 IS-IS advertisement of passive interfaces only.",
    "auth-mode-l1": "Level 1 authentication mode.",
    "auth-mode-l2": "Level 2 authentication mode.",
    "auth-password-l1": "Authentication password for level 1 PDUs.",
    "auth-password-l2": "Authentication password for level 2 PDUs.",
    "auth-keychain-l1": "Authentication key-chain for level 1 PDUs.",
    "auth-keychain-l2": "Authentication key-chain for level 2 PDUs.",
    "auth-sendonly-l1": "Enable/disable level 1 authentication send-only.",
    "auth-sendonly-l2": "Enable/disable level 2 authentication send-only.",
    "ignore-lsp-errors": "Enable/disable ignoring of LSP errors with bad checksums.",
    "lsp-gen-interval-l1": "Minimum interval for level 1 LSP regenerating.",
    "lsp-gen-interval-l2": "Minimum interval for level 2 LSP regenerating.",
    "lsp-refresh-interval": "LSP refresh time in seconds.",
    "max-lsp-lifetime": "Maximum LSP lifetime in seconds.",
    "spf-interval-exp-l1": "Level 1 SPF calculation delay.",
    "spf-interval-exp-l2": "Level 2 SPF calculation delay.",
    "dynamic-hostname": "Enable/disable dynamic hostname.",
    "adjacency-check": "Enable/disable adjacency check.",
    "adjacency-check6": "Enable/disable IPv6 adjacency check.",
    "overload-bit": "Enable/disable signal other routers not to use us in SPF.",
    "overload-bit-suppress": "Suppress overload-bit for the specific prefixes.",
    "overload-bit-on-startup": "Overload-bit only temporarily after reboot.",
    "default-originate": "Enable/disable distribution of default route information.",
    "default-originate6": "Enable/disable distribution of default IPv6 route information.",
    "metric-style": "Use old-style (ISO 10589) or new-style packet formats.",
    "redistribute-l1": "Enable/disable redistribution of level 1 routes into level 2.",
    "redistribute-l1-list": "Access-list for route redistribution from l1 to l2.",
    "redistribute-l2": "Enable/disable redistribution of level 2 routes into level 1.",
    "redistribute-l2-list": "Access-list for route redistribution from l2 to l1.",
    "redistribute6-l1": "Enable/disable redistribution of level 1 IPv6 routes into level 2.",
    "redistribute6-l1-list": "Access-list for IPv6 route redistribution from l1 to l2.",
    "redistribute6-l2": "Enable/disable redistribution of level 2 IPv6 routes into level 1.",
    "redistribute6-l2-list": "Access-list for IPv6 route redistribution from l2 to l1.",
    "isis-net": "IS-IS net configuration.",
    "isis-interface": "IS-IS interface configuration.",
    "summary-address": "IS-IS summary addresses.",
    "summary-address6": "IS-IS IPv6 summary address.",
    "redistribute": "IS-IS redistribute protocols.",
    "redistribute6": "IS-IS IPv6 redistribution for routing protocols.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "auth-keychain-l1": {"type": "string", "max_length": 35},
    "auth-keychain-l2": {"type": "string", "max_length": 35},
    "lsp-gen-interval-l1": {"type": "integer", "min": 1, "max": 120},
    "lsp-gen-interval-l2": {"type": "integer", "min": 1, "max": 120},
    "lsp-refresh-interval": {"type": "integer", "min": 1, "max": 65535},
    "max-lsp-lifetime": {"type": "integer", "min": 350, "max": 65535},
    "overload-bit-on-startup": {"type": "integer", "min": 5, "max": 86400},
    "redistribute-l1-list": {"type": "string", "max_length": 35},
    "redistribute-l2-list": {"type": "string", "max_length": 35},
    "redistribute6-l1-list": {"type": "string", "max_length": 35},
    "redistribute6-l2-list": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "isis-net": {
        "id": {
            "type": "integer",
            "help": "ISIS network ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "net": {
            "type": "user",
            "help": "IS-IS networks (format = xx.xxxx.  .xxxx.xx.).",
            "default": "",
        },
    },
    "isis-interface": {
        "name": {
            "type": "string",
            "help": "IS-IS interface name.",
            "default": "",
            "max_length": 15,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable interface for IS-IS.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "status6": {
            "type": "option",
            "help": "Enable/disable IPv6 interface for IS-IS.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "network-type": {
            "type": "option",
            "help": "IS-IS interface's network type.",
            "default": "",
            "options": ["broadcast", "point-to-point", "loopback"],
        },
        "circuit-type": {
            "type": "option",
            "help": "IS-IS interface's circuit type.",
            "default": "level-1-2",
            "options": ["level-1-2", "level-1", "level-2"],
        },
        "csnp-interval-l1": {
            "type": "integer",
            "help": "Level 1 CSNP interval.",
            "default": 10,
            "min_value": 1,
            "max_value": 65535,
        },
        "csnp-interval-l2": {
            "type": "integer",
            "help": "Level 2 CSNP interval.",
            "default": 10,
            "min_value": 1,
            "max_value": 65535,
        },
        "hello-interval-l1": {
            "type": "integer",
            "help": "Level 1 hello interval.",
            "default": 10,
            "min_value": 0,
            "max_value": 65535,
        },
        "hello-interval-l2": {
            "type": "integer",
            "help": "Level 2 hello interval.",
            "default": 10,
            "min_value": 0,
            "max_value": 65535,
        },
        "hello-multiplier-l1": {
            "type": "integer",
            "help": "Level 1 multiplier for Hello holding time.",
            "default": 3,
            "min_value": 2,
            "max_value": 100,
        },
        "hello-multiplier-l2": {
            "type": "integer",
            "help": "Level 2 multiplier for Hello holding time.",
            "default": 3,
            "min_value": 2,
            "max_value": 100,
        },
        "hello-padding": {
            "type": "option",
            "help": "Enable/disable padding to IS-IS hello packets.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "lsp-interval": {
            "type": "integer",
            "help": "LSP transmission interval (milliseconds).",
            "default": 33,
            "min_value": 1,
            "max_value": 4294967295,
        },
        "lsp-retransmit-interval": {
            "type": "integer",
            "help": "LSP retransmission interval (sec).",
            "default": 5,
            "min_value": 1,
            "max_value": 65535,
        },
        "metric-l1": {
            "type": "integer",
            "help": "Level 1 metric for interface.",
            "default": 10,
            "min_value": 1,
            "max_value": 63,
        },
        "metric-l2": {
            "type": "integer",
            "help": "Level 2 metric for interface.",
            "default": 10,
            "min_value": 1,
            "max_value": 63,
        },
        "wide-metric-l1": {
            "type": "integer",
            "help": "Level 1 wide metric for interface.",
            "default": 10,
            "min_value": 1,
            "max_value": 16777214,
        },
        "wide-metric-l2": {
            "type": "integer",
            "help": "Level 2 wide metric for interface.",
            "default": 10,
            "min_value": 1,
            "max_value": 16777214,
        },
        "auth-password-l1": {
            "type": "password",
            "help": "Authentication password for level 1 PDUs.",
            "max_length": 128,
        },
        "auth-password-l2": {
            "type": "password",
            "help": "Authentication password for level 2 PDUs.",
            "max_length": 128,
        },
        "auth-keychain-l1": {
            "type": "string",
            "help": "Authentication key-chain for level 1 PDUs.",
            "default": "",
            "max_length": 35,
        },
        "auth-keychain-l2": {
            "type": "string",
            "help": "Authentication key-chain for level 2 PDUs.",
            "default": "",
            "max_length": 35,
        },
        "auth-send-only-l1": {
            "type": "option",
            "help": "Enable/disable authentication send-only for level 1 PDUs.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auth-send-only-l2": {
            "type": "option",
            "help": "Enable/disable authentication send-only for level 2 PDUs.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auth-mode-l1": {
            "type": "option",
            "help": "Level 1 authentication mode.",
            "default": "password",
            "options": ["md5", "password"],
        },
        "auth-mode-l2": {
            "type": "option",
            "help": "Level 2 authentication mode.",
            "default": "password",
            "options": ["md5", "password"],
        },
        "priority-l1": {
            "type": "integer",
            "help": "Level 1 priority.",
            "default": 64,
            "min_value": 0,
            "max_value": 127,
        },
        "priority-l2": {
            "type": "integer",
            "help": "Level 2 priority.",
            "default": 64,
            "min_value": 0,
            "max_value": 127,
        },
        "mesh-group": {
            "type": "option",
            "help": "Enable/disable IS-IS mesh group.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "mesh-group-id": {
            "type": "integer",
            "help": "Mesh group ID <0-4294967295>, 0: mesh-group blocked.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "summary-address": {
        "id": {
            "type": "integer",
            "help": "Summary address entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "prefix": {
            "type": "ipv4-classnet-any",
            "help": "Prefix.",
            "required": True,
            "default": "0.0.0.0 0.0.0.0",
        },
        "level": {
            "type": "option",
            "help": "Level.",
            "default": "level-2",
            "options": ["level-1-2", "level-1", "level-2"],
        },
    },
    "summary-address6": {
        "id": {
            "type": "integer",
            "help": "Prefix entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "prefix6": {
            "type": "ipv6-prefix",
            "help": "IPv6 prefix.",
            "required": True,
            "default": "::/0",
        },
        "level": {
            "type": "option",
            "help": "Level.",
            "default": "level-2",
            "options": ["level-1-2", "level-1", "level-2"],
        },
    },
    "redistribute": {
        "protocol": {
            "type": "string",
            "help": "Protocol name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "status": {
            "type": "option",
            "help": "Status.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "metric": {
            "type": "integer",
            "help": "Metric.",
            "default": 0,
            "min_value": 0,
            "max_value": 4261412864,
        },
        "metric-type": {
            "type": "option",
            "help": "Metric type.",
            "default": "internal",
            "options": ["external", "internal"],
        },
        "level": {
            "type": "option",
            "help": "Level.",
            "default": "level-2",
            "options": ["level-1-2", "level-1", "level-2"],
        },
        "routemap": {
            "type": "string",
            "help": "Route map name.",
            "default": "",
            "max_length": 35,
        },
    },
    "redistribute6": {
        "protocol": {
            "type": "string",
            "help": "Protocol name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable redistribution.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "metric": {
            "type": "integer",
            "help": "Metric.",
            "default": 0,
            "min_value": 0,
            "max_value": 4261412864,
        },
        "metric-type": {
            "type": "option",
            "help": "Metric type.",
            "default": "internal",
            "options": ["external", "internal"],
        },
        "level": {
            "type": "option",
            "help": "Level.",
            "default": "level-2",
            "options": ["level-1-2", "level-1", "level-2"],
        },
        "routemap": {
            "type": "string",
            "help": "Route map name.",
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_IS_TYPE = [
    "level-1-2",
    "level-1",
    "level-2-only",
]
VALID_BODY_ADV_PASSIVE_ONLY = [
    "enable",
    "disable",
]
VALID_BODY_ADV_PASSIVE_ONLY6 = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_MODE_L1 = [
    "password",
    "md5",
]
VALID_BODY_AUTH_MODE_L2 = [
    "password",
    "md5",
]
VALID_BODY_AUTH_SENDONLY_L1 = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_SENDONLY_L2 = [
    "enable",
    "disable",
]
VALID_BODY_IGNORE_LSP_ERRORS = [
    "enable",
    "disable",
]
VALID_BODY_DYNAMIC_HOSTNAME = [
    "enable",
    "disable",
]
VALID_BODY_ADJACENCY_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_ADJACENCY_CHECK6 = [
    "enable",
    "disable",
]
VALID_BODY_OVERLOAD_BIT = [
    "enable",
    "disable",
]
VALID_BODY_OVERLOAD_BIT_SUPPRESS = [
    "external",
    "interlevel",
]
VALID_BODY_DEFAULT_ORIGINATE = [
    "enable",
    "disable",
]
VALID_BODY_DEFAULT_ORIGINATE6 = [
    "enable",
    "disable",
]
VALID_BODY_METRIC_STYLE = [
    "narrow",
    "wide",
    "transition",
    "narrow-transition",
    "narrow-transition-l1",
    "narrow-transition-l2",
    "wide-l1",
    "wide-l2",
    "wide-transition",
    "wide-transition-l1",
    "wide-transition-l2",
    "transition-l1",
    "transition-l2",
]
VALID_BODY_REDISTRIBUTE_L1 = [
    "enable",
    "disable",
]
VALID_BODY_REDISTRIBUTE_L2 = [
    "enable",
    "disable",
]
VALID_BODY_REDISTRIBUTE6_L1 = [
    "enable",
    "disable",
]
VALID_BODY_REDISTRIBUTE6_L2 = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_router_isis_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for router/isis."""
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


def validate_router_isis_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new router/isis object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "is-type" in payload:
        is_valid, error = _validate_enum_field(
            "is-type",
            payload["is-type"],
            VALID_BODY_IS_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adv-passive-only" in payload:
        is_valid, error = _validate_enum_field(
            "adv-passive-only",
            payload["adv-passive-only"],
            VALID_BODY_ADV_PASSIVE_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adv-passive-only6" in payload:
        is_valid, error = _validate_enum_field(
            "adv-passive-only6",
            payload["adv-passive-only6"],
            VALID_BODY_ADV_PASSIVE_ONLY6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-mode-l1" in payload:
        is_valid, error = _validate_enum_field(
            "auth-mode-l1",
            payload["auth-mode-l1"],
            VALID_BODY_AUTH_MODE_L1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-mode-l2" in payload:
        is_valid, error = _validate_enum_field(
            "auth-mode-l2",
            payload["auth-mode-l2"],
            VALID_BODY_AUTH_MODE_L2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-sendonly-l1" in payload:
        is_valid, error = _validate_enum_field(
            "auth-sendonly-l1",
            payload["auth-sendonly-l1"],
            VALID_BODY_AUTH_SENDONLY_L1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-sendonly-l2" in payload:
        is_valid, error = _validate_enum_field(
            "auth-sendonly-l2",
            payload["auth-sendonly-l2"],
            VALID_BODY_AUTH_SENDONLY_L2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ignore-lsp-errors" in payload:
        is_valid, error = _validate_enum_field(
            "ignore-lsp-errors",
            payload["ignore-lsp-errors"],
            VALID_BODY_IGNORE_LSP_ERRORS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dynamic-hostname" in payload:
        is_valid, error = _validate_enum_field(
            "dynamic-hostname",
            payload["dynamic-hostname"],
            VALID_BODY_DYNAMIC_HOSTNAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adjacency-check" in payload:
        is_valid, error = _validate_enum_field(
            "adjacency-check",
            payload["adjacency-check"],
            VALID_BODY_ADJACENCY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adjacency-check6" in payload:
        is_valid, error = _validate_enum_field(
            "adjacency-check6",
            payload["adjacency-check6"],
            VALID_BODY_ADJACENCY_CHECK6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "overload-bit" in payload:
        is_valid, error = _validate_enum_field(
            "overload-bit",
            payload["overload-bit"],
            VALID_BODY_OVERLOAD_BIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "overload-bit-suppress" in payload:
        is_valid, error = _validate_enum_field(
            "overload-bit-suppress",
            payload["overload-bit-suppress"],
            VALID_BODY_OVERLOAD_BIT_SUPPRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-originate" in payload:
        is_valid, error = _validate_enum_field(
            "default-originate",
            payload["default-originate"],
            VALID_BODY_DEFAULT_ORIGINATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-originate6" in payload:
        is_valid, error = _validate_enum_field(
            "default-originate6",
            payload["default-originate6"],
            VALID_BODY_DEFAULT_ORIGINATE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "metric-style" in payload:
        is_valid, error = _validate_enum_field(
            "metric-style",
            payload["metric-style"],
            VALID_BODY_METRIC_STYLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redistribute-l1" in payload:
        is_valid, error = _validate_enum_field(
            "redistribute-l1",
            payload["redistribute-l1"],
            VALID_BODY_REDISTRIBUTE_L1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redistribute-l2" in payload:
        is_valid, error = _validate_enum_field(
            "redistribute-l2",
            payload["redistribute-l2"],
            VALID_BODY_REDISTRIBUTE_L2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redistribute6-l1" in payload:
        is_valid, error = _validate_enum_field(
            "redistribute6-l1",
            payload["redistribute6-l1"],
            VALID_BODY_REDISTRIBUTE6_L1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redistribute6-l2" in payload:
        is_valid, error = _validate_enum_field(
            "redistribute6-l2",
            payload["redistribute6-l2"],
            VALID_BODY_REDISTRIBUTE6_L2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_router_isis_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update router/isis."""
    # Validate enum values using central function
    if "is-type" in payload:
        is_valid, error = _validate_enum_field(
            "is-type",
            payload["is-type"],
            VALID_BODY_IS_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adv-passive-only" in payload:
        is_valid, error = _validate_enum_field(
            "adv-passive-only",
            payload["adv-passive-only"],
            VALID_BODY_ADV_PASSIVE_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adv-passive-only6" in payload:
        is_valid, error = _validate_enum_field(
            "adv-passive-only6",
            payload["adv-passive-only6"],
            VALID_BODY_ADV_PASSIVE_ONLY6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-mode-l1" in payload:
        is_valid, error = _validate_enum_field(
            "auth-mode-l1",
            payload["auth-mode-l1"],
            VALID_BODY_AUTH_MODE_L1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-mode-l2" in payload:
        is_valid, error = _validate_enum_field(
            "auth-mode-l2",
            payload["auth-mode-l2"],
            VALID_BODY_AUTH_MODE_L2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-sendonly-l1" in payload:
        is_valid, error = _validate_enum_field(
            "auth-sendonly-l1",
            payload["auth-sendonly-l1"],
            VALID_BODY_AUTH_SENDONLY_L1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-sendonly-l2" in payload:
        is_valid, error = _validate_enum_field(
            "auth-sendonly-l2",
            payload["auth-sendonly-l2"],
            VALID_BODY_AUTH_SENDONLY_L2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ignore-lsp-errors" in payload:
        is_valid, error = _validate_enum_field(
            "ignore-lsp-errors",
            payload["ignore-lsp-errors"],
            VALID_BODY_IGNORE_LSP_ERRORS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dynamic-hostname" in payload:
        is_valid, error = _validate_enum_field(
            "dynamic-hostname",
            payload["dynamic-hostname"],
            VALID_BODY_DYNAMIC_HOSTNAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adjacency-check" in payload:
        is_valid, error = _validate_enum_field(
            "adjacency-check",
            payload["adjacency-check"],
            VALID_BODY_ADJACENCY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adjacency-check6" in payload:
        is_valid, error = _validate_enum_field(
            "adjacency-check6",
            payload["adjacency-check6"],
            VALID_BODY_ADJACENCY_CHECK6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "overload-bit" in payload:
        is_valid, error = _validate_enum_field(
            "overload-bit",
            payload["overload-bit"],
            VALID_BODY_OVERLOAD_BIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "overload-bit-suppress" in payload:
        is_valid, error = _validate_enum_field(
            "overload-bit-suppress",
            payload["overload-bit-suppress"],
            VALID_BODY_OVERLOAD_BIT_SUPPRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-originate" in payload:
        is_valid, error = _validate_enum_field(
            "default-originate",
            payload["default-originate"],
            VALID_BODY_DEFAULT_ORIGINATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-originate6" in payload:
        is_valid, error = _validate_enum_field(
            "default-originate6",
            payload["default-originate6"],
            VALID_BODY_DEFAULT_ORIGINATE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "metric-style" in payload:
        is_valid, error = _validate_enum_field(
            "metric-style",
            payload["metric-style"],
            VALID_BODY_METRIC_STYLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redistribute-l1" in payload:
        is_valid, error = _validate_enum_field(
            "redistribute-l1",
            payload["redistribute-l1"],
            VALID_BODY_REDISTRIBUTE_L1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redistribute-l2" in payload:
        is_valid, error = _validate_enum_field(
            "redistribute-l2",
            payload["redistribute-l2"],
            VALID_BODY_REDISTRIBUTE_L2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redistribute6-l1" in payload:
        is_valid, error = _validate_enum_field(
            "redistribute6-l1",
            payload["redistribute6-l1"],
            VALID_BODY_REDISTRIBUTE6_L1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redistribute6-l2" in payload:
        is_valid, error = _validate_enum_field(
            "redistribute6-l2",
            payload["redistribute6-l2"],
            VALID_BODY_REDISTRIBUTE6_L2,
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
    "endpoint": "router/isis",
    "category": "cmdb",
    "api_path": "router/isis",
    "help": "Configure IS-IS.",
    "total_fields": 41,
    "required_fields_count": 0,
    "fields_with_defaults_count": 33,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
