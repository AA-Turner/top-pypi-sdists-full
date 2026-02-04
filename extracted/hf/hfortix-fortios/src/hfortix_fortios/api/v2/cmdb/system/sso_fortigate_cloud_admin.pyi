""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/sso_fortigate_cloud_admin
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

class SsoFortigateCloudAdminVdomItem(TypedDict, total=False):
    """Nested item for vdom field."""
    name: str


class SsoFortigateCloudAdminPayload(TypedDict, total=False):
    """Payload type for SsoFortigateCloudAdmin operations."""
    name: str
    accprofile: str
    vdom: str | list[str] | list[SsoFortigateCloudAdminVdomItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SsoFortigateCloudAdminResponse(TypedDict, total=False):
    """Response type for SsoFortigateCloudAdmin - use with .dict property for typed dict access."""
    name: str
    accprofile: str
    vdom: list[SsoFortigateCloudAdminVdomItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SsoFortigateCloudAdminVdomItemObject(FortiObject[SsoFortigateCloudAdminVdomItem]):
    """Typed object for vdom table items with attribute access."""
    name: str


class SsoFortigateCloudAdminObject(FortiObject):
    """Typed FortiObject for SsoFortigateCloudAdmin with field access."""
    name: str
    accprofile: str


# ================================================================
# Main Endpoint Class
# ================================================================

class SsoFortigateCloudAdmin:
    """
    
    Endpoint: system/sso_fortigate_cloud_admin
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
    ) -> SsoFortigateCloudAdminObject: ...
    
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
    ) -> FortiObjectList[SsoFortigateCloudAdminObject]: ...
    
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
        payload_dict: SsoFortigateCloudAdminPayload | None = ...,
        name: str | None = ...,
        accprofile: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SsoFortigateCloudAdminObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SsoFortigateCloudAdminPayload | None = ...,
        name: str | None = ...,
        accprofile: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SsoFortigateCloudAdminObject: ...

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
        payload_dict: SsoFortigateCloudAdminPayload | None = ...,
        name: str | None = ...,
        accprofile: str | None = ...,
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
    "SsoFortigateCloudAdmin",
    "SsoFortigateCloudAdminPayload",
    "SsoFortigateCloudAdminResponse",
    "SsoFortigateCloudAdminObject",
]