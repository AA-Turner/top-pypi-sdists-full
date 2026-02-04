"""
Pydantic Models for CMDB - application/name

Runtime validation models for application/name configuration.
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

class NameStatusApplicationListName(BaseModel):
    """
    Child table model for status.<application list name>.
    
    Application list name.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    application_entry_name: Any = Field(default=None, description="application entry name")
class NameStatus(BaseModel):
    """
    Child table model for status.
    
    print all application information
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    application_list_name: list[NameStatusApplicationListName] = Field(default_factory=list, description="Application list name.")
class NameParameters(BaseModel):
    """
    Child table model for parameters.
    
    Application parameters.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=31, default=None, description="Parameter name.")    
    default_value: str | None = Field(max_length=199, default=None, description="Parameter default value.")
class NameMetadata(BaseModel):
    """
    Child table model for metadata.
    
    Meta data.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    metaid: int | None = Field(ge=0, le=4294967295, default=0, description="Meta ID.")    
    valueid: int | None = Field(ge=0, le=4294967295, default=0, description="Value ID.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class NameModel(BaseModel):
    """
    Pydantic model for application/name configuration.
    
    Configure application signatures.
    
    Validation Rules:        - name: max_length=63 pattern=        - id_: min=0 max=4294967295 pattern=        - category: min=0 max=4294967295 pattern=        - popularity: min=0 max=255 pattern=        - risk: min=0 max=255 pattern=        - weight: min=0 max=255 pattern=        - protocol: pattern=        - technology: pattern=        - behavior: pattern=        - vendor: pattern=        - parameters: pattern=        - metadata: pattern=        - status: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=63, default=None, description="Application name.")    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Application ID.")    
    category: int = Field(ge=0, le=4294967295, default=0, description="Application category ID.")    
    popularity: int | None = Field(ge=0, le=255, default=0, description="Application popularity.")    
    risk: int | None = Field(ge=0, le=255, default=0, description="Application risk.")    
    weight: int | None = Field(ge=0, le=255, default=0, description="Application weight.")    
    protocol: str | None = Field(default=None, description="Application protocol.")    
    technology: str | None = Field(default=None, description="Application technology.")    
    behavior: str | None = Field(default=None, description="Application behavior.")    
    vendor: str | None = Field(default=None, description="Application vendor.")    
    parameters: list[NameParameters] = Field(default_factory=list, description="Application parameters.")    
    metadata: list[NameMetadata] = Field(default_factory=list, description="Meta data.")    
    status: list[NameStatus] = Field(default_factory=list, description="print all application information")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "NameModel":
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
    "NameModel",    "NameParameters",    "NameMetadata",    "NameStatus",    "NameStatus.<Application List Name>",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:39.969637Z
# ============================================================================