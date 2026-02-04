""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: dlp/label
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

class LabelEntriesItem(TypedDict, total=False):
    """Nested item for entries field."""
    id: int
    fortidata_label_name: str
    mpip_label_name: str
    guid: str


class LabelPayload(TypedDict, total=False):
    """Payload type for Label operations."""
    name: str
    type: Literal["mpip", "fortidata"]
    mpip_type: Literal["remote", "local"]
    connector: str
    comment: str
    entries: str | list[str] | list[LabelEntriesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LabelResponse(TypedDict, total=False):
    """Response type for Label - use with .dict property for typed dict access."""
    name: str
    type: Literal["mpip", "fortidata"]
    mpip_type: Literal["remote", "local"]
    connector: str
    comment: str
    entries: list[LabelEntriesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LabelEntriesItemObject(FortiObject[LabelEntriesItem]):
    """Typed object for entries table items with attribute access."""
    id: int
    fortidata_label_name: str
    mpip_label_name: str
    guid: str


class LabelObject(FortiObject):
    """Typed FortiObject for Label with field access."""
    name: str
    type: Literal["mpip", "fortidata"]
    mpip_type: Literal["remote", "local"]
    connector: str
    comment: str
    entries: FortiObjectList[LabelEntriesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Label:
    """
    
    Endpoint: dlp/label
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
    ) -> LabelObject: ...
    
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
    ) -> FortiObjectList[LabelObject]: ...
    
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
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[LabelEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LabelObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[LabelEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LabelObject: ...

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
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[LabelEntriesItem] | None = ...,
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
    "Label",
    "LabelPayload",
    "LabelResponse",
    "LabelObject",
]