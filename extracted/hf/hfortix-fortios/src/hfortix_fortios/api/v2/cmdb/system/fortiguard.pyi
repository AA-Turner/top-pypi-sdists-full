""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/fortiguard
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

class FortiguardPayload(TypedDict, total=False):
    """Payload type for Fortiguard operations."""
    fortiguard_anycast: Literal["enable", "disable"]
    fortiguard_anycast_source: Literal["fortinet", "aws", "debug"]
    protocol: Literal["udp", "http", "https"]
    port: Literal["8888", "53", "80", "443"]
    load_balance_servers: int
    auto_join_forticloud: Literal["enable", "disable"]
    update_server_location: Literal["automatic", "usa", "eu"]
    sandbox_region: str
    sandbox_inline_scan: Literal["enable", "disable"]
    update_ffdb: Literal["enable", "disable"]
    update_uwdb: Literal["enable", "disable"]
    update_dldb: Literal["enable", "disable"]
    update_extdb: Literal["enable", "disable"]
    update_build_proxy: Literal["enable", "disable"]
    persistent_connection: Literal["enable", "disable"]
    vdom: str
    auto_firmware_upgrade: Literal["enable", "disable"]
    auto_firmware_upgrade_day: str | list[str]
    auto_firmware_upgrade_delay: int
    auto_firmware_upgrade_start_hour: int
    auto_firmware_upgrade_end_hour: int
    FDS_license_expiring_days: int
    subscribe_update_notification: Literal["enable", "disable"]
    antispam_force_off: Literal["enable", "disable"]
    antispam_cache: Literal["enable", "disable"]
    antispam_cache_ttl: int
    antispam_cache_mpermille: int
    antispam_license: int
    antispam_expiration: int
    antispam_timeout: int
    outbreak_prevention_force_off: Literal["enable", "disable"]
    outbreak_prevention_cache: Literal["enable", "disable"]
    outbreak_prevention_cache_ttl: int
    outbreak_prevention_cache_mpermille: int
    outbreak_prevention_license: int
    outbreak_prevention_expiration: int
    outbreak_prevention_timeout: int
    webfilter_force_off: Literal["enable", "disable"]
    webfilter_cache: Literal["enable", "disable"]
    webfilter_cache_ttl: int
    webfilter_license: int
    webfilter_expiration: int
    webfilter_timeout: int
    sdns_server_ip: str | list[str]
    sdns_server_port: int
    anycast_sdns_server_ip: str
    anycast_sdns_server_port: int
    sdns_options: str | list[str]
    source_ip: str
    source_ip6: str
    proxy_server_ip: str
    proxy_server_port: int
    proxy_username: str
    proxy_password: str
    ddns_server_ip: str
    ddns_server_ip6: str
    ddns_server_port: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FortiguardResponse(TypedDict, total=False):
    """Response type for Fortiguard - use with .dict property for typed dict access."""
    fortiguard_anycast: Literal["enable", "disable"]
    fortiguard_anycast_source: Literal["fortinet", "aws", "debug"]
    protocol: Literal["udp", "http", "https"]
    port: Literal["8888", "53", "80", "443"]
    load_balance_servers: int
    auto_join_forticloud: Literal["enable", "disable"]
    update_server_location: Literal["automatic", "usa", "eu"]
    sandbox_region: str
    sandbox_inline_scan: Literal["enable", "disable"]
    update_ffdb: Literal["enable", "disable"]
    update_uwdb: Literal["enable", "disable"]
    update_dldb: Literal["enable", "disable"]
    update_extdb: Literal["enable", "disable"]
    update_build_proxy: Literal["enable", "disable"]
    persistent_connection: Literal["enable", "disable"]
    vdom: str
    auto_firmware_upgrade: Literal["enable", "disable"]
    auto_firmware_upgrade_day: str
    auto_firmware_upgrade_delay: int
    auto_firmware_upgrade_start_hour: int
    auto_firmware_upgrade_end_hour: int
    FDS_license_expiring_days: int
    subscribe_update_notification: Literal["enable", "disable"]
    antispam_force_off: Literal["enable", "disable"]
    antispam_cache: Literal["enable", "disable"]
    antispam_cache_ttl: int
    antispam_cache_mpermille: int
    antispam_license: int
    antispam_expiration: int
    antispam_timeout: int
    outbreak_prevention_force_off: Literal["enable", "disable"]
    outbreak_prevention_cache: Literal["enable", "disable"]
    outbreak_prevention_cache_ttl: int
    outbreak_prevention_cache_mpermille: int
    outbreak_prevention_license: int
    outbreak_prevention_expiration: int
    outbreak_prevention_timeout: int
    webfilter_force_off: Literal["enable", "disable"]
    webfilter_cache: Literal["enable", "disable"]
    webfilter_cache_ttl: int
    webfilter_license: int
    webfilter_expiration: int
    webfilter_timeout: int
    sdns_server_ip: str | list[str]
    sdns_server_port: int
    anycast_sdns_server_ip: str
    anycast_sdns_server_port: int
    sdns_options: str
    source_ip: str
    source_ip6: str
    proxy_server_ip: str
    proxy_server_port: int
    proxy_username: str
    proxy_password: str
    ddns_server_ip: str
    ddns_server_ip6: str
    ddns_server_port: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FortiguardObject(FortiObject):
    """Typed FortiObject for Fortiguard with field access."""
    fortiguard_anycast: Literal["enable", "disable"]
    fortiguard_anycast_source: Literal["fortinet", "aws", "debug"]
    protocol: Literal["udp", "http", "https"]
    port: Literal["8888", "53", "80", "443"]
    load_balance_servers: int
    auto_join_forticloud: Literal["enable", "disable"]
    update_server_location: Literal["automatic", "usa", "eu"]
    sandbox_region: str
    sandbox_inline_scan: Literal["enable", "disable"]
    update_ffdb: Literal["enable", "disable"]
    update_uwdb: Literal["enable", "disable"]
    update_dldb: Literal["enable", "disable"]
    update_extdb: Literal["enable", "disable"]
    update_build_proxy: Literal["enable", "disable"]
    persistent_connection: Literal["enable", "disable"]
    auto_firmware_upgrade: Literal["enable", "disable"]
    auto_firmware_upgrade_day: str
    auto_firmware_upgrade_delay: int
    auto_firmware_upgrade_start_hour: int
    auto_firmware_upgrade_end_hour: int
    FDS_license_expiring_days: int
    subscribe_update_notification: Literal["enable", "disable"]
    antispam_force_off: Literal["enable", "disable"]
    antispam_cache: Literal["enable", "disable"]
    antispam_cache_ttl: int
    antispam_cache_mpermille: int
    antispam_license: int
    antispam_expiration: int
    antispam_timeout: int
    outbreak_prevention_force_off: Literal["enable", "disable"]
    outbreak_prevention_cache: Literal["enable", "disable"]
    outbreak_prevention_cache_ttl: int
    outbreak_prevention_cache_mpermille: int
    outbreak_prevention_license: int
    outbreak_prevention_expiration: int
    outbreak_prevention_timeout: int
    webfilter_force_off: Literal["enable", "disable"]
    webfilter_cache: Literal["enable", "disable"]
    webfilter_cache_ttl: int
    webfilter_license: int
    webfilter_expiration: int
    webfilter_timeout: int
    sdns_server_ip: str | list[str]
    sdns_server_port: int
    anycast_sdns_server_ip: str
    anycast_sdns_server_port: int
    sdns_options: str
    source_ip: str
    source_ip6: str
    proxy_server_ip: str
    proxy_server_port: int
    proxy_username: str
    proxy_password: str
    ddns_server_ip: str
    ddns_server_ip6: str
    ddns_server_port: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Fortiguard:
    """
    
    Endpoint: system/fortiguard
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
    ) -> FortiguardObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        fortiguard_anycast: Literal["enable", "disable"] | None = ...,
        fortiguard_anycast_source: Literal["fortinet", "aws", "debug"] | None = ...,
        protocol: Literal["udp", "http", "https"] | None = ...,
        port: Literal["8888", "53", "80", "443"] | None = ...,
        load_balance_servers: int | None = ...,
        auto_join_forticloud: Literal["enable", "disable"] | None = ...,
        update_server_location: Literal["automatic", "usa", "eu"] | None = ...,
        sandbox_region: str | None = ...,
        sandbox_inline_scan: Literal["enable", "disable"] | None = ...,
        update_ffdb: Literal["enable", "disable"] | None = ...,
        update_uwdb: Literal["enable", "disable"] | None = ...,
        update_dldb: Literal["enable", "disable"] | None = ...,
        update_extdb: Literal["enable", "disable"] | None = ...,
        update_build_proxy: Literal["enable", "disable"] | None = ...,
        persistent_connection: Literal["enable", "disable"] | None = ...,
        auto_firmware_upgrade: Literal["enable", "disable"] | None = ...,
        auto_firmware_upgrade_day: str | list[str] | None = ...,
        auto_firmware_upgrade_delay: int | None = ...,
        auto_firmware_upgrade_start_hour: int | None = ...,
        auto_firmware_upgrade_end_hour: int | None = ...,
        FDS_license_expiring_days: int | None = ...,
        subscribe_update_notification: Literal["enable", "disable"] | None = ...,
        antispam_force_off: Literal["enable", "disable"] | None = ...,
        antispam_cache: Literal["enable", "disable"] | None = ...,
        antispam_cache_ttl: int | None = ...,
        antispam_cache_mpermille: int | None = ...,
        antispam_license: int | None = ...,
        antispam_expiration: int | None = ...,
        antispam_timeout: int | None = ...,
        outbreak_prevention_force_off: Literal["enable", "disable"] | None = ...,
        outbreak_prevention_cache: Literal["enable", "disable"] | None = ...,
        outbreak_prevention_cache_ttl: int | None = ...,
        outbreak_prevention_cache_mpermille: int | None = ...,
        outbreak_prevention_license: int | None = ...,
        outbreak_prevention_expiration: int | None = ...,
        outbreak_prevention_timeout: int | None = ...,
        webfilter_force_off: Literal["enable", "disable"] | None = ...,
        webfilter_cache: Literal["enable", "disable"] | None = ...,
        webfilter_cache_ttl: int | None = ...,
        webfilter_license: int | None = ...,
        webfilter_expiration: int | None = ...,
        webfilter_timeout: int | None = ...,
        sdns_server_ip: str | list[str] | None = ...,
        sdns_server_port: int | None = ...,
        anycast_sdns_server_ip: str | None = ...,
        anycast_sdns_server_port: int | None = ...,
        sdns_options: str | list[str] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        proxy_server_ip: str | None = ...,
        proxy_server_port: int | None = ...,
        proxy_username: str | None = ...,
        proxy_password: str | None = ...,
        ddns_server_ip: str | None = ...,
        ddns_server_ip6: str | None = ...,
        ddns_server_port: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiguardObject: ...


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
        payload_dict: FortiguardPayload | None = ...,
        fortiguard_anycast: Literal["enable", "disable"] | None = ...,
        fortiguard_anycast_source: Literal["fortinet", "aws", "debug"] | None = ...,
        protocol: Literal["udp", "http", "https"] | None = ...,
        port: Literal["8888", "53", "80", "443"] | None = ...,
        load_balance_servers: int | None = ...,
        auto_join_forticloud: Literal["enable", "disable"] | None = ...,
        update_server_location: Literal["automatic", "usa", "eu"] | None = ...,
        sandbox_region: str | None = ...,
        sandbox_inline_scan: Literal["enable", "disable"] | None = ...,
        update_ffdb: Literal["enable", "disable"] | None = ...,
        update_uwdb: Literal["enable", "disable"] | None = ...,
        update_dldb: Literal["enable", "disable"] | None = ...,
        update_extdb: Literal["enable", "disable"] | None = ...,
        update_build_proxy: Literal["enable", "disable"] | None = ...,
        persistent_connection: Literal["enable", "disable"] | None = ...,
        auto_firmware_upgrade: Literal["enable", "disable"] | None = ...,
        auto_firmware_upgrade_day: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | list[str] | None = ...,
        auto_firmware_upgrade_delay: int | None = ...,
        auto_firmware_upgrade_start_hour: int | None = ...,
        auto_firmware_upgrade_end_hour: int | None = ...,
        FDS_license_expiring_days: int | None = ...,
        subscribe_update_notification: Literal["enable", "disable"] | None = ...,
        antispam_force_off: Literal["enable", "disable"] | None = ...,
        antispam_cache: Literal["enable", "disable"] | None = ...,
        antispam_cache_ttl: int | None = ...,
        antispam_cache_mpermille: int | None = ...,
        antispam_license: int | None = ...,
        antispam_expiration: int | None = ...,
        antispam_timeout: int | None = ...,
        outbreak_prevention_force_off: Literal["enable", "disable"] | None = ...,
        outbreak_prevention_cache: Literal["enable", "disable"] | None = ...,
        outbreak_prevention_cache_ttl: int | None = ...,
        outbreak_prevention_cache_mpermille: int | None = ...,
        outbreak_prevention_license: int | None = ...,
        outbreak_prevention_expiration: int | None = ...,
        outbreak_prevention_timeout: int | None = ...,
        webfilter_force_off: Literal["enable", "disable"] | None = ...,
        webfilter_cache: Literal["enable", "disable"] | None = ...,
        webfilter_cache_ttl: int | None = ...,
        webfilter_license: int | None = ...,
        webfilter_expiration: int | None = ...,
        webfilter_timeout: int | None = ...,
        sdns_server_ip: str | list[str] | None = ...,
        sdns_server_port: int | None = ...,
        anycast_sdns_server_ip: str | None = ...,
        anycast_sdns_server_port: int | None = ...,
        sdns_options: Literal["include-question-section"] | list[str] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        proxy_server_ip: str | None = ...,
        proxy_server_port: int | None = ...,
        proxy_username: str | None = ...,
        proxy_password: str | None = ...,
        ddns_server_ip: str | None = ...,
        ddns_server_ip6: str | None = ...,
        ddns_server_port: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
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
    "Fortiguard",
    "FortiguardPayload",
    "FortiguardResponse",
    "FortiguardObject",
]