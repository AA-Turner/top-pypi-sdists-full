""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/lte_modem
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

class LteModemPayload(TypedDict, total=False):
    """Payload type for LteModem operations."""
    status: Literal["enable", "disable"]
    extra_init: str
    pdptype: Literal["IPv4"]
    authtype: Literal["none", "pap", "chap"]
    username: str
    passwd: str
    apn: str
    modem_port: int
    mode: Literal["standalone", "redundant"]
    holddown_timer: int
    interface: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LteModemResponse(TypedDict, total=False):
    """Response type for LteModem - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    extra_init: str
    pdptype: Literal["IPv4"]
    authtype: Literal["none", "pap", "chap"]
    username: str
    passwd: str
    apn: str
    modem_port: int
    mode: Literal["standalone", "redundant"]
    holddown_timer: int
    interface: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LteModemObject(FortiObject):
    """Typed FortiObject for LteModem with field access."""
    status: Literal["enable", "disable"]
    extra_init: str
    pdptype: Literal["IPv4"]
    authtype: Literal["none", "pap", "chap"]
    username: str
    passwd: str
    apn: str
    modem_port: int
    mode: Literal["standalone", "redundant"]
    holddown_timer: int
    interface: str


# ================================================================
# Main Endpoint Class
# ================================================================

class LteModem:
    """
    
    Endpoint: system/lte_modem
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
    ) -> LteModemObject: ...
    
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
        payload_dict: LteModemPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        extra_init: str | None = ...,
        pdptype: Literal["IPv4"] | None = ...,
        authtype: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        passwd: str | None = ...,
        apn: str | None = ...,
        modem_port: int | None = ...,
        mode: Literal["standalone", "redundant"] | None = ...,
        holddown_timer: int | None = ...,
        interface: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LteModemObject: ...


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
        payload_dict: LteModemPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        extra_init: str | None = ...,
        pdptype: Literal["IPv4"] | None = ...,
        authtype: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        passwd: str | None = ...,
        apn: str | None = ...,
        modem_port: int | None = ...,
        mode: Literal["standalone", "redundant"] | None = ...,
        holddown_timer: int | None = ...,
        interface: str | None = ...,
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
    "LteModem",
    "LteModemPayload",
    "LteModemResponse",
    "LteModemObject",
]