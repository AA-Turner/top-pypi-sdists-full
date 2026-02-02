""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/qos/queue_policy
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

class QueuePolicyCosqueueItem(TypedDict, total=False):
    """Nested item for cos-queue field."""
    name: str
    description: str
    min_rate: int
    max_rate: int
    min_rate_percent: int
    max_rate_percent: int
    drop_policy: Literal["taildrop", "weighted-random-early-detection"]
    ecn: Literal["disable", "enable"]
    weight: int


class QueuePolicyPayload(TypedDict, total=False):
    """Payload type for QueuePolicy operations."""
    name: str
    schedule: Literal["strict", "round-robin", "weighted"]
    rate_by: Literal["kbps", "percent"]
    cos_queue: str | list[str] | list[QueuePolicyCosqueueItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class QueuePolicyResponse(TypedDict, total=False):
    """Response type for QueuePolicy - use with .dict property for typed dict access."""
    name: str
    schedule: Literal["strict", "round-robin", "weighted"]
    rate_by: Literal["kbps", "percent"]
    cos_queue: list[QueuePolicyCosqueueItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class QueuePolicyCosqueueItemObject(FortiObject[QueuePolicyCosqueueItem]):
    """Typed object for cos-queue table items with attribute access."""
    name: str
    description: str
    min_rate: int
    max_rate: int
    min_rate_percent: int
    max_rate_percent: int
    drop_policy: Literal["taildrop", "weighted-random-early-detection"]
    ecn: Literal["disable", "enable"]
    weight: int


class QueuePolicyObject(FortiObject):
    """Typed FortiObject for QueuePolicy with field access."""
    name: str
    schedule: Literal["strict", "round-robin", "weighted"]
    rate_by: Literal["kbps", "percent"]
    cos_queue: FortiObjectList[QueuePolicyCosqueueItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class QueuePolicy:
    """
    
    Endpoint: switch_controller/qos/queue_policy
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
    ) -> QueuePolicyObject: ...
    
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
    ) -> FortiObjectList[QueuePolicyObject]: ...
    
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
        payload_dict: QueuePolicyPayload | None = ...,
        name: str | None = ...,
        schedule: Literal["strict", "round-robin", "weighted"] | None = ...,
        rate_by: Literal["kbps", "percent"] | None = ...,
        cos_queue: str | list[str] | list[QueuePolicyCosqueueItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QueuePolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: QueuePolicyPayload | None = ...,
        name: str | None = ...,
        schedule: Literal["strict", "round-robin", "weighted"] | None = ...,
        rate_by: Literal["kbps", "percent"] | None = ...,
        cos_queue: str | list[str] | list[QueuePolicyCosqueueItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QueuePolicyObject: ...

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
        payload_dict: QueuePolicyPayload | None = ...,
        name: str | None = ...,
        schedule: Literal["strict", "round-robin", "weighted"] | None = ...,
        rate_by: Literal["kbps", "percent"] | None = ...,
        cos_queue: str | list[str] | list[QueuePolicyCosqueueItem] | None = ...,
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
    "QueuePolicy",
    "QueuePolicyPayload",
    "QueuePolicyResponse",
    "QueuePolicyObject",
]