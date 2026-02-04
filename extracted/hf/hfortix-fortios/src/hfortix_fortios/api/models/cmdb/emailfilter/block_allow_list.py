"""
Pydantic Models for CMDB - emailfilter/block_allow_list

Runtime validation models for emailfilter/block_allow_list configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class BlockAllowListEntriesTypeEnum(str, Enum):
    """Allowed values for type_ field in entries."""
    IP = "ip"
    EMAIL_TO = "email-to"
    EMAIL_FROM = "email-from"
    SUBJECT = "subject"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class BlockAllowListEntries(BaseModel):
    """
    Child table model for entries.
    
    Anti-spam block/allow entries.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] = Field(default="enable", description="Enable/disable status.")    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Entry ID.")    
    type_: BlockAllowListEntriesTypeEnum = Field(default=BlockAllowListEntriesTypeEnum.IP, serialization_alias="type", description="Entry type.")    
    action: Literal["reject", "spam", "clear"] = Field(default="spam", description="Reject, mark as spam or good email.")    
    addr_type: Literal["ipv4", "ipv6"] = Field(default="ipv4", description="IP address type.")    
    ip4_subnet: str = Field(default="0.0.0.0 0.0.0.0", description="IPv4 network address/subnet mask bits.")    
    ip6_subnet: str = Field(default="::/128", description="IPv6 network address/subnet mask bits.")    
    pattern_type: Literal["wildcard", "regexp"] = Field(default="wildcard", description="Wildcard pattern or regular expression.")    
    pattern: str = Field(max_length=127, description="Pattern to match.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class BlockAllowListModel(BaseModel):
    """
    Pydantic model for emailfilter/block_allow_list configuration.
    
    Configure anti-spam block/allow list.
    
    Validation Rules:        - id_: min=0 max=4294967295 pattern=        - name: max_length=63 pattern=        - comment: max_length=255 pattern=        - entries: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    name: str = Field(max_length=63, description="Name of table.")    
    comment: str | None = Field(max_length=255, default=None, description="Optional comments.")    
    entries: list[BlockAllowListEntries] = Field(description="Anti-spam block/allow entries.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "BlockAllowListModel":
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
    "BlockAllowListModel",    "BlockAllowListEntries",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:41.048207Z
# ============================================================================