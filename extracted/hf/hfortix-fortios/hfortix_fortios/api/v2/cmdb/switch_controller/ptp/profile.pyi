""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/ptp/profile
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

class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    description: str
    mode: Literal["transparent-e2e", "transparent-p2p"]
    ptp_profile: Literal["C37.238-2017"]
    transport: Literal["l2-mcast"]
    domain: int
    pdelay_req_interval: Literal["1sec", "2sec", "4sec", "8sec", "16sec", "32sec"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    description: str
    mode: Literal["transparent-e2e", "transparent-p2p"]
    ptp_profile: Literal["C37.238-2017"]
    transport: Literal["l2-mcast"]
    domain: int
    pdelay_req_interval: Literal["1sec", "2sec", "4sec", "8sec", "16sec", "32sec"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    description: str
    mode: Literal["transparent-e2e", "transparent-p2p"]
    ptp_profile: Literal["C37.238-2017"]
    transport: Literal["l2-mcast"]
    domain: int
    pdelay_req_interval: Literal["1sec", "2sec", "4sec", "8sec", "16sec", "32sec"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: switch_controller/ptp/profile
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
    ) -> ProfileObject: ...
    
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
    ) -> FortiObjectList[ProfileObject]: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        mode: Literal["transparent-e2e", "transparent-p2p"] | None = ...,
        ptp_profile: Literal["C37.238-2017"] | None = ...,
        transport: Literal["l2-mcast"] | None = ...,
        domain: int | None = ...,
        pdelay_req_interval: Literal["1sec", "2sec", "4sec", "8sec", "16sec", "32sec"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        mode: Literal["transparent-e2e", "transparent-p2p"] | None = ...,
        ptp_profile: Literal["C37.238-2017"] | None = ...,
        transport: Literal["l2-mcast"] | None = ...,
        domain: int | None = ...,
        pdelay_req_interval: Literal["1sec", "2sec", "4sec", "8sec", "16sec", "32sec"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        mode: Literal["transparent-e2e", "transparent-p2p"] | None = ...,
        ptp_profile: Literal["C37.238-2017"] | None = ...,
        transport: Literal["l2-mcast"] | None = ...,
        domain: int | None = ...,
        pdelay_req_interval: Literal["1sec", "2sec", "4sec", "8sec", "16sec", "32sec"] | None = ...,
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
    "Profile",
    "ProfilePayload",
    "ProfileResponse",
    "ProfileObject",
]