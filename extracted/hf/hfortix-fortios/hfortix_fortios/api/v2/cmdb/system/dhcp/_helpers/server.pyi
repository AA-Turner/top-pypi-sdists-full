from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["disable", "enable"]
VALID_BODY_MAC_ACL_DEFAULT_ACTION: Literal["assign", "block"]
VALID_BODY_FORTICLIENT_ON_NET_STATUS: Literal["disable", "enable"]
VALID_BODY_DNS_SERVICE: Literal["local", "default", "specify"]
VALID_BODY_WIFI_AC_SERVICE: Literal["specify", "local"]
VALID_BODY_NTP_SERVICE: Literal["local", "default", "specify"]
VALID_BODY_TIMEZONE_OPTION: Literal["disable", "default", "specify"]
VALID_BODY_SERVER_TYPE: Literal["regular", "ipsec"]
VALID_BODY_IP_MODE: Literal["range", "usrgrp"]
VALID_BODY_AUTO_CONFIGURATION: Literal["disable", "enable"]
VALID_BODY_DHCP_SETTINGS_FROM_FORTIIPAM: Literal["disable", "enable"]
VALID_BODY_AUTO_MANAGED_STATUS: Literal["disable", "enable"]
VALID_BODY_DDNS_UPDATE: Literal["disable", "enable"]
VALID_BODY_DDNS_UPDATE_OVERRIDE: Literal["disable", "enable"]
VALID_BODY_DDNS_AUTH: Literal["disable", "tsig"]
VALID_BODY_VCI_MATCH: Literal["disable", "enable"]
VALID_BODY_SHARED_SUBNET: Literal["disable", "enable"]

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
    "VALID_BODY_MAC_ACL_DEFAULT_ACTION",
    "VALID_BODY_FORTICLIENT_ON_NET_STATUS",
    "VALID_BODY_DNS_SERVICE",
    "VALID_BODY_WIFI_AC_SERVICE",
    "VALID_BODY_NTP_SERVICE",
    "VALID_BODY_TIMEZONE_OPTION",
    "VALID_BODY_SERVER_TYPE",
    "VALID_BODY_IP_MODE",
    "VALID_BODY_AUTO_CONFIGURATION",
    "VALID_BODY_DHCP_SETTINGS_FROM_FORTIIPAM",
    "VALID_BODY_AUTO_MANAGED_STATUS",
    "VALID_BODY_DDNS_UPDATE",
    "VALID_BODY_DDNS_UPDATE_OVERRIDE",
    "VALID_BODY_DDNS_AUTH",
    "VALID_BODY_VCI_MATCH",
    "VALID_BODY_SHARED_SUBNET",
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