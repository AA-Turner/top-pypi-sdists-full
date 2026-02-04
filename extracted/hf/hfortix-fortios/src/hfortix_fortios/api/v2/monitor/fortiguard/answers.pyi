""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: fortiguard/answers
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

class AnswersPayload(TypedDict, total=False):
    """Payload type for Answers operations."""
    page: int
    pagesize: int
    sortkey: str
    topics: str
    limit: int


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class AnswersResponse(TypedDict, total=False):
    """Response type for Answers - use with .dict property for typed dict access."""
    name: str
    sort: str
    page: int
    pageSize: int
    pageCount: int
    listCount: int
    totalCount: int
    sorts: list[str]
    list: list[str]


class AnswersObject(FortiObject[AnswersResponse]):
    """Typed FortiObject for Answers with field access."""
    name: str
    sort: str
    page: int
    pageSize: int
    pageCount: int
    listCount: int
    totalCount: int
    sorts: list[str]
    list: list[str]



# ================================================================
# Main Endpoint Class
# ================================================================

class Answers:
    """
    
    Endpoint: fortiguard/answers
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
        page: int | None = ...,
        pagesize: int | None = ...,
        sortkey: str | None = ...,
        topics: str | None = ...,
        limit: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[AnswersObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AnswersPayload | None = ...,
        page: int | None = ...,
        pagesize: int | None = ...,
        sortkey: str | None = ...,
        topics: str | None = ...,
        limit: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AnswersObject: ...




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
        payload_dict: AnswersPayload | None = ...,
        page: int | None = ...,
        pagesize: int | None = ...,
        sortkey: str | None = ...,
        topics: str | None = ...,
        limit: int | None = ...,
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
    "Answers",
    "AnswersResponse",
    "AnswersObject",
]