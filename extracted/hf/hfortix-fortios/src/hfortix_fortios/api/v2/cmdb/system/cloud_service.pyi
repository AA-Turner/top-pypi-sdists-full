""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/cloud_service
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

class CloudServicePayload(TypedDict, total=False):
    """Payload type for CloudService operations."""
    name: str
    vendor: Literal["unknown", "google-cloud-kms"]
    traffic_vdom: str
    gck_service_account: str
    gck_private_key: str
    gck_keyid: str
    gck_access_token_lifetime: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CloudServiceResponse(TypedDict, total=False):
    """Response type for CloudService - use with .dict property for typed dict access."""
    name: str
    vendor: Literal["unknown", "google-cloud-kms"]
    traffic_vdom: str
    gck_service_account: str
    gck_private_key: str
    gck_keyid: str
    gck_access_token_lifetime: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CloudServiceObject(FortiObject):
    """Typed FortiObject for CloudService with field access."""
    name: str
    vendor: Literal["unknown", "google-cloud-kms"]
    traffic_vdom: str
    gck_service_account: str
    gck_private_key: str
    gck_keyid: str
    gck_access_token_lifetime: int


# ================================================================
# Main Endpoint Class
# ================================================================

class CloudService:
    """
    
    Endpoint: system/cloud_service
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CloudServiceObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[CloudServiceObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CloudServiceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CloudServiceObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
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
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
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
    "CloudService",
    "CloudServicePayload",
    "CloudServiceResponse",
    "CloudServiceObject",
]