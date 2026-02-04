""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/modem
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

class ModemPayload(TypedDict, total=False):
    """Payload type for Modem operations."""
    status: Literal["enable", "disable"]
    pin_init: str
    network_init: str
    lockdown_lac: str
    mode: Literal["standalone", "redundant"]
    auto_dial: Literal["enable", "disable"]
    dial_on_demand: Literal["enable", "disable"]
    idle_timer: int
    redial: Literal["none", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    reset: int
    holddown_timer: int
    connect_timeout: int
    interface: str
    wireless_port: int
    dont_send_CR1: Literal["enable", "disable"]
    phone1: str
    dial_cmd1: str
    username1: str
    passwd1: str
    extra_init1: str
    peer_modem1: Literal["generic", "actiontec", "ascend_TNT"]
    ppp_echo_request1: Literal["enable", "disable"]
    authtype1: Literal["pap", "chap", "mschap", "mschapv2"]
    dont_send_CR2: Literal["enable", "disable"]
    phone2: str
    dial_cmd2: str
    username2: str
    passwd2: str
    extra_init2: str
    peer_modem2: Literal["generic", "actiontec", "ascend_TNT"]
    ppp_echo_request2: Literal["enable", "disable"]
    authtype2: Literal["pap", "chap", "mschap", "mschapv2"]
    dont_send_CR3: Literal["enable", "disable"]
    phone3: str
    dial_cmd3: str
    username3: str
    passwd3: str
    extra_init3: str
    peer_modem3: Literal["generic", "actiontec", "ascend_TNT"]
    ppp_echo_request3: Literal["enable", "disable"]
    altmode: Literal["enable", "disable"]
    authtype3: Literal["pap", "chap", "mschap", "mschapv2"]
    traffic_check: Literal["enable", "disable"]
    action: Literal["dial", "stop", "none"]
    distance: int
    priority: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ModemResponse(TypedDict, total=False):
    """Response type for Modem - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    pin_init: str
    network_init: str
    lockdown_lac: str
    mode: Literal["standalone", "redundant"]
    auto_dial: Literal["enable", "disable"]
    dial_on_demand: Literal["enable", "disable"]
    idle_timer: int
    redial: Literal["none", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    reset: int
    holddown_timer: int
    connect_timeout: int
    interface: str
    wireless_port: int
    dont_send_CR1: Literal["enable", "disable"]
    phone1: str
    dial_cmd1: str
    username1: str
    passwd1: str
    extra_init1: str
    peer_modem1: Literal["generic", "actiontec", "ascend_TNT"]
    ppp_echo_request1: Literal["enable", "disable"]
    authtype1: Literal["pap", "chap", "mschap", "mschapv2"]
    dont_send_CR2: Literal["enable", "disable"]
    phone2: str
    dial_cmd2: str
    username2: str
    passwd2: str
    extra_init2: str
    peer_modem2: Literal["generic", "actiontec", "ascend_TNT"]
    ppp_echo_request2: Literal["enable", "disable"]
    authtype2: Literal["pap", "chap", "mschap", "mschapv2"]
    dont_send_CR3: Literal["enable", "disable"]
    phone3: str
    dial_cmd3: str
    username3: str
    passwd3: str
    extra_init3: str
    peer_modem3: Literal["generic", "actiontec", "ascend_TNT"]
    ppp_echo_request3: Literal["enable", "disable"]
    altmode: Literal["enable", "disable"]
    authtype3: Literal["pap", "chap", "mschap", "mschapv2"]
    traffic_check: Literal["enable", "disable"]
    action: Literal["dial", "stop", "none"]
    distance: int
    priority: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ModemObject(FortiObject):
    """Typed FortiObject for Modem with field access."""
    status: Literal["enable", "disable"]
    pin_init: str
    network_init: str
    lockdown_lac: str
    mode: Literal["standalone", "redundant"]
    auto_dial: Literal["enable", "disable"]
    dial_on_demand: Literal["enable", "disable"]
    idle_timer: int
    redial: Literal["none", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    reset: int
    holddown_timer: int
    connect_timeout: int
    interface: str
    wireless_port: int
    dont_send_CR1: Literal["enable", "disable"]
    phone1: str
    dial_cmd1: str
    username1: str
    passwd1: str
    extra_init1: str
    peer_modem1: Literal["generic", "actiontec", "ascend_TNT"]
    ppp_echo_request1: Literal["enable", "disable"]
    authtype1: Literal["pap", "chap", "mschap", "mschapv2"]
    dont_send_CR2: Literal["enable", "disable"]
    phone2: str
    dial_cmd2: str
    username2: str
    passwd2: str
    extra_init2: str
    peer_modem2: Literal["generic", "actiontec", "ascend_TNT"]
    ppp_echo_request2: Literal["enable", "disable"]
    authtype2: Literal["pap", "chap", "mschap", "mschapv2"]
    dont_send_CR3: Literal["enable", "disable"]
    phone3: str
    dial_cmd3: str
    username3: str
    passwd3: str
    extra_init3: str
    peer_modem3: Literal["generic", "actiontec", "ascend_TNT"]
    ppp_echo_request3: Literal["enable", "disable"]
    altmode: Literal["enable", "disable"]
    authtype3: Literal["pap", "chap", "mschap", "mschapv2"]
    traffic_check: Literal["enable", "disable"]
    action: Literal["dial", "stop", "none"]
    distance: int
    priority: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Modem:
    """
    
    Endpoint: system/modem
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
    ) -> ModemObject: ...
    
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
        payload_dict: ModemPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        pin_init: str | None = ...,
        network_init: str | None = ...,
        lockdown_lac: str | None = ...,
        mode: Literal["standalone", "redundant"] | None = ...,
        auto_dial: Literal["enable", "disable"] | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        idle_timer: int | None = ...,
        redial: Literal["none", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] | None = ...,
        reset: int | None = ...,
        holddown_timer: int | None = ...,
        connect_timeout: int | None = ...,
        interface: str | None = ...,
        wireless_port: int | None = ...,
        dont_send_CR1: Literal["enable", "disable"] | None = ...,
        phone1: str | None = ...,
        dial_cmd1: str | None = ...,
        username1: str | None = ...,
        passwd1: str | None = ...,
        extra_init1: str | None = ...,
        peer_modem1: Literal["generic", "actiontec", "ascend_TNT"] | None = ...,
        ppp_echo_request1: Literal["enable", "disable"] | None = ...,
        authtype1: Literal["pap", "chap", "mschap", "mschapv2"] | None = ...,
        dont_send_CR2: Literal["enable", "disable"] | None = ...,
        phone2: str | None = ...,
        dial_cmd2: str | None = ...,
        username2: str | None = ...,
        passwd2: str | None = ...,
        extra_init2: str | None = ...,
        peer_modem2: Literal["generic", "actiontec", "ascend_TNT"] | None = ...,
        ppp_echo_request2: Literal["enable", "disable"] | None = ...,
        authtype2: Literal["pap", "chap", "mschap", "mschapv2"] | None = ...,
        dont_send_CR3: Literal["enable", "disable"] | None = ...,
        phone3: str | None = ...,
        dial_cmd3: str | None = ...,
        username3: str | None = ...,
        passwd3: str | None = ...,
        extra_init3: str | None = ...,
        peer_modem3: Literal["generic", "actiontec", "ascend_TNT"] | None = ...,
        ppp_echo_request3: Literal["enable", "disable"] | None = ...,
        altmode: Literal["enable", "disable"] | None = ...,
        authtype3: Literal["pap", "chap", "mschap", "mschapv2"] | None = ...,
        traffic_check: Literal["enable", "disable"] | None = ...,
        action: Literal["dial", "stop", "none"] | None = ...,
        distance: int | None = ...,
        priority: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ModemObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
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
        payload_dict: ModemPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        pin_init: str | None = ...,
        network_init: str | None = ...,
        lockdown_lac: str | None = ...,
        mode: Literal["standalone", "redundant"] | None = ...,
        auto_dial: Literal["enable", "disable"] | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        idle_timer: int | None = ...,
        redial: Literal["none", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] | None = ...,
        reset: int | None = ...,
        holddown_timer: int | None = ...,
        connect_timeout: int | None = ...,
        interface: str | None = ...,
        wireless_port: int | None = ...,
        dont_send_CR1: Literal["enable", "disable"] | None = ...,
        phone1: str | None = ...,
        dial_cmd1: str | None = ...,
        username1: str | None = ...,
        passwd1: str | None = ...,
        extra_init1: str | None = ...,
        peer_modem1: Literal["generic", "actiontec", "ascend_TNT"] | None = ...,
        ppp_echo_request1: Literal["enable", "disable"] | None = ...,
        authtype1: Literal["pap", "chap", "mschap", "mschapv2"] | None = ...,
        dont_send_CR2: Literal["enable", "disable"] | None = ...,
        phone2: str | None = ...,
        dial_cmd2: str | None = ...,
        username2: str | None = ...,
        passwd2: str | None = ...,
        extra_init2: str | None = ...,
        peer_modem2: Literal["generic", "actiontec", "ascend_TNT"] | None = ...,
        ppp_echo_request2: Literal["enable", "disable"] | None = ...,
        authtype2: Literal["pap", "chap", "mschap", "mschapv2"] | None = ...,
        dont_send_CR3: Literal["enable", "disable"] | None = ...,
        phone3: str | None = ...,
        dial_cmd3: str | None = ...,
        username3: str | None = ...,
        passwd3: str | None = ...,
        extra_init3: str | None = ...,
        peer_modem3: Literal["generic", "actiontec", "ascend_TNT"] | None = ...,
        ppp_echo_request3: Literal["enable", "disable"] | None = ...,
        altmode: Literal["enable", "disable"] | None = ...,
        authtype3: Literal["pap", "chap", "mschap", "mschapv2"] | None = ...,
        traffic_check: Literal["enable", "disable"] | None = ...,
        action: Literal["dial", "stop", "none"] | None = ...,
        distance: int | None = ...,
        priority: int | None = ...,
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
    "Modem",
    "ModemPayload",
    "ModemResponse",
    "ModemObject",
]