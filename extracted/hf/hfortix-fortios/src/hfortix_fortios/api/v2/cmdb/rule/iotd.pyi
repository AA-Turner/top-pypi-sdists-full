""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: rule/iotd
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

class IotdParametersItem(TypedDict, total=False):
    """Nested item for parameters field."""
    name: str
    default_value: str


class IotdMetadataItem(TypedDict, total=False):
    """Nested item for metadata field."""
    id: int
    metaid: int
    valueid: int


class IotdPayload(TypedDict, total=False):
    """Payload type for Iotd operations."""
    name: str
    id: int
    category: int
    popularity: int
    risk: int
    weight: int
    protocol: str
    technology: str
    behavior: str
    vendor: str
    parameters: str | list[str] | list[IotdParametersItem]
    metadata: str | list[str] | list[IotdMetadataItem]
    status: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IotdResponse(TypedDict, total=False):
    """Response type for Iotd - use with .dict property for typed dict access."""
    name: str
    id: int
    category: int
    popularity: int
    risk: int
    weight: int
    protocol: str
    technology: str
    behavior: str
    vendor: str
    parameters: list[IotdParametersItem]
    metadata: list[IotdMetadataItem]
    status: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IotdParametersItemObject(FortiObject[IotdParametersItem]):
    """Typed object for parameters table items with attribute access."""
    name: str
    default_value: str


class IotdMetadataItemObject(FortiObject[IotdMetadataItem]):
    """Typed object for metadata table items with attribute access."""
    id: int
    metaid: int
    valueid: int


class IotdObject(FortiObject):
    """Typed FortiObject for Iotd with field access."""
    name: str
    id: int
    category: int
    popularity: int
    risk: int
    weight: int
    protocol: str
    technology: str
    behavior: str
    vendor: str
    parameters: FortiObjectList[IotdParametersItemObject]
    metadata: FortiObjectList[IotdMetadataItemObject]
    status: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Iotd:
    """
    
    Endpoint: rule/iotd
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
    ) -> IotdObject: ...
    
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
    ) -> FortiObjectList[IotdObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...




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
        payload_dict: IotdPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        category: int | None = ...,
        popularity: int | None = ...,
        risk: int | None = ...,
        weight: int | None = ...,
        protocol: str | None = ...,
        technology: str | None = ...,
        behavior: str | None = ...,
        vendor: str | None = ...,
        parameters: str | list[str] | list[IotdParametersItem] | None = ...,
        metadata: str | list[str] | list[IotdMetadataItem] | None = ...,
        status: str | None = ...,
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
    "Iotd",
    "IotdPayload",
    "IotdResponse",
    "IotdObject",
]