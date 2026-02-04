"""
Pydantic Models for MONITOR - firewall/sessions

Runtime validation models for firewall/sessions configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class SessionsProtocolEnum(str, Enum):
    """Allowed values for protocol field."""
    ALL = "all"
    IGMP = "igmp"
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ETC = "etc"


# ============================================================================
# Main Model
# ============================================================================

class SessionsModel(BaseModel):
    """
    Pydantic model for firewall/sessions configuration.
    
    List all active firewall sessions (optionally filtered).
    
    Validation Rules:        - ip_version: pattern=        - count: pattern=        - summary: pattern=        - srcport: pattern=        - policyid: pattern=        - security_policyid: pattern=        - application: pattern=        - protocol: pattern=        - dstport: pattern=        - srcintf: pattern=        - dstintf: pattern=        - srcintfrole: pattern=        - dstintfrole: pattern=        - srcaddr: pattern=        - srcaddr6: pattern=        - srcuuid: pattern=        - dstaddr: pattern=        - dstaddr6: pattern=        - dstuuid: pattern=        - username: pattern=        - shaper: pattern=        - country: pattern=        - owner: pattern=        - natsourceaddress: pattern=        - natsourceport: pattern=        - since: pattern=        - seconds: pattern=        - fortiasic: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = Field(default=None)    
    count: Any = Field()    
    summary: Any = Field(default=None)    
    srcport: Any = Field(default=None)    
    policyid: Any = Field(default=None)    
    security_policyid: Any = Field(default=None)    
    application: Any = Field(default=None)    
    protocol: SessionsProtocolEnum | None = Field(default=None)    
    dstport: Any = Field(default=None)    
    srcintf: Any = Field(default=None)    
    dstintf: Any = Field(default=None)    
    srcintfrole: Any = Field(default=None)    
    dstintfrole: Any = Field(default=None)    
    srcaddr: Any = Field(default=None)    
    srcaddr6: Any = Field(default=None)    
    srcuuid: Any = Field(default=None)    
    dstaddr: Any = Field(default=None)    
    dstaddr6: Any = Field(default=None)    
    dstuuid: Any = Field(default=None)    
    username: Any = Field(default=None)    
    shaper: Any = Field(default=None)    
    country: Any = Field(default=None)    
    owner: Any = Field(default=None)    
    natsourceaddress: Any = Field(default=None)    
    natsourceport: Any = Field(default=None)    
    since: Any = Field(default=None)    
    seconds: Any = Field(default=None)    
    fortiasic: Any = Field(default=None)    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "SessionsModel":
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
    "SessionsModel",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:43.471367Z
# ============================================================================