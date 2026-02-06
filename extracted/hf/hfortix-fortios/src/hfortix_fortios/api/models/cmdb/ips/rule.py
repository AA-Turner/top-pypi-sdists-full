"""
Pydantic Models for CMDB - ips/rule

Runtime validation models for ips/rule configuration.
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

class RuleStatusSensorName(BaseModel):
    """
    Child table model for status.<sensor name>.
    
    IPS sensor name.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    filter_name: Any = Field(default=None, description="IPS filter name.")
class RuleStatus(BaseModel):
    """
    Child table model for status.
    
    Print all IPS rule status information.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    sensor_name: list[RuleStatusSensorName] = Field(default_factory=list, description="IPS sensor name.")
class RuleMetadata(BaseModel):
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

class RuleModel(BaseModel):
    """
    Pydantic model for ips/rule configuration.
    
    Configure IPS rules.
    
    Validation Rules:        - name: max_length=63 pattern=        - status: pattern=        - log: pattern=        - log_packet: pattern=        - action: pattern=        - group: max_length=63 pattern=        - severity: pattern=        - location: pattern=        - os: pattern=        - application: pattern=        - service: pattern=        - rule_id: min=0 max=4294967295 pattern=        - rev: min=0 max=4294967295 pattern=        - date: min=0 max=4294967295 pattern=        - metadata: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=63, default=None, description="Rule name.")    
    status: list[RuleStatus] = Field(default_factory=list, description="Print all IPS rule status information.")    
    log: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable logging.")    
    log_packet: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable packet logging.")    
    action: Literal["pass", "block"] | None = Field(default="pass", description="Action.")    
    group: str | None = Field(max_length=63, default=None, description="Group.")    
    severity: str | None = Field(default=None, description="Severity.")    
    location: list[str] = Field(default_factory=list, description="Vulnerable location.")    
    os: str | None = Field(default=None, description="Vulnerable operation systems.")    
    application: str | None = Field(default=None, description="Vulnerable applications.")    
    service: str | None = Field(default=None, description="Vulnerable service.")    
    rule_id: int | None = Field(ge=0, le=4294967295, default=0, description="Rule ID.")    
    rev: int | None = Field(ge=0, le=4294967295, default=0, description="Revision.")    
    date: int | None = Field(ge=0, le=4294967295, default=0, description="Date.")    
    metadata: list[RuleMetadata] = Field(default_factory=list, description="Meta data.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "RuleModel":
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
    "RuleModel",    "RuleStatus",    "RuleStatus.<Sensor Name>",    "RuleMetadata",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:29.463651Z
# ============================================================================