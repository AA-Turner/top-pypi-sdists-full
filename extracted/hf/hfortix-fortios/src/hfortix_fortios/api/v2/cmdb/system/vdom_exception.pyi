""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/vdom_exception
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

class VdomExceptionVdomItem(TypedDict, total=False):
    """Nested item for vdom field."""
    name: str


class VdomExceptionPayload(TypedDict, total=False):
    """Payload type for VdomException operations."""
    id: int
    object: Literal["log.fortianalyzer.setting", "log.fortianalyzer.override-setting", "log.fortianalyzer2.setting", "log.fortianalyzer2.override-setting", "log.fortianalyzer3.setting", "log.fortianalyzer3.override-setting", "log.fortianalyzer-cloud.setting", "log.fortianalyzer-cloud.override-setting", "log.syslogd.setting", "log.syslogd.override-setting", "log.syslogd2.setting", "log.syslogd2.override-setting", "log.syslogd3.setting", "log.syslogd3.override-setting", "log.syslogd4.setting", "log.syslogd4.override-setting", "system.gre-tunnel", "system.central-management", "system.csf", "user.radius", "system.interface", "vpn.ipsec.phase1-interface", "vpn.ipsec.phase2-interface", "router.bgp", "router.route-map", "router.prefix-list", "firewall.ippool", "firewall.ippool6", "router.static", "router.static6", "firewall.vip", "firewall.vip6", "system.sdwan", "system.saml", "router.policy", "router.policy6", "log.syslogd.setting", "log.syslogd.override-setting", "firewall.address"]
    scope: Literal["all", "inclusive", "exclusive"]
    vdom: str | list[str] | list[VdomExceptionVdomItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VdomExceptionResponse(TypedDict, total=False):
    """Response type for VdomException - use with .dict property for typed dict access."""
    id: int
    object: Literal["log.fortianalyzer.setting", "log.fortianalyzer.override-setting", "log.fortianalyzer2.setting", "log.fortianalyzer2.override-setting", "log.fortianalyzer3.setting", "log.fortianalyzer3.override-setting", "log.fortianalyzer-cloud.setting", "log.fortianalyzer-cloud.override-setting", "log.syslogd.setting", "log.syslogd.override-setting", "log.syslogd2.setting", "log.syslogd2.override-setting", "log.syslogd3.setting", "log.syslogd3.override-setting", "log.syslogd4.setting", "log.syslogd4.override-setting", "system.gre-tunnel", "system.central-management", "system.csf", "user.radius", "system.interface", "vpn.ipsec.phase1-interface", "vpn.ipsec.phase2-interface", "router.bgp", "router.route-map", "router.prefix-list", "firewall.ippool", "firewall.ippool6", "router.static", "router.static6", "firewall.vip", "firewall.vip6", "system.sdwan", "system.saml", "router.policy", "router.policy6", "log.syslogd.setting", "log.syslogd.override-setting", "firewall.address"]
    scope: Literal["all", "inclusive", "exclusive"]
    vdom: list[VdomExceptionVdomItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VdomExceptionVdomItemObject(FortiObject[VdomExceptionVdomItem]):
    """Typed object for vdom table items with attribute access."""
    name: str


class VdomExceptionObject(FortiObject):
    """Typed FortiObject for VdomException with field access."""
    id: int
    object: Literal["log.fortianalyzer.setting", "log.fortianalyzer.override-setting", "log.fortianalyzer2.setting", "log.fortianalyzer2.override-setting", "log.fortianalyzer3.setting", "log.fortianalyzer3.override-setting", "log.fortianalyzer-cloud.setting", "log.fortianalyzer-cloud.override-setting", "log.syslogd.setting", "log.syslogd.override-setting", "log.syslogd2.setting", "log.syslogd2.override-setting", "log.syslogd3.setting", "log.syslogd3.override-setting", "log.syslogd4.setting", "log.syslogd4.override-setting", "system.gre-tunnel", "system.central-management", "system.csf", "user.radius", "system.interface", "vpn.ipsec.phase1-interface", "vpn.ipsec.phase2-interface", "router.bgp", "router.route-map", "router.prefix-list", "firewall.ippool", "firewall.ippool6", "router.static", "router.static6", "firewall.vip", "firewall.vip6", "system.sdwan", "system.saml", "router.policy", "router.policy6", "log.syslogd.setting", "log.syslogd.override-setting", "firewall.address"]
    scope: Literal["all", "inclusive", "exclusive"]


# ================================================================
# Main Endpoint Class
# ================================================================

class VdomException:
    """
    
    Endpoint: system/vdom_exception
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> VdomExceptionObject: ...
    
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
    ) -> FortiObjectList[VdomExceptionObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: VdomExceptionPayload | None = ...,
        id: int | None = ...,
        object: Literal["log.fortianalyzer.setting", "log.fortianalyzer.override-setting", "log.fortianalyzer2.setting", "log.fortianalyzer2.override-setting", "log.fortianalyzer3.setting", "log.fortianalyzer3.override-setting", "log.fortianalyzer-cloud.setting", "log.fortianalyzer-cloud.override-setting", "log.syslogd.setting", "log.syslogd.override-setting", "log.syslogd2.setting", "log.syslogd2.override-setting", "log.syslogd3.setting", "log.syslogd3.override-setting", "log.syslogd4.setting", "log.syslogd4.override-setting", "system.gre-tunnel", "system.central-management", "system.csf", "user.radius", "system.interface", "vpn.ipsec.phase1-interface", "vpn.ipsec.phase2-interface", "router.bgp", "router.route-map", "router.prefix-list", "firewall.ippool", "firewall.ippool6", "router.static", "router.static6", "firewall.vip", "firewall.vip6", "system.sdwan", "system.saml", "router.policy", "router.policy6", "log.syslogd.setting", "log.syslogd.override-setting", "firewall.address"] | None = ...,
        scope: Literal["all", "inclusive", "exclusive"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomExceptionObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VdomExceptionPayload | None = ...,
        id: int | None = ...,
        object: Literal["log.fortianalyzer.setting", "log.fortianalyzer.override-setting", "log.fortianalyzer2.setting", "log.fortianalyzer2.override-setting", "log.fortianalyzer3.setting", "log.fortianalyzer3.override-setting", "log.fortianalyzer-cloud.setting", "log.fortianalyzer-cloud.override-setting", "log.syslogd.setting", "log.syslogd.override-setting", "log.syslogd2.setting", "log.syslogd2.override-setting", "log.syslogd3.setting", "log.syslogd3.override-setting", "log.syslogd4.setting", "log.syslogd4.override-setting", "system.gre-tunnel", "system.central-management", "system.csf", "user.radius", "system.interface", "vpn.ipsec.phase1-interface", "vpn.ipsec.phase2-interface", "router.bgp", "router.route-map", "router.prefix-list", "firewall.ippool", "firewall.ippool6", "router.static", "router.static6", "firewall.vip", "firewall.vip6", "system.sdwan", "system.saml", "router.policy", "router.policy6", "log.syslogd.setting", "log.syslogd.override-setting", "firewall.address"] | None = ...,
        scope: Literal["all", "inclusive", "exclusive"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomExceptionObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: VdomExceptionPayload | None = ...,
        id: int | None = ...,
        object: Literal["log.fortianalyzer.setting", "log.fortianalyzer.override-setting", "log.fortianalyzer2.setting", "log.fortianalyzer2.override-setting", "log.fortianalyzer3.setting", "log.fortianalyzer3.override-setting", "log.fortianalyzer-cloud.setting", "log.fortianalyzer-cloud.override-setting", "log.syslogd.setting", "log.syslogd.override-setting", "log.syslogd2.setting", "log.syslogd2.override-setting", "log.syslogd3.setting", "log.syslogd3.override-setting", "log.syslogd4.setting", "log.syslogd4.override-setting", "system.gre-tunnel", "system.central-management", "system.csf", "user.radius", "system.interface", "vpn.ipsec.phase1-interface", "vpn.ipsec.phase2-interface", "router.bgp", "router.route-map", "router.prefix-list", "firewall.ippool", "firewall.ippool6", "router.static", "router.static6", "firewall.vip", "firewall.vip6", "system.sdwan", "system.saml", "router.policy", "router.policy6", "log.syslogd.setting", "log.syslogd.override-setting", "firewall.address"] | None = ...,
        scope: Literal["all", "inclusive", "exclusive"] | None = ...,
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
    "VdomException",
    "VdomExceptionPayload",
    "VdomExceptionResponse",
    "VdomExceptionObject",
]