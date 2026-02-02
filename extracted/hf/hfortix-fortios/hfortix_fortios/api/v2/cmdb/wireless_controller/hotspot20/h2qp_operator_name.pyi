""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/h2qp_operator_name
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

class H2qpOperatorNameValuelistItem(TypedDict, total=False):
    """Nested item for value-list field."""
    index: int
    lang: str
    value: str


class H2qpOperatorNamePayload(TypedDict, total=False):
    """Payload type for H2qpOperatorName operations."""
    name: str
    value_list: str | list[str] | list[H2qpOperatorNameValuelistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class H2qpOperatorNameResponse(TypedDict, total=False):
    """Response type for H2qpOperatorName - use with .dict property for typed dict access."""
    name: str
    value_list: list[H2qpOperatorNameValuelistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class H2qpOperatorNameValuelistItemObject(FortiObject[H2qpOperatorNameValuelistItem]):
    """Typed object for value-list table items with attribute access."""
    index: int
    lang: str
    value: str


class H2qpOperatorNameObject(FortiObject):
    """Typed FortiObject for H2qpOperatorName with field access."""
    name: str
    value_list: FortiObjectList[H2qpOperatorNameValuelistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class H2qpOperatorName:
    """
    
    Endpoint: wireless_controller/hotspot20/h2qp_operator_name
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
    ) -> H2qpOperatorNameObject: ...
    
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
    ) -> FortiObjectList[H2qpOperatorNameObject]: ...
    
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
        payload_dict: H2qpOperatorNamePayload | None = ...,
        name: str | None = ...,
        value_list: str | list[str] | list[H2qpOperatorNameValuelistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpOperatorNameObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: H2qpOperatorNamePayload | None = ...,
        name: str | None = ...,
        value_list: str | list[str] | list[H2qpOperatorNameValuelistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpOperatorNameObject: ...

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
        payload_dict: H2qpOperatorNamePayload | None = ...,
        name: str | None = ...,
        value_list: str | list[str] | list[H2qpOperatorNameValuelistItem] | None = ...,
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
    "H2qpOperatorName",
    "H2qpOperatorNamePayload",
    "H2qpOperatorNameResponse",
    "H2qpOperatorNameObject",
]