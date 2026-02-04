""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: webfilter/ftgd_local_risk
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

class FtgdLocalRiskPayload(TypedDict, total=False):
    """Payload type for FtgdLocalRisk operations."""
    url: str
    status: Literal["enable", "disable"]
    comment: str
    risk_score: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FtgdLocalRiskResponse(TypedDict, total=False):
    """Response type for FtgdLocalRisk - use with .dict property for typed dict access."""
    url: str
    status: Literal["enable", "disable"]
    comment: str
    risk_score: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FtgdLocalRiskObject(FortiObject):
    """Typed FortiObject for FtgdLocalRisk with field access."""
    url: str
    status: Literal["enable", "disable"]
    comment: str
    risk_score: int


# ================================================================
# Main Endpoint Class
# ================================================================

class FtgdLocalRisk:
    """
    
    Endpoint: webfilter/ftgd_local_risk
    Category: cmdb
    MKey: url
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
        url: str,
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
    ) -> FtgdLocalRiskObject: ...
    
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
    ) -> FortiObjectList[FtgdLocalRiskObject]: ...
    
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
        payload_dict: FtgdLocalRiskPayload | None = ...,
        url: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comment: str | None = ...,
        risk_score: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FtgdLocalRiskObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FtgdLocalRiskPayload | None = ...,
        url: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comment: str | None = ...,
        risk_score: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FtgdLocalRiskObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        url: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        url: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_url: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        url: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FtgdLocalRiskPayload | None = ...,
        url: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comment: str | None = ...,
        risk_score: int | None = ...,
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
    "FtgdLocalRisk",
    "FtgdLocalRiskPayload",
    "FtgdLocalRiskResponse",
    "FtgdLocalRiskObject",
]