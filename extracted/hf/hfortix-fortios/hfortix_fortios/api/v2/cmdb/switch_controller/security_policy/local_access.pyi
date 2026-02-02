""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/security_policy/local_access
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

class LocalAccessPayload(TypedDict, total=False):
    """Payload type for LocalAccess operations."""
    name: str
    mgmt_allowaccess: str | list[str]
    internal_allowaccess: str | list[str]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LocalAccessResponse(TypedDict, total=False):
    """Response type for LocalAccess - use with .dict property for typed dict access."""
    name: str
    mgmt_allowaccess: str
    internal_allowaccess: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LocalAccessObject(FortiObject):
    """Typed FortiObject for LocalAccess with field access."""
    name: str
    mgmt_allowaccess: str
    internal_allowaccess: str


# ================================================================
# Main Endpoint Class
# ================================================================

class LocalAccess:
    """
    
    Endpoint: switch_controller/security_policy/local_access
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
    ) -> LocalAccessObject: ...
    
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
    ) -> FortiObjectList[LocalAccessObject]: ...
    
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
        payload_dict: LocalAccessPayload | None = ...,
        name: str | None = ...,
        mgmt_allowaccess: str | list[str] | None = ...,
        internal_allowaccess: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocalAccessObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LocalAccessPayload | None = ...,
        name: str | None = ...,
        mgmt_allowaccess: str | list[str] | None = ...,
        internal_allowaccess: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocalAccessObject: ...

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
        payload_dict: LocalAccessPayload | None = ...,
        name: str | None = ...,
        mgmt_allowaccess: Literal["https", "ping", "ssh", "snmp", "http", "telnet", "radius-acct"] | list[str] | None = ...,
        internal_allowaccess: Literal["https", "ping", "ssh", "snmp", "http", "telnet", "radius-acct"] | list[str] | None = ...,
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
    "LocalAccess",
    "LocalAccessPayload",
    "LocalAccessResponse",
    "LocalAccessObject",
]