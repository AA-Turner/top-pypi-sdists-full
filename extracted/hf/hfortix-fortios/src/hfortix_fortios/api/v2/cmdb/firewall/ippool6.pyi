""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/ippool6
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

class Ippool6Payload(TypedDict, total=False):
    """Payload type for Ippool6 operations."""
    name: str
    type: Literal["overload", "nptv6"]
    startip: str
    endip: str
    internal_prefix: str
    external_prefix: str
    comments: str
    nat46: Literal["disable", "enable"]
    add_nat46_route: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Ippool6Response(TypedDict, total=False):
    """Response type for Ippool6 - use with .dict property for typed dict access."""
    name: str
    type: Literal["overload", "nptv6"]
    startip: str
    endip: str
    internal_prefix: str
    external_prefix: str
    comments: str
    nat46: Literal["disable", "enable"]
    add_nat46_route: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Ippool6Object(FortiObject):
    """Typed FortiObject for Ippool6 with field access."""
    name: str
    type: Literal["overload", "nptv6"]
    startip: str
    endip: str
    internal_prefix: str
    external_prefix: str
    comments: str
    nat46: Literal["disable", "enable"]
    add_nat46_route: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Ippool6:
    """
    
    Endpoint: firewall/ippool6
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
    ) -> Ippool6Object: ...
    
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
    ) -> FortiObjectList[Ippool6Object]: ...
    
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
        payload_dict: Ippool6Payload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "nptv6"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        internal_prefix: str | None = ...,
        external_prefix: str | None = ...,
        comments: str | None = ...,
        nat46: Literal["disable", "enable"] | None = ...,
        add_nat46_route: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Ippool6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Ippool6Payload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "nptv6"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        internal_prefix: str | None = ...,
        external_prefix: str | None = ...,
        comments: str | None = ...,
        nat46: Literal["disable", "enable"] | None = ...,
        add_nat46_route: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Ippool6Object: ...

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
        payload_dict: Ippool6Payload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "nptv6"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        internal_prefix: str | None = ...,
        external_prefix: str | None = ...,
        comments: str | None = ...,
        nat46: Literal["disable", "enable"] | None = ...,
        add_nat46_route: Literal["disable", "enable"] | None = ...,
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
    "Ippool6",
    "Ippool6Payload",
    "Ippool6Response",
    "Ippool6Object",
]