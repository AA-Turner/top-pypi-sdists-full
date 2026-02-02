""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: extension_controller/extender_profile
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class ExtenderProfileCellularDataplanItem(TypedDict, total=False):
    """Nested item for cellular.dataplan field."""
    name: str


class ExtenderProfileCellularControllerreportDict(TypedDict, total=False):
    """Nested object type for cellular.controller-report field."""
    status: Literal["disable", "enable"]
    interval: int
    signal_threshold: int


class ExtenderProfileCellularSmsnotificationDict(TypedDict, total=False):
    """Nested object type for cellular.sms-notification field."""
    status: Literal["disable", "enable"]
    alert: str
    receiver: str | list[str]


class ExtenderProfileCellularModem1Dict(TypedDict, total=False):
    """Nested object type for cellular.modem1 field."""
    redundant_mode: Literal["disable", "enable"]
    redundant_intf: str
    conn_status: int
    default_sim: Literal["sim1", "sim2", "carrier", "cost"]
    gps: Literal["disable", "enable"]
    sim1_pin: Literal["disable", "enable"]
    sim2_pin: Literal["disable", "enable"]
    sim1_pin_code: str
    sim2_pin_code: str
    preferred_carrier: str
    auto_switch: str
    multiple_PDN: Literal["disable", "enable"]
    pdn1_dataplan: str
    pdn2_dataplan: str
    pdn3_dataplan: str
    pdn4_dataplan: str


class ExtenderProfileCellularModem2Dict(TypedDict, total=False):
    """Nested object type for cellular.modem2 field."""
    redundant_mode: Literal["disable", "enable"]
    redundant_intf: str
    conn_status: int
    default_sim: Literal["sim1", "sim2", "carrier", "cost"]
    gps: Literal["disable", "enable"]
    sim1_pin: Literal["disable", "enable"]
    sim2_pin: Literal["disable", "enable"]
    sim1_pin_code: str
    sim2_pin_code: str
    preferred_carrier: str
    auto_switch: str
    multiple_PDN: Literal["disable", "enable"]
    pdn1_dataplan: str
    pdn2_dataplan: str
    pdn3_dataplan: str
    pdn4_dataplan: str


class ExtenderProfileWifiRadio1Dict(TypedDict, total=False):
    """Nested object type for wifi.radio-1 field."""
    mode: Literal["AP", "Client"]
    band: Literal["2.4GHz"]
    status: Literal["disable", "enable"]
    operating_standard: Literal["auto", "11A-N-AC-AX", "11A-N-AC", "11A-N", "11A", "11N-AC-AX", "11AC-AX", "11AC", "11N-AC", "11B-G-N-AX", "11B-G-N", "11B-G", "11B", "11G-N-AX", "11N-AX", "11AX", "11G-N", "11N", "11G"]
    guard_interval: Literal["auto", "400ns", "800ns"]
    channel: Literal["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11"]
    bandwidth: Literal["auto", "20MHz", "40MHz", "80MHz"]
    power_level: int
    beacon_interval: int
    x80211d: Literal["disable", "enable"]
    max_clients: int
    extension_channel: Literal["auto", "higher", "lower"]
    bss_color_mode: Literal["auto", "static"]
    bss_color: int
    lan_ext_vap: str
    local_vaps: str | list[str]


class ExtenderProfileWifiRadio2Dict(TypedDict, total=False):
    """Nested object type for wifi.radio-2 field."""
    mode: Literal["AP", "Client"]
    band: Literal["5GHz"]
    status: Literal["disable", "enable"]
    operating_standard: Literal["auto", "11A-N-AC-AX", "11A-N-AC", "11A-N", "11A", "11N-AC-AX", "11AC-AX", "11AC", "11N-AC", "11B-G-N-AX", "11B-G-N", "11B-G", "11B", "11G-N-AX", "11N-AX", "11AX", "11G-N", "11N", "11G"]
    guard_interval: Literal["auto", "400ns", "800ns"]
    channel: Literal["CH36", "CH40", "CH44", "CH48", "CH52", "CH56", "CH60", "CH64", "CH100", "CH104", "CH108", "CH112", "CH116", "CH120", "CH124", "CH128", "CH132", "CH136", "CH140", "CH144", "CH149", "CH153", "CH157", "CH161", "CH165"]
    bandwidth: Literal["auto", "20MHz", "40MHz", "80MHz"]
    power_level: int
    beacon_interval: int
    x80211d: Literal["disable", "enable"]
    max_clients: int
    extension_channel: Literal["auto", "higher", "lower"]
    bss_color_mode: Literal["auto", "static"]
    bss_color: int
    lan_ext_vap: str
    local_vaps: str | list[str]


class ExtenderProfileLanextensionBackhaulItem(TypedDict, total=False):
    """Nested item for lan-extension.backhaul field."""
    name: str
    port: Literal["wan", "lte1", "lte2", "port1", "port2", "port3", "port4", "port5", "sfp"]
    role: Literal["primary", "secondary"]
    weight: int
    health_check_interval: int
    health_check_probe_cnt: int
    health_check_probe_tm: int
    health_check_fail_cnt: int
    health_check_recovery_cnt: int


class ExtenderProfileLanextensionDownlinksItem(TypedDict, total=False):
    """Nested item for lan-extension.downlinks field."""
    name: str
    type: Literal["port", "vap"]
    port: Literal["port1", "port2", "port3", "port4", "port5", "lan1", "lan2", "lan"]
    vap: str
    pvid: int
    vids: str | list[str]


class ExtenderProfileLanextensionTrafficsplitservicesItem(TypedDict, total=False):
    """Nested item for lan-extension.traffic-split-services field."""
    name: str
    vsdb: Literal["disable", "enable"]
    address: str
    service: str


class ExtenderProfileCellularDict(TypedDict, total=False):
    """Nested object type for cellular field."""
    dataplan: str | list[str] | list[ExtenderProfileCellularDataplanItem]
    controller_report: ExtenderProfileCellularControllerreportDict
    sms_notification: ExtenderProfileCellularSmsnotificationDict
    modem1: ExtenderProfileCellularModem1Dict
    modem2: ExtenderProfileCellularModem2Dict


class ExtenderProfileWifiDict(TypedDict, total=False):
    """Nested object type for wifi field."""
    country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"]
    radio_1: ExtenderProfileWifiRadio1Dict
    radio_2: ExtenderProfileWifiRadio2Dict


class ExtenderProfileLanextensionDict(TypedDict, total=False):
    """Nested object type for lan-extension field."""
    link_loadbalance: Literal["activebackup", "loadbalance"]
    ipsec_tunnel: str
    backhaul_interface: str
    backhaul_ip: str
    backhaul: str | list[str] | list[ExtenderProfileLanextensionBackhaulItem]
    downlinks: str | list[str] | list[ExtenderProfileLanextensionDownlinksItem]
    traffic_split_services: str | list[str] | list[ExtenderProfileLanextensionTrafficsplitservicesItem]


class ExtenderProfilePayload(TypedDict, total=False):
    """Payload type for ExtenderProfile operations."""
    name: str
    id: int
    model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"]
    extension: Literal["wan-extension", "lan-extension"]
    allowaccess: str | list[str]
    login_password_change: Literal["yes", "default", "no"]
    login_password: str
    enforce_bandwidth: Literal["enable", "disable"]
    bandwidth_limit: int
    cellular: ExtenderProfileCellularDict
    wifi: ExtenderProfileWifiDict
    lan_extension: ExtenderProfileLanextensionDict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ExtenderProfileResponse(TypedDict, total=False):
    """Response type for ExtenderProfile - use with .dict property for typed dict access."""
    name: str
    id: int
    model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"]
    extension: Literal["wan-extension", "lan-extension"]
    allowaccess: str
    login_password_change: Literal["yes", "default", "no"]
    login_password: str
    enforce_bandwidth: Literal["enable", "disable"]
    bandwidth_limit: int
    cellular: ExtenderProfileCellularDict
    wifi: ExtenderProfileWifiDict
    lan_extension: ExtenderProfileLanextensionDict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ExtenderProfileCellularDataplanItemObject(FortiObject[ExtenderProfileCellularDataplanItem]):
    """Typed object for cellular.dataplan table items with attribute access."""
    name: str


class ExtenderProfileLanextensionBackhaulItemObject(FortiObject[ExtenderProfileLanextensionBackhaulItem]):
    """Typed object for lan-extension.backhaul table items with attribute access."""
    name: str
    port: Literal["wan", "lte1", "lte2", "port1", "port2", "port3", "port4", "port5", "sfp"]
    role: Literal["primary", "secondary"]
    weight: int
    health_check_interval: int
    health_check_probe_cnt: int
    health_check_probe_tm: int
    health_check_fail_cnt: int
    health_check_recovery_cnt: int


class ExtenderProfileLanextensionDownlinksItemObject(FortiObject[ExtenderProfileLanextensionDownlinksItem]):
    """Typed object for lan-extension.downlinks table items with attribute access."""
    name: str
    type: Literal["port", "vap"]
    port: Literal["port1", "port2", "port3", "port4", "port5", "lan1", "lan2", "lan"]
    vap: str
    pvid: int
    vids: str | list[str]


class ExtenderProfileLanextensionTrafficsplitservicesItemObject(FortiObject[ExtenderProfileLanextensionTrafficsplitservicesItem]):
    """Typed object for lan-extension.traffic-split-services table items with attribute access."""
    name: str
    vsdb: Literal["disable", "enable"]
    address: str
    service: str


class ExtenderProfileCellularObject(FortiObject):
    """Nested object for cellular field with attribute access."""
    dataplan: str | list[str]
    controller_report: str
    sms_notification: str
    modem1: str
    modem2: str


class ExtenderProfileWifiObject(FortiObject):
    """Nested object for wifi field with attribute access."""
    country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"]
    radio_1: str
    radio_2: str


class ExtenderProfileLanextensionObject(FortiObject):
    """Nested object for lan-extension field with attribute access."""
    link_loadbalance: Literal["activebackup", "loadbalance"]
    ipsec_tunnel: str
    backhaul_interface: str
    backhaul_ip: str
    backhaul: str | list[str]
    downlinks: str | list[str]
    traffic_split_services: str | list[str]


class ExtenderProfileObject(FortiObject):
    """Typed FortiObject for ExtenderProfile with field access."""
    name: str
    id: int
    model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"]
    extension: Literal["wan-extension", "lan-extension"]
    allowaccess: str
    login_password_change: Literal["yes", "default", "no"]
    login_password: str
    enforce_bandwidth: Literal["enable", "disable"]
    bandwidth_limit: int
    cellular: ExtenderProfileCellularObject
    wifi: ExtenderProfileWifiObject
    lan_extension: ExtenderProfileLanextensionObject


# ================================================================
# Main Endpoint Class
# ================================================================

class ExtenderProfile:
    """
    
    Endpoint: extension_controller/extender_profile
    Category: cmdb
    MKey: name
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        name: str,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExtenderProfileObject: ...
    
    @overload
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[ExtenderProfileObject]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: str | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: ExtenderProfileCellularDict | None = ...,
        wifi: ExtenderProfileWifiDict | None = ...,
        lan_extension: ExtenderProfileLanextensionDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExtenderProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: str | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: ExtenderProfileCellularDict | None = ...,
        wifi: ExtenderProfileWifiDict | None = ...,
        lan_extension: ExtenderProfileLanextensionDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExtenderProfileObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: ExtenderProfileCellularDict | None = ...,
        wifi: ExtenderProfileWifiDict | None = ...,
        lan_extension: ExtenderProfileLanextensionDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...
    
    # Helper methods
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> list[str] | list[dict[str, Any]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> FortiObject[Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> FortiObject[Any]: ...
    
    @staticmethod
    def schema() -> FortiObject[Any]: ...


__all__ = [
    "ExtenderProfile",
    "ExtenderProfilePayload",
    "ExtenderProfileResponse",
    "ExtenderProfileObject",
]