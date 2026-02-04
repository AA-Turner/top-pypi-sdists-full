""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/policy6
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

class Policy6InputdeviceItem(TypedDict, total=False):
    """Nested item for input-device field."""
    name: str


class Policy6SrcItem(TypedDict, total=False):
    """Nested item for src field."""
    addr6: str


class Policy6SrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class Policy6DstItem(TypedDict, total=False):
    """Nested item for dst field."""
    addr6: str


class Policy6DstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class Policy6InternetserviceidItem(TypedDict, total=False):
    """Nested item for internet-service-id field."""
    id: int


class Policy6InternetservicecustomItem(TypedDict, total=False):
    """Nested item for internet-service-custom field."""
    name: str


class Policy6InternetservicefortiguardItem(TypedDict, total=False):
    """Nested item for internet-service-fortiguard field."""
    name: str


class Policy6UsersItem(TypedDict, total=False):
    """Nested item for users field."""
    name: str


class Policy6GroupsItem(TypedDict, total=False):
    """Nested item for groups field."""
    name: str


class Policy6Payload(TypedDict, total=False):
    """Payload type for Policy6 operations."""
    seq_num: int
    input_device: str | list[str] | list[Policy6InputdeviceItem]
    input_device_negate: Literal["enable", "disable"]
    src: str | list[str] | list[Policy6SrcItem]
    srcaddr: str | list[str] | list[Policy6SrcaddrItem]
    src_negate: Literal["enable", "disable"]
    dst: str | list[str] | list[Policy6DstItem]
    dstaddr: str | list[str] | list[Policy6DstaddrItem]
    dst_negate: Literal["enable", "disable"]
    action: Literal["deny", "permit"]
    protocol: int
    start_port: int
    end_port: int
    start_source_port: int
    end_source_port: int
    gateway: str
    output_device: str
    tos: str
    tos_mask: str
    status: Literal["enable", "disable"]
    comments: str
    internet_service_id: str | list[str] | list[Policy6InternetserviceidItem]
    internet_service_custom: str | list[str] | list[Policy6InternetservicecustomItem]
    internet_service_fortiguard: str | list[str] | list[Policy6InternetservicefortiguardItem]
    users: str | list[str] | list[Policy6UsersItem]
    groups: str | list[str] | list[Policy6GroupsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Policy6Response(TypedDict, total=False):
    """Response type for Policy6 - use with .dict property for typed dict access."""
    seq_num: int
    input_device: list[Policy6InputdeviceItem]
    input_device_negate: Literal["enable", "disable"]
    src: list[Policy6SrcItem]
    srcaddr: list[Policy6SrcaddrItem]
    src_negate: Literal["enable", "disable"]
    dst: list[Policy6DstItem]
    dstaddr: list[Policy6DstaddrItem]
    dst_negate: Literal["enable", "disable"]
    action: Literal["deny", "permit"]
    protocol: int
    start_port: int
    end_port: int
    start_source_port: int
    end_source_port: int
    gateway: str
    output_device: str
    tos: str
    tos_mask: str
    status: Literal["enable", "disable"]
    comments: str
    internet_service_id: list[Policy6InternetserviceidItem]
    internet_service_custom: list[Policy6InternetservicecustomItem]
    internet_service_fortiguard: list[Policy6InternetservicefortiguardItem]
    users: list[Policy6UsersItem]
    groups: list[Policy6GroupsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Policy6InputdeviceItemObject(FortiObject[Policy6InputdeviceItem]):
    """Typed object for input-device table items with attribute access."""
    name: str


class Policy6SrcItemObject(FortiObject[Policy6SrcItem]):
    """Typed object for src table items with attribute access."""
    addr6: str


class Policy6SrcaddrItemObject(FortiObject[Policy6SrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class Policy6DstItemObject(FortiObject[Policy6DstItem]):
    """Typed object for dst table items with attribute access."""
    addr6: str


class Policy6DstaddrItemObject(FortiObject[Policy6DstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class Policy6InternetserviceidItemObject(FortiObject[Policy6InternetserviceidItem]):
    """Typed object for internet-service-id table items with attribute access."""
    id: int


class Policy6InternetservicecustomItemObject(FortiObject[Policy6InternetservicecustomItem]):
    """Typed object for internet-service-custom table items with attribute access."""
    name: str


class Policy6InternetservicefortiguardItemObject(FortiObject[Policy6InternetservicefortiguardItem]):
    """Typed object for internet-service-fortiguard table items with attribute access."""
    name: str


class Policy6UsersItemObject(FortiObject[Policy6UsersItem]):
    """Typed object for users table items with attribute access."""
    name: str


class Policy6GroupsItemObject(FortiObject[Policy6GroupsItem]):
    """Typed object for groups table items with attribute access."""
    name: str


class Policy6Object(FortiObject):
    """Typed FortiObject for Policy6 with field access."""
    seq_num: int
    input_device: FortiObjectList[Policy6InputdeviceItemObject]
    input_device_negate: Literal["enable", "disable"]
    src: FortiObjectList[Policy6SrcItemObject]
    srcaddr: FortiObjectList[Policy6SrcaddrItemObject]
    src_negate: Literal["enable", "disable"]
    dst: FortiObjectList[Policy6DstItemObject]
    dstaddr: FortiObjectList[Policy6DstaddrItemObject]
    dst_negate: Literal["enable", "disable"]
    action: Literal["deny", "permit"]
    protocol: int
    start_port: int
    end_port: int
    start_source_port: int
    end_source_port: int
    gateway: str
    output_device: str
    tos: str
    tos_mask: str
    status: Literal["enable", "disable"]
    comments: str
    internet_service_id: FortiObjectList[Policy6InternetserviceidItemObject]
    internet_service_custom: FortiObjectList[Policy6InternetservicecustomItemObject]
    internet_service_fortiguard: FortiObjectList[Policy6InternetservicefortiguardItemObject]
    users: FortiObjectList[Policy6UsersItemObject]
    groups: FortiObjectList[Policy6GroupsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Policy6:
    """
    
    Endpoint: router/policy6
    Category: cmdb
    MKey: seq-num
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
        seq_num: int,
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
    ) -> Policy6Object: ...
    
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
    ) -> FortiObjectList[Policy6Object]: ...
    
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
        payload_dict: Policy6Payload | None = ...,
        seq_num: int | None = ...,
        input_device: str | list[str] | list[Policy6InputdeviceItem] | None = ...,
        input_device_negate: Literal["enable", "disable"] | None = ...,
        src: str | list[str] | list[Policy6SrcItem] | None = ...,
        srcaddr: str | list[str] | list[Policy6SrcaddrItem] | None = ...,
        src_negate: Literal["enable", "disable"] | None = ...,
        dst: str | list[str] | list[Policy6DstItem] | None = ...,
        dstaddr: str | list[str] | list[Policy6DstaddrItem] | None = ...,
        dst_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["deny", "permit"] | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        start_source_port: int | None = ...,
        end_source_port: int | None = ...,
        gateway: str | None = ...,
        output_device: str | None = ...,
        tos: str | None = ...,
        tos_mask: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        internet_service_id: str | list[str] | list[Policy6InternetserviceidItem] | None = ...,
        internet_service_custom: str | list[str] | list[Policy6InternetservicecustomItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[Policy6InternetservicefortiguardItem] | None = ...,
        users: str | list[str] | list[Policy6UsersItem] | None = ...,
        groups: str | list[str] | list[Policy6GroupsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Policy6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Policy6Payload | None = ...,
        seq_num: int | None = ...,
        input_device: str | list[str] | list[Policy6InputdeviceItem] | None = ...,
        input_device_negate: Literal["enable", "disable"] | None = ...,
        src: str | list[str] | list[Policy6SrcItem] | None = ...,
        srcaddr: str | list[str] | list[Policy6SrcaddrItem] | None = ...,
        src_negate: Literal["enable", "disable"] | None = ...,
        dst: str | list[str] | list[Policy6DstItem] | None = ...,
        dstaddr: str | list[str] | list[Policy6DstaddrItem] | None = ...,
        dst_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["deny", "permit"] | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        start_source_port: int | None = ...,
        end_source_port: int | None = ...,
        gateway: str | None = ...,
        output_device: str | None = ...,
        tos: str | None = ...,
        tos_mask: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        internet_service_id: str | list[str] | list[Policy6InternetserviceidItem] | None = ...,
        internet_service_custom: str | list[str] | list[Policy6InternetservicecustomItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[Policy6InternetservicefortiguardItem] | None = ...,
        users: str | list[str] | list[Policy6UsersItem] | None = ...,
        groups: str | list[str] | list[Policy6GroupsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Policy6Object: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        seq_num: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        seq_num: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_seq_num: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        seq_num: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: Policy6Payload | None = ...,
        seq_num: int | None = ...,
        input_device: str | list[str] | list[Policy6InputdeviceItem] | None = ...,
        input_device_negate: Literal["enable", "disable"] | None = ...,
        src: str | list[str] | list[Policy6SrcItem] | None = ...,
        srcaddr: str | list[str] | list[Policy6SrcaddrItem] | None = ...,
        src_negate: Literal["enable", "disable"] | None = ...,
        dst: str | list[str] | list[Policy6DstItem] | None = ...,
        dstaddr: str | list[str] | list[Policy6DstaddrItem] | None = ...,
        dst_negate: Literal["enable", "disable"] | None = ...,
        action: Literal["deny", "permit"] | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        start_source_port: int | None = ...,
        end_source_port: int | None = ...,
        gateway: str | None = ...,
        output_device: str | None = ...,
        tos: str | None = ...,
        tos_mask: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        internet_service_id: str | list[str] | list[Policy6InternetserviceidItem] | None = ...,
        internet_service_custom: str | list[str] | list[Policy6InternetservicecustomItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[Policy6InternetservicefortiguardItem] | None = ...,
        users: str | list[str] | list[Policy6UsersItem] | None = ...,
        groups: str | list[str] | list[Policy6GroupsItem] | None = ...,
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
    "Policy6",
    "Policy6Payload",
    "Policy6Response",
    "Policy6Object",
]