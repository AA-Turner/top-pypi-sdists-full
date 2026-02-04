from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_UPSTREAM_INTERFACE_SELECT_METHOD: Literal["auto", "sdwan", "specify"]
VALID_BODY_ACCEPT_AUTH_BY_CERT: Literal["disable", "enable"]
VALID_BODY_LOG_UNIFICATION: Literal["disable", "enable"]
VALID_BODY_AUTHORIZATION_REQUEST_TYPE: Literal["serial", "certificate"]
VALID_BODY_DOWNSTREAM_ACCESS: Literal["enable", "disable"]
VALID_BODY_LEGACY_AUTHENTICATION: Literal["disable", "enable"]
VALID_BODY_CONFIGURATION_SYNC: Literal["default", "local"]
VALID_BODY_FABRIC_OBJECT_UNIFICATION: Literal["default", "local"]
VALID_BODY_SAML_CONFIGURATION_SYNC: Literal["default", "local"]
VALID_BODY_FORTICLOUD_ACCOUNT_ENFORCEMENT: Literal["enable", "disable"]
VALID_BODY_FILE_MGMT: Literal["enable", "disable"]

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
    "VALID_BODY_UPSTREAM_INTERFACE_SELECT_METHOD",
    "VALID_BODY_ACCEPT_AUTH_BY_CERT",
    "VALID_BODY_LOG_UNIFICATION",
    "VALID_BODY_AUTHORIZATION_REQUEST_TYPE",
    "VALID_BODY_DOWNSTREAM_ACCESS",
    "VALID_BODY_LEGACY_AUTHENTICATION",
    "VALID_BODY_CONFIGURATION_SYNC",
    "VALID_BODY_FABRIC_OBJECT_UNIFICATION",
    "VALID_BODY_SAML_CONFIGURATION_SYNC",
    "VALID_BODY_FORTICLOUD_ACCOUNT_ENFORCEMENT",
    "VALID_BODY_FILE_MGMT",
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