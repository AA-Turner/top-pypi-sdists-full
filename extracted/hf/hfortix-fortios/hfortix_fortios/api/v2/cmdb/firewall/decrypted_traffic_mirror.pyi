""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/decrypted_traffic_mirror
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

class DecryptedTrafficMirrorInterfaceItem(TypedDict, total=False):
    """Nested item for interface field."""
    name: str


class DecryptedTrafficMirrorPayload(TypedDict, total=False):
    """Payload type for DecryptedTrafficMirror operations."""
    name: str
    dstmac: str
    traffic_type: str | list[str]
    traffic_source: Literal["client", "server", "both"]
    interface: str | list[str] | list[DecryptedTrafficMirrorInterfaceItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DecryptedTrafficMirrorResponse(TypedDict, total=False):
    """Response type for DecryptedTrafficMirror - use with .dict property for typed dict access."""
    name: str
    dstmac: str
    traffic_type: str
    traffic_source: Literal["client", "server", "both"]
    interface: list[DecryptedTrafficMirrorInterfaceItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DecryptedTrafficMirrorInterfaceItemObject(FortiObject[DecryptedTrafficMirrorInterfaceItem]):
    """Typed object for interface table items with attribute access."""
    name: str


class DecryptedTrafficMirrorObject(FortiObject):
    """Typed FortiObject for DecryptedTrafficMirror with field access."""
    name: str
    dstmac: str
    traffic_type: str
    traffic_source: Literal["client", "server", "both"]
    interface: FortiObjectList[DecryptedTrafficMirrorInterfaceItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class DecryptedTrafficMirror:
    """
    
    Endpoint: firewall/decrypted_traffic_mirror
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
    ) -> DecryptedTrafficMirrorObject: ...
    
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
    ) -> FortiObjectList[DecryptedTrafficMirrorObject]: ...
    
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
        payload_dict: DecryptedTrafficMirrorPayload | None = ...,
        name: str | None = ...,
        dstmac: str | None = ...,
        traffic_type: str | list[str] | None = ...,
        traffic_source: Literal["client", "server", "both"] | None = ...,
        interface: str | list[str] | list[DecryptedTrafficMirrorInterfaceItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DecryptedTrafficMirrorObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DecryptedTrafficMirrorPayload | None = ...,
        name: str | None = ...,
        dstmac: str | None = ...,
        traffic_type: str | list[str] | None = ...,
        traffic_source: Literal["client", "server", "both"] | None = ...,
        interface: str | list[str] | list[DecryptedTrafficMirrorInterfaceItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DecryptedTrafficMirrorObject: ...

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
        payload_dict: DecryptedTrafficMirrorPayload | None = ...,
        name: str | None = ...,
        dstmac: str | None = ...,
        traffic_type: Literal["ssl", "ssh"] | list[str] | None = ...,
        traffic_source: Literal["client", "server", "both"] | None = ...,
        interface: str | list[str] | list[DecryptedTrafficMirrorInterfaceItem] | None = ...,
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
    "DecryptedTrafficMirror",
    "DecryptedTrafficMirrorPayload",
    "DecryptedTrafficMirrorResponse",
    "DecryptedTrafficMirrorObject",
]