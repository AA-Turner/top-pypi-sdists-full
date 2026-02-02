""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/automation_action
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

class AutomationActionEmailtoItem(TypedDict, total=False):
    """Nested item for email-to field."""
    name: str


class AutomationActionHttpheadersItem(TypedDict, total=False):
    """Nested item for http-headers field."""
    id: int
    key: str
    value: str


class AutomationActionFormdataItem(TypedDict, total=False):
    """Nested item for form-data field."""
    id: int
    key: str
    value: str


class AutomationActionSdnconnectorItem(TypedDict, total=False):
    """Nested item for sdn-connector field."""
    name: str


class AutomationActionPayload(TypedDict, total=False):
    """Payload type for AutomationAction operations."""
    name: str
    description: str
    action_type: Literal["email", "fortiexplorer-notification", "alert", "disable-ssid", "system-actions", "quarantine", "quarantine-forticlient", "quarantine-nsx", "quarantine-fortinac", "ban-ip", "aws-lambda", "azure-function", "google-cloud-function", "alicloud-function", "webhook", "cli-script", "diagnose-script", "regular-expression", "slack-notification", "microsoft-teams-notification"]
    system_action: Literal["reboot", "shutdown", "backup-config"]
    tls_certificate: str
    forticare_email: Literal["enable", "disable"]
    email_to: str | list[str] | list[AutomationActionEmailtoItem]
    email_from: str
    email_subject: str
    minimum_interval: int
    aws_api_key: str
    azure_function_authorization: Literal["anonymous", "function", "admin"]
    azure_api_key: str
    alicloud_function_authorization: Literal["anonymous", "function"]
    alicloud_access_key_id: str
    alicloud_access_key_secret: str
    message_type: Literal["text", "json", "form-data"]
    message: str
    replacement_message: Literal["enable", "disable"]
    replacemsg_group: str
    protocol: Literal["http", "https"]
    method: Literal["post", "put", "get", "patch", "delete"]
    uri: str
    http_body: str
    port: int
    http_headers: str | list[str] | list[AutomationActionHttpheadersItem]
    form_data: str | list[str] | list[AutomationActionFormdataItem]
    verify_host_cert: Literal["enable", "disable"]
    script: str
    output_size: int
    timeout: int
    duration: int
    output_interval: int
    file_only: Literal["enable", "disable"]
    execute_security_fabric: Literal["enable", "disable"]
    accprofile: str
    regular_expression: str
    log_debug_print: Literal["enable", "disable"]
    security_tag: str
    sdn_connector: str | list[str] | list[AutomationActionSdnconnectorItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AutomationActionResponse(TypedDict, total=False):
    """Response type for AutomationAction - use with .dict property for typed dict access."""
    name: str
    description: str
    action_type: Literal["email", "fortiexplorer-notification", "alert", "disable-ssid", "system-actions", "quarantine", "quarantine-forticlient", "quarantine-nsx", "quarantine-fortinac", "ban-ip", "aws-lambda", "azure-function", "google-cloud-function", "alicloud-function", "webhook", "cli-script", "diagnose-script", "regular-expression", "slack-notification", "microsoft-teams-notification"]
    system_action: Literal["reboot", "shutdown", "backup-config"]
    tls_certificate: str
    forticare_email: Literal["enable", "disable"]
    email_to: list[AutomationActionEmailtoItem]
    email_from: str
    email_subject: str
    minimum_interval: int
    aws_api_key: str
    azure_function_authorization: Literal["anonymous", "function", "admin"]
    azure_api_key: str
    alicloud_function_authorization: Literal["anonymous", "function"]
    alicloud_access_key_id: str
    alicloud_access_key_secret: str
    message_type: Literal["text", "json", "form-data"]
    message: str
    replacement_message: Literal["enable", "disable"]
    replacemsg_group: str
    protocol: Literal["http", "https"]
    method: Literal["post", "put", "get", "patch", "delete"]
    uri: str
    http_body: str
    port: int
    http_headers: list[AutomationActionHttpheadersItem]
    form_data: list[AutomationActionFormdataItem]
    verify_host_cert: Literal["enable", "disable"]
    script: str
    output_size: int
    timeout: int
    duration: int
    output_interval: int
    file_only: Literal["enable", "disable"]
    execute_security_fabric: Literal["enable", "disable"]
    accprofile: str
    regular_expression: str
    log_debug_print: Literal["enable", "disable"]
    security_tag: str
    sdn_connector: list[AutomationActionSdnconnectorItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AutomationActionEmailtoItemObject(FortiObject[AutomationActionEmailtoItem]):
    """Typed object for email-to table items with attribute access."""
    name: str


class AutomationActionHttpheadersItemObject(FortiObject[AutomationActionHttpheadersItem]):
    """Typed object for http-headers table items with attribute access."""
    id: int
    key: str
    value: str


class AutomationActionFormdataItemObject(FortiObject[AutomationActionFormdataItem]):
    """Typed object for form-data table items with attribute access."""
    id: int
    key: str
    value: str


class AutomationActionSdnconnectorItemObject(FortiObject[AutomationActionSdnconnectorItem]):
    """Typed object for sdn-connector table items with attribute access."""
    name: str


class AutomationActionObject(FortiObject):
    """Typed FortiObject for AutomationAction with field access."""
    name: str
    description: str
    action_type: Literal["email", "fortiexplorer-notification", "alert", "disable-ssid", "system-actions", "quarantine", "quarantine-forticlient", "quarantine-nsx", "quarantine-fortinac", "ban-ip", "aws-lambda", "azure-function", "google-cloud-function", "alicloud-function", "webhook", "cli-script", "diagnose-script", "regular-expression", "slack-notification", "microsoft-teams-notification"]
    system_action: Literal["reboot", "shutdown", "backup-config"]
    tls_certificate: str
    forticare_email: Literal["enable", "disable"]
    email_to: FortiObjectList[AutomationActionEmailtoItemObject]
    email_from: str
    email_subject: str
    minimum_interval: int
    aws_api_key: str
    azure_function_authorization: Literal["anonymous", "function", "admin"]
    azure_api_key: str
    alicloud_function_authorization: Literal["anonymous", "function"]
    alicloud_access_key_id: str
    alicloud_access_key_secret: str
    message_type: Literal["text", "json", "form-data"]
    message: str
    replacement_message: Literal["enable", "disable"]
    replacemsg_group: str
    protocol: Literal["http", "https"]
    method: Literal["post", "put", "get", "patch", "delete"]
    uri: str
    http_body: str
    port: int
    http_headers: FortiObjectList[AutomationActionHttpheadersItemObject]
    form_data: FortiObjectList[AutomationActionFormdataItemObject]
    verify_host_cert: Literal["enable", "disable"]
    script: str
    output_size: int
    timeout: int
    duration: int
    output_interval: int
    file_only: Literal["enable", "disable"]
    execute_security_fabric: Literal["enable", "disable"]
    accprofile: str
    regular_expression: str
    log_debug_print: Literal["enable", "disable"]
    security_tag: str
    sdn_connector: FortiObjectList[AutomationActionSdnconnectorItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class AutomationAction:
    """
    
    Endpoint: system/automation_action
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
    ) -> AutomationActionObject: ...
    
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
    ) -> FortiObjectList[AutomationActionObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: AutomationActionPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        action_type: Literal["email", "fortiexplorer-notification", "alert", "disable-ssid", "system-actions", "quarantine", "quarantine-forticlient", "quarantine-nsx", "quarantine-fortinac", "ban-ip", "aws-lambda", "azure-function", "google-cloud-function", "alicloud-function", "webhook", "cli-script", "diagnose-script", "regular-expression", "slack-notification", "microsoft-teams-notification"] | None = ...,
        system_action: Literal["reboot", "shutdown", "backup-config"] | None = ...,
        tls_certificate: str | None = ...,
        forticare_email: Literal["enable", "disable"] | None = ...,
        email_to: str | list[str] | list[AutomationActionEmailtoItem] | None = ...,
        email_from: str | None = ...,
        email_subject: str | None = ...,
        minimum_interval: int | None = ...,
        aws_api_key: str | None = ...,
        azure_function_authorization: Literal["anonymous", "function", "admin"] | None = ...,
        azure_api_key: str | None = ...,
        alicloud_function_authorization: Literal["anonymous", "function"] | None = ...,
        alicloud_access_key_id: str | None = ...,
        alicloud_access_key_secret: str | None = ...,
        message_type: Literal["text", "json", "form-data"] | None = ...,
        message: str | None = ...,
        replacement_message: Literal["enable", "disable"] | None = ...,
        replacemsg_group: str | None = ...,
        protocol: Literal["http", "https"] | None = ...,
        method: Literal["post", "put", "get", "patch", "delete"] | None = ...,
        uri: str | None = ...,
        http_body: str | None = ...,
        port: int | None = ...,
        http_headers: str | list[str] | list[AutomationActionHttpheadersItem] | None = ...,
        form_data: str | list[str] | list[AutomationActionFormdataItem] | None = ...,
        verify_host_cert: Literal["enable", "disable"] | None = ...,
        script: str | None = ...,
        output_size: int | None = ...,
        timeout: int | None = ...,
        duration: int | None = ...,
        output_interval: int | None = ...,
        file_only: Literal["enable", "disable"] | None = ...,
        execute_security_fabric: Literal["enable", "disable"] | None = ...,
        accprofile: str | None = ...,
        regular_expression: str | None = ...,
        log_debug_print: Literal["enable", "disable"] | None = ...,
        security_tag: str | None = ...,
        sdn_connector: str | list[str] | list[AutomationActionSdnconnectorItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AutomationActionObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AutomationActionPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        action_type: Literal["email", "fortiexplorer-notification", "alert", "disable-ssid", "system-actions", "quarantine", "quarantine-forticlient", "quarantine-nsx", "quarantine-fortinac", "ban-ip", "aws-lambda", "azure-function", "google-cloud-function", "alicloud-function", "webhook", "cli-script", "diagnose-script", "regular-expression", "slack-notification", "microsoft-teams-notification"] | None = ...,
        system_action: Literal["reboot", "shutdown", "backup-config"] | None = ...,
        tls_certificate: str | None = ...,
        forticare_email: Literal["enable", "disable"] | None = ...,
        email_to: str | list[str] | list[AutomationActionEmailtoItem] | None = ...,
        email_from: str | None = ...,
        email_subject: str | None = ...,
        minimum_interval: int | None = ...,
        aws_api_key: str | None = ...,
        azure_function_authorization: Literal["anonymous", "function", "admin"] | None = ...,
        azure_api_key: str | None = ...,
        alicloud_function_authorization: Literal["anonymous", "function"] | None = ...,
        alicloud_access_key_id: str | None = ...,
        alicloud_access_key_secret: str | None = ...,
        message_type: Literal["text", "json", "form-data"] | None = ...,
        message: str | None = ...,
        replacement_message: Literal["enable", "disable"] | None = ...,
        replacemsg_group: str | None = ...,
        protocol: Literal["http", "https"] | None = ...,
        method: Literal["post", "put", "get", "patch", "delete"] | None = ...,
        uri: str | None = ...,
        http_body: str | None = ...,
        port: int | None = ...,
        http_headers: str | list[str] | list[AutomationActionHttpheadersItem] | None = ...,
        form_data: str | list[str] | list[AutomationActionFormdataItem] | None = ...,
        verify_host_cert: Literal["enable", "disable"] | None = ...,
        script: str | None = ...,
        output_size: int | None = ...,
        timeout: int | None = ...,
        duration: int | None = ...,
        output_interval: int | None = ...,
        file_only: Literal["enable", "disable"] | None = ...,
        execute_security_fabric: Literal["enable", "disable"] | None = ...,
        accprofile: str | None = ...,
        regular_expression: str | None = ...,
        log_debug_print: Literal["enable", "disable"] | None = ...,
        security_tag: str | None = ...,
        sdn_connector: str | list[str] | list[AutomationActionSdnconnectorItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AutomationActionObject: ...

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
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: AutomationActionPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        action_type: Literal["email", "fortiexplorer-notification", "alert", "disable-ssid", "system-actions", "quarantine", "quarantine-forticlient", "quarantine-nsx", "quarantine-fortinac", "ban-ip", "aws-lambda", "azure-function", "google-cloud-function", "alicloud-function", "webhook", "cli-script", "diagnose-script", "regular-expression", "slack-notification", "microsoft-teams-notification"] | None = ...,
        system_action: Literal["reboot", "shutdown", "backup-config"] | None = ...,
        tls_certificate: str | None = ...,
        forticare_email: Literal["enable", "disable"] | None = ...,
        email_to: str | list[str] | list[AutomationActionEmailtoItem] | None = ...,
        email_from: str | None = ...,
        email_subject: str | None = ...,
        minimum_interval: int | None = ...,
        aws_api_key: str | None = ...,
        azure_function_authorization: Literal["anonymous", "function", "admin"] | None = ...,
        azure_api_key: str | None = ...,
        alicloud_function_authorization: Literal["anonymous", "function"] | None = ...,
        alicloud_access_key_id: str | None = ...,
        alicloud_access_key_secret: str | None = ...,
        message_type: Literal["text", "json", "form-data"] | None = ...,
        message: str | None = ...,
        replacement_message: Literal["enable", "disable"] | None = ...,
        replacemsg_group: str | None = ...,
        protocol: Literal["http", "https"] | None = ...,
        method: Literal["post", "put", "get", "patch", "delete"] | None = ...,
        uri: str | None = ...,
        http_body: str | None = ...,
        port: int | None = ...,
        http_headers: str | list[str] | list[AutomationActionHttpheadersItem] | None = ...,
        form_data: str | list[str] | list[AutomationActionFormdataItem] | None = ...,
        verify_host_cert: Literal["enable", "disable"] | None = ...,
        script: str | None = ...,
        output_size: int | None = ...,
        timeout: int | None = ...,
        duration: int | None = ...,
        output_interval: int | None = ...,
        file_only: Literal["enable", "disable"] | None = ...,
        execute_security_fabric: Literal["enable", "disable"] | None = ...,
        accprofile: str | None = ...,
        regular_expression: str | None = ...,
        log_debug_print: Literal["enable", "disable"] | None = ...,
        security_tag: str | None = ...,
        sdn_connector: str | list[str] | list[AutomationActionSdnconnectorItem] | None = ...,
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
    "AutomationAction",
    "AutomationActionPayload",
    "AutomationActionResponse",
    "AutomationActionObject",
]