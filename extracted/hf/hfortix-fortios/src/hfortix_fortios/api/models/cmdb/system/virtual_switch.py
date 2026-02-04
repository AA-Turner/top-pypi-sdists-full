"""
Pydantic Models for CMDB - system/virtual_switch

Runtime validation models for system/virtual_switch configuration.
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

class VirtualSwitchPort(BaseModel):
    """
    Child table model for port.
    
    Configure member ports.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(default=None, description="Physical interface name.")    
    alias: str | None = Field(default=None, description="Alias.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class VirtualSwitchModel(BaseModel):
    """
    Pydantic model for system/virtual_switch configuration.
    
    Configuration for system/virtual_switch
    
    Validation Rules:        - name: pattern=        - physical_switch: pattern=        - vlan: pattern=        - port: pattern=        - span: pattern=        - span_source_port: pattern=        - span_dest_port: pattern=        - span_direction: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(default=None, description="Name of the virtual switch.")    
    physical_switch: str | None = Field(default=None, description="Physical switch parent.")    
    vlan: int | None = Field(default=None, description="VLAN.")    
    port: list[VirtualSwitchPort] = Field(default_factory=list, description="Configure member ports.")    
    span: Literal["disable", "enable"] | None = Field(default=None, description="Enable/disable SPAN.    disable:Disable SPAN.    enable:Enable SPAN.")    
    span_source_port: str | None = Field(default=None, description="SPAN source port.")    
    span_dest_port: str | None = Field(default=None, description="SPAN destination port.")    
    span_direction: Literal["rx", "tx", "both"] | None = Field(default=None, description="SPAN direction.    rx:SPAN receive direction only.    tx:SPAN transmit direction only.    both:SPAN both directions.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "VirtualSwitchModel":
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
    "VirtualSwitchModel",    "VirtualSwitchPort",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:39.902299Z
# ============================================================================