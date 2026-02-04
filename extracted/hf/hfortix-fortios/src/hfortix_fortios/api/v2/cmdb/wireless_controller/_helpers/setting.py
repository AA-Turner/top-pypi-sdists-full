"""Validation helpers for wireless_controller/setting - Auto-generated"""

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
    "account-id": "",
    "country": "US",
    "duplicate-ssid": "disable",
    "fapc-compatibility": "disable",
    "wfa-compatibility": "disable",
    "phishing-ssid-detect": "enable",
    "fake-ssid-action": "log",
    "device-weight": 1,
    "device-holdoff": 5,
    "device-idle": 1440,
    "firmware-provision-on-authorization": "disable",
    "rolling-wtp-upgrade": "disable",
    "darrp-optimize": 86400,
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
    "account-id": "string",  # FortiCloud customer account ID.
    "country": "option",  # Country or region in which the FortiGate is located. The country determines the 
    "duplicate-ssid": "option",  # Enable/disable allowing Virtual Access Points (VAPs) to use the same SSID name i
    "fapc-compatibility": "option",  # Enable/disable FAP-C series compatibility.
    "wfa-compatibility": "option",  # Enable/disable WFA compatibility.
    "phishing-ssid-detect": "option",  # Enable/disable phishing SSID detection.
    "fake-ssid-action": "option",  # Actions taken for detected fake SSID.
    "offending-ssid": "string",  # Configure offending SSID.
    "device-weight": "integer",  # Upper limit of confidence of device for identification (0 - 255, default = 1, 0 
    "device-holdoff": "integer",  # Lower limit of creation time of device for identification in minutes (0 - 60, de
    "device-idle": "integer",  # Upper limit of idle time of device for identification in minutes (0 - 14400, def
    "firmware-provision-on-authorization": "option",  # Enable/disable automatic provisioning of latest firmware on authorization.
    "rolling-wtp-upgrade": "option",  # Enable/disable rolling WTP upgrade (default = disable).
    "darrp-optimize": "integer",  # Time for running Distributed Automatic Radio Resource Provisioning (DARRP) optim
    "darrp-optimize-schedules": "string",  # Firewall schedules for DARRP running time. DARRP will run periodically based on 
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "account-id": "FortiCloud customer account ID.",
    "country": "Country or region in which the FortiGate is located. The country determines the 802.11 bands and channels that are available.",
    "duplicate-ssid": "Enable/disable allowing Virtual Access Points (VAPs) to use the same SSID name in the same VDOM.",
    "fapc-compatibility": "Enable/disable FAP-C series compatibility.",
    "wfa-compatibility": "Enable/disable WFA compatibility.",
    "phishing-ssid-detect": "Enable/disable phishing SSID detection.",
    "fake-ssid-action": "Actions taken for detected fake SSID.",
    "offending-ssid": "Configure offending SSID.",
    "device-weight": "Upper limit of confidence of device for identification (0 - 255, default = 1, 0 = disable).",
    "device-holdoff": "Lower limit of creation time of device for identification in minutes (0 - 60, default = 5).",
    "device-idle": "Upper limit of idle time of device for identification in minutes (0 - 14400, default = 1440).",
    "firmware-provision-on-authorization": "Enable/disable automatic provisioning of latest firmware on authorization.",
    "rolling-wtp-upgrade": "Enable/disable rolling WTP upgrade (default = disable).",
    "darrp-optimize": "Time for running Distributed Automatic Radio Resource Provisioning (DARRP) optimizations (0 - 86400 sec, default = 86400, 0 = disable).",
    "darrp-optimize-schedules": "Firewall schedules for DARRP running time. DARRP will run periodically based on darrp-optimize within the schedules. Separate multiple schedule names with a space.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "account-id": {"type": "string", "max_length": 63},
    "device-weight": {"type": "integer", "min": 0, "max": 255},
    "device-holdoff": {"type": "integer", "min": 0, "max": 60},
    "device-idle": {"type": "integer", "min": 0, "max": 14400},
    "darrp-optimize": {"type": "integer", "min": 0, "max": 86400},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "offending-ssid": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "ssid-pattern": {
            "type": "string",
            "help": "Define offending SSID pattern (case insensitive). For example, word, word*, *word, wo*rd.",
            "required": True,
            "default": "",
            "max_length": 33,
        },
        "action": {
            "type": "option",
            "help": "Actions taken for detected offending SSID.",
            "default": "log",
            "options": ["log", "suppress"],
        },
    },
    "darrp-optimize-schedules": {
        "name": {
            "type": "string",
            "help": "Schedule name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_COUNTRY = [
    "--",
    "AF",
    "AL",
    "DZ",
    "AS",
    "AO",
    "AR",
    "AM",
    "AU",
    "AT",
    "AZ",
    "BS",
    "BH",
    "BD",
    "BB",
    "BY",
    "BE",
    "BZ",
    "BJ",
    "BM",
    "BT",
    "BO",
    "BA",
    "BW",
    "BR",
    "BN",
    "BG",
    "BF",
    "KH",
    "CM",
    "KY",
    "CF",
    "TD",
    "CL",
    "CN",
    "CX",
    "CO",
    "CG",
    "CD",
    "CR",
    "HR",
    "CY",
    "CZ",
    "DK",
    "DJ",
    "DM",
    "DO",
    "EC",
    "EG",
    "SV",
    "ET",
    "EE",
    "GF",
    "PF",
    "FO",
    "FJ",
    "FI",
    "FR",
    "GA",
    "GE",
    "GM",
    "DE",
    "GH",
    "GI",
    "GR",
    "GL",
    "GD",
    "GP",
    "GU",
    "GT",
    "GY",
    "HT",
    "HN",
    "HK",
    "HU",
    "IS",
    "IN",
    "ID",
    "IQ",
    "IE",
    "IM",
    "IL",
    "IT",
    "CI",
    "JM",
    "JO",
    "KZ",
    "KE",
    "KR",
    "KW",
    "LA",
    "LV",
    "LB",
    "LS",
    "LR",
    "LY",
    "LI",
    "LT",
    "LU",
    "MO",
    "MK",
    "MG",
    "MW",
    "MY",
    "MV",
    "ML",
    "MT",
    "MH",
    "MQ",
    "MR",
    "MU",
    "YT",
    "MX",
    "FM",
    "MD",
    "MC",
    "MN",
    "MA",
    "MZ",
    "MM",
    "NA",
    "NP",
    "NL",
    "AN",
    "AW",
    "NZ",
    "NI",
    "NE",
    "NG",
    "NO",
    "MP",
    "OM",
    "PK",
    "PW",
    "PA",
    "PG",
    "PY",
    "PE",
    "PH",
    "PL",
    "PT",
    "PR",
    "QA",
    "RE",
    "RO",
    "RU",
    "RW",
    "BL",
    "KN",
    "LC",
    "MF",
    "PM",
    "VC",
    "SA",
    "SN",
    "RS",
    "ME",
    "SL",
    "SG",
    "SK",
    "SI",
    "SO",
    "ZA",
    "ES",
    "LK",
    "SR",
    "SZ",
    "SE",
    "CH",
    "TW",
    "TZ",
    "TH",
    "TL",
    "TG",
    "TT",
    "TN",
    "TR",
    "TM",
    "AE",
    "TC",
    "UG",
    "UA",
    "GB",
    "US",
    "PS",
    "UY",
    "UZ",
    "VU",
    "VE",
    "VN",
    "VI",
    "WF",
    "YE",
    "ZM",
    "ZW",
    "JP",
    "CA",
]
VALID_BODY_DUPLICATE_SSID = [
    "enable",
    "disable",
]
VALID_BODY_FAPC_COMPATIBILITY = [
    "enable",
    "disable",
]
VALID_BODY_WFA_COMPATIBILITY = [
    "enable",
    "disable",
]
VALID_BODY_PHISHING_SSID_DETECT = [
    "enable",
    "disable",
]
VALID_BODY_FAKE_SSID_ACTION = [
    "log",
    "suppress",
]
VALID_BODY_FIRMWARE_PROVISION_ON_AUTHORIZATION = [
    "enable",
    "disable",
]
VALID_BODY_ROLLING_WTP_UPGRADE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/setting."""
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


def validate_wireless_controller_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/setting object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "country" in payload:
        is_valid, error = _validate_enum_field(
            "country",
            payload["country"],
            VALID_BODY_COUNTRY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "duplicate-ssid" in payload:
        is_valid, error = _validate_enum_field(
            "duplicate-ssid",
            payload["duplicate-ssid"],
            VALID_BODY_DUPLICATE_SSID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fapc-compatibility" in payload:
        is_valid, error = _validate_enum_field(
            "fapc-compatibility",
            payload["fapc-compatibility"],
            VALID_BODY_FAPC_COMPATIBILITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wfa-compatibility" in payload:
        is_valid, error = _validate_enum_field(
            "wfa-compatibility",
            payload["wfa-compatibility"],
            VALID_BODY_WFA_COMPATIBILITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "phishing-ssid-detect" in payload:
        is_valid, error = _validate_enum_field(
            "phishing-ssid-detect",
            payload["phishing-ssid-detect"],
            VALID_BODY_PHISHING_SSID_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fake-ssid-action" in payload:
        is_valid, error = _validate_enum_field(
            "fake-ssid-action",
            payload["fake-ssid-action"],
            VALID_BODY_FAKE_SSID_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firmware-provision-on-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision-on-authorization",
            payload["firmware-provision-on-authorization"],
            VALID_BODY_FIRMWARE_PROVISION_ON_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rolling-wtp-upgrade" in payload:
        is_valid, error = _validate_enum_field(
            "rolling-wtp-upgrade",
            payload["rolling-wtp-upgrade"],
            VALID_BODY_ROLLING_WTP_UPGRADE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/setting."""
    # Validate enum values using central function
    if "country" in payload:
        is_valid, error = _validate_enum_field(
            "country",
            payload["country"],
            VALID_BODY_COUNTRY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "duplicate-ssid" in payload:
        is_valid, error = _validate_enum_field(
            "duplicate-ssid",
            payload["duplicate-ssid"],
            VALID_BODY_DUPLICATE_SSID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fapc-compatibility" in payload:
        is_valid, error = _validate_enum_field(
            "fapc-compatibility",
            payload["fapc-compatibility"],
            VALID_BODY_FAPC_COMPATIBILITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wfa-compatibility" in payload:
        is_valid, error = _validate_enum_field(
            "wfa-compatibility",
            payload["wfa-compatibility"],
            VALID_BODY_WFA_COMPATIBILITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "phishing-ssid-detect" in payload:
        is_valid, error = _validate_enum_field(
            "phishing-ssid-detect",
            payload["phishing-ssid-detect"],
            VALID_BODY_PHISHING_SSID_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fake-ssid-action" in payload:
        is_valid, error = _validate_enum_field(
            "fake-ssid-action",
            payload["fake-ssid-action"],
            VALID_BODY_FAKE_SSID_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firmware-provision-on-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision-on-authorization",
            payload["firmware-provision-on-authorization"],
            VALID_BODY_FIRMWARE_PROVISION_ON_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rolling-wtp-upgrade" in payload:
        is_valid, error = _validate_enum_field(
            "rolling-wtp-upgrade",
            payload["rolling-wtp-upgrade"],
            VALID_BODY_ROLLING_WTP_UPGRADE,
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
    "endpoint": "wireless_controller/setting",
    "category": "cmdb",
    "api_path": "wireless-controller/setting",
    "help": "VDOM wireless controller configuration.",
    "total_fields": 15,
    "required_fields_count": 0,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
