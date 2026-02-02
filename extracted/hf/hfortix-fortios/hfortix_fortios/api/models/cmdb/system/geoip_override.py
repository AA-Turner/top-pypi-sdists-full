"""
Pydantic Models for CMDB - system/geoip_override

Runtime validation models for system/geoip_override configuration.
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

class GeoipOverrideIp6Range(BaseModel):
    """
    Child table model for ip6-range.
    
    Table of IPv6 ranges assigned to country.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=65535, default=0, serialization_alias="id", description="ID of individual entry in the IPv6 range table.")    
    start_ip: str | None = Field(default="::", description="Starting IP address, inclusive, of the address range (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx).")    
    end_ip: str | None = Field(default="::", description="Ending IP address, inclusive, of the address range (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx).")
class GeoipOverrideIpRange(BaseModel):
    """
    Child table model for ip-range.
    
    Table of IP ranges assigned to country.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=65535, default=0, serialization_alias="id", description="ID of individual entry in the IP range table.")    
    start_ip: str | None = Field(default="0.0.0.0", description="Starting IP address, inclusive, of the address range (format: xxx.xxx.xxx.xxx).")    
    end_ip: str | None = Field(default="0.0.0.0", description="Ending IP address, inclusive, of the address range (format: xxx.xxx.xxx.xxx).")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class GeoipOverrideModel(BaseModel):
    """
    Pydantic model for system/geoip_override configuration.
    
    Configure geographical location mapping for IP address(es) to override mappings from FortiGuard.
    
    Validation Rules:        - name: max_length=63 pattern=        - description: max_length=127 pattern=        - country_id: max_length=2 pattern=        - ip_range: pattern=        - ip6_range: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str = Field(max_length=63, description="Location name.")    
    description: str | None = Field(max_length=127, default=None, description="Description.")    
    country_id: str | None = Field(max_length=2, default=None, description="Two character Country ID code.")    
    ip_range: list[GeoipOverrideIpRange] = Field(default_factory=list, description="Table of IP ranges assigned to country.")    
    ip6_range: list[GeoipOverrideIp6Range] = Field(default_factory=list, description="Table of IPv6 ranges assigned to country.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "GeoipOverrideModel":
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
    "GeoipOverrideModel",    "GeoipOverrideIpRange",    "GeoipOverrideIp6Range",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:58.228732Z
# ============================================================================