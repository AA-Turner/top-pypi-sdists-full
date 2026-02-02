"""
Pydantic Models for CMDB - system/ipam

Runtime validation models for system/ipam configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class IpamRulesRoleEnum(str, Enum):
    """Allowed values for role field in rules."""
    ANY = "any"
    LAN = "lan"
    WAN = "wan"
    DMZ = "dmz"
    UNDEFINED = "undefined"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class IpamRulesPool(BaseModel):
    """
    Child table model for rules.pool.
    
    Configure name of IPAM pool to use.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="IPAM pool name.")  # datasource: ['system.ipam.pools.name']
class IpamRulesInterface(BaseModel):
    """
    Child table model for rules.interface.
    
    Configure name or wildcard of interface to match.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="Interface name or wildcard.")
class IpamRulesDevice(BaseModel):
    """
    Child table model for rules.device.
    
    Configure serial number or wildcard of FortiGate to match.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="FortiGate serial number or wildcard.")
class IpamRules(BaseModel):
    """
    Child table model for rules.
    
    Configure IPAM allocation rules.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="IPAM rule name.")    
    description: str | None = Field(max_length=127, default=None, description="Description.")    
    device: list[IpamRulesDevice] = Field(description="Configure serial number or wildcard of FortiGate to match.")    
    interface: list[IpamRulesInterface] = Field(description="Configure name or wildcard of interface to match.")    
    role: IpamRulesRoleEnum | None = Field(default=IpamRulesRoleEnum.ANY, description="Configure role of interface to match.")    
    pool: list[IpamRulesPool] = Field(description="Configure name of IPAM pool to use.")    
    dhcp: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable DHCP server for matching IPAM interfaces.")
class IpamPoolsExclude(BaseModel):
    """
    Child table model for pools.exclude.
    
    Configure pool exclude subnets.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    ID: int = Field(ge=0, le=4294967295, default=0, description="Exclude ID.")    
    exclude_subnet: str = Field(default="0.0.0.0 0.0.0.0", description="Configure subnet to exclude from the IPAM pool.")
class IpamPools(BaseModel):
    """
    Child table model for pools.
    
    Configure IPAM pools.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="IPAM pool name.")    
    description: str | None = Field(max_length=127, default=None, description="Description.")    
    subnet: str = Field(default="0.0.0.0 0.0.0.0", description="Configure IPAM pool subnet, Class A - Class B subnet.")    
    exclude: list[IpamPoolsExclude] = Field(default_factory=list, description="Configure pool exclude subnets.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class IpamModel(BaseModel):
    """
    Pydantic model for system/ipam configuration.
    
    Configure IP address management services.
    
    Validation Rules:        - status: pattern=        - server_type: pattern=        - automatic_conflict_resolution: pattern=        - require_subnet_size_match: pattern=        - manage_lan_addresses: pattern=        - manage_lan_extension_addresses: pattern=        - manage_ssid_addresses: pattern=        - pools: pattern=        - rules: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable IP address management services.")    
    server_type: Literal["fabric-root"] | None = Field(default="fabric-root", description="Configure the type of IPAM server to use.")    
    automatic_conflict_resolution: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable automatic conflict resolution.")    
    require_subnet_size_match: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable reassignment of subnets to make requested and actual sizes match.")    
    manage_lan_addresses: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable default management of LAN interface addresses.")    
    manage_lan_extension_addresses: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable default management of FortiExtender LAN extension interface addresses.")    
    manage_ssid_addresses: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable default management of FortiAP SSID addresses.")    
    pools: list[IpamPools] = Field(default_factory=list, description="Configure IPAM pools.")    
    rules: list[IpamRules] = Field(default_factory=list, description="Configure IPAM allocation rules.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "IpamModel":
        """
        Create model instance from FortiOS API response.
        
        Args:
            data: Response data from API
            
        Returns:
            Validated model instance
        """
        return cls(**data)

# ============================================================================
# Type Aliases for Convenience
# ============================================================================

Dict = dict[str, Any]  # For backward compatibility

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "IpamModel",    "IpamPools",    "IpamPools.Exclude",    "IpamRules",    "IpamRules.Device",    "IpamRules.Interface",    "IpamRules.Pool",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:56.075497Z
# ============================================================================