""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/ssl/setting
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
    proxy_connect_timeout: int
    ssl_dh_bits: Literal["768", "1024", "1536", "2048"]
    ssl_send_empty_frags: Literal["enable", "disable"]
    no_matching_cipher_action: Literal["bypass", "drop"]
    cert_manager_cache_timeout: int
    resigned_short_lived_certificate: Literal["enable", "disable"]
    cert_cache_capacity: int
    cert_cache_timeout: int
    session_cache_capacity: int
    session_cache_timeout: int
    abbreviate_handshake: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SettingResponse(TypedDict, total=False):
    """Response type for Setting - use with .dict property for typed dict access."""
    proxy_connect_timeout: int
    ssl_dh_bits: Literal["768", "1024", "1536", "2048"]
    ssl_send_empty_frags: Literal["enable", "disable"]
    no_matching_cipher_action: Literal["bypass", "drop"]
    cert_manager_cache_timeout: int
    resigned_short_lived_certificate: Literal["enable", "disable"]
    cert_cache_capacity: int
    cert_cache_timeout: int
    session_cache_capacity: int
    session_cache_timeout: int
    abbreviate_handshake: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SettingObject(FortiObject):
    """Typed FortiObject for Setting with field access."""
    proxy_connect_timeout: int
    ssl_dh_bits: Literal["768", "1024", "1536", "2048"]
    ssl_send_empty_frags: Literal["enable", "disable"]
    no_matching_cipher_action: Literal["bypass", "drop"]
    cert_manager_cache_timeout: int
    resigned_short_lived_certificate: Literal["enable", "disable"]
    cert_cache_capacity: int
    cert_cache_timeout: int
    session_cache_capacity: int
    session_cache_timeout: int
    abbreviate_handshake: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Setting:
    """
    
    Endpoint: firewall/ssl/setting
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SettingObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SettingPayload | None = ...,
        proxy_connect_timeout: int | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048"] | None = ...,
        ssl_send_empty_frags: Literal["enable", "disable"] | None = ...,
        no_matching_cipher_action: Literal["bypass", "drop"] | None = ...,
        cert_manager_cache_timeout: int | None = ...,
        resigned_short_lived_certificate: Literal["enable", "disable"] | None = ...,
        cert_cache_capacity: int | None = ...,
        cert_cache_timeout: int | None = ...,
        session_cache_capacity: int | None = ...,
        session_cache_timeout: int | None = ...,
        abbreviate_handshake: Literal["enable", "disable"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SettingObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SettingPayload | None = ...,
        proxy_connect_timeout: int | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048"] | None = ...,
        ssl_send_empty_frags: Literal["enable", "disable"] | None = ...,
        no_matching_cipher_action: Literal["bypass", "drop"] | None = ...,
        cert_manager_cache_timeout: int | None = ...,
        resigned_short_lived_certificate: Literal["enable", "disable"] | None = ...,
        cert_cache_capacity: int | None = ...,
        cert_cache_timeout: int | None = ...,
        session_cache_capacity: int | None = ...,
        session_cache_timeout: int | None = ...,
        abbreviate_handshake: Literal["enable", "disable"] | None = ...,
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