""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/npu
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class NpuPriorityprotocolItem(TypedDict, total=False):
    """Nested item for priority-protocol field."""
    bgp: Literal["enable", "disable"]
    slbc: Literal["enable", "disable"]
    bfd: Literal["enable", "disable"]


class NpuPayload(TypedDict, total=False):
    """Payload type for Npu operations."""
    dedicated_management_cpu: Literal["enable", "disable"]
    dedicated_management_affinity: str
    capwap_offload: Literal["enable", "disable"]
    ipsec_mtu_override: Literal["disable", "enable"]
    ipsec_ordering: Literal["disable", "enable"]
    ipsec_enc_subengine_mask: str
    ipsec_dec_subengine_mask: str
    priority_protocol: str | list[str] | list[NpuPriorityprotocolItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class NpuResponse(TypedDict, total=False):
    """Response type for Npu - use with .dict property for typed dict access."""
    dedicated_management_cpu: Literal["enable", "disable"]
    dedicated_management_affinity: str
    capwap_offload: Literal["enable", "disable"]
    ipsec_mtu_override: Literal["disable", "enable"]
    ipsec_ordering: Literal["disable", "enable"]
    ipsec_enc_subengine_mask: str
    ipsec_dec_subengine_mask: str
    priority_protocol: list[NpuPriorityprotocolItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class NpuPriorityprotocolItemObject(FortiObject[NpuPriorityprotocolItem]):
    """Typed object for priority-protocol table items with attribute access."""
    bgp: Literal["enable", "disable"]
    slbc: Literal["enable", "disable"]
    bfd: Literal["enable", "disable"]


class NpuObject(FortiObject):
    """Typed FortiObject for Npu with field access."""
    dedicated_management_cpu: Literal["enable", "disable"]
    dedicated_management_affinity: str
    capwap_offload: Literal["enable", "disable"]
    ipsec_mtu_override: Literal["disable", "enable"]
    ipsec_ordering: Literal["disable", "enable"]
    ipsec_enc_subengine_mask: str
    ipsec_dec_subengine_mask: str
    priority_protocol: FortiObjectList[NpuPriorityprotocolItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Npu:
    """
    
    Endpoint: system/npu
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Singleton endpoint (no mkey)
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
    ) -> NpuObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: NpuPayload | None = ...,
        dedicated_management_cpu: Literal["enable", "disable"] | None = ...,
        dedicated_management_affinity: str | None = ...,
        capwap_offload: Literal["enable", "disable"] | None = ...,
        ipsec_mtu_override: Literal["disable", "enable"] | None = ...,
        ipsec_ordering: Literal["disable", "enable"] | None = ...,
        ipsec_enc_subengine_mask: str | None = ...,
        ipsec_dec_subengine_mask: str | None = ...,
        priority_protocol: str | list[str] | list[NpuPriorityprotocolItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NpuObject: ...


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
        payload_dict: NpuPayload | None = ...,
        dedicated_management_cpu: Literal["enable", "disable"] | None = ...,
        dedicated_management_affinity: str | None = ...,
        capwap_offload: Literal["enable", "disable"] | None = ...,
        ipsec_mtu_override: Literal["disable", "enable"] | None = ...,
        ipsec_ordering: Literal["disable", "enable"] | None = ...,
        ipsec_enc_subengine_mask: str | None = ...,
        ipsec_dec_subengine_mask: str | None = ...,
        priority_protocol: str | list[str] | list[NpuPriorityprotocolItem] | None = ...,
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
    "Npu",
    "NpuPayload",
    "NpuResponse",
    "NpuObject",
]