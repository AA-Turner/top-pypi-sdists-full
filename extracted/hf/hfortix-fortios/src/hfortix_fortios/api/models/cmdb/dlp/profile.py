"""
Pydantic Models for CMDB - dlp/profile

Runtime validation models for dlp/profile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class ProfileRuleSeverityEnum(str, Enum):
    """Allowed values for severity field in rule."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ProfileRuleProtoEnum(str, Enum):
    """Allowed values for proto field in rule."""
    SMTP = "smtp"
    POP3 = "pop3"
    IMAP = "imap"
    HTTP_GET = "http-get"
    HTTP_POST = "http-post"
    FTP = "ftp"
    NNTP = "nntp"
    MAPI = "mapi"
    SSH = "ssh"
    CIFS = "cifs"

class ProfileRuleFilterByEnum(str, Enum):
    """Allowed values for filter_by field in rule."""
    SENSOR = "sensor"
    LABEL = "label"
    FINGERPRINT = "fingerprint"
    ENCRYPTED = "encrypted"
    NONE = "none"

class ProfileRuleActionEnum(str, Enum):
    """Allowed values for action field in rule."""
    ALLOW = "allow"
    LOG_ONLY = "log-only"
    BLOCK = "block"
    QUARANTINE_IP = "quarantine-ip"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ProfileRuleSensor(BaseModel):
    """
    Child table model for rule.sensor.
    
    Select DLP sensors.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Address name.")  # datasource: ['dlp.sensor.name']
class ProfileRuleSensitivity(BaseModel):
    """
    Child table model for rule.sensitivity.
    
    Select a DLP file pattern sensitivity to match.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Select a DLP sensitivity.")  # datasource: ['dlp.sensitivity.name']
class ProfileRule(BaseModel):
    """
    Child table model for rule.
    
    Set up DLP rules for this profile.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    name: str | None = Field(max_length=35, default=None, description="Filter name.")    
    severity: ProfileRuleSeverityEnum | None = Field(default=ProfileRuleSeverityEnum.MEDIUM, description="Select the severity or threat level that matches this filter.")    
    type_: Literal["file", "message"] | None = Field(default="file", serialization_alias="type", description="Select whether to check the content of messages (an email message) or files (downloaded files or email attachments).")    
    proto: list[ProfileRuleProtoEnum] = Field(default_factory=list, description="Check messages or files over one or more of these protocols.")    
    filter_by: ProfileRuleFilterByEnum | None = Field(default=ProfileRuleFilterByEnum.NONE, description="Select the type of content to match.")    
    file_size: int | None = Field(ge=0, le=4193280, default=0, description="Match files greater than or equal to this size (KB).")    
    sensitivity: list[ProfileRuleSensitivity] = Field(description="Select a DLP file pattern sensitivity to match.")    
    match_percentage: int | None = Field(ge=1, le=100, default=10, description="Percentage of fingerprints in the fingerprint databases designated with the selected sensitivity to match.")    
    file_type: int | None = Field(ge=0, le=4294967295, default=0, description="Select the number of a DLP file pattern table to match.")  # datasource: ['dlp.filepattern.id']    
    sensor: list[ProfileRuleSensor] = Field(description="Select DLP sensors.")    
    label: str = Field(max_length=35, description="Select DLP label.")  # datasource: ['dlp.label.name']    
    archive: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable DLP archiving.")    
    action: ProfileRuleActionEnum | None = Field(default=ProfileRuleActionEnum.ALLOW, description="Action to take with content that this DLP profile matches.")    
    expiry: str | None = Field(default="5m", description="Quarantine duration in days, hours, minutes (format = dddhhmm).")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class ProfileFullArchiveProtoEnum(str, Enum):
    """Allowed values for full_archive_proto field."""
    SMTP = "smtp"
    POP3 = "pop3"
    IMAP = "imap"
    HTTP_GET = "http-get"
    HTTP_POST = "http-post"
    FTP = "ftp"
    NNTP = "nntp"
    MAPI = "mapi"
    SSH = "ssh"
    CIFS = "cifs"

class ProfileSummaryProtoEnum(str, Enum):
    """Allowed values for summary_proto field."""
    SMTP = "smtp"
    POP3 = "pop3"
    IMAP = "imap"
    HTTP_GET = "http-get"
    HTTP_POST = "http-post"
    FTP = "ftp"
    NNTP = "nntp"
    MAPI = "mapi"
    SSH = "ssh"
    CIFS = "cifs"


# ============================================================================
# Main Model
# ============================================================================

class ProfileModel(BaseModel):
    """
    Pydantic model for dlp/profile configuration.
    
    Configure DLP profiles.
    
    Validation Rules:        - name: max_length=47 pattern=        - comment: max_length=255 pattern=        - feature_set: pattern=        - replacemsg_group: max_length=35 pattern=        - rule: pattern=        - dlp_log: pattern=        - extended_log: pattern=        - nac_quar_log: pattern=        - full_archive_proto: pattern=        - summary_proto: pattern=        - fortidata_error_action: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str = Field(max_length=47, description="Name of the DLP profile.")    
    comment: str | None = Field(max_length=255, default=None, description="Comment.")    
    feature_set: Literal["flow", "proxy"] | None = Field(default="flow", description="Flow/proxy feature set.")    
    replacemsg_group: str | None = Field(max_length=35, default=None, description="Replacement message group used by this DLP profile.")  # datasource: ['system.replacemsg-group.name']    
    rule: list[ProfileRule] = Field(default_factory=list, description="Set up DLP rules for this profile.")    
    dlp_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable DLP logging.")    
    extended_log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable extended logging for data loss prevention.")    
    nac_quar_log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable NAC quarantine logging.")    
    full_archive_proto: list[ProfileFullArchiveProtoEnum] = Field(default_factory=list, description="Protocols to always content archive.")    
    summary_proto: list[ProfileSummaryProtoEnum] = Field(default_factory=list, description="Protocols to always log summary.")    
    fortidata_error_action: Literal["log-only", "block", "ignore"] | None = Field(default="block", description="Action to take if FortiData query fails.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('replacemsg_group')
    @classmethod
    def validate_replacemsg_group(cls, v: Any) -> Any:
        """
        Validate replacemsg_group field.
        
        Datasource: ['system.replacemsg-group.name']
        
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
    async def validate_replacemsg_group_references(self, client: Any) -> list[str]:
        """
        Validate replacemsg_group references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - system/replacemsg-group        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ProfileModel(
            ...     replacemsg_group="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_replacemsg_group_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.dlp.profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "replacemsg_group", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.system.replacemsg_group.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Replacemsg-Group '{value}' not found in "
                "system/replacemsg-group"
            )        
        return errors    
    async def validate_rule_references(self, client: Any) -> list[str]:
        """
        Validate rule references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - dlp/label        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ProfileModel(
            ...     rule=[{"label": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_rule_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.dlp.profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "rule", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("label")
            else:
                value = getattr(item, "label", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.dlp.label.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Rule '{value}' not found in "
                    "dlp/label"
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
        
        errors = await self.validate_replacemsg_group_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_rule_references(client)
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
    "ProfileModel",    "ProfileRule",    "ProfileRule.Sensitivity",    "ProfileRule.Sensor",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:41.367198Z
# ============================================================================