""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/security_policy/update_global_label
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

class UpdateGlobalLabelPayload(TypedDict, total=False):
    """Payload type for UpdateGlobalLabel operations."""
    policyid: str
    current_label: str
    new_label: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class UpdateGlobalLabelResponse(TypedDict, total=False):
    """Response type for UpdateGlobalLabel - use with .dict property for typed dict access."""
    policyid: str
    current_label: str
    new_label: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class UpdateGlobalLabelObject(FortiObject):
    """Typed FortiObject for UpdateGlobalLabel with field access."""
    policyid: str
    current_label: str
    new_label: str


# ================================================================
# Main Endpoint Class
# ================================================================

class UpdateGlobalLabel:
    """
    
    Endpoint: firewall/security_policy/update_global_label
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
    ) -> UpdateGlobalLabelObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: UpdateGlobalLabelPayload | None = ...,
        policyid: str | None = ...,
        current_label: str | None = ...,
        new_label: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UpdateGlobalLabelObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: UpdateGlobalLabelPayload | None = ...,
        policyid: str | None = ...,
        current_label: str | None = ...,
        new_label: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UpdateGlobalLabelObject: ...


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
        payload_dict: UpdateGlobalLabelPayload | None = ...,
        policyid: str | None = ...,
        current_label: str | None = ...,
        new_label: str | None = ...,
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
    "UpdateGlobalLabel",
    "UpdateGlobalLabelPayload",
    "UpdateGlobalLabelResponse",
    "UpdateGlobalLabelObject",
]