from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_TYPE: Literal["static", "dynamic", "ddns"]
VALID_BODY_IP_VERSION: Literal["4", "6"]
VALID_BODY_IKE_VERSION: Literal["1", "2"]
VALID_BODY_AUTHMETHOD: Literal["psk", "signature"]
VALID_BODY_AUTHMETHOD_REMOTE: Literal["psk", "signature"]
VALID_BODY_MODE: Literal["aggressive", "main"]
VALID_BODY_PEERTYPE: Literal["any", "one", "dialup", "peer", "peergrp"]
VALID_BODY_MONITOR_HOLD_DOWN_TYPE: Literal["immediate", "delay", "time"]
VALID_BODY_MONITOR_HOLD_DOWN_WEEKDAY: Literal["everyday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
VALID_BODY_NET_DEVICE: Literal["enable", "disable"]
VALID_BODY_PASSIVE_MODE: Literal["enable", "disable"]
VALID_BODY_EXCHANGE_INTERFACE_IP: Literal["enable", "disable"]
VALID_BODY_AGGREGATE_MEMBER: Literal["enable", "disable"]
VALID_BODY_PACKET_REDISTRIBUTION: Literal["enable", "disable"]
VALID_BODY_PEER_EGRESS_SHAPING: Literal["enable", "disable"]
VALID_BODY_MODE_CFG: Literal["disable", "enable"]
VALID_BODY_MODE_CFG_ALLOW_CLIENT_SELECTOR: Literal["disable", "enable"]
VALID_BODY_ASSIGN_IP: Literal["disable", "enable"]
VALID_BODY_ASSIGN_IP_FROM: Literal["range", "usrgrp", "dhcp", "name"]
VALID_BODY_DNS_MODE: Literal["manual", "auto"]
VALID_BODY_UNITY_SUPPORT: Literal["disable", "enable"]
VALID_BODY_INCLUDE_LOCAL_LAN: Literal["disable", "enable"]
VALID_BODY_SAVE_PASSWORD: Literal["disable", "enable"]
VALID_BODY_CLIENT_AUTO_NEGOTIATE: Literal["disable", "enable"]
VALID_BODY_CLIENT_KEEP_ALIVE: Literal["disable", "enable"]
VALID_BODY_PROPOSAL: Literal["des-md5", "des-sha1", "des-sha256", "des-sha384", "des-sha512", "3des-md5", "3des-sha1", "3des-sha256", "3des-sha384", "3des-sha512", "aes128-md5", "aes128-sha1", "aes128-sha256", "aes128-sha384", "aes128-sha512", "aes128gcm-prfsha1", "aes128gcm-prfsha256", "aes128gcm-prfsha384", "aes128gcm-prfsha512", "aes192-md5", "aes192-sha1", "aes192-sha256", "aes192-sha384", "aes192-sha512", "aes256-md5", "aes256-sha1", "aes256-sha256", "aes256-sha384", "aes256-sha512", "aes256gcm-prfsha1", "aes256gcm-prfsha256", "aes256gcm-prfsha384", "aes256gcm-prfsha512", "chacha20poly1305-prfsha1", "chacha20poly1305-prfsha256", "chacha20poly1305-prfsha384", "chacha20poly1305-prfsha512", "aria128-md5", "aria128-sha1", "aria128-sha256", "aria128-sha384", "aria128-sha512", "aria192-md5", "aria192-sha1", "aria192-sha256", "aria192-sha384", "aria192-sha512", "aria256-md5", "aria256-sha1", "aria256-sha256", "aria256-sha384", "aria256-sha512", "seed-md5", "seed-sha1", "seed-sha256", "seed-sha384", "seed-sha512"]
VALID_BODY_ADD_ROUTE: Literal["disable", "enable"]
VALID_BODY_ADD_GW_ROUTE: Literal["enable", "disable"]
VALID_BODY_LOCALID_TYPE: Literal["auto", "fqdn", "user-fqdn", "keyid", "address", "asn1dn"]
VALID_BODY_AUTO_NEGOTIATE: Literal["enable", "disable"]
VALID_BODY_FRAGMENTATION: Literal["enable", "disable"]
VALID_BODY_IP_FRAGMENTATION: Literal["pre-encapsulation", "post-encapsulation"]
VALID_BODY_DPD: Literal["disable", "on-idle", "on-demand"]
VALID_BODY_NPU_OFFLOAD: Literal["enable", "disable"]
VALID_BODY_SEND_CERT_CHAIN: Literal["enable", "disable"]
VALID_BODY_DHGRP: Literal["1", "2", "5", "14", "15", "16", "17", "18", "19", "20", "21", "27", "28", "29", "30", "31", "32"]
VALID_BODY_ADDKE1: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE2: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE3: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE4: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE5: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE6: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_ADDKE7: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"]
VALID_BODY_SUITE_B: Literal["disable", "suite-b-gcm-128", "suite-b-gcm-256"]
VALID_BODY_EAP: Literal["enable", "disable"]
VALID_BODY_EAP_IDENTITY: Literal["use-id-payload", "send-request"]
VALID_BODY_EAP_CERT_AUTH: Literal["enable", "disable"]
VALID_BODY_ACCT_VERIFY: Literal["enable", "disable"]
VALID_BODY_PPK: Literal["disable", "allow", "require"]
VALID_BODY_WIZARD_TYPE: Literal["custom", "dialup-forticlient", "dialup-ios", "dialup-android", "dialup-windows", "dialup-cisco", "static-fortigate", "dialup-fortigate", "static-cisco", "dialup-cisco-fw", "simplified-static-fortigate", "hub-fortigate-auto-discovery", "spoke-fortigate-auto-discovery", "fabric-overlay-orchestrator"]
VALID_BODY_XAUTHTYPE: Literal["disable", "client", "pap", "chap", "auto"]
VALID_BODY_REAUTH: Literal["disable", "enable"]
VALID_BODY_GROUP_AUTHENTICATION: Literal["enable", "disable"]
VALID_BODY_MESH_SELECTOR_TYPE: Literal["disable", "subnet", "host"]
VALID_BODY_IDLE_TIMEOUT: Literal["enable", "disable"]
VALID_BODY_SHARED_IDLE_TIMEOUT: Literal["enable", "disable"]
VALID_BODY_HA_SYNC_ESP_SEQNO: Literal["enable", "disable"]
VALID_BODY_FGSP_SYNC: Literal["enable", "disable"]
VALID_BODY_INBOUND_DSCP_COPY: Literal["enable", "disable"]
VALID_BODY_AUTO_DISCOVERY_SENDER: Literal["enable", "disable"]
VALID_BODY_AUTO_DISCOVERY_RECEIVER: Literal["enable", "disable"]
VALID_BODY_AUTO_DISCOVERY_FORWARDER: Literal["enable", "disable"]
VALID_BODY_AUTO_DISCOVERY_PSK: Literal["enable", "disable"]
VALID_BODY_AUTO_DISCOVERY_SHORTCUTS: Literal["independent", "dependent"]
VALID_BODY_AUTO_DISCOVERY_CROSSOVER: Literal["allow", "block"]
VALID_BODY_AUTO_DISCOVERY_DIALUP_PLACEHOLDER: Literal["disable", "enable"]
VALID_BODY_ENCAPSULATION: Literal["none", "gre", "vxlan", "vpn-id-ipip"]
VALID_BODY_ENCAPSULATION_ADDRESS: Literal["ike", "ipv4", "ipv6"]
VALID_BODY_NATTRAVERSAL: Literal["enable", "disable", "forced"]
VALID_BODY_ESN: Literal["require", "allow", "disable"]
VALID_BODY_CHILDLESS_IKE: Literal["enable", "disable"]
VALID_BODY_AZURE_AD_AUTOCONNECT: Literal["enable", "disable"]
VALID_BODY_CLIENT_RESUME: Literal["enable", "disable"]
VALID_BODY_REKEY: Literal["enable", "disable"]
VALID_BODY_DIGITAL_SIGNATURE_AUTH: Literal["enable", "disable"]
VALID_BODY_SIGNATURE_HASH_ALG: Literal["sha1", "sha2-256", "sha2-384", "sha2-512"]
VALID_BODY_RSA_SIGNATURE_FORMAT: Literal["pkcs1", "pss"]
VALID_BODY_RSA_SIGNATURE_HASH_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_ENFORCE_UNIQUE_ID: Literal["disable", "keep-new", "keep-old"]
VALID_BODY_CERT_ID_VALIDATION: Literal["enable", "disable"]
VALID_BODY_FEC_EGRESS: Literal["enable", "disable"]
VALID_BODY_FEC_CODEC: Literal["rs", "xor"]
VALID_BODY_FEC_INGRESS: Literal["enable", "disable"]
VALID_BODY_NETWORK_OVERLAY: Literal["disable", "enable"]
VALID_BODY_DEV_ID_NOTIFICATION: Literal["disable", "enable"]
VALID_BODY_LOOPBACK_ASYMROUTE: Literal["enable", "disable"]
VALID_BODY_EXCHANGE_FGT_DEVICE_ID: Literal["enable", "disable"]
VALID_BODY_IPV6_AUTO_LINKLOCAL: Literal["enable", "disable"]
VALID_BODY_EMS_SN_CHECK: Literal["enable", "disable"]
VALID_BODY_CERT_TRUST_STORE: Literal["local", "ems"]
VALID_BODY_QKD: Literal["disable", "allow", "require"]
VALID_BODY_QKD_HYBRID: Literal["disable", "allow", "require"]
VALID_BODY_TRANSPORT: Literal["udp", "auto", "tcp"]
VALID_BODY_FORTINET_ESP: Literal["enable", "disable"]
VALID_BODY_REMOTE_GW_MATCH: Literal["any", "ipmask", "iprange", "geography", "ztna"]
VALID_BODY_REMOTE_GW6_MATCH: Literal["any", "ipprefix", "iprange", "geography"]
VALID_BODY_CERT_PEER_USERNAME_VALIDATION: Literal["none", "othername", "rfc822name", "cn"]
VALID_BODY_CERT_PEER_USERNAME_STRIP: Literal["disable", "enable"]

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
    "VALID_BODY_TYPE",
    "VALID_BODY_IP_VERSION",
    "VALID_BODY_IKE_VERSION",
    "VALID_BODY_AUTHMETHOD",
    "VALID_BODY_AUTHMETHOD_REMOTE",
    "VALID_BODY_MODE",
    "VALID_BODY_PEERTYPE",
    "VALID_BODY_MONITOR_HOLD_DOWN_TYPE",
    "VALID_BODY_MONITOR_HOLD_DOWN_WEEKDAY",
    "VALID_BODY_NET_DEVICE",
    "VALID_BODY_PASSIVE_MODE",
    "VALID_BODY_EXCHANGE_INTERFACE_IP",
    "VALID_BODY_AGGREGATE_MEMBER",
    "VALID_BODY_PACKET_REDISTRIBUTION",
    "VALID_BODY_PEER_EGRESS_SHAPING",
    "VALID_BODY_MODE_CFG",
    "VALID_BODY_MODE_CFG_ALLOW_CLIENT_SELECTOR",
    "VALID_BODY_ASSIGN_IP",
    "VALID_BODY_ASSIGN_IP_FROM",
    "VALID_BODY_DNS_MODE",
    "VALID_BODY_UNITY_SUPPORT",
    "VALID_BODY_INCLUDE_LOCAL_LAN",
    "VALID_BODY_SAVE_PASSWORD",
    "VALID_BODY_CLIENT_AUTO_NEGOTIATE",
    "VALID_BODY_CLIENT_KEEP_ALIVE",
    "VALID_BODY_PROPOSAL",
    "VALID_BODY_ADD_ROUTE",
    "VALID_BODY_ADD_GW_ROUTE",
    "VALID_BODY_LOCALID_TYPE",
    "VALID_BODY_AUTO_NEGOTIATE",
    "VALID_BODY_FRAGMENTATION",
    "VALID_BODY_IP_FRAGMENTATION",
    "VALID_BODY_DPD",
    "VALID_BODY_NPU_OFFLOAD",
    "VALID_BODY_SEND_CERT_CHAIN",
    "VALID_BODY_DHGRP",
    "VALID_BODY_ADDKE1",
    "VALID_BODY_ADDKE2",
    "VALID_BODY_ADDKE3",
    "VALID_BODY_ADDKE4",
    "VALID_BODY_ADDKE5",
    "VALID_BODY_ADDKE6",
    "VALID_BODY_ADDKE7",
    "VALID_BODY_SUITE_B",
    "VALID_BODY_EAP",
    "VALID_BODY_EAP_IDENTITY",
    "VALID_BODY_EAP_CERT_AUTH",
    "VALID_BODY_ACCT_VERIFY",
    "VALID_BODY_PPK",
    "VALID_BODY_WIZARD_TYPE",
    "VALID_BODY_XAUTHTYPE",
    "VALID_BODY_REAUTH",
    "VALID_BODY_GROUP_AUTHENTICATION",
    "VALID_BODY_MESH_SELECTOR_TYPE",
    "VALID_BODY_IDLE_TIMEOUT",
    "VALID_BODY_SHARED_IDLE_TIMEOUT",
    "VALID_BODY_HA_SYNC_ESP_SEQNO",
    "VALID_BODY_FGSP_SYNC",
    "VALID_BODY_INBOUND_DSCP_COPY",
    "VALID_BODY_AUTO_DISCOVERY_SENDER",
    "VALID_BODY_AUTO_DISCOVERY_RECEIVER",
    "VALID_BODY_AUTO_DISCOVERY_FORWARDER",
    "VALID_BODY_AUTO_DISCOVERY_PSK",
    "VALID_BODY_AUTO_DISCOVERY_SHORTCUTS",
    "VALID_BODY_AUTO_DISCOVERY_CROSSOVER",
    "VALID_BODY_AUTO_DISCOVERY_DIALUP_PLACEHOLDER",
    "VALID_BODY_ENCAPSULATION",
    "VALID_BODY_ENCAPSULATION_ADDRESS",
    "VALID_BODY_NATTRAVERSAL",
    "VALID_BODY_ESN",
    "VALID_BODY_CHILDLESS_IKE",
    "VALID_BODY_AZURE_AD_AUTOCONNECT",
    "VALID_BODY_CLIENT_RESUME",
    "VALID_BODY_REKEY",
    "VALID_BODY_DIGITAL_SIGNATURE_AUTH",
    "VALID_BODY_SIGNATURE_HASH_ALG",
    "VALID_BODY_RSA_SIGNATURE_FORMAT",
    "VALID_BODY_RSA_SIGNATURE_HASH_OVERRIDE",
    "VALID_BODY_ENFORCE_UNIQUE_ID",
    "VALID_BODY_CERT_ID_VALIDATION",
    "VALID_BODY_FEC_EGRESS",
    "VALID_BODY_FEC_CODEC",
    "VALID_BODY_FEC_INGRESS",
    "VALID_BODY_NETWORK_OVERLAY",
    "VALID_BODY_DEV_ID_NOTIFICATION",
    "VALID_BODY_LOOPBACK_ASYMROUTE",
    "VALID_BODY_EXCHANGE_FGT_DEVICE_ID",
    "VALID_BODY_IPV6_AUTO_LINKLOCAL",
    "VALID_BODY_EMS_SN_CHECK",
    "VALID_BODY_CERT_TRUST_STORE",
    "VALID_BODY_QKD",
    "VALID_BODY_QKD_HYBRID",
    "VALID_BODY_TRANSPORT",
    "VALID_BODY_FORTINET_ESP",
    "VALID_BODY_REMOTE_GW_MATCH",
    "VALID_BODY_REMOTE_GW6_MATCH",
    "VALID_BODY_CERT_PEER_USERNAME_VALIDATION",
    "VALID_BODY_CERT_PEER_USERNAME_STRIP",
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