""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/anqp_3gpp_cellular
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

class Anqp3gppCellularMccmnclistItem(TypedDict, total=False):
    """Nested item for mcc-mnc-list field."""
    id: int
    mcc: str
    mnc: str


class Anqp3gppCellularPayload(TypedDict, total=False):
    """Payload type for Anqp3gppCellular operations."""
    name: str
    mcc_mnc_list: str | list[str] | list[Anqp3gppCellularMccmnclistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Anqp3gppCellularResponse(TypedDict, total=False):
    """Response type for Anqp3gppCellular - use with .dict property for typed dict access."""
    name: str
    mcc_mnc_list: list[Anqp3gppCellularMccmnclistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Anqp3gppCellularMccmnclistItemObject(FortiObject[Anqp3gppCellularMccmnclistItem]):
    """Typed object for mcc-mnc-list table items with attribute access."""
    id: int
    mcc: str
    mnc: str


class Anqp3gppCellularObject(FortiObject):
    """Typed FortiObject for Anqp3gppCellular with field access."""
    name: str
    mcc_mnc_list: FortiObjectList[Anqp3gppCellularMccmnclistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Anqp3gppCellular:
    """
    
    Endpoint: wireless_controller/hotspot20/anqp_3gpp_cellular
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
    ) -> Anqp3gppCellularObject: ...
    
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
    ) -> FortiObjectList[Anqp3gppCellularObject]: ...
    
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
        payload_dict: Anqp3gppCellularPayload | None = ...,
        name: str | None = ...,
        mcc_mnc_list: str | list[str] | list[Anqp3gppCellularMccmnclistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Anqp3gppCellularObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Anqp3gppCellularPayload | None = ...,
        name: str | None = ...,
        mcc_mnc_list: str | list[str] | list[Anqp3gppCellularMccmnclistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Anqp3gppCellularObject: ...

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
        payload_dict: Anqp3gppCellularPayload | None = ...,
        name: str | None = ...,
        mcc_mnc_list: str | list[str] | list[Anqp3gppCellularMccmnclistItem] | None = ...,
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
    "Anqp3gppCellular",
    "Anqp3gppCellularPayload",
    "Anqp3gppCellularResponse",
    "Anqp3gppCellularObject",
]