""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: application/list
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

class ListEntriesRiskItem(TypedDict, total=False):
    """Nested item for entries.risk field."""
    level: int


class ListEntriesCategoryItem(TypedDict, total=False):
    """Nested item for entries.category field."""
    id: int


class ListEntriesApplicationItem(TypedDict, total=False):
    """Nested item for entries.application field."""
    id: int


class ListEntriesExclusionItem(TypedDict, total=False):
    """Nested item for entries.exclusion field."""
    id: int


class ListEntriesParametersItem(TypedDict, total=False):
    """Nested item for entries.parameters field."""
    id: int
    members: str | list[str]


class ListEntriesItem(TypedDict, total=False):
    """Nested item for entries field."""
    id: int
    risk: str | list[str] | list[ListEntriesRiskItem]
    category: str | list[str] | list[ListEntriesCategoryItem]
    application: str | list[str] | list[ListEntriesApplicationItem]
    protocols: str | list[str]
    vendor: str | list[str]
    technology: str | list[str]
    behavior: str | list[str]
    popularity: Literal["1", "2", "3", "4", "5"]
    exclusion: str | list[str] | list[ListEntriesExclusionItem]
    parameters: str | list[str] | list[ListEntriesParametersItem]
    action: Literal["pass", "block", "reset"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    rate_count: int
    rate_duration: int
    rate_mode: Literal["periodical", "continuous"]
    rate_track: Literal["none", "src-ip", "dest-ip", "dhcp-client-mac", "dns-domain"]
    session_ttl: int
    shaper: str
    shaper_reverse: str
    per_ip_shaper: str
    quarantine: Literal["none", "attacker"]
    quarantine_expiry: str
    quarantine_log: Literal["disable", "enable"]


class ListDefaultnetworkservicesItem(TypedDict, total=False):
    """Nested item for default-network-services field."""
    id: int
    port: int
    services: Literal["http", "ssh", "telnet", "ftp", "dns", "smtp", "pop3", "imap", "snmp", "nntp", "https"]
    violation_action: Literal["pass", "monitor", "block"]


class ListPayload(TypedDict, total=False):
    """Payload type for List operations."""
    name: str
    comment: str
    replacemsg_group: str
    extended_log: Literal["enable", "disable"]
    other_application_action: Literal["pass", "block"]
    app_replacemsg: Literal["disable", "enable"]
    other_application_log: Literal["disable", "enable"]
    enforce_default_app_port: Literal["disable", "enable"]
    force_inclusion_ssl_di_sigs: Literal["disable", "enable"]
    unknown_application_action: Literal["pass", "block"]
    unknown_application_log: Literal["disable", "enable"]
    p2p_block_list: str | list[str]
    deep_app_inspection: Literal["disable", "enable"]
    options: str | list[str]
    entries: str | list[str] | list[ListEntriesItem]
    control_default_network_services: Literal["disable", "enable"]
    default_network_services: str | list[str] | list[ListDefaultnetworkservicesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ListResponse(TypedDict, total=False):
    """Response type for List - use with .dict property for typed dict access."""
    name: str
    comment: str
    replacemsg_group: str
    extended_log: Literal["enable", "disable"]
    other_application_action: Literal["pass", "block"]
    app_replacemsg: Literal["disable", "enable"]
    other_application_log: Literal["disable", "enable"]
    enforce_default_app_port: Literal["disable", "enable"]
    force_inclusion_ssl_di_sigs: Literal["disable", "enable"]
    unknown_application_action: Literal["pass", "block"]
    unknown_application_log: Literal["disable", "enable"]
    p2p_block_list: str
    deep_app_inspection: Literal["disable", "enable"]
    options: str
    entries: list[ListEntriesItem]
    control_default_network_services: Literal["disable", "enable"]
    default_network_services: list[ListDefaultnetworkservicesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ListEntriesRiskItemObject(FortiObject[ListEntriesRiskItem]):
    """Typed object for entries.risk table items with attribute access."""
    level: int


class ListEntriesCategoryItemObject(FortiObject[ListEntriesCategoryItem]):
    """Typed object for entries.category table items with attribute access."""
    id: int


class ListEntriesApplicationItemObject(FortiObject[ListEntriesApplicationItem]):
    """Typed object for entries.application table items with attribute access."""
    id: int


class ListEntriesExclusionItemObject(FortiObject[ListEntriesExclusionItem]):
    """Typed object for entries.exclusion table items with attribute access."""
    id: int


class ListEntriesParametersItemObject(FortiObject[ListEntriesParametersItem]):
    """Typed object for entries.parameters table items with attribute access."""
    id: int
    members: str | list[str]


class ListEntriesItemObject(FortiObject[ListEntriesItem]):
    """Typed object for entries table items with attribute access."""
    id: int
    risk: FortiObjectList[ListEntriesRiskItemObject]
    category: FortiObjectList[ListEntriesCategoryItemObject]
    application: FortiObjectList[ListEntriesApplicationItemObject]
    protocols: str | list[str]
    vendor: str | list[str]
    technology: str | list[str]
    behavior: str | list[str]
    popularity: Literal["1", "2", "3", "4", "5"]
    exclusion: FortiObjectList[ListEntriesExclusionItemObject]
    parameters: FortiObjectList[ListEntriesParametersItemObject]
    action: Literal["pass", "block", "reset"]
    log: Literal["disable", "enable"]
    log_packet: Literal["disable", "enable"]
    rate_count: int
    rate_duration: int
    rate_mode: Literal["periodical", "continuous"]
    rate_track: Literal["none", "src-ip", "dest-ip", "dhcp-client-mac", "dns-domain"]
    session_ttl: int
    shaper: str
    shaper_reverse: str
    per_ip_shaper: str
    quarantine: Literal["none", "attacker"]
    quarantine_expiry: str
    quarantine_log: Literal["disable", "enable"]


class ListDefaultnetworkservicesItemObject(FortiObject[ListDefaultnetworkservicesItem]):
    """Typed object for default-network-services table items with attribute access."""
    id: int
    port: int
    services: Literal["http", "ssh", "telnet", "ftp", "dns", "smtp", "pop3", "imap", "snmp", "nntp", "https"]
    violation_action: Literal["pass", "monitor", "block"]


class ListObject(FortiObject):
    """Typed FortiObject for List with field access."""
    name: str
    comment: str
    replacemsg_group: str
    extended_log: Literal["enable", "disable"]
    other_application_action: Literal["pass", "block"]
    app_replacemsg: Literal["disable", "enable"]
    other_application_log: Literal["disable", "enable"]
    enforce_default_app_port: Literal["disable", "enable"]
    force_inclusion_ssl_di_sigs: Literal["disable", "enable"]
    unknown_application_action: Literal["pass", "block"]
    unknown_application_log: Literal["disable", "enable"]
    p2p_block_list: str
    deep_app_inspection: Literal["disable", "enable"]
    options: str
    entries: FortiObjectList[ListEntriesItemObject]
    control_default_network_services: Literal["disable", "enable"]
    default_network_services: FortiObjectList[ListDefaultnetworkservicesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class List:
    """
    
    Endpoint: application/list
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
    ) -> ListObject: ...
    
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
    ) -> FortiObjectList[ListObject]: ...
    
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
        payload_dict: ListPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        other_application_action: Literal["pass", "block"] | None = ...,
        app_replacemsg: Literal["disable", "enable"] | None = ...,
        other_application_log: Literal["disable", "enable"] | None = ...,
        enforce_default_app_port: Literal["disable", "enable"] | None = ...,
        force_inclusion_ssl_di_sigs: Literal["disable", "enable"] | None = ...,
        unknown_application_action: Literal["pass", "block"] | None = ...,
        unknown_application_log: Literal["disable", "enable"] | None = ...,
        p2p_block_list: str | list[str] | None = ...,
        deep_app_inspection: Literal["disable", "enable"] | None = ...,
        options: str | list[str] | None = ...,
        entries: str | list[str] | list[ListEntriesItem] | None = ...,
        control_default_network_services: Literal["disable", "enable"] | None = ...,
        default_network_services: str | list[str] | list[ListDefaultnetworkservicesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ListObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ListPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        other_application_action: Literal["pass", "block"] | None = ...,
        app_replacemsg: Literal["disable", "enable"] | None = ...,
        other_application_log: Literal["disable", "enable"] | None = ...,
        enforce_default_app_port: Literal["disable", "enable"] | None = ...,
        force_inclusion_ssl_di_sigs: Literal["disable", "enable"] | None = ...,
        unknown_application_action: Literal["pass", "block"] | None = ...,
        unknown_application_log: Literal["disable", "enable"] | None = ...,
        p2p_block_list: str | list[str] | None = ...,
        deep_app_inspection: Literal["disable", "enable"] | None = ...,
        options: str | list[str] | None = ...,
        entries: str | list[str] | list[ListEntriesItem] | None = ...,
        control_default_network_services: Literal["disable", "enable"] | None = ...,
        default_network_services: str | list[str] | list[ListDefaultnetworkservicesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ListObject: ...

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
        payload_dict: ListPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        other_application_action: Literal["pass", "block"] | None = ...,
        app_replacemsg: Literal["disable", "enable"] | None = ...,
        other_application_log: Literal["disable", "enable"] | None = ...,
        enforce_default_app_port: Literal["disable", "enable"] | None = ...,
        force_inclusion_ssl_di_sigs: Literal["disable", "enable"] | None = ...,
        unknown_application_action: Literal["pass", "block"] | None = ...,
        unknown_application_log: Literal["disable", "enable"] | None = ...,
        p2p_block_list: Literal["skype", "edonkey", "bittorrent"] | list[str] | None = ...,
        deep_app_inspection: Literal["disable", "enable"] | None = ...,
        options: Literal["allow-dns", "allow-icmp", "allow-http", "allow-ssl"] | list[str] | None = ...,
        entries: str | list[str] | list[ListEntriesItem] | None = ...,
        control_default_network_services: Literal["disable", "enable"] | None = ...,
        default_network_services: str | list[str] | list[ListDefaultnetworkservicesItem] | None = ...,
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
    "List",
    "ListPayload",
    "ListResponse",
    "ListObject",
]