""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: web_proxy/global_
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class GlobalLearnclientipsrcaddrItem(TypedDict, total=False):
    """Nested item for learn-client-ip-srcaddr field."""
    name: str


class GlobalLearnclientipsrcaddr6Item(TypedDict, total=False):
    """Nested item for learn-client-ip-srcaddr6 field."""
    name: str


class GlobalPayload(TypedDict, total=False):
    """Payload type for Global operations."""
    ssl_cert: str
    ssl_ca_cert: str
    fast_policy_match: Literal["enable", "disable"]
    ldap_user_cache: Literal["enable", "disable"]
    proxy_fqdn: str
    max_request_length: int
    max_message_length: int
    http2_client_window_size: int
    http2_server_window_size: int
    auth_sign_timeout: int
    strict_web_check: Literal["enable", "disable"]
    forward_proxy_auth: Literal["enable", "disable"]
    forward_server_affinity_timeout: int
    max_waf_body_cache_length: int
    webproxy_profile: str
    learn_client_ip: Literal["enable", "disable"]
    always_learn_client_ip: Literal["enable", "disable"]
    learn_client_ip_from_header: str | list[str]
    learn_client_ip_srcaddr: str | list[str] | list[GlobalLearnclientipsrcaddrItem]
    learn_client_ip_srcaddr6: str | list[str] | list[GlobalLearnclientipsrcaddr6Item]
    src_affinity_exempt_addr: str | list[str]
    src_affinity_exempt_addr6: str | list[str]
    policy_partial_match: Literal["enable", "disable"]
    log_policy_pending: Literal["enable", "disable"]
    log_forward_server: Literal["enable", "disable"]
    log_app_id: Literal["enable", "disable"]
    proxy_transparent_cert_inspection: Literal["enable", "disable"]
    request_obs_fold: Literal["replace-with-sp", "block", "keep"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GlobalResponse(TypedDict, total=False):
    """Response type for Global - use with .dict property for typed dict access."""
    ssl_cert: str
    ssl_ca_cert: str
    fast_policy_match: Literal["enable", "disable"]
    ldap_user_cache: Literal["enable", "disable"]
    proxy_fqdn: str
    max_request_length: int
    max_message_length: int
    http2_client_window_size: int
    http2_server_window_size: int
    auth_sign_timeout: int
    strict_web_check: Literal["enable", "disable"]
    forward_proxy_auth: Literal["enable", "disable"]
    forward_server_affinity_timeout: int
    max_waf_body_cache_length: int
    webproxy_profile: str
    learn_client_ip: Literal["enable", "disable"]
    always_learn_client_ip: Literal["enable", "disable"]
    learn_client_ip_from_header: str
    learn_client_ip_srcaddr: list[GlobalLearnclientipsrcaddrItem]
    learn_client_ip_srcaddr6: list[GlobalLearnclientipsrcaddr6Item]
    src_affinity_exempt_addr: str | list[str]
    src_affinity_exempt_addr6: str | list[str]
    policy_partial_match: Literal["enable", "disable"]
    log_policy_pending: Literal["enable", "disable"]
    log_forward_server: Literal["enable", "disable"]
    log_app_id: Literal["enable", "disable"]
    proxy_transparent_cert_inspection: Literal["enable", "disable"]
    request_obs_fold: Literal["replace-with-sp", "block", "keep"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GlobalLearnclientipsrcaddrItemObject(FortiObject[GlobalLearnclientipsrcaddrItem]):
    """Typed object for learn-client-ip-srcaddr table items with attribute access."""
    name: str


class GlobalLearnclientipsrcaddr6ItemObject(FortiObject[GlobalLearnclientipsrcaddr6Item]):
    """Typed object for learn-client-ip-srcaddr6 table items with attribute access."""
    name: str


class GlobalObject(FortiObject):
    """Typed FortiObject for Global with field access."""
    ssl_cert: str
    ssl_ca_cert: str
    fast_policy_match: Literal["enable", "disable"]
    ldap_user_cache: Literal["enable", "disable"]
    proxy_fqdn: str
    max_request_length: int
    max_message_length: int
    http2_client_window_size: int
    http2_server_window_size: int
    auth_sign_timeout: int
    strict_web_check: Literal["enable", "disable"]
    forward_proxy_auth: Literal["enable", "disable"]
    forward_server_affinity_timeout: int
    max_waf_body_cache_length: int
    webproxy_profile: str
    learn_client_ip: Literal["enable", "disable"]
    always_learn_client_ip: Literal["enable", "disable"]
    learn_client_ip_from_header: str
    learn_client_ip_srcaddr: FortiObjectList[GlobalLearnclientipsrcaddrItemObject]
    learn_client_ip_srcaddr6: FortiObjectList[GlobalLearnclientipsrcaddr6ItemObject]
    src_affinity_exempt_addr: str | list[str]
    src_affinity_exempt_addr6: str | list[str]
    policy_partial_match: Literal["enable", "disable"]
    log_policy_pending: Literal["enable", "disable"]
    log_forward_server: Literal["enable", "disable"]
    log_app_id: Literal["enable", "disable"]
    proxy_transparent_cert_inspection: Literal["enable", "disable"]
    request_obs_fold: Literal["replace-with-sp", "block", "keep"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Global:
    """
    
    Endpoint: web_proxy/global_
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Singleton endpoint (no mkey)
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
    ) -> GlobalObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: GlobalPayload | None = ...,
        ssl_cert: str | None = ...,
        ssl_ca_cert: str | None = ...,
        fast_policy_match: Literal["enable", "disable"] | None = ...,
        ldap_user_cache: Literal["enable", "disable"] | None = ...,
        proxy_fqdn: str | None = ...,
        max_request_length: int | None = ...,
        max_message_length: int | None = ...,
        http2_client_window_size: int | None = ...,
        http2_server_window_size: int | None = ...,
        auth_sign_timeout: int | None = ...,
        strict_web_check: Literal["enable", "disable"] | None = ...,
        forward_proxy_auth: Literal["enable", "disable"] | None = ...,
        forward_server_affinity_timeout: int | None = ...,
        max_waf_body_cache_length: int | None = ...,
        webproxy_profile: str | None = ...,
        learn_client_ip: Literal["enable", "disable"] | None = ...,
        always_learn_client_ip: Literal["enable", "disable"] | None = ...,
        learn_client_ip_from_header: str | list[str] | None = ...,
        learn_client_ip_srcaddr: str | list[str] | list[GlobalLearnclientipsrcaddrItem] | None = ...,
        learn_client_ip_srcaddr6: str | list[str] | list[GlobalLearnclientipsrcaddr6Item] | None = ...,
        src_affinity_exempt_addr: str | list[str] | None = ...,
        src_affinity_exempt_addr6: str | list[str] | None = ...,
        policy_partial_match: Literal["enable", "disable"] | None = ...,
        log_policy_pending: Literal["enable", "disable"] | None = ...,
        log_forward_server: Literal["enable", "disable"] | None = ...,
        log_app_id: Literal["enable", "disable"] | None = ...,
        proxy_transparent_cert_inspection: Literal["enable", "disable"] | None = ...,
        request_obs_fold: Literal["replace-with-sp", "block", "keep"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GlobalObject: ...


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
        payload_dict: GlobalPayload | None = ...,
        ssl_cert: str | None = ...,
        ssl_ca_cert: str | None = ...,
        fast_policy_match: Literal["enable", "disable"] | None = ...,
        ldap_user_cache: Literal["enable", "disable"] | None = ...,
        proxy_fqdn: str | None = ...,
        max_request_length: int | None = ...,
        max_message_length: int | None = ...,
        http2_client_window_size: int | None = ...,
        http2_server_window_size: int | None = ...,
        auth_sign_timeout: int | None = ...,
        strict_web_check: Literal["enable", "disable"] | None = ...,
        forward_proxy_auth: Literal["enable", "disable"] | None = ...,
        forward_server_affinity_timeout: int | None = ...,
        max_waf_body_cache_length: int | None = ...,
        webproxy_profile: str | None = ...,
        learn_client_ip: Literal["enable", "disable"] | None = ...,
        always_learn_client_ip: Literal["enable", "disable"] | None = ...,
        learn_client_ip_from_header: Literal["true-client-ip", "x-real-ip", "x-forwarded-for"] | list[str] | None = ...,
        learn_client_ip_srcaddr: str | list[str] | list[GlobalLearnclientipsrcaddrItem] | None = ...,
        learn_client_ip_srcaddr6: str | list[str] | list[GlobalLearnclientipsrcaddr6Item] | None = ...,
        src_affinity_exempt_addr: str | list[str] | None = ...,
        src_affinity_exempt_addr6: str | list[str] | None = ...,
        policy_partial_match: Literal["enable", "disable"] | None = ...,
        log_policy_pending: Literal["enable", "disable"] | None = ...,
        log_forward_server: Literal["enable", "disable"] | None = ...,
        log_app_id: Literal["enable", "disable"] | None = ...,
        proxy_transparent_cert_inspection: Literal["enable", "disable"] | None = ...,
        request_obs_fold: Literal["replace-with-sp", "block", "keep"] | None = ...,
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
    "Global",
    "GlobalPayload",
    "GlobalResponse",
    "GlobalObject",
]