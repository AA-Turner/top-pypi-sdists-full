""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/ipsec/phase2
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

class Phase2Payload(TypedDict, total=False):
    """Payload type for Phase2 operations."""
    name: str
    phase1name: str
    dhcp_ipsec: Literal["enable", "disable"]
    use_natip: Literal["enable", "disable"]
    selector_match: Literal["exact", "subset", "auto"]
    proposal: str | list[str]
    pfs: Literal["enable", "disable"]
    dhgrp: str | list[str]
    addke1: str | list[str]
    addke2: str | list[str]
    addke3: str | list[str]
    addke4: str | list[str]
    addke5: str | list[str]
    addke6: str | list[str]
    addke7: str | list[str]
    replay: Literal["enable", "disable"]
    keepalive: Literal["enable", "disable"]
    auto_negotiate: Literal["enable", "disable"]
    add_route: Literal["phase1", "enable", "disable"]
    inbound_dscp_copy: Literal["phase1", "enable", "disable"]
    keylifeseconds: int
    keylifekbs: int
    keylife_type: Literal["seconds", "kbs", "both"]
    single_source: Literal["enable", "disable"]
    route_overlap: Literal["use-old", "use-new", "allow"]
    encapsulation: Literal["tunnel-mode", "transport-mode"]
    l2tp: Literal["enable", "disable"]
    comments: str
    initiator_ts_narrow: Literal["enable", "disable"]
    diffserv: Literal["enable", "disable"]
    diffservcode: str
    protocol: int
    src_name: str
    src_name6: str
    src_addr_type: Literal["subnet", "range", "ip", "name"]
    src_start_ip: str
    src_start_ip6: str
    src_end_ip: str
    src_end_ip6: str
    src_subnet: str
    src_subnet6: str
    src_port: int
    dst_name: str
    dst_name6: str
    dst_addr_type: Literal["subnet", "range", "ip", "name"]
    dst_start_ip: str
    dst_start_ip6: str
    dst_end_ip: str
    dst_end_ip6: str
    dst_subnet: str
    dst_subnet6: str
    dst_port: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Phase2Response(TypedDict, total=False):
    """Response type for Phase2 - use with .dict property for typed dict access."""
    name: str
    phase1name: str
    dhcp_ipsec: Literal["enable", "disable"]
    use_natip: Literal["enable", "disable"]
    selector_match: Literal["exact", "subset", "auto"]
    proposal: str
    pfs: Literal["enable", "disable"]
    dhgrp: str
    addke1: str
    addke2: str
    addke3: str
    addke4: str
    addke5: str
    addke6: str
    addke7: str
    replay: Literal["enable", "disable"]
    keepalive: Literal["enable", "disable"]
    auto_negotiate: Literal["enable", "disable"]
    add_route: Literal["phase1", "enable", "disable"]
    inbound_dscp_copy: Literal["phase1", "enable", "disable"]
    keylifeseconds: int
    keylifekbs: int
    keylife_type: Literal["seconds", "kbs", "both"]
    single_source: Literal["enable", "disable"]
    route_overlap: Literal["use-old", "use-new", "allow"]
    encapsulation: Literal["tunnel-mode", "transport-mode"]
    l2tp: Literal["enable", "disable"]
    comments: str
    initiator_ts_narrow: Literal["enable", "disable"]
    diffserv: Literal["enable", "disable"]
    diffservcode: str
    protocol: int
    src_name: str
    src_name6: str
    src_addr_type: Literal["subnet", "range", "ip", "name"]
    src_start_ip: str
    src_start_ip6: str
    src_end_ip: str
    src_end_ip6: str
    src_subnet: str
    src_subnet6: str
    src_port: int
    dst_name: str
    dst_name6: str
    dst_addr_type: Literal["subnet", "range", "ip", "name"]
    dst_start_ip: str
    dst_start_ip6: str
    dst_end_ip: str
    dst_end_ip6: str
    dst_subnet: str
    dst_subnet6: str
    dst_port: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Phase2Object(FortiObject):
    """Typed FortiObject for Phase2 with field access."""
    name: str
    phase1name: str
    dhcp_ipsec: Literal["enable", "disable"]
    use_natip: Literal["enable", "disable"]
    selector_match: Literal["exact", "subset", "auto"]
    proposal: str
    pfs: Literal["enable", "disable"]
    dhgrp: str
    addke1: str
    addke2: str
    addke3: str
    addke4: str
    addke5: str
    addke6: str
    addke7: str
    replay: Literal["enable", "disable"]
    keepalive: Literal["enable", "disable"]
    auto_negotiate: Literal["enable", "disable"]
    add_route: Literal["phase1", "enable", "disable"]
    inbound_dscp_copy: Literal["phase1", "enable", "disable"]
    keylifeseconds: int
    keylifekbs: int
    keylife_type: Literal["seconds", "kbs", "both"]
    single_source: Literal["enable", "disable"]
    route_overlap: Literal["use-old", "use-new", "allow"]
    encapsulation: Literal["tunnel-mode", "transport-mode"]
    l2tp: Literal["enable", "disable"]
    comments: str
    initiator_ts_narrow: Literal["enable", "disable"]
    diffserv: Literal["enable", "disable"]
    diffservcode: str
    protocol: int
    src_name: str
    src_name6: str
    src_addr_type: Literal["subnet", "range", "ip", "name"]
    src_start_ip: str
    src_start_ip6: str
    src_end_ip: str
    src_end_ip6: str
    src_subnet: str
    src_subnet6: str
    src_port: int
    dst_name: str
    dst_name6: str
    dst_addr_type: Literal["subnet", "range", "ip", "name"]
    dst_start_ip: str
    dst_start_ip6: str
    dst_end_ip: str
    dst_end_ip6: str
    dst_subnet: str
    dst_subnet6: str
    dst_port: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Phase2:
    """
    
    Endpoint: vpn/ipsec/phase2
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
    ) -> Phase2Object: ...
    
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
    ) -> FortiObjectList[Phase2Object]: ...
    
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
        payload_dict: Phase2Payload | None = ...,
        name: str | None = ...,
        phase1name: str | None = ...,
        dhcp_ipsec: Literal["enable", "disable"] | None = ...,
        use_natip: Literal["enable", "disable"] | None = ...,
        selector_match: Literal["exact", "subset", "auto"] | None = ...,
        proposal: str | list[str] | None = ...,
        pfs: Literal["enable", "disable"] | None = ...,
        dhgrp: str | list[str] | None = ...,
        addke1: str | list[str] | None = ...,
        addke2: str | list[str] | None = ...,
        addke3: str | list[str] | None = ...,
        addke4: str | list[str] | None = ...,
        addke5: str | list[str] | None = ...,
        addke6: str | list[str] | None = ...,
        addke7: str | list[str] | None = ...,
        replay: Literal["enable", "disable"] | None = ...,
        keepalive: Literal["enable", "disable"] | None = ...,
        auto_negotiate: Literal["enable", "disable"] | None = ...,
        add_route: Literal["phase1", "enable", "disable"] | None = ...,
        inbound_dscp_copy: Literal["phase1", "enable", "disable"] | None = ...,
        keylifeseconds: int | None = ...,
        keylifekbs: int | None = ...,
        keylife_type: Literal["seconds", "kbs", "both"] | None = ...,
        single_source: Literal["enable", "disable"] | None = ...,
        route_overlap: Literal["use-old", "use-new", "allow"] | None = ...,
        encapsulation: Literal["tunnel-mode", "transport-mode"] | None = ...,
        l2tp: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        initiator_ts_narrow: Literal["enable", "disable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        protocol: int | None = ...,
        src_name: str | None = ...,
        src_name6: str | None = ...,
        src_addr_type: Literal["subnet", "range", "ip", "name"] | None = ...,
        src_start_ip: str | None = ...,
        src_start_ip6: str | None = ...,
        src_end_ip: str | None = ...,
        src_end_ip6: str | None = ...,
        src_subnet: str | None = ...,
        src_subnet6: str | None = ...,
        src_port: int | None = ...,
        dst_name: str | None = ...,
        dst_name6: str | None = ...,
        dst_addr_type: Literal["subnet", "range", "ip", "name"] | None = ...,
        dst_start_ip: str | None = ...,
        dst_start_ip6: str | None = ...,
        dst_end_ip: str | None = ...,
        dst_end_ip6: str | None = ...,
        dst_subnet: str | None = ...,
        dst_subnet6: str | None = ...,
        dst_port: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Phase2Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Phase2Payload | None = ...,
        name: str | None = ...,
        phase1name: str | None = ...,
        dhcp_ipsec: Literal["enable", "disable"] | None = ...,
        use_natip: Literal["enable", "disable"] | None = ...,
        selector_match: Literal["exact", "subset", "auto"] | None = ...,
        proposal: str | list[str] | None = ...,
        pfs: Literal["enable", "disable"] | None = ...,
        dhgrp: str | list[str] | None = ...,
        addke1: str | list[str] | None = ...,
        addke2: str | list[str] | None = ...,
        addke3: str | list[str] | None = ...,
        addke4: str | list[str] | None = ...,
        addke5: str | list[str] | None = ...,
        addke6: str | list[str] | None = ...,
        addke7: str | list[str] | None = ...,
        replay: Literal["enable", "disable"] | None = ...,
        keepalive: Literal["enable", "disable"] | None = ...,
        auto_negotiate: Literal["enable", "disable"] | None = ...,
        add_route: Literal["phase1", "enable", "disable"] | None = ...,
        inbound_dscp_copy: Literal["phase1", "enable", "disable"] | None = ...,
        keylifeseconds: int | None = ...,
        keylifekbs: int | None = ...,
        keylife_type: Literal["seconds", "kbs", "both"] | None = ...,
        single_source: Literal["enable", "disable"] | None = ...,
        route_overlap: Literal["use-old", "use-new", "allow"] | None = ...,
        encapsulation: Literal["tunnel-mode", "transport-mode"] | None = ...,
        l2tp: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        initiator_ts_narrow: Literal["enable", "disable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        protocol: int | None = ...,
        src_name: str | None = ...,
        src_name6: str | None = ...,
        src_addr_type: Literal["subnet", "range", "ip", "name"] | None = ...,
        src_start_ip: str | None = ...,
        src_start_ip6: str | None = ...,
        src_end_ip: str | None = ...,
        src_end_ip6: str | None = ...,
        src_subnet: str | None = ...,
        src_subnet6: str | None = ...,
        src_port: int | None = ...,
        dst_name: str | None = ...,
        dst_name6: str | None = ...,
        dst_addr_type: Literal["subnet", "range", "ip", "name"] | None = ...,
        dst_start_ip: str | None = ...,
        dst_start_ip6: str | None = ...,
        dst_end_ip: str | None = ...,
        dst_end_ip6: str | None = ...,
        dst_subnet: str | None = ...,
        dst_subnet6: str | None = ...,
        dst_port: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Phase2Object: ...

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
        payload_dict: Phase2Payload | None = ...,
        name: str | None = ...,
        phase1name: str | None = ...,
        dhcp_ipsec: Literal["enable", "disable"] | None = ...,
        use_natip: Literal["enable", "disable"] | None = ...,
        selector_match: Literal["exact", "subset", "auto"] | None = ...,
        proposal: Literal["null-md5", "null-sha1", "null-sha256", "null-sha384", "null-sha512", "des-null", "des-md5", "des-sha1", "des-sha256", "des-sha384", "des-sha512", "3des-null", "3des-md5", "3des-sha1", "3des-sha256", "3des-sha384", "3des-sha512", "aes128-null", "aes128-md5", "aes128-sha1", "aes128-sha256", "aes128-sha384", "aes128-sha512", "aes128gcm", "aes192-null", "aes192-md5", "aes192-sha1", "aes192-sha256", "aes192-sha384", "aes192-sha512", "aes256-null", "aes256-md5", "aes256-sha1", "aes256-sha256", "aes256-sha384", "aes256-sha512", "aes256gcm", "chacha20poly1305", "aria128-null", "aria128-md5", "aria128-sha1", "aria128-sha256", "aria128-sha384", "aria128-sha512", "aria192-null", "aria192-md5", "aria192-sha1", "aria192-sha256", "aria192-sha384", "aria192-sha512", "aria256-null", "aria256-md5", "aria256-sha1", "aria256-sha256", "aria256-sha384", "aria256-sha512", "seed-null", "seed-md5", "seed-sha1", "seed-sha256", "seed-sha384", "seed-sha512"] | list[str] | None = ...,
        pfs: Literal["enable", "disable"] | None = ...,
        dhgrp: Literal["1", "2", "5", "14", "15", "16", "17", "18", "19", "20", "21", "27", "28", "29", "30", "31", "32"] | list[str] | None = ...,
        addke1: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke2: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke3: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke4: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke5: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke6: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        addke7: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = ...,
        replay: Literal["enable", "disable"] | None = ...,
        keepalive: Literal["enable", "disable"] | None = ...,
        auto_negotiate: Literal["enable", "disable"] | None = ...,
        add_route: Literal["phase1", "enable", "disable"] | None = ...,
        inbound_dscp_copy: Literal["phase1", "enable", "disable"] | None = ...,
        keylifeseconds: int | None = ...,
        keylifekbs: int | None = ...,
        keylife_type: Literal["seconds", "kbs", "both"] | None = ...,
        single_source: Literal["enable", "disable"] | None = ...,
        route_overlap: Literal["use-old", "use-new", "allow"] | None = ...,
        encapsulation: Literal["tunnel-mode", "transport-mode"] | None = ...,
        l2tp: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        initiator_ts_narrow: Literal["enable", "disable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        protocol: int | None = ...,
        src_name: str | None = ...,
        src_name6: str | None = ...,
        src_addr_type: Literal["subnet", "range", "ip", "name"] | None = ...,
        src_start_ip: str | None = ...,
        src_start_ip6: str | None = ...,
        src_end_ip: str | None = ...,
        src_end_ip6: str | None = ...,
        src_subnet: str | None = ...,
        src_subnet6: str | None = ...,
        src_port: int | None = ...,
        dst_name: str | None = ...,
        dst_name6: str | None = ...,
        dst_addr_type: Literal["subnet", "range", "ip", "name"] | None = ...,
        dst_start_ip: str | None = ...,
        dst_start_ip6: str | None = ...,
        dst_end_ip: str | None = ...,
        dst_end_ip6: str | None = ...,
        dst_subnet: str | None = ...,
        dst_subnet6: str | None = ...,
        dst_port: int | None = ...,
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
    "Phase2",
    "Phase2Payload",
    "Phase2Response",
    "Phase2Object",
]