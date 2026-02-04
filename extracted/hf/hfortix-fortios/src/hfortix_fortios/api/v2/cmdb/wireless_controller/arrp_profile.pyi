""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/arrp_profile
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

class ArrpProfileDarrpoptimizeschedulesItem(TypedDict, total=False):
    """Nested item for darrp-optimize-schedules field."""
    name: str


class ArrpProfilePayload(TypedDict, total=False):
    """Payload type for ArrpProfile operations."""
    name: str
    comment: str
    selection_period: int
    monitor_period: int
    weight_managed_ap: int
    weight_rogue_ap: int
    weight_noise_floor: int
    weight_channel_load: int
    weight_spectral_rssi: int
    weight_weather_channel: int
    weight_dfs_channel: int
    threshold_ap: int
    threshold_noise_floor: str
    threshold_channel_load: int
    threshold_spectral_rssi: str
    threshold_tx_retries: int
    threshold_rx_errors: int
    include_weather_channel: Literal["enable", "disable"]
    include_dfs_channel: Literal["enable", "disable"]
    override_darrp_optimize: Literal["enable", "disable"]
    darrp_optimize: int
    darrp_optimize_schedules: str | list[str] | list[ArrpProfileDarrpoptimizeschedulesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ArrpProfileResponse(TypedDict, total=False):
    """Response type for ArrpProfile - use with .dict property for typed dict access."""
    name: str
    comment: str
    selection_period: int
    monitor_period: int
    weight_managed_ap: int
    weight_rogue_ap: int
    weight_noise_floor: int
    weight_channel_load: int
    weight_spectral_rssi: int
    weight_weather_channel: int
    weight_dfs_channel: int
    threshold_ap: int
    threshold_noise_floor: str
    threshold_channel_load: int
    threshold_spectral_rssi: str
    threshold_tx_retries: int
    threshold_rx_errors: int
    include_weather_channel: Literal["enable", "disable"]
    include_dfs_channel: Literal["enable", "disable"]
    override_darrp_optimize: Literal["enable", "disable"]
    darrp_optimize: int
    darrp_optimize_schedules: list[ArrpProfileDarrpoptimizeschedulesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ArrpProfileDarrpoptimizeschedulesItemObject(FortiObject[ArrpProfileDarrpoptimizeschedulesItem]):
    """Typed object for darrp-optimize-schedules table items with attribute access."""
    name: str


class ArrpProfileObject(FortiObject):
    """Typed FortiObject for ArrpProfile with field access."""
    name: str
    comment: str
    selection_period: int
    monitor_period: int
    weight_managed_ap: int
    weight_rogue_ap: int
    weight_noise_floor: int
    weight_channel_load: int
    weight_spectral_rssi: int
    weight_weather_channel: int
    weight_dfs_channel: int
    threshold_ap: int
    threshold_noise_floor: str
    threshold_channel_load: int
    threshold_spectral_rssi: str
    threshold_tx_retries: int
    threshold_rx_errors: int
    include_weather_channel: Literal["enable", "disable"]
    include_dfs_channel: Literal["enable", "disable"]
    override_darrp_optimize: Literal["enable", "disable"]
    darrp_optimize: int
    darrp_optimize_schedules: FortiObjectList[ArrpProfileDarrpoptimizeschedulesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ArrpProfile:
    """
    
    Endpoint: wireless_controller/arrp_profile
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
    ) -> ArrpProfileObject: ...
    
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
    ) -> FortiObjectList[ArrpProfileObject]: ...
    
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
        payload_dict: ArrpProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        selection_period: int | None = ...,
        monitor_period: int | None = ...,
        weight_managed_ap: int | None = ...,
        weight_rogue_ap: int | None = ...,
        weight_noise_floor: int | None = ...,
        weight_channel_load: int | None = ...,
        weight_spectral_rssi: int | None = ...,
        weight_weather_channel: int | None = ...,
        weight_dfs_channel: int | None = ...,
        threshold_ap: int | None = ...,
        threshold_noise_floor: str | None = ...,
        threshold_channel_load: int | None = ...,
        threshold_spectral_rssi: str | None = ...,
        threshold_tx_retries: int | None = ...,
        threshold_rx_errors: int | None = ...,
        include_weather_channel: Literal["enable", "disable"] | None = ...,
        include_dfs_channel: Literal["enable", "disable"] | None = ...,
        override_darrp_optimize: Literal["enable", "disable"] | None = ...,
        darrp_optimize: int | None = ...,
        darrp_optimize_schedules: str | list[str] | list[ArrpProfileDarrpoptimizeschedulesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ArrpProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ArrpProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        selection_period: int | None = ...,
        monitor_period: int | None = ...,
        weight_managed_ap: int | None = ...,
        weight_rogue_ap: int | None = ...,
        weight_noise_floor: int | None = ...,
        weight_channel_load: int | None = ...,
        weight_spectral_rssi: int | None = ...,
        weight_weather_channel: int | None = ...,
        weight_dfs_channel: int | None = ...,
        threshold_ap: int | None = ...,
        threshold_noise_floor: str | None = ...,
        threshold_channel_load: int | None = ...,
        threshold_spectral_rssi: str | None = ...,
        threshold_tx_retries: int | None = ...,
        threshold_rx_errors: int | None = ...,
        include_weather_channel: Literal["enable", "disable"] | None = ...,
        include_dfs_channel: Literal["enable", "disable"] | None = ...,
        override_darrp_optimize: Literal["enable", "disable"] | None = ...,
        darrp_optimize: int | None = ...,
        darrp_optimize_schedules: str | list[str] | list[ArrpProfileDarrpoptimizeschedulesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ArrpProfileObject: ...

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
        payload_dict: ArrpProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        selection_period: int | None = ...,
        monitor_period: int | None = ...,
        weight_managed_ap: int | None = ...,
        weight_rogue_ap: int | None = ...,
        weight_noise_floor: int | None = ...,
        weight_channel_load: int | None = ...,
        weight_spectral_rssi: int | None = ...,
        weight_weather_channel: int | None = ...,
        weight_dfs_channel: int | None = ...,
        threshold_ap: int | None = ...,
        threshold_noise_floor: str | None = ...,
        threshold_channel_load: int | None = ...,
        threshold_spectral_rssi: str | None = ...,
        threshold_tx_retries: int | None = ...,
        threshold_rx_errors: int | None = ...,
        include_weather_channel: Literal["enable", "disable"] | None = ...,
        include_dfs_channel: Literal["enable", "disable"] | None = ...,
        override_darrp_optimize: Literal["enable", "disable"] | None = ...,
        darrp_optimize: int | None = ...,
        darrp_optimize_schedules: str | list[str] | list[ArrpProfileDarrpoptimizeschedulesItem] | None = ...,
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
    "ArrpProfile",
    "ArrpProfilePayload",
    "ArrpProfileResponse",
    "ArrpProfileObject",
]