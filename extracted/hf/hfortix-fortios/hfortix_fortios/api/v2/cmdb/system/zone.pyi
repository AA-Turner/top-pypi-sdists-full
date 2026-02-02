""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/zone
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

class ZoneTaggingTagsItem(TypedDict, total=False):
    """Nested item for tagging.tags field."""
    name: str


class ZoneTaggingItem(TypedDict, total=False):
    """Nested item for tagging field."""
    name: str
    category: str
    tags: str | list[str] | list[ZoneTaggingTagsItem]


class ZoneInterfaceItem(TypedDict, total=False):
    """Nested item for interface field."""
    interface_name: str


class ZonePayload(TypedDict, total=False):
    """Payload type for Zone operations."""
    name: str
    tagging: str | list[str] | list[ZoneTaggingItem]
    description: str
    intrazone: Literal["allow", "deny"]
    interface: str | list[str] | list[ZoneInterfaceItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ZoneResponse(TypedDict, total=False):
    """Response type for Zone - use with .dict property for typed dict access."""
    name: str
    tagging: list[ZoneTaggingItem]
    description: str
    intrazone: Literal["allow", "deny"]
    interface: list[ZoneInterfaceItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ZoneTaggingTagsItemObject(FortiObject[ZoneTaggingTagsItem]):
    """Typed object for tagging.tags table items with attribute access."""
    name: str


class ZoneTaggingItemObject(FortiObject[ZoneTaggingItem]):
    """Typed object for tagging table items with attribute access."""
    name: str
    category: str
    tags: FortiObjectList[ZoneTaggingTagsItemObject]


class ZoneInterfaceItemObject(FortiObject[ZoneInterfaceItem]):
    """Typed object for interface table items with attribute access."""
    interface_name: str


class ZoneObject(FortiObject):
    """Typed FortiObject for Zone with field access."""
    name: str
    tagging: FortiObjectList[ZoneTaggingItemObject]
    description: str
    intrazone: Literal["allow", "deny"]
    interface: FortiObjectList[ZoneInterfaceItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Zone:
    """
    
    Endpoint: system/zone
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
    ) -> ZoneObject: ...
    
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
    ) -> FortiObjectList[ZoneObject]: ...
    
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
        payload_dict: ZonePayload | None = ...,
        name: str | None = ...,
        tagging: str | list[str] | list[ZoneTaggingItem] | None = ...,
        description: str | None = ...,
        intrazone: Literal["allow", "deny"] | None = ...,
        interface: str | list[str] | list[ZoneInterfaceItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ZoneObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ZonePayload | None = ...,
        name: str | None = ...,
        tagging: str | list[str] | list[ZoneTaggingItem] | None = ...,
        description: str | None = ...,
        intrazone: Literal["allow", "deny"] | None = ...,
        interface: str | list[str] | list[ZoneInterfaceItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ZoneObject: ...

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
        payload_dict: ZonePayload | None = ...,
        name: str | None = ...,
        tagging: str | list[str] | list[ZoneTaggingItem] | None = ...,
        description: str | None = ...,
        intrazone: Literal["allow", "deny"] | None = ...,
        interface: str | list[str] | list[ZoneInterfaceItem] | None = ...,
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
    "Zone",
    "ZonePayload",
    "ZoneResponse",
    "ZoneObject",
]