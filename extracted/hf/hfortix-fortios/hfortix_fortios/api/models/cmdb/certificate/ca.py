"""
Pydantic Models for CMDB - certificate/ca

Runtime validation models for certificate/ca configuration.
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

class CaDetails(BaseModel):
    """
    Child table model for details.
    
    Print CA certificate detailed information.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    CA_certficate_name: Any = Field(default=None, description="CA certificate name.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class CaModel(BaseModel):
    """
    Pydantic model for certificate/ca configuration.
    
    CA certificate.
    
    Validation Rules:        - name: max_length=79 pattern=        - ca: pattern=        - range_: pattern=        - source: pattern=        - ssl_inspection_trusted: pattern=        - scep_url: max_length=255 pattern=        - est_url: max_length=255 pattern=        - auto_update_days: min=0 max=4294967295 pattern=        - auto_update_days_warning: min=0 max=4294967295 pattern=        - source_ip: pattern=        - ca_identifier: max_length=255 pattern=        - obsolete: pattern=        - fabric_ca: pattern=        - details: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str = Field(max_length=79, description="Name.")    
    ca: str = Field(description="CA certificate as a PEM file.")    
    range_: Literal["global", "vdom"] | None = Field(default="global", serialization_alias="range", description="Either global or VDOM IP address range for the CA certificate.")    
    source: Literal["factory", "user", "bundle"] | None = Field(default="user", description="CA certificate source type.")    
    ssl_inspection_trusted: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable this CA as a trusted CA for SSL inspection.")    
    scep_url: str | None = Field(max_length=255, default=None, description="URL of the SCEP server.")    
    est_url: str | None = Field(max_length=255, default=None, description="URL of the EST server.")    
    auto_update_days: int | None = Field(ge=0, le=4294967295, default=0, description="Number of days to wait before requesting an updated CA certificate (0 - 4294967295, 0 = disabled).")    
    auto_update_days_warning: int | None = Field(ge=0, le=4294967295, default=0, description="Number of days before an expiry-warning message is generated (0 - 4294967295, 0 = disabled).")    
    source_ip: str | None = Field(default="0.0.0.0", description="Source IP address for communications to the SCEP server.")    
    ca_identifier: str | None = Field(max_length=255, default=None, description="CA identifier of the SCEP server.")    
    obsolete: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable this CA as obsoleted.")    
    fabric_ca: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable synchronization of CA across Security Fabric.")    
    details: list[CaDetails] = Field(default_factory=list, description="Print CA certificate detailed information.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "CaModel":
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
    "CaModel",    "CaDetails",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:57.563912Z
# ============================================================================