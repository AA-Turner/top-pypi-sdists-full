""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/wids_profile
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

class WidsProfileApscanchannellist2g5gItem(TypedDict, total=False):
    """Nested item for ap-scan-channel-list-2G-5G field."""
    chan: str


class WidsProfileApscanchannellist6gItem(TypedDict, total=False):
    """Nested item for ap-scan-channel-list-6G field."""
    chan: str


class WidsProfileApbgscandisableschedulesItem(TypedDict, total=False):
    """Nested item for ap-bgscan-disable-schedules field."""
    name: str


class WidsProfilePayload(TypedDict, total=False):
    """Payload type for WidsProfile operations."""
    name: str
    comment: str
    sensor_mode: Literal["disable", "foreign", "both"]
    ap_scan: Literal["disable", "enable"]
    ap_scan_channel_list_2G_5G: str | list[str] | list[WidsProfileApscanchannellist2g5gItem]
    ap_scan_channel_list_6G: str | list[str] | list[WidsProfileApscanchannellist6gItem]
    ap_bgscan_period: int
    ap_bgscan_intv: int
    ap_bgscan_duration: int
    ap_bgscan_idle: int
    ap_bgscan_report_intv: int
    ap_bgscan_disable_schedules: str | list[str] | list[WidsProfileApbgscandisableschedulesItem]
    ap_fgscan_report_intv: int
    ap_scan_passive: Literal["enable", "disable"]
    ap_scan_threshold: str
    ap_auto_suppress: Literal["enable", "disable"]
    wireless_bridge: Literal["enable", "disable"]
    deauth_broadcast: Literal["enable", "disable"]
    null_ssid_probe_resp: Literal["enable", "disable"]
    long_duration_attack: Literal["enable", "disable"]
    long_duration_thresh: int
    invalid_mac_oui: Literal["enable", "disable"]
    weak_wep_iv: Literal["enable", "disable"]
    auth_frame_flood: Literal["enable", "disable"]
    auth_flood_time: int
    auth_flood_thresh: int
    assoc_frame_flood: Literal["enable", "disable"]
    assoc_flood_time: int
    assoc_flood_thresh: int
    reassoc_flood: Literal["enable", "disable"]
    reassoc_flood_time: int
    reassoc_flood_thresh: int
    probe_flood: Literal["enable", "disable"]
    probe_flood_time: int
    probe_flood_thresh: int
    bcn_flood: Literal["enable", "disable"]
    bcn_flood_time: int
    bcn_flood_thresh: int
    rts_flood: Literal["enable", "disable"]
    rts_flood_time: int
    rts_flood_thresh: int
    cts_flood: Literal["enable", "disable"]
    cts_flood_time: int
    cts_flood_thresh: int
    client_flood: Literal["enable", "disable"]
    client_flood_time: int
    client_flood_thresh: int
    block_ack_flood: Literal["enable", "disable"]
    block_ack_flood_time: int
    block_ack_flood_thresh: int
    pspoll_flood: Literal["enable", "disable"]
    pspoll_flood_time: int
    pspoll_flood_thresh: int
    netstumbler: Literal["enable", "disable"]
    netstumbler_time: int
    netstumbler_thresh: int
    wellenreiter: Literal["enable", "disable"]
    wellenreiter_time: int
    wellenreiter_thresh: int
    spoofed_deauth: Literal["enable", "disable"]
    asleap_attack: Literal["enable", "disable"]
    eapol_start_flood: Literal["enable", "disable"]
    eapol_start_thresh: int
    eapol_start_intv: int
    eapol_logoff_flood: Literal["enable", "disable"]
    eapol_logoff_thresh: int
    eapol_logoff_intv: int
    eapol_succ_flood: Literal["enable", "disable"]
    eapol_succ_thresh: int
    eapol_succ_intv: int
    eapol_fail_flood: Literal["enable", "disable"]
    eapol_fail_thresh: int
    eapol_fail_intv: int
    eapol_pre_succ_flood: Literal["enable", "disable"]
    eapol_pre_succ_thresh: int
    eapol_pre_succ_intv: int
    eapol_pre_fail_flood: Literal["enable", "disable"]
    eapol_pre_fail_thresh: int
    eapol_pre_fail_intv: int
    deauth_unknown_src_thresh: int
    windows_bridge: Literal["enable", "disable"]
    disassoc_broadcast: Literal["enable", "disable"]
    ap_spoofing: Literal["enable", "disable"]
    chan_based_mitm: Literal["enable", "disable"]
    adhoc_valid_ssid: Literal["enable", "disable"]
    adhoc_network: Literal["enable", "disable"]
    eapol_key_overflow: Literal["enable", "disable"]
    ap_impersonation: Literal["enable", "disable"]
    invalid_addr_combination: Literal["enable", "disable"]
    beacon_wrong_channel: Literal["enable", "disable"]
    ht_greenfield: Literal["enable", "disable"]
    overflow_ie: Literal["enable", "disable"]
    malformed_ht_ie: Literal["enable", "disable"]
    malformed_auth: Literal["enable", "disable"]
    malformed_association: Literal["enable", "disable"]
    ht_40mhz_intolerance: Literal["enable", "disable"]
    valid_ssid_misuse: Literal["enable", "disable"]
    valid_client_misassociation: Literal["enable", "disable"]
    hotspotter_attack: Literal["enable", "disable"]
    pwsave_dos_attack: Literal["enable", "disable"]
    omerta_attack: Literal["enable", "disable"]
    disconnect_station: Literal["enable", "disable"]
    unencrypted_valid: Literal["enable", "disable"]
    fata_jack: Literal["enable", "disable"]
    risky_encryption: Literal["enable", "disable"]
    fuzzed_beacon: Literal["enable", "disable"]
    fuzzed_probe_request: Literal["enable", "disable"]
    fuzzed_probe_response: Literal["enable", "disable"]
    air_jack: Literal["enable", "disable"]
    wpa_ft_attack: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class WidsProfileResponse(TypedDict, total=False):
    """Response type for WidsProfile - use with .dict property for typed dict access."""
    name: str
    comment: str
    sensor_mode: Literal["disable", "foreign", "both"]
    ap_scan: Literal["disable", "enable"]
    ap_scan_channel_list_2G_5G: list[WidsProfileApscanchannellist2g5gItem]
    ap_scan_channel_list_6G: list[WidsProfileApscanchannellist6gItem]
    ap_bgscan_period: int
    ap_bgscan_intv: int
    ap_bgscan_duration: int
    ap_bgscan_idle: int
    ap_bgscan_report_intv: int
    ap_bgscan_disable_schedules: list[WidsProfileApbgscandisableschedulesItem]
    ap_fgscan_report_intv: int
    ap_scan_passive: Literal["enable", "disable"]
    ap_scan_threshold: str
    ap_auto_suppress: Literal["enable", "disable"]
    wireless_bridge: Literal["enable", "disable"]
    deauth_broadcast: Literal["enable", "disable"]
    null_ssid_probe_resp: Literal["enable", "disable"]
    long_duration_attack: Literal["enable", "disable"]
    long_duration_thresh: int
    invalid_mac_oui: Literal["enable", "disable"]
    weak_wep_iv: Literal["enable", "disable"]
    auth_frame_flood: Literal["enable", "disable"]
    auth_flood_time: int
    auth_flood_thresh: int
    assoc_frame_flood: Literal["enable", "disable"]
    assoc_flood_time: int
    assoc_flood_thresh: int
    reassoc_flood: Literal["enable", "disable"]
    reassoc_flood_time: int
    reassoc_flood_thresh: int
    probe_flood: Literal["enable", "disable"]
    probe_flood_time: int
    probe_flood_thresh: int
    bcn_flood: Literal["enable", "disable"]
    bcn_flood_time: int
    bcn_flood_thresh: int
    rts_flood: Literal["enable", "disable"]
    rts_flood_time: int
    rts_flood_thresh: int
    cts_flood: Literal["enable", "disable"]
    cts_flood_time: int
    cts_flood_thresh: int
    client_flood: Literal["enable", "disable"]
    client_flood_time: int
    client_flood_thresh: int
    block_ack_flood: Literal["enable", "disable"]
    block_ack_flood_time: int
    block_ack_flood_thresh: int
    pspoll_flood: Literal["enable", "disable"]
    pspoll_flood_time: int
    pspoll_flood_thresh: int
    netstumbler: Literal["enable", "disable"]
    netstumbler_time: int
    netstumbler_thresh: int
    wellenreiter: Literal["enable", "disable"]
    wellenreiter_time: int
    wellenreiter_thresh: int
    spoofed_deauth: Literal["enable", "disable"]
    asleap_attack: Literal["enable", "disable"]
    eapol_start_flood: Literal["enable", "disable"]
    eapol_start_thresh: int
    eapol_start_intv: int
    eapol_logoff_flood: Literal["enable", "disable"]
    eapol_logoff_thresh: int
    eapol_logoff_intv: int
    eapol_succ_flood: Literal["enable", "disable"]
    eapol_succ_thresh: int
    eapol_succ_intv: int
    eapol_fail_flood: Literal["enable", "disable"]
    eapol_fail_thresh: int
    eapol_fail_intv: int
    eapol_pre_succ_flood: Literal["enable", "disable"]
    eapol_pre_succ_thresh: int
    eapol_pre_succ_intv: int
    eapol_pre_fail_flood: Literal["enable", "disable"]
    eapol_pre_fail_thresh: int
    eapol_pre_fail_intv: int
    deauth_unknown_src_thresh: int
    windows_bridge: Literal["enable", "disable"]
    disassoc_broadcast: Literal["enable", "disable"]
    ap_spoofing: Literal["enable", "disable"]
    chan_based_mitm: Literal["enable", "disable"]
    adhoc_valid_ssid: Literal["enable", "disable"]
    adhoc_network: Literal["enable", "disable"]
    eapol_key_overflow: Literal["enable", "disable"]
    ap_impersonation: Literal["enable", "disable"]
    invalid_addr_combination: Literal["enable", "disable"]
    beacon_wrong_channel: Literal["enable", "disable"]
    ht_greenfield: Literal["enable", "disable"]
    overflow_ie: Literal["enable", "disable"]
    malformed_ht_ie: Literal["enable", "disable"]
    malformed_auth: Literal["enable", "disable"]
    malformed_association: Literal["enable", "disable"]
    ht_40mhz_intolerance: Literal["enable", "disable"]
    valid_ssid_misuse: Literal["enable", "disable"]
    valid_client_misassociation: Literal["enable", "disable"]
    hotspotter_attack: Literal["enable", "disable"]
    pwsave_dos_attack: Literal["enable", "disable"]
    omerta_attack: Literal["enable", "disable"]
    disconnect_station: Literal["enable", "disable"]
    unencrypted_valid: Literal["enable", "disable"]
    fata_jack: Literal["enable", "disable"]
    risky_encryption: Literal["enable", "disable"]
    fuzzed_beacon: Literal["enable", "disable"]
    fuzzed_probe_request: Literal["enable", "disable"]
    fuzzed_probe_response: Literal["enable", "disable"]
    air_jack: Literal["enable", "disable"]
    wpa_ft_attack: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class WidsProfileApscanchannellist2g5gItemObject(FortiObject[WidsProfileApscanchannellist2g5gItem]):
    """Typed object for ap-scan-channel-list-2G-5G table items with attribute access."""
    chan: str


class WidsProfileApscanchannellist6gItemObject(FortiObject[WidsProfileApscanchannellist6gItem]):
    """Typed object for ap-scan-channel-list-6G table items with attribute access."""
    chan: str


class WidsProfileApbgscandisableschedulesItemObject(FortiObject[WidsProfileApbgscandisableschedulesItem]):
    """Typed object for ap-bgscan-disable-schedules table items with attribute access."""
    name: str


class WidsProfileObject(FortiObject):
    """Typed FortiObject for WidsProfile with field access."""
    name: str
    comment: str
    sensor_mode: Literal["disable", "foreign", "both"]
    ap_scan: Literal["disable", "enable"]
    ap_scan_channel_list_2G_5G: FortiObjectList[WidsProfileApscanchannellist2g5gItemObject]
    ap_scan_channel_list_6G: FortiObjectList[WidsProfileApscanchannellist6gItemObject]
    ap_bgscan_period: int
    ap_bgscan_intv: int
    ap_bgscan_duration: int
    ap_bgscan_idle: int
    ap_bgscan_report_intv: int
    ap_bgscan_disable_schedules: FortiObjectList[WidsProfileApbgscandisableschedulesItemObject]
    ap_fgscan_report_intv: int
    ap_scan_passive: Literal["enable", "disable"]
    ap_scan_threshold: str
    ap_auto_suppress: Literal["enable", "disable"]
    wireless_bridge: Literal["enable", "disable"]
    deauth_broadcast: Literal["enable", "disable"]
    null_ssid_probe_resp: Literal["enable", "disable"]
    long_duration_attack: Literal["enable", "disable"]
    long_duration_thresh: int
    invalid_mac_oui: Literal["enable", "disable"]
    weak_wep_iv: Literal["enable", "disable"]
    auth_frame_flood: Literal["enable", "disable"]
    auth_flood_time: int
    auth_flood_thresh: int
    assoc_frame_flood: Literal["enable", "disable"]
    assoc_flood_time: int
    assoc_flood_thresh: int
    reassoc_flood: Literal["enable", "disable"]
    reassoc_flood_time: int
    reassoc_flood_thresh: int
    probe_flood: Literal["enable", "disable"]
    probe_flood_time: int
    probe_flood_thresh: int
    bcn_flood: Literal["enable", "disable"]
    bcn_flood_time: int
    bcn_flood_thresh: int
    rts_flood: Literal["enable", "disable"]
    rts_flood_time: int
    rts_flood_thresh: int
    cts_flood: Literal["enable", "disable"]
    cts_flood_time: int
    cts_flood_thresh: int
    client_flood: Literal["enable", "disable"]
    client_flood_time: int
    client_flood_thresh: int
    block_ack_flood: Literal["enable", "disable"]
    block_ack_flood_time: int
    block_ack_flood_thresh: int
    pspoll_flood: Literal["enable", "disable"]
    pspoll_flood_time: int
    pspoll_flood_thresh: int
    netstumbler: Literal["enable", "disable"]
    netstumbler_time: int
    netstumbler_thresh: int
    wellenreiter: Literal["enable", "disable"]
    wellenreiter_time: int
    wellenreiter_thresh: int
    spoofed_deauth: Literal["enable", "disable"]
    asleap_attack: Literal["enable", "disable"]
    eapol_start_flood: Literal["enable", "disable"]
    eapol_start_thresh: int
    eapol_start_intv: int
    eapol_logoff_flood: Literal["enable", "disable"]
    eapol_logoff_thresh: int
    eapol_logoff_intv: int
    eapol_succ_flood: Literal["enable", "disable"]
    eapol_succ_thresh: int
    eapol_succ_intv: int
    eapol_fail_flood: Literal["enable", "disable"]
    eapol_fail_thresh: int
    eapol_fail_intv: int
    eapol_pre_succ_flood: Literal["enable", "disable"]
    eapol_pre_succ_thresh: int
    eapol_pre_succ_intv: int
    eapol_pre_fail_flood: Literal["enable", "disable"]
    eapol_pre_fail_thresh: int
    eapol_pre_fail_intv: int
    deauth_unknown_src_thresh: int
    windows_bridge: Literal["enable", "disable"]
    disassoc_broadcast: Literal["enable", "disable"]
    ap_spoofing: Literal["enable", "disable"]
    chan_based_mitm: Literal["enable", "disable"]
    adhoc_valid_ssid: Literal["enable", "disable"]
    adhoc_network: Literal["enable", "disable"]
    eapol_key_overflow: Literal["enable", "disable"]
    ap_impersonation: Literal["enable", "disable"]
    invalid_addr_combination: Literal["enable", "disable"]
    beacon_wrong_channel: Literal["enable", "disable"]
    ht_greenfield: Literal["enable", "disable"]
    overflow_ie: Literal["enable", "disable"]
    malformed_ht_ie: Literal["enable", "disable"]
    malformed_auth: Literal["enable", "disable"]
    malformed_association: Literal["enable", "disable"]
    ht_40mhz_intolerance: Literal["enable", "disable"]
    valid_ssid_misuse: Literal["enable", "disable"]
    valid_client_misassociation: Literal["enable", "disable"]
    hotspotter_attack: Literal["enable", "disable"]
    pwsave_dos_attack: Literal["enable", "disable"]
    omerta_attack: Literal["enable", "disable"]
    disconnect_station: Literal["enable", "disable"]
    unencrypted_valid: Literal["enable", "disable"]
    fata_jack: Literal["enable", "disable"]
    risky_encryption: Literal["enable", "disable"]
    fuzzed_beacon: Literal["enable", "disable"]
    fuzzed_probe_request: Literal["enable", "disable"]
    fuzzed_probe_response: Literal["enable", "disable"]
    air_jack: Literal["enable", "disable"]
    wpa_ft_attack: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class WidsProfile:
    """
    
    Endpoint: wireless_controller/wids_profile
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
    ) -> WidsProfileObject: ...
    
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
    ) -> FortiObjectList[WidsProfileObject]: ...
    
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
        payload_dict: WidsProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        sensor_mode: Literal["disable", "foreign", "both"] | None = ...,
        ap_scan: Literal["disable", "enable"] | None = ...,
        ap_scan_channel_list_2G_5G: str | list[str] | list[WidsProfileApscanchannellist2g5gItem] | None = ...,
        ap_scan_channel_list_6G: str | list[str] | list[WidsProfileApscanchannellist6gItem] | None = ...,
        ap_bgscan_period: int | None = ...,
        ap_bgscan_intv: int | None = ...,
        ap_bgscan_duration: int | None = ...,
        ap_bgscan_idle: int | None = ...,
        ap_bgscan_report_intv: int | None = ...,
        ap_bgscan_disable_schedules: str | list[str] | list[WidsProfileApbgscandisableschedulesItem] | None = ...,
        ap_fgscan_report_intv: int | None = ...,
        ap_scan_passive: Literal["enable", "disable"] | None = ...,
        ap_scan_threshold: str | None = ...,
        ap_auto_suppress: Literal["enable", "disable"] | None = ...,
        wireless_bridge: Literal["enable", "disable"] | None = ...,
        deauth_broadcast: Literal["enable", "disable"] | None = ...,
        null_ssid_probe_resp: Literal["enable", "disable"] | None = ...,
        long_duration_attack: Literal["enable", "disable"] | None = ...,
        long_duration_thresh: int | None = ...,
        invalid_mac_oui: Literal["enable", "disable"] | None = ...,
        weak_wep_iv: Literal["enable", "disable"] | None = ...,
        auth_frame_flood: Literal["enable", "disable"] | None = ...,
        auth_flood_time: int | None = ...,
        auth_flood_thresh: int | None = ...,
        assoc_frame_flood: Literal["enable", "disable"] | None = ...,
        assoc_flood_time: int | None = ...,
        assoc_flood_thresh: int | None = ...,
        reassoc_flood: Literal["enable", "disable"] | None = ...,
        reassoc_flood_time: int | None = ...,
        reassoc_flood_thresh: int | None = ...,
        probe_flood: Literal["enable", "disable"] | None = ...,
        probe_flood_time: int | None = ...,
        probe_flood_thresh: int | None = ...,
        bcn_flood: Literal["enable", "disable"] | None = ...,
        bcn_flood_time: int | None = ...,
        bcn_flood_thresh: int | None = ...,
        rts_flood: Literal["enable", "disable"] | None = ...,
        rts_flood_time: int | None = ...,
        rts_flood_thresh: int | None = ...,
        cts_flood: Literal["enable", "disable"] | None = ...,
        cts_flood_time: int | None = ...,
        cts_flood_thresh: int | None = ...,
        client_flood: Literal["enable", "disable"] | None = ...,
        client_flood_time: int | None = ...,
        client_flood_thresh: int | None = ...,
        block_ack_flood: Literal["enable", "disable"] | None = ...,
        block_ack_flood_time: int | None = ...,
        block_ack_flood_thresh: int | None = ...,
        pspoll_flood: Literal["enable", "disable"] | None = ...,
        pspoll_flood_time: int | None = ...,
        pspoll_flood_thresh: int | None = ...,
        netstumbler: Literal["enable", "disable"] | None = ...,
        netstumbler_time: int | None = ...,
        netstumbler_thresh: int | None = ...,
        wellenreiter: Literal["enable", "disable"] | None = ...,
        wellenreiter_time: int | None = ...,
        wellenreiter_thresh: int | None = ...,
        spoofed_deauth: Literal["enable", "disable"] | None = ...,
        asleap_attack: Literal["enable", "disable"] | None = ...,
        eapol_start_flood: Literal["enable", "disable"] | None = ...,
        eapol_start_thresh: int | None = ...,
        eapol_start_intv: int | None = ...,
        eapol_logoff_flood: Literal["enable", "disable"] | None = ...,
        eapol_logoff_thresh: int | None = ...,
        eapol_logoff_intv: int | None = ...,
        eapol_succ_flood: Literal["enable", "disable"] | None = ...,
        eapol_succ_thresh: int | None = ...,
        eapol_succ_intv: int | None = ...,
        eapol_fail_flood: Literal["enable", "disable"] | None = ...,
        eapol_fail_thresh: int | None = ...,
        eapol_fail_intv: int | None = ...,
        eapol_pre_succ_flood: Literal["enable", "disable"] | None = ...,
        eapol_pre_succ_thresh: int | None = ...,
        eapol_pre_succ_intv: int | None = ...,
        eapol_pre_fail_flood: Literal["enable", "disable"] | None = ...,
        eapol_pre_fail_thresh: int | None = ...,
        eapol_pre_fail_intv: int | None = ...,
        deauth_unknown_src_thresh: int | None = ...,
        windows_bridge: Literal["enable", "disable"] | None = ...,
        disassoc_broadcast: Literal["enable", "disable"] | None = ...,
        ap_spoofing: Literal["enable", "disable"] | None = ...,
        chan_based_mitm: Literal["enable", "disable"] | None = ...,
        adhoc_valid_ssid: Literal["enable", "disable"] | None = ...,
        adhoc_network: Literal["enable", "disable"] | None = ...,
        eapol_key_overflow: Literal["enable", "disable"] | None = ...,
        ap_impersonation: Literal["enable", "disable"] | None = ...,
        invalid_addr_combination: Literal["enable", "disable"] | None = ...,
        beacon_wrong_channel: Literal["enable", "disable"] | None = ...,
        ht_greenfield: Literal["enable", "disable"] | None = ...,
        overflow_ie: Literal["enable", "disable"] | None = ...,
        malformed_ht_ie: Literal["enable", "disable"] | None = ...,
        malformed_auth: Literal["enable", "disable"] | None = ...,
        malformed_association: Literal["enable", "disable"] | None = ...,
        ht_40mhz_intolerance: Literal["enable", "disable"] | None = ...,
        valid_ssid_misuse: Literal["enable", "disable"] | None = ...,
        valid_client_misassociation: Literal["enable", "disable"] | None = ...,
        hotspotter_attack: Literal["enable", "disable"] | None = ...,
        pwsave_dos_attack: Literal["enable", "disable"] | None = ...,
        omerta_attack: Literal["enable", "disable"] | None = ...,
        disconnect_station: Literal["enable", "disable"] | None = ...,
        unencrypted_valid: Literal["enable", "disable"] | None = ...,
        fata_jack: Literal["enable", "disable"] | None = ...,
        risky_encryption: Literal["enable", "disable"] | None = ...,
        fuzzed_beacon: Literal["enable", "disable"] | None = ...,
        fuzzed_probe_request: Literal["enable", "disable"] | None = ...,
        fuzzed_probe_response: Literal["enable", "disable"] | None = ...,
        air_jack: Literal["enable", "disable"] | None = ...,
        wpa_ft_attack: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WidsProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: WidsProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        sensor_mode: Literal["disable", "foreign", "both"] | None = ...,
        ap_scan: Literal["disable", "enable"] | None = ...,
        ap_scan_channel_list_2G_5G: str | list[str] | list[WidsProfileApscanchannellist2g5gItem] | None = ...,
        ap_scan_channel_list_6G: str | list[str] | list[WidsProfileApscanchannellist6gItem] | None = ...,
        ap_bgscan_period: int | None = ...,
        ap_bgscan_intv: int | None = ...,
        ap_bgscan_duration: int | None = ...,
        ap_bgscan_idle: int | None = ...,
        ap_bgscan_report_intv: int | None = ...,
        ap_bgscan_disable_schedules: str | list[str] | list[WidsProfileApbgscandisableschedulesItem] | None = ...,
        ap_fgscan_report_intv: int | None = ...,
        ap_scan_passive: Literal["enable", "disable"] | None = ...,
        ap_scan_threshold: str | None = ...,
        ap_auto_suppress: Literal["enable", "disable"] | None = ...,
        wireless_bridge: Literal["enable", "disable"] | None = ...,
        deauth_broadcast: Literal["enable", "disable"] | None = ...,
        null_ssid_probe_resp: Literal["enable", "disable"] | None = ...,
        long_duration_attack: Literal["enable", "disable"] | None = ...,
        long_duration_thresh: int | None = ...,
        invalid_mac_oui: Literal["enable", "disable"] | None = ...,
        weak_wep_iv: Literal["enable", "disable"] | None = ...,
        auth_frame_flood: Literal["enable", "disable"] | None = ...,
        auth_flood_time: int | None = ...,
        auth_flood_thresh: int | None = ...,
        assoc_frame_flood: Literal["enable", "disable"] | None = ...,
        assoc_flood_time: int | None = ...,
        assoc_flood_thresh: int | None = ...,
        reassoc_flood: Literal["enable", "disable"] | None = ...,
        reassoc_flood_time: int | None = ...,
        reassoc_flood_thresh: int | None = ...,
        probe_flood: Literal["enable", "disable"] | None = ...,
        probe_flood_time: int | None = ...,
        probe_flood_thresh: int | None = ...,
        bcn_flood: Literal["enable", "disable"] | None = ...,
        bcn_flood_time: int | None = ...,
        bcn_flood_thresh: int | None = ...,
        rts_flood: Literal["enable", "disable"] | None = ...,
        rts_flood_time: int | None = ...,
        rts_flood_thresh: int | None = ...,
        cts_flood: Literal["enable", "disable"] | None = ...,
        cts_flood_time: int | None = ...,
        cts_flood_thresh: int | None = ...,
        client_flood: Literal["enable", "disable"] | None = ...,
        client_flood_time: int | None = ...,
        client_flood_thresh: int | None = ...,
        block_ack_flood: Literal["enable", "disable"] | None = ...,
        block_ack_flood_time: int | None = ...,
        block_ack_flood_thresh: int | None = ...,
        pspoll_flood: Literal["enable", "disable"] | None = ...,
        pspoll_flood_time: int | None = ...,
        pspoll_flood_thresh: int | None = ...,
        netstumbler: Literal["enable", "disable"] | None = ...,
        netstumbler_time: int | None = ...,
        netstumbler_thresh: int | None = ...,
        wellenreiter: Literal["enable", "disable"] | None = ...,
        wellenreiter_time: int | None = ...,
        wellenreiter_thresh: int | None = ...,
        spoofed_deauth: Literal["enable", "disable"] | None = ...,
        asleap_attack: Literal["enable", "disable"] | None = ...,
        eapol_start_flood: Literal["enable", "disable"] | None = ...,
        eapol_start_thresh: int | None = ...,
        eapol_start_intv: int | None = ...,
        eapol_logoff_flood: Literal["enable", "disable"] | None = ...,
        eapol_logoff_thresh: int | None = ...,
        eapol_logoff_intv: int | None = ...,
        eapol_succ_flood: Literal["enable", "disable"] | None = ...,
        eapol_succ_thresh: int | None = ...,
        eapol_succ_intv: int | None = ...,
        eapol_fail_flood: Literal["enable", "disable"] | None = ...,
        eapol_fail_thresh: int | None = ...,
        eapol_fail_intv: int | None = ...,
        eapol_pre_succ_flood: Literal["enable", "disable"] | None = ...,
        eapol_pre_succ_thresh: int | None = ...,
        eapol_pre_succ_intv: int | None = ...,
        eapol_pre_fail_flood: Literal["enable", "disable"] | None = ...,
        eapol_pre_fail_thresh: int | None = ...,
        eapol_pre_fail_intv: int | None = ...,
        deauth_unknown_src_thresh: int | None = ...,
        windows_bridge: Literal["enable", "disable"] | None = ...,
        disassoc_broadcast: Literal["enable", "disable"] | None = ...,
        ap_spoofing: Literal["enable", "disable"] | None = ...,
        chan_based_mitm: Literal["enable", "disable"] | None = ...,
        adhoc_valid_ssid: Literal["enable", "disable"] | None = ...,
        adhoc_network: Literal["enable", "disable"] | None = ...,
        eapol_key_overflow: Literal["enable", "disable"] | None = ...,
        ap_impersonation: Literal["enable", "disable"] | None = ...,
        invalid_addr_combination: Literal["enable", "disable"] | None = ...,
        beacon_wrong_channel: Literal["enable", "disable"] | None = ...,
        ht_greenfield: Literal["enable", "disable"] | None = ...,
        overflow_ie: Literal["enable", "disable"] | None = ...,
        malformed_ht_ie: Literal["enable", "disable"] | None = ...,
        malformed_auth: Literal["enable", "disable"] | None = ...,
        malformed_association: Literal["enable", "disable"] | None = ...,
        ht_40mhz_intolerance: Literal["enable", "disable"] | None = ...,
        valid_ssid_misuse: Literal["enable", "disable"] | None = ...,
        valid_client_misassociation: Literal["enable", "disable"] | None = ...,
        hotspotter_attack: Literal["enable", "disable"] | None = ...,
        pwsave_dos_attack: Literal["enable", "disable"] | None = ...,
        omerta_attack: Literal["enable", "disable"] | None = ...,
        disconnect_station: Literal["enable", "disable"] | None = ...,
        unencrypted_valid: Literal["enable", "disable"] | None = ...,
        fata_jack: Literal["enable", "disable"] | None = ...,
        risky_encryption: Literal["enable", "disable"] | None = ...,
        fuzzed_beacon: Literal["enable", "disable"] | None = ...,
        fuzzed_probe_request: Literal["enable", "disable"] | None = ...,
        fuzzed_probe_response: Literal["enable", "disable"] | None = ...,
        air_jack: Literal["enable", "disable"] | None = ...,
        wpa_ft_attack: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WidsProfileObject: ...

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
        payload_dict: WidsProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        sensor_mode: Literal["disable", "foreign", "both"] | None = ...,
        ap_scan: Literal["disable", "enable"] | None = ...,
        ap_scan_channel_list_2G_5G: str | list[str] | list[WidsProfileApscanchannellist2g5gItem] | None = ...,
        ap_scan_channel_list_6G: str | list[str] | list[WidsProfileApscanchannellist6gItem] | None = ...,
        ap_bgscan_period: int | None = ...,
        ap_bgscan_intv: int | None = ...,
        ap_bgscan_duration: int | None = ...,
        ap_bgscan_idle: int | None = ...,
        ap_bgscan_report_intv: int | None = ...,
        ap_bgscan_disable_schedules: str | list[str] | list[WidsProfileApbgscandisableschedulesItem] | None = ...,
        ap_fgscan_report_intv: int | None = ...,
        ap_scan_passive: Literal["enable", "disable"] | None = ...,
        ap_scan_threshold: str | None = ...,
        ap_auto_suppress: Literal["enable", "disable"] | None = ...,
        wireless_bridge: Literal["enable", "disable"] | None = ...,
        deauth_broadcast: Literal["enable", "disable"] | None = ...,
        null_ssid_probe_resp: Literal["enable", "disable"] | None = ...,
        long_duration_attack: Literal["enable", "disable"] | None = ...,
        long_duration_thresh: int | None = ...,
        invalid_mac_oui: Literal["enable", "disable"] | None = ...,
        weak_wep_iv: Literal["enable", "disable"] | None = ...,
        auth_frame_flood: Literal["enable", "disable"] | None = ...,
        auth_flood_time: int | None = ...,
        auth_flood_thresh: int | None = ...,
        assoc_frame_flood: Literal["enable", "disable"] | None = ...,
        assoc_flood_time: int | None = ...,
        assoc_flood_thresh: int | None = ...,
        reassoc_flood: Literal["enable", "disable"] | None = ...,
        reassoc_flood_time: int | None = ...,
        reassoc_flood_thresh: int | None = ...,
        probe_flood: Literal["enable", "disable"] | None = ...,
        probe_flood_time: int | None = ...,
        probe_flood_thresh: int | None = ...,
        bcn_flood: Literal["enable", "disable"] | None = ...,
        bcn_flood_time: int | None = ...,
        bcn_flood_thresh: int | None = ...,
        rts_flood: Literal["enable", "disable"] | None = ...,
        rts_flood_time: int | None = ...,
        rts_flood_thresh: int | None = ...,
        cts_flood: Literal["enable", "disable"] | None = ...,
        cts_flood_time: int | None = ...,
        cts_flood_thresh: int | None = ...,
        client_flood: Literal["enable", "disable"] | None = ...,
        client_flood_time: int | None = ...,
        client_flood_thresh: int | None = ...,
        block_ack_flood: Literal["enable", "disable"] | None = ...,
        block_ack_flood_time: int | None = ...,
        block_ack_flood_thresh: int | None = ...,
        pspoll_flood: Literal["enable", "disable"] | None = ...,
        pspoll_flood_time: int | None = ...,
        pspoll_flood_thresh: int | None = ...,
        netstumbler: Literal["enable", "disable"] | None = ...,
        netstumbler_time: int | None = ...,
        netstumbler_thresh: int | None = ...,
        wellenreiter: Literal["enable", "disable"] | None = ...,
        wellenreiter_time: int | None = ...,
        wellenreiter_thresh: int | None = ...,
        spoofed_deauth: Literal["enable", "disable"] | None = ...,
        asleap_attack: Literal["enable", "disable"] | None = ...,
        eapol_start_flood: Literal["enable", "disable"] | None = ...,
        eapol_start_thresh: int | None = ...,
        eapol_start_intv: int | None = ...,
        eapol_logoff_flood: Literal["enable", "disable"] | None = ...,
        eapol_logoff_thresh: int | None = ...,
        eapol_logoff_intv: int | None = ...,
        eapol_succ_flood: Literal["enable", "disable"] | None = ...,
        eapol_succ_thresh: int | None = ...,
        eapol_succ_intv: int | None = ...,
        eapol_fail_flood: Literal["enable", "disable"] | None = ...,
        eapol_fail_thresh: int | None = ...,
        eapol_fail_intv: int | None = ...,
        eapol_pre_succ_flood: Literal["enable", "disable"] | None = ...,
        eapol_pre_succ_thresh: int | None = ...,
        eapol_pre_succ_intv: int | None = ...,
        eapol_pre_fail_flood: Literal["enable", "disable"] | None = ...,
        eapol_pre_fail_thresh: int | None = ...,
        eapol_pre_fail_intv: int | None = ...,
        deauth_unknown_src_thresh: int | None = ...,
        windows_bridge: Literal["enable", "disable"] | None = ...,
        disassoc_broadcast: Literal["enable", "disable"] | None = ...,
        ap_spoofing: Literal["enable", "disable"] | None = ...,
        chan_based_mitm: Literal["enable", "disable"] | None = ...,
        adhoc_valid_ssid: Literal["enable", "disable"] | None = ...,
        adhoc_network: Literal["enable", "disable"] | None = ...,
        eapol_key_overflow: Literal["enable", "disable"] | None = ...,
        ap_impersonation: Literal["enable", "disable"] | None = ...,
        invalid_addr_combination: Literal["enable", "disable"] | None = ...,
        beacon_wrong_channel: Literal["enable", "disable"] | None = ...,
        ht_greenfield: Literal["enable", "disable"] | None = ...,
        overflow_ie: Literal["enable", "disable"] | None = ...,
        malformed_ht_ie: Literal["enable", "disable"] | None = ...,
        malformed_auth: Literal["enable", "disable"] | None = ...,
        malformed_association: Literal["enable", "disable"] | None = ...,
        ht_40mhz_intolerance: Literal["enable", "disable"] | None = ...,
        valid_ssid_misuse: Literal["enable", "disable"] | None = ...,
        valid_client_misassociation: Literal["enable", "disable"] | None = ...,
        hotspotter_attack: Literal["enable", "disable"] | None = ...,
        pwsave_dos_attack: Literal["enable", "disable"] | None = ...,
        omerta_attack: Literal["enable", "disable"] | None = ...,
        disconnect_station: Literal["enable", "disable"] | None = ...,
        unencrypted_valid: Literal["enable", "disable"] | None = ...,
        fata_jack: Literal["enable", "disable"] | None = ...,
        risky_encryption: Literal["enable", "disable"] | None = ...,
        fuzzed_beacon: Literal["enable", "disable"] | None = ...,
        fuzzed_probe_request: Literal["enable", "disable"] | None = ...,
        fuzzed_probe_response: Literal["enable", "disable"] | None = ...,
        air_jack: Literal["enable", "disable"] | None = ...,
        wpa_ft_attack: Literal["enable", "disable"] | None = ...,
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
    "WidsProfile",
    "WidsProfilePayload",
    "WidsProfileResponse",
    "WidsProfileObject",
]