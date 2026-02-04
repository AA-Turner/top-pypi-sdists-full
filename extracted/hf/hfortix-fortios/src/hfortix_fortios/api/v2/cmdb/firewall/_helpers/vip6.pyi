from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_TYPE: Literal["static-nat", "server-load-balance", "access-proxy"]
VALID_BODY_SRC_VIP_FILTER: Literal["disable", "enable"]
VALID_BODY_NAT_SOURCE_VIP: Literal["disable", "enable"]
VALID_BODY_NDP_REPLY: Literal["disable", "enable"]
VALID_BODY_PORTFORWARD: Literal["disable", "enable"]
VALID_BODY_PROTOCOL: Literal["tcp", "udp", "sctp"]
VALID_BODY_LDB_METHOD: Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"]
VALID_BODY_SERVER_TYPE: Literal["http", "https", "imaps", "pop3s", "smtps", "ssl", "tcp", "udp", "ip"]
VALID_BODY_HTTP_REDIRECT: Literal["enable", "disable"]
VALID_BODY_PERSISTENCE: Literal["none", "http-cookie", "ssl-session-id"]
VALID_BODY_H2_SUPPORT: Literal["enable", "disable"]
VALID_BODY_H3_SUPPORT: Literal["enable", "disable"]
VALID_BODY_NAT66: Literal["disable", "enable"]
VALID_BODY_NAT64: Literal["disable", "enable"]
VALID_BODY_ADD_NAT64_ROUTE: Literal["disable", "enable"]
VALID_BODY_EMPTY_CERT_ACTION: Literal["accept", "block", "accept-unmanageable"]
VALID_BODY_USER_AGENT_DETECT: Literal["disable", "enable"]
VALID_BODY_CLIENT_CERT: Literal["disable", "enable"]
VALID_BODY_HTTP_COOKIE_DOMAIN_FROM_HOST: Literal["disable", "enable"]
VALID_BODY_HTTP_COOKIE_SHARE: Literal["disable", "same-ip"]
VALID_BODY_HTTPS_COOKIE_SECURE: Literal["disable", "enable"]
VALID_BODY_HTTP_MULTIPLEX: Literal["enable", "disable"]
VALID_BODY_HTTP_IP_HEADER: Literal["enable", "disable"]
VALID_BODY_OUTLOOK_WEB_ACCESS: Literal["disable", "enable"]
VALID_BODY_WEBLOGIC_SERVER: Literal["disable", "enable"]
VALID_BODY_WEBSPHERE_SERVER: Literal["disable", "enable"]
VALID_BODY_SSL_MODE: Literal["half", "full"]
VALID_BODY_SSL_DH_BITS: Literal["768", "1024", "1536", "2048", "3072", "4096"]
VALID_BODY_SSL_ALGORITHM: Literal["high", "medium", "low", "custom"]
VALID_BODY_SSL_SERVER_RENEGOTIATION: Literal["enable", "disable"]
VALID_BODY_SSL_SERVER_ALGORITHM: Literal["high", "medium", "low", "custom", "client"]
VALID_BODY_SSL_PFS: Literal["require", "deny", "allow"]
VALID_BODY_SSL_MIN_VERSION: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
VALID_BODY_SSL_MAX_VERSION: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
VALID_BODY_SSL_SERVER_MIN_VERSION: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"]
VALID_BODY_SSL_SERVER_MAX_VERSION: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3", "client"]
VALID_BODY_SSL_ACCEPT_FFDHE_GROUPS: Literal["enable", "disable"]
VALID_BODY_SSL_SEND_EMPTY_FRAGS: Literal["enable", "disable"]
VALID_BODY_SSL_CLIENT_FALLBACK: Literal["disable", "enable"]
VALID_BODY_SSL_CLIENT_RENEGOTIATION: Literal["allow", "deny", "secure"]
VALID_BODY_SSL_CLIENT_SESSION_STATE_TYPE: Literal["disable", "time", "count", "both"]
VALID_BODY_SSL_SERVER_SESSION_STATE_TYPE: Literal["disable", "time", "count", "both"]
VALID_BODY_SSL_HTTP_LOCATION_CONVERSION: Literal["enable", "disable"]
VALID_BODY_SSL_HTTP_MATCH_HOST: Literal["enable", "disable"]
VALID_BODY_SSL_HPKP: Literal["disable", "enable", "report-only"]
VALID_BODY_SSL_HPKP_INCLUDE_SUBDOMAINS: Literal["disable", "enable"]
VALID_BODY_SSL_HSTS: Literal["disable", "enable"]
VALID_BODY_SSL_HSTS_INCLUDE_SUBDOMAINS: Literal["disable", "enable"]
VALID_BODY_EMBEDDED_IPV4_ADDRESS: Literal["disable", "enable"]

# Metadata dictionaries
FIELD_TYPES: dict[str, str]
FIELD_DESCRIPTIONS: dict[str, str]
FIELD_CONSTRAINTS: dict[str, dict[str, Any]]
NESTED_SCHEMAS: dict[str, dict[str, Any]]
FIELDS_WITH_DEFAULTS: dict[str, Any]
DEPRECATED_FIELDS: dict[str, dict[str, str]]
REQUIRED_FIELDS: list[str]

# Helper functions
def get_field_type(field_name: str) -> str | None: ...
def get_field_description(field_name: str) -> str | None: ...
def get_field_default(field_name: str) -> Any: ...
def get_field_constraints(field_name: str) -> dict[str, Any]: ...
def get_nested_schema(field_name: str) -> dict[str, Any] | None: ...
def get_field_metadata(field_name: str) -> dict[str, Any]: ...
def validate_field_value(field_name: str, value: Any) -> bool: ...
def get_all_fields() -> list[str]: ...
def get_required_fields() -> list[str]: ...
def get_schema_info() -> dict[str, Any]: ...


__all__ = [
    "VALID_BODY_TYPE",
    "VALID_BODY_SRC_VIP_FILTER",
    "VALID_BODY_NAT_SOURCE_VIP",
    "VALID_BODY_NDP_REPLY",
    "VALID_BODY_PORTFORWARD",
    "VALID_BODY_PROTOCOL",
    "VALID_BODY_LDB_METHOD",
    "VALID_BODY_SERVER_TYPE",
    "VALID_BODY_HTTP_REDIRECT",
    "VALID_BODY_PERSISTENCE",
    "VALID_BODY_H2_SUPPORT",
    "VALID_BODY_H3_SUPPORT",
    "VALID_BODY_NAT66",
    "VALID_BODY_NAT64",
    "VALID_BODY_ADD_NAT64_ROUTE",
    "VALID_BODY_EMPTY_CERT_ACTION",
    "VALID_BODY_USER_AGENT_DETECT",
    "VALID_BODY_CLIENT_CERT",
    "VALID_BODY_HTTP_COOKIE_DOMAIN_FROM_HOST",
    "VALID_BODY_HTTP_COOKIE_SHARE",
    "VALID_BODY_HTTPS_COOKIE_SECURE",
    "VALID_BODY_HTTP_MULTIPLEX",
    "VALID_BODY_HTTP_IP_HEADER",
    "VALID_BODY_OUTLOOK_WEB_ACCESS",
    "VALID_BODY_WEBLOGIC_SERVER",
    "VALID_BODY_WEBSPHERE_SERVER",
    "VALID_BODY_SSL_MODE",
    "VALID_BODY_SSL_DH_BITS",
    "VALID_BODY_SSL_ALGORITHM",
    "VALID_BODY_SSL_SERVER_RENEGOTIATION",
    "VALID_BODY_SSL_SERVER_ALGORITHM",
    "VALID_BODY_SSL_PFS",
    "VALID_BODY_SSL_MIN_VERSION",
    "VALID_BODY_SSL_MAX_VERSION",
    "VALID_BODY_SSL_SERVER_MIN_VERSION",
    "VALID_BODY_SSL_SERVER_MAX_VERSION",
    "VALID_BODY_SSL_ACCEPT_FFDHE_GROUPS",
    "VALID_BODY_SSL_SEND_EMPTY_FRAGS",
    "VALID_BODY_SSL_CLIENT_FALLBACK",
    "VALID_BODY_SSL_CLIENT_RENEGOTIATION",
    "VALID_BODY_SSL_CLIENT_SESSION_STATE_TYPE",
    "VALID_BODY_SSL_SERVER_SESSION_STATE_TYPE",
    "VALID_BODY_SSL_HTTP_LOCATION_CONVERSION",
    "VALID_BODY_SSL_HTTP_MATCH_HOST",
    "VALID_BODY_SSL_HPKP",
    "VALID_BODY_SSL_HPKP_INCLUDE_SUBDOMAINS",
    "VALID_BODY_SSL_HSTS",
    "VALID_BODY_SSL_HSTS_INCLUDE_SUBDOMAINS",
    "VALID_BODY_EMBEDDED_IPV4_ADDRESS",
    "FIELD_TYPES",
    "FIELD_DESCRIPTIONS",
    "FIELD_CONSTRAINTS",
    "NESTED_SCHEMAS",
    "FIELDS_WITH_DEFAULTS",
    "DEPRECATED_FIELDS",
    "REQUIRED_FIELDS",
    "get_field_type",
    "get_field_description",
    "get_field_default",
    "get_field_constraints",
    "get_nested_schema",
    "get_field_metadata",
    "validate_field_value",
    "get_all_fields",
    "get_required_fields",
    "get_schema_info",
]