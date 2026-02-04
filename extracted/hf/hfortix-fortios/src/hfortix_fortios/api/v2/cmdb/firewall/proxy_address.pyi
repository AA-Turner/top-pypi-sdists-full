""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/proxy_address
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

class ProxyAddressTaggingTagsItem(TypedDict, total=False):
    """Nested item for tagging.tags field."""
    name: str


class ProxyAddressCategoryItem(TypedDict, total=False):
    """Nested item for category field."""
    id: int


class ProxyAddressHeadergroupItem(TypedDict, total=False):
    """Nested item for header-group field."""
    id: int
    header_name: str
    header: str
    case_sensitivity: Literal["disable", "enable"]


class ProxyAddressTaggingItem(TypedDict, total=False):
    """Nested item for tagging field."""
    name: str
    category: str
    tags: str | list[str] | list[ProxyAddressTaggingTagsItem]


class ProxyAddressApplicationItem(TypedDict, total=False):
    """Nested item for application field."""
    name: str


class ProxyAddressPayload(TypedDict, total=False):
    """Payload type for ProxyAddress operations."""
    name: str
    uuid: str
    type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"]
    host: str
    host_regex: str
    path: str
    query: str
    referrer: Literal["enable", "disable"]
    category: str | list[str] | list[ProxyAddressCategoryItem]
    method: str | list[str]
    ua: str | list[str]
    ua_min_ver: str
    ua_max_ver: str
    header_name: str
    header: str
    case_sensitivity: Literal["disable", "enable"]
    header_group: str | list[str] | list[ProxyAddressHeadergroupItem]
    color: int
    tagging: str | list[str] | list[ProxyAddressTaggingItem]
    comment: str
    application: str | list[str] | list[ProxyAddressApplicationItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProxyAddressResponse(TypedDict, total=False):
    """Response type for ProxyAddress - use with .dict property for typed dict access."""
    name: str
    uuid: str
    type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"]
    host: str
    host_regex: str
    path: str
    query: str
    referrer: Literal["enable", "disable"]
    category: list[ProxyAddressCategoryItem]
    method: str
    ua: str
    ua_min_ver: str
    ua_max_ver: str
    header_name: str
    header: str
    case_sensitivity: Literal["disable", "enable"]
    header_group: list[ProxyAddressHeadergroupItem]
    color: int
    tagging: list[ProxyAddressTaggingItem]
    comment: str
    application: list[ProxyAddressApplicationItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProxyAddressTaggingTagsItemObject(FortiObject[ProxyAddressTaggingTagsItem]):
    """Typed object for tagging.tags table items with attribute access."""
    name: str


class ProxyAddressCategoryItemObject(FortiObject[ProxyAddressCategoryItem]):
    """Typed object for category table items with attribute access."""
    id: int


class ProxyAddressHeadergroupItemObject(FortiObject[ProxyAddressHeadergroupItem]):
    """Typed object for header-group table items with attribute access."""
    id: int
    header_name: str
    header: str
    case_sensitivity: Literal["disable", "enable"]


class ProxyAddressTaggingItemObject(FortiObject[ProxyAddressTaggingItem]):
    """Typed object for tagging table items with attribute access."""
    name: str
    category: str
    tags: FortiObjectList[ProxyAddressTaggingTagsItemObject]


class ProxyAddressApplicationItemObject(FortiObject[ProxyAddressApplicationItem]):
    """Typed object for application table items with attribute access."""
    name: str


class ProxyAddressObject(FortiObject):
    """Typed FortiObject for ProxyAddress with field access."""
    name: str
    uuid: str
    type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"]
    host: str
    host_regex: str
    path: str
    query: str
    referrer: Literal["enable", "disable"]
    category: FortiObjectList[ProxyAddressCategoryItemObject]
    method: str
    ua: str
    ua_min_ver: str
    ua_max_ver: str
    header_name: str
    header: str
    case_sensitivity: Literal["disable", "enable"]
    header_group: FortiObjectList[ProxyAddressHeadergroupItemObject]
    color: int
    tagging: FortiObjectList[ProxyAddressTaggingItemObject]
    comment: str
    application: FortiObjectList[ProxyAddressApplicationItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ProxyAddress:
    """
    
    Endpoint: firewall/proxy_address
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
    ) -> ProxyAddressObject: ...
    
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
    ) -> FortiObjectList[ProxyAddressObject]: ...
    
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
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[ProxyAddressCategoryItem] | None = ...,
        method: str | list[str] | None = ...,
        ua: str | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[ProxyAddressHeadergroupItem] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[ProxyAddressTaggingItem] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[ProxyAddressApplicationItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProxyAddressObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[ProxyAddressCategoryItem] | None = ...,
        method: str | list[str] | None = ...,
        ua: str | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[ProxyAddressHeadergroupItem] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[ProxyAddressTaggingItem] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[ProxyAddressApplicationItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProxyAddressObject: ...

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
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[ProxyAddressCategoryItem] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[ProxyAddressHeadergroupItem] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[ProxyAddressTaggingItem] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[ProxyAddressApplicationItem] | None = ...,
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
    "ProxyAddress",
    "ProxyAddressPayload",
    "ProxyAddressResponse",
    "ProxyAddressObject",
]