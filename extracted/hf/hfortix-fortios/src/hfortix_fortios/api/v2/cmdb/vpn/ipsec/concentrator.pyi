""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/ipsec/concentrator
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

class ConcentratorMemberItem(TypedDict, total=False):
    """Nested item for member field."""
    name: str


class ConcentratorPayload(TypedDict, total=False):
    """Payload type for Concentrator operations."""
    id: int
    name: str
    src_check: Literal["disable", "enable"]
    member: str | list[str] | list[ConcentratorMemberItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ConcentratorResponse(TypedDict, total=False):
    """Response type for Concentrator - use with .dict property for typed dict access."""
    id: int
    name: str
    src_check: Literal["disable", "enable"]
    member: list[ConcentratorMemberItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ConcentratorMemberItemObject(FortiObject[ConcentratorMemberItem]):
    """Typed object for member table items with attribute access."""
    name: str


class ConcentratorObject(FortiObject):
    """Typed FortiObject for Concentrator with field access."""
    id: int
    name: str
    src_check: Literal["disable", "enable"]
    member: FortiObjectList[ConcentratorMemberItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Concentrator:
    """
    
    Endpoint: vpn/ipsec/concentrator
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> ConcentratorObject: ...
    
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
    ) -> FortiObjectList[ConcentratorObject]: ...
    
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
        payload_dict: ConcentratorPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        src_check: Literal["disable", "enable"] | None = ...,
        member: str | list[str] | list[ConcentratorMemberItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ConcentratorObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ConcentratorPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        src_check: Literal["disable", "enable"] | None = ...,
        member: str | list[str] | list[ConcentratorMemberItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ConcentratorObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ConcentratorPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        src_check: Literal["disable", "enable"] | None = ...,
        member: str | list[str] | list[ConcentratorMemberItem] | None = ...,
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
    "Concentrator",
    "ConcentratorPayload",
    "ConcentratorResponse",
    "ConcentratorObject",
]