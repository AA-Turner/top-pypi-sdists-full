"""Validation helpers for wireless_controller/hotspot20/hs_profile - Auto-generated"""

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
    "name": "",
    "release": 2,
    "access-network-type": "private-network",
    "access-network-internet": "disable",
    "access-network-asra": "disable",
    "access-network-esr": "disable",
    "access-network-uesa": "disable",
    "venue-group": "unspecified",
    "venue-type": "unspecified",
    "hessid": "00:00:00:00:00:00",
    "proxy-arp": "enable",
    "l2tif": "disable",
    "pame-bi": "enable",
    "anqp-domain-id": 0,
    "domain-name": "",
    "osu-ssid": "",
    "gas-comeback-delay": 500,
    "gas-fragmentation-limit": 1024,
    "dgaf": "disable",
    "deauth-request-timeout": 60,
    "wnm-sleep-mode": "disable",
    "bss-transition": "disable",
    "venue-name": "",
    "venue-url": "",
    "roaming-consortium": "",
    "nai-realm": "",
    "oper-friendly-name": "",
    "oper-icon": "",
    "advice-of-charge": "",
    "osu-provider-nai": "",
    "terms-and-conditions": "",
    "wan-metrics": "",
    "network-auth": "",
    "3gpp-plmn": "",
    "conn-cap": "",
    "qos-map": "",
    "ip-addr-type": "",
    "wba-open-roaming": "disable",
    "wba-financial-clearing-provider": "",
    "wba-data-clearing-provider": "",
    "wba-charging-currency": "",
    "wba-charging-rate": 0,
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
    "name": "string",  # Hotspot profile name.
    "release": "integer",  # Hotspot 2.0 Release number (1, 2, 3, default = 2).
    "access-network-type": "option",  # Access network type.
    "access-network-internet": "option",  # Enable/disable connectivity to the Internet.
    "access-network-asra": "option",  # Enable/disable additional step required for access (ASRA).
    "access-network-esr": "option",  # Enable/disable emergency services reachable (ESR).
    "access-network-uesa": "option",  # Enable/disable unauthenticated emergency service accessible 
    "venue-group": "option",  # Venue group.
    "venue-type": "option",  # Venue type.
    "hessid": "mac-address",  # Homogeneous extended service set identifier (HESSID).
    "proxy-arp": "option",  # Enable/disable Proxy ARP.
    "l2tif": "option",  # Enable/disable Layer 2 traffic inspection and filtering.
    "pame-bi": "option",  # Enable/disable Pre-Association Message Exchange BSSID Indepe
    "anqp-domain-id": "integer",  # ANQP Domain ID (0-65535).
    "domain-name": "string",  # Domain name.
    "osu-ssid": "string",  # Online sign up (OSU) SSID.
    "gas-comeback-delay": "integer",  # GAS comeback delay (0 or 100 - 10000 milliseconds, default =
    "gas-fragmentation-limit": "integer",  # GAS fragmentation limit (512 - 4096, default = 1024).
    "dgaf": "option",  # Enable/disable downstream group-addressed forwarding (DGAF).
    "deauth-request-timeout": "integer",  # Deauthentication request timeout (in seconds).
    "wnm-sleep-mode": "option",  # Enable/disable wireless network management (WNM) sleep mode.
    "bss-transition": "option",  # Enable/disable basic service set (BSS) transition Support.
    "venue-name": "string",  # Venue name.
    "venue-url": "string",  # Venue name.
    "roaming-consortium": "string",  # Roaming consortium list name.
    "nai-realm": "string",  # NAI realm list name.
    "oper-friendly-name": "string",  # Operator friendly name.
    "oper-icon": "string",  # Operator icon.
    "advice-of-charge": "string",  # Advice of charge.
    "osu-provider-nai": "string",  # OSU Provider NAI.
    "terms-and-conditions": "string",  # Terms and conditions.
    "osu-provider": "string",  # Manually selected list of OSU provider(s).
    "wan-metrics": "string",  # WAN metric name.
    "network-auth": "string",  # Network authentication name.
    "3gpp-plmn": "string",  # 3GPP PLMN name.
    "conn-cap": "string",  # Connection capability name.
    "qos-map": "string",  # QoS MAP set ID.
    "ip-addr-type": "string",  # IP address type name.
    "wba-open-roaming": "option",  # Enable/disable WBA open roaming support.
    "wba-financial-clearing-provider": "string",  # WBA ID of financial clearing provider.
    "wba-data-clearing-provider": "string",  # WBA ID of data clearing provider.
    "wba-charging-currency": "string",  # Three letter currency code.
    "wba-charging-rate": "integer",  # Number of currency units per kilobyte.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Hotspot profile name.",
    "release": "Hotspot 2.0 Release number (1, 2, 3, default = 2).",
    "access-network-type": "Access network type.",
    "access-network-internet": "Enable/disable connectivity to the Internet.",
    "access-network-asra": "Enable/disable additional step required for access (ASRA).",
    "access-network-esr": "Enable/disable emergency services reachable (ESR).",
    "access-network-uesa": "Enable/disable unauthenticated emergency service accessible (UESA).",
    "venue-group": "Venue group.",
    "venue-type": "Venue type.",
    "hessid": "Homogeneous extended service set identifier (HESSID).",
    "proxy-arp": "Enable/disable Proxy ARP.",
    "l2tif": "Enable/disable Layer 2 traffic inspection and filtering.",
    "pame-bi": "Enable/disable Pre-Association Message Exchange BSSID Independent (PAME-BI).",
    "anqp-domain-id": "ANQP Domain ID (0-65535).",
    "domain-name": "Domain name.",
    "osu-ssid": "Online sign up (OSU) SSID.",
    "gas-comeback-delay": "GAS comeback delay (0 or 100 - 10000 milliseconds, default = 500).",
    "gas-fragmentation-limit": "GAS fragmentation limit (512 - 4096, default = 1024).",
    "dgaf": "Enable/disable downstream group-addressed forwarding (DGAF).",
    "deauth-request-timeout": "Deauthentication request timeout (in seconds).",
    "wnm-sleep-mode": "Enable/disable wireless network management (WNM) sleep mode.",
    "bss-transition": "Enable/disable basic service set (BSS) transition Support.",
    "venue-name": "Venue name.",
    "venue-url": "Venue name.",
    "roaming-consortium": "Roaming consortium list name.",
    "nai-realm": "NAI realm list name.",
    "oper-friendly-name": "Operator friendly name.",
    "oper-icon": "Operator icon.",
    "advice-of-charge": "Advice of charge.",
    "osu-provider-nai": "OSU Provider NAI.",
    "terms-and-conditions": "Terms and conditions.",
    "osu-provider": "Manually selected list of OSU provider(s).",
    "wan-metrics": "WAN metric name.",
    "network-auth": "Network authentication name.",
    "3gpp-plmn": "3GPP PLMN name.",
    "conn-cap": "Connection capability name.",
    "qos-map": "QoS MAP set ID.",
    "ip-addr-type": "IP address type name.",
    "wba-open-roaming": "Enable/disable WBA open roaming support.",
    "wba-financial-clearing-provider": "WBA ID of financial clearing provider.",
    "wba-data-clearing-provider": "WBA ID of data clearing provider.",
    "wba-charging-currency": "Three letter currency code.",
    "wba-charging-rate": "Number of currency units per kilobyte.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "release": {"type": "integer", "min": 1, "max": 3},
    "anqp-domain-id": {"type": "integer", "min": 0, "max": 65535},
    "domain-name": {"type": "string", "max_length": 255},
    "osu-ssid": {"type": "string", "max_length": 255},
    "gas-comeback-delay": {"type": "integer", "min": 100, "max": 10000},
    "gas-fragmentation-limit": {"type": "integer", "min": 512, "max": 4096},
    "deauth-request-timeout": {"type": "integer", "min": 30, "max": 120},
    "venue-name": {"type": "string", "max_length": 35},
    "venue-url": {"type": "string", "max_length": 35},
    "roaming-consortium": {"type": "string", "max_length": 35},
    "nai-realm": {"type": "string", "max_length": 35},
    "oper-friendly-name": {"type": "string", "max_length": 35},
    "oper-icon": {"type": "string", "max_length": 35},
    "advice-of-charge": {"type": "string", "max_length": 35},
    "osu-provider-nai": {"type": "string", "max_length": 35},
    "terms-and-conditions": {"type": "string", "max_length": 35},
    "wan-metrics": {"type": "string", "max_length": 35},
    "network-auth": {"type": "string", "max_length": 35},
    "3gpp-plmn": {"type": "string", "max_length": 35},
    "conn-cap": {"type": "string", "max_length": 35},
    "qos-map": {"type": "string", "max_length": 35},
    "ip-addr-type": {"type": "string", "max_length": 35},
    "wba-financial-clearing-provider": {"type": "string", "max_length": 127},
    "wba-data-clearing-provider": {"type": "string", "max_length": 127},
    "wba-charging-currency": {"type": "string", "max_length": 3},
    "wba-charging-rate": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "osu-provider": {
        "name": {
            "type": "string",
            "help": "OSU provider name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_ACCESS_NETWORK_TYPE = [
    "private-network",
    "private-network-with-guest-access",
    "chargeable-public-network",
    "free-public-network",
    "personal-device-network",
    "emergency-services-only-network",
    "test-or-experimental",
    "wildcard",
]
VALID_BODY_ACCESS_NETWORK_INTERNET = [
    "enable",
    "disable",
]
VALID_BODY_ACCESS_NETWORK_ASRA = [
    "enable",
    "disable",
]
VALID_BODY_ACCESS_NETWORK_ESR = [
    "enable",
    "disable",
]
VALID_BODY_ACCESS_NETWORK_UESA = [
    "enable",
    "disable",
]
VALID_BODY_VENUE_GROUP = [
    "unspecified",
    "assembly",
    "business",
    "educational",
    "factory",
    "institutional",
    "mercantile",
    "residential",
    "storage",
    "utility",
    "vehicular",
    "outdoor",
]
VALID_BODY_VENUE_TYPE = [
    "unspecified",
    "arena",
    "stadium",
    "passenger-terminal",
    "amphitheater",
    "amusement-park",
    "place-of-worship",
    "convention-center",
    "library",
    "museum",
    "restaurant",
    "theater",
    "bar",
    "coffee-shop",
    "zoo-or-aquarium",
    "emergency-center",
    "doctor-office",
    "bank",
    "fire-station",
    "police-station",
    "post-office",
    "professional-office",
    "research-facility",
    "attorney-office",
    "primary-school",
    "secondary-school",
    "university-or-college",
    "factory",
    "hospital",
    "long-term-care-facility",
    "rehab-center",
    "group-home",
    "prison-or-jail",
    "retail-store",
    "grocery-market",
    "auto-service-station",
    "shopping-mall",
    "gas-station",
    "private",
    "hotel-or-motel",
    "dormitory",
    "boarding-house",
    "automobile",
    "airplane",
    "bus",
    "ferry",
    "ship-or-boat",
    "train",
    "motor-bike",
    "muni-mesh-network",
    "city-park",
    "rest-area",
    "traffic-control",
    "bus-stop",
    "kiosk",
]
VALID_BODY_PROXY_ARP = [
    "enable",
    "disable",
]
VALID_BODY_L2TIF = [
    "enable",
    "disable",
]
VALID_BODY_PAME_BI = [
    "disable",
    "enable",
]
VALID_BODY_DGAF = [
    "enable",
    "disable",
]
VALID_BODY_WNM_SLEEP_MODE = [
    "enable",
    "disable",
]
VALID_BODY_BSS_TRANSITION = [
    "enable",
    "disable",
]
VALID_BODY_WBA_OPEN_ROAMING = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_hotspot20_hs_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/hotspot20/hs_profile."""
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


def validate_wireless_controller_hotspot20_hs_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/hotspot20/hs_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "access-network-type" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-type",
            payload["access-network-type"],
            VALID_BODY_ACCESS_NETWORK_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-network-internet" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-internet",
            payload["access-network-internet"],
            VALID_BODY_ACCESS_NETWORK_INTERNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-network-asra" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-asra",
            payload["access-network-asra"],
            VALID_BODY_ACCESS_NETWORK_ASRA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-network-esr" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-esr",
            payload["access-network-esr"],
            VALID_BODY_ACCESS_NETWORK_ESR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-network-uesa" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-uesa",
            payload["access-network-uesa"],
            VALID_BODY_ACCESS_NETWORK_UESA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "venue-group" in payload:
        is_valid, error = _validate_enum_field(
            "venue-group",
            payload["venue-group"],
            VALID_BODY_VENUE_GROUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "venue-type" in payload:
        is_valid, error = _validate_enum_field(
            "venue-type",
            payload["venue-type"],
            VALID_BODY_VENUE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-arp" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-arp",
            payload["proxy-arp"],
            VALID_BODY_PROXY_ARP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l2tif" in payload:
        is_valid, error = _validate_enum_field(
            "l2tif",
            payload["l2tif"],
            VALID_BODY_L2TIF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pame-bi" in payload:
        is_valid, error = _validate_enum_field(
            "pame-bi",
            payload["pame-bi"],
            VALID_BODY_PAME_BI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dgaf" in payload:
        is_valid, error = _validate_enum_field(
            "dgaf",
            payload["dgaf"],
            VALID_BODY_DGAF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wnm-sleep-mode" in payload:
        is_valid, error = _validate_enum_field(
            "wnm-sleep-mode",
            payload["wnm-sleep-mode"],
            VALID_BODY_WNM_SLEEP_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bss-transition" in payload:
        is_valid, error = _validate_enum_field(
            "bss-transition",
            payload["bss-transition"],
            VALID_BODY_BSS_TRANSITION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wba-open-roaming" in payload:
        is_valid, error = _validate_enum_field(
            "wba-open-roaming",
            payload["wba-open-roaming"],
            VALID_BODY_WBA_OPEN_ROAMING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_hotspot20_hs_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/hotspot20/hs_profile."""
    # Validate enum values using central function
    if "access-network-type" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-type",
            payload["access-network-type"],
            VALID_BODY_ACCESS_NETWORK_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-network-internet" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-internet",
            payload["access-network-internet"],
            VALID_BODY_ACCESS_NETWORK_INTERNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-network-asra" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-asra",
            payload["access-network-asra"],
            VALID_BODY_ACCESS_NETWORK_ASRA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-network-esr" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-esr",
            payload["access-network-esr"],
            VALID_BODY_ACCESS_NETWORK_ESR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-network-uesa" in payload:
        is_valid, error = _validate_enum_field(
            "access-network-uesa",
            payload["access-network-uesa"],
            VALID_BODY_ACCESS_NETWORK_UESA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "venue-group" in payload:
        is_valid, error = _validate_enum_field(
            "venue-group",
            payload["venue-group"],
            VALID_BODY_VENUE_GROUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "venue-type" in payload:
        is_valid, error = _validate_enum_field(
            "venue-type",
            payload["venue-type"],
            VALID_BODY_VENUE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-arp" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-arp",
            payload["proxy-arp"],
            VALID_BODY_PROXY_ARP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l2tif" in payload:
        is_valid, error = _validate_enum_field(
            "l2tif",
            payload["l2tif"],
            VALID_BODY_L2TIF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pame-bi" in payload:
        is_valid, error = _validate_enum_field(
            "pame-bi",
            payload["pame-bi"],
            VALID_BODY_PAME_BI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dgaf" in payload:
        is_valid, error = _validate_enum_field(
            "dgaf",
            payload["dgaf"],
            VALID_BODY_DGAF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wnm-sleep-mode" in payload:
        is_valid, error = _validate_enum_field(
            "wnm-sleep-mode",
            payload["wnm-sleep-mode"],
            VALID_BODY_WNM_SLEEP_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bss-transition" in payload:
        is_valid, error = _validate_enum_field(
            "bss-transition",
            payload["bss-transition"],
            VALID_BODY_BSS_TRANSITION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wba-open-roaming" in payload:
        is_valid, error = _validate_enum_field(
            "wba-open-roaming",
            payload["wba-open-roaming"],
            VALID_BODY_WBA_OPEN_ROAMING,
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
    "endpoint": "wireless_controller/hotspot20/hs_profile",
    "category": "cmdb",
    "api_path": "wireless-controller.hotspot20/hs-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure hotspot profile.",
    "total_fields": 43,
    "required_fields_count": 0,
    "fields_with_defaults_count": 42,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
