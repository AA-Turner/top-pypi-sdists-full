""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/multicast_policy
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

class MulticastPolicySrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class MulticastPolicyDstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class MulticastPolicyPayload(TypedDict, total=False):
    """Payload type for MulticastPolicy operations."""
    id: int
    uuid: str
    name: str
    comments: str
    status: Literal["enable", "disable"]
    srcintf: str
    dstintf: str
    srcaddr: str | list[str] | list[MulticastPolicySrcaddrItem]
    dstaddr: str | list[str] | list[MulticastPolicyDstaddrItem]
    snat: Literal["enable", "disable"]
    snat_ip: str
    dnat: str
    action: Literal["accept", "deny"]
    protocol: int
    start_port: int
    end_port: int
    utm_status: Literal["enable", "disable"]
    ips_sensor: str
    logtraffic: Literal["all", "utm", "disable"]
    auto_asic_offload: Literal["enable", "disable"]
    traffic_shaper: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class MulticastPolicyResponse(TypedDict, total=False):
    """Response type for MulticastPolicy - use with .dict property for typed dict access."""
    id: int
    uuid: str
    name: str
    comments: str
    status: Literal["enable", "disable"]
    srcintf: str
    dstintf: str
    srcaddr: list[MulticastPolicySrcaddrItem]
    dstaddr: list[MulticastPolicyDstaddrItem]
    snat: Literal["enable", "disable"]
    snat_ip: str
    dnat: str
    action: Literal["accept", "deny"]
    protocol: int
    start_port: int
    end_port: int
    utm_status: Literal["enable", "disable"]
    ips_sensor: str
    logtraffic: Literal["all", "utm", "disable"]
    auto_asic_offload: Literal["enable", "disable"]
    traffic_shaper: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class MulticastPolicySrcaddrItemObject(FortiObject[MulticastPolicySrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class MulticastPolicyDstaddrItemObject(FortiObject[MulticastPolicyDstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class MulticastPolicyObject(FortiObject):
    """Typed FortiObject for MulticastPolicy with field access."""
    id: int
    uuid: str
    name: str
    comments: str
    status: Literal["enable", "disable"]
    srcintf: str
    dstintf: str
    srcaddr: FortiObjectList[MulticastPolicySrcaddrItemObject]
    dstaddr: FortiObjectList[MulticastPolicyDstaddrItemObject]
    snat: Literal["enable", "disable"]
    snat_ip: str
    dnat: str
    action: Literal["accept", "deny"]
    protocol: int
    start_port: int
    end_port: int
    utm_status: Literal["enable", "disable"]
    ips_sensor: str
    logtraffic: Literal["all", "utm", "disable"]
    auto_asic_offload: Literal["enable", "disable"]
    traffic_shaper: str


# ================================================================
# Main Endpoint Class
# ================================================================

class MulticastPolicy:
    """
    
    Endpoint: firewall/multicast_policy
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
    ) -> MulticastPolicyObject: ...
    
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
    ) -> FortiObjectList[MulticastPolicyObject]: ...
    
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
        payload_dict: MulticastPolicyPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        srcintf: str | None = ...,
        dstintf: str | None = ...,
        srcaddr: str | list[str] | list[MulticastPolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[MulticastPolicyDstaddrItem] | None = ...,
        snat: Literal["enable", "disable"] | None = ...,
        snat_ip: str | None = ...,
        dnat: str | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        traffic_shaper: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MulticastPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: MulticastPolicyPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        srcintf: str | None = ...,
        dstintf: str | None = ...,
        srcaddr: str | list[str] | list[MulticastPolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[MulticastPolicyDstaddrItem] | None = ...,
        snat: Literal["enable", "disable"] | None = ...,
        snat_ip: str | None = ...,
        dnat: str | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        traffic_shaper: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MulticastPolicyObject: ...

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
        payload_dict: MulticastPolicyPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        srcintf: str | None = ...,
        dstintf: str | None = ...,
        srcaddr: str | list[str] | list[MulticastPolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[MulticastPolicyDstaddrItem] | None = ...,
        snat: Literal["enable", "disable"] | None = ...,
        snat_ip: str | None = ...,
        dnat: str | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        traffic_shaper: str | None = ...,
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
    "MulticastPolicy",
    "MulticastPolicyPayload",
    "MulticastPolicyResponse",
    "MulticastPolicyObject",
]