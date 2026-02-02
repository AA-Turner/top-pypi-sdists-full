"""
Pydantic Models for CMDB - wireless_controller/wtp_group

Runtime validation models for wireless_controller/wtp_group configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class WtpGroupWtps(BaseModel):
    """
    Child table model for wtps.
    
    WTP list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    wtp_id: str = Field(max_length=35, description="WTP ID.")  # datasource: ['wireless-controller.wtp.wtp-id']
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class WtpGroupPlatformTypeEnum(str, Enum):
    """Allowed values for platform_type field."""
    AP_11N = "AP-11N"
    C24JE = "C24JE"
    V_421E = "421E"
    V_423E = "423E"
    V_221E = "221E"
    V_222E = "222E"
    V_223E = "223E"
    V_224E = "224E"
    V_231E = "231E"
    V_321E = "321E"
    V_431F = "431F"
    V_431FL = "431FL"
    V_432F = "432F"
    V_432FR = "432FR"
    V_433F = "433F"
    V_433FL = "433FL"
    V_231F = "231F"
    V_231FL = "231FL"
    V_234F = "234F"
    V_23JF = "23JF"
    V_831F = "831F"
    V_231G = "231G"
    V_233G = "233G"
    V_234G = "234G"
    V_431G = "431G"
    V_432G = "432G"
    V_433G = "433G"
    V_231K = "231K"
    V_231KD = "231KD"
    V_23JK = "23JK"
    V_222KL = "222KL"
    V_241K = "241K"
    V_243K = "243K"
    V_244K = "244K"
    V_441K = "441K"
    V_432K = "432K"
    V_443K = "443K"
    U421E = "U421E"
    U422EV = "U422EV"
    U423E = "U423E"
    U221EV = "U221EV"
    U223EV = "U223EV"
    U24JEV = "U24JEV"
    U321EV = "U321EV"
    U323EV = "U323EV"
    U431F = "U431F"
    U433F = "U433F"
    U231F = "U231F"
    U234F = "U234F"
    U432F = "U432F"
    U231G = "U231G"
    MVP = "MVP"


# ============================================================================
# Main Model
# ============================================================================

class WtpGroupModel(BaseModel):
    """
    Pydantic model for wireless_controller/wtp_group configuration.
    
    Configure WTP groups.
    
    Validation Rules:        - name: max_length=35 pattern=        - platform_type: pattern=        - ble_major_id: min=0 max=65535 pattern=        - wtps: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=35, default=None, description="WTP group name.")    
    platform_type: WtpGroupPlatformTypeEnum | None = Field(default=None, description="FortiAP models to define the WTP group platform type.")    
    ble_major_id: int | None = Field(ge=0, le=65535, default=0, description="Override BLE Major ID.")    
    wtps: list[WtpGroupWtps] = Field(default_factory=list, description="WTP list.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "WtpGroupModel":
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
    async def validate_wtps_references(self, client: Any) -> list[str]:
        """
        Validate wtps references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/wtp        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpGroupModel(
            ...     wtps=[{"wtp-id": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_wtps_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_group.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "wtps", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("wtp-id")
            else:
                value = getattr(item, "wtp-id", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.wireless_controller.wtp.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Wtps '{value}' not found in "
                    "wireless-controller/wtp"
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
        
        errors = await self.validate_wtps_references(client)
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
    "WtpGroupModel",    "WtpGroupWtps",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:57.546027Z
# ============================================================================