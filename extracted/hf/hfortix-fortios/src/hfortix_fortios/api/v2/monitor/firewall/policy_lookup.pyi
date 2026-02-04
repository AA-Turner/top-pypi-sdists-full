""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/policy_lookup
Category: monitor
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

class PolicyLookupPayload(TypedDict, total=False):
    """Payload type for PolicyLookup operations."""
    ipv6: bool
    srcintf: str
    sourceport: int
    sourceip: str
    protocol: str
    dest: str
    destport: int
    icmptype: int
    icmpcode: int
    policy_type: Literal["policy", "proxy"]
    auth_type: Literal["user", "group", "saml", "ldap"]
    user_group: list[str]
    server_name: str
    user_db: str
    group_attr_type: Literal["name", "id"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class PolicyLookupResponse(TypedDict, total=False):
    """Response type for PolicyLookup - use with .dict property for typed dict access."""
    dstaddr: str
    dst_cate: int
    match: bool
    matched_policy_type: str
    policy_action: str
    policy_id: int
    proxy_policy_id: int
    remote_groups: list[str]
    sec_default_action: str
    srcaddr: str
    success: bool
    urlf_entry_id: int
    user_group: str
    webfilter_action: str
    webfilter_category: int
    webfilter_profile: str
    error_code: str


class PolicyLookupObject(FortiObject[PolicyLookupResponse]):
    """Typed FortiObject for PolicyLookup with field access."""
    dstaddr: str
    dst_cate: int
    match: bool
    matched_policy_type: str
    policy_action: str
    policy_id: int
    proxy_policy_id: int
    remote_groups: list[str]
    sec_default_action: str
    srcaddr: str
    success: bool
    urlf_entry_id: int
    user_group: str
    webfilter_action: str
    webfilter_category: int
    webfilter_profile: str
    error_code: str



# ================================================================
# Main Endpoint Class
# ================================================================

class PolicyLookup:
    """
    
    Endpoint: firewall/policy_lookup
    Category: monitor
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
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        ipv6: bool | None = ...,
        srcintf: str,
        sourceport: int | None = ...,
        sourceip: str,
        protocol: str,
        dest: str,
        destport: int | None = ...,
        icmptype: int | None = ...,
        icmpcode: int | None = ...,
        policy_type: Literal["policy", "proxy"] | None = ...,
        auth_type: Literal["user", "group", "saml", "ldap"] | None = ...,
        user_group: list[str] | None = ...,
        server_name: str | None = ...,
        user_db: str | None = ...,
        group_attr_type: Literal["name", "id"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[PolicyLookupObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PolicyLookupPayload | None = ...,
        ipv6: bool | None = ...,
        srcintf: str | None = ...,
        sourceport: int | None = ...,
        sourceip: str | None = ...,
        protocol: str | None = ...,
        dest: str | None = ...,
        destport: int | None = ...,
        icmptype: int | None = ...,
        icmpcode: int | None = ...,
        policy_type: Literal["policy", "proxy"] | None = ...,
        auth_type: Literal["user", "group", "saml", "ldap"] | None = ...,
        user_group: list[str] | None = ...,
        server_name: str | None = ...,
        user_db: str | None = ...,
        group_attr_type: Literal["name", "id"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PolicyLookupObject: ...




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
        payload_dict: PolicyLookupPayload | None = ...,
        ipv6: bool | None = ...,
        srcintf: str | None = ...,
        sourceport: int | None = ...,
        sourceip: str | None = ...,
        protocol: str | None = ...,
        dest: str | None = ...,
        destport: int | None = ...,
        icmptype: int | None = ...,
        icmpcode: int | None = ...,
        policy_type: Literal["policy", "proxy"] | None = ...,
        auth_type: Literal["user", "group", "saml", "ldap"] | None = ...,
        user_group: list[str] | None = ...,
        server_name: str | None = ...,
        user_db: str | None = ...,
        group_attr_type: Literal["name", "id"] | None = ...,
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
    "PolicyLookup",
    "PolicyLookupResponse",
    "PolicyLookupObject",
]