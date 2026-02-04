""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/ssh/setting
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class SettingPayload(TypedDict, total=False):
    """Payload type for Setting operations."""
    caname: str
    untrusted_caname: str
    hostkey_rsa2048: str
    hostkey_dsa1024: str
    hostkey_ecdsa256: str
    hostkey_ecdsa384: str
    hostkey_ecdsa521: str
    hostkey_ed25519: str
    host_trusted_checking: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SettingResponse(TypedDict, total=False):
    """Response type for Setting - use with .dict property for typed dict access."""
    caname: str
    untrusted_caname: str
    hostkey_rsa2048: str
    hostkey_dsa1024: str
    hostkey_ecdsa256: str
    hostkey_ecdsa384: str
    hostkey_ecdsa521: str
    hostkey_ed25519: str
    host_trusted_checking: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SettingObject(FortiObject):
    """Typed FortiObject for Setting with field access."""
    caname: str
    untrusted_caname: str
    hostkey_rsa2048: str
    hostkey_dsa1024: str
    hostkey_ecdsa256: str
    hostkey_ecdsa384: str
    hostkey_ecdsa521: str
    hostkey_ed25519: str
    host_trusted_checking: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Setting:
    """
    
    Endpoint: firewall/ssh/setting
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Singleton endpoint (no mkey)
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
    ) -> SettingObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SettingPayload | None = ...,
        caname: str | None = ...,
        untrusted_caname: str | None = ...,
        hostkey_rsa2048: str | None = ...,
        hostkey_dsa1024: str | None = ...,
        hostkey_ecdsa256: str | None = ...,
        hostkey_ecdsa384: str | None = ...,
        hostkey_ecdsa521: str | None = ...,
        hostkey_ed25519: str | None = ...,
        host_trusted_checking: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SettingObject: ...


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
        payload_dict: SettingPayload | None = ...,
        caname: str | None = ...,
        untrusted_caname: str | None = ...,
        hostkey_rsa2048: str | None = ...,
        hostkey_dsa1024: str | None = ...,
        hostkey_ecdsa256: str | None = ...,
        hostkey_ecdsa384: str | None = ...,
        hostkey_ecdsa521: str | None = ...,
        hostkey_ed25519: str | None = ...,
        host_trusted_checking: Literal["enable", "disable"] | None = ...,
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
    "Setting",
    "SettingPayload",
    "SettingResponse",
    "SettingObject",
]