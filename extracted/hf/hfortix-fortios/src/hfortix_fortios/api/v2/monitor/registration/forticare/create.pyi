""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: registration/forticare/create
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

class CreatePayload(TypedDict, total=False):
    """Payload type for Create operations."""
    email: str
    password: str
    first_name: str
    last_name: str
    title: str
    company: str
    address: str
    city: str
    country_code: int
    state: str
    state_code: str
    postal_code: str
    phone: str
    industry: str
    industry_id: int
    orgsize_id: int
    reseller_name: str
    reseller_id: int
    is_government: bool


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CreateResponse(TypedDict, total=False):
    """Response type for Create - use with .dict property for typed dict access."""
    email: str
    password: str
    first_name: str
    last_name: str
    title: str
    company: str
    address: str
    city: str
    country_code: int
    state: str
    state_code: str
    postal_code: str
    phone: str
    industry: str
    industry_id: int
    orgsize_id: int
    reseller_name: str
    reseller_id: int
    is_government: bool


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CreateObject(FortiObject):
    """Typed FortiObject for Create with field access."""
    email: str
    password: str
    first_name: str
    last_name: str
    title: str
    company: str
    address: str
    city: str
    country_code: int
    state: str
    state_code: str
    postal_code: str
    phone: str
    industry: str
    industry_id: int
    orgsize_id: int
    reseller_name: str
    reseller_id: int
    is_government: bool


# ================================================================
# Main Endpoint Class
# ================================================================

class Create:
    """
    
    Endpoint: registration/forticare/create
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
    ) -> CreateObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: CreatePayload | None = ...,
        email: str | None = ...,
        password: str | None = ...,
        first_name: str | None = ...,
        last_name: str | None = ...,
        title: str | None = ...,
        company: str | None = ...,
        address: str | None = ...,
        city: str | None = ...,
        country_code: int | None = ...,
        state: str | None = ...,
        state_code: str | None = ...,
        postal_code: str | None = ...,
        phone: str | None = ...,
        industry: str | None = ...,
        industry_id: int | None = ...,
        orgsize_id: int | None = ...,
        reseller_name: str | None = ...,
        reseller_id: int | None = ...,
        is_government: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CreateObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CreatePayload | None = ...,
        email: str | None = ...,
        password: str | None = ...,
        first_name: str | None = ...,
        last_name: str | None = ...,
        title: str | None = ...,
        company: str | None = ...,
        address: str | None = ...,
        city: str | None = ...,
        country_code: int | None = ...,
        state: str | None = ...,
        state_code: str | None = ...,
        postal_code: str | None = ...,
        phone: str | None = ...,
        industry: str | None = ...,
        industry_id: int | None = ...,
        orgsize_id: int | None = ...,
        reseller_name: str | None = ...,
        reseller_id: int | None = ...,
        is_government: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CreateObject: ...




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
        payload_dict: CreatePayload | None = ...,
        email: str | None = ...,
        password: str | None = ...,
        first_name: str | None = ...,
        last_name: str | None = ...,
        title: str | None = ...,
        company: str | None = ...,
        address: str | None = ...,
        city: str | None = ...,
        country_code: int | None = ...,
        state: str | None = ...,
        state_code: str | None = ...,
        postal_code: str | None = ...,
        phone: str | None = ...,
        industry: str | None = ...,
        industry_id: int | None = ...,
        orgsize_id: int | None = ...,
        reseller_name: str | None = ...,
        reseller_id: int | None = ...,
        is_government: bool | None = ...,
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
    "Create",
    "CreatePayload",
    "CreateResponse",
    "CreateObject",
]