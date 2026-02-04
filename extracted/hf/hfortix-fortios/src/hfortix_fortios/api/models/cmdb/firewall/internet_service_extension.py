"""
Pydantic Models for CMDB - firewall/internet_service_extension

Runtime validation models for firewall/internet_service_extension configuration.
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

class InternetServiceExtensionEntryPortRange(BaseModel):
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
class InternetServiceExtensionEntryDst6(BaseModel):
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
class InternetServiceExtensionEntryDst(BaseModel):
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
class InternetServiceExtensionEntry(BaseModel):
    """
    Child table model for entry.
    
    Entries added to the Internet Service extension database.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=255, default=0, serialization_alias="id", description="Entry ID(1-255).")    
    addr_mode: Literal["ipv4", "ipv6"] | None = Field(default="ipv4", description="Address mode (IPv4 or IPv6).")    
    protocol: int | None = Field(ge=0, le=255, default=0, description="Integer value for the protocol type as defined by IANA (0 - 255).")    
    port_range: list[InternetServiceExtensionEntryPortRange] = Field(default_factory=list, description="Port ranges in the custom entry.")    
    dst: list[InternetServiceExtensionEntryDst] = Field(default_factory=list, description="Destination address or address group name.")    
    dst6: list[InternetServiceExtensionEntryDst6] = Field(default_factory=list, description="Destination address6 or address6 group name.")
class InternetServiceExtensionDisableEntryPortRange(BaseModel):
    """
    Child table model for disable-entry.port-range.
    
    Port ranges in the disable entry.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Custom entry port range ID.")    
    start_port: int = Field(ge=0, le=65535, default=1, description="Starting TCP/UDP/SCTP destination port (0 to 65535).")    
    end_port: int = Field(ge=0, le=65535, default=65535, description="Ending TCP/UDP/SCTP destination port (0 to 65535).")
class InternetServiceExtensionDisableEntryIp6Range(BaseModel):
    """
    Child table model for disable-entry.ip6-range.
    
    IPv6 ranges in the disable entry.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Disable entry range ID.")    
    start_ip6: str = Field(default="::", description="Start IPv6 address.")    
    end_ip6: str = Field(default="::", description="End IPv6 address.")
class InternetServiceExtensionDisableEntryIpRange(BaseModel):
    """
    Child table model for disable-entry.ip-range.
    
    IPv4 ranges in the disable entry.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Disable entry range ID.")    
    start_ip: str = Field(default="0.0.0.0", description="Start IPv4 address.")    
    end_ip: str = Field(default="0.0.0.0", description="End IPv4 address.")
class InternetServiceExtensionDisableEntry(BaseModel):
    """
    Child table model for disable-entry.
    
    Disable entries in the Internet Service database.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Disable entry ID.")    
    addr_mode: Literal["ipv4", "ipv6"] | None = Field(default="ipv4", description="Address mode (IPv4 or IPv6).")    
    protocol: int = Field(ge=0, le=255, default=0, description="Integer value for the protocol type as defined by IANA (0 - 255).")    
    port_range: list[InternetServiceExtensionDisableEntryPortRange] = Field(default_factory=list, description="Port ranges in the disable entry.")    
    ip_range: list[InternetServiceExtensionDisableEntryIpRange] = Field(default_factory=list, description="IPv4 ranges in the disable entry.")    
    ip6_range: list[InternetServiceExtensionDisableEntryIp6Range] = Field(default_factory=list, description="IPv6 ranges in the disable entry.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class InternetServiceExtensionModel(BaseModel):
    """
    Pydantic model for firewall/internet_service_extension configuration.
    
    Configure Internet Services Extension.
    
    Validation Rules:        - id_: min=0 max=4294967295 pattern=        - comment: max_length=255 pattern=        - entry: pattern=        - disable_entry: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Internet Service ID in the Internet Service database.")  # datasource: ['firewall.internet-service.id']    
    comment: str | None = Field(max_length=255, default=None, description="Comment.")    
    entry: list[InternetServiceExtensionEntry] = Field(default_factory=list, description="Entries added to the Internet Service extension database.")    
    disable_entry: list[InternetServiceExtensionDisableEntry] = Field(default_factory=list, description="Disable entries in the Internet Service database.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('id_')
    @classmethod
    def validate_id_(cls, v: Any) -> Any:
        """
        Validate id_ field.
        
        Datasource: ['firewall.internet-service.id']
        
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "InternetServiceExtensionModel":
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
    async def validate_id_references(self, client: Any) -> list[str]:
        """
        Validate id references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/internet-service        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = InternetServiceExtensionModel(
            ...     id="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_id_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.firewall.internet_service_extension.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "id", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.firewall.internet_service.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Id '{value}' not found in "
                "firewall/internet-service"
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
        
        errors = await self.validate_id_references(client)
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
    "InternetServiceExtensionModel",    "InternetServiceExtensionEntry",    "InternetServiceExtensionEntry.PortRange",    "InternetServiceExtensionEntry.Dst",    "InternetServiceExtensionEntry.Dst6",    "InternetServiceExtensionDisableEntry",    "InternetServiceExtensionDisableEntry.PortRange",    "InternetServiceExtensionDisableEntry.IpRange",    "InternetServiceExtensionDisableEntry.Ip6Range",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:40.257125Z
# ============================================================================