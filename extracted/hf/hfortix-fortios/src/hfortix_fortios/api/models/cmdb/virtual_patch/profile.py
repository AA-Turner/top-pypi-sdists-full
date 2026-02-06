"""
Pydantic Models for CMDB - virtual_patch/profile

Runtime validation models for virtual_patch/profile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ProfileExemptionRule(BaseModel):
    """
    Child table model for exemption.rule.
    
    Patch signature rule IDs.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Rule IDs.")
class ProfileExemptionDevice(BaseModel):
    """
    Child table model for exemption.device.
    
    Device MAC addresses.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    mac: str | None = Field(default="00:00:00:00:00:00", description="Device MAC address.")
class ProfileExemption(BaseModel):
    """
    Child table model for exemption.
    
    Exempt devices or rules.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="IDs.")    
    status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable exemption.")    
    rule: list[ProfileExemptionRule] = Field(default_factory=list, description="Patch signature rule IDs.")    
    device: list[ProfileExemptionDevice] = Field(default_factory=list, description="Device MAC addresses.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class ProfileSeverityEnum(str, Enum):
    """Allowed values for severity field."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# Main Model
# ============================================================================

class ProfileModel(BaseModel):
    """
    Pydantic model for virtual_patch/profile configuration.
    
    Configure virtual-patch profile.
    
    Validation Rules:        - name: max_length=47 pattern=        - comment: max_length=255 pattern=        - severity: pattern=        - action: pattern=        - log: pattern=        - exemption: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str = Field(max_length=47, description="Profile name.")    
    comment: str | None = Field(max_length=255, default=None, description="Comment.")    
    severity: list[ProfileSeverityEnum] = Field(default_factory=list, description="Relative severity of the signature (low, medium, high, critical).")    
    action: Literal["pass", "block"] | None = Field(default="block", description="Action (pass/block).")    
    log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging of detection.")    
    exemption: list[ProfileExemption] = Field(default_factory=list, description="Exempt devices or rules.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "ProfileModel":
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
    "ProfileModel",    "ProfileExemption",    "ProfileExemption.Rule",    "ProfileExemption.Device",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:29.268812Z
# ============================================================================