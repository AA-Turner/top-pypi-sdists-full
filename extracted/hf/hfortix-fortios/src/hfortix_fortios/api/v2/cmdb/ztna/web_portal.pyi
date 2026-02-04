""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ztna/web_portal
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

class WebPortalPayload(TypedDict, total=False):
    """Payload type for WebPortal operations."""
    name: str
    vip: str
    host: str
    decrypted_traffic_mirror: str
    log_blocked_traffic: Literal["disable", "enable"]
    auth_portal: Literal["disable", "enable"]
    auth_virtual_host: str
    vip6: str
    auth_rule: str
    display_bookmark: Literal["enable", "disable"]
    focus_bookmark: Literal["enable", "disable"]
    display_status: Literal["enable", "disable"]
    display_history: Literal["enable", "disable"]
    policy_auth_sso: Literal["enable", "disable"]
    heading: str
    theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"]
    clipboard: Literal["enable", "disable"]
    default_window_width: int
    default_window_height: int
    cookie_age: int
    forticlient_download: Literal["enable", "disable"]
    customize_forticlient_download_url: Literal["enable", "disable"]
    windows_forticlient_download_url: str
    macos_forticlient_download_url: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class WebPortalResponse(TypedDict, total=False):
    """Response type for WebPortal - use with .dict property for typed dict access."""
    name: str
    vip: str
    host: str
    decrypted_traffic_mirror: str
    log_blocked_traffic: Literal["disable", "enable"]
    auth_portal: Literal["disable", "enable"]
    auth_virtual_host: str
    vip6: str
    auth_rule: str
    display_bookmark: Literal["enable", "disable"]
    focus_bookmark: Literal["enable", "disable"]
    display_status: Literal["enable", "disable"]
    display_history: Literal["enable", "disable"]
    policy_auth_sso: Literal["enable", "disable"]
    heading: str
    theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"]
    clipboard: Literal["enable", "disable"]
    default_window_width: int
    default_window_height: int
    cookie_age: int
    forticlient_download: Literal["enable", "disable"]
    customize_forticlient_download_url: Literal["enable", "disable"]
    windows_forticlient_download_url: str
    macos_forticlient_download_url: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class WebPortalObject(FortiObject):
    """Typed FortiObject for WebPortal with field access."""
    name: str
    vip: str
    host: str
    decrypted_traffic_mirror: str
    log_blocked_traffic: Literal["disable", "enable"]
    auth_portal: Literal["disable", "enable"]
    auth_virtual_host: str
    vip6: str
    auth_rule: str
    display_bookmark: Literal["enable", "disable"]
    focus_bookmark: Literal["enable", "disable"]
    display_status: Literal["enable", "disable"]
    display_history: Literal["enable", "disable"]
    policy_auth_sso: Literal["enable", "disable"]
    heading: str
    theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"]
    clipboard: Literal["enable", "disable"]
    default_window_width: int
    default_window_height: int
    cookie_age: int
    forticlient_download: Literal["enable", "disable"]
    customize_forticlient_download_url: Literal["enable", "disable"]
    windows_forticlient_download_url: str
    macos_forticlient_download_url: str


# ================================================================
# Main Endpoint Class
# ================================================================

class WebPortal:
    """
    
    Endpoint: ztna/web_portal
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
    ) -> WebPortalObject: ...
    
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
    ) -> FortiObjectList[WebPortalObject]: ...
    
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
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WebPortalObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> WebPortalObject: ...

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
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
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
    "WebPortal",
    "WebPortalPayload",
    "WebPortalResponse",
    "WebPortalObject",
]