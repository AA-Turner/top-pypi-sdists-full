from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_ACTION: Literal["accept", "deny", "ipsec"]
VALID_BODY_NAT64: Literal["enable", "disable"]
VALID_BODY_NAT46: Literal["enable", "disable"]
VALID_BODY_ZTNA_STATUS: Literal["enable", "disable"]
VALID_BODY_ZTNA_DEVICE_OWNERSHIP: Literal["enable", "disable"]
VALID_BODY_ZTNA_TAGS_MATCH_LOGIC: Literal["or", "and"]
VALID_BODY_INTERNET_SERVICE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE_SRC: Literal["enable", "disable"]
VALID_BODY_REPUTATION_DIRECTION: Literal["source", "destination"]
VALID_BODY_INTERNET_SERVICE6: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE6_SRC: Literal["enable", "disable"]
VALID_BODY_REPUTATION_DIRECTION6: Literal["source", "destination"]
VALID_BODY_RTP_NAT: Literal["disable", "enable"]
VALID_BODY_SEND_DENY_PACKET: Literal["disable", "enable"]
VALID_BODY_FIREWALL_SESSION_DIRTY: Literal["check-all", "check-new"]
VALID_BODY_SCHEDULE_TIMEOUT: Literal["enable", "disable"]
VALID_BODY_POLICY_EXPIRY: Literal["enable", "disable"]
VALID_BODY_TOS_NEGATE: Literal["enable", "disable"]
VALID_BODY_ANTI_REPLAY: Literal["enable", "disable"]
VALID_BODY_TCP_SESSION_WITHOUT_SYN: Literal["all", "data-only", "disable"]
VALID_BODY_GEOIP_ANYCAST: Literal["enable", "disable"]
VALID_BODY_GEOIP_MATCH: Literal["physical-location", "registered-location"]
VALID_BODY_DYNAMIC_SHAPING: Literal["enable", "disable"]
VALID_BODY_PASSIVE_WAN_HEALTH_MEASUREMENT: Literal["enable", "disable"]
VALID_BODY_APP_MONITOR: Literal["enable", "disable"]
VALID_BODY_UTM_STATUS: Literal["enable", "disable"]
VALID_BODY_INSPECTION_MODE: Literal["proxy", "flow"]
VALID_BODY_HTTP_POLICY_REDIRECT: Literal["enable", "disable", "legacy"]
VALID_BODY_SSH_POLICY_REDIRECT: Literal["enable", "disable"]
VALID_BODY_ZTNA_POLICY_REDIRECT: Literal["enable", "disable"]
VALID_BODY_PROFILE_TYPE: Literal["single", "group"]
VALID_BODY_LOGTRAFFIC: Literal["all", "utm", "disable"]
VALID_BODY_LOGTRAFFIC_START: Literal["enable", "disable"]
VALID_BODY_LOG_HTTP_TRANSACTION: Literal["enable", "disable"]
VALID_BODY_CAPTURE_PACKET: Literal["enable", "disable"]
VALID_BODY_AUTO_ASIC_OFFLOAD: Literal["enable", "disable"]
VALID_BODY_WANOPT: Literal["enable", "disable"]
VALID_BODY_WANOPT_DETECTION: Literal["active", "passive", "off"]
VALID_BODY_WANOPT_PASSIVE_OPT: Literal["default", "transparent", "non-transparent"]
VALID_BODY_WEBCACHE: Literal["enable", "disable"]
VALID_BODY_WEBCACHE_HTTPS: Literal["disable", "enable"]
VALID_BODY_NAT: Literal["enable", "disable"]
VALID_BODY_PCP_OUTBOUND: Literal["enable", "disable"]
VALID_BODY_PCP_INBOUND: Literal["enable", "disable"]
VALID_BODY_PERMIT_ANY_HOST: Literal["enable", "disable"]
VALID_BODY_PERMIT_STUN_HOST: Literal["enable", "disable"]
VALID_BODY_FIXEDPORT: Literal["enable", "disable"]
VALID_BODY_PORT_PRESERVE: Literal["enable", "disable"]
VALID_BODY_PORT_RANDOM: Literal["enable", "disable"]
VALID_BODY_IPPOOL: Literal["enable", "disable"]
VALID_BODY_INBOUND: Literal["enable", "disable"]
VALID_BODY_OUTBOUND: Literal["enable", "disable"]
VALID_BODY_NATINBOUND: Literal["enable", "disable"]
VALID_BODY_NATOUTBOUND: Literal["enable", "disable"]
VALID_BODY_FEC: Literal["enable", "disable"]
VALID_BODY_WCCP: Literal["enable", "disable"]
VALID_BODY_NTLM: Literal["enable", "disable"]
VALID_BODY_NTLM_GUEST: Literal["enable", "disable"]
VALID_BODY_AUTH_PATH: Literal["enable", "disable"]
VALID_BODY_DISCLAIMER: Literal["enable", "disable"]
VALID_BODY_EMAIL_COLLECT: Literal["enable", "disable"]
VALID_BODY_MATCH_VIP: Literal["enable", "disable"]
VALID_BODY_MATCH_VIP_ONLY: Literal["enable", "disable"]
VALID_BODY_DIFFSERV_COPY: Literal["enable", "disable"]
VALID_BODY_DIFFSERV_FORWARD: Literal["enable", "disable"]
VALID_BODY_DIFFSERV_REVERSE: Literal["enable", "disable"]
VALID_BODY_BLOCK_NOTIFICATION: Literal["enable", "disable"]
VALID_BODY_SRCADDR_NEGATE: Literal["enable", "disable"]
VALID_BODY_SRCADDR6_NEGATE: Literal["enable", "disable"]
VALID_BODY_DSTADDR_NEGATE: Literal["enable", "disable"]
VALID_BODY_DSTADDR6_NEGATE: Literal["enable", "disable"]
VALID_BODY_ZTNA_EMS_TAG_NEGATE: Literal["enable", "disable"]
VALID_BODY_SERVICE_NEGATE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE_NEGATE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE_SRC_NEGATE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE6_NEGATE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE: Literal["enable", "disable"]
VALID_BODY_TIMEOUT_SEND_RST: Literal["enable", "disable"]
VALID_BODY_CAPTIVE_PORTAL_EXEMPT: Literal["enable", "disable"]
VALID_BODY_DSRI: Literal["enable", "disable"]
VALID_BODY_RADIUS_MAC_AUTH_BYPASS: Literal["enable", "disable"]
VALID_BODY_RADIUS_IP_AUTH_BYPASS: Literal["enable", "disable"]
VALID_BODY_DELAY_TCP_NPU_SESSION: Literal["enable", "disable"]
VALID_BODY_SGT_CHECK: Literal["enable", "disable"]

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
    "VALID_BODY_ACTION",
    "VALID_BODY_NAT64",
    "VALID_BODY_NAT46",
    "VALID_BODY_ZTNA_STATUS",
    "VALID_BODY_ZTNA_DEVICE_OWNERSHIP",
    "VALID_BODY_ZTNA_TAGS_MATCH_LOGIC",
    "VALID_BODY_INTERNET_SERVICE",
    "VALID_BODY_INTERNET_SERVICE_SRC",
    "VALID_BODY_REPUTATION_DIRECTION",
    "VALID_BODY_INTERNET_SERVICE6",
    "VALID_BODY_INTERNET_SERVICE6_SRC",
    "VALID_BODY_REPUTATION_DIRECTION6",
    "VALID_BODY_RTP_NAT",
    "VALID_BODY_SEND_DENY_PACKET",
    "VALID_BODY_FIREWALL_SESSION_DIRTY",
    "VALID_BODY_SCHEDULE_TIMEOUT",
    "VALID_BODY_POLICY_EXPIRY",
    "VALID_BODY_TOS_NEGATE",
    "VALID_BODY_ANTI_REPLAY",
    "VALID_BODY_TCP_SESSION_WITHOUT_SYN",
    "VALID_BODY_GEOIP_ANYCAST",
    "VALID_BODY_GEOIP_MATCH",
    "VALID_BODY_DYNAMIC_SHAPING",
    "VALID_BODY_PASSIVE_WAN_HEALTH_MEASUREMENT",
    "VALID_BODY_APP_MONITOR",
    "VALID_BODY_UTM_STATUS",
    "VALID_BODY_INSPECTION_MODE",
    "VALID_BODY_HTTP_POLICY_REDIRECT",
    "VALID_BODY_SSH_POLICY_REDIRECT",
    "VALID_BODY_ZTNA_POLICY_REDIRECT",
    "VALID_BODY_PROFILE_TYPE",
    "VALID_BODY_LOGTRAFFIC",
    "VALID_BODY_LOGTRAFFIC_START",
    "VALID_BODY_LOG_HTTP_TRANSACTION",
    "VALID_BODY_CAPTURE_PACKET",
    "VALID_BODY_AUTO_ASIC_OFFLOAD",
    "VALID_BODY_WANOPT",
    "VALID_BODY_WANOPT_DETECTION",
    "VALID_BODY_WANOPT_PASSIVE_OPT",
    "VALID_BODY_WEBCACHE",
    "VALID_BODY_WEBCACHE_HTTPS",
    "VALID_BODY_NAT",
    "VALID_BODY_PCP_OUTBOUND",
    "VALID_BODY_PCP_INBOUND",
    "VALID_BODY_PERMIT_ANY_HOST",
    "VALID_BODY_PERMIT_STUN_HOST",
    "VALID_BODY_FIXEDPORT",
    "VALID_BODY_PORT_PRESERVE",
    "VALID_BODY_PORT_RANDOM",
    "VALID_BODY_IPPOOL",
    "VALID_BODY_INBOUND",
    "VALID_BODY_OUTBOUND",
    "VALID_BODY_NATINBOUND",
    "VALID_BODY_NATOUTBOUND",
    "VALID_BODY_FEC",
    "VALID_BODY_WCCP",
    "VALID_BODY_NTLM",
    "VALID_BODY_NTLM_GUEST",
    "VALID_BODY_AUTH_PATH",
    "VALID_BODY_DISCLAIMER",
    "VALID_BODY_EMAIL_COLLECT",
    "VALID_BODY_MATCH_VIP",
    "VALID_BODY_MATCH_VIP_ONLY",
    "VALID_BODY_DIFFSERV_COPY",
    "VALID_BODY_DIFFSERV_FORWARD",
    "VALID_BODY_DIFFSERV_REVERSE",
    "VALID_BODY_BLOCK_NOTIFICATION",
    "VALID_BODY_SRCADDR_NEGATE",
    "VALID_BODY_SRCADDR6_NEGATE",
    "VALID_BODY_DSTADDR_NEGATE",
    "VALID_BODY_DSTADDR6_NEGATE",
    "VALID_BODY_ZTNA_EMS_TAG_NEGATE",
    "VALID_BODY_SERVICE_NEGATE",
    "VALID_BODY_INTERNET_SERVICE_NEGATE",
    "VALID_BODY_INTERNET_SERVICE_SRC_NEGATE",
    "VALID_BODY_INTERNET_SERVICE6_NEGATE",
    "VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE",
    "VALID_BODY_TIMEOUT_SEND_RST",
    "VALID_BODY_CAPTIVE_PORTAL_EXEMPT",
    "VALID_BODY_DSRI",
    "VALID_BODY_RADIUS_MAC_AUTH_BYPASS",
    "VALID_BODY_RADIUS_IP_AUTH_BYPASS",
    "VALID_BODY_DELAY_TCP_NPU_SESSION",
    "VALID_BODY_SGT_CHECK",
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