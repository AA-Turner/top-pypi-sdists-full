""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/multicast_address
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

class MulticastAddressTaggingTagsItem(TypedDict, total=False):
    """Nested item for tagging.tags field."""
    name: str


class MulticastAddressTaggingItem(TypedDict, total=False):
    """Nested item for tagging field."""
    name: str
    category: str
    tags: str | list[str] | list[MulticastAddressTaggingTagsItem]


class MulticastAddressPayload(TypedDict, total=False):
    """Payload type for MulticastAddress operations."""
    name: str
    type: Literal["multicastrange", "broadcastmask"]
    subnet: str
    start_ip: str
    end_ip: str
    comment: str
    associated_interface: str
    color: int
    tagging: str | list[str] | list[MulticastAddressTaggingItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class MulticastAddressResponse(TypedDict, total=False):
    """Response type for MulticastAddress - use with .dict property for typed dict access."""
    name: str
    type: Literal["multicastrange", "broadcastmask"]
    subnet: str
    start_ip: str
    end_ip: str
    comment: str
    associated_interface: str
    color: int
    tagging: list[MulticastAddressTaggingItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class MulticastAddressTaggingTagsItemObject(FortiObject[MulticastAddressTaggingTagsItem]):
    """Typed object for tagging.tags table items with attribute access."""
    name: str


class MulticastAddressTaggingItemObject(FortiObject[MulticastAddressTaggingItem]):
    """Typed object for tagging table items with attribute access."""
    name: str
    category: str
    tags: FortiObjectList[MulticastAddressTaggingTagsItemObject]


class MulticastAddressObject(FortiObject):
    """Typed FortiObject for MulticastAddress with field access."""
    name: str
    type: Literal["multicastrange", "broadcastmask"]
    subnet: str
    start_ip: str
    end_ip: str
    comment: str
    associated_interface: str
    color: int
    tagging: FortiObjectList[MulticastAddressTaggingItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class MulticastAddress:
    """
    
    Endpoint: firewall/multicast_address
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
    ) -> MulticastAddressObject: ...
    
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
    ) -> FortiObjectList[MulticastAddressObject]: ...
    
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
        payload_dict: MulticastAddressPayload | None = ...,
        name: str | None = ...,
        type: Literal["multicastrange", "broadcastmask"] | None = ...,
        subnet: str | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        comment: str | None = ...,
        associated_interface: str | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[MulticastAddressTaggingItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MulticastAddressObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: MulticastAddressPayload | None = ...,
        name: str | None = ...,
        type: Literal["multicastrange", "broadcastmask"] | None = ...,
        subnet: str | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        comment: str | None = ...,
        associated_interface: str | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[MulticastAddressTaggingItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MulticastAddressObject: ...

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
        payload_dict: MulticastAddressPayload | None = ...,
        name: str | None = ...,
        type: Literal["multicastrange", "broadcastmask"] | None = ...,
        subnet: str | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        comment: str | None = ...,
        associated_interface: str | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[MulticastAddressTaggingItem] | None = ...,
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
    "MulticastAddress",
    "MulticastAddressPayload",
    "MulticastAddressResponse",
    "MulticastAddressObject",
]