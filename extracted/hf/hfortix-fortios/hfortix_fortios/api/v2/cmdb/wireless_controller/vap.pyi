""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/vap
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

class VapRadiusmacauthusergroupsItem(TypedDict, total=False):
    """Nested item for radius-mac-auth-usergroups field."""
    name: str


class VapUsergroupItem(TypedDict, total=False):
    """Nested item for usergroup field."""
    name: str


class VapPortalmessageoverridesDict(TypedDict, total=False):
    """Nested object type for portal-message-overrides field."""
    auth_disclaimer_page: str
    auth_reject_page: str
    auth_login_page: str
    auth_login_failed_page: str


class VapSelectedusergroupsItem(TypedDict, total=False):
    """Nested item for selected-usergroups field."""
    name: str


class VapScheduleItem(TypedDict, total=False):
    """Nested item for schedule field."""
    name: str


class VapVlannameItem(TypedDict, total=False):
    """Nested item for vlan-name field."""
    name: str
    vlan_id: int | list[int]


class VapVlanpoolItem(TypedDict, total=False):
    """Nested item for vlan-pool field."""
    id: int
    wtp_group: str


class VapPayload(TypedDict, total=False):
    """Payload type for Vap operations."""
    name: str
    pre_auth: Literal["enable", "disable"]
    external_pre_auth: Literal["enable", "disable"]
    mesh_backhaul: Literal["enable", "disable"]
    atf_weight: int
    max_clients: int
    max_clients_ap: int
    ssid: str
    broadcast_ssid: Literal["enable", "disable"]
    security: Literal["open", "wep64", "wep128", "wpa-personal", "wpa-enterprise", "wpa-only-personal", "wpa-only-enterprise", "wpa2-only-personal", "wpa2-only-enterprise", "wpa3-enterprise", "wpa3-only-enterprise", "wpa3-enterprise-transition", "wpa3-sae", "wpa3-sae-transition", "owe", "osen"]
    pmf: Literal["disable", "enable", "optional"]
    pmf_assoc_comeback_timeout: int
    pmf_sa_query_retry_timeout: int
    beacon_protection: Literal["disable", "enable"]
    okc: Literal["disable", "enable"]
    mbo: Literal["disable", "enable"]
    gas_comeback_delay: int
    gas_fragmentation_limit: int
    mbo_cell_data_conn_pref: Literal["excluded", "prefer-not", "prefer-use"]
    x80211k: Literal["disable", "enable"]
    x80211v: Literal["disable", "enable"]
    neighbor_report_dual_band: Literal["disable", "enable"]
    fast_bss_transition: Literal["disable", "enable"]
    ft_mobility_domain: int
    ft_r0_key_lifetime: int
    ft_over_ds: Literal["disable", "enable"]
    sae_groups: str | list[str]
    owe_groups: str | list[str]
    owe_transition: Literal["disable", "enable"]
    owe_transition_ssid: str
    additional_akms: str | list[str]
    eapol_key_retries: Literal["disable", "enable"]
    tkip_counter_measure: Literal["enable", "disable"]
    external_web: str
    external_web_format: Literal["auto-detect", "no-query-string", "partial-query-string"]
    external_logout: str
    mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_calling_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_called_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_case: Literal["uppercase", "lowercase"]
    called_station_id_type: Literal["mac", "ip", "apname"]
    mac_auth_bypass: Literal["enable", "disable"]
    radius_mac_auth: Literal["enable", "disable"]
    radius_mac_auth_server: str
    radius_mac_auth_block_interval: int
    radius_mac_mpsk_auth: Literal["enable", "disable"]
    radius_mac_mpsk_timeout: int
    radius_mac_auth_usergroups: str | list[str] | list[VapRadiusmacauthusergroupsItem]
    auth: Literal["radius", "usergroup"]
    encrypt: Literal["TKIP", "AES", "TKIP-AES"]
    keyindex: int
    key: str
    passphrase: str
    sae_password: str
    sae_h2e_only: Literal["enable", "disable"]
    sae_hnp_only: Literal["enable", "disable"]
    sae_pk: Literal["enable", "disable"]
    sae_private_key: str
    akm24_only: Literal["disable", "enable"]
    radius_server: str
    nas_filter_rule: Literal["enable", "disable"]
    domain_name_stripping: Literal["disable", "enable"]
    mlo: Literal["disable", "enable"]
    local_standalone: Literal["enable", "disable"]
    local_standalone_nat: Literal["enable", "disable"]
    ip: str
    dhcp_lease_time: int
    local_standalone_dns: Literal["enable", "disable"]
    local_standalone_dns_ip: str | list[str]
    local_lan_partition: Literal["enable", "disable"]
    local_bridging: Literal["enable", "disable"]
    local_lan: Literal["allow", "deny"]
    local_authentication: Literal["enable", "disable"]
    usergroup: str | list[str] | list[VapUsergroupItem]
    captive_portal: Literal["enable", "disable"]
    captive_network_assistant_bypass: Literal["enable", "disable"]
    portal_message_override_group: str
    portal_message_overrides: VapPortalmessageoverridesDict
    portal_type: Literal["auth", "auth+disclaimer", "disclaimer", "email-collect", "cmcc", "cmcc-macauth", "auth-mac", "external-auth", "external-macauth"]
    selected_usergroups: str | list[str] | list[VapSelectedusergroupsItem]
    security_exempt_list: str
    security_redirect_url: str
    auth_cert: str
    auth_portal_addr: str
    intra_vap_privacy: Literal["enable", "disable"]
    schedule: str | list[str] | list[VapScheduleItem]
    ldpc: Literal["disable", "rx", "tx", "rxtx"]
    high_efficiency: Literal["enable", "disable"]
    target_wake_time: Literal["enable", "disable"]
    port_macauth: Literal["disable", "radius", "address-group"]
    port_macauth_timeout: int
    port_macauth_reauth_timeout: int
    bss_color_partial: Literal["enable", "disable"]
    mpsk_profile: str
    split_tunneling: Literal["enable", "disable"]
    nac: Literal["enable", "disable"]
    nac_profile: str
    vlanid: int
    vlan_auto: Literal["enable", "disable"]
    dynamic_vlan: Literal["enable", "disable"]
    captive_portal_fw_accounting: Literal["enable", "disable"]
    captive_portal_ac_name: str
    captive_portal_auth_timeout: int
    multicast_rate: Literal["0", "6000", "12000", "24000"]
    multicast_enhance: Literal["enable", "disable"]
    igmp_snooping: Literal["enable", "disable"]
    dhcp_address_enforcement: Literal["enable", "disable"]
    broadcast_suppression: str | list[str]
    ipv6_rules: str | list[str]
    me_disable_thresh: int
    mu_mimo: Literal["enable", "disable"]
    probe_resp_suppression: Literal["enable", "disable"]
    probe_resp_threshold: str
    radio_sensitivity: Literal["enable", "disable"]
    quarantine: Literal["enable", "disable"]
    radio_5g_threshold: str
    radio_2g_threshold: str
    vlan_name: str | list[str] | list[VapVlannameItem]
    vlan_pooling: Literal["wtp-group", "round-robin", "hash", "disable"]
    vlan_pool: str | list[str] | list[VapVlanpoolItem]
    dhcp_option43_insertion: Literal["enable", "disable"]
    dhcp_option82_insertion: Literal["enable", "disable"]
    dhcp_option82_circuit_id_insertion: Literal["style-1", "style-2", "style-3", "disable"]
    dhcp_option82_remote_id_insertion: Literal["style-1", "disable"]
    ptk_rekey: Literal["enable", "disable"]
    ptk_rekey_intv: int
    gtk_rekey: Literal["enable", "disable"]
    gtk_rekey_intv: int
    eap_reauth: Literal["enable", "disable"]
    eap_reauth_intv: int
    roaming_acct_interim_update: Literal["enable", "disable"]
    qos_profile: str
    hotspot20_profile: str
    access_control_list: str
    primary_wag_profile: str
    secondary_wag_profile: str
    tunnel_echo_interval: int
    tunnel_fallback_interval: int
    rates_11a: str | list[str]
    rates_11bg: str | list[str]
    rates_11n_ss12: str | list[str]
    rates_11n_ss34: str | list[str]
    rates_11ac_mcs_map: str
    rates_11ax_mcs_map: str
    rates_11be_mcs_map: str
    rates_11be_mcs_map_160: str
    rates_11be_mcs_map_320: str
    utm_profile: str
    utm_status: Literal["enable", "disable"]
    utm_log: Literal["enable", "disable"]
    ips_sensor: str
    application_list: str
    antivirus_profile: str
    webfilter_profile: str
    scan_botnet_connections: Literal["disable", "monitor", "block"]
    address_group: str
    address_group_policy: Literal["disable", "allow", "deny"]
    sticky_client_remove: Literal["enable", "disable"]
    sticky_client_threshold_5g: str
    sticky_client_threshold_2g: str
    sticky_client_threshold_6g: str
    bstm_rssi_disassoc_timer: int
    bstm_load_balancing_disassoc_timer: int
    bstm_disassociation_imminent: Literal["enable", "disable"]
    beacon_advertising: str | list[str]
    osen: Literal["enable", "disable"]
    application_detection_engine: Literal["enable", "disable"]
    application_dscp_marking: Literal["enable", "disable"]
    application_report_intv: int
    l3_roaming: Literal["enable", "disable"]
    l3_roaming_mode: Literal["direct", "indirect"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VapResponse(TypedDict, total=False):
    """Response type for Vap - use with .dict property for typed dict access."""
    name: str
    pre_auth: Literal["enable", "disable"]
    external_pre_auth: Literal["enable", "disable"]
    mesh_backhaul: Literal["enable", "disable"]
    atf_weight: int
    max_clients: int
    max_clients_ap: int
    ssid: str
    broadcast_ssid: Literal["enable", "disable"]
    security: Literal["open", "wep64", "wep128", "wpa-personal", "wpa-enterprise", "wpa-only-personal", "wpa-only-enterprise", "wpa2-only-personal", "wpa2-only-enterprise", "wpa3-enterprise", "wpa3-only-enterprise", "wpa3-enterprise-transition", "wpa3-sae", "wpa3-sae-transition", "owe", "osen"]
    pmf: Literal["disable", "enable", "optional"]
    pmf_assoc_comeback_timeout: int
    pmf_sa_query_retry_timeout: int
    beacon_protection: Literal["disable", "enable"]
    okc: Literal["disable", "enable"]
    mbo: Literal["disable", "enable"]
    gas_comeback_delay: int
    gas_fragmentation_limit: int
    mbo_cell_data_conn_pref: Literal["excluded", "prefer-not", "prefer-use"]
    x80211k: Literal["disable", "enable"]
    x80211v: Literal["disable", "enable"]
    neighbor_report_dual_band: Literal["disable", "enable"]
    fast_bss_transition: Literal["disable", "enable"]
    ft_mobility_domain: int
    ft_r0_key_lifetime: int
    ft_over_ds: Literal["disable", "enable"]
    sae_groups: str
    owe_groups: str
    owe_transition: Literal["disable", "enable"]
    owe_transition_ssid: str
    additional_akms: str
    eapol_key_retries: Literal["disable", "enable"]
    tkip_counter_measure: Literal["enable", "disable"]
    external_web: str
    external_web_format: Literal["auto-detect", "no-query-string", "partial-query-string"]
    external_logout: str
    mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_calling_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_called_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_case: Literal["uppercase", "lowercase"]
    called_station_id_type: Literal["mac", "ip", "apname"]
    mac_auth_bypass: Literal["enable", "disable"]
    radius_mac_auth: Literal["enable", "disable"]
    radius_mac_auth_server: str
    radius_mac_auth_block_interval: int
    radius_mac_mpsk_auth: Literal["enable", "disable"]
    radius_mac_mpsk_timeout: int
    radius_mac_auth_usergroups: list[VapRadiusmacauthusergroupsItem]
    auth: Literal["radius", "usergroup"]
    encrypt: Literal["TKIP", "AES", "TKIP-AES"]
    keyindex: int
    key: str
    passphrase: str
    sae_password: str
    sae_h2e_only: Literal["enable", "disable"]
    sae_hnp_only: Literal["enable", "disable"]
    sae_pk: Literal["enable", "disable"]
    sae_private_key: str
    akm24_only: Literal["disable", "enable"]
    radius_server: str
    nas_filter_rule: Literal["enable", "disable"]
    domain_name_stripping: Literal["disable", "enable"]
    mlo: Literal["disable", "enable"]
    local_standalone: Literal["enable", "disable"]
    local_standalone_nat: Literal["enable", "disable"]
    ip: str
    dhcp_lease_time: int
    local_standalone_dns: Literal["enable", "disable"]
    local_standalone_dns_ip: str | list[str]
    local_lan_partition: Literal["enable", "disable"]
    local_bridging: Literal["enable", "disable"]
    local_lan: Literal["allow", "deny"]
    local_authentication: Literal["enable", "disable"]
    usergroup: list[VapUsergroupItem]
    captive_portal: Literal["enable", "disable"]
    captive_network_assistant_bypass: Literal["enable", "disable"]
    portal_message_override_group: str
    portal_message_overrides: VapPortalmessageoverridesDict
    portal_type: Literal["auth", "auth+disclaimer", "disclaimer", "email-collect", "cmcc", "cmcc-macauth", "auth-mac", "external-auth", "external-macauth"]
    selected_usergroups: list[VapSelectedusergroupsItem]
    security_exempt_list: str
    security_redirect_url: str
    auth_cert: str
    auth_portal_addr: str
    intra_vap_privacy: Literal["enable", "disable"]
    schedule: list[VapScheduleItem]
    ldpc: Literal["disable", "rx", "tx", "rxtx"]
    high_efficiency: Literal["enable", "disable"]
    target_wake_time: Literal["enable", "disable"]
    port_macauth: Literal["disable", "radius", "address-group"]
    port_macauth_timeout: int
    port_macauth_reauth_timeout: int
    bss_color_partial: Literal["enable", "disable"]
    mpsk_profile: str
    split_tunneling: Literal["enable", "disable"]
    nac: Literal["enable", "disable"]
    nac_profile: str
    vlanid: int
    vlan_auto: Literal["enable", "disable"]
    dynamic_vlan: Literal["enable", "disable"]
    captive_portal_fw_accounting: Literal["enable", "disable"]
    captive_portal_ac_name: str
    captive_portal_auth_timeout: int
    multicast_rate: Literal["0", "6000", "12000", "24000"]
    multicast_enhance: Literal["enable", "disable"]
    igmp_snooping: Literal["enable", "disable"]
    dhcp_address_enforcement: Literal["enable", "disable"]
    broadcast_suppression: str
    ipv6_rules: str
    me_disable_thresh: int
    mu_mimo: Literal["enable", "disable"]
    probe_resp_suppression: Literal["enable", "disable"]
    probe_resp_threshold: str
    radio_sensitivity: Literal["enable", "disable"]
    quarantine: Literal["enable", "disable"]
    radio_5g_threshold: str
    radio_2g_threshold: str
    vlan_name: list[VapVlannameItem]
    vlan_pooling: Literal["wtp-group", "round-robin", "hash", "disable"]
    vlan_pool: list[VapVlanpoolItem]
    dhcp_option43_insertion: Literal["enable", "disable"]
    dhcp_option82_insertion: Literal["enable", "disable"]
    dhcp_option82_circuit_id_insertion: Literal["style-1", "style-2", "style-3", "disable"]
    dhcp_option82_remote_id_insertion: Literal["style-1", "disable"]
    ptk_rekey: Literal["enable", "disable"]
    ptk_rekey_intv: int
    gtk_rekey: Literal["enable", "disable"]
    gtk_rekey_intv: int
    eap_reauth: Literal["enable", "disable"]
    eap_reauth_intv: int
    roaming_acct_interim_update: Literal["enable", "disable"]
    qos_profile: str
    hotspot20_profile: str
    access_control_list: str
    primary_wag_profile: str
    secondary_wag_profile: str
    tunnel_echo_interval: int
    tunnel_fallback_interval: int
    rates_11a: str
    rates_11bg: str
    rates_11n_ss12: str
    rates_11n_ss34: str
    rates_11ac_mcs_map: str
    rates_11ax_mcs_map: str
    rates_11be_mcs_map: str
    rates_11be_mcs_map_160: str
    rates_11be_mcs_map_320: str
    utm_profile: str
    utm_status: Literal["enable", "disable"]
    utm_log: Literal["enable", "disable"]
    ips_sensor: str
    application_list: str
    antivirus_profile: str
    webfilter_profile: str
    scan_botnet_connections: Literal["disable", "monitor", "block"]
    address_group: str
    address_group_policy: Literal["disable", "allow", "deny"]
    sticky_client_remove: Literal["enable", "disable"]
    sticky_client_threshold_5g: str
    sticky_client_threshold_2g: str
    sticky_client_threshold_6g: str
    bstm_rssi_disassoc_timer: int
    bstm_load_balancing_disassoc_timer: int
    bstm_disassociation_imminent: Literal["enable", "disable"]
    beacon_advertising: str
    osen: Literal["enable", "disable"]
    application_detection_engine: Literal["enable", "disable"]
    application_dscp_marking: Literal["enable", "disable"]
    application_report_intv: int
    l3_roaming: Literal["enable", "disable"]
    l3_roaming_mode: Literal["direct", "indirect"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VapRadiusmacauthusergroupsItemObject(FortiObject[VapRadiusmacauthusergroupsItem]):
    """Typed object for radius-mac-auth-usergroups table items with attribute access."""
    name: str


class VapUsergroupItemObject(FortiObject[VapUsergroupItem]):
    """Typed object for usergroup table items with attribute access."""
    name: str


class VapSelectedusergroupsItemObject(FortiObject[VapSelectedusergroupsItem]):
    """Typed object for selected-usergroups table items with attribute access."""
    name: str


class VapScheduleItemObject(FortiObject[VapScheduleItem]):
    """Typed object for schedule table items with attribute access."""
    name: str


class VapVlannameItemObject(FortiObject[VapVlannameItem]):
    """Typed object for vlan-name table items with attribute access."""
    name: str
    vlan_id: int | list[int]


class VapVlanpoolItemObject(FortiObject[VapVlanpoolItem]):
    """Typed object for vlan-pool table items with attribute access."""
    id: int
    wtp_group: str


class VapPortalmessageoverridesObject(FortiObject):
    """Nested object for portal-message-overrides field with attribute access."""
    auth_disclaimer_page: str
    auth_reject_page: str
    auth_login_page: str
    auth_login_failed_page: str


class VapObject(FortiObject):
    """Typed FortiObject for Vap with field access."""
    name: str
    pre_auth: Literal["enable", "disable"]
    external_pre_auth: Literal["enable", "disable"]
    mesh_backhaul: Literal["enable", "disable"]
    atf_weight: int
    max_clients: int
    max_clients_ap: int
    ssid: str
    broadcast_ssid: Literal["enable", "disable"]
    security: Literal["open", "wep64", "wep128", "wpa-personal", "wpa-enterprise", "wpa-only-personal", "wpa-only-enterprise", "wpa2-only-personal", "wpa2-only-enterprise", "wpa3-enterprise", "wpa3-only-enterprise", "wpa3-enterprise-transition", "wpa3-sae", "wpa3-sae-transition", "owe", "osen"]
    pmf: Literal["disable", "enable", "optional"]
    pmf_assoc_comeback_timeout: int
    pmf_sa_query_retry_timeout: int
    beacon_protection: Literal["disable", "enable"]
    okc: Literal["disable", "enable"]
    mbo: Literal["disable", "enable"]
    gas_comeback_delay: int
    gas_fragmentation_limit: int
    mbo_cell_data_conn_pref: Literal["excluded", "prefer-not", "prefer-use"]
    x80211k: Literal["disable", "enable"]
    x80211v: Literal["disable", "enable"]
    neighbor_report_dual_band: Literal["disable", "enable"]
    fast_bss_transition: Literal["disable", "enable"]
    ft_mobility_domain: int
    ft_r0_key_lifetime: int
    ft_over_ds: Literal["disable", "enable"]
    sae_groups: str
    owe_groups: str
    owe_transition: Literal["disable", "enable"]
    owe_transition_ssid: str
    additional_akms: str
    eapol_key_retries: Literal["disable", "enable"]
    tkip_counter_measure: Literal["enable", "disable"]
    external_web: str
    external_web_format: Literal["auto-detect", "no-query-string", "partial-query-string"]
    external_logout: str
    mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_calling_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_called_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_case: Literal["uppercase", "lowercase"]
    called_station_id_type: Literal["mac", "ip", "apname"]
    mac_auth_bypass: Literal["enable", "disable"]
    radius_mac_auth: Literal["enable", "disable"]
    radius_mac_auth_server: str
    radius_mac_auth_block_interval: int
    radius_mac_mpsk_auth: Literal["enable", "disable"]
    radius_mac_mpsk_timeout: int
    radius_mac_auth_usergroups: FortiObjectList[VapRadiusmacauthusergroupsItemObject]
    auth: Literal["radius", "usergroup"]
    encrypt: Literal["TKIP", "AES", "TKIP-AES"]
    keyindex: int
    key: str
    passphrase: str
    sae_password: str
    sae_h2e_only: Literal["enable", "disable"]
    sae_hnp_only: Literal["enable", "disable"]
    sae_pk: Literal["enable", "disable"]
    sae_private_key: str
    akm24_only: Literal["disable", "enable"]
    radius_server: str
    nas_filter_rule: Literal["enable", "disable"]
    domain_name_stripping: Literal["disable", "enable"]
    mlo: Literal["disable", "enable"]
    local_standalone: Literal["enable", "disable"]
    local_standalone_nat: Literal["enable", "disable"]
    ip: str
    dhcp_lease_time: int
    local_standalone_dns: Literal["enable", "disable"]
    local_standalone_dns_ip: str | list[str]
    local_lan_partition: Literal["enable", "disable"]
    local_bridging: Literal["enable", "disable"]
    local_lan: Literal["allow", "deny"]
    local_authentication: Literal["enable", "disable"]
    usergroup: FortiObjectList[VapUsergroupItemObject]
    captive_portal: Literal["enable", "disable"]
    captive_network_assistant_bypass: Literal["enable", "disable"]
    portal_message_override_group: str
    portal_message_overrides: VapPortalmessageoverridesObject
    portal_type: Literal["auth", "auth+disclaimer", "disclaimer", "email-collect", "cmcc", "cmcc-macauth", "auth-mac", "external-auth", "external-macauth"]
    selected_usergroups: FortiObjectList[VapSelectedusergroupsItemObject]
    security_exempt_list: str
    security_redirect_url: str
    auth_cert: str
    auth_portal_addr: str
    intra_vap_privacy: Literal["enable", "disable"]
    schedule: FortiObjectList[VapScheduleItemObject]
    ldpc: Literal["disable", "rx", "tx", "rxtx"]
    high_efficiency: Literal["enable", "disable"]
    target_wake_time: Literal["enable", "disable"]
    port_macauth: Literal["disable", "radius", "address-group"]
    port_macauth_timeout: int
    port_macauth_reauth_timeout: int
    bss_color_partial: Literal["enable", "disable"]
    mpsk_profile: str
    split_tunneling: Literal["enable", "disable"]
    nac: Literal["enable", "disable"]
    nac_profile: str
    vlanid: int
    vlan_auto: Literal["enable", "disable"]
    dynamic_vlan: Literal["enable", "disable"]
    captive_portal_fw_accounting: Literal["enable", "disable"]
    captive_portal_ac_name: str
    captive_portal_auth_timeout: int
    multicast_rate: Literal["0", "6000", "12000", "24000"]
    multicast_enhance: Literal["enable", "disable"]
    igmp_snooping: Literal["enable", "disable"]
    dhcp_address_enforcement: Literal["enable", "disable"]
    broadcast_suppression: str
    ipv6_rules: str
    me_disable_thresh: int
    mu_mimo: Literal["enable", "disable"]
    probe_resp_suppression: Literal["enable", "disable"]
    probe_resp_threshold: str
    radio_sensitivity: Literal["enable", "disable"]
    quarantine: Literal["enable", "disable"]
    radio_5g_threshold: str
    radio_2g_threshold: str
    vlan_name: FortiObjectList[VapVlannameItemObject]
    vlan_pooling: Literal["wtp-group", "round-robin", "hash", "disable"]
    vlan_pool: FortiObjectList[VapVlanpoolItemObject]
    dhcp_option43_insertion: Literal["enable", "disable"]
    dhcp_option82_insertion: Literal["enable", "disable"]
    dhcp_option82_circuit_id_insertion: Literal["style-1", "style-2", "style-3", "disable"]
    dhcp_option82_remote_id_insertion: Literal["style-1", "disable"]
    ptk_rekey: Literal["enable", "disable"]
    ptk_rekey_intv: int
    gtk_rekey: Literal["enable", "disable"]
    gtk_rekey_intv: int
    eap_reauth: Literal["enable", "disable"]
    eap_reauth_intv: int
    roaming_acct_interim_update: Literal["enable", "disable"]
    qos_profile: str
    hotspot20_profile: str
    access_control_list: str
    primary_wag_profile: str
    secondary_wag_profile: str
    tunnel_echo_interval: int
    tunnel_fallback_interval: int
    rates_11a: str
    rates_11bg: str
    rates_11n_ss12: str
    rates_11n_ss34: str
    rates_11ac_mcs_map: str
    rates_11ax_mcs_map: str
    rates_11be_mcs_map: str
    rates_11be_mcs_map_160: str
    rates_11be_mcs_map_320: str
    utm_profile: str
    utm_status: Literal["enable", "disable"]
    utm_log: Literal["enable", "disable"]
    ips_sensor: str
    application_list: str
    antivirus_profile: str
    webfilter_profile: str
    scan_botnet_connections: Literal["disable", "monitor", "block"]
    address_group: str
    address_group_policy: Literal["disable", "allow", "deny"]
    sticky_client_remove: Literal["enable", "disable"]
    sticky_client_threshold_5g: str
    sticky_client_threshold_2g: str
    sticky_client_threshold_6g: str
    bstm_rssi_disassoc_timer: int
    bstm_load_balancing_disassoc_timer: int
    bstm_disassociation_imminent: Literal["enable", "disable"]
    beacon_advertising: str
    osen: Literal["enable", "disable"]
    application_detection_engine: Literal["enable", "disable"]
    application_dscp_marking: Literal["enable", "disable"]
    application_report_intv: int
    l3_roaming: Literal["enable", "disable"]
    l3_roaming_mode: Literal["direct", "indirect"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Vap:
    """
    
    Endpoint: wireless_controller/vap
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
    ) -> VapObject: ...
    
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
    ) -> FortiObjectList[VapObject]: ...
    
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
        payload_dict: VapPayload | None = ...,
        name: str | None = ...,
        pre_auth: Literal["enable", "disable"] | None = ...,
        external_pre_auth: Literal["enable", "disable"] | None = ...,
        mesh_backhaul: Literal["enable", "disable"] | None = ...,
        atf_weight: int | None = ...,
        max_clients: int | None = ...,
        max_clients_ap: int | None = ...,
        ssid: str | None = ...,
        broadcast_ssid: Literal["enable", "disable"] | None = ...,
        security: Literal["open", "wep64", "wep128", "wpa-personal", "wpa-enterprise", "wpa-only-personal", "wpa-only-enterprise", "wpa2-only-personal", "wpa2-only-enterprise", "wpa3-enterprise", "wpa3-only-enterprise", "wpa3-enterprise-transition", "wpa3-sae", "wpa3-sae-transition", "owe", "osen"] | None = ...,
        pmf: Literal["disable", "enable", "optional"] | None = ...,
        pmf_assoc_comeback_timeout: int | None = ...,
        pmf_sa_query_retry_timeout: int | None = ...,
        beacon_protection: Literal["disable", "enable"] | None = ...,
        okc: Literal["disable", "enable"] | None = ...,
        mbo: Literal["disable", "enable"] | None = ...,
        gas_comeback_delay: int | None = ...,
        gas_fragmentation_limit: int | None = ...,
        mbo_cell_data_conn_pref: Literal["excluded", "prefer-not", "prefer-use"] | None = ...,
        x80211k: Literal["disable", "enable"] | None = ...,
        x80211v: Literal["disable", "enable"] | None = ...,
        neighbor_report_dual_band: Literal["disable", "enable"] | None = ...,
        fast_bss_transition: Literal["disable", "enable"] | None = ...,
        ft_mobility_domain: int | None = ...,
        ft_r0_key_lifetime: int | None = ...,
        ft_over_ds: Literal["disable", "enable"] | None = ...,
        sae_groups: str | list[str] | None = ...,
        owe_groups: str | list[str] | None = ...,
        owe_transition: Literal["disable", "enable"] | None = ...,
        owe_transition_ssid: str | None = ...,
        additional_akms: str | list[str] | None = ...,
        eapol_key_retries: Literal["disable", "enable"] | None = ...,
        tkip_counter_measure: Literal["enable", "disable"] | None = ...,
        external_web: str | None = ...,
        external_web_format: Literal["auto-detect", "no-query-string", "partial-query-string"] | None = ...,
        external_logout: str | None = ...,
        mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_calling_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_called_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_case: Literal["uppercase", "lowercase"] | None = ...,
        called_station_id_type: Literal["mac", "ip", "apname"] | None = ...,
        mac_auth_bypass: Literal["enable", "disable"] | None = ...,
        radius_mac_auth: Literal["enable", "disable"] | None = ...,
        radius_mac_auth_server: str | None = ...,
        radius_mac_auth_block_interval: int | None = ...,
        radius_mac_mpsk_auth: Literal["enable", "disable"] | None = ...,
        radius_mac_mpsk_timeout: int | None = ...,
        radius_mac_auth_usergroups: str | list[str] | list[VapRadiusmacauthusergroupsItem] | None = ...,
        auth: Literal["radius", "usergroup"] | None = ...,
        encrypt: Literal["TKIP", "AES", "TKIP-AES"] | None = ...,
        keyindex: int | None = ...,
        key: str | None = ...,
        passphrase: str | None = ...,
        sae_password: str | None = ...,
        sae_h2e_only: Literal["enable", "disable"] | None = ...,
        sae_hnp_only: Literal["enable", "disable"] | None = ...,
        sae_pk: Literal["enable", "disable"] | None = ...,
        sae_private_key: str | None = ...,
        akm24_only: Literal["disable", "enable"] | None = ...,
        radius_server: str | None = ...,
        nas_filter_rule: Literal["enable", "disable"] | None = ...,
        domain_name_stripping: Literal["disable", "enable"] | None = ...,
        mlo: Literal["disable", "enable"] | None = ...,
        local_standalone: Literal["enable", "disable"] | None = ...,
        local_standalone_nat: Literal["enable", "disable"] | None = ...,
        ip: str | None = ...,
        dhcp_lease_time: int | None = ...,
        local_standalone_dns: Literal["enable", "disable"] | None = ...,
        local_standalone_dns_ip: str | list[str] | None = ...,
        local_lan_partition: Literal["enable", "disable"] | None = ...,
        local_bridging: Literal["enable", "disable"] | None = ...,
        local_lan: Literal["allow", "deny"] | None = ...,
        local_authentication: Literal["enable", "disable"] | None = ...,
        usergroup: str | list[str] | list[VapUsergroupItem] | None = ...,
        captive_portal: Literal["enable", "disable"] | None = ...,
        captive_network_assistant_bypass: Literal["enable", "disable"] | None = ...,
        portal_message_override_group: str | None = ...,
        portal_message_overrides: VapPortalmessageoverridesDict | None = ...,
        portal_type: Literal["auth", "auth+disclaimer", "disclaimer", "email-collect", "cmcc", "cmcc-macauth", "auth-mac", "external-auth", "external-macauth"] | None = ...,
        selected_usergroups: str | list[str] | list[VapSelectedusergroupsItem] | None = ...,
        security_exempt_list: str | None = ...,
        security_redirect_url: str | None = ...,
        auth_cert: str | None = ...,
        auth_portal_addr: str | None = ...,
        intra_vap_privacy: Literal["enable", "disable"] | None = ...,
        schedule: str | list[str] | list[VapScheduleItem] | None = ...,
        ldpc: Literal["disable", "rx", "tx", "rxtx"] | None = ...,
        high_efficiency: Literal["enable", "disable"] | None = ...,
        target_wake_time: Literal["enable", "disable"] | None = ...,
        port_macauth: Literal["disable", "radius", "address-group"] | None = ...,
        port_macauth_timeout: int | None = ...,
        port_macauth_reauth_timeout: int | None = ...,
        bss_color_partial: Literal["enable", "disable"] | None = ...,
        mpsk_profile: str | None = ...,
        split_tunneling: Literal["enable", "disable"] | None = ...,
        nac: Literal["enable", "disable"] | None = ...,
        nac_profile: str | None = ...,
        vlanid: int | None = ...,
        vlan_auto: Literal["enable", "disable"] | None = ...,
        dynamic_vlan: Literal["enable", "disable"] | None = ...,
        captive_portal_fw_accounting: Literal["enable", "disable"] | None = ...,
        captive_portal_ac_name: str | None = ...,
        captive_portal_auth_timeout: int | None = ...,
        multicast_rate: Literal["0", "6000", "12000", "24000"] | None = ...,
        multicast_enhance: Literal["enable", "disable"] | None = ...,
        igmp_snooping: Literal["enable", "disable"] | None = ...,
        dhcp_address_enforcement: Literal["enable", "disable"] | None = ...,
        broadcast_suppression: str | list[str] | None = ...,
        ipv6_rules: str | list[str] | None = ...,
        me_disable_thresh: int | None = ...,
        mu_mimo: Literal["enable", "disable"] | None = ...,
        probe_resp_suppression: Literal["enable", "disable"] | None = ...,
        probe_resp_threshold: str | None = ...,
        radio_sensitivity: Literal["enable", "disable"] | None = ...,
        quarantine: Literal["enable", "disable"] | None = ...,
        radio_5g_threshold: str | None = ...,
        radio_2g_threshold: str | None = ...,
        vlan_name: str | list[str] | list[VapVlannameItem] | None = ...,
        vlan_pooling: Literal["wtp-group", "round-robin", "hash", "disable"] | None = ...,
        vlan_pool: str | list[str] | list[VapVlanpoolItem] | None = ...,
        dhcp_option43_insertion: Literal["enable", "disable"] | None = ...,
        dhcp_option82_insertion: Literal["enable", "disable"] | None = ...,
        dhcp_option82_circuit_id_insertion: Literal["style-1", "style-2", "style-3", "disable"] | None = ...,
        dhcp_option82_remote_id_insertion: Literal["style-1", "disable"] | None = ...,
        ptk_rekey: Literal["enable", "disable"] | None = ...,
        ptk_rekey_intv: int | None = ...,
        gtk_rekey: Literal["enable", "disable"] | None = ...,
        gtk_rekey_intv: int | None = ...,
        eap_reauth: Literal["enable", "disable"] | None = ...,
        eap_reauth_intv: int | None = ...,
        roaming_acct_interim_update: Literal["enable", "disable"] | None = ...,
        qos_profile: str | None = ...,
        hotspot20_profile: str | None = ...,
        access_control_list: str | None = ...,
        primary_wag_profile: str | None = ...,
        secondary_wag_profile: str | None = ...,
        tunnel_echo_interval: int | None = ...,
        tunnel_fallback_interval: int | None = ...,
        rates_11a: str | list[str] | None = ...,
        rates_11bg: str | list[str] | None = ...,
        rates_11n_ss12: str | list[str] | None = ...,
        rates_11n_ss34: str | list[str] | None = ...,
        rates_11ac_mcs_map: str | None = ...,
        rates_11ax_mcs_map: str | None = ...,
        rates_11be_mcs_map: str | None = ...,
        rates_11be_mcs_map_160: str | None = ...,
        rates_11be_mcs_map_320: str | None = ...,
        utm_profile: str | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        address_group: str | None = ...,
        address_group_policy: Literal["disable", "allow", "deny"] | None = ...,
        sticky_client_remove: Literal["enable", "disable"] | None = ...,
        sticky_client_threshold_5g: str | None = ...,
        sticky_client_threshold_2g: str | None = ...,
        sticky_client_threshold_6g: str | None = ...,
        bstm_rssi_disassoc_timer: int | None = ...,
        bstm_load_balancing_disassoc_timer: int | None = ...,
        bstm_disassociation_imminent: Literal["enable", "disable"] | None = ...,
        beacon_advertising: str | list[str] | None = ...,
        osen: Literal["enable", "disable"] | None = ...,
        application_detection_engine: Literal["enable", "disable"] | None = ...,
        application_dscp_marking: Literal["enable", "disable"] | None = ...,
        application_report_intv: int | None = ...,
        l3_roaming: Literal["enable", "disable"] | None = ...,
        l3_roaming_mode: Literal["direct", "indirect"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VapObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VapPayload | None = ...,
        name: str | None = ...,
        pre_auth: Literal["enable", "disable"] | None = ...,
        external_pre_auth: Literal["enable", "disable"] | None = ...,
        mesh_backhaul: Literal["enable", "disable"] | None = ...,
        atf_weight: int | None = ...,
        max_clients: int | None = ...,
        max_clients_ap: int | None = ...,
        ssid: str | None = ...,
        broadcast_ssid: Literal["enable", "disable"] | None = ...,
        security: Literal["open", "wep64", "wep128", "wpa-personal", "wpa-enterprise", "wpa-only-personal", "wpa-only-enterprise", "wpa2-only-personal", "wpa2-only-enterprise", "wpa3-enterprise", "wpa3-only-enterprise", "wpa3-enterprise-transition", "wpa3-sae", "wpa3-sae-transition", "owe", "osen"] | None = ...,
        pmf: Literal["disable", "enable", "optional"] | None = ...,
        pmf_assoc_comeback_timeout: int | None = ...,
        pmf_sa_query_retry_timeout: int | None = ...,
        beacon_protection: Literal["disable", "enable"] | None = ...,
        okc: Literal["disable", "enable"] | None = ...,
        mbo: Literal["disable", "enable"] | None = ...,
        gas_comeback_delay: int | None = ...,
        gas_fragmentation_limit: int | None = ...,
        mbo_cell_data_conn_pref: Literal["excluded", "prefer-not", "prefer-use"] | None = ...,
        x80211k: Literal["disable", "enable"] | None = ...,
        x80211v: Literal["disable", "enable"] | None = ...,
        neighbor_report_dual_band: Literal["disable", "enable"] | None = ...,
        fast_bss_transition: Literal["disable", "enable"] | None = ...,
        ft_mobility_domain: int | None = ...,
        ft_r0_key_lifetime: int | None = ...,
        ft_over_ds: Literal["disable", "enable"] | None = ...,
        sae_groups: str | list[str] | None = ...,
        owe_groups: str | list[str] | None = ...,
        owe_transition: Literal["disable", "enable"] | None = ...,
        owe_transition_ssid: str | None = ...,
        additional_akms: str | list[str] | None = ...,
        eapol_key_retries: Literal["disable", "enable"] | None = ...,
        tkip_counter_measure: Literal["enable", "disable"] | None = ...,
        external_web: str | None = ...,
        external_web_format: Literal["auto-detect", "no-query-string", "partial-query-string"] | None = ...,
        external_logout: str | None = ...,
        mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_calling_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_called_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_case: Literal["uppercase", "lowercase"] | None = ...,
        called_station_id_type: Literal["mac", "ip", "apname"] | None = ...,
        mac_auth_bypass: Literal["enable", "disable"] | None = ...,
        radius_mac_auth: Literal["enable", "disable"] | None = ...,
        radius_mac_auth_server: str | None = ...,
        radius_mac_auth_block_interval: int | None = ...,
        radius_mac_mpsk_auth: Literal["enable", "disable"] | None = ...,
        radius_mac_mpsk_timeout: int | None = ...,
        radius_mac_auth_usergroups: str | list[str] | list[VapRadiusmacauthusergroupsItem] | None = ...,
        auth: Literal["radius", "usergroup"] | None = ...,
        encrypt: Literal["TKIP", "AES", "TKIP-AES"] | None = ...,
        keyindex: int | None = ...,
        key: str | None = ...,
        passphrase: str | None = ...,
        sae_password: str | None = ...,
        sae_h2e_only: Literal["enable", "disable"] | None = ...,
        sae_hnp_only: Literal["enable", "disable"] | None = ...,
        sae_pk: Literal["enable", "disable"] | None = ...,
        sae_private_key: str | None = ...,
        akm24_only: Literal["disable", "enable"] | None = ...,
        radius_server: str | None = ...,
        nas_filter_rule: Literal["enable", "disable"] | None = ...,
        domain_name_stripping: Literal["disable", "enable"] | None = ...,
        mlo: Literal["disable", "enable"] | None = ...,
        local_standalone: Literal["enable", "disable"] | None = ...,
        local_standalone_nat: Literal["enable", "disable"] | None = ...,
        ip: str | None = ...,
        dhcp_lease_time: int | None = ...,
        local_standalone_dns: Literal["enable", "disable"] | None = ...,
        local_standalone_dns_ip: str | list[str] | None = ...,
        local_lan_partition: Literal["enable", "disable"] | None = ...,
        local_bridging: Literal["enable", "disable"] | None = ...,
        local_lan: Literal["allow", "deny"] | None = ...,
        local_authentication: Literal["enable", "disable"] | None = ...,
        usergroup: str | list[str] | list[VapUsergroupItem] | None = ...,
        captive_portal: Literal["enable", "disable"] | None = ...,
        captive_network_assistant_bypass: Literal["enable", "disable"] | None = ...,
        portal_message_override_group: str | None = ...,
        portal_message_overrides: VapPortalmessageoverridesDict | None = ...,
        portal_type: Literal["auth", "auth+disclaimer", "disclaimer", "email-collect", "cmcc", "cmcc-macauth", "auth-mac", "external-auth", "external-macauth"] | None = ...,
        selected_usergroups: str | list[str] | list[VapSelectedusergroupsItem] | None = ...,
        security_exempt_list: str | None = ...,
        security_redirect_url: str | None = ...,
        auth_cert: str | None = ...,
        auth_portal_addr: str | None = ...,
        intra_vap_privacy: Literal["enable", "disable"] | None = ...,
        schedule: str | list[str] | list[VapScheduleItem] | None = ...,
        ldpc: Literal["disable", "rx", "tx", "rxtx"] | None = ...,
        high_efficiency: Literal["enable", "disable"] | None = ...,
        target_wake_time: Literal["enable", "disable"] | None = ...,
        port_macauth: Literal["disable", "radius", "address-group"] | None = ...,
        port_macauth_timeout: int | None = ...,
        port_macauth_reauth_timeout: int | None = ...,
        bss_color_partial: Literal["enable", "disable"] | None = ...,
        mpsk_profile: str | None = ...,
        split_tunneling: Literal["enable", "disable"] | None = ...,
        nac: Literal["enable", "disable"] | None = ...,
        nac_profile: str | None = ...,
        vlanid: int | None = ...,
        vlan_auto: Literal["enable", "disable"] | None = ...,
        dynamic_vlan: Literal["enable", "disable"] | None = ...,
        captive_portal_fw_accounting: Literal["enable", "disable"] | None = ...,
        captive_portal_ac_name: str | None = ...,
        captive_portal_auth_timeout: int | None = ...,
        multicast_rate: Literal["0", "6000", "12000", "24000"] | None = ...,
        multicast_enhance: Literal["enable", "disable"] | None = ...,
        igmp_snooping: Literal["enable", "disable"] | None = ...,
        dhcp_address_enforcement: Literal["enable", "disable"] | None = ...,
        broadcast_suppression: str | list[str] | None = ...,
        ipv6_rules: str | list[str] | None = ...,
        me_disable_thresh: int | None = ...,
        mu_mimo: Literal["enable", "disable"] | None = ...,
        probe_resp_suppression: Literal["enable", "disable"] | None = ...,
        probe_resp_threshold: str | None = ...,
        radio_sensitivity: Literal["enable", "disable"] | None = ...,
        quarantine: Literal["enable", "disable"] | None = ...,
        radio_5g_threshold: str | None = ...,
        radio_2g_threshold: str | None = ...,
        vlan_name: str | list[str] | list[VapVlannameItem] | None = ...,
        vlan_pooling: Literal["wtp-group", "round-robin", "hash", "disable"] | None = ...,
        vlan_pool: str | list[str] | list[VapVlanpoolItem] | None = ...,
        dhcp_option43_insertion: Literal["enable", "disable"] | None = ...,
        dhcp_option82_insertion: Literal["enable", "disable"] | None = ...,
        dhcp_option82_circuit_id_insertion: Literal["style-1", "style-2", "style-3", "disable"] | None = ...,
        dhcp_option82_remote_id_insertion: Literal["style-1", "disable"] | None = ...,
        ptk_rekey: Literal["enable", "disable"] | None = ...,
        ptk_rekey_intv: int | None = ...,
        gtk_rekey: Literal["enable", "disable"] | None = ...,
        gtk_rekey_intv: int | None = ...,
        eap_reauth: Literal["enable", "disable"] | None = ...,
        eap_reauth_intv: int | None = ...,
        roaming_acct_interim_update: Literal["enable", "disable"] | None = ...,
        qos_profile: str | None = ...,
        hotspot20_profile: str | None = ...,
        access_control_list: str | None = ...,
        primary_wag_profile: str | None = ...,
        secondary_wag_profile: str | None = ...,
        tunnel_echo_interval: int | None = ...,
        tunnel_fallback_interval: int | None = ...,
        rates_11a: str | list[str] | None = ...,
        rates_11bg: str | list[str] | None = ...,
        rates_11n_ss12: str | list[str] | None = ...,
        rates_11n_ss34: str | list[str] | None = ...,
        rates_11ac_mcs_map: str | None = ...,
        rates_11ax_mcs_map: str | None = ...,
        rates_11be_mcs_map: str | None = ...,
        rates_11be_mcs_map_160: str | None = ...,
        rates_11be_mcs_map_320: str | None = ...,
        utm_profile: str | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        address_group: str | None = ...,
        address_group_policy: Literal["disable", "allow", "deny"] | None = ...,
        sticky_client_remove: Literal["enable", "disable"] | None = ...,
        sticky_client_threshold_5g: str | None = ...,
        sticky_client_threshold_2g: str | None = ...,
        sticky_client_threshold_6g: str | None = ...,
        bstm_rssi_disassoc_timer: int | None = ...,
        bstm_load_balancing_disassoc_timer: int | None = ...,
        bstm_disassociation_imminent: Literal["enable", "disable"] | None = ...,
        beacon_advertising: str | list[str] | None = ...,
        osen: Literal["enable", "disable"] | None = ...,
        application_detection_engine: Literal["enable", "disable"] | None = ...,
        application_dscp_marking: Literal["enable", "disable"] | None = ...,
        application_report_intv: int | None = ...,
        l3_roaming: Literal["enable", "disable"] | None = ...,
        l3_roaming_mode: Literal["direct", "indirect"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VapObject: ...

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
        payload_dict: VapPayload | None = ...,
        name: str | None = ...,
        pre_auth: Literal["enable", "disable"] | None = ...,
        external_pre_auth: Literal["enable", "disable"] | None = ...,
        mesh_backhaul: Literal["enable", "disable"] | None = ...,
        atf_weight: int | None = ...,
        max_clients: int | None = ...,
        max_clients_ap: int | None = ...,
        ssid: str | None = ...,
        broadcast_ssid: Literal["enable", "disable"] | None = ...,
        security: Literal["open", "wep64", "wep128", "wpa-personal", "wpa-enterprise", "wpa-only-personal", "wpa-only-enterprise", "wpa2-only-personal", "wpa2-only-enterprise", "wpa3-enterprise", "wpa3-only-enterprise", "wpa3-enterprise-transition", "wpa3-sae", "wpa3-sae-transition", "owe", "osen"] | None = ...,
        pmf: Literal["disable", "enable", "optional"] | None = ...,
        pmf_assoc_comeback_timeout: int | None = ...,
        pmf_sa_query_retry_timeout: int | None = ...,
        beacon_protection: Literal["disable", "enable"] | None = ...,
        okc: Literal["disable", "enable"] | None = ...,
        mbo: Literal["disable", "enable"] | None = ...,
        gas_comeback_delay: int | None = ...,
        gas_fragmentation_limit: int | None = ...,
        mbo_cell_data_conn_pref: Literal["excluded", "prefer-not", "prefer-use"] | None = ...,
        x80211k: Literal["disable", "enable"] | None = ...,
        x80211v: Literal["disable", "enable"] | None = ...,
        neighbor_report_dual_band: Literal["disable", "enable"] | None = ...,
        fast_bss_transition: Literal["disable", "enable"] | None = ...,
        ft_mobility_domain: int | None = ...,
        ft_r0_key_lifetime: int | None = ...,
        ft_over_ds: Literal["disable", "enable"] | None = ...,
        sae_groups: Literal["19", "20", "21"] | list[str] | None = ...,
        owe_groups: Literal["19", "20", "21"] | list[str] | None = ...,
        owe_transition: Literal["disable", "enable"] | None = ...,
        owe_transition_ssid: str | None = ...,
        additional_akms: Literal["akm6", "akm24"] | list[str] | None = ...,
        eapol_key_retries: Literal["disable", "enable"] | None = ...,
        tkip_counter_measure: Literal["enable", "disable"] | None = ...,
        external_web: str | None = ...,
        external_web_format: Literal["auto-detect", "no-query-string", "partial-query-string"] | None = ...,
        external_logout: str | None = ...,
        mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_calling_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_called_station_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_case: Literal["uppercase", "lowercase"] | None = ...,
        called_station_id_type: Literal["mac", "ip", "apname"] | None = ...,
        mac_auth_bypass: Literal["enable", "disable"] | None = ...,
        radius_mac_auth: Literal["enable", "disable"] | None = ...,
        radius_mac_auth_server: str | None = ...,
        radius_mac_auth_block_interval: int | None = ...,
        radius_mac_mpsk_auth: Literal["enable", "disable"] | None = ...,
        radius_mac_mpsk_timeout: int | None = ...,
        radius_mac_auth_usergroups: str | list[str] | list[VapRadiusmacauthusergroupsItem] | None = ...,
        auth: Literal["radius", "usergroup"] | None = ...,
        encrypt: Literal["TKIP", "AES", "TKIP-AES"] | None = ...,
        keyindex: int | None = ...,
        key: str | None = ...,
        passphrase: str | None = ...,
        sae_password: str | None = ...,
        sae_h2e_only: Literal["enable", "disable"] | None = ...,
        sae_hnp_only: Literal["enable", "disable"] | None = ...,
        sae_pk: Literal["enable", "disable"] | None = ...,
        sae_private_key: str | None = ...,
        akm24_only: Literal["disable", "enable"] | None = ...,
        radius_server: str | None = ...,
        nas_filter_rule: Literal["enable", "disable"] | None = ...,
        domain_name_stripping: Literal["disable", "enable"] | None = ...,
        mlo: Literal["disable", "enable"] | None = ...,
        local_standalone: Literal["enable", "disable"] | None = ...,
        local_standalone_nat: Literal["enable", "disable"] | None = ...,
        ip: str | None = ...,
        dhcp_lease_time: int | None = ...,
        local_standalone_dns: Literal["enable", "disable"] | None = ...,
        local_standalone_dns_ip: str | list[str] | None = ...,
        local_lan_partition: Literal["enable", "disable"] | None = ...,
        local_bridging: Literal["enable", "disable"] | None = ...,
        local_lan: Literal["allow", "deny"] | None = ...,
        local_authentication: Literal["enable", "disable"] | None = ...,
        usergroup: str | list[str] | list[VapUsergroupItem] | None = ...,
        captive_portal: Literal["enable", "disable"] | None = ...,
        captive_network_assistant_bypass: Literal["enable", "disable"] | None = ...,
        portal_message_override_group: str | None = ...,
        portal_message_overrides: VapPortalmessageoverridesDict | None = ...,
        portal_type: Literal["auth", "auth+disclaimer", "disclaimer", "email-collect", "cmcc", "cmcc-macauth", "auth-mac", "external-auth", "external-macauth"] | None = ...,
        selected_usergroups: str | list[str] | list[VapSelectedusergroupsItem] | None = ...,
        security_exempt_list: str | None = ...,
        security_redirect_url: str | None = ...,
        auth_cert: str | None = ...,
        auth_portal_addr: str | None = ...,
        intra_vap_privacy: Literal["enable", "disable"] | None = ...,
        schedule: str | list[str] | list[VapScheduleItem] | None = ...,
        ldpc: Literal["disable", "rx", "tx", "rxtx"] | None = ...,
        high_efficiency: Literal["enable", "disable"] | None = ...,
        target_wake_time: Literal["enable", "disable"] | None = ...,
        port_macauth: Literal["disable", "radius", "address-group"] | None = ...,
        port_macauth_timeout: int | None = ...,
        port_macauth_reauth_timeout: int | None = ...,
        bss_color_partial: Literal["enable", "disable"] | None = ...,
        mpsk_profile: str | None = ...,
        split_tunneling: Literal["enable", "disable"] | None = ...,
        nac: Literal["enable", "disable"] | None = ...,
        nac_profile: str | None = ...,
        vlanid: int | None = ...,
        vlan_auto: Literal["enable", "disable"] | None = ...,
        dynamic_vlan: Literal["enable", "disable"] | None = ...,
        captive_portal_fw_accounting: Literal["enable", "disable"] | None = ...,
        captive_portal_ac_name: str | None = ...,
        captive_portal_auth_timeout: int | None = ...,
        multicast_rate: Literal["0", "6000", "12000", "24000"] | None = ...,
        multicast_enhance: Literal["enable", "disable"] | None = ...,
        igmp_snooping: Literal["enable", "disable"] | None = ...,
        dhcp_address_enforcement: Literal["enable", "disable"] | None = ...,
        broadcast_suppression: Literal["dhcp-up", "dhcp-down", "dhcp-starvation", "dhcp-ucast", "arp-known", "arp-unknown", "arp-reply", "arp-poison", "arp-proxy", "netbios-ns", "netbios-ds", "ipv6", "all-other-mc", "all-other-bc"] | list[str] | None = ...,
        ipv6_rules: Literal["drop-icmp6ra", "drop-icmp6rs", "drop-llmnr6", "drop-icmp6mld2", "drop-dhcp6s", "drop-dhcp6c", "ndp-proxy", "drop-ns-dad", "drop-ns-nondad"] | list[str] | None = ...,
        me_disable_thresh: int | None = ...,
        mu_mimo: Literal["enable", "disable"] | None = ...,
        probe_resp_suppression: Literal["enable", "disable"] | None = ...,
        probe_resp_threshold: str | None = ...,
        radio_sensitivity: Literal["enable", "disable"] | None = ...,
        quarantine: Literal["enable", "disable"] | None = ...,
        radio_5g_threshold: str | None = ...,
        radio_2g_threshold: str | None = ...,
        vlan_name: str | list[str] | list[VapVlannameItem] | None = ...,
        vlan_pooling: Literal["wtp-group", "round-robin", "hash", "disable"] | None = ...,
        vlan_pool: str | list[str] | list[VapVlanpoolItem] | None = ...,
        dhcp_option43_insertion: Literal["enable", "disable"] | None = ...,
        dhcp_option82_insertion: Literal["enable", "disable"] | None = ...,
        dhcp_option82_circuit_id_insertion: Literal["style-1", "style-2", "style-3", "disable"] | None = ...,
        dhcp_option82_remote_id_insertion: Literal["style-1", "disable"] | None = ...,
        ptk_rekey: Literal["enable", "disable"] | None = ...,
        ptk_rekey_intv: int | None = ...,
        gtk_rekey: Literal["enable", "disable"] | None = ...,
        gtk_rekey_intv: int | None = ...,
        eap_reauth: Literal["enable", "disable"] | None = ...,
        eap_reauth_intv: int | None = ...,
        roaming_acct_interim_update: Literal["enable", "disable"] | None = ...,
        qos_profile: str | None = ...,
        hotspot20_profile: str | None = ...,
        access_control_list: str | None = ...,
        primary_wag_profile: str | None = ...,
        secondary_wag_profile: str | None = ...,
        tunnel_echo_interval: int | None = ...,
        tunnel_fallback_interval: int | None = ...,
        rates_11a: Literal["6", "6-basic", "9", "9-basic", "12", "12-basic", "18", "18-basic", "24", "24-basic", "36", "36-basic", "48", "48-basic", "54", "54-basic"] | list[str] | None = ...,
        rates_11bg: Literal["1", "1-basic", "2", "2-basic", "5.5", "5.5-basic", "11", "11-basic", "6", "6-basic", "9", "9-basic", "12", "12-basic", "18", "18-basic", "24", "24-basic", "36", "36-basic", "48", "48-basic", "54", "54-basic"] | list[str] | None = ...,
        rates_11n_ss12: Literal["mcs0/1", "mcs1/1", "mcs2/1", "mcs3/1", "mcs4/1", "mcs5/1", "mcs6/1", "mcs7/1", "mcs8/2", "mcs9/2", "mcs10/2", "mcs11/2", "mcs12/2", "mcs13/2", "mcs14/2", "mcs15/2"] | list[str] | None = ...,
        rates_11n_ss34: Literal["mcs16/3", "mcs17/3", "mcs18/3", "mcs19/3", "mcs20/3", "mcs21/3", "mcs22/3", "mcs23/3", "mcs24/4", "mcs25/4", "mcs26/4", "mcs27/4", "mcs28/4", "mcs29/4", "mcs30/4", "mcs31/4"] | list[str] | None = ...,
        rates_11ac_mcs_map: str | None = ...,
        rates_11ax_mcs_map: str | None = ...,
        rates_11be_mcs_map: str | None = ...,
        rates_11be_mcs_map_160: str | None = ...,
        rates_11be_mcs_map_320: str | None = ...,
        utm_profile: str | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        address_group: str | None = ...,
        address_group_policy: Literal["disable", "allow", "deny"] | None = ...,
        sticky_client_remove: Literal["enable", "disable"] | None = ...,
        sticky_client_threshold_5g: str | None = ...,
        sticky_client_threshold_2g: str | None = ...,
        sticky_client_threshold_6g: str | None = ...,
        bstm_rssi_disassoc_timer: int | None = ...,
        bstm_load_balancing_disassoc_timer: int | None = ...,
        bstm_disassociation_imminent: Literal["enable", "disable"] | None = ...,
        beacon_advertising: Literal["name", "model", "serial-number"] | list[str] | None = ...,
        osen: Literal["enable", "disable"] | None = ...,
        application_detection_engine: Literal["enable", "disable"] | None = ...,
        application_dscp_marking: Literal["enable", "disable"] | None = ...,
        application_report_intv: int | None = ...,
        l3_roaming: Literal["enable", "disable"] | None = ...,
        l3_roaming_mode: Literal["direct", "indirect"] | None = ...,
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
    "Vap",
    "VapPayload",
    "VapResponse",
    "VapObject",
]