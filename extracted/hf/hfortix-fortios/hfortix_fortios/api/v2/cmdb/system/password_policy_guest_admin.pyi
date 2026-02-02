""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/password_policy_guest_admin
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

class PasswordPolicyGuestAdminPayload(TypedDict, total=False):
    """Payload type for PasswordPolicyGuestAdmin operations."""
    status: Literal["enable", "disable"]
    apply_to: str | list[str]
    minimum_length: int
    min_lower_case_letter: int
    min_upper_case_letter: int
    min_non_alphanumeric: int
    min_number: int
    expire_status: Literal["enable", "disable"]
    expire_day: int
    reuse_password: Literal["enable", "disable"]
    reuse_password_limit: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class PasswordPolicyGuestAdminResponse(TypedDict, total=False):
    """Response type for PasswordPolicyGuestAdmin - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    apply_to: str
    minimum_length: int
    min_lower_case_letter: int
    min_upper_case_letter: int
    min_non_alphanumeric: int
    min_number: int
    expire_status: Literal["enable", "disable"]
    expire_day: int
    reuse_password: Literal["enable", "disable"]
    reuse_password_limit: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class PasswordPolicyGuestAdminObject(FortiObject):
    """Typed FortiObject for PasswordPolicyGuestAdmin with field access."""
    status: Literal["enable", "disable"]
    apply_to: str
    minimum_length: int
    min_lower_case_letter: int
    min_upper_case_letter: int
    min_non_alphanumeric: int
    min_number: int
    expire_status: Literal["enable", "disable"]
    expire_day: int
    reuse_password: Literal["enable", "disable"]
    reuse_password_limit: int


# ================================================================
# Main Endpoint Class
# ================================================================

class PasswordPolicyGuestAdmin:
    """
    
    Endpoint: system/password_policy_guest_admin
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
    ) -> PasswordPolicyGuestAdminObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PasswordPolicyGuestAdminPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        apply_to: str | list[str] | None = ...,
        minimum_length: int | None = ...,
        min_lower_case_letter: int | None = ...,
        min_upper_case_letter: int | None = ...,
        min_non_alphanumeric: int | None = ...,
        min_number: int | None = ...,
        expire_status: Literal["enable", "disable"] | None = ...,
        expire_day: int | None = ...,
        reuse_password: Literal["enable", "disable"] | None = ...,
        reuse_password_limit: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PasswordPolicyGuestAdminObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: PasswordPolicyGuestAdminPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        apply_to: Literal["guest-admin-password"] | list[str] | None = ...,
        minimum_length: int | None = ...,
        min_lower_case_letter: int | None = ...,
        min_upper_case_letter: int | None = ...,
        min_non_alphanumeric: int | None = ...,
        min_number: int | None = ...,
        expire_status: Literal["enable", "disable"] | None = ...,
        expire_day: int | None = ...,
        reuse_password: Literal["enable", "disable"] | None = ...,
        reuse_password_limit: int | None = ...,
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
    "PasswordPolicyGuestAdmin",
    "PasswordPolicyGuestAdminPayload",
    "PasswordPolicyGuestAdminResponse",
    "PasswordPolicyGuestAdminObject",
]