""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/addrgrp
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

class AddrgrpTaggingTagsItem(TypedDict, total=False):
    """Nested item for tagging.tags field."""
    name: str


class AddrgrpMemberItem(TypedDict, total=False):
    """Nested item for member field."""
    name: str


class AddrgrpExcludememberItem(TypedDict, total=False):
    """Nested item for exclude-member field."""
    name: str


class AddrgrpTaggingItem(TypedDict, total=False):
    """Nested item for tagging field."""
    name: str
    category: str
    tags: str | list[str] | list[AddrgrpTaggingTagsItem]


class AddrgrpPayload(TypedDict, total=False):
    """Payload type for Addrgrp operations."""
    name: str
    type: Literal["default", "folder"]
    category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"]
    allow_routing: Literal["enable", "disable"]
    member: str | list[str] | list[AddrgrpMemberItem]
    comment: str
    uuid: str
    exclude: Literal["enable", "disable"]
    exclude_member: str | list[str] | list[AddrgrpExcludememberItem]
    color: int
    tagging: str | list[str] | list[AddrgrpTaggingItem]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AddrgrpResponse(TypedDict, total=False):
    """Response type for Addrgrp - use with .dict property for typed dict access."""
    name: str
    type: Literal["default", "folder"]
    category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"]
    allow_routing: Literal["enable", "disable"]
    member: list[AddrgrpMemberItem]
    comment: str
    uuid: str
    exclude: Literal["enable", "disable"]
    exclude_member: list[AddrgrpExcludememberItem]
    color: int
    tagging: list[AddrgrpTaggingItem]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AddrgrpTaggingTagsItemObject(FortiObject[AddrgrpTaggingTagsItem]):
    """Typed object for tagging.tags table items with attribute access."""
    name: str


class AddrgrpMemberItemObject(FortiObject[AddrgrpMemberItem]):
    """Typed object for member table items with attribute access."""
    name: str


class AddrgrpExcludememberItemObject(FortiObject[AddrgrpExcludememberItem]):
    """Typed object for exclude-member table items with attribute access."""
    name: str


class AddrgrpTaggingItemObject(FortiObject[AddrgrpTaggingItem]):
    """Typed object for tagging table items with attribute access."""
    name: str
    category: str
    tags: FortiObjectList[AddrgrpTaggingTagsItemObject]


class AddrgrpObject(FortiObject):
    """Typed FortiObject for Addrgrp with field access."""
    name: str
    type: Literal["default", "folder"]
    category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"]
    allow_routing: Literal["enable", "disable"]
    member: FortiObjectList[AddrgrpMemberItemObject]
    comment: str
    uuid: str
    exclude: Literal["enable", "disable"]
    exclude_member: FortiObjectList[AddrgrpExcludememberItemObject]
    color: int
    tagging: FortiObjectList[AddrgrpTaggingItemObject]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Addrgrp:
    """
    
    Endpoint: firewall/addrgrp
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
    ) -> AddrgrpObject: ...
    
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
    ) -> FortiObjectList[AddrgrpObject]: ...
    
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
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[AddrgrpMemberItem] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[AddrgrpExcludememberItem] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[AddrgrpTaggingItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AddrgrpObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[AddrgrpMemberItem] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[AddrgrpExcludememberItem] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[AddrgrpTaggingItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AddrgrpObject: ...

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
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[AddrgrpMemberItem] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[AddrgrpExcludememberItem] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[AddrgrpTaggingItem] | None = ...,
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
    "Addrgrp",
    "AddrgrpPayload",
    "AddrgrpResponse",
    "AddrgrpObject",
]