""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: license/status
Category: monitor
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
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class StatusResponse(TypedDict, total=False):
    """Response type for Status - use with .dict property for typed dict access."""
    antivirus: str
    appctrl: str
    genai_app: str
    forticare: str
    ips: str
    ot_detection: str
    iot_detection: str
    vm: str
    web_filtering: str
    security_rating: str
    mobile_malware: str
    ai_malware_detection: str
    industrial_db: str
    internet_service_db: str
    device_os_id: str
    botnet_domain: str
    data_leak_prevention: str
    psirt_security_rating: str
    fortitelemetry: str
    timezone_database: str
    geoip_db: str
    trusted_cert_db: str
    outbreak_security_rating: str
    icdb: str
    inline_casb: str
    local_in_virtual_patching: str
    malicious_urls: str
    blacklisted_certificates: str
    firmware_updates: str
    outbreak_prevention: str
    antispam: str
    sdwan_network_monitor: str
    forticloud: str
    forticloud_logging: str
    forticloud_sandbox: str
    fortianalyzer_cloud: str
    fortianalyzer_cloud_premium: str
    fortimanager_cloud: str
    fortisandbox_cloud: str
    fortiguard_ai_based_sandbox: str
    forticonverter: str
    sdwan_overlay_aas: str
    sovereign_sase: str
    fortiems_cloud: str
    fortimanager_cloud_alci: str
    fortisandbox_cloud_alci: str
    vdom: str
    sms: str
    load_balance_fpc: str


class StatusObject(FortiObject[StatusResponse]):
    """Typed FortiObject for Status with field access."""
    antivirus: str
    appctrl: str
    genai_app: str
    forticare: str
    ips: str
    ot_detection: str
    iot_detection: str
    vm: str
    web_filtering: str
    security_rating: str
    mobile_malware: str
    ai_malware_detection: str
    industrial_db: str
    internet_service_db: str
    device_os_id: str
    botnet_domain: str
    data_leak_prevention: str
    psirt_security_rating: str
    fortitelemetry: str
    timezone_database: str
    geoip_db: str
    trusted_cert_db: str
    outbreak_security_rating: str
    icdb: str
    inline_casb: str
    local_in_virtual_patching: str
    malicious_urls: str
    blacklisted_certificates: str
    firmware_updates: str
    outbreak_prevention: str
    antispam: str
    sdwan_network_monitor: str
    forticloud: str
    forticloud_logging: str
    forticloud_sandbox: str
    fortianalyzer_cloud: str
    fortianalyzer_cloud_premium: str
    fortimanager_cloud: str
    fortisandbox_cloud: str
    fortiguard_ai_based_sandbox: str
    forticonverter: str
    sdwan_overlay_aas: str
    sovereign_sase: str
    fortiems_cloud: str
    fortimanager_cloud_alci: str
    fortisandbox_cloud_alci: str
    vdom: str
    sms: str
    load_balance_fpc: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Status:
    """
    
    Endpoint: license/status
    Category: monitor
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
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[StatusObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: dict[str, Any] | None = ...,
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
        payload_dict: dict[str, Any] | None = ...,
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
    "Status",
    "StatusResponse",
    "StatusObject",
]