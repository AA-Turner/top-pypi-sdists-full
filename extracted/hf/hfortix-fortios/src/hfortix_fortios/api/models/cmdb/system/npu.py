"""
Pydantic Models for CMDB - system/npu

Runtime validation models for system/npu configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class NpuPriorityProtocol(BaseModel):
    """
    Child table model for priority-protocol.
    
    Configure NPU priority protocol.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    bgp: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable NPU BGP priority protocol.    enable:Enable NPU BGP priority protocol.    disable:Disable NPU BGP priority protocol.")    
    slbc: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable NPU SLBC priority protocol.    enable:Enable NPU SLBC priority protocol.    disable:Disable NPU SLBC priority protocol.")    
    bfd: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable NPU BFD priority protocol.    enable:Enable NPU BFD priority protocol.    disable:Disable NPU BFD priority protocol.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class NpuModel(BaseModel):
    """
    Pydantic model for system/npu configuration.
    
    Configuration for system/npu
    
    Validation Rules:        - dedicated_management_cpu: pattern=        - dedicated_management_affinity: pattern=        - capwap_offload: pattern=        - ipsec_mtu_override: pattern=        - ipsec_ordering: pattern=        - ipsec_enc_subengine_mask: pattern=        - ipsec_dec_subengine_mask: pattern=        - priority_protocol: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    dedicated_management_cpu: Literal["enable", "disable"] | None = Field(default=None, description="Enable to dedicate one CPU for GUI and CLI connections when NPs are busy.    enable:Enable dedication of CPU #0 for management tasks.    disable:Disable dedication of CPU #0 for management tasks.")    
    dedicated_management_affinity: str | None = Field(default=None, description="Affinity setting for management daemons (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).")    
    capwap_offload: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable offloading managed FortiAP and FortiLink CAPWAP sessions.    enable:Enable CAPWAP offload.    disable:Disable CAPWAP offload.")    
    ipsec_mtu_override: Literal["disable", "enable"] | None = Field(default=None, description="Enable/disable NP6 IPsec MTU override.    disable:Disable NP6 IPsec MTU override.    enable:Enable NP6 IPsec MTU override.")    
    ipsec_ordering: Literal["disable", "enable"] | None = Field(default=None, description="Enable/disable IPsec ordering.    disable:Disable IPsec ordering.    enable:Enable IPsec ordering.")    
    ipsec_enc_subengine_mask: str | None = Field(default=None, description="IPsec encryption subengine mask (0x1 - 0x0f, default 0x0f).")    
    ipsec_dec_subengine_mask: str | None = Field(default=None, description="IPsec decryption subengine mask (0x1 - 0x0f, default 0x0f).")    
    priority_protocol: list[NpuPriorityProtocol] = Field(default_factory=list, description="Configure NPU priority protocol.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "NpuModel":
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
    "NpuModel",    "NpuPriorityProtocol",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:40.760517Z
# ============================================================================