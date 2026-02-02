""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/local_in_policy
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

class LocalInPolicyIntfItem(TypedDict, total=False):
    """Nested item for intf field."""
    name: str


class LocalInPolicySrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class LocalInPolicyDstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class LocalInPolicyInternetservicesrcnameItem(TypedDict, total=False):
    """Nested item for internet-service-src-name field."""
    name: str


class LocalInPolicyInternetservicesrcgroupItem(TypedDict, total=False):
    """Nested item for internet-service-src-group field."""
    name: str


class LocalInPolicyInternetservicesrccustomItem(TypedDict, total=False):
    """Nested item for internet-service-src-custom field."""
    name: str


class LocalInPolicyInternetservicesrccustomgroupItem(TypedDict, total=False):
    """Nested item for internet-service-src-custom-group field."""
    name: str


class LocalInPolicyInternetservicesrcfortiguardItem(TypedDict, total=False):
    """Nested item for internet-service-src-fortiguard field."""
    name: str


class LocalInPolicyServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class LocalInPolicyPayload(TypedDict, total=False):
    """Payload type for LocalInPolicy operations."""
    policyid: int
    uuid: str
    ha_mgmt_intf_only: Literal["enable", "disable"]
    intf: str | list[str] | list[LocalInPolicyIntfItem]
    srcaddr: str | list[str] | list[LocalInPolicySrcaddrItem]
    srcaddr_negate: Literal["enable", "disable"]
    dstaddr: str | list[str] | list[LocalInPolicyDstaddrItem]
    internet_service_src: Literal["enable", "disable"]
    internet_service_src_name: str | list[str] | list[LocalInPolicyInternetservicesrcnameItem]
    internet_service_src_group: str | list[str] | list[LocalInPolicyInternetservicesrcgroupItem]
    internet_service_src_custom: str | list[str] | list[LocalInPolicyInternetservicesrccustomItem]
    internet_service_src_custom_group: str | list[str] | list[LocalInPolicyInternetservicesrccustomgroupItem]
    internet_service_src_fortiguard: str | list[str] | list[LocalInPolicyInternetservicesrcfortiguardItem]
    dstaddr_negate: Literal["enable", "disable"]
    action: Literal["accept", "deny"]
    service: str | list[str] | list[LocalInPolicyServiceItem]
    service_negate: Literal["enable", "disable"]
    internet_service_src_negate: Literal["enable", "disable"]
    schedule: str
    status: Literal["enable", "disable"]
    virtual_patch: Literal["enable", "disable"]
    logtraffic: Literal["enable", "disable"]
    comments: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LocalInPolicyResponse(TypedDict, total=False):
    """Response type for LocalInPolicy - use with .dict property for typed dict access."""
    policyid: int
    uuid: str
    ha_mgmt_intf_only: Literal["enable", "disable"]
    intf: list[LocalInPolicyIntfItem]
    srcaddr: list[LocalInPolicySrcaddrItem]
    srcaddr_negate: Literal["enable", "disable"]
    dstaddr: list[LocalInPolicyDstaddrItem]
    internet_service_src: Literal["enable", "disable"]
    internet_service_src_name: list[LocalInPolicyInternetservicesrcnameItem]
    internet_service_src_group: list[LocalInPolicyInternetservicesrcgroupItem]
    internet_service_src_custom: list[LocalInPolicyInternetservicesrccustomItem]
    internet_service_src_custom_group: list[LocalInPolicyInternetservicesrccustomgroupItem]
    internet_service_src_fortiguard: list[LocalInPolicyInternetservicesrcfortiguardItem]
    dstaddr_negate: Literal["enable", "disable"]
    action: Literal["accept", "deny"]
    service: list[LocalInPolicyServiceItem]
    service_negate: Literal["enable", "disable"]
    internet_service_src_negate: Literal["enable", "disable"]
    schedule: str
    status: Literal["enable", "disable"]
    virtual_patch: Literal["enable", "disable"]
    logtraffic: Literal["enable", "disable"]
    comments: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LocalInPolicyIntfItemObject(FortiObject[LocalInPolicyIntfItem]):
    """Typed object for intf table items with attribute access."""
    name: str


class LocalInPolicySrcaddrItemObject(FortiObject[LocalInPolicySrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class LocalInPolicyDstaddrItemObject(FortiObject[LocalInPolicyDstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class LocalInPolicyInternetservicesrcnameItemObject(FortiObject[LocalInPolicyInternetservicesrcnameItem]):
    """Typed object for internet-service-src-name table items with attribute access."""
    name: str


class LocalInPolicyInternetservicesrcgroupItemObject(FortiObject[LocalInPolicyInternetservicesrcgroupItem]):
    """Typed object for internet-service-src-group table items with attribute access."""
    name: str


class LocalInPolicyInternetservicesrccustomItemObject(FortiObject[LocalInPolicyInternetservicesrccustomItem]):
    """Typed object for internet-service-src-custom table items with attribute access."""
    name: str


class LocalInPolicyInternetservicesrccustomgroupItemObject(FortiObject[LocalInPolicyInternetservicesrccustomgroupItem]):
    """Typed object for internet-service-src-custom-group table items with attribute access."""
    name: str


class LocalInPolicyInternetservicesrcfortiguardItemObject(FortiObject[LocalInPolicyInternetservicesrcfortiguardItem]):
    """Typed object for internet-service-src-fortiguard table items with attribute access."""
    name: str


class LocalInPolicyServiceItemObject(FortiObject[LocalInPolicyServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class LocalInPolicyObject(FortiObject):
    """Typed FortiObject for LocalInPolicy with field access."""
    policyid: int
    uuid: str
    ha_mgmt_intf_only: Literal["enable", "disable"]
    intf: FortiObjectList[LocalInPolicyIntfItemObject]
    srcaddr: FortiObjectList[LocalInPolicySrcaddrItemObject]
    srcaddr_negate: Literal["enable", "disable"]
    dstaddr: FortiObjectList[LocalInPolicyDstaddrItemObject]
    internet_service_src: Literal["enable", "disable"]
    internet_service_src_name: FortiObjectList[LocalInPolicyInternetservicesrcnameItemObject]
    internet_service_src_group: FortiObjectList[LocalInPolicyInternetservicesrcgroupItemObject]
    internet_service_src_custom: FortiObjectList[LocalInPolicyInternetservicesrccustomItemObject]
    internet_service_src_custom_group: FortiObjectList[LocalInPolicyInternetservicesrccustomgroupItemObject]
    internet_service_src_fortiguard: FortiObjectList[LocalInPolicyInternetservicesrcfortiguardItemObject]
    dstaddr_negate: Literal["enable", "disable"]
    action: Literal["accept", "deny"]
    service: FortiObjectList[LocalInPolicyServiceItemObject]
    service_negate: Literal["enable", "disable"]
    internet_service_src_negate: Literal["enable", "disable"]
    schedule: str
    status: Literal["enable", "disable"]
    virtual_patch: Literal["enable", "disable"]
    logtraffic: Literal["enable", "disable"]
    comments: str


# ================================================================
# Main Endpoint Class
# ================================================================

class LocalInPolicy:
    """
    
    Endpoint: firewall/local_in_policy
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
    ) -> LocalInPolicyObject: ...
    
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
    ) -> FortiObjectList[LocalInPolicyObject]: ...
    
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
        payload_dict: LocalInPolicyPayload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        ha_mgmt_intf_only: Literal["enable", "disable"] | None = ...,
        intf: str | list[str] | list[LocalInPolicyIntfItem] | None = ...,
        srcaddr: str | list[str] | list[LocalInPolicySrcaddrItem] | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr: str | list[str] | list[LocalInPolicyDstaddrItem] | None = ...,
        internet_service_src: Literal["enable", "disable"] | None = ...,
        internet_service_src_name: str | list[str] | list[LocalInPolicyInternetservicesrcnameItem] | None = ...,
        internet_service_src_group: str | list[str] | list[LocalInPolicyInternetservicesrcgroupItem] | None = ...,
        internet_service_src_custom: str | list[str] | list[LocalInPolicyInternetservicesrccustomItem] | None = ...,
        internet_service_src_custom_group: str | list[str] | list[LocalInPolicyInternetservicesrccustomgroupItem] | None = ...,
        internet_service_src_fortiguard: str | list[str] | list[LocalInPolicyInternetservicesrcfortiguardItem] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        service: str | list[str] | list[LocalInPolicyServiceItem] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_src_negate: Literal["enable", "disable"] | None = ...,
        schedule: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        virtual_patch: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocalInPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LocalInPolicyPayload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        ha_mgmt_intf_only: Literal["enable", "disable"] | None = ...,
        intf: str | list[str] | list[LocalInPolicyIntfItem] | None = ...,
        srcaddr: str | list[str] | list[LocalInPolicySrcaddrItem] | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr: str | list[str] | list[LocalInPolicyDstaddrItem] | None = ...,
        internet_service_src: Literal["enable", "disable"] | None = ...,
        internet_service_src_name: str | list[str] | list[LocalInPolicyInternetservicesrcnameItem] | None = ...,
        internet_service_src_group: str | list[str] | list[LocalInPolicyInternetservicesrcgroupItem] | None = ...,
        internet_service_src_custom: str | list[str] | list[LocalInPolicyInternetservicesrccustomItem] | None = ...,
        internet_service_src_custom_group: str | list[str] | list[LocalInPolicyInternetservicesrccustomgroupItem] | None = ...,
        internet_service_src_fortiguard: str | list[str] | list[LocalInPolicyInternetservicesrcfortiguardItem] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        service: str | list[str] | list[LocalInPolicyServiceItem] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_src_negate: Literal["enable", "disable"] | None = ...,
        schedule: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        virtual_patch: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocalInPolicyObject: ...

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
        payload_dict: LocalInPolicyPayload | None = ...,
        policyid: int | None = ...,
        uuid: str | None = ...,
        ha_mgmt_intf_only: Literal["enable", "disable"] | None = ...,
        intf: str | list[str] | list[LocalInPolicyIntfItem] | None = ...,
        srcaddr: str | list[str] | list[LocalInPolicySrcaddrItem] | None = ...,
        srcaddr_negate: Literal["enable", "disable"] | None = ...,
        dstaddr: str | list[str] | list[LocalInPolicyDstaddrItem] | None = ...,
        internet_service_src: Literal["enable", "disable"] | None = ...,
        internet_service_src_name: str | list[str] | list[LocalInPolicyInternetservicesrcnameItem] | None = ...,
        internet_service_src_group: str | list[str] | list[LocalInPolicyInternetservicesrcgroupItem] | None = ...,
        internet_service_src_custom: str | list[str] | list[LocalInPolicyInternetservicesrccustomItem] | None = ...,
        internet_service_src_custom_group: str | list[str] | list[LocalInPolicyInternetservicesrccustomgroupItem] | None = ...,
        internet_service_src_fortiguard: str | list[str] | list[LocalInPolicyInternetservicesrcfortiguardItem] | None = ...,
        dstaddr_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        service: str | list[str] | list[LocalInPolicyServiceItem] | None = ...,
        service_negate: Literal["enable", "disable"] | None = ...,
        internet_service_src_negate: Literal["enable", "disable"] | None = ...,
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
    "LocalInPolicy",
    "LocalInPolicyPayload",
    "LocalInPolicyResponse",
    "LocalInPolicyObject",
]