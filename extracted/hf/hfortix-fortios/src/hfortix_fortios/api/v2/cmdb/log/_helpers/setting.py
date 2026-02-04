"""Validation helpers for log/setting - Auto-generated"""

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
    "resolve-ip": "disable",
    "resolve-port": "enable",
    "log-user-in-upper": "disable",
    "fwpolicy-implicit-log": "disable",
    "fwpolicy6-implicit-log": "disable",
    "extended-log": "disable",
    "local-in-allow": "disable",
    "local-in-deny-unicast": "disable",
    "local-in-deny-broadcast": "disable",
    "local-in-policy-log": "disable",
    "local-out": "enable",
    "local-out-ioc-detection": "enable",
    "daemon-log": "disable",
    "neighbor-event": "disable",
    "brief-traffic-format": "disable",
    "user-anonymize": "disable",
    "expolicy-implicit-log": "disable",
    "log-policy-comment": "disable",
    "faz-override": "disable",
    "syslog-override": "disable",
    "rest-api-set": "disable",
    "rest-api-get": "disable",
    "rest-api-performance": "disable",
    "long-live-session-stat": "enable",
    "extended-utm-log": "disable",
    "zone-name": "disable",
    "web-svc-perf": "disable",
    "anonymization-hash": "",
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
    "resolve-ip": "option",  # Enable/disable adding resolved domain names to traffic logs if possible.
    "resolve-port": "option",  # Enable/disable adding resolved service names to traffic logs.
    "log-user-in-upper": "option",  # Enable/disable logs with user-in-upper.
    "fwpolicy-implicit-log": "option",  # Enable/disable implicit firewall policy logging.
    "fwpolicy6-implicit-log": "option",  # Enable/disable implicit firewall policy6 logging.
    "extended-log": "option",  # Enable/disable extended traffic logging.
    "local-in-allow": "option",  # Enable/disable local-in-allow logging.
    "local-in-deny-unicast": "option",  # Enable/disable local-in-deny-unicast logging.
    "local-in-deny-broadcast": "option",  # Enable/disable local-in-deny-broadcast logging.
    "local-in-policy-log": "option",  # Enable/disable local-in-policy logging.
    "local-out": "option",  # Enable/disable local-out logging.
    "local-out-ioc-detection": "option",  # Enable/disable local-out traffic IoC detection. Requires local-out to be enabled
    "daemon-log": "option",  # Enable/disable daemon logging.
    "neighbor-event": "option",  # Enable/disable neighbor event logging.
    "brief-traffic-format": "option",  # Enable/disable brief format traffic logging.
    "user-anonymize": "option",  # Enable/disable anonymizing user names in log messages.
    "expolicy-implicit-log": "option",  # Enable/disable proxy firewall implicit policy logging.
    "log-policy-comment": "option",  # Enable/disable inserting policy comments into traffic logs.
    "faz-override": "option",  # Enable/disable override FortiAnalyzer settings.
    "syslog-override": "option",  # Enable/disable override Syslog settings.
    "rest-api-set": "option",  # Enable/disable REST API POST/PUT/DELETE request logging.
    "rest-api-get": "option",  # Enable/disable REST API GET request logging.
    "rest-api-performance": "option",  # Enable/disable REST API memory and performance stats in rest-api-get/set logs.
    "long-live-session-stat": "option",  # Enable/disable long-live-session statistics logging.
    "extended-utm-log": "option",  # Enable/disable extended UTM logging.
    "zone-name": "option",  # Enable/disable zone name logging.
    "web-svc-perf": "option",  # Enable/disable web-svc performance logging.
    "custom-log-fields": "string",  # Custom fields to append to all log messages.
    "anonymization-hash": "string",  # User name anonymization hash salt.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "resolve-ip": "Enable/disable adding resolved domain names to traffic logs if possible.",
    "resolve-port": "Enable/disable adding resolved service names to traffic logs.",
    "log-user-in-upper": "Enable/disable logs with user-in-upper.",
    "fwpolicy-implicit-log": "Enable/disable implicit firewall policy logging.",
    "fwpolicy6-implicit-log": "Enable/disable implicit firewall policy6 logging.",
    "extended-log": "Enable/disable extended traffic logging.",
    "local-in-allow": "Enable/disable local-in-allow logging.",
    "local-in-deny-unicast": "Enable/disable local-in-deny-unicast logging.",
    "local-in-deny-broadcast": "Enable/disable local-in-deny-broadcast logging.",
    "local-in-policy-log": "Enable/disable local-in-policy logging.",
    "local-out": "Enable/disable local-out logging.",
    "local-out-ioc-detection": "Enable/disable local-out traffic IoC detection. Requires local-out to be enabled.",
    "daemon-log": "Enable/disable daemon logging.",
    "neighbor-event": "Enable/disable neighbor event logging.",
    "brief-traffic-format": "Enable/disable brief format traffic logging.",
    "user-anonymize": "Enable/disable anonymizing user names in log messages.",
    "expolicy-implicit-log": "Enable/disable proxy firewall implicit policy logging.",
    "log-policy-comment": "Enable/disable inserting policy comments into traffic logs.",
    "faz-override": "Enable/disable override FortiAnalyzer settings.",
    "syslog-override": "Enable/disable override Syslog settings.",
    "rest-api-set": "Enable/disable REST API POST/PUT/DELETE request logging.",
    "rest-api-get": "Enable/disable REST API GET request logging.",
    "rest-api-performance": "Enable/disable REST API memory and performance stats in rest-api-get/set logs.",
    "long-live-session-stat": "Enable/disable long-live-session statistics logging.",
    "extended-utm-log": "Enable/disable extended UTM logging.",
    "zone-name": "Enable/disable zone name logging.",
    "web-svc-perf": "Enable/disable web-svc performance logging.",
    "custom-log-fields": "Custom fields to append to all log messages.",
    "anonymization-hash": "User name anonymization hash salt.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "anonymization-hash": {"type": "string", "max_length": 32},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "custom-log-fields": {
        "field-id": {
            "type": "string",
            "help": "Custom log field.",
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_RESOLVE_IP = [
    "enable",
    "disable",
]
VALID_BODY_RESOLVE_PORT = [
    "enable",
    "disable",
]
VALID_BODY_LOG_USER_IN_UPPER = [
    "enable",
    "disable",
]
VALID_BODY_FWPOLICY_IMPLICIT_LOG = [
    "enable",
    "disable",
]
VALID_BODY_FWPOLICY6_IMPLICIT_LOG = [
    "enable",
    "disable",
]
VALID_BODY_EXTENDED_LOG = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_IN_ALLOW = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_IN_DENY_UNICAST = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_IN_DENY_BROADCAST = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_IN_POLICY_LOG = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_OUT = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_OUT_IOC_DETECTION = [
    "enable",
    "disable",
]
VALID_BODY_DAEMON_LOG = [
    "enable",
    "disable",
]
VALID_BODY_NEIGHBOR_EVENT = [
    "enable",
    "disable",
]
VALID_BODY_BRIEF_TRAFFIC_FORMAT = [
    "enable",
    "disable",
]
VALID_BODY_USER_ANONYMIZE = [
    "enable",
    "disable",
]
VALID_BODY_EXPOLICY_IMPLICIT_LOG = [
    "enable",
    "disable",
]
VALID_BODY_LOG_POLICY_COMMENT = [
    "enable",
    "disable",
]
VALID_BODY_FAZ_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_SYSLOG_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_REST_API_SET = [
    "enable",
    "disable",
]
VALID_BODY_REST_API_GET = [
    "enable",
    "disable",
]
VALID_BODY_REST_API_PERFORMANCE = [
    "enable",
    "disable",
]
VALID_BODY_LONG_LIVE_SESSION_STAT = [
    "enable",
    "disable",
]
VALID_BODY_EXTENDED_UTM_LOG = [
    "enable",
    "disable",
]
VALID_BODY_ZONE_NAME = [
    "enable",
    "disable",
]
VALID_BODY_WEB_SVC_PERF = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_log_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for log/setting."""
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


def validate_log_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new log/setting object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "resolve-ip" in payload:
        is_valid, error = _validate_enum_field(
            "resolve-ip",
            payload["resolve-ip"],
            VALID_BODY_RESOLVE_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "resolve-port" in payload:
        is_valid, error = _validate_enum_field(
            "resolve-port",
            payload["resolve-port"],
            VALID_BODY_RESOLVE_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-user-in-upper" in payload:
        is_valid, error = _validate_enum_field(
            "log-user-in-upper",
            payload["log-user-in-upper"],
            VALID_BODY_LOG_USER_IN_UPPER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fwpolicy-implicit-log" in payload:
        is_valid, error = _validate_enum_field(
            "fwpolicy-implicit-log",
            payload["fwpolicy-implicit-log"],
            VALID_BODY_FWPOLICY_IMPLICIT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fwpolicy6-implicit-log" in payload:
        is_valid, error = _validate_enum_field(
            "fwpolicy6-implicit-log",
            payload["fwpolicy6-implicit-log"],
            VALID_BODY_FWPOLICY6_IMPLICIT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extended-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-log",
            payload["extended-log"],
            VALID_BODY_EXTENDED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-in-allow" in payload:
        is_valid, error = _validate_enum_field(
            "local-in-allow",
            payload["local-in-allow"],
            VALID_BODY_LOCAL_IN_ALLOW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-in-deny-unicast" in payload:
        is_valid, error = _validate_enum_field(
            "local-in-deny-unicast",
            payload["local-in-deny-unicast"],
            VALID_BODY_LOCAL_IN_DENY_UNICAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-in-deny-broadcast" in payload:
        is_valid, error = _validate_enum_field(
            "local-in-deny-broadcast",
            payload["local-in-deny-broadcast"],
            VALID_BODY_LOCAL_IN_DENY_BROADCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-in-policy-log" in payload:
        is_valid, error = _validate_enum_field(
            "local-in-policy-log",
            payload["local-in-policy-log"],
            VALID_BODY_LOCAL_IN_POLICY_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-out" in payload:
        is_valid, error = _validate_enum_field(
            "local-out",
            payload["local-out"],
            VALID_BODY_LOCAL_OUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-out-ioc-detection" in payload:
        is_valid, error = _validate_enum_field(
            "local-out-ioc-detection",
            payload["local-out-ioc-detection"],
            VALID_BODY_LOCAL_OUT_IOC_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "daemon-log" in payload:
        is_valid, error = _validate_enum_field(
            "daemon-log",
            payload["daemon-log"],
            VALID_BODY_DAEMON_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "neighbor-event" in payload:
        is_valid, error = _validate_enum_field(
            "neighbor-event",
            payload["neighbor-event"],
            VALID_BODY_NEIGHBOR_EVENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "brief-traffic-format" in payload:
        is_valid, error = _validate_enum_field(
            "brief-traffic-format",
            payload["brief-traffic-format"],
            VALID_BODY_BRIEF_TRAFFIC_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-anonymize" in payload:
        is_valid, error = _validate_enum_field(
            "user-anonymize",
            payload["user-anonymize"],
            VALID_BODY_USER_ANONYMIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "expolicy-implicit-log" in payload:
        is_valid, error = _validate_enum_field(
            "expolicy-implicit-log",
            payload["expolicy-implicit-log"],
            VALID_BODY_EXPOLICY_IMPLICIT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-policy-comment" in payload:
        is_valid, error = _validate_enum_field(
            "log-policy-comment",
            payload["log-policy-comment"],
            VALID_BODY_LOG_POLICY_COMMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "faz-override" in payload:
        is_valid, error = _validate_enum_field(
            "faz-override",
            payload["faz-override"],
            VALID_BODY_FAZ_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "syslog-override" in payload:
        is_valid, error = _validate_enum_field(
            "syslog-override",
            payload["syslog-override"],
            VALID_BODY_SYSLOG_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api-set" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api-set",
            payload["rest-api-set"],
            VALID_BODY_REST_API_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api-get" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api-get",
            payload["rest-api-get"],
            VALID_BODY_REST_API_GET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api-performance" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api-performance",
            payload["rest-api-performance"],
            VALID_BODY_REST_API_PERFORMANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "long-live-session-stat" in payload:
        is_valid, error = _validate_enum_field(
            "long-live-session-stat",
            payload["long-live-session-stat"],
            VALID_BODY_LONG_LIVE_SESSION_STAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extended-utm-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-utm-log",
            payload["extended-utm-log"],
            VALID_BODY_EXTENDED_UTM_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "zone-name" in payload:
        is_valid, error = _validate_enum_field(
            "zone-name",
            payload["zone-name"],
            VALID_BODY_ZONE_NAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-svc-perf" in payload:
        is_valid, error = _validate_enum_field(
            "web-svc-perf",
            payload["web-svc-perf"],
            VALID_BODY_WEB_SVC_PERF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_log_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update log/setting."""
    # Validate enum values using central function
    if "resolve-ip" in payload:
        is_valid, error = _validate_enum_field(
            "resolve-ip",
            payload["resolve-ip"],
            VALID_BODY_RESOLVE_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "resolve-port" in payload:
        is_valid, error = _validate_enum_field(
            "resolve-port",
            payload["resolve-port"],
            VALID_BODY_RESOLVE_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-user-in-upper" in payload:
        is_valid, error = _validate_enum_field(
            "log-user-in-upper",
            payload["log-user-in-upper"],
            VALID_BODY_LOG_USER_IN_UPPER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fwpolicy-implicit-log" in payload:
        is_valid, error = _validate_enum_field(
            "fwpolicy-implicit-log",
            payload["fwpolicy-implicit-log"],
            VALID_BODY_FWPOLICY_IMPLICIT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fwpolicy6-implicit-log" in payload:
        is_valid, error = _validate_enum_field(
            "fwpolicy6-implicit-log",
            payload["fwpolicy6-implicit-log"],
            VALID_BODY_FWPOLICY6_IMPLICIT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extended-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-log",
            payload["extended-log"],
            VALID_BODY_EXTENDED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-in-allow" in payload:
        is_valid, error = _validate_enum_field(
            "local-in-allow",
            payload["local-in-allow"],
            VALID_BODY_LOCAL_IN_ALLOW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-in-deny-unicast" in payload:
        is_valid, error = _validate_enum_field(
            "local-in-deny-unicast",
            payload["local-in-deny-unicast"],
            VALID_BODY_LOCAL_IN_DENY_UNICAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-in-deny-broadcast" in payload:
        is_valid, error = _validate_enum_field(
            "local-in-deny-broadcast",
            payload["local-in-deny-broadcast"],
            VALID_BODY_LOCAL_IN_DENY_BROADCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-in-policy-log" in payload:
        is_valid, error = _validate_enum_field(
            "local-in-policy-log",
            payload["local-in-policy-log"],
            VALID_BODY_LOCAL_IN_POLICY_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-out" in payload:
        is_valid, error = _validate_enum_field(
            "local-out",
            payload["local-out"],
            VALID_BODY_LOCAL_OUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-out-ioc-detection" in payload:
        is_valid, error = _validate_enum_field(
            "local-out-ioc-detection",
            payload["local-out-ioc-detection"],
            VALID_BODY_LOCAL_OUT_IOC_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "daemon-log" in payload:
        is_valid, error = _validate_enum_field(
            "daemon-log",
            payload["daemon-log"],
            VALID_BODY_DAEMON_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "neighbor-event" in payload:
        is_valid, error = _validate_enum_field(
            "neighbor-event",
            payload["neighbor-event"],
            VALID_BODY_NEIGHBOR_EVENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "brief-traffic-format" in payload:
        is_valid, error = _validate_enum_field(
            "brief-traffic-format",
            payload["brief-traffic-format"],
            VALID_BODY_BRIEF_TRAFFIC_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-anonymize" in payload:
        is_valid, error = _validate_enum_field(
            "user-anonymize",
            payload["user-anonymize"],
            VALID_BODY_USER_ANONYMIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "expolicy-implicit-log" in payload:
        is_valid, error = _validate_enum_field(
            "expolicy-implicit-log",
            payload["expolicy-implicit-log"],
            VALID_BODY_EXPOLICY_IMPLICIT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-policy-comment" in payload:
        is_valid, error = _validate_enum_field(
            "log-policy-comment",
            payload["log-policy-comment"],
            VALID_BODY_LOG_POLICY_COMMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "faz-override" in payload:
        is_valid, error = _validate_enum_field(
            "faz-override",
            payload["faz-override"],
            VALID_BODY_FAZ_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "syslog-override" in payload:
        is_valid, error = _validate_enum_field(
            "syslog-override",
            payload["syslog-override"],
            VALID_BODY_SYSLOG_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api-set" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api-set",
            payload["rest-api-set"],
            VALID_BODY_REST_API_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api-get" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api-get",
            payload["rest-api-get"],
            VALID_BODY_REST_API_GET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api-performance" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api-performance",
            payload["rest-api-performance"],
            VALID_BODY_REST_API_PERFORMANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "long-live-session-stat" in payload:
        is_valid, error = _validate_enum_field(
            "long-live-session-stat",
            payload["long-live-session-stat"],
            VALID_BODY_LONG_LIVE_SESSION_STAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extended-utm-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-utm-log",
            payload["extended-utm-log"],
            VALID_BODY_EXTENDED_UTM_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "zone-name" in payload:
        is_valid, error = _validate_enum_field(
            "zone-name",
            payload["zone-name"],
            VALID_BODY_ZONE_NAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-svc-perf" in payload:
        is_valid, error = _validate_enum_field(
            "web-svc-perf",
            payload["web-svc-perf"],
            VALID_BODY_WEB_SVC_PERF,
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
    "endpoint": "log/setting",
    "category": "cmdb",
    "api_path": "log/setting",
    "help": "Configure general log settings.",
    "total_fields": 29,
    "required_fields_count": 0,
    "fields_with_defaults_count": 28,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
