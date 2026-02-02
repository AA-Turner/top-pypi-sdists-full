"""Validation helpers for web_proxy/explicit - Auto-generated"""

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
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disable",
    "secure-web-proxy": "disable",
    "ftp-over-http": "disable",
    "socks": "disable",
    "http-incoming-port": "",
    "http-connection-mode": "static",
    "https-incoming-port": "",
    "client-cert": "disable",
    "user-agent-detect": "enable",
    "empty-cert-action": "block",
    "ssl-dh-bits": "2048",
    "ftp-incoming-port": "",
    "socks-incoming-port": "",
    "incoming-ip": "0.0.0.0",
    "outgoing-ip": "",
    "interface-select-method": "sdwan",
    "interface": "",
    "vrf-select": -1,
    "ipv6-status": "disable",
    "incoming-ip6": "::",
    "outgoing-ip6": "",
    "strict-guest": "disable",
    "pref-dns-result": "ipv4",
    "unknown-http-version": "reject",
    "realm": "default",
    "sec-default-action": "deny",
    "https-replacement-message": "enable",
    "message-upon-server-error": "enable",
    "pac-file-server-status": "disable",
    "pac-file-url": "",
    "pac-file-server-port": "",
    "pac-file-through-https": "disable",
    "pac-file-name": "proxy.pac",
    "pac-file-data": "",
    "ssl-algorithm": "low",
    "trace-auth-no-rsp": "disable",
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
    "status": "option",  # Enable/disable the explicit Web proxy for HTTP and HTTPS ses
    "secure-web-proxy": "option",  # Enable/disable/require the secure web proxy for HTTP and HTT
    "ftp-over-http": "option",  # Enable to proxy FTP-over-HTTP sessions sent from a web brows
    "socks": "option",  # Enable/disable the SOCKS proxy.
    "http-incoming-port": "user",  # Accept incoming HTTP requests on one or more ports (0 - 6553
    "http-connection-mode": "option",  # HTTP connection mode (default = static).
    "https-incoming-port": "user",  # Accept incoming HTTPS requests on one or more ports (0 - 655
    "secure-web-proxy-cert": "string",  # Name of certificates for secure web proxy.
    "client-cert": "option",  # Enable/disable to request client certificate.
    "user-agent-detect": "option",  # Enable/disable to detect device type by HTTP user-agent if n
    "empty-cert-action": "option",  # Action of an empty client certificate.
    "ssl-dh-bits": "option",  # Bit-size of Diffie-Hellman (DH) prime used in DHE-RSA negoti
    "ftp-incoming-port": "user",  # Accept incoming FTP-over-HTTP requests on one or more ports 
    "socks-incoming-port": "user",  # Accept incoming SOCKS proxy requests on one or more ports (0
    "incoming-ip": "ipv4-address-any",  # Restrict the explicit HTTP proxy to only accept sessions fro
    "outgoing-ip": "ipv4-address-any",  # Outgoing HTTP requests will have this IP address as their so
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
    "ipv6-status": "option",  # Enable/disable allowing an IPv6 web proxy destination in pol
    "incoming-ip6": "ipv6-address",  # Restrict the explicit web proxy to only accept sessions from
    "outgoing-ip6": "ipv6-address",  # Outgoing HTTP requests will leave this IPv6. Multiple interf
    "strict-guest": "option",  # Enable/disable strict guest user checking by the explicit we
    "pref-dns-result": "option",  # Prefer resolving addresses using the configured IPv4 or IPv6
    "unknown-http-version": "option",  # How to handle HTTP sessions that do not comply with HTTP 0.9
    "realm": "string",  # Authentication realm used to identify the explicit web proxy
    "sec-default-action": "option",  # Accept or deny explicit web proxy sessions when no web proxy
    "https-replacement-message": "option",  # Enable/disable sending the client a replacement message for 
    "message-upon-server-error": "option",  # Enable/disable displaying a replacement message when a serve
    "pac-file-server-status": "option",  # Enable/disable Proxy Auto-Configuration (PAC) for users of t
    "pac-file-url": "user",  # PAC file access URL.
    "pac-file-server-port": "user",  # Port number that PAC traffic from client web browsers uses t
    "pac-file-through-https": "option",  # Enable/disable to get Proxy Auto-Configuration (PAC) through
    "pac-file-name": "string",  # Pac file name.
    "pac-file-data": "user",  # PAC file contents enclosed in quotes (maximum of 256K bytes)
    "pac-policy": "string",  # PAC policies.
    "ssl-algorithm": "option",  # Relative strength of encryption algorithms accepted in HTTPS
    "trace-auth-no-rsp": "option",  # Enable/disable logging timed-out authentication requests.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable the explicit Web proxy for HTTP and HTTPS session.",
    "secure-web-proxy": "Enable/disable/require the secure web proxy for HTTP and HTTPS session.",
    "ftp-over-http": "Enable to proxy FTP-over-HTTP sessions sent from a web browser.",
    "socks": "Enable/disable the SOCKS proxy.",
    "http-incoming-port": "Accept incoming HTTP requests on one or more ports (0 - 65535, default = 8080).",
    "http-connection-mode": "HTTP connection mode (default = static).",
    "https-incoming-port": "Accept incoming HTTPS requests on one or more ports (0 - 65535, default = 0, use the same as HTTP).",
    "secure-web-proxy-cert": "Name of certificates for secure web proxy.",
    "client-cert": "Enable/disable to request client certificate.",
    "user-agent-detect": "Enable/disable to detect device type by HTTP user-agent if no client certificate provided.",
    "empty-cert-action": "Action of an empty client certificate.",
    "ssl-dh-bits": "Bit-size of Diffie-Hellman (DH) prime used in DHE-RSA negotiation (default = 2048).",
    "ftp-incoming-port": "Accept incoming FTP-over-HTTP requests on one or more ports (0 - 65535, default = 0; use the same as HTTP).",
    "socks-incoming-port": "Accept incoming SOCKS proxy requests on one or more ports (0 - 65535, default = 0; use the same as HTTP).",
    "incoming-ip": "Restrict the explicit HTTP proxy to only accept sessions from this IP address. An interface must have this IP address.",
    "outgoing-ip": "Outgoing HTTP requests will have this IP address as their source address. An interface must have this IP address.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
    "ipv6-status": "Enable/disable allowing an IPv6 web proxy destination in policies and all IPv6 related entries in this command.",
    "incoming-ip6": "Restrict the explicit web proxy to only accept sessions from this IPv6 address. An interface must have this IPv6 address.",
    "outgoing-ip6": "Outgoing HTTP requests will leave this IPv6. Multiple interfaces can be specified. Interfaces must have these IPv6 addresses.",
    "strict-guest": "Enable/disable strict guest user checking by the explicit web proxy.",
    "pref-dns-result": "Prefer resolving addresses using the configured IPv4 or IPv6 DNS server (default = ipv4).",
    "unknown-http-version": "How to handle HTTP sessions that do not comply with HTTP 0.9, 1.0, or 1.1.",
    "realm": "Authentication realm used to identify the explicit web proxy (maximum of 63 characters).",
    "sec-default-action": "Accept or deny explicit web proxy sessions when no web proxy firewall policy exists.",
    "https-replacement-message": "Enable/disable sending the client a replacement message for HTTPS requests.",
    "message-upon-server-error": "Enable/disable displaying a replacement message when a server error is detected.",
    "pac-file-server-status": "Enable/disable Proxy Auto-Configuration (PAC) for users of this explicit proxy profile.",
    "pac-file-url": "PAC file access URL.",
    "pac-file-server-port": "Port number that PAC traffic from client web browsers uses to connect to the explicit web proxy (0 - 65535, default = 0; use the same as HTTP).",
    "pac-file-through-https": "Enable/disable to get Proxy Auto-Configuration (PAC) through HTTPS.",
    "pac-file-name": "Pac file name.",
    "pac-file-data": "PAC file contents enclosed in quotes (maximum of 256K bytes).",
    "pac-policy": "PAC policies.",
    "ssl-algorithm": "Relative strength of encryption algorithms accepted in HTTPS deep scan: high, medium, or low.",
    "trace-auth-no-rsp": "Enable/disable logging timed-out authentication requests.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
    "realm": {"type": "string", "max_length": 63},
    "pac-file-name": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "secure-web-proxy-cert": {
        "name": {
            "type": "string",
            "help": "Certificate list.",
            "default": "Fortinet_SSL",
            "max_length": 79,
        },
    },
    "pac-policy": {
        "policyid": {
            "type": "integer",
            "help": "Policy ID.",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 100,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable policy.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "srcaddr": {
            "type": "string",
            "help": "Source address objects.",
            "required": True,
        },
        "srcaddr6": {
            "type": "string",
            "help": "Source address6 objects.",
        },
        "dstaddr": {
            "type": "string",
            "help": "Destination address objects.",
            "required": True,
        },
        "pac-file-name": {
            "type": "string",
            "help": "Pac file name.",
            "required": True,
            "default": "proxy.pac",
            "max_length": 63,
        },
        "pac-file-data": {
            "type": "user",
            "help": "PAC file contents enclosed in quotes (maximum of 256K bytes).",
            "default": "",
        },
        "comments": {
            "type": "var-string",
            "help": "Optional comments.",
            "max_length": 1023,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_SECURE_WEB_PROXY = [
    "disable",
    "enable",
    "secure",
]
VALID_BODY_FTP_OVER_HTTP = [
    "enable",
    "disable",
]
VALID_BODY_SOCKS = [
    "enable",
    "disable",
]
VALID_BODY_HTTP_CONNECTION_MODE = [
    "static",
    "multiplex",
    "serverpool",
]
VALID_BODY_CLIENT_CERT = [
    "disable",
    "enable",
]
VALID_BODY_USER_AGENT_DETECT = [
    "disable",
    "enable",
]
VALID_BODY_EMPTY_CERT_ACTION = [
    "accept",
    "block",
    "accept-unmanageable",
]
VALID_BODY_SSL_DH_BITS = [
    "768",
    "1024",
    "1536",
    "2048",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "sdwan",
    "specify",
]
VALID_BODY_IPV6_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_STRICT_GUEST = [
    "enable",
    "disable",
]
VALID_BODY_PREF_DNS_RESULT = [
    "ipv4",
    "ipv6",
    "ipv4-strict",
    "ipv6-strict",
]
VALID_BODY_UNKNOWN_HTTP_VERSION = [
    "reject",
    "best-effort",
]
VALID_BODY_SEC_DEFAULT_ACTION = [
    "accept",
    "deny",
]
VALID_BODY_HTTPS_REPLACEMENT_MESSAGE = [
    "enable",
    "disable",
]
VALID_BODY_MESSAGE_UPON_SERVER_ERROR = [
    "enable",
    "disable",
]
VALID_BODY_PAC_FILE_SERVER_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_PAC_FILE_THROUGH_HTTPS = [
    "enable",
    "disable",
]
VALID_BODY_SSL_ALGORITHM = [
    "high",
    "medium",
    "low",
]
VALID_BODY_TRACE_AUTH_NO_RSP = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_web_proxy_explicit_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for web_proxy/explicit."""
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


def validate_web_proxy_explicit_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new web_proxy/explicit object."""
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
    if "secure-web-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "secure-web-proxy",
            payload["secure-web-proxy"],
            VALID_BODY_SECURE_WEB_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ftp-over-http" in payload:
        is_valid, error = _validate_enum_field(
            "ftp-over-http",
            payload["ftp-over-http"],
            VALID_BODY_FTP_OVER_HTTP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "socks" in payload:
        is_valid, error = _validate_enum_field(
            "socks",
            payload["socks"],
            VALID_BODY_SOCKS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-connection-mode" in payload:
        is_valid, error = _validate_enum_field(
            "http-connection-mode",
            payload["http-connection-mode"],
            VALID_BODY_HTTP_CONNECTION_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert",
            payload["client-cert"],
            VALID_BODY_CLIENT_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-agent-detect" in payload:
        is_valid, error = _validate_enum_field(
            "user-agent-detect",
            payload["user-agent-detect"],
            VALID_BODY_USER_AGENT_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "empty-cert-action" in payload:
        is_valid, error = _validate_enum_field(
            "empty-cert-action",
            payload["empty-cert-action"],
            VALID_BODY_EMPTY_CERT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-dh-bits" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-dh-bits",
            payload["ssl-dh-bits"],
            VALID_BODY_SSL_DH_BITS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-status" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-status",
            payload["ipv6-status"],
            VALID_BODY_IPV6_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-guest" in payload:
        is_valid, error = _validate_enum_field(
            "strict-guest",
            payload["strict-guest"],
            VALID_BODY_STRICT_GUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pref-dns-result" in payload:
        is_valid, error = _validate_enum_field(
            "pref-dns-result",
            payload["pref-dns-result"],
            VALID_BODY_PREF_DNS_RESULT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unknown-http-version" in payload:
        is_valid, error = _validate_enum_field(
            "unknown-http-version",
            payload["unknown-http-version"],
            VALID_BODY_UNKNOWN_HTTP_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sec-default-action" in payload:
        is_valid, error = _validate_enum_field(
            "sec-default-action",
            payload["sec-default-action"],
            VALID_BODY_SEC_DEFAULT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "https-replacement-message" in payload:
        is_valid, error = _validate_enum_field(
            "https-replacement-message",
            payload["https-replacement-message"],
            VALID_BODY_HTTPS_REPLACEMENT_MESSAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "message-upon-server-error" in payload:
        is_valid, error = _validate_enum_field(
            "message-upon-server-error",
            payload["message-upon-server-error"],
            VALID_BODY_MESSAGE_UPON_SERVER_ERROR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pac-file-server-status" in payload:
        is_valid, error = _validate_enum_field(
            "pac-file-server-status",
            payload["pac-file-server-status"],
            VALID_BODY_PAC_FILE_SERVER_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pac-file-through-https" in payload:
        is_valid, error = _validate_enum_field(
            "pac-file-through-https",
            payload["pac-file-through-https"],
            VALID_BODY_PAC_FILE_THROUGH_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-algorithm",
            payload["ssl-algorithm"],
            VALID_BODY_SSL_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trace-auth-no-rsp" in payload:
        is_valid, error = _validate_enum_field(
            "trace-auth-no-rsp",
            payload["trace-auth-no-rsp"],
            VALID_BODY_TRACE_AUTH_NO_RSP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_web_proxy_explicit_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update web_proxy/explicit."""
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
    if "secure-web-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "secure-web-proxy",
            payload["secure-web-proxy"],
            VALID_BODY_SECURE_WEB_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ftp-over-http" in payload:
        is_valid, error = _validate_enum_field(
            "ftp-over-http",
            payload["ftp-over-http"],
            VALID_BODY_FTP_OVER_HTTP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "socks" in payload:
        is_valid, error = _validate_enum_field(
            "socks",
            payload["socks"],
            VALID_BODY_SOCKS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-connection-mode" in payload:
        is_valid, error = _validate_enum_field(
            "http-connection-mode",
            payload["http-connection-mode"],
            VALID_BODY_HTTP_CONNECTION_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert",
            payload["client-cert"],
            VALID_BODY_CLIENT_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-agent-detect" in payload:
        is_valid, error = _validate_enum_field(
            "user-agent-detect",
            payload["user-agent-detect"],
            VALID_BODY_USER_AGENT_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "empty-cert-action" in payload:
        is_valid, error = _validate_enum_field(
            "empty-cert-action",
            payload["empty-cert-action"],
            VALID_BODY_EMPTY_CERT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-dh-bits" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-dh-bits",
            payload["ssl-dh-bits"],
            VALID_BODY_SSL_DH_BITS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-status" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-status",
            payload["ipv6-status"],
            VALID_BODY_IPV6_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-guest" in payload:
        is_valid, error = _validate_enum_field(
            "strict-guest",
            payload["strict-guest"],
            VALID_BODY_STRICT_GUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pref-dns-result" in payload:
        is_valid, error = _validate_enum_field(
            "pref-dns-result",
            payload["pref-dns-result"],
            VALID_BODY_PREF_DNS_RESULT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unknown-http-version" in payload:
        is_valid, error = _validate_enum_field(
            "unknown-http-version",
            payload["unknown-http-version"],
            VALID_BODY_UNKNOWN_HTTP_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sec-default-action" in payload:
        is_valid, error = _validate_enum_field(
            "sec-default-action",
            payload["sec-default-action"],
            VALID_BODY_SEC_DEFAULT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "https-replacement-message" in payload:
        is_valid, error = _validate_enum_field(
            "https-replacement-message",
            payload["https-replacement-message"],
            VALID_BODY_HTTPS_REPLACEMENT_MESSAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "message-upon-server-error" in payload:
        is_valid, error = _validate_enum_field(
            "message-upon-server-error",
            payload["message-upon-server-error"],
            VALID_BODY_MESSAGE_UPON_SERVER_ERROR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pac-file-server-status" in payload:
        is_valid, error = _validate_enum_field(
            "pac-file-server-status",
            payload["pac-file-server-status"],
            VALID_BODY_PAC_FILE_SERVER_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pac-file-through-https" in payload:
        is_valid, error = _validate_enum_field(
            "pac-file-through-https",
            payload["pac-file-through-https"],
            VALID_BODY_PAC_FILE_THROUGH_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-algorithm",
            payload["ssl-algorithm"],
            VALID_BODY_SSL_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trace-auth-no-rsp" in payload:
        is_valid, error = _validate_enum_field(
            "trace-auth-no-rsp",
            payload["trace-auth-no-rsp"],
            VALID_BODY_TRACE_AUTH_NO_RSP,
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
    "endpoint": "web_proxy/explicit",
    "category": "cmdb",
    "api_path": "web-proxy/explicit",
    "help": "Configure explicit Web proxy settings.",
    "total_fields": 38,
    "required_fields_count": 1,
    "fields_with_defaults_count": 36,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
