""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/interface_policy6
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

class InterfacePolicy6Srcaddr6Item(TypedDict, total=False):
    """Nested item for srcaddr6 field."""
    name: str


class InterfacePolicy6Dstaddr6Item(TypedDict, total=False):
    """Nested item for dstaddr6 field."""
    name: str


class InterfacePolicy6Service6Item(TypedDict, total=False):
    """Nested item for service6 field."""
    name: str


class InterfacePolicy6Payload(TypedDict, total=False):
    """Payload type for InterfacePolicy6 operations."""
    policyid: int
    uuid: str
    status: Literal["enable", "disable"]
    comments: str
    logtraffic: Literal["all", "utm", "disable"]
    interface: str
    srcaddr6: str | list[str] | list[InterfacePolicy6Srcaddr6Item]
    dstaddr6: str | list[str] | list[InterfacePolicy6Dstaddr6Item]
    service6: str | list[str] | list[InterfacePolicy6Service6Item]
    application_list_status: Literal["enable", "disable"]
    application_list: str
    ips_sensor_status: Literal["enable", "disable"]
    ips_sensor: str
    dsri: Literal["enable", "disable"]
    av_profile_status: Literal["enable", "disable"]
    av_profile: str
    webfilter_profile_status: Literal["enable", "disable"]
    webfilter_profile: str
    casb_profile_status: Literal["enable", "disable"]
    casb_profile: str
    emailfilter_profile_status: Literal["enable", "disable"]
    emailfilter_profile: str
    dlp_profile_status: Literal["enable", "disable"]
    dlp_profile: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InterfacePolicy6Response(TypedDict, total=False):
    """Response type for InterfacePolicy6 - use with .dict property for typed dict access."""
    policyid: int
    uuid: str
    status: Literal["enable", "disable"]
    comments: str
    logtraffic: Literal["all", "utm", "disable"]
    interface: str
    srcaddr6: list[InterfacePolicy6Srcaddr6Item]
    dstaddr6: list[InterfacePolicy6Dstaddr6Item]
    service6: list[InterfacePolicy6Service6Item]
    application_list_status: Literal["enable", "disable"]
    application_list: str
    ips_sensor_status: Literal["enable", "disable"]
    ips_sensor: str
    dsri: Literal["enable", "disable"]
    av_profile_status: Literal["enable", "disable"]
    av_profile: str
    webfilter_profile_status: Literal["enable", "disable"]
    webfilter_profile: str
    casb_profile_status: Literal["enable", "disable"]
    casb_profile: str
    emailfilter_profile_status: Literal["enable", "disable"]
    emailfilter_profile: str
    dlp_profile_status: Literal["enable", "disable"]
    dlp_profile: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InterfacePolicy6Srcaddr6ItemObject(FortiObject[InterfacePolicy6Srcaddr6Item]):
    """Typed object for srcaddr6 table items with attribute access."""
    name: str


class InterfacePolicy6Dstaddr6ItemObject(FortiObject[InterfacePolicy6Dstaddr6Item]):
    """Typed object for dstaddr6 table items with attribute access."""
    name: str


class InterfacePolicy6Service6ItemObject(FortiObject[InterfacePolicy6Service6Item]):
    """Typed object for service6 table items with attribute access."""
    name: str


class InterfacePolicy6Object(FortiObject):
    """Typed FortiObject for InterfacePolicy6 with field access."""
    policyid: int
    uuid: str
    status: Literal["enable", "disable"]
    comments: str
    logtraffic: Literal["all", "utm", "disable"]
    interface: str
    srcaddr6: FortiObjectList[InterfacePolicy6Srcaddr6ItemObject]
    dstaddr6: FortiObjectList[InterfacePolicy6Dstaddr6ItemObject]
    service6: FortiObjectList[InterfacePolicy6Service6ItemObject]
    application_list_status: Literal["enable", "disable"]
    application_list: str
    ips_sensor_status: Literal["enable", "disable"]
    ips_sensor: str
    dsri: Literal["enable", "disable"]
    av_profile_status: Literal["enable", "disable"]
    av_profile: str
    webfilter_profile_status: Literal["enable", "disable"]
    webfilter_profile: str
    casb_profile_status: Literal["enable", "disable"]
    casb_profile: str
    emailfilter_profile_status: Literal["enable", "disable"]
    emailfilter_profile: str
    dlp_profile_status: Literal["enable", "disable"]
    dlp_profile: str


# ================================================================
# Main Endpoint Class
# ================================================================

class InterfacePolicy6:
    """
    
    Endpoint: firewall/interface_policy6
    Category: cmdb
    MKey: policyid
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
        policyid: int,
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
    ) -> InterfacePolicy6Object: ...
    
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
    ) -> FortiObjectList[InterfacePolicy6Object]: ...
    
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
        payload_dict: InterfacePolicy6Payload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        interface: str | None = ...,
        srcaddr6: str | list[str] | list[InterfacePolicy6Srcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[InterfacePolicy6Dstaddr6Item] | None = ...,
        service6: str | list[str] | list[InterfacePolicy6Service6Item] | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        casb_profile_status: Literal["enable", "disable"] | None = ...,
        casb_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfacePolicy6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InterfacePolicy6Payload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        interface: str | None = ...,
        srcaddr6: str | list[str] | list[InterfacePolicy6Srcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[InterfacePolicy6Dstaddr6Item] | None = ...,
        service6: str | list[str] | list[InterfacePolicy6Service6Item] | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        casb_profile_status: Literal["enable", "disable"] | None = ...,
        casb_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfacePolicy6Object: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        policyid: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        policyid: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InterfacePolicy6Payload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        interface: str | None = ...,
        srcaddr6: str | list[str] | list[InterfacePolicy6Srcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[InterfacePolicy6Dstaddr6Item] | None = ...,
        service6: str | list[str] | list[InterfacePolicy6Service6Item] | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        casb_profile_status: Literal["enable", "disable"] | None = ...,
        casb_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
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
    "InterfacePolicy6",
    "InterfacePolicy6Payload",
    "InterfacePolicy6Response",
    "InterfacePolicy6Object",
]