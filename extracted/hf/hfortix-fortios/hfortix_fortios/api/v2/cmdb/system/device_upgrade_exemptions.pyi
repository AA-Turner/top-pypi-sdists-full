""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/device_upgrade_exemptions
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

class DeviceUpgradeExemptionsPayload(TypedDict, total=False):
    """Payload type for DeviceUpgradeExemptions operations."""
    id: int
    fortinet_device: str
    version: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DeviceUpgradeExemptionsResponse(TypedDict, total=False):
    """Response type for DeviceUpgradeExemptions - use with .dict property for typed dict access."""
    id: int
    fortinet_device: str
    version: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DeviceUpgradeExemptionsObject(FortiObject):
    """Typed FortiObject for DeviceUpgradeExemptions with field access."""
    id: int
    fortinet_device: str


# ================================================================
# Main Endpoint Class
# ================================================================

class DeviceUpgradeExemptions:
    """
    
    Endpoint: system/device_upgrade_exemptions
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DeviceUpgradeExemptionsObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[DeviceUpgradeExemptionsObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: DeviceUpgradeExemptionsPayload | None = ...,
        id: int | None = ...,
        fortinet_device: str | None = ...,
        version: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DeviceUpgradeExemptionsObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DeviceUpgradeExemptionsPayload | None = ...,
        id: int | None = ...,
        fortinet_device: str | None = ...,
        version: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DeviceUpgradeExemptionsObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DeviceUpgradeExemptionsPayload | None = ...,
        id: int | None = ...,
        fortinet_device: str | None = ...,
        version: str | None = ...,
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
    "DeviceUpgradeExemptions",
    "DeviceUpgradeExemptionsPayload",
    "DeviceUpgradeExemptionsResponse",
    "DeviceUpgradeExemptionsObject",
]