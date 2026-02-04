""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/accprofile
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

class AccprofileNetgrppermissionDict(TypedDict, total=False):
    """Nested object type for netgrp-permission field."""
    cfg: Literal["none", "read", "read-write"]
    packet_capture: Literal["none", "read", "read-write"]
    route_cfg: Literal["none", "read", "read-write"]


class AccprofileSysgrppermissionDict(TypedDict, total=False):
    """Nested object type for sysgrp-permission field."""
    admin: Literal["none", "read", "read-write"]
    upd: Literal["none", "read", "read-write"]
    cfg: Literal["none", "read", "read-write"]
    mnt: Literal["none", "read", "read-write"]


class AccprofileFwgrppermissionDict(TypedDict, total=False):
    """Nested object type for fwgrp-permission field."""
    policy: Literal["none", "read", "read-write"]
    address: Literal["none", "read", "read-write"]
    service: Literal["none", "read", "read-write"]
    schedule: Literal["none", "read", "read-write"]
    others: Literal["none", "read", "read-write"]


class AccprofileLoggrppermissionDict(TypedDict, total=False):
    """Nested object type for loggrp-permission field."""
    config: Literal["none", "read", "read-write"]
    data_access: Literal["none", "read", "read-write"]
    report_access: Literal["none", "read", "read-write"]
    threat_weight: Literal["none", "read", "read-write"]


class AccprofileUtmgrppermissionDict(TypedDict, total=False):
    """Nested object type for utmgrp-permission field."""
    antivirus: Literal["none", "read", "read-write"]
    ips: Literal["none", "read", "read-write"]
    webfilter: Literal["none", "read", "read-write"]
    emailfilter: Literal["none", "read", "read-write"]
    dlp: Literal["none", "read", "read-write"]
    file_filter: Literal["none", "read", "read-write"]
    application_control: Literal["none", "read", "read-write"]
    icap: Literal["none", "read", "read-write"]
    voip: Literal["none", "read", "read-write"]
    waf: Literal["none", "read", "read-write"]
    dnsfilter: Literal["none", "read", "read-write"]
    endpoint_control: Literal["none", "read", "read-write"]
    videofilter: Literal["none", "read", "read-write"]
    virtual_patch: Literal["none", "read", "read-write"]
    casb: Literal["none", "read", "read-write"]
    telemetry: Literal["none", "read", "read-write"]


class AccprofileSecfabgrppermissionDict(TypedDict, total=False):
    """Nested object type for secfabgrp-permission field."""
    csfsys: Literal["none", "read", "read-write"]
    csffoo: Literal["none", "read", "read-write"]


class AccprofilePayload(TypedDict, total=False):
    """Payload type for Accprofile operations."""
    name: str
    scope: Literal["vdom", "global"]
    comments: str
    secfabgrp: Literal["none", "read", "read-write", "custom"]
    ftviewgrp: Literal["none", "read", "read-write"]
    authgrp: Literal["none", "read", "read-write"]
    sysgrp: Literal["none", "read", "read-write", "custom"]
    netgrp: Literal["none", "read", "read-write", "custom"]
    loggrp: Literal["none", "read", "read-write", "custom"]
    fwgrp: Literal["none", "read", "read-write", "custom"]
    vpngrp: Literal["none", "read", "read-write"]
    utmgrp: Literal["none", "read", "read-write", "custom"]
    wanoptgrp: Literal["none", "read", "read-write"]
    wifi: Literal["none", "read", "read-write"]
    netgrp_permission: AccprofileNetgrppermissionDict
    sysgrp_permission: AccprofileSysgrppermissionDict
    fwgrp_permission: AccprofileFwgrppermissionDict
    loggrp_permission: AccprofileLoggrppermissionDict
    utmgrp_permission: AccprofileUtmgrppermissionDict
    secfabgrp_permission: AccprofileSecfabgrppermissionDict
    admintimeout_override: Literal["enable", "disable"]
    admintimeout: int
    cli_diagnose: Literal["enable", "disable"]
    cli_get: Literal["enable", "disable"]
    cli_show: Literal["enable", "disable"]
    cli_exec: Literal["enable", "disable"]
    cli_config: Literal["enable", "disable"]
    system_execute_ssh: Literal["enable", "disable"]
    system_execute_telnet: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AccprofileResponse(TypedDict, total=False):
    """Response type for Accprofile - use with .dict property for typed dict access."""
    name: str
    scope: Literal["vdom", "global"]
    comments: str
    secfabgrp: Literal["none", "read", "read-write", "custom"]
    ftviewgrp: Literal["none", "read", "read-write"]
    authgrp: Literal["none", "read", "read-write"]
    sysgrp: Literal["none", "read", "read-write", "custom"]
    netgrp: Literal["none", "read", "read-write", "custom"]
    loggrp: Literal["none", "read", "read-write", "custom"]
    fwgrp: Literal["none", "read", "read-write", "custom"]
    vpngrp: Literal["none", "read", "read-write"]
    utmgrp: Literal["none", "read", "read-write", "custom"]
    wanoptgrp: Literal["none", "read", "read-write"]
    wifi: Literal["none", "read", "read-write"]
    netgrp_permission: AccprofileNetgrppermissionDict
    sysgrp_permission: AccprofileSysgrppermissionDict
    fwgrp_permission: AccprofileFwgrppermissionDict
    loggrp_permission: AccprofileLoggrppermissionDict
    utmgrp_permission: AccprofileUtmgrppermissionDict
    secfabgrp_permission: AccprofileSecfabgrppermissionDict
    admintimeout_override: Literal["enable", "disable"]
    admintimeout: int
    cli_diagnose: Literal["enable", "disable"]
    cli_get: Literal["enable", "disable"]
    cli_show: Literal["enable", "disable"]
    cli_exec: Literal["enable", "disable"]
    cli_config: Literal["enable", "disable"]
    system_execute_ssh: Literal["enable", "disable"]
    system_execute_telnet: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AccprofileNetgrppermissionObject(FortiObject):
    """Nested object for netgrp-permission field with attribute access."""
    cfg: Literal["none", "read", "read-write"]
    packet_capture: Literal["none", "read", "read-write"]
    route_cfg: Literal["none", "read", "read-write"]


class AccprofileSysgrppermissionObject(FortiObject):
    """Nested object for sysgrp-permission field with attribute access."""
    admin: Literal["none", "read", "read-write"]
    upd: Literal["none", "read", "read-write"]
    cfg: Literal["none", "read", "read-write"]
    mnt: Literal["none", "read", "read-write"]


class AccprofileFwgrppermissionObject(FortiObject):
    """Nested object for fwgrp-permission field with attribute access."""
    policy: Literal["none", "read", "read-write"]
    address: Literal["none", "read", "read-write"]
    service: Literal["none", "read", "read-write"]
    schedule: Literal["none", "read", "read-write"]
    others: Literal["none", "read", "read-write"]


class AccprofileLoggrppermissionObject(FortiObject):
    """Nested object for loggrp-permission field with attribute access."""
    config: Literal["none", "read", "read-write"]
    data_access: Literal["none", "read", "read-write"]
    report_access: Literal["none", "read", "read-write"]
    threat_weight: Literal["none", "read", "read-write"]


class AccprofileUtmgrppermissionObject(FortiObject):
    """Nested object for utmgrp-permission field with attribute access."""
    antivirus: Literal["none", "read", "read-write"]
    ips: Literal["none", "read", "read-write"]
    webfilter: Literal["none", "read", "read-write"]
    emailfilter: Literal["none", "read", "read-write"]
    dlp: Literal["none", "read", "read-write"]
    file_filter: Literal["none", "read", "read-write"]
    application_control: Literal["none", "read", "read-write"]
    icap: Literal["none", "read", "read-write"]
    voip: Literal["none", "read", "read-write"]
    waf: Literal["none", "read", "read-write"]
    dnsfilter: Literal["none", "read", "read-write"]
    endpoint_control: Literal["none", "read", "read-write"]
    videofilter: Literal["none", "read", "read-write"]
    virtual_patch: Literal["none", "read", "read-write"]
    casb: Literal["none", "read", "read-write"]
    telemetry: Literal["none", "read", "read-write"]


class AccprofileSecfabgrppermissionObject(FortiObject):
    """Nested object for secfabgrp-permission field with attribute access."""
    csfsys: Literal["none", "read", "read-write"]
    csffoo: Literal["none", "read", "read-write"]


class AccprofileObject(FortiObject):
    """Typed FortiObject for Accprofile with field access."""
    name: str
    scope: Literal["vdom", "global"]
    comments: str
    secfabgrp: Literal["none", "read", "read-write", "custom"]
    ftviewgrp: Literal["none", "read", "read-write"]
    authgrp: Literal["none", "read", "read-write"]
    sysgrp: Literal["none", "read", "read-write", "custom"]
    netgrp: Literal["none", "read", "read-write", "custom"]
    loggrp: Literal["none", "read", "read-write", "custom"]
    fwgrp: Literal["none", "read", "read-write", "custom"]
    vpngrp: Literal["none", "read", "read-write"]
    utmgrp: Literal["none", "read", "read-write", "custom"]
    wanoptgrp: Literal["none", "read", "read-write"]
    wifi: Literal["none", "read", "read-write"]
    netgrp_permission: AccprofileNetgrppermissionObject
    sysgrp_permission: AccprofileSysgrppermissionObject
    fwgrp_permission: AccprofileFwgrppermissionObject
    loggrp_permission: AccprofileLoggrppermissionObject
    utmgrp_permission: AccprofileUtmgrppermissionObject
    secfabgrp_permission: AccprofileSecfabgrppermissionObject
    admintimeout_override: Literal["enable", "disable"]
    admintimeout: int
    cli_diagnose: Literal["enable", "disable"]
    cli_get: Literal["enable", "disable"]
    cli_show: Literal["enable", "disable"]
    cli_exec: Literal["enable", "disable"]
    cli_config: Literal["enable", "disable"]
    system_execute_ssh: Literal["enable", "disable"]
    system_execute_telnet: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Accprofile:
    """
    
    Endpoint: system/accprofile
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccprofileObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[AccprofileObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: AccprofilePayload | None = ...,
        name: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        comments: str | None = ...,
        secfabgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        ftviewgrp: Literal["none", "read", "read-write"] | None = ...,
        authgrp: Literal["none", "read", "read-write"] | None = ...,
        sysgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        netgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        loggrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        fwgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        vpngrp: Literal["none", "read", "read-write"] | None = ...,
        utmgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        wanoptgrp: Literal["none", "read", "read-write"] | None = ...,
        wifi: Literal["none", "read", "read-write"] | None = ...,
        netgrp_permission: AccprofileNetgrppermissionDict | None = ...,
        sysgrp_permission: AccprofileSysgrppermissionDict | None = ...,
        fwgrp_permission: AccprofileFwgrppermissionDict | None = ...,
        loggrp_permission: AccprofileLoggrppermissionDict | None = ...,
        utmgrp_permission: AccprofileUtmgrppermissionDict | None = ...,
        secfabgrp_permission: AccprofileSecfabgrppermissionDict | None = ...,
        admintimeout_override: Literal["enable", "disable"] | None = ...,
        admintimeout: int | None = ...,
        cli_diagnose: Literal["enable", "disable"] | None = ...,
        cli_get: Literal["enable", "disable"] | None = ...,
        cli_show: Literal["enable", "disable"] | None = ...,
        cli_exec: Literal["enable", "disable"] | None = ...,
        cli_config: Literal["enable", "disable"] | None = ...,
        system_execute_ssh: Literal["enable", "disable"] | None = ...,
        system_execute_telnet: Literal["enable", "disable"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccprofileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AccprofilePayload | None = ...,
        name: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        comments: str | None = ...,
        secfabgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        ftviewgrp: Literal["none", "read", "read-write"] | None = ...,
        authgrp: Literal["none", "read", "read-write"] | None = ...,
        sysgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        netgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        loggrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        fwgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        vpngrp: Literal["none", "read", "read-write"] | None = ...,
        utmgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        wanoptgrp: Literal["none", "read", "read-write"] | None = ...,
        wifi: Literal["none", "read", "read-write"] | None = ...,
        netgrp_permission: AccprofileNetgrppermissionDict | None = ...,
        sysgrp_permission: AccprofileSysgrppermissionDict | None = ...,
        fwgrp_permission: AccprofileFwgrppermissionDict | None = ...,
        loggrp_permission: AccprofileLoggrppermissionDict | None = ...,
        utmgrp_permission: AccprofileUtmgrppermissionDict | None = ...,
        secfabgrp_permission: AccprofileSecfabgrppermissionDict | None = ...,
        admintimeout_override: Literal["enable", "disable"] | None = ...,
        admintimeout: int | None = ...,
        cli_diagnose: Literal["enable", "disable"] | None = ...,
        cli_get: Literal["enable", "disable"] | None = ...,
        cli_show: Literal["enable", "disable"] | None = ...,
        cli_exec: Literal["enable", "disable"] | None = ...,
        cli_config: Literal["enable", "disable"] | None = ...,
        system_execute_ssh: Literal["enable", "disable"] | None = ...,
        system_execute_telnet: Literal["enable", "disable"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccprofileObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
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
        payload_dict: AccprofilePayload | None = ...,
        name: str | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        comments: str | None = ...,
        secfabgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        ftviewgrp: Literal["none", "read", "read-write"] | None = ...,
        authgrp: Literal["none", "read", "read-write"] | None = ...,
        sysgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        netgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        loggrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        fwgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        vpngrp: Literal["none", "read", "read-write"] | None = ...,
        utmgrp: Literal["none", "read", "read-write", "custom"] | None = ...,
        wanoptgrp: Literal["none", "read", "read-write"] | None = ...,
        wifi: Literal["none", "read", "read-write"] | None = ...,
        netgrp_permission: AccprofileNetgrppermissionDict | None = ...,
        sysgrp_permission: AccprofileSysgrppermissionDict | None = ...,
        fwgrp_permission: AccprofileFwgrppermissionDict | None = ...,
        loggrp_permission: AccprofileLoggrppermissionDict | None = ...,
        utmgrp_permission: AccprofileUtmgrppermissionDict | None = ...,
        secfabgrp_permission: AccprofileSecfabgrppermissionDict | None = ...,
        admintimeout_override: Literal["enable", "disable"] | None = ...,
        admintimeout: int | None = ...,
        cli_diagnose: Literal["enable", "disable"] | None = ...,
        cli_get: Literal["enable", "disable"] | None = ...,
        cli_show: Literal["enable", "disable"] | None = ...,
        cli_exec: Literal["enable", "disable"] | None = ...,
        cli_config: Literal["enable", "disable"] | None = ...,
        system_execute_ssh: Literal["enable", "disable"] | None = ...,
        system_execute_telnet: Literal["enable", "disable"] | None = ...,
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
    "Accprofile",
    "AccprofilePayload",
    "AccprofileResponse",
    "AccprofileObject",
]