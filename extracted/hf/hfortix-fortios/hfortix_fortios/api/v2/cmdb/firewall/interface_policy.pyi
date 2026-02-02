""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/interface_policy
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

class InterfacePolicySrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class InterfacePolicyDstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class InterfacePolicyServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class InterfacePolicyPayload(TypedDict, total=False):
    """Payload type for InterfacePolicy operations."""
    policyid: int
    uuid: str
    status: Literal["enable", "disable"]
    comments: str
    logtraffic: Literal["all", "utm", "disable"]
    interface: str
    srcaddr: str | list[str] | list[InterfacePolicySrcaddrItem]
    dstaddr: str | list[str] | list[InterfacePolicyDstaddrItem]
    service: str | list[str] | list[InterfacePolicyServiceItem]
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

class InterfacePolicyResponse(TypedDict, total=False):
    """Response type for InterfacePolicy - use with .dict property for typed dict access."""
    policyid: int
    uuid: str
    status: Literal["enable", "disable"]
    comments: str
    logtraffic: Literal["all", "utm", "disable"]
    interface: str
    srcaddr: list[InterfacePolicySrcaddrItem]
    dstaddr: list[InterfacePolicyDstaddrItem]
    service: list[InterfacePolicyServiceItem]
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


class InterfacePolicySrcaddrItemObject(FortiObject[InterfacePolicySrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class InterfacePolicyDstaddrItemObject(FortiObject[InterfacePolicyDstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class InterfacePolicyServiceItemObject(FortiObject[InterfacePolicyServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class InterfacePolicyObject(FortiObject):
    """Typed FortiObject for InterfacePolicy with field access."""
    policyid: int
    uuid: str
    status: Literal["enable", "disable"]
    comments: str
    logtraffic: Literal["all", "utm", "disable"]
    interface: str
    srcaddr: FortiObjectList[InterfacePolicySrcaddrItemObject]
    dstaddr: FortiObjectList[InterfacePolicyDstaddrItemObject]
    service: FortiObjectList[InterfacePolicyServiceItemObject]
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

class InterfacePolicy:
    """
    
    Endpoint: firewall/interface_policy
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
    ) -> InterfacePolicyObject: ...
    
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
    ) -> FortiObjectList[InterfacePolicyObject]: ...
    
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
        payload_dict: InterfacePolicyPayload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        interface: str | None = ...,
        srcaddr: str | list[str] | list[InterfacePolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[InterfacePolicyDstaddrItem] | None = ...,
        service: str | list[str] | list[InterfacePolicyServiceItem] | None = ...,
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
    ) -> InterfacePolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InterfacePolicyPayload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        interface: str | None = ...,
        srcaddr: str | list[str] | list[InterfacePolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[InterfacePolicyDstaddrItem] | None = ...,
        service: str | list[str] | list[InterfacePolicyServiceItem] | None = ...,
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
    ) -> InterfacePolicyObject: ...

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
        payload_dict: InterfacePolicyPayload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        interface: str | None = ...,
        srcaddr: str | list[str] | list[InterfacePolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[InterfacePolicyDstaddrItem] | None = ...,
        service: str | list[str] | list[InterfacePolicyServiceItem] | None = ...,
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
    "InterfacePolicy",
    "InterfacePolicyPayload",
    "InterfacePolicyResponse",
    "InterfacePolicyObject",
]