"""
Pydantic Models for CMDB - firewall/internet_service_fortiguard

Runtime validation models for firewall/internet_service_fortiguard configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class InternetServiceFortiguardEntryPortRange(BaseModel):
    """
    Child table model for entry.port-range.
    
    Port ranges in the custom entry.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Custom entry port range ID.")    
    start_port: int = Field(ge=0, le=65535, default=1, description="Integer value for starting TCP/UDP/SCTP destination port in range (0 to 65535).")    
    end_port: int = Field(ge=0, le=65535, default=65535, description="Integer value for ending TCP/UDP/SCTP destination port in range (0 to 65535).")
class InternetServiceFortiguardEntryDst6(BaseModel):
    """
    Child table model for entry.dst6.
    
    Destination address6 or address6 group name.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="Select the destination address6 or address group object from available options.")  # datasource: ['firewall.address6.name', 'firewall.addrgrp6.name']
class InternetServiceFortiguardEntryDst(BaseModel):
    """
    Child table model for entry.dst.
    
    Destination address or address group name.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="Select the destination address or address group object from available options.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']
class InternetServiceFortiguardEntry(BaseModel):
    """
    Child table model for entry.
    
    Entries added to the Internet Service FortiGuard database.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=255, default=0, serialization_alias="id", description="Entry ID(1-255).")    
    addr_mode: Literal["ipv4", "ipv6"] | None = Field(default="ipv4", description="Address mode (IPv4 or IPv6).")    
    protocol: int | None = Field(ge=0, le=255, default=0, description="Integer value for the protocol type as defined by IANA (0 - 255).")    
    port_range: list[InternetServiceFortiguardEntryPortRange] = Field(default_factory=list, description="Port ranges in the custom entry.")    
    dst: list[InternetServiceFortiguardEntryDst] = Field(default_factory=list, description="Destination address or address group name.")    
    dst6: list[InternetServiceFortiguardEntryDst6] = Field(default_factory=list, description="Destination address6 or address6 group name.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class InternetServiceFortiguardModel(BaseModel):
    """
    Pydantic model for firewall/internet_service_fortiguard configuration.
    
    Configure FortiGuard Internet Services.
    
    Validation Rules:        - name: max_length=63 pattern=        - comment: max_length=255 pattern=        - entry: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=63, default=None, description="Internet Service name.")    
    comment: str | None = Field(max_length=255, default=None, description="Comment.")    
    entry: list[InternetServiceFortiguardEntry] = Field(default_factory=list, description="Entries added to the Internet Service FortiGuard database.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "InternetServiceFortiguardModel":
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
    "InternetServiceFortiguardModel",    "InternetServiceFortiguardEntry",    "InternetServiceFortiguardEntry.PortRange",    "InternetServiceFortiguardEntry.Dst",    "InternetServiceFortiguardEntry.Dst6",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:28.826214Z
# ============================================================================