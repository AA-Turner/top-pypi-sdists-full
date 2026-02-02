"""
Pydantic Models for CMDB - firewall/internet_service_definition

Runtime validation models for firewall/internet_service_definition configuration.
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

class InternetServiceDefinitionEntryPortRange(BaseModel):
    """
    Child table model for entry.port-range.
    
    Port ranges in the definition entry.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Custom entry port range ID.")    
    start_port: int | None = Field(ge=1, le=65535, default=1, description="Starting TCP/UDP/SCTP destination port (1 to 65535).")    
    end_port: int | None = Field(ge=1, le=65535, default=65535, description="Ending TCP/UDP/SCTP destination port (1 to 65535).")
class InternetServiceDefinitionEntry(BaseModel):
    """
    Child table model for entry.
    
    Protocol and port information in an Internet Service entry.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    seq_num: int | None = Field(ge=0, le=4294967295, default=0, description="Entry sequence number.")    
    category_id: int | None = Field(ge=0, le=4294967295, default=0, description="Internet Service category ID.")    
    name: str | None = Field(max_length=63, default=None, description="Internet Service name.")    
    protocol: int | None = Field(ge=0, le=255, default=0, description="Integer value for the protocol type as defined by IANA (0 - 255).")    
    port_range: list[InternetServiceDefinitionEntryPortRange] = Field(default_factory=list, description="Port ranges in the definition entry.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class InternetServiceDefinitionModel(BaseModel):
    """
    Pydantic model for firewall/internet_service_definition configuration.
    
    Configure Internet Service definition.
    
    Validation Rules:        - id_: min=0 max=4294967295 pattern=        - entry: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Internet Service application list ID.")    
    entry: list[InternetServiceDefinitionEntry] = Field(default_factory=list, description="Protocol and port information in an Internet Service entry.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "InternetServiceDefinitionModel":
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
    "InternetServiceDefinitionModel",    "InternetServiceDefinitionEntry",    "InternetServiceDefinitionEntry.PortRange",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:56.489678Z
# ============================================================================