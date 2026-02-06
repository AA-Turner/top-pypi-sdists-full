"""
Pydantic Models for CMDB - wireless_controller/snmp

Runtime validation models for wireless_controller/snmp configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class SnmpUserAuthProtoEnum(str, Enum):
    """Allowed values for auth_proto field in user."""
    MD5 = "md5"
    SHA = "sha"
    SHA224 = "sha224"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"

class SnmpUserPrivProtoEnum(str, Enum):
    """Allowed values for priv_proto field in user."""
    AES = "aes"
    DES = "des"
    AES256 = "aes256"
    AES256CISCO = "aes256cisco"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class SnmpUser(BaseModel):
    """
    Child table model for user.
    
    SNMP User Configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=32, description="SNMP user name.")    
    status: Literal["enable", "disable"] | None = Field(default="enable", description="SNMP user enable.")    
    queries: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable SNMP queries for this user.")    
    trap_status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable traps for this SNMP user.")    
    security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"] | None = Field(default="no-auth-no-priv", description="Security level for message authentication and encryption.")    
    auth_proto: SnmpUserAuthProtoEnum | None = Field(default=SnmpUserAuthProtoEnum.SHA, description="Authentication protocol.")    
    auth_pwd: Any = Field(max_length=128, description="Password for authentication protocol.")    
    priv_proto: SnmpUserPrivProtoEnum | None = Field(default=SnmpUserPrivProtoEnum.AES, description="Privacy (encryption) protocol.")    
    priv_pwd: Any = Field(max_length=128, description="Password for privacy (encryption) protocol.")    
    notify_hosts: list[str] = Field(default_factory=list, description="Configure SNMP User Notify Hosts.")    
    notify_hosts6: list[str] = Field(default_factory=list, description="Configure IPv6 SNMP User Notify Hosts.")
class SnmpCommunityHosts6(BaseModel):
    """
    Child table model for community.hosts6.
    
    Configure IPv6 SNMP managers (hosts).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Host6 entry ID.")    
    ipv6: str = Field(default="::/0", description="IPv6 address of the SNMP manager (host).")
class SnmpCommunityHosts(BaseModel):
    """
    Child table model for community.hosts.
    
    Configure IPv4 SNMP managers (hosts).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Host entry ID.")    
    ip: str = Field(description="IPv4 address of the SNMP manager (host).")
class SnmpCommunity(BaseModel):
    """
    Child table model for community.
    
    SNMP Community Configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Community ID.")    
    name: str = Field(max_length=35, description="Community name.")    
    status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable this SNMP community.")    
    query_v1_status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable SNMP v1 queries.")    
    query_v2c_status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable SNMP v2c queries.")    
    trap_v1_status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable SNMP v1 traps.")    
    trap_v2c_status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable SNMP v2c traps.")    
    hosts: list[SnmpCommunityHosts] = Field(default_factory=list, description="Configure IPv4 SNMP managers (hosts).")    
    hosts6: list[SnmpCommunityHosts6] = Field(default_factory=list, description="Configure IPv6 SNMP managers (hosts).")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class SnmpModel(BaseModel):
    """
    Pydantic model for wireless_controller/snmp configuration.
    
    Configure SNMP.
    
    Validation Rules:        - engine_id: max_length=23 pattern=        - contact_info: max_length=31 pattern=        - trap_high_cpu_threshold: min=10 max=100 pattern=        - trap_high_mem_threshold: min=10 max=100 pattern=        - community: pattern=        - user: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    engine_id: str | None = Field(max_length=23, default=None, description="AC SNMP engineID string (maximum 24 characters).")    
    contact_info: str | None = Field(max_length=31, default=None, description="Contact Information.")    
    trap_high_cpu_threshold: int | None = Field(ge=10, le=100, default=80, description="CPU usage when trap is sent.")    
    trap_high_mem_threshold: int | None = Field(ge=10, le=100, default=80, description="Memory usage when trap is sent.")    
    community: list[SnmpCommunity] = Field(default_factory=list, description="SNMP Community Configuration.")    
    user: list[SnmpUser] = Field(default_factory=list, description="SNMP User Configuration.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "SnmpModel":
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
    "SnmpModel",    "SnmpCommunity",    "SnmpCommunity.Hosts",    "SnmpCommunity.Hosts6",    "SnmpUser",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:27.900269Z
# ============================================================================