""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/apcfg_profile
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

class ApcfgProfileCommandlistItem(TypedDict, total=False):
    """Nested item for command-list field."""
    id: int
    type: Literal["non-password", "password"]
    name: str
    value: str
    passwd_value: str


class ApcfgProfilePayload(TypedDict, total=False):
    """Payload type for ApcfgProfile operations."""
    name: str
    ap_family: Literal["fap", "fap-u", "fap-c"]
    comment: str
    ac_type: Literal["default", "specify", "apcfg"]
    ac_timer: int
    ac_ip: str
    ac_port: int
    command_list: str | list[str] | list[ApcfgProfileCommandlistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ApcfgProfileResponse(TypedDict, total=False):
    """Response type for ApcfgProfile - use with .dict property for typed dict access."""
    name: str
    ap_family: Literal["fap", "fap-u", "fap-c"]
    comment: str
    ac_type: Literal["default", "specify", "apcfg"]
    ac_timer: int
    ac_ip: str
    ac_port: int
    command_list: list[ApcfgProfileCommandlistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ApcfgProfileCommandlistItemObject(FortiObject[ApcfgProfileCommandlistItem]):
    """Typed object for command-list table items with attribute access."""
    id: int
    type: Literal["non-password", "password"]
    name: str
    value: str
    passwd_value: str


class ApcfgProfileObject(FortiObject):
    """Typed FortiObject for ApcfgProfile with field access."""
    name: str
    ap_family: Literal["fap", "fap-u", "fap-c"]
    comment: str
    ac_type: Literal["default", "specify", "apcfg"]
    ac_timer: int
    ac_ip: str
    ac_port: int
    command_list: FortiObjectList[ApcfgProfileCommandlistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ApcfgProfile:
    """
    
    Endpoint: wireless_controller/apcfg_profile
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
    ) -> ApcfgProfileObject: ...
    
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
    ) -> FortiObjectList[ApcfgProfileObject]: ...
    
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
        payload_dict: ApcfgProfilePayload | None = ...,
        name: str | None = ...,
        ap_family: Literal["fap", "fap-u", "fap-c"] | None = ...,
        comment: str | None = ...,
        ac_type: Literal["default", "specify", "apcfg"] | None = ...,
        ac_timer: int | None = ...,
        ac_ip: str | None = ...,
        ac_port: int | None = ...,
        command_list: str | list[str] | list[ApcfgProfileCommandlistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ApcfgProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ApcfgProfilePayload | None = ...,
        name: str | None = ...,
        ap_family: Literal["fap", "fap-u", "fap-c"] | None = ...,
        comment: str | None = ...,
        ac_type: Literal["default", "specify", "apcfg"] | None = ...,
        ac_timer: int | None = ...,
        ac_ip: str | None = ...,
        ac_port: int | None = ...,
        command_list: str | list[str] | list[ApcfgProfileCommandlistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ApcfgProfileObject: ...

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
        payload_dict: ApcfgProfilePayload | None = ...,
        name: str | None = ...,
        ap_family: Literal["fap", "fap-u", "fap-c"] | None = ...,
        comment: str | None = ...,
        ac_type: Literal["default", "specify", "apcfg"] | None = ...,
        ac_timer: int | None = ...,
        ac_ip: str | None = ...,
        ac_port: int | None = ...,
        command_list: str | list[str] | list[ApcfgProfileCommandlistItem] | None = ...,
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
    "ApcfgProfile",
    "ApcfgProfilePayload",
    "ApcfgProfileResponse",
    "ApcfgProfileObject",
]