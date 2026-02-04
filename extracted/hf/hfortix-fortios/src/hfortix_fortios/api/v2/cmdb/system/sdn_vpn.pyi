""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/sdn_vpn
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

class SdnVpnPayload(TypedDict, total=False):
    """Payload type for SdnVpn operations."""
    name: str
    sdn: str
    remote_type: Literal["vgw", "tgw"]
    routing_type: Literal["static", "dynamic"]
    vgw_id: str
    tgw_id: str
    subnet_id: str
    bgp_as: int
    cgw_gateway: str
    nat_traversal: Literal["disable", "enable"]
    tunnel_interface: str
    internal_interface: str
    local_cidr: str
    remote_cidr: str
    cgw_name: str
    psksecret: str
    type: int
    status: int
    code: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SdnVpnResponse(TypedDict, total=False):
    """Response type for SdnVpn - use with .dict property for typed dict access."""
    name: str
    sdn: str
    remote_type: Literal["vgw", "tgw"]
    routing_type: Literal["static", "dynamic"]
    vgw_id: str
    tgw_id: str
    subnet_id: str
    bgp_as: int
    cgw_gateway: str
    nat_traversal: Literal["disable", "enable"]
    tunnel_interface: str
    internal_interface: str
    local_cidr: str
    remote_cidr: str
    cgw_name: str
    psksecret: str
    type: int
    status: int
    code: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SdnVpnObject(FortiObject):
    """Typed FortiObject for SdnVpn with field access."""
    name: str
    sdn: str
    remote_type: Literal["vgw", "tgw"]
    routing_type: Literal["static", "dynamic"]
    vgw_id: str
    tgw_id: str
    subnet_id: str
    bgp_as: int
    cgw_gateway: str
    nat_traversal: Literal["disable", "enable"]
    tunnel_interface: str
    internal_interface: str
    local_cidr: str
    remote_cidr: str
    cgw_name: str
    psksecret: str
    type: int
    status: int
    code: int


# ================================================================
# Main Endpoint Class
# ================================================================

class SdnVpn:
    """
    
    Endpoint: system/sdn_vpn
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SdnVpnObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[SdnVpnObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SdnVpnObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SdnVpnObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

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
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
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
    "SdnVpn",
    "SdnVpnPayload",
    "SdnVpnResponse",
    "SdnVpnObject",
]