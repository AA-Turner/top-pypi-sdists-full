""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/krb_keytab
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

class KrbKeytabLdapserverItem(TypedDict, total=False):
    """Nested item for ldap-server field."""
    name: str


class KrbKeytabPayload(TypedDict, total=False):
    """Payload type for KrbKeytab operations."""
    name: str
    pac_data: Literal["enable", "disable"]
    principal: str
    ldap_server: str | list[str] | list[KrbKeytabLdapserverItem]
    keytab: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class KrbKeytabResponse(TypedDict, total=False):
    """Response type for KrbKeytab - use with .dict property for typed dict access."""
    name: str
    pac_data: Literal["enable", "disable"]
    principal: str
    ldap_server: list[KrbKeytabLdapserverItem]
    keytab: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class KrbKeytabLdapserverItemObject(FortiObject[KrbKeytabLdapserverItem]):
    """Typed object for ldap-server table items with attribute access."""
    name: str


class KrbKeytabObject(FortiObject):
    """Typed FortiObject for KrbKeytab with field access."""
    name: str
    pac_data: Literal["enable", "disable"]
    principal: str
    ldap_server: FortiObjectList[KrbKeytabLdapserverItemObject]
    keytab: str


# ================================================================
# Main Endpoint Class
# ================================================================

class KrbKeytab:
    """
    
    Endpoint: user/krb_keytab
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
    ) -> KrbKeytabObject: ...
    
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
    ) -> FortiObjectList[KrbKeytabObject]: ...
    
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
        payload_dict: KrbKeytabPayload | None = ...,
        name: str | None = ...,
        pac_data: Literal["enable", "disable"] | None = ...,
        principal: str | None = ...,
        ldap_server: str | list[str] | list[KrbKeytabLdapserverItem] | None = ...,
        keytab: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> KrbKeytabObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: KrbKeytabPayload | None = ...,
        name: str | None = ...,
        pac_data: Literal["enable", "disable"] | None = ...,
        principal: str | None = ...,
        ldap_server: str | list[str] | list[KrbKeytabLdapserverItem] | None = ...,
        keytab: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> KrbKeytabObject: ...

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
        payload_dict: KrbKeytabPayload | None = ...,
        name: str | None = ...,
        pac_data: Literal["enable", "disable"] | None = ...,
        principal: str | None = ...,
        ldap_server: str | list[str] | list[KrbKeytabLdapserverItem] | None = ...,
        keytab: str | None = ...,
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
    "KrbKeytab",
    "KrbKeytabPayload",
    "KrbKeytabResponse",
    "KrbKeytabObject",
]