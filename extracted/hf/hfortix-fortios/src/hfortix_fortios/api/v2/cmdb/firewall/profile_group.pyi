""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/profile_group
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

class ProfileGroupPayload(TypedDict, total=False):
    """Payload type for ProfileGroup operations."""
    name: str
    profile_protocol_options: str
    ssl_ssh_profile: str
    av_profile: str
    webfilter_profile: str
    dnsfilter_profile: str
    emailfilter_profile: str
    dlp_profile: str
    file_filter_profile: str
    ips_sensor: str
    application_list: str
    voip_profile: str
    ips_voip_filter: str
    sctp_filter_profile: str
    diameter_filter_profile: str
    virtual_patch_profile: str
    icap_profile: str
    videofilter_profile: str
    waf_profile: str
    ssh_filter_profile: str
    casb_profile: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileGroupResponse(TypedDict, total=False):
    """Response type for ProfileGroup - use with .dict property for typed dict access."""
    name: str
    profile_protocol_options: str
    ssl_ssh_profile: str
    av_profile: str
    webfilter_profile: str
    dnsfilter_profile: str
    emailfilter_profile: str
    dlp_profile: str
    file_filter_profile: str
    ips_sensor: str
    application_list: str
    voip_profile: str
    ips_voip_filter: str
    sctp_filter_profile: str
    diameter_filter_profile: str
    virtual_patch_profile: str
    icap_profile: str
    videofilter_profile: str
    waf_profile: str
    ssh_filter_profile: str
    casb_profile: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileGroupObject(FortiObject):
    """Typed FortiObject for ProfileGroup with field access."""
    name: str
    profile_protocol_options: str
    ssl_ssh_profile: str
    av_profile: str
    webfilter_profile: str
    dnsfilter_profile: str
    emailfilter_profile: str
    dlp_profile: str
    file_filter_profile: str
    ips_sensor: str
    application_list: str
    voip_profile: str
    ips_voip_filter: str
    sctp_filter_profile: str
    diameter_filter_profile: str
    virtual_patch_profile: str
    icap_profile: str
    videofilter_profile: str
    waf_profile: str
    ssh_filter_profile: str
    casb_profile: str


# ================================================================
# Main Endpoint Class
# ================================================================

class ProfileGroup:
    """
    
    Endpoint: firewall/profile_group
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
    ) -> ProfileGroupObject: ...
    
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
    ) -> FortiObjectList[ProfileGroupObject]: ...
    
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
        payload_dict: ProfileGroupPayload | None = ...,
        name: str | None = ...,
        profile_protocol_options: str | None = ...,
        ssl_ssh_profile: str | None = ...,
        av_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        dnsfilter_profile: str | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile: str | None = ...,
        file_filter_profile: str | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        voip_profile: str | None = ...,
        ips_voip_filter: str | None = ...,
        sctp_filter_profile: str | None = ...,
        diameter_filter_profile: str | None = ...,
        virtual_patch_profile: str | None = ...,
        icap_profile: str | None = ...,
        videofilter_profile: str | None = ...,
        waf_profile: str | None = ...,
        ssh_filter_profile: str | None = ...,
        casb_profile: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileGroupObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProfileGroupPayload | None = ...,
        name: str | None = ...,
        profile_protocol_options: str | None = ...,
        ssl_ssh_profile: str | None = ...,
        av_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        dnsfilter_profile: str | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile: str | None = ...,
        file_filter_profile: str | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        voip_profile: str | None = ...,
        ips_voip_filter: str | None = ...,
        sctp_filter_profile: str | None = ...,
        diameter_filter_profile: str | None = ...,
        virtual_patch_profile: str | None = ...,
        icap_profile: str | None = ...,
        videofilter_profile: str | None = ...,
        waf_profile: str | None = ...,
        ssh_filter_profile: str | None = ...,
        casb_profile: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileGroupObject: ...

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
        payload_dict: ProfileGroupPayload | None = ...,
        name: str | None = ...,
        profile_protocol_options: str | None = ...,
        ssl_ssh_profile: str | None = ...,
        av_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        dnsfilter_profile: str | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile: str | None = ...,
        file_filter_profile: str | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        voip_profile: str | None = ...,
        ips_voip_filter: str | None = ...,
        sctp_filter_profile: str | None = ...,
        diameter_filter_profile: str | None = ...,
        virtual_patch_profile: str | None = ...,
        icap_profile: str | None = ...,
        videofilter_profile: str | None = ...,
        waf_profile: str | None = ...,
        ssh_filter_profile: str | None = ...,
        casb_profile: str | None = ...,
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
    "ProfileGroup",
    "ProfileGroupPayload",
    "ProfileGroupResponse",
    "ProfileGroupObject",
]