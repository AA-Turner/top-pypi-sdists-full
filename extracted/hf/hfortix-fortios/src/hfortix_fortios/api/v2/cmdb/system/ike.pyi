""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ike
Category: cmdb
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
# TypedDict Payloads
# ================================================================

class IkeDhgroup1Dict(TypedDict, total=False):
    """Nested object type for dh-group-1 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup2Dict(TypedDict, total=False):
    """Nested object type for dh-group-2 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup5Dict(TypedDict, total=False):
    """Nested object type for dh-group-5 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup14Dict(TypedDict, total=False):
    """Nested object type for dh-group-14 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup15Dict(TypedDict, total=False):
    """Nested object type for dh-group-15 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup16Dict(TypedDict, total=False):
    """Nested object type for dh-group-16 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup17Dict(TypedDict, total=False):
    """Nested object type for dh-group-17 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup18Dict(TypedDict, total=False):
    """Nested object type for dh-group-18 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup19Dict(TypedDict, total=False):
    """Nested object type for dh-group-19 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup20Dict(TypedDict, total=False):
    """Nested object type for dh-group-20 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup21Dict(TypedDict, total=False):
    """Nested object type for dh-group-21 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup27Dict(TypedDict, total=False):
    """Nested object type for dh-group-27 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup28Dict(TypedDict, total=False):
    """Nested object type for dh-group-28 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup29Dict(TypedDict, total=False):
    """Nested object type for dh-group-29 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup30Dict(TypedDict, total=False):
    """Nested object type for dh-group-30 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup31Dict(TypedDict, total=False):
    """Nested object type for dh-group-31 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup32Dict(TypedDict, total=False):
    """Nested object type for dh-group-32 field."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkePayload(TypedDict, total=False):
    """Payload type for Ike operations."""
    embryonic_limit: int
    dh_multiprocess: Literal["enable", "disable"]
    dh_worker_count: int
    dh_mode: Literal["software", "hardware"]
    dh_keypair_cache: Literal["enable", "disable"]
    dh_keypair_count: int
    dh_keypair_throttle: Literal["enable", "disable"]
    dh_group_1: IkeDhgroup1Dict
    dh_group_2: IkeDhgroup2Dict
    dh_group_5: IkeDhgroup5Dict
    dh_group_14: IkeDhgroup14Dict
    dh_group_15: IkeDhgroup15Dict
    dh_group_16: IkeDhgroup16Dict
    dh_group_17: IkeDhgroup17Dict
    dh_group_18: IkeDhgroup18Dict
    dh_group_19: IkeDhgroup19Dict
    dh_group_20: IkeDhgroup20Dict
    dh_group_21: IkeDhgroup21Dict
    dh_group_27: IkeDhgroup27Dict
    dh_group_28: IkeDhgroup28Dict
    dh_group_29: IkeDhgroup29Dict
    dh_group_30: IkeDhgroup30Dict
    dh_group_31: IkeDhgroup31Dict
    dh_group_32: IkeDhgroup32Dict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IkeResponse(TypedDict, total=False):
    """Response type for Ike - use with .dict property for typed dict access."""
    embryonic_limit: int
    dh_multiprocess: Literal["enable", "disable"]
    dh_worker_count: int
    dh_mode: Literal["software", "hardware"]
    dh_keypair_cache: Literal["enable", "disable"]
    dh_keypair_count: int
    dh_keypair_throttle: Literal["enable", "disable"]
    dh_group_1: IkeDhgroup1Dict
    dh_group_2: IkeDhgroup2Dict
    dh_group_5: IkeDhgroup5Dict
    dh_group_14: IkeDhgroup14Dict
    dh_group_15: IkeDhgroup15Dict
    dh_group_16: IkeDhgroup16Dict
    dh_group_17: IkeDhgroup17Dict
    dh_group_18: IkeDhgroup18Dict
    dh_group_19: IkeDhgroup19Dict
    dh_group_20: IkeDhgroup20Dict
    dh_group_21: IkeDhgroup21Dict
    dh_group_27: IkeDhgroup27Dict
    dh_group_28: IkeDhgroup28Dict
    dh_group_29: IkeDhgroup29Dict
    dh_group_30: IkeDhgroup30Dict
    dh_group_31: IkeDhgroup31Dict
    dh_group_32: IkeDhgroup32Dict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IkeDhgroup1Object(FortiObject):
    """Nested object for dh-group-1 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup2Object(FortiObject):
    """Nested object for dh-group-2 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup5Object(FortiObject):
    """Nested object for dh-group-5 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup14Object(FortiObject):
    """Nested object for dh-group-14 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup15Object(FortiObject):
    """Nested object for dh-group-15 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup16Object(FortiObject):
    """Nested object for dh-group-16 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup17Object(FortiObject):
    """Nested object for dh-group-17 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup18Object(FortiObject):
    """Nested object for dh-group-18 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup19Object(FortiObject):
    """Nested object for dh-group-19 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup20Object(FortiObject):
    """Nested object for dh-group-20 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup21Object(FortiObject):
    """Nested object for dh-group-21 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup27Object(FortiObject):
    """Nested object for dh-group-27 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup28Object(FortiObject):
    """Nested object for dh-group-28 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup29Object(FortiObject):
    """Nested object for dh-group-29 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup30Object(FortiObject):
    """Nested object for dh-group-30 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup31Object(FortiObject):
    """Nested object for dh-group-31 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeDhgroup32Object(FortiObject):
    """Nested object for dh-group-32 field with attribute access."""
    mode: Literal["software", "hardware", "global"]
    keypair_cache: Literal["global", "custom"]
    keypair_count: int


class IkeObject(FortiObject):
    """Typed FortiObject for Ike with field access."""
    embryonic_limit: int
    dh_multiprocess: Literal["enable", "disable"]
    dh_worker_count: int
    dh_mode: Literal["software", "hardware"]
    dh_keypair_cache: Literal["enable", "disable"]
    dh_keypair_count: int
    dh_keypair_throttle: Literal["enable", "disable"]
    dh_group_1: IkeDhgroup1Object
    dh_group_2: IkeDhgroup2Object
    dh_group_5: IkeDhgroup5Object
    dh_group_14: IkeDhgroup14Object
    dh_group_15: IkeDhgroup15Object
    dh_group_16: IkeDhgroup16Object
    dh_group_17: IkeDhgroup17Object
    dh_group_18: IkeDhgroup18Object
    dh_group_19: IkeDhgroup19Object
    dh_group_20: IkeDhgroup20Object
    dh_group_21: IkeDhgroup21Object
    dh_group_27: IkeDhgroup27Object
    dh_group_28: IkeDhgroup28Object
    dh_group_29: IkeDhgroup29Object
    dh_group_30: IkeDhgroup30Object
    dh_group_31: IkeDhgroup31Object
    dh_group_32: IkeDhgroup32Object


# ================================================================
# Main Endpoint Class
# ================================================================

class Ike:
    """
    
    Endpoint: system/ike
    Category: cmdb
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
    
    # Singleton endpoint (no mkey)
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
    ) -> IkeObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: IkePayload | None = ...,
        embryonic_limit: int | None = ...,
        dh_multiprocess: Literal["enable", "disable"] | None = ...,
        dh_worker_count: int | None = ...,
        dh_mode: Literal["software", "hardware"] | None = ...,
        dh_keypair_cache: Literal["enable", "disable"] | None = ...,
        dh_keypair_count: int | None = ...,
        dh_keypair_throttle: Literal["enable", "disable"] | None = ...,
        dh_group_1: IkeDhgroup1Dict | None = ...,
        dh_group_2: IkeDhgroup2Dict | None = ...,
        dh_group_5: IkeDhgroup5Dict | None = ...,
        dh_group_14: IkeDhgroup14Dict | None = ...,
        dh_group_15: IkeDhgroup15Dict | None = ...,
        dh_group_16: IkeDhgroup16Dict | None = ...,
        dh_group_17: IkeDhgroup17Dict | None = ...,
        dh_group_18: IkeDhgroup18Dict | None = ...,
        dh_group_19: IkeDhgroup19Dict | None = ...,
        dh_group_20: IkeDhgroup20Dict | None = ...,
        dh_group_21: IkeDhgroup21Dict | None = ...,
        dh_group_27: IkeDhgroup27Dict | None = ...,
        dh_group_28: IkeDhgroup28Dict | None = ...,
        dh_group_29: IkeDhgroup29Dict | None = ...,
        dh_group_30: IkeDhgroup30Dict | None = ...,
        dh_group_31: IkeDhgroup31Dict | None = ...,
        dh_group_32: IkeDhgroup32Dict | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IkeObject: ...


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
        payload_dict: IkePayload | None = ...,
        embryonic_limit: int | None = ...,
        dh_multiprocess: Literal["enable", "disable"] | None = ...,
        dh_worker_count: int | None = ...,
        dh_mode: Literal["software", "hardware"] | None = ...,
        dh_keypair_cache: Literal["enable", "disable"] | None = ...,
        dh_keypair_count: int | None = ...,
        dh_keypair_throttle: Literal["enable", "disable"] | None = ...,
        dh_group_1: IkeDhgroup1Dict | None = ...,
        dh_group_2: IkeDhgroup2Dict | None = ...,
        dh_group_5: IkeDhgroup5Dict | None = ...,
        dh_group_14: IkeDhgroup14Dict | None = ...,
        dh_group_15: IkeDhgroup15Dict | None = ...,
        dh_group_16: IkeDhgroup16Dict | None = ...,
        dh_group_17: IkeDhgroup17Dict | None = ...,
        dh_group_18: IkeDhgroup18Dict | None = ...,
        dh_group_19: IkeDhgroup19Dict | None = ...,
        dh_group_20: IkeDhgroup20Dict | None = ...,
        dh_group_21: IkeDhgroup21Dict | None = ...,
        dh_group_27: IkeDhgroup27Dict | None = ...,
        dh_group_28: IkeDhgroup28Dict | None = ...,
        dh_group_29: IkeDhgroup29Dict | None = ...,
        dh_group_30: IkeDhgroup30Dict | None = ...,
        dh_group_31: IkeDhgroup31Dict | None = ...,
        dh_group_32: IkeDhgroup32Dict | None = ...,
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
    "Ike",
    "IkePayload",
    "IkeResponse",
    "IkeObject",
]