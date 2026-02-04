""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/local_in_policy6
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

class LocalInPolicy6IntfItem(TypedDict, total=False):
    """Nested item for intf field."""
    name: str


class LocalInPolicy6SrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class LocalInPolicy6DstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class LocalInPolicy6Internetservice6srcnameItem(TypedDict, total=False):
    """Nested item for internet-service6-src-name field."""
    name: str


class LocalInPolicy6Internetservice6srcgroupItem(TypedDict, total=False):
    """Nested item for internet-service6-src-group field."""
    name: str


class LocalInPolicy6Internetservice6srccustomItem(TypedDict, total=False):
    """Nested item for internet-service6-src-custom field."""
    name: str


class LocalInPolicy6Internetservice6srccustomgroupItem(TypedDict, total=False):
    """Nested item for internet-service6-src-custom-group field."""
    name: str


class LocalInPolicy6Internetservice6srcfortiguardItem(TypedDict, total=False):
    """Nested item for internet-service6-src-fortiguard field."""
    name: str


class LocalInPolicy6ServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class LocalInPolicy6Payload(TypedDict, total=False):
    """Payload type for LocalInPolicy6 operations."""
    policyid: int
    uuid: str
    intf: str | list[str] | list[LocalInPolicy6IntfItem]
    srcaddr: str | list[str] | list[LocalInPolicy6SrcaddrItem]
    srcaddr_negate: Literal["enable", "disable"]
    dstaddr: str | list[str] | list[LocalInPolicy6DstaddrItem]
    internet_service6_src: Literal["enable", "disable"]
    internet_service6_src_name: str | list[str] | list[LocalInPolicy6Internetservice6srcnameItem]
    internet_service6_src_group: str | list[str] | list[LocalInPolicy6Internetservice6srcgroupItem]
    internet_service6_src_custom: str | list[str] | list[LocalInPolicy6Internetservice6srccustomItem]
    internet_service6_src_custom_group: str | list[str] | list[LocalInPolicy6Internetservice6srccustomgroupItem]
    internet_service6_src_fortiguard: str | list[str] | list[LocalInPolicy6Internetservice6srcfortiguardItem]
    dstaddr_negate: Literal["enable", "disable"]
    action: Literal["accept", "deny"]
    service: str | list[str] | list[LocalInPolicy6ServiceItem]
    service_negate: Literal["enable", "disable"]
    internet_service6_src_negate: Literal["enable", "disable"]
    schedule: str
    status: Literal["enable", "disable"]
    virtual_patch: Literal["enable", "disable"]
    logtraffic: Literal["enable", "disable"]
    comments: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LocalInPolicy6Response(TypedDict, total=False):
    """Response type for LocalInPolicy6 - use with .dict property for typed dict access."""
    policyid: int
    uuid: str
    intf: list[LocalInPolicy6IntfItem]
    srcaddr: list[LocalInPolicy6SrcaddrItem]
    srcaddr_negate: Literal["enable", "disable"]
    dstaddr: list[LocalInPolicy6DstaddrItem]
    internet_service6_src: Literal["enable", "disable"]
    internet_service6_src_name: list[LocalInPolicy6Internetservice6srcnameItem]
    internet_service6_src_group: list[LocalInPolicy6Internetservice6srcgroupItem]
    internet_service6_src_custom: list[LocalInPolicy6Internetservice6srccustomItem]
    internet_service6_src_custom_group: list[LocalInPolicy6Internetservice6srccustomgroupItem]
    internet_service6_src_fortiguard: list[LocalInPolicy6Internetservice6srcfortiguardItem]
    dstaddr_negate: Literal["enable", "disable"]
    action: Literal["accept", "deny"]
    service: list[LocalInPolicy6ServiceItem]
    service_negate: Literal["enable", "disable"]
    internet_service6_src_negate: Literal["enable", "disable"]
    schedule: str
    status: Literal["enable", "disable"]
    virtual_patch: Literal["enable", "disable"]
    logtraffic: Literal["enable", "disable"]
    comments: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LocalInPolicy6IntfItemObject(FortiObject[LocalInPolicy6IntfItem]):
    """Typed object for intf table items with attribute access."""
    name: str


class LocalInPolicy6SrcaddrItemObject(FortiObject[LocalInPolicy6SrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class LocalInPolicy6DstaddrItemObject(FortiObject[LocalInPolicy6DstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class LocalInPolicy6Internetservice6srcnameItemObject(FortiObject[LocalInPolicy6Internetservice6srcnameItem]):
    """Typed object for internet-service6-src-name table items with attribute access."""
    name: str


class LocalInPolicy6Internetservice6srcgroupItemObject(FortiObject[LocalInPolicy6Internetservice6srcgroupItem]):
    """Typed object for internet-service6-src-group table items with attribute access."""
    name: str


class LocalInPolicy6Internetservice6srccustomItemObject(FortiObject[LocalInPolicy6Internetservice6srccustomItem]):
    """Typed object for internet-service6-src-custom table items with attribute access."""
    name: str


class LocalInPolicy6Internetservice6srccustomgroupItemObject(FortiObject[LocalInPolicy6Internetservice6srccustomgroupItem]):
    """Typed object for internet-service6-src-custom-group table items with attribute access."""
    name: str


class LocalInPolicy6Internetservice6srcfortiguardItemObject(FortiObject[LocalInPolicy6Internetservice6srcfortiguardItem]):
    """Typed object for internet-service6-src-fortiguard table items with attribute access."""
    name: str


class LocalInPolicy6ServiceItemObject(FortiObject[LocalInPolicy6ServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class LocalInPolicy6Object(FortiObject):
    """Typed FortiObject for LocalInPolicy6 with field access."""
    policyid: int
    uuid: str
    intf: FortiObjectList[LocalInPolicy6IntfItemObject]
    srcaddr: FortiObjectList[LocalInPolicy6SrcaddrItemObject]
    srcaddr_negate: Literal["enable", "disable"]
    dstaddr: FortiObjectList[LocalInPolicy6DstaddrItemObject]
    internet_service6_src: Literal["enable", "disable"]
    internet_service6_src_name: FortiObjectList[LocalInPolicy6Internetservice6srcnameItemObject]
    internet_service6_src_group: FortiObjectList[LocalInPolicy6Internetservice6srcgroupItemObject]
    internet_service6_src_custom: FortiObjectList[LocalInPolicy6Internetservice6srccustomItemObject]
    internet_service6_src_custom_group: FortiObjectList[LocalInPolicy6Internetservice6srccustomgroupItemObject]
    internet_service6_src_fortiguard: FortiObjectList[LocalInPolicy6Internetservice6srcfortiguardItemObject]
    dstaddr_negate: Literal["enable", "disable"]
    action: Literal["accept", "deny"]
    service: FortiObjectList[LocalInPolicy6ServiceItemObject]
    service_negate: Literal["enable", "disable"]
    internet_service6_src_negate: Literal["enable", "disable"]
    schedule: str
    status: Literal["enable", "disable"]
    virtual_patch: Literal["enable", "disable"]
    logtraffic: Literal["enable", "disable"]
    comments: str


# ================================================================
# Main Endpoint Class
# ================================================================

class LocalInPolicy6:
    """
    
    Endpoint: firewall/local_in_policy6
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
    ) -> LocalInPolicy6Object: ...
    
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
    ) -> FortiObjectList[LocalInPolicy6Object]: ...
    
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
        payload_dict: LocalInPolicy6Payload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        intf: str | list[str] | list[LocalInPolicy6IntfItem] | None = ...,
        srcaddr: str | list[str] | list[LocalInPolicy6SrcaddrItem] | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr: str | list[str] | list[LocalInPolicy6DstaddrItem] | None = ...,
        internet_service6_src: Literal["enable", "disable"] | None = ...,
        internet_service6_src_name: str | list[str] | list[LocalInPolicy6Internetservice6srcnameItem] | None = ...,
        internet_service6_src_group: str | list[str] | list[LocalInPolicy6Internetservice6srcgroupItem] | None = ...,
        internet_service6_src_custom: str | list[str] | list[LocalInPolicy6Internetservice6srccustomItem] | None = ...,
        internet_service6_src_custom_group: str | list[str] | list[LocalInPolicy6Internetservice6srccustomgroupItem] | None = ...,
        internet_service6_src_fortiguard: str | list[str] | list[LocalInPolicy6Internetservice6srcfortiguardItem] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        service: str | list[str] | list[LocalInPolicy6ServiceItem] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_src_negate: Literal["enable", "disable"] | None = ...,
        schedule: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        virtual_patch: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocalInPolicy6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LocalInPolicy6Payload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        intf: str | list[str] | list[LocalInPolicy6IntfItem] | None = ...,
        srcaddr: str | list[str] | list[LocalInPolicy6SrcaddrItem] | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr: str | list[str] | list[LocalInPolicy6DstaddrItem] | None = ...,
        internet_service6_src: Literal["enable", "disable"] | None = ...,
        internet_service6_src_name: str | list[str] | list[LocalInPolicy6Internetservice6srcnameItem] | None = ...,
        internet_service6_src_group: str | list[str] | list[LocalInPolicy6Internetservice6srcgroupItem] | None = ...,
        internet_service6_src_custom: str | list[str] | list[LocalInPolicy6Internetservice6srccustomItem] | None = ...,
        internet_service6_src_custom_group: str | list[str] | list[LocalInPolicy6Internetservice6srccustomgroupItem] | None = ...,
        internet_service6_src_fortiguard: str | list[str] | list[LocalInPolicy6Internetservice6srcfortiguardItem] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        service: str | list[str] | list[LocalInPolicy6ServiceItem] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_src_negate: Literal["enable", "disable"] | None = ...,
        schedule: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        virtual_patch: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocalInPolicy6Object: ...

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
    # Action: Move
    # ================================================================
    
    def move(
        self,
        policyid: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_policyid: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
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
        payload_dict: LocalInPolicy6Payload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        intf: str | list[str] | list[LocalInPolicy6IntfItem] | None = ...,
        srcaddr: str | list[str] | list[LocalInPolicy6SrcaddrItem] | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr: str | list[str] | list[LocalInPolicy6DstaddrItem] | None = ...,
        internet_service6_src: Literal["enable", "disable"] | None = ...,
        internet_service6_src_name: str | list[str] | list[LocalInPolicy6Internetservice6srcnameItem] | None = ...,
        internet_service6_src_group: str | list[str] | list[LocalInPolicy6Internetservice6srcgroupItem] | None = ...,
        internet_service6_src_custom: str | list[str] | list[LocalInPolicy6Internetservice6srccustomItem] | None = ...,
        internet_service6_src_custom_group: str | list[str] | list[LocalInPolicy6Internetservice6srccustomgroupItem] | None = ...,
        internet_service6_src_fortiguard: str | list[str] | list[LocalInPolicy6Internetservice6srcfortiguardItem] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        service: str | list[str] | list[LocalInPolicy6ServiceItem] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        internet_service6_src_negate: Literal["enable", "disable"] | None = ...,
        schedule: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        virtual_patch: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
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
    "LocalInPolicy6",
    "LocalInPolicy6Payload",
    "LocalInPolicy6Response",
    "LocalInPolicy6Object",
]