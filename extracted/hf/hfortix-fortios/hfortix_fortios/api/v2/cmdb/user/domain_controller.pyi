""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/domain_controller
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

class DomainControllerExtraserverItem(TypedDict, total=False):
    """Nested item for extra-server field."""
    id: int
    ip_address: str
    port: int
    source_ip_address: str
    source_port: int


class DomainControllerLdapserverItem(TypedDict, total=False):
    """Nested item for ldap-server field."""
    name: str


class DomainControllerPayload(TypedDict, total=False):
    """Payload type for DomainController operations."""
    name: str
    ad_mode: Literal["none", "ds", "lds"]
    hostname: str
    username: str
    password: str
    ip_address: str
    ip6: str
    port: int
    source_ip_address: str
    source_ip6: str
    source_port: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    extra_server: str | list[str] | list[DomainControllerExtraserverItem]
    domain_name: str
    replication_port: int
    ldap_server: str | list[str] | list[DomainControllerLdapserverItem]
    change_detection: Literal["enable", "disable"]
    change_detection_period: int
    dns_srv_lookup: Literal["enable", "disable"]
    adlds_dn: str
    adlds_ip_address: str
    adlds_ip6: str
    adlds_port: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DomainControllerResponse(TypedDict, total=False):
    """Response type for DomainController - use with .dict property for typed dict access."""
    name: str
    ad_mode: Literal["none", "ds", "lds"]
    hostname: str
    username: str
    password: str
    ip_address: str
    ip6: str
    port: int
    source_ip_address: str
    source_ip6: str
    source_port: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    extra_server: list[DomainControllerExtraserverItem]
    domain_name: str
    replication_port: int
    ldap_server: list[DomainControllerLdapserverItem]
    change_detection: Literal["enable", "disable"]
    change_detection_period: int
    dns_srv_lookup: Literal["enable", "disable"]
    adlds_dn: str
    adlds_ip_address: str
    adlds_ip6: str
    adlds_port: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DomainControllerExtraserverItemObject(FortiObject[DomainControllerExtraserverItem]):
    """Typed object for extra-server table items with attribute access."""
    id: int
    ip_address: str
    port: int
    source_ip_address: str
    source_port: int


class DomainControllerLdapserverItemObject(FortiObject[DomainControllerLdapserverItem]):
    """Typed object for ldap-server table items with attribute access."""
    name: str


class DomainControllerObject(FortiObject):
    """Typed FortiObject for DomainController with field access."""
    name: str
    ad_mode: Literal["none", "ds", "lds"]
    hostname: str
    username: str
    password: str
    ip_address: str
    ip6: str
    port: int
    source_ip_address: str
    source_ip6: str
    source_port: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    extra_server: FortiObjectList[DomainControllerExtraserverItemObject]
    domain_name: str
    replication_port: int
    ldap_server: FortiObjectList[DomainControllerLdapserverItemObject]
    change_detection: Literal["enable", "disable"]
    change_detection_period: int
    dns_srv_lookup: Literal["enable", "disable"]
    adlds_dn: str
    adlds_ip_address: str
    adlds_ip6: str
    adlds_port: int


# ================================================================
# Main Endpoint Class
# ================================================================

class DomainController:
    """
    
    Endpoint: user/domain_controller
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
    ) -> DomainControllerObject: ...
    
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
    ) -> FortiObjectList[DomainControllerObject]: ...
    
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
        payload_dict: DomainControllerPayload | None = ...,
        name: str | None = ...,
        ad_mode: Literal["none", "ds", "lds"] | None = ...,
        hostname: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip_address: str | None = ...,
        ip6: str | None = ...,
        port: int | None = ...,
        source_ip_address: str | None = ...,
        source_ip6: str | None = ...,
        source_port: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        extra_server: str | list[str] | list[DomainControllerExtraserverItem] | None = ...,
        domain_name: str | None = ...,
        replication_port: int | None = ...,
        ldap_server: str | list[str] | list[DomainControllerLdapserverItem] | None = ...,
        change_detection: Literal["enable", "disable"] | None = ...,
        change_detection_period: int | None = ...,
        dns_srv_lookup: Literal["enable", "disable"] | None = ...,
        adlds_dn: str | None = ...,
        adlds_ip_address: str | None = ...,
        adlds_ip6: str | None = ...,
        adlds_port: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DomainControllerObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DomainControllerPayload | None = ...,
        name: str | None = ...,
        ad_mode: Literal["none", "ds", "lds"] | None = ...,
        hostname: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip_address: str | None = ...,
        ip6: str | None = ...,
        port: int | None = ...,
        source_ip_address: str | None = ...,
        source_ip6: str | None = ...,
        source_port: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        extra_server: str | list[str] | list[DomainControllerExtraserverItem] | None = ...,
        domain_name: str | None = ...,
        replication_port: int | None = ...,
        ldap_server: str | list[str] | list[DomainControllerLdapserverItem] | None = ...,
        change_detection: Literal["enable", "disable"] | None = ...,
        change_detection_period: int | None = ...,
        dns_srv_lookup: Literal["enable", "disable"] | None = ...,
        adlds_dn: str | None = ...,
        adlds_ip_address: str | None = ...,
        adlds_ip6: str | None = ...,
        adlds_port: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DomainControllerObject: ...

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
        payload_dict: DomainControllerPayload | None = ...,
        name: str | None = ...,
        ad_mode: Literal["none", "ds", "lds"] | None = ...,
        hostname: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip_address: str | None = ...,
        ip6: str | None = ...,
        port: int | None = ...,
        source_ip_address: str | None = ...,
        source_ip6: str | None = ...,
        source_port: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        extra_server: str | list[str] | list[DomainControllerExtraserverItem] | None = ...,
        domain_name: str | None = ...,
        replication_port: int | None = ...,
        ldap_server: str | list[str] | list[DomainControllerLdapserverItem] | None = ...,
        change_detection: Literal["enable", "disable"] | None = ...,
        change_detection_period: int | None = ...,
        dns_srv_lookup: Literal["enable", "disable"] | None = ...,
        adlds_dn: str | None = ...,
        adlds_ip_address: str | None = ...,
        adlds_ip6: str | None = ...,
        adlds_port: int | None = ...,
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
    "DomainController",
    "DomainControllerPayload",
    "DomainControllerResponse",
    "DomainControllerObject",
]