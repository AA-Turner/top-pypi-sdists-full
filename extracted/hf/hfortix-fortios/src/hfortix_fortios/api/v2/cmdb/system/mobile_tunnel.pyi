""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/mobile_tunnel
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

class MobileTunnelNetworkItem(TypedDict, total=False):
    """Nested item for network field."""
    id: int
    interface: str
    prefix: str


class MobileTunnelPayload(TypedDict, total=False):
    """Payload type for MobileTunnel operations."""
    name: str
    status: Literal["disable", "enable"]
    roaming_interface: str
    home_agent: str
    home_address: str
    renew_interval: int
    lifetime: int
    reg_interval: int
    reg_retry: int
    n_mhae_spi: int
    n_mhae_key_type: Literal["ascii", "base64"]
    n_mhae_key: str
    hash_algorithm: Literal["hmac-md5"]
    tunnel_mode: Literal["gre"]
    network: str | list[str] | list[MobileTunnelNetworkItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class MobileTunnelResponse(TypedDict, total=False):
    """Response type for MobileTunnel - use with .dict property for typed dict access."""
    name: str
    status: Literal["disable", "enable"]
    roaming_interface: str
    home_agent: str
    home_address: str
    renew_interval: int
    lifetime: int
    reg_interval: int
    reg_retry: int
    n_mhae_spi: int
    n_mhae_key_type: Literal["ascii", "base64"]
    n_mhae_key: str
    hash_algorithm: Literal["hmac-md5"]
    tunnel_mode: Literal["gre"]
    network: list[MobileTunnelNetworkItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class MobileTunnelNetworkItemObject(FortiObject[MobileTunnelNetworkItem]):
    """Typed object for network table items with attribute access."""
    id: int
    interface: str
    prefix: str


class MobileTunnelObject(FortiObject):
    """Typed FortiObject for MobileTunnel with field access."""
    name: str
    status: Literal["disable", "enable"]
    roaming_interface: str
    home_agent: str
    home_address: str
    renew_interval: int
    lifetime: int
    reg_interval: int
    reg_retry: int
    n_mhae_spi: int
    n_mhae_key_type: Literal["ascii", "base64"]
    n_mhae_key: str
    hash_algorithm: Literal["hmac-md5"]
    tunnel_mode: Literal["gre"]
    network: FortiObjectList[MobileTunnelNetworkItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class MobileTunnel:
    """
    
    Endpoint: system/mobile_tunnel
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MobileTunnelObject: ...
    
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
    ) -> FortiObjectList[MobileTunnelObject]: ...
    
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
        payload_dict: MobileTunnelPayload | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        roaming_interface: str | None = ...,
        home_agent: str | None = ...,
        home_address: str | None = ...,
        renew_interval: int | None = ...,
        lifetime: int | None = ...,
        reg_interval: int | None = ...,
        reg_retry: int | None = ...,
        n_mhae_spi: int | None = ...,
        n_mhae_key_type: Literal["ascii", "base64"] | None = ...,
        n_mhae_key: str | None = ...,
        hash_algorithm: Literal["hmac-md5"] | None = ...,
        tunnel_mode: Literal["gre"] | None = ...,
        network: str | list[str] | list[MobileTunnelNetworkItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MobileTunnelObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: MobileTunnelPayload | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        roaming_interface: str | None = ...,
        home_agent: str | None = ...,
        home_address: str | None = ...,
        renew_interval: int | None = ...,
        lifetime: int | None = ...,
        reg_interval: int | None = ...,
        reg_retry: int | None = ...,
        n_mhae_spi: int | None = ...,
        n_mhae_key_type: Literal["ascii", "base64"] | None = ...,
        n_mhae_key: str | None = ...,
        hash_algorithm: Literal["hmac-md5"] | None = ...,
        tunnel_mode: Literal["gre"] | None = ...,
        network: str | list[str] | list[MobileTunnelNetworkItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MobileTunnelObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
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
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: MobileTunnelPayload | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        roaming_interface: str | None = ...,
        home_agent: str | None = ...,
        home_address: str | None = ...,
        renew_interval: int | None = ...,
        lifetime: int | None = ...,
        reg_interval: int | None = ...,
        reg_retry: int | None = ...,
        n_mhae_spi: int | None = ...,
        n_mhae_key_type: Literal["ascii", "base64"] | None = ...,
        n_mhae_key: str | None = ...,
        hash_algorithm: Literal["hmac-md5"] | None = ...,
        tunnel_mode: Literal["gre"] | None = ...,
        network: str | list[str] | list[MobileTunnelNetworkItem] | None = ...,
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
    "MobileTunnel",
    "MobileTunnelPayload",
    "MobileTunnelResponse",
    "MobileTunnelObject",
]