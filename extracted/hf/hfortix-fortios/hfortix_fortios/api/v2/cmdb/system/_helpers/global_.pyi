from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_LANGUAGE: Literal["english", "french", "spanish", "portuguese", "japanese", "trach", "simch", "korean"]
VALID_BODY_GUI_IPV6: Literal["enable", "disable"]
VALID_BODY_GUI_REPLACEMENT_MESSAGE_GROUPS: Literal["enable", "disable"]
VALID_BODY_GUI_LOCAL_OUT: Literal["enable", "disable"]
VALID_BODY_GUI_CERTIFICATES: Literal["enable", "disable"]
VALID_BODY_GUI_CUSTOM_LANGUAGE: Literal["enable", "disable"]
VALID_BODY_GUI_WIRELESS_OPENSECURITY: Literal["enable", "disable"]
VALID_BODY_GUI_APP_DETECTION_SDWAN: Literal["enable", "disable"]
VALID_BODY_GUI_DISPLAY_HOSTNAME: Literal["enable", "disable"]
VALID_BODY_GUI_FORTIGATE_CLOUD_SANDBOX: Literal["enable", "disable"]
VALID_BODY_GUI_FIRMWARE_UPGRADE_WARNING: Literal["enable", "disable"]
VALID_BODY_GUI_FORTICARE_REGISTRATION_SETUP_WARNING: Literal["enable", "disable"]
VALID_BODY_GUI_AUTO_UPGRADE_SETUP_WARNING: Literal["enable", "disable"]
VALID_BODY_GUI_WORKFLOW_MANAGEMENT: Literal["enable", "disable"]
VALID_BODY_GUI_CDN_USAGE: Literal["enable", "disable"]
VALID_BODY_ADMIN_HTTPS_SSL_VERSIONS: Literal["tlsv1-1", "tlsv1-2", "tlsv1-3"]
VALID_BODY_ADMIN_HTTPS_SSL_CIPHERSUITES: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-AES-128-CCM-SHA256", "TLS-AES-128-CCM-8-SHA256"]
VALID_BODY_ADMIN_HTTPS_SSL_BANNED_CIPHERS: Literal["RSA", "DHE", "ECDHE", "DSS", "ECDSA", "AES", "AESGCM", "CAMELLIA", "3DES", "SHA1", "SHA256", "SHA384", "STATIC", "CHACHA20", "ARIA", "AESCCM"]
VALID_BODY_SSD_TRIM_FREQ: Literal["never", "hourly", "daily", "weekly", "monthly"]
VALID_BODY_SSD_TRIM_WEEKDAY: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
VALID_BODY_ADMIN_CONCURRENT: Literal["enable", "disable"]
VALID_BODY_PURDUE_LEVEL: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
VALID_BODY_DAILY_RESTART: Literal["enable", "disable"]
VALID_BODY_WAD_RESTART_MODE: Literal["none", "time", "memory"]
VALID_BODY_BATCH_CMDB: Literal["enable", "disable"]
VALID_BODY_MULTI_FACTOR_AUTHENTICATION: Literal["optional", "mandatory"]
VALID_BODY_SSL_MIN_PROTO_VERSION: Literal["SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
VALID_BODY_AUTORUN_LOG_FSCK: Literal["enable", "disable"]
VALID_BODY_TRAFFIC_PRIORITY: Literal["tos", "dscp"]
VALID_BODY_TRAFFIC_PRIORITY_LEVEL: Literal["low", "medium", "high"]
VALID_BODY_QUIC_CONGESTION_CONTROL_ALGO: Literal["cubic", "bbr", "bbr2", "reno"]
VALID_BODY_QUIC_UDP_PAYLOAD_SIZE_SHAPING_PER_CID: Literal["enable", "disable"]
VALID_BODY_QUIC_PMTUD: Literal["enable", "disable"]
VALID_BODY_ANTI_REPLAY: Literal["disable", "loose", "strict"]
VALID_BODY_SEND_PMTU_ICMP: Literal["enable", "disable"]
VALID_BODY_HONOR_DF: Literal["enable", "disable"]
VALID_BODY_PMTU_DISCOVERY: Literal["enable", "disable"]
VALID_BODY_REVISION_IMAGE_AUTO_BACKUP: Literal["enable", "disable"]
VALID_BODY_REVISION_BACKUP_ON_LOGOUT: Literal["enable", "disable"]
VALID_BODY_STRONG_CRYPTO: Literal["enable", "disable"]
VALID_BODY_SSL_STATIC_KEY_CIPHERS: Literal["enable", "disable"]
VALID_BODY_SNAT_ROUTE_CHANGE: Literal["enable", "disable"]
VALID_BODY_IPV6_SNAT_ROUTE_CHANGE: Literal["enable", "disable"]
VALID_BODY_SPEEDTEST_SERVER: Literal["enable", "disable"]
VALID_BODY_CLI_AUDIT_LOG: Literal["enable", "disable"]
VALID_BODY_DH_PARAMS: Literal["1024", "1536", "2048", "3072", "4096", "6144", "8192"]
VALID_BODY_FDS_STATISTICS: Literal["enable", "disable"]
VALID_BODY_TCP_OPTION: Literal["enable", "disable"]
VALID_BODY_LLDP_TRANSMISSION: Literal["enable", "disable"]
VALID_BODY_LLDP_RECEPTION: Literal["enable", "disable"]
VALID_BODY_PROXY_KEEP_ALIVE_MODE: Literal["session", "traffic", "re-authentication"]
VALID_BODY_PROXY_AUTH_LIFETIME: Literal["enable", "disable"]
VALID_BODY_PROXY_RESOURCE_MODE: Literal["enable", "disable"]
VALID_BODY_PROXY_CERT_USE_MGMT_VDOM: Literal["enable", "disable"]
VALID_BODY_CHECK_PROTOCOL_HEADER: Literal["loose", "strict"]
VALID_BODY_VIP_ARP_RANGE: Literal["unlimited", "restricted"]
VALID_BODY_RESET_SESSIONLESS_TCP: Literal["enable", "disable"]
VALID_BODY_ALLOW_TRAFFIC_REDIRECT: Literal["enable", "disable"]
VALID_BODY_IPV6_ALLOW_TRAFFIC_REDIRECT: Literal["enable", "disable"]
VALID_BODY_STRICT_DIRTY_SESSION_CHECK: Literal["enable", "disable"]
VALID_BODY_PRE_LOGIN_BANNER: Literal["enable", "disable"]
VALID_BODY_POST_LOGIN_BANNER: Literal["disable", "enable"]
VALID_BODY_TFTP: Literal["enable", "disable"]
VALID_BODY_AV_FAILOPEN: Literal["pass", "off", "one-shot"]
VALID_BODY_AV_FAILOPEN_SESSION: Literal["enable", "disable"]
VALID_BODY_LOG_SINGLE_CPU_HIGH: Literal["enable", "disable"]
VALID_BODY_CHECK_RESET_RANGE: Literal["strict", "disable"]
VALID_BODY_UPGRADE_REPORT: Literal["enable", "disable"]
VALID_BODY_ADMIN_HTTPS_REDIRECT: Literal["enable", "disable"]
VALID_BODY_ADMIN_SSH_PASSWORD: Literal["enable", "disable"]
VALID_BODY_ADMIN_RESTRICT_LOCAL: Literal["all", "non-console-only", "disable"]
VALID_BODY_ADMIN_SSH_V1: Literal["enable", "disable"]
VALID_BODY_ADMIN_TELNET: Literal["enable", "disable"]
VALID_BODY_ADMIN_FORTICLOUD_SSO_LOGIN: Literal["enable", "disable"]
VALID_BODY_ADMIN_HTTPS_PKI_REQUIRED: Literal["enable", "disable"]
VALID_BODY_AUTH_KEEPALIVE: Literal["enable", "disable"]
VALID_BODY_AUTH_SESSION_LIMIT: Literal["block-new", "logout-inactive"]
VALID_BODY_CLT_CERT_REQ: Literal["enable", "disable"]
VALID_BODY_CFG_SAVE: Literal["automatic", "manual", "revert"]
VALID_BODY_REBOOT_UPON_CONFIG_RESTORE: Literal["enable", "disable"]
VALID_BODY_ADMIN_SCP: Literal["enable", "disable"]
VALID_BODY_WIRELESS_CONTROLLER: Literal["enable", "disable"]
VALID_BODY_FORTIEXTENDER: Literal["disable", "enable"]
VALID_BODY_FORTIEXTENDER_DISCOVERY_LOCKDOWN: Literal["disable", "enable"]
VALID_BODY_FORTIEXTENDER_VLAN_MODE: Literal["enable", "disable"]
VALID_BODY_FORTIEXTENDER_PROVISION_ON_AUTHORIZATION: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER: Literal["disable", "enable"]
VALID_BODY_FGD_ALERT_SUBSCRIPTION: Literal["advisory", "latest-threat", "latest-virus", "latest-attack", "new-antivirus-db", "new-attack-db"]
VALID_BODY_IPV6_ALLOW_ANYCAST_PROBE: Literal["enable", "disable"]
VALID_BODY_IPV6_ALLOW_MULTICAST_PROBE: Literal["enable", "disable"]
VALID_BODY_IPV6_ALLOW_LOCAL_IN_SILENT_DROP: Literal["enable", "disable"]
VALID_BODY_CSR_CA_ATTRIBUTE: Literal["enable", "disable"]
VALID_BODY_WIMAX_4G_USB: Literal["enable", "disable"]
VALID_BODY_SSLVPN_WEB_MODE: Literal["enable", "disable"]
VALID_BODY_PER_USER_BAL: Literal["enable", "disable"]
VALID_BODY_WAD_SOURCE_AFFINITY: Literal["disable", "enable"]
VALID_BODY_LOGIN_TIMESTAMP: Literal["enable", "disable"]
VALID_BODY_IP_CONFLICT_DETECTION: Literal["enable", "disable"]
VALID_BODY_SPECIAL_FILE_23_SUPPORT: Literal["disable", "enable"]
VALID_BODY_LOG_UUID_ADDRESS: Literal["enable", "disable"]
VALID_BODY_LOG_SSL_CONNECTION: Literal["enable", "disable"]
VALID_BODY_GUI_REST_API_CACHE: Literal["enable", "disable"]
VALID_BODY_REST_API_KEY_URL_QUERY: Literal["enable", "disable"]
VALID_BODY_IPSEC_QAT_OFFLOAD: Literal["enable", "disable"]
VALID_BODY_PRIVATE_DATA_ENCRYPTION: Literal["disable", "enable"]
VALID_BODY_AUTO_AUTH_EXTENSION_DEVICE: Literal["enable", "disable"]
VALID_BODY_GUI_THEME: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "retro", "dark-matter", "onyx", "eclipse"]
VALID_BODY_GUI_DATE_FORMAT: Literal["yyyy/MM/dd", "dd/MM/yyyy", "MM/dd/yyyy", "yyyy-MM-dd", "dd-MM-yyyy", "MM-dd-yyyy"]
VALID_BODY_GUI_DATE_TIME_SOURCE: Literal["system", "browser"]
VALID_BODY_CLOUD_COMMUNICATION: Literal["enable", "disable"]
VALID_BODY_FORTITOKEN_CLOUD: Literal["enable", "disable"]
VALID_BODY_FORTITOKEN_CLOUD_PUSH_STATUS: Literal["enable", "disable"]
VALID_BODY_IRQ_TIME_ACCOUNTING: Literal["auto", "force"]
VALID_BODY_MANAGEMENT_PORT_USE_ADMIN_SPORT: Literal["enable", "disable"]
VALID_BODY_FORTICONVERTER_INTEGRATION: Literal["enable", "disable"]
VALID_BODY_FORTICONVERTER_CONFIG_UPLOAD: Literal["once", "disable"]
VALID_BODY_INTERNET_SERVICE_DATABASE: Literal["mini", "standard", "full", "on-demand"]
VALID_BODY_GEOIP_FULL_DB: Literal["enable", "disable"]
VALID_BODY_EARLY_TCP_NPU_SESSION: Literal["enable", "disable"]
VALID_BODY_NPU_NEIGHBOR_UPDATE: Literal["enable", "disable"]
VALID_BODY_DELAY_TCP_NPU_SESSION: Literal["enable", "disable"]
VALID_BODY_INTERFACE_SUBNET_USAGE: Literal["disable", "enable"]
VALID_BODY_FORTIGSLB_INTEGRATION: Literal["disable", "enable"]
VALID_BODY_AUTH_SESSION_AUTO_BACKUP: Literal["enable", "disable"]
VALID_BODY_AUTH_SESSION_AUTO_BACKUP_INTERVAL: Literal["1min", "5min", "15min", "30min", "1hr"]
VALID_BODY_APPLICATION_BANDWIDTH_TRACKING: Literal["disable", "enable"]
VALID_BODY_TLS_SESSION_CACHE: Literal["enable", "disable"]

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
    "VALID_BODY_LANGUAGE",
    "VALID_BODY_GUI_IPV6",
    "VALID_BODY_GUI_REPLACEMENT_MESSAGE_GROUPS",
    "VALID_BODY_GUI_LOCAL_OUT",
    "VALID_BODY_GUI_CERTIFICATES",
    "VALID_BODY_GUI_CUSTOM_LANGUAGE",
    "VALID_BODY_GUI_WIRELESS_OPENSECURITY",
    "VALID_BODY_GUI_APP_DETECTION_SDWAN",
    "VALID_BODY_GUI_DISPLAY_HOSTNAME",
    "VALID_BODY_GUI_FORTIGATE_CLOUD_SANDBOX",
    "VALID_BODY_GUI_FIRMWARE_UPGRADE_WARNING",
    "VALID_BODY_GUI_FORTICARE_REGISTRATION_SETUP_WARNING",
    "VALID_BODY_GUI_AUTO_UPGRADE_SETUP_WARNING",
    "VALID_BODY_GUI_WORKFLOW_MANAGEMENT",
    "VALID_BODY_GUI_CDN_USAGE",
    "VALID_BODY_ADMIN_HTTPS_SSL_VERSIONS",
    "VALID_BODY_ADMIN_HTTPS_SSL_CIPHERSUITES",
    "VALID_BODY_ADMIN_HTTPS_SSL_BANNED_CIPHERS",
    "VALID_BODY_SSD_TRIM_FREQ",
    "VALID_BODY_SSD_TRIM_WEEKDAY",
    "VALID_BODY_ADMIN_CONCURRENT",
    "VALID_BODY_PURDUE_LEVEL",
    "VALID_BODY_DAILY_RESTART",
    "VALID_BODY_WAD_RESTART_MODE",
    "VALID_BODY_BATCH_CMDB",
    "VALID_BODY_MULTI_FACTOR_AUTHENTICATION",
    "VALID_BODY_SSL_MIN_PROTO_VERSION",
    "VALID_BODY_AUTORUN_LOG_FSCK",
    "VALID_BODY_TRAFFIC_PRIORITY",
    "VALID_BODY_TRAFFIC_PRIORITY_LEVEL",
    "VALID_BODY_QUIC_CONGESTION_CONTROL_ALGO",
    "VALID_BODY_QUIC_UDP_PAYLOAD_SIZE_SHAPING_PER_CID",
    "VALID_BODY_QUIC_PMTUD",
    "VALID_BODY_ANTI_REPLAY",
    "VALID_BODY_SEND_PMTU_ICMP",
    "VALID_BODY_HONOR_DF",
    "VALID_BODY_PMTU_DISCOVERY",
    "VALID_BODY_REVISION_IMAGE_AUTO_BACKUP",
    "VALID_BODY_REVISION_BACKUP_ON_LOGOUT",
    "VALID_BODY_STRONG_CRYPTO",
    "VALID_BODY_SSL_STATIC_KEY_CIPHERS",
    "VALID_BODY_SNAT_ROUTE_CHANGE",
    "VALID_BODY_IPV6_SNAT_ROUTE_CHANGE",
    "VALID_BODY_SPEEDTEST_SERVER",
    "VALID_BODY_CLI_AUDIT_LOG",
    "VALID_BODY_DH_PARAMS",
    "VALID_BODY_FDS_STATISTICS",
    "VALID_BODY_TCP_OPTION",
    "VALID_BODY_LLDP_TRANSMISSION",
    "VALID_BODY_LLDP_RECEPTION",
    "VALID_BODY_PROXY_KEEP_ALIVE_MODE",
    "VALID_BODY_PROXY_AUTH_LIFETIME",
    "VALID_BODY_PROXY_RESOURCE_MODE",
    "VALID_BODY_PROXY_CERT_USE_MGMT_VDOM",
    "VALID_BODY_CHECK_PROTOCOL_HEADER",
    "VALID_BODY_VIP_ARP_RANGE",
    "VALID_BODY_RESET_SESSIONLESS_TCP",
    "VALID_BODY_ALLOW_TRAFFIC_REDIRECT",
    "VALID_BODY_IPV6_ALLOW_TRAFFIC_REDIRECT",
    "VALID_BODY_STRICT_DIRTY_SESSION_CHECK",
    "VALID_BODY_PRE_LOGIN_BANNER",
    "VALID_BODY_POST_LOGIN_BANNER",
    "VALID_BODY_TFTP",
    "VALID_BODY_AV_FAILOPEN",
    "VALID_BODY_AV_FAILOPEN_SESSION",
    "VALID_BODY_LOG_SINGLE_CPU_HIGH",
    "VALID_BODY_CHECK_RESET_RANGE",
    "VALID_BODY_UPGRADE_REPORT",
    "VALID_BODY_ADMIN_HTTPS_REDIRECT",
    "VALID_BODY_ADMIN_SSH_PASSWORD",
    "VALID_BODY_ADMIN_RESTRICT_LOCAL",
    "VALID_BODY_ADMIN_SSH_V1",
    "VALID_BODY_ADMIN_TELNET",
    "VALID_BODY_ADMIN_FORTICLOUD_SSO_LOGIN",
    "VALID_BODY_ADMIN_HTTPS_PKI_REQUIRED",
    "VALID_BODY_AUTH_KEEPALIVE",
    "VALID_BODY_AUTH_SESSION_LIMIT",
    "VALID_BODY_CLT_CERT_REQ",
    "VALID_BODY_CFG_SAVE",
    "VALID_BODY_REBOOT_UPON_CONFIG_RESTORE",
    "VALID_BODY_ADMIN_SCP",
    "VALID_BODY_WIRELESS_CONTROLLER",
    "VALID_BODY_FORTIEXTENDER",
    "VALID_BODY_FORTIEXTENDER_DISCOVERY_LOCKDOWN",
    "VALID_BODY_FORTIEXTENDER_VLAN_MODE",
    "VALID_BODY_FORTIEXTENDER_PROVISION_ON_AUTHORIZATION",
    "VALID_BODY_SWITCH_CONTROLLER",
    "VALID_BODY_FGD_ALERT_SUBSCRIPTION",
    "VALID_BODY_IPV6_ALLOW_ANYCAST_PROBE",
    "VALID_BODY_IPV6_ALLOW_MULTICAST_PROBE",
    "VALID_BODY_IPV6_ALLOW_LOCAL_IN_SILENT_DROP",
    "VALID_BODY_CSR_CA_ATTRIBUTE",
    "VALID_BODY_WIMAX_4G_USB",
    "VALID_BODY_SSLVPN_WEB_MODE",
    "VALID_BODY_PER_USER_BAL",
    "VALID_BODY_WAD_SOURCE_AFFINITY",
    "VALID_BODY_LOGIN_TIMESTAMP",
    "VALID_BODY_IP_CONFLICT_DETECTION",
    "VALID_BODY_SPECIAL_FILE_23_SUPPORT",
    "VALID_BODY_LOG_UUID_ADDRESS",
    "VALID_BODY_LOG_SSL_CONNECTION",
    "VALID_BODY_GUI_REST_API_CACHE",
    "VALID_BODY_REST_API_KEY_URL_QUERY",
    "VALID_BODY_IPSEC_QAT_OFFLOAD",
    "VALID_BODY_PRIVATE_DATA_ENCRYPTION",
    "VALID_BODY_AUTO_AUTH_EXTENSION_DEVICE",
    "VALID_BODY_GUI_THEME",
    "VALID_BODY_GUI_DATE_FORMAT",
    "VALID_BODY_GUI_DATE_TIME_SOURCE",
    "VALID_BODY_CLOUD_COMMUNICATION",
    "VALID_BODY_FORTITOKEN_CLOUD",
    "VALID_BODY_FORTITOKEN_CLOUD_PUSH_STATUS",
    "VALID_BODY_IRQ_TIME_ACCOUNTING",
    "VALID_BODY_MANAGEMENT_PORT_USE_ADMIN_SPORT",
    "VALID_BODY_FORTICONVERTER_INTEGRATION",
    "VALID_BODY_FORTICONVERTER_CONFIG_UPLOAD",
    "VALID_BODY_INTERNET_SERVICE_DATABASE",
    "VALID_BODY_GEOIP_FULL_DB",
    "VALID_BODY_EARLY_TCP_NPU_SESSION",
    "VALID_BODY_NPU_NEIGHBOR_UPDATE",
    "VALID_BODY_DELAY_TCP_NPU_SESSION",
    "VALID_BODY_INTERFACE_SUBNET_USAGE",
    "VALID_BODY_FORTIGSLB_INTEGRATION",
    "VALID_BODY_AUTH_SESSION_AUTO_BACKUP",
    "VALID_BODY_AUTH_SESSION_AUTO_BACKUP_INTERVAL",
    "VALID_BODY_APPLICATION_BANDWIDTH_TRACKING",
    "VALID_BODY_TLS_SESSION_CACHE",
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