"""
Pydantic Models for CMDB - log/threat_weight

Runtime validation models for log/threat_weight configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class ThreatWeightWebLevelEnum(str, Enum):
    """Allowed values for level field in web."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareVirusInfectedEnum(str, Enum):
    """Allowed values for virus_infected field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareInlineBlockEnum(str, Enum):
    """Allowed values for inline_block field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareFileBlockedEnum(str, Enum):
    """Allowed values for file_blocked field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareCommandBlockedEnum(str, Enum):
    """Allowed values for command_blocked field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareOversizedEnum(str, Enum):
    """Allowed values for oversized field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareVirusScanErrorEnum(str, Enum):
    """Allowed values for virus_scan_error field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareSwitchProtoEnum(str, Enum):
    """Allowed values for switch_proto field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareMimefragmentedEnum(str, Enum):
    """Allowed values for mimefragmented field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareVirusFileTypeExecutableEnum(str, Enum):
    """Allowed values for virus_file_type_executable field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareVirusOutbreakPreventionEnum(str, Enum):
    """Allowed values for virus_outbreak_prevention field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareContentDisarmEnum(str, Enum):
    """Allowed values for content_disarm field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareMalwareListEnum(str, Enum):
    """Allowed values for malware_list field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareEmsThreatFeedEnum(str, Enum):
    """Allowed values for ems_threat_feed field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareFsaMaliciousEnum(str, Enum):
    """Allowed values for fsa_malicious field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareFsaHighRiskEnum(str, Enum):
    """Allowed values for fsa_high_risk field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightMalwareFsaMediumRiskEnum(str, Enum):
    """Allowed values for fsa_medium_risk field in malware."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightIpsInfoSeverityEnum(str, Enum):
    """Allowed values for info_severity field in ips."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightIpsLowSeverityEnum(str, Enum):
    """Allowed values for low_severity field in ips."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightIpsMediumSeverityEnum(str, Enum):
    """Allowed values for medium_severity field in ips."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightIpsHighSeverityEnum(str, Enum):
    """Allowed values for high_severity field in ips."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightIpsCriticalSeverityEnum(str, Enum):
    """Allowed values for critical_severity field in ips."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightGeolocationLevelEnum(str, Enum):
    """Allowed values for level field in geolocation."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightApplicationLevelEnum(str, Enum):
    """Allowed values for level field in application."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ThreatWeightWeb(BaseModel):
    """
    Child table model for web.
    
    Web filtering threat weight settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=255, default=0, serialization_alias="id", description="Entry ID.")    
    category: int = Field(ge=0, le=255, default=0, description="Threat weight score for web category filtering matches.")    
    level: ThreatWeightWebLevelEnum | None = Field(default=ThreatWeightWebLevelEnum.LOW, description="Threat weight score for web category filtering matches.")
class ThreatWeightMalware(BaseModel):
    """
    Child table model for malware.
    
    Anti-virus malware threat weight settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    virus_infected: ThreatWeightMalwareVirusInfectedEnum | None = Field(default=ThreatWeightMalwareVirusInfectedEnum.CRITICAL, description="Threat weight score for virus (infected) detected.")    
    inline_block: ThreatWeightMalwareInlineBlockEnum | None = Field(default=ThreatWeightMalwareInlineBlockEnum.CRITICAL, description="Threat weight score for malware detected by inline block.")    
    file_blocked: ThreatWeightMalwareFileBlockedEnum | None = Field(default=ThreatWeightMalwareFileBlockedEnum.LOW, description="Threat weight score for blocked file detected.")    
    command_blocked: ThreatWeightMalwareCommandBlockedEnum | None = Field(default=ThreatWeightMalwareCommandBlockedEnum.DISABLE, description="Threat weight score for blocked command detected.")    
    oversized: ThreatWeightMalwareOversizedEnum | None = Field(default=ThreatWeightMalwareOversizedEnum.DISABLE, description="Threat weight score for oversized file detected.")    
    virus_scan_error: ThreatWeightMalwareVirusScanErrorEnum | None = Field(default=ThreatWeightMalwareVirusScanErrorEnum.HIGH, description="Threat weight score for virus (scan error) detected.")    
    switch_proto: ThreatWeightMalwareSwitchProtoEnum | None = Field(default=ThreatWeightMalwareSwitchProtoEnum.DISABLE, description="Threat weight score for switch proto detected.")    
    mimefragmented: ThreatWeightMalwareMimefragmentedEnum | None = Field(default=ThreatWeightMalwareMimefragmentedEnum.DISABLE, description="Threat weight score for mimefragmented detected.")    
    virus_file_type_executable: ThreatWeightMalwareVirusFileTypeExecutableEnum | None = Field(default=ThreatWeightMalwareVirusFileTypeExecutableEnum.MEDIUM, description="Threat weight score for virus (file type executable) detected.")    
    virus_outbreak_prevention: ThreatWeightMalwareVirusOutbreakPreventionEnum | None = Field(default=ThreatWeightMalwareVirusOutbreakPreventionEnum.CRITICAL, description="Threat weight score for virus (outbreak prevention) event.")    
    content_disarm: ThreatWeightMalwareContentDisarmEnum | None = Field(default=ThreatWeightMalwareContentDisarmEnum.MEDIUM, description="Threat weight score for virus (content disarm) detected.")    
    malware_list: ThreatWeightMalwareMalwareListEnum | None = Field(default=ThreatWeightMalwareMalwareListEnum.MEDIUM, description="Threat weight score for virus (malware list) detected.")    
    ems_threat_feed: ThreatWeightMalwareEmsThreatFeedEnum | None = Field(default=ThreatWeightMalwareEmsThreatFeedEnum.MEDIUM, description="Threat weight score for virus (EMS threat feed) detected.")    
    fsa_malicious: ThreatWeightMalwareFsaMaliciousEnum | None = Field(default=ThreatWeightMalwareFsaMaliciousEnum.CRITICAL, description="Threat weight score for FortiSandbox malicious malware detected.")    
    fsa_high_risk: ThreatWeightMalwareFsaHighRiskEnum | None = Field(default=ThreatWeightMalwareFsaHighRiskEnum.HIGH, description="Threat weight score for FortiSandbox high risk malware detected.")    
    fsa_medium_risk: ThreatWeightMalwareFsaMediumRiskEnum | None = Field(default=ThreatWeightMalwareFsaMediumRiskEnum.MEDIUM, description="Threat weight score for FortiSandbox medium risk malware detected.")
class ThreatWeightLevel(BaseModel):
    """
    Child table model for level.
    
    Score mapping for threat weight levels.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    low: int | None = Field(ge=1, le=100, default=5, description="Low level score value (1 - 100).")    
    medium: int | None = Field(ge=1, le=100, default=10, description="Medium level score value (1 - 100).")    
    high: int | None = Field(ge=1, le=100, default=30, description="High level score value (1 - 100).")    
    critical: int | None = Field(ge=1, le=100, default=50, description="Critical level score value (1 - 100).")
class ThreatWeightIps(BaseModel):
    """
    Child table model for ips.
    
    IPS threat weight settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    info_severity: ThreatWeightIpsInfoSeverityEnum | None = Field(default=ThreatWeightIpsInfoSeverityEnum.DISABLE, description="Threat weight score for IPS info severity events.")    
    low_severity: ThreatWeightIpsLowSeverityEnum | None = Field(default=ThreatWeightIpsLowSeverityEnum.LOW, description="Threat weight score for IPS low severity events.")    
    medium_severity: ThreatWeightIpsMediumSeverityEnum | None = Field(default=ThreatWeightIpsMediumSeverityEnum.MEDIUM, description="Threat weight score for IPS medium severity events.")    
    high_severity: ThreatWeightIpsHighSeverityEnum | None = Field(default=ThreatWeightIpsHighSeverityEnum.HIGH, description="Threat weight score for IPS high severity events.")    
    critical_severity: ThreatWeightIpsCriticalSeverityEnum | None = Field(default=ThreatWeightIpsCriticalSeverityEnum.CRITICAL, description="Threat weight score for IPS critical severity events.")
class ThreatWeightGeolocation(BaseModel):
    """
    Child table model for geolocation.
    
    Geolocation-based threat weight settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=255, default=0, serialization_alias="id", description="Entry ID.")    
    country: str = Field(max_length=2, description="Country code.")    
    level: ThreatWeightGeolocationLevelEnum | None = Field(default=ThreatWeightGeolocationLevelEnum.LOW, description="Threat weight score for Geolocation-based events.")
class ThreatWeightApplication(BaseModel):
    """
    Child table model for application.
    
    Application-control threat weight settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=255, default=0, serialization_alias="id", description="Entry ID.")    
    category: int = Field(ge=0, le=65535, default=0, description="Application category.")    
    level: ThreatWeightApplicationLevelEnum | None = Field(default=ThreatWeightApplicationLevelEnum.LOW, description="Threat weight score for Application events.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class ThreatWeightBlockedConnectionEnum(str, Enum):
    """Allowed values for blocked_connection field."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightFailedConnectionEnum(str, Enum):
    """Allowed values for failed_connection field."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightUrlBlockDetectedEnum(str, Enum):
    """Allowed values for url_block_detected field."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatWeightBotnetConnectionDetectedEnum(str, Enum):
    """Allowed values for botnet_connection_detected field."""
    DISABLE = "disable"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# Main Model
# ============================================================================

class ThreatWeightModel(BaseModel):
    """
    Pydantic model for log/threat_weight configuration.
    
    Configure threat weight settings.
    
    Validation Rules:        - status: pattern=        - level: pattern=        - blocked_connection: pattern=        - failed_connection: pattern=        - url_block_detected: pattern=        - botnet_connection_detected: pattern=        - malware: pattern=        - ips: pattern=        - web: pattern=        - geolocation: pattern=        - application: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable the threat weight feature.")    
    level: ThreatWeightLevel | None = Field(default=None, description="Score mapping for threat weight levels.")    
    blocked_connection: ThreatWeightBlockedConnectionEnum | None = Field(default=ThreatWeightBlockedConnectionEnum.HIGH, description="Threat weight score for blocked connections.")    
    failed_connection: ThreatWeightFailedConnectionEnum | None = Field(default=ThreatWeightFailedConnectionEnum.LOW, description="Threat weight score for failed connections.")    
    url_block_detected: ThreatWeightUrlBlockDetectedEnum | None = Field(default=ThreatWeightUrlBlockDetectedEnum.HIGH, description="Threat weight score for URL blocking.")    
    botnet_connection_detected: ThreatWeightBotnetConnectionDetectedEnum | None = Field(default=ThreatWeightBotnetConnectionDetectedEnum.CRITICAL, description="Threat weight score for detected botnet connections.")    
    malware: ThreatWeightMalware | None = Field(default=None, description="Anti-virus malware threat weight settings.")    
    ips: ThreatWeightIps | None = Field(default=None, description="IPS threat weight settings.")    
    web: list[ThreatWeightWeb] = Field(default_factory=list, description="Web filtering threat weight settings.")    
    geolocation: list[ThreatWeightGeolocation] = Field(default_factory=list, description="Geolocation-based threat weight settings.")    
    application: list[ThreatWeightApplication] = Field(default_factory=list, description="Application-control threat weight settings.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "ThreatWeightModel":
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
    "ThreatWeightModel",    "ThreatWeightLevel",    "ThreatWeightMalware",    "ThreatWeightIps",    "ThreatWeightWeb",    "ThreatWeightGeolocation",    "ThreatWeightApplication",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:57.782592Z
# ============================================================================