from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_MODE: Literal["standalone", "redundant"]
VALID_BODY_AUTO_DIAL: Literal["enable", "disable"]
VALID_BODY_DIAL_ON_DEMAND: Literal["enable", "disable"]
VALID_BODY_REDIAL: Literal["none", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
VALID_BODY_DONT_SEND_CR1: Literal["enable", "disable"]
VALID_BODY_PEER_MODEM1: Literal["generic", "actiontec", "ascend_TNT"]
VALID_BODY_PPP_ECHO_REQUEST1: Literal["enable", "disable"]
VALID_BODY_AUTHTYPE1: Literal["pap", "chap", "mschap", "mschapv2"]
VALID_BODY_DONT_SEND_CR2: Literal["enable", "disable"]
VALID_BODY_PEER_MODEM2: Literal["generic", "actiontec", "ascend_TNT"]
VALID_BODY_PPP_ECHO_REQUEST2: Literal["enable", "disable"]
VALID_BODY_AUTHTYPE2: Literal["pap", "chap", "mschap", "mschapv2"]
VALID_BODY_DONT_SEND_CR3: Literal["enable", "disable"]
VALID_BODY_PEER_MODEM3: Literal["generic", "actiontec", "ascend_TNT"]
VALID_BODY_PPP_ECHO_REQUEST3: Literal["enable", "disable"]
VALID_BODY_ALTMODE: Literal["enable", "disable"]
VALID_BODY_AUTHTYPE3: Literal["pap", "chap", "mschap", "mschapv2"]
VALID_BODY_TRAFFIC_CHECK: Literal["enable", "disable"]
VALID_BODY_ACTION: Literal["dial", "stop", "none"]

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
    "VALID_BODY_MODE",
    "VALID_BODY_AUTO_DIAL",
    "VALID_BODY_DIAL_ON_DEMAND",
    "VALID_BODY_REDIAL",
    "VALID_BODY_DONT_SEND_CR1",
    "VALID_BODY_PEER_MODEM1",
    "VALID_BODY_PPP_ECHO_REQUEST1",
    "VALID_BODY_AUTHTYPE1",
    "VALID_BODY_DONT_SEND_CR2",
    "VALID_BODY_PEER_MODEM2",
    "VALID_BODY_PPP_ECHO_REQUEST2",
    "VALID_BODY_AUTHTYPE2",
    "VALID_BODY_DONT_SEND_CR3",
    "VALID_BODY_PEER_MODEM3",
    "VALID_BODY_PPP_ECHO_REQUEST3",
    "VALID_BODY_ALTMODE",
    "VALID_BODY_AUTHTYPE3",
    "VALID_BODY_TRAFFIC_CHECK",
    "VALID_BODY_ACTION",
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