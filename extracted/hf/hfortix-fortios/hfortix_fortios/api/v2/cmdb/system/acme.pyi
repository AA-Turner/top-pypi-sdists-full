""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/acme
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

class AcmeInterfaceItem(TypedDict, total=False):
    """Nested item for interface field."""
    interface_name: str


class AcmeAccountsItem(TypedDict, total=False):
    """Nested item for accounts field."""
    id: str
    status: str
    url: str
    ca_url: str
    email: str
    eab_key_id: str
    eab_key_hmac: str
    privatekey: str


class AcmePayload(TypedDict, total=False):
    """Payload type for Acme operations."""
    interface: str | list[str] | list[AcmeInterfaceItem]
    use_ha_direct: Literal["enable", "disable"]
    source_ip: str
    source_ip6: str
    accounts: str | list[str] | list[AcmeAccountsItem]
    acc_details: str
    status: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AcmeResponse(TypedDict, total=False):
    """Response type for Acme - use with .dict property for typed dict access."""
    interface: list[AcmeInterfaceItem]
    use_ha_direct: Literal["enable", "disable"]
    source_ip: str
    source_ip6: str
    accounts: list[AcmeAccountsItem]
    acc_details: str
    status: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AcmeInterfaceItemObject(FortiObject[AcmeInterfaceItem]):
    """Typed object for interface table items with attribute access."""
    interface_name: str


class AcmeAccountsItemObject(FortiObject[AcmeAccountsItem]):
    """Typed object for accounts table items with attribute access."""
    id: str
    status: str
    url: str
    ca_url: str
    email: str
    eab_key_id: str
    eab_key_hmac: str
    privatekey: str


class AcmeObject(FortiObject):
    """Typed FortiObject for Acme with field access."""
    interface: FortiObjectList[AcmeInterfaceItemObject]
    use_ha_direct: Literal["enable", "disable"]
    source_ip: str
    source_ip6: str
    accounts: FortiObjectList[AcmeAccountsItemObject]
    acc_details: str
    status: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Acme:
    """
    
    Endpoint: system/acme
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
    ) -> AcmeObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[AcmeInterfaceItem] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[AcmeAccountsItem] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AcmeObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[AcmeInterfaceItem] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[AcmeAccountsItem] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
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
    "Acme",
    "AcmePayload",
    "AcmeResponse",
    "AcmeObject",
]