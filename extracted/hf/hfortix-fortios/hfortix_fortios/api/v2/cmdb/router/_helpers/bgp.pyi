from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_ALWAYS_COMPARE_MED: Literal["enable", "disable"]
VALID_BODY_BESTPATH_AS_PATH_IGNORE: Literal["enable", "disable"]
VALID_BODY_BESTPATH_CMP_CONFED_ASPATH: Literal["enable", "disable"]
VALID_BODY_BESTPATH_CMP_ROUTERID: Literal["enable", "disable"]
VALID_BODY_BESTPATH_MED_CONFED: Literal["enable", "disable"]
VALID_BODY_BESTPATH_MED_MISSING_AS_WORST: Literal["enable", "disable"]
VALID_BODY_CLIENT_TO_CLIENT_REFLECTION: Literal["enable", "disable"]
VALID_BODY_DAMPENING: Literal["enable", "disable"]
VALID_BODY_DETERMINISTIC_MED: Literal["enable", "disable"]
VALID_BODY_EBGP_MULTIPATH: Literal["enable", "disable"]
VALID_BODY_IBGP_MULTIPATH: Literal["enable", "disable"]
VALID_BODY_ENFORCE_FIRST_AS: Literal["enable", "disable"]
VALID_BODY_FAST_EXTERNAL_FAILOVER: Literal["enable", "disable"]
VALID_BODY_LOG_NEIGHBOUR_CHANGES: Literal["enable", "disable"]
VALID_BODY_NETWORK_IMPORT_CHECK: Literal["enable", "disable"]
VALID_BODY_IGNORE_OPTIONAL_CAPABILITY: Literal["enable", "disable"]
VALID_BODY_ADDITIONAL_PATH: Literal["enable", "disable"]
VALID_BODY_ADDITIONAL_PATH6: Literal["enable", "disable"]
VALID_BODY_ADDITIONAL_PATH_VPNV4: Literal["enable", "disable"]
VALID_BODY_ADDITIONAL_PATH_VPNV6: Literal["enable", "disable"]
VALID_BODY_MULTIPATH_RECURSIVE_DISTANCE: Literal["enable", "disable"]
VALID_BODY_RECURSIVE_NEXT_HOP: Literal["enable", "disable"]
VALID_BODY_RECURSIVE_INHERIT_PRIORITY: Literal["enable", "disable"]
VALID_BODY_TAG_RESOLVE_MODE: Literal["disable", "preferred", "merge", "merge-all"]
VALID_BODY_SYNCHRONIZATION: Literal["enable", "disable"]
VALID_BODY_GRACEFUL_RESTART: Literal["enable", "disable"]
VALID_BODY_GRACEFUL_END_ON_TIMER: Literal["enable", "disable"]
VALID_BODY_CROSS_FAMILY_CONDITIONAL_ADV: Literal["enable", "disable"]

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
    "VALID_BODY_ALWAYS_COMPARE_MED",
    "VALID_BODY_BESTPATH_AS_PATH_IGNORE",
    "VALID_BODY_BESTPATH_CMP_CONFED_ASPATH",
    "VALID_BODY_BESTPATH_CMP_ROUTERID",
    "VALID_BODY_BESTPATH_MED_CONFED",
    "VALID_BODY_BESTPATH_MED_MISSING_AS_WORST",
    "VALID_BODY_CLIENT_TO_CLIENT_REFLECTION",
    "VALID_BODY_DAMPENING",
    "VALID_BODY_DETERMINISTIC_MED",
    "VALID_BODY_EBGP_MULTIPATH",
    "VALID_BODY_IBGP_MULTIPATH",
    "VALID_BODY_ENFORCE_FIRST_AS",
    "VALID_BODY_FAST_EXTERNAL_FAILOVER",
    "VALID_BODY_LOG_NEIGHBOUR_CHANGES",
    "VALID_BODY_NETWORK_IMPORT_CHECK",
    "VALID_BODY_IGNORE_OPTIONAL_CAPABILITY",
    "VALID_BODY_ADDITIONAL_PATH",
    "VALID_BODY_ADDITIONAL_PATH6",
    "VALID_BODY_ADDITIONAL_PATH_VPNV4",
    "VALID_BODY_ADDITIONAL_PATH_VPNV6",
    "VALID_BODY_MULTIPATH_RECURSIVE_DISTANCE",
    "VALID_BODY_RECURSIVE_NEXT_HOP",
    "VALID_BODY_RECURSIVE_INHERIT_PRIORITY",
    "VALID_BODY_TAG_RESOLVE_MODE",
    "VALID_BODY_SYNCHRONIZATION",
    "VALID_BODY_GRACEFUL_RESTART",
    "VALID_BODY_GRACEFUL_END_ON_TIMER",
    "VALID_BODY_CROSS_FAMILY_CONDITIONAL_ADV",
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