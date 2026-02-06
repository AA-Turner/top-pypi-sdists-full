"""
Pydantic Models for CMDB - system/modem

Runtime validation models for system/modem configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class ModemRedialEnum(str, Enum):
    """Allowed values for redial field."""
    NONE = "none"
    V_1 = "1"
    V_2 = "2"
    V_3 = "3"
    V_4 = "4"
    V_5 = "5"
    V_6 = "6"
    V_7 = "7"
    V_8 = "8"
    V_9 = "9"
    V_10 = "10"

class ModemAuthtype1Enum(str, Enum):
    """Allowed values for authtype1 field."""
    PAP = "pap"
    CHAP = "chap"
    MSCHAP = "mschap"
    MSCHAPV2 = "mschapv2"

class ModemAuthtype2Enum(str, Enum):
    """Allowed values for authtype2 field."""
    PAP = "pap"
    CHAP = "chap"
    MSCHAP = "mschap"
    MSCHAPV2 = "mschapv2"

class ModemAuthtype3Enum(str, Enum):
    """Allowed values for authtype3 field."""
    PAP = "pap"
    CHAP = "chap"
    MSCHAP = "mschap"
    MSCHAPV2 = "mschapv2"


# ============================================================================
# Main Model
# ============================================================================

class ModemModel(BaseModel):
    """
    Pydantic model for system/modem configuration.
    
    Configuration for system/modem
    
    Validation Rules:        - status: pattern=        - pin_init: pattern=        - network_init: pattern=        - lockdown_lac: pattern=        - mode: pattern=        - auto_dial: pattern=        - dial_on_demand: pattern=        - idle_timer: pattern=        - redial: pattern=        - reset: pattern=        - holddown_timer: pattern=        - connect_timeout: pattern=        - interface: pattern=        - wireless_port: pattern=        - dont_send_CR1: pattern=        - phone1: pattern=        - dial_cmd1: pattern=        - username1: pattern=        - passwd1: pattern=        - extra_init1: pattern=        - peer_modem1: pattern=        - ppp_echo_request1: pattern=        - authtype1: pattern=        - dont_send_CR2: pattern=        - phone2: pattern=        - dial_cmd2: pattern=        - username2: pattern=        - passwd2: pattern=        - extra_init2: pattern=        - peer_modem2: pattern=        - ppp_echo_request2: pattern=        - authtype2: pattern=        - dont_send_CR3: pattern=        - phone3: pattern=        - dial_cmd3: pattern=        - username3: pattern=        - passwd3: pattern=        - extra_init3: pattern=        - peer_modem3: pattern=        - ppp_echo_request3: pattern=        - altmode: pattern=        - authtype3: pattern=        - traffic_check: pattern=        - action: pattern=        - distance: pattern=        - priority: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    status: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable Modem support (equivalent to bringing an interface up or down).    enable:Enable setting.    disable:Disable setting.")    
    pin_init: str | None = Field(default=None, description="AT command to set the PIN (AT+PIN=<pin>).")    
    network_init: str | None = Field(default=None, description="AT command to set the Network name/type (AT+COPS=<mode>,[<format>,<oper>[,<AcT>]]).")    
    lockdown_lac: str | None = Field(default=None, description="Allow connection only to the specified Location Area Code (LAC).")    
    mode: Literal["standalone", "redundant"] | None = Field(default=None, description="Set MODEM operation mode to redundant or standalone.    standalone:Standalone.    redundant:Redundant for an interface.")    
    auto_dial: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable auto-dial after a reboot or disconnection.    enable:Enable setting.    disable:Disable setting.")    
    dial_on_demand: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable to dial the modem when packets are routed to the modem interface.    enable:Enable setting.    disable:Disable setting.")    
    idle_timer: int | None = Field(default=None, description="MODEM connection idle time (1 - 9999 min, default = 5).")    
    redial: ModemRedialEnum | None = Field(default=None, description="Redial limit (1 - 10 attempts, none = redial forever).    none:Forever.    1:One attempt.    2:Two attempts.    3:Three attempts.    4:Four attempts.    5:Five attempts.    6:Six attempts.    7:Seven attempts.    8:Eight attempts.    9:Nine attempts.    10:Ten attempts.")    
    reset: int | None = Field(default=None, description="Number of dial attempts before resetting modem (0 = never reset).")    
    holddown_timer: int | None = Field(default=None, description="Hold down timer in seconds (1 - 60 sec).")    
    connect_timeout: int | None = Field(default=None, description="Connection completion timeout (30 - 255 sec, default = 90).")    
    interface: str | None = Field(default=None, description="Name of redundant interface.")    
    wireless_port: int | None = Field(default=None, description="Enter wireless port number: 0 for default, 1 for first port, and so on (0 - 4294967295).")    
    dont_send_CR1: Literal["enable", "disable"] | None = Field(default=None, description="Do not send CR when connected (ISP1).    enable:Enable setting.    disable:Disable setting.")    
    phone1: str | None = Field(default=None, description="Phone number to connect to the dialup account (must not contain spaces, and should include standard special characters).")    
    dial_cmd1: str | None = Field(default=None, description="Dial command (this is often an ATD or ATDT command).")    
    username1: str | None = Field(default=None, description="User name to access the specified dialup account.")    
    passwd1: str | None = Field(default=None, description="Password to access the specified dialup account.")    
    extra_init1: str | None = Field(default=None, description="Extra initialization string to ISP 1.")    
    peer_modem1: Literal["generic", "actiontec", "ascend_TNT"] | None = Field(default=None, description="Specify peer MODEM type for phone1.    generic:All other modem type.    actiontec:ActionTec modem.    ascend_TNT:Ascend TNT modem.")    
    ppp_echo_request1: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable PPP echo-request to ISP 1.    enable:Enable setting.    disable:Disable setting.")    
    authtype1: ModemAuthtype1Enum | None = Field(default=None, description="Allowed authentication types for ISP 1.    pap:PAP    chap:CHAP    mschap:MSCHAP    mschapv2:MSCHAPv2")    
    dont_send_CR2: Literal["enable", "disable"] | None = Field(default=None, description="Do not send CR when connected (ISP2).    enable:Enable setting.    disable:Disable setting.")    
    phone2: str | None = Field(default=None, description="Phone number to connect to the dialup account (must not contain spaces, and should include standard special characters).")    
    dial_cmd2: str | None = Field(default=None, description="Dial command (this is often an ATD or ATDT command).")    
    username2: str | None = Field(default=None, description="User name to access the specified dialup account.")    
    passwd2: str | None = Field(default=None, description="Password to access the specified dialup account.")    
    extra_init2: str | None = Field(default=None, description="Extra initialization string to ISP 2.")    
    peer_modem2: Literal["generic", "actiontec", "ascend_TNT"] | None = Field(default=None, description="Specify peer MODEM type for phone2.    generic:All other modem type.    actiontec:ActionTec modem.    ascend_TNT:Ascend TNT modem.")    
    ppp_echo_request2: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable PPP echo-request to ISP 2.    enable:Enable setting.    disable:Disable setting.")    
    authtype2: ModemAuthtype2Enum | None = Field(default=None, description="Allowed authentication types for ISP 2.    pap:PAP    chap:CHAP    mschap:MSCHAP    mschapv2:MSCHAPv2")    
    dont_send_CR3: Literal["enable", "disable"] | None = Field(default=None, description="Do not send CR when connected (ISP3).    enable:Enable setting.    disable:Disable setting.")    
    phone3: str | None = Field(default=None, description="Phone number to connect to the dialup account (must not contain spaces, and should include standard special characters).")    
    dial_cmd3: str | None = Field(default=None, description="Dial command (this is often an ATD or ATDT command).")    
    username3: str | None = Field(default=None, description="User name to access the specified dialup account.")    
    passwd3: str | None = Field(default=None, description="Password to access the specified dialup account.")    
    extra_init3: str | None = Field(default=None, description="Extra initialization string to ISP 3.")    
    peer_modem3: Literal["generic", "actiontec", "ascend_TNT"] | None = Field(default=None, description="Specify peer MODEM type for phone3.    generic:All other modem type.    actiontec:ActionTec modem.    ascend_TNT:Ascend TNT modem.")    
    ppp_echo_request3: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable PPP echo-request to ISP 3.    enable:Enable setting.    disable:Disable setting.")    
    altmode: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable altmode for installations using PPP in China.    enable:Enable setting.    disable:Disable setting.")    
    authtype3: ModemAuthtype3Enum | None = Field(default=None, description="Allowed authentication types for ISP 3.    pap:PAP    chap:CHAP    mschap:MSCHAP    mschapv2:MSCHAPv2")    
    traffic_check: Literal["enable", "disable"] | None = Field(default=None, description="Enable/disable traffic-check.    enable:Enable setting.    disable:Disable setting.")    
    action: Literal["dial", "stop", "none"] | None = Field(default=None, description="Dial up/stop MODEM.    dial:Dial up number.    stop:Stop dialup.    none:No action.")    
    distance: int | None = Field(default=None, description="Distance of learned routes (1 - 255, default = 1).")    
    priority: int | None = Field(default=None, description="Priority of learned routes (1 - 65535, default = 1).")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "ModemModel":
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
    "ModemModel",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:28.865540Z
# ============================================================================