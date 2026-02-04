""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/fortilink_settings
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

class FortilinkSettingsNacportsNacsegmentvlansItem(TypedDict, total=False):
    """Nested item for nac-ports.nac-segment-vlans field."""
    vlan_name: str


class FortilinkSettingsNacportsDict(TypedDict, total=False):
    """Nested object type for nac-ports field."""
    onboarding_vlan: str
    lan_segment: Literal["enabled", "disabled"]
    nac_lan_interface: str
    nac_segment_vlans: str | list[str] | list[FortilinkSettingsNacportsNacsegmentvlansItem]
    parent_key: str
    member_change: int


class FortilinkSettingsPayload(TypedDict, total=False):
    """Payload type for FortilinkSettings operations."""
    name: str
    fortilink: str
    inactive_timer: int
    link_down_flush: Literal["disable", "enable"]
    access_vlan_mode: Literal["legacy", "fail-open", "fail-close"]
    nac_ports: FortilinkSettingsNacportsDict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FortilinkSettingsResponse(TypedDict, total=False):
    """Response type for FortilinkSettings - use with .dict property for typed dict access."""
    name: str
    fortilink: str
    inactive_timer: int
    link_down_flush: Literal["disable", "enable"]
    access_vlan_mode: Literal["legacy", "fail-open", "fail-close"]
    nac_ports: FortilinkSettingsNacportsDict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FortilinkSettingsNacportsNacsegmentvlansItemObject(FortiObject[FortilinkSettingsNacportsNacsegmentvlansItem]):
    """Typed object for nac-ports.nac-segment-vlans table items with attribute access."""
    vlan_name: str


class FortilinkSettingsNacportsObject(FortiObject):
    """Nested object for nac-ports field with attribute access."""
    onboarding_vlan: str
    lan_segment: Literal["enabled", "disabled"]
    nac_lan_interface: str
    nac_segment_vlans: str | list[str]
    parent_key: str
    member_change: int


class FortilinkSettingsObject(FortiObject):
    """Typed FortiObject for FortilinkSettings with field access."""
    name: str
    fortilink: str
    inactive_timer: int
    link_down_flush: Literal["disable", "enable"]
    access_vlan_mode: Literal["legacy", "fail-open", "fail-close"]
    nac_ports: FortilinkSettingsNacportsObject


# ================================================================
# Main Endpoint Class
# ================================================================

class FortilinkSettings:
    """
    
    Endpoint: switch_controller/fortilink_settings
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
    ) -> FortilinkSettingsObject: ...
    
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
    ) -> FortiObjectList[FortilinkSettingsObject]: ...
    
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
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: FortilinkSettingsNacportsDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortilinkSettingsObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: FortilinkSettingsNacportsDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortilinkSettingsObject: ...

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
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: FortilinkSettingsNacportsDict | None = ...,
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
    "FortilinkSettings",
    "FortilinkSettingsPayload",
    "FortilinkSettingsResponse",
    "FortilinkSettingsObject",
]