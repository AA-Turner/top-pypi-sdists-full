""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/ble_profile
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

class BleProfilePayload(TypedDict, total=False):
    """Payload type for BleProfile operations."""
    name: str
    comment: str
    advertising: str | list[str]
    ibeacon_uuid: str
    major_id: int
    minor_id: int
    eddystone_namespace: str
    eddystone_instance: str
    eddystone_url: str
    txpower: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
    beacon_interval: int
    ble_scanning: Literal["enable", "disable"]
    scan_type: Literal["active", "passive"]
    scan_threshold: str
    scan_period: int
    scan_time: int
    scan_interval: int
    scan_window: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class BleProfileResponse(TypedDict, total=False):
    """Response type for BleProfile - use with .dict property for typed dict access."""
    name: str
    comment: str
    advertising: str
    ibeacon_uuid: str
    major_id: int
    minor_id: int
    eddystone_namespace: str
    eddystone_instance: str
    eddystone_url: str
    txpower: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
    beacon_interval: int
    ble_scanning: Literal["enable", "disable"]
    scan_type: Literal["active", "passive"]
    scan_threshold: str
    scan_period: int
    scan_time: int
    scan_interval: int
    scan_window: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class BleProfileObject(FortiObject):
    """Typed FortiObject for BleProfile with field access."""
    name: str
    comment: str
    advertising: str
    ibeacon_uuid: str
    major_id: int
    minor_id: int
    eddystone_namespace: str
    eddystone_instance: str
    eddystone_url: str
    txpower: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
    beacon_interval: int
    ble_scanning: Literal["enable", "disable"]
    scan_type: Literal["active", "passive"]
    scan_threshold: str
    scan_period: int
    scan_time: int
    scan_interval: int
    scan_window: int


# ================================================================
# Main Endpoint Class
# ================================================================

class BleProfile:
    """
    
    Endpoint: wireless_controller/ble_profile
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
    ) -> BleProfileObject: ...
    
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
    ) -> FortiObjectList[BleProfileObject]: ...
    
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
        payload_dict: BleProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        advertising: str | list[str] | None = ...,
        ibeacon_uuid: str | None = ...,
        major_id: int | None = ...,
        minor_id: int | None = ...,
        eddystone_namespace: str | None = ...,
        eddystone_instance: str | None = ...,
        eddystone_url: str | None = ...,
        txpower: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"] | None = ...,
        beacon_interval: int | None = ...,
        ble_scanning: Literal["enable", "disable"] | None = ...,
        scan_type: Literal["active", "passive"] | None = ...,
        scan_threshold: str | None = ...,
        scan_period: int | None = ...,
        scan_time: int | None = ...,
        scan_interval: int | None = ...,
        scan_window: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BleProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: BleProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        advertising: str | list[str] | None = ...,
        ibeacon_uuid: str | None = ...,
        major_id: int | None = ...,
        minor_id: int | None = ...,
        eddystone_namespace: str | None = ...,
        eddystone_instance: str | None = ...,
        eddystone_url: str | None = ...,
        txpower: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"] | None = ...,
        beacon_interval: int | None = ...,
        ble_scanning: Literal["enable", "disable"] | None = ...,
        scan_type: Literal["active", "passive"] | None = ...,
        scan_threshold: str | None = ...,
        scan_period: int | None = ...,
        scan_time: int | None = ...,
        scan_interval: int | None = ...,
        scan_window: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BleProfileObject: ...

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
        payload_dict: BleProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        advertising: Literal["ibeacon", "eddystone-uid", "eddystone-url"] | list[str] | None = ...,
        ibeacon_uuid: str | None = ...,
        major_id: int | None = ...,
        minor_id: int | None = ...,
        eddystone_namespace: str | None = ...,
        eddystone_instance: str | None = ...,
        eddystone_url: str | None = ...,
        txpower: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"] | None = ...,
        beacon_interval: int | None = ...,
        ble_scanning: Literal["enable", "disable"] | None = ...,
        scan_type: Literal["active", "passive"] | None = ...,
        scan_threshold: str | None = ...,
        scan_period: int | None = ...,
        scan_time: int | None = ...,
        scan_interval: int | None = ...,
        scan_window: int | None = ...,
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
    "BleProfile",
    "BleProfilePayload",
    "BleProfileResponse",
    "BleProfileObject",
]