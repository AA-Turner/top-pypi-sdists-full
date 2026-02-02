from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_PRE_AUTH: Literal["enable", "disable"]
VALID_BODY_EXTERNAL_PRE_AUTH: Literal["enable", "disable"]
VALID_BODY_MESH_BACKHAUL: Literal["enable", "disable"]
VALID_BODY_BROADCAST_SSID: Literal["enable", "disable"]
VALID_BODY_SECURITY: Literal["open", "wep64", "wep128", "wpa-personal", "wpa-enterprise", "wpa-only-personal", "wpa-only-enterprise", "wpa2-only-personal", "wpa2-only-enterprise", "wpa3-enterprise", "wpa3-only-enterprise", "wpa3-enterprise-transition", "wpa3-sae", "wpa3-sae-transition", "owe", "osen"]
VALID_BODY_PMF: Literal["disable", "enable", "optional"]
VALID_BODY_BEACON_PROTECTION: Literal["disable", "enable"]
VALID_BODY_OKC: Literal["disable", "enable"]
VALID_BODY_MBO: Literal["disable", "enable"]
VALID_BODY_MBO_CELL_DATA_CONN_PREF: Literal["excluded", "prefer-not", "prefer-use"]
VALID_BODY_80211K: Literal["disable", "enable"]
VALID_BODY_80211V: Literal["disable", "enable"]
VALID_BODY_NEIGHBOR_REPORT_DUAL_BAND: Literal["disable", "enable"]
VALID_BODY_FAST_BSS_TRANSITION: Literal["disable", "enable"]
VALID_BODY_FT_OVER_DS: Literal["disable", "enable"]
VALID_BODY_SAE_GROUPS: Literal["19", "20", "21"]
VALID_BODY_OWE_GROUPS: Literal["19", "20", "21"]
VALID_BODY_OWE_TRANSITION: Literal["disable", "enable"]
VALID_BODY_ADDITIONAL_AKMS: Literal["akm6", "akm24"]
VALID_BODY_EAPOL_KEY_RETRIES: Literal["disable", "enable"]
VALID_BODY_TKIP_COUNTER_MEASURE: Literal["enable", "disable"]
VALID_BODY_EXTERNAL_WEB_FORMAT: Literal["auto-detect", "no-query-string", "partial-query-string"]
VALID_BODY_MAC_USERNAME_DELIMITER: Literal["hyphen", "single-hyphen", "colon", "none"]
VALID_BODY_MAC_PASSWORD_DELIMITER: Literal["hyphen", "single-hyphen", "colon", "none"]
VALID_BODY_MAC_CALLING_STATION_DELIMITER: Literal["hyphen", "single-hyphen", "colon", "none"]
VALID_BODY_MAC_CALLED_STATION_DELIMITER: Literal["hyphen", "single-hyphen", "colon", "none"]
VALID_BODY_MAC_CASE: Literal["uppercase", "lowercase"]
VALID_BODY_CALLED_STATION_ID_TYPE: Literal["mac", "ip", "apname"]
VALID_BODY_MAC_AUTH_BYPASS: Literal["enable", "disable"]
VALID_BODY_RADIUS_MAC_AUTH: Literal["enable", "disable"]
VALID_BODY_RADIUS_MAC_MPSK_AUTH: Literal["enable", "disable"]
VALID_BODY_AUTH: Literal["radius", "usergroup"]
VALID_BODY_ENCRYPT: Literal["TKIP", "AES", "TKIP-AES"]
VALID_BODY_SAE_H2E_ONLY: Literal["enable", "disable"]
VALID_BODY_SAE_HNP_ONLY: Literal["enable", "disable"]
VALID_BODY_SAE_PK: Literal["enable", "disable"]
VALID_BODY_AKM24_ONLY: Literal["disable", "enable"]
VALID_BODY_NAS_FILTER_RULE: Literal["enable", "disable"]
VALID_BODY_DOMAIN_NAME_STRIPPING: Literal["disable", "enable"]
VALID_BODY_MLO: Literal["disable", "enable"]
VALID_BODY_LOCAL_STANDALONE: Literal["enable", "disable"]
VALID_BODY_LOCAL_STANDALONE_NAT: Literal["enable", "disable"]
VALID_BODY_LOCAL_STANDALONE_DNS: Literal["enable", "disable"]
VALID_BODY_LOCAL_LAN_PARTITION: Literal["enable", "disable"]
VALID_BODY_LOCAL_BRIDGING: Literal["enable", "disable"]
VALID_BODY_LOCAL_LAN: Literal["allow", "deny"]
VALID_BODY_LOCAL_AUTHENTICATION: Literal["enable", "disable"]
VALID_BODY_CAPTIVE_PORTAL: Literal["enable", "disable"]
VALID_BODY_CAPTIVE_NETWORK_ASSISTANT_BYPASS: Literal["enable", "disable"]
VALID_BODY_PORTAL_TYPE: Literal["auth", "auth+disclaimer", "disclaimer", "email-collect", "cmcc", "cmcc-macauth", "auth-mac", "external-auth", "external-macauth"]
VALID_BODY_INTRA_VAP_PRIVACY: Literal["enable", "disable"]
VALID_BODY_LDPC: Literal["disable", "rx", "tx", "rxtx"]
VALID_BODY_HIGH_EFFICIENCY: Literal["enable", "disable"]
VALID_BODY_TARGET_WAKE_TIME: Literal["enable", "disable"]
VALID_BODY_PORT_MACAUTH: Literal["disable", "radius", "address-group"]
VALID_BODY_BSS_COLOR_PARTIAL: Literal["enable", "disable"]
VALID_BODY_SPLIT_TUNNELING: Literal["enable", "disable"]
VALID_BODY_NAC: Literal["enable", "disable"]
VALID_BODY_VLAN_AUTO: Literal["enable", "disable"]
VALID_BODY_DYNAMIC_VLAN: Literal["enable", "disable"]
VALID_BODY_CAPTIVE_PORTAL_FW_ACCOUNTING: Literal["enable", "disable"]
VALID_BODY_MULTICAST_RATE: Literal["0", "6000", "12000", "24000"]
VALID_BODY_MULTICAST_ENHANCE: Literal["enable", "disable"]
VALID_BODY_IGMP_SNOOPING: Literal["enable", "disable"]
VALID_BODY_DHCP_ADDRESS_ENFORCEMENT: Literal["enable", "disable"]
VALID_BODY_BROADCAST_SUPPRESSION: Literal["dhcp-up", "dhcp-down", "dhcp-starvation", "dhcp-ucast", "arp-known", "arp-unknown", "arp-reply", "arp-poison", "arp-proxy", "netbios-ns", "netbios-ds", "ipv6", "all-other-mc", "all-other-bc"]
VALID_BODY_IPV6_RULES: Literal["drop-icmp6ra", "drop-icmp6rs", "drop-llmnr6", "drop-icmp6mld2", "drop-dhcp6s", "drop-dhcp6c", "ndp-proxy", "drop-ns-dad", "drop-ns-nondad"]
VALID_BODY_MU_MIMO: Literal["enable", "disable"]
VALID_BODY_PROBE_RESP_SUPPRESSION: Literal["enable", "disable"]
VALID_BODY_RADIO_SENSITIVITY: Literal["enable", "disable"]
VALID_BODY_QUARANTINE: Literal["enable", "disable"]
VALID_BODY_VLAN_POOLING: Literal["wtp-group", "round-robin", "hash", "disable"]
VALID_BODY_DHCP_OPTION43_INSERTION: Literal["enable", "disable"]
VALID_BODY_DHCP_OPTION82_INSERTION: Literal["enable", "disable"]
VALID_BODY_DHCP_OPTION82_CIRCUIT_ID_INSERTION: Literal["style-1", "style-2", "style-3", "disable"]
VALID_BODY_DHCP_OPTION82_REMOTE_ID_INSERTION: Literal["style-1", "disable"]
VALID_BODY_PTK_REKEY: Literal["enable", "disable"]
VALID_BODY_GTK_REKEY: Literal["enable", "disable"]
VALID_BODY_EAP_REAUTH: Literal["enable", "disable"]
VALID_BODY_ROAMING_ACCT_INTERIM_UPDATE: Literal["enable", "disable"]
VALID_BODY_RATES_11A: Literal["6", "6-basic", "9", "9-basic", "12", "12-basic", "18", "18-basic", "24", "24-basic", "36", "36-basic", "48", "48-basic", "54", "54-basic"]
VALID_BODY_RATES_11BG: Literal["1", "1-basic", "2", "2-basic", "5.5", "5.5-basic", "11", "11-basic", "6", "6-basic", "9", "9-basic", "12", "12-basic", "18", "18-basic", "24", "24-basic", "36", "36-basic", "48", "48-basic", "54", "54-basic"]
VALID_BODY_RATES_11N_SS12: Literal["mcs0/1", "mcs1/1", "mcs2/1", "mcs3/1", "mcs4/1", "mcs5/1", "mcs6/1", "mcs7/1", "mcs8/2", "mcs9/2", "mcs10/2", "mcs11/2", "mcs12/2", "mcs13/2", "mcs14/2", "mcs15/2"]
VALID_BODY_RATES_11N_SS34: Literal["mcs16/3", "mcs17/3", "mcs18/3", "mcs19/3", "mcs20/3", "mcs21/3", "mcs22/3", "mcs23/3", "mcs24/4", "mcs25/4", "mcs26/4", "mcs27/4", "mcs28/4", "mcs29/4", "mcs30/4", "mcs31/4"]
VALID_BODY_UTM_STATUS: Literal["enable", "disable"]
VALID_BODY_UTM_LOG: Literal["enable", "disable"]
VALID_BODY_SCAN_BOTNET_CONNECTIONS: Literal["disable", "monitor", "block"]
VALID_BODY_ADDRESS_GROUP_POLICY: Literal["disable", "allow", "deny"]
VALID_BODY_STICKY_CLIENT_REMOVE: Literal["enable", "disable"]
VALID_BODY_BSTM_DISASSOCIATION_IMMINENT: Literal["enable", "disable"]
VALID_BODY_BEACON_ADVERTISING: Literal["name", "model", "serial-number"]
VALID_BODY_OSEN: Literal["enable", "disable"]
VALID_BODY_APPLICATION_DETECTION_ENGINE: Literal["enable", "disable"]
VALID_BODY_APPLICATION_DSCP_MARKING: Literal["enable", "disable"]
VALID_BODY_L3_ROAMING: Literal["enable", "disable"]
VALID_BODY_L3_ROAMING_MODE: Literal["direct", "indirect"]

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
    "VALID_BODY_PRE_AUTH",
    "VALID_BODY_EXTERNAL_PRE_AUTH",
    "VALID_BODY_MESH_BACKHAUL",
    "VALID_BODY_BROADCAST_SSID",
    "VALID_BODY_SECURITY",
    "VALID_BODY_PMF",
    "VALID_BODY_BEACON_PROTECTION",
    "VALID_BODY_OKC",
    "VALID_BODY_MBO",
    "VALID_BODY_MBO_CELL_DATA_CONN_PREF",
    "VALID_BODY_80211K",
    "VALID_BODY_80211V",
    "VALID_BODY_NEIGHBOR_REPORT_DUAL_BAND",
    "VALID_BODY_FAST_BSS_TRANSITION",
    "VALID_BODY_FT_OVER_DS",
    "VALID_BODY_SAE_GROUPS",
    "VALID_BODY_OWE_GROUPS",
    "VALID_BODY_OWE_TRANSITION",
    "VALID_BODY_ADDITIONAL_AKMS",
    "VALID_BODY_EAPOL_KEY_RETRIES",
    "VALID_BODY_TKIP_COUNTER_MEASURE",
    "VALID_BODY_EXTERNAL_WEB_FORMAT",
    "VALID_BODY_MAC_USERNAME_DELIMITER",
    "VALID_BODY_MAC_PASSWORD_DELIMITER",
    "VALID_BODY_MAC_CALLING_STATION_DELIMITER",
    "VALID_BODY_MAC_CALLED_STATION_DELIMITER",
    "VALID_BODY_MAC_CASE",
    "VALID_BODY_CALLED_STATION_ID_TYPE",
    "VALID_BODY_MAC_AUTH_BYPASS",
    "VALID_BODY_RADIUS_MAC_AUTH",
    "VALID_BODY_RADIUS_MAC_MPSK_AUTH",
    "VALID_BODY_AUTH",
    "VALID_BODY_ENCRYPT",
    "VALID_BODY_SAE_H2E_ONLY",
    "VALID_BODY_SAE_HNP_ONLY",
    "VALID_BODY_SAE_PK",
    "VALID_BODY_AKM24_ONLY",
    "VALID_BODY_NAS_FILTER_RULE",
    "VALID_BODY_DOMAIN_NAME_STRIPPING",
    "VALID_BODY_MLO",
    "VALID_BODY_LOCAL_STANDALONE",
    "VALID_BODY_LOCAL_STANDALONE_NAT",
    "VALID_BODY_LOCAL_STANDALONE_DNS",
    "VALID_BODY_LOCAL_LAN_PARTITION",
    "VALID_BODY_LOCAL_BRIDGING",
    "VALID_BODY_LOCAL_LAN",
    "VALID_BODY_LOCAL_AUTHENTICATION",
    "VALID_BODY_CAPTIVE_PORTAL",
    "VALID_BODY_CAPTIVE_NETWORK_ASSISTANT_BYPASS",
    "VALID_BODY_PORTAL_TYPE",
    "VALID_BODY_INTRA_VAP_PRIVACY",
    "VALID_BODY_LDPC",
    "VALID_BODY_HIGH_EFFICIENCY",
    "VALID_BODY_TARGET_WAKE_TIME",
    "VALID_BODY_PORT_MACAUTH",
    "VALID_BODY_BSS_COLOR_PARTIAL",
    "VALID_BODY_SPLIT_TUNNELING",
    "VALID_BODY_NAC",
    "VALID_BODY_VLAN_AUTO",
    "VALID_BODY_DYNAMIC_VLAN",
    "VALID_BODY_CAPTIVE_PORTAL_FW_ACCOUNTING",
    "VALID_BODY_MULTICAST_RATE",
    "VALID_BODY_MULTICAST_ENHANCE",
    "VALID_BODY_IGMP_SNOOPING",
    "VALID_BODY_DHCP_ADDRESS_ENFORCEMENT",
    "VALID_BODY_BROADCAST_SUPPRESSION",
    "VALID_BODY_IPV6_RULES",
    "VALID_BODY_MU_MIMO",
    "VALID_BODY_PROBE_RESP_SUPPRESSION",
    "VALID_BODY_RADIO_SENSITIVITY",
    "VALID_BODY_QUARANTINE",
    "VALID_BODY_VLAN_POOLING",
    "VALID_BODY_DHCP_OPTION43_INSERTION",
    "VALID_BODY_DHCP_OPTION82_INSERTION",
    "VALID_BODY_DHCP_OPTION82_CIRCUIT_ID_INSERTION",
    "VALID_BODY_DHCP_OPTION82_REMOTE_ID_INSERTION",
    "VALID_BODY_PTK_REKEY",
    "VALID_BODY_GTK_REKEY",
    "VALID_BODY_EAP_REAUTH",
    "VALID_BODY_ROAMING_ACCT_INTERIM_UPDATE",
    "VALID_BODY_RATES_11A",
    "VALID_BODY_RATES_11BG",
    "VALID_BODY_RATES_11N_SS12",
    "VALID_BODY_RATES_11N_SS34",
    "VALID_BODY_UTM_STATUS",
    "VALID_BODY_UTM_LOG",
    "VALID_BODY_SCAN_BOTNET_CONNECTIONS",
    "VALID_BODY_ADDRESS_GROUP_POLICY",
    "VALID_BODY_STICKY_CLIENT_REMOVE",
    "VALID_BODY_BSTM_DISASSOCIATION_IMMINENT",
    "VALID_BODY_BEACON_ADVERTISING",
    "VALID_BODY_OSEN",
    "VALID_BODY_APPLICATION_DETECTION_ENGINE",
    "VALID_BODY_APPLICATION_DSCP_MARKING",
    "VALID_BODY_L3_ROAMING",
    "VALID_BODY_L3_ROAMING_MODE",
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