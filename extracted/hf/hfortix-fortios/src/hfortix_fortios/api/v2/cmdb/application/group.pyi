""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: application/group
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

class GroupApplicationItem(TypedDict, total=False):
    """Nested item for application field."""
    id: int


class GroupCategoryItem(TypedDict, total=False):
    """Nested item for category field."""
    id: int


class GroupRiskItem(TypedDict, total=False):
    """Nested item for risk field."""
    level: int


class GroupPayload(TypedDict, total=False):
    """Payload type for Group operations."""
    name: str
    comment: str
    type: Literal["application", "filter"]
    application: str | list[str] | list[GroupApplicationItem]
    category: str | list[str] | list[GroupCategoryItem]
    risk: str | list[str] | list[GroupRiskItem]
    protocols: str | list[str]
    vendor: str | list[str]
    technology: str | list[str]
    behavior: str | list[str]
    popularity: str | list[str]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GroupResponse(TypedDict, total=False):
    """Response type for Group - use with .dict property for typed dict access."""
    name: str
    comment: str
    type: Literal["application", "filter"]
    application: list[GroupApplicationItem]
    category: list[GroupCategoryItem]
    risk: list[GroupRiskItem]
    protocols: str | list[str]
    vendor: str | list[str]
    technology: str | list[str]
    behavior: str | list[str]
    popularity: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GroupApplicationItemObject(FortiObject[GroupApplicationItem]):
    """Typed object for application table items with attribute access."""
    id: int


class GroupCategoryItemObject(FortiObject[GroupCategoryItem]):
    """Typed object for category table items with attribute access."""
    id: int


class GroupRiskItemObject(FortiObject[GroupRiskItem]):
    """Typed object for risk table items with attribute access."""
    level: int


class GroupObject(FortiObject):
    """Typed FortiObject for Group with field access."""
    name: str
    comment: str
    type: Literal["application", "filter"]
    application: FortiObjectList[GroupApplicationItemObject]
    category: FortiObjectList[GroupCategoryItemObject]
    risk: FortiObjectList[GroupRiskItemObject]
    protocols: str | list[str]
    vendor: str | list[str]
    technology: str | list[str]
    behavior: str | list[str]
    popularity: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Group:
    """
    
    Endpoint: application/group
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
    ) -> GroupObject: ...
    
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
    ) -> FortiObjectList[GroupObject]: ...
    
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
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[GroupApplicationItem] | None = ...,
        category: str | list[str] | list[GroupCategoryItem] | None = ...,
        risk: str | list[str] | list[GroupRiskItem] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GroupObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[GroupApplicationItem] | None = ...,
        category: str | list[str] | list[GroupCategoryItem] | None = ...,
        risk: str | list[str] | list[GroupRiskItem] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GroupObject: ...

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
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[GroupApplicationItem] | None = ...,
        category: str | list[str] | list[GroupCategoryItem] | None = ...,
        risk: str | list[str] | list[GroupRiskItem] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
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
    "Group",
    "GroupPayload",
    "GroupResponse",
    "GroupObject",
]