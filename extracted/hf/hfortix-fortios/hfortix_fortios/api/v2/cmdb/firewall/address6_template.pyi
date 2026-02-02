""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/address6_template
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

class Address6TemplateSubnetsegmentValuesItem(TypedDict, total=False):
    """Nested item for subnet-segment.values field."""
    name: str
    value: str


class Address6TemplateSubnetsegmentItem(TypedDict, total=False):
    """Nested item for subnet-segment field."""
    id: int
    name: str
    bits: int
    exclusive: Literal["enable", "disable"]
    values: str | list[str] | list[Address6TemplateSubnetsegmentValuesItem]


class Address6TemplatePayload(TypedDict, total=False):
    """Payload type for Address6Template operations."""
    name: str
    uuid: str
    ip6: str
    subnet_segment_count: int
    subnet_segment: str | list[str] | list[Address6TemplateSubnetsegmentItem]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Address6TemplateResponse(TypedDict, total=False):
    """Response type for Address6Template - use with .dict property for typed dict access."""
    name: str
    uuid: str
    ip6: str
    subnet_segment_count: int
    subnet_segment: list[Address6TemplateSubnetsegmentItem]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Address6TemplateSubnetsegmentValuesItemObject(FortiObject[Address6TemplateSubnetsegmentValuesItem]):
    """Typed object for subnet-segment.values table items with attribute access."""
    name: str
    value: str


class Address6TemplateSubnetsegmentItemObject(FortiObject[Address6TemplateSubnetsegmentItem]):
    """Typed object for subnet-segment table items with attribute access."""
    id: int
    name: str
    bits: int
    exclusive: Literal["enable", "disable"]
    values: FortiObjectList[Address6TemplateSubnetsegmentValuesItemObject]


class Address6TemplateObject(FortiObject):
    """Typed FortiObject for Address6Template with field access."""
    name: str
    uuid: str
    ip6: str
    subnet_segment_count: int
    subnet_segment: FortiObjectList[Address6TemplateSubnetsegmentItemObject]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Address6Template:
    """
    
    Endpoint: firewall/address6_template
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
    ) -> Address6TemplateObject: ...
    
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
    ) -> FortiObjectList[Address6TemplateObject]: ...
    
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
        payload_dict: Address6TemplatePayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        ip6: str | None = ...,
        subnet_segment_count: int | None = ...,
        subnet_segment: str | list[str] | list[Address6TemplateSubnetsegmentItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Address6TemplateObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Address6TemplatePayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        ip6: str | None = ...,
        subnet_segment_count: int | None = ...,
        subnet_segment: str | list[str] | list[Address6TemplateSubnetsegmentItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Address6TemplateObject: ...

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
        payload_dict: Address6TemplatePayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        ip6: str | None = ...,
        subnet_segment_count: int | None = ...,
        subnet_segment: str | list[str] | list[Address6TemplateSubnetsegmentItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
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
    "Address6Template",
    "Address6TemplatePayload",
    "Address6TemplateResponse",
    "Address6TemplateObject",
]