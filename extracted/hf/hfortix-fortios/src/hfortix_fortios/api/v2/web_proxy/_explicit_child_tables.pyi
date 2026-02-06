"""
Child Table Helper Type Stubs for web-proxy/explicit

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class SecureWebProxyCertDict(TypedDict, total=False):
    """Type definition for secure_web_proxy_cert child table entry."""
    name: str | None

class PacPolicyDict(TypedDict, total=False):
    """Type definition for pac_policy child table entry."""
    policyid: int
    status: str | None
    srcaddr: list[Any]
    srcaddr6: list[Any] | None
    dstaddr: list[Any]
    pac_file_name: str
    pac_file_data: str | None
    comments: str | None


class SecureWebProxyCertObject(FortiObject):
    """Typed FortiObject for secure_web_proxy_cert child table entry with attribute access."""
    name: str | None


class PacPolicyObject(FortiObject):
    """Typed FortiObject for pac_policy child table entry with attribute access."""
    policyid: int
    status: str | None
    srcaddr: list[Any]
    srcaddr6: list[Any] | None
    dstaddr: list[Any]
    pac_file_name: str
    pac_file_data: str | None
    comments: str | None



class SecureWebProxyCertHelper:
    """Helper class for managing secure_web_proxy_cert child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[SecureWebProxyCertObject] | SecureWebProxyCertObject | None: ...
    
    def set(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
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
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class PacPolicyHelper:
    """Helper class for managing pac_policy child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        policyid: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[PacPolicyObject] | PacPolicyObject | None: ...
    
    def set(
        self,
        policyid: int,
        srcaddr: list[Any],
        dstaddr: list[Any],
        pac_file_name: str,
        status: str | None = ...,
        srcaddr6: list[Any] | None = ...,
        pac_file_data: str | None = ...,
        comments: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        policyid: str,
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
        policyid: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

