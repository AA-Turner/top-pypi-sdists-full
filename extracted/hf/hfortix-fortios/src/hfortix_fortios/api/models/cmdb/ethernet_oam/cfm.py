"""
Pydantic Models for CMDB - ethernet_oam/cfm

Runtime validation models for ethernet_oam/cfm configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class CfmServiceMessageIntervalEnum(str, Enum):
    """Allowed values for message_interval field in service."""
    V_100 = "100"
    V_1000 = "1000"
    V_10000 = "10000"
    V_60000 = "60000"
    V_600000 = "600000"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class CfmService(BaseModel):
    """
    Child table model for service.
    
    CFM service configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    service_id: int | None = Field(default=None, description="Service ID to specify service")    
    service_name: str | None = Field(default=None, description="Short MA Name (SMAN)")    
    interface: str | None = Field(default=None, description="VLAN interface name where service is enabled")    
    mepid: int | None = Field(default=None, description="ID of the local MEP. range[1 - 8191]")    
    message_interval: CfmServiceMessageIntervalEnum | None = Field(default=None, description="Continuity-check message frequency interval in ms    100:100 msc    1000:1000 msc    10000:10000 msc    60000:60000 msc    600000:600000 msc")    
    cos: int | None = Field(default=None, description="Set Class of service (CoS) bit for continuity-check messages. range[0 - 7]")    
    sender_id: Literal["None", "Hostname"] | None = Field(default=None, description="TLV Sender ID. {None | Hostname}    None:None    Hostname:Hostname")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class CfmModel(BaseModel):
    """
    Pydantic model for ethernet_oam/cfm configuration.
    
    Configuration for ethernet_oam/cfm
    
    Validation Rules:        - domain_id: pattern=        - domain_name: pattern=        - domain_level: pattern=        - service: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    domain_id: int | None = Field(default=None, description="OAM domain ID.")    
    domain_name: str | None = Field(default=None, description="OAM domain name. Maintenance Domain Identifier (MDID).")    
    domain_level: int | None = Field(default=None, description="OAM maintenance level (0 - 7)")    
    service: list[CfmService] = Field(default_factory=list, description="CFM service configuration.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "CfmModel":
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
    "CfmModel",    "CfmService",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:29.193602Z
# ============================================================================