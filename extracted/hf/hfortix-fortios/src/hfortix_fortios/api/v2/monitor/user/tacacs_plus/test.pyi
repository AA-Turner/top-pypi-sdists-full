""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/tacacs_plus/test
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

class TestPayload(TypedDict, total=False):
    """Payload type for Test operations."""
    mkey: str
    ordinal: str
    server: str
    secret: str
    port: int
    source_ip: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class TestResponse(TypedDict, total=False):
    """Response type for Test - use with .dict property for typed dict access."""
    status: int
    message: str


class TestObject(FortiObject[TestResponse]):
    """Typed FortiObject for Test with field access."""
    status: int
    message: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Test:
    """
    
    Endpoint: user/tacacs_plus/test
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
    ) -> FortiObjectList[TestObject]: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: TestPayload | None = ...,
        mkey: str | None = ...,
        ordinal: str | None = ...,
        server: str | None = ...,
        secret: str | None = ...,
        port: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TestObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: TestPayload | None = ...,
        mkey: str | None = ...,
        ordinal: str | None = ...,
        server: str | None = ...,
        secret: str | None = ...,
        port: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TestObject: ...




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
        payload_dict: TestPayload | None = ...,
        mkey: str | None = ...,
        ordinal: str | None = ...,
        server: str | None = ...,
        secret: str | None = ...,
        port: int | None = ...,
        source_ip: str | None = ...,
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
    "Test",
    "TestResponse",
    "TestObject",
]