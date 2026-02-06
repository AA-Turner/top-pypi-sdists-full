"""
Pydantic Models for CMDB - webfilter/profile

Runtime validation models for webfilter/profile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class ProfileWebAllowlistEnum(str, Enum):
    """Allowed values for allowlist field in web."""
    EXEMPT_AV = "exempt-av"
    EXEMPT_WEBCONTENT = "exempt-webcontent"
    EXEMPT_ACTIVEX_JAVA_COOKIE = "exempt-activex-java-cookie"
    EXEMPT_DLP = "exempt-dlp"
    EXEMPT_RANGEBLOCK = "exempt-rangeblock"
    EXTENDED_LOG_OTHERS = "extended-log-others"

class ProfileOverrideOvrdScopeEnum(str, Enum):
    """Allowed values for ovrd_scope field in override."""
    USER = "user"
    USER_GROUP = "user-group"
    IP = "ip"
    BROWSER = "browser"
    ASK = "ask"

class ProfileOverrideProfileAttributeEnum(str, Enum):
    """Allowed values for profile_attribute field in override."""
    USER_NAME = "User-Name"
    NAS_IP_ADDRESS = "NAS-IP-Address"
    FRAMED_IP_ADDRESS = "Framed-IP-Address"
    FRAMED_IP_NETMASK = "Framed-IP-Netmask"
    FILTER_ID = "Filter-Id"
    LOGIN_IP_HOST = "Login-IP-Host"
    REPLY_MESSAGE = "Reply-Message"
    CALLBACK_NUMBER = "Callback-Number"
    CALLBACK_ID = "Callback-Id"
    FRAMED_ROUTE = "Framed-Route"
    FRAMED_IPX_NETWORK = "Framed-IPX-Network"
    CLASS = "Class"
    CALLED_STATION_ID = "Called-Station-Id"
    CALLING_STATION_ID = "Calling-Station-Id"
    NAS_IDENTIFIER = "NAS-Identifier"
    PROXY_STATE = "Proxy-State"
    LOGIN_LAT_SERVICE = "Login-LAT-Service"
    LOGIN_LAT_NODE = "Login-LAT-Node"
    LOGIN_LAT_GROUP = "Login-LAT-Group"
    FRAMED_APPLETALK_ZONE = "Framed-AppleTalk-Zone"
    ACCT_SESSION_ID = "Acct-Session-Id"
    ACCT_MULTI_SESSION_ID = "Acct-Multi-Session-Id"

class ProfileFtgdWfQuotaUnitEnum(str, Enum):
    """Allowed values for unit field in ftgd-wf.quota."""
    B = "B"
    KB = "KB"
    MB = "MB"
    GB = "GB"

class ProfileFtgdWfFiltersActionEnum(str, Enum):
    """Allowed values for action field in ftgd-wf.filters."""
    BLOCK = "block"
    AUTHENTICATE = "authenticate"
    MONITOR = "monitor"
    WARNING = "warning"

class ProfileFtgdWfOptionsEnum(str, Enum):
    """Allowed values for options field in ftgd-wf."""
    ERROR_ALLOW = "error-allow"
    RATE_SERVER_IP = "rate-server-ip"
    CONNECT_REQUEST_BYPASS = "connect-request-bypass"
    FTGD_DISABLE = "ftgd-disable"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ProfileWispServers(BaseModel):
    """
    Child table model for wisp-servers.
    
    WISP servers.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="Server name.")  # datasource: ['web-proxy.wisp.name']
class ProfileWebKeywordMatch(BaseModel):
    """
    Child table model for web.keyword-match.
    
    Search keywords to log when match is found.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    pattern: str | None = Field(max_length=79, default=None, description="Pattern/keyword to search for.")
class ProfileWeb(BaseModel):
    """
    Child table model for web.
    
    Web content filtering settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    bword_threshold: int | None = Field(ge=0, le=2147483647, default=10, description="Banned word score threshold.")    
    bword_table: int | None = Field(ge=0, le=4294967295, default=0, description="Banned word table ID.")  # datasource: ['webfilter.content.id']    
    urlfilter_table: int | None = Field(ge=0, le=4294967295, default=0, description="URL filter table ID.")  # datasource: ['webfilter.urlfilter.id']    
    content_header_list: int | None = Field(ge=0, le=4294967295, default=0, description="Content header list.")  # datasource: ['webfilter.content-header.id']    
    blocklist: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatic addition of URLs detected by FortiSandbox to blocklist.")    
    allowlist: list[ProfileWebAllowlistEnum] = Field(default_factory=list, description="FortiGuard allowlist settings.")    
    safe_search: list[Literal["url", "header"]] = Field(default_factory=list, description="Safe search type.")    
    youtube_restrict: Literal["none", "strict", "moderate"] | None = Field(default="none", description="YouTube EDU filter level.")    
    vimeo_restrict: str | None = Field(max_length=63, default=None, description="Set Vimeo-restrict (\"7\" = don't show mature content, \"134\" = don't show unrated and mature content). A value of cookie \"content_rating\".")    
    log_search: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging all search phrases.")    
    keyword_match: list[ProfileWebKeywordMatch] = Field(default_factory=list, description="Search keywords to log when match is found.")
class ProfileOverrideProfile(BaseModel):
    """
    Child table model for override.profile.
    
    Web filter profile with permission to create overrides.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Web profile.")  # datasource: ['webfilter.profile.name']
class ProfileOverrideOvrdUserGroup(BaseModel):
    """
    Child table model for override.ovrd-user-group.
    
    User groups with permission to use the override.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="User group name.")  # datasource: ['user.group.name']
class ProfileOverride(BaseModel):
    """
    Child table model for override.
    
    Web Filter override settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    ovrd_cookie: Literal["allow", "deny"] | None = Field(default="deny", description="Allow/deny browser-based (cookie) overrides.")    
    ovrd_scope: ProfileOverrideOvrdScopeEnum | None = Field(default=ProfileOverrideOvrdScopeEnum.USER, description="Override scope.")    
    profile_type: Literal["list", "radius"] | None = Field(default="list", description="Override profile type.")    
    ovrd_dur_mode: Literal["constant", "ask"] | None = Field(default="constant", description="Override duration mode.")    
    ovrd_dur: str | None = Field(default="15m", description="Override duration.")    
    profile_attribute: ProfileOverrideProfileAttributeEnum | None = Field(default=ProfileOverrideProfileAttributeEnum.LOGIN_LAT_SERVICE, description="Profile attribute to retrieve from the RADIUS server.")    
    ovrd_user_group: list[ProfileOverrideOvrdUserGroup] = Field(default_factory=list, description="User groups with permission to use the override.")    
    profile: list[ProfileOverrideProfile] = Field(default_factory=list, description="Web filter profile with permission to create overrides.")
class ProfileFtgdWfRisk(BaseModel):
    """
    Child table model for ftgd-wf.risk.
    
    FortiGuard risk level settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=255, default=0, serialization_alias="id", description="ID number.")    
    risk_level: str = Field(max_length=35, description="Risk level to be examined.")  # datasource: ['webfilter.ftgd-risk-level.name']    
    action: Literal["block", "monitor"] | None = Field(default="monitor", description="Action to take for matches.")    
    log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging.")
class ProfileFtgdWfQuota(BaseModel):
    """
    Child table model for ftgd-wf.quota.
    
    FortiGuard traffic quota settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID number.")    
    category: list[str] = Field(default_factory=list, description="FortiGuard categories to apply quota to (category action must be set to monitor).")    
    type_: Literal["time", "traffic"] | None = Field(default="time", serialization_alias="type", description="Quota type.")    
    unit: ProfileFtgdWfQuotaUnitEnum | None = Field(default=ProfileFtgdWfQuotaUnitEnum.MB, description="Traffic quota unit of measurement.")    
    value: int | None = Field(ge=1, le=4294967295, default=1024, description="Traffic quota value.")    
    duration: str | None = Field(default="5m", description="Duration of quota.")    
    override_replacemsg: str | None = Field(max_length=28, default=None, description="Override replacement message.")
class ProfileFtgdWfFiltersAuthUsrGrp(BaseModel):
    """
    Child table model for ftgd-wf.filters.auth-usr-grp.
    
    Groups with permission to authenticate.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="User group name.")  # datasource: ['user.group.name']
class ProfileFtgdWfFilters(BaseModel):
    """
    Child table model for ftgd-wf.filters.
    
    FortiGuard filters.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=255, default=0, serialization_alias="id", description="ID number.")    
    category: int | None = Field(ge=0, le=255, default=0, description="Categories and groups the filter examines.")    
    action: ProfileFtgdWfFiltersActionEnum | None = Field(default=ProfileFtgdWfFiltersActionEnum.MONITOR, description="Action to take for matches.")    
    warn_duration: str | None = Field(default="5m", description="Duration of warnings.")    
    auth_usr_grp: list[ProfileFtgdWfFiltersAuthUsrGrp] = Field(default_factory=list, description="Groups with permission to authenticate.")    
    log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging.")    
    override_replacemsg: str | None = Field(max_length=28, default=None, description="Override replacement message.")    
    warning_prompt: Literal["per-domain", "per-category"] | None = Field(default="per-category", description="Warning prompts in each category or each domain.")    
    warning_duration_type: Literal["session", "timeout"] | None = Field(default="timeout", description="Re-display warning after closing browser or after a timeout.")
class ProfileFtgdWf(BaseModel):
    """
    Child table model for ftgd-wf.
    
    FortiGuard Web Filter settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    options: list[ProfileFtgdWfOptionsEnum] = Field(default_factory=list, description="Options for FortiGuard Web Filter.")    
    exempt_quota: list[str] = Field(default_factory=list, description="Do not stop quota for these categories.")    
    ovrd: list[str] = Field(default_factory=list, description="Allow web filter profile overrides.")    
    filters: list[ProfileFtgdWfFilters] = Field(default_factory=list, description="FortiGuard filters.")    
    risk: list[ProfileFtgdWfRisk] = Field(default_factory=list, description="FortiGuard risk level settings.")    
    quota: list[ProfileFtgdWfQuota] = Field(default_factory=list, description="FortiGuard traffic quota settings.")    
    max_quota_timeout: int | None = Field(ge=1, le=86400, default=300, description="Maximum FortiGuard quota used by single page view in seconds (excludes streams).")    
    rate_javascript_urls: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable rating JavaScript by URL.")    
    rate_css_urls: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable rating CSS by URL.")    
    rate_crl_urls: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable rating CRL by URL.")
class ProfileAntiphishInspectionEntries(BaseModel):
    """
    Child table model for antiphish.inspection-entries.
    
    AntiPhishing entries.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=63, description="Inspection target name.")    
    fortiguard_category: list[str] = Field(description="FortiGuard category to match.")    
    action: Literal["exempt", "log", "block"] = Field(default="exempt", description="Action to be taken upon an AntiPhishing match.")
class ProfileAntiphishCustomPatterns(BaseModel):
    """
    Child table model for antiphish.custom-patterns.
    
    Custom username and password regex patterns.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    pattern: str = Field(max_length=255, description="Target pattern.")    
    category: Literal["username", "password"] = Field(default="username", description="Category that the pattern matches.")    
    type_: Literal["regex", "literal"] = Field(default="regex", serialization_alias="type", description="Pattern will be treated either as a regex pattern or literal string.")
class ProfileAntiphish(BaseModel):
    """
    Child table model for antiphish.
    
    AntiPhishing profile.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Toggle AntiPhishing functionality.")    
    default_action: Literal["exempt", "log", "block"] | None = Field(default="exempt", description="Action to be taken when there is no matching rule.")    
    check_uri: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable checking of GET URI parameters for known credentials.")    
    check_basic_auth: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable checking of HTTP Basic Auth field for known credentials.")    
    check_username_only: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable username only matching of credentials. Action will be taken for valid usernames regardless of password validity.")    
    max_body_len: int | None = Field(ge=0, le=4294967295, default=1024, description="Maximum size of a POST body to check for credentials.")    
    inspection_entries: list[ProfileAntiphishInspectionEntries] = Field(default_factory=list, description="AntiPhishing entries.")    
    custom_patterns: list[ProfileAntiphishCustomPatterns] = Field(default_factory=list, description="Custom username and password regex patterns.")    
    authentication: Literal["domain-controller", "ldap"] = Field(default="domain-controller", description="Authentication methods.")    
    domain_controller: str | None = Field(max_length=63, default=None, description="Domain for which to verify received credentials against.")  # datasource: ['user.domain-controller.name', 'credential-store.domain-controller.server-name']    
    ldap: str | None = Field(max_length=63, default=None, description="LDAP server for which to verify received credentials against.")  # datasource: ['user.ldap.name']
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class ProfileOptionsEnum(str, Enum):
    """Allowed values for options field."""
    ACTIVEXFILTER = "activexfilter"
    COOKIEFILTER = "cookiefilter"
    JAVAFILTER = "javafilter"
    BLOCK_INVALID_URL = "block-invalid-url"
    JSCRIPT = "jscript"
    JS = "js"
    VBS = "vbs"
    UNKNOWN = "unknown"
    INTRINSIC = "intrinsic"
    WF_REFERER = "wf-referer"
    WF_COOKIE = "wf-cookie"
    PER_USER_BAL = "per-user-bal"

class ProfileOvrdPermEnum(str, Enum):
    """Allowed values for ovrd_perm field."""
    BANNEDWORD_OVERRIDE = "bannedword-override"
    URLFILTER_OVERRIDE = "urlfilter-override"
    FORTIGUARD_WF_OVERRIDE = "fortiguard-wf-override"
    CONTENTTYPE_CHECK_OVERRIDE = "contenttype-check-override"


# ============================================================================
# Main Model
# ============================================================================

class ProfileModel(BaseModel):
    """
    Pydantic model for webfilter/profile configuration.
    
    Configure Web filter profiles.
    
    Validation Rules:        - name: max_length=47 pattern=        - comment: max_length=255 pattern=        - feature_set: pattern=        - replacemsg_group: max_length=35 pattern=        - options: pattern=        - https_replacemsg: pattern=        - web_flow_log_encoding: pattern=        - ovrd_perm: pattern=        - post_action: pattern=        - override: pattern=        - web: pattern=        - ftgd_wf: pattern=        - antiphish: pattern=        - wisp: pattern=        - wisp_servers: pattern=        - wisp_algorithm: pattern=        - log_all_url: pattern=        - web_content_log: pattern=        - web_filter_activex_log: pattern=        - web_filter_command_block_log: pattern=        - web_filter_cookie_log: pattern=        - web_filter_applet_log: pattern=        - web_filter_jscript_log: pattern=        - web_filter_js_log: pattern=        - web_filter_vbs_log: pattern=        - web_filter_unknown_log: pattern=        - web_filter_referer_log: pattern=        - web_filter_cookie_removal_log: pattern=        - web_url_log: pattern=        - web_invalid_domain_log: pattern=        - web_ftgd_err_log: pattern=        - web_ftgd_quota_usage: pattern=        - extended_log: pattern=        - web_extended_all_action_log: pattern=        - web_antiphishing_log: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str = Field(max_length=47, description="Profile name.")    
    comment: str | None = Field(max_length=255, default=None, description="Optional comments.")    
    feature_set: Literal["flow", "proxy"] | None = Field(default="flow", description="Flow/proxy feature set.")    
    replacemsg_group: str | None = Field(max_length=35, default=None, description="Replacement message group.")  # datasource: ['system.replacemsg-group.name']    
    options: list[ProfileOptionsEnum] = Field(default_factory=list, description="Options.")    
    https_replacemsg: Literal["enable", "disable"] | None = Field(default="enable", description="Enable replacement messages for HTTPS.")    
    web_flow_log_encoding: Literal["utf-8", "punycode"] | None = Field(default="utf-8", description="Log encoding in flow mode.")    
    ovrd_perm: list[ProfileOvrdPermEnum] = Field(default_factory=list, description="Permitted override types.")    
    post_action: Literal["normal", "block"] | None = Field(default="normal", description="Action taken for HTTP POST traffic.")    
    override: ProfileOverride | None = Field(default=None, description="Web Filter override settings.")    
    web: ProfileWeb | None = Field(default=None, description="Web content filtering settings.")    
    ftgd_wf: ProfileFtgdWf | None = Field(default=None, description="FortiGuard Web Filter settings.")    
    antiphish: ProfileAntiphish | None = Field(default=None, description="AntiPhishing profile.")    
    wisp: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable web proxy WISP.")    
    wisp_servers: list[ProfileWispServers] = Field(default_factory=list, description="WISP servers.")    
    wisp_algorithm: Literal["primary-secondary", "round-robin", "auto-learning"] | None = Field(default="auto-learning", description="WISP server selection algorithm.")    
    log_all_url: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging all URLs visited.")    
    web_content_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging logging blocked web content.")    
    web_filter_activex_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging ActiveX.")    
    web_filter_command_block_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging blocked commands.")    
    web_filter_cookie_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging cookie filtering.")    
    web_filter_applet_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging Java applets.")    
    web_filter_jscript_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging JScripts.")    
    web_filter_js_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging Java scripts.")    
    web_filter_vbs_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging VBS scripts.")    
    web_filter_unknown_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging unknown scripts.")    
    web_filter_referer_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging referrers.")    
    web_filter_cookie_removal_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging blocked cookies.")    
    web_url_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging URL filtering.")    
    web_invalid_domain_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging invalid domain names.")    
    web_ftgd_err_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging rating errors.")    
    web_ftgd_quota_usage: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging daily quota usage.")    
    extended_log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable extended logging for web filtering.")    
    web_extended_all_action_log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable extended any filter action logging for web filtering.")    
    web_antiphishing_log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging of AntiPhishing checks.")    
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
            ...     result = await fgt.api.cmdb.webfilter.profile.post(policy.to_fortios_dict())
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
    async def validate_web_references(self, client: Any) -> list[str]:
        """
        Validate web references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - webfilter/content-header        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ProfileModel(
            ...     web=[{"content-header-list": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_web_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.webfilter.profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "web", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("content-header-list")
            else:
                value = getattr(item, "content-header-list", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.webfilter.content_header.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Web '{value}' not found in "
                    "webfilter/content-header"
                )        
        return errors    
    async def validate_antiphish_references(self, client: Any) -> list[str]:
        """
        Validate antiphish references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - user/ldap        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ProfileModel(
            ...     antiphish=[{"ldap": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_antiphish_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.webfilter.profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "antiphish", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("ldap")
            else:
                value = getattr(item, "ldap", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.user.ldap.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Antiphish '{value}' not found in "
                    "user/ldap"
                )        
        return errors    
    async def validate_wisp_servers_references(self, client: Any) -> list[str]:
        """
        Validate wisp_servers references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - web-proxy/wisp        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ProfileModel(
            ...     wisp_servers=[{"name": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_wisp_servers_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.webfilter.profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "wisp_servers", [])
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
            if await client.api.cmdb.web_proxy.wisp.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Wisp-Servers '{value}' not found in "
                    "web-proxy/wisp"
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
        errors = await self.validate_web_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_antiphish_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_wisp_servers_references(client)
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
    "ProfileModel",    "ProfileOverride",    "ProfileOverride.OvrdUserGroup",    "ProfileOverride.Profile",    "ProfileWeb",    "ProfileWeb.KeywordMatch",    "ProfileFtgdWf",    "ProfileFtgdWf.Filters",    "ProfileFtgdWf.Filters.AuthUsrGrp",    "ProfileFtgdWf.Risk",    "ProfileFtgdWf.Quota",    "ProfileAntiphish",    "ProfileAntiphish.InspectionEntries",    "ProfileAntiphish.CustomPatterns",    "ProfileWispServers",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:27.338424Z
# ============================================================================