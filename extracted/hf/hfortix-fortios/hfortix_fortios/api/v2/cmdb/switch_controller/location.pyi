""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/location
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

class LocationAddresscivicDict(TypedDict, total=False):
    """Nested object type for address-civic field."""
    additional: str
    additional_code: str
    block: str
    branch_road: str
    building: str
    city: str
    city_division: str
    country: str
    country_subdivision: str
    county: str
    direction: str
    floor: str
    landmark: str
    language: str
    name: str
    number: str
    number_suffix: str
    place_type: str
    post_office_box: str
    postal_community: str
    primary_road: str
    road_section: str
    room: str
    script: str
    seat: str
    street: str
    street_name_post_mod: str
    street_name_pre_mod: str
    street_suffix: str
    sub_branch_road: str
    trailing_str_suffix: str
    unit: str
    zip: str
    parent_key: str


class LocationCoordinatesDict(TypedDict, total=False):
    """Nested object type for coordinates field."""
    altitude: str
    altitude_unit: Literal["m", "f"]
    datum: Literal["WGS84", "NAD83", "NAD83/MLLW"]
    latitude: str
    longitude: str
    parent_key: str


class LocationElinnumberDict(TypedDict, total=False):
    """Nested object type for elin-number field."""
    elin_num: str
    parent_key: str


class LocationPayload(TypedDict, total=False):
    """Payload type for Location operations."""
    name: str
    address_civic: LocationAddresscivicDict
    coordinates: LocationCoordinatesDict
    elin_number: LocationElinnumberDict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LocationResponse(TypedDict, total=False):
    """Response type for Location - use with .dict property for typed dict access."""
    name: str
    address_civic: LocationAddresscivicDict
    coordinates: LocationCoordinatesDict
    elin_number: LocationElinnumberDict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LocationAddresscivicObject(FortiObject):
    """Nested object for address-civic field with attribute access."""
    additional: str
    additional_code: str
    block: str
    branch_road: str
    building: str
    city: str
    city_division: str
    country: str
    country_subdivision: str
    county: str
    direction: str
    floor: str
    landmark: str
    language: str
    name: str
    number: str
    number_suffix: str
    place_type: str
    post_office_box: str
    postal_community: str
    primary_road: str
    road_section: str
    room: str
    script: str
    seat: str
    street: str
    street_name_post_mod: str
    street_name_pre_mod: str
    street_suffix: str
    sub_branch_road: str
    trailing_str_suffix: str
    unit: str
    zip: str
    parent_key: str


class LocationCoordinatesObject(FortiObject):
    """Nested object for coordinates field with attribute access."""
    altitude: str
    altitude_unit: Literal["m", "f"]
    datum: Literal["WGS84", "NAD83", "NAD83/MLLW"]
    latitude: str
    longitude: str
    parent_key: str


class LocationElinnumberObject(FortiObject):
    """Nested object for elin-number field with attribute access."""
    elin_num: str
    parent_key: str


class LocationObject(FortiObject):
    """Typed FortiObject for Location with field access."""
    name: str
    address_civic: LocationAddresscivicObject
    coordinates: LocationCoordinatesObject
    elin_number: LocationElinnumberObject


# ================================================================
# Main Endpoint Class
# ================================================================

class Location:
    """
    
    Endpoint: switch_controller/location
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
    ) -> LocationObject: ...
    
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
    ) -> FortiObjectList[LocationObject]: ...
    
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
        payload_dict: LocationPayload | None = ...,
        name: str | None = ...,
        address_civic: LocationAddresscivicDict | None = ...,
        coordinates: LocationCoordinatesDict | None = ...,
        elin_number: LocationElinnumberDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocationObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LocationPayload | None = ...,
        name: str | None = ...,
        address_civic: LocationAddresscivicDict | None = ...,
        coordinates: LocationCoordinatesDict | None = ...,
        elin_number: LocationElinnumberDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LocationObject: ...

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
        payload_dict: LocationPayload | None = ...,
        name: str | None = ...,
        address_civic: LocationAddresscivicDict | None = ...,
        coordinates: LocationCoordinatesDict | None = ...,
        elin_number: LocationElinnumberDict | None = ...,
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
    "Location",
    "LocationPayload",
    "LocationResponse",
    "LocationObject",
]