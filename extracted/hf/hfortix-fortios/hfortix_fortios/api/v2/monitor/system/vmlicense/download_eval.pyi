""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/vmlicense/download_eval
Category: monitor
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

class DownloadEvalPayload(TypedDict, total=False):
    """Payload type for DownloadEval operations."""
    account_id: str
    account_password: str
    is_government: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class DownloadEvalResponse(TypedDict, total=False):
    """Response type for DownloadEval - use with .dict property for typed dict access."""
    forticare_error_code: int
    forticare_error_message: str


class DownloadEvalObject(FortiObject[DownloadEvalResponse]):
    """Typed FortiObject for DownloadEval with field access."""
    forticare_error_code: int
    forticare_error_message: str



# ================================================================
# Main Endpoint Class
# ================================================================

class DownloadEval:
    """
    
    Endpoint: system/vmlicense/download_eval
    Category: monitor
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
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[DownloadEvalObject]: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: DownloadEvalPayload | None = ...,
        account_id: str | None = ...,
        account_password: str | None = ...,
        is_government: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DownloadEvalObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DownloadEvalPayload | None = ...,
        account_id: str | None = ...,
        account_password: str | None = ...,
        is_government: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DownloadEvalObject: ...


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
        payload_dict: DownloadEvalPayload | None = ...,
        account_id: str | None = ...,
        account_password: str | None = ...,
        is_government: bool | None = ...,
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
    "DownloadEval",
    "DownloadEvalResponse",
    "DownloadEvalObject",
]