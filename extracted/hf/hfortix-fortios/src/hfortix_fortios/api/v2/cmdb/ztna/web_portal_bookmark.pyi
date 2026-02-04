""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ztna/web_portal_bookmark
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

class WebPortalBookmarkUsersItem(TypedDict, total=False):
    """Nested item for users field."""
    name: str


class WebPortalBookmarkGroupsItem(TypedDict, total=False):
    """Nested item for groups field."""
    name: str


class WebPortalBookmarkBookmarksItem(TypedDict, total=False):
    """Nested item for bookmarks field."""
    name: str
    apptype: Literal["ftp", "rdp", "sftp", "smb", "ssh", "telnet", "vnc", "web"]
    url: str
    host: str
    folder: str
    domain: str
    description: str
    keyboard_layout: Literal["ar-101", "ar-102", "ar-102-azerty", "can-mul", "cz", "cz-qwerty", "cz-pr", "da", "nl", "de", "de-ch", "de-ibm", "en-uk", "en-uk-ext", "en-us", "en-us-dvorak", "es", "es-var", "fi", "fi-sami", "fr", "fr-apple", "fr-ca", "fr-ch", "fr-be", "hr", "hu", "hu-101", "it", "it-142", "ja", "ja-106", "ko", "la-am", "lt", "lt-ibm", "lt-std", "lav-std", "lav-leg", "mk", "mk-std", "no", "no-sami", "pol-214", "pol-pr", "pt", "pt-br", "pt-br-abnt2", "ru", "ru-mne", "ru-t", "sl", "sv", "sv-sami", "tuk", "tur-f", "tur-q", "zh-sym-sg-us", "zh-sym-us", "zh-tr-hk", "zh-tr-mo", "zh-tr-us"]
    security: Literal["any", "rdp", "nla", "tls"]
    send_preconnection_id: Literal["enable", "disable"]
    preconnection_id: int
    preconnection_blob: str
    load_balancing_info: str
    restricted_admin: Literal["enable", "disable"]
    port: int
    logon_user: str
    logon_password: str
    color_depth: Literal["32", "16", "8"]
    sso: Literal["disable", "enable"]
    width: int
    height: int
    vnc_keyboard_layout: Literal["default", "da", "nl", "en-uk", "en-uk-ext", "fi", "fr", "fr-be", "fr-ca-mul", "de", "de-ch", "it", "it-142", "pt", "pt-br-abnt2", "no", "gd", "es", "sv", "us-intl"]


class WebPortalBookmarkPayload(TypedDict, total=False):
    """Payload type for WebPortalBookmark operations."""
    name: str
    users: str | list[str] | list[WebPortalBookmarkUsersItem]
    groups: str | list[str] | list[WebPortalBookmarkGroupsItem]
    bookmarks: str | list[str] | list[WebPortalBookmarkBookmarksItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class WebPortalBookmarkResponse(TypedDict, total=False):
    """Response type for WebPortalBookmark - use with .dict property for typed dict access."""
    name: str
    users: list[WebPortalBookmarkUsersItem]
    groups: list[WebPortalBookmarkGroupsItem]
    bookmarks: list[WebPortalBookmarkBookmarksItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class WebPortalBookmarkUsersItemObject(FortiObject[WebPortalBookmarkUsersItem]):
    """Typed object for users table items with attribute access."""
    name: str


class WebPortalBookmarkGroupsItemObject(FortiObject[WebPortalBookmarkGroupsItem]):
    """Typed object for groups table items with attribute access."""
    name: str


class WebPortalBookmarkBookmarksItemObject(FortiObject[WebPortalBookmarkBookmarksItem]):
    """Typed object for bookmarks table items with attribute access."""
    name: str
    apptype: Literal["ftp", "rdp", "sftp", "smb", "ssh", "telnet", "vnc", "web"]
    url: str
    host: str
    folder: str
    domain: str
    description: str
    keyboard_layout: Literal["ar-101", "ar-102", "ar-102-azerty", "can-mul", "cz", "cz-qwerty", "cz-pr", "da", "nl", "de", "de-ch", "de-ibm", "en-uk", "en-uk-ext", "en-us", "en-us-dvorak", "es", "es-var", "fi", "fi-sami", "fr", "fr-apple", "fr-ca", "fr-ch", "fr-be", "hr", "hu", "hu-101", "it", "it-142", "ja", "ja-106", "ko", "la-am", "lt", "lt-ibm", "lt-std", "lav-std", "lav-leg", "mk", "mk-std", "no", "no-sami", "pol-214", "pol-pr", "pt", "pt-br", "pt-br-abnt2", "ru", "ru-mne", "ru-t", "sl", "sv", "sv-sami", "tuk", "tur-f", "tur-q", "zh-sym-sg-us", "zh-sym-us", "zh-tr-hk", "zh-tr-mo", "zh-tr-us"]
    security: Literal["any", "rdp", "nla", "tls"]
    send_preconnection_id: Literal["enable", "disable"]
    preconnection_id: int
    preconnection_blob: str
    load_balancing_info: str
    restricted_admin: Literal["enable", "disable"]
    port: int
    logon_user: str
    logon_password: str
    color_depth: Literal["32", "16", "8"]
    sso: Literal["disable", "enable"]
    width: int
    height: int
    vnc_keyboard_layout: Literal["default", "da", "nl", "en-uk", "en-uk-ext", "fi", "fr", "fr-be", "fr-ca-mul", "de", "de-ch", "it", "it-142", "pt", "pt-br-abnt2", "no", "gd", "es", "sv", "us-intl"]


class WebPortalBookmarkObject(FortiObject):
    """Typed FortiObject for WebPortalBookmark with field access."""
    name: str
    users: FortiObjectList[WebPortalBookmarkUsersItemObject]
    groups: FortiObjectList[WebPortalBookmarkGroupsItemObject]
    bookmarks: FortiObjectList[WebPortalBookmarkBookmarksItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class WebPortalBookmark:
    """
    
    Endpoint: ztna/web_portal_bookmark
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
    ) -> WebPortalBookmarkObject: ...
    
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
    ) -> FortiObjectList[WebPortalBookmarkObject]: ...
    
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
        payload_dict: WebPortalBookmarkPayload | None = ...,
        name: str | None = ...,
        users: str | list[str] | list[WebPortalBookmarkUsersItem] | None = ...,
        groups: str | list[str] | list[WebPortalBookmarkGroupsItem] | None = ...,
        bookmarks: str | list[str] | list[WebPortalBookmarkBookmarksItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WebPortalBookmarkObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: WebPortalBookmarkPayload | None = ...,
        name: str | None = ...,
        users: str | list[str] | list[WebPortalBookmarkUsersItem] | None = ...,
        groups: str | list[str] | list[WebPortalBookmarkGroupsItem] | None = ...,
        bookmarks: str | list[str] | list[WebPortalBookmarkBookmarksItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WebPortalBookmarkObject: ...

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
        payload_dict: WebPortalBookmarkPayload | None = ...,
        name: str | None = ...,
        users: str | list[str] | list[WebPortalBookmarkUsersItem] | None = ...,
        groups: str | list[str] | list[WebPortalBookmarkGroupsItem] | None = ...,
        bookmarks: str | list[str] | list[WebPortalBookmarkBookmarksItem] | None = ...,
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
    "WebPortalBookmark",
    "WebPortalBookmarkPayload",
    "WebPortalBookmarkResponse",
    "WebPortalBookmarkObject",
]