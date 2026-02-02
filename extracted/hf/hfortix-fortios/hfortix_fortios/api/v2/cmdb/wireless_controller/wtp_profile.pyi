""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/wtp_profile
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

class WtpProfileRadio1VapsItem(TypedDict, total=False):
    """Nested item for radio-1.vaps field."""
    name: str


class WtpProfileRadio1ChannelItem(TypedDict, total=False):
    """Nested item for radio-1.channel field."""
    chan: str


class WtpProfileRadio2VapsItem(TypedDict, total=False):
    """Nested item for radio-2.vaps field."""
    name: str


class WtpProfileRadio2ChannelItem(TypedDict, total=False):
    """Nested item for radio-2.channel field."""
    chan: str


class WtpProfileRadio3VapsItem(TypedDict, total=False):
    """Nested item for radio-3.vaps field."""
    name: str


class WtpProfileRadio3ChannelItem(TypedDict, total=False):
    """Nested item for radio-3.channel field."""
    chan: str


class WtpProfileRadio4VapsItem(TypedDict, total=False):
    """Nested item for radio-4.vaps field."""
    name: str


class WtpProfileRadio4ChannelItem(TypedDict, total=False):
    """Nested item for radio-4.channel field."""
    chan: str


class WtpProfilePlatformDict(TypedDict, total=False):
    """Nested object type for platform field."""
    type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"]
    mode: Literal["single-5G", "dual-5G"]
    ddscan: Literal["enable", "disable"]


class WtpProfileLanDict(TypedDict, total=False):
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


class WtpProfileLedschedulesItem(TypedDict, total=False):
    """Nested item for led-schedules field."""
    name: str


class WtpProfileDenymaclistItem(TypedDict, total=False):
    """Nested item for deny-mac-list field."""
    id: int
    mac: str


class WtpProfileSplittunnelingaclItem(TypedDict, total=False):
    """Nested item for split-tunneling-acl field."""
    id: int
    dest_ip: str


class WtpProfileRadio1Dict(TypedDict, total=False):
    """Nested object type for radio-1 field."""
    mode: Literal["disabled", "ap", "monitor", "sniffer", "sam"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"]
    drma: Literal["disable", "enable"]
    drma_sensitivity: Literal["low", "medium", "high"]
    airtime_fairness: Literal["enable", "disable"]
    protection_mode: Literal["rtscts", "ctsonly", "disable"]
    powersave_optimize: Literal["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"]
    transmit_optimize: Literal["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"]
    amsdu: Literal["enable", "disable"]
    coexistence: Literal["enable", "disable"]
    zero_wait_dfs: Literal["enable", "disable"]
    bss_color: int
    bss_color_mode: Literal["auto", "static"]
    short_guard_interval: Literal["enable", "disable"]
    mimo_mode: Literal["default", "1x1", "2x2", "3x3", "4x4", "8x8"]
    channel_bonding: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"]
    optional_antenna: Literal["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"]
    optional_antenna_gain: str
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    dtim: int
    beacon_interval: int
    x80211d: Literal["enable", "disable"]
    x80211mc: Literal["enable", "disable"]
    rts_threshold: int
    frag_threshold: int
    ap_sniffer_bufsize: int
    ap_sniffer_chan: int
    ap_sniffer_chan_width: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    ap_sniffer_addr: str
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"]
    ap_sniffer_mgmt_probe: Literal["enable", "disable"]
    ap_sniffer_mgmt_other: Literal["enable", "disable"]
    ap_sniffer_ctl: Literal["enable", "disable"]
    ap_sniffer_data: Literal["enable", "disable"]
    sam_ssid: str
    sam_bssid: str
    sam_security_type: Literal["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"]
    sam_captive_portal: Literal["enable", "disable"]
    sam_cwp_username: str
    sam_cwp_password: str
    sam_cwp_test_url: str
    sam_cwp_match_string: str
    sam_cwp_success_string: str
    sam_cwp_failure_string: str
    sam_eap_method: Literal["both", "tls", "peap"]
    sam_client_certificate: str
    sam_private_key: str
    sam_private_key_password: str
    sam_ca_certificate: str
    sam_username: str
    sam_password: str
    sam_test: Literal["ping", "iperf"]
    sam_server_type: Literal["ip", "fqdn"]
    sam_server_ip: str
    sam_server_fqdn: str
    iperf_server_port: int
    iperf_protocol: Literal["udp", "tcp"]
    sam_report_intv: int
    channel_utilization: Literal["enable", "disable"]
    wids_profile: str
    ai_darrp_support: Literal["enable", "disable"]
    darrp: Literal["enable", "disable"]
    arrp_profile: str
    max_clients: int
    max_distance: int
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str] | list[WtpProfileRadio1VapsItem]
    channel: str | list[str] | list[WtpProfileRadio1ChannelItem]
    call_admission_control: Literal["enable", "disable"]
    call_capacity: int
    bandwidth_admission_control: Literal["enable", "disable"]
    bandwidth_capacity: int


class WtpProfileRadio2Dict(TypedDict, total=False):
    """Nested object type for radio-2 field."""
    mode: Literal["disabled", "ap", "monitor", "sniffer", "sam"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"]
    drma: Literal["disable", "enable"]
    drma_sensitivity: Literal["low", "medium", "high"]
    airtime_fairness: Literal["enable", "disable"]
    protection_mode: Literal["rtscts", "ctsonly", "disable"]
    powersave_optimize: Literal["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"]
    transmit_optimize: Literal["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"]
    amsdu: Literal["enable", "disable"]
    coexistence: Literal["enable", "disable"]
    zero_wait_dfs: Literal["enable", "disable"]
    bss_color: int
    bss_color_mode: Literal["auto", "static"]
    short_guard_interval: Literal["enable", "disable"]
    mimo_mode: Literal["default", "1x1", "2x2", "3x3", "4x4", "8x8"]
    channel_bonding: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"]
    optional_antenna: Literal["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"]
    optional_antenna_gain: str
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    dtim: int
    beacon_interval: int
    x80211d: Literal["enable", "disable"]
    x80211mc: Literal["enable", "disable"]
    rts_threshold: int
    frag_threshold: int
    ap_sniffer_bufsize: int
    ap_sniffer_chan: int
    ap_sniffer_chan_width: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    ap_sniffer_addr: str
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"]
    ap_sniffer_mgmt_probe: Literal["enable", "disable"]
    ap_sniffer_mgmt_other: Literal["enable", "disable"]
    ap_sniffer_ctl: Literal["enable", "disable"]
    ap_sniffer_data: Literal["enable", "disable"]
    sam_ssid: str
    sam_bssid: str
    sam_security_type: Literal["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"]
    sam_captive_portal: Literal["enable", "disable"]
    sam_cwp_username: str
    sam_cwp_password: str
    sam_cwp_test_url: str
    sam_cwp_match_string: str
    sam_cwp_success_string: str
    sam_cwp_failure_string: str
    sam_eap_method: Literal["both", "tls", "peap"]
    sam_client_certificate: str
    sam_private_key: str
    sam_private_key_password: str
    sam_ca_certificate: str
    sam_username: str
    sam_password: str
    sam_test: Literal["ping", "iperf"]
    sam_server_type: Literal["ip", "fqdn"]
    sam_server_ip: str
    sam_server_fqdn: str
    iperf_server_port: int
    iperf_protocol: Literal["udp", "tcp"]
    sam_report_intv: int
    channel_utilization: Literal["enable", "disable"]
    wids_profile: str
    ai_darrp_support: Literal["enable", "disable"]
    darrp: Literal["enable", "disable"]
    arrp_profile: str
    max_clients: int
    max_distance: int
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str] | list[WtpProfileRadio2VapsItem]
    channel: str | list[str] | list[WtpProfileRadio2ChannelItem]
    call_admission_control: Literal["enable", "disable"]
    call_capacity: int
    bandwidth_admission_control: Literal["enable", "disable"]
    bandwidth_capacity: int


class WtpProfileRadio3Dict(TypedDict, total=False):
    """Nested object type for radio-3 field."""
    mode: Literal["disabled", "ap", "monitor", "sniffer", "sam"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"]
    drma: Literal["disable", "enable"]
    drma_sensitivity: Literal["low", "medium", "high"]
    airtime_fairness: Literal["enable", "disable"]
    protection_mode: Literal["rtscts", "ctsonly", "disable"]
    powersave_optimize: Literal["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"]
    transmit_optimize: Literal["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"]
    amsdu: Literal["enable", "disable"]
    coexistence: Literal["enable", "disable"]
    zero_wait_dfs: Literal["enable", "disable"]
    bss_color: int
    bss_color_mode: Literal["auto", "static"]
    short_guard_interval: Literal["enable", "disable"]
    mimo_mode: Literal["default", "1x1", "2x2", "3x3", "4x4", "8x8"]
    channel_bonding: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"]
    optional_antenna: Literal["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"]
    optional_antenna_gain: str
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    dtim: int
    beacon_interval: int
    x80211d: Literal["enable", "disable"]
    x80211mc: Literal["enable", "disable"]
    rts_threshold: int
    frag_threshold: int
    ap_sniffer_bufsize: int
    ap_sniffer_chan: int
    ap_sniffer_chan_width: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    ap_sniffer_addr: str
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"]
    ap_sniffer_mgmt_probe: Literal["enable", "disable"]
    ap_sniffer_mgmt_other: Literal["enable", "disable"]
    ap_sniffer_ctl: Literal["enable", "disable"]
    ap_sniffer_data: Literal["enable", "disable"]
    sam_ssid: str
    sam_bssid: str
    sam_security_type: Literal["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"]
    sam_captive_portal: Literal["enable", "disable"]
    sam_cwp_username: str
    sam_cwp_password: str
    sam_cwp_test_url: str
    sam_cwp_match_string: str
    sam_cwp_success_string: str
    sam_cwp_failure_string: str
    sam_eap_method: Literal["both", "tls", "peap"]
    sam_client_certificate: str
    sam_private_key: str
    sam_private_key_password: str
    sam_ca_certificate: str
    sam_username: str
    sam_password: str
    sam_test: Literal["ping", "iperf"]
    sam_server_type: Literal["ip", "fqdn"]
    sam_server_ip: str
    sam_server_fqdn: str
    iperf_server_port: int
    iperf_protocol: Literal["udp", "tcp"]
    sam_report_intv: int
    channel_utilization: Literal["enable", "disable"]
    wids_profile: str
    ai_darrp_support: Literal["enable", "disable"]
    darrp: Literal["enable", "disable"]
    arrp_profile: str
    max_clients: int
    max_distance: int
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str] | list[WtpProfileRadio3VapsItem]
    channel: str | list[str] | list[WtpProfileRadio3ChannelItem]
    call_admission_control: Literal["enable", "disable"]
    call_capacity: int
    bandwidth_admission_control: Literal["enable", "disable"]
    bandwidth_capacity: int


class WtpProfileRadio4Dict(TypedDict, total=False):
    """Nested object type for radio-4 field."""
    mode: Literal["disabled", "ap", "monitor", "sniffer", "sam"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"]
    drma: Literal["disable", "enable"]
    drma_sensitivity: Literal["low", "medium", "high"]
    airtime_fairness: Literal["enable", "disable"]
    protection_mode: Literal["rtscts", "ctsonly", "disable"]
    powersave_optimize: Literal["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"]
    transmit_optimize: Literal["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"]
    amsdu: Literal["enable", "disable"]
    coexistence: Literal["enable", "disable"]
    zero_wait_dfs: Literal["enable", "disable"]
    bss_color: int
    bss_color_mode: Literal["auto", "static"]
    short_guard_interval: Literal["enable", "disable"]
    mimo_mode: Literal["default", "1x1", "2x2", "3x3", "4x4", "8x8"]
    channel_bonding: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"]
    optional_antenna: Literal["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"]
    optional_antenna_gain: str
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    dtim: int
    beacon_interval: int
    x80211d: Literal["enable", "disable"]
    x80211mc: Literal["enable", "disable"]
    rts_threshold: int
    frag_threshold: int
    ap_sniffer_bufsize: int
    ap_sniffer_chan: int
    ap_sniffer_chan_width: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    ap_sniffer_addr: str
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"]
    ap_sniffer_mgmt_probe: Literal["enable", "disable"]
    ap_sniffer_mgmt_other: Literal["enable", "disable"]
    ap_sniffer_ctl: Literal["enable", "disable"]
    ap_sniffer_data: Literal["enable", "disable"]
    sam_ssid: str
    sam_bssid: str
    sam_security_type: Literal["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"]
    sam_captive_portal: Literal["enable", "disable"]
    sam_cwp_username: str
    sam_cwp_password: str
    sam_cwp_test_url: str
    sam_cwp_match_string: str
    sam_cwp_success_string: str
    sam_cwp_failure_string: str
    sam_eap_method: Literal["both", "tls", "peap"]
    sam_client_certificate: str
    sam_private_key: str
    sam_private_key_password: str
    sam_ca_certificate: str
    sam_username: str
    sam_password: str
    sam_test: Literal["ping", "iperf"]
    sam_server_type: Literal["ip", "fqdn"]
    sam_server_ip: str
    sam_server_fqdn: str
    iperf_server_port: int
    iperf_protocol: Literal["udp", "tcp"]
    sam_report_intv: int
    channel_utilization: Literal["enable", "disable"]
    wids_profile: str
    ai_darrp_support: Literal["enable", "disable"]
    darrp: Literal["enable", "disable"]
    arrp_profile: str
    max_clients: int
    max_distance: int
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str] | list[WtpProfileRadio4VapsItem]
    channel: str | list[str] | list[WtpProfileRadio4ChannelItem]
    call_admission_control: Literal["enable", "disable"]
    call_capacity: int
    bandwidth_admission_control: Literal["enable", "disable"]
    bandwidth_capacity: int


class WtpProfileLbsDict(TypedDict, total=False):
    """Nested object type for lbs field."""
    ekahau_blink_mode: Literal["enable", "disable"]
    ekahau_tag: str
    erc_server_ip: str
    erc_server_port: int
    aeroscout: Literal["enable", "disable"]
    aeroscout_server_ip: str
    aeroscout_server_port: int
    aeroscout_mu: Literal["enable", "disable"]
    aeroscout_ap_mac: Literal["bssid", "board-mac"]
    aeroscout_mmu_report: Literal["enable", "disable"]
    aeroscout_mu_factor: int
    aeroscout_mu_timeout: int
    fortipresence: Literal["foreign", "both", "disable"]
    fortipresence_server_addr_type: Literal["ipv4", "fqdn"]
    fortipresence_server: str
    fortipresence_server_fqdn: str
    fortipresence_port: int
    fortipresence_secret: str
    fortipresence_project: str
    fortipresence_frequency: int
    fortipresence_rogue: Literal["enable", "disable"]
    fortipresence_unassoc: Literal["enable", "disable"]
    fortipresence_ble: Literal["enable", "disable"]
    station_locate: Literal["enable", "disable"]
    ble_rtls: Literal["none", "polestar", "evresys"]
    ble_rtls_protocol: Literal["WSS"]
    ble_rtls_server_fqdn: str
    ble_rtls_server_path: str
    ble_rtls_server_token: str
    ble_rtls_server_port: int
    ble_rtls_accumulation_interval: int
    ble_rtls_reporting_interval: int
    ble_rtls_asset_uuid_list1: str
    ble_rtls_asset_uuid_list2: str
    ble_rtls_asset_uuid_list3: str
    ble_rtls_asset_uuid_list4: str
    ble_rtls_asset_addrgrp_list: str


class WtpProfileEslsesdongleDict(TypedDict, total=False):
    """Nested object type for esl-ses-dongle field."""
    compliance_level: Literal["compliance-level-2"]
    scd_enable: Literal["enable", "disable"]
    esl_channel: Literal["-1", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "127"]
    output_power: Literal["a", "b", "c", "d", "e", "f", "g", "h"]
    apc_addr_type: Literal["fqdn", "ip"]
    apc_fqdn: str
    apc_ip: str
    apc_port: int
    coex_level: Literal["none"]
    tls_cert_verification: Literal["enable", "disable"]
    tls_fqdn_verification: Literal["enable", "disable"]


class WtpProfilePayload(TypedDict, total=False):
    """Payload type for WtpProfile operations."""
    name: str
    comment: str
    platform: WtpProfilePlatformDict
    control_message_offload: str | list[str]
    bonjour_profile: str
    apcfg_profile: str
    apcfg_mesh: Literal["enable", "disable"]
    apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"]
    apcfg_mesh_ssid: str
    apcfg_mesh_eth_bridge: Literal["enable", "disable"]
    ble_profile: str
    lw_profile: str
    syslog_profile: str
    wan_port_mode: Literal["wan-lan", "wan-only"]
    lan: WtpProfileLanDict
    energy_efficient_ethernet: Literal["enable", "disable"]
    led_state: Literal["enable", "disable"]
    led_schedules: str | list[str] | list[WtpProfileLedschedulesItem]
    dtls_policy: str | list[str]
    dtls_in_kernel: Literal["enable", "disable"]
    max_clients: int
    handoff_rssi: int
    handoff_sta_thresh: int
    handoff_roaming: Literal["enable", "disable"]
    deny_mac_list: str | list[str] | list[WtpProfileDenymaclistItem]
    ap_country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"]
    ip_fragment_preventing: str | list[str]
    tun_mtu_uplink: int
    tun_mtu_downlink: int
    split_tunneling_acl_path: Literal["tunnel", "local"]
    split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"]
    split_tunneling_acl: str | list[str] | list[WtpProfileSplittunnelingaclItem]
    allowaccess: str | list[str]
    login_passwd_change: Literal["yes", "default", "no"]
    login_passwd: str
    lldp: Literal["enable", "disable"]
    poe_mode: Literal["auto", "8023af", "8023at", "power-adapter", "full", "high", "low"]
    usb_port: Literal["enable", "disable"]
    frequency_handoff: Literal["enable", "disable"]
    ap_handoff: Literal["enable", "disable"]
    default_mesh_root: Literal["enable", "disable"]
    radio_1: WtpProfileRadio1Dict
    radio_2: WtpProfileRadio2Dict
    radio_3: WtpProfileRadio3Dict
    radio_4: WtpProfileRadio4Dict
    lbs: WtpProfileLbsDict
    ext_info_enable: Literal["enable", "disable"]
    indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"]
    esl_ses_dongle: WtpProfileEslsesdongleDict
    console_login: Literal["enable", "disable"]
    wan_port_auth: Literal["none", "802.1x"]
    wan_port_auth_usrname: str
    wan_port_auth_password: str
    wan_port_auth_methods: Literal["all", "EAP-FAST", "EAP-TLS", "EAP-PEAP"]
    wan_port_auth_macsec: Literal["enable", "disable"]
    apcfg_auto_cert: Literal["enable", "disable"]
    apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"]
    apcfg_auto_cert_crypto_algo: Literal["rsa-1024", "rsa-1536", "rsa-2048", "rsa-4096", "ec-secp256r1", "ec-secp384r1", "ec-secp521r1"]
    apcfg_auto_cert_est_server: str
    apcfg_auto_cert_est_ca_id: str
    apcfg_auto_cert_est_http_username: str
    apcfg_auto_cert_est_http_password: str
    apcfg_auto_cert_est_subject: str
    apcfg_auto_cert_est_subject_alt_name: str
    apcfg_auto_cert_auto_regen_days: int
    apcfg_auto_cert_est_https_ca: str
    apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"]
    apcfg_auto_cert_scep_keysize: Literal["1024", "1536", "2048", "4096"]
    apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"]
    apcfg_auto_cert_scep_sub_fully_dn: str
    apcfg_auto_cert_scep_url: str
    apcfg_auto_cert_scep_password: str
    apcfg_auto_cert_scep_ca_id: str
    apcfg_auto_cert_scep_subject_alt_name: str
    apcfg_auto_cert_scep_https_ca: str
    unii_4_5ghz_band: Literal["enable", "disable"]
    admin_auth_tacacs_plus: str
    admin_restrict_local: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class WtpProfileResponse(TypedDict, total=False):
    """Response type for WtpProfile - use with .dict property for typed dict access."""
    name: str
    comment: str
    platform: WtpProfilePlatformDict
    control_message_offload: str
    bonjour_profile: str
    apcfg_profile: str
    apcfg_mesh: Literal["enable", "disable"]
    apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"]
    apcfg_mesh_ssid: str
    apcfg_mesh_eth_bridge: Literal["enable", "disable"]
    ble_profile: str
    lw_profile: str
    syslog_profile: str
    wan_port_mode: Literal["wan-lan", "wan-only"]
    lan: WtpProfileLanDict
    energy_efficient_ethernet: Literal["enable", "disable"]
    led_state: Literal["enable", "disable"]
    led_schedules: list[WtpProfileLedschedulesItem]
    dtls_policy: str
    dtls_in_kernel: Literal["enable", "disable"]
    max_clients: int
    handoff_rssi: int
    handoff_sta_thresh: int
    handoff_roaming: Literal["enable", "disable"]
    deny_mac_list: list[WtpProfileDenymaclistItem]
    ap_country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"]
    ip_fragment_preventing: str
    tun_mtu_uplink: int
    tun_mtu_downlink: int
    split_tunneling_acl_path: Literal["tunnel", "local"]
    split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"]
    split_tunneling_acl: list[WtpProfileSplittunnelingaclItem]
    allowaccess: str
    login_passwd_change: Literal["yes", "default", "no"]
    login_passwd: str
    lldp: Literal["enable", "disable"]
    poe_mode: Literal["auto", "8023af", "8023at", "power-adapter", "full", "high", "low"]
    usb_port: Literal["enable", "disable"]
    frequency_handoff: Literal["enable", "disable"]
    ap_handoff: Literal["enable", "disable"]
    default_mesh_root: Literal["enable", "disable"]
    radio_1: WtpProfileRadio1Dict
    radio_2: WtpProfileRadio2Dict
    radio_3: WtpProfileRadio3Dict
    radio_4: WtpProfileRadio4Dict
    lbs: WtpProfileLbsDict
    ext_info_enable: Literal["enable", "disable"]
    indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"]
    esl_ses_dongle: WtpProfileEslsesdongleDict
    console_login: Literal["enable", "disable"]
    wan_port_auth: Literal["none", "802.1x"]
    wan_port_auth_usrname: str
    wan_port_auth_password: str
    wan_port_auth_methods: Literal["all", "EAP-FAST", "EAP-TLS", "EAP-PEAP"]
    wan_port_auth_macsec: Literal["enable", "disable"]
    apcfg_auto_cert: Literal["enable", "disable"]
    apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"]
    apcfg_auto_cert_crypto_algo: Literal["rsa-1024", "rsa-1536", "rsa-2048", "rsa-4096", "ec-secp256r1", "ec-secp384r1", "ec-secp521r1"]
    apcfg_auto_cert_est_server: str
    apcfg_auto_cert_est_ca_id: str
    apcfg_auto_cert_est_http_username: str
    apcfg_auto_cert_est_http_password: str
    apcfg_auto_cert_est_subject: str
    apcfg_auto_cert_est_subject_alt_name: str
    apcfg_auto_cert_auto_regen_days: int
    apcfg_auto_cert_est_https_ca: str
    apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"]
    apcfg_auto_cert_scep_keysize: Literal["1024", "1536", "2048", "4096"]
    apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"]
    apcfg_auto_cert_scep_sub_fully_dn: str
    apcfg_auto_cert_scep_url: str
    apcfg_auto_cert_scep_password: str
    apcfg_auto_cert_scep_ca_id: str
    apcfg_auto_cert_scep_subject_alt_name: str
    apcfg_auto_cert_scep_https_ca: str
    unii_4_5ghz_band: Literal["enable", "disable"]
    admin_auth_tacacs_plus: str
    admin_restrict_local: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class WtpProfileLedschedulesItemObject(FortiObject[WtpProfileLedschedulesItem]):
    """Typed object for led-schedules table items with attribute access."""
    name: str


class WtpProfileDenymaclistItemObject(FortiObject[WtpProfileDenymaclistItem]):
    """Typed object for deny-mac-list table items with attribute access."""
    id: int
    mac: str


class WtpProfileSplittunnelingaclItemObject(FortiObject[WtpProfileSplittunnelingaclItem]):
    """Typed object for split-tunneling-acl table items with attribute access."""
    id: int
    dest_ip: str


class WtpProfileRadio1VapsItemObject(FortiObject[WtpProfileRadio1VapsItem]):
    """Typed object for radio-1.vaps table items with attribute access."""
    name: str


class WtpProfileRadio1ChannelItemObject(FortiObject[WtpProfileRadio1ChannelItem]):
    """Typed object for radio-1.channel table items with attribute access."""
    chan: str


class WtpProfileRadio2VapsItemObject(FortiObject[WtpProfileRadio2VapsItem]):
    """Typed object for radio-2.vaps table items with attribute access."""
    name: str


class WtpProfileRadio2ChannelItemObject(FortiObject[WtpProfileRadio2ChannelItem]):
    """Typed object for radio-2.channel table items with attribute access."""
    chan: str


class WtpProfileRadio3VapsItemObject(FortiObject[WtpProfileRadio3VapsItem]):
    """Typed object for radio-3.vaps table items with attribute access."""
    name: str


class WtpProfileRadio3ChannelItemObject(FortiObject[WtpProfileRadio3ChannelItem]):
    """Typed object for radio-3.channel table items with attribute access."""
    chan: str


class WtpProfileRadio4VapsItemObject(FortiObject[WtpProfileRadio4VapsItem]):
    """Typed object for radio-4.vaps table items with attribute access."""
    name: str


class WtpProfileRadio4ChannelItemObject(FortiObject[WtpProfileRadio4ChannelItem]):
    """Typed object for radio-4.channel table items with attribute access."""
    chan: str


class WtpProfilePlatformObject(FortiObject):
    """Nested object for platform field with attribute access."""
    type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"]
    mode: Literal["single-5G", "dual-5G"]
    ddscan: Literal["enable", "disable"]


class WtpProfileLanObject(FortiObject):
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


class WtpProfileRadio1Object(FortiObject):
    """Nested object for radio-1 field with attribute access."""
    mode: Literal["disabled", "ap", "monitor", "sniffer", "sam"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"]
    drma: Literal["disable", "enable"]
    drma_sensitivity: Literal["low", "medium", "high"]
    airtime_fairness: Literal["enable", "disable"]
    protection_mode: Literal["rtscts", "ctsonly", "disable"]
    powersave_optimize: Literal["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"]
    transmit_optimize: Literal["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"]
    amsdu: Literal["enable", "disable"]
    coexistence: Literal["enable", "disable"]
    zero_wait_dfs: Literal["enable", "disable"]
    bss_color: int
    bss_color_mode: Literal["auto", "static"]
    short_guard_interval: Literal["enable", "disable"]
    mimo_mode: Literal["default", "1x1", "2x2", "3x3", "4x4", "8x8"]
    channel_bonding: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"]
    optional_antenna: Literal["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"]
    optional_antenna_gain: str
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    dtim: int
    beacon_interval: int
    x80211d: Literal["enable", "disable"]
    x80211mc: Literal["enable", "disable"]
    rts_threshold: int
    frag_threshold: int
    ap_sniffer_bufsize: int
    ap_sniffer_chan: int
    ap_sniffer_chan_width: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    ap_sniffer_addr: str
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"]
    ap_sniffer_mgmt_probe: Literal["enable", "disable"]
    ap_sniffer_mgmt_other: Literal["enable", "disable"]
    ap_sniffer_ctl: Literal["enable", "disable"]
    ap_sniffer_data: Literal["enable", "disable"]
    sam_ssid: str
    sam_bssid: str
    sam_security_type: Literal["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"]
    sam_captive_portal: Literal["enable", "disable"]
    sam_cwp_username: str
    sam_cwp_password: str
    sam_cwp_test_url: str
    sam_cwp_match_string: str
    sam_cwp_success_string: str
    sam_cwp_failure_string: str
    sam_eap_method: Literal["both", "tls", "peap"]
    sam_client_certificate: str
    sam_private_key: str
    sam_private_key_password: str
    sam_ca_certificate: str
    sam_username: str
    sam_password: str
    sam_test: Literal["ping", "iperf"]
    sam_server_type: Literal["ip", "fqdn"]
    sam_server_ip: str
    sam_server_fqdn: str
    iperf_server_port: int
    iperf_protocol: Literal["udp", "tcp"]
    sam_report_intv: int
    channel_utilization: Literal["enable", "disable"]
    wids_profile: str
    ai_darrp_support: Literal["enable", "disable"]
    darrp: Literal["enable", "disable"]
    arrp_profile: str
    max_clients: int
    max_distance: int
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str]
    channel: str | list[str]
    call_admission_control: Literal["enable", "disable"]
    call_capacity: int
    bandwidth_admission_control: Literal["enable", "disable"]
    bandwidth_capacity: int


class WtpProfileRadio2Object(FortiObject):
    """Nested object for radio-2 field with attribute access."""
    mode: Literal["disabled", "ap", "monitor", "sniffer", "sam"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"]
    drma: Literal["disable", "enable"]
    drma_sensitivity: Literal["low", "medium", "high"]
    airtime_fairness: Literal["enable", "disable"]
    protection_mode: Literal["rtscts", "ctsonly", "disable"]
    powersave_optimize: Literal["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"]
    transmit_optimize: Literal["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"]
    amsdu: Literal["enable", "disable"]
    coexistence: Literal["enable", "disable"]
    zero_wait_dfs: Literal["enable", "disable"]
    bss_color: int
    bss_color_mode: Literal["auto", "static"]
    short_guard_interval: Literal["enable", "disable"]
    mimo_mode: Literal["default", "1x1", "2x2", "3x3", "4x4", "8x8"]
    channel_bonding: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"]
    optional_antenna: Literal["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"]
    optional_antenna_gain: str
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    dtim: int
    beacon_interval: int
    x80211d: Literal["enable", "disable"]
    x80211mc: Literal["enable", "disable"]
    rts_threshold: int
    frag_threshold: int
    ap_sniffer_bufsize: int
    ap_sniffer_chan: int
    ap_sniffer_chan_width: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    ap_sniffer_addr: str
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"]
    ap_sniffer_mgmt_probe: Literal["enable", "disable"]
    ap_sniffer_mgmt_other: Literal["enable", "disable"]
    ap_sniffer_ctl: Literal["enable", "disable"]
    ap_sniffer_data: Literal["enable", "disable"]
    sam_ssid: str
    sam_bssid: str
    sam_security_type: Literal["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"]
    sam_captive_portal: Literal["enable", "disable"]
    sam_cwp_username: str
    sam_cwp_password: str
    sam_cwp_test_url: str
    sam_cwp_match_string: str
    sam_cwp_success_string: str
    sam_cwp_failure_string: str
    sam_eap_method: Literal["both", "tls", "peap"]
    sam_client_certificate: str
    sam_private_key: str
    sam_private_key_password: str
    sam_ca_certificate: str
    sam_username: str
    sam_password: str
    sam_test: Literal["ping", "iperf"]
    sam_server_type: Literal["ip", "fqdn"]
    sam_server_ip: str
    sam_server_fqdn: str
    iperf_server_port: int
    iperf_protocol: Literal["udp", "tcp"]
    sam_report_intv: int
    channel_utilization: Literal["enable", "disable"]
    wids_profile: str
    ai_darrp_support: Literal["enable", "disable"]
    darrp: Literal["enable", "disable"]
    arrp_profile: str
    max_clients: int
    max_distance: int
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str]
    channel: str | list[str]
    call_admission_control: Literal["enable", "disable"]
    call_capacity: int
    bandwidth_admission_control: Literal["enable", "disable"]
    bandwidth_capacity: int


class WtpProfileRadio3Object(FortiObject):
    """Nested object for radio-3 field with attribute access."""
    mode: Literal["disabled", "ap", "monitor", "sniffer", "sam"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"]
    drma: Literal["disable", "enable"]
    drma_sensitivity: Literal["low", "medium", "high"]
    airtime_fairness: Literal["enable", "disable"]
    protection_mode: Literal["rtscts", "ctsonly", "disable"]
    powersave_optimize: Literal["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"]
    transmit_optimize: Literal["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"]
    amsdu: Literal["enable", "disable"]
    coexistence: Literal["enable", "disable"]
    zero_wait_dfs: Literal["enable", "disable"]
    bss_color: int
    bss_color_mode: Literal["auto", "static"]
    short_guard_interval: Literal["enable", "disable"]
    mimo_mode: Literal["default", "1x1", "2x2", "3x3", "4x4", "8x8"]
    channel_bonding: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"]
    optional_antenna: Literal["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"]
    optional_antenna_gain: str
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    dtim: int
    beacon_interval: int
    x80211d: Literal["enable", "disable"]
    x80211mc: Literal["enable", "disable"]
    rts_threshold: int
    frag_threshold: int
    ap_sniffer_bufsize: int
    ap_sniffer_chan: int
    ap_sniffer_chan_width: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    ap_sniffer_addr: str
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"]
    ap_sniffer_mgmt_probe: Literal["enable", "disable"]
    ap_sniffer_mgmt_other: Literal["enable", "disable"]
    ap_sniffer_ctl: Literal["enable", "disable"]
    ap_sniffer_data: Literal["enable", "disable"]
    sam_ssid: str
    sam_bssid: str
    sam_security_type: Literal["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"]
    sam_captive_portal: Literal["enable", "disable"]
    sam_cwp_username: str
    sam_cwp_password: str
    sam_cwp_test_url: str
    sam_cwp_match_string: str
    sam_cwp_success_string: str
    sam_cwp_failure_string: str
    sam_eap_method: Literal["both", "tls", "peap"]
    sam_client_certificate: str
    sam_private_key: str
    sam_private_key_password: str
    sam_ca_certificate: str
    sam_username: str
    sam_password: str
    sam_test: Literal["ping", "iperf"]
    sam_server_type: Literal["ip", "fqdn"]
    sam_server_ip: str
    sam_server_fqdn: str
    iperf_server_port: int
    iperf_protocol: Literal["udp", "tcp"]
    sam_report_intv: int
    channel_utilization: Literal["enable", "disable"]
    wids_profile: str
    ai_darrp_support: Literal["enable", "disable"]
    darrp: Literal["enable", "disable"]
    arrp_profile: str
    max_clients: int
    max_distance: int
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str]
    channel: str | list[str]
    call_admission_control: Literal["enable", "disable"]
    call_capacity: int
    bandwidth_admission_control: Literal["enable", "disable"]
    bandwidth_capacity: int


class WtpProfileRadio4Object(FortiObject):
    """Nested object for radio-4 field with attribute access."""
    mode: Literal["disabled", "ap", "monitor", "sniffer", "sam"]
    band: Literal["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"]
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"]
    drma: Literal["disable", "enable"]
    drma_sensitivity: Literal["low", "medium", "high"]
    airtime_fairness: Literal["enable", "disable"]
    protection_mode: Literal["rtscts", "ctsonly", "disable"]
    powersave_optimize: Literal["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"]
    transmit_optimize: Literal["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"]
    amsdu: Literal["enable", "disable"]
    coexistence: Literal["enable", "disable"]
    zero_wait_dfs: Literal["enable", "disable"]
    bss_color: int
    bss_color_mode: Literal["auto", "static"]
    short_guard_interval: Literal["enable", "disable"]
    mimo_mode: Literal["default", "1x1", "2x2", "3x3", "4x4", "8x8"]
    channel_bonding: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"]
    optional_antenna: Literal["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"]
    optional_antenna_gain: str
    auto_power_level: Literal["enable", "disable"]
    auto_power_high: int
    auto_power_low: int
    auto_power_target: str
    power_mode: Literal["dBm", "percentage"]
    power_level: int
    power_value: int
    dtim: int
    beacon_interval: int
    x80211d: Literal["enable", "disable"]
    x80211mc: Literal["enable", "disable"]
    rts_threshold: int
    frag_threshold: int
    ap_sniffer_bufsize: int
    ap_sniffer_chan: int
    ap_sniffer_chan_width: Literal["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"]
    ap_sniffer_addr: str
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"]
    ap_sniffer_mgmt_probe: Literal["enable", "disable"]
    ap_sniffer_mgmt_other: Literal["enable", "disable"]
    ap_sniffer_ctl: Literal["enable", "disable"]
    ap_sniffer_data: Literal["enable", "disable"]
    sam_ssid: str
    sam_bssid: str
    sam_security_type: Literal["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"]
    sam_captive_portal: Literal["enable", "disable"]
    sam_cwp_username: str
    sam_cwp_password: str
    sam_cwp_test_url: str
    sam_cwp_match_string: str
    sam_cwp_success_string: str
    sam_cwp_failure_string: str
    sam_eap_method: Literal["both", "tls", "peap"]
    sam_client_certificate: str
    sam_private_key: str
    sam_private_key_password: str
    sam_ca_certificate: str
    sam_username: str
    sam_password: str
    sam_test: Literal["ping", "iperf"]
    sam_server_type: Literal["ip", "fqdn"]
    sam_server_ip: str
    sam_server_fqdn: str
    iperf_server_port: int
    iperf_protocol: Literal["udp", "tcp"]
    sam_report_intv: int
    channel_utilization: Literal["enable", "disable"]
    wids_profile: str
    ai_darrp_support: Literal["enable", "disable"]
    darrp: Literal["enable", "disable"]
    arrp_profile: str
    max_clients: int
    max_distance: int
    vap_all: Literal["tunnel", "bridge", "manual"]
    vaps: str | list[str]
    channel: str | list[str]
    call_admission_control: Literal["enable", "disable"]
    call_capacity: int
    bandwidth_admission_control: Literal["enable", "disable"]
    bandwidth_capacity: int


class WtpProfileLbsObject(FortiObject):
    """Nested object for lbs field with attribute access."""
    ekahau_blink_mode: Literal["enable", "disable"]
    ekahau_tag: str
    erc_server_ip: str
    erc_server_port: int
    aeroscout: Literal["enable", "disable"]
    aeroscout_server_ip: str
    aeroscout_server_port: int
    aeroscout_mu: Literal["enable", "disable"]
    aeroscout_ap_mac: Literal["bssid", "board-mac"]
    aeroscout_mmu_report: Literal["enable", "disable"]
    aeroscout_mu_factor: int
    aeroscout_mu_timeout: int
    fortipresence: Literal["foreign", "both", "disable"]
    fortipresence_server_addr_type: Literal["ipv4", "fqdn"]
    fortipresence_server: str
    fortipresence_server_fqdn: str
    fortipresence_port: int
    fortipresence_secret: str
    fortipresence_project: str
    fortipresence_frequency: int
    fortipresence_rogue: Literal["enable", "disable"]
    fortipresence_unassoc: Literal["enable", "disable"]
    fortipresence_ble: Literal["enable", "disable"]
    station_locate: Literal["enable", "disable"]
    ble_rtls: Literal["none", "polestar", "evresys"]
    ble_rtls_protocol: Literal["WSS"]
    ble_rtls_server_fqdn: str
    ble_rtls_server_path: str
    ble_rtls_server_token: str
    ble_rtls_server_port: int
    ble_rtls_accumulation_interval: int
    ble_rtls_reporting_interval: int
    ble_rtls_asset_uuid_list1: str
    ble_rtls_asset_uuid_list2: str
    ble_rtls_asset_uuid_list3: str
    ble_rtls_asset_uuid_list4: str
    ble_rtls_asset_addrgrp_list: str


class WtpProfileEslsesdongleObject(FortiObject):
    """Nested object for esl-ses-dongle field with attribute access."""
    compliance_level: Literal["compliance-level-2"]
    scd_enable: Literal["enable", "disable"]
    esl_channel: Literal["-1", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "127"]
    output_power: Literal["a", "b", "c", "d", "e", "f", "g", "h"]
    apc_addr_type: Literal["fqdn", "ip"]
    apc_fqdn: str
    apc_ip: str
    apc_port: int
    coex_level: Literal["none"]
    tls_cert_verification: Literal["enable", "disable"]
    tls_fqdn_verification: Literal["enable", "disable"]


class WtpProfileObject(FortiObject):
    """Typed FortiObject for WtpProfile with field access."""
    name: str
    comment: str
    platform: WtpProfilePlatformObject
    control_message_offload: str
    bonjour_profile: str
    apcfg_profile: str
    apcfg_mesh: Literal["enable", "disable"]
    apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"]
    apcfg_mesh_ssid: str
    apcfg_mesh_eth_bridge: Literal["enable", "disable"]
    ble_profile: str
    lw_profile: str
    syslog_profile: str
    wan_port_mode: Literal["wan-lan", "wan-only"]
    lan: WtpProfileLanObject
    energy_efficient_ethernet: Literal["enable", "disable"]
    led_state: Literal["enable", "disable"]
    led_schedules: FortiObjectList[WtpProfileLedschedulesItemObject]
    dtls_policy: str
    dtls_in_kernel: Literal["enable", "disable"]
    max_clients: int
    handoff_rssi: int
    handoff_sta_thresh: int
    handoff_roaming: Literal["enable", "disable"]
    deny_mac_list: FortiObjectList[WtpProfileDenymaclistItemObject]
    ap_country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"]
    ip_fragment_preventing: str
    tun_mtu_uplink: int
    tun_mtu_downlink: int
    split_tunneling_acl_path: Literal["tunnel", "local"]
    split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"]
    split_tunneling_acl: FortiObjectList[WtpProfileSplittunnelingaclItemObject]
    allowaccess: str
    login_passwd_change: Literal["yes", "default", "no"]
    login_passwd: str
    lldp: Literal["enable", "disable"]
    poe_mode: Literal["auto", "8023af", "8023at", "power-adapter", "full", "high", "low"]
    usb_port: Literal["enable", "disable"]
    frequency_handoff: Literal["enable", "disable"]
    ap_handoff: Literal["enable", "disable"]
    default_mesh_root: Literal["enable", "disable"]
    radio_1: WtpProfileRadio1Object
    radio_2: WtpProfileRadio2Object
    radio_3: WtpProfileRadio3Object
    radio_4: WtpProfileRadio4Object
    lbs: WtpProfileLbsObject
    ext_info_enable: Literal["enable", "disable"]
    indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"]
    esl_ses_dongle: WtpProfileEslsesdongleObject
    console_login: Literal["enable", "disable"]
    wan_port_auth: Literal["none", "802.1x"]
    wan_port_auth_usrname: str
    wan_port_auth_password: str
    wan_port_auth_methods: Literal["all", "EAP-FAST", "EAP-TLS", "EAP-PEAP"]
    wan_port_auth_macsec: Literal["enable", "disable"]
    apcfg_auto_cert: Literal["enable", "disable"]
    apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"]
    apcfg_auto_cert_crypto_algo: Literal["rsa-1024", "rsa-1536", "rsa-2048", "rsa-4096", "ec-secp256r1", "ec-secp384r1", "ec-secp521r1"]
    apcfg_auto_cert_est_server: str
    apcfg_auto_cert_est_ca_id: str
    apcfg_auto_cert_est_http_username: str
    apcfg_auto_cert_est_http_password: str
    apcfg_auto_cert_est_subject: str
    apcfg_auto_cert_est_subject_alt_name: str
    apcfg_auto_cert_auto_regen_days: int
    apcfg_auto_cert_est_https_ca: str
    apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"]
    apcfg_auto_cert_scep_keysize: Literal["1024", "1536", "2048", "4096"]
    apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"]
    apcfg_auto_cert_scep_sub_fully_dn: str
    apcfg_auto_cert_scep_url: str
    apcfg_auto_cert_scep_password: str
    apcfg_auto_cert_scep_ca_id: str
    apcfg_auto_cert_scep_subject_alt_name: str
    apcfg_auto_cert_scep_https_ca: str
    unii_4_5ghz_band: Literal["enable", "disable"]
    admin_auth_tacacs_plus: str
    admin_restrict_local: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class WtpProfile:
    """
    
    Endpoint: wireless_controller/wtp_profile
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
    ) -> WtpProfileObject: ...
    
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
    ) -> FortiObjectList[WtpProfileObject]: ...
    
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
        payload_dict: WtpProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        platform: WtpProfilePlatformDict | None = ...,
        control_message_offload: str | list[str] | None = ...,
        bonjour_profile: str | None = ...,
        apcfg_profile: str | None = ...,
        apcfg_mesh: Literal["enable", "disable"] | None = ...,
        apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"] | None = ...,
        apcfg_mesh_ssid: str | None = ...,
        apcfg_mesh_eth_bridge: Literal["enable", "disable"] | None = ...,
        ble_profile: str | None = ...,
        lw_profile: str | None = ...,
        syslog_profile: str | None = ...,
        wan_port_mode: Literal["wan-lan", "wan-only"] | None = ...,
        lan: WtpProfileLanDict | None = ...,
        energy_efficient_ethernet: Literal["enable", "disable"] | None = ...,
        led_state: Literal["enable", "disable"] | None = ...,
        led_schedules: str | list[str] | list[WtpProfileLedschedulesItem] | None = ...,
        dtls_policy: str | list[str] | None = ...,
        dtls_in_kernel: Literal["enable", "disable"] | None = ...,
        max_clients: int | None = ...,
        handoff_rssi: int | None = ...,
        handoff_sta_thresh: int | None = ...,
        handoff_roaming: Literal["enable", "disable"] | None = ...,
        deny_mac_list: str | list[str] | list[WtpProfileDenymaclistItem] | None = ...,
        ap_country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"] | None = ...,
        ip_fragment_preventing: str | list[str] | None = ...,
        tun_mtu_uplink: int | None = ...,
        tun_mtu_downlink: int | None = ...,
        split_tunneling_acl_path: Literal["tunnel", "local"] | None = ...,
        split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = ...,
        split_tunneling_acl: str | list[str] | list[WtpProfileSplittunnelingaclItem] | None = ...,
        allowaccess: str | list[str] | None = ...,
        login_passwd_change: Literal["yes", "default", "no"] | None = ...,
        login_passwd: str | None = ...,
        lldp: Literal["enable", "disable"] | None = ...,
        poe_mode: Literal["auto", "8023af", "8023at", "power-adapter", "full", "high", "low"] | None = ...,
        usb_port: Literal["enable", "disable"] | None = ...,
        frequency_handoff: Literal["enable", "disable"] | None = ...,
        ap_handoff: Literal["enable", "disable"] | None = ...,
        default_mesh_root: Literal["enable", "disable"] | None = ...,
        radio_1: WtpProfileRadio1Dict | None = ...,
        radio_2: WtpProfileRadio2Dict | None = ...,
        radio_3: WtpProfileRadio3Dict | None = ...,
        radio_4: WtpProfileRadio4Dict | None = ...,
        lbs: WtpProfileLbsDict | None = ...,
        ext_info_enable: Literal["enable", "disable"] | None = ...,
        indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"] | None = ...,
        esl_ses_dongle: WtpProfileEslsesdongleDict | None = ...,
        console_login: Literal["enable", "disable"] | None = ...,
        wan_port_auth: Literal["none", "802.1x"] | None = ...,
        wan_port_auth_usrname: str | None = ...,
        wan_port_auth_password: str | None = ...,
        wan_port_auth_methods: Literal["all", "EAP-FAST", "EAP-TLS", "EAP-PEAP"] | None = ...,
        wan_port_auth_macsec: Literal["enable", "disable"] | None = ...,
        apcfg_auto_cert: Literal["enable", "disable"] | None = ...,
        apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"] | None = ...,
        apcfg_auto_cert_crypto_algo: Literal["rsa-1024", "rsa-1536", "rsa-2048", "rsa-4096", "ec-secp256r1", "ec-secp384r1", "ec-secp521r1"] | None = ...,
        apcfg_auto_cert_est_server: str | None = ...,
        apcfg_auto_cert_est_ca_id: str | None = ...,
        apcfg_auto_cert_est_http_username: str | None = ...,
        apcfg_auto_cert_est_http_password: str | None = ...,
        apcfg_auto_cert_est_subject: str | None = ...,
        apcfg_auto_cert_est_subject_alt_name: str | None = ...,
        apcfg_auto_cert_auto_regen_days: int | None = ...,
        apcfg_auto_cert_est_https_ca: str | None = ...,
        apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"] | None = ...,
        apcfg_auto_cert_scep_keysize: Literal["1024", "1536", "2048", "4096"] | None = ...,
        apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"] | None = ...,
        apcfg_auto_cert_scep_sub_fully_dn: str | None = ...,
        apcfg_auto_cert_scep_url: str | None = ...,
        apcfg_auto_cert_scep_password: str | None = ...,
        apcfg_auto_cert_scep_ca_id: str | None = ...,
        apcfg_auto_cert_scep_subject_alt_name: str | None = ...,
        apcfg_auto_cert_scep_https_ca: str | None = ...,
        unii_4_5ghz_band: Literal["enable", "disable"] | None = ...,
        admin_auth_tacacs_plus: str | None = ...,
        admin_restrict_local: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WtpProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: WtpProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        platform: WtpProfilePlatformDict | None = ...,
        control_message_offload: str | list[str] | None = ...,
        bonjour_profile: str | None = ...,
        apcfg_profile: str | None = ...,
        apcfg_mesh: Literal["enable", "disable"] | None = ...,
        apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"] | None = ...,
        apcfg_mesh_ssid: str | None = ...,
        apcfg_mesh_eth_bridge: Literal["enable", "disable"] | None = ...,
        ble_profile: str | None = ...,
        lw_profile: str | None = ...,
        syslog_profile: str | None = ...,
        wan_port_mode: Literal["wan-lan", "wan-only"] | None = ...,
        lan: WtpProfileLanDict | None = ...,
        energy_efficient_ethernet: Literal["enable", "disable"] | None = ...,
        led_state: Literal["enable", "disable"] | None = ...,
        led_schedules: str | list[str] | list[WtpProfileLedschedulesItem] | None = ...,
        dtls_policy: str | list[str] | None = ...,
        dtls_in_kernel: Literal["enable", "disable"] | None = ...,
        max_clients: int | None = ...,
        handoff_rssi: int | None = ...,
        handoff_sta_thresh: int | None = ...,
        handoff_roaming: Literal["enable", "disable"] | None = ...,
        deny_mac_list: str | list[str] | list[WtpProfileDenymaclistItem] | None = ...,
        ap_country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"] | None = ...,
        ip_fragment_preventing: str | list[str] | None = ...,
        tun_mtu_uplink: int | None = ...,
        tun_mtu_downlink: int | None = ...,
        split_tunneling_acl_path: Literal["tunnel", "local"] | None = ...,
        split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = ...,
        split_tunneling_acl: str | list[str] | list[WtpProfileSplittunnelingaclItem] | None = ...,
        allowaccess: str | list[str] | None = ...,
        login_passwd_change: Literal["yes", "default", "no"] | None = ...,
        login_passwd: str | None = ...,
        lldp: Literal["enable", "disable"] | None = ...,
        poe_mode: Literal["auto", "8023af", "8023at", "power-adapter", "full", "high", "low"] | None = ...,
        usb_port: Literal["enable", "disable"] | None = ...,
        frequency_handoff: Literal["enable", "disable"] | None = ...,
        ap_handoff: Literal["enable", "disable"] | None = ...,
        default_mesh_root: Literal["enable", "disable"] | None = ...,
        radio_1: WtpProfileRadio1Dict | None = ...,
        radio_2: WtpProfileRadio2Dict | None = ...,
        radio_3: WtpProfileRadio3Dict | None = ...,
        radio_4: WtpProfileRadio4Dict | None = ...,
        lbs: WtpProfileLbsDict | None = ...,
        ext_info_enable: Literal["enable", "disable"] | None = ...,
        indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"] | None = ...,
        esl_ses_dongle: WtpProfileEslsesdongleDict | None = ...,
        console_login: Literal["enable", "disable"] | None = ...,
        wan_port_auth: Literal["none", "802.1x"] | None = ...,
        wan_port_auth_usrname: str | None = ...,
        wan_port_auth_password: str | None = ...,
        wan_port_auth_methods: Literal["all", "EAP-FAST", "EAP-TLS", "EAP-PEAP"] | None = ...,
        wan_port_auth_macsec: Literal["enable", "disable"] | None = ...,
        apcfg_auto_cert: Literal["enable", "disable"] | None = ...,
        apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"] | None = ...,
        apcfg_auto_cert_crypto_algo: Literal["rsa-1024", "rsa-1536", "rsa-2048", "rsa-4096", "ec-secp256r1", "ec-secp384r1", "ec-secp521r1"] | None = ...,
        apcfg_auto_cert_est_server: str | None = ...,
        apcfg_auto_cert_est_ca_id: str | None = ...,
        apcfg_auto_cert_est_http_username: str | None = ...,
        apcfg_auto_cert_est_http_password: str | None = ...,
        apcfg_auto_cert_est_subject: str | None = ...,
        apcfg_auto_cert_est_subject_alt_name: str | None = ...,
        apcfg_auto_cert_auto_regen_days: int | None = ...,
        apcfg_auto_cert_est_https_ca: str | None = ...,
        apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"] | None = ...,
        apcfg_auto_cert_scep_keysize: Literal["1024", "1536", "2048", "4096"] | None = ...,
        apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"] | None = ...,
        apcfg_auto_cert_scep_sub_fully_dn: str | None = ...,
        apcfg_auto_cert_scep_url: str | None = ...,
        apcfg_auto_cert_scep_password: str | None = ...,
        apcfg_auto_cert_scep_ca_id: str | None = ...,
        apcfg_auto_cert_scep_subject_alt_name: str | None = ...,
        apcfg_auto_cert_scep_https_ca: str | None = ...,
        unii_4_5ghz_band: Literal["enable", "disable"] | None = ...,
        admin_auth_tacacs_plus: str | None = ...,
        admin_restrict_local: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WtpProfileObject: ...

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
        payload_dict: WtpProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        platform: WtpProfilePlatformDict | None = ...,
        control_message_offload: Literal["ebp-frame", "aeroscout-tag", "ap-list", "sta-list", "sta-cap-list", "stats", "aeroscout-mu", "sta-health", "spectral-analysis"] | list[str] | None = ...,
        bonjour_profile: str | None = ...,
        apcfg_profile: str | None = ...,
        apcfg_mesh: Literal["enable", "disable"] | None = ...,
        apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"] | None = ...,
        apcfg_mesh_ssid: str | None = ...,
        apcfg_mesh_eth_bridge: Literal["enable", "disable"] | None = ...,
        ble_profile: str | None = ...,
        lw_profile: str | None = ...,
        syslog_profile: str | None = ...,
        wan_port_mode: Literal["wan-lan", "wan-only"] | None = ...,
        lan: WtpProfileLanDict | None = ...,
        energy_efficient_ethernet: Literal["enable", "disable"] | None = ...,
        led_state: Literal["enable", "disable"] | None = ...,
        led_schedules: str | list[str] | list[WtpProfileLedschedulesItem] | None = ...,
        dtls_policy: Literal["clear-text", "dtls-enabled", "ipsec-vpn", "ipsec-sn-vpn"] | list[str] | None = ...,
        dtls_in_kernel: Literal["enable", "disable"] | None = ...,
        max_clients: int | None = ...,
        handoff_rssi: int | None = ...,
        handoff_sta_thresh: int | None = ...,
        handoff_roaming: Literal["enable", "disable"] | None = ...,
        deny_mac_list: str | list[str] | list[WtpProfileDenymaclistItem] | None = ...,
        ap_country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"] | None = ...,
        ip_fragment_preventing: Literal["tcp-mss-adjust", "icmp-unreachable"] | list[str] | None = ...,
        tun_mtu_uplink: int | None = ...,
        tun_mtu_downlink: int | None = ...,
        split_tunneling_acl_path: Literal["tunnel", "local"] | None = ...,
        split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = ...,
        split_tunneling_acl: str | list[str] | list[WtpProfileSplittunnelingaclItem] | None = ...,
        allowaccess: Literal["https", "ssh", "snmp"] | list[str] | None = ...,
        login_passwd_change: Literal["yes", "default", "no"] | None = ...,
        login_passwd: str | None = ...,
        lldp: Literal["enable", "disable"] | None = ...,
        poe_mode: Literal["auto", "8023af", "8023at", "power-adapter", "full", "high", "low"] | None = ...,
        usb_port: Literal["enable", "disable"] | None = ...,
        frequency_handoff: Literal["enable", "disable"] | None = ...,
        ap_handoff: Literal["enable", "disable"] | None = ...,
        default_mesh_root: Literal["enable", "disable"] | None = ...,
        radio_1: WtpProfileRadio1Dict | None = ...,
        radio_2: WtpProfileRadio2Dict | None = ...,
        radio_3: WtpProfileRadio3Dict | None = ...,
        radio_4: WtpProfileRadio4Dict | None = ...,
        lbs: WtpProfileLbsDict | None = ...,
        ext_info_enable: Literal["enable", "disable"] | None = ...,
        indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"] | None = ...,
        esl_ses_dongle: WtpProfileEslsesdongleDict | None = ...,
        console_login: Literal["enable", "disable"] | None = ...,
        wan_port_auth: Literal["none", "802.1x"] | None = ...,
        wan_port_auth_usrname: str | None = ...,
        wan_port_auth_password: str | None = ...,
        wan_port_auth_methods: Literal["all", "EAP-FAST", "EAP-TLS", "EAP-PEAP"] | None = ...,
        wan_port_auth_macsec: Literal["enable", "disable"] | None = ...,
        apcfg_auto_cert: Literal["enable", "disable"] | None = ...,
        apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"] | None = ...,
        apcfg_auto_cert_crypto_algo: Literal["rsa-1024", "rsa-1536", "rsa-2048", "rsa-4096", "ec-secp256r1", "ec-secp384r1", "ec-secp521r1"] | None = ...,
        apcfg_auto_cert_est_server: str | None = ...,
        apcfg_auto_cert_est_ca_id: str | None = ...,
        apcfg_auto_cert_est_http_username: str | None = ...,
        apcfg_auto_cert_est_http_password: str | None = ...,
        apcfg_auto_cert_est_subject: str | None = ...,
        apcfg_auto_cert_est_subject_alt_name: str | None = ...,
        apcfg_auto_cert_auto_regen_days: int | None = ...,
        apcfg_auto_cert_est_https_ca: str | None = ...,
        apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"] | None = ...,
        apcfg_auto_cert_scep_keysize: Literal["1024", "1536", "2048", "4096"] | None = ...,
        apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"] | None = ...,
        apcfg_auto_cert_scep_sub_fully_dn: str | None = ...,
        apcfg_auto_cert_scep_url: str | None = ...,
        apcfg_auto_cert_scep_password: str | None = ...,
        apcfg_auto_cert_scep_ca_id: str | None = ...,
        apcfg_auto_cert_scep_subject_alt_name: str | None = ...,
        apcfg_auto_cert_scep_https_ca: str | None = ...,
        unii_4_5ghz_band: Literal["enable", "disable"] | None = ...,
        admin_auth_tacacs_plus: str | None = ...,
        admin_restrict_local: Literal["enable", "disable"] | None = ...,
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
    "WtpProfile",
    "WtpProfilePayload",
    "WtpProfileResponse",
    "WtpProfileObject",
]