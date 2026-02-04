from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_TYPE: Literal["ipmask", "iprange", "fqdn", "geography", "wildcard", "dynamic", "interface-subnet", "mac", "route-tag"]
VALID_BODY_SUB_TYPE: Literal["sdn", "clearpass-spt", "fsso", "rsso", "ems-tag", "fortivoice-tag", "fortinac-tag", "swc-tag", "device-identification", "external-resource", "obsolete"]
VALID_BODY_CLEARPASS_SPT: Literal["unknown", "healthy", "quarantine", "checkup", "transient", "infected"]
VALID_BODY_OBJ_TYPE: Literal["ip", "mac"]
VALID_BODY_SDN_ADDR_TYPE: Literal["private", "public", "all"]
VALID_BODY_NODE_IP_ONLY: Literal["enable", "disable"]
VALID_BODY_ALLOW_ROUTING: Literal["enable", "disable"]
VALID_BODY_PASSIVE_FQDN_LEARNING: Literal["disable", "enable"]
VALID_BODY_FABRIC_OBJECT: Literal["enable", "disable"]

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
    "VALID_BODY_SUB_TYPE",
    "VALID_BODY_CLEARPASS_SPT",
    "VALID_BODY_OBJ_TYPE",
    "VALID_BODY_SDN_ADDR_TYPE",
    "VALID_BODY_NODE_IP_ONLY",
    "VALID_BODY_ALLOW_ROUTING",
    "VALID_BODY_PASSIVE_FQDN_LEARNING",
    "VALID_BODY_FABRIC_OBJECT",
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