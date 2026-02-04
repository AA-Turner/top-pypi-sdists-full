""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/scim
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

class ScimPayload(TypedDict, total=False):
    """Payload type for Scim operations."""
    name: str
    id: int
    status: Literal["enable", "disable"]
    base_url: str
    auth_method: Literal["token", "base"]
    token_certificate: str
    secret: str
    certificate: str
    client_identity_check: Literal["enable", "disable"]
    cascade: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ScimResponse(TypedDict, total=False):
    """Response type for Scim - use with .dict property for typed dict access."""
    name: str
    id: int
    status: Literal["enable", "disable"]
    base_url: str
    auth_method: Literal["token", "base"]
    token_certificate: str
    secret: str
    certificate: str
    client_identity_check: Literal["enable", "disable"]
    cascade: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ScimObject(FortiObject):
    """Typed FortiObject for Scim with field access."""
    name: str
    id: int
    status: Literal["enable", "disable"]
    base_url: str
    auth_method: Literal["token", "base"]
    token_certificate: str
    secret: str
    certificate: str
    client_identity_check: Literal["enable", "disable"]
    cascade: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Scim:
    """
    
    Endpoint: user/scim
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
    ) -> ScimObject: ...
    
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
    ) -> FortiObjectList[ScimObject]: ...
    
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
        payload_dict: ScimPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        base_url: str | None = ...,
        auth_method: Literal["token", "base"] | None = ...,
        token_certificate: str | None = ...,
        secret: str | None = ...,
        certificate: str | None = ...,
        client_identity_check: Literal["enable", "disable"] | None = ...,
        cascade: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ScimObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ScimPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        base_url: str | None = ...,
        auth_method: Literal["token", "base"] | None = ...,
        token_certificate: str | None = ...,
        secret: str | None = ...,
        certificate: str | None = ...,
        client_identity_check: Literal["enable", "disable"] | None = ...,
        cascade: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ScimObject: ...

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
        payload_dict: ScimPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        base_url: str | None = ...,
        auth_method: Literal["token", "base"] | None = ...,
        token_certificate: str | None = ...,
        secret: str | None = ...,
        certificate: str | None = ...,
        client_identity_check: Literal["enable", "disable"] | None = ...,
        cascade: Literal["disable", "enable"] | None = ...,
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
    "Scim",
    "ScimPayload",
    "ScimResponse",
    "ScimObject",
]