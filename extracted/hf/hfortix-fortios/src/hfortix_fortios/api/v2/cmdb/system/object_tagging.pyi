""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/object_tagging
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

class ObjectTaggingTagsItem(TypedDict, total=False):
    """Nested item for tags field."""
    name: str


class ObjectTaggingPayload(TypedDict, total=False):
    """Payload type for ObjectTagging operations."""
    category: str
    address: Literal["disable", "mandatory", "optional"]
    device: Literal["disable", "mandatory", "optional"]
    interface: Literal["disable", "mandatory", "optional"]
    multiple: Literal["enable", "disable"]
    color: int
    tags: str | list[str] | list[ObjectTaggingTagsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ObjectTaggingResponse(TypedDict, total=False):
    """Response type for ObjectTagging - use with .dict property for typed dict access."""
    category: str
    address: Literal["disable", "mandatory", "optional"]
    device: Literal["disable", "mandatory", "optional"]
    interface: Literal["disable", "mandatory", "optional"]
    multiple: Literal["enable", "disable"]
    color: int
    tags: list[ObjectTaggingTagsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ObjectTaggingTagsItemObject(FortiObject[ObjectTaggingTagsItem]):
    """Typed object for tags table items with attribute access."""
    name: str


class ObjectTaggingObject(FortiObject):
    """Typed FortiObject for ObjectTagging with field access."""
    category: str
    address: Literal["disable", "mandatory", "optional"]
    device: Literal["disable", "mandatory", "optional"]
    interface: Literal["disable", "mandatory", "optional"]
    multiple: Literal["enable", "disable"]
    color: int
    tags: FortiObjectList[ObjectTaggingTagsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ObjectTagging:
    """
    
    Endpoint: system/object_tagging
    Category: cmdb
    MKey: category
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
        category: str,
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
    ) -> ObjectTaggingObject: ...
    
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
    ) -> FortiObjectList[ObjectTaggingObject]: ...
    
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
        payload_dict: ObjectTaggingPayload | None = ...,
        category: str | None = ...,
        address: Literal["disable", "mandatory", "optional"] | None = ...,
        device: Literal["disable", "mandatory", "optional"] | None = ...,
        interface: Literal["disable", "mandatory", "optional"] | None = ...,
        multiple: Literal["enable", "disable"] | None = ...,
        color: int | None = ...,
        tags: str | list[str] | list[ObjectTaggingTagsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ObjectTaggingObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ObjectTaggingPayload | None = ...,
        category: str | None = ...,
        address: Literal["disable", "mandatory", "optional"] | None = ...,
        device: Literal["disable", "mandatory", "optional"] | None = ...,
        interface: Literal["disable", "mandatory", "optional"] | None = ...,
        multiple: Literal["enable", "disable"] | None = ...,
        color: int | None = ...,
        tags: str | list[str] | list[ObjectTaggingTagsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ObjectTaggingObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        category: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        category: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_category: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        category: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ObjectTaggingPayload | None = ...,
        category: str | None = ...,
        address: Literal["disable", "mandatory", "optional"] | None = ...,
        device: Literal["disable", "mandatory", "optional"] | None = ...,
        interface: Literal["disable", "mandatory", "optional"] | None = ...,
        multiple: Literal["enable", "disable"] | None = ...,
        color: int | None = ...,
        tags: str | list[str] | list[ObjectTaggingTagsItem] | None = ...,
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
    "ObjectTagging",
    "ObjectTaggingPayload",
    "ObjectTaggingResponse",
    "ObjectTaggingObject",
]