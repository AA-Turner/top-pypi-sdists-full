""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: icap/profile
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

class ProfileRespmodforwardrulesHeadergroupItem(TypedDict, total=False):
    """Nested item for respmod-forward-rules.header-group field."""
    id: int
    header_name: str
    header: str
    case_sensitivity: Literal["disable", "enable"]


class ProfileRespmodforwardrulesHttprespstatuscodeItem(TypedDict, total=False):
    """Nested item for respmod-forward-rules.http-resp-status-code field."""
    code: int


class ProfileIcapheadersItem(TypedDict, total=False):
    """Nested item for icap-headers field."""
    id: int
    name: str
    content: str
    base64_encoding: Literal["disable", "enable"]


class ProfileRespmodforwardrulesItem(TypedDict, total=False):
    """Nested item for respmod-forward-rules field."""
    name: str
    host: str
    header_group: str | list[str] | list[ProfileRespmodforwardrulesHeadergroupItem]
    action: Literal["forward", "bypass"]
    http_resp_status_code: str | list[str] | list[ProfileRespmodforwardrulesHttprespstatuscodeItem]


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    replacemsg_group: str
    name: str
    comment: str
    request: Literal["disable", "enable"]
    response: Literal["disable", "enable"]
    file_transfer: str | list[str]
    streaming_content_bypass: Literal["disable", "enable"]
    ocr_only: Literal["disable", "enable"]
    x204_size_limit: int
    x204_response: Literal["disable", "enable"]
    preview: Literal["disable", "enable"]
    preview_data_length: int
    request_server: str
    response_server: str
    file_transfer_server: str
    request_failure: Literal["error", "bypass"]
    response_failure: Literal["error", "bypass"]
    file_transfer_failure: Literal["error", "bypass"]
    request_path: str
    response_path: str
    file_transfer_path: str
    methods: str | list[str]
    response_req_hdr: Literal["disable", "enable"]
    respmod_default_action: Literal["forward", "bypass"]
    icap_block_log: Literal["disable", "enable"]
    chunk_encap: Literal["disable", "enable"]
    extension_feature: str | list[str]
    scan_progress_interval: int
    timeout: int
    icap_headers: str | list[str] | list[ProfileIcapheadersItem]
    respmod_forward_rules: str | list[str] | list[ProfileRespmodforwardrulesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    replacemsg_group: str
    name: str
    comment: str
    request: Literal["disable", "enable"]
    response: Literal["disable", "enable"]
    file_transfer: str
    streaming_content_bypass: Literal["disable", "enable"]
    ocr_only: Literal["disable", "enable"]
    x204_size_limit: int
    x204_response: Literal["disable", "enable"]
    preview: Literal["disable", "enable"]
    preview_data_length: int
    request_server: str
    response_server: str
    file_transfer_server: str
    request_failure: Literal["error", "bypass"]
    response_failure: Literal["error", "bypass"]
    file_transfer_failure: Literal["error", "bypass"]
    request_path: str
    response_path: str
    file_transfer_path: str
    methods: str
    response_req_hdr: Literal["disable", "enable"]
    respmod_default_action: Literal["forward", "bypass"]
    icap_block_log: Literal["disable", "enable"]
    chunk_encap: Literal["disable", "enable"]
    extension_feature: str
    scan_progress_interval: int
    timeout: int
    icap_headers: list[ProfileIcapheadersItem]
    respmod_forward_rules: list[ProfileRespmodforwardrulesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileRespmodforwardrulesHeadergroupItemObject(FortiObject[ProfileRespmodforwardrulesHeadergroupItem]):
    """Typed object for respmod-forward-rules.header-group table items with attribute access."""
    id: int
    header_name: str
    header: str
    case_sensitivity: Literal["disable", "enable"]


class ProfileRespmodforwardrulesHttprespstatuscodeItemObject(FortiObject[ProfileRespmodforwardrulesHttprespstatuscodeItem]):
    """Typed object for respmod-forward-rules.http-resp-status-code table items with attribute access."""
    code: int


class ProfileIcapheadersItemObject(FortiObject[ProfileIcapheadersItem]):
    """Typed object for icap-headers table items with attribute access."""
    id: int
    name: str
    content: str
    base64_encoding: Literal["disable", "enable"]


class ProfileRespmodforwardrulesItemObject(FortiObject[ProfileRespmodforwardrulesItem]):
    """Typed object for respmod-forward-rules table items with attribute access."""
    name: str
    host: str
    header_group: FortiObjectList[ProfileRespmodforwardrulesHeadergroupItemObject]
    action: Literal["forward", "bypass"]
    http_resp_status_code: FortiObjectList[ProfileRespmodforwardrulesHttprespstatuscodeItemObject]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    replacemsg_group: str
    name: str
    comment: str
    request: Literal["disable", "enable"]
    response: Literal["disable", "enable"]
    file_transfer: str
    streaming_content_bypass: Literal["disable", "enable"]
    ocr_only: Literal["disable", "enable"]
    x204_size_limit: int
    x204_response: Literal["disable", "enable"]
    preview: Literal["disable", "enable"]
    preview_data_length: int
    request_server: str
    response_server: str
    file_transfer_server: str
    request_failure: Literal["error", "bypass"]
    response_failure: Literal["error", "bypass"]
    file_transfer_failure: Literal["error", "bypass"]
    request_path: str
    response_path: str
    file_transfer_path: str
    methods: str
    response_req_hdr: Literal["disable", "enable"]
    respmod_default_action: Literal["forward", "bypass"]
    icap_block_log: Literal["disable", "enable"]
    chunk_encap: Literal["disable", "enable"]
    extension_feature: str
    scan_progress_interval: int
    timeout: int
    icap_headers: FortiObjectList[ProfileIcapheadersItemObject]
    respmod_forward_rules: FortiObjectList[ProfileRespmodforwardrulesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: icap/profile
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
        replacemsg_group: str | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        request: Literal["disable", "enable"] | None = ...,
        response: Literal["disable", "enable"] | None = ...,
        file_transfer: str | list[str] | None = ...,
        streaming_content_bypass: Literal["disable", "enable"] | None = ...,
        ocr_only: Literal["disable", "enable"] | None = ...,
        x204_size_limit: int | None = ...,
        x204_response: Literal["disable", "enable"] | None = ...,
        preview: Literal["disable", "enable"] | None = ...,
        preview_data_length: int | None = ...,
        request_server: str | None = ...,
        response_server: str | None = ...,
        file_transfer_server: str | None = ...,
        request_failure: Literal["error", "bypass"] | None = ...,
        response_failure: Literal["error", "bypass"] | None = ...,
        file_transfer_failure: Literal["error", "bypass"] | None = ...,
        request_path: str | None = ...,
        response_path: str | None = ...,
        file_transfer_path: str | None = ...,
        methods: str | list[str] | None = ...,
        response_req_hdr: Literal["disable", "enable"] | None = ...,
        respmod_default_action: Literal["forward", "bypass"] | None = ...,
        icap_block_log: Literal["disable", "enable"] | None = ...,
        chunk_encap: Literal["disable", "enable"] | None = ...,
        extension_feature: str | list[str] | None = ...,
        scan_progress_interval: int | None = ...,
        timeout: int | None = ...,
        icap_headers: str | list[str] | list[ProfileIcapheadersItem] | None = ...,
        respmod_forward_rules: str | list[str] | list[ProfileRespmodforwardrulesItem] | None = ...,
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
        replacemsg_group: str | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        request: Literal["disable", "enable"] | None = ...,
        response: Literal["disable", "enable"] | None = ...,
        file_transfer: str | list[str] | None = ...,
        streaming_content_bypass: Literal["disable", "enable"] | None = ...,
        ocr_only: Literal["disable", "enable"] | None = ...,
        x204_size_limit: int | None = ...,
        x204_response: Literal["disable", "enable"] | None = ...,
        preview: Literal["disable", "enable"] | None = ...,
        preview_data_length: int | None = ...,
        request_server: str | None = ...,
        response_server: str | None = ...,
        file_transfer_server: str | None = ...,
        request_failure: Literal["error", "bypass"] | None = ...,
        response_failure: Literal["error", "bypass"] | None = ...,
        file_transfer_failure: Literal["error", "bypass"] | None = ...,
        request_path: str | None = ...,
        response_path: str | None = ...,
        file_transfer_path: str | None = ...,
        methods: str | list[str] | None = ...,
        response_req_hdr: Literal["disable", "enable"] | None = ...,
        respmod_default_action: Literal["forward", "bypass"] | None = ...,
        icap_block_log: Literal["disable", "enable"] | None = ...,
        chunk_encap: Literal["disable", "enable"] | None = ...,
        extension_feature: str | list[str] | None = ...,
        scan_progress_interval: int | None = ...,
        timeout: int | None = ...,
        icap_headers: str | list[str] | list[ProfileIcapheadersItem] | None = ...,
        respmod_forward_rules: str | list[str] | list[ProfileRespmodforwardrulesItem] | None = ...,
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
        replacemsg_group: str | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        request: Literal["disable", "enable"] | None = ...,
        response: Literal["disable", "enable"] | None = ...,
        file_transfer: Literal["ssh", "ftp"] | list[str] | None = ...,
        streaming_content_bypass: Literal["disable", "enable"] | None = ...,
        ocr_only: Literal["disable", "enable"] | None = ...,
        x204_size_limit: int | None = ...,
        x204_response: Literal["disable", "enable"] | None = ...,
        preview: Literal["disable", "enable"] | None = ...,
        preview_data_length: int | None = ...,
        request_server: str | None = ...,
        response_server: str | None = ...,
        file_transfer_server: str | None = ...,
        request_failure: Literal["error", "bypass"] | None = ...,
        response_failure: Literal["error", "bypass"] | None = ...,
        file_transfer_failure: Literal["error", "bypass"] | None = ...,
        request_path: str | None = ...,
        response_path: str | None = ...,
        file_transfer_path: str | None = ...,
        methods: Literal["delete", "get", "head", "options", "post", "put", "trace", "connect", "other"] | list[str] | None = ...,
        response_req_hdr: Literal["disable", "enable"] | None = ...,
        respmod_default_action: Literal["forward", "bypass"] | None = ...,
        icap_block_log: Literal["disable", "enable"] | None = ...,
        chunk_encap: Literal["disable", "enable"] | None = ...,
        extension_feature: Literal["scan-progress"] | list[str] | None = ...,
        scan_progress_interval: int | None = ...,
        timeout: int | None = ...,
        icap_headers: str | list[str] | list[ProfileIcapheadersItem] | None = ...,
        respmod_forward_rules: str | list[str] | list[ProfileRespmodforwardrulesItem] | None = ...,
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