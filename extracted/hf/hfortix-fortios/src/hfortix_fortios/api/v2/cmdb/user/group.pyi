""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/group
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

class GroupMemberItem(TypedDict, total=False):
    """Nested item for member field."""
    name: str


class GroupMatchItem(TypedDict, total=False):
    """Nested item for match field."""
    id: int
    server_name: str
    group_name: str


class GroupGuestItem(TypedDict, total=False):
    """Nested item for guest field."""
    id: int
    user_id: str
    name: str
    password: str
    mobile_phone: str
    sponsor: str
    company: str
    email: str
    expiration: str
    comment: str


class GroupPayload(TypedDict, total=False):
    """Payload type for Group operations."""
    name: str
    id: int
    group_type: Literal["firewall", "fsso-service", "rsso", "guest"]
    authtimeout: int
    auth_concurrent_override: Literal["enable", "disable"]
    auth_concurrent_value: int
    http_digest_realm: str
    sso_attribute_value: str
    member: str | list[str] | list[GroupMemberItem]
    match: str | list[str] | list[GroupMatchItem]
    user_id: Literal["email", "auto-generate", "specify"]
    password: Literal["auto-generate", "specify", "disable"]
    user_name: Literal["disable", "enable"]
    sponsor: Literal["optional", "mandatory", "disabled"]
    company: Literal["optional", "mandatory", "disabled"]
    email: Literal["disable", "enable"]
    mobile_phone: Literal["disable", "enable"]
    sms_server: Literal["fortiguard", "custom"]
    sms_custom_server: str
    expire_type: Literal["immediately", "first-successful-login"]
    expire: int
    max_accounts: int
    multiple_guest_add: Literal["disable", "enable"]
    guest: str | list[str] | list[GroupGuestItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GroupResponse(TypedDict, total=False):
    """Response type for Group - use with .dict property for typed dict access."""
    name: str
    id: int
    group_type: Literal["firewall", "fsso-service", "rsso", "guest"]
    authtimeout: int
    auth_concurrent_override: Literal["enable", "disable"]
    auth_concurrent_value: int
    http_digest_realm: str
    sso_attribute_value: str
    member: list[GroupMemberItem]
    match: list[GroupMatchItem]
    user_id: Literal["email", "auto-generate", "specify"]
    password: Literal["auto-generate", "specify", "disable"]
    user_name: Literal["disable", "enable"]
    sponsor: Literal["optional", "mandatory", "disabled"]
    company: Literal["optional", "mandatory", "disabled"]
    email: Literal["disable", "enable"]
    mobile_phone: Literal["disable", "enable"]
    sms_server: Literal["fortiguard", "custom"]
    sms_custom_server: str
    expire_type: Literal["immediately", "first-successful-login"]
    expire: int
    max_accounts: int
    multiple_guest_add: Literal["disable", "enable"]
    guest: list[GroupGuestItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GroupMemberItemObject(FortiObject[GroupMemberItem]):
    """Typed object for member table items with attribute access."""
    name: str


class GroupMatchItemObject(FortiObject[GroupMatchItem]):
    """Typed object for match table items with attribute access."""
    id: int
    server_name: str
    group_name: str


class GroupGuestItemObject(FortiObject[GroupGuestItem]):
    """Typed object for guest table items with attribute access."""
    id: int
    user_id: str
    name: str
    password: str
    mobile_phone: str
    sponsor: str
    company: str
    email: str
    expiration: str
    comment: str


class GroupObject(FortiObject):
    """Typed FortiObject for Group with field access."""
    name: str
    id: int
    group_type: Literal["firewall", "fsso-service", "rsso", "guest"]
    authtimeout: int
    auth_concurrent_override: Literal["enable", "disable"]
    auth_concurrent_value: int
    http_digest_realm: str
    sso_attribute_value: str
    member: FortiObjectList[GroupMemberItemObject]
    match: FortiObjectList[GroupMatchItemObject]
    user_id: Literal["email", "auto-generate", "specify"]
    password: Literal["auto-generate", "specify", "disable"]
    user_name: Literal["disable", "enable"]
    sponsor: Literal["optional", "mandatory", "disabled"]
    company: Literal["optional", "mandatory", "disabled"]
    email: Literal["disable", "enable"]
    mobile_phone: Literal["disable", "enable"]
    sms_server: Literal["fortiguard", "custom"]
    sms_custom_server: str
    expire_type: Literal["immediately", "first-successful-login"]
    expire: int
    max_accounts: int
    multiple_guest_add: Literal["disable", "enable"]
    guest: FortiObjectList[GroupGuestItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Group:
    """
    
    Endpoint: user/group
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
    ) -> GroupObject: ...
    
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
    ) -> FortiObjectList[GroupObject]: ...
    
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
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[GroupMemberItem] | None = ...,
        match: str | list[str] | list[GroupMatchItem] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[GroupGuestItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GroupObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[GroupMemberItem] | None = ...,
        match: str | list[str] | list[GroupMatchItem] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[GroupGuestItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GroupObject: ...

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
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[GroupMemberItem] | None = ...,
        match: str | list[str] | list[GroupMatchItem] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[GroupGuestItem] | None = ...,
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
    "Group",
    "GroupPayload",
    "GroupResponse",
    "GroupObject",
]