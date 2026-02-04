""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/h2qp_wan_metric
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

class H2qpWanMetricPayload(TypedDict, total=False):
    """Payload type for H2qpWanMetric operations."""
    name: str
    link_status: Literal["up", "down", "in-test"]
    symmetric_wan_link: Literal["symmetric", "asymmetric"]
    link_at_capacity: Literal["enable", "disable"]
    uplink_speed: int
    downlink_speed: int
    uplink_load: int
    downlink_load: int
    load_measurement_duration: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class H2qpWanMetricResponse(TypedDict, total=False):
    """Response type for H2qpWanMetric - use with .dict property for typed dict access."""
    name: str
    link_status: Literal["up", "down", "in-test"]
    symmetric_wan_link: Literal["symmetric", "asymmetric"]
    link_at_capacity: Literal["enable", "disable"]
    uplink_speed: int
    downlink_speed: int
    uplink_load: int
    downlink_load: int
    load_measurement_duration: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class H2qpWanMetricObject(FortiObject):
    """Typed FortiObject for H2qpWanMetric with field access."""
    name: str
    link_status: Literal["up", "down", "in-test"]
    symmetric_wan_link: Literal["symmetric", "asymmetric"]
    link_at_capacity: Literal["enable", "disable"]
    uplink_speed: int
    downlink_speed: int
    uplink_load: int
    downlink_load: int
    load_measurement_duration: int


# ================================================================
# Main Endpoint Class
# ================================================================

class H2qpWanMetric:
    """
    
    Endpoint: wireless_controller/hotspot20/h2qp_wan_metric
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
    ) -> H2qpWanMetricObject: ...
    
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
    ) -> FortiObjectList[H2qpWanMetricObject]: ...
    
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
        payload_dict: H2qpWanMetricPayload | None = ...,
        name: str | None = ...,
        link_status: Literal["up", "down", "in-test"] | None = ...,
        symmetric_wan_link: Literal["symmetric", "asymmetric"] | None = ...,
        link_at_capacity: Literal["enable", "disable"] | None = ...,
        uplink_speed: int | None = ...,
        downlink_speed: int | None = ...,
        uplink_load: int | None = ...,
        downlink_load: int | None = ...,
        load_measurement_duration: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpWanMetricObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: H2qpWanMetricPayload | None = ...,
        name: str | None = ...,
        link_status: Literal["up", "down", "in-test"] | None = ...,
        symmetric_wan_link: Literal["symmetric", "asymmetric"] | None = ...,
        link_at_capacity: Literal["enable", "disable"] | None = ...,
        uplink_speed: int | None = ...,
        downlink_speed: int | None = ...,
        uplink_load: int | None = ...,
        downlink_load: int | None = ...,
        load_measurement_duration: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpWanMetricObject: ...

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
        payload_dict: H2qpWanMetricPayload | None = ...,
        name: str | None = ...,
        link_status: Literal["up", "down", "in-test"] | None = ...,
        symmetric_wan_link: Literal["symmetric", "asymmetric"] | None = ...,
        link_at_capacity: Literal["enable", "disable"] | None = ...,
        uplink_speed: int | None = ...,
        downlink_speed: int | None = ...,
        uplink_load: int | None = ...,
        downlink_load: int | None = ...,
        load_measurement_duration: int | None = ...,
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
    "H2qpWanMetric",
    "H2qpWanMetricPayload",
    "H2qpWanMetricResponse",
    "H2qpWanMetricObject",
]