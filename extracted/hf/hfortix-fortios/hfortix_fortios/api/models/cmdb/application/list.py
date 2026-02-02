"""
Pydantic Models for CMDB - application/list

Runtime validation models for application/list configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class ListEntriesPopularityEnum(str, Enum):
    """Allowed values for popularity field in entries."""
    V_1 = "1"
    V_2 = "2"
    V_3 = "3"
    V_4 = "4"
    V_5 = "5"

class ListEntriesRateTrackEnum(str, Enum):
    """Allowed values for rate_track field in entries."""
    NONE = "none"
    SRC_IP = "src-ip"
    DEST_IP = "dest-ip"
    DHCP_CLIENT_MAC = "dhcp-client-mac"
    DNS_DOMAIN = "dns-domain"

class ListDefaultNetworkServicesServicesEnum(str, Enum):
    """Allowed values for services field in default-network-services."""
    HTTP = "http"
    SSH = "ssh"
    TELNET = "telnet"
    FTP = "ftp"
    DNS = "dns"
    SMTP = "smtp"
    POP3 = "pop3"
    IMAP = "imap"
    SNMP = "snmp"
    NNTP = "nntp"
    HTTPS = "https"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ListEntriesRisk(BaseModel):
    """
    Child table model for entries.risk.
    
    Risk, or impact, of allowing traffic from this application to occur (1 - 5; Low, Elevated, Medium, High, and Critical).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    level: int = Field(ge=0, le=4294967295, default=0, description="Risk, or impact, of allowing traffic from this application to occur (1 - 5; Low, Elevated, Medium, High, and Critical).")
class ListEntriesParametersMembers(BaseModel):
    """
    Child table model for entries.parameters.members.
    
    Parameter tuple members.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Parameter.")    
    name: str = Field(max_length=31, description="Parameter name.")    
    value: str = Field(max_length=199, description="Parameter value.")
class ListEntriesParameters(BaseModel):
    """
    Child table model for entries.parameters.
    
    Application parameters.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Parameter tuple ID.")    
    members: list[ListEntriesParametersMembers] = Field(default_factory=list, description="Parameter tuple members.")
class ListEntriesExclusion(BaseModel):
    """
    Child table model for entries.exclusion.
    
    ID of excluded applications.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Excluded application IDs.")
class ListEntriesCategory(BaseModel):
    """
    Child table model for entries.category.
    
    Category ID list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Application category ID.")
class ListEntriesApplication(BaseModel):
    """
    Child table model for entries.application.
    
    ID of allowed applications.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Application IDs.")
class ListEntries(BaseModel):
    """
    Child table model for entries.
    
    Application list entries.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Entry ID.")    
    risk: list[ListEntriesRisk] = Field(default_factory=list, description="Risk, or impact, of allowing traffic from this application to occur (1 - 5; Low, Elevated, Medium, High, and Critical).")    
    category: list[ListEntriesCategory] = Field(default_factory=list, description="Category ID list.")    
    application: list[ListEntriesApplication] = Field(default_factory=list, description="ID of allowed applications.")    
    protocols: list[str] = Field(default_factory=list, description="Application protocol filter.")    
    vendor: list[str] = Field(default_factory=list, description="Application vendor filter.")    
    technology: list[str] = Field(default_factory=list, description="Application technology filter.")    
    behavior: list[str] = Field(default_factory=list, description="Application behavior filter.")    
    popularity: list[ListEntriesPopularityEnum] = Field(default_factory=list, description="Application popularity filter (1 - 5, from least to most popular).")    
    exclusion: list[ListEntriesExclusion] = Field(default_factory=list, description="ID of excluded applications.")    
    parameters: list[ListEntriesParameters] = Field(default_factory=list, description="Application parameters.")    
    action: Literal["pass", "block", "reset"] | None = Field(default="block", description="Pass or block traffic, or reset connection for traffic from this application.")    
    log: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable logging for this application list.")    
    log_packet: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable packet logging.")    
    rate_count: int | None = Field(ge=0, le=65535, default=0, description="Count of the rate.")    
    rate_duration: int | None = Field(ge=1, le=65535, default=60, description="Duration (sec) of the rate.")    
    rate_mode: Literal["periodical", "continuous"] | None = Field(default="continuous", description="Rate limit mode.")    
    rate_track: ListEntriesRateTrackEnum | None = Field(default=ListEntriesRateTrackEnum.NONE, description="Track the packet protocol field.")    
    session_ttl: int | None = Field(ge=0, le=4294967295, default=0, description="Session TTL (0 = default).")    
    shaper: str | None = Field(max_length=35, default=None, description="Traffic shaper.")  # datasource: ['firewall.shaper.traffic-shaper.name']    
    shaper_reverse: str | None = Field(max_length=35, default=None, description="Reverse traffic shaper.")  # datasource: ['firewall.shaper.traffic-shaper.name']    
    per_ip_shaper: str | None = Field(max_length=35, default=None, description="Per-IP traffic shaper.")  # datasource: ['firewall.shaper.per-ip-shaper.name']    
    quarantine: Literal["none", "attacker"] | None = Field(default="none", description="Quarantine method.")    
    quarantine_expiry: str | None = Field(default="5m", description="Duration of quarantine. (Format ###d##h##m, minimum 1m, maximum 364d23h59m, default = 5m). Requires quarantine set to attacker.")    
    quarantine_log: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable quarantine logging.")
class ListDefaultNetworkServices(BaseModel):
    """
    Child table model for default-network-services.
    
    Default network service entries.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Entry ID.")    
    port: int = Field(ge=0, le=65535, default=0, description="Port number.")    
    services: list[ListDefaultNetworkServicesServicesEnum] = Field(default_factory=list, description="Network protocols.")    
    violation_action: Literal["pass", "monitor", "block"] | None = Field(default="block", description="Action for protocols not in the allowlist for selected port.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class ListOptionsEnum(str, Enum):
    """Allowed values for options field."""
    ALLOW_DNS = "allow-dns"
    ALLOW_ICMP = "allow-icmp"
    ALLOW_HTTP = "allow-http"
    ALLOW_SSL = "allow-ssl"


# ============================================================================
# Main Model
# ============================================================================

class ListModel(BaseModel):
    """
    Pydantic model for application/list configuration.
    
    Configure application control lists.
    
    Validation Rules:        - name: max_length=47 pattern=        - comment: max_length=255 pattern=        - replacemsg_group: max_length=35 pattern=        - extended_log: pattern=        - other_application_action: pattern=        - app_replacemsg: pattern=        - other_application_log: pattern=        - enforce_default_app_port: pattern=        - force_inclusion_ssl_di_sigs: pattern=        - unknown_application_action: pattern=        - unknown_application_log: pattern=        - p2p_block_list: pattern=        - deep_app_inspection: pattern=        - options: pattern=        - entries: pattern=        - control_default_network_services: pattern=        - default_network_services: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str = Field(max_length=47, description="List name.")    
    comment: str | None = Field(max_length=255, default=None, description="Comments.")    
    replacemsg_group: str | None = Field(max_length=35, default=None, description="Replacement message group.")  # datasource: ['system.replacemsg-group.name']    
    extended_log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable extended logging.")    
    other_application_action: Literal["pass", "block"] | None = Field(default="pass", description="Action for other applications.")    
    app_replacemsg: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable replacement messages for blocked applications.")    
    other_application_log: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable logging for other applications.")    
    enforce_default_app_port: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable default application port enforcement for allowed applications.")    
    force_inclusion_ssl_di_sigs: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable forced inclusion of SSL deep inspection signatures.")    
    unknown_application_action: Literal["pass", "block"] | None = Field(default="pass", description="Pass or block traffic from unknown applications.")    
    unknown_application_log: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable logging for unknown applications.")    
    p2p_block_list: list[Literal["skype", "edonkey", "bittorrent"]] = Field(default_factory=list, description="P2P applications to be block listed.")    
    deep_app_inspection: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable deep application inspection.")    
    options: list[ListOptionsEnum] = Field(default_factory=list, description="Basic application protocol signatures allowed by default.")    
    entries: list[ListEntries] = Field(default_factory=list, description="Application list entries.")    
    control_default_network_services: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable enforcement of protocols over selected ports.")    
    default_network_services: list[ListDefaultNetworkServices] = Field(default_factory=list, description="Default network service entries.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "ListModel":
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
            >>> policy = ListModel(
            ...     replacemsg_group="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_replacemsg_group_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.application.list.post(policy.to_fortios_dict())
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
    async def validate_entries_references(self, client: Any) -> list[str]:
        """
        Validate entries references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/shaper/per-ip-shaper        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ListModel(
            ...     entries=[{"per-ip-shaper": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_entries_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.application.list.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "entries", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("per-ip-shaper")
            else:
                value = getattr(item, "per-ip-shaper", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.firewall.shaper.per_ip_shaper.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Entries '{value}' not found in "
                    "firewall/shaper/per-ip-shaper"
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
        errors = await self.validate_entries_references(client)
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
    "ListModel",    "ListEntries",    "ListEntries.Risk",    "ListEntries.Category",    "ListEntries.Application",    "ListEntries.Exclusion",    "ListEntries.Parameters",    "ListEntries.Parameters.Members",    "ListDefaultNetworkServices",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:57.765860Z
# ============================================================================