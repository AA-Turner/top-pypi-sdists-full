""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/anqp_network_auth_type
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

class AnqpNetworkAuthTypePayload(TypedDict, total=False):
    """Payload type for AnqpNetworkAuthType operations."""
    name: str
    auth_type: Literal["acceptance-of-terms", "online-enrollment", "http-redirection", "dns-redirection"]
    url: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AnqpNetworkAuthTypeResponse(TypedDict, total=False):
    """Response type for AnqpNetworkAuthType - use with .dict property for typed dict access."""
    name: str
    auth_type: Literal["acceptance-of-terms", "online-enrollment", "http-redirection", "dns-redirection"]
    url: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AnqpNetworkAuthTypeObject(FortiObject):
    """Typed FortiObject for AnqpNetworkAuthType with field access."""
    name: str
    auth_type: Literal["acceptance-of-terms", "online-enrollment", "http-redirection", "dns-redirection"]
    url: str


# ================================================================
# Main Endpoint Class
# ================================================================

class AnqpNetworkAuthType:
    """
    
    Endpoint: wireless_controller/hotspot20/anqp_network_auth_type
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
    ) -> AnqpNetworkAuthTypeObject: ...
    
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
    ) -> FortiObjectList[AnqpNetworkAuthTypeObject]: ...
    
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
        payload_dict: AnqpNetworkAuthTypePayload | None = ...,
        name: str | None = ...,
        auth_type: Literal["acceptance-of-terms", "online-enrollment", "http-redirection", "dns-redirection"] | None = ...,
        url: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AnqpNetworkAuthTypeObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AnqpNetworkAuthTypePayload | None = ...,
        name: str | None = ...,
        auth_type: Literal["acceptance-of-terms", "online-enrollment", "http-redirection", "dns-redirection"] | None = ...,
        url: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AnqpNetworkAuthTypeObject: ...

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
        payload_dict: AnqpNetworkAuthTypePayload | None = ...,
        name: str | None = ...,
        auth_type: Literal["acceptance-of-terms", "online-enrollment", "http-redirection", "dns-redirection"] | None = ...,
        url: str | None = ...,
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
    "AnqpNetworkAuthType",
    "AnqpNetworkAuthTypePayload",
    "AnqpNetworkAuthTypeResponse",
    "AnqpNetworkAuthTypeObject",
]