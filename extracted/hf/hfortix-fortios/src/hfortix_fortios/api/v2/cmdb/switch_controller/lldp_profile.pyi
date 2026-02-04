""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/lldp_profile
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

class LldpProfileMednetworkpolicyItem(TypedDict, total=False):
    """Nested item for med-network-policy field."""
    name: str
    status: Literal["disable", "enable"]
    vlan_intf: str
    assign_vlan: Literal["disable", "enable"]
    priority: int
    dscp: int


class LldpProfileMedlocationserviceItem(TypedDict, total=False):
    """Nested item for med-location-service field."""
    name: str
    status: Literal["disable", "enable"]
    sys_location_id: str


class LldpProfileCustomtlvsItem(TypedDict, total=False):
    """Nested item for custom-tlvs field."""
    name: str
    oui: str
    subtype: int
    information_string: str


class LldpProfilePayload(TypedDict, total=False):
    """Payload type for LldpProfile operations."""
    name: str
    med_tlvs: str | list[str]
    x802_1_tlvs: str | list[str]
    x802_3_tlvs: str | list[str]
    auto_isl: Literal["disable", "enable"]
    auto_isl_hello_timer: int
    auto_isl_receive_timeout: int
    auto_isl_port_group: int
    auto_mclag_icl: Literal["disable", "enable"]
    auto_isl_auth: Literal["legacy", "strict", "relax"]
    auto_isl_auth_user: str
    auto_isl_auth_identity: str
    auto_isl_auth_reauth: int
    auto_isl_auth_encrypt: Literal["none", "mixed", "must"]
    auto_isl_auth_macsec_profile: str
    med_network_policy: str | list[str] | list[LldpProfileMednetworkpolicyItem]
    med_location_service: str | list[str] | list[LldpProfileMedlocationserviceItem]
    custom_tlvs: str | list[str] | list[LldpProfileCustomtlvsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LldpProfileResponse(TypedDict, total=False):
    """Response type for LldpProfile - use with .dict property for typed dict access."""
    name: str
    med_tlvs: str
    x802_1_tlvs: str
    x802_3_tlvs: str
    auto_isl: Literal["disable", "enable"]
    auto_isl_hello_timer: int
    auto_isl_receive_timeout: int
    auto_isl_port_group: int
    auto_mclag_icl: Literal["disable", "enable"]
    auto_isl_auth: Literal["legacy", "strict", "relax"]
    auto_isl_auth_user: str
    auto_isl_auth_identity: str
    auto_isl_auth_reauth: int
    auto_isl_auth_encrypt: Literal["none", "mixed", "must"]
    auto_isl_auth_macsec_profile: str
    med_network_policy: list[LldpProfileMednetworkpolicyItem]
    med_location_service: list[LldpProfileMedlocationserviceItem]
    custom_tlvs: list[LldpProfileCustomtlvsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LldpProfileMednetworkpolicyItemObject(FortiObject[LldpProfileMednetworkpolicyItem]):
    """Typed object for med-network-policy table items with attribute access."""
    name: str
    status: Literal["disable", "enable"]
    vlan_intf: str
    assign_vlan: Literal["disable", "enable"]
    priority: int
    dscp: int


class LldpProfileMedlocationserviceItemObject(FortiObject[LldpProfileMedlocationserviceItem]):
    """Typed object for med-location-service table items with attribute access."""
    name: str
    status: Literal["disable", "enable"]
    sys_location_id: str


class LldpProfileCustomtlvsItemObject(FortiObject[LldpProfileCustomtlvsItem]):
    """Typed object for custom-tlvs table items with attribute access."""
    name: str
    oui: str
    subtype: int
    information_string: str


class LldpProfileObject(FortiObject):
    """Typed FortiObject for LldpProfile with field access."""
    name: str
    med_tlvs: str
    x802_1_tlvs: str
    x802_3_tlvs: str
    auto_isl: Literal["disable", "enable"]
    auto_isl_hello_timer: int
    auto_isl_receive_timeout: int
    auto_isl_port_group: int
    auto_mclag_icl: Literal["disable", "enable"]
    auto_isl_auth: Literal["legacy", "strict", "relax"]
    auto_isl_auth_user: str
    auto_isl_auth_identity: str
    auto_isl_auth_reauth: int
    auto_isl_auth_encrypt: Literal["none", "mixed", "must"]
    auto_isl_auth_macsec_profile: str
    med_network_policy: FortiObjectList[LldpProfileMednetworkpolicyItemObject]
    med_location_service: FortiObjectList[LldpProfileMedlocationserviceItemObject]
    custom_tlvs: FortiObjectList[LldpProfileCustomtlvsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class LldpProfile:
    """
    
    Endpoint: switch_controller/lldp_profile
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
    ) -> LldpProfileObject: ...
    
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
    ) -> FortiObjectList[LldpProfileObject]: ...
    
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
        payload_dict: LldpProfilePayload | None = ...,
        name: str | None = ...,
        med_tlvs: str | list[str] | None = ...,
        x802_1_tlvs: str | list[str] | None = ...,
        x802_3_tlvs: str | list[str] | None = ...,
        auto_isl: Literal["disable", "enable"] | None = ...,
        auto_isl_hello_timer: int | None = ...,
        auto_isl_receive_timeout: int | None = ...,
        auto_isl_port_group: int | None = ...,
        auto_mclag_icl: Literal["disable", "enable"] | None = ...,
        auto_isl_auth: Literal["legacy", "strict", "relax"] | None = ...,
        auto_isl_auth_user: str | None = ...,
        auto_isl_auth_identity: str | None = ...,
        auto_isl_auth_reauth: int | None = ...,
        auto_isl_auth_encrypt: Literal["none", "mixed", "must"] | None = ...,
        auto_isl_auth_macsec_profile: str | None = ...,
        med_network_policy: str | list[str] | list[LldpProfileMednetworkpolicyItem] | None = ...,
        med_location_service: str | list[str] | list[LldpProfileMedlocationserviceItem] | None = ...,
        custom_tlvs: str | list[str] | list[LldpProfileCustomtlvsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LldpProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LldpProfilePayload | None = ...,
        name: str | None = ...,
        med_tlvs: str | list[str] | None = ...,
        x802_1_tlvs: str | list[str] | None = ...,
        x802_3_tlvs: str | list[str] | None = ...,
        auto_isl: Literal["disable", "enable"] | None = ...,
        auto_isl_hello_timer: int | None = ...,
        auto_isl_receive_timeout: int | None = ...,
        auto_isl_port_group: int | None = ...,
        auto_mclag_icl: Literal["disable", "enable"] | None = ...,
        auto_isl_auth: Literal["legacy", "strict", "relax"] | None = ...,
        auto_isl_auth_user: str | None = ...,
        auto_isl_auth_identity: str | None = ...,
        auto_isl_auth_reauth: int | None = ...,
        auto_isl_auth_encrypt: Literal["none", "mixed", "must"] | None = ...,
        auto_isl_auth_macsec_profile: str | None = ...,
        med_network_policy: str | list[str] | list[LldpProfileMednetworkpolicyItem] | None = ...,
        med_location_service: str | list[str] | list[LldpProfileMedlocationserviceItem] | None = ...,
        custom_tlvs: str | list[str] | list[LldpProfileCustomtlvsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LldpProfileObject: ...

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
        payload_dict: LldpProfilePayload | None = ...,
        name: str | None = ...,
        med_tlvs: Literal["inventory-management", "network-policy", "power-management", "location-identification"] | list[str] | None = ...,
        x802_1_tlvs: Literal["port-vlan-id"] | list[str] | None = ...,
        x802_3_tlvs: Literal["max-frame-size", "power-negotiation"] | list[str] | None = ...,
        auto_isl: Literal["disable", "enable"] | None = ...,
        auto_isl_hello_timer: int | None = ...,
        auto_isl_receive_timeout: int | None = ...,
        auto_isl_port_group: int | None = ...,
        auto_mclag_icl: Literal["disable", "enable"] | None = ...,
        auto_isl_auth: Literal["legacy", "strict", "relax"] | None = ...,
        auto_isl_auth_user: str | None = ...,
        auto_isl_auth_identity: str | None = ...,
        auto_isl_auth_reauth: int | None = ...,
        auto_isl_auth_encrypt: Literal["none", "mixed", "must"] | None = ...,
        auto_isl_auth_macsec_profile: str | None = ...,
        med_network_policy: str | list[str] | list[LldpProfileMednetworkpolicyItem] | None = ...,
        med_location_service: str | list[str] | list[LldpProfileMedlocationserviceItem] | None = ...,
        custom_tlvs: str | list[str] | list[LldpProfileCustomtlvsItem] | None = ...,
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
    "LldpProfile",
    "LldpProfilePayload",
    "LldpProfileResponse",
    "LldpProfileObject",
]