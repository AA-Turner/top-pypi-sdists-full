"""
Pydantic Models for CMDB - casb/attribute_match

Runtime validation models for casb/attribute_match configuration.
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

class AttributeMatchMatchRule(BaseModel):
    """
    Child table model for match.rule.
    
    CASB attribute match rule.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="CASB attribute rule ID.")    
    attribute: str | None = Field(max_length=79, default=None, description="CASB attribute match name.")    
    match_pattern: Literal["simple", "substr", "regexp"] | None = Field(default="simple", description="CASB attribute match pattern.")    
    match_value: str | None = Field(max_length=1023, default=None, description="CASB attribute match value.")    
    case_sensitive: Literal["enable", "disable"] | None = Field(default="disable", description="CASB attribute match case sensitive.")    
    negate: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable what the matching strategy must not be.")
class AttributeMatchMatch(BaseModel):
    """
    Child table model for match.
    
    CASB tenant match rules.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="CASB attribute match rule ID.")    
    rule_strategy: Literal["and", "or"] | None = Field(default="and", description="CASB attribute match rule strategy.")    
    rule: list[AttributeMatchMatchRule] = Field(default_factory=list, description="CASB attribute match rule.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class AttributeMatchModel(BaseModel):
    """
    Pydantic model for casb/attribute_match configuration.
    
    Configure CASB attribute match rule.
    
    Validation Rules:        - name: max_length=79 pattern=        - application: max_length=79 pattern=        - match_strategy: pattern=        - match: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=79, default=None, description="CASB attribute match name.")    
    application: str = Field(max_length=79, description="CASB attribute application name.")  # datasource: ['casb.saas-application.name']    
    match_strategy: Literal["or", "and", "subset"] | None = Field(default="or", description="CASB attribute match strategy.")    
    match: list[AttributeMatchMatch] = Field(default_factory=list, description="CASB tenant match rules.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('application')
    @classmethod
    def validate_application(cls, v: Any) -> Any:
        """
        Validate application field.
        
        Datasource: ['casb.saas-application.name']
        
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "AttributeMatchModel":
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
    async def validate_application_references(self, client: Any) -> list[str]:
        """
        Validate application references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - casb/saas-application        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = AttributeMatchModel(
            ...     application="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_application_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.casb.attribute_match.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "application", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.casb.saas_application.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Application '{value}' not found in "
                "casb/saas-application"
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
        
        errors = await self.validate_application_references(client)
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
    "AttributeMatchModel",    "AttributeMatchMatch",    "AttributeMatchMatch.Rule",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:38.236967Z
# ============================================================================