""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/gtp/flush
Category: monitor
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

class FlushPayload(TypedDict, total=False):
    """Payload type for Flush operations."""
    scope: Literal["global", "vdom"]
    gtp_profile: str
    version: int
    imsi: str
    msisdn: str
    ms_addr: str
    ms_addr6: str
    cteid: int
    cteid_addr: str
    cteid_addr6: str
    fteid: int
    fteid_addr: str
    fteid_addr6: str
    apn: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FlushResponse(TypedDict, total=False):
    """Response type for Flush - use with .dict property for typed dict access."""
    scope: Literal["global", "vdom"]
    gtp_profile: str
    version: int
    imsi: str
    msisdn: str
    ms_addr: str
    ms_addr6: str
    cteid: int
    cteid_addr: str
    cteid_addr6: str
    fteid: int
    fteid_addr: str
    fteid_addr6: str
    apn: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FlushObject(FortiObject):
    """Typed FortiObject for Flush with field access."""
    scope: Literal["global", "vdom"]
    gtp_profile: str
    imsi: str
    msisdn: str
    ms_addr: str
    ms_addr6: str
    cteid: int
    cteid_addr: str
    cteid_addr6: str
    fteid: int
    fteid_addr: str
    fteid_addr6: str
    apn: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Flush:
    """
    
    Endpoint: firewall/gtp/flush
    Category: monitor
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
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FlushObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: FlushPayload | None = ...,
        scope: Literal["global", "vdom"] | None = ...,
        gtp_profile: str | None = ...,
        version: int | None = ...,
        imsi: str | None = ...,
        msisdn: str | None = ...,
        ms_addr: str | None = ...,
        ms_addr6: str | None = ...,
        cteid: int | None = ...,
        cteid_addr: str | None = ...,
        cteid_addr6: str | None = ...,
        fteid: int | None = ...,
        fteid_addr: str | None = ...,
        fteid_addr6: str | None = ...,
        apn: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FlushObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FlushPayload | None = ...,
        scope: Literal["global", "vdom"] | None = ...,
        gtp_profile: str | None = ...,
        version: int | None = ...,
        imsi: str | None = ...,
        msisdn: str | None = ...,
        ms_addr: str | None = ...,
        ms_addr6: str | None = ...,
        cteid: int | None = ...,
        cteid_addr: str | None = ...,
        cteid_addr6: str | None = ...,
        fteid: int | None = ...,
        fteid_addr: str | None = ...,
        fteid_addr6: str | None = ...,
        apn: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FlushObject: ...




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
        payload_dict: FlushPayload | None = ...,
        scope: Literal["global", "vdom"] | None = ...,
        gtp_profile: str | None = ...,
        version: int | None = ...,
        imsi: str | None = ...,
        msisdn: str | None = ...,
        ms_addr: str | None = ...,
        ms_addr6: str | None = ...,
        cteid: int | None = ...,
        cteid_addr: str | None = ...,
        cteid_addr6: str | None = ...,
        fteid: int | None = ...,
        fteid_addr: str | None = ...,
        fteid_addr6: str | None = ...,
        apn: str | None = ...,
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
    "Flush",
    "FlushPayload",
    "FlushResponse",
    "FlushObject",
]