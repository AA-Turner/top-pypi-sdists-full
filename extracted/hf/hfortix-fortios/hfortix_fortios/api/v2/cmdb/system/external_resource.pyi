""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/external_resource
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

class ExternalResourcePayload(TypedDict, total=False):
    """Payload type for ExternalResource operations."""
    name: str
    uuid: str
    status: Literal["enable", "disable"]
    type: Literal["category", "domain", "malware", "address", "mac-address", "data", "generic-address"]
    namespace: str
    object_array_path: str
    address_name_field: str
    address_data_field: str
    address_comment_field: str
    update_method: Literal["feed", "push"]
    category: int
    username: str
    password: str
    client_cert_auth: Literal["enable", "disable"]
    client_cert: str
    comments: str
    resource: str
    user_agent: str
    server_identity_check: Literal["none", "basic", "full"]
    refresh_rate: int
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ExternalResourceResponse(TypedDict, total=False):
    """Response type for ExternalResource - use with .dict property for typed dict access."""
    name: str
    uuid: str
    status: Literal["enable", "disable"]
    type: Literal["category", "domain", "malware", "address", "mac-address", "data", "generic-address"]
    namespace: str
    object_array_path: str
    address_name_field: str
    address_data_field: str
    address_comment_field: str
    update_method: Literal["feed", "push"]
    category: int
    username: str
    password: str
    client_cert_auth: Literal["enable", "disable"]
    client_cert: str
    comments: str
    resource: str
    user_agent: str
    server_identity_check: Literal["none", "basic", "full"]
    refresh_rate: int
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ExternalResourceObject(FortiObject):
    """Typed FortiObject for ExternalResource with field access."""
    name: str
    uuid: str
    status: Literal["enable", "disable"]
    type: Literal["category", "domain", "malware", "address", "mac-address", "data", "generic-address"]
    namespace: str
    object_array_path: str
    address_name_field: str
    address_data_field: str
    address_comment_field: str
    update_method: Literal["feed", "push"]
    category: int
    username: str
    password: str
    client_cert_auth: Literal["enable", "disable"]
    client_cert: str
    comments: str
    resource: str
    user_agent: str
    server_identity_check: Literal["none", "basic", "full"]
    refresh_rate: int
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Main Endpoint Class
# ================================================================

class ExternalResource:
    """
    
    Endpoint: system/external_resource
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
    ) -> ExternalResourceObject: ...
    
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
    ) -> FortiObjectList[ExternalResourceObject]: ...
    
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
        payload_dict: ExternalResourcePayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["category", "domain", "malware", "address", "mac-address", "data", "generic-address"] | None = ...,
        namespace: str | None = ...,
        object_array_path: str | None = ...,
        address_name_field: str | None = ...,
        address_data_field: str | None = ...,
        address_comment_field: str | None = ...,
        update_method: Literal["feed", "push"] | None = ...,
        category: int | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        comments: str | None = ...,
        resource: str | None = ...,
        user_agent: str | None = ...,
        server_identity_check: Literal["none", "basic", "full"] | None = ...,
        refresh_rate: int | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExternalResourceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ExternalResourcePayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["category", "domain", "malware", "address", "mac-address", "data", "generic-address"] | None = ...,
        namespace: str | None = ...,
        object_array_path: str | None = ...,
        address_name_field: str | None = ...,
        address_data_field: str | None = ...,
        address_comment_field: str | None = ...,
        update_method: Literal["feed", "push"] | None = ...,
        category: int | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        comments: str | None = ...,
        resource: str | None = ...,
        user_agent: str | None = ...,
        server_identity_check: Literal["none", "basic", "full"] | None = ...,
        refresh_rate: int | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExternalResourceObject: ...

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
        payload_dict: ExternalResourcePayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["category", "domain", "malware", "address", "mac-address", "data", "generic-address"] | None = ...,
        namespace: str | None = ...,
        object_array_path: str | None = ...,
        address_name_field: str | None = ...,
        address_data_field: str | None = ...,
        address_comment_field: str | None = ...,
        update_method: Literal["feed", "push"] | None = ...,
        category: int | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        comments: str | None = ...,
        resource: str | None = ...,
        user_agent: str | None = ...,
        server_identity_check: Literal["none", "basic", "full"] | None = ...,
        refresh_rate: int | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
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
    "ExternalResource",
    "ExternalResourcePayload",
    "ExternalResourceResponse",
    "ExternalResourceObject",
]