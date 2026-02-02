""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/ipsec/manualkey_interface
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

class ManualkeyInterfacePayload(TypedDict, total=False):
    """Payload type for ManualkeyInterface operations."""
    name: str
    interface: str
    ip_version: Literal["4", "6"]
    addr_type: Literal["4", "6"]
    remote_gw: str
    remote_gw6: str
    local_gw: str
    local_gw6: str
    auth_alg: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"]
    enc_alg: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"]
    auth_key: str
    enc_key: str
    local_spi: str
    remote_spi: str
    npu_offload: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ManualkeyInterfaceResponse(TypedDict, total=False):
    """Response type for ManualkeyInterface - use with .dict property for typed dict access."""
    name: str
    interface: str
    ip_version: Literal["4", "6"]
    addr_type: Literal["4", "6"]
    remote_gw: str
    remote_gw6: str
    local_gw: str
    local_gw6: str
    auth_alg: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"]
    enc_alg: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"]
    auth_key: str
    enc_key: str
    local_spi: str
    remote_spi: str
    npu_offload: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ManualkeyInterfaceObject(FortiObject):
    """Typed FortiObject for ManualkeyInterface with field access."""
    name: str
    interface: str
    ip_version: Literal["4", "6"]
    addr_type: Literal["4", "6"]
    remote_gw: str
    remote_gw6: str
    local_gw: str
    local_gw6: str
    auth_alg: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"]
    enc_alg: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"]
    auth_key: str
    enc_key: str
    local_spi: str
    remote_spi: str
    npu_offload: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class ManualkeyInterface:
    """
    
    Endpoint: vpn/ipsec/manualkey_interface
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
    ) -> ManualkeyInterfaceObject: ...
    
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
    ) -> FortiObjectList[ManualkeyInterfaceObject]: ...
    
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
        payload_dict: ManualkeyInterfacePayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        ip_version: Literal["4", "6"] | None = ...,
        addr_type: Literal["4", "6"] | None = ...,
        remote_gw: str | None = ...,
        remote_gw6: str | None = ...,
        local_gw: str | None = ...,
        local_gw6: str | None = ...,
        auth_alg: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        enc_alg: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        auth_key: str | None = ...,
        enc_key: str | None = ...,
        local_spi: str | None = ...,
        remote_spi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ManualkeyInterfaceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ManualkeyInterfacePayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        ip_version: Literal["4", "6"] | None = ...,
        addr_type: Literal["4", "6"] | None = ...,
        remote_gw: str | None = ...,
        remote_gw6: str | None = ...,
        local_gw: str | None = ...,
        local_gw6: str | None = ...,
        auth_alg: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        enc_alg: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        auth_key: str | None = ...,
        enc_key: str | None = ...,
        local_spi: str | None = ...,
        remote_spi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ManualkeyInterfaceObject: ...

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
        payload_dict: ManualkeyInterfacePayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        ip_version: Literal["4", "6"] | None = ...,
        addr_type: Literal["4", "6"] | None = ...,
        remote_gw: str | None = ...,
        remote_gw6: str | None = ...,
        local_gw: str | None = ...,
        local_gw6: str | None = ...,
        auth_alg: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        enc_alg: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        auth_key: str | None = ...,
        enc_key: str | None = ...,
        local_spi: str | None = ...,
        remote_spi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
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
    "ManualkeyInterface",
    "ManualkeyInterfacePayload",
    "ManualkeyInterfaceResponse",
    "ManualkeyInterfaceObject",
]