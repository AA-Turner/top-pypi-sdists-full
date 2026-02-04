""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: webfilter/urlfilter
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

class UrlfilterEntriesItem(TypedDict, total=False):
    """Nested item for entries field."""
    id: int
    url: str
    type: Literal["simple", "regex", "wildcard"]
    action: Literal["exempt", "block", "allow", "monitor"]
    antiphish_action: Literal["block", "log"]
    status: Literal["enable", "disable"]
    exempt: Literal["av", "web-content", "activex-java-cookie", "dlp", "fortiguard", "range-block", "pass", "antiphish", "all"]
    web_proxy_profile: str
    referrer_host: str
    dns_address_family: Literal["ipv4", "ipv6", "both"]
    comment: str


class UrlfilterPayload(TypedDict, total=False):
    """Payload type for Urlfilter operations."""
    id: int
    name: str
    comment: str
    one_arm_ips_urlfilter: Literal["enable", "disable"]
    ip_addr_block: Literal["enable", "disable"]
    ip4_mapped_ip6: Literal["enable", "disable"]
    include_subdomains: Literal["enable", "disable"]
    entries: str | list[str] | list[UrlfilterEntriesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class UrlfilterResponse(TypedDict, total=False):
    """Response type for Urlfilter - use with .dict property for typed dict access."""
    id: int
    name: str
    comment: str
    one_arm_ips_urlfilter: Literal["enable", "disable"]
    ip_addr_block: Literal["enable", "disable"]
    ip4_mapped_ip6: Literal["enable", "disable"]
    include_subdomains: Literal["enable", "disable"]
    entries: list[UrlfilterEntriesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class UrlfilterEntriesItemObject(FortiObject[UrlfilterEntriesItem]):
    """Typed object for entries table items with attribute access."""
    id: int
    url: str
    type: Literal["simple", "regex", "wildcard"]
    action: Literal["exempt", "block", "allow", "monitor"]
    antiphish_action: Literal["block", "log"]
    status: Literal["enable", "disable"]
    exempt: Literal["av", "web-content", "activex-java-cookie", "dlp", "fortiguard", "range-block", "pass", "antiphish", "all"]
    web_proxy_profile: str
    referrer_host: str
    dns_address_family: Literal["ipv4", "ipv6", "both"]
    comment: str


class UrlfilterObject(FortiObject):
    """Typed FortiObject for Urlfilter with field access."""
    id: int
    name: str
    comment: str
    one_arm_ips_urlfilter: Literal["enable", "disable"]
    ip_addr_block: Literal["enable", "disable"]
    ip4_mapped_ip6: Literal["enable", "disable"]
    include_subdomains: Literal["enable", "disable"]
    entries: FortiObjectList[UrlfilterEntriesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Urlfilter:
    """
    
    Endpoint: webfilter/urlfilter
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> UrlfilterObject: ...
    
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
    ) -> FortiObjectList[UrlfilterObject]: ...
    
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
        payload_dict: UrlfilterPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        one_arm_ips_urlfilter: Literal["enable", "disable"] | None = ...,
        ip_addr_block: Literal["enable", "disable"] | None = ...,
        ip4_mapped_ip6: Literal["enable", "disable"] | None = ...,
        include_subdomains: Literal["enable", "disable"] | None = ...,
        entries: str | list[str] | list[UrlfilterEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UrlfilterObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: UrlfilterPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        one_arm_ips_urlfilter: Literal["enable", "disable"] | None = ...,
        ip_addr_block: Literal["enable", "disable"] | None = ...,
        ip4_mapped_ip6: Literal["enable", "disable"] | None = ...,
        include_subdomains: Literal["enable", "disable"] | None = ...,
        entries: str | list[str] | list[UrlfilterEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UrlfilterObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: UrlfilterPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        one_arm_ips_urlfilter: Literal["enable", "disable"] | None = ...,
        ip_addr_block: Literal["enable", "disable"] | None = ...,
        ip4_mapped_ip6: Literal["enable", "disable"] | None = ...,
        include_subdomains: Literal["enable", "disable"] | None = ...,
        entries: str | list[str] | list[UrlfilterEntriesItem] | None = ...,
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
    "Urlfilter",
    "UrlfilterPayload",
    "UrlfilterResponse",
    "UrlfilterObject",
]