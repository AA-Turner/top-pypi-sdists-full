""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/mpsk_profile
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

class MpskProfileMpskgroupMpskkeyItem(TypedDict, total=False):
    """Nested item for mpsk-group.mpsk-key field."""
    name: str
    key_type: Literal["wpa2-personal", "wpa3-sae"]
    mac: str
    passphrase: str
    sae_password: str
    sae_pk: Literal["enable", "disable"]
    sae_private_key: str
    concurrent_client_limit_type: Literal["default", "unlimited", "specified"]
    concurrent_clients: int
    comment: str
    mpsk_schedules: str | list[str]


class MpskProfileMpskgroupItem(TypedDict, total=False):
    """Nested item for mpsk-group field."""
    name: str
    vlan_type: Literal["no-vlan", "fixed-vlan"]
    vlan_id: int
    mpsk_key: str | list[str] | list[MpskProfileMpskgroupMpskkeyItem]


class MpskProfilePayload(TypedDict, total=False):
    """Payload type for MpskProfile operations."""
    name: str
    mpsk_concurrent_clients: int
    mpsk_external_server_auth: Literal["enable", "disable"]
    mpsk_external_server: str
    mpsk_type: Literal["wpa2-personal", "wpa3-sae", "wpa3-sae-transition"]
    mpsk_group: str | list[str] | list[MpskProfileMpskgroupItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class MpskProfileResponse(TypedDict, total=False):
    """Response type for MpskProfile - use with .dict property for typed dict access."""
    name: str
    mpsk_concurrent_clients: int
    mpsk_external_server_auth: Literal["enable", "disable"]
    mpsk_external_server: str
    mpsk_type: Literal["wpa2-personal", "wpa3-sae", "wpa3-sae-transition"]
    mpsk_group: list[MpskProfileMpskgroupItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class MpskProfileMpskgroupMpskkeyItemObject(FortiObject[MpskProfileMpskgroupMpskkeyItem]):
    """Typed object for mpsk-group.mpsk-key table items with attribute access."""
    name: str
    key_type: Literal["wpa2-personal", "wpa3-sae"]
    mac: str
    passphrase: str
    sae_password: str
    sae_pk: Literal["enable", "disable"]
    sae_private_key: str
    concurrent_client_limit_type: Literal["default", "unlimited", "specified"]
    concurrent_clients: int
    comment: str
    mpsk_schedules: str | list[str]


class MpskProfileMpskgroupItemObject(FortiObject[MpskProfileMpskgroupItem]):
    """Typed object for mpsk-group table items with attribute access."""
    name: str
    vlan_type: Literal["no-vlan", "fixed-vlan"]
    vlan_id: int
    mpsk_key: FortiObjectList[MpskProfileMpskgroupMpskkeyItemObject]


class MpskProfileObject(FortiObject):
    """Typed FortiObject for MpskProfile with field access."""
    name: str
    mpsk_concurrent_clients: int
    mpsk_external_server_auth: Literal["enable", "disable"]
    mpsk_external_server: str
    mpsk_type: Literal["wpa2-personal", "wpa3-sae", "wpa3-sae-transition"]
    mpsk_group: FortiObjectList[MpskProfileMpskgroupItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class MpskProfile:
    """
    
    Endpoint: wireless_controller/mpsk_profile
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
    ) -> MpskProfileObject: ...
    
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
    ) -> FortiObjectList[MpskProfileObject]: ...
    
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
        payload_dict: MpskProfilePayload | None = ...,
        name: str | None = ...,
        mpsk_concurrent_clients: int | None = ...,
        mpsk_external_server_auth: Literal["enable", "disable"] | None = ...,
        mpsk_external_server: str | None = ...,
        mpsk_type: Literal["wpa2-personal", "wpa3-sae", "wpa3-sae-transition"] | None = ...,
        mpsk_group: str | list[str] | list[MpskProfileMpskgroupItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MpskProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: MpskProfilePayload | None = ...,
        name: str | None = ...,
        mpsk_concurrent_clients: int | None = ...,
        mpsk_external_server_auth: Literal["enable", "disable"] | None = ...,
        mpsk_external_server: str | None = ...,
        mpsk_type: Literal["wpa2-personal", "wpa3-sae", "wpa3-sae-transition"] | None = ...,
        mpsk_group: str | list[str] | list[MpskProfileMpskgroupItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MpskProfileObject: ...

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
        payload_dict: MpskProfilePayload | None = ...,
        name: str | None = ...,
        mpsk_concurrent_clients: int | None = ...,
        mpsk_external_server_auth: Literal["enable", "disable"] | None = ...,
        mpsk_external_server: str | None = ...,
        mpsk_type: Literal["wpa2-personal", "wpa3-sae", "wpa3-sae-transition"] | None = ...,
        mpsk_group: str | list[str] | list[MpskProfileMpskgroupItem] | None = ...,
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
    "MpskProfile",
    "MpskProfilePayload",
    "MpskProfileResponse",
    "MpskProfileObject",
]