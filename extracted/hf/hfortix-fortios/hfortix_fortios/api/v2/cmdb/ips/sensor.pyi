""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ips/sensor
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

class SensorEntriesRuleItem(TypedDict, total=False):
    """Nested item for entries.rule field."""
    id: int


class SensorEntriesCveItem(TypedDict, total=False):
    """Nested item for entries.cve field."""
    cve_entry: str


class SensorEntriesVulntypeItem(TypedDict, total=False):
    """Nested item for entries.vuln-type field."""
    id: int


class SensorEntriesExemptipItem(TypedDict, total=False):
    """Nested item for entries.exempt-ip field."""
    id: int
    src_ip: str
    dst_ip: str


class SensorEntriesItem(TypedDict, total=False):
    """Nested item for entries field."""
    id: int
    rule: str | list[str] | list[SensorEntriesRuleItem]
    location: str | list[str]
    severity: str | list[str]
    protocol: str | list[str]
    os: str | list[str]
    application: str | list[str]
    default_action: Literal["all", "pass", "block"]
    default_status: Literal["all", "enable", "disable"]
    cve: str | list[str] | list[SensorEntriesCveItem]
    vuln_type: str | list[str] | list[SensorEntriesVulntypeItem]
    last_modified: str
    status: Literal["disable", "enable", "default"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    log_attack_context: Literal["disable", "enable"]
    action: Literal["pass", "block", "reset", "default"]
    rate_count: int
    rate_duration: int
    rate_mode: Literal["periodical", "continuous"]
    rate_track: Literal["none", "src-ip", "dest-ip", "dhcp-client-mac", "dns-domain"]
    exempt_ip: str | list[str] | list[SensorEntriesExemptipItem]
    quarantine: Literal["none", "attacker"]
    quarantine_expiry: str
    quarantine_log: Literal["disable", "enable"]


class SensorPayload(TypedDict, total=False):
    """Payload type for Sensor operations."""
    name: str
    comment: str
    replacemsg_group: str
    block_malicious_url: Literal["disable", "enable"]
    scan_botnet_connections: Literal["disable", "block", "monitor"]
    extended_log: Literal["enable", "disable"]
    entries: str | list[str] | list[SensorEntriesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SensorResponse(TypedDict, total=False):
    """Response type for Sensor - use with .dict property for typed dict access."""
    name: str
    comment: str
    replacemsg_group: str
    block_malicious_url: Literal["disable", "enable"]
    scan_botnet_connections: Literal["disable", "block", "monitor"]
    extended_log: Literal["enable", "disable"]
    entries: list[SensorEntriesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SensorEntriesRuleItemObject(FortiObject[SensorEntriesRuleItem]):
    """Typed object for entries.rule table items with attribute access."""
    id: int


class SensorEntriesCveItemObject(FortiObject[SensorEntriesCveItem]):
    """Typed object for entries.cve table items with attribute access."""
    cve_entry: str


class SensorEntriesVulntypeItemObject(FortiObject[SensorEntriesVulntypeItem]):
    """Typed object for entries.vuln-type table items with attribute access."""
    id: int


class SensorEntriesExemptipItemObject(FortiObject[SensorEntriesExemptipItem]):
    """Typed object for entries.exempt-ip table items with attribute access."""
    id: int
    src_ip: str
    dst_ip: str


class SensorEntriesItemObject(FortiObject[SensorEntriesItem]):
    """Typed object for entries table items with attribute access."""
    id: int
    rule: FortiObjectList[SensorEntriesRuleItemObject]
    location: str | list[str]
    severity: str | list[str]
    protocol: str | list[str]
    os: str | list[str]
    application: str | list[str]
    default_action: Literal["all", "pass", "block"]
    default_status: Literal["all", "enable", "disable"]
    cve: FortiObjectList[SensorEntriesCveItemObject]
    vuln_type: FortiObjectList[SensorEntriesVulntypeItemObject]
    last_modified: str
    status: Literal["disable", "enable", "default"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    log_attack_context: Literal["disable", "enable"]
    action: Literal["pass", "block", "reset", "default"]
    rate_count: int
    rate_duration: int
    rate_mode: Literal["periodical", "continuous"]
    rate_track: Literal["none", "src-ip", "dest-ip", "dhcp-client-mac", "dns-domain"]
    exempt_ip: FortiObjectList[SensorEntriesExemptipItemObject]
    quarantine: Literal["none", "attacker"]
    quarantine_expiry: str
    quarantine_log: Literal["disable", "enable"]


class SensorObject(FortiObject):
    """Typed FortiObject for Sensor with field access."""
    name: str
    comment: str
    replacemsg_group: str
    block_malicious_url: Literal["disable", "enable"]
    scan_botnet_connections: Literal["disable", "block", "monitor"]
    extended_log: Literal["enable", "disable"]
    entries: FortiObjectList[SensorEntriesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Sensor:
    """
    
    Endpoint: ips/sensor
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
    ) -> SensorObject: ...
    
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
    ) -> FortiObjectList[SensorObject]: ...
    
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
        payload_dict: SensorPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        block_malicious_url: Literal["disable", "enable"] | None = ...,
        scan_botnet_connections: Literal["disable", "block", "monitor"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        entries: str | list[str] | list[SensorEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SensorObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SensorPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        block_malicious_url: Literal["disable", "enable"] | None = ...,
        scan_botnet_connections: Literal["disable", "block", "monitor"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        entries: str | list[str] | list[SensorEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SensorObject: ...

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
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SensorPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        block_malicious_url: Literal["disable", "enable"] | None = ...,
        scan_botnet_connections: Literal["disable", "block", "monitor"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        entries: str | list[str] | list[SensorEntriesItem] | None = ...,
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
    "Sensor",
    "SensorPayload",
    "SensorResponse",
    "SensorObject",
]