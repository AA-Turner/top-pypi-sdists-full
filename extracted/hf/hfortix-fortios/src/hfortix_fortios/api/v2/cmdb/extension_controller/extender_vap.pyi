""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: extension_controller/extender_vap
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

class ExtenderVapPayload(TypedDict, total=False):
    """Payload type for ExtenderVap operations."""
    name: str
    type: Literal["local-vap", "lan-ext-vap"]
    ssid: str
    max_clients: int
    broadcast_ssid: Literal["disable", "enable"]
    security: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"]
    dtim: int
    rts_threshold: int
    pmf: Literal["disabled", "optional", "required"]
    target_wake_time: Literal["disable", "enable"]
    bss_color_partial: Literal["disable", "enable"]
    mu_mimo: Literal["disable", "enable"]
    passphrase: str
    sae_password: str
    auth_server_address: str
    auth_server_port: int
    auth_server_secret: str
    ip_address: str
    start_ip: str
    end_ip: str
    allowaccess: str | list[str]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ExtenderVapResponse(TypedDict, total=False):
    """Response type for ExtenderVap - use with .dict property for typed dict access."""
    name: str
    type: Literal["local-vap", "lan-ext-vap"]
    ssid: str
    max_clients: int
    broadcast_ssid: Literal["disable", "enable"]
    security: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"]
    dtim: int
    rts_threshold: int
    pmf: Literal["disabled", "optional", "required"]
    target_wake_time: Literal["disable", "enable"]
    bss_color_partial: Literal["disable", "enable"]
    mu_mimo: Literal["disable", "enable"]
    passphrase: str
    sae_password: str
    auth_server_address: str
    auth_server_port: int
    auth_server_secret: str
    ip_address: str
    start_ip: str
    end_ip: str
    allowaccess: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ExtenderVapObject(FortiObject):
    """Typed FortiObject for ExtenderVap with field access."""
    name: str
    type: Literal["local-vap", "lan-ext-vap"]
    ssid: str
    max_clients: int
    broadcast_ssid: Literal["disable", "enable"]
    security: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"]
    dtim: int
    rts_threshold: int
    pmf: Literal["disabled", "optional", "required"]
    target_wake_time: Literal["disable", "enable"]
    bss_color_partial: Literal["disable", "enable"]
    mu_mimo: Literal["disable", "enable"]
    passphrase: str
    sae_password: str
    auth_server_address: str
    auth_server_port: int
    auth_server_secret: str
    ip_address: str
    start_ip: str
    end_ip: str
    allowaccess: str


# ================================================================
# Main Endpoint Class
# ================================================================

class ExtenderVap:
    """
    
    Endpoint: extension_controller/extender_vap
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
    ) -> ExtenderVapObject: ...
    
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
    ) -> FortiObjectList[ExtenderVapObject]: ...
    
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
        payload_dict: ExtenderVapPayload | None = ...,
        name: str | None = ...,
        type: Literal["local-vap", "lan-ext-vap"] | None = ...,
        ssid: str | None = ...,
        max_clients: int | None = ...,
        broadcast_ssid: Literal["disable", "enable"] | None = ...,
        security: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"] | None = ...,
        dtim: int | None = ...,
        rts_threshold: int | None = ...,
        pmf: Literal["disabled", "optional", "required"] | None = ...,
        target_wake_time: Literal["disable", "enable"] | None = ...,
        bss_color_partial: Literal["disable", "enable"] | None = ...,
        mu_mimo: Literal["disable", "enable"] | None = ...,
        passphrase: str | None = ...,
        sae_password: str | None = ...,
        auth_server_address: str | None = ...,
        auth_server_port: int | None = ...,
        auth_server_secret: str | None = ...,
        ip_address: str | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        allowaccess: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExtenderVapObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ExtenderVapPayload | None = ...,
        name: str | None = ...,
        type: Literal["local-vap", "lan-ext-vap"] | None = ...,
        ssid: str | None = ...,
        max_clients: int | None = ...,
        broadcast_ssid: Literal["disable", "enable"] | None = ...,
        security: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"] | None = ...,
        dtim: int | None = ...,
        rts_threshold: int | None = ...,
        pmf: Literal["disabled", "optional", "required"] | None = ...,
        target_wake_time: Literal["disable", "enable"] | None = ...,
        bss_color_partial: Literal["disable", "enable"] | None = ...,
        mu_mimo: Literal["disable", "enable"] | None = ...,
        passphrase: str | None = ...,
        sae_password: str | None = ...,
        auth_server_address: str | None = ...,
        auth_server_port: int | None = ...,
        auth_server_secret: str | None = ...,
        ip_address: str | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        allowaccess: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExtenderVapObject: ...

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
        payload_dict: ExtenderVapPayload | None = ...,
        name: str | None = ...,
        type: Literal["local-vap", "lan-ext-vap"] | None = ...,
        ssid: str | None = ...,
        max_clients: int | None = ...,
        broadcast_ssid: Literal["disable", "enable"] | None = ...,
        security: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"] | None = ...,
        dtim: int | None = ...,
        rts_threshold: int | None = ...,
        pmf: Literal["disabled", "optional", "required"] | None = ...,
        target_wake_time: Literal["disable", "enable"] | None = ...,
        bss_color_partial: Literal["disable", "enable"] | None = ...,
        mu_mimo: Literal["disable", "enable"] | None = ...,
        passphrase: str | None = ...,
        sae_password: str | None = ...,
        auth_server_address: str | None = ...,
        auth_server_port: int | None = ...,
        auth_server_secret: str | None = ...,
        ip_address: str | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
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
    "ExtenderVap",
    "ExtenderVapPayload",
    "ExtenderVapResponse",
    "ExtenderVapObject",
]