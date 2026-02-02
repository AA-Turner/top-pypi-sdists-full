""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/fsso_polling
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

class FssoPollingAdgrpItem(TypedDict, total=False):
    """Nested item for adgrp field."""
    name: str


class FssoPollingPayload(TypedDict, total=False):
    """Payload type for FssoPolling operations."""
    id: int
    status: Literal["enable", "disable"]
    server: str
    default_domain: str
    port: int
    user: str
    password: str
    ldap_server: str
    logon_history: int
    polling_frequency: int
    adgrp: str | list[str] | list[FssoPollingAdgrpItem]
    smbv1: Literal["enable", "disable"]
    smb_ntlmv1_auth: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FssoPollingResponse(TypedDict, total=False):
    """Response type for FssoPolling - use with .dict property for typed dict access."""
    id: int
    status: Literal["enable", "disable"]
    server: str
    default_domain: str
    port: int
    user: str
    password: str
    ldap_server: str
    logon_history: int
    polling_frequency: int
    adgrp: list[FssoPollingAdgrpItem]
    smbv1: Literal["enable", "disable"]
    smb_ntlmv1_auth: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FssoPollingAdgrpItemObject(FortiObject[FssoPollingAdgrpItem]):
    """Typed object for adgrp table items with attribute access."""
    name: str


class FssoPollingObject(FortiObject):
    """Typed FortiObject for FssoPolling with field access."""
    id: int
    status: Literal["enable", "disable"]
    server: str
    default_domain: str
    port: int
    user: str
    password: str
    ldap_server: str
    logon_history: int
    polling_frequency: int
    adgrp: FortiObjectList[FssoPollingAdgrpItemObject]
    smbv1: Literal["enable", "disable"]
    smb_ntlmv1_auth: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class FssoPolling:
    """
    
    Endpoint: user/fsso_polling
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> FssoPollingObject: ...
    
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
    ) -> FortiObjectList[FssoPollingObject]: ...
    
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
        payload_dict: FssoPollingPayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        default_domain: str | None = ...,
        port: int | None = ...,
        user: str | None = ...,
        password: str | None = ...,
        ldap_server: str | None = ...,
        logon_history: int | None = ...,
        polling_frequency: int | None = ...,
        adgrp: str | list[str] | list[FssoPollingAdgrpItem] | None = ...,
        smbv1: Literal["enable", "disable"] | None = ...,
        smb_ntlmv1_auth: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FssoPollingObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FssoPollingPayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        default_domain: str | None = ...,
        port: int | None = ...,
        user: str | None = ...,
        password: str | None = ...,
        ldap_server: str | None = ...,
        logon_history: int | None = ...,
        polling_frequency: int | None = ...,
        adgrp: str | list[str] | list[FssoPollingAdgrpItem] | None = ...,
        smbv1: Literal["enable", "disable"] | None = ...,
        smb_ntlmv1_auth: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FssoPollingObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FssoPollingPayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        default_domain: str | None = ...,
        port: int | None = ...,
        user: str | None = ...,
        password: str | None = ...,
        ldap_server: str | None = ...,
        logon_history: int | None = ...,
        polling_frequency: int | None = ...,
        adgrp: str | list[str] | list[FssoPollingAdgrpItem] | None = ...,
        smbv1: Literal["enable", "disable"] | None = ...,
        smb_ntlmv1_auth: Literal["enable", "disable"] | None = ...,
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
    "FssoPolling",
    "FssoPollingPayload",
    "FssoPollingResponse",
    "FssoPollingObject",
]