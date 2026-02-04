""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/acl/ingress
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

class IngressActionDict(TypedDict, total=False):
    """Nested object type for action field."""
    drop: Literal["enable", "disable"]
    count: Literal["enable", "disable"]


class IngressClassifierDict(TypedDict, total=False):
    """Nested object type for classifier field."""
    dst_ip_prefix: str
    dst_mac: str
    src_ip_prefix: str
    src_mac: str
    vlan: int


class IngressPayload(TypedDict, total=False):
    """Payload type for Ingress operations."""
    id: int
    description: str
    action: IngressActionDict
    classifier: IngressClassifierDict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IngressResponse(TypedDict, total=False):
    """Response type for Ingress - use with .dict property for typed dict access."""
    id: int
    description: str
    action: IngressActionDict
    classifier: IngressClassifierDict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IngressActionObject(FortiObject):
    """Nested object for action field with attribute access."""
    drop: Literal["enable", "disable"]
    count: Literal["enable", "disable"]


class IngressClassifierObject(FortiObject):
    """Nested object for classifier field with attribute access."""
    dst_ip_prefix: str
    dst_mac: str
    src_ip_prefix: str
    src_mac: str
    vlan: int


class IngressObject(FortiObject):
    """Typed FortiObject for Ingress with field access."""
    id: int
    description: str
    action: IngressActionObject
    classifier: IngressClassifierObject


# ================================================================
# Main Endpoint Class
# ================================================================

class Ingress:
    """
    
    Endpoint: switch_controller/acl/ingress
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> IngressObject: ...
    
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
    ) -> FortiObjectList[IngressObject]: ...
    
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
        payload_dict: IngressPayload | None = ...,
        id: int | None = ...,
        description: str | None = ...,
        action: IngressActionDict | None = ...,
        classifier: IngressClassifierDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IngressObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: IngressPayload | None = ...,
        id: int | None = ...,
        description: str | None = ...,
        action: IngressActionDict | None = ...,
        classifier: IngressClassifierDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IngressObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: IngressPayload | None = ...,
        id: int | None = ...,
        description: str | None = ...,
        action: IngressActionDict | None = ...,
        classifier: IngressClassifierDict | None = ...,
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
    "Ingress",
    "IngressPayload",
    "IngressResponse",
    "IngressObject",
]