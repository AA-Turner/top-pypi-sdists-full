from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_TRAP_STATUS: Literal["enable", "disable"]
VALID_BODY_QUERIES: Literal["enable", "disable"]
VALID_BODY_HA_DIRECT: Literal["enable", "disable"]
VALID_BODY_EVENTS: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "vpn-tun-up", "vpn-tun-down", "ha-switch", "ha-hb-failure", "ips-signature", "ips-anomaly", "av-virus", "av-oversize", "av-pattern", "av-fragmented", "fm-if-change", "fm-conf-change", "bgp-established", "bgp-backward-transition", "ha-member-up", "ha-member-down", "ent-conf-change", "av-conserve", "av-bypass", "av-oversize-passed", "av-oversize-blocked", "ips-pkg-update", "ips-fail-open", "faz-disconnect", "faz", "wc-ap-up", "wc-ap-down", "fswctl-session-up", "fswctl-session-down", "load-balance-real-server-down", "device-new", "per-cpu-high", "dhcp", "pool-usage", "ippool", "interface", "ospf-nbr-state-change", "ospf-virtnbr-state-change", "bfd"]
VALID_BODY_SECURITY_LEVEL: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]
VALID_BODY_AUTH_PROTO: Literal["md5", "sha", "sha224", "sha256", "sha384", "sha512"]
VALID_BODY_PRIV_PROTO: Literal["aes", "des", "aes256", "aes256cisco"]
VALID_BODY_INTERFACE_SELECT_METHOD: Literal["auto", "sdwan", "specify"]

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
    "VALID_BODY_TRAP_STATUS",
    "VALID_BODY_QUERIES",
    "VALID_BODY_HA_DIRECT",
    "VALID_BODY_EVENTS",
    "VALID_BODY_SECURITY_LEVEL",
    "VALID_BODY_AUTH_PROTO",
    "VALID_BODY_PRIV_PROTO",
    "VALID_BODY_INTERFACE_SELECT_METHOD",
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