"""
Pydantic Models for CMDB - emailfilter/bword

Runtime validation models for emailfilter/bword configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class BwordEntriesLanguageEnum(str, Enum):
    """Allowed values for language field in entries."""
    WESTERN = "western"
    SIMCH = "simch"
    TRACH = "trach"
    JAPANESE = "japanese"
    KOREAN = "korean"
    FRENCH = "french"
    THAI = "thai"
    SPANISH = "spanish"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class BwordEntries(BaseModel):
    """
    Child table model for entries.
    
    Spam filter banned word.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] = Field(default="enable", description="Enable/disable status.")    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Banned word entry ID.")    
    pattern: str = Field(max_length=127, description="Pattern for the banned word.")    
    pattern_type: Literal["wildcard", "regexp"] = Field(default="wildcard", description="Wildcard pattern or regular expression.")    
    action: Literal["spam", "clear"] = Field(default="spam", description="Mark spam or good.")    
    where: Literal["subject", "body", "all"] = Field(default="all", description="Component of the email to be scanned.")    
    language: BwordEntriesLanguageEnum = Field(default=BwordEntriesLanguageEnum.WESTERN, description="Language for the banned word.")    
    score: int | None = Field(ge=1, le=99999, default=10, description="Score value.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class BwordModel(BaseModel):
    """
    Pydantic model for emailfilter/bword configuration.
    
    Configure AntiSpam banned word list.
    
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
    entries: list[BwordEntries] = Field(default_factory=list, description="Spam filter banned word.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "BwordModel":
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
    "BwordModel",    "BwordEntries",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:39.885521Z
# ============================================================================