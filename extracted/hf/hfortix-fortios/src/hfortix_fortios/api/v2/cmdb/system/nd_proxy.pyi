""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/nd_proxy
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

class NdProxyMemberItem(TypedDict, total=False):
    """Nested item for member field."""
    interface_name: str


class NdProxyPayload(TypedDict, total=False):
    """Payload type for NdProxy operations."""
    status: Literal["enable", "disable"]
    member: str | list[str] | list[NdProxyMemberItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class NdProxyResponse(TypedDict, total=False):
    """Response type for NdProxy - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    member: list[NdProxyMemberItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class NdProxyMemberItemObject(FortiObject[NdProxyMemberItem]):
    """Typed object for member table items with attribute access."""
    interface_name: str


class NdProxyObject(FortiObject):
    """Typed FortiObject for NdProxy with field access."""
    status: Literal["enable", "disable"]
    member: FortiObjectList[NdProxyMemberItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class NdProxy:
    """
    
    Endpoint: system/nd_proxy
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
    ) -> NdProxyObject: ...
    
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
        payload_dict: NdProxyPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[NdProxyMemberItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NdProxyObject: ...


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
        payload_dict: NdProxyPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[NdProxyMemberItem] | None = ...,
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
    "NdProxy",
    "NdProxyPayload",
    "NdProxyResponse",
    "NdProxyObject",
]