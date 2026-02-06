"""
Pydantic Models for CMDB - web_proxy/profile

Runtime validation models for web_proxy/profile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class ProfileHeadersActionEnum(str, Enum):
    """Allowed values for action field in headers."""
    ADD_TO_REQUEST = "add-to-request"
    ADD_TO_RESPONSE = "add-to-response"
    REMOVE_FROM_REQUEST = "remove-from-request"
    REMOVE_FROM_RESPONSE = "remove-from-response"
    MONITOR_REQUEST = "monitor-request"
    MONITOR_RESPONSE = "monitor-response"

class ProfileHeadersAddOptionEnum(str, Enum):
    """Allowed values for add_option field in headers."""
    APPEND = "append"
    NEW_ON_NOT_FOUND = "new-on-not-found"
    NEW = "new"
    REPLACE = "replace"
    REPLACE_WHEN_MATCH = "replace-when-match"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ProfileHeadersDstaddr6(BaseModel):
    """
    Child table model for headers.dstaddr6.
    
    Destination address and address group names (IPv6).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Address name.")  # datasource: ['firewall.address6.name', 'firewall.addrgrp6.name']
class ProfileHeadersDstaddr(BaseModel):
    """
    Child table model for headers.dstaddr.
    
    Destination address and address group names.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Address name.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']
class ProfileHeaders(BaseModel):
    """
    Child table model for headers.
    
    Configure HTTP forwarded requests headers.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="HTTP forwarded header id.")    
    name: str | None = Field(max_length=79, default=None, description="HTTP forwarded header name.")    
    dstaddr: list[ProfileHeadersDstaddr] = Field(default_factory=list, description="Destination address and address group names.")    
    dstaddr6: list[ProfileHeadersDstaddr6] = Field(default_factory=list, description="Destination address and address group names (IPv6).")    
    action: ProfileHeadersActionEnum | None = Field(default=ProfileHeadersActionEnum.ADD_TO_REQUEST, description="Configure adding, removing, or logging of the HTTP header entry in HTTP requests and responses.")    
    content: str | None = Field(max_length=3999, default=None, description="HTTP header content (max length: 3999 characters).")    
    base64_encoding: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable use of base64 encoding of HTTP content.")    
    add_option: ProfileHeadersAddOptionEnum | None = Field(default=ProfileHeadersAddOptionEnum.NEW, description="Configure options to append content to existing HTTP header or add new HTTP header.")    
    protocol: list[Literal["https", "http"]] = Field(default_factory=list, description="Configure protocol(s) to take add-option action on (HTTP, HTTPS, or both).")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class ProfileModel(BaseModel):
    """
    Pydantic model for web_proxy/profile configuration.
    
    Configure web proxy profiles.
    
    Validation Rules:        - name: max_length=63 pattern=        - header_client_ip: pattern=        - header_via_request: pattern=        - header_via_response: pattern=        - header_client_cert: pattern=        - header_x_forwarded_for: pattern=        - header_x_forwarded_client_cert: pattern=        - header_front_end_https: pattern=        - header_x_authenticated_user: pattern=        - header_x_authenticated_groups: pattern=        - strip_encoding: pattern=        - log_header_change: pattern=        - headers: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=63, default=None, description="Profile name.")    
    header_client_ip: Literal["pass", "add", "remove"] | None = Field(default="pass", description="Action to take on the HTTP client-IP header in forwarded requests: forwards (pass), adds, or removes the HTTP header.")    
    header_via_request: Literal["pass", "add", "remove"] | None = Field(default="pass", description="Action to take on the HTTP via header in forwarded requests: forwards (pass), adds, or removes the HTTP header.")    
    header_via_response: Literal["pass", "add", "remove"] | None = Field(default="pass", description="Action to take on the HTTP via header in forwarded responses: forwards (pass), adds, or removes the HTTP header.")    
    header_client_cert: Literal["pass", "add", "remove"] | None = Field(default="pass", description="Action to take on the HTTP Client-Cert/Client-Cert-Chain headers in forwarded responses: forwards (pass), adds, or removes the HTTP header.")    
    header_x_forwarded_for: Literal["pass", "add", "remove"] | None = Field(default="pass", description="Action to take on the HTTP x-forwarded-for header in forwarded requests: forwards (pass), adds, or removes the HTTP header.")    
    header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = Field(default="pass", description="Action to take on the HTTP x-forwarded-client-cert header in forwarded requests: forwards (pass), adds, or removes the HTTP header.")    
    header_front_end_https: Literal["pass", "add", "remove"] | None = Field(default="pass", description="Action to take on the HTTP front-end-HTTPS header in forwarded requests: forwards (pass), adds, or removes the HTTP header.")    
    header_x_authenticated_user: Literal["pass", "add", "remove"] | None = Field(default="pass", description="Action to take on the HTTP x-authenticated-user header in forwarded requests: forwards (pass), adds, or removes the HTTP header.")    
    header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = Field(default="pass", description="Action to take on the HTTP x-authenticated-groups header in forwarded requests: forwards (pass), adds, or removes the HTTP header.")    
    strip_encoding: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable stripping unsupported encoding from the request header.")    
    log_header_change: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging HTTP header changes.")    
    headers: list[ProfileHeaders] = Field(default_factory=list, description="Configure HTTP forwarded requests headers.")    
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

# ============================================================================
# Type Aliases for Convenience
# ============================================================================

Dict = dict[str, Any]  # For backward compatibility

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "ProfileModel",    "ProfileHeaders",    "ProfileHeaders.Dstaddr",    "ProfileHeaders.Dstaddr6",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:28.675336Z
# ============================================================================