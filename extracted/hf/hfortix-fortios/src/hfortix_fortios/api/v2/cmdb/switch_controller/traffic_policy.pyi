""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/traffic_policy
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

class TrafficPolicyPayload(TypedDict, total=False):
    """Payload type for TrafficPolicy operations."""
    name: str
    description: str
    policer_status: Literal["enable", "disable"]
    guaranteed_bandwidth: int
    guaranteed_burst: int
    maximum_burst: int
    type: Literal["ingress", "egress"]
    cos_queue: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class TrafficPolicyResponse(TypedDict, total=False):
    """Response type for TrafficPolicy - use with .dict property for typed dict access."""
    name: str
    description: str
    policer_status: Literal["enable", "disable"]
    guaranteed_bandwidth: int
    guaranteed_burst: int
    maximum_burst: int
    type: Literal["ingress", "egress"]
    cos_queue: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class TrafficPolicyObject(FortiObject):
    """Typed FortiObject for TrafficPolicy with field access."""
    name: str
    description: str
    policer_status: Literal["enable", "disable"]
    guaranteed_bandwidth: int
    guaranteed_burst: int
    maximum_burst: int
    type: Literal["ingress", "egress"]
    cos_queue: int


# ================================================================
# Main Endpoint Class
# ================================================================

class TrafficPolicy:
    """
    
    Endpoint: switch_controller/traffic_policy
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
    ) -> TrafficPolicyObject: ...
    
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
    ) -> FortiObjectList[TrafficPolicyObject]: ...
    
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
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TrafficPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TrafficPolicyObject: ...

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
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
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
    "TrafficPolicy",
    "TrafficPolicyPayload",
    "TrafficPolicyResponse",
    "TrafficPolicyObject",
]