"""
Pydantic Models for MONITOR - fortiview/realtime_statistics

Runtime validation models for fortiview/realtime_statistics configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional

# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class RealtimeStatisticsModel(BaseModel):
    """
    Pydantic model for fortiview/realtime_statistics configuration.
    
    Retrieve realtime drill-down and summary data for FortiView.
    
    Validation Rules:        - srcaddr: pattern=        - dstaddr: pattern=        - srcaddr6: pattern=        - dstaddr6: pattern=        - srcport: pattern=        - dstport: pattern=        - srcintf: pattern=        - srcintfrole: pattern=        - dstintf: pattern=        - dstintfrole: pattern=        - policyid: pattern=        - security_policyid: pattern=        - protocol: pattern=        - web_category: pattern=        - web_domain: pattern=        - application: pattern=        - country: pattern=        - seconds: pattern=        - since: pattern=        - owner: pattern=        - username: pattern=        - shaper: pattern=        - srcuuid: pattern=        - dstuuid: pattern=        - sessionid: pattern=        - report_by: pattern=        - sort_by: pattern=        - ip_version: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    srcaddr: Any = Field(default=None)    
    dstaddr: Any = Field(default=None)    
    srcaddr6: Any = Field(default=None)    
    dstaddr6: Any = Field(default=None)    
    srcport: Any = Field(default=None)    
    dstport: Any = Field(default=None)    
    srcintf: Any = Field(default=None)    
    srcintfrole: Any = Field(default=None)    
    dstintf: Any = Field(default=None)    
    dstintfrole: Any = Field(default=None)    
    policyid: Any = Field(default=None)    
    security_policyid: Any = Field(default=None)    
    protocol: Any = Field(default=None)    
    web_category: Any = Field(default=None)    
    web_domain: Any = Field(default=None)    
    application: Any = Field(default=None)    
    country: Any = Field(default=None)    
    seconds: Any = Field(default=None)    
    since: Any = Field(default=None)    
    owner: Any = Field(default=None)    
    username: Any = Field(default=None)    
    shaper: Any = Field(default=None)    
    srcuuid: Any = Field(default=None)    
    dstuuid: Any = Field(default=None)    
    sessionid: Any = Field(default=None)    
    report_by: str | None = Field(default=None)    
    sort_by: str | None = Field(default=None)    
    ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = Field(default=None)    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "RealtimeStatisticsModel":
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
    "RealtimeStatisticsModel",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-05T01:53:53.122199Z
# ============================================================================