""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: dnsfilter/profile
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

class ProfileFtgddnsFiltersItem(TypedDict, total=False):
    """Nested item for ftgd-dns.filters field."""
    id: int
    category: int
    action: Literal["block", "monitor"]
    log: Literal["enable", "disable"]


class ProfileDomainfilterDict(TypedDict, total=False):
    """Nested object type for domain-filter field."""
    domain_filter_table: int


class ProfileFtgddnsDict(TypedDict, total=False):
    """Nested object type for ftgd-dns field."""
    options: Literal["error-allow", "ftgd-disable"]
    filters: str | list[str] | list[ProfileFtgddnsFiltersItem]


class ProfileExternalipblocklistItem(TypedDict, total=False):
    """Nested item for external-ip-blocklist field."""
    name: str


class ProfileDnstranslationItem(TypedDict, total=False):
    """Nested item for dns-translation field."""
    id: int
    addr_type: Literal["ipv4", "ipv6"]
    src: str
    dst: str
    netmask: str
    status: Literal["enable", "disable"]
    src6: str
    dst6: str
    prefix: int


class ProfileTransparentdnsdatabaseItem(TypedDict, total=False):
    """Nested item for transparent-dns-database field."""
    name: str


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    comment: str
    domain_filter: ProfileDomainfilterDict
    ftgd_dns: ProfileFtgddnsDict
    log_all_domain: Literal["enable", "disable"]
    sdns_ftgd_err_log: Literal["enable", "disable"]
    sdns_domain_log: Literal["enable", "disable"]
    block_action: Literal["block", "redirect", "block-sevrfail"]
    redirect_portal: str
    redirect_portal6: str
    block_botnet: Literal["disable", "enable"]
    safe_search: Literal["disable", "enable"]
    youtube_restrict: Literal["strict", "moderate", "none"]
    external_ip_blocklist: str | list[str] | list[ProfileExternalipblocklistItem]
    dns_translation: str | list[str] | list[ProfileDnstranslationItem]
    transparent_dns_database: str | list[str] | list[ProfileTransparentdnsdatabaseItem]
    strip_ech: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    comment: str
    domain_filter: ProfileDomainfilterDict
    ftgd_dns: ProfileFtgddnsDict
    log_all_domain: Literal["enable", "disable"]
    sdns_ftgd_err_log: Literal["enable", "disable"]
    sdns_domain_log: Literal["enable", "disable"]
    block_action: Literal["block", "redirect", "block-sevrfail"]
    redirect_portal: str
    redirect_portal6: str
    block_botnet: Literal["disable", "enable"]
    safe_search: Literal["disable", "enable"]
    youtube_restrict: Literal["strict", "moderate", "none"]
    external_ip_blocklist: list[ProfileExternalipblocklistItem]
    dns_translation: list[ProfileDnstranslationItem]
    transparent_dns_database: list[ProfileTransparentdnsdatabaseItem]
    strip_ech: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileExternalipblocklistItemObject(FortiObject[ProfileExternalipblocklistItem]):
    """Typed object for external-ip-blocklist table items with attribute access."""
    name: str


class ProfileDnstranslationItemObject(FortiObject[ProfileDnstranslationItem]):
    """Typed object for dns-translation table items with attribute access."""
    id: int
    addr_type: Literal["ipv4", "ipv6"]
    src: str
    dst: str
    netmask: str
    status: Literal["enable", "disable"]
    src6: str
    dst6: str
    prefix: int


class ProfileTransparentdnsdatabaseItemObject(FortiObject[ProfileTransparentdnsdatabaseItem]):
    """Typed object for transparent-dns-database table items with attribute access."""
    name: str


class ProfileFtgddnsFiltersItemObject(FortiObject[ProfileFtgddnsFiltersItem]):
    """Typed object for ftgd-dns.filters table items with attribute access."""
    id: int
    category: int
    action: Literal["block", "monitor"]
    log: Literal["enable", "disable"]


class ProfileDomainfilterObject(FortiObject):
    """Nested object for domain-filter field with attribute access."""
    domain_filter_table: int


class ProfileFtgddnsObject(FortiObject):
    """Nested object for ftgd-dns field with attribute access."""
    options: Literal["error-allow", "ftgd-disable"]
    filters: str | list[str]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    comment: str
    domain_filter: ProfileDomainfilterObject
    ftgd_dns: ProfileFtgddnsObject
    log_all_domain: Literal["enable", "disable"]
    sdns_ftgd_err_log: Literal["enable", "disable"]
    sdns_domain_log: Literal["enable", "disable"]
    block_action: Literal["block", "redirect", "block-sevrfail"]
    redirect_portal: str
    redirect_portal6: str
    block_botnet: Literal["disable", "enable"]
    safe_search: Literal["disable", "enable"]
    youtube_restrict: Literal["strict", "moderate", "none"]
    external_ip_blocklist: FortiObjectList[ProfileExternalipblocklistItemObject]
    dns_translation: FortiObjectList[ProfileDnstranslationItemObject]
    transparent_dns_database: FortiObjectList[ProfileTransparentdnsdatabaseItemObject]
    strip_ech: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: dnsfilter/profile
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
    ) -> ProfileObject: ...
    
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
    ) -> FortiObjectList[ProfileObject]: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        domain_filter: ProfileDomainfilterDict | None = ...,
        ftgd_dns: ProfileFtgddnsDict | None = ...,
        log_all_domain: Literal["enable", "disable"] | None = ...,
        sdns_ftgd_err_log: Literal["enable", "disable"] | None = ...,
        sdns_domain_log: Literal["enable", "disable"] | None = ...,
        block_action: Literal["block", "redirect", "block-sevrfail"] | None = ...,
        redirect_portal: str | None = ...,
        redirect_portal6: str | None = ...,
        block_botnet: Literal["disable", "enable"] | None = ...,
        safe_search: Literal["disable", "enable"] | None = ...,
        youtube_restrict: Literal["strict", "moderate", "none"] | None = ...,
        external_ip_blocklist: str | list[str] | list[ProfileExternalipblocklistItem] | None = ...,
        dns_translation: str | list[str] | list[ProfileDnstranslationItem] | None = ...,
        transparent_dns_database: str | list[str] | list[ProfileTransparentdnsdatabaseItem] | None = ...,
        strip_ech: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        domain_filter: ProfileDomainfilterDict | None = ...,
        ftgd_dns: ProfileFtgddnsDict | None = ...,
        log_all_domain: Literal["enable", "disable"] | None = ...,
        sdns_ftgd_err_log: Literal["enable", "disable"] | None = ...,
        sdns_domain_log: Literal["enable", "disable"] | None = ...,
        block_action: Literal["block", "redirect", "block-sevrfail"] | None = ...,
        redirect_portal: str | None = ...,
        redirect_portal6: str | None = ...,
        block_botnet: Literal["disable", "enable"] | None = ...,
        safe_search: Literal["disable", "enable"] | None = ...,
        youtube_restrict: Literal["strict", "moderate", "none"] | None = ...,
        external_ip_blocklist: str | list[str] | list[ProfileExternalipblocklistItem] | None = ...,
        dns_translation: str | list[str] | list[ProfileDnstranslationItem] | None = ...,
        transparent_dns_database: str | list[str] | list[ProfileTransparentdnsdatabaseItem] | None = ...,
        strip_ech: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        domain_filter: ProfileDomainfilterDict | None = ...,
        ftgd_dns: ProfileFtgddnsDict | None = ...,
        log_all_domain: Literal["enable", "disable"] | None = ...,
        sdns_ftgd_err_log: Literal["enable", "disable"] | None = ...,
        sdns_domain_log: Literal["enable", "disable"] | None = ...,
        block_action: Literal["block", "redirect", "block-sevrfail"] | None = ...,
        redirect_portal: str | None = ...,
        redirect_portal6: str | None = ...,
        block_botnet: Literal["disable", "enable"] | None = ...,
        safe_search: Literal["disable", "enable"] | None = ...,
        youtube_restrict: Literal["strict", "moderate", "none"] | None = ...,
        external_ip_blocklist: str | list[str] | list[ProfileExternalipblocklistItem] | None = ...,
        dns_translation: str | list[str] | list[ProfileDnstranslationItem] | None = ...,
        transparent_dns_database: str | list[str] | list[ProfileTransparentdnsdatabaseItem] | None = ...,
        strip_ech: Literal["disable", "enable"] | None = ...,
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
    "Profile",
    "ProfilePayload",
    "ProfileResponse",
    "ProfileObject",
]