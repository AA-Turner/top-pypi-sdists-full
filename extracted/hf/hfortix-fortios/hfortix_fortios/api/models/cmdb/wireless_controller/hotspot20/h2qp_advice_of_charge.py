"""
Pydantic Models for CMDB - wireless_controller/hotspot20/h2qp_advice_of_charge

Runtime validation models for wireless_controller/hotspot20/h2qp_advice_of_charge configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class H2qpAdviceOfChargeAocListTypeEnum(str, Enum):
    """Allowed values for type_ field in aoc-list."""
    TIME_BASED = "time-based"
    VOLUME_BASED = "volume-based"
    TIME_AND_VOLUME_BASED = "time-and-volume-based"
    UNLIMITED = "unlimited"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class H2qpAdviceOfChargeAocListPlanInfo(BaseModel):
    """
    Child table model for aoc-list.plan-info.
    
    Plan info.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=35, default=None, description="Plan name.")    
    lang: str = Field(max_length=3, description="Language code.")    
    currency: str = Field(max_length=3, description="Currency code.")    
    info_file: str = Field(max_length=255, description="Info file.")
class H2qpAdviceOfChargeAocList(BaseModel):
    """
    Child table model for aoc-list.
    
    AOC list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=35, default=None, description="Advice of charge ID.")    
    type_: H2qpAdviceOfChargeAocListTypeEnum = Field(default=H2qpAdviceOfChargeAocListTypeEnum.TIME_BASED, serialization_alias="type", description="Usage charge type.")    
    nai_realm_encoding: str | None = Field(max_length=1, default=None, description="NAI realm encoding.")    
    nai_realm: str | None = Field(max_length=255, default=None, description="NAI realm list name.")    
    plan_info: list[H2qpAdviceOfChargeAocListPlanInfo] = Field(default_factory=list, description="Plan info.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class H2qpAdviceOfChargeModel(BaseModel):
    """
    Pydantic model for wireless_controller/hotspot20/h2qp_advice_of_charge configuration.
    
    Configure advice of charge.
    
    Validation Rules:        - name: max_length=35 pattern=        - aoc_list: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=35, default=None, description="Plan name.")    
    aoc_list: list[H2qpAdviceOfChargeAocList] = Field(default_factory=list, description="AOC list.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "H2qpAdviceOfChargeModel":
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
    "H2qpAdviceOfChargeModel",    "H2qpAdviceOfChargeAocList",    "H2qpAdviceOfChargeAocList.PlanInfo",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:58.002748Z
# ============================================================================