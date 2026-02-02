""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ethernet_oam/cfm
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

class CfmServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    service_id: int
    service_name: str
    interface: str
    mepid: int
    message_interval: Literal["100", "1000", "10000", "60000", "600000"]
    cos: int
    sender_id: Literal["None", "Hostname"]


class CfmPayload(TypedDict, total=False):
    """Payload type for Cfm operations."""
    domain_id: int
    domain_name: str
    domain_level: int
    service: str | list[str] | list[CfmServiceItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CfmResponse(TypedDict, total=False):
    """Response type for Cfm - use with .dict property for typed dict access."""
    domain_id: int
    domain_name: str
    domain_level: int
    service: list[CfmServiceItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CfmServiceItemObject(FortiObject[CfmServiceItem]):
    """Typed object for service table items with attribute access."""
    service_id: int
    service_name: str
    interface: str
    mepid: int
    message_interval: Literal["100", "1000", "10000", "60000", "600000"]
    cos: int
    sender_id: Literal["None", "Hostname"]


class CfmObject(FortiObject):
    """Typed FortiObject for Cfm with field access."""
    domain_id: int
    domain_name: str
    domain_level: int
    service: FortiObjectList[CfmServiceItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Cfm:
    """
    
    Endpoint: ethernet_oam/cfm
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CfmObject: ...
    
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
        payload_dict: CfmPayload | None = ...,
        domain_id: int | None = ...,
        domain_name: str | None = ...,
        domain_level: int | None = ...,
        service: str | list[str] | list[CfmServiceItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CfmObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CfmPayload | None = ...,
        domain_id: int | None = ...,
        domain_name: str | None = ...,
        domain_level: int | None = ...,
        service: str | list[str] | list[CfmServiceItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CfmObject: ...

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
        payload_dict: CfmPayload | None = ...,
        domain_id: int | None = ...,
        domain_name: str | None = ...,
        domain_level: int | None = ...,
        service: str | list[str] | list[CfmServiceItem] | None = ...,
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
    "Cfm",
    "CfmPayload",
    "CfmResponse",
    "CfmObject",
]