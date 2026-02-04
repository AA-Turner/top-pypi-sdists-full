"""Validation helpers for firewall/ssl_ssh_profile - Auto-generated"""

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
    "name",  # Name.
    "ssl-server",  # SSL server settings used for client certificate request.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "allowlist": "disable",
    "block-blocklisted-certificates": "enable",
    "server-cert-mode": "re-sign",
    "use-ssl-server": "disable",
    "caname": "Fortinet_CA_SSL",
    "untrusted-caname": "Fortinet_CA_Untrusted",
    "ssl-exemption-ip-rating": "enable",
    "ssl-exemption-log": "disable",
    "ssl-anomaly-log": "enable",
    "ssl-negotiation-log": "enable",
    "ssl-server-cert-log": "disable",
    "ssl-handshake-log": "disable",
    "rpc-over-https": "disable",
    "mapi-over-https": "disable",
    "supported-alpn": "all",
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
    "name": "string",  # Name.
    "comment": "var-string",  # Optional comments.
    "ssl": "string",  # Configure SSL options.
    "https": "string",  # Configure HTTPS options.
    "ftps": "string",  # Configure FTPS options.
    "imaps": "string",  # Configure IMAPS options.
    "pop3s": "string",  # Configure POP3S options.
    "smtps": "string",  # Configure SMTPS options.
    "ssh": "string",  # Configure SSH options.
    "dot": "string",  # Configure DNS over TLS options.
    "allowlist": "option",  # Enable/disable exempting servers by FortiGuard allowlist.
    "block-blocklisted-certificates": "option",  # Enable/disable blocking SSL-based botnet communication by FortiGuard certificate
    "ssl-exempt": "string",  # Servers to exempt from SSL inspection.
    "ech-outer-sni": "string",  # ClientHelloOuter SNIs to be blocked.
    "server-cert-mode": "option",  # Re-sign or replace the server's certificate.
    "use-ssl-server": "option",  # Enable/disable the use of SSL server table for SSL offloading.
    "caname": "string",  # CA certificate used by SSL Inspection.
    "untrusted-caname": "string",  # Untrusted CA certificate used by SSL Inspection.
    "server-cert": "string",  # Certificate used by SSL Inspection to replace server certificate.
    "ssl-server": "string",  # SSL server settings used for client certificate request.
    "ssl-exemption-ip-rating": "option",  # Enable/disable IP based URL rating.
    "ssl-exemption-log": "option",  # Enable/disable logging of SSL exemptions.
    "ssl-anomaly-log": "option",  # Enable/disable logging of SSL anomalies.
    "ssl-negotiation-log": "option",  # Enable/disable logging of SSL negotiation events.
    "ssl-server-cert-log": "option",  # Enable/disable logging of server certificate information.
    "ssl-handshake-log": "option",  # Enable/disable logging of TLS handshakes.
    "rpc-over-https": "option",  # Enable/disable inspection of RPC over HTTPS.
    "mapi-over-https": "option",  # Enable/disable inspection of MAPI over HTTPS.
    "supported-alpn": "option",  # Configure ALPN option.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "comment": "Optional comments.",
    "ssl": "Configure SSL options.",
    "https": "Configure HTTPS options.",
    "ftps": "Configure FTPS options.",
    "imaps": "Configure IMAPS options.",
    "pop3s": "Configure POP3S options.",
    "smtps": "Configure SMTPS options.",
    "ssh": "Configure SSH options.",
    "dot": "Configure DNS over TLS options.",
    "allowlist": "Enable/disable exempting servers by FortiGuard allowlist.",
    "block-blocklisted-certificates": "Enable/disable blocking SSL-based botnet communication by FortiGuard certificate blocklist.",
    "ssl-exempt": "Servers to exempt from SSL inspection.",
    "ech-outer-sni": "ClientHelloOuter SNIs to be blocked.",
    "server-cert-mode": "Re-sign or replace the server's certificate.",
    "use-ssl-server": "Enable/disable the use of SSL server table for SSL offloading.",
    "caname": "CA certificate used by SSL Inspection.",
    "untrusted-caname": "Untrusted CA certificate used by SSL Inspection.",
    "server-cert": "Certificate used by SSL Inspection to replace server certificate.",
    "ssl-server": "SSL server settings used for client certificate request.",
    "ssl-exemption-ip-rating": "Enable/disable IP based URL rating.",
    "ssl-exemption-log": "Enable/disable logging of SSL exemptions.",
    "ssl-anomaly-log": "Enable/disable logging of SSL anomalies.",
    "ssl-negotiation-log": "Enable/disable logging of SSL negotiation events.",
    "ssl-server-cert-log": "Enable/disable logging of server certificate information.",
    "ssl-handshake-log": "Enable/disable logging of TLS handshakes.",
    "rpc-over-https": "Enable/disable inspection of RPC over HTTPS.",
    "mapi-over-https": "Enable/disable inspection of MAPI over HTTPS.",
    "supported-alpn": "Configure ALPN option.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
    "caname": {"type": "string", "max_length": 35},
    "untrusted-caname": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "ssl": {
        "inspect-all": {
            "type": "option",
            "help": "Level of SSL inspection.",
            "default": "disable",
            "options": ["disable", "certificate-inspection", "deep-inspection"],
        },
        "client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
        "unsupported-ssl-version": {
            "type": "option",
            "help": "Action based on the SSL version used being unsupported.",
            "default": "block",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-cipher": {
            "type": "option",
            "help": "Action based on the SSL cipher used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-negotiation": {
            "type": "option",
            "help": "Action based on the SSL negotiation used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "expired-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is expired.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "revoked-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is revoked.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "untrusted-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is not issued by a trusted CA.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-timeout": {
            "type": "option",
            "help": "Action based on certificate validation timeout.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-failure": {
            "type": "option",
            "help": "Action based on certificate validation failure.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "sni-server-cert-check": {
            "type": "option",
            "help": "Check the SNI in the client hello message with the CN or SAN fields in the returned server certificate.",
            "default": "enable",
            "options": ["enable", "strict", "disable"],
        },
        "cert-probe-failure": {
            "type": "option",
            "help": "Action based on certificate probe failure.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "encrypted-client-hello": {
            "type": "option",
            "help": "Block/allow session based on existence of encrypted-client-hello.",
            "default": "block",
            "options": ["allow", "block"],
        },
        "min-allowed-ssl-version": {
            "type": "option",
            "help": "Minimum SSL version to be allowed.",
            "default": "tls-1.1",
            "options": ["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
    },
    "https": {
        "ports": {
            "type": "integer",
            "help": "Ports to use for scanning (1 - 65535, default = 443).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Configure protocol inspection status.",
            "default": "deep-inspection",
            "options": ["disable", "certificate-inspection", "deep-inspection"],
        },
        "quic": {
            "type": "option",
            "help": "QUIC inspection status (default = inspect).",
            "default": "inspect",
            "options": ["inspect", "bypass", "block"],
        },
        "udp-not-quic": {
            "type": "option",
            "help": "Action to be taken when matched UDP packet is not QUIC.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
        "unsupported-ssl-version": {
            "type": "option",
            "help": "Action based on the SSL version used being unsupported.",
            "default": "block",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-cipher": {
            "type": "option",
            "help": "Action based on the SSL cipher used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-negotiation": {
            "type": "option",
            "help": "Action based on the SSL negotiation used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "expired-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is expired.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "revoked-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is revoked.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "untrusted-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is not issued by a trusted CA.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-timeout": {
            "type": "option",
            "help": "Action based on certificate validation timeout.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-failure": {
            "type": "option",
            "help": "Action based on certificate validation failure.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "sni-server-cert-check": {
            "type": "option",
            "help": "Check the SNI in the client hello message with the CN or SAN fields in the returned server certificate.",
            "default": "enable",
            "options": ["enable", "strict", "disable"],
        },
        "cert-probe-failure": {
            "type": "option",
            "help": "Action based on certificate probe failure.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "encrypted-client-hello": {
            "type": "option",
            "help": "Block/allow session based on existence of encrypted-client-hello.",
            "default": "block",
            "options": ["allow", "block"],
        },
        "min-allowed-ssl-version": {
            "type": "option",
            "help": "Minimum SSL version to be allowed.",
            "default": "tls-1.1",
            "options": ["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
    },
    "ftps": {
        "ports": {
            "type": "integer",
            "help": "Ports to use for scanning (1 - 65535, default = 443).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Configure protocol inspection status.",
            "default": "deep-inspection",
            "options": ["disable", "deep-inspection"],
        },
        "client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
        "unsupported-ssl-version": {
            "type": "option",
            "help": "Action based on the SSL version used being unsupported.",
            "default": "block",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-cipher": {
            "type": "option",
            "help": "Action based on the SSL cipher used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-negotiation": {
            "type": "option",
            "help": "Action based on the SSL negotiation used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "expired-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is expired.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "revoked-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is revoked.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "untrusted-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is not issued by a trusted CA.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-timeout": {
            "type": "option",
            "help": "Action based on certificate validation timeout.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-failure": {
            "type": "option",
            "help": "Action based on certificate validation failure.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "sni-server-cert-check": {
            "type": "option",
            "help": "Check the SNI in the client hello message with the CN or SAN fields in the returned server certificate.",
            "default": "enable",
            "options": ["enable", "strict", "disable"],
        },
        "min-allowed-ssl-version": {
            "type": "option",
            "help": "Minimum SSL version to be allowed.",
            "default": "tls-1.1",
            "options": ["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
    },
    "imaps": {
        "ports": {
            "type": "integer",
            "help": "Ports to use for scanning (1 - 65535, default = 443).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Configure protocol inspection status.",
            "default": "deep-inspection",
            "options": ["disable", "deep-inspection"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate.",
            "default": "inspect",
            "options": ["bypass", "inspect", "block"],
        },
        "unsupported-ssl-version": {
            "type": "option",
            "help": "Action based on the SSL version used being unsupported.",
            "default": "block",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-cipher": {
            "type": "option",
            "help": "Action based on the SSL cipher used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-negotiation": {
            "type": "option",
            "help": "Action based on the SSL negotiation used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "expired-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is expired.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "revoked-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is revoked.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "untrusted-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is not issued by a trusted CA.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-timeout": {
            "type": "option",
            "help": "Action based on certificate validation timeout.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-failure": {
            "type": "option",
            "help": "Action based on certificate validation failure.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "sni-server-cert-check": {
            "type": "option",
            "help": "Check the SNI in the client hello message with the CN or SAN fields in the returned server certificate.",
            "default": "enable",
            "options": ["enable", "strict", "disable"],
        },
    },
    "pop3s": {
        "ports": {
            "type": "integer",
            "help": "Ports to use for scanning (1 - 65535, default = 443).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Configure protocol inspection status.",
            "default": "deep-inspection",
            "options": ["disable", "deep-inspection"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate.",
            "default": "inspect",
            "options": ["bypass", "inspect", "block"],
        },
        "unsupported-ssl-version": {
            "type": "option",
            "help": "Action based on the SSL version used being unsupported.",
            "default": "block",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-cipher": {
            "type": "option",
            "help": "Action based on the SSL cipher used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-negotiation": {
            "type": "option",
            "help": "Action based on the SSL negotiation used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "expired-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is expired.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "revoked-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is revoked.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "untrusted-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is not issued by a trusted CA.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-timeout": {
            "type": "option",
            "help": "Action based on certificate validation timeout.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-failure": {
            "type": "option",
            "help": "Action based on certificate validation failure.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "sni-server-cert-check": {
            "type": "option",
            "help": "Check the SNI in the client hello message with the CN or SAN fields in the returned server certificate.",
            "default": "enable",
            "options": ["enable", "strict", "disable"],
        },
    },
    "smtps": {
        "ports": {
            "type": "integer",
            "help": "Ports to use for scanning (1 - 65535, default = 443).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Configure protocol inspection status.",
            "default": "deep-inspection",
            "options": ["disable", "deep-inspection"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate.",
            "default": "inspect",
            "options": ["bypass", "inspect", "block"],
        },
        "unsupported-ssl-version": {
            "type": "option",
            "help": "Action based on the SSL version used being unsupported.",
            "default": "block",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-cipher": {
            "type": "option",
            "help": "Action based on the SSL cipher used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-negotiation": {
            "type": "option",
            "help": "Action based on the SSL negotiation used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "expired-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is expired.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "revoked-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is revoked.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "untrusted-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is not issued by a trusted CA.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-timeout": {
            "type": "option",
            "help": "Action based on certificate validation timeout.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-failure": {
            "type": "option",
            "help": "Action based on certificate validation failure.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "sni-server-cert-check": {
            "type": "option",
            "help": "Check the SNI in the client hello message with the CN or SAN fields in the returned server certificate.",
            "default": "enable",
            "options": ["enable", "strict", "disable"],
        },
    },
    "ssh": {
        "ports": {
            "type": "integer",
            "help": "Ports to use for scanning (1 - 65535, default = 443).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Configure protocol inspection status.",
            "default": "disable",
            "options": ["disable", "deep-inspection"],
        },
        "inspect-all": {
            "type": "option",
            "help": "Level of SSL inspection.",
            "default": "disable",
            "options": ["disable", "deep-inspection"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "unsupported-version": {
            "type": "option",
            "help": "Action based on SSH version being unsupported.",
            "default": "bypass",
            "options": ["bypass", "block"],
        },
        "ssh-tun-policy-check": {
            "type": "option",
            "help": "Enable/disable SSH tunnel policy check.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "ssh-algorithm": {
            "type": "option",
            "help": "Relative strength of encryption algorithms accepted during negotiation.",
            "default": "compatible",
            "options": ["compatible", "high-encryption"],
        },
    },
    "dot": {
        "status": {
            "type": "option",
            "help": "Configure protocol inspection status.",
            "default": "disable",
            "options": ["disable", "deep-inspection"],
        },
        "quic": {
            "type": "option",
            "help": "QUIC inspection status (default = inspect).",
            "default": "inspect",
            "options": ["inspect", "bypass", "block"],
        },
        "udp-not-quic": {
            "type": "option",
            "help": "Action to be taken when matched UDP packet is not QUIC.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
        "unsupported-ssl-version": {
            "type": "option",
            "help": "Action based on the SSL version used being unsupported.",
            "default": "block",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-cipher": {
            "type": "option",
            "help": "Action based on the SSL cipher used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "unsupported-ssl-negotiation": {
            "type": "option",
            "help": "Action based on the SSL negotiation used being unsupported.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "expired-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is expired.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "revoked-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is revoked.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "untrusted-server-cert": {
            "type": "option",
            "help": "Action based on server certificate is not issued by a trusted CA.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-timeout": {
            "type": "option",
            "help": "Action based on certificate validation timeout.",
            "default": "allow",
            "options": ["allow", "block", "ignore"],
        },
        "cert-validation-failure": {
            "type": "option",
            "help": "Action based on certificate validation failure.",
            "default": "block",
            "options": ["allow", "block", "ignore"],
        },
        "sni-server-cert-check": {
            "type": "option",
            "help": "Check the SNI in the client hello message with the CN or SAN fields in the returned server certificate.",
            "default": "enable",
            "options": ["enable", "strict", "disable"],
        },
    },
    "ssl-exempt": {
        "id": {
            "type": "integer",
            "help": "ID number.",
            "default": 0,
            "min_value": 0,
            "max_value": 512,
        },
        "type": {
            "type": "option",
            "help": "Type of address object (IPv4 or IPv6) or FortiGuard category.",
            "required": True,
            "default": "fortiguard-category",
            "options": ["fortiguard-category", "address", "address6", "wildcard-fqdn", "regex"],
        },
        "fortiguard-category": {
            "type": "integer",
            "help": "FortiGuard category ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "address": {
            "type": "string",
            "help": "IPv4 address object.",
            "default": "",
            "max_length": 79,
        },
        "address6": {
            "type": "string",
            "help": "IPv6 address object.",
            "default": "",
            "max_length": 79,
        },
        "wildcard-fqdn": {
            "type": "string",
            "help": "Exempt servers by wildcard FQDN.",
            "default": "",
            "max_length": 79,
        },
        "regex": {
            "type": "string",
            "help": "Exempt servers by regular expression.",
            "default": "",
            "max_length": 255,
        },
    },
    "ech-outer-sni": {
        "name": {
            "type": "string",
            "help": "ClientHelloOuter SNI name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
        "sni": {
            "type": "string",
            "help": "ClientHelloOuter SNI to be blocked.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
    },
    "server-cert": {
        "name": {
            "type": "string",
            "help": "Certificate list.",
            "default": "Fortinet_SSL",
            "max_length": 79,
        },
    },
    "ssl-server": {
        "id": {
            "type": "integer",
            "help": "SSL server ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ip": {
            "type": "ipv4-address-any",
            "help": "IPv4 address of the SSL server.",
            "required": True,
            "default": "0.0.0.0",
        },
        "https-client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate during the HTTPS handshake.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
        "smtps-client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate during the SMTPS handshake.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
        "pop3s-client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate during the POP3S handshake.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
        "imaps-client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate during the IMAPS handshake.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
        "ftps-client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate during the FTPS handshake.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
        "ssl-other-client-certificate": {
            "type": "option",
            "help": "Action based on received client certificate during an SSL protocol handshake.",
            "default": "bypass",
            "options": ["bypass", "inspect", "block"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_ALLOWLIST = [
    "enable",
    "disable",
]
VALID_BODY_BLOCK_BLOCKLISTED_CERTIFICATES = [
    "disable",
    "enable",
]
VALID_BODY_SERVER_CERT_MODE = [
    "re-sign",
    "replace",
]
VALID_BODY_USE_SSL_SERVER = [
    "disable",
    "enable",
]
VALID_BODY_SSL_EXEMPTION_IP_RATING = [
    "enable",
    "disable",
]
VALID_BODY_SSL_EXEMPTION_LOG = [
    "disable",
    "enable",
]
VALID_BODY_SSL_ANOMALY_LOG = [
    "disable",
    "enable",
]
VALID_BODY_SSL_NEGOTIATION_LOG = [
    "disable",
    "enable",
]
VALID_BODY_SSL_SERVER_CERT_LOG = [
    "disable",
    "enable",
]
VALID_BODY_SSL_HANDSHAKE_LOG = [
    "disable",
    "enable",
]
VALID_BODY_RPC_OVER_HTTPS = [
    "enable",
    "disable",
]
VALID_BODY_MAPI_OVER_HTTPS = [
    "enable",
    "disable",
]
VALID_BODY_SUPPORTED_ALPN = [
    "http1-1",
    "http2",
    "all",
    "none",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_ssl_ssh_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/ssl_ssh_profile."""
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


def validate_firewall_ssl_ssh_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/ssl_ssh_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "allowlist" in payload:
        is_valid, error = _validate_enum_field(
            "allowlist",
            payload["allowlist"],
            VALID_BODY_ALLOWLIST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-blocklisted-certificates" in payload:
        is_valid, error = _validate_enum_field(
            "block-blocklisted-certificates",
            payload["block-blocklisted-certificates"],
            VALID_BODY_BLOCK_BLOCKLISTED_CERTIFICATES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-cert-mode" in payload:
        is_valid, error = _validate_enum_field(
            "server-cert-mode",
            payload["server-cert-mode"],
            VALID_BODY_SERVER_CERT_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-ssl-server" in payload:
        is_valid, error = _validate_enum_field(
            "use-ssl-server",
            payload["use-ssl-server"],
            VALID_BODY_USE_SSL_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-exemption-ip-rating" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-exemption-ip-rating",
            payload["ssl-exemption-ip-rating"],
            VALID_BODY_SSL_EXEMPTION_IP_RATING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-exemption-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-exemption-log",
            payload["ssl-exemption-log"],
            VALID_BODY_SSL_EXEMPTION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-anomaly-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-anomaly-log",
            payload["ssl-anomaly-log"],
            VALID_BODY_SSL_ANOMALY_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-negotiation-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-negotiation-log",
            payload["ssl-negotiation-log"],
            VALID_BODY_SSL_NEGOTIATION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-cert-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-cert-log",
            payload["ssl-server-cert-log"],
            VALID_BODY_SSL_SERVER_CERT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-handshake-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-handshake-log",
            payload["ssl-handshake-log"],
            VALID_BODY_SSL_HANDSHAKE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rpc-over-https" in payload:
        is_valid, error = _validate_enum_field(
            "rpc-over-https",
            payload["rpc-over-https"],
            VALID_BODY_RPC_OVER_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mapi-over-https" in payload:
        is_valid, error = _validate_enum_field(
            "mapi-over-https",
            payload["mapi-over-https"],
            VALID_BODY_MAPI_OVER_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "supported-alpn" in payload:
        is_valid, error = _validate_enum_field(
            "supported-alpn",
            payload["supported-alpn"],
            VALID_BODY_SUPPORTED_ALPN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_ssl_ssh_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/ssl_ssh_profile."""
    # Validate enum values using central function
    if "allowlist" in payload:
        is_valid, error = _validate_enum_field(
            "allowlist",
            payload["allowlist"],
            VALID_BODY_ALLOWLIST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-blocklisted-certificates" in payload:
        is_valid, error = _validate_enum_field(
            "block-blocklisted-certificates",
            payload["block-blocklisted-certificates"],
            VALID_BODY_BLOCK_BLOCKLISTED_CERTIFICATES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-cert-mode" in payload:
        is_valid, error = _validate_enum_field(
            "server-cert-mode",
            payload["server-cert-mode"],
            VALID_BODY_SERVER_CERT_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-ssl-server" in payload:
        is_valid, error = _validate_enum_field(
            "use-ssl-server",
            payload["use-ssl-server"],
            VALID_BODY_USE_SSL_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-exemption-ip-rating" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-exemption-ip-rating",
            payload["ssl-exemption-ip-rating"],
            VALID_BODY_SSL_EXEMPTION_IP_RATING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-exemption-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-exemption-log",
            payload["ssl-exemption-log"],
            VALID_BODY_SSL_EXEMPTION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-anomaly-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-anomaly-log",
            payload["ssl-anomaly-log"],
            VALID_BODY_SSL_ANOMALY_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-negotiation-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-negotiation-log",
            payload["ssl-negotiation-log"],
            VALID_BODY_SSL_NEGOTIATION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-cert-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-cert-log",
            payload["ssl-server-cert-log"],
            VALID_BODY_SSL_SERVER_CERT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-handshake-log" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-handshake-log",
            payload["ssl-handshake-log"],
            VALID_BODY_SSL_HANDSHAKE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rpc-over-https" in payload:
        is_valid, error = _validate_enum_field(
            "rpc-over-https",
            payload["rpc-over-https"],
            VALID_BODY_RPC_OVER_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mapi-over-https" in payload:
        is_valid, error = _validate_enum_field(
            "mapi-over-https",
            payload["mapi-over-https"],
            VALID_BODY_MAPI_OVER_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "supported-alpn" in payload:
        is_valid, error = _validate_enum_field(
            "supported-alpn",
            payload["supported-alpn"],
            VALID_BODY_SUPPORTED_ALPN,
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
    "endpoint": "firewall/ssl_ssh_profile",
    "category": "cmdb",
    "api_path": "firewall/ssl-ssh-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure SSL/SSH protocol options.",
    "total_fields": 29,
    "required_fields_count": 2,
    "fields_with_defaults_count": 16,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
