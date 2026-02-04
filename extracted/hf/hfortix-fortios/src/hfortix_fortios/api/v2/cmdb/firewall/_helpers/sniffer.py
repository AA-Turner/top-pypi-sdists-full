"""Validation helpers for firewall/sniffer - Auto-generated"""

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
    "application-list",  # Name of an existing application list.
    "ips-sensor",  # Name of an existing IPS sensor.
    "av-profile",  # Name of an existing antivirus profile.
    "webfilter-profile",  # Name of an existing web filter profile.
    "emailfilter-profile",  # Name of an existing email filter profile.
    "dlp-profile",  # Name of an existing DLP profile.
    "file-filter-profile",  # Name of an existing file-filter profile.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "id": 0,
    "uuid": "00000000-0000-0000-0000-000000000000",
    "status": "enable",
    "logtraffic": "utm",
    "ipv6": "disable",
    "non-ip": "disable",
    "interface": "",
    "host": "",
    "port": "",
    "protocol": "",
    "vlan": "",
    "application-list-status": "disable",
    "application-list": "",
    "ips-sensor-status": "disable",
    "ips-sensor": "",
    "dsri": "disable",
    "av-profile-status": "disable",
    "av-profile": "",
    "webfilter-profile-status": "disable",
    "webfilter-profile": "",
    "emailfilter-profile-status": "disable",
    "emailfilter-profile": "",
    "dlp-profile-status": "disable",
    "dlp-profile": "",
    "ip-threatfeed-status": "disable",
    "file-filter-profile-status": "disable",
    "file-filter-profile": "",
    "ips-dos-status": "disable",
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
    "id": "integer",  # Sniffer ID (0 - 9999).
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "status": "option",  # Enable/disable the active status of the sniffer.
    "logtraffic": "option",  # Either log all sessions, only sessions that have a security profile applied, or 
    "ipv6": "option",  # Enable/disable sniffing IPv6 packets.
    "non-ip": "option",  # Enable/disable sniffing non-IP packets.
    "interface": "string",  # Interface name that traffic sniffing will take place on.
    "host": "string",  # Hosts to filter for in sniffer traffic (Format examples: 1.1.1.1, 2.2.2.0/24, 3.
    "port": "string",  # Ports to sniff (Format examples: 10, :20, 30:40, 50-, 100-200).
    "protocol": "string",  # Integer value for the protocol type as defined by IANA (0 - 255).
    "vlan": "string",  # List of VLANs to sniff.
    "application-list-status": "option",  # Enable/disable application control profile.
    "application-list": "string",  # Name of an existing application list.
    "ips-sensor-status": "option",  # Enable/disable IPS sensor.
    "ips-sensor": "string",  # Name of an existing IPS sensor.
    "dsri": "option",  # Enable/disable DSRI.
    "av-profile-status": "option",  # Enable/disable antivirus profile.
    "av-profile": "string",  # Name of an existing antivirus profile.
    "webfilter-profile-status": "option",  # Enable/disable web filter profile.
    "webfilter-profile": "string",  # Name of an existing web filter profile.
    "emailfilter-profile-status": "option",  # Enable/disable emailfilter.
    "emailfilter-profile": "string",  # Name of an existing email filter profile.
    "dlp-profile-status": "option",  # Enable/disable DLP profile.
    "dlp-profile": "string",  # Name of an existing DLP profile.
    "ip-threatfeed-status": "option",  # Enable/disable IP threat feed.
    "ip-threatfeed": "string",  # Name of an existing IP threat feed.
    "file-filter-profile-status": "option",  # Enable/disable file filter.
    "file-filter-profile": "string",  # Name of an existing file-filter profile.
    "ips-dos-status": "option",  # Enable/disable IPS DoS anomaly detection.
    "anomaly": "string",  # Configuration method to edit Denial of Service (DoS) anomaly settings.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "id": "Sniffer ID (0 - 9999).",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "status": "Enable/disable the active status of the sniffer.",
    "logtraffic": "Either log all sessions, only sessions that have a security profile applied, or disable all logging for this policy.",
    "ipv6": "Enable/disable sniffing IPv6 packets.",
    "non-ip": "Enable/disable sniffing non-IP packets.",
    "interface": "Interface name that traffic sniffing will take place on.",
    "host": "Hosts to filter for in sniffer traffic (Format examples: 1.1.1.1, 2.2.2.0/24, 3.3.3.3/255.255.255.0, 4.4.4.0-4.4.4.240).",
    "port": "Ports to sniff (Format examples: 10, :20, 30:40, 50-, 100-200).",
    "protocol": "Integer value for the protocol type as defined by IANA (0 - 255).",
    "vlan": "List of VLANs to sniff.",
    "application-list-status": "Enable/disable application control profile.",
    "application-list": "Name of an existing application list.",
    "ips-sensor-status": "Enable/disable IPS sensor.",
    "ips-sensor": "Name of an existing IPS sensor.",
    "dsri": "Enable/disable DSRI.",
    "av-profile-status": "Enable/disable antivirus profile.",
    "av-profile": "Name of an existing antivirus profile.",
    "webfilter-profile-status": "Enable/disable web filter profile.",
    "webfilter-profile": "Name of an existing web filter profile.",
    "emailfilter-profile-status": "Enable/disable emailfilter.",
    "emailfilter-profile": "Name of an existing email filter profile.",
    "dlp-profile-status": "Enable/disable DLP profile.",
    "dlp-profile": "Name of an existing DLP profile.",
    "ip-threatfeed-status": "Enable/disable IP threat feed.",
    "ip-threatfeed": "Name of an existing IP threat feed.",
    "file-filter-profile-status": "Enable/disable file filter.",
    "file-filter-profile": "Name of an existing file-filter profile.",
    "ips-dos-status": "Enable/disable IPS DoS anomaly detection.",
    "anomaly": "Configuration method to edit Denial of Service (DoS) anomaly settings.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "id": {"type": "integer", "min": 0, "max": 9999},
    "interface": {"type": "string", "max_length": 35},
    "host": {"type": "string", "max_length": 63},
    "port": {"type": "string", "max_length": 63},
    "protocol": {"type": "string", "max_length": 63},
    "vlan": {"type": "string", "max_length": 63},
    "application-list": {"type": "string", "max_length": 47},
    "ips-sensor": {"type": "string", "max_length": 47},
    "av-profile": {"type": "string", "max_length": 47},
    "webfilter-profile": {"type": "string", "max_length": 47},
    "emailfilter-profile": {"type": "string", "max_length": 47},
    "dlp-profile": {"type": "string", "max_length": 47},
    "file-filter-profile": {"type": "string", "max_length": 47},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "ip-threatfeed": {
        "name": {
            "type": "string",
            "help": "Threat feed name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "anomaly": {
        "name": {
            "type": "string",
            "help": "Anomaly name.",
            "default": "",
            "max_length": 63,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable this anomaly.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "log": {
            "type": "option",
            "help": "Enable/disable anomaly logging.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "action": {
            "type": "option",
            "help": "Action taken when the threshold is reached.",
            "default": "pass",
            "options": ["pass", "block"],
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
        "threshold": {
            "type": "integer",
            "help": "Anomaly threshold. Number of detected instances (packets per second or concurrent session number) that triggers the anomaly action.",
            "default": 0,
            "min_value": 1,
            "max_value": 2147483647,
        },
        "threshold(default)": {
            "type": "integer",
            "help": "Number of detected instances (packets per second or concurrent session number) which triggers action (1 - 2147483647, default = 1000). Note that each anomaly has a different threshold value assigned to it.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_LOGTRAFFIC = [
    "all",
    "utm",
    "disable",
]
VALID_BODY_IPV6 = [
    "enable",
    "disable",
]
VALID_BODY_NON_IP = [
    "enable",
    "disable",
]
VALID_BODY_APPLICATION_LIST_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_IPS_SENSOR_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_DSRI = [
    "enable",
    "disable",
]
VALID_BODY_AV_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_WEBFILTER_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_EMAILFILTER_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_DLP_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_IP_THREATFEED_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_FILE_FILTER_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_IPS_DOS_STATUS = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_sniffer_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/sniffer."""
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


def validate_firewall_sniffer_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/sniffer object."""
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
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6",
            payload["ipv6"],
            VALID_BODY_IPV6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "non-ip" in payload:
        is_valid, error = _validate_enum_field(
            "non-ip",
            payload["non-ip"],
            VALID_BODY_NON_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-list-status" in payload:
        is_valid, error = _validate_enum_field(
            "application-list-status",
            payload["application-list-status"],
            VALID_BODY_APPLICATION_LIST_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ips-sensor-status" in payload:
        is_valid, error = _validate_enum_field(
            "ips-sensor-status",
            payload["ips-sensor-status"],
            VALID_BODY_IPS_SENSOR_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dsri" in payload:
        is_valid, error = _validate_enum_field(
            "dsri",
            payload["dsri"],
            VALID_BODY_DSRI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "av-profile-status",
            payload["av-profile-status"],
            VALID_BODY_AV_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-profile-status",
            payload["webfilter-profile-status"],
            VALID_BODY_WEBFILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "emailfilter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "emailfilter-profile-status",
            payload["emailfilter-profile-status"],
            VALID_BODY_EMAILFILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dlp-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "dlp-profile-status",
            payload["dlp-profile-status"],
            VALID_BODY_DLP_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-threatfeed-status" in payload:
        is_valid, error = _validate_enum_field(
            "ip-threatfeed-status",
            payload["ip-threatfeed-status"],
            VALID_BODY_IP_THREATFEED_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-filter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "file-filter-profile-status",
            payload["file-filter-profile-status"],
            VALID_BODY_FILE_FILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ips-dos-status" in payload:
        is_valid, error = _validate_enum_field(
            "ips-dos-status",
            payload["ips-dos-status"],
            VALID_BODY_IPS_DOS_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_sniffer_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/sniffer."""
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
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6",
            payload["ipv6"],
            VALID_BODY_IPV6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "non-ip" in payload:
        is_valid, error = _validate_enum_field(
            "non-ip",
            payload["non-ip"],
            VALID_BODY_NON_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-list-status" in payload:
        is_valid, error = _validate_enum_field(
            "application-list-status",
            payload["application-list-status"],
            VALID_BODY_APPLICATION_LIST_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ips-sensor-status" in payload:
        is_valid, error = _validate_enum_field(
            "ips-sensor-status",
            payload["ips-sensor-status"],
            VALID_BODY_IPS_SENSOR_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dsri" in payload:
        is_valid, error = _validate_enum_field(
            "dsri",
            payload["dsri"],
            VALID_BODY_DSRI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "av-profile-status",
            payload["av-profile-status"],
            VALID_BODY_AV_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-profile-status",
            payload["webfilter-profile-status"],
            VALID_BODY_WEBFILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "emailfilter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "emailfilter-profile-status",
            payload["emailfilter-profile-status"],
            VALID_BODY_EMAILFILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dlp-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "dlp-profile-status",
            payload["dlp-profile-status"],
            VALID_BODY_DLP_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-threatfeed-status" in payload:
        is_valid, error = _validate_enum_field(
            "ip-threatfeed-status",
            payload["ip-threatfeed-status"],
            VALID_BODY_IP_THREATFEED_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-filter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "file-filter-profile-status",
            payload["file-filter-profile-status"],
            VALID_BODY_FILE_FILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ips-dos-status" in payload:
        is_valid, error = _validate_enum_field(
            "ips-dos-status",
            payload["ips-dos-status"],
            VALID_BODY_IPS_DOS_STATUS,
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
    "endpoint": "firewall/sniffer",
    "category": "cmdb",
    "api_path": "firewall/sniffer",
    "mkey": "id",
    "mkey_type": "integer",
    "help": "Configure sniffer.",
    "total_fields": 30,
    "required_fields_count": 7,
    "fields_with_defaults_count": 28,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
