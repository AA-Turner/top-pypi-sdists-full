""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: fortiguard/service_communication_stats
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

class ServiceCommunicationStatsPayload(TypedDict, total=False):
    """Payload type for ServiceCommunicationStats operations."""
    service_type: Literal["forticare", "fortiguard_download", "fortiguard_query", "forticloud_log", "fortisandbox_cloud", "fortiguard.com", "sdns", "fortitoken_registration", "sms_service"]
    timeslot: Literal["1_hour", "24_hour", "1_week"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class ServiceCommunicationStatsResponse(TypedDict, total=False):
    """Response type for ServiceCommunicationStats - use with .dict property for typed dict access."""
    forticare: str
    fortiguard_download: str
    fortiguard_query: str
    forticloud_log: str
    fortisandbox_cloud: str
    fortiguard_com: str
    sdns: str
    fortitoken_registration: str
    sms_service: str


class ServiceCommunicationStatsObject(FortiObject[ServiceCommunicationStatsResponse]):
    """Typed FortiObject for ServiceCommunicationStats with field access."""
    forticare: str
    fortiguard_download: str
    fortiguard_query: str
    forticloud_log: str
    fortisandbox_cloud: str
    fortiguard_com: str
    sdns: str
    fortitoken_registration: str
    sms_service: str



# ================================================================
# Main Endpoint Class
# ================================================================

class ServiceCommunicationStats:
    """
    
    Endpoint: fortiguard/service_communication_stats
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
        service_type: Literal["forticare", "fortiguard_download", "fortiguard_query", "forticloud_log", "fortisandbox_cloud", "fortiguard.com", "sdns", "fortitoken_registration", "sms_service"] | None = ...,
        timeslot: Literal["1_hour", "24_hour", "1_week"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[ServiceCommunicationStatsObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ServiceCommunicationStatsPayload | None = ...,
        service_type: Literal["forticare", "fortiguard_download", "fortiguard_query", "forticloud_log", "fortisandbox_cloud", "fortiguard.com", "sdns", "fortitoken_registration", "sms_service"] | None = ...,
        timeslot: Literal["1_hour", "24_hour", "1_week"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ServiceCommunicationStatsObject: ...




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
        payload_dict: ServiceCommunicationStatsPayload | None = ...,
        service_type: Literal["forticare", "fortiguard_download", "fortiguard_query", "forticloud_log", "fortisandbox_cloud", "fortiguard.com", "sdns", "fortitoken_registration", "sms_service"] | None = ...,
        timeslot: Literal["1_hour", "24_hour", "1_week"] | None = ...,
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
    "ServiceCommunicationStats",
    "ServiceCommunicationStatsResponse",
    "ServiceCommunicationStatsObject",
]