""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/shaping_profile
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

class ShapingProfileShapingentriesItem(TypedDict, total=False):
    """Nested item for shaping-entries field."""
    id: int
    class_id: int
    priority: Literal["top", "critical", "high", "medium", "low"]
    guaranteed_bandwidth_percentage: int
    maximum_bandwidth_percentage: int
    limit: int
    burst_in_msec: int
    cburst_in_msec: int
    red_probability: int
    min: int
    max: int


class ShapingProfilePayload(TypedDict, total=False):
    """Payload type for ShapingProfile operations."""
    profile_name: str
    comment: str
    type: Literal["policing", "queuing"]
    npu_offloading: Literal["disable", "enable"]
    default_class_id: int
    shaping_entries: str | list[str] | list[ShapingProfileShapingentriesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ShapingProfileResponse(TypedDict, total=False):
    """Response type for ShapingProfile - use with .dict property for typed dict access."""
    profile_name: str
    comment: str
    type: Literal["policing", "queuing"]
    npu_offloading: Literal["disable", "enable"]
    default_class_id: int
    shaping_entries: list[ShapingProfileShapingentriesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ShapingProfileShapingentriesItemObject(FortiObject[ShapingProfileShapingentriesItem]):
    """Typed object for shaping-entries table items with attribute access."""
    id: int
    class_id: int
    priority: Literal["top", "critical", "high", "medium", "low"]
    guaranteed_bandwidth_percentage: int
    maximum_bandwidth_percentage: int
    limit: int
    burst_in_msec: int
    cburst_in_msec: int
    red_probability: int
    min: int
    max: int


class ShapingProfileObject(FortiObject):
    """Typed FortiObject for ShapingProfile with field access."""
    profile_name: str
    comment: str
    type: Literal["policing", "queuing"]
    npu_offloading: Literal["disable", "enable"]
    default_class_id: int
    shaping_entries: FortiObjectList[ShapingProfileShapingentriesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ShapingProfile:
    """
    
    Endpoint: firewall/shaping_profile
    Category: cmdb
    MKey: profile-name
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
        profile_name: str,
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
    ) -> ShapingProfileObject: ...
    
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
    ) -> FortiObjectList[ShapingProfileObject]: ...
    
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
        payload_dict: ShapingProfilePayload | None = ...,
        profile_name: str | None = ...,
        comment: str | None = ...,
        type: Literal["policing", "queuing"] | None = ...,
        npu_offloading: Literal["disable", "enable"] | None = ...,
        default_class_id: int | None = ...,
        shaping_entries: str | list[str] | list[ShapingProfileShapingentriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ShapingProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ShapingProfilePayload | None = ...,
        profile_name: str | None = ...,
        comment: str | None = ...,
        type: Literal["policing", "queuing"] | None = ...,
        npu_offloading: Literal["disable", "enable"] | None = ...,
        default_class_id: int | None = ...,
        shaping_entries: str | list[str] | list[ShapingProfileShapingentriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ShapingProfileObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        profile_name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        profile_name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_profile_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        profile_name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ShapingProfilePayload | None = ...,
        profile_name: str | None = ...,
        comment: str | None = ...,
        type: Literal["policing", "queuing"] | None = ...,
        npu_offloading: Literal["disable", "enable"] | None = ...,
        default_class_id: int | None = ...,
        shaping_entries: str | list[str] | list[ShapingProfileShapingentriesItem] | None = ...,
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
    "ShapingProfile",
    "ShapingProfilePayload",
    "ShapingProfileResponse",
    "ShapingProfileObject",
]