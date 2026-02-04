""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/h2qp_osu_provider
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

class H2qpOsuProviderFriendlynameItem(TypedDict, total=False):
    """Nested item for friendly-name field."""
    index: int
    lang: str
    friendly_name: str


class H2qpOsuProviderServicedescriptionItem(TypedDict, total=False):
    """Nested item for service-description field."""
    service_id: int
    lang: str
    service_description: str


class H2qpOsuProviderPayload(TypedDict, total=False):
    """Payload type for H2qpOsuProvider operations."""
    name: str
    friendly_name: str | list[str] | list[H2qpOsuProviderFriendlynameItem]
    server_uri: str
    osu_method: str | list[str]
    osu_nai: str
    service_description: str | list[str] | list[H2qpOsuProviderServicedescriptionItem]
    icon: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class H2qpOsuProviderResponse(TypedDict, total=False):
    """Response type for H2qpOsuProvider - use with .dict property for typed dict access."""
    name: str
    friendly_name: list[H2qpOsuProviderFriendlynameItem]
    server_uri: str
    osu_method: str
    osu_nai: str
    service_description: list[H2qpOsuProviderServicedescriptionItem]
    icon: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class H2qpOsuProviderFriendlynameItemObject(FortiObject[H2qpOsuProviderFriendlynameItem]):
    """Typed object for friendly-name table items with attribute access."""
    index: int
    lang: str
    friendly_name: str


class H2qpOsuProviderServicedescriptionItemObject(FortiObject[H2qpOsuProviderServicedescriptionItem]):
    """Typed object for service-description table items with attribute access."""
    service_id: int
    lang: str
    service_description: str


class H2qpOsuProviderObject(FortiObject):
    """Typed FortiObject for H2qpOsuProvider with field access."""
    name: str
    friendly_name: FortiObjectList[H2qpOsuProviderFriendlynameItemObject]
    server_uri: str
    osu_method: str
    osu_nai: str
    service_description: FortiObjectList[H2qpOsuProviderServicedescriptionItemObject]
    icon: str


# ================================================================
# Main Endpoint Class
# ================================================================

class H2qpOsuProvider:
    """
    
    Endpoint: wireless_controller/hotspot20/h2qp_osu_provider
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
    ) -> H2qpOsuProviderObject: ...
    
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
    ) -> FortiObjectList[H2qpOsuProviderObject]: ...
    
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
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[H2qpOsuProviderFriendlynameItem] | None = ...,
        server_uri: str | None = ...,
        osu_method: str | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[H2qpOsuProviderServicedescriptionItem] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpOsuProviderObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[H2qpOsuProviderFriendlynameItem] | None = ...,
        server_uri: str | None = ...,
        osu_method: str | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[H2qpOsuProviderServicedescriptionItem] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpOsuProviderObject: ...

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
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[H2qpOsuProviderFriendlynameItem] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[H2qpOsuProviderServicedescriptionItem] | None = ...,
        icon: str | None = ...,
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
    "H2qpOsuProvider",
    "H2qpOsuProviderPayload",
    "H2qpOsuProviderResponse",
    "H2qpOsuProviderObject",
]