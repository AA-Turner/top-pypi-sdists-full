from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_DHCP_IPSEC: Literal["enable", "disable"]
VALID_BODY_PROPOSAL: Literal["null-md5", "null-sha1", "null-sha256", "null-sha384", "null-sha512", "des-null", "des-md5", "des-sha1", "des-sha256", "des-sha384", "des-sha512", "3des-null", "3des-md5", "3des-sha1", "3des-sha256", "3des-sha384", "3des-sha512", "aes128-null", "aes128-md5", "aes128-sha1", "aes128-sha256", "aes128-sha384", "aes128-sha512", "aes128gcm", "aes192-null", "aes192-md5", "aes192-sha1", "aes192-sha256", "aes192-sha384", "aes192-sha512", "aes256-null", "aes256-md5", "aes256-sha1", "aes256-sha256", "aes256-sha384", "aes256-sha512", "aes256gcm", "chacha20poly1305", "aria128-null", "aria128-md5", "aria128-sha1", "aria128-sha256", "aria128-sha384", "aria128-sha512", "aria192-null", "aria192-md5", "aria192-sha1", "aria192-sha256", "aria192-sha384", "aria192-sha512", "aria256-null", "aria256-md5", "aria256-sha1", "aria256-sha256", "aria256-sha384", "aria256-sha512", "seed-null", "seed-md5", "seed-sha1", "seed-sha256", "seed-sha384", "seed-sha512"]
VALID_BODY_PFS: Literal["enable", "disable"]
VALID_BODY_DHGRP: Literal["1", "2", "5", "14", "15", "16", "17", "18", "19", "20", "21", "27", "28", "29", "30", "31", "32"]
VALID_BODY_ADDKE1: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE2: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE3: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE4: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE5: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE6: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE7: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_REPLAY: Literal["enable", "disable"]
VALID_BODY_KEEPALIVE: Literal["enable", "disable"]
VALID_BODY_AUTO_NEGOTIATE: Literal["enable", "disable"]
VALID_BODY_ADD_ROUTE: Literal["phase1", "enable", "disable"]
VALID_BODY_INBOUND_DSCP_COPY: Literal["phase1", "enable", "disable"]
VALID_BODY_AUTO_DISCOVERY_SENDER: Literal["phase1", "enable", "disable"]
VALID_BODY_AUTO_DISCOVERY_FORWARDER: Literal["phase1", "enable", "disable"]
VALID_BODY_KEYLIFE_TYPE: Literal["seconds", "kbs", "both"]
VALID_BODY_SINGLE_SOURCE: Literal["enable", "disable"]
VALID_BODY_ROUTE_OVERLAP: Literal["use-old", "use-new", "allow"]
VALID_BODY_ENCAPSULATION: Literal["tunnel-mode", "transport-mode"]
VALID_BODY_L2TP: Literal["enable", "disable"]
VALID_BODY_INITIATOR_TS_NARROW: Literal["enable", "disable"]
VALID_BODY_DIFFSERV: Literal["enable", "disable"]
VALID_BODY_SRC_ADDR_TYPE: Literal["subnet", "range", "ip", "name", "subnet6", "range6", "ip6", "name6"]
VALID_BODY_DST_ADDR_TYPE: Literal["subnet", "range", "ip", "name", "subnet6", "range6", "ip6", "name6"]

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
    "VALID_BODY_DHCP_IPSEC",
    "VALID_BODY_PROPOSAL",
    "VALID_BODY_PFS",
    "VALID_BODY_DHGRP",
    "VALID_BODY_ADDKE1",
    "VALID_BODY_ADDKE2",
    "VALID_BODY_ADDKE3",
    "VALID_BODY_ADDKE4",
    "VALID_BODY_ADDKE5",
    "VALID_BODY_ADDKE6",
    "VALID_BODY_ADDKE7",
    "VALID_BODY_REPLAY",
    "VALID_BODY_KEEPALIVE",
    "VALID_BODY_AUTO_NEGOTIATE",
    "VALID_BODY_ADD_ROUTE",
    "VALID_BODY_INBOUND_DSCP_COPY",
    "VALID_BODY_AUTO_DISCOVERY_SENDER",
    "VALID_BODY_AUTO_DISCOVERY_FORWARDER",
    "VALID_BODY_KEYLIFE_TYPE",
    "VALID_BODY_SINGLE_SOURCE",
    "VALID_BODY_ROUTE_OVERLAP",
    "VALID_BODY_ENCAPSULATION",
    "VALID_BODY_L2TP",
    "VALID_BODY_INITIATOR_TS_NARROW",
    "VALID_BODY_DIFFSERV",
    "VALID_BODY_SRC_ADDR_TYPE",
    "VALID_BODY_DST_ADDR_TYPE",
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