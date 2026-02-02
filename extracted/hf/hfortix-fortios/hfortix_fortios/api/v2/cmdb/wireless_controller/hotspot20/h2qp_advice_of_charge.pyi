""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/h2qp_advice_of_charge
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

class H2qpAdviceOfChargeAoclistPlaninfoItem(TypedDict, total=False):
    """Nested item for aoc-list.plan-info field."""
    name: str
    lang: str
    currency: str
    info_file: str


class H2qpAdviceOfChargeAoclistItem(TypedDict, total=False):
    """Nested item for aoc-list field."""
    name: str
    type: Literal["time-based", "volume-based", "time-and-volume-based", "unlimited"]
    nai_realm_encoding: str
    nai_realm: str
    plan_info: str | list[str] | list[H2qpAdviceOfChargeAoclistPlaninfoItem]


class H2qpAdviceOfChargePayload(TypedDict, total=False):
    """Payload type for H2qpAdviceOfCharge operations."""
    name: str
    aoc_list: str | list[str] | list[H2qpAdviceOfChargeAoclistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class H2qpAdviceOfChargeResponse(TypedDict, total=False):
    """Response type for H2qpAdviceOfCharge - use with .dict property for typed dict access."""
    name: str
    aoc_list: list[H2qpAdviceOfChargeAoclistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class H2qpAdviceOfChargeAoclistPlaninfoItemObject(FortiObject[H2qpAdviceOfChargeAoclistPlaninfoItem]):
    """Typed object for aoc-list.plan-info table items with attribute access."""
    name: str
    lang: str
    currency: str
    info_file: str


class H2qpAdviceOfChargeAoclistItemObject(FortiObject[H2qpAdviceOfChargeAoclistItem]):
    """Typed object for aoc-list table items with attribute access."""
    name: str
    type: Literal["time-based", "volume-based", "time-and-volume-based", "unlimited"]
    nai_realm_encoding: str
    nai_realm: str
    plan_info: FortiObjectList[H2qpAdviceOfChargeAoclistPlaninfoItemObject]


class H2qpAdviceOfChargeObject(FortiObject):
    """Typed FortiObject for H2qpAdviceOfCharge with field access."""
    name: str
    aoc_list: FortiObjectList[H2qpAdviceOfChargeAoclistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class H2qpAdviceOfCharge:
    """
    
    Endpoint: wireless_controller/hotspot20/h2qp_advice_of_charge
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
    ) -> H2qpAdviceOfChargeObject: ...
    
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
    ) -> FortiObjectList[H2qpAdviceOfChargeObject]: ...
    
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
        payload_dict: H2qpAdviceOfChargePayload | None = ...,
        name: str | None = ...,
        aoc_list: str | list[str] | list[H2qpAdviceOfChargeAoclistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpAdviceOfChargeObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: H2qpAdviceOfChargePayload | None = ...,
        name: str | None = ...,
        aoc_list: str | list[str] | list[H2qpAdviceOfChargeAoclistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpAdviceOfChargeObject: ...

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
        payload_dict: H2qpAdviceOfChargePayload | None = ...,
        name: str | None = ...,
        aoc_list: str | list[str] | list[H2qpAdviceOfChargeAoclistItem] | None = ...,
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
    "H2qpAdviceOfCharge",
    "H2qpAdviceOfChargePayload",
    "H2qpAdviceOfChargeResponse",
    "H2qpAdviceOfChargeObject",
]