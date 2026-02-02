""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service_definition
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

class InternetServiceDefinitionEntryPortrangeItem(TypedDict, total=False):
    """Nested item for entry.port-range field."""
    id: int
    start_port: int
    end_port: int


class InternetServiceDefinitionEntryItem(TypedDict, total=False):
    """Nested item for entry field."""
    seq_num: int
    category_id: int
    name: str
    protocol: int
    port_range: str | list[str] | list[InternetServiceDefinitionEntryPortrangeItem]


class InternetServiceDefinitionPayload(TypedDict, total=False):
    """Payload type for InternetServiceDefinition operations."""
    id: int
    entry: str | list[str] | list[InternetServiceDefinitionEntryItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InternetServiceDefinitionResponse(TypedDict, total=False):
    """Response type for InternetServiceDefinition - use with .dict property for typed dict access."""
    id: int
    entry: list[InternetServiceDefinitionEntryItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InternetServiceDefinitionEntryPortrangeItemObject(FortiObject[InternetServiceDefinitionEntryPortrangeItem]):
    """Typed object for entry.port-range table items with attribute access."""
    id: int
    start_port: int
    end_port: int


class InternetServiceDefinitionEntryItemObject(FortiObject[InternetServiceDefinitionEntryItem]):
    """Typed object for entry table items with attribute access."""
    seq_num: int
    category_id: int
    name: str
    protocol: int
    port_range: FortiObjectList[InternetServiceDefinitionEntryPortrangeItemObject]


class InternetServiceDefinitionObject(FortiObject):
    """Typed FortiObject for InternetServiceDefinition with field access."""
    id: int
    entry: FortiObjectList[InternetServiceDefinitionEntryItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class InternetServiceDefinition:
    """
    
    Endpoint: firewall/internet_service_definition
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceDefinitionObject: ...
    
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
    ) -> FortiObjectList[InternetServiceDefinitionObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: InternetServiceDefinitionPayload | None = ...,
        id: int | None = ...,
        entry: str | list[str] | list[InternetServiceDefinitionEntryItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceDefinitionObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InternetServiceDefinitionPayload | None = ...,
        id: int | None = ...,
        entry: str | list[str] | list[InternetServiceDefinitionEntryItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceDefinitionObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InternetServiceDefinitionPayload | None = ...,
        id: int | None = ...,
        entry: str | list[str] | list[InternetServiceDefinitionEntryItem] | None = ...,
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
    "InternetServiceDefinition",
    "InternetServiceDefinitionPayload",
    "InternetServiceDefinitionResponse",
    "InternetServiceDefinitionObject",
]