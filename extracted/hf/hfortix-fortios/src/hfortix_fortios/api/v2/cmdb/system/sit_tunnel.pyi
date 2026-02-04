""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/sit_tunnel
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

class SitTunnelPayload(TypedDict, total=False):
    """Payload type for SitTunnel operations."""
    name: str
    source: str
    destination: str
    ip6: str
    interface: str
    use_sdwan: Literal["disable", "enable"]
    auto_asic_offload: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SitTunnelResponse(TypedDict, total=False):
    """Response type for SitTunnel - use with .dict property for typed dict access."""
    name: str
    source: str
    destination: str
    ip6: str
    interface: str
    use_sdwan: Literal["disable", "enable"]
    auto_asic_offload: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SitTunnelObject(FortiObject):
    """Typed FortiObject for SitTunnel with field access."""
    name: str
    source: str
    destination: str
    ip6: str
    interface: str
    use_sdwan: Literal["disable", "enable"]
    auto_asic_offload: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class SitTunnel:
    """
    
    Endpoint: system/sit_tunnel
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
    ) -> SitTunnelObject: ...
    
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
    ) -> FortiObjectList[SitTunnelObject]: ...
    
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
        payload_dict: SitTunnelPayload | None = ...,
        name: str | None = ...,
        source: str | None = ...,
        destination: str | None = ...,
        ip6: str | None = ...,
        interface: str | None = ...,
        use_sdwan: Literal["disable", "enable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SitTunnelObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SitTunnelPayload | None = ...,
        name: str | None = ...,
        source: str | None = ...,
        destination: str | None = ...,
        ip6: str | None = ...,
        interface: str | None = ...,
        use_sdwan: Literal["disable", "enable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SitTunnelObject: ...

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
        payload_dict: SitTunnelPayload | None = ...,
        name: str | None = ...,
        source: str | None = ...,
        destination: str | None = ...,
        ip6: str | None = ...,
        interface: str | None = ...,
        use_sdwan: Literal["disable", "enable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
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
    "SitTunnel",
    "SitTunnelPayload",
    "SitTunnelResponse",
    "SitTunnelObject",
]