from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_SENSOR_MODE: Literal["disable", "foreign", "both"]
VALID_BODY_AP_SCAN: Literal["disable", "enable"]
VALID_BODY_AP_SCAN_PASSIVE: Literal["enable", "disable"]
VALID_BODY_AP_AUTO_SUPPRESS: Literal["enable", "disable"]
VALID_BODY_WIRELESS_BRIDGE: Literal["enable", "disable"]
VALID_BODY_DEAUTH_BROADCAST: Literal["enable", "disable"]
VALID_BODY_NULL_SSID_PROBE_RESP: Literal["enable", "disable"]
VALID_BODY_LONG_DURATION_ATTACK: Literal["enable", "disable"]
VALID_BODY_INVALID_MAC_OUI: Literal["enable", "disable"]
VALID_BODY_WEAK_WEP_IV: Literal["enable", "disable"]
VALID_BODY_AUTH_FRAME_FLOOD: Literal["enable", "disable"]
VALID_BODY_ASSOC_FRAME_FLOOD: Literal["enable", "disable"]
VALID_BODY_REASSOC_FLOOD: Literal["enable", "disable"]
VALID_BODY_PROBE_FLOOD: Literal["enable", "disable"]
VALID_BODY_BCN_FLOOD: Literal["enable", "disable"]
VALID_BODY_RTS_FLOOD: Literal["enable", "disable"]
VALID_BODY_CTS_FLOOD: Literal["enable", "disable"]
VALID_BODY_CLIENT_FLOOD: Literal["enable", "disable"]
VALID_BODY_BLOCK_ACK_FLOOD: Literal["enable", "disable"]
VALID_BODY_PSPOLL_FLOOD: Literal["enable", "disable"]
VALID_BODY_NETSTUMBLER: Literal["enable", "disable"]
VALID_BODY_WELLENREITER: Literal["enable", "disable"]
VALID_BODY_SPOOFED_DEAUTH: Literal["enable", "disable"]
VALID_BODY_ASLEAP_ATTACK: Literal["enable", "disable"]
VALID_BODY_EAPOL_START_FLOOD: Literal["enable", "disable"]
VALID_BODY_EAPOL_LOGOFF_FLOOD: Literal["enable", "disable"]
VALID_BODY_EAPOL_SUCC_FLOOD: Literal["enable", "disable"]
VALID_BODY_EAPOL_FAIL_FLOOD: Literal["enable", "disable"]
VALID_BODY_EAPOL_PRE_SUCC_FLOOD: Literal["enable", "disable"]
VALID_BODY_EAPOL_PRE_FAIL_FLOOD: Literal["enable", "disable"]
VALID_BODY_WINDOWS_BRIDGE: Literal["enable", "disable"]
VALID_BODY_DISASSOC_BROADCAST: Literal["enable", "disable"]
VALID_BODY_AP_SPOOFING: Literal["enable", "disable"]
VALID_BODY_CHAN_BASED_MITM: Literal["enable", "disable"]
VALID_BODY_ADHOC_VALID_SSID: Literal["enable", "disable"]
VALID_BODY_ADHOC_NETWORK: Literal["enable", "disable"]
VALID_BODY_EAPOL_KEY_OVERFLOW: Literal["enable", "disable"]
VALID_BODY_AP_IMPERSONATION: Literal["enable", "disable"]
VALID_BODY_INVALID_ADDR_COMBINATION: Literal["enable", "disable"]
VALID_BODY_BEACON_WRONG_CHANNEL: Literal["enable", "disable"]
VALID_BODY_HT_GREENFIELD: Literal["enable", "disable"]
VALID_BODY_OVERFLOW_IE: Literal["enable", "disable"]
VALID_BODY_MALFORMED_HT_IE: Literal["enable", "disable"]
VALID_BODY_MALFORMED_AUTH: Literal["enable", "disable"]
VALID_BODY_MALFORMED_ASSOCIATION: Literal["enable", "disable"]
VALID_BODY_HT_40MHZ_INTOLERANCE: Literal["enable", "disable"]
VALID_BODY_VALID_SSID_MISUSE: Literal["enable", "disable"]
VALID_BODY_VALID_CLIENT_MISASSOCIATION: Literal["enable", "disable"]
VALID_BODY_HOTSPOTTER_ATTACK: Literal["enable", "disable"]
VALID_BODY_PWSAVE_DOS_ATTACK: Literal["enable", "disable"]
VALID_BODY_OMERTA_ATTACK: Literal["enable", "disable"]
VALID_BODY_DISCONNECT_STATION: Literal["enable", "disable"]
VALID_BODY_UNENCRYPTED_VALID: Literal["enable", "disable"]
VALID_BODY_FATA_JACK: Literal["enable", "disable"]
VALID_BODY_RISKY_ENCRYPTION: Literal["enable", "disable"]
VALID_BODY_FUZZED_BEACON: Literal["enable", "disable"]
VALID_BODY_FUZZED_PROBE_REQUEST: Literal["enable", "disable"]
VALID_BODY_FUZZED_PROBE_RESPONSE: Literal["enable", "disable"]
VALID_BODY_AIR_JACK: Literal["enable", "disable"]
VALID_BODY_WPA_FT_ATTACK: Literal["enable", "disable"]

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
    "VALID_BODY_SENSOR_MODE",
    "VALID_BODY_AP_SCAN",
    "VALID_BODY_AP_SCAN_PASSIVE",
    "VALID_BODY_AP_AUTO_SUPPRESS",
    "VALID_BODY_WIRELESS_BRIDGE",
    "VALID_BODY_DEAUTH_BROADCAST",
    "VALID_BODY_NULL_SSID_PROBE_RESP",
    "VALID_BODY_LONG_DURATION_ATTACK",
    "VALID_BODY_INVALID_MAC_OUI",
    "VALID_BODY_WEAK_WEP_IV",
    "VALID_BODY_AUTH_FRAME_FLOOD",
    "VALID_BODY_ASSOC_FRAME_FLOOD",
    "VALID_BODY_REASSOC_FLOOD",
    "VALID_BODY_PROBE_FLOOD",
    "VALID_BODY_BCN_FLOOD",
    "VALID_BODY_RTS_FLOOD",
    "VALID_BODY_CTS_FLOOD",
    "VALID_BODY_CLIENT_FLOOD",
    "VALID_BODY_BLOCK_ACK_FLOOD",
    "VALID_BODY_PSPOLL_FLOOD",
    "VALID_BODY_NETSTUMBLER",
    "VALID_BODY_WELLENREITER",
    "VALID_BODY_SPOOFED_DEAUTH",
    "VALID_BODY_ASLEAP_ATTACK",
    "VALID_BODY_EAPOL_START_FLOOD",
    "VALID_BODY_EAPOL_LOGOFF_FLOOD",
    "VALID_BODY_EAPOL_SUCC_FLOOD",
    "VALID_BODY_EAPOL_FAIL_FLOOD",
    "VALID_BODY_EAPOL_PRE_SUCC_FLOOD",
    "VALID_BODY_EAPOL_PRE_FAIL_FLOOD",
    "VALID_BODY_WINDOWS_BRIDGE",
    "VALID_BODY_DISASSOC_BROADCAST",
    "VALID_BODY_AP_SPOOFING",
    "VALID_BODY_CHAN_BASED_MITM",
    "VALID_BODY_ADHOC_VALID_SSID",
    "VALID_BODY_ADHOC_NETWORK",
    "VALID_BODY_EAPOL_KEY_OVERFLOW",
    "VALID_BODY_AP_IMPERSONATION",
    "VALID_BODY_INVALID_ADDR_COMBINATION",
    "VALID_BODY_BEACON_WRONG_CHANNEL",
    "VALID_BODY_HT_GREENFIELD",
    "VALID_BODY_OVERFLOW_IE",
    "VALID_BODY_MALFORMED_HT_IE",
    "VALID_BODY_MALFORMED_AUTH",
    "VALID_BODY_MALFORMED_ASSOCIATION",
    "VALID_BODY_HT_40MHZ_INTOLERANCE",
    "VALID_BODY_VALID_SSID_MISUSE",
    "VALID_BODY_VALID_CLIENT_MISASSOCIATION",
    "VALID_BODY_HOTSPOTTER_ATTACK",
    "VALID_BODY_PWSAVE_DOS_ATTACK",
    "VALID_BODY_OMERTA_ATTACK",
    "VALID_BODY_DISCONNECT_STATION",
    "VALID_BODY_UNENCRYPTED_VALID",
    "VALID_BODY_FATA_JACK",
    "VALID_BODY_RISKY_ENCRYPTION",
    "VALID_BODY_FUZZED_BEACON",
    "VALID_BODY_FUZZED_PROBE_REQUEST",
    "VALID_BODY_FUZZED_PROBE_RESPONSE",
    "VALID_BODY_AIR_JACK",
    "VALID_BODY_WPA_FT_ATTACK",
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