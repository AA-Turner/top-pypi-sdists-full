""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: extension_controller/fortigate_profile
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

class FortigateProfileLanextensionDict(TypedDict, total=False):
    """Nested object type for lan-extension field."""
    ipsec_tunnel: str
    backhaul_interface: str
    backhaul_ip: str


class FortigateProfilePayload(TypedDict, total=False):
    """Payload type for FortigateProfile operations."""
    name: str
    id: int
    extension: Literal["lan-extension"]
    lan_extension: FortigateProfileLanextensionDict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FortigateProfileResponse(TypedDict, total=False):
    """Response type for FortigateProfile - use with .dict property for typed dict access."""
    name: str
    id: int
    extension: Literal["lan-extension"]
    lan_extension: FortigateProfileLanextensionDict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FortigateProfileLanextensionObject(FortiObject):
    """Nested object for lan-extension field with attribute access."""
    ipsec_tunnel: str
    backhaul_interface: str
    backhaul_ip: str


class FortigateProfileObject(FortiObject):
    """Typed FortiObject for FortigateProfile with field access."""
    name: str
    id: int
    extension: Literal["lan-extension"]
    lan_extension: FortigateProfileLanextensionObject


# ================================================================
# Main Endpoint Class
# ================================================================

class FortigateProfile:
    """
    
    Endpoint: extension_controller/fortigate_profile
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
    ) -> FortigateProfileObject: ...
    
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
    ) -> FortiObjectList[FortigateProfileObject]: ...
    
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
        payload_dict: FortigateProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        extension: Literal["lan-extension"] | None = ...,
        lan_extension: FortigateProfileLanextensionDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortigateProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FortigateProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        extension: Literal["lan-extension"] | None = ...,
        lan_extension: FortigateProfileLanextensionDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortigateProfileObject: ...

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
        payload_dict: FortigateProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        extension: Literal["lan-extension"] | None = ...,
        lan_extension: FortigateProfileLanextensionDict | None = ...,
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
    "FortigateProfile",
    "FortigateProfilePayload",
    "FortigateProfileResponse",
    "FortigateProfileObject",
]