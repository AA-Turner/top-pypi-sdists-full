"""
Pydantic Models for CMDB - wireless_controller/hotspot20/qos_map

Runtime validation models for wireless_controller/hotspot20/qos_map configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Optional

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class QosMapDscpRange(BaseModel):
    """
    Child table model for dscp-range.
    
    Differentiated Services Code Point (DSCP) ranges.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    index: int | None = Field(ge=1, le=8, default=0, description="DSCP range index.")    
    up: int = Field(ge=0, le=7, default=0, description="User priority.")    
    low: int | None = Field(ge=0, le=63, default=255, description="DSCP low value.")    
    high: int | None = Field(ge=0, le=63, default=255, description="DSCP high value.")
class QosMapDscpExcept(BaseModel):
    """
    Child table model for dscp-except.
    
    Differentiated Services Code Point (DSCP) exceptions.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    index: int | None = Field(ge=1, le=21, default=0, description="DSCP exception index.")    
    dscp: int | None = Field(ge=0, le=63, default=0, description="DSCP value.")    
    up: int | None = Field(ge=0, le=7, default=0, description="User priority.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class QosMapModel(BaseModel):
    """
    Pydantic model for wireless_controller/hotspot20/qos_map configuration.
    
    Configure QoS map set.
    
    Validation Rules:        - name: max_length=35 pattern=        - dscp_except: pattern=        - dscp_range: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=35, default=None, description="QOS-MAP name.")    
    dscp_except: list[QosMapDscpExcept] = Field(default_factory=list, description="Differentiated Services Code Point (DSCP) exceptions.")    
    dscp_range: list[QosMapDscpRange] = Field(default_factory=list, description="Differentiated Services Code Point (DSCP) ranges.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "QosMapModel":
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
    "QosMapModel",    "QosMapDscpExcept",    "QosMapDscpRange",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:30.052212Z
# ============================================================================