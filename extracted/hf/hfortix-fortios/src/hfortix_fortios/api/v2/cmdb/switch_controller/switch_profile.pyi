""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/switch_profile
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

class SwitchProfilePayload(TypedDict, total=False):
    """Payload type for SwitchProfile operations."""
    name: str
    login_passwd_override: Literal["enable", "disable"]
    login_passwd: str
    login: Literal["enable", "disable"]
    revision_backup_on_logout: Literal["enable", "disable"]
    revision_backup_on_upgrade: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SwitchProfileResponse(TypedDict, total=False):
    """Response type for SwitchProfile - use with .dict property for typed dict access."""
    name: str
    login_passwd_override: Literal["enable", "disable"]
    login_passwd: str
    login: Literal["enable", "disable"]
    revision_backup_on_logout: Literal["enable", "disable"]
    revision_backup_on_upgrade: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SwitchProfileObject(FortiObject):
    """Typed FortiObject for SwitchProfile with field access."""
    name: str
    login_passwd_override: Literal["enable", "disable"]
    login_passwd: str
    login: Literal["enable", "disable"]
    revision_backup_on_logout: Literal["enable", "disable"]
    revision_backup_on_upgrade: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class SwitchProfile:
    """
    
    Endpoint: switch_controller/switch_profile
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
    ) -> SwitchProfileObject: ...
    
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
    ) -> FortiObjectList[SwitchProfileObject]: ...
    
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
        payload_dict: SwitchProfilePayload | None = ...,
        name: str | None = ...,
        login_passwd_override: Literal["enable", "disable"] | None = ...,
        login_passwd: str | None = ...,
        login: Literal["enable", "disable"] | None = ...,
        revision_backup_on_logout: Literal["enable", "disable"] | None = ...,
        revision_backup_on_upgrade: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SwitchProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SwitchProfilePayload | None = ...,
        name: str | None = ...,
        login_passwd_override: Literal["enable", "disable"] | None = ...,
        login_passwd: str | None = ...,
        login: Literal["enable", "disable"] | None = ...,
        revision_backup_on_logout: Literal["enable", "disable"] | None = ...,
        revision_backup_on_upgrade: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SwitchProfileObject: ...

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
        payload_dict: SwitchProfilePayload | None = ...,
        name: str | None = ...,
        login_passwd_override: Literal["enable", "disable"] | None = ...,
        login_passwd: str | None = ...,
        login: Literal["enable", "disable"] | None = ...,
        revision_backup_on_logout: Literal["enable", "disable"] | None = ...,
        revision_backup_on_upgrade: Literal["enable", "disable"] | None = ...,
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
    "SwitchProfile",
    "SwitchProfilePayload",
    "SwitchProfileResponse",
    "SwitchProfileObject",
]