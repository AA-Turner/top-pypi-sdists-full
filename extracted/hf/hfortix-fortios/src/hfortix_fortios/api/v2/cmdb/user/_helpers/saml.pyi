from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_SCIM_USER_ATTR_TYPE: Literal["user-name", "display-name", "external-id", "email"]
VALID_BODY_SCIM_GROUP_ATTR_TYPE: Literal["display-name", "external-id"]
VALID_BODY_DIGEST_METHOD: Literal["sha1", "sha256"]
VALID_BODY_REQUIRE_SIGNED_RESP_AND_ASRT: Literal["enable", "disable"]
VALID_BODY_LIMIT_RELAYSTATE: Literal["enable", "disable"]
VALID_BODY_ADFS_CLAIM: Literal["enable", "disable"]
VALID_BODY_USER_CLAIM_TYPE: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"]
VALID_BODY_GROUP_CLAIM_TYPE: Literal["email", "given-name", "name", "upn", "common-name", "email-adfs-1x", "group", "upn-adfs-1x", "role", "sur-name", "ppid", "name-identifier", "authentication-method", "deny-only-group-sid", "deny-only-primary-sid", "deny-only-primary-group-sid", "group-sid", "primary-group-sid", "primary-sid", "windows-account-name"]
VALID_BODY_REAUTH: Literal["enable", "disable"]

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
    "VALID_BODY_SCIM_USER_ATTR_TYPE",
    "VALID_BODY_SCIM_GROUP_ATTR_TYPE",
    "VALID_BODY_DIGEST_METHOD",
    "VALID_BODY_REQUIRE_SIGNED_RESP_AND_ASRT",
    "VALID_BODY_LIMIT_RELAYSTATE",
    "VALID_BODY_ADFS_CLAIM",
    "VALID_BODY_USER_CLAIM_TYPE",
    "VALID_BODY_GROUP_CLAIM_TYPE",
    "VALID_BODY_REAUTH",
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