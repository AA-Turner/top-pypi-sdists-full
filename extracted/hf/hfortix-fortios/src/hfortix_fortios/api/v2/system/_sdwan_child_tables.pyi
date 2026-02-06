"""
Child Table Helper Type Stubs for system/sdwan

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class FailAlertInterfacesDict(TypedDict, total=False):
    """Type definition for fail_alert_interfaces child table entry."""
    name: str

class ZoneDict(TypedDict, total=False):
    """Type definition for zone child table entry."""
    name: str
    advpn_select: str | None
    advpn_health_check: str | None
    service_sla_tie_break: str | None
    minimum_sla_meet_members: int | None

class MembersDict(TypedDict, total=False):
    """Type definition for members child table entry."""
    seq_num: int | None
    interface: str | None
    zone: str | None
    gateway: str | None
    preferred_source: str | None
    source: str | None
    gateway6: str | None
    source6: str | None
    cost: int | None
    weight: int | None
    priority: int | None
    priority6: int | None
    priority_in_sla: int | None
    priority_out_sla: int | None
    spillover_threshold: int | None
    ingress_spillover_threshold: int | None
    volume_ratio: int | None
    status: str | None
    transport_group: int | None
    comment: str | None

class HealthCheckDict(TypedDict, total=False):
    """Type definition for health_check child table entry."""
    name: str
    fortiguard: str | None
    fortiguard_name: str | None
    probe_packets: str | None
    addr_mode: str | None
    system_dns: str | None
    server: str | None
    detect_mode: str | None
    protocol: str | None
    port: int | None
    quality_measured_method: str | None
    security_mode: str | None
    user: str | None
    password: str | None
    packet_size: int | None
    ha_priority: int | None
    ftp_mode: str | None
    ftp_file: str | None
    http_get: str | None
    http_agent: str | None
    http_match: str | None
    dns_request_domain: str | None
    dns_match_ip: str | None
    interval: int | None
    probe_timeout: int | None
    agent_probe_timeout: int | None
    remote_probe_timeout: int | None
    failtime: int | None
    recoverytime: int | None
    probe_count: int | None
    diffservcode: str | None
    update_cascade_interface: str | None
    update_static_route: str | None
    update_bgp_route: str | None
    embed_measured_health: str | None
    sla_id_redistribute: int | None
    sla_fail_log_period: int | None
    sla_pass_log_period: int | None
    threshold_warning_packetloss: int | None
    threshold_alert_packetloss: int | None
    threshold_warning_latency: int | None
    threshold_alert_latency: int | None
    threshold_warning_jitter: int | None
    threshold_alert_jitter: int | None
    vrf: int | None
    source: str | None
    source6: str | None
    members: list[Any] | None
    mos_codec: str | None
    class_id: int | None
    packet_loss_weight: int | None
    latency_weight: int | None
    jitter_weight: int | None
    bandwidth_weight: int | None
    sla: list[Any] | None

class ServiceDict(TypedDict, total=False):
    """Type definition for service child table entry."""
    id: int
    name: str | None
    addr_mode: str | None
    load_balance: str | None
    input_device: list[Any] | None
    input_device_negate: str | None
    input_zone: list[Any] | None
    mode: str | None
    zone_mode: str | None
    minimum_sla_meet_members: int | None
    hash_mode: str | None
    shortcut_priority: str | None
    role: str | None
    standalone_action: str | None
    quality_link: int | None
    tos: str | None
    tos_mask: str | None
    protocol: int | None
    start_port: int | None
    end_port: int | None
    start_src_port: int | None
    end_src_port: int | None
    dst: list[Any] | None
    dst_negate: str | None
    src: list[Any] | None
    dst6: list[Any] | None
    src6: list[Any] | None
    src_negate: str | None
    users: list[Any] | None
    groups: list[Any] | None
    internet_service: str | None
    internet_service_custom: list[Any] | None
    internet_service_custom_group: list[Any] | None
    internet_service_fortiguard: list[Any] | None
    internet_service_name: list[Any] | None
    internet_service_group: list[Any] | None
    internet_service_app_ctrl: list[Any] | None
    internet_service_app_ctrl_group: list[Any] | None
    internet_service_app_ctrl_category: list[Any] | None
    health_check: list[Any] | None
    link_cost_factor: str | None
    packet_loss_weight: int | None
    latency_weight: int | None
    jitter_weight: int | None
    bandwidth_weight: int | None
    link_cost_threshold: int | None
    hold_down_time: int | None
    sla_stickiness: str | None
    dscp_forward: str | None
    dscp_reverse: str | None
    dscp_forward_tag: str | None
    dscp_reverse_tag: str | None
    sla: list[Any] | None
    priority_members: list[Any] | None
    priority_zone: list[Any] | None
    status: str | None
    gateway: str | None
    default: str | None
    sla_compare_method: str | None
    fib_best_match_force: str | None
    tie_break: str | None
    use_shortcut_sla: str | None
    passive_measurement: str | None
    agent_exclusive: str | None
    shortcut: str | None
    comment: str | None

class NeighborDict(TypedDict, total=False):
    """Type definition for neighbor child table entry."""
    ip: str
    member: list[Any] | None
    service_id: int | None
    minimum_sla_meet_members: int | None
    mode: str | None
    role: str | None
    route_metric: str | None
    health_check: str | None
    sla_id: int | None

class DuplicationDict(TypedDict, total=False):
    """Type definition for duplication child table entry."""
    id: int
    service_id: list[Any] | None
    srcaddr: list[Any] | None
    dstaddr: list[Any] | None
    srcaddr6: list[Any] | None
    dstaddr6: list[Any] | None
    srcintf: list[Any] | None
    dstintf: list[Any] | None
    service: list[Any] | None
    packet_duplication: str | None
    sla_match_service: str | None
    packet_de_duplication: str | None


class FailAlertInterfacesObject(FortiObject):
    """Typed FortiObject for fail_alert_interfaces child table entry with attribute access."""
    name: str


class ZoneObject(FortiObject):
    """Typed FortiObject for zone child table entry with attribute access."""
    name: str
    advpn_select: str | None
    advpn_health_check: str | None
    service_sla_tie_break: str | None
    minimum_sla_meet_members: int | None


class MembersObject(FortiObject):
    """Typed FortiObject for members child table entry with attribute access."""
    seq_num: int | None
    interface: str | None
    zone: str | None
    gateway: str | None
    preferred_source: str | None
    source: str | None
    gateway6: str | None
    source6: str | None
    cost: int | None
    weight: int | None
    priority: int | None
    priority6: int | None
    priority_in_sla: int | None
    priority_out_sla: int | None
    spillover_threshold: int | None
    ingress_spillover_threshold: int | None
    volume_ratio: int | None
    status: str | None
    transport_group: int | None
    comment: str | None


class HealthCheckObject(FortiObject):
    """Typed FortiObject for health_check child table entry with attribute access."""
    name: str
    fortiguard: str | None
    fortiguard_name: str | None
    probe_packets: str | None
    addr_mode: str | None
    system_dns: str | None
    server: str | None
    detect_mode: str | None
    protocol: str | None
    port: int | None
    quality_measured_method: str | None
    security_mode: str | None
    user: str | None
    password: str | None
    packet_size: int | None
    ha_priority: int | None
    ftp_mode: str | None
    ftp_file: str | None
    http_get: str | None
    http_agent: str | None
    http_match: str | None
    dns_request_domain: str | None
    dns_match_ip: str | None
    interval: int | None
    probe_timeout: int | None
    agent_probe_timeout: int | None
    remote_probe_timeout: int | None
    failtime: int | None
    recoverytime: int | None
    probe_count: int | None
    diffservcode: str | None
    update_cascade_interface: str | None
    update_static_route: str | None
    update_bgp_route: str | None
    embed_measured_health: str | None
    sla_id_redistribute: int | None
    sla_fail_log_period: int | None
    sla_pass_log_period: int | None
    threshold_warning_packetloss: int | None
    threshold_alert_packetloss: int | None
    threshold_warning_latency: int | None
    threshold_alert_latency: int | None
    threshold_warning_jitter: int | None
    threshold_alert_jitter: int | None
    vrf: int | None
    source: str | None
    source6: str | None
    members: list[Any] | None
    mos_codec: str | None
    class_id: int | None
    packet_loss_weight: int | None
    latency_weight: int | None
    jitter_weight: int | None
    bandwidth_weight: int | None
    sla: list[Any] | None


class ServiceObject(FortiObject):
    """Typed FortiObject for service child table entry with attribute access."""
    id: int
    name: str | None
    addr_mode: str | None
    load_balance: str | None
    input_device: list[Any] | None
    input_device_negate: str | None
    input_zone: list[Any] | None
    mode: str | None
    zone_mode: str | None
    minimum_sla_meet_members: int | None
    hash_mode: str | None
    shortcut_priority: str | None
    role: str | None
    standalone_action: str | None
    quality_link: int | None
    tos: str | None
    tos_mask: str | None
    protocol: int | None
    start_port: int | None
    end_port: int | None
    start_src_port: int | None
    end_src_port: int | None
    dst: list[Any] | None
    dst_negate: str | None
    src: list[Any] | None
    dst6: list[Any] | None
    src6: list[Any] | None
    src_negate: str | None
    users: list[Any] | None
    groups: list[Any] | None
    internet_service: str | None
    internet_service_custom: list[Any] | None
    internet_service_custom_group: list[Any] | None
    internet_service_fortiguard: list[Any] | None
    internet_service_name: list[Any] | None
    internet_service_group: list[Any] | None
    internet_service_app_ctrl: list[Any] | None
    internet_service_app_ctrl_group: list[Any] | None
    internet_service_app_ctrl_category: list[Any] | None
    health_check: list[Any] | None
    link_cost_factor: str | None
    packet_loss_weight: int | None
    latency_weight: int | None
    jitter_weight: int | None
    bandwidth_weight: int | None
    link_cost_threshold: int | None
    hold_down_time: int | None
    sla_stickiness: str | None
    dscp_forward: str | None
    dscp_reverse: str | None
    dscp_forward_tag: str | None
    dscp_reverse_tag: str | None
    sla: list[Any] | None
    priority_members: list[Any] | None
    priority_zone: list[Any] | None
    status: str | None
    gateway: str | None
    default: str | None
    sla_compare_method: str | None
    fib_best_match_force: str | None
    tie_break: str | None
    use_shortcut_sla: str | None
    passive_measurement: str | None
    agent_exclusive: str | None
    shortcut: str | None
    comment: str | None


class NeighborObject(FortiObject):
    """Typed FortiObject for neighbor child table entry with attribute access."""
    ip: str
    member: list[Any] | None
    service_id: int | None
    minimum_sla_meet_members: int | None
    mode: str | None
    role: str | None
    route_metric: str | None
    health_check: str | None
    sla_id: int | None


class DuplicationObject(FortiObject):
    """Typed FortiObject for duplication child table entry with attribute access."""
    id: int
    service_id: list[Any] | None
    srcaddr: list[Any] | None
    dstaddr: list[Any] | None
    srcaddr6: list[Any] | None
    dstaddr6: list[Any] | None
    srcintf: list[Any] | None
    dstintf: list[Any] | None
    service: list[Any] | None
    packet_duplication: str | None
    sla_match_service: str | None
    packet_de_duplication: str | None



class FailAlertInterfacesHelper:
    """Helper class for managing fail_alert_interfaces child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[FailAlertInterfacesObject] | FailAlertInterfacesObject | None: ...
    
    def set(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class ZoneHelper:
    """Helper class for managing zone child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[ZoneObject] | ZoneObject | None: ...
    
    def set(
        self,
        name: str,
        advpn_select: str | None = ...,
        advpn_health_check: str | None = ...,
        service_sla_tie_break: str | None = ...,
        minimum_sla_meet_members: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class MembersHelper:
    """Helper class for managing members child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        seq_num: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[MembersObject] | MembersObject | None: ...
    
    def set(
        self,
        seq_num: int | None = ...,
        interface: str | None = ...,
        zone: str | None = ...,
        gateway: str | None = ...,
        preferred_source: str | None = ...,
        source: str | None = ...,
        gateway6: str | None = ...,
        source6: str | None = ...,
        cost: int | None = ...,
        weight: int | None = ...,
        priority: int | None = ...,
        priority6: int | None = ...,
        priority_in_sla: int | None = ...,
        priority_out_sla: int | None = ...,
        spillover_threshold: int | None = ...,
        ingress_spillover_threshold: int | None = ...,
        volume_ratio: int | None = ...,
        status: str | None = ...,
        transport_group: int | None = ...,
        comment: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        seq_num: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        seq_num: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class HealthCheckHelper:
    """Helper class for managing health_check child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[HealthCheckObject] | HealthCheckObject | None: ...
    
    def set(
        self,
        name: str,
        fortiguard: str | None = ...,
        fortiguard_name: str | None = ...,
        probe_packets: str | None = ...,
        addr_mode: str | None = ...,
        system_dns: str | None = ...,
        server: str | None = ...,
        detect_mode: str | None = ...,
        protocol: str | None = ...,
        port: int | None = ...,
        quality_measured_method: str | None = ...,
        security_mode: str | None = ...,
        user: str | None = ...,
        password: str | None = ...,
        packet_size: int | None = ...,
        ha_priority: int | None = ...,
        ftp_mode: str | None = ...,
        ftp_file: str | None = ...,
        http_get: str | None = ...,
        http_agent: str | None = ...,
        http_match: str | None = ...,
        dns_request_domain: str | None = ...,
        dns_match_ip: str | None = ...,
        interval: int | None = ...,
        probe_timeout: int | None = ...,
        agent_probe_timeout: int | None = ...,
        remote_probe_timeout: int | None = ...,
        failtime: int | None = ...,
        recoverytime: int | None = ...,
        probe_count: int | None = ...,
        diffservcode: str | None = ...,
        update_cascade_interface: str | None = ...,
        update_static_route: str | None = ...,
        update_bgp_route: str | None = ...,
        embed_measured_health: str | None = ...,
        sla_id_redistribute: int | None = ...,
        sla_fail_log_period: int | None = ...,
        sla_pass_log_period: int | None = ...,
        threshold_warning_packetloss: int | None = ...,
        threshold_alert_packetloss: int | None = ...,
        threshold_warning_latency: int | None = ...,
        threshold_alert_latency: int | None = ...,
        threshold_warning_jitter: int | None = ...,
        threshold_alert_jitter: int | None = ...,
        vrf: int | None = ...,
        source: str | None = ...,
        source6: str | None = ...,
        members: list[Any] | None = ...,
        mos_codec: str | None = ...,
        class_id: int | None = ...,
        packet_loss_weight: int | None = ...,
        latency_weight: int | None = ...,
        jitter_weight: int | None = ...,
        bandwidth_weight: int | None = ...,
        sla: list[Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class ServiceHelper:
    """Helper class for managing service child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[ServiceObject] | ServiceObject | None: ...
    
    def set(
        self,
        id: int,
        name: str | None = ...,
        addr_mode: str | None = ...,
        load_balance: str | None = ...,
        input_device: list[Any] | None = ...,
        input_device_negate: str | None = ...,
        input_zone: list[Any] | None = ...,
        mode: str | None = ...,
        zone_mode: str | None = ...,
        minimum_sla_meet_members: int | None = ...,
        hash_mode: str | None = ...,
        shortcut_priority: str | None = ...,
        role: str | None = ...,
        standalone_action: str | None = ...,
        quality_link: int | None = ...,
        tos: str | None = ...,
        tos_mask: str | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        start_src_port: int | None = ...,
        end_src_port: int | None = ...,
        dst: list[Any] | None = ...,
        dst_negate: str | None = ...,
        src: list[Any] | None = ...,
        dst6: list[Any] | None = ...,
        src6: list[Any] | None = ...,
        src_negate: str | None = ...,
        users: list[Any] | None = ...,
        groups: list[Any] | None = ...,
        internet_service: str | None = ...,
        internet_service_custom: list[Any] | None = ...,
        internet_service_custom_group: list[Any] | None = ...,
        internet_service_fortiguard: list[Any] | None = ...,
        internet_service_name: list[Any] | None = ...,
        internet_service_group: list[Any] | None = ...,
        internet_service_app_ctrl: list[Any] | None = ...,
        internet_service_app_ctrl_group: list[Any] | None = ...,
        internet_service_app_ctrl_category: list[Any] | None = ...,
        health_check: list[Any] | None = ...,
        link_cost_factor: str | None = ...,
        packet_loss_weight: int | None = ...,
        latency_weight: int | None = ...,
        jitter_weight: int | None = ...,
        bandwidth_weight: int | None = ...,
        link_cost_threshold: int | None = ...,
        hold_down_time: int | None = ...,
        sla_stickiness: str | None = ...,
        dscp_forward: str | None = ...,
        dscp_reverse: str | None = ...,
        dscp_forward_tag: str | None = ...,
        dscp_reverse_tag: str | None = ...,
        sla: list[Any] | None = ...,
        priority_members: list[Any] | None = ...,
        priority_zone: list[Any] | None = ...,
        status: str | None = ...,
        gateway: str | None = ...,
        default: str | None = ...,
        sla_compare_method: str | None = ...,
        fib_best_match_force: str | None = ...,
        tie_break: str | None = ...,
        use_shortcut_sla: str | None = ...,
        passive_measurement: str | None = ...,
        agent_exclusive: str | None = ...,
        shortcut: str | None = ...,
        comment: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class NeighborHelper:
    """Helper class for managing neighbor child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        ip: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NeighborObject] | NeighborObject | None: ...
    
    def set(
        self,
        ip: str,
        member: list[Any] | None = ...,
        service_id: int | None = ...,
        minimum_sla_meet_members: int | None = ...,
        mode: str | None = ...,
        role: str | None = ...,
        route_metric: str | None = ...,
        health_check: str | None = ...,
        sla_id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        ip: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        ip: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class DuplicationHelper:
    """Helper class for managing duplication child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[DuplicationObject] | DuplicationObject | None: ...
    
    def set(
        self,
        id: int,
        service_id: list[Any] | None = ...,
        srcaddr: list[Any] | None = ...,
        dstaddr: list[Any] | None = ...,
        srcaddr6: list[Any] | None = ...,
        dstaddr6: list[Any] | None = ...,
        srcintf: list[Any] | None = ...,
        dstintf: list[Any] | None = ...,
        service: list[Any] | None = ...,
        packet_duplication: str | None = ...,
        sla_match_service: str | None = ...,
        packet_de_duplication: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

