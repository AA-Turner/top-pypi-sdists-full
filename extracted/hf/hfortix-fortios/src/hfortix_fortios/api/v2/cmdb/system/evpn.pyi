""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/evpn
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

class EvpnImportrtItem(TypedDict, total=False):
    """Nested item for import-rt field."""
    route_target: str


class EvpnExportrtItem(TypedDict, total=False):
    """Nested item for export-rt field."""
    route_target: str


class EvpnPayload(TypedDict, total=False):
    """Payload type for Evpn operations."""
    id: int
    rd: str
    import_rt: str | list[str] | list[EvpnImportrtItem]
    export_rt: str | list[str] | list[EvpnExportrtItem]
    ip_local_learning: Literal["enable", "disable"]
    arp_suppression: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class EvpnResponse(TypedDict, total=False):
    """Response type for Evpn - use with .dict property for typed dict access."""
    id: int
    rd: str
    import_rt: list[EvpnImportrtItem]
    export_rt: list[EvpnExportrtItem]
    ip_local_learning: Literal["enable", "disable"]
    arp_suppression: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class EvpnImportrtItemObject(FortiObject[EvpnImportrtItem]):
    """Typed object for import-rt table items with attribute access."""
    route_target: str


class EvpnExportrtItemObject(FortiObject[EvpnExportrtItem]):
    """Typed object for export-rt table items with attribute access."""
    route_target: str


class EvpnObject(FortiObject):
    """Typed FortiObject for Evpn with field access."""
    id: int
    rd: str
    import_rt: FortiObjectList[EvpnImportrtItemObject]
    export_rt: FortiObjectList[EvpnExportrtItemObject]
    ip_local_learning: Literal["enable", "disable"]
    arp_suppression: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Evpn:
    """
    
    Endpoint: system/evpn
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> EvpnObject: ...
    
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
    ) -> FortiObjectList[EvpnObject]: ...
    
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
        payload_dict: EvpnPayload | None = ...,
        id: int | None = ...,
        rd: str | None = ...,
        import_rt: str | list[str] | list[EvpnImportrtItem] | None = ...,
        export_rt: str | list[str] | list[EvpnExportrtItem] | None = ...,
        ip_local_learning: Literal["enable", "disable"] | None = ...,
        arp_suppression: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> EvpnObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: EvpnPayload | None = ...,
        id: int | None = ...,
        rd: str | None = ...,
        import_rt: str | list[str] | list[EvpnImportrtItem] | None = ...,
        export_rt: str | list[str] | list[EvpnExportrtItem] | None = ...,
        ip_local_learning: Literal["enable", "disable"] | None = ...,
        arp_suppression: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> EvpnObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: EvpnPayload | None = ...,
        id: int | None = ...,
        rd: str | None = ...,
        import_rt: str | list[str] | list[EvpnImportrtItem] | None = ...,
        export_rt: str | list[str] | list[EvpnExportrtItem] | None = ...,
        ip_local_learning: Literal["enable", "disable"] | None = ...,
        arp_suppression: Literal["enable", "disable"] | None = ...,
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
    "Evpn",
    "EvpnPayload",
    "EvpnResponse",
    "EvpnObject",
]