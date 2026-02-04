""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/gre_tunnel
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

class GreTunnelPayload(TypedDict, total=False):
    """Payload type for GreTunnel operations."""
    name: str
    interface: str
    ip_version: Literal["4", "6"]
    remote_gw6: str
    local_gw6: str
    remote_gw: str
    local_gw: str
    use_sdwan: Literal["disable", "enable"]
    sequence_number_transmission: Literal["disable", "enable"]
    sequence_number_reception: Literal["disable", "enable"]
    checksum_transmission: Literal["disable", "enable"]
    checksum_reception: Literal["disable", "enable"]
    key_outbound: int
    key_inbound: int
    dscp_copying: Literal["disable", "enable"]
    diffservcode: str
    keepalive_interval: int
    keepalive_failtimes: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GreTunnelResponse(TypedDict, total=False):
    """Response type for GreTunnel - use with .dict property for typed dict access."""
    name: str
    interface: str
    ip_version: Literal["4", "6"]
    remote_gw6: str
    local_gw6: str
    remote_gw: str
    local_gw: str
    use_sdwan: Literal["disable", "enable"]
    sequence_number_transmission: Literal["disable", "enable"]
    sequence_number_reception: Literal["disable", "enable"]
    checksum_transmission: Literal["disable", "enable"]
    checksum_reception: Literal["disable", "enable"]
    key_outbound: int
    key_inbound: int
    dscp_copying: Literal["disable", "enable"]
    diffservcode: str
    keepalive_interval: int
    keepalive_failtimes: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GreTunnelObject(FortiObject):
    """Typed FortiObject for GreTunnel with field access."""
    name: str
    interface: str
    ip_version: Literal["4", "6"]
    remote_gw6: str
    local_gw6: str
    remote_gw: str
    local_gw: str
    use_sdwan: Literal["disable", "enable"]
    sequence_number_transmission: Literal["disable", "enable"]
    sequence_number_reception: Literal["disable", "enable"]
    checksum_transmission: Literal["disable", "enable"]
    checksum_reception: Literal["disable", "enable"]
    key_outbound: int
    key_inbound: int
    dscp_copying: Literal["disable", "enable"]
    diffservcode: str
    keepalive_interval: int
    keepalive_failtimes: int


# ================================================================
# Main Endpoint Class
# ================================================================

class GreTunnel:
    """
    
    Endpoint: system/gre_tunnel
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
    ) -> GreTunnelObject: ...
    
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
    ) -> FortiObjectList[GreTunnelObject]: ...
    
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
        payload_dict: GreTunnelPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        ip_version: Literal["4", "6"] | None = ...,
        remote_gw6: str | None = ...,
        local_gw6: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        use_sdwan: Literal["disable", "enable"] | None = ...,
        sequence_number_transmission: Literal["disable", "enable"] | None = ...,
        sequence_number_reception: Literal["disable", "enable"] | None = ...,
        checksum_transmission: Literal["disable", "enable"] | None = ...,
        checksum_reception: Literal["disable", "enable"] | None = ...,
        key_outbound: int | None = ...,
        key_inbound: int | None = ...,
        dscp_copying: Literal["disable", "enable"] | None = ...,
        diffservcode: str | None = ...,
        keepalive_interval: int | None = ...,
        keepalive_failtimes: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GreTunnelObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: GreTunnelPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        ip_version: Literal["4", "6"] | None = ...,
        remote_gw6: str | None = ...,
        local_gw6: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        use_sdwan: Literal["disable", "enable"] | None = ...,
        sequence_number_transmission: Literal["disable", "enable"] | None = ...,
        sequence_number_reception: Literal["disable", "enable"] | None = ...,
        checksum_transmission: Literal["disable", "enable"] | None = ...,
        checksum_reception: Literal["disable", "enable"] | None = ...,
        key_outbound: int | None = ...,
        key_inbound: int | None = ...,
        dscp_copying: Literal["disable", "enable"] | None = ...,
        diffservcode: str | None = ...,
        keepalive_interval: int | None = ...,
        keepalive_failtimes: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GreTunnelObject: ...

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
        payload_dict: GreTunnelPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        ip_version: Literal["4", "6"] | None = ...,
        remote_gw6: str | None = ...,
        local_gw6: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        use_sdwan: Literal["disable", "enable"] | None = ...,
        sequence_number_transmission: Literal["disable", "enable"] | None = ...,
        sequence_number_reception: Literal["disable", "enable"] | None = ...,
        checksum_transmission: Literal["disable", "enable"] | None = ...,
        checksum_reception: Literal["disable", "enable"] | None = ...,
        key_outbound: int | None = ...,
        key_inbound: int | None = ...,
        dscp_copying: Literal["disable", "enable"] | None = ...,
        diffservcode: str | None = ...,
        keepalive_interval: int | None = ...,
        keepalive_failtimes: int | None = ...,
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
    "GreTunnel",
    "GreTunnelPayload",
    "GreTunnelResponse",
    "GreTunnelObject",
]