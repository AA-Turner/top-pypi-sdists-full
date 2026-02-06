"""
Child Table Helper Type Stubs for system/acme

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class InterfaceDict(TypedDict, total=False):
    """Type definition for interface child table entry."""
    interface_name: str

class AccountsDict(TypedDict, total=False):
    """Type definition for accounts child table entry."""
    id: str | None
    status: str
    url: str
    ca_url: str
    email: str
    eab_key_id: str | None
    eab_key_hmac: str | None
    privatekey: str


class InterfaceObject(FortiObject):
    """Typed FortiObject for interface child table entry with attribute access."""
    interface_name: str


class AccountsObject(FortiObject):
    """Typed FortiObject for accounts child table entry with attribute access."""
    id: str | None
    status: str
    url: str
    ca_url: str
    email: str
    eab_key_id: str | None
    eab_key_hmac: str | None
    privatekey: str



class InterfaceHelper:
    """Helper class for managing interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        interface_name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[InterfaceObject] | InterfaceObject | None: ...
    
    def set(
        self,
        interface_name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        interface_name: str,
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
        interface_name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class AccountsHelper:
    """Helper class for managing accounts child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[AccountsObject] | AccountsObject | None: ...
    
    def set(
        self,
        status: str,
        url: str,
        ca_url: str,
        email: str,
        privatekey: str,
        id: str | None = ...,
        eab_key_id: str | None = ...,
        eab_key_hmac: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
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
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

