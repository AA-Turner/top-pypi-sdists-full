""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/sniffer
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

class SnifferIpthreatfeedItem(TypedDict, total=False):
    """Nested item for ip-threatfeed field."""
    name: str


class SnifferAnomalyItem(TypedDict, total=False):
    """Nested item for anomaly field."""
    name: str
    status: Literal["disable", "enable"]
    log: Literal["enable", "disable"]
    action: Literal["pass", "block"]
    quarantine: Literal["none", "attacker"]
    quarantine_expiry: str
    quarantine_log: Literal["disable", "enable"]
    threshold: int
    threshold_default: int


class SnifferPayload(TypedDict, total=False):
    """Payload type for Sniffer operations."""
    id: int
    uuid: str
    status: Literal["enable", "disable"]
    logtraffic: Literal["all", "utm", "disable"]
    ipv6: Literal["enable", "disable"]
    non_ip: Literal["enable", "disable"]
    interface: str
    host: str
    port: str
    protocol: str
    vlan: str
    application_list_status: Literal["enable", "disable"]
    application_list: str
    ips_sensor_status: Literal["enable", "disable"]
    ips_sensor: str
    dsri: Literal["enable", "disable"]
    av_profile_status: Literal["enable", "disable"]
    av_profile: str
    webfilter_profile_status: Literal["enable", "disable"]
    webfilter_profile: str
    emailfilter_profile_status: Literal["enable", "disable"]
    emailfilter_profile: str
    dlp_profile_status: Literal["enable", "disable"]
    dlp_profile: str
    ip_threatfeed_status: Literal["enable", "disable"]
    ip_threatfeed: str | list[str] | list[SnifferIpthreatfeedItem]
    file_filter_profile_status: Literal["enable", "disable"]
    file_filter_profile: str
    ips_dos_status: Literal["enable", "disable"]
    anomaly: str | list[str] | list[SnifferAnomalyItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SnifferResponse(TypedDict, total=False):
    """Response type for Sniffer - use with .dict property for typed dict access."""
    id: int
    uuid: str
    status: Literal["enable", "disable"]
    logtraffic: Literal["all", "utm", "disable"]
    ipv6: Literal["enable", "disable"]
    non_ip: Literal["enable", "disable"]
    interface: str
    host: str
    port: str
    protocol: str
    vlan: str
    application_list_status: Literal["enable", "disable"]
    application_list: str
    ips_sensor_status: Literal["enable", "disable"]
    ips_sensor: str
    dsri: Literal["enable", "disable"]
    av_profile_status: Literal["enable", "disable"]
    av_profile: str
    webfilter_profile_status: Literal["enable", "disable"]
    webfilter_profile: str
    emailfilter_profile_status: Literal["enable", "disable"]
    emailfilter_profile: str
    dlp_profile_status: Literal["enable", "disable"]
    dlp_profile: str
    ip_threatfeed_status: Literal["enable", "disable"]
    ip_threatfeed: list[SnifferIpthreatfeedItem]
    file_filter_profile_status: Literal["enable", "disable"]
    file_filter_profile: str
    ips_dos_status: Literal["enable", "disable"]
    anomaly: list[SnifferAnomalyItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SnifferIpthreatfeedItemObject(FortiObject[SnifferIpthreatfeedItem]):
    """Typed object for ip-threatfeed table items with attribute access."""
    name: str


class SnifferAnomalyItemObject(FortiObject[SnifferAnomalyItem]):
    """Typed object for anomaly table items with attribute access."""
    name: str
    status: Literal["disable", "enable"]
    log: Literal["enable", "disable"]
    action: Literal["pass", "block"]
    quarantine: Literal["none", "attacker"]
    quarantine_expiry: str
    quarantine_log: Literal["disable", "enable"]
    threshold: int
    threshold_default: int


class SnifferObject(FortiObject):
    """Typed FortiObject for Sniffer with field access."""
    id: int
    uuid: str
    status: Literal["enable", "disable"]
    logtraffic: Literal["all", "utm", "disable"]
    ipv6: Literal["enable", "disable"]
    non_ip: Literal["enable", "disable"]
    interface: str
    host: str
    port: str
    protocol: str
    vlan: str
    application_list_status: Literal["enable", "disable"]
    application_list: str
    ips_sensor_status: Literal["enable", "disable"]
    ips_sensor: str
    dsri: Literal["enable", "disable"]
    av_profile_status: Literal["enable", "disable"]
    av_profile: str
    webfilter_profile_status: Literal["enable", "disable"]
    webfilter_profile: str
    emailfilter_profile_status: Literal["enable", "disable"]
    emailfilter_profile: str
    dlp_profile_status: Literal["enable", "disable"]
    dlp_profile: str
    ip_threatfeed_status: Literal["enable", "disable"]
    ip_threatfeed: FortiObjectList[SnifferIpthreatfeedItemObject]
    file_filter_profile_status: Literal["enable", "disable"]
    file_filter_profile: str
    ips_dos_status: Literal["enable", "disable"]
    anomaly: FortiObjectList[SnifferAnomalyItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Sniffer:
    """
    
    Endpoint: firewall/sniffer
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> SnifferObject: ...
    
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
    ) -> FortiObjectList[SnifferObject]: ...
    
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
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[SnifferIpthreatfeedItem] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[SnifferAnomalyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SnifferObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[SnifferIpthreatfeedItem] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[SnifferAnomalyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SnifferObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[SnifferIpthreatfeedItem] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[SnifferAnomalyItem] | None = ...,
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
    "Sniffer",
    "SnifferPayload",
    "SnifferResponse",
    "SnifferObject",
]