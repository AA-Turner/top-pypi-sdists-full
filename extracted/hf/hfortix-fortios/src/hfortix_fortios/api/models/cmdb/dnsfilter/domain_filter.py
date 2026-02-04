"""
Pydantic Models for CMDB - dnsfilter/domain_filter

Runtime validation models for dnsfilter/domain_filter configuration.
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

class DomainFilterEntries(BaseModel):
    """
    Child table model for entries.
    
    DNS domain filter entries.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Id.")    
    domain: str | None = Field(max_length=511, default=None, description="Domain entries to be filtered.")    
    type_: Literal["simple", "regex", "wildcard"] | None = Field(default="simple", serialization_alias="type", description="DNS domain filter type.")    
    action: Literal["block", "allow", "monitor"] | None = Field(default="block", description="Action to take for domain filter matches.")    
    status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable this domain filter.")    
    comment: str | None = Field(max_length=255, default=None, description="Comment.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class DomainFilterModel(BaseModel):
    """
    Pydantic model for dnsfilter/domain_filter configuration.
    
    Configure DNS domain filters.
    
    Validation Rules:        - id_: min=0 max=4294967295 pattern=        - name: max_length=63 pattern=        - comment: max_length=255 pattern=        - entries: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    name: str = Field(max_length=63, description="Name of table.")    
    comment: str | None = Field(max_length=255, default=None, description="Optional comments.")    
    entries: list[DomainFilterEntries] = Field(description="DNS domain filter entries.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "DomainFilterModel":
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
    "DomainFilterModel",    "DomainFilterEntries",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:39.881230Z
# ============================================================================