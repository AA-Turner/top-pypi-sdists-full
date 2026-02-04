""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/global_
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class GlobalInternetservicedownloadlistItem(TypedDict, total=False):
    """Nested item for internet-service-download-list field."""
    id: int


class GlobalPayload(TypedDict, total=False):
    """Payload type for Global operations."""
    language: Literal["english", "french", "spanish", "portuguese", "japanese", "trach", "simch", "korean"]
    gui_ipv6: Literal["enable", "disable"]
    gui_replacement_message_groups: Literal["enable", "disable"]
    gui_local_out: Literal["enable", "disable"]
    gui_certificates: Literal["enable", "disable"]
    gui_custom_language: Literal["enable", "disable"]
    gui_wireless_opensecurity: Literal["enable", "disable"]
    gui_app_detection_sdwan: Literal["enable", "disable"]
    gui_display_hostname: Literal["enable", "disable"]
    gui_fortigate_cloud_sandbox: Literal["enable", "disable"]
    gui_firmware_upgrade_warning: Literal["enable", "disable"]
    gui_forticare_registration_setup_warning: Literal["enable", "disable"]
    gui_auto_upgrade_setup_warning: Literal["enable", "disable"]
    gui_workflow_management: Literal["enable", "disable"]
    gui_cdn_usage: Literal["enable", "disable"]
    admin_https_ssl_versions: str | list[str]
    admin_https_ssl_ciphersuites: str | list[str]
    admin_https_ssl_banned_ciphers: str | list[str]
    admintimeout: int
    admin_console_timeout: int
    ssd_trim_freq: Literal["never", "hourly", "daily", "weekly", "monthly"]
    ssd_trim_hour: int
    ssd_trim_min: int
    ssd_trim_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    ssd_trim_date: int
    admin_concurrent: Literal["enable", "disable"]
    admin_lockout_threshold: int
    admin_lockout_duration: int
    refresh: int
    interval: int
    failtime: int
    purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    daily_restart: Literal["enable", "disable"]
    restart_time: str
    wad_restart_mode: Literal["none", "time", "memory"]
    wad_restart_start_time: str
    wad_restart_end_time: str
    wad_p2s_max_body_size: int
    radius_port: int
    speedtestd_server_port: int
    speedtestd_ctrl_port: int
    admin_login_max: int
    remoteauthtimeout: int
    ldapconntimeout: int
    batch_cmdb: Literal["enable", "disable"]
    multi_factor_authentication: Literal["optional", "mandatory"]
    ssl_min_proto_version: Literal["SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    autorun_log_fsck: Literal["enable", "disable"]
    timezone: str
    traffic_priority: Literal["tos", "dscp"]
    traffic_priority_level: Literal["low", "medium", "high"]
    quic_congestion_control_algo: Literal["cubic", "bbr", "bbr2", "reno"]
    quic_max_datagram_size: int
    quic_udp_payload_size_shaping_per_cid: Literal["enable", "disable"]
    quic_ack_thresold: int
    quic_pmtud: Literal["enable", "disable"]
    quic_tls_handshake_timeout: int
    anti_replay: Literal["disable", "loose", "strict"]
    send_pmtu_icmp: Literal["enable", "disable"]
    honor_df: Literal["enable", "disable"]
    pmtu_discovery: Literal["enable", "disable"]
    revision_image_auto_backup: Literal["enable", "disable"]
    revision_backup_on_logout: Literal["enable", "disable"]
    management_vdom: str
    hostname: str
    alias: str
    strong_crypto: Literal["enable", "disable"]
    ssl_static_key_ciphers: Literal["enable", "disable"]
    snat_route_change: Literal["enable", "disable"]
    ipv6_snat_route_change: Literal["enable", "disable"]
    speedtest_server: Literal["enable", "disable"]
    cli_audit_log: Literal["enable", "disable"]
    dh_params: Literal["1024", "1536", "2048", "3072", "4096", "6144", "8192"]
    fds_statistics: Literal["enable", "disable"]
    fds_statistics_period: int
    tcp_option: Literal["enable", "disable"]
    lldp_transmission: Literal["enable", "disable"]
    lldp_reception: Literal["enable", "disable"]
    proxy_auth_timeout: int
    proxy_keep_alive_mode: Literal["session", "traffic", "re-authentication"]
    proxy_re_authentication_time: int
    proxy_auth_lifetime: Literal["enable", "disable"]
    proxy_auth_lifetime_timeout: int
    proxy_resource_mode: Literal["enable", "disable"]
    proxy_cert_use_mgmt_vdom: Literal["enable", "disable"]
    sys_perf_log_interval: int
    check_protocol_header: Literal["loose", "strict"]
    vip_arp_range: Literal["unlimited", "restricted"]
    reset_sessionless_tcp: Literal["enable", "disable"]
    allow_traffic_redirect: Literal["enable", "disable"]
    ipv6_allow_traffic_redirect: Literal["enable", "disable"]
    strict_dirty_session_check: Literal["enable", "disable"]
    tcp_halfclose_timer: int
    tcp_halfopen_timer: int
    tcp_timewait_timer: int
    tcp_rst_timer: int
    udp_idle_timer: int
    block_session_timer: int
    ip_src_port_range: str
    pre_login_banner: Literal["enable", "disable"]
    post_login_banner: Literal["disable", "enable"]
    tftp: Literal["enable", "disable"]
    av_failopen: Literal["pass", "off", "one-shot"]
    av_failopen_session: Literal["enable", "disable"]
    memory_use_threshold_extreme: int
    memory_use_threshold_red: int
    memory_use_threshold_green: int
    ip_fragment_mem_thresholds: int
    ip_fragment_timeout: int
    ipv6_fragment_timeout: int
    cpu_use_threshold: int
    log_single_cpu_high: Literal["enable", "disable"]
    check_reset_range: Literal["strict", "disable"]
    upgrade_report: Literal["enable", "disable"]
    admin_port: int
    admin_sport: int
    admin_host: str
    admin_https_redirect: Literal["enable", "disable"]
    admin_hsts_max_age: int
    admin_ssh_password: Literal["enable", "disable"]
    admin_restrict_local: Literal["all", "non-console-only", "disable"]
    admin_ssh_port: int
    admin_ssh_grace_time: int
    admin_ssh_v1: Literal["enable", "disable"]
    admin_telnet: Literal["enable", "disable"]
    admin_telnet_port: int
    admin_forticloud_sso_login: Literal["enable", "disable"]
    admin_forticloud_sso_default_profile: str
    default_service_source_port: str
    admin_server_cert: str
    admin_https_pki_required: Literal["enable", "disable"]
    wifi_certificate: str
    dhcp_lease_backup_interval: int
    wifi_ca_certificate: str
    auth_http_port: int
    auth_https_port: int
    auth_ike_saml_port: int
    auth_keepalive: Literal["enable", "disable"]
    policy_auth_concurrent: int
    auth_session_limit: Literal["block-new", "logout-inactive"]
    auth_cert: str
    clt_cert_req: Literal["enable", "disable"]
    fortiservice_port: int
    cfg_save: Literal["automatic", "manual", "revert"]
    cfg_revert_timeout: int
    reboot_upon_config_restore: Literal["enable", "disable"]
    admin_scp: Literal["enable", "disable"]
    wireless_controller: Literal["enable", "disable"]
    wireless_controller_port: int
    fortiextender_data_port: int
    fortiextender: Literal["disable", "enable"]
    extender_controller_reserved_network: str
    fortiextender_discovery_lockdown: Literal["disable", "enable"]
    fortiextender_vlan_mode: Literal["enable", "disable"]
    fortiextender_provision_on_authorization: Literal["enable", "disable"]
    switch_controller: Literal["disable", "enable"]
    switch_controller_reserved_network: str
    dnsproxy_worker_count: int
    url_filter_count: int
    httpd_max_worker_count: int
    proxy_worker_count: int
    scanunit_count: int
    fgd_alert_subscription: str | list[str]
    ipv6_accept_dad: int
    ipv6_allow_anycast_probe: Literal["enable", "disable"]
    ipv6_allow_multicast_probe: Literal["enable", "disable"]
    ipv6_allow_local_in_silent_drop: Literal["enable", "disable"]
    csr_ca_attribute: Literal["enable", "disable"]
    wimax_4g_usb: Literal["enable", "disable"]
    cert_chain_max: int
    sslvpn_max_worker_count: int
    sslvpn_affinity: str
    sslvpn_web_mode: Literal["enable", "disable"]
    two_factor_ftk_expiry: int
    two_factor_email_expiry: int
    two_factor_sms_expiry: int
    two_factor_fac_expiry: int
    two_factor_ftm_expiry: int
    per_user_bal: Literal["enable", "disable"]
    wad_worker_count: int
    wad_worker_dev_cache: int
    wad_csvc_cs_count: int
    wad_csvc_db_count: int
    wad_source_affinity: Literal["disable", "enable"]
    wad_memory_change_granularity: int
    login_timestamp: Literal["enable", "disable"]
    ip_conflict_detection: Literal["enable", "disable"]
    miglogd_children: int
    log_daemon_cpu_threshold: int
    special_file_23_support: Literal["disable", "enable"]
    log_uuid_address: Literal["enable", "disable"]
    log_ssl_connection: Literal["enable", "disable"]
    gui_rest_api_cache: Literal["enable", "disable"]
    rest_api_key_url_query: Literal["enable", "disable"]
    arp_max_entry: int
    ha_affinity: str
    bfd_affinity: str
    cmdbsvr_affinity: str
    av_affinity: str
    wad_affinity: str
    ips_affinity: str
    miglog_affinity: str
    syslog_affinity: str
    url_filter_affinity: str
    router_affinity: str
    ndp_max_entry: int
    br_fdb_max_entry: int
    max_route_cache_size: int
    ipsec_qat_offload: Literal["enable", "disable"]
    device_idle_timeout: int
    user_device_store_max_devices: int
    user_device_store_max_device_mem: int
    user_device_store_max_users: int
    user_device_store_max_unified_mem: int
    gui_device_latitude: str
    gui_device_longitude: str
    private_data_encryption: Literal["disable", "enable"]
    auto_auth_extension_device: Literal["enable", "disable"]
    gui_theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "retro", "dark-matter", "onyx", "eclipse"]
    gui_date_format: Literal["yyyy/MM/dd", "dd/MM/yyyy", "MM/dd/yyyy", "yyyy-MM-dd", "dd-MM-yyyy", "MM-dd-yyyy"]
    gui_date_time_source: Literal["system", "browser"]
    igmp_state_limit: int
    cloud_communication: Literal["enable", "disable"]
    ipsec_ha_seqjump_rate: int
    fortitoken_cloud: Literal["enable", "disable"]
    fortitoken_cloud_push_status: Literal["enable", "disable"]
    fortitoken_cloud_region: str
    fortitoken_cloud_sync_interval: int
    faz_disk_buffer_size: int
    irq_time_accounting: Literal["auto", "force"]
    management_ip: str
    management_port: int
    management_port_use_admin_sport: Literal["enable", "disable"]
    forticonverter_integration: Literal["enable", "disable"]
    forticonverter_config_upload: Literal["once", "disable"]
    internet_service_database: Literal["mini", "standard", "full", "on-demand"]
    internet_service_download_list: str | list[str] | list[GlobalInternetservicedownloadlistItem]
    geoip_full_db: Literal["enable", "disable"]
    early_tcp_npu_session: Literal["enable", "disable"]
    npu_neighbor_update: Literal["enable", "disable"]
    delay_tcp_npu_session: Literal["enable", "disable"]
    interface_subnet_usage: Literal["disable", "enable"]
    sflowd_max_children_num: int
    fortigslb_integration: Literal["disable", "enable"]
    user_history_password_threshold: int
    auth_session_auto_backup: Literal["enable", "disable"]
    auth_session_auto_backup_interval: Literal["1min", "5min", "15min", "30min", "1hr"]
    scim_https_port: int
    scim_http_port: int
    scim_server_cert: str
    application_bandwidth_tracking: Literal["disable", "enable"]
    tls_session_cache: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GlobalResponse(TypedDict, total=False):
    """Response type for Global - use with .dict property for typed dict access."""
    language: Literal["english", "french", "spanish", "portuguese", "japanese", "trach", "simch", "korean"]
    gui_ipv6: Literal["enable", "disable"]
    gui_replacement_message_groups: Literal["enable", "disable"]
    gui_local_out: Literal["enable", "disable"]
    gui_certificates: Literal["enable", "disable"]
    gui_custom_language: Literal["enable", "disable"]
    gui_wireless_opensecurity: Literal["enable", "disable"]
    gui_app_detection_sdwan: Literal["enable", "disable"]
    gui_display_hostname: Literal["enable", "disable"]
    gui_fortigate_cloud_sandbox: Literal["enable", "disable"]
    gui_firmware_upgrade_warning: Literal["enable", "disable"]
    gui_forticare_registration_setup_warning: Literal["enable", "disable"]
    gui_auto_upgrade_setup_warning: Literal["enable", "disable"]
    gui_workflow_management: Literal["enable", "disable"]
    gui_cdn_usage: Literal["enable", "disable"]
    admin_https_ssl_versions: str
    admin_https_ssl_ciphersuites: str
    admin_https_ssl_banned_ciphers: str
    admintimeout: int
    admin_console_timeout: int
    ssd_trim_freq: Literal["never", "hourly", "daily", "weekly", "monthly"]
    ssd_trim_hour: int
    ssd_trim_min: int
    ssd_trim_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    ssd_trim_date: int
    admin_concurrent: Literal["enable", "disable"]
    admin_lockout_threshold: int
    admin_lockout_duration: int
    refresh: int
    interval: int
    failtime: int
    purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    daily_restart: Literal["enable", "disable"]
    restart_time: str
    wad_restart_mode: Literal["none", "time", "memory"]
    wad_restart_start_time: str
    wad_restart_end_time: str
    wad_p2s_max_body_size: int
    radius_port: int
    speedtestd_server_port: int
    speedtestd_ctrl_port: int
    admin_login_max: int
    remoteauthtimeout: int
    ldapconntimeout: int
    batch_cmdb: Literal["enable", "disable"]
    multi_factor_authentication: Literal["optional", "mandatory"]
    ssl_min_proto_version: Literal["SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    autorun_log_fsck: Literal["enable", "disable"]
    timezone: str
    traffic_priority: Literal["tos", "dscp"]
    traffic_priority_level: Literal["low", "medium", "high"]
    quic_congestion_control_algo: Literal["cubic", "bbr", "bbr2", "reno"]
    quic_max_datagram_size: int
    quic_udp_payload_size_shaping_per_cid: Literal["enable", "disable"]
    quic_ack_thresold: int
    quic_pmtud: Literal["enable", "disable"]
    quic_tls_handshake_timeout: int
    anti_replay: Literal["disable", "loose", "strict"]
    send_pmtu_icmp: Literal["enable", "disable"]
    honor_df: Literal["enable", "disable"]
    pmtu_discovery: Literal["enable", "disable"]
    revision_image_auto_backup: Literal["enable", "disable"]
    revision_backup_on_logout: Literal["enable", "disable"]
    management_vdom: str
    hostname: str
    alias: str
    strong_crypto: Literal["enable", "disable"]
    ssl_static_key_ciphers: Literal["enable", "disable"]
    snat_route_change: Literal["enable", "disable"]
    ipv6_snat_route_change: Literal["enable", "disable"]
    speedtest_server: Literal["enable", "disable"]
    cli_audit_log: Literal["enable", "disable"]
    dh_params: Literal["1024", "1536", "2048", "3072", "4096", "6144", "8192"]
    fds_statistics: Literal["enable", "disable"]
    fds_statistics_period: int
    tcp_option: Literal["enable", "disable"]
    lldp_transmission: Literal["enable", "disable"]
    lldp_reception: Literal["enable", "disable"]
    proxy_auth_timeout: int
    proxy_keep_alive_mode: Literal["session", "traffic", "re-authentication"]
    proxy_re_authentication_time: int
    proxy_auth_lifetime: Literal["enable", "disable"]
    proxy_auth_lifetime_timeout: int
    proxy_resource_mode: Literal["enable", "disable"]
    proxy_cert_use_mgmt_vdom: Literal["enable", "disable"]
    sys_perf_log_interval: int
    check_protocol_header: Literal["loose", "strict"]
    vip_arp_range: Literal["unlimited", "restricted"]
    reset_sessionless_tcp: Literal["enable", "disable"]
    allow_traffic_redirect: Literal["enable", "disable"]
    ipv6_allow_traffic_redirect: Literal["enable", "disable"]
    strict_dirty_session_check: Literal["enable", "disable"]
    tcp_halfclose_timer: int
    tcp_halfopen_timer: int
    tcp_timewait_timer: int
    tcp_rst_timer: int
    udp_idle_timer: int
    block_session_timer: int
    ip_src_port_range: str
    pre_login_banner: Literal["enable", "disable"]
    post_login_banner: Literal["disable", "enable"]
    tftp: Literal["enable", "disable"]
    av_failopen: Literal["pass", "off", "one-shot"]
    av_failopen_session: Literal["enable", "disable"]
    memory_use_threshold_extreme: int
    memory_use_threshold_red: int
    memory_use_threshold_green: int
    ip_fragment_mem_thresholds: int
    ip_fragment_timeout: int
    ipv6_fragment_timeout: int
    cpu_use_threshold: int
    log_single_cpu_high: Literal["enable", "disable"]
    check_reset_range: Literal["strict", "disable"]
    upgrade_report: Literal["enable", "disable"]
    admin_port: int
    admin_sport: int
    admin_host: str
    admin_https_redirect: Literal["enable", "disable"]
    admin_hsts_max_age: int
    admin_ssh_password: Literal["enable", "disable"]
    admin_restrict_local: Literal["all", "non-console-only", "disable"]
    admin_ssh_port: int
    admin_ssh_grace_time: int
    admin_ssh_v1: Literal["enable", "disable"]
    admin_telnet: Literal["enable", "disable"]
    admin_telnet_port: int
    admin_forticloud_sso_login: Literal["enable", "disable"]
    admin_forticloud_sso_default_profile: str
    default_service_source_port: str
    admin_server_cert: str
    admin_https_pki_required: Literal["enable", "disable"]
    wifi_certificate: str
    dhcp_lease_backup_interval: int
    wifi_ca_certificate: str
    auth_http_port: int
    auth_https_port: int
    auth_ike_saml_port: int
    auth_keepalive: Literal["enable", "disable"]
    policy_auth_concurrent: int
    auth_session_limit: Literal["block-new", "logout-inactive"]
    auth_cert: str
    clt_cert_req: Literal["enable", "disable"]
    fortiservice_port: int
    cfg_save: Literal["automatic", "manual", "revert"]
    cfg_revert_timeout: int
    reboot_upon_config_restore: Literal["enable", "disable"]
    admin_scp: Literal["enable", "disable"]
    wireless_controller: Literal["enable", "disable"]
    wireless_controller_port: int
    fortiextender_data_port: int
    fortiextender: Literal["disable", "enable"]
    extender_controller_reserved_network: str
    fortiextender_discovery_lockdown: Literal["disable", "enable"]
    fortiextender_vlan_mode: Literal["enable", "disable"]
    fortiextender_provision_on_authorization: Literal["enable", "disable"]
    switch_controller: Literal["disable", "enable"]
    switch_controller_reserved_network: str
    dnsproxy_worker_count: int
    url_filter_count: int
    httpd_max_worker_count: int
    proxy_worker_count: int
    scanunit_count: int
    fgd_alert_subscription: str
    ipv6_accept_dad: int
    ipv6_allow_anycast_probe: Literal["enable", "disable"]
    ipv6_allow_multicast_probe: Literal["enable", "disable"]
    ipv6_allow_local_in_silent_drop: Literal["enable", "disable"]
    csr_ca_attribute: Literal["enable", "disable"]
    wimax_4g_usb: Literal["enable", "disable"]
    cert_chain_max: int
    sslvpn_max_worker_count: int
    sslvpn_affinity: str
    sslvpn_web_mode: Literal["enable", "disable"]
    two_factor_ftk_expiry: int
    two_factor_email_expiry: int
    two_factor_sms_expiry: int
    two_factor_fac_expiry: int
    two_factor_ftm_expiry: int
    per_user_bal: Literal["enable", "disable"]
    wad_worker_count: int
    wad_worker_dev_cache: int
    wad_csvc_cs_count: int
    wad_csvc_db_count: int
    wad_source_affinity: Literal["disable", "enable"]
    wad_memory_change_granularity: int
    login_timestamp: Literal["enable", "disable"]
    ip_conflict_detection: Literal["enable", "disable"]
    miglogd_children: int
    log_daemon_cpu_threshold: int
    special_file_23_support: Literal["disable", "enable"]
    log_uuid_address: Literal["enable", "disable"]
    log_ssl_connection: Literal["enable", "disable"]
    gui_rest_api_cache: Literal["enable", "disable"]
    rest_api_key_url_query: Literal["enable", "disable"]
    arp_max_entry: int
    ha_affinity: str
    bfd_affinity: str
    cmdbsvr_affinity: str
    av_affinity: str
    wad_affinity: str
    ips_affinity: str
    miglog_affinity: str
    syslog_affinity: str
    url_filter_affinity: str
    router_affinity: str
    ndp_max_entry: int
    br_fdb_max_entry: int
    max_route_cache_size: int
    ipsec_qat_offload: Literal["enable", "disable"]
    device_idle_timeout: int
    user_device_store_max_devices: int
    user_device_store_max_device_mem: int
    user_device_store_max_users: int
    user_device_store_max_unified_mem: int
    gui_device_latitude: str
    gui_device_longitude: str
    private_data_encryption: Literal["disable", "enable"]
    auto_auth_extension_device: Literal["enable", "disable"]
    gui_theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "retro", "dark-matter", "onyx", "eclipse"]
    gui_date_format: Literal["yyyy/MM/dd", "dd/MM/yyyy", "MM/dd/yyyy", "yyyy-MM-dd", "dd-MM-yyyy", "MM-dd-yyyy"]
    gui_date_time_source: Literal["system", "browser"]
    igmp_state_limit: int
    cloud_communication: Literal["enable", "disable"]
    ipsec_ha_seqjump_rate: int
    fortitoken_cloud: Literal["enable", "disable"]
    fortitoken_cloud_push_status: Literal["enable", "disable"]
    fortitoken_cloud_region: str
    fortitoken_cloud_sync_interval: int
    faz_disk_buffer_size: int
    irq_time_accounting: Literal["auto", "force"]
    management_ip: str
    management_port: int
    management_port_use_admin_sport: Literal["enable", "disable"]
    forticonverter_integration: Literal["enable", "disable"]
    forticonverter_config_upload: Literal["once", "disable"]
    internet_service_database: Literal["mini", "standard", "full", "on-demand"]
    internet_service_download_list: list[GlobalInternetservicedownloadlistItem]
    geoip_full_db: Literal["enable", "disable"]
    early_tcp_npu_session: Literal["enable", "disable"]
    npu_neighbor_update: Literal["enable", "disable"]
    delay_tcp_npu_session: Literal["enable", "disable"]
    interface_subnet_usage: Literal["disable", "enable"]
    sflowd_max_children_num: int
    fortigslb_integration: Literal["disable", "enable"]
    user_history_password_threshold: int
    auth_session_auto_backup: Literal["enable", "disable"]
    auth_session_auto_backup_interval: Literal["1min", "5min", "15min", "30min", "1hr"]
    scim_https_port: int
    scim_http_port: int
    scim_server_cert: str
    application_bandwidth_tracking: Literal["disable", "enable"]
    tls_session_cache: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GlobalInternetservicedownloadlistItemObject(FortiObject[GlobalInternetservicedownloadlistItem]):
    """Typed object for internet-service-download-list table items with attribute access."""
    id: int


class GlobalObject(FortiObject):
    """Typed FortiObject for Global with field access."""
    language: Literal["english", "french", "spanish", "portuguese", "japanese", "trach", "simch", "korean"]
    gui_ipv6: Literal["enable", "disable"]
    gui_replacement_message_groups: Literal["enable", "disable"]
    gui_local_out: Literal["enable", "disable"]
    gui_certificates: Literal["enable", "disable"]
    gui_custom_language: Literal["enable", "disable"]
    gui_wireless_opensecurity: Literal["enable", "disable"]
    gui_app_detection_sdwan: Literal["enable", "disable"]
    gui_display_hostname: Literal["enable", "disable"]
    gui_fortigate_cloud_sandbox: Literal["enable", "disable"]
    gui_firmware_upgrade_warning: Literal["enable", "disable"]
    gui_forticare_registration_setup_warning: Literal["enable", "disable"]
    gui_auto_upgrade_setup_warning: Literal["enable", "disable"]
    gui_workflow_management: Literal["enable", "disable"]
    gui_cdn_usage: Literal["enable", "disable"]
    admin_https_ssl_versions: str
    admin_https_ssl_ciphersuites: str
    admin_https_ssl_banned_ciphers: str
    admintimeout: int
    admin_console_timeout: int
    ssd_trim_freq: Literal["never", "hourly", "daily", "weekly", "monthly"]
    ssd_trim_hour: int
    ssd_trim_min: int
    ssd_trim_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    ssd_trim_date: int
    admin_concurrent: Literal["enable", "disable"]
    admin_lockout_threshold: int
    admin_lockout_duration: int
    refresh: int
    interval: int
    failtime: int
    purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]
    daily_restart: Literal["enable", "disable"]
    restart_time: str
    wad_restart_mode: Literal["none", "time", "memory"]
    wad_restart_start_time: str
    wad_restart_end_time: str
    wad_p2s_max_body_size: int
    radius_port: int
    speedtestd_server_port: int
    speedtestd_ctrl_port: int
    admin_login_max: int
    remoteauthtimeout: int
    ldapconntimeout: int
    batch_cmdb: Literal["enable", "disable"]
    multi_factor_authentication: Literal["optional", "mandatory"]
    ssl_min_proto_version: Literal["SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    autorun_log_fsck: Literal["enable", "disable"]
    timezone: str
    traffic_priority: Literal["tos", "dscp"]
    traffic_priority_level: Literal["low", "medium", "high"]
    quic_congestion_control_algo: Literal["cubic", "bbr", "bbr2", "reno"]
    quic_max_datagram_size: int
    quic_udp_payload_size_shaping_per_cid: Literal["enable", "disable"]
    quic_ack_thresold: int
    quic_pmtud: Literal["enable", "disable"]
    quic_tls_handshake_timeout: int
    anti_replay: Literal["disable", "loose", "strict"]
    send_pmtu_icmp: Literal["enable", "disable"]
    honor_df: Literal["enable", "disable"]
    pmtu_discovery: Literal["enable", "disable"]
    revision_image_auto_backup: Literal["enable", "disable"]
    revision_backup_on_logout: Literal["enable", "disable"]
    management_vdom: str
    hostname: str
    alias: str
    strong_crypto: Literal["enable", "disable"]
    ssl_static_key_ciphers: Literal["enable", "disable"]
    snat_route_change: Literal["enable", "disable"]
    ipv6_snat_route_change: Literal["enable", "disable"]
    speedtest_server: Literal["enable", "disable"]
    cli_audit_log: Literal["enable", "disable"]
    dh_params: Literal["1024", "1536", "2048", "3072", "4096", "6144", "8192"]
    fds_statistics: Literal["enable", "disable"]
    fds_statistics_period: int
    tcp_option: Literal["enable", "disable"]
    lldp_transmission: Literal["enable", "disable"]
    lldp_reception: Literal["enable", "disable"]
    proxy_auth_timeout: int
    proxy_keep_alive_mode: Literal["session", "traffic", "re-authentication"]
    proxy_re_authentication_time: int
    proxy_auth_lifetime: Literal["enable", "disable"]
    proxy_auth_lifetime_timeout: int
    proxy_resource_mode: Literal["enable", "disable"]
    proxy_cert_use_mgmt_vdom: Literal["enable", "disable"]
    sys_perf_log_interval: int
    check_protocol_header: Literal["loose", "strict"]
    vip_arp_range: Literal["unlimited", "restricted"]
    reset_sessionless_tcp: Literal["enable", "disable"]
    allow_traffic_redirect: Literal["enable", "disable"]
    ipv6_allow_traffic_redirect: Literal["enable", "disable"]
    strict_dirty_session_check: Literal["enable", "disable"]
    tcp_halfclose_timer: int
    tcp_halfopen_timer: int
    tcp_timewait_timer: int
    tcp_rst_timer: int
    udp_idle_timer: int
    block_session_timer: int
    ip_src_port_range: str
    pre_login_banner: Literal["enable", "disable"]
    post_login_banner: Literal["disable", "enable"]
    tftp: Literal["enable", "disable"]
    av_failopen: Literal["pass", "off", "one-shot"]
    av_failopen_session: Literal["enable", "disable"]
    memory_use_threshold_extreme: int
    memory_use_threshold_red: int
    memory_use_threshold_green: int
    ip_fragment_mem_thresholds: int
    ip_fragment_timeout: int
    ipv6_fragment_timeout: int
    cpu_use_threshold: int
    log_single_cpu_high: Literal["enable", "disable"]
    check_reset_range: Literal["strict", "disable"]
    upgrade_report: Literal["enable", "disable"]
    admin_port: int
    admin_sport: int
    admin_host: str
    admin_https_redirect: Literal["enable", "disable"]
    admin_hsts_max_age: int
    admin_ssh_password: Literal["enable", "disable"]
    admin_restrict_local: Literal["all", "non-console-only", "disable"]
    admin_ssh_port: int
    admin_ssh_grace_time: int
    admin_ssh_v1: Literal["enable", "disable"]
    admin_telnet: Literal["enable", "disable"]
    admin_telnet_port: int
    admin_forticloud_sso_login: Literal["enable", "disable"]
    admin_forticloud_sso_default_profile: str
    default_service_source_port: str
    admin_server_cert: str
    admin_https_pki_required: Literal["enable", "disable"]
    wifi_certificate: str
    dhcp_lease_backup_interval: int
    wifi_ca_certificate: str
    auth_http_port: int
    auth_https_port: int
    auth_ike_saml_port: int
    auth_keepalive: Literal["enable", "disable"]
    policy_auth_concurrent: int
    auth_session_limit: Literal["block-new", "logout-inactive"]
    auth_cert: str
    clt_cert_req: Literal["enable", "disable"]
    fortiservice_port: int
    cfg_save: Literal["automatic", "manual", "revert"]
    cfg_revert_timeout: int
    reboot_upon_config_restore: Literal["enable", "disable"]
    admin_scp: Literal["enable", "disable"]
    wireless_controller: Literal["enable", "disable"]
    wireless_controller_port: int
    fortiextender_data_port: int
    fortiextender: Literal["disable", "enable"]
    extender_controller_reserved_network: str
    fortiextender_discovery_lockdown: Literal["disable", "enable"]
    fortiextender_vlan_mode: Literal["enable", "disable"]
    fortiextender_provision_on_authorization: Literal["enable", "disable"]
    switch_controller: Literal["disable", "enable"]
    switch_controller_reserved_network: str
    dnsproxy_worker_count: int
    url_filter_count: int
    httpd_max_worker_count: int
    proxy_worker_count: int
    scanunit_count: int
    fgd_alert_subscription: str
    ipv6_accept_dad: int
    ipv6_allow_anycast_probe: Literal["enable", "disable"]
    ipv6_allow_multicast_probe: Literal["enable", "disable"]
    ipv6_allow_local_in_silent_drop: Literal["enable", "disable"]
    csr_ca_attribute: Literal["enable", "disable"]
    wimax_4g_usb: Literal["enable", "disable"]
    cert_chain_max: int
    sslvpn_max_worker_count: int
    sslvpn_affinity: str
    sslvpn_web_mode: Literal["enable", "disable"]
    two_factor_ftk_expiry: int
    two_factor_email_expiry: int
    two_factor_sms_expiry: int
    two_factor_fac_expiry: int
    two_factor_ftm_expiry: int
    per_user_bal: Literal["enable", "disable"]
    wad_worker_count: int
    wad_worker_dev_cache: int
    wad_csvc_cs_count: int
    wad_csvc_db_count: int
    wad_source_affinity: Literal["disable", "enable"]
    wad_memory_change_granularity: int
    login_timestamp: Literal["enable", "disable"]
    ip_conflict_detection: Literal["enable", "disable"]
    miglogd_children: int
    log_daemon_cpu_threshold: int
    special_file_23_support: Literal["disable", "enable"]
    log_uuid_address: Literal["enable", "disable"]
    log_ssl_connection: Literal["enable", "disable"]
    gui_rest_api_cache: Literal["enable", "disable"]
    rest_api_key_url_query: Literal["enable", "disable"]
    arp_max_entry: int
    ha_affinity: str
    bfd_affinity: str
    cmdbsvr_affinity: str
    av_affinity: str
    wad_affinity: str
    ips_affinity: str
    miglog_affinity: str
    syslog_affinity: str
    url_filter_affinity: str
    router_affinity: str
    ndp_max_entry: int
    br_fdb_max_entry: int
    max_route_cache_size: int
    ipsec_qat_offload: Literal["enable", "disable"]
    device_idle_timeout: int
    user_device_store_max_devices: int
    user_device_store_max_device_mem: int
    user_device_store_max_users: int
    user_device_store_max_unified_mem: int
    gui_device_latitude: str
    gui_device_longitude: str
    private_data_encryption: Literal["disable", "enable"]
    auto_auth_extension_device: Literal["enable", "disable"]
    gui_theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "retro", "dark-matter", "onyx", "eclipse"]
    gui_date_format: Literal["yyyy/MM/dd", "dd/MM/yyyy", "MM/dd/yyyy", "yyyy-MM-dd", "dd-MM-yyyy", "MM-dd-yyyy"]
    gui_date_time_source: Literal["system", "browser"]
    igmp_state_limit: int
    cloud_communication: Literal["enable", "disable"]
    ipsec_ha_seqjump_rate: int
    fortitoken_cloud: Literal["enable", "disable"]
    fortitoken_cloud_push_status: Literal["enable", "disable"]
    fortitoken_cloud_region: str
    fortitoken_cloud_sync_interval: int
    faz_disk_buffer_size: int
    irq_time_accounting: Literal["auto", "force"]
    management_ip: str
    management_port: int
    management_port_use_admin_sport: Literal["enable", "disable"]
    forticonverter_integration: Literal["enable", "disable"]
    forticonverter_config_upload: Literal["once", "disable"]
    internet_service_database: Literal["mini", "standard", "full", "on-demand"]
    internet_service_download_list: FortiObjectList[GlobalInternetservicedownloadlistItemObject]
    geoip_full_db: Literal["enable", "disable"]
    early_tcp_npu_session: Literal["enable", "disable"]
    npu_neighbor_update: Literal["enable", "disable"]
    delay_tcp_npu_session: Literal["enable", "disable"]
    interface_subnet_usage: Literal["disable", "enable"]
    sflowd_max_children_num: int
    fortigslb_integration: Literal["disable", "enable"]
    user_history_password_threshold: int
    auth_session_auto_backup: Literal["enable", "disable"]
    auth_session_auto_backup_interval: Literal["1min", "5min", "15min", "30min", "1hr"]
    scim_https_port: int
    scim_http_port: int
    scim_server_cert: str
    application_bandwidth_tracking: Literal["disable", "enable"]
    tls_session_cache: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Global:
    """
    
    Endpoint: system/global_
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Singleton endpoint (no mkey)
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GlobalObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: GlobalPayload | None = ...,
        language: Literal["english", "french", "spanish", "portuguese", "japanese", "trach", "simch", "korean"] | None = ...,
        gui_ipv6: Literal["enable", "disable"] | None = ...,
        gui_replacement_message_groups: Literal["enable", "disable"] | None = ...,
        gui_local_out: Literal["enable", "disable"] | None = ...,
        gui_certificates: Literal["enable", "disable"] | None = ...,
        gui_custom_language: Literal["enable", "disable"] | None = ...,
        gui_wireless_opensecurity: Literal["enable", "disable"] | None = ...,
        gui_app_detection_sdwan: Literal["enable", "disable"] | None = ...,
        gui_display_hostname: Literal["enable", "disable"] | None = ...,
        gui_fortigate_cloud_sandbox: Literal["enable", "disable"] | None = ...,
        gui_firmware_upgrade_warning: Literal["enable", "disable"] | None = ...,
        gui_forticare_registration_setup_warning: Literal["enable", "disable"] | None = ...,
        gui_auto_upgrade_setup_warning: Literal["enable", "disable"] | None = ...,
        gui_workflow_management: Literal["enable", "disable"] | None = ...,
        gui_cdn_usage: Literal["enable", "disable"] | None = ...,
        admin_https_ssl_versions: str | list[str] | None = ...,
        admin_https_ssl_ciphersuites: str | list[str] | None = ...,
        admin_https_ssl_banned_ciphers: str | list[str] | None = ...,
        admintimeout: int | None = ...,
        admin_console_timeout: int | None = ...,
        ssd_trim_freq: Literal["never", "hourly", "daily", "weekly", "monthly"] | None = ...,
        ssd_trim_hour: int | None = ...,
        ssd_trim_min: int | None = ...,
        ssd_trim_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        ssd_trim_date: int | None = ...,
        admin_concurrent: Literal["enable", "disable"] | None = ...,
        admin_lockout_threshold: int | None = ...,
        admin_lockout_duration: int | None = ...,
        refresh: int | None = ...,
        interval: int | None = ...,
        failtime: int | None = ...,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        daily_restart: Literal["enable", "disable"] | None = ...,
        restart_time: str | None = ...,
        wad_restart_mode: Literal["none", "time", "memory"] | None = ...,
        wad_restart_start_time: str | None = ...,
        wad_restart_end_time: str | None = ...,
        wad_p2s_max_body_size: int | None = ...,
        radius_port: int | None = ...,
        speedtestd_server_port: int | None = ...,
        speedtestd_ctrl_port: int | None = ...,
        admin_login_max: int | None = ...,
        remoteauthtimeout: int | None = ...,
        ldapconntimeout: int | None = ...,
        batch_cmdb: Literal["enable", "disable"] | None = ...,
        multi_factor_authentication: Literal["optional", "mandatory"] | None = ...,
        ssl_min_proto_version: Literal["SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        autorun_log_fsck: Literal["enable", "disable"] | None = ...,
        timezone: str | None = ...,
        traffic_priority: Literal["tos", "dscp"] | None = ...,
        traffic_priority_level: Literal["low", "medium", "high"] | None = ...,
        quic_congestion_control_algo: Literal["cubic", "bbr", "bbr2", "reno"] | None = ...,
        quic_max_datagram_size: int | None = ...,
        quic_udp_payload_size_shaping_per_cid: Literal["enable", "disable"] | None = ...,
        quic_ack_thresold: int | None = ...,
        quic_pmtud: Literal["enable", "disable"] | None = ...,
        quic_tls_handshake_timeout: int | None = ...,
        anti_replay: Literal["disable", "loose", "strict"] | None = ...,
        send_pmtu_icmp: Literal["enable", "disable"] | None = ...,
        honor_df: Literal["enable", "disable"] | None = ...,
        pmtu_discovery: Literal["enable", "disable"] | None = ...,
        revision_image_auto_backup: Literal["enable", "disable"] | None = ...,
        revision_backup_on_logout: Literal["enable", "disable"] | None = ...,
        management_vdom: str | None = ...,
        hostname: str | None = ...,
        alias: str | None = ...,
        strong_crypto: Literal["enable", "disable"] | None = ...,
        ssl_static_key_ciphers: Literal["enable", "disable"] | None = ...,
        snat_route_change: Literal["enable", "disable"] | None = ...,
        ipv6_snat_route_change: Literal["enable", "disable"] | None = ...,
        speedtest_server: Literal["enable", "disable"] | None = ...,
        cli_audit_log: Literal["enable", "disable"] | None = ...,
        dh_params: Literal["1024", "1536", "2048", "3072", "4096", "6144", "8192"] | None = ...,
        fds_statistics: Literal["enable", "disable"] | None = ...,
        fds_statistics_period: int | None = ...,
        tcp_option: Literal["enable", "disable"] | None = ...,
        lldp_transmission: Literal["enable", "disable"] | None = ...,
        lldp_reception: Literal["enable", "disable"] | None = ...,
        proxy_auth_timeout: int | None = ...,
        proxy_keep_alive_mode: Literal["session", "traffic", "re-authentication"] | None = ...,
        proxy_re_authentication_time: int | None = ...,
        proxy_auth_lifetime: Literal["enable", "disable"] | None = ...,
        proxy_auth_lifetime_timeout: int | None = ...,
        proxy_resource_mode: Literal["enable", "disable"] | None = ...,
        proxy_cert_use_mgmt_vdom: Literal["enable", "disable"] | None = ...,
        sys_perf_log_interval: int | None = ...,
        check_protocol_header: Literal["loose", "strict"] | None = ...,
        vip_arp_range: Literal["unlimited", "restricted"] | None = ...,
        reset_sessionless_tcp: Literal["enable", "disable"] | None = ...,
        allow_traffic_redirect: Literal["enable", "disable"] | None = ...,
        ipv6_allow_traffic_redirect: Literal["enable", "disable"] | None = ...,
        strict_dirty_session_check: Literal["enable", "disable"] | None = ...,
        tcp_halfclose_timer: int | None = ...,
        tcp_halfopen_timer: int | None = ...,
        tcp_timewait_timer: int | None = ...,
        tcp_rst_timer: int | None = ...,
        udp_idle_timer: int | None = ...,
        block_session_timer: int | None = ...,
        ip_src_port_range: str | None = ...,
        pre_login_banner: Literal["enable", "disable"] | None = ...,
        post_login_banner: Literal["disable", "enable"] | None = ...,
        tftp: Literal["enable", "disable"] | None = ...,
        av_failopen: Literal["pass", "off", "one-shot"] | None = ...,
        av_failopen_session: Literal["enable", "disable"] | None = ...,
        memory_use_threshold_extreme: int | None = ...,
        memory_use_threshold_red: int | None = ...,
        memory_use_threshold_green: int | None = ...,
        ip_fragment_mem_thresholds: int | None = ...,
        ip_fragment_timeout: int | None = ...,
        ipv6_fragment_timeout: int | None = ...,
        cpu_use_threshold: int | None = ...,
        log_single_cpu_high: Literal["enable", "disable"] | None = ...,
        check_reset_range: Literal["strict", "disable"] | None = ...,
        upgrade_report: Literal["enable", "disable"] | None = ...,
        admin_port: int | None = ...,
        admin_sport: int | None = ...,
        admin_host: str | None = ...,
        admin_https_redirect: Literal["enable", "disable"] | None = ...,
        admin_hsts_max_age: int | None = ...,
        admin_ssh_password: Literal["enable", "disable"] | None = ...,
        admin_restrict_local: Literal["all", "non-console-only", "disable"] | None = ...,
        admin_ssh_port: int | None = ...,
        admin_ssh_grace_time: int | None = ...,
        admin_ssh_v1: Literal["enable", "disable"] | None = ...,
        admin_telnet: Literal["enable", "disable"] | None = ...,
        admin_telnet_port: int | None = ...,
        admin_forticloud_sso_login: Literal["enable", "disable"] | None = ...,
        admin_forticloud_sso_default_profile: str | None = ...,
        default_service_source_port: str | None = ...,
        admin_server_cert: str | None = ...,
        admin_https_pki_required: Literal["enable", "disable"] | None = ...,
        wifi_certificate: str | None = ...,
        dhcp_lease_backup_interval: int | None = ...,
        wifi_ca_certificate: str | None = ...,
        auth_http_port: int | None = ...,
        auth_https_port: int | None = ...,
        auth_ike_saml_port: int | None = ...,
        auth_keepalive: Literal["enable", "disable"] | None = ...,
        policy_auth_concurrent: int | None = ...,
        auth_session_limit: Literal["block-new", "logout-inactive"] | None = ...,
        auth_cert: str | None = ...,
        clt_cert_req: Literal["enable", "disable"] | None = ...,
        fortiservice_port: int | None = ...,
        cfg_save: Literal["automatic", "manual", "revert"] | None = ...,
        cfg_revert_timeout: int | None = ...,
        reboot_upon_config_restore: Literal["enable", "disable"] | None = ...,
        admin_scp: Literal["enable", "disable"] | None = ...,
        wireless_controller: Literal["enable", "disable"] | None = ...,
        wireless_controller_port: int | None = ...,
        fortiextender_data_port: int | None = ...,
        fortiextender: Literal["disable", "enable"] | None = ...,
        extender_controller_reserved_network: str | None = ...,
        fortiextender_discovery_lockdown: Literal["disable", "enable"] | None = ...,
        fortiextender_vlan_mode: Literal["enable", "disable"] | None = ...,
        fortiextender_provision_on_authorization: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["disable", "enable"] | None = ...,
        switch_controller_reserved_network: str | None = ...,
        dnsproxy_worker_count: int | None = ...,
        url_filter_count: int | None = ...,
        httpd_max_worker_count: int | None = ...,
        proxy_worker_count: int | None = ...,
        scanunit_count: int | None = ...,
        fgd_alert_subscription: str | list[str] | None = ...,
        ipv6_accept_dad: int | None = ...,
        ipv6_allow_anycast_probe: Literal["enable", "disable"] | None = ...,
        ipv6_allow_multicast_probe: Literal["enable", "disable"] | None = ...,
        ipv6_allow_local_in_silent_drop: Literal["enable", "disable"] | None = ...,
        csr_ca_attribute: Literal["enable", "disable"] | None = ...,
        wimax_4g_usb: Literal["enable", "disable"] | None = ...,
        cert_chain_max: int | None = ...,
        sslvpn_max_worker_count: int | None = ...,
        sslvpn_affinity: str | None = ...,
        sslvpn_web_mode: Literal["enable", "disable"] | None = ...,
        two_factor_ftk_expiry: int | None = ...,
        two_factor_email_expiry: int | None = ...,
        two_factor_sms_expiry: int | None = ...,
        two_factor_fac_expiry: int | None = ...,
        two_factor_ftm_expiry: int | None = ...,
        per_user_bal: Literal["enable", "disable"] | None = ...,
        wad_worker_count: int | None = ...,
        wad_worker_dev_cache: int | None = ...,
        wad_csvc_cs_count: int | None = ...,
        wad_csvc_db_count: int | None = ...,
        wad_source_affinity: Literal["disable", "enable"] | None = ...,
        wad_memory_change_granularity: int | None = ...,
        login_timestamp: Literal["enable", "disable"] | None = ...,
        ip_conflict_detection: Literal["enable", "disable"] | None = ...,
        miglogd_children: int | None = ...,
        log_daemon_cpu_threshold: int | None = ...,
        special_file_23_support: Literal["disable", "enable"] | None = ...,
        log_uuid_address: Literal["enable", "disable"] | None = ...,
        log_ssl_connection: Literal["enable", "disable"] | None = ...,
        gui_rest_api_cache: Literal["enable", "disable"] | None = ...,
        rest_api_key_url_query: Literal["enable", "disable"] | None = ...,
        arp_max_entry: int | None = ...,
        ha_affinity: str | None = ...,
        bfd_affinity: str | None = ...,
        cmdbsvr_affinity: str | None = ...,
        av_affinity: str | None = ...,
        wad_affinity: str | None = ...,
        ips_affinity: str | None = ...,
        miglog_affinity: str | None = ...,
        syslog_affinity: str | None = ...,
        url_filter_affinity: str | None = ...,
        router_affinity: str | None = ...,
        ndp_max_entry: int | None = ...,
        br_fdb_max_entry: int | None = ...,
        max_route_cache_size: int | None = ...,
        ipsec_qat_offload: Literal["enable", "disable"] | None = ...,
        device_idle_timeout: int | None = ...,
        user_device_store_max_devices: int | None = ...,
        user_device_store_max_device_mem: int | None = ...,
        user_device_store_max_users: int | None = ...,
        user_device_store_max_unified_mem: int | None = ...,
        gui_device_latitude: str | None = ...,
        gui_device_longitude: str | None = ...,
        private_data_encryption: Literal["disable", "enable"] | None = ...,
        auto_auth_extension_device: Literal["enable", "disable"] | None = ...,
        gui_theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "retro", "dark-matter", "onyx", "eclipse"] | None = ...,
        gui_date_format: Literal["yyyy/MM/dd", "dd/MM/yyyy", "MM/dd/yyyy", "yyyy-MM-dd", "dd-MM-yyyy", "MM-dd-yyyy"] | None = ...,
        gui_date_time_source: Literal["system", "browser"] | None = ...,
        igmp_state_limit: int | None = ...,
        cloud_communication: Literal["enable", "disable"] | None = ...,
        ipsec_ha_seqjump_rate: int | None = ...,
        fortitoken_cloud: Literal["enable", "disable"] | None = ...,
        fortitoken_cloud_push_status: Literal["enable", "disable"] | None = ...,
        fortitoken_cloud_region: str | None = ...,
        fortitoken_cloud_sync_interval: int | None = ...,
        faz_disk_buffer_size: int | None = ...,
        irq_time_accounting: Literal["auto", "force"] | None = ...,
        management_ip: str | None = ...,
        management_port: int | None = ...,
        management_port_use_admin_sport: Literal["enable", "disable"] | None = ...,
        forticonverter_integration: Literal["enable", "disable"] | None = ...,
        forticonverter_config_upload: Literal["once", "disable"] | None = ...,
        internet_service_database: Literal["mini", "standard", "full", "on-demand"] | None = ...,
        internet_service_download_list: str | list[str] | list[GlobalInternetservicedownloadlistItem] | None = ...,
        geoip_full_db: Literal["enable", "disable"] | None = ...,
        early_tcp_npu_session: Literal["enable", "disable"] | None = ...,
        npu_neighbor_update: Literal["enable", "disable"] | None = ...,
        delay_tcp_npu_session: Literal["enable", "disable"] | None = ...,
        interface_subnet_usage: Literal["disable", "enable"] | None = ...,
        sflowd_max_children_num: int | None = ...,
        fortigslb_integration: Literal["disable", "enable"] | None = ...,
        user_history_password_threshold: int | None = ...,
        auth_session_auto_backup: Literal["enable", "disable"] | None = ...,
        auth_session_auto_backup_interval: Literal["1min", "5min", "15min", "30min", "1hr"] | None = ...,
        scim_https_port: int | None = ...,
        scim_http_port: int | None = ...,
        scim_server_cert: str | None = ...,
        application_bandwidth_tracking: Literal["disable", "enable"] | None = ...,
        tls_session_cache: Literal["enable", "disable"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GlobalObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: GlobalPayload | None = ...,
        language: Literal["english", "french", "spanish", "portuguese", "japanese", "trach", "simch", "korean"] | None = ...,
        gui_ipv6: Literal["enable", "disable"] | None = ...,
        gui_replacement_message_groups: Literal["enable", "disable"] | None = ...,
        gui_local_out: Literal["enable", "disable"] | None = ...,
        gui_certificates: Literal["enable", "disable"] | None = ...,
        gui_custom_language: Literal["enable", "disable"] | None = ...,
        gui_wireless_opensecurity: Literal["enable", "disable"] | None = ...,
        gui_app_detection_sdwan: Literal["enable", "disable"] | None = ...,
        gui_display_hostname: Literal["enable", "disable"] | None = ...,
        gui_fortigate_cloud_sandbox: Literal["enable", "disable"] | None = ...,
        gui_firmware_upgrade_warning: Literal["enable", "disable"] | None = ...,
        gui_forticare_registration_setup_warning: Literal["enable", "disable"] | None = ...,
        gui_auto_upgrade_setup_warning: Literal["enable", "disable"] | None = ...,
        gui_workflow_management: Literal["enable", "disable"] | None = ...,
        gui_cdn_usage: Literal["enable", "disable"] | None = ...,
        admin_https_ssl_versions: Literal["tlsv1-1", "tlsv1-2", "tlsv1-3"] | list[str] | None = ...,
        admin_https_ssl_ciphersuites: Literal["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-AES-128-CCM-SHA256", "TLS-AES-128-CCM-8-SHA256"] | list[str] | None = ...,
        admin_https_ssl_banned_ciphers: Literal["RSA", "DHE", "ECDHE", "DSS", "ECDSA", "AES", "AESGCM", "CAMELLIA", "3DES", "SHA1", "SHA256", "SHA384", "STATIC", "CHACHA20", "ARIA", "AESCCM"] | list[str] | None = ...,
        admintimeout: int | None = ...,
        admin_console_timeout: int | None = ...,
        ssd_trim_freq: Literal["never", "hourly", "daily", "weekly", "monthly"] | None = ...,
        ssd_trim_hour: int | None = ...,
        ssd_trim_min: int | None = ...,
        ssd_trim_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        ssd_trim_date: int | None = ...,
        admin_concurrent: Literal["enable", "disable"] | None = ...,
        admin_lockout_threshold: int | None = ...,
        admin_lockout_duration: int | None = ...,
        refresh: int | None = ...,
        interval: int | None = ...,
        failtime: int | None = ...,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        daily_restart: Literal["enable", "disable"] | None = ...,
        restart_time: str | None = ...,
        wad_restart_mode: Literal["none", "time", "memory"] | None = ...,
        wad_restart_start_time: str | None = ...,
        wad_restart_end_time: str | None = ...,
        wad_p2s_max_body_size: int | None = ...,
        radius_port: int | None = ...,
        speedtestd_server_port: int | None = ...,
        speedtestd_ctrl_port: int | None = ...,
        admin_login_max: int | None = ...,
        remoteauthtimeout: int | None = ...,
        ldapconntimeout: int | None = ...,
        batch_cmdb: Literal["enable", "disable"] | None = ...,
        multi_factor_authentication: Literal["optional", "mandatory"] | None = ...,
        ssl_min_proto_version: Literal["SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        autorun_log_fsck: Literal["enable", "disable"] | None = ...,
        timezone: str | None = ...,
        traffic_priority: Literal["tos", "dscp"] | None = ...,
        traffic_priority_level: Literal["low", "medium", "high"] | None = ...,
        quic_congestion_control_algo: Literal["cubic", "bbr", "bbr2", "reno"] | None = ...,
        quic_max_datagram_size: int | None = ...,
        quic_udp_payload_size_shaping_per_cid: Literal["enable", "disable"] | None = ...,
        quic_ack_thresold: int | None = ...,
        quic_pmtud: Literal["enable", "disable"] | None = ...,
        quic_tls_handshake_timeout: int | None = ...,
        anti_replay: Literal["disable", "loose", "strict"] | None = ...,
        send_pmtu_icmp: Literal["enable", "disable"] | None = ...,
        honor_df: Literal["enable", "disable"] | None = ...,
        pmtu_discovery: Literal["enable", "disable"] | None = ...,
        revision_image_auto_backup: Literal["enable", "disable"] | None = ...,
        revision_backup_on_logout: Literal["enable", "disable"] | None = ...,
        management_vdom: str | None = ...,
        hostname: str | None = ...,
        alias: str | None = ...,
        strong_crypto: Literal["enable", "disable"] | None = ...,
        ssl_static_key_ciphers: Literal["enable", "disable"] | None = ...,
        snat_route_change: Literal["enable", "disable"] | None = ...,
        ipv6_snat_route_change: Literal["enable", "disable"] | None = ...,
        speedtest_server: Literal["enable", "disable"] | None = ...,
        cli_audit_log: Literal["enable", "disable"] | None = ...,
        dh_params: Literal["1024", "1536", "2048", "3072", "4096", "6144", "8192"] | None = ...,
        fds_statistics: Literal["enable", "disable"] | None = ...,
        fds_statistics_period: int | None = ...,
        tcp_option: Literal["enable", "disable"] | None = ...,
        lldp_transmission: Literal["enable", "disable"] | None = ...,
        lldp_reception: Literal["enable", "disable"] | None = ...,
        proxy_auth_timeout: int | None = ...,
        proxy_keep_alive_mode: Literal["session", "traffic", "re-authentication"] | None = ...,
        proxy_re_authentication_time: int | None = ...,
        proxy_auth_lifetime: Literal["enable", "disable"] | None = ...,
        proxy_auth_lifetime_timeout: int | None = ...,
        proxy_resource_mode: Literal["enable", "disable"] | None = ...,
        proxy_cert_use_mgmt_vdom: Literal["enable", "disable"] | None = ...,
        sys_perf_log_interval: int | None = ...,
        check_protocol_header: Literal["loose", "strict"] | None = ...,
        vip_arp_range: Literal["unlimited", "restricted"] | None = ...,
        reset_sessionless_tcp: Literal["enable", "disable"] | None = ...,
        allow_traffic_redirect: Literal["enable", "disable"] | None = ...,
        ipv6_allow_traffic_redirect: Literal["enable", "disable"] | None = ...,
        strict_dirty_session_check: Literal["enable", "disable"] | None = ...,
        tcp_halfclose_timer: int | None = ...,
        tcp_halfopen_timer: int | None = ...,
        tcp_timewait_timer: int | None = ...,
        tcp_rst_timer: int | None = ...,
        udp_idle_timer: int | None = ...,
        block_session_timer: int | None = ...,
        ip_src_port_range: str | None = ...,
        pre_login_banner: Literal["enable", "disable"] | None = ...,
        post_login_banner: Literal["disable", "enable"] | None = ...,
        tftp: Literal["enable", "disable"] | None = ...,
        av_failopen: Literal["pass", "off", "one-shot"] | None = ...,
        av_failopen_session: Literal["enable", "disable"] | None = ...,
        memory_use_threshold_extreme: int | None = ...,
        memory_use_threshold_red: int | None = ...,
        memory_use_threshold_green: int | None = ...,
        ip_fragment_mem_thresholds: int | None = ...,
        ip_fragment_timeout: int | None = ...,
        ipv6_fragment_timeout: int | None = ...,
        cpu_use_threshold: int | None = ...,
        log_single_cpu_high: Literal["enable", "disable"] | None = ...,
        check_reset_range: Literal["strict", "disable"] | None = ...,
        upgrade_report: Literal["enable", "disable"] | None = ...,
        admin_port: int | None = ...,
        admin_sport: int | None = ...,
        admin_host: str | None = ...,
        admin_https_redirect: Literal["enable", "disable"] | None = ...,
        admin_hsts_max_age: int | None = ...,
        admin_ssh_password: Literal["enable", "disable"] | None = ...,
        admin_restrict_local: Literal["all", "non-console-only", "disable"] | None = ...,
        admin_ssh_port: int | None = ...,
        admin_ssh_grace_time: int | None = ...,
        admin_ssh_v1: Literal["enable", "disable"] | None = ...,
        admin_telnet: Literal["enable", "disable"] | None = ...,
        admin_telnet_port: int | None = ...,
        admin_forticloud_sso_login: Literal["enable", "disable"] | None = ...,
        admin_forticloud_sso_default_profile: str | None = ...,
        default_service_source_port: str | None = ...,
        admin_server_cert: str | None = ...,
        admin_https_pki_required: Literal["enable", "disable"] | None = ...,
        wifi_certificate: str | None = ...,
        dhcp_lease_backup_interval: int | None = ...,
        wifi_ca_certificate: str | None = ...,
        auth_http_port: int | None = ...,
        auth_https_port: int | None = ...,
        auth_ike_saml_port: int | None = ...,
        auth_keepalive: Literal["enable", "disable"] | None = ...,
        policy_auth_concurrent: int | None = ...,
        auth_session_limit: Literal["block-new", "logout-inactive"] | None = ...,
        auth_cert: str | None = ...,
        clt_cert_req: Literal["enable", "disable"] | None = ...,
        fortiservice_port: int | None = ...,
        cfg_save: Literal["automatic", "manual", "revert"] | None = ...,
        cfg_revert_timeout: int | None = ...,
        reboot_upon_config_restore: Literal["enable", "disable"] | None = ...,
        admin_scp: Literal["enable", "disable"] | None = ...,
        wireless_controller: Literal["enable", "disable"] | None = ...,
        wireless_controller_port: int | None = ...,
        fortiextender_data_port: int | None = ...,
        fortiextender: Literal["disable", "enable"] | None = ...,
        extender_controller_reserved_network: str | None = ...,
        fortiextender_discovery_lockdown: Literal["disable", "enable"] | None = ...,
        fortiextender_vlan_mode: Literal["enable", "disable"] | None = ...,
        fortiextender_provision_on_authorization: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["disable", "enable"] | None = ...,
        switch_controller_reserved_network: str | None = ...,
        dnsproxy_worker_count: int | None = ...,
        url_filter_count: int | None = ...,
        httpd_max_worker_count: int | None = ...,
        proxy_worker_count: int | None = ...,
        scanunit_count: int | None = ...,
        fgd_alert_subscription: Literal["advisory", "latest-threat", "latest-virus", "latest-attack", "new-antivirus-db", "new-attack-db"] | list[str] | None = ...,
        ipv6_accept_dad: int | None = ...,
        ipv6_allow_anycast_probe: Literal["enable", "disable"] | None = ...,
        ipv6_allow_multicast_probe: Literal["enable", "disable"] | None = ...,
        ipv6_allow_local_in_silent_drop: Literal["enable", "disable"] | None = ...,
        csr_ca_attribute: Literal["enable", "disable"] | None = ...,
        wimax_4g_usb: Literal["enable", "disable"] | None = ...,
        cert_chain_max: int | None = ...,
        sslvpn_max_worker_count: int | None = ...,
        sslvpn_affinity: str | None = ...,
        sslvpn_web_mode: Literal["enable", "disable"] | None = ...,
        two_factor_ftk_expiry: int | None = ...,
        two_factor_email_expiry: int | None = ...,
        two_factor_sms_expiry: int | None = ...,
        two_factor_fac_expiry: int | None = ...,
        two_factor_ftm_expiry: int | None = ...,
        per_user_bal: Literal["enable", "disable"] | None = ...,
        wad_worker_count: int | None = ...,
        wad_worker_dev_cache: int | None = ...,
        wad_csvc_cs_count: int | None = ...,
        wad_csvc_db_count: int | None = ...,
        wad_source_affinity: Literal["disable", "enable"] | None = ...,
        wad_memory_change_granularity: int | None = ...,
        login_timestamp: Literal["enable", "disable"] | None = ...,
        ip_conflict_detection: Literal["enable", "disable"] | None = ...,
        miglogd_children: int | None = ...,
        log_daemon_cpu_threshold: int | None = ...,
        special_file_23_support: Literal["disable", "enable"] | None = ...,
        log_uuid_address: Literal["enable", "disable"] | None = ...,
        log_ssl_connection: Literal["enable", "disable"] | None = ...,
        gui_rest_api_cache: Literal["enable", "disable"] | None = ...,
        rest_api_key_url_query: Literal["enable", "disable"] | None = ...,
        arp_max_entry: int | None = ...,
        ha_affinity: str | None = ...,
        bfd_affinity: str | None = ...,
        cmdbsvr_affinity: str | None = ...,
        av_affinity: str | None = ...,
        wad_affinity: str | None = ...,
        ips_affinity: str | None = ...,
        miglog_affinity: str | None = ...,
        syslog_affinity: str | None = ...,
        url_filter_affinity: str | None = ...,
        router_affinity: str | None = ...,
        ndp_max_entry: int | None = ...,
        br_fdb_max_entry: int | None = ...,
        max_route_cache_size: int | None = ...,
        ipsec_qat_offload: Literal["enable", "disable"] | None = ...,
        device_idle_timeout: int | None = ...,
        user_device_store_max_devices: int | None = ...,
        user_device_store_max_device_mem: int | None = ...,
        user_device_store_max_users: int | None = ...,
        user_device_store_max_unified_mem: int | None = ...,
        gui_device_latitude: str | None = ...,
        gui_device_longitude: str | None = ...,
        private_data_encryption: Literal["disable", "enable"] | None = ...,
        auto_auth_extension_device: Literal["enable", "disable"] | None = ...,
        gui_theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "retro", "dark-matter", "onyx", "eclipse"] | None = ...,
        gui_date_format: Literal["yyyy/MM/dd", "dd/MM/yyyy", "MM/dd/yyyy", "yyyy-MM-dd", "dd-MM-yyyy", "MM-dd-yyyy"] | None = ...,
        gui_date_time_source: Literal["system", "browser"] | None = ...,
        igmp_state_limit: int | None = ...,
        cloud_communication: Literal["enable", "disable"] | None = ...,
        ipsec_ha_seqjump_rate: int | None = ...,
        fortitoken_cloud: Literal["enable", "disable"] | None = ...,
        fortitoken_cloud_push_status: Literal["enable", "disable"] | None = ...,
        fortitoken_cloud_region: str | None = ...,
        fortitoken_cloud_sync_interval: int | None = ...,
        faz_disk_buffer_size: int | None = ...,
        irq_time_accounting: Literal["auto", "force"] | None = ...,
        management_ip: str | None = ...,
        management_port: int | None = ...,
        management_port_use_admin_sport: Literal["enable", "disable"] | None = ...,
        forticonverter_integration: Literal["enable", "disable"] | None = ...,
        forticonverter_config_upload: Literal["once", "disable"] | None = ...,
        internet_service_database: Literal["mini", "standard", "full", "on-demand"] | None = ...,
        internet_service_download_list: str | list[str] | list[GlobalInternetservicedownloadlistItem] | None = ...,
        geoip_full_db: Literal["enable", "disable"] | None = ...,
        early_tcp_npu_session: Literal["enable", "disable"] | None = ...,
        npu_neighbor_update: Literal["enable", "disable"] | None = ...,
        delay_tcp_npu_session: Literal["enable", "disable"] | None = ...,
        interface_subnet_usage: Literal["disable", "enable"] | None = ...,
        sflowd_max_children_num: int | None = ...,
        fortigslb_integration: Literal["disable", "enable"] | None = ...,
        user_history_password_threshold: int | None = ...,
        auth_session_auto_backup: Literal["enable", "disable"] | None = ...,
        auth_session_auto_backup_interval: Literal["1min", "5min", "15min", "30min", "1hr"] | None = ...,
        scim_https_port: int | None = ...,
        scim_http_port: int | None = ...,
        scim_server_cert: str | None = ...,
        application_bandwidth_tracking: Literal["disable", "enable"] | None = ...,
        tls_session_cache: Literal["enable", "disable"] | None = ...,
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
    "Global",
    "GlobalPayload",
    "GlobalResponse",
    "GlobalObject",
]