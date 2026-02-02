""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/quarantine
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class QuarantineTargetsMacsItem(TypedDict, total=False):
    """Nested item for targets.macs field."""
    mac: str
    description: str
    drop: Literal["disable", "enable"]
    parent: str


class QuarantineTargetsItem(TypedDict, total=False):
    """Nested item for targets field."""
    entry: str
    description: str
    macs: str | list[str] | list[QuarantineTargetsMacsItem]


class QuarantinePayload(TypedDict, total=False):
    """Payload type for Quarantine operations."""
    quarantine: Literal["enable", "disable"]
    traffic_policy: str
    firewall_groups: str
    targets: str | list[str] | list[QuarantineTargetsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class QuarantineResponse(TypedDict, total=False):
    """Response type for Quarantine - use with .dict property for typed dict access."""
    quarantine: Literal["enable", "disable"]
    traffic_policy: str
    firewall_groups: str
    targets: list[QuarantineTargetsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class QuarantineTargetsMacsItemObject(FortiObject[QuarantineTargetsMacsItem]):
    """Typed object for targets.macs table items with attribute access."""
    mac: str
    description: str
    drop: Literal["disable", "enable"]
    parent: str


class QuarantineTargetsItemObject(FortiObject[QuarantineTargetsItem]):
    """Typed object for targets table items with attribute access."""
    entry: str
    description: str
    macs: FortiObjectList[QuarantineTargetsMacsItemObject]


class QuarantineObject(FortiObject):
    """Typed FortiObject for Quarantine with field access."""
    quarantine: Literal["enable", "disable"]
    traffic_policy: str
    firewall_groups: str
    targets: FortiObjectList[QuarantineTargetsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Quarantine:
    """
    
    Endpoint: user/quarantine
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Singleton endpoint (no mkey)
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
    ) -> QuarantineObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: QuarantinePayload | None = ...,
        quarantine: Literal["enable", "disable"] | None = ...,
        traffic_policy: str | None = ...,
        firewall_groups: str | None = ...,
        targets: str | list[str] | list[QuarantineTargetsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QuarantineObject: ...


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
        payload_dict: QuarantinePayload | None = ...,
        quarantine: Literal["enable", "disable"] | None = ...,
        traffic_policy: str | None = ...,
        firewall_groups: str | None = ...,
        targets: str | list[str] | list[QuarantineTargetsItem] | None = ...,
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
    "Quarantine",
    "QuarantinePayload",
    "QuarantineResponse",
    "QuarantineObject",
]