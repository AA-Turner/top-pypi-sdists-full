from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_VDOM_TYPE: Literal["traffic", "lan-extension", "admin"]
VALID_BODY_OPMODE: Literal["nat", "transparent"]
VALID_BODY_NGFW_MODE: Literal["profile-based", "policy-based"]
VALID_BODY_HTTP_EXTERNAL_DEST: Literal["fortiweb", "forticache"]
VALID_BODY_FIREWALL_SESSION_DIRTY: Literal["check-all", "check-new", "check-policy-option"]
VALID_BODY_BFD: Literal["enable", "disable"]
VALID_BODY_BFD_DONT_ENFORCE_SRC_PORT: Literal["enable", "disable"]
VALID_BODY_UTF8_SPAM_TAGGING: Literal["enable", "disable"]
VALID_BODY_WCCP_CACHE_ENGINE: Literal["enable", "disable"]
VALID_BODY_VPN_STATS_LOG: Literal["ipsec", "pptp", "l2tp", "ssl"]
VALID_BODY_V4_ECMP_MODE: Literal["source-ip-based", "weight-based", "usage-based", "source-dest-ip-based"]
VALID_BODY_FW_SESSION_HAIRPIN: Literal["enable", "disable"]
VALID_BODY_PRP_TRAILER_ACTION: Literal["enable", "disable"]
VALID_BODY_SNAT_HAIRPIN_TRAFFIC: Literal["enable", "disable"]
VALID_BODY_DHCP_PROXY: Literal["enable", "disable"]
VALID_BODY_DHCP_PROXY_INTERFACE_SELECT_METHOD: Literal["auto", "sdwan", "specify"]
VALID_BODY_CENTRAL_NAT: Literal["enable", "disable"]
VALID_BODY_LLDP_RECEPTION: Literal["enable", "disable", "global"]
VALID_BODY_LLDP_TRANSMISSION: Literal["enable", "disable", "global"]
VALID_BODY_LINK_DOWN_ACCESS: Literal["enable", "disable"]
VALID_BODY_NAT46_GENERATE_IPV6_FRAGMENT_HEADER: Literal["enable", "disable"]
VALID_BODY_NAT46_FORCE_IPV4_PACKET_FORWARDING: Literal["enable", "disable"]
VALID_BODY_NAT64_FORCE_IPV6_PACKET_FORWARDING: Literal["enable", "disable"]
VALID_BODY_DETECT_UNKNOWN_ESP: Literal["enable", "disable"]
VALID_BODY_INTREE_SES_BEST_ROUTE: Literal["force", "disable"]
VALID_BODY_AUXILIARY_SESSION: Literal["enable", "disable"]
VALID_BODY_ASYMROUTE: Literal["enable", "disable"]
VALID_BODY_ASYMROUTE_ICMP: Literal["enable", "disable"]
VALID_BODY_TCP_SESSION_WITHOUT_SYN: Literal["enable", "disable"]
VALID_BODY_SES_DENIED_TRAFFIC: Literal["enable", "disable"]
VALID_BODY_SES_DENIED_MULTICAST_TRAFFIC: Literal["enable", "disable"]
VALID_BODY_STRICT_SRC_CHECK: Literal["enable", "disable"]
VALID_BODY_ALLOW_LINKDOWN_PATH: Literal["enable", "disable"]
VALID_BODY_ASYMROUTE6: Literal["enable", "disable"]
VALID_BODY_ASYMROUTE6_ICMP: Literal["enable", "disable"]
VALID_BODY_SCTP_SESSION_WITHOUT_INIT: Literal["enable", "disable"]
VALID_BODY_SIP_EXPECTATION: Literal["enable", "disable"]
VALID_BODY_SIP_NAT_TRACE: Literal["enable", "disable"]
VALID_BODY_H323_DIRECT_MODEL: Literal["disable", "enable"]
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_MULTICAST_FORWARD: Literal["enable", "disable"]
VALID_BODY_MULTICAST_TTL_NOTCHANGE: Literal["enable", "disable"]
VALID_BODY_MULTICAST_SKIP_POLICY: Literal["enable", "disable"]
VALID_BODY_ALLOW_SUBNET_OVERLAP: Literal["enable", "disable"]
VALID_BODY_DENY_TCP_WITH_ICMP: Literal["enable", "disable"]
VALID_BODY_EMAIL_PORTAL_CHECK_DNS: Literal["disable", "enable"]
VALID_BODY_DEFAULT_VOIP_ALG_MODE: Literal["proxy-based", "kernel-helper-based"]
VALID_BODY_GUI_ICAP: Literal["enable", "disable"]
VALID_BODY_GUI_IMPLICIT_POLICY: Literal["enable", "disable"]
VALID_BODY_GUI_DNS_DATABASE: Literal["enable", "disable"]
VALID_BODY_GUI_LOAD_BALANCE: Literal["enable", "disable"]
VALID_BODY_GUI_MULTICAST_POLICY: Literal["enable", "disable"]
VALID_BODY_GUI_DOS_POLICY: Literal["enable", "disable"]
VALID_BODY_GUI_OBJECT_COLORS: Literal["enable", "disable"]
VALID_BODY_GUI_ROUTE_TAG_ADDRESS_CREATION: Literal["enable", "disable"]
VALID_BODY_GUI_VOIP_PROFILE: Literal["enable", "disable"]
VALID_BODY_GUI_AP_PROFILE: Literal["enable", "disable"]
VALID_BODY_GUI_SECURITY_PROFILE_GROUP: Literal["enable", "disable"]
VALID_BODY_GUI_LOCAL_IN_POLICY: Literal["enable", "disable"]
VALID_BODY_GUI_WANOPT_CACHE: Literal["enable", "disable"]
VALID_BODY_GUI_EXPLICIT_PROXY: Literal["enable", "disable"]
VALID_BODY_GUI_DYNAMIC_ROUTING: Literal["enable", "disable"]
VALID_BODY_GUI_SSLVPN_PERSONAL_BOOKMARKS: Literal["enable", "disable"]
VALID_BODY_GUI_SSLVPN_REALMS: Literal["enable", "disable"]
VALID_BODY_GUI_POLICY_BASED_IPSEC: Literal["enable", "disable"]
VALID_BODY_GUI_THREAT_WEIGHT: Literal["enable", "disable"]
VALID_BODY_GUI_SPAMFILTER: Literal["enable", "disable"]
VALID_BODY_GUI_FILE_FILTER: Literal["enable", "disable"]
VALID_BODY_GUI_APPLICATION_CONTROL: Literal["enable", "disable"]
VALID_BODY_GUI_IPS: Literal["enable", "disable"]
VALID_BODY_GUI_DHCP_ADVANCED: Literal["enable", "disable"]
VALID_BODY_GUI_VPN: Literal["enable", "disable"]
VALID_BODY_GUI_SSLVPN: Literal["enable", "disable"]
VALID_BODY_GUI_WIRELESS_CONTROLLER: Literal["enable", "disable"]
VALID_BODY_GUI_ADVANCED_WIRELESS_FEATURES: Literal["enable", "disable"]
VALID_BODY_GUI_SWITCH_CONTROLLER: Literal["enable", "disable"]
VALID_BODY_GUI_FORTIAP_SPLIT_TUNNELING: Literal["enable", "disable"]
VALID_BODY_GUI_WEBFILTER_ADVANCED: Literal["enable", "disable"]
VALID_BODY_GUI_TRAFFIC_SHAPING: Literal["enable", "disable"]
VALID_BODY_GUI_WAN_LOAD_BALANCING: Literal["enable", "disable"]
VALID_BODY_GUI_ANTIVIRUS: Literal["enable", "disable"]
VALID_BODY_GUI_WEBFILTER: Literal["enable", "disable"]
VALID_BODY_GUI_VIDEOFILTER: Literal["enable", "disable"]
VALID_BODY_GUI_DNSFILTER: Literal["enable", "disable"]
VALID_BODY_GUI_WAF_PROFILE: Literal["enable", "disable"]
VALID_BODY_GUI_DLP_PROFILE: Literal["enable", "disable"]
VALID_BODY_GUI_DLP_ADVANCED: Literal["enable", "disable"]
VALID_BODY_GUI_VIRTUAL_PATCH_PROFILE: Literal["enable", "disable"]
VALID_BODY_GUI_CASB: Literal["enable", "disable"]
VALID_BODY_GUI_FORTIEXTENDER_CONTROLLER: Literal["enable", "disable"]
VALID_BODY_GUI_ADVANCED_POLICY: Literal["enable", "disable"]
VALID_BODY_GUI_ALLOW_UNNAMED_POLICY: Literal["enable", "disable"]
VALID_BODY_GUI_EMAIL_COLLECTION: Literal["enable", "disable"]
VALID_BODY_GUI_MULTIPLE_INTERFACE_POLICY: Literal["enable", "disable"]
VALID_BODY_GUI_POLICY_DISCLAIMER: Literal["enable", "disable"]
VALID_BODY_GUI_ZTNA: Literal["enable", "disable"]
VALID_BODY_GUI_OT: Literal["enable", "disable"]
VALID_BODY_GUI_DYNAMIC_DEVICE_OS_ID: Literal["enable", "disable"]
VALID_BODY_GUI_GTP: Literal["enable", "disable"]
VALID_BODY_IKE_SESSION_RESUME: Literal["enable", "disable"]
VALID_BODY_IKE_QUICK_CRASH_DETECT: Literal["enable", "disable"]
VALID_BODY_IKE_DN_FORMAT: Literal["with-space", "no-space"]
VALID_BODY_IKE_POLICY_ROUTE: Literal["enable", "disable"]
VALID_BODY_IKE_DETAILED_EVENT_LOGS: Literal["disable", "enable"]
VALID_BODY_BLOCK_LAND_ATTACK: Literal["disable", "enable"]
VALID_BODY_DEFAULT_APP_PORT_AS_SERVICE: Literal["enable", "disable"]
VALID_BODY_FQDN_SESSION_CHECK: Literal["enable", "disable"]
VALID_BODY_EXT_RESOURCE_SESSION_CHECK: Literal["enable", "disable"]
VALID_BODY_DYN_ADDR_SESSION_CHECK: Literal["enable", "disable"]
VALID_BODY_GUI_ENFORCE_CHANGE_SUMMARY: Literal["disable", "require", "optional"]
VALID_BODY_INTERNET_SERVICE_DATABASE_CACHE: Literal["disable", "enable"]

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
    "VALID_BODY_VDOM_TYPE",
    "VALID_BODY_OPMODE",
    "VALID_BODY_NGFW_MODE",
    "VALID_BODY_HTTP_EXTERNAL_DEST",
    "VALID_BODY_FIREWALL_SESSION_DIRTY",
    "VALID_BODY_BFD",
    "VALID_BODY_BFD_DONT_ENFORCE_SRC_PORT",
    "VALID_BODY_UTF8_SPAM_TAGGING",
    "VALID_BODY_WCCP_CACHE_ENGINE",
    "VALID_BODY_VPN_STATS_LOG",
    "VALID_BODY_V4_ECMP_MODE",
    "VALID_BODY_FW_SESSION_HAIRPIN",
    "VALID_BODY_PRP_TRAILER_ACTION",
    "VALID_BODY_SNAT_HAIRPIN_TRAFFIC",
    "VALID_BODY_DHCP_PROXY",
    "VALID_BODY_DHCP_PROXY_INTERFACE_SELECT_METHOD",
    "VALID_BODY_CENTRAL_NAT",
    "VALID_BODY_LLDP_RECEPTION",
    "VALID_BODY_LLDP_TRANSMISSION",
    "VALID_BODY_LINK_DOWN_ACCESS",
    "VALID_BODY_NAT46_GENERATE_IPV6_FRAGMENT_HEADER",
    "VALID_BODY_NAT46_FORCE_IPV4_PACKET_FORWARDING",
    "VALID_BODY_NAT64_FORCE_IPV6_PACKET_FORWARDING",
    "VALID_BODY_DETECT_UNKNOWN_ESP",
    "VALID_BODY_INTREE_SES_BEST_ROUTE",
    "VALID_BODY_AUXILIARY_SESSION",
    "VALID_BODY_ASYMROUTE",
    "VALID_BODY_ASYMROUTE_ICMP",
    "VALID_BODY_TCP_SESSION_WITHOUT_SYN",
    "VALID_BODY_SES_DENIED_TRAFFIC",
    "VALID_BODY_SES_DENIED_MULTICAST_TRAFFIC",
    "VALID_BODY_STRICT_SRC_CHECK",
    "VALID_BODY_ALLOW_LINKDOWN_PATH",
    "VALID_BODY_ASYMROUTE6",
    "VALID_BODY_ASYMROUTE6_ICMP",
    "VALID_BODY_SCTP_SESSION_WITHOUT_INIT",
    "VALID_BODY_SIP_EXPECTATION",
    "VALID_BODY_SIP_NAT_TRACE",
    "VALID_BODY_H323_DIRECT_MODEL",
    "VALID_BODY_STATUS",
    "VALID_BODY_MULTICAST_FORWARD",
    "VALID_BODY_MULTICAST_TTL_NOTCHANGE",
    "VALID_BODY_MULTICAST_SKIP_POLICY",
    "VALID_BODY_ALLOW_SUBNET_OVERLAP",
    "VALID_BODY_DENY_TCP_WITH_ICMP",
    "VALID_BODY_EMAIL_PORTAL_CHECK_DNS",
    "VALID_BODY_DEFAULT_VOIP_ALG_MODE",
    "VALID_BODY_GUI_ICAP",
    "VALID_BODY_GUI_IMPLICIT_POLICY",
    "VALID_BODY_GUI_DNS_DATABASE",
    "VALID_BODY_GUI_LOAD_BALANCE",
    "VALID_BODY_GUI_MULTICAST_POLICY",
    "VALID_BODY_GUI_DOS_POLICY",
    "VALID_BODY_GUI_OBJECT_COLORS",
    "VALID_BODY_GUI_ROUTE_TAG_ADDRESS_CREATION",
    "VALID_BODY_GUI_VOIP_PROFILE",
    "VALID_BODY_GUI_AP_PROFILE",
    "VALID_BODY_GUI_SECURITY_PROFILE_GROUP",
    "VALID_BODY_GUI_LOCAL_IN_POLICY",
    "VALID_BODY_GUI_WANOPT_CACHE",
    "VALID_BODY_GUI_EXPLICIT_PROXY",
    "VALID_BODY_GUI_DYNAMIC_ROUTING",
    "VALID_BODY_GUI_SSLVPN_PERSONAL_BOOKMARKS",
    "VALID_BODY_GUI_SSLVPN_REALMS",
    "VALID_BODY_GUI_POLICY_BASED_IPSEC",
    "VALID_BODY_GUI_THREAT_WEIGHT",
    "VALID_BODY_GUI_SPAMFILTER",
    "VALID_BODY_GUI_FILE_FILTER",
    "VALID_BODY_GUI_APPLICATION_CONTROL",
    "VALID_BODY_GUI_IPS",
    "VALID_BODY_GUI_DHCP_ADVANCED",
    "VALID_BODY_GUI_VPN",
    "VALID_BODY_GUI_SSLVPN",
    "VALID_BODY_GUI_WIRELESS_CONTROLLER",
    "VALID_BODY_GUI_ADVANCED_WIRELESS_FEATURES",
    "VALID_BODY_GUI_SWITCH_CONTROLLER",
    "VALID_BODY_GUI_FORTIAP_SPLIT_TUNNELING",
    "VALID_BODY_GUI_WEBFILTER_ADVANCED",
    "VALID_BODY_GUI_TRAFFIC_SHAPING",
    "VALID_BODY_GUI_WAN_LOAD_BALANCING",
    "VALID_BODY_GUI_ANTIVIRUS",
    "VALID_BODY_GUI_WEBFILTER",
    "VALID_BODY_GUI_VIDEOFILTER",
    "VALID_BODY_GUI_DNSFILTER",
    "VALID_BODY_GUI_WAF_PROFILE",
    "VALID_BODY_GUI_DLP_PROFILE",
    "VALID_BODY_GUI_DLP_ADVANCED",
    "VALID_BODY_GUI_VIRTUAL_PATCH_PROFILE",
    "VALID_BODY_GUI_CASB",
    "VALID_BODY_GUI_FORTIEXTENDER_CONTROLLER",
    "VALID_BODY_GUI_ADVANCED_POLICY",
    "VALID_BODY_GUI_ALLOW_UNNAMED_POLICY",
    "VALID_BODY_GUI_EMAIL_COLLECTION",
    "VALID_BODY_GUI_MULTIPLE_INTERFACE_POLICY",
    "VALID_BODY_GUI_POLICY_DISCLAIMER",
    "VALID_BODY_GUI_ZTNA",
    "VALID_BODY_GUI_OT",
    "VALID_BODY_GUI_DYNAMIC_DEVICE_OS_ID",
    "VALID_BODY_GUI_GTP",
    "VALID_BODY_IKE_SESSION_RESUME",
    "VALID_BODY_IKE_QUICK_CRASH_DETECT",
    "VALID_BODY_IKE_DN_FORMAT",
    "VALID_BODY_IKE_POLICY_ROUTE",
    "VALID_BODY_IKE_DETAILED_EVENT_LOGS",
    "VALID_BODY_BLOCK_LAND_ATTACK",
    "VALID_BODY_DEFAULT_APP_PORT_AS_SERVICE",
    "VALID_BODY_FQDN_SESSION_CHECK",
    "VALID_BODY_EXT_RESOURCE_SESSION_CHECK",
    "VALID_BODY_DYN_ADDR_SESSION_CHECK",
    "VALID_BODY_GUI_ENFORCE_CHANGE_SUMMARY",
    "VALID_BODY_INTERNET_SERVICE_DATABASE_CACHE",
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