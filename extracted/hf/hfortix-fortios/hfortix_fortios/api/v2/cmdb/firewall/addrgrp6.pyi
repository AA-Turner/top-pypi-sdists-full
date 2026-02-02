""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/addrgrp6
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

class Addrgrp6TaggingTagsItem(TypedDict, total=False):
    """Nested item for tagging.tags field."""
    name: str


class Addrgrp6MemberItem(TypedDict, total=False):
    """Nested item for member field."""
    name: str


class Addrgrp6ExcludememberItem(TypedDict, total=False):
    """Nested item for exclude-member field."""
    name: str


class Addrgrp6TaggingItem(TypedDict, total=False):
    """Nested item for tagging field."""
    name: str
    category: str
    tags: str | list[str] | list[Addrgrp6TaggingTagsItem]


class Addrgrp6Payload(TypedDict, total=False):
    """Payload type for Addrgrp6 operations."""
    name: str
    uuid: str
    color: int
    comment: str
    member: str | list[str] | list[Addrgrp6MemberItem]
    exclude: Literal["enable", "disable"]
    exclude_member: str | list[str] | list[Addrgrp6ExcludememberItem]
    tagging: str | list[str] | list[Addrgrp6TaggingItem]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Addrgrp6Response(TypedDict, total=False):
    """Response type for Addrgrp6 - use with .dict property for typed dict access."""
    name: str
    uuid: str
    color: int
    comment: str
    member: list[Addrgrp6MemberItem]
    exclude: Literal["enable", "disable"]
    exclude_member: list[Addrgrp6ExcludememberItem]
    tagging: list[Addrgrp6TaggingItem]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Addrgrp6TaggingTagsItemObject(FortiObject[Addrgrp6TaggingTagsItem]):
    """Typed object for tagging.tags table items with attribute access."""
    name: str


class Addrgrp6MemberItemObject(FortiObject[Addrgrp6MemberItem]):
    """Typed object for member table items with attribute access."""
    name: str


class Addrgrp6ExcludememberItemObject(FortiObject[Addrgrp6ExcludememberItem]):
    """Typed object for exclude-member table items with attribute access."""
    name: str


class Addrgrp6TaggingItemObject(FortiObject[Addrgrp6TaggingItem]):
    """Typed object for tagging table items with attribute access."""
    name: str
    category: str
    tags: FortiObjectList[Addrgrp6TaggingTagsItemObject]


class Addrgrp6Object(FortiObject):
    """Typed FortiObject for Addrgrp6 with field access."""
    name: str
    uuid: str
    color: int
    comment: str
    member: FortiObjectList[Addrgrp6MemberItemObject]
    exclude: Literal["enable", "disable"]
    exclude_member: FortiObjectList[Addrgrp6ExcludememberItemObject]
    tagging: FortiObjectList[Addrgrp6TaggingItemObject]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Addrgrp6:
    """
    
    Endpoint: firewall/addrgrp6
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
    ) -> Addrgrp6Object: ...
    
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
    ) -> FortiObjectList[Addrgrp6Object]: ...
    
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
        payload_dict: Addrgrp6Payload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        color: int | None = ...,
        comment: str | None = ...,
        member: str | list[str] | list[Addrgrp6MemberItem] | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[Addrgrp6ExcludememberItem] | None = ...,
        tagging: str | list[str] | list[Addrgrp6TaggingItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Addrgrp6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Addrgrp6Payload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        color: int | None = ...,
        comment: str | None = ...,
        member: str | list[str] | list[Addrgrp6MemberItem] | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[Addrgrp6ExcludememberItem] | None = ...,
        tagging: str | list[str] | list[Addrgrp6TaggingItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Addrgrp6Object: ...

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
        payload_dict: Addrgrp6Payload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        color: int | None = ...,
        comment: str | None = ...,
        member: str | list[str] | list[Addrgrp6MemberItem] | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[Addrgrp6ExcludememberItem] | None = ...,
        tagging: str | list[str] | list[Addrgrp6TaggingItem] | None = ...,
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
    "Addrgrp6",
    "Addrgrp6Payload",
    "Addrgrp6Response",
    "Addrgrp6Object",
]