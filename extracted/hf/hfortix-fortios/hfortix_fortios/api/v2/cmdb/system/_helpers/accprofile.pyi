from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_SCOPE: Literal["vdom", "global"]
VALID_BODY_SECFABGRP: Literal["none", "read", "read-write", "custom"]
VALID_BODY_FTVIEWGRP: Literal["none", "read", "read-write"]
VALID_BODY_AUTHGRP: Literal["none", "read", "read-write"]
VALID_BODY_SYSGRP: Literal["none", "read", "read-write", "custom"]
VALID_BODY_NETGRP: Literal["none", "read", "read-write", "custom"]
VALID_BODY_LOGGRP: Literal["none", "read", "read-write", "custom"]
VALID_BODY_FWGRP: Literal["none", "read", "read-write", "custom"]
VALID_BODY_VPNGRP: Literal["none", "read", "read-write"]
VALID_BODY_UTMGRP: Literal["none", "read", "read-write", "custom"]
VALID_BODY_WANOPTGRP: Literal["none", "read", "read-write"]
VALID_BODY_WIFI: Literal["none", "read", "read-write"]
VALID_BODY_ADMINTIMEOUT_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_CLI_DIAGNOSE: Literal["enable", "disable"]
VALID_BODY_CLI_GET: Literal["enable", "disable"]
VALID_BODY_CLI_SHOW: Literal["enable", "disable"]
VALID_BODY_CLI_EXEC: Literal["enable", "disable"]
VALID_BODY_CLI_CONFIG: Literal["enable", "disable"]
VALID_BODY_SYSTEM_EXECUTE_SSH: Literal["enable", "disable"]
VALID_BODY_SYSTEM_EXECUTE_TELNET: Literal["enable", "disable"]

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
    "VALID_BODY_SCOPE",
    "VALID_BODY_SECFABGRP",
    "VALID_BODY_FTVIEWGRP",
    "VALID_BODY_AUTHGRP",
    "VALID_BODY_SYSGRP",
    "VALID_BODY_NETGRP",
    "VALID_BODY_LOGGRP",
    "VALID_BODY_FWGRP",
    "VALID_BODY_VPNGRP",
    "VALID_BODY_UTMGRP",
    "VALID_BODY_WANOPTGRP",
    "VALID_BODY_WIFI",
    "VALID_BODY_ADMINTIMEOUT_OVERRIDE",
    "VALID_BODY_CLI_DIAGNOSE",
    "VALID_BODY_CLI_GET",
    "VALID_BODY_CLI_SHOW",
    "VALID_BODY_CLI_EXEC",
    "VALID_BODY_CLI_CONFIG",
    "VALID_BODY_SYSTEM_EXECUTE_SSH",
    "VALID_BODY_SYSTEM_EXECUTE_TELNET",
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