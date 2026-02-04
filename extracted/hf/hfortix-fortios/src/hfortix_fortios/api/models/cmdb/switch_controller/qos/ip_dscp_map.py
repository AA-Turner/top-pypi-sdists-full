"""
Pydantic Models for CMDB - switch_controller/qos/ip_dscp_map

Runtime validation models for switch_controller/qos/ip_dscp_map configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class IpDscpMapMapDiffservEnum(str, Enum):
    """Allowed values for diffserv field in map."""
    CS0 = "CS0"
    CS1 = "CS1"
    AF11 = "AF11"
    AF12 = "AF12"
    AF13 = "AF13"
    CS2 = "CS2"
    AF21 = "AF21"
    AF22 = "AF22"
    AF23 = "AF23"
    CS3 = "CS3"
    AF31 = "AF31"
    AF32 = "AF32"
    AF33 = "AF33"
    CS4 = "CS4"
    AF41 = "AF41"
    AF42 = "AF42"
    AF43 = "AF43"
    CS5 = "CS5"
    EF = "EF"
    CS6 = "CS6"
    CS7 = "CS7"

class IpDscpMapMapIpPrecedenceEnum(str, Enum):
    """Allowed values for ip_precedence field in map."""
    NETWORK_CONTROL = "network-control"
    INTERNETWORK_CONTROL = "internetwork-control"
    CRITIC_ECP = "critic-ecp"
    FLASHOVERRIDE = "flashoverride"
    FLASH = "flash"
    IMMEDIATE = "immediate"
    PRIORITY = "priority"
    ROUTINE = "routine"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class IpDscpMapMap(BaseModel):
    """
    Child table model for map.
    
    Maps between IP-DSCP value to COS queue.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=63, description="Dscp mapping entry name.")    
    cos_queue: int = Field(ge=0, le=7, default=0, description="COS queue number.")    
    diffserv: list[IpDscpMapMapDiffservEnum] = Field(default_factory=list, description="Differentiated service.")    
    ip_precedence: list[IpDscpMapMapIpPrecedenceEnum] = Field(default_factory=list, description="IP Precedence.")    
    value: str | None = Field(default=None, description="Raw values of DSCP (0 - 63).")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class IpDscpMapModel(BaseModel):
    """
    Pydantic model for switch_controller/qos/ip_dscp_map configuration.
    
    Configure FortiSwitch QoS IP precedence/DSCP.
    
    Validation Rules:        - name: max_length=63 pattern=        - description: max_length=63 pattern=        - map_: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str = Field(max_length=63, description="Dscp map name.")    
    description: str | None = Field(max_length=63, default=None, description="Description of the ip-dscp map name.")    
    map_: list[IpDscpMapMap] = Field(default_factory=list, serialization_alias="map", description="Maps between IP-DSCP value to COS queue.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "IpDscpMapModel":
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
    "IpDscpMapModel",    "IpDscpMapMap",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:40.135255Z
# ============================================================================