"""
Pydantic Models for CMDB - waf/profile

Runtime validation models for waf/profile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class ProfileSignatureCustomSignatureTargetEnum(str, Enum):
    """Allowed values for target field in signature.custom-signature."""
    ARG = "arg"
    ARG_NAME = "arg-name"
    REQ_BODY = "req-body"
    REQ_COOKIE = "req-cookie"
    REQ_COOKIE_NAME = "req-cookie-name"
    REQ_FILENAME = "req-filename"
    REQ_HEADER = "req-header"
    REQ_HEADER_NAME = "req-header-name"
    REQ_RAW_URI = "req-raw-uri"
    REQ_URI = "req-uri"
    RESP_BODY = "resp-body"
    RESP_HDR = "resp-hdr"
    RESP_STATUS = "resp-status"

class ProfileMethodMethodPolicyAllowedMethodsEnum(str, Enum):
    """Allowed values for allowed_methods field in method.method-policy."""
    GET = "get"
    POST = "post"
    PUT = "put"
    HEAD = "head"
    CONNECT = "connect"
    TRACE = "trace"
    OPTIONS = "options"
    DELETE = "delete"
    OTHERS = "others"

class ProfileMethodDefaultAllowedMethodsEnum(str, Enum):
    """Allowed values for default_allowed_methods field in method."""
    GET = "get"
    POST = "post"
    PUT = "put"
    HEAD = "head"
    CONNECT = "connect"
    TRACE = "trace"
    OPTIONS = "options"
    DELETE = "delete"
    OTHERS = "others"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ProfileUrlAccessAccessPattern(BaseModel):
    """
    Child table model for url-access.access-pattern.
    
    URL access pattern.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="URL access pattern ID.")    
    srcaddr: str | None = Field(max_length=79, default=None, description="Source address.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']    
    pattern: str = Field(max_length=511, description="URL pattern.")    
    regex: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable regular expression based pattern match.")    
    negate: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable match negation.")
class ProfileUrlAccess(BaseModel):
    """
    Child table model for url-access.
    
    URL access list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="URL access ID.")    
    address: str = Field(max_length=79, description="Host address.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']    
    action: Literal["bypass", "permit", "block"] | None = Field(default="permit", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")    
    access_pattern: list[ProfileUrlAccessAccessPattern] = Field(default_factory=list, description="URL access pattern.")
class ProfileSignatureMainClass(BaseModel):
    """
    Child table model for signature.main-class.
    
    Main signature class.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Main signature class ID.")  # datasource: ['waf.main-class.id']    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Status.")    
    action: Literal["allow", "block", "erase"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileSignatureDisabledSubClass(BaseModel):
    """
    Child table model for signature.disabled-sub-class.
    
    Disabled signature subclasses.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Signature subclass ID.")  # datasource: ['waf.sub-class.id']
class ProfileSignatureDisabledSignature(BaseModel):
    """
    Child table model for signature.disabled-signature.
    
    Disabled signatures.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Signature ID.")  # datasource: ['waf.signature.id']
class ProfileSignatureCustomSignature(BaseModel):
    """
    Child table model for signature.custom-signature.
    
    Custom signature.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=35, default=None, description="Signature name.")    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Status.")    
    action: Literal["allow", "block", "erase"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")    
    direction: Literal["request", "response"] | None = Field(default="request", description="Traffic direction.")    
    case_sensitivity: Literal["disable", "enable"] | None = Field(default="disable", description="Case sensitivity in pattern.")    
    pattern: str | None = Field(max_length=511, default=None, description="Match pattern.")    
    target: list[ProfileSignatureCustomSignatureTargetEnum] = Field(default_factory=list, description="Match HTTP target.")
class ProfileSignature(BaseModel):
    """
    Child table model for signature.
    
    WAF signatures.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    main_class: list[ProfileSignatureMainClass] = Field(default_factory=list, description="Main signature class.")    
    disabled_sub_class: list[ProfileSignatureDisabledSubClass] = Field(default_factory=list, description="Disabled signature subclasses.")    
    disabled_signature: list[ProfileSignatureDisabledSignature] = Field(default_factory=list, description="Disabled signatures.")    
    credit_card_detection_threshold: int | None = Field(ge=0, le=128, default=3, description="The minimum number of Credit cards to detect violation.")    
    custom_signature: list[ProfileSignatureCustomSignature] = Field(default_factory=list, description="Custom signature.")
class ProfileMethodMethodPolicy(BaseModel):
    """
    Child table model for method.method-policy.
    
    HTTP method policy.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="HTTP method policy ID.")    
    pattern: str | None = Field(max_length=511, default=None, description="URL pattern.")    
    regex: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable regular expression based pattern match.")    
    address: str = Field(max_length=79, description="Host address.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']    
    allowed_methods: list[ProfileMethodMethodPolicyAllowedMethodsEnum] = Field(default_factory=list, description="Allowed Methods.")
class ProfileMethod(BaseModel):
    """
    Child table model for method.
    
    Method restriction.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Status.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")    
    default_allowed_methods: list[ProfileMethodDefaultAllowedMethodsEnum] = Field(default_factory=list, description="Methods.")    
    method_policy: list[ProfileMethodMethodPolicy] = Field(default_factory=list, description="HTTP method policy.")
class ProfileConstraintVersion(BaseModel):
    """
    Child table model for constraint.version.
    
    Enable/disable HTTP version check.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintUrlParamLength(BaseModel):
    """
    Child table model for constraint.url-param-length.
    
    Maximum length of parameter in URL.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    length: int | None = Field(ge=0, le=2147483647, default=8192, description="Maximum length of URL parameter in bytes (0 to 2147483647).")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintParamLength(BaseModel):
    """
    Child table model for constraint.param-length.
    
    Maximum length of parameter in URL, HTTP POST request or HTTP body.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    length: int | None = Field(ge=0, le=2147483647, default=8192, description="Maximum length of parameter in URL, HTTP POST request or HTTP body in bytes (0 to 2147483647).")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintMethod(BaseModel):
    """
    Child table model for constraint.method.
    
    Enable/disable HTTP method check.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintMaxUrlParam(BaseModel):
    """
    Child table model for constraint.max-url-param.
    
    Maximum number of parameters in URL.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    max_url_param: int | None = Field(ge=0, le=2147483647, default=16, description="Maximum number of parameters in URL (0 to 2147483647).")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintMaxRangeSegment(BaseModel):
    """
    Child table model for constraint.max-range-segment.
    
    Maximum number of range segments in HTTP range line.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    max_range_segment: int | None = Field(ge=0, le=2147483647, default=5, description="Maximum number of range segments in HTTP range line (0 to 2147483647).")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintMaxHeaderLine(BaseModel):
    """
    Child table model for constraint.max-header-line.
    
    Maximum number of HTTP header line.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    max_header_line: int | None = Field(ge=0, le=2147483647, default=32, description="Maximum number HTTP header lines (0 to 2147483647).")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintMaxCookie(BaseModel):
    """
    Child table model for constraint.max-cookie.
    
    Maximum number of cookies in HTTP request.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    max_cookie: int | None = Field(ge=0, le=2147483647, default=16, description="Maximum number of cookies in HTTP request (0 to 2147483647).")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintMalformed(BaseModel):
    """
    Child table model for constraint.malformed.
    
    Enable/disable malformed HTTP request check.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintLineLength(BaseModel):
    """
    Child table model for constraint.line-length.
    
    HTTP line length in request.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    length: int | None = Field(ge=0, le=2147483647, default=1024, description="Length of HTTP line in bytes (0 to 2147483647).")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintHostname(BaseModel):
    """
    Child table model for constraint.hostname.
    
    Enable/disable hostname check.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintHeaderLength(BaseModel):
    """
    Child table model for constraint.header-length.
    
    HTTP header length in request.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    length: int | None = Field(ge=0, le=2147483647, default=8192, description="Length of HTTP header in bytes (0 to 2147483647).")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraintException(BaseModel):
    """
    Child table model for constraint.exception.
    
    HTTP constraint exception.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Exception ID.")    
    pattern: str = Field(max_length=511, description="URL pattern.")    
    regex: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable regular expression based pattern match.")    
    address: str = Field(max_length=79, description="Host address.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']    
    header_length: Literal["enable", "disable"] | None = Field(default="disable", description="HTTP header length in request.")    
    content_length: Literal["enable", "disable"] | None = Field(default="disable", description="HTTP content length in request.")    
    param_length: Literal["enable", "disable"] | None = Field(default="disable", description="Maximum length of parameter in URL, HTTP POST request or HTTP body.")    
    line_length: Literal["enable", "disable"] | None = Field(default="disable", description="HTTP line length in request.")    
    url_param_length: Literal["enable", "disable"] | None = Field(default="disable", description="Maximum length of parameter in URL.")    
    version: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable HTTP version check.")    
    method: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable HTTP method check.")    
    hostname: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable hostname check.")    
    malformed: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable malformed HTTP request check.")    
    max_cookie: Literal["enable", "disable"] | None = Field(default="disable", description="Maximum number of cookies in HTTP request.")    
    max_header_line: Literal["enable", "disable"] | None = Field(default="disable", description="Maximum number of HTTP header line.")    
    max_url_param: Literal["enable", "disable"] | None = Field(default="disable", description="Maximum number of parameters in URL.")    
    max_range_segment: Literal["enable", "disable"] | None = Field(default="disable", description="Maximum number of range segments in HTTP range line.")
class ProfileConstraintContentLength(BaseModel):
    """
    Child table model for constraint.content-length.
    
    HTTP content length in request.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable the constraint.")    
    length: int | None = Field(ge=0, le=2147483647, default=67108864, description="Length of HTTP content in bytes (0 to 2147483647).")    
    action: Literal["allow", "block"] | None = Field(default="allow", description="Action.")    
    log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")
class ProfileConstraint(BaseModel):
    """
    Child table model for constraint.
    
    WAF HTTP protocol restrictions.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    header_length: ProfileConstraintHeaderLength | None = Field(default=None, description="HTTP header length in request.")    
    content_length: ProfileConstraintContentLength | None = Field(default=None, description="HTTP content length in request.")    
    param_length: ProfileConstraintParamLength | None = Field(default=None, description="Maximum length of parameter in URL, HTTP POST request or HTTP body.")    
    line_length: ProfileConstraintLineLength | None = Field(default=None, description="HTTP line length in request.")    
    url_param_length: ProfileConstraintUrlParamLength | None = Field(default=None, description="Maximum length of parameter in URL.")    
    version: ProfileConstraintVersion | None = Field(default=None, description="Enable/disable HTTP version check.")    
    method: ProfileConstraintMethod | None = Field(default=None, description="Enable/disable HTTP method check.")    
    hostname: ProfileConstraintHostname | None = Field(default=None, description="Enable/disable hostname check.")    
    malformed: ProfileConstraintMalformed | None = Field(default=None, description="Enable/disable malformed HTTP request check.")    
    max_cookie: ProfileConstraintMaxCookie | None = Field(default=None, description="Maximum number of cookies in HTTP request.")    
    max_header_line: ProfileConstraintMaxHeaderLine | None = Field(default=None, description="Maximum number of HTTP header line.")    
    max_url_param: ProfileConstraintMaxUrlParam | None = Field(default=None, description="Maximum number of parameters in URL.")    
    max_range_segment: ProfileConstraintMaxRangeSegment | None = Field(default=None, description="Maximum number of range segments in HTTP range line.")    
    exception: list[ProfileConstraintException] = Field(default_factory=list, description="HTTP constraint exception.")
class ProfileAddressListTrustedAddress(BaseModel):
    """
    Child table model for address-list.trusted-address.
    
    Trusted address.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="Address name.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']
class ProfileAddressListBlockedAddress(BaseModel):
    """
    Child table model for address-list.blocked-address.
    
    Blocked address.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="Address name.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']
class ProfileAddressList(BaseModel):
    """
    Child table model for address-list.
    
    Address block and allow lists.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Status.")    
    blocked_log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging on blocked addresses.")    
    severity: Literal["high", "medium", "low"] | None = Field(default="medium", description="Severity.")    
    trusted_address: list[ProfileAddressListTrustedAddress] = Field(default_factory=list, description="Trusted address.")    
    blocked_address: list[ProfileAddressListBlockedAddress] = Field(default_factory=list, description="Blocked address.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class ProfileModel(BaseModel):
    """
    Pydantic model for waf/profile configuration.
    
    Configure Web application firewall configuration.
    
    Validation Rules:        - name: max_length=47 pattern=        - external: pattern=        - extended_log: pattern=        - signature: pattern=        - constraint: pattern=        - method: pattern=        - address_list: pattern=        - url_access: pattern=        - comment: max_length=1023 pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=47, default=None, description="WAF Profile name.")    
    external: Literal["disable", "enable"] | None = Field(default="disable", description="Disable/Enable external HTTP Inspection.")    
    extended_log: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable extended logging.")    
    signature: ProfileSignature | None = Field(default=None, description="WAF signatures.")    
    constraint: ProfileConstraint | None = Field(default=None, description="WAF HTTP protocol restrictions.")    
    method: ProfileMethod | None = Field(default=None, description="Method restriction.")    
    address_list: ProfileAddressList | None = Field(default=None, description="Address block and allow lists.")    
    url_access: list[ProfileUrlAccess] = Field(default_factory=list, description="URL access list.")    
    comment: str | None = Field(max_length=1023, default=None, description="Comment.")    
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
    async def validate_url_access_references(self, client: Any) -> list[str]:
        """
        Validate url_access references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/address        - firewall/addrgrp        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ProfileModel(
            ...     url_access=[{"address": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_url_access_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.waf.profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "url_access", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("address")
            else:
                value = getattr(item, "address", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.firewall.address.exists(value):
                found = True
            elif await client.api.cmdb.firewall.addrgrp.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Url-Access '{value}' not found in "
                    "firewall/address or firewall/addrgrp"
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
        
        errors = await self.validate_url_access_references(client)
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
    "ProfileModel",    "ProfileSignature",    "ProfileSignature.MainClass",    "ProfileSignature.DisabledSubClass",    "ProfileSignature.DisabledSignature",    "ProfileSignature.CustomSignature",    "ProfileConstraint",    "ProfileConstraint.HeaderLength",    "ProfileConstraint.ContentLength",    "ProfileConstraint.ParamLength",    "ProfileConstraint.LineLength",    "ProfileConstraint.UrlParamLength",    "ProfileConstraint.Version",    "ProfileConstraint.Method",    "ProfileConstraint.Hostname",    "ProfileConstraint.Malformed",    "ProfileConstraint.MaxCookie",    "ProfileConstraint.MaxHeaderLine",    "ProfileConstraint.MaxUrlParam",    "ProfileConstraint.MaxRangeSegment",    "ProfileConstraint.Exception",    "ProfileMethod",    "ProfileMethod.MethodPolicy",    "ProfileAddressList",    "ProfileAddressList.TrustedAddress",    "ProfileAddressList.BlockedAddress",    "ProfileUrlAccess",    "ProfileUrlAccess.AccessPattern",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:27.441474Z
# ============================================================================