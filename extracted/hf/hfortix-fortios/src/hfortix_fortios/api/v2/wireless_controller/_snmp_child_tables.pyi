"""
Child Table Helper Type Stubs for wireless-controller/snmp

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class CommunityDict(TypedDict, total=False):
    """Type definition for community child table entry."""
    id: int
    name: str
    status: str | None
    query_v1_status: str | None
    query_v2c_status: str | None
    trap_v1_status: str | None
    trap_v2c_status: str | None
    hosts: list[Any] | None
    hosts6: list[Any] | None

class UserDict(TypedDict, total=False):
    """Type definition for user child table entry."""
    name: str
    status: str | None
    queries: str | None
    trap_status: str | None
    security_level: str | None
    auth_proto: str | None
    auth_pwd: str
    priv_proto: str | None
    priv_pwd: str
    notify_hosts: str | None
    notify_hosts6: str | None


class CommunityObject(FortiObject):
    """Typed FortiObject for community child table entry with attribute access."""
    id: int
    name: str
    status: str | None
    query_v1_status: str | None
    query_v2c_status: str | None
    trap_v1_status: str | None
    trap_v2c_status: str | None
    hosts: list[Any] | None
    hosts6: list[Any] | None


class UserObject(FortiObject):
    """Typed FortiObject for user child table entry with attribute access."""
    name: str
    status: str | None
    queries: str | None
    trap_status: str | None
    security_level: str | None
    auth_proto: str | None
    auth_pwd: str
    priv_proto: str | None
    priv_pwd: str
    notify_hosts: str | None
    notify_hosts6: str | None



class CommunityHelper:
    """Helper class for managing community child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[CommunityObject] | CommunityObject | None: ...
    
    def set(
        self,
        id: int,
        name: str,
        status: str | None = ...,
        query_v1_status: str | None = ...,
        query_v2c_status: str | None = ...,
        trap_v1_status: str | None = ...,
        trap_v2c_status: str | None = ...,
        hosts: list[Any] | None = ...,
        hosts6: list[Any] | None = ...,
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


class UserHelper:
    """Helper class for managing user child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[UserObject] | UserObject | None: ...
    
    def set(
        self,
        name: str,
        auth_pwd: str,
        priv_pwd: str,
        status: str | None = ...,
        queries: str | None = ...,
        trap_status: str | None = ...,
        security_level: str | None = ...,
        auth_proto: str | None = ...,
        priv_proto: str | None = ...,
        notify_hosts: str | None = ...,
        notify_hosts6: str | None = ...,
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

