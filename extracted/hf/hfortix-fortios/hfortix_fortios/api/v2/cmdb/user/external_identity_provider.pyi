""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/external_identity_provider
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

class ExternalIdentityProviderPayload(TypedDict, total=False):
    """Payload type for ExternalIdentityProvider operations."""
    name: str
    type: Literal["ms-graph"]
    version: Literal["v1.0", "beta"]
    url: str
    user_attr_name: str
    group_attr_name: str
    port: int
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    server_identity_check: Literal["disable", "enable"]
    timeout: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ExternalIdentityProviderResponse(TypedDict, total=False):
    """Response type for ExternalIdentityProvider - use with .dict property for typed dict access."""
    name: str
    type: Literal["ms-graph"]
    version: Literal["v1.0", "beta"]
    url: str
    user_attr_name: str
    group_attr_name: str
    port: int
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    server_identity_check: Literal["disable", "enable"]
    timeout: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ExternalIdentityProviderObject(FortiObject):
    """Typed FortiObject for ExternalIdentityProvider with field access."""
    name: str
    type: Literal["ms-graph"]
    url: str
    user_attr_name: str
    group_attr_name: str
    port: int
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    server_identity_check: Literal["disable", "enable"]
    timeout: int


# ================================================================
# Main Endpoint Class
# ================================================================

class ExternalIdentityProvider:
    """
    
    Endpoint: user/external_identity_provider
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
    ) -> ExternalIdentityProviderObject: ...
    
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
    ) -> FortiObjectList[ExternalIdentityProviderObject]: ...
    
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
        payload_dict: ExternalIdentityProviderPayload | None = ...,
        name: str | None = ...,
        type: Literal["ms-graph"] | None = ...,
        version: Literal["v1.0", "beta"] | None = ...,
        url: str | None = ...,
        user_attr_name: str | None = ...,
        group_attr_name: str | None = ...,
        port: int | None = ...,
        source_ip: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        server_identity_check: Literal["disable", "enable"] | None = ...,
        timeout: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExternalIdentityProviderObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ExternalIdentityProviderPayload | None = ...,
        name: str | None = ...,
        type: Literal["ms-graph"] | None = ...,
        version: Literal["v1.0", "beta"] | None = ...,
        url: str | None = ...,
        user_attr_name: str | None = ...,
        group_attr_name: str | None = ...,
        port: int | None = ...,
        source_ip: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        server_identity_check: Literal["disable", "enable"] | None = ...,
        timeout: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExternalIdentityProviderObject: ...

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
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ExternalIdentityProviderPayload | None = ...,
        name: str | None = ...,
        type: Literal["ms-graph"] | None = ...,
        version: Literal["v1.0", "beta"] | None = ...,
        url: str | None = ...,
        user_attr_name: str | None = ...,
        group_attr_name: str | None = ...,
        port: int | None = ...,
        source_ip: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        server_identity_check: Literal["disable", "enable"] | None = ...,
        timeout: int | None = ...,
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
    "ExternalIdentityProvider",
    "ExternalIdentityProviderPayload",
    "ExternalIdentityProviderResponse",
    "ExternalIdentityProviderObject",
]