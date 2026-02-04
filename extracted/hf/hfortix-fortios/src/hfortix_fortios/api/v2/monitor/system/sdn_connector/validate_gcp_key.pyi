""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/sdn_connector/validate_gcp_key
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

class ValidateGcpKeyPayload(TypedDict, total=False):
    """Payload type for ValidateGcpKey operations."""
    private_key: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ValidateGcpKeyResponse(TypedDict, total=False):
    """Response type for ValidateGcpKey - use with .dict property for typed dict access."""
    private_key: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ValidateGcpKeyObject(FortiObject):
    """Typed FortiObject for ValidateGcpKey with field access."""
    private_key: str


# ================================================================
# Main Endpoint Class
# ================================================================

class ValidateGcpKey:
    """
    
    Endpoint: system/sdn_connector/validate_gcp_key
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
    ) -> ValidateGcpKeyObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: ValidateGcpKeyPayload | None = ...,
        private_key: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ValidateGcpKeyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ValidateGcpKeyPayload | None = ...,
        private_key: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ValidateGcpKeyObject: ...




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
        payload_dict: ValidateGcpKeyPayload | None = ...,
        private_key: str | None = ...,
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
    "ValidateGcpKey",
    "ValidateGcpKeyPayload",
    "ValidateGcpKeyResponse",
    "ValidateGcpKeyObject",
]