"""Validation helpers for voip/profile - Auto-generated"""

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
    "name",  # Profile name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "feature-set": "voipd",
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
    "name": "string",  # Profile name.
    "feature-set": "option",  # IPS or voipd (SIP-ALG) inspection feature set.
    "comment": "var-string",  # Comment.
    "sip": "string",  # SIP.
    "sccp": "string",  # SCCP.
    "msrp": "string",  # MSRP.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "feature-set": "IPS or voipd (SIP-ALG) inspection feature set.",
    "comment": "Comment.",
    "sip": "SIP.",
    "sccp": "SCCP.",
    "msrp": "MSRP.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "sip": {
        "status": {
            "type": "option",
            "help": "Enable/disable SIP.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "rtp": {
            "type": "option",
            "help": "Enable/disable create pinholes for RTP traffic to traverse firewall.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "nat-port-range": {
            "type": "user",
            "help": "RTP NAT port range.",
            "default": "5117-65533",
        },
        "open-register-pinhole": {
            "type": "option",
            "help": "Enable/disable open pinhole for REGISTER Contact port.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "open-contact-pinhole": {
            "type": "option",
            "help": "Enable/disable open pinhole for non-REGISTER Contact port.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "strict-register": {
            "type": "option",
            "help": "Enable/disable only allow the registrar to connect.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "register-rate": {
            "type": "integer",
            "help": "REGISTER request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "register-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "invite-rate": {
            "type": "integer",
            "help": "INVITE request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "invite-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "max-dialogs": {
            "type": "integer",
            "help": "Maximum number of concurrent calls/dialogs (per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "max-line-length": {
            "type": "integer",
            "help": "Maximum SIP header line length (78-4096).",
            "default": 998,
            "min_value": 78,
            "max_value": 4096,
        },
        "block-long-lines": {
            "type": "option",
            "help": "Enable/disable block requests with headers exceeding max-line-length.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "block-unknown": {
            "type": "option",
            "help": "Block unrecognized SIP requests (enabled by default).",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "call-keepalive": {
            "type": "integer",
            "help": "Continue tracking calls with no RTP for this many minutes.",
            "default": 0,
            "min_value": 0,
            "max_value": 10080,
        },
        "block-ack": {
            "type": "option",
            "help": "Enable/disable block ACK requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-bye": {
            "type": "option",
            "help": "Enable/disable block BYE requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-cancel": {
            "type": "option",
            "help": "Enable/disable block CANCEL requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-info": {
            "type": "option",
            "help": "Enable/disable block INFO requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-invite": {
            "type": "option",
            "help": "Enable/disable block INVITE requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-message": {
            "type": "option",
            "help": "Enable/disable block MESSAGE requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-notify": {
            "type": "option",
            "help": "Enable/disable block NOTIFY requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-options": {
            "type": "option",
            "help": "Enable/disable block OPTIONS requests and no OPTIONS as notifying message for redundancy either.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-prack": {
            "type": "option",
            "help": "Enable/disable block prack requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-publish": {
            "type": "option",
            "help": "Enable/disable block PUBLISH requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-refer": {
            "type": "option",
            "help": "Enable/disable block REFER requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-register": {
            "type": "option",
            "help": "Enable/disable block REGISTER requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-subscribe": {
            "type": "option",
            "help": "Enable/disable block SUBSCRIBE requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "block-update": {
            "type": "option",
            "help": "Enable/disable block UPDATE requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "register-contact-trace": {
            "type": "option",
            "help": "Enable/disable trace original IP/port within the contact header of REGISTER requests.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "open-via-pinhole": {
            "type": "option",
            "help": "Enable/disable open pinhole for Via port.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "open-record-route-pinhole": {
            "type": "option",
            "help": "Enable/disable open pinhole for Record-Route port.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "rfc2543-branch": {
            "type": "option",
            "help": "Enable/disable support via branch compliant with RFC 2543.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "log-violations": {
            "type": "option",
            "help": "Enable/disable logging of SIP violations.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "log-call-summary": {
            "type": "option",
            "help": "Enable/disable logging of SIP call summary.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "nat-trace": {
            "type": "option",
            "help": "Enable/disable preservation of original IP in SDP i line.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "subscribe-rate": {
            "type": "integer",
            "help": "SUBSCRIBE request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "subscribe-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "message-rate": {
            "type": "integer",
            "help": "MESSAGE request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "message-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "notify-rate": {
            "type": "integer",
            "help": "NOTIFY request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "notify-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "refer-rate": {
            "type": "integer",
            "help": "REFER request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "refer-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "update-rate": {
            "type": "integer",
            "help": "UPDATE request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "update-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "options-rate": {
            "type": "integer",
            "help": "OPTIONS request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "options-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "ack-rate": {
            "type": "integer",
            "help": "ACK request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ack-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "prack-rate": {
            "type": "integer",
            "help": "PRACK request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "prack-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "info-rate": {
            "type": "integer",
            "help": "INFO request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "info-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "publish-rate": {
            "type": "integer",
            "help": "PUBLISH request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "publish-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "bye-rate": {
            "type": "integer",
            "help": "BYE request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "bye-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "cancel-rate": {
            "type": "integer",
            "help": "CANCEL request rate limit (per second, per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "cancel-rate-track": {
            "type": "option",
            "help": "Track the packet protocol field.",
            "default": "none",
            "options": ["none", "src-ip", "dest-ip"],
        },
        "preserve-override": {
            "type": "option",
            "help": "Override i line to preserve original IPs (default: append).",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "no-sdp-fixup": {
            "type": "option",
            "help": "Enable/disable no SDP fix-up.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "contact-fixup": {
            "type": "option",
            "help": "Fixup contact anyway even if contact's IP:port doesn't match session's IP:port.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "max-idle-dialogs": {
            "type": "integer",
            "help": "Maximum number established but idle dialogs to retain (per policy).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "block-geo-red-options": {
            "type": "option",
            "help": "Enable/disable block OPTIONS requests, but OPTIONS requests still notify for redundancy.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "hosted-nat-traversal": {
            "type": "option",
            "help": "Hosted NAT Traversal (HNT).",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "hnt-restrict-source-ip": {
            "type": "option",
            "help": "Enable/disable restrict RTP source IP to be the same as SIP source IP when HNT is enabled.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "call-id-regex": {
            "type": "var-string",
            "help": "Validate PCRE regular expression for Call-Id header value.",
            "max_length": 511,
        },
        "content-type-regex": {
            "type": "var-string",
            "help": "Validate PCRE regular expression for Content-Type header value.",
            "max_length": 511,
        },
        "max-body-length": {
            "type": "integer",
            "help": "Maximum SIP message body length (0 meaning no limit).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "unknown-header": {
            "type": "option",
            "help": "Action for unknown SIP header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-request-line": {
            "type": "option",
            "help": "Action for malformed request line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-via": {
            "type": "option",
            "help": "Action for malformed VIA header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-from": {
            "type": "option",
            "help": "Action for malformed From header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-to": {
            "type": "option",
            "help": "Action for malformed To header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-call-id": {
            "type": "option",
            "help": "Action for malformed Call-ID header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-cseq": {
            "type": "option",
            "help": "Action for malformed CSeq header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-rack": {
            "type": "option",
            "help": "Action for malformed RAck header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-rseq": {
            "type": "option",
            "help": "Action for malformed RSeq header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-contact": {
            "type": "option",
            "help": "Action for malformed Contact header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-record-route": {
            "type": "option",
            "help": "Action for malformed Record-Route header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-route": {
            "type": "option",
            "help": "Action for malformed Route header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-expires": {
            "type": "option",
            "help": "Action for malformed Expires header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-content-type": {
            "type": "option",
            "help": "Action for malformed Content-Type header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-content-length": {
            "type": "option",
            "help": "Action for malformed Content-Length header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-max-forwards": {
            "type": "option",
            "help": "Action for malformed Max-Forwards header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-allow": {
            "type": "option",
            "help": "Action for malformed Allow header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-p-asserted-identity": {
            "type": "option",
            "help": "Action for malformed P-Asserted-Identity header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-no-require": {
            "type": "option",
            "help": "Action for malformed SIP messages without Require header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-no-proxy-require": {
            "type": "option",
            "help": "Action for malformed SIP messages without Proxy-Require header.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-v": {
            "type": "option",
            "help": "Action for malformed SDP v line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-o": {
            "type": "option",
            "help": "Action for malformed SDP o line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-s": {
            "type": "option",
            "help": "Action for malformed SDP s line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-i": {
            "type": "option",
            "help": "Action for malformed SDP i line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-c": {
            "type": "option",
            "help": "Action for malformed SDP c line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-b": {
            "type": "option",
            "help": "Action for malformed SDP b line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-z": {
            "type": "option",
            "help": "Action for malformed SDP z line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-k": {
            "type": "option",
            "help": "Action for malformed SDP k line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-a": {
            "type": "option",
            "help": "Action for malformed SDP a line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-t": {
            "type": "option",
            "help": "Action for malformed SDP t line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-r": {
            "type": "option",
            "help": "Action for malformed SDP r line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "malformed-header-sdp-m": {
            "type": "option",
            "help": "Action for malformed SDP m line.",
            "default": "pass",
            "options": ["discard", "pass", "respond"],
        },
        "provisional-invite-expiry-time": {
            "type": "integer",
            "help": "Expiry time (10-3600, in seconds) for provisional INVITE.",
            "default": 210,
            "min_value": 10,
            "max_value": 3600,
        },
        "ips-rtp": {
            "type": "option",
            "help": "Enable/disable allow IPS on RTP.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "ssl-mode": {
            "type": "option",
            "help": "SSL/TLS mode for encryption & decryption of traffic.",
            "default": "off",
            "options": ["off", "full"],
        },
        "ssl-send-empty-frags": {
            "type": "option",
            "help": "Send empty fragments to avoid attack on CBC IV (SSL 3.0 & TLS 1.0 only).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ssl-client-renegotiation": {
            "type": "option",
            "help": "Allow/block client renegotiation by server.",
            "default": "allow",
            "options": ["allow", "deny", "secure"],
        },
        "ssl-algorithm": {
            "type": "option",
            "help": "Relative strength of encryption algorithms accepted in negotiation.",
            "default": "high",
            "options": ["high", "medium", "low"],
        },
        "ssl-pfs": {
            "type": "option",
            "help": "SSL Perfect Forward Secrecy.",
            "default": "allow",
            "options": ["require", "deny", "allow"],
        },
        "ssl-min-version": {
            "type": "option",
            "help": "Lowest SSL/TLS version to negotiate.",
            "default": "tls-1.1",
            "options": ["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
        "ssl-max-version": {
            "type": "option",
            "help": "Highest SSL/TLS version to negotiate.",
            "default": "tls-1.3",
            "options": ["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
        "ssl-client-certificate": {
            "type": "string",
            "help": "Name of Certificate to offer to server if requested.",
            "default": "",
            "max_length": 35,
        },
        "ssl-server-certificate": {
            "type": "string",
            "help": "Name of Certificate return to the client in every SSL connection.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "ssl-auth-client": {
            "type": "string",
            "help": "Require a client certificate and authenticate it with the peer/peergrp.",
            "default": "",
            "max_length": 35,
        },
        "ssl-auth-server": {
            "type": "string",
            "help": "Authenticate the server's certificate with the peer/peergrp.",
            "default": "",
            "max_length": 35,
        },
    },
    "sccp": {
        "status": {
            "type": "option",
            "help": "Enable/disable SCCP.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "block-mcast": {
            "type": "option",
            "help": "Enable/disable block multicast RTP connections.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "verify-header": {
            "type": "option",
            "help": "Enable/disable verify SCCP header content.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "log-call-summary": {
            "type": "option",
            "help": "Enable/disable log summary of SCCP calls.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "log-violations": {
            "type": "option",
            "help": "Enable/disable logging of SCCP violations.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "max-calls": {
            "type": "integer",
            "help": "Maximum calls per minute per SCCP client (max 65535).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
    },
    "msrp": {
        "status": {
            "type": "option",
            "help": "Enable/disable MSRP.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "log-violations": {
            "type": "option",
            "help": "Enable/disable logging of MSRP violations.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "max-msg-size": {
            "type": "integer",
            "help": "Maximum allowable MSRP message size (1-65535).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "max-msg-size-action": {
            "type": "option",
            "help": "Action for violation of max-msg-size.",
            "default": "pass",
            "options": ["pass", "block", "reset", "monitor"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_FEATURE_SET = [
    "ips",
    "voipd",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_voip_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for voip/profile."""
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


def validate_voip_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new voip/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "feature-set" in payload:
        is_valid, error = _validate_enum_field(
            "feature-set",
            payload["feature-set"],
            VALID_BODY_FEATURE_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_voip_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update voip/profile."""
    # Validate enum values using central function
    if "feature-set" in payload:
        is_valid, error = _validate_enum_field(
            "feature-set",
            payload["feature-set"],
            VALID_BODY_FEATURE_SET,
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
    "endpoint": "voip/profile",
    "category": "cmdb",
    "api_path": "voip/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure VoIP profiles.",
    "total_fields": 6,
    "required_fields_count": 1,
    "fields_with_defaults_count": 2,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
