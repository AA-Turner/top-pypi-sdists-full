""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/shaper/traffic_shaper
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

class TrafficShaperPayload(TypedDict, total=False):
    """Payload type for TrafficShaper operations."""
    name: str
    guaranteed_bandwidth: int
    maximum_bandwidth: int
    bandwidth_unit: Literal["kbps", "mbps", "gbps"]
    priority: Literal["low", "medium", "high"]
    per_policy: Literal["disable", "enable"]
    diffserv: Literal["enable", "disable"]
    diffservcode: str
    dscp_marking_method: Literal["multi-stage", "static"]
    exceed_bandwidth: int
    exceed_dscp: str
    maximum_dscp: str
    cos_marking: Literal["enable", "disable"]
    cos_marking_method: Literal["multi-stage", "static"]
    cos: str
    exceed_cos: str
    maximum_cos: str
    overhead: int
    exceed_class_id: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class TrafficShaperResponse(TypedDict, total=False):
    """Response type for TrafficShaper - use with .dict property for typed dict access."""
    name: str
    guaranteed_bandwidth: int
    maximum_bandwidth: int
    bandwidth_unit: Literal["kbps", "mbps", "gbps"]
    priority: Literal["low", "medium", "high"]
    per_policy: Literal["disable", "enable"]
    diffserv: Literal["enable", "disable"]
    diffservcode: str
    dscp_marking_method: Literal["multi-stage", "static"]
    exceed_bandwidth: int
    exceed_dscp: str
    maximum_dscp: str
    cos_marking: Literal["enable", "disable"]
    cos_marking_method: Literal["multi-stage", "static"]
    cos: str
    exceed_cos: str
    maximum_cos: str
    overhead: int
    exceed_class_id: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class TrafficShaperObject(FortiObject):
    """Typed FortiObject for TrafficShaper with field access."""
    name: str
    guaranteed_bandwidth: int
    maximum_bandwidth: int
    bandwidth_unit: Literal["kbps", "mbps", "gbps"]
    priority: Literal["low", "medium", "high"]
    per_policy: Literal["disable", "enable"]
    diffserv: Literal["enable", "disable"]
    diffservcode: str
    dscp_marking_method: Literal["multi-stage", "static"]
    exceed_bandwidth: int
    exceed_dscp: str
    maximum_dscp: str
    cos_marking: Literal["enable", "disable"]
    cos_marking_method: Literal["multi-stage", "static"]
    cos: str
    exceed_cos: str
    maximum_cos: str
    overhead: int
    exceed_class_id: int


# ================================================================
# Main Endpoint Class
# ================================================================

class TrafficShaper:
    """
    
    Endpoint: firewall/shaper/traffic_shaper
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
    ) -> TrafficShaperObject: ...
    
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
    ) -> FortiObjectList[TrafficShaperObject]: ...
    
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
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TrafficShaperObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TrafficShaperObject: ...

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
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
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
    "TrafficShaper",
    "TrafficShaperPayload",
    "TrafficShaperResponse",
    "TrafficShaperObject",
]