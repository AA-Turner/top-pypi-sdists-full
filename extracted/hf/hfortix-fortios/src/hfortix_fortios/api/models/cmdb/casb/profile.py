"""
Pydantic Models for CMDB - casb/profile

Runtime validation models for casb/profile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class ProfileSaasApplicationAccessRuleBypassEnum(str, Enum):
    """Allowed values for bypass field in saas-application.access-rule."""
    AV = "av"
    DLP = "dlp"
    WEB_FILTER = "web-filter"
    FILE_FILTER = "file-filter"
    VIDEO_FILTER = "video-filter"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ProfileSaasApplicationTenantControlTenants(BaseModel):
    """
    Child table model for saas-application.tenant-control-tenants.
    
    CASB profile tenant control tenants.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Tenant control tenants name.")
class ProfileSaasApplicationSafeSearchControl(BaseModel):
    """
    Child table model for saas-application.safe-search-control.
    
    CASB profile safe search control.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Safe search control name.")
class ProfileSaasApplicationDomainControlDomains(BaseModel):
    """
    Child table model for saas-application.domain-control-domains.
    
    CASB profile domain control domains.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Domain control domain name.")
class ProfileSaasApplicationCustomControlOptionUserInput(BaseModel):
    """
    Child table model for saas-application.custom-control.option.user-input.
    
    CASB custom control user input.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    value: str | None = Field(max_length=79, default=None, description="user input value.")
class ProfileSaasApplicationCustomControlOption(BaseModel):
    """
    Child table model for saas-application.custom-control.option.
    
    CASB custom control option.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="CASB custom control option name.")    
    user_input: list[ProfileSaasApplicationCustomControlOptionUserInput] = Field(default_factory=list, description="CASB custom control user input.")
class ProfileSaasApplicationCustomControlAttributeFilter(BaseModel):
    """
    Child table model for saas-application.custom-control.attribute-filter.
    
    CASB attribute filter.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="CASB tenant control ID.")    
    attribute_match: str = Field(max_length=79, description="CASB access rule tenant match.")  # datasource: ['casb.attribute-match.name']    
    action: Literal["monitor", "bypass", "block"] | None = Field(default="monitor", description="CASB access rule tenant control action.")
class ProfileSaasApplicationCustomControl(BaseModel):
    """
    Child table model for saas-application.custom-control.
    
    CASB profile custom control.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="CASB custom control user activity name.")  # datasource: ['casb.user-activity.name']    
    option: list[ProfileSaasApplicationCustomControlOption] = Field(default_factory=list, description="CASB custom control option.")    
    attribute_filter: list[ProfileSaasApplicationCustomControlAttributeFilter] = Field(default_factory=list, description="CASB attribute filter.")
class ProfileSaasApplicationAdvancedTenantControlAttributeInput(BaseModel):
    """
    Child table model for saas-application.advanced-tenant-control.attribute.input.
    
    CASB extend user input value.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    value: str | None = Field(max_length=79, default=None, description="User input value.")
class ProfileSaasApplicationAdvancedTenantControlAttribute(BaseModel):
    """
    Child table model for saas-application.advanced-tenant-control.attribute.
    
    CASB advanced tenant control attribute.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="CASB extend user input name.")    
    input_: list[ProfileSaasApplicationAdvancedTenantControlAttributeInput] = Field(default_factory=list, serialization_alias="input", description="CASB extend user input value.")
class ProfileSaasApplicationAdvancedTenantControl(BaseModel):
    """
    Child table model for saas-application.advanced-tenant-control.
    
    CASB profile advanced tenant control.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="CASB advanced tenant control name.")  # datasource: ['casb.user-activity.name']    
    attribute: list[ProfileSaasApplicationAdvancedTenantControlAttribute] = Field(default_factory=list, description="CASB advanced tenant control attribute.")
class ProfileSaasApplicationAccessRuleAttributeFilter(BaseModel):
    """
    Child table model for saas-application.access-rule.attribute-filter.
    
    CASB profile attribute filter.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="CASB tenant control ID.")    
    attribute_match: str = Field(max_length=79, description="CASB access rule tenant match.")  # datasource: ['casb.attribute-match.name']    
    action: Literal["monitor", "bypass", "block"] | None = Field(default="monitor", description="CASB access rule tenant control action.")
class ProfileSaasApplicationAccessRule(BaseModel):
    """
    Child table model for saas-application.access-rule.
    
    CASB profile access rule.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="CASB access rule activity name.")  # datasource: ['casb.user-activity.name']    
    action: Literal["monitor", "bypass", "block"] | None = Field(default="monitor", description="CASB access rule action.")    
    bypass: list[ProfileSaasApplicationAccessRuleBypassEnum] = Field(default_factory=list, description="CASB bypass options.")    
    attribute_filter: list[ProfileSaasApplicationAccessRuleAttributeFilter] = Field(default_factory=list, description="CASB profile attribute filter.")
class ProfileSaasApplication(BaseModel):
    """
    Child table model for saas-application.
    
    CASB profile SaaS application.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="CASB profile SaaS application name.")  # datasource: ['casb.saas-application.name']    
    status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable setting.")    
    safe_search: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable safe search.")    
    safe_search_control: list[ProfileSaasApplicationSafeSearchControl] = Field(description="CASB profile safe search control.")    
    tenant_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable tenant control.")    
    tenant_control_tenants: list[ProfileSaasApplicationTenantControlTenants] = Field(description="CASB profile tenant control tenants.")    
    advanced_tenant_control: list[ProfileSaasApplicationAdvancedTenantControl] = Field(default_factory=list, description="CASB profile advanced tenant control.")    
    domain_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable domain control.")    
    domain_control_domains: list[ProfileSaasApplicationDomainControlDomains] = Field(description="CASB profile domain control domains.")    
    log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable log settings.")    
    access_rule: list[ProfileSaasApplicationAccessRule] = Field(default_factory=list, description="CASB profile access rule.")    
    custom_control: list[ProfileSaasApplicationCustomControl] = Field(default_factory=list, description="CASB profile custom control.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class ProfileModel(BaseModel):
    """
    Pydantic model for casb/profile configuration.
    
    Configure CASB profile.
    
    Validation Rules:        - name: max_length=47 pattern=        - comment: max_length=255 pattern=        - saas_application: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=47, default=None, description="CASB profile name.")    
    comment: str | None = Field(max_length=255, default=None, description="Comment.")    
    saas_application: list[ProfileSaasApplication] = Field(default_factory=list, description="CASB profile SaaS application.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "ProfileModel":
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
    async def validate_saas_application_references(self, client: Any) -> list[str]:
        """
        Validate saas_application references exist in FortiGate.
        
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
            >>> policy = ProfileModel(
            ...     saas_application=[{"name": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_saas_application_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.casb.profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "saas_application", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("name")
            else:
                value = getattr(item, "name", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.casb.saas_application.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Saas-Application '{value}' not found in "
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
        
        errors = await self.validate_saas_application_references(client)
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
    "ProfileModel",    "ProfileSaasApplication",    "ProfileSaasApplication.SafeSearchControl",    "ProfileSaasApplication.TenantControlTenants",    "ProfileSaasApplication.AdvancedTenantControl",    "ProfileSaasApplication.AdvancedTenantControl.Attribute",    "ProfileSaasApplication.AdvancedTenantControl.Attribute.Input",    "ProfileSaasApplication.DomainControlDomains",    "ProfileSaasApplication.AccessRule",    "ProfileSaasApplication.AccessRule.AttributeFilter",    "ProfileSaasApplication.CustomControl",    "ProfileSaasApplication.CustomControl.Option",    "ProfileSaasApplication.CustomControl.Option.UserInput",    "ProfileSaasApplication.CustomControl.AttributeFilter",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:29.488574Z
# ============================================================================