"""
Pydantic Models for CMDB - router/bgp

Runtime validation models for router/bgp configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class BgpNeighborGroupCapabilityOrfEnum(str, Enum):
    """Allowed values for capability_orf field in neighbor-group."""
    NONE = "none"
    RECEIVE = "receive"
    SEND = "send"
    BOTH = "both"

class BgpNeighborGroupCapabilityOrf6Enum(str, Enum):
    """Allowed values for capability_orf6 field in neighbor-group."""
    NONE = "none"
    RECEIVE = "receive"
    SEND = "send"
    BOTH = "both"

class BgpNeighborGroupSendCommunityEnum(str, Enum):
    """Allowed values for send_community field in neighbor-group."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborGroupSendCommunity6Enum(str, Enum):
    """Allowed values for send_community6 field in neighbor-group."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborGroupSendCommunityVpnv4Enum(str, Enum):
    """Allowed values for send_community_vpnv4 field in neighbor-group."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborGroupSendCommunityVpnv6Enum(str, Enum):
    """Allowed values for send_community_vpnv6 field in neighbor-group."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborGroupSendCommunityEvpnEnum(str, Enum):
    """Allowed values for send_community_evpn field in neighbor-group."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborGroupAdditionalPathEnum(str, Enum):
    """Allowed values for additional_path field in neighbor-group."""
    SEND = "send"
    RECEIVE = "receive"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborGroupAdditionalPath6Enum(str, Enum):
    """Allowed values for additional_path6 field in neighbor-group."""
    SEND = "send"
    RECEIVE = "receive"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborGroupAdditionalPathVpnv4Enum(str, Enum):
    """Allowed values for additional_path_vpnv4 field in neighbor-group."""
    SEND = "send"
    RECEIVE = "receive"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborGroupAdditionalPathVpnv6Enum(str, Enum):
    """Allowed values for additional_path_vpnv6 field in neighbor-group."""
    SEND = "send"
    RECEIVE = "receive"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborCapabilityOrfEnum(str, Enum):
    """Allowed values for capability_orf field in neighbor."""
    NONE = "none"
    RECEIVE = "receive"
    SEND = "send"
    BOTH = "both"

class BgpNeighborCapabilityOrf6Enum(str, Enum):
    """Allowed values for capability_orf6 field in neighbor."""
    NONE = "none"
    RECEIVE = "receive"
    SEND = "send"
    BOTH = "both"

class BgpNeighborSendCommunityEnum(str, Enum):
    """Allowed values for send_community field in neighbor."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborSendCommunity6Enum(str, Enum):
    """Allowed values for send_community6 field in neighbor."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborSendCommunityVpnv4Enum(str, Enum):
    """Allowed values for send_community_vpnv4 field in neighbor."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborSendCommunityVpnv6Enum(str, Enum):
    """Allowed values for send_community_vpnv6 field in neighbor."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborSendCommunityEvpnEnum(str, Enum):
    """Allowed values for send_community_evpn field in neighbor."""
    STANDARD = "standard"
    EXTENDED = "extended"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborAdditionalPathEnum(str, Enum):
    """Allowed values for additional_path field in neighbor."""
    SEND = "send"
    RECEIVE = "receive"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborAdditionalPath6Enum(str, Enum):
    """Allowed values for additional_path6 field in neighbor."""
    SEND = "send"
    RECEIVE = "receive"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborAdditionalPathVpnv4Enum(str, Enum):
    """Allowed values for additional_path_vpnv4 field in neighbor."""
    SEND = "send"
    RECEIVE = "receive"
    BOTH = "both"
    DISABLE = "disable"

class BgpNeighborAdditionalPathVpnv6Enum(str, Enum):
    """Allowed values for additional_path_vpnv6 field in neighbor."""
    SEND = "send"
    RECEIVE = "receive"
    BOTH = "both"
    DISABLE = "disable"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class BgpVrf6LeakTarget(BaseModel):
    """
    Child table model for vrf6.leak-target.
    
    Target VRF table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vrf: str | None = Field(max_length=7, default=None, description="Target VRF ID <0-511>.")    
    route_map: str = Field(max_length=35, description="Route map of VRF leaking.")  # datasource: ['router.route-map.name']    
    interface: str = Field(max_length=15, description="Interface which is used to leak routes to target VRF.")  # datasource: ['system.interface.name']
class BgpVrf6ImportRt(BaseModel):
    """
    Child table model for vrf6.import-rt.
    
    List of import route target.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    route_target: str | None = Field(max_length=79, default=None, description="Attribute: AA:NN|A.B.C.D:NN")
class BgpVrf6ExportRt(BaseModel):
    """
    Child table model for vrf6.export-rt.
    
    List of export route target.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    route_target: str | None = Field(max_length=79, default=None, description="Attribute: AA:NN|A.B.C.D:NN.")
class BgpVrf6(BaseModel):
    """
    Child table model for vrf6.
    
    BGP IPv6 VRF leaking table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vrf: str | None = Field(max_length=7, default=None, description="Origin VRF ID <0-511>.")    
    role: Literal["standalone", "ce", "pe"] | None = Field(default="standalone", description="VRF role.")    
    rd: str | None = Field(max_length=79, default=None, description="Route Distinguisher: AA:NN|A.B.C.D:NN.")    
    export_rt: list[BgpVrf6ExportRt] = Field(default_factory=list, description="List of export route target.")    
    import_rt: list[BgpVrf6ImportRt] = Field(default_factory=list, description="List of import route target.")    
    import_route_map: str | None = Field(max_length=35, default=None, description="Import route map.")  # datasource: ['router.route-map.name']    
    leak_target: list[BgpVrf6LeakTarget] = Field(default_factory=list, description="Target VRF table.")
class BgpVrfLeakTarget(BaseModel):
    """
    Child table model for vrf.leak-target.
    
    Target VRF table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vrf: str | None = Field(max_length=7, default=None, description="Target VRF ID <0-511>.")    
    route_map: str = Field(max_length=35, description="Route map of VRF leaking.")  # datasource: ['router.route-map.name']    
    interface: str = Field(max_length=15, description="Interface which is used to leak routes to target VRF.")  # datasource: ['system.interface.name']
class BgpVrfImportRt(BaseModel):
    """
    Child table model for vrf.import-rt.
    
    List of import route target.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    route_target: str | None = Field(max_length=79, default=None, description="Attribute: AA:NN|A.B.C.D:NN")
class BgpVrfExportRt(BaseModel):
    """
    Child table model for vrf.export-rt.
    
    List of export route target.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    route_target: str | None = Field(max_length=79, default=None, description="Attribute: AA:NN|A.B.C.D:NN.")
class BgpVrf(BaseModel):
    """
    Child table model for vrf.
    
    BGP VRF leaking table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vrf: str | None = Field(max_length=7, default=None, description="Origin VRF ID <0-511>.")    
    role: Literal["standalone", "ce", "pe"] | None = Field(default="standalone", description="VRF role.")    
    rd: str | None = Field(max_length=79, default=None, description="Route Distinguisher: AA:NN|A.B.C.D:NN.")    
    export_rt: list[BgpVrfExportRt] = Field(default_factory=list, description="List of export route target.")    
    import_rt: list[BgpVrfImportRt] = Field(default_factory=list, description="List of import route target.")    
    import_route_map: str | None = Field(max_length=35, default=None, description="Import route map.")  # datasource: ['router.route-map.name']    
    leak_target: list[BgpVrfLeakTarget] = Field(default_factory=list, description="Target VRF table.")
class BgpRedistribute6(BaseModel):
    """
    Child table model for redistribute6.
    
    BGP IPv6 redistribute table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Distribute list entry name.")    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Status.")    
    route_map: str | None = Field(max_length=35, default=None, description="Route map name.")  # datasource: ['router.route-map.name']
class BgpRedistribute(BaseModel):
    """
    Child table model for redistribute.
    
    BGP IPv4 redistribute table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Distribute list entry name.")    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Status.")    
    route_map: str | None = Field(max_length=35, default=None, description="Route map name.")  # datasource: ['router.route-map.name']
class BgpNetwork6(BaseModel):
    """
    Child table model for network6.
    
    BGP IPv6 network table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    prefix6: str = Field(default="::/0", description="Network IPv6 prefix.")    
    network_import_check: Literal["global", "enable", "disable"] | None = Field(default="global", description="Configure insurance of BGP network route existence in IGP.")    
    backdoor: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable route as backdoor.")    
    route_map: str | None = Field(max_length=35, default=None, description="Route map to modify generated route.")  # datasource: ['router.route-map.name']
class BgpNetwork(BaseModel):
    """
    Child table model for network.
    
    BGP network table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    prefix: str = Field(default="0.0.0.0 0.0.0.0", description="Network prefix.")    
    network_import_check: Literal["global", "enable", "disable"] | None = Field(default="global", description="Configure insurance of BGP network route existence in IGP.")    
    backdoor: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable route as backdoor.")    
    route_map: str | None = Field(max_length=35, default=None, description="Route map to modify generated route.")  # datasource: ['router.route-map.name']    
    prefix_name: str | None = Field(max_length=79, default=None, description="Name of firewall address or address group.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']
class BgpNeighborConditionalAdvertise6ConditionRoutemap(BaseModel):
    """
    Child table model for neighbor.conditional-advertise6.condition-routemap.
    
    List of conditional route maps.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Route map.")  # datasource: ['router.route-map.name']
class BgpNeighborConditionalAdvertise6(BaseModel):
    """
    Child table model for neighbor.conditional-advertise6.
    
    IPv6 conditional advertisement.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    advertise_routemap: str = Field(max_length=35, description="Name of advertising route map.")  # datasource: ['router.route-map.name']    
    condition_routemap: list[BgpNeighborConditionalAdvertise6ConditionRoutemap] = Field(description="List of conditional route maps.")    
    condition_type: Literal["exist", "non-exist"] | None = Field(default="exist", description="Type of condition.")
class BgpNeighborConditionalAdvertiseConditionRoutemap(BaseModel):
    """
    Child table model for neighbor.conditional-advertise.condition-routemap.
    
    List of conditional route maps.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Route map.")  # datasource: ['router.route-map.name']
class BgpNeighborConditionalAdvertise(BaseModel):
    """
    Child table model for neighbor.conditional-advertise.
    
    Conditional advertisement.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    advertise_routemap: str = Field(max_length=35, description="Name of advertising route map.")  # datasource: ['router.route-map.name']    
    condition_routemap: list[BgpNeighborConditionalAdvertiseConditionRoutemap] = Field(description="List of conditional route maps.")    
    condition_type: Literal["exist", "non-exist"] | None = Field(default="exist", description="Type of condition.")
class BgpNeighborRange6(BaseModel):
    """
    Child table model for neighbor-range6.
    
    BGP IPv6 neighbor range table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="IPv6 neighbor range ID.")    
    prefix6: str = Field(default="::/0", description="IPv6 prefix.")    
    max_neighbor_num: int | None = Field(ge=1, le=1000, default=0, description="Maximum number of neighbors.")    
    neighbor_group: str = Field(max_length=63, description="Neighbor group name.")  # datasource: ['router.bgp.neighbor-group.name']
class BgpNeighborRange(BaseModel):
    """
    Child table model for neighbor-range.
    
    BGP neighbor range table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Neighbor range ID.")    
    prefix: str = Field(default="0.0.0.0 0.0.0.0", description="Neighbor range prefix.")    
    max_neighbor_num: int | None = Field(ge=1, le=1000, default=0, description="Maximum number of neighbors.")    
    neighbor_group: str = Field(max_length=63, description="Neighbor group name.")  # datasource: ['router.bgp.neighbor-group.name']
class BgpNeighborGroup(BaseModel):
    """
    Child table model for neighbor-group.
    
    BGP neighbor group table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=45, description="Neighbor group name.")    
    advertisement_interval: int | None = Field(ge=0, le=600, default=30, description="Minimum interval (sec) between sending updates.")    
    allowas_in_enable: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 Enable to allow my AS in AS path.")    
    allowas_in_enable6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 Enable to allow my AS in AS path.")    
    allowas_in_enable_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable to allow my AS in AS path for VPNv4 route.")    
    allowas_in_enable_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable use of my AS in AS path for VPNv6 route.")    
    allowas_in_enable_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable to allow my AS in AS path for L2VPN EVPN route.")    
    allowas_in: int | None = Field(ge=1, le=10, default=3, description="IPv4 The maximum number of occurrence of my AS number allowed.")    
    allowas_in6: int | None = Field(ge=1, le=10, default=3, description="IPv6 The maximum number of occurrence of my AS number allowed.")    
    allowas_in_vpnv4: int | None = Field(ge=1, le=10, default=3, description="The maximum number of occurrence of my AS number allowed for VPNv4 route.")    
    allowas_in_vpnv6: int | None = Field(ge=1, le=10, default=3, description="The maximum number of occurrence of my AS number allowed for VPNv6 route.")    
    allowas_in_evpn: int | None = Field(ge=1, le=10, default=3, description="The maximum number of occurrence of my AS number allowed for L2VPN EVPN route.")    
    attribute_unchanged: list[Literal["as-path", "med", "next-hop"]] = Field(default_factory=list, description="IPv4 List of attributes that should be unchanged.")    
    attribute_unchanged6: list[Literal["as-path", "med", "next-hop"]] = Field(default_factory=list, description="IPv6 List of attributes that should be unchanged.")    
    attribute_unchanged_vpnv4: list[Literal["as-path", "med", "next-hop"]] = Field(default_factory=list, description="List of attributes that should be unchanged for VPNv4 route.")    
    attribute_unchanged_vpnv6: list[Literal["as-path", "med", "next-hop"]] = Field(default_factory=list, description="List of attributes that should not be changed for VPNv6 route.")    
    activate: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family IPv4 for this neighbor.")    
    activate6: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family IPv6 for this neighbor.")    
    activate_vpnv4: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family VPNv4 for this neighbor.")    
    activate_vpnv6: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family VPNv6 for this neighbor.")    
    activate_evpn: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family L2VPN EVPN for this neighbor.")    
    bfd: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable BFD for this neighbor.")    
    capability_dynamic: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise dynamic capability to this neighbor.")    
    capability_orf: BgpNeighborGroupCapabilityOrfEnum | None = Field(default=BgpNeighborGroupCapabilityOrfEnum.NONE, description="Accept/Send IPv4 ORF lists to/from this neighbor.")    
    capability_orf6: BgpNeighborGroupCapabilityOrf6Enum | None = Field(default=BgpNeighborGroupCapabilityOrf6Enum.NONE, description="Accept/Send IPv6 ORF lists to/from this neighbor.")    
    capability_graceful_restart: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise IPv4 graceful restart capability to this neighbor.")    
    capability_graceful_restart6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise IPv6 graceful restart capability to this neighbor.")    
    capability_graceful_restart_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise VPNv4 graceful restart capability to this neighbor.")    
    capability_graceful_restart_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertisement of VPNv6 graceful restart capability to this neighbor.")    
    capability_graceful_restart_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertisement of L2VPN EVPN graceful restart capability to this neighbor.")    
    capability_route_refresh: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable advertise route refresh capability to this neighbor.")    
    capability_default_originate: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise default IPv4 route to this neighbor.")    
    capability_default_originate6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise default IPv6 route to this neighbor.")    
    dont_capability_negotiate: Literal["enable", "disable"] | None = Field(default="disable", description="Do not negotiate capabilities with this neighbor.")    
    ebgp_enforce_multihop: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allow multi-hop EBGP neighbors.")    
    link_down_failover: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable failover upon link down.")    
    stale_route: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable stale route after neighbor down.")    
    next_hop_self: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 next-hop calculation for this neighbor.")    
    next_hop_self6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 next-hop calculation for this neighbor.")    
    next_hop_self_rr: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable setting nexthop's address to interface's IPv4 address for route-reflector routes.")    
    next_hop_self_rr6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable setting nexthop's address to interface's IPv6 address for route-reflector routes.")    
    next_hop_self_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable setting VPNv4 next-hop to interface's IP address for this neighbor.")    
    next_hop_self_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable use of outgoing interface's IP address as VPNv6 next-hop for this neighbor.")    
    override_capability: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable override result of capability negotiation.")    
    passive: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sending of open messages to this neighbor.")    
    remove_private_as: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable remove private AS number from IPv4 outbound updates.")    
    remove_private_as6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable remove private AS number from IPv6 outbound updates.")    
    remove_private_as_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable remove private AS number from VPNv4 outbound updates.")    
    remove_private_as_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable to remove private AS number from VPNv6 outbound updates.")    
    remove_private_as_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable removing private AS number from L2VPN EVPN outbound updates.")    
    route_reflector_client: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 AS route reflector client.")    
    route_reflector_client6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 AS route reflector client.")    
    route_reflector_client_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv4 AS route reflector client for this neighbor.")    
    route_reflector_client_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv6 AS route reflector client for this neighbor.")    
    route_reflector_client_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable L2VPN EVPN AS route reflector client for this neighbor.")    
    route_server_client: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 AS route server client.")    
    route_server_client6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 AS route server client.")    
    route_server_client_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv4 AS route server client for this neighbor.")    
    route_server_client_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv6 AS route server client for this neighbor.")    
    route_server_client_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable L2VPN EVPN AS route server client for this neighbor.")    
    rr_attr_allow_change: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to IPv4 route reflector clients.")    
    rr_attr_allow_change6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to IPv6 route reflector clients.")    
    rr_attr_allow_change_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to VPNv4 route reflector clients.")    
    rr_attr_allow_change_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to VPNv6 route reflector clients.")    
    rr_attr_allow_change_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to L2VPN EVPN route reflector clients.")    
    shutdown: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable shutdown this neighbor.")    
    soft_reconfiguration: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allow IPv4 inbound soft reconfiguration.")    
    soft_reconfiguration6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allow IPv6 inbound soft reconfiguration.")    
    soft_reconfiguration_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allow VPNv4 inbound soft reconfiguration.")    
    soft_reconfiguration_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv6 inbound soft reconfiguration.")    
    soft_reconfiguration_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable L2VPN EVPN inbound soft reconfiguration.")    
    as_override: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable replace peer AS with own AS for IPv4.")    
    as_override6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable replace peer AS with own AS for IPv6.")    
    strict_capability_match: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable strict capability matching.")    
    default_originate_routemap: str | None = Field(max_length=35, default=None, description="Route map to specify criteria to originate IPv4 default.")  # datasource: ['router.route-map.name']    
    default_originate_routemap6: str | None = Field(max_length=35, default=None, description="Route map to specify criteria to originate IPv6 default.")  # datasource: ['router.route-map.name']    
    description: str | None = Field(max_length=63, default=None, description="Description.")    
    distribute_list_in: str | None = Field(max_length=35, default=None, description="Filter for IPv4 updates from this neighbor.")  # datasource: ['router.access-list.name']    
    distribute_list_in6: str | None = Field(max_length=35, default=None, description="Filter for IPv6 updates from this neighbor.")  # datasource: ['router.access-list6.name']    
    distribute_list_in_vpnv4: str | None = Field(max_length=35, default=None, description="Filter for VPNv4 updates from this neighbor.")  # datasource: ['router.access-list.name']    
    distribute_list_in_vpnv6: str | None = Field(max_length=35, default=None, description="Filter for VPNv6 updates from this neighbor.")  # datasource: ['router.access-list6.name']    
    distribute_list_out: str | None = Field(max_length=35, default=None, description="Filter for IPv4 updates to this neighbor.")  # datasource: ['router.access-list.name']    
    distribute_list_out6: str | None = Field(max_length=35, default=None, description="Filter for IPv6 updates to this neighbor.")  # datasource: ['router.access-list6.name']    
    distribute_list_out_vpnv4: str | None = Field(max_length=35, default=None, description="Filter for VPNv4 updates to this neighbor.")  # datasource: ['router.access-list.name']    
    distribute_list_out_vpnv6: str | None = Field(max_length=35, default=None, description="Filter for VPNv6 updates to this neighbor.")  # datasource: ['router.access-list6.name']    
    ebgp_multihop_ttl: int | None = Field(ge=1, le=255, default=255, description="EBGP multihop TTL for this peer.")    
    filter_list_in: str | None = Field(max_length=35, default=None, description="BGP filter for IPv4 inbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_in6: str | None = Field(max_length=35, default=None, description="BGP filter for IPv6 inbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_in_vpnv4: str | None = Field(max_length=35, default=None, description="BGP filter for VPNv4 inbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_in_vpnv6: str | None = Field(max_length=35, default=None, description="BGP filter for VPNv6 inbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_out: str | None = Field(max_length=35, default=None, description="BGP filter for IPv4 outbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_out6: str | None = Field(max_length=35, default=None, description="BGP filter for IPv6 outbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_out_vpnv4: str | None = Field(max_length=35, default=None, description="BGP filter for VPNv4 outbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_out_vpnv6: str | None = Field(max_length=35, default=None, description="BGP filter for VPNv6 outbound routes.")  # datasource: ['router.aspath-list.name']    
    interface: str | None = Field(max_length=15, default=None, description="Specify outgoing interface for peer connection. For IPv6 peer, the interface should have link-local address.")  # datasource: ['system.interface.name']    
    maximum_prefix: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of IPv4 prefixes to accept from this peer.")    
    maximum_prefix6: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of IPv6 prefixes to accept from this peer.")    
    maximum_prefix_vpnv4: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of VPNv4 prefixes to accept from this peer.")    
    maximum_prefix_vpnv6: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of VPNv6 prefixes to accept from this peer.")    
    maximum_prefix_evpn: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of L2VPN EVPN prefixes to accept from this peer.")    
    maximum_prefix_threshold: int | None = Field(ge=1, le=100, default=75, description="Maximum IPv4 prefix threshold value (1 - 100 percent).")    
    maximum_prefix_threshold6: int | None = Field(ge=1, le=100, default=75, description="Maximum IPv6 prefix threshold value (1 - 100 percent).")    
    maximum_prefix_threshold_vpnv4: int | None = Field(ge=1, le=100, default=75, description="Maximum VPNv4 prefix threshold value (1 - 100 percent).")    
    maximum_prefix_threshold_vpnv6: int | None = Field(ge=1, le=100, default=75, description="Maximum VPNv6 prefix threshold value (1 - 100 percent).")    
    maximum_prefix_threshold_evpn: int | None = Field(ge=1, le=100, default=75, description="Maximum L2VPN EVPN prefix threshold value (1 - 100 percent).")    
    maximum_prefix_warning_only: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 Only give warning message when limit is exceeded.")    
    maximum_prefix_warning_only6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 Only give warning message when limit is exceeded.")    
    maximum_prefix_warning_only_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable only giving warning message when limit is exceeded for VPNv4 routes.")    
    maximum_prefix_warning_only_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable warning message when limit is exceeded for VPNv6 routes.")    
    maximum_prefix_warning_only_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable only sending warning message when exceeding limit of L2VPN EVPN routes.")    
    prefix_list_in: str | None = Field(max_length=35, default=None, description="IPv4 Inbound filter for updates from this neighbor.")  # datasource: ['router.prefix-list.name']    
    prefix_list_in6: str | None = Field(max_length=35, default=None, description="IPv6 Inbound filter for updates from this neighbor.")  # datasource: ['router.prefix-list6.name']    
    prefix_list_in_vpnv4: str | None = Field(max_length=35, default=None, description="Inbound filter for VPNv4 updates from this neighbor.")  # datasource: ['router.prefix-list.name']    
    prefix_list_in_vpnv6: str | None = Field(max_length=35, default=None, description="Inbound filter for VPNv6 updates from this neighbor.")  # datasource: ['router.prefix-list6.name']    
    prefix_list_out: str | None = Field(max_length=35, default=None, description="IPv4 Outbound filter for updates to this neighbor.")  # datasource: ['router.prefix-list.name']    
    prefix_list_out6: str | None = Field(max_length=35, default=None, description="IPv6 Outbound filter for updates to this neighbor.")  # datasource: ['router.prefix-list6.name']    
    prefix_list_out_vpnv4: str | None = Field(max_length=35, default=None, description="Outbound filter for VPNv4 updates to this neighbor.")  # datasource: ['router.prefix-list.name']    
    prefix_list_out_vpnv6: str | None = Field(max_length=35, default=None, description="Outbound filter for VPNv6 updates to this neighbor.")  # datasource: ['router.prefix-list6.name']    
    remote_as: str = Field(description="AS number of neighbor.")    
    remote_as_filter: str = Field(max_length=35, description="BGP filter for remote AS.")  # datasource: ['router.aspath-list.name']    
    local_as: str | None = Field(default=None, description="Local AS number of neighbor.")    
    local_as_no_prepend: Literal["enable", "disable"] | None = Field(default="disable", description="Do not prepend local-as to incoming updates.")    
    local_as_replace_as: Literal["enable", "disable"] | None = Field(default="disable", description="Replace real AS with local-as in outgoing updates.")    
    retain_stale_time: int | None = Field(ge=0, le=65535, default=0, description="Time to retain stale routes.")    
    route_map_in: str | None = Field(max_length=35, default=None, description="IPv4 Inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_in6: str | None = Field(max_length=35, default=None, description="IPv6 Inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_in_vpnv4: str | None = Field(max_length=35, default=None, description="VPNv4 inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_in_vpnv6: str | None = Field(max_length=35, default=None, description="VPNv6 inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_in_evpn: str | None = Field(max_length=35, default=None, description="L2VPN EVPN inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out: str | None = Field(max_length=35, default=None, description="IPv4 outbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out_preferable: str | None = Field(max_length=35, default=None, description="IPv4 outbound route map filter if the peer is preferred.")  # datasource: ['router.route-map.name']    
    route_map_out6: str | None = Field(max_length=35, default=None, description="IPv6 Outbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out6_preferable: str | None = Field(max_length=35, default=None, description="IPv6 outbound route map filter if the peer is preferred.")  # datasource: ['router.route-map.name']    
    route_map_out_vpnv4: str | None = Field(max_length=35, default=None, description="VPNv4 outbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out_vpnv6: str | None = Field(max_length=35, default=None, description="VPNv6 outbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out_vpnv4_preferable: str | None = Field(max_length=35, default=None, description="VPNv4 outbound route map filter if the peer is preferred.")  # datasource: ['router.route-map.name']    
    route_map_out_vpnv6_preferable: str | None = Field(max_length=35, default=None, description="VPNv6 outbound route map filter if this neighbor is preferred.")  # datasource: ['router.route-map.name']    
    route_map_out_evpn: str | None = Field(max_length=35, default=None, description="L2VPN EVPN outbound route map filter.")  # datasource: ['router.route-map.name']    
    send_community: BgpNeighborGroupSendCommunityEnum | None = Field(default=BgpNeighborGroupSendCommunityEnum.BOTH, description="IPv4 Send community attribute to neighbor.")    
    send_community6: BgpNeighborGroupSendCommunity6Enum | None = Field(default=BgpNeighborGroupSendCommunity6Enum.BOTH, description="IPv6 Send community attribute to neighbor.")    
    send_community_vpnv4: BgpNeighborGroupSendCommunityVpnv4Enum | None = Field(default=BgpNeighborGroupSendCommunityVpnv4Enum.BOTH, description="Send community attribute to neighbor for VPNv4 address family.")    
    send_community_vpnv6: BgpNeighborGroupSendCommunityVpnv6Enum | None = Field(default=BgpNeighborGroupSendCommunityVpnv6Enum.BOTH, description="Enable/disable sending community attribute to this neighbor for VPNv6 address family.")    
    send_community_evpn: BgpNeighborGroupSendCommunityEvpnEnum | None = Field(default=BgpNeighborGroupSendCommunityEvpnEnum.BOTH, description="Enable/disable sending community attribute to neighbor for L2VPN EVPN address family.")    
    keep_alive_timer: int | None = Field(ge=0, le=65535, default=4294967295, description="Keep alive timer interval (sec).")    
    holdtime_timer: int | None = Field(ge=3, le=65535, default=4294967295, description="Interval (sec) before peer considered dead.")    
    connect_timer: int | None = Field(ge=1, le=65535, default=4294967295, description="Interval (sec) for connect timer.")    
    unsuppress_map: str | None = Field(max_length=35, default=None, description="IPv4 Route map to selectively unsuppress suppressed routes.")  # datasource: ['router.route-map.name']    
    unsuppress_map6: str | None = Field(max_length=35, default=None, description="IPv6 Route map to selectively unsuppress suppressed routes.")  # datasource: ['router.route-map.name']    
    update_source: str | None = Field(max_length=15, default=None, description="Interface to use as source IP/IPv6 address of TCP connections.")  # datasource: ['system.interface.name']    
    weight: int | None = Field(ge=0, le=65535, default=4294967295, description="Neighbor weight.")    
    restart_time: int | None = Field(ge=0, le=3600, default=0, description="Graceful restart delay time (sec, 0 = global default).")    
    additional_path: BgpNeighborGroupAdditionalPathEnum | None = Field(default=BgpNeighborGroupAdditionalPathEnum.DISABLE, description="Enable/disable IPv4 additional-path capability.")    
    additional_path6: BgpNeighborGroupAdditionalPath6Enum | None = Field(default=BgpNeighborGroupAdditionalPath6Enum.DISABLE, description="Enable/disable IPv6 additional-path capability.")    
    additional_path_vpnv4: BgpNeighborGroupAdditionalPathVpnv4Enum | None = Field(default=BgpNeighborGroupAdditionalPathVpnv4Enum.DISABLE, description="Enable/disable VPNv4 additional-path capability.")    
    additional_path_vpnv6: BgpNeighborGroupAdditionalPathVpnv6Enum | None = Field(default=BgpNeighborGroupAdditionalPathVpnv6Enum.DISABLE, description="Enable/disable VPNv6 additional-path capability.")    
    adv_additional_path: int | None = Field(ge=2, le=255, default=2, description="Number of IPv4 additional paths that can be advertised to this neighbor.")    
    adv_additional_path6: int | None = Field(ge=2, le=255, default=2, description="Number of IPv6 additional paths that can be advertised to this neighbor.")    
    adv_additional_path_vpnv4: int | None = Field(ge=2, le=255, default=2, description="Number of VPNv4 additional paths that can be advertised to this neighbor.")    
    adv_additional_path_vpnv6: int | None = Field(ge=2, le=255, default=2, description="Number of VPNv6 additional paths that can be advertised to this neighbor.")    
    password: Any = Field(max_length=128, default=None, description="Password used in MD5 authentication.")    
    auth_options: str | None = Field(max_length=35, default=None, description="Key-chain name for TCP authentication options.")  # datasource: ['router.key-chain.name']
class BgpNeighbor(BaseModel):
    """
    Child table model for neighbor.
    
    BGP neighbor table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    ip: str = Field(max_length=45, description="IP/IPv6 address of neighbor.")    
    advertisement_interval: int | None = Field(ge=0, le=600, default=30, description="Minimum interval (sec) between sending updates.")    
    allowas_in_enable: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 Enable to allow my AS in AS path.")    
    allowas_in_enable6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 Enable to allow my AS in AS path.")    
    allowas_in_enable_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable to allow my AS in AS path for VPNv4 route.")    
    allowas_in_enable_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable use of my AS in AS path for VPNv6 route.")    
    allowas_in_enable_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable to allow my AS in AS path for L2VPN EVPN route.")    
    allowas_in: int | None = Field(ge=1, le=10, default=3, description="IPv4 The maximum number of occurrence of my AS number allowed.")    
    allowas_in6: int | None = Field(ge=1, le=10, default=3, description="IPv6 The maximum number of occurrence of my AS number allowed.")    
    allowas_in_vpnv4: int | None = Field(ge=1, le=10, default=3, description="The maximum number of occurrence of my AS number allowed for VPNv4 route.")    
    allowas_in_vpnv6: int | None = Field(ge=1, le=10, default=3, description="The maximum number of occurrence of my AS number allowed for VPNv6 route.")    
    allowas_in_evpn: int | None = Field(ge=1, le=10, default=3, description="The maximum number of occurrence of my AS number allowed for L2VPN EVPN route.")    
    attribute_unchanged: list[Literal["as-path", "med", "next-hop"]] = Field(default_factory=list, description="IPv4 List of attributes that should be unchanged.")    
    attribute_unchanged6: list[Literal["as-path", "med", "next-hop"]] = Field(default_factory=list, description="IPv6 List of attributes that should be unchanged.")    
    attribute_unchanged_vpnv4: list[Literal["as-path", "med", "next-hop"]] = Field(default_factory=list, description="List of attributes that should be unchanged for VPNv4 route.")    
    attribute_unchanged_vpnv6: list[Literal["as-path", "med", "next-hop"]] = Field(default_factory=list, description="List of attributes that should not be changed for VPNv6 route.")    
    activate: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family IPv4 for this neighbor.")    
    activate6: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family IPv6 for this neighbor.")    
    activate_vpnv4: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family VPNv4 for this neighbor.")    
    activate_vpnv6: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family VPNv6 for this neighbor.")    
    activate_evpn: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable address family L2VPN EVPN for this neighbor.")    
    bfd: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable BFD for this neighbor.")    
    capability_dynamic: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise dynamic capability to this neighbor.")    
    capability_orf: BgpNeighborCapabilityOrfEnum | None = Field(default=BgpNeighborCapabilityOrfEnum.NONE, description="Accept/Send IPv4 ORF lists to/from this neighbor.")    
    capability_orf6: BgpNeighborCapabilityOrf6Enum | None = Field(default=BgpNeighborCapabilityOrf6Enum.NONE, description="Accept/Send IPv6 ORF lists to/from this neighbor.")    
    capability_graceful_restart: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise IPv4 graceful restart capability to this neighbor.")    
    capability_graceful_restart6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise IPv6 graceful restart capability to this neighbor.")    
    capability_graceful_restart_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise VPNv4 graceful restart capability to this neighbor.")    
    capability_graceful_restart_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertisement of VPNv6 graceful restart capability to this neighbor.")    
    capability_graceful_restart_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertisement of L2VPN EVPN graceful restart capability to this neighbor.")    
    capability_route_refresh: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable advertise route refresh capability to this neighbor.")    
    capability_default_originate: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise default IPv4 route to this neighbor.")    
    capability_default_originate6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable advertise default IPv6 route to this neighbor.")    
    dont_capability_negotiate: Literal["enable", "disable"] | None = Field(default="disable", description="Do not negotiate capabilities with this neighbor.")    
    ebgp_enforce_multihop: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allow multi-hop EBGP neighbors.")    
    link_down_failover: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable failover upon link down.")    
    stale_route: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable stale route after neighbor down.")    
    next_hop_self: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 next-hop calculation for this neighbor.")    
    next_hop_self6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 next-hop calculation for this neighbor.")    
    next_hop_self_rr: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable setting nexthop's address to interface's IPv4 address for route-reflector routes.")    
    next_hop_self_rr6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable setting nexthop's address to interface's IPv6 address for route-reflector routes.")    
    next_hop_self_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable setting VPNv4 next-hop to interface's IP address for this neighbor.")    
    next_hop_self_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable use of outgoing interface's IP address as VPNv6 next-hop for this neighbor.")    
    override_capability: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable override result of capability negotiation.")    
    passive: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable sending of open messages to this neighbor.")    
    remove_private_as: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable remove private AS number from IPv4 outbound updates.")    
    remove_private_as6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable remove private AS number from IPv6 outbound updates.")    
    remove_private_as_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable remove private AS number from VPNv4 outbound updates.")    
    remove_private_as_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable to remove private AS number from VPNv6 outbound updates.")    
    remove_private_as_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable removing private AS number from L2VPN EVPN outbound updates.")    
    route_reflector_client: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 AS route reflector client.")    
    route_reflector_client6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 AS route reflector client.")    
    route_reflector_client_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv4 AS route reflector client for this neighbor.")    
    route_reflector_client_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv6 AS route reflector client for this neighbor.")    
    route_reflector_client_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable L2VPN EVPN AS route reflector client for this neighbor.")    
    route_server_client: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 AS route server client.")    
    route_server_client6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 AS route server client.")    
    route_server_client_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv4 AS route server client for this neighbor.")    
    route_server_client_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv6 AS route server client for this neighbor.")    
    route_server_client_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable L2VPN EVPN AS route server client for this neighbor.")    
    rr_attr_allow_change: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to IPv4 route reflector clients.")    
    rr_attr_allow_change6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to IPv6 route reflector clients.")    
    rr_attr_allow_change_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to VPNv4 route reflector clients.")    
    rr_attr_allow_change_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to VPNv6 route reflector clients.")    
    rr_attr_allow_change_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowing change of route attributes when advertising to L2VPN EVPN route reflector clients.")    
    shutdown: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable shutdown this neighbor.")    
    soft_reconfiguration: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allow IPv4 inbound soft reconfiguration.")    
    soft_reconfiguration6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allow IPv6 inbound soft reconfiguration.")    
    soft_reconfiguration_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allow VPNv4 inbound soft reconfiguration.")    
    soft_reconfiguration_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable VPNv6 inbound soft reconfiguration.")    
    soft_reconfiguration_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable L2VPN EVPN inbound soft reconfiguration.")    
    as_override: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable replace peer AS with own AS for IPv4.")    
    as_override6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable replace peer AS with own AS for IPv6.")    
    strict_capability_match: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable strict capability matching.")    
    default_originate_routemap: str | None = Field(max_length=35, default=None, description="Route map to specify criteria to originate IPv4 default.")  # datasource: ['router.route-map.name']    
    default_originate_routemap6: str | None = Field(max_length=35, default=None, description="Route map to specify criteria to originate IPv6 default.")  # datasource: ['router.route-map.name']    
    description: str | None = Field(max_length=63, default=None, description="Description.")    
    distribute_list_in: str | None = Field(max_length=35, default=None, description="Filter for IPv4 updates from this neighbor.")  # datasource: ['router.access-list.name']    
    distribute_list_in6: str | None = Field(max_length=35, default=None, description="Filter for IPv6 updates from this neighbor.")  # datasource: ['router.access-list6.name']    
    distribute_list_in_vpnv4: str | None = Field(max_length=35, default=None, description="Filter for VPNv4 updates from this neighbor.")  # datasource: ['router.access-list.name']    
    distribute_list_in_vpnv6: str | None = Field(max_length=35, default=None, description="Filter for VPNv6 updates from this neighbor.")  # datasource: ['router.access-list6.name']    
    distribute_list_out: str | None = Field(max_length=35, default=None, description="Filter for IPv4 updates to this neighbor.")  # datasource: ['router.access-list.name']    
    distribute_list_out6: str | None = Field(max_length=35, default=None, description="Filter for IPv6 updates to this neighbor.")  # datasource: ['router.access-list6.name']    
    distribute_list_out_vpnv4: str | None = Field(max_length=35, default=None, description="Filter for VPNv4 updates to this neighbor.")  # datasource: ['router.access-list.name']    
    distribute_list_out_vpnv6: str | None = Field(max_length=35, default=None, description="Filter for VPNv6 updates to this neighbor.")  # datasource: ['router.access-list6.name']    
    ebgp_multihop_ttl: int | None = Field(ge=1, le=255, default=255, description="EBGP multihop TTL for this peer.")    
    filter_list_in: str | None = Field(max_length=35, default=None, description="BGP filter for IPv4 inbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_in6: str | None = Field(max_length=35, default=None, description="BGP filter for IPv6 inbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_in_vpnv4: str | None = Field(max_length=35, default=None, description="BGP filter for VPNv4 inbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_in_vpnv6: str | None = Field(max_length=35, default=None, description="BGP filter for VPNv6 inbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_out: str | None = Field(max_length=35, default=None, description="BGP filter for IPv4 outbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_out6: str | None = Field(max_length=35, default=None, description="BGP filter for IPv6 outbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_out_vpnv4: str | None = Field(max_length=35, default=None, description="BGP filter for VPNv4 outbound routes.")  # datasource: ['router.aspath-list.name']    
    filter_list_out_vpnv6: str | None = Field(max_length=35, default=None, description="BGP filter for VPNv6 outbound routes.")  # datasource: ['router.aspath-list.name']    
    interface: str | None = Field(max_length=15, default=None, description="Specify outgoing interface for peer connection. For IPv6 peer, the interface should have link-local address.")  # datasource: ['system.interface.name']    
    maximum_prefix: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of IPv4 prefixes to accept from this peer.")    
    maximum_prefix6: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of IPv6 prefixes to accept from this peer.")    
    maximum_prefix_vpnv4: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of VPNv4 prefixes to accept from this peer.")    
    maximum_prefix_vpnv6: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of VPNv6 prefixes to accept from this peer.")    
    maximum_prefix_evpn: int | None = Field(ge=1, le=4294967295, default=0, description="Maximum number of L2VPN EVPN prefixes to accept from this peer.")    
    maximum_prefix_threshold: int | None = Field(ge=1, le=100, default=75, description="Maximum IPv4 prefix threshold value (1 - 100 percent).")    
    maximum_prefix_threshold6: int | None = Field(ge=1, le=100, default=75, description="Maximum IPv6 prefix threshold value (1 - 100 percent).")    
    maximum_prefix_threshold_vpnv4: int | None = Field(ge=1, le=100, default=75, description="Maximum VPNv4 prefix threshold value (1 - 100 percent).")    
    maximum_prefix_threshold_vpnv6: int | None = Field(ge=1, le=100, default=75, description="Maximum VPNv6 prefix threshold value (1 - 100 percent).")    
    maximum_prefix_threshold_evpn: int | None = Field(ge=1, le=100, default=75, description="Maximum L2VPN EVPN prefix threshold value (1 - 100 percent).")    
    maximum_prefix_warning_only: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv4 Only give warning message when limit is exceeded.")    
    maximum_prefix_warning_only6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IPv6 Only give warning message when limit is exceeded.")    
    maximum_prefix_warning_only_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable only giving warning message when limit is exceeded for VPNv4 routes.")    
    maximum_prefix_warning_only_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable warning message when limit is exceeded for VPNv6 routes.")    
    maximum_prefix_warning_only_evpn: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable only sending warning message when exceeding limit of L2VPN EVPN routes.")    
    prefix_list_in: str | None = Field(max_length=35, default=None, description="IPv4 Inbound filter for updates from this neighbor.")  # datasource: ['router.prefix-list.name']    
    prefix_list_in6: str | None = Field(max_length=35, default=None, description="IPv6 Inbound filter for updates from this neighbor.")  # datasource: ['router.prefix-list6.name']    
    prefix_list_in_vpnv4: str | None = Field(max_length=35, default=None, description="Inbound filter for VPNv4 updates from this neighbor.")  # datasource: ['router.prefix-list.name']    
    prefix_list_in_vpnv6: str | None = Field(max_length=35, default=None, description="Inbound filter for VPNv6 updates from this neighbor.")  # datasource: ['router.prefix-list6.name']    
    prefix_list_out: str | None = Field(max_length=35, default=None, description="IPv4 Outbound filter for updates to this neighbor.")  # datasource: ['router.prefix-list.name']    
    prefix_list_out6: str | None = Field(max_length=35, default=None, description="IPv6 Outbound filter for updates to this neighbor.")  # datasource: ['router.prefix-list6.name']    
    prefix_list_out_vpnv4: str | None = Field(max_length=35, default=None, description="Outbound filter for VPNv4 updates to this neighbor.")  # datasource: ['router.prefix-list.name']    
    prefix_list_out_vpnv6: str | None = Field(max_length=35, default=None, description="Outbound filter for VPNv6 updates to this neighbor.")  # datasource: ['router.prefix-list6.name']    
    remote_as: str = Field(description="AS number of neighbor.")    
    local_as: str | None = Field(default=None, description="Local AS number of neighbor.")    
    local_as_no_prepend: Literal["enable", "disable"] | None = Field(default="disable", description="Do not prepend local-as to incoming updates.")    
    local_as_replace_as: Literal["enable", "disable"] | None = Field(default="disable", description="Replace real AS with local-as in outgoing updates.")    
    retain_stale_time: int | None = Field(ge=0, le=65535, default=0, description="Time to retain stale routes.")    
    route_map_in: str | None = Field(max_length=35, default=None, description="IPv4 Inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_in6: str | None = Field(max_length=35, default=None, description="IPv6 Inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_in_vpnv4: str | None = Field(max_length=35, default=None, description="VPNv4 inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_in_vpnv6: str | None = Field(max_length=35, default=None, description="VPNv6 inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_in_evpn: str | None = Field(max_length=35, default=None, description="L2VPN EVPN inbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out: str | None = Field(max_length=35, default=None, description="IPv4 outbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out_preferable: str | None = Field(max_length=35, default=None, description="IPv4 outbound route map filter if the peer is preferred.")  # datasource: ['router.route-map.name']    
    route_map_out6: str | None = Field(max_length=35, default=None, description="IPv6 Outbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out6_preferable: str | None = Field(max_length=35, default=None, description="IPv6 outbound route map filter if the peer is preferred.")  # datasource: ['router.route-map.name']    
    route_map_out_vpnv4: str | None = Field(max_length=35, default=None, description="VPNv4 outbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out_vpnv6: str | None = Field(max_length=35, default=None, description="VPNv6 outbound route map filter.")  # datasource: ['router.route-map.name']    
    route_map_out_vpnv4_preferable: str | None = Field(max_length=35, default=None, description="VPNv4 outbound route map filter if the peer is preferred.")  # datasource: ['router.route-map.name']    
    route_map_out_vpnv6_preferable: str | None = Field(max_length=35, default=None, description="VPNv6 outbound route map filter if this neighbor is preferred.")  # datasource: ['router.route-map.name']    
    route_map_out_evpn: str | None = Field(max_length=35, default=None, description="L2VPN EVPN outbound route map filter.")  # datasource: ['router.route-map.name']    
    send_community: BgpNeighborSendCommunityEnum | None = Field(default=BgpNeighborSendCommunityEnum.BOTH, description="IPv4 Send community attribute to neighbor.")    
    send_community6: BgpNeighborSendCommunity6Enum | None = Field(default=BgpNeighborSendCommunity6Enum.BOTH, description="IPv6 Send community attribute to neighbor.")    
    send_community_vpnv4: BgpNeighborSendCommunityVpnv4Enum | None = Field(default=BgpNeighborSendCommunityVpnv4Enum.BOTH, description="Send community attribute to neighbor for VPNv4 address family.")    
    send_community_vpnv6: BgpNeighborSendCommunityVpnv6Enum | None = Field(default=BgpNeighborSendCommunityVpnv6Enum.BOTH, description="Enable/disable sending community attribute to this neighbor for VPNv6 address family.")    
    send_community_evpn: BgpNeighborSendCommunityEvpnEnum | None = Field(default=BgpNeighborSendCommunityEvpnEnum.BOTH, description="Enable/disable sending community attribute to neighbor for L2VPN EVPN address family.")    
    keep_alive_timer: int | None = Field(ge=0, le=65535, default=4294967295, description="Keep alive timer interval (sec).")    
    holdtime_timer: int | None = Field(ge=3, le=65535, default=4294967295, description="Interval (sec) before peer considered dead.")    
    connect_timer: int | None = Field(ge=1, le=65535, default=4294967295, description="Interval (sec) for connect timer.")    
    unsuppress_map: str | None = Field(max_length=35, default=None, description="IPv4 Route map to selectively unsuppress suppressed routes.")  # datasource: ['router.route-map.name']    
    unsuppress_map6: str | None = Field(max_length=35, default=None, description="IPv6 Route map to selectively unsuppress suppressed routes.")  # datasource: ['router.route-map.name']    
    update_source: str | None = Field(max_length=15, default=None, description="Interface to use as source IP/IPv6 address of TCP connections.")  # datasource: ['system.interface.name']    
    weight: int | None = Field(ge=0, le=65535, default=4294967295, description="Neighbor weight.")    
    restart_time: int | None = Field(ge=0, le=3600, default=0, description="Graceful restart delay time (sec, 0 = global default).")    
    additional_path: BgpNeighborAdditionalPathEnum | None = Field(default=BgpNeighborAdditionalPathEnum.DISABLE, description="Enable/disable IPv4 additional-path capability.")    
    additional_path6: BgpNeighborAdditionalPath6Enum | None = Field(default=BgpNeighborAdditionalPath6Enum.DISABLE, description="Enable/disable IPv6 additional-path capability.")    
    additional_path_vpnv4: BgpNeighborAdditionalPathVpnv4Enum | None = Field(default=BgpNeighborAdditionalPathVpnv4Enum.DISABLE, description="Enable/disable VPNv4 additional-path capability.")    
    additional_path_vpnv6: BgpNeighborAdditionalPathVpnv6Enum | None = Field(default=BgpNeighborAdditionalPathVpnv6Enum.DISABLE, description="Enable/disable VPNv6 additional-path capability.")    
    adv_additional_path: int | None = Field(ge=2, le=255, default=2, description="Number of IPv4 additional paths that can be advertised to this neighbor.")    
    adv_additional_path6: int | None = Field(ge=2, le=255, default=2, description="Number of IPv6 additional paths that can be advertised to this neighbor.")    
    adv_additional_path_vpnv4: int | None = Field(ge=2, le=255, default=2, description="Number of VPNv4 additional paths that can be advertised to this neighbor.")    
    adv_additional_path_vpnv6: int | None = Field(ge=2, le=255, default=2, description="Number of VPNv6 additional paths that can be advertised to this neighbor.")    
    password: Any = Field(max_length=128, default=None, description="Password used in MD5 authentication.")    
    auth_options: str | None = Field(max_length=35, default=None, description="Key-chain name for TCP authentication options.")  # datasource: ['router.key-chain.name']    
    conditional_advertise: list[BgpNeighborConditionalAdvertise] = Field(default_factory=list, description="Conditional advertisement.")    
    conditional_advertise6: list[BgpNeighborConditionalAdvertise6] = Field(default_factory=list, description="IPv6 conditional advertisement.")
class BgpConfederationPeers(BaseModel):
    """
    Child table model for confederation-peers.
    
    Confederation peers.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    peer: str | None = Field(max_length=79, default=None, description="Peer ID.")
class BgpAggregateAddress6(BaseModel):
    """
    Child table model for aggregate-address6.
    
    BGP IPv6 aggregate address table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    prefix6: str = Field(default="::/0", description="Aggregate IPv6 prefix.")    
    as_set: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable generate AS set path information.")    
    summary_only: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable filter more specific routes from updates.")
class BgpAggregateAddress(BaseModel):
    """
    Child table model for aggregate-address.
    
    BGP aggregate address table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    prefix: Any = Field(default="0.0.0.0 0.0.0.0", description="Aggregate prefix.")    
    as_set: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable generate AS set path information.")    
    summary_only: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable filter more specific routes from updates.")
class BgpAdminDistance(BaseModel):
    """
    Child table model for admin-distance.
    
    Administrative distance modifications.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    neighbour_prefix: str = Field(default="0.0.0.0 0.0.0.0", description="Neighbor address prefix.")    
    route_list: str | None = Field(max_length=35, default=None, description="Access list of routes to apply new distance to.")  # datasource: ['router.access-list.name']    
    distance: int = Field(ge=1, le=255, default=0, description="Administrative distance to apply (1 - 255).")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class BgpTagResolveModeEnum(str, Enum):
    """Allowed values for tag_resolve_mode field."""
    DISABLE = "disable"
    PREFERRED = "preferred"
    MERGE = "merge"
    MERGE_ALL = "merge-all"


# ============================================================================
# Main Model
# ============================================================================

class BgpModel(BaseModel):
    """
    Pydantic model for router/bgp configuration.
    
    Configure BGP.
    
    Validation Rules:        - as_: pattern=        - router_id: pattern=        - keepalive_timer: min=0 max=65535 pattern=        - holdtime_timer: min=3 max=65535 pattern=        - always_compare_med: pattern=        - bestpath_as_path_ignore: pattern=        - bestpath_cmp_confed_aspath: pattern=        - bestpath_cmp_routerid: pattern=        - bestpath_med_confed: pattern=        - bestpath_med_missing_as_worst: pattern=        - client_to_client_reflection: pattern=        - dampening: pattern=        - deterministic_med: pattern=        - ebgp_multipath: pattern=        - ibgp_multipath: pattern=        - enforce_first_as: pattern=        - fast_external_failover: pattern=        - log_neighbour_changes: pattern=        - network_import_check: pattern=        - ignore_optional_capability: pattern=        - additional_path: pattern=        - additional_path6: pattern=        - additional_path_vpnv4: pattern=        - additional_path_vpnv6: pattern=        - multipath_recursive_distance: pattern=        - recursive_next_hop: pattern=        - recursive_inherit_priority: pattern=        - tag_resolve_mode: pattern=        - cluster_id: pattern=        - confederation_identifier: min=1 max=4294967295 pattern=        - confederation_peers: pattern=        - dampening_route_map: max_length=35 pattern=        - dampening_reachability_half_life: min=1 max=45 pattern=        - dampening_reuse: min=1 max=20000 pattern=        - dampening_suppress: min=1 max=20000 pattern=        - dampening_max_suppress_time: min=1 max=255 pattern=        - dampening_unreachability_half_life: min=1 max=45 pattern=        - default_local_preference: min=0 max=4294967295 pattern=        - scan_time: min=5 max=60 pattern=        - distance_external: min=1 max=255 pattern=        - distance_internal: min=1 max=255 pattern=        - distance_local: min=1 max=255 pattern=        - synchronization: pattern=        - graceful_restart: pattern=        - graceful_restart_time: min=1 max=3600 pattern=        - graceful_stalepath_time: min=1 max=3600 pattern=        - graceful_update_delay: min=1 max=3600 pattern=        - graceful_end_on_timer: pattern=        - additional_path_select: min=2 max=255 pattern=        - additional_path_select6: min=2 max=255 pattern=        - additional_path_select_vpnv4: min=2 max=255 pattern=        - additional_path_select_vpnv6: min=2 max=255 pattern=        - cross_family_conditional_adv: pattern=        - aggregate_address: pattern=        - aggregate_address6: pattern=        - neighbor: pattern=        - neighbor_group: pattern=        - neighbor_range: pattern=        - neighbor_range6: pattern=        - network: pattern=        - network6: pattern=        - redistribute: pattern=        - redistribute6: pattern=        - admin_distance: pattern=        - vrf: pattern=        - vrf6: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    as_: str = Field(serialization_alias="as", description="Router AS number, asplain/asdot/asdot+ format, 0 to disable BGP.")    
    router_id: str | None = Field(default=None, description="Router ID.")    
    keepalive_timer: int | None = Field(ge=0, le=65535, default=60, description="Frequency to send keep alive requests.")    
    holdtime_timer: int | None = Field(ge=3, le=65535, default=180, description="Number of seconds to mark peer as dead.")    
    always_compare_med: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable always compare MED.")    
    bestpath_as_path_ignore: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable ignore AS path.")    
    bestpath_cmp_confed_aspath: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable compare federation AS path length.")    
    bestpath_cmp_routerid: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable compare router ID for identical EBGP paths.")    
    bestpath_med_confed: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable compare MED among confederation paths.")    
    bestpath_med_missing_as_worst: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable treat missing MED as least preferred.")    
    client_to_client_reflection: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable client-to-client route reflection.")    
    dampening: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable route-flap dampening.")    
    deterministic_med: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable enforce deterministic comparison of MED.")    
    ebgp_multipath: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable EBGP multi-path.")    
    ibgp_multipath: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IBGP multi-path.")    
    enforce_first_as: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable enforce first AS for EBGP routes.")    
    fast_external_failover: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable reset peer BGP session if link goes down.")    
    log_neighbour_changes: Literal["enable", "disable"] | None = Field(default="enable", description="Log BGP neighbor changes.")    
    network_import_check: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable ensure BGP network route exists in IGP.")    
    ignore_optional_capability: Literal["enable", "disable"] | None = Field(default="enable", description="Do not send unknown optional capability notification message.")    
    additional_path: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable selection of BGP IPv4 additional paths.")    
    additional_path6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable selection of BGP IPv6 additional paths.")    
    additional_path_vpnv4: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable selection of BGP VPNv4 additional paths.")    
    additional_path_vpnv6: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable selection of BGP VPNv6 additional paths.")    
    multipath_recursive_distance: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable use of recursive distance to select multipath.")    
    recursive_next_hop: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable recursive resolution of next-hop using BGP route.")    
    recursive_inherit_priority: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable priority inheritance for recursive resolution.")    
    tag_resolve_mode: BgpTagResolveModeEnum | None = Field(default=BgpTagResolveModeEnum.DISABLE, description="Configure tag-match mode. Resolves BGP routes with other routes containing the same tag.")    
    cluster_id: str | None = Field(default="0.0.0.0", description="Route reflector cluster ID.")    
    confederation_identifier: int | None = Field(ge=1, le=4294967295, default=0, description="Confederation identifier.")    
    confederation_peers: list[BgpConfederationPeers] = Field(default_factory=list, description="Confederation peers.")    
    dampening_route_map: str | None = Field(max_length=35, default=None, description="Criteria for dampening.")  # datasource: ['router.route-map.name']    
    dampening_reachability_half_life: int | None = Field(ge=1, le=45, default=15, description="Reachability half-life time for penalty (min).")    
    dampening_reuse: int | None = Field(ge=1, le=20000, default=750, description="Threshold to reuse routes.")    
    dampening_suppress: int | None = Field(ge=1, le=20000, default=2000, description="Threshold to suppress routes.")    
    dampening_max_suppress_time: int | None = Field(ge=1, le=255, default=60, description="Maximum minutes a route can be suppressed.")    
    dampening_unreachability_half_life: int | None = Field(ge=1, le=45, default=15, description="Unreachability half-life time for penalty (min).")    
    default_local_preference: int | None = Field(ge=0, le=4294967295, default=100, description="Default local preference.")    
    scan_time: int | None = Field(ge=5, le=60, default=60, description="Background scanner interval (sec), 0 to disable it.")    
    distance_external: int | None = Field(ge=1, le=255, default=20, description="Distance for routes external to the AS.")    
    distance_internal: int | None = Field(ge=1, le=255, default=200, description="Distance for routes internal to the AS.")    
    distance_local: int | None = Field(ge=1, le=255, default=200, description="Distance for routes local to the AS.")    
    synchronization: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable only advertise routes from iBGP if routes present in an IGP.")    
    graceful_restart: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable BGP graceful restart capabilities.")    
    graceful_restart_time: int | None = Field(ge=1, le=3600, default=120, description="Time needed for neighbors to restart (sec).")    
    graceful_stalepath_time: int | None = Field(ge=1, le=3600, default=360, description="Time to hold stale paths of restarting neighbor (sec).")    
    graceful_update_delay: int | None = Field(ge=1, le=3600, default=120, description="Route advertisement/selection delay after restart (sec).")    
    graceful_end_on_timer: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable to exit graceful restart on timer only.")    
    additional_path_select: int | None = Field(ge=2, le=255, default=2, description="Number of additional paths to be selected for each IPv4 NLRI.")    
    additional_path_select6: int | None = Field(ge=2, le=255, default=2, description="Number of additional paths to be selected for each IPv6 NLRI.")    
    additional_path_select_vpnv4: int | None = Field(ge=2, le=255, default=2, description="Number of additional paths to be selected for each VPNv4 NLRI.")    
    additional_path_select_vpnv6: int | None = Field(ge=2, le=255, default=2, description="Number of additional paths to be selected for each VPNv6 NLRI.")    
    cross_family_conditional_adv: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable cross address family conditional advertisement.")    
    aggregate_address: list[BgpAggregateAddress] = Field(default_factory=list, description="BGP aggregate address table.")    
    aggregate_address6: list[BgpAggregateAddress6] = Field(default_factory=list, description="BGP IPv6 aggregate address table.")    
    neighbor: list[BgpNeighbor] = Field(default_factory=list, description="BGP neighbor table.")    
    neighbor_group: list[BgpNeighborGroup] = Field(default_factory=list, description="BGP neighbor group table.")    
    neighbor_range: list[BgpNeighborRange] = Field(default_factory=list, description="BGP neighbor range table.")    
    neighbor_range6: list[BgpNeighborRange6] = Field(default_factory=list, description="BGP IPv6 neighbor range table.")    
    network: list[BgpNetwork] = Field(default_factory=list, description="BGP network table.")    
    network6: list[BgpNetwork6] = Field(default_factory=list, description="BGP IPv6 network table.")    
    redistribute: list[BgpRedistribute] = Field(default_factory=list, description="BGP IPv4 redistribute table.")    
    redistribute6: list[BgpRedistribute6] = Field(default_factory=list, description="BGP IPv6 redistribute table.")    
    admin_distance: list[BgpAdminDistance] = Field(default_factory=list, description="Administrative distance modifications.")    
    vrf: list[BgpVrf] = Field(default_factory=list, description="BGP VRF leaking table.")    
    vrf6: list[BgpVrf6] = Field(default_factory=list, description="BGP IPv6 VRF leaking table.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('dampening_route_map')
    @classmethod
    def validate_dampening_route_map(cls, v: Any) -> Any:
        """
        Validate dampening_route_map field.
        
        Datasource: ['router.route-map.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def to_fortios_dict(self) -> dict[str, Any]:
        """
        Convert model to FortiOS API payload format.
        
        Returns:
            Dict suitable for POST/PUT operations
        """
        # Export with exclude_none to avoid sending null values
        return self.model_dump(exclude_none=True, by_alias=True)
    
    @classmethod
    def from_fortios_response(cls, data: dict[str, Any]) -> "BgpModel":
        """
        Create model instance from FortiOS API response.
        
        Args:
            data: Response data from API
            
        Returns:
            Validated model instance
        """
        return cls(**data)
    # ========================================================================
    # Datasource Validation Methods
    # ========================================================================    
    async def validate_dampening_route_map_references(self, client: Any) -> list[str]:
        """
        Validate dampening_route_map references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/route-map        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     dampening_route_map="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_dampening_route_map_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "dampening_route_map", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.router.route_map.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Dampening-Route-Map '{value}' not found in "
                "router/route-map"
            )        
        return errors    
    async def validate_neighbor_references(self, client: Any) -> list[str]:
        """
        Validate neighbor references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/key-chain        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     neighbor=[{"auth-options": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_neighbor_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "neighbor", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("auth-options")
            else:
                value = getattr(item, "auth-options", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.key_chain.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Neighbor '{value}' not found in "
                    "router/key-chain"
                )        
        return errors    
    async def validate_neighbor_group_references(self, client: Any) -> list[str]:
        """
        Validate neighbor_group references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/key-chain        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     neighbor_group=[{"auth-options": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_neighbor_group_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "neighbor_group", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("auth-options")
            else:
                value = getattr(item, "auth-options", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.key_chain.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Neighbor-Group '{value}' not found in "
                    "router/key-chain"
                )        
        return errors    
    async def validate_neighbor_range_references(self, client: Any) -> list[str]:
        """
        Validate neighbor_range references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/bgp/neighbor-group        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     neighbor_range=[{"neighbor-group": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_neighbor_range_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "neighbor_range", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("neighbor-group")
            else:
                value = getattr(item, "neighbor-group", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.bgp.neighbor_group.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Neighbor-Range '{value}' not found in "
                    "router/bgp/neighbor-group"
                )        
        return errors    
    async def validate_neighbor_range6_references(self, client: Any) -> list[str]:
        """
        Validate neighbor_range6 references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/bgp/neighbor-group        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     neighbor_range6=[{"neighbor-group": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_neighbor_range6_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "neighbor_range6", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("neighbor-group")
            else:
                value = getattr(item, "neighbor-group", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.bgp.neighbor_group.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Neighbor-Range6 '{value}' not found in "
                    "router/bgp/neighbor-group"
                )        
        return errors    
    async def validate_network_references(self, client: Any) -> list[str]:
        """
        Validate network references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/address        - firewall/addrgrp        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     network=[{"prefix-name": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_network_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "network", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("prefix-name")
            else:
                value = getattr(item, "prefix-name", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.firewall.address.exists(value):
                found = True
            elif await client.api.cmdb.firewall.addrgrp.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Network '{value}' not found in "
                    "firewall/address or firewall/addrgrp"
                )        
        return errors    
    async def validate_network6_references(self, client: Any) -> list[str]:
        """
        Validate network6 references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/route-map        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     network6=[{"route-map": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_network6_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "network6", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("route-map")
            else:
                value = getattr(item, "route-map", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.route_map.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Network6 '{value}' not found in "
                    "router/route-map"
                )        
        return errors    
    async def validate_redistribute_references(self, client: Any) -> list[str]:
        """
        Validate redistribute references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/route-map        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     redistribute=[{"route-map": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_redistribute_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "redistribute", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("route-map")
            else:
                value = getattr(item, "route-map", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.route_map.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Redistribute '{value}' not found in "
                    "router/route-map"
                )        
        return errors    
    async def validate_redistribute6_references(self, client: Any) -> list[str]:
        """
        Validate redistribute6 references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/route-map        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     redistribute6=[{"route-map": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_redistribute6_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "redistribute6", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("route-map")
            else:
                value = getattr(item, "route-map", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.route_map.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Redistribute6 '{value}' not found in "
                    "router/route-map"
                )        
        return errors    
    async def validate_admin_distance_references(self, client: Any) -> list[str]:
        """
        Validate admin_distance references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/access-list        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     admin_distance=[{"route-list": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_admin_distance_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "admin_distance", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("route-list")
            else:
                value = getattr(item, "route-list", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.access_list.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Admin-Distance '{value}' not found in "
                    "router/access-list"
                )        
        return errors    
    async def validate_vrf_references(self, client: Any) -> list[str]:
        """
        Validate vrf references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/route-map        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     vrf=[{"import-route-map": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_vrf_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "vrf", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("import-route-map")
            else:
                value = getattr(item, "import-route-map", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.route_map.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Vrf '{value}' not found in "
                    "router/route-map"
                )        
        return errors    
    async def validate_vrf6_references(self, client: Any) -> list[str]:
        """
        Validate vrf6 references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - router/route-map        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = BgpModel(
            ...     vrf6=[{"import-route-map": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_vrf6_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.bgp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "vrf6", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("import-route-map")
            else:
                value = getattr(item, "import-route-map", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.router.route_map.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Vrf6 '{value}' not found in "
                    "router/route-map"
                )        
        return errors    
    async def validate_all_references(self, client: Any) -> list[str]:
        """
        Validate ALL datasource references in this model.
        
        Convenience method that runs all validate_*_references() methods
        and aggregates the results.
        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of all validation errors found
            
        Example:
            >>> errors = await policy.validate_all_references(fgt._client)
            >>> if errors:
            ...     for error in errors:
            ...         print(f"  - {error}")
        """
        all_errors = []
        
        errors = await self.validate_dampening_route_map_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_neighbor_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_neighbor_group_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_neighbor_range_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_neighbor_range6_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_network_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_network6_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_redistribute_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_redistribute6_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_admin_distance_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_vrf_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_vrf6_references(client)
        all_errors.extend(errors)        
        return all_errors

# ============================================================================
# Type Aliases for Convenience
# ============================================================================

Dict = dict[str, Any]  # For backward compatibility

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "BgpModel",    "BgpConfederationPeers",    "BgpAggregateAddress",    "BgpAggregateAddress6",    "BgpNeighbor",    "BgpNeighbor.ConditionalAdvertise",    "BgpNeighbor.ConditionalAdvertise.ConditionRoutemap",    "BgpNeighbor.ConditionalAdvertise6",    "BgpNeighbor.ConditionalAdvertise6.ConditionRoutemap",    "BgpNeighborGroup",    "BgpNeighborRange",    "BgpNeighborRange6",    "BgpNetwork",    "BgpNetwork6",    "BgpRedistribute",    "BgpRedistribute6",    "BgpAdminDistance",    "BgpVrf",    "BgpVrf.ExportRt",    "BgpVrf.ImportRt",    "BgpVrf.LeakTarget",    "BgpVrf6",    "BgpVrf6.ExportRt",    "BgpVrf6.ImportRt",    "BgpVrf6.LeakTarget",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:28.346304Z
# ============================================================================