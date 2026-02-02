"""
Pydantic Models for CMDB - wireless_controller/hotspot20/anqp_nai_realm

Runtime validation models for wireless_controller/hotspot20/anqp_nai_realm configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class AnqpNaiRealmNaiListEapMethodAuthParamIdEnum(str, Enum):
    """Allowed values for id_ field in nai-list.eap-method.auth-param."""
    NON_EAP_INNER_AUTH = "non-eap-inner-auth"
    INNER_AUTH_EAP = "inner-auth-eap"
    CREDENTIAL = "credential"
    TUNNELED_CREDENTIAL = "tunneled-credential"

class AnqpNaiRealmNaiListEapMethodAuthParamValEnum(str, Enum):
    """Allowed values for val field in nai-list.eap-method.auth-param."""
    EAP_IDENTITY = "eap-identity"
    EAP_MD5 = "eap-md5"
    EAP_TLS = "eap-tls"
    EAP_TTLS = "eap-ttls"
    EAP_PEAP = "eap-peap"
    EAP_SIM = "eap-sim"
    EAP_AKA = "eap-aka"
    EAP_AKA_PRIME = "eap-aka-prime"
    NON_EAP_PAP = "non-eap-pap"
    NON_EAP_CHAP = "non-eap-chap"
    NON_EAP_MSCHAP = "non-eap-mschap"
    NON_EAP_MSCHAPV2 = "non-eap-mschapv2"
    CRED_SIM = "cred-sim"
    CRED_USIM = "cred-usim"
    CRED_NFC = "cred-nfc"
    CRED_HARDWARE_TOKEN = "cred-hardware-token"
    CRED_SOFTOKEN = "cred-softoken"
    CRED_CERTIFICATE = "cred-certificate"
    CRED_USER_PWD = "cred-user-pwd"
    CRED_NONE = "cred-none"
    CRED_VENDOR_SPECIFIC = "cred-vendor-specific"
    TUN_CRED_SIM = "tun-cred-sim"
    TUN_CRED_USIM = "tun-cred-usim"
    TUN_CRED_NFC = "tun-cred-nfc"
    TUN_CRED_HARDWARE_TOKEN = "tun-cred-hardware-token"
    TUN_CRED_SOFTOKEN = "tun-cred-softoken"
    TUN_CRED_CERTIFICATE = "tun-cred-certificate"
    TUN_CRED_USER_PWD = "tun-cred-user-pwd"
    TUN_CRED_ANONYMOUS = "tun-cred-anonymous"
    TUN_CRED_VENDOR_SPECIFIC = "tun-cred-vendor-specific"

class AnqpNaiRealmNaiListEapMethodMethodEnum(str, Enum):
    """Allowed values for method field in nai-list.eap-method."""
    EAP_IDENTITY = "eap-identity"
    EAP_MD5 = "eap-md5"
    EAP_TLS = "eap-tls"
    EAP_TTLS = "eap-ttls"
    EAP_PEAP = "eap-peap"
    EAP_SIM = "eap-sim"
    EAP_AKA = "eap-aka"
    EAP_AKA_PRIME = "eap-aka-prime"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class AnqpNaiRealmNaiListEapMethodAuthParam(BaseModel):
    """
    Child table model for nai-list.eap-method.auth-param.
    
    EAP auth param.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    index: int | None = Field(ge=1, le=4, default=0, description="Param index.")    
    id_: AnqpNaiRealmNaiListEapMethodAuthParamIdEnum | None = Field(default=AnqpNaiRealmNaiListEapMethodAuthParamIdEnum.INNER_AUTH_EAP, serialization_alias="id", description="ID of authentication parameter.")    
    val: AnqpNaiRealmNaiListEapMethodAuthParamValEnum | None = Field(default=AnqpNaiRealmNaiListEapMethodAuthParamValEnum.EAP_IDENTITY, description="Value of authentication parameter.")
class AnqpNaiRealmNaiListEapMethod(BaseModel):
    """
    Child table model for nai-list.eap-method.
    
    EAP Methods.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    index: int | None = Field(ge=1, le=5, default=0, description="EAP method index.")    
    method: AnqpNaiRealmNaiListEapMethodMethodEnum | None = Field(default=AnqpNaiRealmNaiListEapMethodMethodEnum.EAP_IDENTITY, description="EAP method type.")    
    auth_param: list[AnqpNaiRealmNaiListEapMethodAuthParam] = Field(default_factory=list, description="EAP auth param.")
class AnqpNaiRealmNaiList(BaseModel):
    """
    Child table model for nai-list.
    
    NAI list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=35, default=None, description="NAI realm name.")    
    encoding: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable format in accordance with IETF RFC 4282.")    
    nai_realm: str | None = Field(max_length=255, default=None, description="Configure NAI realms (delimited by a semi-colon character).")    
    eap_method: list[AnqpNaiRealmNaiListEapMethod] = Field(default_factory=list, description="EAP Methods.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class AnqpNaiRealmModel(BaseModel):
    """
    Pydantic model for wireless_controller/hotspot20/anqp_nai_realm configuration.
    
    Configure network access identifier (NAI) realm.
    
    Validation Rules:        - name: max_length=35 pattern=        - nai_list: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=35, default=None, description="NAI realm list name.")    
    nai_list: list[AnqpNaiRealmNaiList] = Field(default_factory=list, description="NAI list.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "AnqpNaiRealmModel":
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
    "AnqpNaiRealmModel",    "AnqpNaiRealmNaiList",    "AnqpNaiRealmNaiList.EapMethod",    "AnqpNaiRealmNaiList.EapMethod.AuthParam",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:55.715070Z
# ============================================================================