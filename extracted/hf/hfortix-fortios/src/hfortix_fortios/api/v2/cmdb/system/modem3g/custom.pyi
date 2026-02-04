""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/modem3g/custom
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

class CustomPayload(TypedDict, total=False):
    """Payload type for Custom operations."""
    id: int
    vendor: str
    model: str
    vendor_id: str
    product_id: str
    class_id: str
    init_string: str
    modeswitch_string: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CustomResponse(TypedDict, total=False):
    """Response type for Custom - use with .dict property for typed dict access."""
    id: int
    vendor: str
    model: str
    vendor_id: str
    product_id: str
    class_id: str
    init_string: str
    modeswitch_string: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CustomObject(FortiObject):
    """Typed FortiObject for Custom with field access."""
    id: int
    vendor: str
    model: str
    vendor_id: str
    product_id: str
    class_id: str
    init_string: str
    modeswitch_string: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Custom:
    """
    
    Endpoint: system/modem3g/custom
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
    ) -> CustomObject: ...
    
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
        payload_dict: CustomPayload | None = ...,
        id: int | None = ...,
        vendor: str | None = ...,
        model: str | None = ...,
        vendor_id: str | None = ...,
        product_id: str | None = ...,
        class_id: str | None = ...,
        init_string: str | None = ...,
        modeswitch_string: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CustomObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CustomPayload | None = ...,
        id: int | None = ...,
        vendor: str | None = ...,
        model: str | None = ...,
        vendor_id: str | None = ...,
        product_id: str | None = ...,
        class_id: str | None = ...,
        init_string: str | None = ...,
        modeswitch_string: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CustomObject: ...

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
        payload_dict: CustomPayload | None = ...,
        id: int | None = ...,
        vendor: str | None = ...,
        model: str | None = ...,
        vendor_id: str | None = ...,
        product_id: str | None = ...,
        class_id: str | None = ...,
        init_string: str | None = ...,
        modeswitch_string: str | None = ...,
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
    "Custom",
    "CustomPayload",
    "CustomResponse",
    "CustomObject",
]