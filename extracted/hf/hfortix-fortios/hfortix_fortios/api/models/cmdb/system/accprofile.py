"""
Pydantic Models for CMDB - system/accprofile

Runtime validation models for system/accprofile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class AccprofileUtmgrpPermission(BaseModel):
    """
    Child table model for utmgrp-permission.
    
    Custom Security Profile permissions.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    antivirus: Literal["none", "read", "read-write"] | None = Field(default="none", description="Antivirus profiles and settings.")    
    ips: Literal["none", "read", "read-write"] | None = Field(default="none", description="IPS profiles and settings.")    
    webfilter: Literal["none", "read", "read-write"] | None = Field(default="none", description="Web Filter profiles and settings.")    
    emailfilter: Literal["none", "read", "read-write"] | None = Field(default="none", description="Email Filter and settings.")    
    dlp: Literal["none", "read", "read-write"] | None = Field(default="none", description="DLP profiles and settings.")    
    file_filter: Literal["none", "read", "read-write"] | None = Field(default="none", description="File-filter profiles and settings.")    
    application_control: Literal["none", "read", "read-write"] | None = Field(default="none", description="Application Control profiles and settings.")    
    icap: Literal["none", "read", "read-write"] | None = Field(default="none", description="ICAP profiles and settings.")    
    voip: Literal["none", "read", "read-write"] | None = Field(default="none", description="VoIP profiles and settings.")    
    waf: Literal["none", "read", "read-write"] | None = Field(default="none", description="Web Application Firewall profiles and settings.")    
    dnsfilter: Literal["none", "read", "read-write"] | None = Field(default="none", description="DNS Filter profiles and settings.")    
    endpoint_control: Literal["none", "read", "read-write"] | None = Field(default="none", description="FortiClient Profiles.")    
    videofilter: Literal["none", "read", "read-write"] | None = Field(default="none", description="Video filter profiles and settings.")    
    virtual_patch: Literal["none", "read", "read-write"] | None = Field(default="none", description="Virtual patch profiles and settings.")    
    casb: Literal["none", "read", "read-write"] | None = Field(default="none", description="Inline CASB filter profile and settings")    
    telemetry: Literal["none", "read", "read-write"] | None = Field(default="none", description="Telemetry profile and settings.")
class AccprofileSysgrpPermission(BaseModel):
    """
    Child table model for sysgrp-permission.
    
    Custom system permission.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    admin: Literal["none", "read", "read-write"] | None = Field(default="none", description="Administrator Users.")    
    upd: Literal["none", "read", "read-write"] | None = Field(default="none", description="FortiGuard Updates.")    
    cfg: Literal["none", "read", "read-write"] | None = Field(default="none", description="System Configuration.")    
    mnt: Literal["none", "read", "read-write"] | None = Field(default="none", description="Maintenance.")
class AccprofileSecfabgrpPermission(BaseModel):
    """
    Child table model for secfabgrp-permission.
    
    Custom Security Fabric permissions.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    csfsys: Literal["none", "read", "read-write"] | None = Field(default="none", description="Security Fabric system profiles and settings.")    
    csffoo: Literal["none", "read", "read-write"] | None = Field(default="none", description="Fabric Overlay Orchestrator profiles and settings.")
class AccprofileNetgrpPermission(BaseModel):
    """
    Child table model for netgrp-permission.
    
    Custom network permission.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    cfg: Literal["none", "read", "read-write"] | None = Field(default="none", description="Network Configuration.")    
    packet_capture: Literal["none", "read", "read-write"] | None = Field(default="none", description="Packet Capture Configuration.")    
    route_cfg: Literal["none", "read", "read-write"] | None = Field(default="none", description="Router Configuration.")
class AccprofileLoggrpPermission(BaseModel):
    """
    Child table model for loggrp-permission.
    
    Custom Log & Report permission.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    config: Literal["none", "read", "read-write"] | None = Field(default="none", description="Log & Report configuration.")    
    data_access: Literal["none", "read", "read-write"] | None = Field(default="none", description="Log & Report Data Access.")    
    report_access: Literal["none", "read", "read-write"] | None = Field(default="none", description="Log & Report Report Access.")    
    threat_weight: Literal["none", "read", "read-write"] | None = Field(default="none", description="Log & Report Threat Weight.")
class AccprofileFwgrpPermission(BaseModel):
    """
    Child table model for fwgrp-permission.
    
    Custom firewall permission.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    policy: Literal["none", "read", "read-write"] | None = Field(default="none", description="Policy Configuration.")    
    address: Literal["none", "read", "read-write"] | None = Field(default="none", description="Address Configuration.")    
    service: Literal["none", "read", "read-write"] | None = Field(default="none", description="Service Configuration.")    
    schedule: Literal["none", "read", "read-write"] | None = Field(default="none", description="Schedule Configuration.")    
    others: Literal["none", "read", "read-write"] | None = Field(default="none", description="Other Firewall Configuration.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class AccprofileSecfabgrpEnum(str, Enum):
    """Allowed values for secfabgrp field."""
    NONE = "none"
    READ = "read"
    READ_WRITE = "read-write"
    CUSTOM = "custom"

class AccprofileSysgrpEnum(str, Enum):
    """Allowed values for sysgrp field."""
    NONE = "none"
    READ = "read"
    READ_WRITE = "read-write"
    CUSTOM = "custom"

class AccprofileNetgrpEnum(str, Enum):
    """Allowed values for netgrp field."""
    NONE = "none"
    READ = "read"
    READ_WRITE = "read-write"
    CUSTOM = "custom"

class AccprofileLoggrpEnum(str, Enum):
    """Allowed values for loggrp field."""
    NONE = "none"
    READ = "read"
    READ_WRITE = "read-write"
    CUSTOM = "custom"

class AccprofileFwgrpEnum(str, Enum):
    """Allowed values for fwgrp field."""
    NONE = "none"
    READ = "read"
    READ_WRITE = "read-write"
    CUSTOM = "custom"

class AccprofileUtmgrpEnum(str, Enum):
    """Allowed values for utmgrp field."""
    NONE = "none"
    READ = "read"
    READ_WRITE = "read-write"
    CUSTOM = "custom"


# ============================================================================
# Main Model
# ============================================================================

class AccprofileModel(BaseModel):
    """
    Pydantic model for system/accprofile configuration.
    
    Configure access profiles for system administrators.
    
    Validation Rules:        - name: max_length=35 pattern=        - scope: pattern=        - comments: max_length=255 pattern=        - secfabgrp: pattern=        - ftviewgrp: pattern=        - authgrp: pattern=        - sysgrp: pattern=        - netgrp: pattern=        - loggrp: pattern=        - fwgrp: pattern=        - vpngrp: pattern=        - utmgrp: pattern=        - wanoptgrp: pattern=        - wifi: pattern=        - netgrp_permission: pattern=        - sysgrp_permission: pattern=        - fwgrp_permission: pattern=        - loggrp_permission: pattern=        - utmgrp_permission: pattern=        - secfabgrp_permission: pattern=        - admintimeout_override: pattern=        - admintimeout: min=1 max=480 pattern=        - cli_diagnose: pattern=        - cli_get: pattern=        - cli_show: pattern=        - cli_exec: pattern=        - cli_config: pattern=        - system_execute_ssh: pattern=        - system_execute_telnet: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str = Field(max_length=35, description="Profile name.")    
    scope: Literal["vdom", "global"] | None = Field(default="vdom", description="Scope of admin access: global or specific VDOM(s).")    
    comments: str | None = Field(max_length=255, default=None, description="Comment.")    
    secfabgrp: AccprofileSecfabgrpEnum | None = Field(default=AccprofileSecfabgrpEnum.NONE, description="Security Fabric.")    
    ftviewgrp: Literal["none", "read", "read-write"] | None = Field(default="none", description="FortiView.")    
    authgrp: Literal["none", "read", "read-write"] | None = Field(default="none", description="Administrator access to Users and Devices.")    
    sysgrp: AccprofileSysgrpEnum | None = Field(default=AccprofileSysgrpEnum.NONE, description="System Configuration.")    
    netgrp: AccprofileNetgrpEnum | None = Field(default=AccprofileNetgrpEnum.NONE, description="Network Configuration.")    
    loggrp: AccprofileLoggrpEnum | None = Field(default=AccprofileLoggrpEnum.NONE, description="Administrator access to Logging and Reporting including viewing log messages.")    
    fwgrp: AccprofileFwgrpEnum | None = Field(default=AccprofileFwgrpEnum.NONE, description="Administrator access to the Firewall configuration.")    
    vpngrp: Literal["none", "read", "read-write"] | None = Field(default="none", description="Administrator access to IPsec, SSL, PPTP, and L2TP VPN.")    
    utmgrp: AccprofileUtmgrpEnum | None = Field(default=AccprofileUtmgrpEnum.NONE, description="Administrator access to Security Profiles.")    
    wanoptgrp: Literal["none", "read", "read-write"] | None = Field(default="none", description="Administrator access to WAN Opt & Cache.")    
    wifi: Literal["none", "read", "read-write"] | None = Field(default="none", description="Administrator access to the WiFi controller and Switch controller.")    
    netgrp_permission: AccprofileNetgrpPermission | None = Field(default=None, description="Custom network permission.")    
    sysgrp_permission: AccprofileSysgrpPermission | None = Field(default=None, description="Custom system permission.")    
    fwgrp_permission: AccprofileFwgrpPermission | None = Field(default=None, description="Custom firewall permission.")    
    loggrp_permission: AccprofileLoggrpPermission | None = Field(default=None, description="Custom Log & Report permission.")    
    utmgrp_permission: AccprofileUtmgrpPermission | None = Field(default=None, description="Custom Security Profile permissions.")    
    secfabgrp_permission: AccprofileSecfabgrpPermission | None = Field(default=None, description="Custom Security Fabric permissions.")    
    admintimeout_override: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable overriding the global administrator idle timeout.")    
    admintimeout: int | None = Field(ge=1, le=480, default=10, description="Administrator timeout for this access profile (0 - 480 min, default = 10, 0 means never timeout).")    
    cli_diagnose: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable permission to run diagnostic commands.")    
    cli_get: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable permission to run get commands.")    
    cli_show: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable permission to run show commands.")    
    cli_exec: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable permission to run execute commands.")    
    cli_config: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable permission to run config commands.")    
    system_execute_ssh: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable permission to execute SSH commands.")    
    system_execute_telnet: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable permission to execute TELNET commands.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "AccprofileModel":
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
    "AccprofileModel",    "AccprofileNetgrpPermission",    "AccprofileSysgrpPermission",    "AccprofileFwgrpPermission",    "AccprofileLoggrpPermission",    "AccprofileUtmgrpPermission",    "AccprofileSecfabgrpPermission",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:57.557235Z
# ============================================================================