from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_ALLOWLIST: Literal["enable", "disable"]
VALID_BODY_BLOCK_BLOCKLISTED_CERTIFICATES: Literal["disable", "enable"]
VALID_BODY_SERVER_CERT_MODE: Literal["re-sign", "replace"]
VALID_BODY_USE_SSL_SERVER: Literal["disable", "enable"]
VALID_BODY_SSL_EXEMPTION_IP_RATING: Literal["enable", "disable"]
VALID_BODY_SSL_EXEMPTION_LOG: Literal["disable", "enable"]
VALID_BODY_SSL_ANOMALY_LOG: Literal["disable", "enable"]
VALID_BODY_SSL_NEGOTIATION_LOG: Literal["disable", "enable"]
VALID_BODY_SSL_SERVER_CERT_LOG: Literal["disable", "enable"]
VALID_BODY_SSL_HANDSHAKE_LOG: Literal["disable", "enable"]
VALID_BODY_RPC_OVER_HTTPS: Literal["enable", "disable"]
VALID_BODY_MAPI_OVER_HTTPS: Literal["enable", "disable"]
VALID_BODY_SUPPORTED_ALPN: Literal["http1-1", "http2", "all", "none"]

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
    "VALID_BODY_ALLOWLIST",
    "VALID_BODY_BLOCK_BLOCKLISTED_CERTIFICATES",
    "VALID_BODY_SERVER_CERT_MODE",
    "VALID_BODY_USE_SSL_SERVER",
    "VALID_BODY_SSL_EXEMPTION_IP_RATING",
    "VALID_BODY_SSL_EXEMPTION_LOG",
    "VALID_BODY_SSL_ANOMALY_LOG",
    "VALID_BODY_SSL_NEGOTIATION_LOG",
    "VALID_BODY_SSL_SERVER_CERT_LOG",
    "VALID_BODY_SSL_HANDSHAKE_LOG",
    "VALID_BODY_RPC_OVER_HTTPS",
    "VALID_BODY_MAPI_OVER_HTTPS",
    "VALID_BODY_SUPPORTED_ALPN",
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