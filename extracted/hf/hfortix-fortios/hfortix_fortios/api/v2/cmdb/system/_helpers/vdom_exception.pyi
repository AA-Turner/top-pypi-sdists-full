from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_OBJECT: Literal["log.fortianalyzer.setting", "log.fortianalyzer.override-setting", "log.fortianalyzer2.setting", "log.fortianalyzer2.override-setting", "log.fortianalyzer3.setting", "log.fortianalyzer3.override-setting", "log.fortianalyzer-cloud.setting", "log.fortianalyzer-cloud.override-setting", "log.syslogd.setting", "log.syslogd.override-setting", "log.syslogd2.setting", "log.syslogd2.override-setting", "log.syslogd3.setting", "log.syslogd3.override-setting", "log.syslogd4.setting", "log.syslogd4.override-setting", "system.gre-tunnel", "system.central-management", "system.csf", "user.radius", "system.interface", "vpn.ipsec.phase1-interface", "vpn.ipsec.phase2-interface", "router.bgp", "router.route-map", "router.prefix-list", "firewall.ippool", "firewall.ippool6", "router.static", "router.static6", "firewall.vip", "firewall.vip6", "system.sdwan", "system.saml", "router.policy", "router.policy6", "log.syslogd.setting", "log.syslogd.override-setting", "firewall.address"]
VALID_BODY_SCOPE: Literal["all", "inclusive", "exclusive"]

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
    "VALID_BODY_OBJECT",
    "VALID_BODY_SCOPE",
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