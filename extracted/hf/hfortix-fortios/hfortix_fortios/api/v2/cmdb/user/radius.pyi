""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/radius
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

class RadiusClassItem(TypedDict, total=False):
    """Nested item for class field."""
    name: str


class RadiusAccountingserverItem(TypedDict, total=False):
    """Nested item for accounting-server field."""
    id: int
    status: Literal["enable", "disable"]
    server: str
    secret: str
    port: int
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class RadiusPayload(TypedDict, total=False):
    """Payload type for Radius operations."""
    name: str
    server: str
    secret: str
    secondary_server: str
    secondary_secret: str
    tertiary_server: str
    tertiary_secret: str
    timeout: int
    status_ttl: int
    all_usergroup: Literal["disable", "enable"]
    use_management_vdom: Literal["enable", "disable"]
    switch_controller_nas_ip_dynamic: Literal["enable", "disable"]
    nas_ip: str
    nas_id_type: Literal["legacy", "custom", "hostname"]
    call_station_id_type: Literal["legacy", "IP", "MAC"]
    nas_id: str
    acct_interim_interval: int
    radius_coa: Literal["enable", "disable"]
    radius_port: int
    h3c_compatibility: Literal["enable", "disable"]
    auth_type: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"]
    source_ip: str
    source_ip_interface: str
    username_case_sensitive: Literal["enable", "disable"]
    group_override_attr_type: Literal["filter-Id", "class"]
    class_: str | list[str] | list[RadiusClassItem]
    password_renewal: Literal["enable", "disable"]
    require_message_authenticator: Literal["enable", "disable"]
    password_encoding: Literal["auto", "ISO-8859-1"]
    mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_case: Literal["uppercase", "lowercase"]
    acct_all_servers: Literal["enable", "disable"]
    switch_controller_acct_fast_framedip_detect: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    switch_controller_service_type: str | list[str]
    transport_protocol: Literal["udp", "tcp", "tls"]
    tls_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    ca_cert: str
    client_cert: str
    server_identity_check: Literal["enable", "disable"]
    account_key_processing: Literal["same", "strip"]
    account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"]
    rsso: Literal["enable", "disable"]
    rsso_radius_server_port: int
    rsso_radius_response: Literal["enable", "disable"]
    rsso_validate_request_secret: Literal["enable", "disable"]
    rsso_secret: str
    rsso_endpoint_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
    rsso_endpoint_block_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
    sso_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
    sso_attribute_key: str
    sso_attribute_value_override: Literal["enable", "disable"]
    rsso_context_timeout: int
    rsso_log_period: int
    rsso_log_flags: str | list[str]
    rsso_flush_ip_session: Literal["enable", "disable"]
    rsso_ep_one_ip_only: Literal["enable", "disable"]
    delimiter: Literal["plus", "comma"]
    accounting_server: str | list[str] | list[RadiusAccountingserverItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class RadiusResponse(TypedDict, total=False):
    """Response type for Radius - use with .dict property for typed dict access."""
    name: str
    server: str
    secret: str
    secondary_server: str
    secondary_secret: str
    tertiary_server: str
    tertiary_secret: str
    timeout: int
    status_ttl: int
    all_usergroup: Literal["disable", "enable"]
    use_management_vdom: Literal["enable", "disable"]
    switch_controller_nas_ip_dynamic: Literal["enable", "disable"]
    nas_ip: str
    nas_id_type: Literal["legacy", "custom", "hostname"]
    call_station_id_type: Literal["legacy", "IP", "MAC"]
    nas_id: str
    acct_interim_interval: int
    radius_coa: Literal["enable", "disable"]
    radius_port: int
    h3c_compatibility: Literal["enable", "disable"]
    auth_type: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"]
    source_ip: str
    source_ip_interface: str
    username_case_sensitive: Literal["enable", "disable"]
    group_override_attr_type: Literal["filter-Id", "class"]
    class_: list[RadiusClassItem]
    password_renewal: Literal["enable", "disable"]
    require_message_authenticator: Literal["enable", "disable"]
    password_encoding: Literal["auto", "ISO-8859-1"]
    mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_case: Literal["uppercase", "lowercase"]
    acct_all_servers: Literal["enable", "disable"]
    switch_controller_acct_fast_framedip_detect: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    switch_controller_service_type: str
    transport_protocol: Literal["udp", "tcp", "tls"]
    tls_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    ca_cert: str
    client_cert: str
    server_identity_check: Literal["enable", "disable"]
    account_key_processing: Literal["same", "strip"]
    account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"]
    rsso: Literal["enable", "disable"]
    rsso_radius_server_port: int
    rsso_radius_response: Literal["enable", "disable"]
    rsso_validate_request_secret: Literal["enable", "disable"]
    rsso_secret: str
    rsso_endpoint_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
    rsso_endpoint_block_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
    sso_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
    sso_attribute_key: str
    sso_attribute_value_override: Literal["enable", "disable"]
    rsso_context_timeout: int
    rsso_log_period: int
    rsso_log_flags: str
    rsso_flush_ip_session: Literal["enable", "disable"]
    rsso_ep_one_ip_only: Literal["enable", "disable"]
    delimiter: Literal["plus", "comma"]
    accounting_server: list[RadiusAccountingserverItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class RadiusClassItemObject(FortiObject[RadiusClassItem]):
    """Typed object for class table items with attribute access."""
    name: str


class RadiusAccountingserverItemObject(FortiObject[RadiusAccountingserverItem]):
    """Typed object for accounting-server table items with attribute access."""
    id: int
    status: Literal["enable", "disable"]
    server: str
    secret: str
    port: int
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class RadiusObject(FortiObject):
    """Typed FortiObject for Radius with field access."""
    name: str
    server: str
    secret: str
    secondary_server: str
    secondary_secret: str
    tertiary_server: str
    tertiary_secret: str
    timeout: int
    status_ttl: int
    all_usergroup: Literal["disable", "enable"]
    use_management_vdom: Literal["enable", "disable"]
    switch_controller_nas_ip_dynamic: Literal["enable", "disable"]
    nas_ip: str
    nas_id_type: Literal["legacy", "custom", "hostname"]
    call_station_id_type: Literal["legacy", "IP", "MAC"]
    nas_id: str
    acct_interim_interval: int
    radius_coa: Literal["enable", "disable"]
    radius_port: int
    h3c_compatibility: Literal["enable", "disable"]
    auth_type: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"]
    source_ip: str
    source_ip_interface: str
    username_case_sensitive: Literal["enable", "disable"]
    group_override_attr_type: Literal["filter-Id", "class"]
    class_: FortiObjectList[RadiusClassItemObject]
    password_renewal: Literal["enable", "disable"]
    require_message_authenticator: Literal["enable", "disable"]
    password_encoding: Literal["auto", "ISO-8859-1"]
    mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"]
    mac_case: Literal["uppercase", "lowercase"]
    acct_all_servers: Literal["enable", "disable"]
    switch_controller_acct_fast_framedip_detect: int
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    switch_controller_service_type: str
    transport_protocol: Literal["udp", "tcp", "tls"]
    tls_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    ca_cert: str
    client_cert: str
    server_identity_check: Literal["enable", "disable"]
    account_key_processing: Literal["same", "strip"]
    account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"]
    rsso: Literal["enable", "disable"]
    rsso_radius_server_port: int
    rsso_radius_response: Literal["enable", "disable"]
    rsso_validate_request_secret: Literal["enable", "disable"]
    rsso_secret: str
    rsso_endpoint_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
    rsso_endpoint_block_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
    sso_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
    sso_attribute_key: str
    sso_attribute_value_override: Literal["enable", "disable"]
    rsso_context_timeout: int
    rsso_log_period: int
    rsso_log_flags: str
    rsso_flush_ip_session: Literal["enable", "disable"]
    rsso_ep_one_ip_only: Literal["enable", "disable"]
    delimiter: Literal["plus", "comma"]
    accounting_server: FortiObjectList[RadiusAccountingserverItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Radius:
    """
    
    Endpoint: user/radius
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
    ) -> RadiusObject: ...
    
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
    ) -> FortiObjectList[RadiusObject]: ...
    
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
        payload_dict: RadiusPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secret: str | None = ...,
        secondary_server: str | None = ...,
        secondary_secret: str | None = ...,
        tertiary_server: str | None = ...,
        tertiary_secret: str | None = ...,
        timeout: int | None = ...,
        status_ttl: int | None = ...,
        all_usergroup: Literal["disable", "enable"] | None = ...,
        use_management_vdom: Literal["enable", "disable"] | None = ...,
        switch_controller_nas_ip_dynamic: Literal["enable", "disable"] | None = ...,
        nas_ip: str | None = ...,
        nas_id_type: Literal["legacy", "custom", "hostname"] | None = ...,
        call_station_id_type: Literal["legacy", "IP", "MAC"] | None = ...,
        nas_id: str | None = ...,
        acct_interim_interval: int | None = ...,
        radius_coa: Literal["enable", "disable"] | None = ...,
        radius_port: int | None = ...,
        h3c_compatibility: Literal["enable", "disable"] | None = ...,
        auth_type: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        username_case_sensitive: Literal["enable", "disable"] | None = ...,
        group_override_attr_type: Literal["filter-Id", "class"] | None = ...,
        class_: str | list[str] | list[RadiusClassItem] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        require_message_authenticator: Literal["enable", "disable"] | None = ...,
        password_encoding: Literal["auto", "ISO-8859-1"] | None = ...,
        mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_case: Literal["uppercase", "lowercase"] | None = ...,
        acct_all_servers: Literal["enable", "disable"] | None = ...,
        switch_controller_acct_fast_framedip_detect: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        switch_controller_service_type: str | list[str] | None = ...,
        transport_protocol: Literal["udp", "tcp", "tls"] | None = ...,
        tls_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        client_cert: str | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        rsso: Literal["enable", "disable"] | None = ...,
        rsso_radius_server_port: int | None = ...,
        rsso_radius_response: Literal["enable", "disable"] | None = ...,
        rsso_validate_request_secret: Literal["enable", "disable"] | None = ...,
        rsso_secret: str | None = ...,
        rsso_endpoint_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = ...,
        rsso_endpoint_block_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = ...,
        sso_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = ...,
        sso_attribute_key: str | None = ...,
        sso_attribute_value_override: Literal["enable", "disable"] | None = ...,
        rsso_context_timeout: int | None = ...,
        rsso_log_period: int | None = ...,
        rsso_log_flags: str | list[str] | None = ...,
        rsso_flush_ip_session: Literal["enable", "disable"] | None = ...,
        rsso_ep_one_ip_only: Literal["enable", "disable"] | None = ...,
        delimiter: Literal["plus", "comma"] | None = ...,
        accounting_server: str | list[str] | list[RadiusAccountingserverItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RadiusObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: RadiusPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secret: str | None = ...,
        secondary_server: str | None = ...,
        secondary_secret: str | None = ...,
        tertiary_server: str | None = ...,
        tertiary_secret: str | None = ...,
        timeout: int | None = ...,
        status_ttl: int | None = ...,
        all_usergroup: Literal["disable", "enable"] | None = ...,
        use_management_vdom: Literal["enable", "disable"] | None = ...,
        switch_controller_nas_ip_dynamic: Literal["enable", "disable"] | None = ...,
        nas_ip: str | None = ...,
        nas_id_type: Literal["legacy", "custom", "hostname"] | None = ...,
        call_station_id_type: Literal["legacy", "IP", "MAC"] | None = ...,
        nas_id: str | None = ...,
        acct_interim_interval: int | None = ...,
        radius_coa: Literal["enable", "disable"] | None = ...,
        radius_port: int | None = ...,
        h3c_compatibility: Literal["enable", "disable"] | None = ...,
        auth_type: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        username_case_sensitive: Literal["enable", "disable"] | None = ...,
        group_override_attr_type: Literal["filter-Id", "class"] | None = ...,
        class_: str | list[str] | list[RadiusClassItem] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        require_message_authenticator: Literal["enable", "disable"] | None = ...,
        password_encoding: Literal["auto", "ISO-8859-1"] | None = ...,
        mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_case: Literal["uppercase", "lowercase"] | None = ...,
        acct_all_servers: Literal["enable", "disable"] | None = ...,
        switch_controller_acct_fast_framedip_detect: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        switch_controller_service_type: str | list[str] | None = ...,
        transport_protocol: Literal["udp", "tcp", "tls"] | None = ...,
        tls_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        client_cert: str | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        rsso: Literal["enable", "disable"] | None = ...,
        rsso_radius_server_port: int | None = ...,
        rsso_radius_response: Literal["enable", "disable"] | None = ...,
        rsso_validate_request_secret: Literal["enable", "disable"] | None = ...,
        rsso_secret: str | None = ...,
        rsso_endpoint_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = ...,
        rsso_endpoint_block_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = ...,
        sso_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = ...,
        sso_attribute_key: str | None = ...,
        sso_attribute_value_override: Literal["enable", "disable"] | None = ...,
        rsso_context_timeout: int | None = ...,
        rsso_log_period: int | None = ...,
        rsso_log_flags: str | list[str] | None = ...,
        rsso_flush_ip_session: Literal["enable", "disable"] | None = ...,
        rsso_ep_one_ip_only: Literal["enable", "disable"] | None = ...,
        delimiter: Literal["plus", "comma"] | None = ...,
        accounting_server: str | list[str] | list[RadiusAccountingserverItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RadiusObject: ...

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
        payload_dict: RadiusPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secret: str | None = ...,
        secondary_server: str | None = ...,
        secondary_secret: str | None = ...,
        tertiary_server: str | None = ...,
        tertiary_secret: str | None = ...,
        timeout: int | None = ...,
        status_ttl: int | None = ...,
        all_usergroup: Literal["disable", "enable"] | None = ...,
        use_management_vdom: Literal["enable", "disable"] | None = ...,
        switch_controller_nas_ip_dynamic: Literal["enable", "disable"] | None = ...,
        nas_ip: str | None = ...,
        nas_id_type: Literal["legacy", "custom", "hostname"] | None = ...,
        call_station_id_type: Literal["legacy", "IP", "MAC"] | None = ...,
        nas_id: str | None = ...,
        acct_interim_interval: int | None = ...,
        radius_coa: Literal["enable", "disable"] | None = ...,
        radius_port: int | None = ...,
        h3c_compatibility: Literal["enable", "disable"] | None = ...,
        auth_type: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        username_case_sensitive: Literal["enable", "disable"] | None = ...,
        group_override_attr_type: Literal["filter-Id", "class"] | None = ...,
        class_: str | list[str] | list[RadiusClassItem] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        require_message_authenticator: Literal["enable", "disable"] | None = ...,
        password_encoding: Literal["auto", "ISO-8859-1"] | None = ...,
        mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = ...,
        mac_case: Literal["uppercase", "lowercase"] | None = ...,
        acct_all_servers: Literal["enable", "disable"] | None = ...,
        switch_controller_acct_fast_framedip_detect: int | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        switch_controller_service_type: Literal["login", "framed", "callback-login", "callback-framed", "outbound", "administrative", "nas-prompt", "authenticate-only", "callback-nas-prompt", "call-check", "callback-administrative"] | list[str] | None = ...,
        transport_protocol: Literal["udp", "tcp", "tls"] | None = ...,
        tls_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        client_cert: str | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        rsso: Literal["enable", "disable"] | None = ...,
        rsso_radius_server_port: int | None = ...,
        rsso_radius_response: Literal["enable", "disable"] | None = ...,
        rsso_validate_request_secret: Literal["enable", "disable"] | None = ...,
        rsso_secret: str | None = ...,
        rsso_endpoint_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = ...,
        rsso_endpoint_block_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = ...,
        sso_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = ...,
        sso_attribute_key: str | None = ...,
        sso_attribute_value_override: Literal["enable", "disable"] | None = ...,
        rsso_context_timeout: int | None = ...,
        rsso_log_period: int | None = ...,
        rsso_log_flags: Literal["protocol-error", "profile-missing", "accounting-stop-missed", "accounting-event", "endpoint-block", "radiusd-other", "none"] | list[str] | None = ...,
        rsso_flush_ip_session: Literal["enable", "disable"] | None = ...,
        rsso_ep_one_ip_only: Literal["enable", "disable"] | None = ...,
        delimiter: Literal["plus", "comma"] | None = ...,
        accounting_server: str | list[str] | list[RadiusAccountingserverItem] | None = ...,
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
    "Radius",
    "RadiusPayload",
    "RadiusResponse",
    "RadiusObject",
]