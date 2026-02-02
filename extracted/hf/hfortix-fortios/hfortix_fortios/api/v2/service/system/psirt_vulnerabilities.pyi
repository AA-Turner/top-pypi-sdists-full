""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/psirt_vulnerabilities
Category: service
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

class PsirtVulnerabilitiesPayload(TypedDict, total=False):
    """Payload type for PsirtVulnerabilities operations."""
    severity: Literal["critical", "high", "low"]
    count: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class PsirtVulnerabilitiesResponse(TypedDict, total=False):
    """Response type for PsirtVulnerabilities - use with .dict property for typed dict access."""
    name: str
    irNumber: str
    serial: str
    upgradeToVersion: str
    severity: str


class PsirtVulnerabilitiesObject(FortiObject[PsirtVulnerabilitiesResponse]):
    """Typed FortiObject for PsirtVulnerabilities with field access."""
    name: str
    irNumber: str
    serial: str
    upgradeToVersion: str
    severity: str



# ================================================================
# Main Endpoint Class
# ================================================================

class PsirtVulnerabilities:
    """
    
    Endpoint: system/psirt_vulnerabilities
    Category: service
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
    ) -> FortiObjectList[PsirtVulnerabilitiesObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PsirtVulnerabilitiesPayload | None = ...,
        severity: Literal["critical", "high", "low"] | None = ...,
        count: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PsirtVulnerabilitiesObject: ...


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
        payload_dict: PsirtVulnerabilitiesPayload | None = ...,
        severity: Literal["critical", "high", "low"] | None = ...,
        count: str | None = ...,
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
    "PsirtVulnerabilities",
    "PsirtVulnerabilitiesResponse",
    "PsirtVulnerabilitiesObject",
]