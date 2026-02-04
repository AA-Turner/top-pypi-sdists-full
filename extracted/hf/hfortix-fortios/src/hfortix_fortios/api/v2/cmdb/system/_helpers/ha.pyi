from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_MODE: Literal["standalone", "a-a", "a-p"]
VALID_BODY_SYNC_PACKET_BALANCE: Literal["enable", "disable"]
VALID_BODY_UNICAST_HB: Literal["enable", "disable"]
VALID_BODY_LOAD_BALANCE_ALL: Literal["enable", "disable"]
VALID_BODY_SYNC_CONFIG: Literal["enable", "disable"]
VALID_BODY_ENCRYPTION: Literal["enable", "disable"]
VALID_BODY_AUTHENTICATION: Literal["enable", "disable"]
VALID_BODY_HB_INTERVAL_IN_MILLISECONDS: Literal["100ms", "10ms"]
VALID_BODY_GRATUITOUS_ARPS: Literal["enable", "disable"]
VALID_BODY_SESSION_PICKUP: Literal["enable", "disable"]
VALID_BODY_SESSION_PICKUP_CONNECTIONLESS: Literal["enable", "disable"]
VALID_BODY_SESSION_PICKUP_EXPECTATION: Literal["enable", "disable"]
VALID_BODY_SESSION_PICKUP_NAT: Literal["enable", "disable"]
VALID_BODY_SESSION_PICKUP_DELAY: Literal["enable", "disable"]
VALID_BODY_LINK_FAILED_SIGNAL: Literal["enable", "disable"]
VALID_BODY_UPGRADE_MODE: Literal["simultaneous", "uninterruptible", "local-only", "secondary-only"]
VALID_BODY_STANDALONE_MGMT_VDOM: Literal["enable", "disable"]
VALID_BODY_HA_MGMT_STATUS: Literal["enable", "disable"]
VALID_BODY_STANDALONE_CONFIG_SYNC: Literal["enable", "disable"]
VALID_BODY_UNICAST_STATUS: Literal["enable", "disable"]
VALID_BODY_SCHEDULE: Literal["none", "leastconnection", "round-robin", "weight-round-robin", "random", "ip", "ipport"]
VALID_BODY_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_PINGSERVER_SECONDARY_FORCE_RESET: Literal["enable", "disable"]
VALID_BODY_VCLUSTER_STATUS: Literal["enable", "disable"]
VALID_BODY_HA_DIRECT: Literal["enable", "disable"]
VALID_BODY_SSD_FAILOVER: Literal["enable", "disable"]
VALID_BODY_MEMORY_COMPATIBLE_MODE: Literal["enable", "disable"]
VALID_BODY_MEMORY_BASED_FAILOVER: Literal["enable", "disable"]
VALID_BODY_CHECK_SECONDARY_DEV_HEALTH: Literal["enable", "disable"]
VALID_BODY_IPSEC_PHASE2_PROPOSAL: Literal["aes128-sha1", "aes128-sha256", "aes128-sha384", "aes128-sha512", "aes192-sha1", "aes192-sha256", "aes192-sha384", "aes192-sha512", "aes256-sha1", "aes256-sha256", "aes256-sha384", "aes256-sha512", "aes128gcm", "aes256gcm", "chacha20poly1305"]
VALID_BODY_BOUNCE_INTF_UPON_FAILOVER: Literal["enable", "disable"]

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
    "VALID_BODY_MODE",
    "VALID_BODY_SYNC_PACKET_BALANCE",
    "VALID_BODY_UNICAST_HB",
    "VALID_BODY_LOAD_BALANCE_ALL",
    "VALID_BODY_SYNC_CONFIG",
    "VALID_BODY_ENCRYPTION",
    "VALID_BODY_AUTHENTICATION",
    "VALID_BODY_HB_INTERVAL_IN_MILLISECONDS",
    "VALID_BODY_GRATUITOUS_ARPS",
    "VALID_BODY_SESSION_PICKUP",
    "VALID_BODY_SESSION_PICKUP_CONNECTIONLESS",
    "VALID_BODY_SESSION_PICKUP_EXPECTATION",
    "VALID_BODY_SESSION_PICKUP_NAT",
    "VALID_BODY_SESSION_PICKUP_DELAY",
    "VALID_BODY_LINK_FAILED_SIGNAL",
    "VALID_BODY_UPGRADE_MODE",
    "VALID_BODY_STANDALONE_MGMT_VDOM",
    "VALID_BODY_HA_MGMT_STATUS",
    "VALID_BODY_STANDALONE_CONFIG_SYNC",
    "VALID_BODY_UNICAST_STATUS",
    "VALID_BODY_SCHEDULE",
    "VALID_BODY_OVERRIDE",
    "VALID_BODY_PINGSERVER_SECONDARY_FORCE_RESET",
    "VALID_BODY_VCLUSTER_STATUS",
    "VALID_BODY_HA_DIRECT",
    "VALID_BODY_SSD_FAILOVER",
    "VALID_BODY_MEMORY_COMPATIBLE_MODE",
    "VALID_BODY_MEMORY_BASED_FAILOVER",
    "VALID_BODY_CHECK_SECONDARY_DEV_HEALTH",
    "VALID_BODY_IPSEC_PHASE2_PROPOSAL",
    "VALID_BODY_BOUNCE_INTF_UPON_FAILOVER",
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