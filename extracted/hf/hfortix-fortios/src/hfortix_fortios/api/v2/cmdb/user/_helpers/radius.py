"""Validation helpers for user/radius - Auto-generated"""

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
    "server",  # Primary RADIUS server CN domain name or IP address.
    "secret",  # Pre-shared secret key used to access the primary RADIUS server.
    "interface",  # Specify outgoing interface to reach server.
    "rsso-secret",  # RADIUS secret used by the RADIUS accounting server.
    "rsso-endpoint-block-attribute",  # RADIUS attributes used to block a user.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "server": "",
    "secondary-server": "",
    "tertiary-server": "",
    "timeout": 5,
    "status-ttl": 300,
    "all-usergroup": "disable",
    "use-management-vdom": "disable",
    "switch-controller-nas-ip-dynamic": "disable",
    "nas-ip": "0.0.0.0",
    "nas-id-type": "legacy",
    "call-station-id-type": "legacy",
    "nas-id": "",
    "acct-interim-interval": 0,
    "radius-coa": "disable",
    "radius-port": 0,
    "h3c-compatibility": "disable",
    "auth-type": "auto",
    "source-ip": "",
    "source-ip-interface": "",
    "username-case-sensitive": "disable",
    "group-override-attr-type": "",
    "password-renewal": "enable",
    "require-message-authenticator": "enable",
    "password-encoding": "auto",
    "mac-username-delimiter": "hyphen",
    "mac-password-delimiter": "hyphen",
    "mac-case": "lowercase",
    "acct-all-servers": "disable",
    "switch-controller-acct-fast-framedip-detect": 2,
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
    "switch-controller-service-type": "",
    "transport-protocol": "udp",
    "tls-min-proto-version": "default",
    "ca-cert": "",
    "client-cert": "",
    "server-identity-check": "enable",
    "account-key-processing": "same",
    "account-key-cert-field": "othername",
    "rsso": "disable",
    "rsso-radius-server-port": 1813,
    "rsso-radius-response": "disable",
    "rsso-validate-request-secret": "disable",
    "rsso-endpoint-attribute": "Calling-Station-Id",
    "rsso-endpoint-block-attribute": "",
    "sso-attribute": "Class",
    "sso-attribute-key": "",
    "sso-attribute-value-override": "enable",
    "rsso-context-timeout": 28800,
    "rsso-log-period": 0,
    "rsso-log-flags": "protocol-error profile-missing accounting-stop-missed accounting-event endpoint-block radiusd-other",
    "rsso-flush-ip-session": "disable",
    "rsso-ep-one-ip-only": "disable",
    "delimiter": "plus",
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
    "name": "string",  # RADIUS server entry name.
    "server": "string",  # Primary RADIUS server CN domain name or IP address.
    "secret": "password",  # Pre-shared secret key used to access the primary RADIUS server.
    "secondary-server": "string",  # Secondary RADIUS CN domain name or IP address.
    "secondary-secret": "password",  # Secret key to access the secondary server.
    "tertiary-server": "string",  # Tertiary RADIUS CN domain name or IP address.
    "tertiary-secret": "password",  # Secret key to access the tertiary server.
    "timeout": "integer",  # Time in seconds to retry connecting server.
    "status-ttl": "integer",  # Time for which server reachability is cached so that when a server is unreachabl
    "all-usergroup": "option",  # Enable/disable automatically including this RADIUS server in all user groups.
    "use-management-vdom": "option",  # Enable/disable using management VDOM to send requests.
    "switch-controller-nas-ip-dynamic": "option",  # Enable/Disable switch-controller nas-ip dynamic to dynamically set nas-ip.
    "nas-ip": "ipv4-address",  # IP address used to communicate with the RADIUS server and used as NAS-IP-Address
    "nas-id-type": "option",  # NAS identifier type configuration (default = legacy).
    "call-station-id-type": "option",  # Calling & Called station identifier type configuration (default = legacy), this 
    "nas-id": "string",  # Custom NAS identifier.
    "acct-interim-interval": "integer",  # Time in seconds between each accounting interim update message.
    "radius-coa": "option",  # Enable to allow a mechanism to change the attributes of an authentication, autho
    "radius-port": "integer",  # RADIUS service port number.
    "h3c-compatibility": "option",  # Enable/disable compatibility with the H3C, a mechanism that performs security ch
    "auth-type": "option",  # Authentication methods/protocols permitted for this RADIUS server.
    "source-ip": "string",  # Source IP address for communications to the RADIUS server.
    "source-ip-interface": "string",  # Source interface for communication with the RADIUS server.
    "username-case-sensitive": "option",  # Enable/disable case sensitive user names.
    "group-override-attr-type": "option",  # RADIUS attribute type to override user group information.
    "class": "string",  # Class attribute name(s).
    "password-renewal": "option",  # Enable/disable password renewal.
    "require-message-authenticator": "option",  # Require message authenticator in authentication response.
    "password-encoding": "option",  # Password encoding.
    "mac-username-delimiter": "option",  # MAC authentication username delimiter (default = hyphen).
    "mac-password-delimiter": "option",  # MAC authentication password delimiter (default = hyphen).
    "mac-case": "option",  # MAC authentication case (default = lowercase).
    "acct-all-servers": "option",  # Enable/disable sending of accounting messages to all configured servers (default
    "switch-controller-acct-fast-framedip-detect": "integer",  # Switch controller accounting message Framed-IP detection from DHCP snooping (sec
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
    "switch-controller-service-type": "option",  # RADIUS service type.
    "transport-protocol": "option",  # Transport protocol to be used (default = udp).
    "tls-min-proto-version": "option",  # Minimum supported protocol version for TLS connections (default is to follow sys
    "ca-cert": "string",  # CA of server to trust under TLS.
    "client-cert": "string",  # Client certificate to use under TLS.
    "server-identity-check": "option",  # Enable/disable RADIUS server identity check (verify server domain name/IP addres
    "account-key-processing": "option",  # Account key processing operation. The FortiGate will keep either the whole domai
    "account-key-cert-field": "option",  # Define subject identity field in certificate for user access right checking.
    "rsso": "option",  # Enable/disable RADIUS based single sign on feature.
    "rsso-radius-server-port": "integer",  # UDP port to listen on for RADIUS Start and Stop records.
    "rsso-radius-response": "option",  # Enable/disable sending RADIUS response packets after receiving Start and Stop re
    "rsso-validate-request-secret": "option",  # Enable/disable validating the RADIUS request shared secret in the Start or End r
    "rsso-secret": "password",  # RADIUS secret used by the RADIUS accounting server.
    "rsso-endpoint-attribute": "option",  # RADIUS attributes used to extract the user end point identifier from the RADIUS 
    "rsso-endpoint-block-attribute": "option",  # RADIUS attributes used to block a user.
    "sso-attribute": "option",  # RADIUS attribute that contains the profile group name to be extracted from the R
    "sso-attribute-key": "string",  # Key prefix for SSO group value in the SSO attribute.
    "sso-attribute-value-override": "option",  # Enable/disable override old attribute value with new value for the same endpoint
    "rsso-context-timeout": "integer",  # Time in seconds before the logged out user is removed from the \"user context li
    "rsso-log-period": "integer",  # Time interval in seconds that group event log messages will be generated for dyn
    "rsso-log-flags": "option",  # Events to log.
    "rsso-flush-ip-session": "option",  # Enable/disable flushing user IP sessions on RADIUS accounting Stop messages.
    "rsso-ep-one-ip-only": "option",  # Enable/disable the replacement of old IP addresses with new ones for the same en
    "delimiter": "option",  # Configure delimiter to be used for separating profile group names in the SSO att
    "accounting-server": "string",  # Additional accounting servers.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "RADIUS server entry name.",
    "server": "Primary RADIUS server CN domain name or IP address.",
    "secret": "Pre-shared secret key used to access the primary RADIUS server.",
    "secondary-server": "Secondary RADIUS CN domain name or IP address.",
    "secondary-secret": "Secret key to access the secondary server.",
    "tertiary-server": "Tertiary RADIUS CN domain name or IP address.",
    "tertiary-secret": "Secret key to access the tertiary server.",
    "timeout": "Time in seconds to retry connecting server.",
    "status-ttl": "Time for which server reachability is cached so that when a server is unreachable, it will not be retried for at least this period of time (0 = cache disabled, default = 300).",
    "all-usergroup": "Enable/disable automatically including this RADIUS server in all user groups.",
    "use-management-vdom": "Enable/disable using management VDOM to send requests.",
    "switch-controller-nas-ip-dynamic": "Enable/Disable switch-controller nas-ip dynamic to dynamically set nas-ip.",
    "nas-ip": "IP address used to communicate with the RADIUS server and used as NAS-IP-Address and Called-Station-ID attributes.",
    "nas-id-type": "NAS identifier type configuration (default = legacy).",
    "call-station-id-type": "Calling & Called station identifier type configuration (default = legacy), this option is not available for 802.1x authentication. ",
    "nas-id": "Custom NAS identifier.",
    "acct-interim-interval": "Time in seconds between each accounting interim update message.",
    "radius-coa": "Enable to allow a mechanism to change the attributes of an authentication, authorization, and accounting session after it is authenticated.",
    "radius-port": "RADIUS service port number.",
    "h3c-compatibility": "Enable/disable compatibility with the H3C, a mechanism that performs security checking for authentication.",
    "auth-type": "Authentication methods/protocols permitted for this RADIUS server.",
    "source-ip": "Source IP address for communications to the RADIUS server.",
    "source-ip-interface": "Source interface for communication with the RADIUS server.",
    "username-case-sensitive": "Enable/disable case sensitive user names.",
    "group-override-attr-type": "RADIUS attribute type to override user group information.",
    "class": "Class attribute name(s).",
    "password-renewal": "Enable/disable password renewal.",
    "require-message-authenticator": "Require message authenticator in authentication response.",
    "password-encoding": "Password encoding.",
    "mac-username-delimiter": "MAC authentication username delimiter (default = hyphen).",
    "mac-password-delimiter": "MAC authentication password delimiter (default = hyphen).",
    "mac-case": "MAC authentication case (default = lowercase).",
    "acct-all-servers": "Enable/disable sending of accounting messages to all configured servers (default = disable).",
    "switch-controller-acct-fast-framedip-detect": "Switch controller accounting message Framed-IP detection from DHCP snooping (seconds, default=2).",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
    "switch-controller-service-type": "RADIUS service type.",
    "transport-protocol": "Transport protocol to be used (default = udp).",
    "tls-min-proto-version": "Minimum supported protocol version for TLS connections (default is to follow system global setting).",
    "ca-cert": "CA of server to trust under TLS.",
    "client-cert": "Client certificate to use under TLS.",
    "server-identity-check": "Enable/disable RADIUS server identity check (verify server domain name/IP address against the server certificate).",
    "account-key-processing": "Account key processing operation. The FortiGate will keep either the whole domain or strip the domain from the subject identity.",
    "account-key-cert-field": "Define subject identity field in certificate for user access right checking.",
    "rsso": "Enable/disable RADIUS based single sign on feature.",
    "rsso-radius-server-port": "UDP port to listen on for RADIUS Start and Stop records.",
    "rsso-radius-response": "Enable/disable sending RADIUS response packets after receiving Start and Stop records.",
    "rsso-validate-request-secret": "Enable/disable validating the RADIUS request shared secret in the Start or End record.",
    "rsso-secret": "RADIUS secret used by the RADIUS accounting server.",
    "rsso-endpoint-attribute": "RADIUS attributes used to extract the user end point identifier from the RADIUS Start record.",
    "rsso-endpoint-block-attribute": "RADIUS attributes used to block a user.",
    "sso-attribute": "RADIUS attribute that contains the profile group name to be extracted from the RADIUS Start record.",
    "sso-attribute-key": "Key prefix for SSO group value in the SSO attribute.",
    "sso-attribute-value-override": "Enable/disable override old attribute value with new value for the same endpoint.",
    "rsso-context-timeout": "Time in seconds before the logged out user is removed from the \"user context list\" of logged on users.",
    "rsso-log-period": "Time interval in seconds that group event log messages will be generated for dynamic profile events.",
    "rsso-log-flags": "Events to log.",
    "rsso-flush-ip-session": "Enable/disable flushing user IP sessions on RADIUS accounting Stop messages.",
    "rsso-ep-one-ip-only": "Enable/disable the replacement of old IP addresses with new ones for the same endpoint on RADIUS accounting Start messages.",
    "delimiter": "Configure delimiter to be used for separating profile group names in the SSO attribute (default = plus character \"+\").",
    "accounting-server": "Additional accounting servers.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "server": {"type": "string", "max_length": 63},
    "secondary-server": {"type": "string", "max_length": 63},
    "tertiary-server": {"type": "string", "max_length": 63},
    "timeout": {"type": "integer", "min": 1, "max": 300},
    "status-ttl": {"type": "integer", "min": 0, "max": 600},
    "nas-id": {"type": "string", "max_length": 255},
    "acct-interim-interval": {"type": "integer", "min": 60, "max": 86400},
    "radius-port": {"type": "integer", "min": 0, "max": 65535},
    "source-ip": {"type": "string", "max_length": 63},
    "source-ip-interface": {"type": "string", "max_length": 15},
    "switch-controller-acct-fast-framedip-detect": {"type": "integer", "min": 2, "max": 600},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
    "ca-cert": {"type": "string", "max_length": 79},
    "client-cert": {"type": "string", "max_length": 35},
    "rsso-radius-server-port": {"type": "integer", "min": 0, "max": 65535},
    "sso-attribute-key": {"type": "string", "max_length": 35},
    "rsso-context-timeout": {"type": "integer", "min": 0, "max": 4294967295},
    "rsso-log-period": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "class": {
        "name": {
            "type": "string",
            "help": "Class name.",
            "default": "",
            "max_length": 79,
        },
    },
    "accounting-server": {
        "id": {
            "type": "integer",
            "help": "ID (0 - 4294967295).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "status": {
            "type": "option",
            "help": "Status.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "server": {
            "type": "string",
            "help": "Server CN domain name or IP address.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "secret": {
            "type": "password",
            "help": "Secret key.",
            "required": True,
            "max_length": 128,
        },
        "port": {
            "type": "integer",
            "help": "RADIUS accounting port number.",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "source-ip": {
            "type": "string",
            "help": "Source IP address for communications to the RADIUS server.",
            "default": "",
            "max_length": 63,
        },
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
        "vrf-select": {
            "type": "integer",
            "help": "VRF ID used for connection to server.",
            "default": 0,
            "min_value": 0,
            "max_value": 511,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_ALL_USERGROUP = [
    "disable",
    "enable",
]
VALID_BODY_USE_MANAGEMENT_VDOM = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_NAS_IP_DYNAMIC = [
    "enable",
    "disable",
]
VALID_BODY_NAS_ID_TYPE = [
    "legacy",
    "custom",
    "hostname",
]
VALID_BODY_CALL_STATION_ID_TYPE = [
    "legacy",
    "IP",
    "MAC",
]
VALID_BODY_RADIUS_COA = [
    "enable",
    "disable",
]
VALID_BODY_H3C_COMPATIBILITY = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_TYPE = [
    "auto",
    "ms_chap_v2",
    "ms_chap",
    "chap",
    "pap",
]
VALID_BODY_USERNAME_CASE_SENSITIVE = [
    "enable",
    "disable",
]
VALID_BODY_GROUP_OVERRIDE_ATTR_TYPE = [
    "filter-Id",
    "class",
]
VALID_BODY_PASSWORD_RENEWAL = [
    "enable",
    "disable",
]
VALID_BODY_REQUIRE_MESSAGE_AUTHENTICATOR = [
    "enable",
    "disable",
]
VALID_BODY_PASSWORD_ENCODING = [
    "auto",
    "ISO-8859-1",
]
VALID_BODY_MAC_USERNAME_DELIMITER = [
    "hyphen",
    "single-hyphen",
    "colon",
    "none",
]
VALID_BODY_MAC_PASSWORD_DELIMITER = [
    "hyphen",
    "single-hyphen",
    "colon",
    "none",
]
VALID_BODY_MAC_CASE = [
    "uppercase",
    "lowercase",
]
VALID_BODY_ACCT_ALL_SERVERS = [
    "enable",
    "disable",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_SWITCH_CONTROLLER_SERVICE_TYPE = [
    "login",
    "framed",
    "callback-login",
    "callback-framed",
    "outbound",
    "administrative",
    "nas-prompt",
    "authenticate-only",
    "callback-nas-prompt",
    "call-check",
    "callback-administrative",
]
VALID_BODY_TRANSPORT_PROTOCOL = [
    "udp",
    "tcp",
    "tls",
]
VALID_BODY_TLS_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_SERVER_IDENTITY_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_ACCOUNT_KEY_PROCESSING = [
    "same",
    "strip",
]
VALID_BODY_ACCOUNT_KEY_CERT_FIELD = [
    "othername",
    "rfc822name",
    "dnsname",
    "cn",
]
VALID_BODY_RSSO = [
    "enable",
    "disable",
]
VALID_BODY_RSSO_RADIUS_RESPONSE = [
    "enable",
    "disable",
]
VALID_BODY_RSSO_VALIDATE_REQUEST_SECRET = [
    "enable",
    "disable",
]
VALID_BODY_RSSO_ENDPOINT_ATTRIBUTE = [
    "User-Name",
    "NAS-IP-Address",
    "Framed-IP-Address",
    "Framed-IP-Netmask",
    "Filter-Id",
    "Login-IP-Host",
    "Reply-Message",
    "Callback-Number",
    "Callback-Id",
    "Framed-Route",
    "Framed-IPX-Network",
    "Class",
    "Called-Station-Id",
    "Calling-Station-Id",
    "NAS-Identifier",
    "Proxy-State",
    "Login-LAT-Service",
    "Login-LAT-Node",
    "Login-LAT-Group",
    "Framed-AppleTalk-Zone",
    "Acct-Session-Id",
    "Acct-Multi-Session-Id",
]
VALID_BODY_RSSO_ENDPOINT_BLOCK_ATTRIBUTE = [
    "User-Name",
    "NAS-IP-Address",
    "Framed-IP-Address",
    "Framed-IP-Netmask",
    "Filter-Id",
    "Login-IP-Host",
    "Reply-Message",
    "Callback-Number",
    "Callback-Id",
    "Framed-Route",
    "Framed-IPX-Network",
    "Class",
    "Called-Station-Id",
    "Calling-Station-Id",
    "NAS-Identifier",
    "Proxy-State",
    "Login-LAT-Service",
    "Login-LAT-Node",
    "Login-LAT-Group",
    "Framed-AppleTalk-Zone",
    "Acct-Session-Id",
    "Acct-Multi-Session-Id",
]
VALID_BODY_SSO_ATTRIBUTE = [
    "User-Name",
    "NAS-IP-Address",
    "Framed-IP-Address",
    "Framed-IP-Netmask",
    "Filter-Id",
    "Login-IP-Host",
    "Reply-Message",
    "Callback-Number",
    "Callback-Id",
    "Framed-Route",
    "Framed-IPX-Network",
    "Class",
    "Called-Station-Id",
    "Calling-Station-Id",
    "NAS-Identifier",
    "Proxy-State",
    "Login-LAT-Service",
    "Login-LAT-Node",
    "Login-LAT-Group",
    "Framed-AppleTalk-Zone",
    "Acct-Session-Id",
    "Acct-Multi-Session-Id",
]
VALID_BODY_SSO_ATTRIBUTE_VALUE_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_RSSO_LOG_FLAGS = [
    "protocol-error",
    "profile-missing",
    "accounting-stop-missed",
    "accounting-event",
    "endpoint-block",
    "radiusd-other",
    "none",
]
VALID_BODY_RSSO_FLUSH_IP_SESSION = [
    "enable",
    "disable",
]
VALID_BODY_RSSO_EP_ONE_IP_ONLY = [
    "enable",
    "disable",
]
VALID_BODY_DELIMITER = [
    "plus",
    "comma",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_radius_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/radius."""
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


def validate_user_radius_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/radius object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "all-usergroup" in payload:
        is_valid, error = _validate_enum_field(
            "all-usergroup",
            payload["all-usergroup"],
            VALID_BODY_ALL_USERGROUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-management-vdom" in payload:
        is_valid, error = _validate_enum_field(
            "use-management-vdom",
            payload["use-management-vdom"],
            VALID_BODY_USE_MANAGEMENT_VDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-nas-ip-dynamic" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-nas-ip-dynamic",
            payload["switch-controller-nas-ip-dynamic"],
            VALID_BODY_SWITCH_CONTROLLER_NAS_IP_DYNAMIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nas-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "nas-id-type",
            payload["nas-id-type"],
            VALID_BODY_NAS_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "call-station-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "call-station-id-type",
            payload["call-station-id-type"],
            VALID_BODY_CALL_STATION_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-coa" in payload:
        is_valid, error = _validate_enum_field(
            "radius-coa",
            payload["radius-coa"],
            VALID_BODY_RADIUS_COA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "h3c-compatibility" in payload:
        is_valid, error = _validate_enum_field(
            "h3c-compatibility",
            payload["h3c-compatibility"],
            VALID_BODY_H3C_COMPATIBILITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "username-case-sensitive" in payload:
        is_valid, error = _validate_enum_field(
            "username-case-sensitive",
            payload["username-case-sensitive"],
            VALID_BODY_USERNAME_CASE_SENSITIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-override-attr-type" in payload:
        is_valid, error = _validate_enum_field(
            "group-override-attr-type",
            payload["group-override-attr-type"],
            VALID_BODY_GROUP_OVERRIDE_ATTR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "password-renewal" in payload:
        is_valid, error = _validate_enum_field(
            "password-renewal",
            payload["password-renewal"],
            VALID_BODY_PASSWORD_RENEWAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "require-message-authenticator" in payload:
        is_valid, error = _validate_enum_field(
            "require-message-authenticator",
            payload["require-message-authenticator"],
            VALID_BODY_REQUIRE_MESSAGE_AUTHENTICATOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "password-encoding" in payload:
        is_valid, error = _validate_enum_field(
            "password-encoding",
            payload["password-encoding"],
            VALID_BODY_PASSWORD_ENCODING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-username-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-username-delimiter",
            payload["mac-username-delimiter"],
            VALID_BODY_MAC_USERNAME_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-password-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-password-delimiter",
            payload["mac-password-delimiter"],
            VALID_BODY_MAC_PASSWORD_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-case" in payload:
        is_valid, error = _validate_enum_field(
            "mac-case",
            payload["mac-case"],
            VALID_BODY_MAC_CASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "acct-all-servers" in payload:
        is_valid, error = _validate_enum_field(
            "acct-all-servers",
            payload["acct-all-servers"],
            VALID_BODY_ACCT_ALL_SERVERS,
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
    if "switch-controller-service-type" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-service-type",
            payload["switch-controller-service-type"],
            VALID_BODY_SWITCH_CONTROLLER_SERVICE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "transport-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "transport-protocol",
            payload["transport-protocol"],
            VALID_BODY_TRANSPORT_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tls-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "tls-min-proto-version",
            payload["tls-min-proto-version"],
            VALID_BODY_TLS_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "account-key-processing" in payload:
        is_valid, error = _validate_enum_field(
            "account-key-processing",
            payload["account-key-processing"],
            VALID_BODY_ACCOUNT_KEY_PROCESSING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "account-key-cert-field" in payload:
        is_valid, error = _validate_enum_field(
            "account-key-cert-field",
            payload["account-key-cert-field"],
            VALID_BODY_ACCOUNT_KEY_CERT_FIELD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso" in payload:
        is_valid, error = _validate_enum_field(
            "rsso",
            payload["rsso"],
            VALID_BODY_RSSO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-radius-response" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-radius-response",
            payload["rsso-radius-response"],
            VALID_BODY_RSSO_RADIUS_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-validate-request-secret" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-validate-request-secret",
            payload["rsso-validate-request-secret"],
            VALID_BODY_RSSO_VALIDATE_REQUEST_SECRET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-endpoint-attribute" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-endpoint-attribute",
            payload["rsso-endpoint-attribute"],
            VALID_BODY_RSSO_ENDPOINT_ATTRIBUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-endpoint-block-attribute" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-endpoint-block-attribute",
            payload["rsso-endpoint-block-attribute"],
            VALID_BODY_RSSO_ENDPOINT_BLOCK_ATTRIBUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sso-attribute" in payload:
        is_valid, error = _validate_enum_field(
            "sso-attribute",
            payload["sso-attribute"],
            VALID_BODY_SSO_ATTRIBUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sso-attribute-value-override" in payload:
        is_valid, error = _validate_enum_field(
            "sso-attribute-value-override",
            payload["sso-attribute-value-override"],
            VALID_BODY_SSO_ATTRIBUTE_VALUE_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-log-flags" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-log-flags",
            payload["rsso-log-flags"],
            VALID_BODY_RSSO_LOG_FLAGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-flush-ip-session" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-flush-ip-session",
            payload["rsso-flush-ip-session"],
            VALID_BODY_RSSO_FLUSH_IP_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-ep-one-ip-only" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-ep-one-ip-only",
            payload["rsso-ep-one-ip-only"],
            VALID_BODY_RSSO_EP_ONE_IP_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "delimiter",
            payload["delimiter"],
            VALID_BODY_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_radius_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/radius."""
    # Validate enum values using central function
    if "all-usergroup" in payload:
        is_valid, error = _validate_enum_field(
            "all-usergroup",
            payload["all-usergroup"],
            VALID_BODY_ALL_USERGROUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-management-vdom" in payload:
        is_valid, error = _validate_enum_field(
            "use-management-vdom",
            payload["use-management-vdom"],
            VALID_BODY_USE_MANAGEMENT_VDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-nas-ip-dynamic" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-nas-ip-dynamic",
            payload["switch-controller-nas-ip-dynamic"],
            VALID_BODY_SWITCH_CONTROLLER_NAS_IP_DYNAMIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nas-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "nas-id-type",
            payload["nas-id-type"],
            VALID_BODY_NAS_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "call-station-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "call-station-id-type",
            payload["call-station-id-type"],
            VALID_BODY_CALL_STATION_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-coa" in payload:
        is_valid, error = _validate_enum_field(
            "radius-coa",
            payload["radius-coa"],
            VALID_BODY_RADIUS_COA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "h3c-compatibility" in payload:
        is_valid, error = _validate_enum_field(
            "h3c-compatibility",
            payload["h3c-compatibility"],
            VALID_BODY_H3C_COMPATIBILITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "username-case-sensitive" in payload:
        is_valid, error = _validate_enum_field(
            "username-case-sensitive",
            payload["username-case-sensitive"],
            VALID_BODY_USERNAME_CASE_SENSITIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-override-attr-type" in payload:
        is_valid, error = _validate_enum_field(
            "group-override-attr-type",
            payload["group-override-attr-type"],
            VALID_BODY_GROUP_OVERRIDE_ATTR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "password-renewal" in payload:
        is_valid, error = _validate_enum_field(
            "password-renewal",
            payload["password-renewal"],
            VALID_BODY_PASSWORD_RENEWAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "require-message-authenticator" in payload:
        is_valid, error = _validate_enum_field(
            "require-message-authenticator",
            payload["require-message-authenticator"],
            VALID_BODY_REQUIRE_MESSAGE_AUTHENTICATOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "password-encoding" in payload:
        is_valid, error = _validate_enum_field(
            "password-encoding",
            payload["password-encoding"],
            VALID_BODY_PASSWORD_ENCODING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-username-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-username-delimiter",
            payload["mac-username-delimiter"],
            VALID_BODY_MAC_USERNAME_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-password-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-password-delimiter",
            payload["mac-password-delimiter"],
            VALID_BODY_MAC_PASSWORD_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-case" in payload:
        is_valid, error = _validate_enum_field(
            "mac-case",
            payload["mac-case"],
            VALID_BODY_MAC_CASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "acct-all-servers" in payload:
        is_valid, error = _validate_enum_field(
            "acct-all-servers",
            payload["acct-all-servers"],
            VALID_BODY_ACCT_ALL_SERVERS,
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
    if "switch-controller-service-type" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-service-type",
            payload["switch-controller-service-type"],
            VALID_BODY_SWITCH_CONTROLLER_SERVICE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "transport-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "transport-protocol",
            payload["transport-protocol"],
            VALID_BODY_TRANSPORT_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tls-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "tls-min-proto-version",
            payload["tls-min-proto-version"],
            VALID_BODY_TLS_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "account-key-processing" in payload:
        is_valid, error = _validate_enum_field(
            "account-key-processing",
            payload["account-key-processing"],
            VALID_BODY_ACCOUNT_KEY_PROCESSING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "account-key-cert-field" in payload:
        is_valid, error = _validate_enum_field(
            "account-key-cert-field",
            payload["account-key-cert-field"],
            VALID_BODY_ACCOUNT_KEY_CERT_FIELD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso" in payload:
        is_valid, error = _validate_enum_field(
            "rsso",
            payload["rsso"],
            VALID_BODY_RSSO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-radius-response" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-radius-response",
            payload["rsso-radius-response"],
            VALID_BODY_RSSO_RADIUS_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-validate-request-secret" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-validate-request-secret",
            payload["rsso-validate-request-secret"],
            VALID_BODY_RSSO_VALIDATE_REQUEST_SECRET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-endpoint-attribute" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-endpoint-attribute",
            payload["rsso-endpoint-attribute"],
            VALID_BODY_RSSO_ENDPOINT_ATTRIBUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-endpoint-block-attribute" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-endpoint-block-attribute",
            payload["rsso-endpoint-block-attribute"],
            VALID_BODY_RSSO_ENDPOINT_BLOCK_ATTRIBUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sso-attribute" in payload:
        is_valid, error = _validate_enum_field(
            "sso-attribute",
            payload["sso-attribute"],
            VALID_BODY_SSO_ATTRIBUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sso-attribute-value-override" in payload:
        is_valid, error = _validate_enum_field(
            "sso-attribute-value-override",
            payload["sso-attribute-value-override"],
            VALID_BODY_SSO_ATTRIBUTE_VALUE_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-log-flags" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-log-flags",
            payload["rsso-log-flags"],
            VALID_BODY_RSSO_LOG_FLAGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-flush-ip-session" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-flush-ip-session",
            payload["rsso-flush-ip-session"],
            VALID_BODY_RSSO_FLUSH_IP_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsso-ep-one-ip-only" in payload:
        is_valid, error = _validate_enum_field(
            "rsso-ep-one-ip-only",
            payload["rsso-ep-one-ip-only"],
            VALID_BODY_RSSO_EP_ONE_IP_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "delimiter",
            payload["delimiter"],
            VALID_BODY_DELIMITER,
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
    "endpoint": "user/radius",
    "category": "cmdb",
    "api_path": "user/radius",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure RADIUS server entries.",
    "total_fields": 62,
    "required_fields_count": 5,
    "fields_with_defaults_count": 56,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
