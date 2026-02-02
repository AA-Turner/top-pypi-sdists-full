""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/ippool
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

class IppoolPayload(TypedDict, total=False):
    """Payload type for Ippool operations."""
    name: str
    type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"]
    startip: str
    endip: str
    startport: int
    endport: int
    source_startip: str
    source_endip: str
    block_size: int
    port_per_user: int
    num_blocks_per_user: int
    pba_timeout: int
    pba_interim_log: int
    permit_any_host: Literal["disable", "enable"]
    arp_reply: Literal["disable", "enable"]
    arp_intf: str
    associated_interface: str
    comments: str
    nat64: Literal["disable", "enable"]
    add_nat64_route: Literal["disable", "enable"]
    source_prefix6: str
    client_prefix_length: int
    tcp_session_quota: int
    udp_session_quota: int
    icmp_session_quota: int
    privileged_port_use_pba: Literal["disable", "enable"]
    subnet_broadcast_in_ippool: Literal["disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IppoolResponse(TypedDict, total=False):
    """Response type for Ippool - use with .dict property for typed dict access."""
    name: str
    type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"]
    startip: str
    endip: str
    startport: int
    endport: int
    source_startip: str
    source_endip: str
    block_size: int
    port_per_user: int
    num_blocks_per_user: int
    pba_timeout: int
    pba_interim_log: int
    permit_any_host: Literal["disable", "enable"]
    arp_reply: Literal["disable", "enable"]
    arp_intf: str
    associated_interface: str
    comments: str
    nat64: Literal["disable", "enable"]
    add_nat64_route: Literal["disable", "enable"]
    source_prefix6: str
    client_prefix_length: int
    tcp_session_quota: int
    udp_session_quota: int
    icmp_session_quota: int
    privileged_port_use_pba: Literal["disable", "enable"]
    subnet_broadcast_in_ippool: Literal["disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IppoolObject(FortiObject):
    """Typed FortiObject for Ippool with field access."""
    name: str
    type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"]
    startip: str
    endip: str
    startport: int
    endport: int
    source_startip: str
    source_endip: str
    block_size: int
    port_per_user: int
    num_blocks_per_user: int
    pba_timeout: int
    pba_interim_log: int
    permit_any_host: Literal["disable", "enable"]
    arp_reply: Literal["disable", "enable"]
    arp_intf: str
    associated_interface: str
    comments: str
    nat64: Literal["disable", "enable"]
    add_nat64_route: Literal["disable", "enable"]
    source_prefix6: str
    client_prefix_length: int
    tcp_session_quota: int
    udp_session_quota: int
    icmp_session_quota: int
    privileged_port_use_pba: Literal["disable", "enable"]
    subnet_broadcast_in_ippool: Literal["disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Ippool:
    """
    
    Endpoint: firewall/ippool
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
    ) -> IppoolObject: ...
    
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
    ) -> FortiObjectList[IppoolObject]: ...
    
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
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IppoolObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IppoolObject: ...

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
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
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
    "Ippool",
    "IppoolPayload",
    "IppoolResponse",
    "IppoolObject",
]