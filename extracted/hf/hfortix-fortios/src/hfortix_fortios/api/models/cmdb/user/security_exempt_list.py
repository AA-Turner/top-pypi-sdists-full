"""
Pydantic Models for CMDB - user/security_exempt_list

Runtime validation models for user/security_exempt_list configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Optional

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class SecurityExemptListRuleSrcaddr(BaseModel):
    """
    Child table model for rule.srcaddr.
    
    Source addresses or address groups.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Address or group name.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']
class SecurityExemptListRuleService(BaseModel):
    """
    Child table model for rule.service.
    
    Destination services.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Service name.")  # datasource: ['firewall.service.custom.name', 'firewall.service.group.name']
class SecurityExemptListRuleDstaddr(BaseModel):
    """
    Child table model for rule.dstaddr.
    
    Destination addresses or address groups.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Address or group name.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']
class SecurityExemptListRule(BaseModel):
    """
    Child table model for rule.
    
    Configure rules for exempting users from captive portal authentication.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    srcaddr: list[SecurityExemptListRuleSrcaddr] = Field(default_factory=list, description="Source addresses or address groups.")    
    dstaddr: list[SecurityExemptListRuleDstaddr] = Field(default_factory=list, description="Destination addresses or address groups.")    
    service: list[SecurityExemptListRuleService] = Field(default_factory=list, description="Destination services.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class SecurityExemptListModel(BaseModel):
    """
    Pydantic model for user/security_exempt_list configuration.
    
    Configure security exemption list.
    
    Validation Rules:        - name: max_length=35 pattern=        - description: max_length=127 pattern=        - rule: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=35, default=None, description="Name of the exempt list.")    
    description: str | None = Field(max_length=127, default=None, description="Description.")    
    rule: list[SecurityExemptListRule] = Field(default_factory=list, description="Configure rules for exempting users from captive portal authentication.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "SecurityExemptListModel":
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
    "SecurityExemptListModel",    "SecurityExemptListRule",    "SecurityExemptListRule.Srcaddr",    "SecurityExemptListRule.Dstaddr",    "SecurityExemptListRule.Service",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:28.319454Z
# ============================================================================