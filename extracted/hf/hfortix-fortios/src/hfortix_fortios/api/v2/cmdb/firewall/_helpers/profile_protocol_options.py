"""Validation helpers for firewall/profile_protocol_options - Auto-generated"""

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
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "replacemsg-group": "",
    "oversize-log": "disable",
    "switching-protocols-log": "disable",
    "rpc-over-http": "disable",
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
    "replacemsg-group": "string",  # Name of the replacement message group to be used.
    "oversize-log": "option",  # Enable/disable logging for antivirus oversize file blocking.
    "switching-protocols-log": "option",  # Enable/disable logging for HTTP/HTTPS switching protocols.
    "http": "string",  # Configure HTTP protocol options.
    "ftp": "string",  # Configure FTP protocol options.
    "imap": "string",  # Configure IMAP protocol options.
    "mapi": "string",  # Configure MAPI protocol options.
    "pop3": "string",  # Configure POP3 protocol options.
    "smtp": "string",  # Configure SMTP protocol options.
    "nntp": "string",  # Configure NNTP protocol options.
    "ssh": "string",  # Configure SFTP and SCP protocol options.
    "dns": "string",  # Configure DNS protocol options.
    "cifs": "string",  # Configure CIFS protocol options.
    "mail-signature": "string",  # Configure Mail signature.
    "rpc-over-http": "option",  # Enable/disable inspection of RPC over HTTP.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "comment": "Optional comments.",
    "replacemsg-group": "Name of the replacement message group to be used.",
    "oversize-log": "Enable/disable logging for antivirus oversize file blocking.",
    "switching-protocols-log": "Enable/disable logging for HTTP/HTTPS switching protocols.",
    "http": "Configure HTTP protocol options.",
    "ftp": "Configure FTP protocol options.",
    "imap": "Configure IMAP protocol options.",
    "mapi": "Configure MAPI protocol options.",
    "pop3": "Configure POP3 protocol options.",
    "smtp": "Configure SMTP protocol options.",
    "nntp": "Configure NNTP protocol options.",
    "ssh": "Configure SFTP and SCP protocol options.",
    "dns": "Configure DNS protocol options.",
    "cifs": "Configure CIFS protocol options.",
    "mail-signature": "Configure Mail signature.",
    "rpc-over-http": "Enable/disable inspection of RPC over HTTP.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
    "replacemsg-group": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "http": {
        "ports": {
            "type": "integer",
            "help": "Ports to scan for content (1 - 65535, default = 80).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable the active status of scanning for this protocol.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "inspect-all": {
            "type": "option",
            "help": "Enable/disable the inspection of all ports for the protocol.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "options": {
            "type": "option",
            "help": "One or more options that can be applied to the session.",
            "default": "",
            "options": ["clientcomfort", "servercomfort", "oversize", "chunkedbypass"],
        },
        "comfort-interval": {
            "type": "integer",
            "help": "Interval between successive transmissions of data for client comforting (seconds).",
            "default": 10,
            "min_value": 1,
            "max_value": 900,
        },
        "comfort-amount": {
            "type": "integer",
            "help": "Number of bytes to send in each transmission for client comforting (bytes).",
            "default": 1,
            "min_value": 1,
            "max_value": 65535,
        },
        "range-block": {
            "type": "option",
            "help": "Enable/disable blocking of partial downloads.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "strip-x-forwarded-for": {
            "type": "option",
            "help": "Enable/disable stripping of HTTP X-Forwarded-For header.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "post-lang": {
            "type": "option",
            "help": "ID codes for character sets to be used to convert to UTF-8 for banned words and DLP on HTTP posts (maximum of 5 character sets).",
            "default": "",
            "options": ["jisx0201", "jisx0208", "jisx0212", "gb2312", "ksc5601-ex", "euc-jp", "sjis", "iso2022-jp", "iso2022-jp-1", "iso2022-jp-2", "euc-cn", "ces-gbk", "hz", "ces-big5", "euc-kr", "iso2022-jp-3", "iso8859-1", "tis620", "cp874", "cp1252", "cp1251"],
        },
        "streaming-content-bypass": {
            "type": "option",
            "help": "Enable/disable bypassing of streaming content from buffering.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "switching-protocols": {
            "type": "option",
            "help": "Bypass from scanning, or block a connection that attempts to switch protocol.",
            "default": "bypass",
            "options": ["bypass", "block"],
        },
        "unknown-http-version": {
            "type": "option",
            "help": "How to handle HTTP sessions that do not comply with HTTP 0.9, 1.0, or 1.1.",
            "default": "reject",
            "options": ["reject", "tunnel", "best-effort"],
        },
        "http-0.9": {
            "type": "option",
            "help": "Configure action to take upon receipt of HTTP 0.9 request.",
            "default": "allow",
            "options": ["allow", "block"],
        },
        "tunnel-non-http": {
            "type": "option",
            "help": "Configure how to process non-HTTP traffic when a profile configured for HTTP traffic accepts a non-HTTP session. Can occur if an application sends non-HTTP traffic using an HTTP destination port.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "h2c": {
            "type": "option",
            "help": "Enable/disable h2c HTTP connection upgrade.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "unknown-content-encoding": {
            "type": "option",
            "help": "Configure the action the FortiGate unit will take on unknown content-encoding.",
            "default": "block",
            "options": ["block", "inspect", "bypass"],
        },
        "oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory uncompressed file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-nest-limit": {
            "type": "integer",
            "help": "Maximum nested levels of compression that can be uncompressed and scanned (2 - 100, default = 12).",
            "default": 12,
            "min_value": 2,
            "max_value": 100,
        },
        "stream-based-uncompressed-limit": {
            "type": "integer",
            "help": "Maximum stream-based uncompressed data size that will be scanned in megabytes. Stream-based uncompression used only under certain conditions (unlimited = 0, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "scan-bzip2": {
            "type": "option",
            "help": "Enable/disable scanning of BZip2 compressed files.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "verify-dns-for-policy-matching": {
            "type": "option",
            "help": "Enable/disable verification of DNS for policy matching.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "block-page-status-code": {
            "type": "integer",
            "help": "Code number returned for blocked HTTP pages (non-FortiGuard only) (100 - 599, default = 403).",
            "default": 403,
            "min_value": 100,
            "max_value": 599,
        },
        "retry-count": {
            "type": "integer",
            "help": "Number of attempts to retry HTTP connection (0 - 100, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 100,
        },
        "domain-fronting": {
            "type": "option",
            "help": "Configure HTTP domain fronting (default = block).",
            "default": "block",
            "options": ["allow", "monitor", "block", "strict"],
        },
        "tcp-window-type": {
            "type": "option",
            "help": "TCP window type to use for this protocol.",
            "default": "auto-tuning",
            "options": ["auto-tuning", "system", "static", "dynamic"],
        },
        "tcp-window-minimum": {
            "type": "integer",
            "help": "Minimum dynamic TCP window size.",
            "default": 131072,
            "min_value": 65536,
            "max_value": 1048576,
        },
        "tcp-window-maximum": {
            "type": "integer",
            "help": "Maximum dynamic TCP window size.",
            "default": 8388608,
            "min_value": 1048576,
            "max_value": 16777216,
        },
        "tcp-window-size": {
            "type": "integer",
            "help": "Set TCP static window size.",
            "default": 262144,
            "min_value": 65536,
            "max_value": 16777216,
        },
        "ssl-offloaded": {
            "type": "option",
            "help": "SSL decryption and encryption performed by an external device.",
            "default": "no",
            "options": ["no", "yes"],
        },
        "address-ip-rating": {
            "type": "option",
            "help": "Enable/disable IP based URL rating.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "ftp": {
        "ports": {
            "type": "integer",
            "help": "Ports to scan for content (1 - 65535, default = 21).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable the active status of scanning for this protocol.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "inspect-all": {
            "type": "option",
            "help": "Enable/disable the inspection of all ports for the protocol.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "options": {
            "type": "option",
            "help": "One or more options that can be applied to the session.",
            "default": "",
            "options": ["clientcomfort", "oversize", "splice", "bypass-rest-command", "bypass-mode-command"],
        },
        "comfort-interval": {
            "type": "integer",
            "help": "Interval between successive transmissions of data for client comforting (seconds).",
            "default": 10,
            "min_value": 1,
            "max_value": 900,
        },
        "comfort-amount": {
            "type": "integer",
            "help": "Number of bytes to send in each transmission for client comforting (bytes).",
            "default": 1,
            "min_value": 1,
            "max_value": 65535,
        },
        "oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory uncompressed file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-nest-limit": {
            "type": "integer",
            "help": "Maximum nested levels of compression that can be uncompressed and scanned (2 - 100, default = 12).",
            "default": 12,
            "min_value": 2,
            "max_value": 100,
        },
        "stream-based-uncompressed-limit": {
            "type": "integer",
            "help": "Maximum stream-based uncompressed data size that will be scanned in megabytes. Stream-based uncompression used only under certain conditions (unlimited = 0, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "scan-bzip2": {
            "type": "option",
            "help": "Enable/disable scanning of BZip2 compressed files.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "tcp-window-type": {
            "type": "option",
            "help": "TCP window type to use for this protocol.",
            "default": "auto-tuning",
            "options": ["auto-tuning", "system", "static", "dynamic"],
        },
        "tcp-window-minimum": {
            "type": "integer",
            "help": "Minimum dynamic TCP window size.",
            "default": 131072,
            "min_value": 65536,
            "max_value": 1048576,
        },
        "tcp-window-maximum": {
            "type": "integer",
            "help": "Maximum dynamic TCP window size.",
            "default": 8388608,
            "min_value": 1048576,
            "max_value": 16777216,
        },
        "tcp-window-size": {
            "type": "integer",
            "help": "Set TCP static window size.",
            "default": 262144,
            "min_value": 65536,
            "max_value": 16777216,
        },
        "ssl-offloaded": {
            "type": "option",
            "help": "SSL decryption and encryption performed by an external device.",
            "default": "no",
            "options": ["no", "yes"],
        },
        "explicit-ftp-tls": {
            "type": "option",
            "help": "Enable/disable FTP redirection for explicit FTPS.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
    },
    "imap": {
        "ports": {
            "type": "integer",
            "help": "Ports to scan for content (1 - 65535, default = 143).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable the active status of scanning for this protocol.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "inspect-all": {
            "type": "option",
            "help": "Enable/disable the inspection of all ports for the protocol.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "options": {
            "type": "option",
            "help": "One or more options that can be applied to the session.",
            "default": "",
            "options": ["fragmail", "oversize"],
        },
        "oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory uncompressed file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-nest-limit": {
            "type": "integer",
            "help": "Maximum nested levels of compression that can be uncompressed and scanned (2 - 100, default = 12).",
            "default": 12,
            "min_value": 2,
            "max_value": 100,
        },
        "scan-bzip2": {
            "type": "option",
            "help": "Enable/disable scanning of BZip2 compressed files.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ssl-offloaded": {
            "type": "option",
            "help": "SSL decryption and encryption performed by an external device.",
            "default": "no",
            "options": ["no", "yes"],
        },
    },
    "mapi": {
        "ports": {
            "type": "integer",
            "help": "Ports to scan for content (1 - 65535, default = 135).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable the active status of scanning for this protocol.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "options": {
            "type": "option",
            "help": "One or more options that can be applied to the session.",
            "default": "",
            "options": ["fragmail", "oversize"],
        },
        "oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory uncompressed file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-nest-limit": {
            "type": "integer",
            "help": "Maximum nested levels of compression that can be uncompressed and scanned (2 - 100, default = 12).",
            "default": 12,
            "min_value": 2,
            "max_value": 100,
        },
        "scan-bzip2": {
            "type": "option",
            "help": "Enable/disable scanning of BZip2 compressed files.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "pop3": {
        "ports": {
            "type": "integer",
            "help": "Ports to scan for content (1 - 65535, default = 110).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable the active status of scanning for this protocol.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "inspect-all": {
            "type": "option",
            "help": "Enable/disable the inspection of all ports for the protocol.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "options": {
            "type": "option",
            "help": "One or more options that can be applied to the session.",
            "default": "",
            "options": ["fragmail", "oversize"],
        },
        "oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory uncompressed file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-nest-limit": {
            "type": "integer",
            "help": "Maximum nested levels of compression that can be uncompressed and scanned (2 - 100, default = 12).",
            "default": 12,
            "min_value": 2,
            "max_value": 100,
        },
        "scan-bzip2": {
            "type": "option",
            "help": "Enable/disable scanning of BZip2 compressed files.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ssl-offloaded": {
            "type": "option",
            "help": "SSL decryption and encryption performed by an external device.",
            "default": "no",
            "options": ["no", "yes"],
        },
    },
    "smtp": {
        "ports": {
            "type": "integer",
            "help": "Ports to scan for content (1 - 65535, default = 25).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable the active status of scanning for this protocol.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "inspect-all": {
            "type": "option",
            "help": "Enable/disable the inspection of all ports for the protocol.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "options": {
            "type": "option",
            "help": "One or more options that can be applied to the session.",
            "default": "",
            "options": ["fragmail", "oversize", "splice"],
        },
        "oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory uncompressed file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-nest-limit": {
            "type": "integer",
            "help": "Maximum nested levels of compression that can be uncompressed and scanned (2 - 100, default = 12).",
            "default": 12,
            "min_value": 2,
            "max_value": 100,
        },
        "scan-bzip2": {
            "type": "option",
            "help": "Enable/disable scanning of BZip2 compressed files.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "server-busy": {
            "type": "option",
            "help": "Enable/disable SMTP server busy when server not available.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "ssl-offloaded": {
            "type": "option",
            "help": "SSL decryption and encryption performed by an external device.",
            "default": "no",
            "options": ["no", "yes"],
        },
    },
    "nntp": {
        "ports": {
            "type": "integer",
            "help": "Ports to scan for content (1 - 65535, default = 119).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable the active status of scanning for this protocol.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "inspect-all": {
            "type": "option",
            "help": "Enable/disable the inspection of all ports for the protocol.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "proxy-after-tcp-handshake": {
            "type": "option",
            "help": "Proxy traffic after the TCP 3-way handshake has been established (not before).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "options": {
            "type": "option",
            "help": "One or more options that can be applied to the session.",
            "default": "",
            "options": ["oversize", "splice"],
        },
        "oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory uncompressed file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-nest-limit": {
            "type": "integer",
            "help": "Maximum nested levels of compression that can be uncompressed and scanned (2 - 100, default = 12).",
            "default": 12,
            "min_value": 2,
            "max_value": 100,
        },
        "scan-bzip2": {
            "type": "option",
            "help": "Enable/disable scanning of BZip2 compressed files.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "ssh": {
        "options": {
            "type": "option",
            "help": "One or more options that can be applied to the session.",
            "default": "",
            "options": ["oversize", "clientcomfort", "servercomfort"],
        },
        "comfort-interval": {
            "type": "integer",
            "help": "Interval between successive transmissions of data for client comforting (seconds).",
            "default": 10,
            "min_value": 1,
            "max_value": 900,
        },
        "comfort-amount": {
            "type": "integer",
            "help": "Number of bytes to send in each transmission for client comforting (bytes).",
            "default": 1,
            "min_value": 1,
            "max_value": 65535,
        },
        "oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory uncompressed file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-nest-limit": {
            "type": "integer",
            "help": "Maximum nested levels of compression that can be uncompressed and scanned (2 - 100, default = 12).",
            "default": 12,
            "min_value": 2,
            "max_value": 100,
        },
        "stream-based-uncompressed-limit": {
            "type": "integer",
            "help": "Maximum stream-based uncompressed data size that will be scanned in megabytes. Stream-based uncompression used only under certain conditions (unlimited = 0, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "scan-bzip2": {
            "type": "option",
            "help": "Enable/disable scanning of BZip2 compressed files.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "tcp-window-type": {
            "type": "option",
            "help": "TCP window type to use for this protocol.",
            "default": "auto-tuning",
            "options": ["auto-tuning", "system", "static", "dynamic"],
        },
        "tcp-window-minimum": {
            "type": "integer",
            "help": "Minimum dynamic TCP window size.",
            "default": 131072,
            "min_value": 65536,
            "max_value": 1048576,
        },
        "tcp-window-maximum": {
            "type": "integer",
            "help": "Maximum dynamic TCP window size.",
            "default": 8388608,
            "min_value": 1048576,
            "max_value": 16777216,
        },
        "tcp-window-size": {
            "type": "integer",
            "help": "Set TCP static window size.",
            "default": 262144,
            "min_value": 65536,
            "max_value": 16777216,
        },
        "ssl-offloaded": {
            "type": "option",
            "help": "SSL decryption and encryption performed by an external device.",
            "default": "no",
            "options": ["no", "yes"],
        },
    },
    "dns": {
        "ports": {
            "type": "integer",
            "help": "Ports to scan for content (1 - 65535, default = 53).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable the active status of scanning for this protocol.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "cifs": {
        "ports": {
            "type": "integer",
            "help": "Ports to scan for content (1 - 65535, default = 445).",
            "required": True,
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable the active status of scanning for this protocol.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "options": {
            "type": "option",
            "help": "One or more options that can be applied to the session.",
            "default": "",
            "options": ["oversize"],
        },
        "oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-oversize-limit": {
            "type": "integer",
            "help": "Maximum in-memory uncompressed file size that can be scanned (MB).",
            "default": 10,
            "min_value": 1,
            "max_value": 4095,
        },
        "uncompressed-nest-limit": {
            "type": "integer",
            "help": "Maximum nested levels of compression that can be uncompressed and scanned (2 - 100, default = 12).",
            "default": 12,
            "min_value": 2,
            "max_value": 100,
        },
        "scan-bzip2": {
            "type": "option",
            "help": "Enable/disable scanning of BZip2 compressed files.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "tcp-window-type": {
            "type": "option",
            "help": "TCP window type to use for this protocol.",
            "default": "auto-tuning",
            "options": ["auto-tuning", "system", "static", "dynamic"],
        },
        "tcp-window-minimum": {
            "type": "integer",
            "help": "Minimum dynamic TCP window size.",
            "default": 131072,
            "min_value": 65536,
            "max_value": 1048576,
        },
        "tcp-window-maximum": {
            "type": "integer",
            "help": "Maximum dynamic TCP window size.",
            "default": 8388608,
            "min_value": 1048576,
            "max_value": 16777216,
        },
        "tcp-window-size": {
            "type": "integer",
            "help": "Set TCP static window size.",
            "default": 262144,
            "min_value": 65536,
            "max_value": 16777216,
        },
        "server-credential-type": {
            "type": "option",
            "help": "CIFS server credential type.",
            "required": True,
            "default": "none",
            "options": ["none", "credential-replication", "credential-keytab"],
        },
        "domain-controller": {
            "type": "string",
            "help": "Domain for which to decrypt CIFS traffic.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "server-keytab": {
            "type": "string",
            "help": "Server keytab.",
        },
    },
    "mail-signature": {
        "status": {
            "type": "option",
            "help": "Enable/disable adding an email signature to SMTP email messages as they pass through the FortiGate.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "signature": {
            "type": "string",
            "help": "Email signature to be added to outgoing email (if the signature contains spaces, enclose with quotation marks).",
            "default": "",
            "max_length": 1023,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_OVERSIZE_LOG = [
    "disable",
    "enable",
]
VALID_BODY_SWITCHING_PROTOCOLS_LOG = [
    "disable",
    "enable",
]
VALID_BODY_RPC_OVER_HTTP = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_profile_protocol_options_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/profile_protocol_options."""
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


def validate_firewall_profile_protocol_options_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/profile_protocol_options object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "oversize-log" in payload:
        is_valid, error = _validate_enum_field(
            "oversize-log",
            payload["oversize-log"],
            VALID_BODY_OVERSIZE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switching-protocols-log" in payload:
        is_valid, error = _validate_enum_field(
            "switching-protocols-log",
            payload["switching-protocols-log"],
            VALID_BODY_SWITCHING_PROTOCOLS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rpc-over-http" in payload:
        is_valid, error = _validate_enum_field(
            "rpc-over-http",
            payload["rpc-over-http"],
            VALID_BODY_RPC_OVER_HTTP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_profile_protocol_options_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/profile_protocol_options."""
    # Validate enum values using central function
    if "oversize-log" in payload:
        is_valid, error = _validate_enum_field(
            "oversize-log",
            payload["oversize-log"],
            VALID_BODY_OVERSIZE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switching-protocols-log" in payload:
        is_valid, error = _validate_enum_field(
            "switching-protocols-log",
            payload["switching-protocols-log"],
            VALID_BODY_SWITCHING_PROTOCOLS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rpc-over-http" in payload:
        is_valid, error = _validate_enum_field(
            "rpc-over-http",
            payload["rpc-over-http"],
            VALID_BODY_RPC_OVER_HTTP,
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
    "endpoint": "firewall/profile_protocol_options",
    "category": "cmdb",
    "api_path": "firewall/profile-protocol-options",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure protocol options.",
    "total_fields": 17,
    "required_fields_count": 1,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
