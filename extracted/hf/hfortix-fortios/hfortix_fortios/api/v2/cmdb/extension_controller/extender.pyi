""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: extension_controller/extender
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

class ExtenderWanextensionDict(TypedDict, total=False):
    """Nested object type for wan-extension field."""
    modem1_extension: str
    modem2_extension: str
    modem1_pdn1_interface: str
    modem1_pdn2_interface: str
    modem1_pdn3_interface: str
    modem1_pdn4_interface: str
    modem2_pdn1_interface: str
    modem2_pdn2_interface: str
    modem2_pdn3_interface: str
    modem2_pdn4_interface: str


class ExtenderPayload(TypedDict, total=False):
    """Payload type for Extender operations."""
    name: str
    id: str
    authorized: Literal["discovered", "disable", "enable"]
    ext_name: str
    description: str
    vdom: int
    device_id: int
    extension_type: Literal["wan-extension", "lan-extension"]
    profile: str
    override_allowaccess: Literal["enable", "disable"]
    allowaccess: str | list[str]
    override_login_password_change: Literal["enable", "disable"]
    login_password_change: Literal["yes", "default", "no"]
    login_password: str
    override_enforce_bandwidth: Literal["enable", "disable"]
    enforce_bandwidth: Literal["enable", "disable"]
    bandwidth_limit: int
    wan_extension: ExtenderWanextensionDict
    firmware_provision_latest: Literal["disable", "once"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ExtenderResponse(TypedDict, total=False):
    """Response type for Extender - use with .dict property for typed dict access."""
    name: str
    id: str
    authorized: Literal["discovered", "disable", "enable"]
    ext_name: str
    description: str
    vdom: int
    device_id: int
    extension_type: Literal["wan-extension", "lan-extension"]
    profile: str
    override_allowaccess: Literal["enable", "disable"]
    allowaccess: str
    override_login_password_change: Literal["enable", "disable"]
    login_password_change: Literal["yes", "default", "no"]
    login_password: str
    override_enforce_bandwidth: Literal["enable", "disable"]
    enforce_bandwidth: Literal["enable", "disable"]
    bandwidth_limit: int
    wan_extension: ExtenderWanextensionDict
    firmware_provision_latest: Literal["disable", "once"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ExtenderWanextensionObject(FortiObject):
    """Nested object for wan-extension field with attribute access."""
    modem1_extension: str
    modem2_extension: str
    modem1_pdn1_interface: str
    modem1_pdn2_interface: str
    modem1_pdn3_interface: str
    modem1_pdn4_interface: str
    modem2_pdn1_interface: str
    modem2_pdn2_interface: str
    modem2_pdn3_interface: str
    modem2_pdn4_interface: str


class ExtenderObject(FortiObject):
    """Typed FortiObject for Extender with field access."""
    name: str
    id: str
    authorized: Literal["discovered", "disable", "enable"]
    ext_name: str
    description: str
    device_id: int
    extension_type: Literal["wan-extension", "lan-extension"]
    profile: str
    override_allowaccess: Literal["enable", "disable"]
    allowaccess: str
    override_login_password_change: Literal["enable", "disable"]
    login_password_change: Literal["yes", "default", "no"]
    login_password: str
    override_enforce_bandwidth: Literal["enable", "disable"]
    enforce_bandwidth: Literal["enable", "disable"]
    bandwidth_limit: int
    wan_extension: ExtenderWanextensionObject
    firmware_provision_latest: Literal["disable", "once"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Extender:
    """
    
    Endpoint: extension_controller/extender
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
    ) -> ExtenderObject: ...
    
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
    ) -> FortiObjectList[ExtenderObject]: ...
    
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
        payload_dict: ExtenderPayload | None = ...,
        name: str | None = ...,
        id: str | None = ...,
        authorized: Literal["discovered", "disable", "enable"] | None = ...,
        ext_name: str | None = ...,
        description: str | None = ...,
        device_id: int | None = ...,
        extension_type: Literal["wan-extension", "lan-extension"] | None = ...,
        profile: str | None = ...,
        override_allowaccess: Literal["enable", "disable"] | None = ...,
        allowaccess: str | list[str] | None = ...,
        override_login_password_change: Literal["enable", "disable"] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        override_enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        wan_extension: ExtenderWanextensionDict | None = ...,
        firmware_provision_latest: Literal["disable", "once"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExtenderObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ExtenderPayload | None = ...,
        name: str | None = ...,
        id: str | None = ...,
        authorized: Literal["discovered", "disable", "enable"] | None = ...,
        ext_name: str | None = ...,
        description: str | None = ...,
        device_id: int | None = ...,
        extension_type: Literal["wan-extension", "lan-extension"] | None = ...,
        profile: str | None = ...,
        override_allowaccess: Literal["enable", "disable"] | None = ...,
        allowaccess: str | list[str] | None = ...,
        override_login_password_change: Literal["enable", "disable"] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        override_enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        wan_extension: ExtenderWanextensionDict | None = ...,
        firmware_provision_latest: Literal["disable", "once"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExtenderObject: ...

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
        payload_dict: ExtenderPayload | None = ...,
        name: str | None = ...,
        id: str | None = ...,
        authorized: Literal["discovered", "disable", "enable"] | None = ...,
        ext_name: str | None = ...,
        description: str | None = ...,
        device_id: int | None = ...,
        extension_type: Literal["wan-extension", "lan-extension"] | None = ...,
        profile: str | None = ...,
        override_allowaccess: Literal["enable", "disable"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        override_login_password_change: Literal["enable", "disable"] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        override_enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        wan_extension: ExtenderWanextensionDict | None = ...,
        firmware_provision_latest: Literal["disable", "once"] | None = ...,
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
    "Extender",
    "ExtenderPayload",
    "ExtenderResponse",
    "ExtenderObject",
]