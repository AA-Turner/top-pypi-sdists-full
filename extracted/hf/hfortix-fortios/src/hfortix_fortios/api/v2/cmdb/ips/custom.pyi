""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ips/custom
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

class CustomPayload(TypedDict, total=False):
    """Payload type for Custom operations."""
    tag: str
    signature: str
    rule_id: int
    severity: str
    location: str | list[str]
    os: str | list[str]
    application: str | list[str]
    protocol: str
    status: Literal["disable", "enable"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    action: Literal["pass", "block"]
    comment: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CustomResponse(TypedDict, total=False):
    """Response type for Custom - use with .dict property for typed dict access."""
    tag: str
    signature: str
    rule_id: int
    severity: str
    location: str | list[str]
    os: str | list[str]
    application: str | list[str]
    protocol: str
    status: Literal["disable", "enable"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    action: Literal["pass", "block"]
    comment: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CustomObject(FortiObject):
    """Typed FortiObject for Custom with field access."""
    tag: str
    signature: str
    rule_id: int
    severity: str
    location: str | list[str]
    os: str | list[str]
    application: str | list[str]
    protocol: str
    status: Literal["disable", "enable"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    action: Literal["pass", "block"]
    comment: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Custom:
    """
    
    Endpoint: ips/custom
    Category: cmdb
    MKey: tag
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
        tag: str,
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
    ) -> CustomObject: ...
    
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
    ) -> FortiObjectList[CustomObject]: ...
    
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
        payload_dict: CustomPayload | None = ...,
        tag: str | None = ...,
        signature: str | None = ...,
        rule_id: int | None = ...,
        severity: str | None = ...,
        location: str | list[str] | None = ...,
        os: str | list[str] | None = ...,
        application: str | list[str] | None = ...,
        protocol: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        log: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        action: Literal["pass", "block"] | None = ...,
        comment: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CustomObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CustomPayload | None = ...,
        tag: str | None = ...,
        signature: str | None = ...,
        rule_id: int | None = ...,
        severity: str | None = ...,
        location: str | list[str] | None = ...,
        os: str | list[str] | None = ...,
        application: str | list[str] | None = ...,
        protocol: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        log: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        action: Literal["pass", "block"] | None = ...,
        comment: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CustomObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        tag: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        tag: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_tag: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        tag: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: CustomPayload | None = ...,
        tag: str | None = ...,
        signature: str | None = ...,
        rule_id: int | None = ...,
        severity: str | None = ...,
        location: str | list[str] | None = ...,
        os: str | list[str] | None = ...,
        application: str | list[str] | None = ...,
        protocol: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        log: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        action: Literal["pass", "block"] | None = ...,
        comment: str | None = ...,
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
    "Custom",
    "CustomPayload",
    "CustomResponse",
    "CustomObject",
]