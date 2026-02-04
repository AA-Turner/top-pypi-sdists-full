""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: file_filter/profile
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

class ProfileRulesFiletypeItem(TypedDict, total=False):
    """Nested item for rules.file-type field."""
    name: str


class ProfileRulesItem(TypedDict, total=False):
    """Nested item for rules field."""
    name: str
    comment: str
    protocol: Literal["http", "ftp", "smtp", "imap", "pop3", "mapi", "cifs", "ssh"]
    action: Literal["log-only", "block"]
    direction: Literal["incoming", "outgoing", "any"]
    password_protected: Literal["yes", "any"]
    file_type: str | list[str] | list[ProfileRulesFiletypeItem]


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    comment: str
    feature_set: Literal["flow", "proxy"]
    replacemsg_group: str
    log: Literal["disable", "enable"]
    extended_log: Literal["disable", "enable"]
    scan_archive_contents: Literal["disable", "enable"]
    rules: str | list[str] | list[ProfileRulesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    comment: str
    feature_set: Literal["flow", "proxy"]
    replacemsg_group: str
    log: Literal["disable", "enable"]
    extended_log: Literal["disable", "enable"]
    scan_archive_contents: Literal["disable", "enable"]
    rules: list[ProfileRulesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileRulesFiletypeItemObject(FortiObject[ProfileRulesFiletypeItem]):
    """Typed object for rules.file-type table items with attribute access."""
    name: str


class ProfileRulesItemObject(FortiObject[ProfileRulesItem]):
    """Typed object for rules table items with attribute access."""
    name: str
    comment: str
    protocol: Literal["http", "ftp", "smtp", "imap", "pop3", "mapi", "cifs", "ssh"]
    action: Literal["log-only", "block"]
    direction: Literal["incoming", "outgoing", "any"]
    password_protected: Literal["yes", "any"]
    file_type: FortiObjectList[ProfileRulesFiletypeItemObject]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    comment: str
    feature_set: Literal["flow", "proxy"]
    replacemsg_group: str
    log: Literal["disable", "enable"]
    extended_log: Literal["disable", "enable"]
    scan_archive_contents: Literal["disable", "enable"]
    rules: FortiObjectList[ProfileRulesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: file_filter/profile
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
        feature_set: Literal["flow", "proxy"] | None = ...,
        replacemsg_group: str | None = ...,
        log: Literal["disable", "enable"] | None = ...,
        extended_log: Literal["disable", "enable"] | None = ...,
        scan_archive_contents: Literal["disable", "enable"] | None = ...,
        rules: str | list[str] | list[ProfileRulesItem] | None = ...,
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
        feature_set: Literal["flow", "proxy"] | None = ...,
        replacemsg_group: str | None = ...,
        log: Literal["disable", "enable"] | None = ...,
        extended_log: Literal["disable", "enable"] | None = ...,
        scan_archive_contents: Literal["disable", "enable"] | None = ...,
        rules: str | list[str] | list[ProfileRulesItem] | None = ...,
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
        feature_set: Literal["flow", "proxy"] | None = ...,
        replacemsg_group: str | None = ...,
        log: Literal["disable", "enable"] | None = ...,
        extended_log: Literal["disable", "enable"] | None = ...,
        scan_archive_contents: Literal["disable", "enable"] | None = ...,
        rules: str | list[str] | list[ProfileRulesItem] | None = ...,
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