""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/peer
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

class PeerPayload(TypedDict, total=False):
    """Payload type for Peer operations."""
    name: str
    mandatory_ca_verify: Literal["enable", "disable"]
    ca: str
    subject: str
    cn: str
    cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"]
    mfa_mode: Literal["none", "password", "subject-identity"]
    mfa_server: str
    mfa_username: str
    mfa_password: str
    ocsp_override_server: str
    two_factor: Literal["enable", "disable"]
    passwd: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class PeerResponse(TypedDict, total=False):
    """Response type for Peer - use with .dict property for typed dict access."""
    name: str
    mandatory_ca_verify: Literal["enable", "disable"]
    ca: str
    subject: str
    cn: str
    cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"]
    mfa_mode: Literal["none", "password", "subject-identity"]
    mfa_server: str
    mfa_username: str
    mfa_password: str
    ocsp_override_server: str
    two_factor: Literal["enable", "disable"]
    passwd: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class PeerObject(FortiObject):
    """Typed FortiObject for Peer with field access."""
    name: str
    mandatory_ca_verify: Literal["enable", "disable"]
    ca: str
    subject: str
    cn: str
    cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"]
    mfa_mode: Literal["none", "password", "subject-identity"]
    mfa_server: str
    mfa_username: str
    mfa_password: str
    ocsp_override_server: str
    two_factor: Literal["enable", "disable"]
    passwd: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Peer:
    """
    
    Endpoint: user/peer
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
    ) -> PeerObject: ...
    
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
    ) -> FortiObjectList[PeerObject]: ...
    
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
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PeerObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PeerObject: ...

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
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
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
    "Peer",
    "PeerPayload",
    "PeerResponse",
    "PeerObject",
]