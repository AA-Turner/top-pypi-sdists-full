""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: log/threat_weight
Category: cmdb
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

class ThreatWeightLevelDict(TypedDict, total=False):
    """Nested object type for level field."""
    low: int
    medium: int
    high: int
    critical: int


class ThreatWeightMalwareDict(TypedDict, total=False):
    """Nested object type for malware field."""
    virus_infected: Literal["disable", "low", "medium", "high", "critical"]
    inline_block: Literal["disable", "low", "medium", "high", "critical"]
    file_blocked: Literal["disable", "low", "medium", "high", "critical"]
    command_blocked: Literal["disable", "low", "medium", "high", "critical"]
    oversized: Literal["disable", "low", "medium", "high", "critical"]
    virus_scan_error: Literal["disable", "low", "medium", "high", "critical"]
    switch_proto: Literal["disable", "low", "medium", "high", "critical"]
    mimefragmented: Literal["disable", "low", "medium", "high", "critical"]
    virus_file_type_executable: Literal["disable", "low", "medium", "high", "critical"]
    virus_outbreak_prevention: Literal["disable", "low", "medium", "high", "critical"]
    content_disarm: Literal["disable", "low", "medium", "high", "critical"]
    malware_list: Literal["disable", "low", "medium", "high", "critical"]
    ems_threat_feed: Literal["disable", "low", "medium", "high", "critical"]
    fsa_malicious: Literal["disable", "low", "medium", "high", "critical"]
    fsa_high_risk: Literal["disable", "low", "medium", "high", "critical"]
    fsa_medium_risk: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightIpsDict(TypedDict, total=False):
    """Nested object type for ips field."""
    info_severity: Literal["disable", "low", "medium", "high", "critical"]
    low_severity: Literal["disable", "low", "medium", "high", "critical"]
    medium_severity: Literal["disable", "low", "medium", "high", "critical"]
    high_severity: Literal["disable", "low", "medium", "high", "critical"]
    critical_severity: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightWebItem(TypedDict, total=False):
    """Nested item for web field."""
    id: int
    category: int
    level: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightGeolocationItem(TypedDict, total=False):
    """Nested item for geolocation field."""
    id: int
    country: str
    level: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightApplicationItem(TypedDict, total=False):
    """Nested item for application field."""
    id: int
    category: int
    level: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightPayload(TypedDict, total=False):
    """Payload type for ThreatWeight operations."""
    status: Literal["enable", "disable"]
    level: ThreatWeightLevelDict
    blocked_connection: Literal["disable", "low", "medium", "high", "critical"]
    failed_connection: Literal["disable", "low", "medium", "high", "critical"]
    url_block_detected: Literal["disable", "low", "medium", "high", "critical"]
    botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"]
    malware: ThreatWeightMalwareDict
    ips: ThreatWeightIpsDict
    web: str | list[str] | list[ThreatWeightWebItem]
    geolocation: str | list[str] | list[ThreatWeightGeolocationItem]
    application: str | list[str] | list[ThreatWeightApplicationItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ThreatWeightResponse(TypedDict, total=False):
    """Response type for ThreatWeight - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    level: ThreatWeightLevelDict
    blocked_connection: Literal["disable", "low", "medium", "high", "critical"]
    failed_connection: Literal["disable", "low", "medium", "high", "critical"]
    url_block_detected: Literal["disable", "low", "medium", "high", "critical"]
    botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"]
    malware: ThreatWeightMalwareDict
    ips: ThreatWeightIpsDict
    web: list[ThreatWeightWebItem]
    geolocation: list[ThreatWeightGeolocationItem]
    application: list[ThreatWeightApplicationItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ThreatWeightWebItemObject(FortiObject[ThreatWeightWebItem]):
    """Typed object for web table items with attribute access."""
    id: int
    category: int
    level: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightGeolocationItemObject(FortiObject[ThreatWeightGeolocationItem]):
    """Typed object for geolocation table items with attribute access."""
    id: int
    country: str
    level: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightApplicationItemObject(FortiObject[ThreatWeightApplicationItem]):
    """Typed object for application table items with attribute access."""
    id: int
    category: int
    level: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightLevelObject(FortiObject):
    """Nested object for level field with attribute access."""
    low: int
    medium: int
    high: int
    critical: int


class ThreatWeightMalwareObject(FortiObject):
    """Nested object for malware field with attribute access."""
    virus_infected: Literal["disable", "low", "medium", "high", "critical"]
    inline_block: Literal["disable", "low", "medium", "high", "critical"]
    file_blocked: Literal["disable", "low", "medium", "high", "critical"]
    command_blocked: Literal["disable", "low", "medium", "high", "critical"]
    oversized: Literal["disable", "low", "medium", "high", "critical"]
    virus_scan_error: Literal["disable", "low", "medium", "high", "critical"]
    switch_proto: Literal["disable", "low", "medium", "high", "critical"]
    mimefragmented: Literal["disable", "low", "medium", "high", "critical"]
    virus_file_type_executable: Literal["disable", "low", "medium", "high", "critical"]
    virus_outbreak_prevention: Literal["disable", "low", "medium", "high", "critical"]
    content_disarm: Literal["disable", "low", "medium", "high", "critical"]
    malware_list: Literal["disable", "low", "medium", "high", "critical"]
    ems_threat_feed: Literal["disable", "low", "medium", "high", "critical"]
    fsa_malicious: Literal["disable", "low", "medium", "high", "critical"]
    fsa_high_risk: Literal["disable", "low", "medium", "high", "critical"]
    fsa_medium_risk: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightIpsObject(FortiObject):
    """Nested object for ips field with attribute access."""
    info_severity: Literal["disable", "low", "medium", "high", "critical"]
    low_severity: Literal["disable", "low", "medium", "high", "critical"]
    medium_severity: Literal["disable", "low", "medium", "high", "critical"]
    high_severity: Literal["disable", "low", "medium", "high", "critical"]
    critical_severity: Literal["disable", "low", "medium", "high", "critical"]


class ThreatWeightObject(FortiObject):
    """Typed FortiObject for ThreatWeight with field access."""
    status: Literal["enable", "disable"]
    level: ThreatWeightLevelObject
    blocked_connection: Literal["disable", "low", "medium", "high", "critical"]
    failed_connection: Literal["disable", "low", "medium", "high", "critical"]
    url_block_detected: Literal["disable", "low", "medium", "high", "critical"]
    botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"]
    malware: ThreatWeightMalwareObject
    ips: ThreatWeightIpsObject
    web: FortiObjectList[ThreatWeightWebItemObject]
    geolocation: FortiObjectList[ThreatWeightGeolocationItemObject]
    application: FortiObjectList[ThreatWeightApplicationItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ThreatWeight:
    """
    
    Endpoint: log/threat_weight
    Category: cmdb
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
    
    # Singleton endpoint (no mkey)
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
    ) -> ThreatWeightObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: ThreatWeightLevelDict | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: ThreatWeightMalwareDict | None = ...,
        ips: ThreatWeightIpsDict | None = ...,
        web: str | list[str] | list[ThreatWeightWebItem] | None = ...,
        geolocation: str | list[str] | list[ThreatWeightGeolocationItem] | None = ...,
        application: str | list[str] | list[ThreatWeightApplicationItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ThreatWeightObject: ...


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
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: ThreatWeightLevelDict | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: ThreatWeightMalwareDict | None = ...,
        ips: ThreatWeightIpsDict | None = ...,
        web: str | list[str] | list[ThreatWeightWebItem] | None = ...,
        geolocation: str | list[str] | list[ThreatWeightGeolocationItem] | None = ...,
        application: str | list[str] | list[ThreatWeightApplicationItem] | None = ...,
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
    "ThreatWeight",
    "ThreatWeightPayload",
    "ThreatWeightResponse",
    "ThreatWeightObject",
]