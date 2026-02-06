"""
Pydantic Models for CMDB - casb/user_activity

Runtime validation models for casb/user_activity configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class UserActivityMatchRulesTypeEnum(str, Enum):
    """Allowed values for type_ field in match.rules."""
    DOMAINS = "domains"
    HOST = "host"
    PATH = "path"
    HEADER = "header"
    HEADER_VALUE = "header-value"
    METHOD = "method"
    BODY = "body"

class UserActivityControlOptionsOperationsActionEnum(str, Enum):
    """Allowed values for action field in control-options.operations."""
    APPEND = "append"
    PREPEND = "prepend"
    REPLACE = "replace"
    NEW = "new"
    NEW_ON_NOT_FOUND = "new-on-not-found"
    DELETE = "delete"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class UserActivityMatchTenantExtractionFilters(BaseModel):
    """
    Child table model for match.tenant-extraction.filters.
    
    CASB user activity tenant extraction filters.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="CASB tenant extraction filter ID.")    
    direction: Literal["request", "response"] | None = Field(default="request", description="CASB tenant extraction filter direction.")    
    place: Literal["path", "header", "body"] | None = Field(default="header", description="CASB tenant extraction filter place type.")    
    header_name: str | None = Field(max_length=255, default=None, description="CASB tenant extraction filter header name.")    
    body_type: Literal["json"] | None = Field(default="json", description="CASB tenant extraction filter body type.")
class UserActivityMatchTenantExtraction(BaseModel):
    """
    Child table model for match.tenant-extraction.
    
    CASB user activity tenant extraction.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable CASB tenant extraction.")    
    type_: Literal["json-query"] | None = Field(default="json-query", serialization_alias="type", description="CASB user activity tenant extraction type.")    
    jq: str | None = Field(max_length=1023, default=None, description="CASB user activity tenant extraction jq script.")    
    filters: list[UserActivityMatchTenantExtractionFilters] = Field(default_factory=list, description="CASB user activity tenant extraction filters.")
class UserActivityMatchRulesMethods(BaseModel):
    """
    Child table model for match.rules.methods.
    
    CASB user activity method list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    method: str | None = Field(max_length=79, default=None, description="User activity method.")
class UserActivityMatchRulesDomains(BaseModel):
    """
    Child table model for match.rules.domains.
    
    CASB user activity domain list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    domain: str = Field(max_length=127, description="Domain list separated by space.")
class UserActivityMatchRules(BaseModel):
    """
    Child table model for match.rules.
    
    CASB user activity rules.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="CASB user activity rule ID.")    
    type_: UserActivityMatchRulesTypeEnum | None = Field(default=UserActivityMatchRulesTypeEnum.HOST, serialization_alias="type", description="CASB user activity rule type.")    
    domains: list[UserActivityMatchRulesDomains] = Field(default_factory=list, description="CASB user activity domain list.")    
    methods: list[UserActivityMatchRulesMethods] = Field(default_factory=list, description="CASB user activity method list.")    
    match_pattern: Literal["simple", "substr", "regexp"] | None = Field(default="simple", description="CASB user activity rule match pattern.")    
    match_value: str | None = Field(max_length=1023, default=None, description="CASB user activity rule match value.")    
    header_name: str | None = Field(max_length=255, default=None, description="CASB user activity rule header name.")    
    body_type: Literal["json"] | None = Field(default="json", description="CASB user activity match rule body type.")    
    jq: str | None = Field(max_length=255, default=None, description="CASB user activity rule match jq script.")    
    case_sensitive: Literal["enable", "disable"] | None = Field(default="disable", description="CASB user activity match case sensitive.")    
    negate: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable what the matching strategy must not be.")
class UserActivityMatch(BaseModel):
    """
    Child table model for match.
    
    CASB user activity match rules.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="CASB user activity match rules ID.")    
    strategy: Literal["and", "or"] | None = Field(default="and", description="CASB user activity rules strategy.")    
    rules: list[UserActivityMatchRules] = Field(default_factory=list, description="CASB user activity rules.")    
    tenant_extraction: UserActivityMatchTenantExtraction | None = Field(default=None, description="CASB user activity tenant extraction.")
class UserActivityControlOptionsOperationsValues(BaseModel):
    """
    Child table model for control-options.operations.values.
    
    CASB operation new values.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    value: str | None = Field(max_length=79, default=None, description="Operation value.")
class UserActivityControlOptionsOperations(BaseModel):
    """
    Child table model for control-options.operations.
    
    CASB control option operations.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="CASB control option operation name.")    
    target: Literal["header", "path", "body"] | None = Field(default="header", description="CASB operation target.")    
    action: UserActivityControlOptionsOperationsActionEnum | None = Field(default=UserActivityControlOptionsOperationsActionEnum.APPEND, description="CASB operation action.")    
    direction: Literal["request", "response"] | None = Field(default="request", description="CASB operation direction.")    
    header_name: str | None = Field(max_length=255, default=None, description="CASB operation header name to search.")    
    search_pattern: Literal["simple", "substr", "regexp"] | None = Field(default="simple", description="CASB operation search pattern.")    
    search_key: str | None = Field(max_length=1023, default=None, description="CASB operation key to search.")    
    case_sensitive: Literal["enable", "disable"] | None = Field(default="disable", description="CASB operation search case sensitive.")    
    value_from_input: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable value from user input.")    
    value_name_from_input: str | None = Field(max_length=79, default=None, description="CASB operation value name from user input.")    
    values: list[UserActivityControlOptionsOperationsValues] = Field(description="CASB operation new values.")
class UserActivityControlOptions(BaseModel):
    """
    Child table model for control-options.
    
    CASB control options.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="CASB control option name.")    
    status: Literal["enable", "disable"] | None = Field(default="enable", description="CASB control option status.")    
    operations: list[UserActivityControlOptionsOperations] = Field(default_factory=list, description="CASB control option operations.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class UserActivityCategoryEnum(str, Enum):
    """Allowed values for category field."""
    ACTIVITY_CONTROL = "activity-control"
    TENANT_CONTROL = "tenant-control"
    DOMAIN_CONTROL = "domain-control"
    SAFE_SEARCH_CONTROL = "safe-search-control"
    ADVANCED_TENANT_CONTROL = "advanced-tenant-control"
    OTHER = "other"


# ============================================================================
# Main Model
# ============================================================================

class UserActivityModel(BaseModel):
    """
    Pydantic model for casb/user_activity configuration.
    
    Configure CASB user activity.
    
    Validation Rules:        - name: max_length=79 pattern=        - uuid: max_length=36 pattern=        - status: pattern=        - description: max_length=63 pattern=        - type_: pattern=        - casb_name: max_length=79 pattern=        - application: max_length=79 pattern=        - category: pattern=        - match_strategy: pattern=        - match: pattern=        - control_options: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=79, default=None, description="CASB user activity name.")    
    uuid: str | None = Field(max_length=36, default=None, description="Universally Unique Identifier (UUID; automatically assigned but can be manually reset).")    
    status: Literal["enable", "disable"] | None = Field(default="enable", description="CASB user activity status.")    
    description: str | None = Field(max_length=63, default=None, description="CASB user activity description.")    
    type_: Literal["built-in", "customized"] | None = Field(default="customized", serialization_alias="type", description="CASB user activity type.")    
    casb_name: str | None = Field(max_length=79, default=None, description="CASB user activity signature name.")    
    application: str = Field(max_length=79, description="CASB SaaS application name.")  # datasource: ['casb.saas-application.name']    
    category: UserActivityCategoryEnum | None = Field(default=UserActivityCategoryEnum.ACTIVITY_CONTROL, description="CASB user activity category.")    
    match_strategy: Literal["and", "or"] | None = Field(default="or", description="CASB user activity match strategy.")    
    match: list[UserActivityMatch] = Field(default_factory=list, description="CASB user activity match rules.")    
    control_options: list[UserActivityControlOptions] = Field(default_factory=list, description="CASB control options.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "UserActivityModel":
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
            >>> policy = UserActivityModel(
            ...     application="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_application_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.casb.user_activity.post(policy.to_fortios_dict())
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
    "UserActivityModel",    "UserActivityMatch",    "UserActivityMatch.Rules",    "UserActivityMatch.Rules.Domains",    "UserActivityMatch.Rules.Methods",    "UserActivityMatch.TenantExtraction",    "UserActivityMatch.TenantExtraction.Filters",    "UserActivityControlOptions",    "UserActivityControlOptions.Operations",    "UserActivityControlOptions.Operations.Values",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:29.040479Z
# ============================================================================