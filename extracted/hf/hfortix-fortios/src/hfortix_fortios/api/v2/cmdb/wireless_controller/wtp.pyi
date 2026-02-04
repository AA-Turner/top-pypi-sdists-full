""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/wtp
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

class WtpRadio1VapsItem(TypedDict, total=False):
    """Nested item for radio-1.vaps field."""
    name: str


class WtpRadio1ChannelItem(TypedDict, total=False):
    """Nested item for radio-1.channel field."""
    chan: str


class WtpRadio2VapsItem(TypedDict, total=False):
    """Nested item for radio-2.vaps field."""
    name: str


class WtpRadio2ChannelItem(TypedDict, total=False):
    """Nested item for radio-2.channel field."""
    chan: str


class WtpRadio3VapsItem(TypedDict, total=False):
    """Nested item for radio-3.vaps field."""
    name: str


class WtpRadio3ChannelItem(TypedDict, total=False):
    """Nested item for radio-3.channel field."""
    chan: str


class WtpRadio4VapsItem(TypedDict, total=False):
    """Nested item for radio-4.vaps field."""
    name: str


class WtpRadio4ChannelItem(TypedDict, total=False):
    """Nested item for radio-4.channel field."""
    chan: str


class WtpSplittunnelingaclItem(TypedDict, total=False):
    """Nested item for split-tunneling-acl field."""
    id: int
    dest_ip: str


class WtpLanDict(TypedDict, total=False):
    """Nested object type for lan field."""
    port_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port_ssid: str
    port1_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port1_ssid: str
    port2_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port2_ssid: str
    port3_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port3_ssid: str
    port4_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port4_ssid: str
    port5_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port5_ssid: str
    port6_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port6_ssid: str
    port7_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port7_ssid: str
    port8_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port8_ssid: str
    port_esl_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port_esl_ssid: str


class WtpRadio1Dict(TypedDict, total=False):
    """Nested object type for radio-1 field."""
    override_band: Literal["enable", "disable"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    override_txpower: Literal["enable", "disable"]
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    override_vaps: Literal["enable", "disable"]
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str] | list[WtpRadio1VapsItem]
    override_channel: Literal["enable", "disable"]
    channel: str | list[str] | list[WtpRadio1ChannelItem]
    drma_manual_mode: Literal["ap", "monitor", "ncf", "ncf-peek"]


class WtpRadio2Dict(TypedDict, total=False):
    """Nested object type for radio-2 field."""
    override_band: Literal["enable", "disable"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    override_txpower: Literal["enable", "disable"]
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    override_vaps: Literal["enable", "disable"]
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str] | list[WtpRadio2VapsItem]
    override_channel: Literal["enable", "disable"]
    channel: str | list[str] | list[WtpRadio2ChannelItem]
    drma_manual_mode: Literal["ap", "monitor", "ncf", "ncf-peek"]


class WtpRadio3Dict(TypedDict, total=False):
    """Nested object type for radio-3 field."""
    override_band: Literal["enable", "disable"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    override_txpower: Literal["enable", "disable"]
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    override_vaps: Literal["enable", "disable"]
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str] | list[WtpRadio3VapsItem]
    override_channel: Literal["enable", "disable"]
    channel: str | list[str] | list[WtpRadio3ChannelItem]
    drma_manual_mode: Literal["ap", "monitor", "ncf", "ncf-peek"]


class WtpRadio4Dict(TypedDict, total=False):
    """Nested object type for radio-4 field."""
    override_band: Literal["enable", "disable"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    override_txpower: Literal["enable", "disable"]
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    override_vaps: Literal["enable", "disable"]
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str] | list[WtpRadio4VapsItem]
    override_channel: Literal["enable", "disable"]
    channel: str | list[str] | list[WtpRadio4ChannelItem]
    drma_manual_mode: Literal["ap", "monitor", "ncf", "ncf-peek"]


class WtpPayload(TypedDict, total=False):
    """Payload type for Wtp operations."""
    wtp_id: str
    index: int
    uuid: str
    admin: Literal["discovered", "disable", "enable"]
    name: str
    location: str
    comment: str
    region: str
    region_x: str
    region_y: str
    firmware_provision: str
    firmware_provision_latest: Literal["disable", "once"]
    wtp_profile: str
    apcfg_profile: str
    bonjour_profile: str
    ble_major_id: int
    ble_minor_id: int
    override_led_state: Literal["enable", "disable"]
    led_state: Literal["enable", "disable"]
    override_wan_port_mode: Literal["enable", "disable"]
    wan_port_mode: Literal["wan-lan", "wan-only"]
    override_ip_fragment: Literal["enable", "disable"]
    ip_fragment_preventing: str | list[str]
    tun_mtu_uplink: int
    tun_mtu_downlink: int
    override_split_tunnel: Literal["enable", "disable"]
    split_tunneling_acl_path: Literal["tunnel", "local"]
    split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"]
    split_tunneling_acl: str | list[str] | list[WtpSplittunnelingaclItem]
    override_lan: Literal["enable", "disable"]
    lan: WtpLanDict
    override_allowaccess: Literal["enable", "disable"]
    allowaccess: str | list[str]
    override_login_passwd_change: Literal["enable", "disable"]
    login_passwd_change: Literal["yes", "default", "no"]
    login_passwd: str
    override_default_mesh_root: Literal["enable", "disable"]
    default_mesh_root: Literal["enable", "disable"]
    radio_1: WtpRadio1Dict
    radio_2: WtpRadio2Dict
    radio_3: WtpRadio3Dict
    radio_4: WtpRadio4Dict
    image_download: Literal["enable", "disable"]
    mesh_bridge_enable: Literal["default", "enable", "disable"]
    purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    coordinate_latitude: str
    coordinate_longitude: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class WtpResponse(TypedDict, total=False):
    """Response type for Wtp - use with .dict property for typed dict access."""
    wtp_id: str
    index: int
    uuid: str
    admin: Literal["discovered", "disable", "enable"]
    name: str
    location: str
    comment: str
    region: str
    region_x: str
    region_y: str
    firmware_provision: str
    firmware_provision_latest: Literal["disable", "once"]
    wtp_profile: str
    apcfg_profile: str
    bonjour_profile: str
    ble_major_id: int
    ble_minor_id: int
    override_led_state: Literal["enable", "disable"]
    led_state: Literal["enable", "disable"]
    override_wan_port_mode: Literal["enable", "disable"]
    wan_port_mode: Literal["wan-lan", "wan-only"]
    override_ip_fragment: Literal["enable", "disable"]
    ip_fragment_preventing: str
    tun_mtu_uplink: int
    tun_mtu_downlink: int
    override_split_tunnel: Literal["enable", "disable"]
    split_tunneling_acl_path: Literal["tunnel", "local"]
    split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"]
    split_tunneling_acl: list[WtpSplittunnelingaclItem]
    override_lan: Literal["enable", "disable"]
    lan: WtpLanDict
    override_allowaccess: Literal["enable", "disable"]
    allowaccess: str
    override_login_passwd_change: Literal["enable", "disable"]
    login_passwd_change: Literal["yes", "default", "no"]
    login_passwd: str
    override_default_mesh_root: Literal["enable", "disable"]
    default_mesh_root: Literal["enable", "disable"]
    radio_1: WtpRadio1Dict
    radio_2: WtpRadio2Dict
    radio_3: WtpRadio3Dict
    radio_4: WtpRadio4Dict
    image_download: Literal["enable", "disable"]
    mesh_bridge_enable: Literal["default", "enable", "disable"]
    purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    coordinate_latitude: str
    coordinate_longitude: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class WtpSplittunnelingaclItemObject(FortiObject[WtpSplittunnelingaclItem]):
    """Typed object for split-tunneling-acl table items with attribute access."""
    id: int
    dest_ip: str


class WtpRadio1VapsItemObject(FortiObject[WtpRadio1VapsItem]):
    """Typed object for radio-1.vaps table items with attribute access."""
    name: str


class WtpRadio1ChannelItemObject(FortiObject[WtpRadio1ChannelItem]):
    """Typed object for radio-1.channel table items with attribute access."""
    chan: str


class WtpRadio2VapsItemObject(FortiObject[WtpRadio2VapsItem]):
    """Typed object for radio-2.vaps table items with attribute access."""
    name: str


class WtpRadio2ChannelItemObject(FortiObject[WtpRadio2ChannelItem]):
    """Typed object for radio-2.channel table items with attribute access."""
    chan: str


class WtpRadio3VapsItemObject(FortiObject[WtpRadio3VapsItem]):
    """Typed object for radio-3.vaps table items with attribute access."""
    name: str


class WtpRadio3ChannelItemObject(FortiObject[WtpRadio3ChannelItem]):
    """Typed object for radio-3.channel table items with attribute access."""
    chan: str


class WtpRadio4VapsItemObject(FortiObject[WtpRadio4VapsItem]):
    """Typed object for radio-4.vaps table items with attribute access."""
    name: str


class WtpRadio4ChannelItemObject(FortiObject[WtpRadio4ChannelItem]):
    """Typed object for radio-4.channel table items with attribute access."""
    chan: str


class WtpLanObject(FortiObject):
    """Nested object for lan field with attribute access."""
    port_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port_ssid: str
    port1_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port1_ssid: str
    port2_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port2_ssid: str
    port3_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port3_ssid: str
    port4_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port4_ssid: str
    port5_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port5_ssid: str
    port6_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port6_ssid: str
    port7_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port7_ssid: str
    port8_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port8_ssid: str
    port_esl_mode: Literal["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"]
    port_esl_ssid: str


class WtpRadio1Object(FortiObject):
    """Nested object for radio-1 field with attribute access."""
    override_band: Literal["enable", "disable"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    override_txpower: Literal["enable", "disable"]
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    override_vaps: Literal["enable", "disable"]
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str]
    override_channel: Literal["enable", "disable"]
    channel: str | list[str]
    drma_manual_mode: Literal["ap", "monitor", "ncf", "ncf-peek"]


class WtpRadio2Object(FortiObject):
    """Nested object for radio-2 field with attribute access."""
    override_band: Literal["enable", "disable"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    override_txpower: Literal["enable", "disable"]
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    override_vaps: Literal["enable", "disable"]
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str]
    override_channel: Literal["enable", "disable"]
    channel: str | list[str]
    drma_manual_mode: Literal["ap", "monitor", "ncf", "ncf-peek"]


class WtpRadio3Object(FortiObject):
    """Nested object for radio-3 field with attribute access."""
    override_band: Literal["enable", "disable"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    override_txpower: Literal["enable", "disable"]
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    override_vaps: Literal["enable", "disable"]
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str]
    override_channel: Literal["enable", "disable"]
    channel: str | list[str]
    drma_manual_mode: Literal["ap", "monitor", "ncf", "ncf-peek"]


class WtpRadio4Object(FortiObject):
    """Nested object for radio-4 field with attribute access."""
    override_band: Literal["enable", "disable"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    override_txpower: Literal["enable", "disable"]
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    override_vaps: Literal["enable", "disable"]
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str]
    override_channel: Literal["enable", "disable"]
    channel: str | list[str]
    drma_manual_mode: Literal["ap", "monitor", "ncf", "ncf-peek"]


class WtpObject(FortiObject):
    """Typed FortiObject for Wtp with field access."""
    wtp_id: str
    index: int
    uuid: str
    admin: Literal["discovered", "disable", "enable"]
    name: str
    location: str
    comment: str
    region: str
    region_x: str
    region_y: str
    firmware_provision: str
    firmware_provision_latest: Literal["disable", "once"]
    wtp_profile: str
    apcfg_profile: str
    bonjour_profile: str
    ble_major_id: int
    ble_minor_id: int
    override_led_state: Literal["enable", "disable"]
    led_state: Literal["enable", "disable"]
    override_wan_port_mode: Literal["enable", "disable"]
    wan_port_mode: Literal["wan-lan", "wan-only"]
    override_ip_fragment: Literal["enable", "disable"]
    ip_fragment_preventing: str
    tun_mtu_uplink: int
    tun_mtu_downlink: int
    override_split_tunnel: Literal["enable", "disable"]
    split_tunneling_acl_path: Literal["tunnel", "local"]
    split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"]
    split_tunneling_acl: FortiObjectList[WtpSplittunnelingaclItemObject]
    override_lan: Literal["enable", "disable"]
    lan: WtpLanObject
    override_allowaccess: Literal["enable", "disable"]
    allowaccess: str
    override_login_passwd_change: Literal["enable", "disable"]
    login_passwd_change: Literal["yes", "default", "no"]
    login_passwd: str
    override_default_mesh_root: Literal["enable", "disable"]
    default_mesh_root: Literal["enable", "disable"]
    radio_1: WtpRadio1Object
    radio_2: WtpRadio2Object
    radio_3: WtpRadio3Object
    radio_4: WtpRadio4Object
    image_download: Literal["enable", "disable"]
    mesh_bridge_enable: Literal["default", "enable", "disable"]
    purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    coordinate_latitude: str
    coordinate_longitude: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Wtp:
    """
    
    Endpoint: wireless_controller/wtp
    Category: cmdb
    MKey: wtp-id
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
        wtp_id: str,
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
    ) -> WtpObject: ...
    
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
    ) -> FortiObjectList[WtpObject]: ...
    
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
        payload_dict: WtpPayload | None = ...,
        wtp_id: str | None = ...,
        index: int | None = ...,
        uuid: str | None = ...,
        admin: Literal["discovered", "disable", "enable"] | None = ...,
        name: str | None = ...,
        location: str | None = ...,
        comment: str | None = ...,
        region: str | None = ...,
        region_x: str | None = ...,
        region_y: str | None = ...,
        firmware_provision: str | None = ...,
        firmware_provision_latest: Literal["disable", "once"] | None = ...,
        wtp_profile: str | None = ...,
        apcfg_profile: str | None = ...,
        bonjour_profile: str | None = ...,
        ble_major_id: int | None = ...,
        ble_minor_id: int | None = ...,
        override_led_state: Literal["enable", "disable"] | None = ...,
        led_state: Literal["enable", "disable"] | None = ...,
        override_wan_port_mode: Literal["enable", "disable"] | None = ...,
        wan_port_mode: Literal["wan-lan", "wan-only"] | None = ...,
        override_ip_fragment: Literal["enable", "disable"] | None = ...,
        ip_fragment_preventing: str | list[str] | None = ...,
        tun_mtu_uplink: int | None = ...,
        tun_mtu_downlink: int | None = ...,
        override_split_tunnel: Literal["enable", "disable"] | None = ...,
        split_tunneling_acl_path: Literal["tunnel", "local"] | None = ...,
        split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = ...,
        split_tunneling_acl: str | list[str] | list[WtpSplittunnelingaclItem] | None = ...,
        override_lan: Literal["enable", "disable"] | None = ...,
        lan: WtpLanDict | None = ...,
        override_allowaccess: Literal["enable", "disable"] | None = ...,
        allowaccess: str | list[str] | None = ...,
        override_login_passwd_change: Literal["enable", "disable"] | None = ...,
        login_passwd_change: Literal["yes", "default", "no"] | None = ...,
        login_passwd: str | None = ...,
        override_default_mesh_root: Literal["enable", "disable"] | None = ...,
        default_mesh_root: Literal["enable", "disable"] | None = ...,
        radio_1: WtpRadio1Dict | None = ...,
        radio_2: WtpRadio2Dict | None = ...,
        radio_3: WtpRadio3Dict | None = ...,
        radio_4: WtpRadio4Dict | None = ...,
        image_download: Literal["enable", "disable"] | None = ...,
        mesh_bridge_enable: Literal["default", "enable", "disable"] | None = ...,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        coordinate_latitude: str | None = ...,
        coordinate_longitude: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WtpObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: WtpPayload | None = ...,
        wtp_id: str | None = ...,
        index: int | None = ...,
        uuid: str | None = ...,
        admin: Literal["discovered", "disable", "enable"] | None = ...,
        name: str | None = ...,
        location: str | None = ...,
        comment: str | None = ...,
        region: str | None = ...,
        region_x: str | None = ...,
        region_y: str | None = ...,
        firmware_provision: str | None = ...,
        firmware_provision_latest: Literal["disable", "once"] | None = ...,
        wtp_profile: str | None = ...,
        apcfg_profile: str | None = ...,
        bonjour_profile: str | None = ...,
        ble_major_id: int | None = ...,
        ble_minor_id: int | None = ...,
        override_led_state: Literal["enable", "disable"] | None = ...,
        led_state: Literal["enable", "disable"] | None = ...,
        override_wan_port_mode: Literal["enable", "disable"] | None = ...,
        wan_port_mode: Literal["wan-lan", "wan-only"] | None = ...,
        override_ip_fragment: Literal["enable", "disable"] | None = ...,
        ip_fragment_preventing: str | list[str] | None = ...,
        tun_mtu_uplink: int | None = ...,
        tun_mtu_downlink: int | None = ...,
        override_split_tunnel: Literal["enable", "disable"] | None = ...,
        split_tunneling_acl_path: Literal["tunnel", "local"] | None = ...,
        split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = ...,
        split_tunneling_acl: str | list[str] | list[WtpSplittunnelingaclItem] | None = ...,
        override_lan: Literal["enable", "disable"] | None = ...,
        lan: WtpLanDict | None = ...,
        override_allowaccess: Literal["enable", "disable"] | None = ...,
        allowaccess: str | list[str] | None = ...,
        override_login_passwd_change: Literal["enable", "disable"] | None = ...,
        login_passwd_change: Literal["yes", "default", "no"] | None = ...,
        login_passwd: str | None = ...,
        override_default_mesh_root: Literal["enable", "disable"] | None = ...,
        default_mesh_root: Literal["enable", "disable"] | None = ...,
        radio_1: WtpRadio1Dict | None = ...,
        radio_2: WtpRadio2Dict | None = ...,
        radio_3: WtpRadio3Dict | None = ...,
        radio_4: WtpRadio4Dict | None = ...,
        image_download: Literal["enable", "disable"] | None = ...,
        mesh_bridge_enable: Literal["default", "enable", "disable"] | None = ...,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        coordinate_latitude: str | None = ...,
        coordinate_longitude: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WtpObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        wtp_id: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        wtp_id: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_wtp_id: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        wtp_id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: WtpPayload | None = ...,
        wtp_id: str | None = ...,
        index: int | None = ...,
        uuid: str | None = ...,
        admin: Literal["discovered", "disable", "enable"] | None = ...,
        name: str | None = ...,
        location: str | None = ...,
        comment: str | None = ...,
        region: str | None = ...,
        region_x: str | None = ...,
        region_y: str | None = ...,
        firmware_provision: str | None = ...,
        firmware_provision_latest: Literal["disable", "once"] | None = ...,
        wtp_profile: str | None = ...,
        apcfg_profile: str | None = ...,
        bonjour_profile: str | None = ...,
        ble_major_id: int | None = ...,
        ble_minor_id: int | None = ...,
        override_led_state: Literal["enable", "disable"] | None = ...,
        led_state: Literal["enable", "disable"] | None = ...,
        override_wan_port_mode: Literal["enable", "disable"] | None = ...,
        wan_port_mode: Literal["wan-lan", "wan-only"] | None = ...,
        override_ip_fragment: Literal["enable", "disable"] | None = ...,
        ip_fragment_preventing: Literal["tcp-mss-adjust", "icmp-unreachable"] | list[str] | None = ...,
        tun_mtu_uplink: int | None = ...,
        tun_mtu_downlink: int | None = ...,
        override_split_tunnel: Literal["enable", "disable"] | None = ...,
        split_tunneling_acl_path: Literal["tunnel", "local"] | None = ...,
        split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = ...,
        split_tunneling_acl: str | list[str] | list[WtpSplittunnelingaclItem] | None = ...,
        override_lan: Literal["enable", "disable"] | None = ...,
        lan: WtpLanDict | None = ...,
        override_allowaccess: Literal["enable", "disable"] | None = ...,
        allowaccess: Literal["https", "ssh", "snmp"] | list[str] | None = ...,
        override_login_passwd_change: Literal["enable", "disable"] | None = ...,
        login_passwd_change: Literal["yes", "default", "no"] | None = ...,
        login_passwd: str | None = ...,
        override_default_mesh_root: Literal["enable", "disable"] | None = ...,
        default_mesh_root: Literal["enable", "disable"] | None = ...,
        radio_1: WtpRadio1Dict | None = ...,
        radio_2: WtpRadio2Dict | None = ...,
        radio_3: WtpRadio3Dict | None = ...,
        radio_4: WtpRadio4Dict | None = ...,
        image_download: Literal["enable", "disable"] | None = ...,
        mesh_bridge_enable: Literal["default", "enable", "disable"] | None = ...,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        coordinate_latitude: str | None = ...,
        coordinate_longitude: str | None = ...,
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
    "Wtp",
    "WtpPayload",
    "WtpResponse",
    "WtpObject",
]