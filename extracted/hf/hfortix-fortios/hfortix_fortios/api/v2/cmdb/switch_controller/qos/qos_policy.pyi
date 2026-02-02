""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/qos/qos_policy
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

class QosPolicyPayload(TypedDict, total=False):
    """Payload type for QosPolicy operations."""
    name: str
    default_cos: int
    trust_dot1p_map: str
    trust_ip_dscp_map: str
    queue_policy: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class QosPolicyResponse(TypedDict, total=False):
    """Response type for QosPolicy - use with .dict property for typed dict access."""
    name: str
    default_cos: int
    trust_dot1p_map: str
    trust_ip_dscp_map: str
    queue_policy: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class QosPolicyObject(FortiObject):
    """Typed FortiObject for QosPolicy with field access."""
    name: str
    default_cos: int
    trust_dot1p_map: str
    trust_ip_dscp_map: str
    queue_policy: str


# ================================================================
# Main Endpoint Class
# ================================================================

class QosPolicy:
    """
    
    Endpoint: switch_controller/qos/qos_policy
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
    ) -> QosPolicyObject: ...
    
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
    ) -> FortiObjectList[QosPolicyObject]: ...
    
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
        payload_dict: QosPolicyPayload | None = ...,
        name: str | None = ...,
        default_cos: int | None = ...,
        trust_dot1p_map: str | None = ...,
        trust_ip_dscp_map: str | None = ...,
        queue_policy: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QosPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: QosPolicyPayload | None = ...,
        name: str | None = ...,
        default_cos: int | None = ...,
        trust_dot1p_map: str | None = ...,
        trust_ip_dscp_map: str | None = ...,
        queue_policy: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QosPolicyObject: ...

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
        payload_dict: QosPolicyPayload | None = ...,
        name: str | None = ...,
        default_cos: int | None = ...,
        trust_dot1p_map: str | None = ...,
        trust_ip_dscp_map: str | None = ...,
        queue_policy: str | None = ...,
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
    "QosPolicy",
    "QosPolicyPayload",
    "QosPolicyResponse",
    "QosPolicyObject",
]