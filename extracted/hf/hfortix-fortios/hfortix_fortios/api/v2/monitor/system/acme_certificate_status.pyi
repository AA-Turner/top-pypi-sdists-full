""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/acme_certificate_status
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

class AcmeCertificateStatusPayload(TypedDict, total=False):
    """Payload type for AcmeCertificateStatus operations."""
    mkey: str
    scope: Literal["vdom", "global"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class AcmeCertificateStatusResponse(TypedDict, total=False):
    """Response type for AcmeCertificateStatus - use with .dict property for typed dict access."""
    is_ssl_server_cert: bool
    acme_status: str


class AcmeCertificateStatusObject(FortiObject[AcmeCertificateStatusResponse]):
    """Typed FortiObject for AcmeCertificateStatus with field access."""
    is_ssl_server_cert: bool
    acme_status: str



# ================================================================
# Main Endpoint Class
# ================================================================

class AcmeCertificateStatus:
    """
    
    Endpoint: system/acme_certificate_status
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
        scope: Literal["vdom", "global"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[AcmeCertificateStatusObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AcmeCertificateStatusPayload | None = ...,
        mkey: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AcmeCertificateStatusObject: ...


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
        payload_dict: AcmeCertificateStatusPayload | None = ...,
        mkey: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
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
    "AcmeCertificateStatus",
    "AcmeCertificateStatusResponse",
    "AcmeCertificateStatusObject",
]