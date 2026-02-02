""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: endpoint_control/fctems_override
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

class FctemsOverridePayload(TypedDict, total=False):
    """Payload type for FctemsOverride operations."""
    ems_id: int
    status: Literal["enable", "disable"]
    name: str
    dirty_reason: Literal["none", "mismatched-ems-sn"]
    fortinetone_cloud_authentication: Literal["enable", "disable"]
    cloud_authentication_access_key: str
    server: str
    https_port: int
    serial_number: str
    tenant_id: str
    source_ip: str
    pull_sysinfo: Literal["enable", "disable"]
    pull_vulnerabilities: Literal["enable", "disable"]
    pull_tags: Literal["enable", "disable"]
    pull_malware_hash: Literal["enable", "disable"]
    capabilities: str | list[str]
    call_timeout: int
    out_of_sync_threshold: int
    send_tags_to_all_vdoms: Literal["enable", "disable"]
    websocket_override: Literal["enable", "disable"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    trust_ca_cn: Literal["enable", "disable"]
    verifying_ca: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FctemsOverrideResponse(TypedDict, total=False):
    """Response type for FctemsOverride - use with .dict property for typed dict access."""
    ems_id: int
    status: Literal["enable", "disable"]
    name: str
    dirty_reason: Literal["none", "mismatched-ems-sn"]
    fortinetone_cloud_authentication: Literal["enable", "disable"]
    cloud_authentication_access_key: str
    server: str
    https_port: int
    serial_number: str
    tenant_id: str
    source_ip: str
    pull_sysinfo: Literal["enable", "disable"]
    pull_vulnerabilities: Literal["enable", "disable"]
    pull_tags: Literal["enable", "disable"]
    pull_malware_hash: Literal["enable", "disable"]
    capabilities: str
    call_timeout: int
    out_of_sync_threshold: int
    send_tags_to_all_vdoms: Literal["enable", "disable"]
    websocket_override: Literal["enable", "disable"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    trust_ca_cn: Literal["enable", "disable"]
    verifying_ca: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FctemsOverrideObject(FortiObject):
    """Typed FortiObject for FctemsOverride with field access."""
    ems_id: int
    status: Literal["enable", "disable"]
    name: str
    dirty_reason: Literal["none", "mismatched-ems-sn"]
    fortinetone_cloud_authentication: Literal["enable", "disable"]
    cloud_authentication_access_key: str
    server: str
    https_port: int
    serial_number: str
    tenant_id: str
    source_ip: str
    pull_sysinfo: Literal["enable", "disable"]
    pull_vulnerabilities: Literal["enable", "disable"]
    pull_tags: Literal["enable", "disable"]
    pull_malware_hash: Literal["enable", "disable"]
    capabilities: str
    call_timeout: int
    out_of_sync_threshold: int
    send_tags_to_all_vdoms: Literal["enable", "disable"]
    websocket_override: Literal["enable", "disable"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    trust_ca_cn: Literal["enable", "disable"]
    verifying_ca: str


# ================================================================
# Main Endpoint Class
# ================================================================

class FctemsOverride:
    """
    
    Endpoint: endpoint_control/fctems_override
    Category: cmdb
    MKey: ems-id
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
        ems_id: int,
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
    ) -> FctemsOverrideObject: ...
    
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
    ) -> FortiObjectList[FctemsOverrideObject]: ...
    
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
        payload_dict: FctemsOverridePayload | None = ...,
        ems_id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        dirty_reason: Literal["none", "mismatched-ems-sn"] | None = ...,
        fortinetone_cloud_authentication: Literal["enable", "disable"] | None = ...,
        cloud_authentication_access_key: str | None = ...,
        server: str | None = ...,
        https_port: int | None = ...,
        serial_number: str | None = ...,
        tenant_id: str | None = ...,
        source_ip: str | None = ...,
        pull_sysinfo: Literal["enable", "disable"] | None = ...,
        pull_vulnerabilities: Literal["enable", "disable"] | None = ...,
        pull_tags: Literal["enable", "disable"] | None = ...,
        pull_malware_hash: Literal["enable", "disable"] | None = ...,
        capabilities: str | list[str] | None = ...,
        call_timeout: int | None = ...,
        out_of_sync_threshold: int | None = ...,
        send_tags_to_all_vdoms: Literal["enable", "disable"] | None = ...,
        websocket_override: Literal["enable", "disable"] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        trust_ca_cn: Literal["enable", "disable"] | None = ...,
        verifying_ca: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FctemsOverrideObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FctemsOverridePayload | None = ...,
        ems_id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        dirty_reason: Literal["none", "mismatched-ems-sn"] | None = ...,
        fortinetone_cloud_authentication: Literal["enable", "disable"] | None = ...,
        cloud_authentication_access_key: str | None = ...,
        server: str | None = ...,
        https_port: int | None = ...,
        serial_number: str | None = ...,
        tenant_id: str | None = ...,
        source_ip: str | None = ...,
        pull_sysinfo: Literal["enable", "disable"] | None = ...,
        pull_vulnerabilities: Literal["enable", "disable"] | None = ...,
        pull_tags: Literal["enable", "disable"] | None = ...,
        pull_malware_hash: Literal["enable", "disable"] | None = ...,
        capabilities: str | list[str] | None = ...,
        call_timeout: int | None = ...,
        out_of_sync_threshold: int | None = ...,
        send_tags_to_all_vdoms: Literal["enable", "disable"] | None = ...,
        websocket_override: Literal["enable", "disable"] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        trust_ca_cn: Literal["enable", "disable"] | None = ...,
        verifying_ca: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FctemsOverrideObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        ems_id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        ems_id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FctemsOverridePayload | None = ...,
        ems_id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        dirty_reason: Literal["none", "mismatched-ems-sn"] | None = ...,
        fortinetone_cloud_authentication: Literal["enable", "disable"] | None = ...,
        cloud_authentication_access_key: str | None = ...,
        server: str | None = ...,
        https_port: int | None = ...,
        serial_number: str | None = ...,
        tenant_id: str | None = ...,
        source_ip: str | None = ...,
        pull_sysinfo: Literal["enable", "disable"] | None = ...,
        pull_vulnerabilities: Literal["enable", "disable"] | None = ...,
        pull_tags: Literal["enable", "disable"] | None = ...,
        pull_malware_hash: Literal["enable", "disable"] | None = ...,
        capabilities: Literal["fabric-auth", "silent-approval", "websocket", "websocket-malware", "push-ca-certs", "common-tags-api", "tenant-id", "client-avatars", "single-vdom-connector", "fgt-sysinfo-api", "ztna-server-info", "used-tags"] | list[str] | None = ...,
        call_timeout: int | None = ...,
        out_of_sync_threshold: int | None = ...,
        send_tags_to_all_vdoms: Literal["enable", "disable"] | None = ...,
        websocket_override: Literal["enable", "disable"] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        trust_ca_cn: Literal["enable", "disable"] | None = ...,
        verifying_ca: str | None = ...,
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
    "FctemsOverride",
    "FctemsOverridePayload",
    "FctemsOverrideResponse",
    "FctemsOverrideObject",
]