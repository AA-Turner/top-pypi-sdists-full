"""
Pydantic Models for CMDB - wireless_controller/wtp

Runtime validation models for wireless_controller/wtp configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum
from uuid import UUID

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class WtpRadio4BandEnum(str, Enum):
    """Allowed values for band field in radio-4."""
    V_802_11A = "802.11a"
    V_802_11B = "802.11b"
    V_802_11G = "802.11g"
    V_802_11N_2G = "802.11n-2G"
    V_802_11N_5G = "802.11n-5G"
    V_802_11AC_2G = "802.11ac-2G"
    V_802_11AC_5G = "802.11ac-5G"
    V_802_11AX_2G = "802.11ax-2G"
    V_802_11AX_5G = "802.11ax-5G"
    V_802_11AX_6G = "802.11ax-6G"
    V_802_11BE_2G = "802.11be-2G"
    V_802_11BE_5G = "802.11be-5G"
    V_802_11BE_6G = "802.11be-6G"

class WtpRadio4DrmaManualModeEnum(str, Enum):
    """Allowed values for drma_manual_mode field in radio-4."""
    AP = "ap"
    MONITOR = "monitor"
    NCF = "ncf"
    NCF_PEEK = "ncf-peek"

class WtpRadio3BandEnum(str, Enum):
    """Allowed values for band field in radio-3."""
    V_802_11A = "802.11a"
    V_802_11B = "802.11b"
    V_802_11G = "802.11g"
    V_802_11N_2G = "802.11n-2G"
    V_802_11N_5G = "802.11n-5G"
    V_802_11AC_2G = "802.11ac-2G"
    V_802_11AC_5G = "802.11ac-5G"
    V_802_11AX_2G = "802.11ax-2G"
    V_802_11AX_5G = "802.11ax-5G"
    V_802_11AX_6G = "802.11ax-6G"
    V_802_11BE_2G = "802.11be-2G"
    V_802_11BE_5G = "802.11be-5G"
    V_802_11BE_6G = "802.11be-6G"

class WtpRadio3DrmaManualModeEnum(str, Enum):
    """Allowed values for drma_manual_mode field in radio-3."""
    AP = "ap"
    MONITOR = "monitor"
    NCF = "ncf"
    NCF_PEEK = "ncf-peek"

class WtpRadio2BandEnum(str, Enum):
    """Allowed values for band field in radio-2."""
    V_802_11A = "802.11a"
    V_802_11B = "802.11b"
    V_802_11G = "802.11g"
    V_802_11N_2G = "802.11n-2G"
    V_802_11N_5G = "802.11n-5G"
    V_802_11AC_2G = "802.11ac-2G"
    V_802_11AC_5G = "802.11ac-5G"
    V_802_11AX_2G = "802.11ax-2G"
    V_802_11AX_5G = "802.11ax-5G"
    V_802_11AX_6G = "802.11ax-6G"
    V_802_11BE_2G = "802.11be-2G"
    V_802_11BE_5G = "802.11be-5G"
    V_802_11BE_6G = "802.11be-6G"

class WtpRadio2DrmaManualModeEnum(str, Enum):
    """Allowed values for drma_manual_mode field in radio-2."""
    AP = "ap"
    MONITOR = "monitor"
    NCF = "ncf"
    NCF_PEEK = "ncf-peek"

class WtpRadio1BandEnum(str, Enum):
    """Allowed values for band field in radio-1."""
    V_802_11A = "802.11a"
    V_802_11B = "802.11b"
    V_802_11G = "802.11g"
    V_802_11N_2G = "802.11n-2G"
    V_802_11N_5G = "802.11n-5G"
    V_802_11AC_2G = "802.11ac-2G"
    V_802_11AC_5G = "802.11ac-5G"
    V_802_11AX_2G = "802.11ax-2G"
    V_802_11AX_5G = "802.11ax-5G"
    V_802_11AX_6G = "802.11ax-6G"
    V_802_11BE_2G = "802.11be-2G"
    V_802_11BE_5G = "802.11be-5G"
    V_802_11BE_6G = "802.11be-6G"

class WtpRadio1DrmaManualModeEnum(str, Enum):
    """Allowed values for drma_manual_mode field in radio-1."""
    AP = "ap"
    MONITOR = "monitor"
    NCF = "ncf"
    NCF_PEEK = "ncf-peek"

class WtpLanPortModeEnum(str, Enum):
    """Allowed values for port_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpLanPort1ModeEnum(str, Enum):
    """Allowed values for port1_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpLanPort2ModeEnum(str, Enum):
    """Allowed values for port2_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpLanPort3ModeEnum(str, Enum):
    """Allowed values for port3_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpLanPort4ModeEnum(str, Enum):
    """Allowed values for port4_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpLanPort5ModeEnum(str, Enum):
    """Allowed values for port5_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpLanPort6ModeEnum(str, Enum):
    """Allowed values for port6_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpLanPort7ModeEnum(str, Enum):
    """Allowed values for port7_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpLanPort8ModeEnum(str, Enum):
    """Allowed values for port8_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpLanPortEslModeEnum(str, Enum):
    """Allowed values for port_esl_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class WtpSplitTunnelingAcl(BaseModel):
    """
    Child table model for split-tunneling-acl.
    
    Split tunneling ACL filter list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    dest_ip: str = Field(default="0.0.0.0 0.0.0.0", description="Destination IP and mask for the split-tunneling subnet.")
class WtpRadio4Vaps(BaseModel):
    """
    Child table model for radio-4.vaps.
    
    Manually selected list of Virtual Access Points (VAPs).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Virtual Access Point (VAP) name.")  # datasource: ['wireless-controller.vap-group.name', 'system.interface.name']
class WtpRadio4Channel(BaseModel):
    """
    Child table model for radio-4.channel.
    
    Selected list of wireless radio channels.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    chan: str = Field(max_length=3, description="Channel number.")
class WtpRadio4(BaseModel):
    """
    Child table model for radio-4.
    
    Configuration options for radio 4.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    override_band: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile band setting.")    
    band: list[WtpRadio4BandEnum] = Field(default_factory=list, description="WiFi band that Radio 4 operates on.")    
    override_txpower: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile power level configuration.")    
    auto_power_level: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatic power-level adjustment to prevent co-channel interference (default = enable).")    
    auto_power_high: int | None = Field(ge=0, le=4294967295, default=17, description="The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_low: int | None = Field(ge=0, le=4294967295, default=10, description="The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_target: str | None = Field(max_length=7, default="-70", description="Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).")    
    power_mode: Literal["dBm", "percentage"] | None = Field(default="percentage", description="Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).")    
    power_value: int | None = Field(ge=1, le=33, default=27, description="Radio EIRP power in dBm (1 - 33, default = 27).")    
    override_vaps: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override WTP profile Virtual Access Point (VAP) settings.")    
    vap_all: Literal["tunnel", "bridge", "manual"] | None = Field(default="tunnel", description="Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).")    
    vaps: list[WtpRadio4Vaps] = Field(default_factory=list, description="Manually selected list of Virtual Access Points (VAPs).")    
    override_channel: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override WTP profile channel settings.")    
    channel: list[WtpRadio4Channel] = Field(default_factory=list, description="Selected list of wireless radio channels.")    
    drma_manual_mode: WtpRadio4DrmaManualModeEnum | None = Field(default=WtpRadio4DrmaManualModeEnum.NCF, description="Radio mode to be used for DRMA manual mode (default = ncf).")
class WtpRadio3Vaps(BaseModel):
    """
    Child table model for radio-3.vaps.
    
    Manually selected list of Virtual Access Points (VAPs).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Virtual Access Point (VAP) name.")  # datasource: ['wireless-controller.vap-group.name', 'system.interface.name']
class WtpRadio3Channel(BaseModel):
    """
    Child table model for radio-3.channel.
    
    Selected list of wireless radio channels.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    chan: str = Field(max_length=3, description="Channel number.")
class WtpRadio3(BaseModel):
    """
    Child table model for radio-3.
    
    Configuration options for radio 3.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    override_band: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile band setting.")    
    band: list[WtpRadio3BandEnum] = Field(default_factory=list, description="WiFi band that Radio 3 operates on.")    
    override_txpower: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile power level configuration.")    
    auto_power_level: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatic power-level adjustment to prevent co-channel interference (default = enable).")    
    auto_power_high: int | None = Field(ge=0, le=4294967295, default=17, description="The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_low: int | None = Field(ge=0, le=4294967295, default=10, description="The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_target: str | None = Field(max_length=7, default="-70", description="Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).")    
    power_mode: Literal["dBm", "percentage"] | None = Field(default="percentage", description="Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).")    
    power_value: int | None = Field(ge=1, le=33, default=27, description="Radio EIRP power in dBm (1 - 33, default = 27).")    
    override_vaps: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override WTP profile Virtual Access Point (VAP) settings.")    
    vap_all: Literal["tunnel", "bridge", "manual"] | None = Field(default="tunnel", description="Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).")    
    vaps: list[WtpRadio3Vaps] = Field(default_factory=list, description="Manually selected list of Virtual Access Points (VAPs).")    
    override_channel: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override WTP profile channel settings.")    
    channel: list[WtpRadio3Channel] = Field(default_factory=list, description="Selected list of wireless radio channels.")    
    drma_manual_mode: WtpRadio3DrmaManualModeEnum | None = Field(default=WtpRadio3DrmaManualModeEnum.NCF, description="Radio mode to be used for DRMA manual mode (default = ncf).")
class WtpRadio2Vaps(BaseModel):
    """
    Child table model for radio-2.vaps.
    
    Manually selected list of Virtual Access Points (VAPs).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Virtual Access Point (VAP) name.")  # datasource: ['wireless-controller.vap-group.name', 'system.interface.name']
class WtpRadio2Channel(BaseModel):
    """
    Child table model for radio-2.channel.
    
    Selected list of wireless radio channels.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    chan: str = Field(max_length=3, description="Channel number.")
class WtpRadio2(BaseModel):
    """
    Child table model for radio-2.
    
    Configuration options for radio 2.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    override_band: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile band setting.")    
    band: list[WtpRadio2BandEnum] = Field(default_factory=list, description="WiFi band that Radio 2 operates on.")    
    override_txpower: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile power level configuration.")    
    auto_power_level: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatic power-level adjustment to prevent co-channel interference (default = enable).")    
    auto_power_high: int | None = Field(ge=0, le=4294967295, default=17, description="The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_low: int | None = Field(ge=0, le=4294967295, default=10, description="The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_target: str | None = Field(max_length=7, default="-70", description="Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).")    
    power_mode: Literal["dBm", "percentage"] | None = Field(default="percentage", description="Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).")    
    power_value: int | None = Field(ge=1, le=33, default=27, description="Radio EIRP power in dBm (1 - 33, default = 27).")    
    override_vaps: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override WTP profile Virtual Access Point (VAP) settings.")    
    vap_all: Literal["tunnel", "bridge", "manual"] | None = Field(default="tunnel", description="Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).")    
    vaps: list[WtpRadio2Vaps] = Field(default_factory=list, description="Manually selected list of Virtual Access Points (VAPs).")    
    override_channel: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override WTP profile channel settings.")    
    channel: list[WtpRadio2Channel] = Field(default_factory=list, description="Selected list of wireless radio channels.")    
    drma_manual_mode: WtpRadio2DrmaManualModeEnum | None = Field(default=WtpRadio2DrmaManualModeEnum.NCF, description="Radio mode to be used for DRMA manual mode (default = ncf).")
class WtpRadio1Vaps(BaseModel):
    """
    Child table model for radio-1.vaps.
    
    Manually selected list of Virtual Access Points (VAPs).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Virtual Access Point (VAP) name.")  # datasource: ['wireless-controller.vap-group.name', 'system.interface.name']
class WtpRadio1Channel(BaseModel):
    """
    Child table model for radio-1.channel.
    
    Selected list of wireless radio channels.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    chan: str = Field(max_length=3, description="Channel number.")
class WtpRadio1(BaseModel):
    """
    Child table model for radio-1.
    
    Configuration options for radio 1.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    override_band: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile band setting.")    
    band: list[WtpRadio1BandEnum] = Field(default_factory=list, description="WiFi band that Radio 1 operates on.")    
    override_txpower: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile power level configuration.")    
    auto_power_level: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatic power-level adjustment to prevent co-channel interference (default = enable).")    
    auto_power_high: int | None = Field(ge=0, le=4294967295, default=17, description="The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_low: int | None = Field(ge=0, le=4294967295, default=10, description="The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_target: str | None = Field(max_length=7, default="-70", description="Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).")    
    power_mode: Literal["dBm", "percentage"] | None = Field(default="percentage", description="Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).")    
    power_value: int | None = Field(ge=1, le=33, default=27, description="Radio EIRP power in dBm (1 - 33, default = 27).")    
    override_vaps: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override WTP profile Virtual Access Point (VAP) settings.")    
    vap_all: Literal["tunnel", "bridge", "manual"] | None = Field(default="tunnel", description="Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).")    
    vaps: list[WtpRadio1Vaps] = Field(default_factory=list, description="Manually selected list of Virtual Access Points (VAPs).")    
    override_channel: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override WTP profile channel settings.")    
    channel: list[WtpRadio1Channel] = Field(default_factory=list, description="Selected list of wireless radio channels.")    
    drma_manual_mode: WtpRadio1DrmaManualModeEnum | None = Field(default=WtpRadio1DrmaManualModeEnum.NCF, description="Radio mode to be used for DRMA manual mode (default = ncf).")
class WtpLan(BaseModel):
    """
    Child table model for lan.
    
    WTP LAN port mapping.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    port_mode: WtpLanPortModeEnum | None = Field(default=WtpLanPortModeEnum.OFFLINE, description="LAN port mode.")    
    port_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port to SSID.")  # datasource: ['system.interface.name']    
    port1_mode: WtpLanPort1ModeEnum | None = Field(default=WtpLanPort1ModeEnum.OFFLINE, description="LAN port 1 mode.")    
    port1_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 1 to SSID.")  # datasource: ['system.interface.name']    
    port2_mode: WtpLanPort2ModeEnum | None = Field(default=WtpLanPort2ModeEnum.OFFLINE, description="LAN port 2 mode.")    
    port2_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 2 to SSID.")  # datasource: ['system.interface.name']    
    port3_mode: WtpLanPort3ModeEnum | None = Field(default=WtpLanPort3ModeEnum.OFFLINE, description="LAN port 3 mode.")    
    port3_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 3 to SSID.")  # datasource: ['system.interface.name']    
    port4_mode: WtpLanPort4ModeEnum | None = Field(default=WtpLanPort4ModeEnum.OFFLINE, description="LAN port 4 mode.")    
    port4_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 4 to SSID.")  # datasource: ['system.interface.name']    
    port5_mode: WtpLanPort5ModeEnum | None = Field(default=WtpLanPort5ModeEnum.OFFLINE, description="LAN port 5 mode.")    
    port5_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 5 to SSID.")  # datasource: ['system.interface.name']    
    port6_mode: WtpLanPort6ModeEnum | None = Field(default=WtpLanPort6ModeEnum.OFFLINE, description="LAN port 6 mode.")    
    port6_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 6 to SSID.")  # datasource: ['system.interface.name']    
    port7_mode: WtpLanPort7ModeEnum | None = Field(default=WtpLanPort7ModeEnum.OFFLINE, description="LAN port 7 mode.")    
    port7_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 7 to SSID.")  # datasource: ['system.interface.name']    
    port8_mode: WtpLanPort8ModeEnum | None = Field(default=WtpLanPort8ModeEnum.OFFLINE, description="LAN port 8 mode.")    
    port8_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 8 to SSID.")  # datasource: ['system.interface.name']    
    port_esl_mode: WtpLanPortEslModeEnum | None = Field(default=WtpLanPortEslModeEnum.OFFLINE, description="ESL port mode.")    
    port_esl_ssid: str | None = Field(max_length=15, default=None, description="Bridge ESL port to SSID.")  # datasource: ['system.interface.name']
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class WtpPurdueLevelEnum(str, Enum):
    """Allowed values for purdue_level field."""
    V_1 = "1"
    V_1_5 = "1.5"
    V_2 = "2"
    V_2_5 = "2.5"
    V_3 = "3"
    V_3_5 = "3.5"
    V_4 = "4"
    V_5 = "5"
    V_5_5 = "5.5"


# ============================================================================
# Main Model
# ============================================================================

class WtpModel(BaseModel):
    """
    Pydantic model for wireless_controller/wtp configuration.
    
    Configure Wireless Termination Points (WTPs), that is, FortiAPs or APs to be managed by FortiGate.
    
    Validation Rules:        - wtp_id: max_length=35 pattern=        - index: min=0 max=4294967295 pattern=        - uuid: pattern=        - admin: pattern=        - name: max_length=35 pattern=        - location: max_length=35 pattern=        - comment: max_length=255 pattern=        - region: max_length=35 pattern=        - region_x: max_length=15 pattern=        - region_y: max_length=15 pattern=        - firmware_provision: max_length=35 pattern=        - firmware_provision_latest: pattern=        - wtp_profile: max_length=35 pattern=        - apcfg_profile: max_length=35 pattern=        - bonjour_profile: max_length=35 pattern=        - ble_major_id: min=0 max=65535 pattern=        - ble_minor_id: min=0 max=65535 pattern=        - override_led_state: pattern=        - led_state: pattern=        - override_wan_port_mode: pattern=        - wan_port_mode: pattern=        - override_ip_fragment: pattern=        - ip_fragment_preventing: pattern=        - tun_mtu_uplink: min=576 max=1500 pattern=        - tun_mtu_downlink: min=576 max=1500 pattern=        - override_split_tunnel: pattern=        - split_tunneling_acl_path: pattern=        - split_tunneling_acl_local_ap_subnet: pattern=        - split_tunneling_acl: pattern=        - override_lan: pattern=        - lan: pattern=        - override_allowaccess: pattern=        - allowaccess: pattern=        - override_login_passwd_change: pattern=        - login_passwd_change: pattern=        - login_passwd: max_length=128 pattern=        - override_default_mesh_root: pattern=        - default_mesh_root: pattern=        - radio_1: pattern=        - radio_2: pattern=        - radio_3: pattern=        - radio_4: pattern=        - image_download: pattern=        - mesh_bridge_enable: pattern=        - purdue_level: pattern=        - coordinate_latitude: max_length=19 pattern=        - coordinate_longitude: max_length=19 pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    wtp_id: str = Field(max_length=35, description="WTP ID.")    
    index: int | None = Field(ge=0, le=4294967295, default=0, description="Index (0 - 4294967295).")    
    uuid: str | None = Field(default="00000000-0000-0000-0000-000000000000", description="Universally Unique Identifier (UUID; automatically assigned but can be manually reset).")    
    admin: Literal["discovered", "disable", "enable"] | None = Field(default="enable", description="Configure how the FortiGate operating as a wireless controller discovers and manages this WTP, AP or FortiAP.")    
    name: str | None = Field(max_length=35, default=None, description="WTP, AP or FortiAP configuration name.")    
    location: str | None = Field(max_length=35, default=None, description="Field for describing the physical location of the WTP, AP or FortiAP.")    
    comment: str | None = Field(max_length=255, default=None, description="Comment.")    
    region: str | None = Field(max_length=35, default=None, description="Region name WTP is associated with.")  # datasource: ['wireless-controller.region.name']    
    region_x: str | None = Field(max_length=15, default="0", description="Relative horizontal region coordinate (between 0 and 1).")    
    region_y: str | None = Field(max_length=15, default="0", description="Relative vertical region coordinate (between 0 and 1).")    
    firmware_provision: str | None = Field(max_length=35, default=None, description="Firmware version to provision to this FortiAP on bootup (major.minor.build, i.e. 6.2.1234).")    
    firmware_provision_latest: Literal["disable", "once"] | None = Field(default="disable", description="Enable/disable one-time automatic provisioning of the latest firmware version.")    
    wtp_profile: str = Field(max_length=35, description="WTP profile name to apply to this WTP, AP or FortiAP.")  # datasource: ['wireless-controller.wtp-profile.name']    
    apcfg_profile: str | None = Field(max_length=35, default=None, description="AP local configuration profile name.")  # datasource: ['wireless-controller.apcfg-profile.name']    
    bonjour_profile: str | None = Field(max_length=35, default=None, description="Bonjour profile name.")  # datasource: ['wireless-controller.bonjour-profile.name']    
    ble_major_id: int | None = Field(ge=0, le=65535, default=0, description="Override BLE Major ID.")    
    ble_minor_id: int | None = Field(ge=0, le=65535, default=0, description="Override BLE Minor ID.")    
    override_led_state: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the profile LED state setting for this FortiAP. You must enable this option to use the led-state command to turn off the FortiAP's LEDs.")    
    led_state: Literal["enable", "disable"] | None = Field(default="enable", description="Enable to allow the FortiAPs LEDs to light. Disable to keep the LEDs off. You may want to keep the LEDs off so they are not distracting in low light areas etc.")    
    override_wan_port_mode: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable overriding the wan-port-mode in the WTP profile.")    
    wan_port_mode: Literal["wan-lan", "wan-only"] | None = Field(default="wan-only", description="Enable/disable using the FortiAP WAN port as a LAN port.")    
    override_ip_fragment: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable overriding the WTP profile IP fragment prevention setting.")    
    ip_fragment_preventing: list[Literal["tcp-mss-adjust", "icmp-unreachable"]] = Field(default_factory=list, description="Method(s) by which IP fragmentation is prevented for control and data packets through CAPWAP tunnel (default = tcp-mss-adjust).")    
    tun_mtu_uplink: int | None = Field(ge=576, le=1500, default=0, description="The maximum transmission unit (MTU) of uplink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).")    
    tun_mtu_downlink: int | None = Field(ge=576, le=1500, default=0, description="The MTU of downlink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).")    
    override_split_tunnel: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable overriding the WTP profile split tunneling setting.")    
    split_tunneling_acl_path: Literal["tunnel", "local"] | None = Field(default="local", description="Split tunneling ACL path is local/tunnel.")    
    split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatically adding local subnetwork of FortiAP to split-tunneling ACL (default = disable).")    
    split_tunneling_acl: list[WtpSplitTunnelingAcl] = Field(default_factory=list, description="Split tunneling ACL filter list.")    
    override_lan: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile LAN port setting.")    
    lan: WtpLan | None = Field(default=None, description="WTP LAN port mapping.")    
    override_allowaccess: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile management access configuration.")    
    allowaccess: list[Literal["https", "ssh", "snmp"]] = Field(default_factory=list, description="Control management access to the managed WTP, FortiAP, or AP. Separate entries with a space.")    
    override_login_passwd_change: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile login-password (administrator password) setting.")    
    login_passwd_change: Literal["yes", "default", "no"] | None = Field(default="no", description="Change or reset the administrator password of a managed WTP, FortiAP or AP (yes, default, or no, default = no).")    
    login_passwd: Any = Field(max_length=128, default=None, description="Set the managed WTP, FortiAP, or AP's administrator password.")    
    override_default_mesh_root: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override the WTP profile default mesh root SSID setting.")    
    default_mesh_root: Literal["enable", "disable"] | None = Field(default="disable", description="Configure default mesh root SSID when it is not included by radio's SSID configuration.")    
    radio_1: WtpRadio1 | None = Field(default=None, description="Configuration options for radio 1.")    
    radio_2: WtpRadio2 | None = Field(default=None, description="Configuration options for radio 2.")    
    radio_3: WtpRadio3 | None = Field(default=None, description="Configuration options for radio 3.")    
    radio_4: WtpRadio4 | None = Field(default=None, description="Configuration options for radio 4.")    
    image_download: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable WTP image download.")    
    mesh_bridge_enable: Literal["default", "enable", "disable"] | None = Field(default="default", description="Enable/disable mesh Ethernet bridge when WTP is configured as a mesh branch/leaf AP.")    
    purdue_level: WtpPurdueLevelEnum | None = Field(default=WtpPurdueLevelEnum.V_3, description="Purdue Level of this WTP.")    
    coordinate_latitude: str | None = Field(max_length=19, default=None, description="WTP latitude coordinate.")    
    coordinate_longitude: str | None = Field(max_length=19, default=None, description="WTP longitude coordinate.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('region')
    @classmethod
    def validate_region(cls, v: Any) -> Any:
        """
        Validate region field.
        
        Datasource: ['wireless-controller.region.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('wtp_profile')
    @classmethod
    def validate_wtp_profile(cls, v: Any) -> Any:
        """
        Validate wtp_profile field.
        
        Datasource: ['wireless-controller.wtp-profile.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('apcfg_profile')
    @classmethod
    def validate_apcfg_profile(cls, v: Any) -> Any:
        """
        Validate apcfg_profile field.
        
        Datasource: ['wireless-controller.apcfg-profile.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('bonjour_profile')
    @classmethod
    def validate_bonjour_profile(cls, v: Any) -> Any:
        """
        Validate bonjour_profile field.
        
        Datasource: ['wireless-controller.bonjour-profile.name']
        
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "WtpModel":
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
    async def validate_region_references(self, client: Any) -> list[str]:
        """
        Validate region references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/region        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpModel(
            ...     region="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_region_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "region", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.wireless_controller.region.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Region '{value}' not found in "
                "wireless-controller/region"
            )        
        return errors    
    async def validate_wtp_profile_references(self, client: Any) -> list[str]:
        """
        Validate wtp_profile references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/wtp-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpModel(
            ...     wtp_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_wtp_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "wtp_profile", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.wireless_controller.wtp_profile.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Wtp-Profile '{value}' not found in "
                "wireless-controller/wtp-profile"
            )        
        return errors    
    async def validate_apcfg_profile_references(self, client: Any) -> list[str]:
        """
        Validate apcfg_profile references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/apcfg-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpModel(
            ...     apcfg_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_apcfg_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "apcfg_profile", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.wireless_controller.apcfg_profile.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Apcfg-Profile '{value}' not found in "
                "wireless-controller/apcfg-profile"
            )        
        return errors    
    async def validate_bonjour_profile_references(self, client: Any) -> list[str]:
        """
        Validate bonjour_profile references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/bonjour-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpModel(
            ...     bonjour_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_bonjour_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "bonjour_profile", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.wireless_controller.bonjour_profile.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Bonjour-Profile '{value}' not found in "
                "wireless-controller/bonjour-profile"
            )        
        return errors    
    async def validate_lan_references(self, client: Any) -> list[str]:
        """
        Validate lan references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - system/interface        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpModel(
            ...     lan=[{"port-esl-ssid": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_lan_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "lan", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("port-esl-ssid")
            else:
                value = getattr(item, "port-esl-ssid", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.system.interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Lan '{value}' not found in "
                    "system/interface"
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
        
        errors = await self.validate_region_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_wtp_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_apcfg_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_bonjour_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_lan_references(client)
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
    "WtpModel",    "WtpSplitTunnelingAcl",    "WtpLan",    "WtpRadio1",    "WtpRadio1.Vaps",    "WtpRadio1.Channel",    "WtpRadio2",    "WtpRadio2.Vaps",    "WtpRadio2.Channel",    "WtpRadio3",    "WtpRadio3.Vaps",    "WtpRadio3.Channel",    "WtpRadio4",    "WtpRadio4.Vaps",    "WtpRadio4.Channel",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:56.199132Z
# ============================================================================