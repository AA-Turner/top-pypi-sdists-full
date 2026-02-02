""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/external_resource/entry_list
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

class EntryListPayload(TypedDict, total=False):
    """Payload type for EntryList operations."""
    mkey: str
    status_only: bool
    include_notes: bool
    counts_only: bool
    entry: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class EntryListResponse(TypedDict, total=False):
    """Response type for EntryList - use with .dict property for typed dict access."""
    status: str
    error: str
    error_code: int
    http_status_code: int
    conn_attempt_time: int
    resource_file_status: str
    last_content_update_time: int
    last_conn_success_time: int
    entries: list[str]
    invalid_count: int
    valid_count: int
    accepted_count: int
    accepted_limit: int
    overflow: bool
    matched_invalid: int
    matched_valid: int
    notes: list[str]


class EntryListObject(FortiObject[EntryListResponse]):
    """Typed FortiObject for EntryList with field access."""
    status: str
    error: str
    error_code: int
    http_status_code: int
    conn_attempt_time: int
    resource_file_status: str
    last_content_update_time: int
    last_conn_success_time: int
    entries: list[str]
    invalid_count: int
    valid_count: int
    accepted_count: int
    accepted_limit: int
    overflow: bool
    matched_invalid: int
    matched_valid: int
    notes: list[str]



# ================================================================
# Main Endpoint Class
# ================================================================

class EntryList:
    """
    
    Endpoint: system/external_resource/entry_list
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
        mkey: str,
        status_only: bool | None = ...,
        include_notes: bool | None = ...,
        counts_only: bool | None = ...,
        entry: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[EntryListObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: EntryListPayload | None = ...,
        mkey: str | None = ...,
        status_only: bool | None = ...,
        include_notes: bool | None = ...,
        counts_only: bool | None = ...,
        entry: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> EntryListObject: ...


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
        payload_dict: EntryListPayload | None = ...,
        mkey: str | None = ...,
        status_only: bool | None = ...,
        include_notes: bool | None = ...,
        counts_only: bool | None = ...,
        entry: str | None = ...,
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
    "EntryList",
    "EntryListResponse",
    "EntryListObject",
]