""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ha
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

class HaVclusterVdomItem(TypedDict, total=False):
    """Nested item for vcluster.vdom field."""
    name: str


class HaAutovirtualmacinterfaceItem(TypedDict, total=False):
    """Nested item for auto-virtual-mac-interface field."""
    interface_name: str


class HaBackuphbdevItem(TypedDict, total=False):
    """Nested item for backup-hbdev field."""
    name: str


class HaHamgmtinterfacesItem(TypedDict, total=False):
    """Nested item for ha-mgmt-interfaces field."""
    id: int
    interface: str
    dst: str
    gateway: str
    dst6: str
    gateway6: str


class HaUnicastpeersItem(TypedDict, total=False):
    """Nested item for unicast-peers field."""
    id: int
    peer_ip: str


class HaVclusterItem(TypedDict, total=False):
    """Nested item for vcluster field."""
    vcluster_id: int
    override: Literal["enable", "disable"]
    priority: int
    override_wait_time: int
    monitor: str | list[str]
    pingserver_monitor_interface: str | list[str]
    pingserver_failover_threshold: int
    pingserver_secondary_force_reset: Literal["enable", "disable"]
    pingserver_flip_timeout: int
    vdom: str | list[str] | list[HaVclusterVdomItem]


class HaPayload(TypedDict, total=False):
    """Payload type for Ha operations."""
    group_id: int
    group_name: str
    mode: Literal["standalone", "a-a", "a-p"]
    sync_packet_balance: Literal["enable", "disable"]
    password: str
    key: str
    hbdev: str | list[str]
    auto_virtual_mac_interface: str | list[str] | list[HaAutovirtualmacinterfaceItem]
    backup_hbdev: str | list[str] | list[HaBackuphbdevItem]
    unicast_hb: Literal["enable", "disable"]
    unicast_hb_peerip: str
    unicast_hb_netmask: str
    session_sync_dev: str | list[str]
    route_ttl: int
    route_wait: int
    route_hold: int
    multicast_ttl: int
    evpn_ttl: int
    load_balance_all: Literal["enable", "disable"]
    sync_config: Literal["enable", "disable"]
    encryption: Literal["enable", "disable"]
    authentication: Literal["enable", "disable"]
    hb_interval: int
    hb_interval_in_milliseconds: Literal["100ms", "10ms"]
    hb_lost_threshold: int
    hello_holddown: int
    gratuitous_arps: Literal["enable", "disable"]
    arps: int
    arps_interval: int
    session_pickup: Literal["enable", "disable"]
    session_pickup_connectionless: Literal["enable", "disable"]
    session_pickup_expectation: Literal["enable", "disable"]
    session_pickup_nat: Literal["enable", "disable"]
    session_pickup_delay: Literal["enable", "disable"]
    link_failed_signal: Literal["enable", "disable"]
    upgrade_mode: Literal["simultaneous", "uninterruptible", "local-only", "secondary-only"]
    uninterruptible_primary_wait: int
    standalone_mgmt_vdom: Literal["enable", "disable"]
    ha_mgmt_status: Literal["enable", "disable"]
    ha_mgmt_interfaces: str | list[str] | list[HaHamgmtinterfacesItem]
    ha_eth_type: str
    hc_eth_type: str
    l2ep_eth_type: str
    ha_uptime_diff_margin: int
    standalone_config_sync: Literal["enable", "disable"]
    unicast_status: Literal["enable", "disable"]
    unicast_gateway: str
    unicast_peers: str | list[str] | list[HaUnicastpeersItem]
    schedule: Literal["none", "leastconnection", "round-robin", "weight-round-robin", "random", "ip", "ipport"]
    weight: str
    cpu_threshold: str
    memory_threshold: str
    http_proxy_threshold: str
    ftp_proxy_threshold: str
    imap_proxy_threshold: str
    nntp_proxy_threshold: str
    pop3_proxy_threshold: str
    smtp_proxy_threshold: str
    override: Literal["enable", "disable"]
    priority: int
    override_wait_time: int
    monitor: str | list[str]
    pingserver_monitor_interface: str | list[str]
    pingserver_failover_threshold: int
    pingserver_secondary_force_reset: Literal["enable", "disable"]
    pingserver_flip_timeout: int
    vcluster_status: Literal["enable", "disable"]
    vcluster: str | list[str] | list[HaVclusterItem]
    ha_direct: Literal["enable", "disable"]
    ssd_failover: Literal["enable", "disable"]
    memory_compatible_mode: Literal["enable", "disable"]
    memory_based_failover: Literal["enable", "disable"]
    memory_failover_threshold: int
    memory_failover_monitor_period: int
    memory_failover_sample_rate: int
    memory_failover_flip_timeout: int
    failover_hold_time: int
    check_secondary_dev_health: Literal["enable", "disable"]
    ipsec_phase2_proposal: str | list[str]
    bounce_intf_upon_failover: Literal["enable", "disable"]
    status: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class HaResponse(TypedDict, total=False):
    """Response type for Ha - use with .dict property for typed dict access."""
    group_id: int
    group_name: str
    mode: Literal["standalone", "a-a", "a-p"]
    sync_packet_balance: Literal["enable", "disable"]
    password: str
    key: str
    hbdev: str | list[str]
    auto_virtual_mac_interface: list[HaAutovirtualmacinterfaceItem]
    backup_hbdev: list[HaBackuphbdevItem]
    unicast_hb: Literal["enable", "disable"]
    unicast_hb_peerip: str
    unicast_hb_netmask: str
    session_sync_dev: str | list[str]
    route_ttl: int
    route_wait: int
    route_hold: int
    multicast_ttl: int
    evpn_ttl: int
    load_balance_all: Literal["enable", "disable"]
    sync_config: Literal["enable", "disable"]
    encryption: Literal["enable", "disable"]
    authentication: Literal["enable", "disable"]
    hb_interval: int
    hb_interval_in_milliseconds: Literal["100ms", "10ms"]
    hb_lost_threshold: int
    hello_holddown: int
    gratuitous_arps: Literal["enable", "disable"]
    arps: int
    arps_interval: int
    session_pickup: Literal["enable", "disable"]
    session_pickup_connectionless: Literal["enable", "disable"]
    session_pickup_expectation: Literal["enable", "disable"]
    session_pickup_nat: Literal["enable", "disable"]
    session_pickup_delay: Literal["enable", "disable"]
    link_failed_signal: Literal["enable", "disable"]
    upgrade_mode: Literal["simultaneous", "uninterruptible", "local-only", "secondary-only"]
    uninterruptible_primary_wait: int
    standalone_mgmt_vdom: Literal["enable", "disable"]
    ha_mgmt_status: Literal["enable", "disable"]
    ha_mgmt_interfaces: list[HaHamgmtinterfacesItem]
    ha_eth_type: str
    hc_eth_type: str
    l2ep_eth_type: str
    ha_uptime_diff_margin: int
    standalone_config_sync: Literal["enable", "disable"]
    unicast_status: Literal["enable", "disable"]
    unicast_gateway: str
    unicast_peers: list[HaUnicastpeersItem]
    schedule: Literal["none", "leastconnection", "round-robin", "weight-round-robin", "random", "ip", "ipport"]
    weight: str
    cpu_threshold: str
    memory_threshold: str
    http_proxy_threshold: str
    ftp_proxy_threshold: str
    imap_proxy_threshold: str
    nntp_proxy_threshold: str
    pop3_proxy_threshold: str
    smtp_proxy_threshold: str
    override: Literal["enable", "disable"]
    priority: int
    override_wait_time: int
    monitor: str | list[str]
    pingserver_monitor_interface: str | list[str]
    pingserver_failover_threshold: int
    pingserver_secondary_force_reset: Literal["enable", "disable"]
    pingserver_flip_timeout: int
    vcluster_status: Literal["enable", "disable"]
    vcluster: list[HaVclusterItem]
    ha_direct: Literal["enable", "disable"]
    ssd_failover: Literal["enable", "disable"]
    memory_compatible_mode: Literal["enable", "disable"]
    memory_based_failover: Literal["enable", "disable"]
    memory_failover_threshold: int
    memory_failover_monitor_period: int
    memory_failover_sample_rate: int
    memory_failover_flip_timeout: int
    failover_hold_time: int
    check_secondary_dev_health: Literal["enable", "disable"]
    ipsec_phase2_proposal: str
    bounce_intf_upon_failover: Literal["enable", "disable"]
    status: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class HaVclusterVdomItemObject(FortiObject[HaVclusterVdomItem]):
    """Typed object for vcluster.vdom table items with attribute access."""
    name: str


class HaAutovirtualmacinterfaceItemObject(FortiObject[HaAutovirtualmacinterfaceItem]):
    """Typed object for auto-virtual-mac-interface table items with attribute access."""
    interface_name: str


class HaBackuphbdevItemObject(FortiObject[HaBackuphbdevItem]):
    """Typed object for backup-hbdev table items with attribute access."""
    name: str


class HaHamgmtinterfacesItemObject(FortiObject[HaHamgmtinterfacesItem]):
    """Typed object for ha-mgmt-interfaces table items with attribute access."""
    id: int
    interface: str
    dst: str
    gateway: str
    dst6: str
    gateway6: str


class HaUnicastpeersItemObject(FortiObject[HaUnicastpeersItem]):
    """Typed object for unicast-peers table items with attribute access."""
    id: int
    peer_ip: str


class HaVclusterItemObject(FortiObject[HaVclusterItem]):
    """Typed object for vcluster table items with attribute access."""
    vcluster_id: int
    override: Literal["enable", "disable"]
    priority: int
    override_wait_time: int
    monitor: str | list[str]
    pingserver_monitor_interface: str | list[str]
    pingserver_failover_threshold: int
    pingserver_secondary_force_reset: Literal["enable", "disable"]
    pingserver_flip_timeout: int
    vdom: FortiObjectList[HaVclusterVdomItemObject]


class HaObject(FortiObject):
    """Typed FortiObject for Ha with field access."""
    group_id: int
    group_name: str
    mode: Literal["standalone", "a-a", "a-p"]
    sync_packet_balance: Literal["enable", "disable"]
    password: str
    key: str
    hbdev: str | list[str]
    auto_virtual_mac_interface: FortiObjectList[HaAutovirtualmacinterfaceItemObject]
    backup_hbdev: FortiObjectList[HaBackuphbdevItemObject]
    unicast_hb: Literal["enable", "disable"]
    unicast_hb_peerip: str
    unicast_hb_netmask: str
    session_sync_dev: str | list[str]
    route_ttl: int
    route_wait: int
    route_hold: int
    multicast_ttl: int
    evpn_ttl: int
    load_balance_all: Literal["enable", "disable"]
    sync_config: Literal["enable", "disable"]
    encryption: Literal["enable", "disable"]
    authentication: Literal["enable", "disable"]
    hb_interval: int
    hb_interval_in_milliseconds: Literal["100ms", "10ms"]
    hb_lost_threshold: int
    hello_holddown: int
    gratuitous_arps: Literal["enable", "disable"]
    arps: int
    arps_interval: int
    session_pickup: Literal["enable", "disable"]
    session_pickup_connectionless: Literal["enable", "disable"]
    session_pickup_expectation: Literal["enable", "disable"]
    session_pickup_nat: Literal["enable", "disable"]
    session_pickup_delay: Literal["enable", "disable"]
    link_failed_signal: Literal["enable", "disable"]
    upgrade_mode: Literal["simultaneous", "uninterruptible", "local-only", "secondary-only"]
    uninterruptible_primary_wait: int
    standalone_mgmt_vdom: Literal["enable", "disable"]
    ha_mgmt_status: Literal["enable", "disable"]
    ha_mgmt_interfaces: FortiObjectList[HaHamgmtinterfacesItemObject]
    ha_eth_type: str
    hc_eth_type: str
    l2ep_eth_type: str
    ha_uptime_diff_margin: int
    standalone_config_sync: Literal["enable", "disable"]
    unicast_status: Literal["enable", "disable"]
    unicast_gateway: str
    unicast_peers: FortiObjectList[HaUnicastpeersItemObject]
    schedule: Literal["none", "leastconnection", "round-robin", "weight-round-robin", "random", "ip", "ipport"]
    weight: str
    cpu_threshold: str
    memory_threshold: str
    http_proxy_threshold: str
    ftp_proxy_threshold: str
    imap_proxy_threshold: str
    nntp_proxy_threshold: str
    pop3_proxy_threshold: str
    smtp_proxy_threshold: str
    override: Literal["enable", "disable"]
    priority: int
    override_wait_time: int
    monitor: str | list[str]
    pingserver_monitor_interface: str | list[str]
    pingserver_failover_threshold: int
    pingserver_secondary_force_reset: Literal["enable", "disable"]
    pingserver_flip_timeout: int
    vcluster_status: Literal["enable", "disable"]
    vcluster: FortiObjectList[HaVclusterItemObject]
    ha_direct: Literal["enable", "disable"]
    ssd_failover: Literal["enable", "disable"]
    memory_compatible_mode: Literal["enable", "disable"]
    memory_based_failover: Literal["enable", "disable"]
    memory_failover_threshold: int
    memory_failover_monitor_period: int
    memory_failover_sample_rate: int
    memory_failover_flip_timeout: int
    failover_hold_time: int
    check_secondary_dev_health: Literal["enable", "disable"]
    ipsec_phase2_proposal: str
    bounce_intf_upon_failover: Literal["enable", "disable"]
    status: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Ha:
    """
    
    Endpoint: system/ha
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
    ) -> HaObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: HaPayload | None = ...,
        group_id: int | None = ...,
        group_name: str | None = ...,
        mode: Literal["standalone", "a-a", "a-p"] | None = ...,
        sync_packet_balance: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        key: str | None = ...,
        hbdev: str | list[str] | None = ...,
        auto_virtual_mac_interface: str | list[str] | list[HaAutovirtualmacinterfaceItem] | None = ...,
        backup_hbdev: str | list[str] | list[HaBackuphbdevItem] | None = ...,
        unicast_hb: Literal["enable", "disable"] | None = ...,
        unicast_hb_peerip: str | None = ...,
        unicast_hb_netmask: str | None = ...,
        session_sync_dev: str | list[str] | None = ...,
        route_ttl: int | None = ...,
        route_wait: int | None = ...,
        route_hold: int | None = ...,
        multicast_ttl: int | None = ...,
        evpn_ttl: int | None = ...,
        load_balance_all: Literal["enable", "disable"] | None = ...,
        sync_config: Literal["enable", "disable"] | None = ...,
        encryption: Literal["enable", "disable"] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        hb_interval: int | None = ...,
        hb_interval_in_milliseconds: Literal["100ms", "10ms"] | None = ...,
        hb_lost_threshold: int | None = ...,
        hello_holddown: int | None = ...,
        gratuitous_arps: Literal["enable", "disable"] | None = ...,
        arps: int | None = ...,
        arps_interval: int | None = ...,
        session_pickup: Literal["enable", "disable"] | None = ...,
        session_pickup_connectionless: Literal["enable", "disable"] | None = ...,
        session_pickup_expectation: Literal["enable", "disable"] | None = ...,
        session_pickup_nat: Literal["enable", "disable"] | None = ...,
        session_pickup_delay: Literal["enable", "disable"] | None = ...,
        link_failed_signal: Literal["enable", "disable"] | None = ...,
        upgrade_mode: Literal["simultaneous", "uninterruptible", "local-only", "secondary-only"] | None = ...,
        uninterruptible_primary_wait: int | None = ...,
        standalone_mgmt_vdom: Literal["enable", "disable"] | None = ...,
        ha_mgmt_status: Literal["enable", "disable"] | None = ...,
        ha_mgmt_interfaces: str | list[str] | list[HaHamgmtinterfacesItem] | None = ...,
        ha_eth_type: str | None = ...,
        hc_eth_type: str | None = ...,
        l2ep_eth_type: str | None = ...,
        ha_uptime_diff_margin: int | None = ...,
        standalone_config_sync: Literal["enable", "disable"] | None = ...,
        unicast_status: Literal["enable", "disable"] | None = ...,
        unicast_gateway: str | None = ...,
        unicast_peers: str | list[str] | list[HaUnicastpeersItem] | None = ...,
        schedule: Literal["none", "leastconnection", "round-robin", "weight-round-robin", "random", "ip", "ipport"] | None = ...,
        weight: str | None = ...,
        cpu_threshold: str | None = ...,
        memory_threshold: str | None = ...,
        http_proxy_threshold: str | None = ...,
        ftp_proxy_threshold: str | None = ...,
        imap_proxy_threshold: str | None = ...,
        nntp_proxy_threshold: str | None = ...,
        pop3_proxy_threshold: str | None = ...,
        smtp_proxy_threshold: str | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        priority: int | None = ...,
        override_wait_time: int | None = ...,
        monitor: str | list[str] | None = ...,
        pingserver_monitor_interface: str | list[str] | None = ...,
        pingserver_failover_threshold: int | None = ...,
        pingserver_secondary_force_reset: Literal["enable", "disable"] | None = ...,
        pingserver_flip_timeout: int | None = ...,
        vcluster_status: Literal["enable", "disable"] | None = ...,
        vcluster: str | list[str] | list[HaVclusterItem] | None = ...,
        ha_direct: Literal["enable", "disable"] | None = ...,
        ssd_failover: Literal["enable", "disable"] | None = ...,
        memory_compatible_mode: Literal["enable", "disable"] | None = ...,
        memory_based_failover: Literal["enable", "disable"] | None = ...,
        memory_failover_threshold: int | None = ...,
        memory_failover_monitor_period: int | None = ...,
        memory_failover_sample_rate: int | None = ...,
        memory_failover_flip_timeout: int | None = ...,
        failover_hold_time: int | None = ...,
        check_secondary_dev_health: Literal["enable", "disable"] | None = ...,
        ipsec_phase2_proposal: str | list[str] | None = ...,
        bounce_intf_upon_failover: Literal["enable", "disable"] | None = ...,
        status: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> HaObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: HaPayload | None = ...,
        group_id: int | None = ...,
        group_name: str | None = ...,
        mode: Literal["standalone", "a-a", "a-p"] | None = ...,
        sync_packet_balance: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        key: str | None = ...,
        hbdev: str | list[str] | None = ...,
        auto_virtual_mac_interface: str | list[str] | list[HaAutovirtualmacinterfaceItem] | None = ...,
        backup_hbdev: str | list[str] | list[HaBackuphbdevItem] | None = ...,
        unicast_hb: Literal["enable", "disable"] | None = ...,
        unicast_hb_peerip: str | None = ...,
        unicast_hb_netmask: str | None = ...,
        session_sync_dev: str | list[str] | None = ...,
        route_ttl: int | None = ...,
        route_wait: int | None = ...,
        route_hold: int | None = ...,
        multicast_ttl: int | None = ...,
        evpn_ttl: int | None = ...,
        load_balance_all: Literal["enable", "disable"] | None = ...,
        sync_config: Literal["enable", "disable"] | None = ...,
        encryption: Literal["enable", "disable"] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        hb_interval: int | None = ...,
        hb_interval_in_milliseconds: Literal["100ms", "10ms"] | None = ...,
        hb_lost_threshold: int | None = ...,
        hello_holddown: int | None = ...,
        gratuitous_arps: Literal["enable", "disable"] | None = ...,
        arps: int | None = ...,
        arps_interval: int | None = ...,
        session_pickup: Literal["enable", "disable"] | None = ...,
        session_pickup_connectionless: Literal["enable", "disable"] | None = ...,
        session_pickup_expectation: Literal["enable", "disable"] | None = ...,
        session_pickup_nat: Literal["enable", "disable"] | None = ...,
        session_pickup_delay: Literal["enable", "disable"] | None = ...,
        link_failed_signal: Literal["enable", "disable"] | None = ...,
        upgrade_mode: Literal["simultaneous", "uninterruptible", "local-only", "secondary-only"] | None = ...,
        uninterruptible_primary_wait: int | None = ...,
        standalone_mgmt_vdom: Literal["enable", "disable"] | None = ...,
        ha_mgmt_status: Literal["enable", "disable"] | None = ...,
        ha_mgmt_interfaces: str | list[str] | list[HaHamgmtinterfacesItem] | None = ...,
        ha_eth_type: str | None = ...,
        hc_eth_type: str | None = ...,
        l2ep_eth_type: str | None = ...,
        ha_uptime_diff_margin: int | None = ...,
        standalone_config_sync: Literal["enable", "disable"] | None = ...,
        unicast_status: Literal["enable", "disable"] | None = ...,
        unicast_gateway: str | None = ...,
        unicast_peers: str | list[str] | list[HaUnicastpeersItem] | None = ...,
        schedule: Literal["none", "leastconnection", "round-robin", "weight-round-robin", "random", "ip", "ipport"] | None = ...,
        weight: str | None = ...,
        cpu_threshold: str | None = ...,
        memory_threshold: str | None = ...,
        http_proxy_threshold: str | None = ...,
        ftp_proxy_threshold: str | None = ...,
        imap_proxy_threshold: str | None = ...,
        nntp_proxy_threshold: str | None = ...,
        pop3_proxy_threshold: str | None = ...,
        smtp_proxy_threshold: str | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        priority: int | None = ...,
        override_wait_time: int | None = ...,
        monitor: str | list[str] | None = ...,
        pingserver_monitor_interface: str | list[str] | None = ...,
        pingserver_failover_threshold: int | None = ...,
        pingserver_secondary_force_reset: Literal["enable", "disable"] | None = ...,
        pingserver_flip_timeout: int | None = ...,
        vcluster_status: Literal["enable", "disable"] | None = ...,
        vcluster: str | list[str] | list[HaVclusterItem] | None = ...,
        ha_direct: Literal["enable", "disable"] | None = ...,
        ssd_failover: Literal["enable", "disable"] | None = ...,
        memory_compatible_mode: Literal["enable", "disable"] | None = ...,
        memory_based_failover: Literal["enable", "disable"] | None = ...,
        memory_failover_threshold: int | None = ...,
        memory_failover_monitor_period: int | None = ...,
        memory_failover_sample_rate: int | None = ...,
        memory_failover_flip_timeout: int | None = ...,
        failover_hold_time: int | None = ...,
        check_secondary_dev_health: Literal["enable", "disable"] | None = ...,
        ipsec_phase2_proposal: Literal["aes128-sha1", "aes128-sha256", "aes128-sha384", "aes128-sha512", "aes192-sha1", "aes192-sha256", "aes192-sha384", "aes192-sha512", "aes256-sha1", "aes256-sha256", "aes256-sha384", "aes256-sha512", "aes128gcm", "aes256gcm", "chacha20poly1305"] | list[str] | None = ...,
        bounce_intf_upon_failover: Literal["enable", "disable"] | None = ...,
        status: str | None = ...,
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
    "Ha",
    "HaPayload",
    "HaResponse",
    "HaObject",
]