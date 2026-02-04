from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_DIRTY_REASON: Literal["none", "mismatched-ems-sn"]
VALID_BODY_FORTINETONE_CLOUD_AUTHENTICATION: Literal["enable", "disable"]
VALID_BODY_PULL_SYSINFO: Literal["enable", "disable"]
VALID_BODY_PULL_VULNERABILITIES: Literal["enable", "disable"]
VALID_BODY_PULL_TAGS: Literal["enable", "disable"]
VALID_BODY_PULL_MALWARE_HASH: Literal["enable", "disable"]
VALID_BODY_CAPABILITIES: Literal["fabric-auth", "silent-approval", "websocket", "websocket-malware", "push-ca-certs", "common-tags-api", "tenant-id", "client-avatars", "single-vdom-connector", "fgt-sysinfo-api", "ztna-server-info", "used-tags"]
VALID_BODY_SEND_TAGS_TO_ALL_VDOMS: Literal["enable", "disable"]
VALID_BODY_WEBSOCKET_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_INTERFACE_SELECT_METHOD: Literal["auto", "sdwan", "specify"]
VALID_BODY_TRUST_CA_CN: Literal["enable", "disable"]

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
    "VALID_BODY_STATUS",
    "VALID_BODY_DIRTY_REASON",
    "VALID_BODY_FORTINETONE_CLOUD_AUTHENTICATION",
    "VALID_BODY_PULL_SYSINFO",
    "VALID_BODY_PULL_VULNERABILITIES",
    "VALID_BODY_PULL_TAGS",
    "VALID_BODY_PULL_MALWARE_HASH",
    "VALID_BODY_CAPABILITIES",
    "VALID_BODY_SEND_TAGS_TO_ALL_VDOMS",
    "VALID_BODY_WEBSOCKET_OVERRIDE",
    "VALID_BODY_INTERFACE_SELECT_METHOD",
    "VALID_BODY_TRUST_CA_CN",
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