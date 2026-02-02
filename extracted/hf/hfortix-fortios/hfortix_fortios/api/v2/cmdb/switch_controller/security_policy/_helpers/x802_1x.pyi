from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_SECURITY_MODE: Literal["802.1X", "802.1X-mac-based"]
VALID_BODY_MAC_AUTH_BYPASS: Literal["disable", "enable"]
VALID_BODY_AUTH_ORDER: Literal["dot1x-mab", "mab-dot1x", "mab"]
VALID_BODY_AUTH_PRIORITY: Literal["legacy", "dot1x-mab", "mab-dot1x"]
VALID_BODY_OPEN_AUTH: Literal["disable", "enable"]
VALID_BODY_EAP_PASSTHRU: Literal["disable", "enable"]
VALID_BODY_EAP_AUTO_UNTAGGED_VLANS: Literal["disable", "enable"]
VALID_BODY_GUEST_VLAN: Literal["disable", "enable"]
VALID_BODY_AUTH_FAIL_VLAN: Literal["disable", "enable"]
VALID_BODY_FRAMEVID_APPLY: Literal["disable", "enable"]
VALID_BODY_RADIUS_TIMEOUT_OVERWRITE: Literal["disable", "enable"]
VALID_BODY_POLICY_TYPE: Literal["802.1X"]
VALID_BODY_AUTHSERVER_TIMEOUT_VLAN: Literal["disable", "enable"]
VALID_BODY_AUTHSERVER_TIMEOUT_TAGGED: Literal["disable", "lldp-voice", "static"]
VALID_BODY_DACL: Literal["disable", "enable"]

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
    "VALID_BODY_SECURITY_MODE",
    "VALID_BODY_MAC_AUTH_BYPASS",
    "VALID_BODY_AUTH_ORDER",
    "VALID_BODY_AUTH_PRIORITY",
    "VALID_BODY_OPEN_AUTH",
    "VALID_BODY_EAP_PASSTHRU",
    "VALID_BODY_EAP_AUTO_UNTAGGED_VLANS",
    "VALID_BODY_GUEST_VLAN",
    "VALID_BODY_AUTH_FAIL_VLAN",
    "VALID_BODY_FRAMEVID_APPLY",
    "VALID_BODY_RADIUS_TIMEOUT_OVERWRITE",
    "VALID_BODY_POLICY_TYPE",
    "VALID_BODY_AUTHSERVER_TIMEOUT_VLAN",
    "VALID_BODY_AUTHSERVER_TIMEOUT_TAGGED",
    "VALID_BODY_DACL",
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