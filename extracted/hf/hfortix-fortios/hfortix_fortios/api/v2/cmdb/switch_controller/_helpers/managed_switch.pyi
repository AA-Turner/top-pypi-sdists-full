from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_PURDUE_LEVEL: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
VALID_BODY_FSW_WAN1_ADMIN: Literal["discovered", "disable", "enable"]
VALID_BODY_POE_PRE_STANDARD_DETECTION: Literal["enable", "disable"]
VALID_BODY_DHCP_SERVER_ACCESS_LIST: Literal["global", "enable", "disable"]
VALID_BODY_MCLAG_IGMP_SNOOPING_AWARE: Literal["enable", "disable"]
VALID_BODY_PTP_STATUS: Literal["disable", "enable"]
VALID_BODY_RADIUS_NAS_IP_OVERRIDE: Literal["disable", "enable"]
VALID_BODY_ROUTE_OFFLOAD: Literal["disable", "enable"]
VALID_BODY_ROUTE_OFFLOAD_MCLAG: Literal["disable", "enable"]
VALID_BODY_TYPE: Literal["virtual", "physical"]
VALID_BODY_FIRMWARE_PROVISION: Literal["enable", "disable"]
VALID_BODY_FIRMWARE_PROVISION_LATEST: Literal["disable", "once"]
VALID_BODY_OVERRIDE_SNMP_SYSINFO: Literal["disable", "enable"]
VALID_BODY_OVERRIDE_SNMP_TRAP_THRESHOLD: Literal["enable", "disable"]
VALID_BODY_OVERRIDE_SNMP_COMMUNITY: Literal["enable", "disable"]
VALID_BODY_OVERRIDE_SNMP_USER: Literal["enable", "disable"]
VALID_BODY_QOS_DROP_POLICY: Literal["taildrop", "random-early-detection"]

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
    "VALID_BODY_PURDUE_LEVEL",
    "VALID_BODY_FSW_WAN1_ADMIN",
    "VALID_BODY_POE_PRE_STANDARD_DETECTION",
    "VALID_BODY_DHCP_SERVER_ACCESS_LIST",
    "VALID_BODY_MCLAG_IGMP_SNOOPING_AWARE",
    "VALID_BODY_PTP_STATUS",
    "VALID_BODY_RADIUS_NAS_IP_OVERRIDE",
    "VALID_BODY_ROUTE_OFFLOAD",
    "VALID_BODY_ROUTE_OFFLOAD_MCLAG",
    "VALID_BODY_TYPE",
    "VALID_BODY_FIRMWARE_PROVISION",
    "VALID_BODY_FIRMWARE_PROVISION_LATEST",
    "VALID_BODY_OVERRIDE_SNMP_SYSINFO",
    "VALID_BODY_OVERRIDE_SNMP_TRAP_THRESHOLD",
    "VALID_BODY_OVERRIDE_SNMP_COMMUNITY",
    "VALID_BODY_OVERRIDE_SNMP_USER",
    "VALID_BODY_QOS_DROP_POLICY",
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