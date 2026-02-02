from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_FORTILINK: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_SOURCE_IP: Literal["outbound", "fixed"]
VALID_BODY_MODE: Literal["static", "dhcp", "pppoe"]
VALID_BODY_DHCP_RELAY_INTERFACE_SELECT_METHOD: Literal["auto", "sdwan", "specify"]
VALID_BODY_DHCP_BROADCAST_FLAG: Literal["disable", "enable"]
VALID_BODY_DHCP_RELAY_SERVICE: Literal["disable", "enable"]
VALID_BODY_DHCP_RELAY_REQUEST_ALL_SERVER: Literal["disable", "enable"]
VALID_BODY_DHCP_RELAY_ALLOW_NO_END_OPTION: Literal["disable", "enable"]
VALID_BODY_DHCP_RELAY_TYPE: Literal["regular", "ipsec"]
VALID_BODY_DHCP_SMART_RELAY: Literal["disable", "enable"]
VALID_BODY_DHCP_RELAY_AGENT_OPTION: Literal["enable", "disable"]
VALID_BODY_DHCP_CLASSLESS_ROUTE_ADDITION: Literal["enable", "disable"]
VALID_BODY_ALLOWACCESS: Literal["ping", "https", "ssh", "snmp", "http", "telnet", "fgfm", "radius-acct", "probe-response", "fabric", "ftm", "speed-test", "scim"]
VALID_BODY_GWDETECT: Literal["enable", "disable"]
VALID_BODY_DETECTPROTOCOL: Literal["ping", "tcp-echo", "udp-echo"]
VALID_BODY_FAIL_DETECT: Literal["enable", "disable"]
VALID_BODY_FAIL_DETECT_OPTION: Literal["detectserver", "link-down"]
VALID_BODY_FAIL_ALERT_METHOD: Literal["link-failed-signal", "link-down"]
VALID_BODY_FAIL_ACTION_ON_EXTENDER: Literal["soft-restart", "hard-restart", "reboot"]
VALID_BODY_PPPOE_EGRESS_COS: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]
VALID_BODY_PPPOE_UNNUMBERED_NEGOTIATE: Literal["enable", "disable"]
VALID_BODY_MULTILINK: Literal["enable", "disable"]
VALID_BODY_DEFAULTGW: Literal["enable", "disable"]
VALID_BODY_DNS_SERVER_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_DNS_SERVER_PROTOCOL: Literal["cleartext", "dot", "doh"]
VALID_BODY_AUTH_TYPE: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
VALID_BODY_PPTP_CLIENT: Literal["enable", "disable"]
VALID_BODY_PPTP_AUTH_TYPE: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
VALID_BODY_ARPFORWARD: Literal["enable", "disable"]
VALID_BODY_NDISCFORWARD: Literal["enable", "disable"]
VALID_BODY_BROADCAST_FORWARD: Literal["enable", "disable"]
VALID_BODY_BFD: Literal["global", "enable", "disable"]
VALID_BODY_L2FORWARD: Literal["enable", "disable"]
VALID_BODY_ICMP_SEND_REDIRECT: Literal["enable", "disable"]
VALID_BODY_ICMP_ACCEPT_REDIRECT: Literal["enable", "disable"]
VALID_BODY_VLANFORWARD: Literal["enable", "disable"]
VALID_BODY_STPFORWARD: Literal["enable", "disable"]
VALID_BODY_STPFORWARD_MODE: Literal["rpl-all-ext-id", "rpl-bridge-ext-id", "rpl-nothing"]
VALID_BODY_IPS_SNIFFER_MODE: Literal["enable", "disable"]
VALID_BODY_IDENT_ACCEPT: Literal["enable", "disable"]
VALID_BODY_IPMAC: Literal["enable", "disable"]
VALID_BODY_SUBST: Literal["enable", "disable"]
VALID_BODY_SPEED: Literal["auto", "10full", "10half", "100full", "100half", "100auto", "1000full", "1000auto"]
VALID_BODY_STATUS: Literal["up", "down"]
VALID_BODY_NETBIOS_FORWARD: Literal["disable", "enable"]
VALID_BODY_TYPE: Literal["physical", "vlan", "aggregate", "redundant", "tunnel", "vdom-link", "loopback", "switch", "vap-switch", "wl-mesh", "fext-wan", "vxlan", "geneve", "switch-vlan", "emac-vlan", "lan-extension"]
VALID_BODY_DEDICATED_TO: Literal["none", "management"]
VALID_BODY_WCCP: Literal["enable", "disable"]
VALID_BODY_NETFLOW_SAMPLER: Literal["disable", "tx", "rx", "both"]
VALID_BODY_SFLOW_SAMPLER: Literal["enable", "disable"]
VALID_BODY_DROP_FRAGMENT: Literal["enable", "disable"]
VALID_BODY_SRC_CHECK: Literal["enable", "disable"]
VALID_BODY_SAMPLE_DIRECTION: Literal["tx", "rx", "both"]
VALID_BODY_EXPLICIT_WEB_PROXY: Literal["enable", "disable"]
VALID_BODY_EXPLICIT_FTP_PROXY: Literal["enable", "disable"]
VALID_BODY_PROXY_CAPTIVE_PORTAL: Literal["enable", "disable"]
VALID_BODY_EXTERNAL: Literal["enable", "disable"]
VALID_BODY_MTU_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_VLAN_PROTOCOL: Literal["8021q", "8021ad"]
VALID_BODY_LACP_MODE: Literal["static", "passive", "active"]
VALID_BODY_LACP_HA_SECONDARY: Literal["enable", "disable"]
VALID_BODY_SYSTEM_ID_TYPE: Literal["auto", "user"]
VALID_BODY_LACP_SPEED: Literal["slow", "fast"]
VALID_BODY_MIN_LINKS_DOWN: Literal["operational", "administrative"]
VALID_BODY_ALGORITHM: Literal["L2", "L3", "L4", "NPU-GRE", "Source-MAC"]
VALID_BODY_AGGREGATE_TYPE: Literal["physical", "vxlan"]
VALID_BODY_PRIORITY_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_SECURITY_MODE: Literal["none", "captive-portal", "802.1X"]
VALID_BODY_SECURITY_MAC_AUTH_BYPASS: Literal["mac-auth-only", "enable", "disable"]
VALID_BODY_SECURITY_IP_AUTH_BYPASS: Literal["enable", "disable"]
VALID_BODY_DEVICE_IDENTIFICATION: Literal["enable", "disable"]
VALID_BODY_EXCLUDE_SIGNATURES: Literal["iot", "ot"]
VALID_BODY_DEVICE_USER_IDENTIFICATION: Literal["enable", "disable"]
VALID_BODY_LLDP_RECEPTION: Literal["enable", "disable", "vdom"]
VALID_BODY_LLDP_TRANSMISSION: Literal["enable", "disable", "vdom"]
VALID_BODY_MONITOR_BANDWIDTH: Literal["enable", "disable"]
VALID_BODY_VRRP_VIRTUAL_MAC: Literal["enable", "disable"]
VALID_BODY_ROLE: Literal["lan", "wan", "dmz", "undefined"]
VALID_BODY_SECONDARY_IP: Literal["enable", "disable"]
VALID_BODY_PRESERVE_SESSION_ROUTE: Literal["enable", "disable"]
VALID_BODY_AUTO_AUTH_EXTENSION_DEVICE: Literal["enable", "disable"]
VALID_BODY_AP_DISCOVER: Literal["enable", "disable"]
VALID_BODY_FORTILINK_NEIGHBOR_DETECT: Literal["lldp", "fortilink"]
VALID_BODY_IP_MANAGED_BY_FORTIIPAM: Literal["inherit-global", "enable", "disable"]
VALID_BODY_MANAGED_SUBNETWORK_SIZE: Literal["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32768", "65536", "131072", "262144", "524288", "1048576", "2097152", "4194304", "8388608", "16777216"]
VALID_BODY_FORTILINK_SPLIT_INTERFACE: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_ACCESS_VLAN: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_RSPAN_MODE: Literal["disable", "enable"]
VALID_BODY_SWITCH_CONTROLLER_NETFLOW_COLLECT: Literal["disable", "enable"]
VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_PROXY: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_FAST_LEAVE: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_VERIFY_MAC: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_OPTION82: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_ARP_INSPECTION: Literal["enable", "disable", "monitor"]
VALID_BODY_SWITCH_CONTROLLER_FEATURE: Literal["none", "default-vlan", "quarantine", "rspan", "voice", "video", "nac", "nac-segment"]
VALID_BODY_SWITCH_CONTROLLER_IOT_SCANNING: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_OFFLOAD: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_OFFLOAD_GW: Literal["enable", "disable"]
VALID_BODY_EAP_SUPPLICANT: Literal["enable", "disable"]
VALID_BODY_EAP_METHOD: Literal["tls", "peap"]
VALID_BODY_DEFAULT_PURDUE_LEVEL: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]

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
    "VALID_BODY_FORTILINK",
    "VALID_BODY_SWITCH_CONTROLLER_SOURCE_IP",
    "VALID_BODY_MODE",
    "VALID_BODY_DHCP_RELAY_INTERFACE_SELECT_METHOD",
    "VALID_BODY_DHCP_BROADCAST_FLAG",
    "VALID_BODY_DHCP_RELAY_SERVICE",
    "VALID_BODY_DHCP_RELAY_REQUEST_ALL_SERVER",
    "VALID_BODY_DHCP_RELAY_ALLOW_NO_END_OPTION",
    "VALID_BODY_DHCP_RELAY_TYPE",
    "VALID_BODY_DHCP_SMART_RELAY",
    "VALID_BODY_DHCP_RELAY_AGENT_OPTION",
    "VALID_BODY_DHCP_CLASSLESS_ROUTE_ADDITION",
    "VALID_BODY_ALLOWACCESS",
    "VALID_BODY_GWDETECT",
    "VALID_BODY_DETECTPROTOCOL",
    "VALID_BODY_FAIL_DETECT",
    "VALID_BODY_FAIL_DETECT_OPTION",
    "VALID_BODY_FAIL_ALERT_METHOD",
    "VALID_BODY_FAIL_ACTION_ON_EXTENDER",
    "VALID_BODY_PPPOE_EGRESS_COS",
    "VALID_BODY_PPPOE_UNNUMBERED_NEGOTIATE",
    "VALID_BODY_MULTILINK",
    "VALID_BODY_DEFAULTGW",
    "VALID_BODY_DNS_SERVER_OVERRIDE",
    "VALID_BODY_DNS_SERVER_PROTOCOL",
    "VALID_BODY_AUTH_TYPE",
    "VALID_BODY_PPTP_CLIENT",
    "VALID_BODY_PPTP_AUTH_TYPE",
    "VALID_BODY_ARPFORWARD",
    "VALID_BODY_NDISCFORWARD",
    "VALID_BODY_BROADCAST_FORWARD",
    "VALID_BODY_BFD",
    "VALID_BODY_L2FORWARD",
    "VALID_BODY_ICMP_SEND_REDIRECT",
    "VALID_BODY_ICMP_ACCEPT_REDIRECT",
    "VALID_BODY_VLANFORWARD",
    "VALID_BODY_STPFORWARD",
    "VALID_BODY_STPFORWARD_MODE",
    "VALID_BODY_IPS_SNIFFER_MODE",
    "VALID_BODY_IDENT_ACCEPT",
    "VALID_BODY_IPMAC",
    "VALID_BODY_SUBST",
    "VALID_BODY_SPEED",
    "VALID_BODY_STATUS",
    "VALID_BODY_NETBIOS_FORWARD",
    "VALID_BODY_TYPE",
    "VALID_BODY_DEDICATED_TO",
    "VALID_BODY_WCCP",
    "VALID_BODY_NETFLOW_SAMPLER",
    "VALID_BODY_SFLOW_SAMPLER",
    "VALID_BODY_DROP_FRAGMENT",
    "VALID_BODY_SRC_CHECK",
    "VALID_BODY_SAMPLE_DIRECTION",
    "VALID_BODY_EXPLICIT_WEB_PROXY",
    "VALID_BODY_EXPLICIT_FTP_PROXY",
    "VALID_BODY_PROXY_CAPTIVE_PORTAL",
    "VALID_BODY_EXTERNAL",
    "VALID_BODY_MTU_OVERRIDE",
    "VALID_BODY_VLAN_PROTOCOL",
    "VALID_BODY_LACP_MODE",
    "VALID_BODY_LACP_HA_SECONDARY",
    "VALID_BODY_SYSTEM_ID_TYPE",
    "VALID_BODY_LACP_SPEED",
    "VALID_BODY_MIN_LINKS_DOWN",
    "VALID_BODY_ALGORITHM",
    "VALID_BODY_AGGREGATE_TYPE",
    "VALID_BODY_PRIORITY_OVERRIDE",
    "VALID_BODY_SECURITY_MODE",
    "VALID_BODY_SECURITY_MAC_AUTH_BYPASS",
    "VALID_BODY_SECURITY_IP_AUTH_BYPASS",
    "VALID_BODY_DEVICE_IDENTIFICATION",
    "VALID_BODY_EXCLUDE_SIGNATURES",
    "VALID_BODY_DEVICE_USER_IDENTIFICATION",
    "VALID_BODY_LLDP_RECEPTION",
    "VALID_BODY_LLDP_TRANSMISSION",
    "VALID_BODY_MONITOR_BANDWIDTH",
    "VALID_BODY_VRRP_VIRTUAL_MAC",
    "VALID_BODY_ROLE",
    "VALID_BODY_SECONDARY_IP",
    "VALID_BODY_PRESERVE_SESSION_ROUTE",
    "VALID_BODY_AUTO_AUTH_EXTENSION_DEVICE",
    "VALID_BODY_AP_DISCOVER",
    "VALID_BODY_FORTILINK_NEIGHBOR_DETECT",
    "VALID_BODY_IP_MANAGED_BY_FORTIIPAM",
    "VALID_BODY_MANAGED_SUBNETWORK_SIZE",
    "VALID_BODY_FORTILINK_SPLIT_INTERFACE",
    "VALID_BODY_SWITCH_CONTROLLER_ACCESS_VLAN",
    "VALID_BODY_SWITCH_CONTROLLER_RSPAN_MODE",
    "VALID_BODY_SWITCH_CONTROLLER_NETFLOW_COLLECT",
    "VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING",
    "VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_PROXY",
    "VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_FAST_LEAVE",
    "VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING",
    "VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_VERIFY_MAC",
    "VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_OPTION82",
    "VALID_BODY_SWITCH_CONTROLLER_ARP_INSPECTION",
    "VALID_BODY_SWITCH_CONTROLLER_FEATURE",
    "VALID_BODY_SWITCH_CONTROLLER_IOT_SCANNING",
    "VALID_BODY_SWITCH_CONTROLLER_OFFLOAD",
    "VALID_BODY_SWITCH_CONTROLLER_OFFLOAD_GW",
    "VALID_BODY_EAP_SUPPLICANT",
    "VALID_BODY_EAP_METHOD",
    "VALID_BODY_DEFAULT_PURDUE_LEVEL",
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