""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/x802_1x_settings
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

class X8021xSettingsPayload(TypedDict, total=False):
    """Payload type for X8021xSettings operations."""
    link_down_auth: Literal["set-unauth", "no-action"]
    reauth_period: int
    max_reauth_attempt: int
    tx_period: int
    mab_reauth: Literal["disable", "enable"]
    mac_username_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_password_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_calling_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_called_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_case: Literal["lowercase", "uppercase"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class X8021xSettingsResponse(TypedDict, total=False):
    """Response type for X8021xSettings - use with .dict property for typed dict access."""
    link_down_auth: Literal["set-unauth", "no-action"]
    reauth_period: int
    max_reauth_attempt: int
    tx_period: int
    mab_reauth: Literal["disable", "enable"]
    mac_username_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_password_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_calling_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_called_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_case: Literal["lowercase", "uppercase"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class X8021xSettingsObject(FortiObject):
    """Typed FortiObject for X8021xSettings with field access."""
    link_down_auth: Literal["set-unauth", "no-action"]
    reauth_period: int
    max_reauth_attempt: int
    tx_period: int
    mab_reauth: Literal["disable", "enable"]
    mac_username_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_password_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_calling_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_called_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"]
    mac_case: Literal["lowercase", "uppercase"]


# ================================================================
# Main Endpoint Class
# ================================================================

class X8021xSettings:
    """
    
    Endpoint: switch_controller/x802_1x_settings
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
    ) -> X8021xSettingsObject: ...
    
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
        payload_dict: X8021xSettingsPayload | None = ...,
        link_down_auth: Literal["set-unauth", "no-action"] | None = ...,
        reauth_period: int | None = ...,
        max_reauth_attempt: int | None = ...,
        tx_period: int | None = ...,
        mab_reauth: Literal["disable", "enable"] | None = ...,
        mac_username_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"] | None = ...,
        mac_password_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"] | None = ...,
        mac_calling_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"] | None = ...,
        mac_called_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"] | None = ...,
        mac_case: Literal["lowercase", "uppercase"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> X8021xSettingsObject: ...


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
        payload_dict: X8021xSettingsPayload | None = ...,
        link_down_auth: Literal["set-unauth", "no-action"] | None = ...,
        reauth_period: int | None = ...,
        max_reauth_attempt: int | None = ...,
        tx_period: int | None = ...,
        mab_reauth: Literal["disable", "enable"] | None = ...,
        mac_username_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"] | None = ...,
        mac_password_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"] | None = ...,
        mac_calling_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"] | None = ...,
        mac_called_station_delimiter: Literal["colon", "hyphen", "none", "single-hyphen"] | None = ...,
        mac_case: Literal["lowercase", "uppercase"] | None = ...,
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
    "X8021xSettings",
    "X8021xSettingsPayload",
    "X8021xSettingsResponse",
    "X8021xSettingsObject",
]