""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: voip/profile
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

class ProfileSipDict(TypedDict, total=False):
    """Nested object type for sip field."""
    status: Literal["disable", "enable"]
    rtp: Literal["disable", "enable"]
    nat_port_range: str
    open_register_pinhole: Literal["disable", "enable"]
    open_contact_pinhole: Literal["disable", "enable"]
    strict_register: Literal["disable", "enable"]
    register_rate: int
    register_rate_track: Literal["none", "src-ip", "dest-ip"]
    invite_rate: int
    invite_rate_track: Literal["none", "src-ip", "dest-ip"]
    max_dialogs: int
    max_line_length: int
    block_long_lines: Literal["disable", "enable"]
    block_unknown: Literal["disable", "enable"]
    call_keepalive: int
    block_ack: Literal["disable", "enable"]
    block_bye: Literal["disable", "enable"]
    block_cancel: Literal["disable", "enable"]
    block_info: Literal["disable", "enable"]
    block_invite: Literal["disable", "enable"]
    block_message: Literal["disable", "enable"]
    block_notify: Literal["disable", "enable"]
    block_options: Literal["disable", "enable"]
    block_prack: Literal["disable", "enable"]
    block_publish: Literal["disable", "enable"]
    block_refer: Literal["disable", "enable"]
    block_register: Literal["disable", "enable"]
    block_subscribe: Literal["disable", "enable"]
    block_update: Literal["disable", "enable"]
    register_contact_trace: Literal["disable", "enable"]
    open_via_pinhole: Literal["disable", "enable"]
    open_record_route_pinhole: Literal["disable", "enable"]
    rfc2543_branch: Literal["disable", "enable"]
    log_violations: Literal["disable", "enable"]
    log_call_summary: Literal["disable", "enable"]
    nat_trace: Literal["disable", "enable"]
    subscribe_rate: int
    subscribe_rate_track: Literal["none", "src-ip", "dest-ip"]
    message_rate: int
    message_rate_track: Literal["none", "src-ip", "dest-ip"]
    notify_rate: int
    notify_rate_track: Literal["none", "src-ip", "dest-ip"]
    refer_rate: int
    refer_rate_track: Literal["none", "src-ip", "dest-ip"]
    update_rate: int
    update_rate_track: Literal["none", "src-ip", "dest-ip"]
    options_rate: int
    options_rate_track: Literal["none", "src-ip", "dest-ip"]
    ack_rate: int
    ack_rate_track: Literal["none", "src-ip", "dest-ip"]
    prack_rate: int
    prack_rate_track: Literal["none", "src-ip", "dest-ip"]
    info_rate: int
    info_rate_track: Literal["none", "src-ip", "dest-ip"]
    publish_rate: int
    publish_rate_track: Literal["none", "src-ip", "dest-ip"]
    bye_rate: int
    bye_rate_track: Literal["none", "src-ip", "dest-ip"]
    cancel_rate: int
    cancel_rate_track: Literal["none", "src-ip", "dest-ip"]
    preserve_override: Literal["disable", "enable"]
    no_sdp_fixup: Literal["disable", "enable"]
    contact_fixup: Literal["disable", "enable"]
    max_idle_dialogs: int
    block_geo_red_options: Literal["disable", "enable"]
    hosted_nat_traversal: Literal["disable", "enable"]
    hnt_restrict_source_ip: Literal["disable", "enable"]
    call_id_regex: str
    content_type_regex: str
    max_body_length: int
    unknown_header: Literal["discard", "pass", "respond"]
    malformed_request_line: Literal["discard", "pass", "respond"]
    malformed_header_via: Literal["discard", "pass", "respond"]
    malformed_header_from: Literal["discard", "pass", "respond"]
    malformed_header_to: Literal["discard", "pass", "respond"]
    malformed_header_call_id: Literal["discard", "pass", "respond"]
    malformed_header_cseq: Literal["discard", "pass", "respond"]
    malformed_header_rack: Literal["discard", "pass", "respond"]
    malformed_header_rseq: Literal["discard", "pass", "respond"]
    malformed_header_contact: Literal["discard", "pass", "respond"]
    malformed_header_record_route: Literal["discard", "pass", "respond"]
    malformed_header_route: Literal["discard", "pass", "respond"]
    malformed_header_expires: Literal["discard", "pass", "respond"]
    malformed_header_content_type: Literal["discard", "pass", "respond"]
    malformed_header_content_length: Literal["discard", "pass", "respond"]
    malformed_header_max_forwards: Literal["discard", "pass", "respond"]
    malformed_header_allow: Literal["discard", "pass", "respond"]
    malformed_header_p_asserted_identity: Literal["discard", "pass", "respond"]
    malformed_header_no_require: Literal["discard", "pass", "respond"]
    malformed_header_no_proxy_require: Literal["discard", "pass", "respond"]
    malformed_header_sdp_v: Literal["discard", "pass", "respond"]
    malformed_header_sdp_o: Literal["discard", "pass", "respond"]
    malformed_header_sdp_s: Literal["discard", "pass", "respond"]
    malformed_header_sdp_i: Literal["discard", "pass", "respond"]
    malformed_header_sdp_c: Literal["discard", "pass", "respond"]
    malformed_header_sdp_b: Literal["discard", "pass", "respond"]
    malformed_header_sdp_z: Literal["discard", "pass", "respond"]
    malformed_header_sdp_k: Literal["discard", "pass", "respond"]
    malformed_header_sdp_a: Literal["discard", "pass", "respond"]
    malformed_header_sdp_t: Literal["discard", "pass", "respond"]
    malformed_header_sdp_r: Literal["discard", "pass", "respond"]
    malformed_header_sdp_m: Literal["discard", "pass", "respond"]
    provisional_invite_expiry_time: int
    ips_rtp: Literal["disable", "enable"]
    ssl_mode: Literal["off", "full"]
    ssl_send_empty_frags: Literal["enable", "disable"]
    ssl_client_renegotiation: Literal["allow", "deny", "secure"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_pfs: Literal["require", "deny", "allow"]
    ssl_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_client_certificate: str
    ssl_server_certificate: str
    ssl_auth_client: str
    ssl_auth_server: str


class ProfileSccpDict(TypedDict, total=False):
    """Nested object type for sccp field."""
    status: Literal["disable", "enable"]
    block_mcast: Literal["disable", "enable"]
    verify_header: Literal["disable", "enable"]
    log_call_summary: Literal["disable", "enable"]
    log_violations: Literal["disable", "enable"]
    max_calls: int


class ProfileMsrpDict(TypedDict, total=False):
    """Nested object type for msrp field."""
    status: Literal["disable", "enable"]
    log_violations: Literal["disable", "enable"]
    max_msg_size: int
    max_msg_size_action: Literal["pass", "block", "reset", "monitor"]


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    feature_set: Literal["ips", "voipd"]
    comment: str
    sip: ProfileSipDict
    sccp: ProfileSccpDict
    msrp: ProfileMsrpDict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    feature_set: Literal["ips", "voipd"]
    comment: str
    sip: ProfileSipDict
    sccp: ProfileSccpDict
    msrp: ProfileMsrpDict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileSipObject(FortiObject):
    """Nested object for sip field with attribute access."""
    status: Literal["disable", "enable"]
    rtp: Literal["disable", "enable"]
    nat_port_range: str
    open_register_pinhole: Literal["disable", "enable"]
    open_contact_pinhole: Literal["disable", "enable"]
    strict_register: Literal["disable", "enable"]
    register_rate: int
    register_rate_track: Literal["none", "src-ip", "dest-ip"]
    invite_rate: int
    invite_rate_track: Literal["none", "src-ip", "dest-ip"]
    max_dialogs: int
    max_line_length: int
    block_long_lines: Literal["disable", "enable"]
    block_unknown: Literal["disable", "enable"]
    call_keepalive: int
    block_ack: Literal["disable", "enable"]
    block_bye: Literal["disable", "enable"]
    block_cancel: Literal["disable", "enable"]
    block_info: Literal["disable", "enable"]
    block_invite: Literal["disable", "enable"]
    block_message: Literal["disable", "enable"]
    block_notify: Literal["disable", "enable"]
    block_options: Literal["disable", "enable"]
    block_prack: Literal["disable", "enable"]
    block_publish: Literal["disable", "enable"]
    block_refer: Literal["disable", "enable"]
    block_register: Literal["disable", "enable"]
    block_subscribe: Literal["disable", "enable"]
    block_update: Literal["disable", "enable"]
    register_contact_trace: Literal["disable", "enable"]
    open_via_pinhole: Literal["disable", "enable"]
    open_record_route_pinhole: Literal["disable", "enable"]
    rfc2543_branch: Literal["disable", "enable"]
    log_violations: Literal["disable", "enable"]
    log_call_summary: Literal["disable", "enable"]
    nat_trace: Literal["disable", "enable"]
    subscribe_rate: int
    subscribe_rate_track: Literal["none", "src-ip", "dest-ip"]
    message_rate: int
    message_rate_track: Literal["none", "src-ip", "dest-ip"]
    notify_rate: int
    notify_rate_track: Literal["none", "src-ip", "dest-ip"]
    refer_rate: int
    refer_rate_track: Literal["none", "src-ip", "dest-ip"]
    update_rate: int
    update_rate_track: Literal["none", "src-ip", "dest-ip"]
    options_rate: int
    options_rate_track: Literal["none", "src-ip", "dest-ip"]
    ack_rate: int
    ack_rate_track: Literal["none", "src-ip", "dest-ip"]
    prack_rate: int
    prack_rate_track: Literal["none", "src-ip", "dest-ip"]
    info_rate: int
    info_rate_track: Literal["none", "src-ip", "dest-ip"]
    publish_rate: int
    publish_rate_track: Literal["none", "src-ip", "dest-ip"]
    bye_rate: int
    bye_rate_track: Literal["none", "src-ip", "dest-ip"]
    cancel_rate: int
    cancel_rate_track: Literal["none", "src-ip", "dest-ip"]
    preserve_override: Literal["disable", "enable"]
    no_sdp_fixup: Literal["disable", "enable"]
    contact_fixup: Literal["disable", "enable"]
    max_idle_dialogs: int
    block_geo_red_options: Literal["disable", "enable"]
    hosted_nat_traversal: Literal["disable", "enable"]
    hnt_restrict_source_ip: Literal["disable", "enable"]
    call_id_regex: str
    content_type_regex: str
    max_body_length: int
    unknown_header: Literal["discard", "pass", "respond"]
    malformed_request_line: Literal["discard", "pass", "respond"]
    malformed_header_via: Literal["discard", "pass", "respond"]
    malformed_header_from: Literal["discard", "pass", "respond"]
    malformed_header_to: Literal["discard", "pass", "respond"]
    malformed_header_call_id: Literal["discard", "pass", "respond"]
    malformed_header_cseq: Literal["discard", "pass", "respond"]
    malformed_header_rack: Literal["discard", "pass", "respond"]
    malformed_header_rseq: Literal["discard", "pass", "respond"]
    malformed_header_contact: Literal["discard", "pass", "respond"]
    malformed_header_record_route: Literal["discard", "pass", "respond"]
    malformed_header_route: Literal["discard", "pass", "respond"]
    malformed_header_expires: Literal["discard", "pass", "respond"]
    malformed_header_content_type: Literal["discard", "pass", "respond"]
    malformed_header_content_length: Literal["discard", "pass", "respond"]
    malformed_header_max_forwards: Literal["discard", "pass", "respond"]
    malformed_header_allow: Literal["discard", "pass", "respond"]
    malformed_header_p_asserted_identity: Literal["discard", "pass", "respond"]
    malformed_header_no_require: Literal["discard", "pass", "respond"]
    malformed_header_no_proxy_require: Literal["discard", "pass", "respond"]
    malformed_header_sdp_v: Literal["discard", "pass", "respond"]
    malformed_header_sdp_o: Literal["discard", "pass", "respond"]
    malformed_header_sdp_s: Literal["discard", "pass", "respond"]
    malformed_header_sdp_i: Literal["discard", "pass", "respond"]
    malformed_header_sdp_c: Literal["discard", "pass", "respond"]
    malformed_header_sdp_b: Literal["discard", "pass", "respond"]
    malformed_header_sdp_z: Literal["discard", "pass", "respond"]
    malformed_header_sdp_k: Literal["discard", "pass", "respond"]
    malformed_header_sdp_a: Literal["discard", "pass", "respond"]
    malformed_header_sdp_t: Literal["discard", "pass", "respond"]
    malformed_header_sdp_r: Literal["discard", "pass", "respond"]
    malformed_header_sdp_m: Literal["discard", "pass", "respond"]
    provisional_invite_expiry_time: int
    ips_rtp: Literal["disable", "enable"]
    ssl_mode: Literal["off", "full"]
    ssl_send_empty_frags: Literal["enable", "disable"]
    ssl_client_renegotiation: Literal["allow", "deny", "secure"]
    ssl_algorithm: Literal["high", "medium", "low"]
    ssl_pfs: Literal["require", "deny", "allow"]
    ssl_min_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_max_version: Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
    ssl_client_certificate: str
    ssl_server_certificate: str
    ssl_auth_client: str
    ssl_auth_server: str


class ProfileSccpObject(FortiObject):
    """Nested object for sccp field with attribute access."""
    status: Literal["disable", "enable"]
    block_mcast: Literal["disable", "enable"]
    verify_header: Literal["disable", "enable"]
    log_call_summary: Literal["disable", "enable"]
    log_violations: Literal["disable", "enable"]
    max_calls: int


class ProfileMsrpObject(FortiObject):
    """Nested object for msrp field with attribute access."""
    status: Literal["disable", "enable"]
    log_violations: Literal["disable", "enable"]
    max_msg_size: int
    max_msg_size_action: Literal["pass", "block", "reset", "monitor"]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    feature_set: Literal["ips", "voipd"]
    comment: str
    sip: ProfileSipObject
    sccp: ProfileSccpObject
    msrp: ProfileMsrpObject


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: voip/profile
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
        feature_set: Literal["ips", "voipd"] | None = ...,
        comment: str | None = ...,
        sip: ProfileSipDict | None = ...,
        sccp: ProfileSccpDict | None = ...,
        msrp: ProfileMsrpDict | None = ...,
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
        feature_set: Literal["ips", "voipd"] | None = ...,
        comment: str | None = ...,
        sip: ProfileSipDict | None = ...,
        sccp: ProfileSccpDict | None = ...,
        msrp: ProfileMsrpDict | None = ...,
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        feature_set: Literal["ips", "voipd"] | None = ...,
        comment: str | None = ...,
        sip: ProfileSipDict | None = ...,
        sccp: ProfileSccpDict | None = ...,
        msrp: ProfileMsrpDict | None = ...,
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