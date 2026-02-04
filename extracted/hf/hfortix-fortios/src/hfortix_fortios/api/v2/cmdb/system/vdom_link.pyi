""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/vdom_link
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

class VdomLinkPayload(TypedDict, total=False):
    """Payload type for VdomLink operations."""
    name: str
    vcluster: Literal["vcluster1", "vcluster2"]
    type: Literal["ppp", "ethernet"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VdomLinkResponse(TypedDict, total=False):
    """Response type for VdomLink - use with .dict property for typed dict access."""
    name: str
    vcluster: Literal["vcluster1", "vcluster2"]
    type: Literal["ppp", "ethernet"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VdomLinkObject(FortiObject):
    """Typed FortiObject for VdomLink with field access."""
    name: str
    vcluster: Literal["vcluster1", "vcluster2"]
    type: Literal["ppp", "ethernet"]


# ================================================================
# Main Endpoint Class
# ================================================================

class VdomLink:
    """
    
    Endpoint: system/vdom_link
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomLinkObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[VdomLinkObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: VdomLinkPayload | None = ...,
        name: str | None = ...,
        vcluster: Literal["vcluster1", "vcluster2"] | None = ...,
        type: Literal["ppp", "ethernet"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomLinkObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VdomLinkPayload | None = ...,
        name: str | None = ...,
        vcluster: Literal["vcluster1", "vcluster2"] | None = ...,
        type: Literal["ppp", "ethernet"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomLinkObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
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
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: VdomLinkPayload | None = ...,
        name: str | None = ...,
        vcluster: Literal["vcluster1", "vcluster2"] | None = ...,
        type: Literal["ppp", "ethernet"] | None = ...,
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
    "VdomLink",
    "VdomLinkPayload",
    "VdomLinkResponse",
    "VdomLinkObject",
]