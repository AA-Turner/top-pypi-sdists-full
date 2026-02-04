""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/shaper/multi_class_shaper
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
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class MultiClassShaperResponse(TypedDict, total=False):
    """Response type for MultiClassShaper - use with .dict property for typed dict access."""
    interface: str
    bandwidth: int
    default_class: int
    active_classes: list[str]
    parent: str
    remote_gateway: str
    network_id: int
    peer_id: str


class MultiClassShaperObject(FortiObject[MultiClassShaperResponse]):
    """Typed FortiObject for MultiClassShaper with field access."""
    interface: str
    bandwidth: int
    default_class: int
    active_classes: list[str]
    parent: str
    remote_gateway: str
    network_id: int
    peer_id: str



# ================================================================
# Main Endpoint Class
# ================================================================

class MultiClassShaper:
    """
    
    Endpoint: firewall/shaper/multi_class_shaper
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
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[MultiClassShaperObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: dict[str, Any] | None = ...,
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
        payload_dict: dict[str, Any] | None = ...,
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
    "MultiClassShaper",
    "MultiClassShaperResponse",
    "MultiClassShaperObject",
]