"""Validation helpers for wireless_controller/hotspot20/h2qp_conn_capability - Auto-generated"""

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
    "icmp-port": "unknown",
    "ftp-port": "unknown",
    "ssh-port": "unknown",
    "http-port": "unknown",
    "tls-port": "unknown",
    "pptp-vpn-port": "unknown",
    "voip-tcp-port": "unknown",
    "voip-udp-port": "unknown",
    "ikev2-port": "unknown",
    "ikev2-xx-port": "unknown",
    "esp-port": "unknown",
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
    "name": "string",  # Connection capability name.
    "icmp-port": "option",  # Set ICMP port service status.
    "ftp-port": "option",  # Set FTP port service status.
    "ssh-port": "option",  # Set SSH port service status.
    "http-port": "option",  # Set HTTP port service status.
    "tls-port": "option",  # Set TLS VPN (HTTPS) port service status.
    "pptp-vpn-port": "option",  # Set Point to Point Tunneling Protocol (PPTP) VPN port service status.
    "voip-tcp-port": "option",  # Set VoIP TCP port service status.
    "voip-udp-port": "option",  # Set VoIP UDP port service status.
    "ikev2-port": "option",  # Set IKEv2 port service for IPsec VPN status.
    "ikev2-xx-port": "option",  # Set UDP port 4500 (which may be used by IKEv2 for IPsec VPN) service status.
    "esp-port": "option",  # Set ESP port service (used by IPsec VPNs) status.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Connection capability name.",
    "icmp-port": "Set ICMP port service status.",
    "ftp-port": "Set FTP port service status.",
    "ssh-port": "Set SSH port service status.",
    "http-port": "Set HTTP port service status.",
    "tls-port": "Set TLS VPN (HTTPS) port service status.",
    "pptp-vpn-port": "Set Point to Point Tunneling Protocol (PPTP) VPN port service status.",
    "voip-tcp-port": "Set VoIP TCP port service status.",
    "voip-udp-port": "Set VoIP UDP port service status.",
    "ikev2-port": "Set IKEv2 port service for IPsec VPN status.",
    "ikev2-xx-port": "Set UDP port 4500 (which may be used by IKEv2 for IPsec VPN) service status.",
    "esp-port": "Set ESP port service (used by IPsec VPNs) status.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_ICMP_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_FTP_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_SSH_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_HTTP_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_TLS_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_PPTP_VPN_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_VOIP_TCP_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_VOIP_UDP_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_IKEV2_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_IKEV2_XX_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_BODY_ESP_PORT = [
    "closed",
    "open",
    "unknown",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_hotspot20_h2qp_conn_capability_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/hotspot20/h2qp_conn_capability."""
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


def validate_wireless_controller_hotspot20_h2qp_conn_capability_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/hotspot20/h2qp_conn_capability object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "icmp-port" in payload:
        is_valid, error = _validate_enum_field(
            "icmp-port",
            payload["icmp-port"],
            VALID_BODY_ICMP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ftp-port" in payload:
        is_valid, error = _validate_enum_field(
            "ftp-port",
            payload["ftp-port"],
            VALID_BODY_FTP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-port" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-port",
            payload["ssh-port"],
            VALID_BODY_SSH_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-port" in payload:
        is_valid, error = _validate_enum_field(
            "http-port",
            payload["http-port"],
            VALID_BODY_HTTP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tls-port" in payload:
        is_valid, error = _validate_enum_field(
            "tls-port",
            payload["tls-port"],
            VALID_BODY_TLS_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pptp-vpn-port" in payload:
        is_valid, error = _validate_enum_field(
            "pptp-vpn-port",
            payload["pptp-vpn-port"],
            VALID_BODY_PPTP_VPN_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "voip-tcp-port" in payload:
        is_valid, error = _validate_enum_field(
            "voip-tcp-port",
            payload["voip-tcp-port"],
            VALID_BODY_VOIP_TCP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "voip-udp-port" in payload:
        is_valid, error = _validate_enum_field(
            "voip-udp-port",
            payload["voip-udp-port"],
            VALID_BODY_VOIP_UDP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ikev2-port" in payload:
        is_valid, error = _validate_enum_field(
            "ikev2-port",
            payload["ikev2-port"],
            VALID_BODY_IKEV2_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ikev2-xx-port" in payload:
        is_valid, error = _validate_enum_field(
            "ikev2-xx-port",
            payload["ikev2-xx-port"],
            VALID_BODY_IKEV2_XX_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "esp-port" in payload:
        is_valid, error = _validate_enum_field(
            "esp-port",
            payload["esp-port"],
            VALID_BODY_ESP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_hotspot20_h2qp_conn_capability_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/hotspot20/h2qp_conn_capability."""
    # Validate enum values using central function
    if "icmp-port" in payload:
        is_valid, error = _validate_enum_field(
            "icmp-port",
            payload["icmp-port"],
            VALID_BODY_ICMP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ftp-port" in payload:
        is_valid, error = _validate_enum_field(
            "ftp-port",
            payload["ftp-port"],
            VALID_BODY_FTP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-port" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-port",
            payload["ssh-port"],
            VALID_BODY_SSH_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-port" in payload:
        is_valid, error = _validate_enum_field(
            "http-port",
            payload["http-port"],
            VALID_BODY_HTTP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tls-port" in payload:
        is_valid, error = _validate_enum_field(
            "tls-port",
            payload["tls-port"],
            VALID_BODY_TLS_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pptp-vpn-port" in payload:
        is_valid, error = _validate_enum_field(
            "pptp-vpn-port",
            payload["pptp-vpn-port"],
            VALID_BODY_PPTP_VPN_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "voip-tcp-port" in payload:
        is_valid, error = _validate_enum_field(
            "voip-tcp-port",
            payload["voip-tcp-port"],
            VALID_BODY_VOIP_TCP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "voip-udp-port" in payload:
        is_valid, error = _validate_enum_field(
            "voip-udp-port",
            payload["voip-udp-port"],
            VALID_BODY_VOIP_UDP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ikev2-port" in payload:
        is_valid, error = _validate_enum_field(
            "ikev2-port",
            payload["ikev2-port"],
            VALID_BODY_IKEV2_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ikev2-xx-port" in payload:
        is_valid, error = _validate_enum_field(
            "ikev2-xx-port",
            payload["ikev2-xx-port"],
            VALID_BODY_IKEV2_XX_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "esp-port" in payload:
        is_valid, error = _validate_enum_field(
            "esp-port",
            payload["esp-port"],
            VALID_BODY_ESP_PORT,
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
    "endpoint": "wireless_controller/hotspot20/h2qp_conn_capability",
    "category": "cmdb",
    "api_path": "wireless-controller.hotspot20/h2qp-conn-capability",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure connection capability.",
    "total_fields": 12,
    "required_fields_count": 0,
    "fields_with_defaults_count": 12,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
