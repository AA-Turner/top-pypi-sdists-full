""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/speed_test_schedule
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

class SpeedTestScheduleSchedulesItem(TypedDict, total=False):
    """Nested item for schedules field."""
    name: str


class SpeedTestSchedulePayload(TypedDict, total=False):
    """Payload type for SpeedTestSchedule operations."""
    interface: str
    status: Literal["disable", "enable"]
    diffserv: str
    server_name: str
    mode: Literal["UDP", "TCP", "Auto"]
    schedules: str | list[str] | list[SpeedTestScheduleSchedulesItem]
    dynamic_server: Literal["disable", "enable"]
    ctrl_port: int
    server_port: int
    update_shaper: Literal["disable", "local", "remote", "both"]
    update_inbandwidth: Literal["disable", "enable"]
    update_outbandwidth: Literal["disable", "enable"]
    update_interface_shaping: Literal["disable", "enable"]
    update_inbandwidth_maximum: int
    update_inbandwidth_minimum: int
    update_outbandwidth_maximum: int
    update_outbandwidth_minimum: int
    expected_inbandwidth_minimum: int
    expected_inbandwidth_maximum: int
    expected_outbandwidth_minimum: int
    expected_outbandwidth_maximum: int
    retries: int
    retry_pause: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SpeedTestScheduleResponse(TypedDict, total=False):
    """Response type for SpeedTestSchedule - use with .dict property for typed dict access."""
    interface: str
    status: Literal["disable", "enable"]
    diffserv: str
    server_name: str
    mode: Literal["UDP", "TCP", "Auto"]
    schedules: list[SpeedTestScheduleSchedulesItem]
    dynamic_server: Literal["disable", "enable"]
    ctrl_port: int
    server_port: int
    update_shaper: Literal["disable", "local", "remote", "both"]
    update_inbandwidth: Literal["disable", "enable"]
    update_outbandwidth: Literal["disable", "enable"]
    update_interface_shaping: Literal["disable", "enable"]
    update_inbandwidth_maximum: int
    update_inbandwidth_minimum: int
    update_outbandwidth_maximum: int
    update_outbandwidth_minimum: int
    expected_inbandwidth_minimum: int
    expected_inbandwidth_maximum: int
    expected_outbandwidth_minimum: int
    expected_outbandwidth_maximum: int
    retries: int
    retry_pause: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SpeedTestScheduleSchedulesItemObject(FortiObject[SpeedTestScheduleSchedulesItem]):
    """Typed object for schedules table items with attribute access."""
    name: str


class SpeedTestScheduleObject(FortiObject):
    """Typed FortiObject for SpeedTestSchedule with field access."""
    interface: str
    status: Literal["disable", "enable"]
    diffserv: str
    server_name: str
    mode: Literal["UDP", "TCP", "Auto"]
    schedules: FortiObjectList[SpeedTestScheduleSchedulesItemObject]
    dynamic_server: Literal["disable", "enable"]
    ctrl_port: int
    server_port: int
    update_shaper: Literal["disable", "local", "remote", "both"]
    update_inbandwidth: Literal["disable", "enable"]
    update_outbandwidth: Literal["disable", "enable"]
    update_interface_shaping: Literal["disable", "enable"]
    update_inbandwidth_maximum: int
    update_inbandwidth_minimum: int
    update_outbandwidth_maximum: int
    update_outbandwidth_minimum: int
    expected_inbandwidth_minimum: int
    expected_inbandwidth_maximum: int
    expected_outbandwidth_minimum: int
    expected_outbandwidth_maximum: int
    retries: int
    retry_pause: int


# ================================================================
# Main Endpoint Class
# ================================================================

class SpeedTestSchedule:
    """
    
    Endpoint: system/speed_test_schedule
    Category: cmdb
    MKey: interface
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
        interface: str,
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
    ) -> SpeedTestScheduleObject: ...
    
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
    ) -> FortiObjectList[SpeedTestScheduleObject]: ...
    
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
        payload_dict: SpeedTestSchedulePayload | None = ...,
        interface: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        diffserv: str | None = ...,
        server_name: str | None = ...,
        mode: Literal["UDP", "TCP", "Auto"] | None = ...,
        schedules: str | list[str] | list[SpeedTestScheduleSchedulesItem] | None = ...,
        dynamic_server: Literal["disable", "enable"] | None = ...,
        ctrl_port: int | None = ...,
        server_port: int | None = ...,
        update_shaper: Literal["disable", "local", "remote", "both"] | None = ...,
        update_inbandwidth: Literal["disable", "enable"] | None = ...,
        update_outbandwidth: Literal["disable", "enable"] | None = ...,
        update_interface_shaping: Literal["disable", "enable"] | None = ...,
        update_inbandwidth_maximum: int | None = ...,
        update_inbandwidth_minimum: int | None = ...,
        update_outbandwidth_maximum: int | None = ...,
        update_outbandwidth_minimum: int | None = ...,
        expected_inbandwidth_minimum: int | None = ...,
        expected_inbandwidth_maximum: int | None = ...,
        expected_outbandwidth_minimum: int | None = ...,
        expected_outbandwidth_maximum: int | None = ...,
        retries: int | None = ...,
        retry_pause: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SpeedTestScheduleObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SpeedTestSchedulePayload | None = ...,
        interface: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        diffserv: str | None = ...,
        server_name: str | None = ...,
        mode: Literal["UDP", "TCP", "Auto"] | None = ...,
        schedules: str | list[str] | list[SpeedTestScheduleSchedulesItem] | None = ...,
        dynamic_server: Literal["disable", "enable"] | None = ...,
        ctrl_port: int | None = ...,
        server_port: int | None = ...,
        update_shaper: Literal["disable", "local", "remote", "both"] | None = ...,
        update_inbandwidth: Literal["disable", "enable"] | None = ...,
        update_outbandwidth: Literal["disable", "enable"] | None = ...,
        update_interface_shaping: Literal["disable", "enable"] | None = ...,
        update_inbandwidth_maximum: int | None = ...,
        update_inbandwidth_minimum: int | None = ...,
        update_outbandwidth_maximum: int | None = ...,
        update_outbandwidth_minimum: int | None = ...,
        expected_inbandwidth_minimum: int | None = ...,
        expected_inbandwidth_maximum: int | None = ...,
        expected_outbandwidth_minimum: int | None = ...,
        expected_outbandwidth_maximum: int | None = ...,
        retries: int | None = ...,
        retry_pause: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SpeedTestScheduleObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        interface: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        interface: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_interface: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        interface: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SpeedTestSchedulePayload | None = ...,
        interface: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        diffserv: str | None = ...,
        server_name: str | None = ...,
        mode: Literal["UDP", "TCP", "Auto"] | None = ...,
        schedules: str | list[str] | list[SpeedTestScheduleSchedulesItem] | None = ...,
        dynamic_server: Literal["disable", "enable"] | None = ...,
        ctrl_port: int | None = ...,
        server_port: int | None = ...,
        update_shaper: Literal["disable", "local", "remote", "both"] | None = ...,
        update_inbandwidth: Literal["disable", "enable"] | None = ...,
        update_outbandwidth: Literal["disable", "enable"] | None = ...,
        update_interface_shaping: Literal["disable", "enable"] | None = ...,
        update_inbandwidth_maximum: int | None = ...,
        update_inbandwidth_minimum: int | None = ...,
        update_outbandwidth_maximum: int | None = ...,
        update_outbandwidth_minimum: int | None = ...,
        expected_inbandwidth_minimum: int | None = ...,
        expected_inbandwidth_maximum: int | None = ...,
        expected_outbandwidth_minimum: int | None = ...,
        expected_outbandwidth_maximum: int | None = ...,
        retries: int | None = ...,
        retry_pause: int | None = ...,
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
    "SpeedTestSchedule",
    "SpeedTestSchedulePayload",
    "SpeedTestScheduleResponse",
    "SpeedTestScheduleObject",
]