"""
Pydantic Models for CMDB - wireless_controller/bonjour_profile

Runtime validation models for wireless_controller/bonjour_profile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class BonjourProfilePolicyListServicesEnum(str, Enum):
    """Allowed values for services field in policy-list."""
    ALL = "all"
    AIRPLAY = "airplay"
    AFP = "afp"
    BIT_TORRENT = "bit-torrent"
    FTP = "ftp"
    ICHAT = "ichat"
    ITUNES = "itunes"
    PRINTERS = "printers"
    SAMBA = "samba"
    SCANNERS = "scanners"
    SSH = "ssh"
    CHROMECAST = "chromecast"
    MIRACAST = "miracast"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class BonjourProfilePolicyList(BaseModel):
    """
    Child table model for policy-list.
    
    Bonjour policy list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    policy_id: int | None = Field(ge=1, le=65535, default=0, description="Policy ID.")    
    description: str | None = Field(max_length=63, default=None, description="Description.")    
    from_vlan: str | None = Field(max_length=63, default="0", description="VLAN ID from which the Bonjour service is advertised (0 - 4094, default = 0).")    
    to_vlan: str | None = Field(max_length=63, default="all", description="VLAN ID to which the Bonjour service is made available (0 - 4094, default = all).")    
    services: list[BonjourProfilePolicyListServicesEnum] = Field(default_factory=list, description="Bonjour services for the VLAN connecting to the Bonjour network.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class BonjourProfileModel(BaseModel):
    """
    Pydantic model for wireless_controller/bonjour_profile configuration.
    
    Configure Bonjour profiles. Bonjour is Apple's zero configuration networking protocol. Bonjour profiles allow APs and FortiAPs to connect to networks using Bonjour.
    
    Validation Rules:        - name: max_length=35 pattern=        - comment: max_length=63 pattern=        - micro_location: pattern=        - policy_list: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=35, default=None, description="Bonjour profile name.")    
    comment: str | None = Field(max_length=63, default=None, description="Comment.")    
    micro_location: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Micro location for Bonjour profile (default = disable).")    
    policy_list: list[BonjourProfilePolicyList] = Field(default_factory=list, description="Bonjour policy list.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "BonjourProfileModel":
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
    "BonjourProfileModel",    "BonjourProfilePolicyList",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:39.137959Z
# ============================================================================