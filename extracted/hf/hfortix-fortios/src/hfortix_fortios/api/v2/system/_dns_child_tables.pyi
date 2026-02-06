"""
Child Table Helper Type Stubs for system/dns

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class ServerHostnameDict(TypedDict, total=False):
    """Type definition for server_hostname child table entry."""
    hostname: str

class DomainDict(TypedDict, total=False):
    """Type definition for domain child table entry."""
    domain: str


class ServerHostnameObject(FortiObject):
    """Typed FortiObject for server_hostname child table entry with attribute access."""
    hostname: str


class DomainObject(FortiObject):
    """Typed FortiObject for domain child table entry with attribute access."""
    domain: str



class ServerHostnameHelper:
    """Helper class for managing server_hostname child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        hostname: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[ServerHostnameObject] | ServerHostnameObject | None: ...
    
    def set(
        self,
        hostname: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        hostname: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        hostname: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class DomainHelper:
    """Helper class for managing domain child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        domain: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[DomainObject] | DomainObject | None: ...
    
    def set(
        self,
        domain: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        domain: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        domain: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

