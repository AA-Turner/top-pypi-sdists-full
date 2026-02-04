""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/key_chain
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

class KeyChainKeyItem(TypedDict, total=False):
    """Nested item for key field."""
    id: str
    accept_lifetime: str
    send_lifetime: str
    key_string: str
    algorithm: Literal["md5", "hmac-sha1", "hmac-sha256", "hmac-sha384", "hmac-sha512", "cmac-aes128"]


class KeyChainPayload(TypedDict, total=False):
    """Payload type for KeyChain operations."""
    name: str
    key: str | list[str] | list[KeyChainKeyItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class KeyChainResponse(TypedDict, total=False):
    """Response type for KeyChain - use with .dict property for typed dict access."""
    name: str
    key: list[KeyChainKeyItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class KeyChainKeyItemObject(FortiObject[KeyChainKeyItem]):
    """Typed object for key table items with attribute access."""
    id: str
    accept_lifetime: str
    send_lifetime: str
    key_string: str
    algorithm: Literal["md5", "hmac-sha1", "hmac-sha256", "hmac-sha384", "hmac-sha512", "cmac-aes128"]


class KeyChainObject(FortiObject):
    """Typed FortiObject for KeyChain with field access."""
    name: str
    key: FortiObjectList[KeyChainKeyItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class KeyChain:
    """
    
    Endpoint: router/key_chain
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
    ) -> KeyChainObject: ...
    
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
    ) -> FortiObjectList[KeyChainObject]: ...
    
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
        payload_dict: KeyChainPayload | None = ...,
        name: str | None = ...,
        key: str | list[str] | list[KeyChainKeyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> KeyChainObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: KeyChainPayload | None = ...,
        name: str | None = ...,
        key: str | list[str] | list[KeyChainKeyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> KeyChainObject: ...

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
        payload_dict: KeyChainPayload | None = ...,
        name: str | None = ...,
        key: str | list[str] | list[KeyChainKeyItem] | None = ...,
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
    "KeyChain",
    "KeyChainPayload",
    "KeyChainResponse",
    "KeyChainObject",
]