""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/qos/dot1p_map
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

class Dot1pMapPayload(TypedDict, total=False):
    """Payload type for Dot1pMap operations."""
    name: str
    description: str
    egress_pri_tagging: Literal["disable", "enable"]
    priority_0: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_1: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_2: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_3: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_4: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_5: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_6: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_7: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Dot1pMapResponse(TypedDict, total=False):
    """Response type for Dot1pMap - use with .dict property for typed dict access."""
    name: str
    description: str
    egress_pri_tagging: Literal["disable", "enable"]
    priority_0: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_1: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_2: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_3: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_4: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_5: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_6: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_7: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Dot1pMapObject(FortiObject):
    """Typed FortiObject for Dot1pMap with field access."""
    name: str
    description: str
    egress_pri_tagging: Literal["disable", "enable"]
    priority_0: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_1: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_2: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_3: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_4: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_5: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_6: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
    priority_7: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Dot1pMap:
    """
    
    Endpoint: switch_controller/qos/dot1p_map
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
    ) -> Dot1pMapObject: ...
    
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
    ) -> FortiObjectList[Dot1pMapObject]: ...
    
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
        payload_dict: Dot1pMapPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        egress_pri_tagging: Literal["disable", "enable"] | None = ...,
        priority_0: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_1: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_2: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_3: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_4: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_5: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_6: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_7: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Dot1pMapObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Dot1pMapPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        egress_pri_tagging: Literal["disable", "enable"] | None = ...,
        priority_0: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_1: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_2: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_3: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_4: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_5: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_6: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_7: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Dot1pMapObject: ...

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
        payload_dict: Dot1pMapPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        egress_pri_tagging: Literal["disable", "enable"] | None = ...,
        priority_0: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_1: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_2: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_3: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_4: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_5: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_6: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
        priority_7: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"] | None = ...,
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
    "Dot1pMap",
    "Dot1pMapPayload",
    "Dot1pMapResponse",
    "Dot1pMapObject",
]