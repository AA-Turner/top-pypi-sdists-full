""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: extension_controller/dataplan
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

class DataplanPayload(TypedDict, total=False):
    """Payload type for Dataplan operations."""
    name: str
    modem_id: Literal["modem1", "modem2", "all"]
    type: Literal["carrier", "slot", "iccid", "generic"]
    slot: Literal["sim1", "sim2"]
    iccid: str
    carrier: str
    apn: str
    auth_type: Literal["none", "pap", "chap"]
    username: str
    password: str
    pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"]
    signal_threshold: int
    signal_period: int
    capacity: int
    monthly_fee: int
    billing_date: int
    overage: Literal["disable", "enable"]
    preferred_subnet: int
    private_network: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DataplanResponse(TypedDict, total=False):
    """Response type for Dataplan - use with .dict property for typed dict access."""
    name: str
    modem_id: Literal["modem1", "modem2", "all"]
    type: Literal["carrier", "slot", "iccid", "generic"]
    slot: Literal["sim1", "sim2"]
    iccid: str
    carrier: str
    apn: str
    auth_type: Literal["none", "pap", "chap"]
    username: str
    password: str
    pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"]
    signal_threshold: int
    signal_period: int
    capacity: int
    monthly_fee: int
    billing_date: int
    overage: Literal["disable", "enable"]
    preferred_subnet: int
    private_network: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DataplanObject(FortiObject):
    """Typed FortiObject for Dataplan with field access."""
    name: str
    modem_id: Literal["modem1", "modem2", "all"]
    type: Literal["carrier", "slot", "iccid", "generic"]
    slot: Literal["sim1", "sim2"]
    iccid: str
    carrier: str
    apn: str
    auth_type: Literal["none", "pap", "chap"]
    username: str
    password: str
    pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"]
    signal_threshold: int
    signal_period: int
    capacity: int
    monthly_fee: int
    billing_date: int
    overage: Literal["disable", "enable"]
    preferred_subnet: int
    private_network: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Dataplan:
    """
    
    Endpoint: extension_controller/dataplan
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
    ) -> DataplanObject: ...
    
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
    ) -> FortiObjectList[DataplanObject]: ...
    
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
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DataplanObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DataplanObject: ...

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
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
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
    "Dataplan",
    "DataplanPayload",
    "DataplanResponse",
    "DataplanObject",
]