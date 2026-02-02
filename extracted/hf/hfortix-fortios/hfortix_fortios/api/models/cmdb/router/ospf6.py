"""
Pydantic Models for CMDB - router/ospf6

Runtime validation models for router/ospf6 configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class Ospf6Ospf6InterfaceNetworkTypeEnum(str, Enum):
    """Allowed values for network_type field in ospf6-interface."""
    BROADCAST = "broadcast"
    POINT_TO_POINT = "point-to-point"
    NON_BROADCAST = "non-broadcast"
    POINT_TO_MULTIPOINT = "point-to-multipoint"
    POINT_TO_MULTIPOINT_NON_BROADCAST = "point-to-multipoint-non-broadcast"

class Ospf6Ospf6InterfaceAuthenticationEnum(str, Enum):
    """Allowed values for authentication field in ospf6-interface."""
    NONE = "none"
    AH = "ah"
    ESP = "esp"
    AREA = "area"

class Ospf6Ospf6InterfaceIpsecAuthAlgEnum(str, Enum):
    """Allowed values for ipsec_auth_alg field in ospf6-interface."""
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"

class Ospf6Ospf6InterfaceIpsecEncAlgEnum(str, Enum):
    """Allowed values for ipsec_enc_alg field in ospf6-interface."""
    NULL = "null"
    DES = "des"
    V_3DES = "3des"
    AES128 = "aes128"
    AES192 = "aes192"
    AES256 = "aes256"

class Ospf6AreaVirtualLinkAuthenticationEnum(str, Enum):
    """Allowed values for authentication field in area.virtual-link."""
    NONE = "none"
    AH = "ah"
    ESP = "esp"
    AREA = "area"

class Ospf6AreaVirtualLinkIpsecAuthAlgEnum(str, Enum):
    """Allowed values for ipsec_auth_alg field in area.virtual-link."""
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"

class Ospf6AreaVirtualLinkIpsecEncAlgEnum(str, Enum):
    """Allowed values for ipsec_enc_alg field in area.virtual-link."""
    NULL = "null"
    DES = "des"
    V_3DES = "3des"
    AES128 = "aes128"
    AES192 = "aes192"
    AES256 = "aes256"

class Ospf6AreaIpsecAuthAlgEnum(str, Enum):
    """Allowed values for ipsec_auth_alg field in area."""
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"

class Ospf6AreaIpsecEncAlgEnum(str, Enum):
    """Allowed values for ipsec_enc_alg field in area."""
    NULL = "null"
    DES = "des"
    V_3DES = "3des"
    AES128 = "aes128"
    AES192 = "aes192"
    AES256 = "aes256"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class Ospf6SummaryAddress(BaseModel):
    """
    Child table model for summary-address.
    
    IPv6 address summary configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Summary address entry ID.")    
    prefix6: str = Field(default="::/0", description="IPv6 prefix.")    
    advertise: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable advertise status.")    
    tag: int | None = Field(ge=0, le=4294967295, default=0, description="Tag value.")
class Ospf6Redistribute(BaseModel):
    """
    Child table model for redistribute.
    
    Redistribute configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Redistribute name.")    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Status.")    
    metric: int | None = Field(ge=0, le=16777214, default=0, description="Redistribute metric setting.")    
    routemap: str | None = Field(max_length=35, default=None, description="Route map name.")  # datasource: ['router.route-map.name']    
    metric_type: Literal["1", "2"] | None = Field(default="2", description="Metric type.")
class Ospf6PassiveInterface(BaseModel):
    """
    Child table model for passive-interface.
    
    Passive interface configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="Passive interface name.")  # datasource: ['system.interface.name']
class Ospf6Ospf6InterfaceNeighbor(BaseModel):
    """
    Child table model for ospf6-interface.neighbor.
    
    OSPFv3 neighbors are used when OSPFv3 runs on non-broadcast media.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    ip6: str = Field(default="::", description="IPv6 link local address of the neighbor.")    
    poll_interval: int | None = Field(ge=1, le=65535, default=10, description="Poll interval time in seconds.")    
    cost: int | None = Field(ge=0, le=65535, default=0, description="Cost of the interface, value range from 0 to 65535, 0 means auto-cost.")    
    priority: int | None = Field(ge=0, le=255, default=1, description="Priority.")
class Ospf6Ospf6InterfaceIpsecKeys(BaseModel):
    """
    Child table model for ospf6-interface.ipsec-keys.
    
    IPsec authentication and encryption keys.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    spi: int = Field(ge=256, le=4294967295, default=0, description="Security Parameters Index.")    
    auth_key: Any = Field(max_length=128, default=None, description="Authentication key.")    
    enc_key: Any = Field(max_length=128, default=None, description="Encryption key.")
class Ospf6Ospf6Interface(BaseModel):
    """
    Child table model for ospf6-interface.
    
    OSPF6 interface configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=35, default=None, description="Interface entry name.")    
    area_id: str = Field(default="0.0.0.0", description="A.B.C.D, in IPv4 address format.")    
    interface: str = Field(max_length=15, description="Configuration interface name.")  # datasource: ['system.interface.name']    
    retransmit_interval: int | None = Field(ge=1, le=65535, default=5, description="Retransmit interval.")    
    transmit_delay: int | None = Field(ge=1, le=65535, default=1, description="Transmit delay.")    
    cost: int | None = Field(ge=0, le=65535, default=0, description="Cost of the interface, value range from 0 to 65535, 0 means auto-cost.")    
    priority: int | None = Field(ge=0, le=255, default=1, description="Priority.")    
    dead_interval: int | None = Field(ge=1, le=65535, default=0, description="Dead interval.")    
    hello_interval: int | None = Field(ge=1, le=65535, default=0, description="Hello interval.")    
    status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable OSPF6 routing on this interface.")    
    network_type: Ospf6Ospf6InterfaceNetworkTypeEnum | None = Field(default=Ospf6Ospf6InterfaceNetworkTypeEnum.BROADCAST, description="Network type.")    
    bfd: Literal["global", "enable", "disable"] | None = Field(default="global", description="Enable/disable Bidirectional Forwarding Detection (BFD).")    
    mtu: int | None = Field(ge=576, le=65535, default=0, description="MTU for OSPFv3 packets.")    
    mtu_ignore: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable ignoring MTU field in DBD packets.")    
    authentication: Ospf6Ospf6InterfaceAuthenticationEnum | None = Field(default=Ospf6Ospf6InterfaceAuthenticationEnum.AREA, description="Authentication mode.")    
    key_rollover_interval: int | None = Field(ge=300, le=216000, default=300, description="Key roll-over interval.")    
    ipsec_auth_alg: Ospf6Ospf6InterfaceIpsecAuthAlgEnum | None = Field(default=Ospf6Ospf6InterfaceIpsecAuthAlgEnum.MD5, description="Authentication algorithm.")    
    ipsec_enc_alg: Ospf6Ospf6InterfaceIpsecEncAlgEnum | None = Field(default=Ospf6Ospf6InterfaceIpsecEncAlgEnum.NULL, description="Encryption algorithm.")    
    ipsec_keys: list[Ospf6Ospf6InterfaceIpsecKeys] = Field(default_factory=list, description="IPsec authentication and encryption keys.")    
    neighbor: list[Ospf6Ospf6InterfaceNeighbor] = Field(default_factory=list, description="OSPFv3 neighbors are used when OSPFv3 runs on non-broadcast media.")
class Ospf6AreaVirtualLinkIpsecKeys(BaseModel):
    """
    Child table model for area.virtual-link.ipsec-keys.
    
    IPsec authentication and encryption keys.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    spi: int = Field(ge=256, le=4294967295, default=0, description="Security Parameters Index.")    
    auth_key: Any = Field(max_length=128, default=None, description="Authentication key.")    
    enc_key: Any = Field(max_length=128, default=None, description="Encryption key.")
class Ospf6AreaVirtualLink(BaseModel):
    """
    Child table model for area.virtual-link.
    
    OSPF6 virtual link configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=35, default=None, description="Virtual link entry name.")    
    dead_interval: int | None = Field(ge=1, le=65535, default=40, description="Dead interval.")    
    hello_interval: int | None = Field(ge=1, le=65535, default=10, description="Hello interval.")    
    retransmit_interval: int | None = Field(ge=1, le=65535, default=5, description="Retransmit interval.")    
    transmit_delay: int | None = Field(ge=1, le=65535, default=1, description="Transmit delay.")    
    peer: str = Field(default="0.0.0.0", description="A.B.C.D, peer router ID.")    
    authentication: Ospf6AreaVirtualLinkAuthenticationEnum | None = Field(default=Ospf6AreaVirtualLinkAuthenticationEnum.AREA, description="Authentication mode.")    
    key_rollover_interval: int | None = Field(ge=300, le=216000, default=300, description="Key roll-over interval.")    
    ipsec_auth_alg: Ospf6AreaVirtualLinkIpsecAuthAlgEnum | None = Field(default=Ospf6AreaVirtualLinkIpsecAuthAlgEnum.MD5, description="Authentication algorithm.")    
    ipsec_enc_alg: Ospf6AreaVirtualLinkIpsecEncAlgEnum | None = Field(default=Ospf6AreaVirtualLinkIpsecEncAlgEnum.NULL, description="Encryption algorithm.")    
    ipsec_keys: list[Ospf6AreaVirtualLinkIpsecKeys] = Field(default_factory=list, description="IPsec authentication and encryption keys.")
class Ospf6AreaRange(BaseModel):
    """
    Child table model for area.range.
    
    OSPF6 area range configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Range entry ID.")    
    prefix6: str = Field(default="::/0", description="IPv6 prefix.")    
    advertise: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable advertise status.")
class Ospf6AreaIpsecKeys(BaseModel):
    """
    Child table model for area.ipsec-keys.
    
    IPsec authentication and encryption keys.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    spi: int = Field(ge=256, le=4294967295, default=0, description="Security Parameters Index.")    
    auth_key: Any = Field(max_length=128, default=None, description="Authentication key.")    
    enc_key: Any = Field(max_length=128, default=None, description="Encryption key.")
class Ospf6Area(BaseModel):
    """
    Child table model for area.
    
    OSPF6 area configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: str | None = Field(default="0.0.0.0", serialization_alias="id", description="Area entry IP address.")    
    default_cost: int | None = Field(ge=0, le=16777215, default=10, description="Summary default cost of stub or NSSA area.")    
    nssa_translator_role: Literal["candidate", "never", "always"] | None = Field(default="candidate", description="NSSA translator role type.")    
    stub_type: Literal["no-summary", "summary"] | None = Field(default="summary", description="Stub summary setting.")    
    type_: Literal["regular", "nssa", "stub"] | None = Field(default="regular", serialization_alias="type", description="Area type setting.")    
    nssa_default_information_originate: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable originate type 7 default into NSSA area.")    
    nssa_default_information_originate_metric: int | None = Field(ge=0, le=16777214, default=10, description="OSPFv3 default metric.")    
    nssa_default_information_originate_metric_type: Literal["1", "2"] | None = Field(default="2", description="OSPFv3 metric type for default routes.")    
    nssa_redistribution: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable redistribute into NSSA area.")    
    authentication: Literal["none", "ah", "esp"] | None = Field(default="none", description="Authentication mode.")    
    key_rollover_interval: int | None = Field(ge=300, le=216000, default=300, description="Key roll-over interval.")    
    ipsec_auth_alg: Ospf6AreaIpsecAuthAlgEnum | None = Field(default=Ospf6AreaIpsecAuthAlgEnum.MD5, description="Authentication algorithm.")    
    ipsec_enc_alg: Ospf6AreaIpsecEncAlgEnum | None = Field(default=Ospf6AreaIpsecEncAlgEnum.NULL, description="Encryption algorithm.")    
    ipsec_keys: list[Ospf6AreaIpsecKeys] = Field(default_factory=list, description="IPsec authentication and encryption keys.")    
    range_: list[Ospf6AreaRange] = Field(default_factory=list, serialization_alias="range", description="OSPF6 area range configuration.")    
    virtual_link: list[Ospf6AreaVirtualLink] = Field(default_factory=list, description="OSPF6 virtual link configuration.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class Ospf6Model(BaseModel):
    """
    Pydantic model for router/ospf6 configuration.
    
    Configure IPv6 OSPF.
    
    Validation Rules:        - abr_type: pattern=        - auto_cost_ref_bandwidth: min=1 max=1000000 pattern=        - default_information_originate: pattern=        - log_neighbour_changes: pattern=        - default_information_metric: min=1 max=16777214 pattern=        - default_information_metric_type: pattern=        - default_information_route_map: max_length=35 pattern=        - default_metric: min=1 max=16777214 pattern=        - router_id: pattern=        - spf_timers: pattern=        - bfd: pattern=        - restart_mode: pattern=        - restart_period: min=1 max=3600 pattern=        - restart_on_topology_change: pattern=        - area: pattern=        - ospf6_interface: pattern=        - redistribute: pattern=        - passive_interface: pattern=        - summary_address: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    abr_type: Literal["cisco", "ibm", "standard"] | None = Field(default="standard", description="Area border router type.")    
    auto_cost_ref_bandwidth: int | None = Field(ge=1, le=1000000, default=1000, description="Reference bandwidth in terms of megabits per second.")    
    default_information_originate: Literal["enable", "always", "disable"] | None = Field(default="disable", description="Enable/disable generation of default route.")    
    log_neighbour_changes: Literal["enable", "disable"] | None = Field(default="enable", description="Log OSPFv3 neighbor changes.")    
    default_information_metric: int | None = Field(ge=1, le=16777214, default=10, description="Default information metric.")    
    default_information_metric_type: Literal["1", "2"] | None = Field(default="2", description="Default information metric type.")    
    default_information_route_map: str | None = Field(max_length=35, default=None, description="Default information route map.")  # datasource: ['router.route-map.name']    
    default_metric: int | None = Field(ge=1, le=16777214, default=10, description="Default metric of redistribute routes.")    
    router_id: str = Field(default="0.0.0.0", description="A.B.C.D, in IPv4 address format.")    
    spf_timers: str | None = Field(default=None, description="SPF calculation frequency.")    
    bfd: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Bidirectional Forwarding Detection (BFD).")    
    restart_mode: Literal["none", "graceful-restart"] | None = Field(default="none", description="OSPFv3 restart mode (graceful or none).")    
    restart_period: int | None = Field(ge=1, le=3600, default=120, description="Graceful restart period in seconds.")    
    restart_on_topology_change: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable continuing graceful restart upon topology change.")    
    area: list[Ospf6Area] = Field(default_factory=list, description="OSPF6 area configuration.")    
    ospf6_interface: list[Ospf6Ospf6Interface] = Field(default_factory=list, description="OSPF6 interface configuration.")    
    redistribute: list[Ospf6Redistribute] = Field(default_factory=list, description="Redistribute configuration.")    
    passive_interface: list[Ospf6PassiveInterface] = Field(default_factory=list, description="Passive interface configuration.")    
    summary_address: list[Ospf6SummaryAddress] = Field(default_factory=list, description="IPv6 address summary configuration.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('default_information_route_map')
    @classmethod
    def validate_default_information_route_map(cls, v: Any) -> Any:
        """
        Validate default_information_route_map field.
        
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "Ospf6Model":
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
    async def validate_default_information_route_map_references(self, client: Any) -> list[str]:
        """
        Validate default_information_route_map references exist in FortiGate.
        
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
            >>> policy = Ospf6Model(
            ...     default_information_route_map="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_default_information_route_map_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.ospf6.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "default_information_route_map", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.router.route_map.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Default-Information-Route-Map '{value}' not found in "
                "router/route-map"
            )        
        return errors    
    async def validate_ospf6_interface_references(self, client: Any) -> list[str]:
        """
        Validate ospf6_interface references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - system/interface        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = Ospf6Model(
            ...     ospf6_interface=[{"interface": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_ospf6_interface_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.ospf6.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "ospf6_interface", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("interface")
            else:
                value = getattr(item, "interface", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.system.interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Ospf6-Interface '{value}' not found in "
                    "system/interface"
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
            >>> policy = Ospf6Model(
            ...     redistribute=[{"routemap": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_redistribute_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.ospf6.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "redistribute", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("routemap")
            else:
                value = getattr(item, "routemap", None)
            
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
    async def validate_passive_interface_references(self, client: Any) -> list[str]:
        """
        Validate passive_interface references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - system/interface        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = Ospf6Model(
            ...     passive_interface=[{"name": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_passive_interface_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.router.ospf6.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "passive_interface", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("name")
            else:
                value = getattr(item, "name", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.system.interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Passive-Interface '{value}' not found in "
                    "system/interface"
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
        
        errors = await self.validate_default_information_route_map_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_ospf6_interface_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_redistribute_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_passive_interface_references(client)
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
    "Ospf6Model",    "Ospf6Area",    "Ospf6Area.IpsecKeys",    "Ospf6Area.Range",    "Ospf6Area.VirtualLink",    "Ospf6Area.VirtualLink.IpsecKeys",    "Ospf6Ospf6Interface",    "Ospf6Ospf6Interface.IpsecKeys",    "Ospf6Ospf6Interface.Neighbor",    "Ospf6Redistribute",    "Ospf6PassiveInterface",    "Ospf6SummaryAddress",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:56.634664Z
# ============================================================================