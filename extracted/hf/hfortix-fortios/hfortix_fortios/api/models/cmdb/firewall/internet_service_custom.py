"""
Pydantic Models for CMDB - firewall/internet_service_custom

Runtime validation models for firewall/internet_service_custom configuration.
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

class InternetServiceCustomEntryPortRange(BaseModel):
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
class InternetServiceCustomEntryDst6(BaseModel):
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
class InternetServiceCustomEntryDst(BaseModel):
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
class InternetServiceCustomEntry(BaseModel):
    """
    Child table model for entry.
    
    Entries added to the Internet Service database and custom database.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=255, default=0, serialization_alias="id", description="Entry ID(1-255).")    
    addr_mode: Literal["ipv4", "ipv6"] | None = Field(default="ipv4", description="Address mode (IPv4 or IPv6).")    
    protocol: int | None = Field(ge=0, le=255, default=0, description="Integer value for the protocol type as defined by IANA (0 - 255).")    
    port_range: list[InternetServiceCustomEntryPortRange] = Field(default_factory=list, description="Port ranges in the custom entry.")    
    dst: list[InternetServiceCustomEntryDst] = Field(default_factory=list, description="Destination address or address group name.")    
    dst6: list[InternetServiceCustomEntryDst6] = Field(default_factory=list, description="Destination address6 or address6 group name.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class InternetServiceCustomModel(BaseModel):
    """
    Pydantic model for firewall/internet_service_custom configuration.
    
    Configure custom Internet Services.
    
    Validation Rules:        - name: max_length=63 pattern=        - reputation: min=0 max=4294967295 pattern=        - comment: max_length=255 pattern=        - entry: pattern=    """
    
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
    reputation: int | None = Field(ge=0, le=4294967295, default=3, description="Reputation level of the custom Internet Service.")  # datasource: ['firewall.internet-service-reputation.id']    
    comment: str | None = Field(max_length=255, default=None, description="Comment.")    
    entry: list[InternetServiceCustomEntry] = Field(default_factory=list, description="Entries added to the Internet Service database and custom database.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('reputation')
    @classmethod
    def validate_reputation(cls, v: Any) -> Any:
        """
        Validate reputation field.
        
        Datasource: ['firewall.internet-service-reputation.id']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "InternetServiceCustomModel":
        """
        Create model instance from FortiOS API response.
        
        Args:
            data: Response data from API
            
        Returns:
            Validated model instance
        """
        return cls(**data)
    # ========================================================================
    # Datasource Validation Methods
    # ========================================================================    
    async def validate_reputation_references(self, client: Any) -> list[str]:
        """
        Validate reputation references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/internet-service-reputation        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = InternetServiceCustomModel(
            ...     reputation="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_reputation_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.firewall.internet_service_custom.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "reputation", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.firewall.internet_service_reputation.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Reputation '{value}' not found in "
                "firewall/internet-service-reputation"
            )        
        return errors    
    async def validate_all_references(self, client: Any) -> list[str]:
        """
        Validate ALL datasource references in this model.
        
        Convenience method that runs all validate_*_references() methods
        and aggregates the results.
        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of all validation errors found
            
        Example:
            >>> errors = await policy.validate_all_references(fgt._client)
            >>> if errors:
            ...     for error in errors:
            ...         print(f"  - {error}")
        """
        all_errors = []
        
        errors = await self.validate_reputation_references(client)
        all_errors.extend(errors)        
        return all_errors

# ============================================================================
# Type Aliases for Convenience
# ============================================================================

Dict = dict[str, Any]  # For backward compatibility

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "InternetServiceCustomModel",    "InternetServiceCustomEntry",    "InternetServiceCustomEntry.PortRange",    "InternetServiceCustomEntry.Dst",    "InternetServiceCustomEntry.Dst6",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:58.267082Z
# ============================================================================