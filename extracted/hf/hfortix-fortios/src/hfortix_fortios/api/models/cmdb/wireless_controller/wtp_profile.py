"""
Pydantic Models for CMDB - wireless_controller/wtp_profile

Runtime validation models for wireless_controller/wtp_profile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class WtpProfileRadio4ModeEnum(str, Enum):
    """Allowed values for mode field in radio-4."""
    DISABLED = "disabled"
    AP = "ap"
    MONITOR = "monitor"
    SNIFFER = "sniffer"
    SAM = "sam"

class WtpProfileRadio4BandEnum(str, Enum):
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

class WtpProfileRadio4PowersaveOptimizeEnum(str, Enum):
    """Allowed values for powersave_optimize field in radio-4."""
    TIM = "tim"
    AC_VO = "ac-vo"
    NO_OBSS_SCAN = "no-obss-scan"
    NO_11B_RATE = "no-11b-rate"
    CLIENT_RATE_FOLLOW = "client-rate-follow"

class WtpProfileRadio4TransmitOptimizeEnum(str, Enum):
    """Allowed values for transmit_optimize field in radio-4."""
    DISABLE = "disable"
    POWER_SAVE = "power-save"
    AGGR_LIMIT = "aggr-limit"
    RETRY_LIMIT = "retry-limit"
    SEND_BAR = "send-bar"

class WtpProfileRadio4MimoModeEnum(str, Enum):
    """Allowed values for mimo_mode field in radio-4."""
    DEFAULT = "default"
    V_1X1 = "1x1"
    V_2X2 = "2x2"
    V_3X3 = "3x3"
    V_4X4 = "4x4"
    V_8X8 = "8x8"

class WtpProfileRadio4ChannelBondingEnum(str, Enum):
    """Allowed values for channel_bonding field in radio-4."""
    V_320MHZ = "320MHz"
    V_240MHZ = "240MHz"
    V_160MHZ = "160MHz"
    V_80MHZ = "80MHz"
    V_40MHZ = "40MHz"
    V_20MHZ = "20MHz"

class WtpProfileRadio4OptionalAntennaEnum(str, Enum):
    """Allowed values for optional_antenna field in radio-4."""
    NONE = "none"
    CUSTOM = "custom"
    FANT_04ABGN_0606_O_N = "FANT-04ABGN-0606-O-N"
    FANT_04ABGN_1414_P_N = "FANT-04ABGN-1414-P-N"
    FANT_04ABGN_8065_P_N = "FANT-04ABGN-8065-P-N"
    FANT_04ABGN_0606_O_R = "FANT-04ABGN-0606-O-R"
    FANT_04ABGN_0606_P_R = "FANT-04ABGN-0606-P-R"
    FANT_10ACAX_1213_D_N = "FANT-10ACAX-1213-D-N"
    FANT_08ABGN_1213_D_R = "FANT-08ABGN-1213-D-R"
    FANT_04BEAX_0606_P_R = "FANT-04BEAX-0606-P-R"

class WtpProfileRadio4ApSnifferChanWidthEnum(str, Enum):
    """Allowed values for ap_sniffer_chan_width field in radio-4."""
    V_320MHZ = "320MHz"
    V_240MHZ = "240MHz"
    V_160MHZ = "160MHz"
    V_80MHZ = "80MHz"
    V_40MHZ = "40MHz"
    V_20MHZ = "20MHz"

class WtpProfileRadio4SamSecurityTypeEnum(str, Enum):
    """Allowed values for sam_security_type field in radio-4."""
    OPEN = "open"
    WPA_PERSONAL = "wpa-personal"
    WPA_ENTERPRISE = "wpa-enterprise"
    WPA3_SAE = "wpa3-sae"
    OWE = "owe"

class WtpProfileRadio3ModeEnum(str, Enum):
    """Allowed values for mode field in radio-3."""
    DISABLED = "disabled"
    AP = "ap"
    MONITOR = "monitor"
    SNIFFER = "sniffer"
    SAM = "sam"

class WtpProfileRadio3BandEnum(str, Enum):
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

class WtpProfileRadio3PowersaveOptimizeEnum(str, Enum):
    """Allowed values for powersave_optimize field in radio-3."""
    TIM = "tim"
    AC_VO = "ac-vo"
    NO_OBSS_SCAN = "no-obss-scan"
    NO_11B_RATE = "no-11b-rate"
    CLIENT_RATE_FOLLOW = "client-rate-follow"

class WtpProfileRadio3TransmitOptimizeEnum(str, Enum):
    """Allowed values for transmit_optimize field in radio-3."""
    DISABLE = "disable"
    POWER_SAVE = "power-save"
    AGGR_LIMIT = "aggr-limit"
    RETRY_LIMIT = "retry-limit"
    SEND_BAR = "send-bar"

class WtpProfileRadio3MimoModeEnum(str, Enum):
    """Allowed values for mimo_mode field in radio-3."""
    DEFAULT = "default"
    V_1X1 = "1x1"
    V_2X2 = "2x2"
    V_3X3 = "3x3"
    V_4X4 = "4x4"
    V_8X8 = "8x8"

class WtpProfileRadio3ChannelBondingEnum(str, Enum):
    """Allowed values for channel_bonding field in radio-3."""
    V_320MHZ = "320MHz"
    V_240MHZ = "240MHz"
    V_160MHZ = "160MHz"
    V_80MHZ = "80MHz"
    V_40MHZ = "40MHz"
    V_20MHZ = "20MHz"

class WtpProfileRadio3OptionalAntennaEnum(str, Enum):
    """Allowed values for optional_antenna field in radio-3."""
    NONE = "none"
    CUSTOM = "custom"
    FANT_04ABGN_0606_O_N = "FANT-04ABGN-0606-O-N"
    FANT_04ABGN_1414_P_N = "FANT-04ABGN-1414-P-N"
    FANT_04ABGN_8065_P_N = "FANT-04ABGN-8065-P-N"
    FANT_04ABGN_0606_O_R = "FANT-04ABGN-0606-O-R"
    FANT_04ABGN_0606_P_R = "FANT-04ABGN-0606-P-R"
    FANT_10ACAX_1213_D_N = "FANT-10ACAX-1213-D-N"
    FANT_08ABGN_1213_D_R = "FANT-08ABGN-1213-D-R"
    FANT_04BEAX_0606_P_R = "FANT-04BEAX-0606-P-R"

class WtpProfileRadio3ApSnifferChanWidthEnum(str, Enum):
    """Allowed values for ap_sniffer_chan_width field in radio-3."""
    V_320MHZ = "320MHz"
    V_240MHZ = "240MHz"
    V_160MHZ = "160MHz"
    V_80MHZ = "80MHz"
    V_40MHZ = "40MHz"
    V_20MHZ = "20MHz"

class WtpProfileRadio3SamSecurityTypeEnum(str, Enum):
    """Allowed values for sam_security_type field in radio-3."""
    OPEN = "open"
    WPA_PERSONAL = "wpa-personal"
    WPA_ENTERPRISE = "wpa-enterprise"
    WPA3_SAE = "wpa3-sae"
    OWE = "owe"

class WtpProfileRadio2ModeEnum(str, Enum):
    """Allowed values for mode field in radio-2."""
    DISABLED = "disabled"
    AP = "ap"
    MONITOR = "monitor"
    SNIFFER = "sniffer"
    SAM = "sam"

class WtpProfileRadio2BandEnum(str, Enum):
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

class WtpProfileRadio2PowersaveOptimizeEnum(str, Enum):
    """Allowed values for powersave_optimize field in radio-2."""
    TIM = "tim"
    AC_VO = "ac-vo"
    NO_OBSS_SCAN = "no-obss-scan"
    NO_11B_RATE = "no-11b-rate"
    CLIENT_RATE_FOLLOW = "client-rate-follow"

class WtpProfileRadio2TransmitOptimizeEnum(str, Enum):
    """Allowed values for transmit_optimize field in radio-2."""
    DISABLE = "disable"
    POWER_SAVE = "power-save"
    AGGR_LIMIT = "aggr-limit"
    RETRY_LIMIT = "retry-limit"
    SEND_BAR = "send-bar"

class WtpProfileRadio2MimoModeEnum(str, Enum):
    """Allowed values for mimo_mode field in radio-2."""
    DEFAULT = "default"
    V_1X1 = "1x1"
    V_2X2 = "2x2"
    V_3X3 = "3x3"
    V_4X4 = "4x4"
    V_8X8 = "8x8"

class WtpProfileRadio2ChannelBondingEnum(str, Enum):
    """Allowed values for channel_bonding field in radio-2."""
    V_320MHZ = "320MHz"
    V_240MHZ = "240MHz"
    V_160MHZ = "160MHz"
    V_80MHZ = "80MHz"
    V_40MHZ = "40MHz"
    V_20MHZ = "20MHz"

class WtpProfileRadio2OptionalAntennaEnum(str, Enum):
    """Allowed values for optional_antenna field in radio-2."""
    NONE = "none"
    CUSTOM = "custom"
    FANT_04ABGN_0606_O_N = "FANT-04ABGN-0606-O-N"
    FANT_04ABGN_1414_P_N = "FANT-04ABGN-1414-P-N"
    FANT_04ABGN_8065_P_N = "FANT-04ABGN-8065-P-N"
    FANT_04ABGN_0606_O_R = "FANT-04ABGN-0606-O-R"
    FANT_04ABGN_0606_P_R = "FANT-04ABGN-0606-P-R"
    FANT_10ACAX_1213_D_N = "FANT-10ACAX-1213-D-N"
    FANT_08ABGN_1213_D_R = "FANT-08ABGN-1213-D-R"
    FANT_04BEAX_0606_P_R = "FANT-04BEAX-0606-P-R"

class WtpProfileRadio2ApSnifferChanWidthEnum(str, Enum):
    """Allowed values for ap_sniffer_chan_width field in radio-2."""
    V_320MHZ = "320MHz"
    V_240MHZ = "240MHz"
    V_160MHZ = "160MHz"
    V_80MHZ = "80MHz"
    V_40MHZ = "40MHz"
    V_20MHZ = "20MHz"

class WtpProfileRadio2SamSecurityTypeEnum(str, Enum):
    """Allowed values for sam_security_type field in radio-2."""
    OPEN = "open"
    WPA_PERSONAL = "wpa-personal"
    WPA_ENTERPRISE = "wpa-enterprise"
    WPA3_SAE = "wpa3-sae"
    OWE = "owe"

class WtpProfileRadio1ModeEnum(str, Enum):
    """Allowed values for mode field in radio-1."""
    DISABLED = "disabled"
    AP = "ap"
    MONITOR = "monitor"
    SNIFFER = "sniffer"
    SAM = "sam"

class WtpProfileRadio1BandEnum(str, Enum):
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

class WtpProfileRadio1PowersaveOptimizeEnum(str, Enum):
    """Allowed values for powersave_optimize field in radio-1."""
    TIM = "tim"
    AC_VO = "ac-vo"
    NO_OBSS_SCAN = "no-obss-scan"
    NO_11B_RATE = "no-11b-rate"
    CLIENT_RATE_FOLLOW = "client-rate-follow"

class WtpProfileRadio1TransmitOptimizeEnum(str, Enum):
    """Allowed values for transmit_optimize field in radio-1."""
    DISABLE = "disable"
    POWER_SAVE = "power-save"
    AGGR_LIMIT = "aggr-limit"
    RETRY_LIMIT = "retry-limit"
    SEND_BAR = "send-bar"

class WtpProfileRadio1MimoModeEnum(str, Enum):
    """Allowed values for mimo_mode field in radio-1."""
    DEFAULT = "default"
    V_1X1 = "1x1"
    V_2X2 = "2x2"
    V_3X3 = "3x3"
    V_4X4 = "4x4"
    V_8X8 = "8x8"

class WtpProfileRadio1ChannelBondingEnum(str, Enum):
    """Allowed values for channel_bonding field in radio-1."""
    V_320MHZ = "320MHz"
    V_240MHZ = "240MHz"
    V_160MHZ = "160MHz"
    V_80MHZ = "80MHz"
    V_40MHZ = "40MHz"
    V_20MHZ = "20MHz"

class WtpProfileRadio1OptionalAntennaEnum(str, Enum):
    """Allowed values for optional_antenna field in radio-1."""
    NONE = "none"
    CUSTOM = "custom"
    FANT_04ABGN_0606_O_N = "FANT-04ABGN-0606-O-N"
    FANT_04ABGN_1414_P_N = "FANT-04ABGN-1414-P-N"
    FANT_04ABGN_8065_P_N = "FANT-04ABGN-8065-P-N"
    FANT_04ABGN_0606_O_R = "FANT-04ABGN-0606-O-R"
    FANT_04ABGN_0606_P_R = "FANT-04ABGN-0606-P-R"
    FANT_10ACAX_1213_D_N = "FANT-10ACAX-1213-D-N"
    FANT_08ABGN_1213_D_R = "FANT-08ABGN-1213-D-R"
    FANT_04BEAX_0606_P_R = "FANT-04BEAX-0606-P-R"

class WtpProfileRadio1ApSnifferChanWidthEnum(str, Enum):
    """Allowed values for ap_sniffer_chan_width field in radio-1."""
    V_320MHZ = "320MHz"
    V_240MHZ = "240MHz"
    V_160MHZ = "160MHz"
    V_80MHZ = "80MHz"
    V_40MHZ = "40MHz"
    V_20MHZ = "20MHz"

class WtpProfileRadio1SamSecurityTypeEnum(str, Enum):
    """Allowed values for sam_security_type field in radio-1."""
    OPEN = "open"
    WPA_PERSONAL = "wpa-personal"
    WPA_ENTERPRISE = "wpa-enterprise"
    WPA3_SAE = "wpa3-sae"
    OWE = "owe"

class WtpProfilePlatformTypeEnum(str, Enum):
    """Allowed values for type_ field in platform."""
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

class WtpProfileLanPortModeEnum(str, Enum):
    """Allowed values for port_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileLanPort1ModeEnum(str, Enum):
    """Allowed values for port1_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileLanPort2ModeEnum(str, Enum):
    """Allowed values for port2_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileLanPort3ModeEnum(str, Enum):
    """Allowed values for port3_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileLanPort4ModeEnum(str, Enum):
    """Allowed values for port4_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileLanPort5ModeEnum(str, Enum):
    """Allowed values for port5_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileLanPort6ModeEnum(str, Enum):
    """Allowed values for port6_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileLanPort7ModeEnum(str, Enum):
    """Allowed values for port7_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileLanPort8ModeEnum(str, Enum):
    """Allowed values for port8_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileLanPortEslModeEnum(str, Enum):
    """Allowed values for port_esl_mode field in lan."""
    OFFLINE = "offline"
    NAT_TO_WAN = "nat-to-wan"
    BRIDGE_TO_WAN = "bridge-to-wan"
    BRIDGE_TO_SSID = "bridge-to-ssid"

class WtpProfileEslSesDongleEslChannelEnum(str, Enum):
    """Allowed values for esl_channel field in esl-ses-dongle."""
    _1 = "-1"
    V_0 = "0"
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
    V_127 = "127"

class WtpProfileEslSesDongleOutputPowerEnum(str, Enum):
    """Allowed values for output_power field in esl-ses-dongle."""
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class WtpProfileSplitTunnelingAcl(BaseModel):
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
class WtpProfileRadio4Vaps(BaseModel):
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
class WtpProfileRadio4Channel(BaseModel):
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
class WtpProfileRadio4(BaseModel):
    """
    Child table model for radio-4.
    
    Configuration options for radio 4.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    mode: WtpProfileRadio4ModeEnum | None = Field(default=WtpProfileRadio4ModeEnum.AP, description="Mode of radio 4. Radio 4 can be disabled, configured as an access point, a rogue AP monitor, a sniffer, or a station.")    
    band: list[WtpProfileRadio4BandEnum] = Field(default_factory=list, description="WiFi band that Radio 4 operates on.")    
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"] | None = Field(default="5g-full", description="WiFi 5G band type.")    
    drma: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable dynamic radio mode assignment (DRMA) (default = disable).")    
    drma_sensitivity: Literal["low", "medium", "high"] | None = Field(default="low", description="Network Coverage Factor (NCF) percentage required to consider a radio as redundant (default = low).")    
    airtime_fairness: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable airtime fairness (default = disable).")    
    protection_mode: Literal["rtscts", "ctsonly", "disable"] | None = Field(default="disable", description="Enable/disable 802.11g protection modes to support backwards compatibility with older clients (rtscts, ctsonly, disable).")    
    powersave_optimize: list[WtpProfileRadio4PowersaveOptimizeEnum] = Field(default_factory=list, description="Enable client power-saving features such as TIM, AC VO, and OBSS etc.")    
    transmit_optimize: list[WtpProfileRadio4TransmitOptimizeEnum] = Field(default_factory=list, description="Packet transmission optimization options including power saving, aggregation limiting, retry limiting, etc. All are enabled by default.")    
    amsdu: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable 802.11n AMSDU support. AMSDU can improve performance if supported by your WiFi clients (default = enable).")    
    coexistence: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable allowing both HT20 and HT40 on the same radio (default = enable).")    
    zero_wait_dfs: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable zero wait DFS on radio (default = enable).")    
    bss_color: int | None = Field(ge=0, le=63, default=0, description="BSS color value for this 11ax radio (0 - 63, disable = 0, default = 0).")    
    bss_color_mode: Literal["auto", "static"] | None = Field(default="auto", description="BSS color mode for this 11ax radio (default = auto).")    
    short_guard_interval: Literal["enable", "disable"] | None = Field(default="disable", description="Use either the short guard interval (Short GI) of 400 ns or the long guard interval (Long GI) of 800 ns.")    
    mimo_mode: WtpProfileRadio4MimoModeEnum | None = Field(default=WtpProfileRadio4MimoModeEnum.DEFAULT, description="Configure radio MIMO mode (default = default).")    
    channel_bonding: WtpProfileRadio4ChannelBondingEnum | None = Field(default=WtpProfileRadio4ChannelBondingEnum.V_20MHZ, description="Channel bandwidth: 320, 240, 160, 80, 40, or 20MHz. Channels may use both 20 and 40 by enabling coexistence.")    
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"] | None = Field(default="320MHz-2", description="Channel bandwidth extension: 320 MHz-1 and 320 MHz-2 (default = 320 MHz-2).")    
    optional_antenna: WtpProfileRadio4OptionalAntennaEnum | None = Field(default=WtpProfileRadio4OptionalAntennaEnum.NONE, description="Optional antenna used on FAP (default = none).")    
    optional_antenna_gain: str | None = Field(max_length=7, default="0", description="Optional antenna gain in dBi (0 to 20, default = 0).")    
    auto_power_level: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatic power-level adjustment to prevent co-channel interference (default = disable).")    
    auto_power_high: int | None = Field(ge=0, le=4294967295, default=17, description="The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_low: int | None = Field(ge=0, le=4294967295, default=10, description="The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_target: str | None = Field(max_length=7, default="-70", description="Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).")    
    power_mode: Literal["dBm", "percentage"] | None = Field(default="percentage", description="Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).")    
    power_value: int | None = Field(ge=1, le=33, default=27, description="Radio EIRP power in dBm (1 - 33, default = 27).")    
    dtim: int | None = Field(ge=1, le=255, default=1, description="Delivery Traffic Indication Map (DTIM) period (1 - 255, default = 1). Set higher to save battery life of WiFi client in power-save mode.")    
    beacon_interval: int | None = Field(ge=0, le=65535, default=100, description="Beacon interval. The time between beacon frames in milliseconds. Actual range of beacon interval depends on the AP platform type (default = 100).")    
    _80211d: Literal["enable", "disable"] | None = Field(default="enable", serialization_alias="80211d", description="Enable/disable 802.11d countryie(default = enable).")    
    _80211mc: Literal["enable", "disable"] | None = Field(default="disable", serialization_alias="80211mc", description="Enable/disable 802.11mc responder mode (default = disable).")    
    rts_threshold: int | None = Field(ge=256, le=2346, default=2346, description="Maximum packet size for RTS transmissions, specifying the maximum size of a data packet before RTS/CTS (256 - 2346 bytes, default = 2346).")    
    frag_threshold: int | None = Field(ge=800, le=2346, default=2346, description="Maximum packet size that can be sent without fragmentation (800 - 2346 bytes, default = 2346).")    
    ap_sniffer_bufsize: int | None = Field(ge=1, le=32, default=16, description="Sniffer buffer size (1 - 32 MB, default = 16).")    
    ap_sniffer_chan: int | None = Field(ge=0, le=4294967295, default=6, description="Channel on which to operate the sniffer (default = 6).")    
    ap_sniffer_chan_width: WtpProfileRadio4ApSnifferChanWidthEnum | None = Field(default=WtpProfileRadio4ApSnifferChanWidthEnum.V_20MHZ, description="Channel bandwidth for sniffer.")    
    ap_sniffer_addr: str | None = Field(default="00:00:00:00:00:00", description="MAC address to monitor.")    
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management Beacon frames (default = enable).")    
    ap_sniffer_mgmt_probe: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management probe frames (default = enable).")    
    ap_sniffer_mgmt_other: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management other frames  (default = enable).")    
    ap_sniffer_ctl: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi control frame (default = enable).")    
    ap_sniffer_data: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi data frame (default = enable).")    
    sam_ssid: str | None = Field(max_length=32, default=None, description="SSID for WiFi network.")    
    sam_bssid: str | None = Field(default="00:00:00:00:00:00", description="BSSID for WiFi network.")    
    sam_security_type: WtpProfileRadio4SamSecurityTypeEnum | None = Field(default=WtpProfileRadio4SamSecurityTypeEnum.WPA_PERSONAL, description="Select WiFi network security type (default = \"wpa-personal\" for 2.4/5G radio, \"wpa3-sae\" for 6G radio).")    
    sam_captive_portal: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Captive Portal Authentication (default = disable).")    
    sam_cwp_username: str | None = Field(max_length=35, default=None, description="Username for captive portal authentication.")    
    sam_cwp_password: Any = Field(max_length=128, default=None, description="Password for captive portal authentication.")    
    sam_cwp_test_url: str | None = Field(max_length=255, default=None, description="Website the client is trying to access.")    
    sam_cwp_match_string: str | None = Field(max_length=64, default=None, description="Identification string from the captive portal login form.")    
    sam_cwp_success_string: str | None = Field(max_length=64, default=None, description="Success identification on the page after a successful login.")    
    sam_cwp_failure_string: str | None = Field(max_length=64, default=None, description="Failure identification on the page after an incorrect login.")    
    sam_eap_method: Literal["both", "tls", "peap"] | None = Field(default="peap", description="Select WPA2/WPA3-ENTERPRISE EAP Method (default = PEAP).")    
    sam_client_certificate: str | None = Field(max_length=35, default=None, description="Client certificate for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.local.name']    
    sam_private_key: str | None = Field(max_length=35, default=None, description="Private key for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.local.name']    
    sam_private_key_password: Any = Field(max_length=128, default=None, description="Password for private key file for WPA2/WPA3-ENTERPRISE.")    
    sam_ca_certificate: str | None = Field(max_length=79, default=None, description="CA certificate for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.ca.name']    
    sam_username: str | None = Field(max_length=35, default=None, description="Username for WiFi network connection.")    
    sam_password: Any = Field(max_length=128, default=None, description="Passphrase for WiFi network connection.")    
    sam_test: Literal["ping", "iperf"] | None = Field(default="ping", description="Select SAM test type (default = \"PING\").")    
    sam_server_type: Literal["ip", "fqdn"] | None = Field(default="ip", description="Select SAM server type (default = \"IP\").")    
    sam_server_ip: str | None = Field(default="0.0.0.0", description="SAM test server IP address.")    
    sam_server_fqdn: str | None = Field(max_length=255, default=None, description="SAM test server domain name.")    
    iperf_server_port: int | None = Field(ge=0, le=65535, default=5001, description="Iperf service port number.")    
    iperf_protocol: Literal["udp", "tcp"] | None = Field(default="udp", description="Iperf test protocol (default = \"UDP\").")    
    sam_report_intv: int | None = Field(ge=60, le=864000, default=0, description="SAM report interval (sec), 0 for a one-time report.")    
    channel_utilization: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable measuring channel utilization.")    
    wids_profile: str | None = Field(max_length=35, default=None, description="Wireless Intrusion Detection System (WIDS) profile name to assign to the radio.")  # datasource: ['wireless-controller.wids-profile.name']    
    ai_darrp_support: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable support for FortiAIOps to retrieve Distributed Automatic Radio Resource Provisioning (DARRP) data through REST API calls (default = disable).")    
    darrp: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Distributed Automatic Radio Resource Provisioning (DARRP) to make sure the radio is always using the most optimal channel (default = disable).")    
    arrp_profile: str | None = Field(max_length=35, default=None, description="Distributed Automatic Radio Resource Provisioning (DARRP) profile name to assign to the radio.")  # datasource: ['wireless-controller.arrp-profile.name']    
    max_clients: int | None = Field(ge=0, le=4294967295, default=0, description="Maximum number of stations (STAs) or WiFi clients supported by the radio. Range depends on the hardware.")    
    max_distance: int | None = Field(ge=0, le=54000, default=0, description="Maximum expected distance between the AP and clients (0 - 54000 m, default = 0).")    
    vap_all: Literal["tunnel", "bridge", "manual"] | None = Field(default="tunnel", description="Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).")    
    vaps: list[WtpProfileRadio4Vaps] = Field(default_factory=list, description="Manually selected list of Virtual Access Points (VAPs).")    
    channel: list[WtpProfileRadio4Channel] = Field(default_factory=list, description="Selected list of wireless radio channels.")    
    call_admission_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable WiFi multimedia (WMM) call admission control to optimize WiFi bandwidth use for VoIP calls. New VoIP calls are only accepted if there is enough bandwidth available to support them.")    
    call_capacity: int | None = Field(ge=0, le=60, default=10, description="Maximum number of Voice over WLAN (VoWLAN) phones supported by the radio (0 - 60, default = 10).")    
    bandwidth_admission_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable WiFi multimedia (WMM) bandwidth admission control to optimize WiFi bandwidth use. A request to join the wireless network is only allowed if the access point has enough bandwidth to support it.")    
    bandwidth_capacity: int | None = Field(ge=1, le=600000, default=2000, description="Maximum bandwidth capacity allowed (1 - 600000 Kbps, default = 2000).")
class WtpProfileRadio3Vaps(BaseModel):
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
class WtpProfileRadio3Channel(BaseModel):
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
class WtpProfileRadio3(BaseModel):
    """
    Child table model for radio-3.
    
    Configuration options for radio 3.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    mode: WtpProfileRadio3ModeEnum | None = Field(default=WtpProfileRadio3ModeEnum.AP, description="Mode of radio 3. Radio 3 can be disabled, configured as an access point, a rogue AP monitor, a sniffer, or a station.")    
    band: list[WtpProfileRadio3BandEnum] = Field(default_factory=list, description="WiFi band that Radio 3 operates on.")    
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"] | None = Field(default="5g-full", description="WiFi 5G band type.")    
    drma: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable dynamic radio mode assignment (DRMA) (default = disable).")    
    drma_sensitivity: Literal["low", "medium", "high"] | None = Field(default="low", description="Network Coverage Factor (NCF) percentage required to consider a radio as redundant (default = low).")    
    airtime_fairness: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable airtime fairness (default = disable).")    
    protection_mode: Literal["rtscts", "ctsonly", "disable"] | None = Field(default="disable", description="Enable/disable 802.11g protection modes to support backwards compatibility with older clients (rtscts, ctsonly, disable).")    
    powersave_optimize: list[WtpProfileRadio3PowersaveOptimizeEnum] = Field(default_factory=list, description="Enable client power-saving features such as TIM, AC VO, and OBSS etc.")    
    transmit_optimize: list[WtpProfileRadio3TransmitOptimizeEnum] = Field(default_factory=list, description="Packet transmission optimization options including power saving, aggregation limiting, retry limiting, etc. All are enabled by default.")    
    amsdu: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable 802.11n AMSDU support. AMSDU can improve performance if supported by your WiFi clients (default = enable).")    
    coexistence: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable allowing both HT20 and HT40 on the same radio (default = enable).")    
    zero_wait_dfs: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable zero wait DFS on radio (default = enable).")    
    bss_color: int | None = Field(ge=0, le=63, default=0, description="BSS color value for this 11ax radio (0 - 63, disable = 0, default = 0).")    
    bss_color_mode: Literal["auto", "static"] | None = Field(default="auto", description="BSS color mode for this 11ax radio (default = auto).")    
    short_guard_interval: Literal["enable", "disable"] | None = Field(default="disable", description="Use either the short guard interval (Short GI) of 400 ns or the long guard interval (Long GI) of 800 ns.")    
    mimo_mode: WtpProfileRadio3MimoModeEnum | None = Field(default=WtpProfileRadio3MimoModeEnum.DEFAULT, description="Configure radio MIMO mode (default = default).")    
    channel_bonding: WtpProfileRadio3ChannelBondingEnum | None = Field(default=WtpProfileRadio3ChannelBondingEnum.V_20MHZ, description="Channel bandwidth: 320, 240, 160, 80, 40, or 20MHz. Channels may use both 20 and 40 by enabling coexistence.")    
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"] | None = Field(default="320MHz-2", description="Channel bandwidth extension: 320 MHz-1 and 320 MHz-2 (default = 320 MHz-2).")    
    optional_antenna: WtpProfileRadio3OptionalAntennaEnum | None = Field(default=WtpProfileRadio3OptionalAntennaEnum.NONE, description="Optional antenna used on FAP (default = none).")    
    optional_antenna_gain: str | None = Field(max_length=7, default="0", description="Optional antenna gain in dBi (0 to 20, default = 0).")    
    auto_power_level: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatic power-level adjustment to prevent co-channel interference (default = disable).")    
    auto_power_high: int | None = Field(ge=0, le=4294967295, default=17, description="The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_low: int | None = Field(ge=0, le=4294967295, default=10, description="The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_target: str | None = Field(max_length=7, default="-70", description="Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).")    
    power_mode: Literal["dBm", "percentage"] | None = Field(default="percentage", description="Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).")    
    power_value: int | None = Field(ge=1, le=33, default=27, description="Radio EIRP power in dBm (1 - 33, default = 27).")    
    dtim: int | None = Field(ge=1, le=255, default=1, description="Delivery Traffic Indication Map (DTIM) period (1 - 255, default = 1). Set higher to save battery life of WiFi client in power-save mode.")    
    beacon_interval: int | None = Field(ge=0, le=65535, default=100, description="Beacon interval. The time between beacon frames in milliseconds. Actual range of beacon interval depends on the AP platform type (default = 100).")    
    _80211d: Literal["enable", "disable"] | None = Field(default="enable", serialization_alias="80211d", description="Enable/disable 802.11d countryie(default = enable).")    
    _80211mc: Literal["enable", "disable"] | None = Field(default="disable", serialization_alias="80211mc", description="Enable/disable 802.11mc responder mode (default = disable).")    
    rts_threshold: int | None = Field(ge=256, le=2346, default=2346, description="Maximum packet size for RTS transmissions, specifying the maximum size of a data packet before RTS/CTS (256 - 2346 bytes, default = 2346).")    
    frag_threshold: int | None = Field(ge=800, le=2346, default=2346, description="Maximum packet size that can be sent without fragmentation (800 - 2346 bytes, default = 2346).")    
    ap_sniffer_bufsize: int | None = Field(ge=1, le=32, default=16, description="Sniffer buffer size (1 - 32 MB, default = 16).")    
    ap_sniffer_chan: int | None = Field(ge=0, le=4294967295, default=37, description="Channel on which to operate the sniffer (default = 6).")    
    ap_sniffer_chan_width: WtpProfileRadio3ApSnifferChanWidthEnum | None = Field(default=WtpProfileRadio3ApSnifferChanWidthEnum.V_20MHZ, description="Channel bandwidth for sniffer.")    
    ap_sniffer_addr: str | None = Field(default="00:00:00:00:00:00", description="MAC address to monitor.")    
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management Beacon frames (default = enable).")    
    ap_sniffer_mgmt_probe: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management probe frames (default = enable).")    
    ap_sniffer_mgmt_other: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management other frames  (default = enable).")    
    ap_sniffer_ctl: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi control frame (default = enable).")    
    ap_sniffer_data: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi data frame (default = enable).")    
    sam_ssid: str | None = Field(max_length=32, default=None, description="SSID for WiFi network.")    
    sam_bssid: str | None = Field(default="00:00:00:00:00:00", description="BSSID for WiFi network.")    
    sam_security_type: WtpProfileRadio3SamSecurityTypeEnum | None = Field(default=WtpProfileRadio3SamSecurityTypeEnum.WPA_PERSONAL, description="Select WiFi network security type (default = \"wpa-personal\" for 2.4/5G radio, \"wpa3-sae\" for 6G radio).")    
    sam_captive_portal: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Captive Portal Authentication (default = disable).")    
    sam_cwp_username: str | None = Field(max_length=35, default=None, description="Username for captive portal authentication.")    
    sam_cwp_password: Any = Field(max_length=128, default=None, description="Password for captive portal authentication.")    
    sam_cwp_test_url: str | None = Field(max_length=255, default=None, description="Website the client is trying to access.")    
    sam_cwp_match_string: str | None = Field(max_length=64, default=None, description="Identification string from the captive portal login form.")    
    sam_cwp_success_string: str | None = Field(max_length=64, default=None, description="Success identification on the page after a successful login.")    
    sam_cwp_failure_string: str | None = Field(max_length=64, default=None, description="Failure identification on the page after an incorrect login.")    
    sam_eap_method: Literal["both", "tls", "peap"] | None = Field(default="peap", description="Select WPA2/WPA3-ENTERPRISE EAP Method (default = PEAP).")    
    sam_client_certificate: str | None = Field(max_length=35, default=None, description="Client certificate for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.local.name']    
    sam_private_key: str | None = Field(max_length=35, default=None, description="Private key for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.local.name']    
    sam_private_key_password: Any = Field(max_length=128, default=None, description="Password for private key file for WPA2/WPA3-ENTERPRISE.")    
    sam_ca_certificate: str | None = Field(max_length=79, default=None, description="CA certificate for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.ca.name']    
    sam_username: str | None = Field(max_length=35, default=None, description="Username for WiFi network connection.")    
    sam_password: Any = Field(max_length=128, default=None, description="Passphrase for WiFi network connection.")    
    sam_test: Literal["ping", "iperf"] | None = Field(default="ping", description="Select SAM test type (default = \"PING\").")    
    sam_server_type: Literal["ip", "fqdn"] | None = Field(default="ip", description="Select SAM server type (default = \"IP\").")    
    sam_server_ip: str | None = Field(default="0.0.0.0", description="SAM test server IP address.")    
    sam_server_fqdn: str | None = Field(max_length=255, default=None, description="SAM test server domain name.")    
    iperf_server_port: int | None = Field(ge=0, le=65535, default=5001, description="Iperf service port number.")    
    iperf_protocol: Literal["udp", "tcp"] | None = Field(default="udp", description="Iperf test protocol (default = \"UDP\").")    
    sam_report_intv: int | None = Field(ge=60, le=864000, default=0, description="SAM report interval (sec), 0 for a one-time report.")    
    channel_utilization: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable measuring channel utilization.")    
    wids_profile: str | None = Field(max_length=35, default=None, description="Wireless Intrusion Detection System (WIDS) profile name to assign to the radio.")  # datasource: ['wireless-controller.wids-profile.name']    
    ai_darrp_support: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable support for FortiAIOps to retrieve Distributed Automatic Radio Resource Provisioning (DARRP) data through REST API calls (default = disable).")    
    darrp: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Distributed Automatic Radio Resource Provisioning (DARRP) to make sure the radio is always using the most optimal channel (default = disable).")    
    arrp_profile: str | None = Field(max_length=35, default=None, description="Distributed Automatic Radio Resource Provisioning (DARRP) profile name to assign to the radio.")  # datasource: ['wireless-controller.arrp-profile.name']    
    max_clients: int | None = Field(ge=0, le=4294967295, default=0, description="Maximum number of stations (STAs) or WiFi clients supported by the radio. Range depends on the hardware.")    
    max_distance: int | None = Field(ge=0, le=54000, default=0, description="Maximum expected distance between the AP and clients (0 - 54000 m, default = 0).")    
    vap_all: Literal["tunnel", "bridge", "manual"] | None = Field(default="tunnel", description="Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).")    
    vaps: list[WtpProfileRadio3Vaps] = Field(default_factory=list, description="Manually selected list of Virtual Access Points (VAPs).")    
    channel: list[WtpProfileRadio3Channel] = Field(default_factory=list, description="Selected list of wireless radio channels.")    
    call_admission_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable WiFi multimedia (WMM) call admission control to optimize WiFi bandwidth use for VoIP calls. New VoIP calls are only accepted if there is enough bandwidth available to support them.")    
    call_capacity: int | None = Field(ge=0, le=60, default=10, description="Maximum number of Voice over WLAN (VoWLAN) phones supported by the radio (0 - 60, default = 10).")    
    bandwidth_admission_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable WiFi multimedia (WMM) bandwidth admission control to optimize WiFi bandwidth use. A request to join the wireless network is only allowed if the access point has enough bandwidth to support it.")    
    bandwidth_capacity: int | None = Field(ge=1, le=600000, default=2000, description="Maximum bandwidth capacity allowed (1 - 600000 Kbps, default = 2000).")
class WtpProfileRadio2Vaps(BaseModel):
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
class WtpProfileRadio2Channel(BaseModel):
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
class WtpProfileRadio2(BaseModel):
    """
    Child table model for radio-2.
    
    Configuration options for radio 2.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    mode: WtpProfileRadio2ModeEnum | None = Field(default=WtpProfileRadio2ModeEnum.AP, description="Mode of radio 2. Radio 2 can be disabled, configured as an access point, a rogue AP monitor, a sniffer, or a station.")    
    band: list[WtpProfileRadio2BandEnum] = Field(default_factory=list, description="WiFi band that Radio 2 operates on.")    
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"] | None = Field(default="5g-full", description="WiFi 5G band type.")    
    drma: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable dynamic radio mode assignment (DRMA) (default = disable).")    
    drma_sensitivity: Literal["low", "medium", "high"] | None = Field(default="low", description="Network Coverage Factor (NCF) percentage required to consider a radio as redundant (default = low).")    
    airtime_fairness: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable airtime fairness (default = disable).")    
    protection_mode: Literal["rtscts", "ctsonly", "disable"] | None = Field(default="disable", description="Enable/disable 802.11g protection modes to support backwards compatibility with older clients (rtscts, ctsonly, disable).")    
    powersave_optimize: list[WtpProfileRadio2PowersaveOptimizeEnum] = Field(default_factory=list, description="Enable client power-saving features such as TIM, AC VO, and OBSS etc.")    
    transmit_optimize: list[WtpProfileRadio2TransmitOptimizeEnum] = Field(default_factory=list, description="Packet transmission optimization options including power saving, aggregation limiting, retry limiting, etc. All are enabled by default.")    
    amsdu: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable 802.11n AMSDU support. AMSDU can improve performance if supported by your WiFi clients (default = enable).")    
    coexistence: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable allowing both HT20 and HT40 on the same radio (default = enable).")    
    zero_wait_dfs: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable zero wait DFS on radio (default = enable).")    
    bss_color: int | None = Field(ge=0, le=63, default=0, description="BSS color value for this 11ax radio (0 - 63, disable = 0, default = 0).")    
    bss_color_mode: Literal["auto", "static"] | None = Field(default="auto", description="BSS color mode for this 11ax radio (default = auto).")    
    short_guard_interval: Literal["enable", "disable"] | None = Field(default="disable", description="Use either the short guard interval (Short GI) of 400 ns or the long guard interval (Long GI) of 800 ns.")    
    mimo_mode: WtpProfileRadio2MimoModeEnum | None = Field(default=WtpProfileRadio2MimoModeEnum.DEFAULT, description="Configure radio MIMO mode (default = default).")    
    channel_bonding: WtpProfileRadio2ChannelBondingEnum | None = Field(default=WtpProfileRadio2ChannelBondingEnum.V_20MHZ, description="Channel bandwidth: 320, 240, 160, 80, 40, or 20MHz. Channels may use both 20 and 40 by enabling coexistence.")    
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"] | None = Field(default="320MHz-2", description="Channel bandwidth extension: 320 MHz-1 and 320 MHz-2 (default = 320 MHz-2).")    
    optional_antenna: WtpProfileRadio2OptionalAntennaEnum | None = Field(default=WtpProfileRadio2OptionalAntennaEnum.NONE, description="Optional antenna used on FAP (default = none).")    
    optional_antenna_gain: str | None = Field(max_length=7, default="0", description="Optional antenna gain in dBi (0 to 20, default = 0).")    
    auto_power_level: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatic power-level adjustment to prevent co-channel interference (default = disable).")    
    auto_power_high: int | None = Field(ge=0, le=4294967295, default=17, description="The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_low: int | None = Field(ge=0, le=4294967295, default=10, description="The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_target: str | None = Field(max_length=7, default="-70", description="Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).")    
    power_mode: Literal["dBm", "percentage"] | None = Field(default="percentage", description="Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).")    
    power_value: int | None = Field(ge=1, le=33, default=27, description="Radio EIRP power in dBm (1 - 33, default = 27).")    
    dtim: int | None = Field(ge=1, le=255, default=1, description="Delivery Traffic Indication Map (DTIM) period (1 - 255, default = 1). Set higher to save battery life of WiFi client in power-save mode.")    
    beacon_interval: int | None = Field(ge=0, le=65535, default=100, description="Beacon interval. The time between beacon frames in milliseconds. Actual range of beacon interval depends on the AP platform type (default = 100).")    
    _80211d: Literal["enable", "disable"] | None = Field(default="enable", serialization_alias="80211d", description="Enable/disable 802.11d countryie(default = enable).")    
    _80211mc: Literal["enable", "disable"] | None = Field(default="disable", serialization_alias="80211mc", description="Enable/disable 802.11mc responder mode (default = disable).")    
    rts_threshold: int | None = Field(ge=256, le=2346, default=2346, description="Maximum packet size for RTS transmissions, specifying the maximum size of a data packet before RTS/CTS (256 - 2346 bytes, default = 2346).")    
    frag_threshold: int | None = Field(ge=800, le=2346, default=2346, description="Maximum packet size that can be sent without fragmentation (800 - 2346 bytes, default = 2346).")    
    ap_sniffer_bufsize: int | None = Field(ge=1, le=32, default=16, description="Sniffer buffer size (1 - 32 MB, default = 16).")    
    ap_sniffer_chan: int | None = Field(ge=0, le=4294967295, default=6, description="Channel on which to operate the sniffer (default = 6).")    
    ap_sniffer_chan_width: WtpProfileRadio2ApSnifferChanWidthEnum | None = Field(default=WtpProfileRadio2ApSnifferChanWidthEnum.V_20MHZ, description="Channel bandwidth for sniffer.")    
    ap_sniffer_addr: str | None = Field(default="00:00:00:00:00:00", description="MAC address to monitor.")    
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management Beacon frames (default = enable).")    
    ap_sniffer_mgmt_probe: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management probe frames (default = enable).")    
    ap_sniffer_mgmt_other: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management other frames  (default = enable).")    
    ap_sniffer_ctl: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi control frame (default = enable).")    
    ap_sniffer_data: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi data frame (default = enable).")    
    sam_ssid: str | None = Field(max_length=32, default=None, description="SSID for WiFi network.")    
    sam_bssid: str | None = Field(default="00:00:00:00:00:00", description="BSSID for WiFi network.")    
    sam_security_type: WtpProfileRadio2SamSecurityTypeEnum | None = Field(default=WtpProfileRadio2SamSecurityTypeEnum.WPA_PERSONAL, description="Select WiFi network security type (default = \"wpa-personal\" for 2.4/5G radio, \"wpa3-sae\" for 6G radio).")    
    sam_captive_portal: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Captive Portal Authentication (default = disable).")    
    sam_cwp_username: str | None = Field(max_length=35, default=None, description="Username for captive portal authentication.")    
    sam_cwp_password: Any = Field(max_length=128, default=None, description="Password for captive portal authentication.")    
    sam_cwp_test_url: str | None = Field(max_length=255, default=None, description="Website the client is trying to access.")    
    sam_cwp_match_string: str | None = Field(max_length=64, default=None, description="Identification string from the captive portal login form.")    
    sam_cwp_success_string: str | None = Field(max_length=64, default=None, description="Success identification on the page after a successful login.")    
    sam_cwp_failure_string: str | None = Field(max_length=64, default=None, description="Failure identification on the page after an incorrect login.")    
    sam_eap_method: Literal["both", "tls", "peap"] | None = Field(default="peap", description="Select WPA2/WPA3-ENTERPRISE EAP Method (default = PEAP).")    
    sam_client_certificate: str | None = Field(max_length=35, default=None, description="Client certificate for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.local.name']    
    sam_private_key: str | None = Field(max_length=35, default=None, description="Private key for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.local.name']    
    sam_private_key_password: Any = Field(max_length=128, default=None, description="Password for private key file for WPA2/WPA3-ENTERPRISE.")    
    sam_ca_certificate: str | None = Field(max_length=79, default=None, description="CA certificate for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.ca.name']    
    sam_username: str | None = Field(max_length=35, default=None, description="Username for WiFi network connection.")    
    sam_password: Any = Field(max_length=128, default=None, description="Passphrase for WiFi network connection.")    
    sam_test: Literal["ping", "iperf"] | None = Field(default="ping", description="Select SAM test type (default = \"PING\").")    
    sam_server_type: Literal["ip", "fqdn"] | None = Field(default="ip", description="Select SAM server type (default = \"IP\").")    
    sam_server_ip: str | None = Field(default="0.0.0.0", description="SAM test server IP address.")    
    sam_server_fqdn: str | None = Field(max_length=255, default=None, description="SAM test server domain name.")    
    iperf_server_port: int | None = Field(ge=0, le=65535, default=5001, description="Iperf service port number.")    
    iperf_protocol: Literal["udp", "tcp"] | None = Field(default="udp", description="Iperf test protocol (default = \"UDP\").")    
    sam_report_intv: int | None = Field(ge=60, le=864000, default=0, description="SAM report interval (sec), 0 for a one-time report.")    
    channel_utilization: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable measuring channel utilization.")    
    wids_profile: str | None = Field(max_length=35, default=None, description="Wireless Intrusion Detection System (WIDS) profile name to assign to the radio.")  # datasource: ['wireless-controller.wids-profile.name']    
    ai_darrp_support: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable support for FortiAIOps to retrieve Distributed Automatic Radio Resource Provisioning (DARRP) data through REST API calls (default = disable).")    
    darrp: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Distributed Automatic Radio Resource Provisioning (DARRP) to make sure the radio is always using the most optimal channel (default = disable).")    
    arrp_profile: str | None = Field(max_length=35, default=None, description="Distributed Automatic Radio Resource Provisioning (DARRP) profile name to assign to the radio.")  # datasource: ['wireless-controller.arrp-profile.name']    
    max_clients: int | None = Field(ge=0, le=4294967295, default=0, description="Maximum number of stations (STAs) or WiFi clients supported by the radio. Range depends on the hardware.")    
    max_distance: int | None = Field(ge=0, le=54000, default=0, description="Maximum expected distance between the AP and clients (0 - 54000 m, default = 0).")    
    vap_all: Literal["tunnel", "bridge", "manual"] | None = Field(default="tunnel", description="Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).")    
    vaps: list[WtpProfileRadio2Vaps] = Field(default_factory=list, description="Manually selected list of Virtual Access Points (VAPs).")    
    channel: list[WtpProfileRadio2Channel] = Field(default_factory=list, description="Selected list of wireless radio channels.")    
    call_admission_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable WiFi multimedia (WMM) call admission control to optimize WiFi bandwidth use for VoIP calls. New VoIP calls are only accepted if there is enough bandwidth available to support them.")    
    call_capacity: int | None = Field(ge=0, le=60, default=10, description="Maximum number of Voice over WLAN (VoWLAN) phones supported by the radio (0 - 60, default = 10).")    
    bandwidth_admission_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable WiFi multimedia (WMM) bandwidth admission control to optimize WiFi bandwidth use. A request to join the wireless network is only allowed if the access point has enough bandwidth to support it.")    
    bandwidth_capacity: int | None = Field(ge=1, le=600000, default=2000, description="Maximum bandwidth capacity allowed (1 - 600000 Kbps, default = 2000).")
class WtpProfileRadio1Vaps(BaseModel):
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
class WtpProfileRadio1Channel(BaseModel):
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
class WtpProfileRadio1(BaseModel):
    """
    Child table model for radio-1.
    
    Configuration options for radio 1.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    mode: WtpProfileRadio1ModeEnum | None = Field(default=WtpProfileRadio1ModeEnum.AP, description="Mode of radio 1. Radio 1 can be disabled, configured as an access point, a rogue AP monitor, a sniffer, or a station.")    
    band: list[WtpProfileRadio1BandEnum] = Field(default_factory=list, description="WiFi band that Radio 1 operates on.")    
    band_5g_type: Literal["5g-full", "5g-high", "5g-low"] | None = Field(default="5g-full", description="WiFi 5G band type.")    
    drma: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable dynamic radio mode assignment (DRMA) (default = disable).")    
    drma_sensitivity: Literal["low", "medium", "high"] | None = Field(default="low", description="Network Coverage Factor (NCF) percentage required to consider a radio as redundant (default = low).")    
    airtime_fairness: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable airtime fairness (default = disable).")    
    protection_mode: Literal["rtscts", "ctsonly", "disable"] | None = Field(default="disable", description="Enable/disable 802.11g protection modes to support backwards compatibility with older clients (rtscts, ctsonly, disable).")    
    powersave_optimize: list[WtpProfileRadio1PowersaveOptimizeEnum] = Field(default_factory=list, description="Enable client power-saving features such as TIM, AC VO, and OBSS etc.")    
    transmit_optimize: list[WtpProfileRadio1TransmitOptimizeEnum] = Field(default_factory=list, description="Packet transmission optimization options including power saving, aggregation limiting, retry limiting, etc. All are enabled by default.")    
    amsdu: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable 802.11n AMSDU support. AMSDU can improve performance if supported by your WiFi clients (default = enable).")    
    coexistence: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable allowing both HT20 and HT40 on the same radio (default = enable).")    
    zero_wait_dfs: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable zero wait DFS on radio (default = enable).")    
    bss_color: int | None = Field(ge=0, le=63, default=0, description="BSS color value for this 11ax radio (0 - 63, disable = 0, default = 0).")    
    bss_color_mode: Literal["auto", "static"] | None = Field(default="auto", description="BSS color mode for this 11ax radio (default = auto).")    
    short_guard_interval: Literal["enable", "disable"] | None = Field(default="disable", description="Use either the short guard interval (Short GI) of 400 ns or the long guard interval (Long GI) of 800 ns.")    
    mimo_mode: WtpProfileRadio1MimoModeEnum | None = Field(default=WtpProfileRadio1MimoModeEnum.DEFAULT, description="Configure radio MIMO mode (default = default).")    
    channel_bonding: WtpProfileRadio1ChannelBondingEnum | None = Field(default=WtpProfileRadio1ChannelBondingEnum.V_20MHZ, description="Channel bandwidth: 320, 240, 160, 80, 40, or 20MHz. Channels may use both 20 and 40 by enabling coexistence.")    
    channel_bonding_ext: Literal["320MHz-1", "320MHz-2"] | None = Field(default="320MHz-2", description="Channel bandwidth extension: 320 MHz-1 and 320 MHz-2 (default = 320 MHz-2).")    
    optional_antenna: WtpProfileRadio1OptionalAntennaEnum | None = Field(default=WtpProfileRadio1OptionalAntennaEnum.NONE, description="Optional antenna used on FAP (default = none).")    
    optional_antenna_gain: str | None = Field(max_length=7, default="0", description="Optional antenna gain in dBi (0 to 20, default = 0).")    
    auto_power_level: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatic power-level adjustment to prevent co-channel interference (default = disable).")    
    auto_power_high: int | None = Field(ge=0, le=4294967295, default=17, description="The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_low: int | None = Field(ge=0, le=4294967295, default=10, description="The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).")    
    auto_power_target: str | None = Field(max_length=7, default="-70", description="Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).")    
    power_mode: Literal["dBm", "percentage"] | None = Field(default="percentage", description="Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).")    
    power_value: int | None = Field(ge=1, le=33, default=27, description="Radio EIRP power in dBm (1 - 33, default = 27).")    
    dtim: int | None = Field(ge=1, le=255, default=1, description="Delivery Traffic Indication Map (DTIM) period (1 - 255, default = 1). Set higher to save battery life of WiFi client in power-save mode.")    
    beacon_interval: int | None = Field(ge=0, le=65535, default=100, description="Beacon interval. The time between beacon frames in milliseconds. Actual range of beacon interval depends on the AP platform type (default = 100).")    
    _80211d: Literal["enable", "disable"] | None = Field(default="enable", serialization_alias="80211d", description="Enable/disable 802.11d countryie(default = enable).")    
    _80211mc: Literal["enable", "disable"] | None = Field(default="disable", serialization_alias="80211mc", description="Enable/disable 802.11mc responder mode (default = disable).")    
    rts_threshold: int | None = Field(ge=256, le=2346, default=2346, description="Maximum packet size for RTS transmissions, specifying the maximum size of a data packet before RTS/CTS (256 - 2346 bytes, default = 2346).")    
    frag_threshold: int | None = Field(ge=800, le=2346, default=2346, description="Maximum packet size that can be sent without fragmentation (800 - 2346 bytes, default = 2346).")    
    ap_sniffer_bufsize: int | None = Field(ge=1, le=32, default=16, description="Sniffer buffer size (1 - 32 MB, default = 16).")    
    ap_sniffer_chan: int | None = Field(ge=0, le=4294967295, default=36, description="Channel on which to operate the sniffer (default = 6).")    
    ap_sniffer_chan_width: WtpProfileRadio1ApSnifferChanWidthEnum | None = Field(default=WtpProfileRadio1ApSnifferChanWidthEnum.V_20MHZ, description="Channel bandwidth for sniffer.")    
    ap_sniffer_addr: str | None = Field(default="00:00:00:00:00:00", description="MAC address to monitor.")    
    ap_sniffer_mgmt_beacon: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management Beacon frames (default = enable).")    
    ap_sniffer_mgmt_probe: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management probe frames (default = enable).")    
    ap_sniffer_mgmt_other: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi management other frames  (default = enable).")    
    ap_sniffer_ctl: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi control frame (default = enable).")    
    ap_sniffer_data: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable sniffer on WiFi data frame (default = enable).")    
    sam_ssid: str | None = Field(max_length=32, default=None, description="SSID for WiFi network.")    
    sam_bssid: str | None = Field(default="00:00:00:00:00:00", description="BSSID for WiFi network.")    
    sam_security_type: WtpProfileRadio1SamSecurityTypeEnum | None = Field(default=WtpProfileRadio1SamSecurityTypeEnum.WPA_PERSONAL, description="Select WiFi network security type (default = \"wpa-personal\" for 2.4/5G radio, \"wpa3-sae\" for 6G radio).")    
    sam_captive_portal: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Captive Portal Authentication (default = disable).")    
    sam_cwp_username: str | None = Field(max_length=35, default=None, description="Username for captive portal authentication.")    
    sam_cwp_password: Any = Field(max_length=128, default=None, description="Password for captive portal authentication.")    
    sam_cwp_test_url: str | None = Field(max_length=255, default=None, description="Website the client is trying to access.")    
    sam_cwp_match_string: str | None = Field(max_length=64, default=None, description="Identification string from the captive portal login form.")    
    sam_cwp_success_string: str | None = Field(max_length=64, default=None, description="Success identification on the page after a successful login.")    
    sam_cwp_failure_string: str | None = Field(max_length=64, default=None, description="Failure identification on the page after an incorrect login.")    
    sam_eap_method: Literal["both", "tls", "peap"] | None = Field(default="peap", description="Select WPA2/WPA3-ENTERPRISE EAP Method (default = PEAP).")    
    sam_client_certificate: str | None = Field(max_length=35, default=None, description="Client certificate for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.local.name']    
    sam_private_key: str | None = Field(max_length=35, default=None, description="Private key for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.local.name']    
    sam_private_key_password: Any = Field(max_length=128, default=None, description="Password for private key file for WPA2/WPA3-ENTERPRISE.")    
    sam_ca_certificate: str | None = Field(max_length=79, default=None, description="CA certificate for WPA2/WPA3-ENTERPRISE.")  # datasource: ['vpn.certificate.ca.name']    
    sam_username: str | None = Field(max_length=35, default=None, description="Username for WiFi network connection.")    
    sam_password: Any = Field(max_length=128, default=None, description="Passphrase for WiFi network connection.")    
    sam_test: Literal["ping", "iperf"] | None = Field(default="ping", description="Select SAM test type (default = \"PING\").")    
    sam_server_type: Literal["ip", "fqdn"] | None = Field(default="ip", description="Select SAM server type (default = \"IP\").")    
    sam_server_ip: str | None = Field(default="0.0.0.0", description="SAM test server IP address.")    
    sam_server_fqdn: str | None = Field(max_length=255, default=None, description="SAM test server domain name.")    
    iperf_server_port: int | None = Field(ge=0, le=65535, default=5001, description="Iperf service port number.")    
    iperf_protocol: Literal["udp", "tcp"] | None = Field(default="udp", description="Iperf test protocol (default = \"UDP\").")    
    sam_report_intv: int | None = Field(ge=60, le=864000, default=0, description="SAM report interval (sec), 0 for a one-time report.")    
    channel_utilization: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable measuring channel utilization.")    
    wids_profile: str | None = Field(max_length=35, default=None, description="Wireless Intrusion Detection System (WIDS) profile name to assign to the radio.")  # datasource: ['wireless-controller.wids-profile.name']    
    ai_darrp_support: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable support for FortiAIOps to retrieve Distributed Automatic Radio Resource Provisioning (DARRP) data through REST API calls (default = disable).")    
    darrp: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Distributed Automatic Radio Resource Provisioning (DARRP) to make sure the radio is always using the most optimal channel (default = disable).")    
    arrp_profile: str | None = Field(max_length=35, default=None, description="Distributed Automatic Radio Resource Provisioning (DARRP) profile name to assign to the radio.")  # datasource: ['wireless-controller.arrp-profile.name']    
    max_clients: int | None = Field(ge=0, le=4294967295, default=0, description="Maximum number of stations (STAs) or WiFi clients supported by the radio. Range depends on the hardware.")    
    max_distance: int | None = Field(ge=0, le=54000, default=0, description="Maximum expected distance between the AP and clients (0 - 54000 m, default = 0).")    
    vap_all: Literal["tunnel", "bridge", "manual"] | None = Field(default="tunnel", description="Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).")    
    vaps: list[WtpProfileRadio1Vaps] = Field(default_factory=list, description="Manually selected list of Virtual Access Points (VAPs).")    
    channel: list[WtpProfileRadio1Channel] = Field(default_factory=list, description="Selected list of wireless radio channels.")    
    call_admission_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable WiFi multimedia (WMM) call admission control to optimize WiFi bandwidth use for VoIP calls. New VoIP calls are only accepted if there is enough bandwidth available to support them.")    
    call_capacity: int | None = Field(ge=0, le=60, default=10, description="Maximum number of Voice over WLAN (VoWLAN) phones supported by the radio (0 - 60, default = 10).")    
    bandwidth_admission_control: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable WiFi multimedia (WMM) bandwidth admission control to optimize WiFi bandwidth use. A request to join the wireless network is only allowed if the access point has enough bandwidth to support it.")    
    bandwidth_capacity: int | None = Field(ge=1, le=600000, default=2000, description="Maximum bandwidth capacity allowed (1 - 600000 Kbps, default = 2000).")
class WtpProfilePlatform(BaseModel):
    """
    Child table model for platform.
    
    WTP, FortiAP, or AP platform.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    type_: WtpProfilePlatformTypeEnum | None = Field(default=WtpProfilePlatformTypeEnum.V_221E, serialization_alias="type", description="WTP, FortiAP or AP platform type. There are built-in WTP profiles for all supported FortiAP models. You can select a built-in profile and customize it or create a new profile.")    
    mode: Literal["single-5G", "dual-5G"] | None = Field(default="single-5G", description="Configure operation mode of 5G radios (default = single-5G).")    
    ddscan: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable use of one radio for dedicated full-band scanning to detect RF characterization and wireless threat management.")
class WtpProfileLedSchedules(BaseModel):
    """
    Child table model for led-schedules.
    
    Recurring firewall schedules for illuminating LEDs on the FortiAP. If led-state is enabled, LEDs will be visible when at least one of the schedules is valid. Separate multiple schedule names with a space.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Schedule name.")  # datasource: ['firewall.schedule.group.name', 'firewall.schedule.recurring.name', 'firewall.schedule.onetime.name']
class WtpProfileLbs(BaseModel):
    """
    Child table model for lbs.
    
    Set various location based service (LBS) options.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    ekahau_blink_mode: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Ekahau blink mode (now known as AiRISTA Flow) to track and locate WiFi tags (default = disable).")    
    ekahau_tag: str | None = Field(default="01:18:8e:00:00:00", description="WiFi frame MAC address or WiFi Tag.")    
    erc_server_ip: str | None = Field(default="0.0.0.0", description="IP address of Ekahau RTLS Controller (ERC).")    
    erc_server_port: int | None = Field(ge=1024, le=65535, default=8569, description="Ekahau RTLS Controller (ERC) UDP listening port.")    
    aeroscout: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable AeroScout Real Time Location Service (RTLS) support (default = disable).")    
    aeroscout_server_ip: str | None = Field(default="0.0.0.0", description="IP address of AeroScout server.")    
    aeroscout_server_port: int | None = Field(ge=1024, le=65535, default=0, description="AeroScout server UDP listening port.")    
    aeroscout_mu: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable AeroScout Mobile Unit (MU) support (default = disable).")    
    aeroscout_ap_mac: Literal["bssid", "board-mac"] | None = Field(default="bssid", description="Use BSSID or board MAC address as AP MAC address in AeroScout AP messages (default = bssid).")    
    aeroscout_mmu_report: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable compounded AeroScout tag and MU report (default = enable).")    
    aeroscout_mu_factor: int | None = Field(ge=0, le=4294967295, default=20, description="AeroScout MU mode dilution factor (default = 20).")    
    aeroscout_mu_timeout: int | None = Field(ge=0, le=65535, default=5, description="AeroScout MU mode timeout (0 - 65535 sec, default = 5).")    
    fortipresence: Literal["foreign", "both", "disable"] | None = Field(default="disable", description="Enable/disable FortiPresence to monitor the location and activity of WiFi clients even if they don't connect to this WiFi network (default = disable).")    
    fortipresence_server_addr_type: Literal["ipv4", "fqdn"] | None = Field(default="ipv4", description="FortiPresence server address type (default = ipv4).")    
    fortipresence_server: str | None = Field(default="0.0.0.0", description="IP address of FortiPresence server.")    
    fortipresence_server_fqdn: str | None = Field(max_length=255, default=None, description="FQDN of FortiPresence server.")    
    fortipresence_port: int | None = Field(ge=300, le=65535, default=3000, description="UDP listening port of FortiPresence server (default = 3000).")    
    fortipresence_secret: Any = Field(max_length=123, default=None, description="FortiPresence secret password (max. 16 characters).")    
    fortipresence_project: str | None = Field(max_length=16, default="fortipresence", description="FortiPresence project name (max. 16 characters, default = fortipresence).")    
    fortipresence_frequency: int | None = Field(ge=5, le=65535, default=30, description="FortiPresence report transmit frequency (5 - 65535 sec, default = 30).")    
    fortipresence_rogue: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable FortiPresence finding and reporting rogue APs.")    
    fortipresence_unassoc: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable FortiPresence finding and reporting unassociated stations.")    
    fortipresence_ble: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable FortiPresence finding and reporting BLE devices.")    
    station_locate: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable client station locating services for all clients, whether associated or not (default = disable).")    
    ble_rtls: Literal["none", "polestar", "evresys"] | None = Field(default="none", description="Set BLE Real Time Location Service (RTLS) support (default = none).")    
    ble_rtls_protocol: Literal["WSS"] | None = Field(default="WSS", description="Select the protocol to report Measurements, Advertising Data, or Location Data to Cloud Server (default = WSS).")    
    ble_rtls_server_fqdn: str | None = Field(max_length=255, default=None, description="FQDN of BLE Real Time Location Service (RTLS) Server.")    
    ble_rtls_server_path: str | None = Field(max_length=255, default=None, description="Path of BLE Real Time Location Service (RTLS) Server.")    
    ble_rtls_server_token: str | None = Field(max_length=31, default=None, description="Access Token of BLE Real Time Location Service (RTLS) Server.")    
    ble_rtls_server_port: int | None = Field(ge=1, le=65535, default=443, description="Port of BLE Real Time Location Service (RTLS) Server (default = 443).")    
    ble_rtls_accumulation_interval: int | None = Field(ge=1, le=60, default=2, description="Time that measurements should be accumulated in seconds (default = 2).")    
    ble_rtls_reporting_interval: int | None = Field(ge=1, le=600, default=2, description="Time between reporting accumulated measurements in seconds (default = 2).")    
    ble_rtls_asset_uuid_list1: str | None = Field(max_length=36, default=None, description="Tags and asset UUID list 1 to be reported (string in the format of 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX').")    
    ble_rtls_asset_uuid_list2: str | None = Field(max_length=36, default=None, description="Tags and asset UUID list 2 to be reported (string in the format of 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX').")    
    ble_rtls_asset_uuid_list3: str | None = Field(max_length=36, default=None, description="Tags and asset UUID list 3 to be reported (string in the format of 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX').")    
    ble_rtls_asset_uuid_list4: str | None = Field(max_length=36, default=None, description="Tags and asset UUID list 4 to be reported (string in the format of 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX').")    
    ble_rtls_asset_addrgrp_list: str | None = Field(max_length=79, default=None, description="Tags and asset addrgrp list to be reported.")  # datasource: ['firewall.addrgrp.name']
class WtpProfileLan(BaseModel):
    """
    Child table model for lan.
    
    WTP LAN port mapping.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    port_mode: WtpProfileLanPortModeEnum | None = Field(default=WtpProfileLanPortModeEnum.OFFLINE, description="LAN port mode.")    
    port_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port to SSID.")  # datasource: ['system.interface.name']    
    port1_mode: WtpProfileLanPort1ModeEnum | None = Field(default=WtpProfileLanPort1ModeEnum.OFFLINE, description="LAN port 1 mode.")    
    port1_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 1 to SSID.")  # datasource: ['system.interface.name']    
    port2_mode: WtpProfileLanPort2ModeEnum | None = Field(default=WtpProfileLanPort2ModeEnum.OFFLINE, description="LAN port 2 mode.")    
    port2_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 2 to SSID.")  # datasource: ['system.interface.name']    
    port3_mode: WtpProfileLanPort3ModeEnum | None = Field(default=WtpProfileLanPort3ModeEnum.OFFLINE, description="LAN port 3 mode.")    
    port3_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 3 to SSID.")  # datasource: ['system.interface.name']    
    port4_mode: WtpProfileLanPort4ModeEnum | None = Field(default=WtpProfileLanPort4ModeEnum.OFFLINE, description="LAN port 4 mode.")    
    port4_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 4 to SSID.")  # datasource: ['system.interface.name']    
    port5_mode: WtpProfileLanPort5ModeEnum | None = Field(default=WtpProfileLanPort5ModeEnum.OFFLINE, description="LAN port 5 mode.")    
    port5_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 5 to SSID.")  # datasource: ['system.interface.name']    
    port6_mode: WtpProfileLanPort6ModeEnum | None = Field(default=WtpProfileLanPort6ModeEnum.OFFLINE, description="LAN port 6 mode.")    
    port6_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 6 to SSID.")  # datasource: ['system.interface.name']    
    port7_mode: WtpProfileLanPort7ModeEnum | None = Field(default=WtpProfileLanPort7ModeEnum.OFFLINE, description="LAN port 7 mode.")    
    port7_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 7 to SSID.")  # datasource: ['system.interface.name']    
    port8_mode: WtpProfileLanPort8ModeEnum | None = Field(default=WtpProfileLanPort8ModeEnum.OFFLINE, description="LAN port 8 mode.")    
    port8_ssid: str | None = Field(max_length=15, default=None, description="Bridge LAN port 8 to SSID.")  # datasource: ['system.interface.name']    
    port_esl_mode: WtpProfileLanPortEslModeEnum | None = Field(default=WtpProfileLanPortEslModeEnum.OFFLINE, description="ESL port mode.")    
    port_esl_ssid: str | None = Field(max_length=15, default=None, description="Bridge ESL port to SSID.")  # datasource: ['system.interface.name']
class WtpProfileEslSesDongle(BaseModel):
    """
    Child table model for esl-ses-dongle.
    
    ESL SES-imagotag dongle configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    compliance_level: Literal["compliance-level-2"] | None = Field(default="compliance-level-2", description="Compliance levels for the ESL solution integration (default = compliance-level-2).")    
    scd_enable: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable ESL SES-imagotag Serial Communication Daemon (SCD) (default = disable).")    
    esl_channel: WtpProfileEslSesDongleEslChannelEnum | None = Field(default=WtpProfileEslSesDongleEslChannelEnum.V_127, description="ESL SES-imagotag dongle channel (default = 127).")    
    output_power: WtpProfileEslSesDongleOutputPowerEnum | None = Field(default=WtpProfileEslSesDongleOutputPowerEnum.A, description="ESL SES-imagotag dongle output power (default = A).")    
    apc_addr_type: Literal["fqdn", "ip"] | None = Field(default="fqdn", description="ESL SES-imagotag APC address type (default = fqdn).")    
    apc_fqdn: str | None = Field(max_length=63, default=None, description="FQDN of ESL SES-imagotag Access Point Controller (APC).")    
    apc_ip: str | None = Field(default="0.0.0.0", description="IP address of ESL SES-imagotag Access Point Controller (APC).")    
    apc_port: int | None = Field(ge=0, le=65535, default=0, description="Port of ESL SES-imagotag Access Point Controller (APC).")    
    coex_level: Literal["none"] | None = Field(default="none", description="ESL SES-imagotag dongle coexistence level (default = none).")    
    tls_cert_verification: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable TLS certificate verification (default = enable).")    
    tls_fqdn_verification: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable TLS FQDN verification (default = disable).")
class WtpProfileDenyMacList(BaseModel):
    """
    Child table model for deny-mac-list.
    
    List of MAC addresses that are denied access to this WTP, FortiAP, or AP.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    mac: str | None = Field(default="00:00:00:00:00:00", description="A WiFi device with this MAC address is denied access to this WTP, FortiAP or AP.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class WtpProfileControlMessageOffloadEnum(str, Enum):
    """Allowed values for control_message_offload field."""
    EBP_FRAME = "ebp-frame"
    AEROSCOUT_TAG = "aeroscout-tag"
    AP_LIST = "ap-list"
    STA_LIST = "sta-list"
    STA_CAP_LIST = "sta-cap-list"
    STATS = "stats"
    AEROSCOUT_MU = "aeroscout-mu"
    STA_HEALTH = "sta-health"
    SPECTRAL_ANALYSIS = "spectral-analysis"

class WtpProfileDtlsPolicyEnum(str, Enum):
    """Allowed values for dtls_policy field."""
    CLEAR_TEXT = "clear-text"
    DTLS_ENABLED = "dtls-enabled"
    IPSEC_VPN = "ipsec-vpn"
    IPSEC_SN_VPN = "ipsec-sn-vpn"

class WtpProfileApCountryEnum(str, Enum):
    """Allowed values for ap_country field."""
    __ = "--"
    AF = "AF"
    AL = "AL"
    DZ = "DZ"
    AS = "AS"
    AO = "AO"
    AR = "AR"
    AM = "AM"
    AU = "AU"
    AT = "AT"
    AZ = "AZ"
    BS = "BS"
    BH = "BH"
    BD = "BD"
    BB = "BB"
    BY = "BY"
    BE = "BE"
    BZ = "BZ"
    BJ = "BJ"
    BM = "BM"
    BT = "BT"
    BO = "BO"
    BA = "BA"
    BW = "BW"
    BR = "BR"
    BN = "BN"
    BG = "BG"
    BF = "BF"
    KH = "KH"
    CM = "CM"
    KY = "KY"
    CF = "CF"
    TD = "TD"
    CL = "CL"
    CN = "CN"
    CX = "CX"
    CO = "CO"
    CG = "CG"
    CD = "CD"
    CR = "CR"
    HR = "HR"
    CY = "CY"
    CZ = "CZ"
    DK = "DK"
    DJ = "DJ"
    DM = "DM"
    DO = "DO"
    EC = "EC"
    EG = "EG"
    SV = "SV"
    ET = "ET"
    EE = "EE"
    GF = "GF"
    PF = "PF"
    FO = "FO"
    FJ = "FJ"
    FI = "FI"
    FR = "FR"
    GA = "GA"
    GE = "GE"
    GM = "GM"
    DE = "DE"
    GH = "GH"
    GI = "GI"
    GR = "GR"
    GL = "GL"
    GD = "GD"
    GP = "GP"
    GU = "GU"
    GT = "GT"
    GY = "GY"
    HT = "HT"
    HN = "HN"
    HK = "HK"
    HU = "HU"
    IS = "IS"
    IN = "IN"
    ID = "ID"
    IQ = "IQ"
    IE = "IE"
    IM = "IM"
    IL = "IL"
    IT = "IT"
    CI = "CI"
    JM = "JM"
    JO = "JO"
    KZ = "KZ"
    KE = "KE"
    KR = "KR"
    KW = "KW"
    LA = "LA"
    LV = "LV"
    LB = "LB"
    LS = "LS"
    LR = "LR"
    LY = "LY"
    LI = "LI"
    LT = "LT"
    LU = "LU"
    MO = "MO"
    MK = "MK"
    MG = "MG"
    MW = "MW"
    MY = "MY"
    MV = "MV"
    ML = "ML"
    MT = "MT"
    MH = "MH"
    MQ = "MQ"
    MR = "MR"
    MU = "MU"
    YT = "YT"
    MX = "MX"
    FM = "FM"
    MD = "MD"
    MC = "MC"
    MN = "MN"
    MA = "MA"
    MZ = "MZ"
    MM = "MM"
    NA = "NA"
    NP = "NP"
    NL = "NL"
    AN = "AN"
    AW = "AW"
    NZ = "NZ"
    NI = "NI"
    NE = "NE"
    NG = "NG"
    NO = "NO"
    MP = "MP"
    OM = "OM"
    PK = "PK"
    PW = "PW"
    PA = "PA"
    PG = "PG"
    PY = "PY"
    PE = "PE"
    PH = "PH"
    PL = "PL"
    PT = "PT"
    PR = "PR"
    QA = "QA"
    RE = "RE"
    RO = "RO"
    RU = "RU"
    RW = "RW"
    BL = "BL"
    KN = "KN"
    LC = "LC"
    MF = "MF"
    PM = "PM"
    VC = "VC"
    SA = "SA"
    SN = "SN"
    RS = "RS"
    ME = "ME"
    SL = "SL"
    SG = "SG"
    SK = "SK"
    SI = "SI"
    SO = "SO"
    ZA = "ZA"
    ES = "ES"
    LK = "LK"
    SR = "SR"
    SZ = "SZ"
    SE = "SE"
    CH = "CH"
    TW = "TW"
    TZ = "TZ"
    TH = "TH"
    TL = "TL"
    TG = "TG"
    TT = "TT"
    TN = "TN"
    TR = "TR"
    TM = "TM"
    AE = "AE"
    TC = "TC"
    UG = "UG"
    UA = "UA"
    GB = "GB"
    US = "US"
    PS = "PS"
    UY = "UY"
    UZ = "UZ"
    VU = "VU"
    VE = "VE"
    VN = "VN"
    VI = "VI"
    WF = "WF"
    YE = "YE"
    ZM = "ZM"
    ZW = "ZW"
    JP = "JP"
    CA = "CA"

class WtpProfilePoeModeEnum(str, Enum):
    """Allowed values for poe_mode field."""
    AUTO = "auto"
    V_8023AF = "8023af"
    V_8023AT = "8023at"
    POWER_ADAPTER = "power-adapter"
    FULL = "full"
    HIGH = "high"
    LOW = "low"

class WtpProfileWanPortAuthMethodsEnum(str, Enum):
    """Allowed values for wan_port_auth_methods field."""
    ALL = "all"
    EAP_FAST = "EAP-FAST"
    EAP_TLS = "EAP-TLS"
    EAP_PEAP = "EAP-PEAP"

class WtpProfileApcfgAutoCertCryptoAlgoEnum(str, Enum):
    """Allowed values for apcfg_auto_cert_crypto_algo field."""
    RSA_1024 = "rsa-1024"
    RSA_1536 = "rsa-1536"
    RSA_2048 = "rsa-2048"
    RSA_4096 = "rsa-4096"
    EC_SECP256R1 = "ec-secp256r1"
    EC_SECP384R1 = "ec-secp384r1"
    EC_SECP521R1 = "ec-secp521r1"

class WtpProfileApcfgAutoCertScepKeysizeEnum(str, Enum):
    """Allowed values for apcfg_auto_cert_scep_keysize field."""
    V_1024 = "1024"
    V_1536 = "1536"
    V_2048 = "2048"
    V_4096 = "4096"


# ============================================================================
# Main Model
# ============================================================================

class WtpProfileModel(BaseModel):
    """
    Pydantic model for wireless_controller/wtp_profile configuration.
    
    Configure WTP profiles or FortiAP profiles that define radio settings for manageable FortiAP platforms.
    
    Validation Rules:        - name: max_length=35 pattern=        - comment: max_length=255 pattern=        - platform: pattern=        - control_message_offload: pattern=        - bonjour_profile: max_length=35 pattern=        - apcfg_profile: max_length=35 pattern=        - apcfg_mesh: pattern=        - apcfg_mesh_ap_type: pattern=        - apcfg_mesh_ssid: max_length=15 pattern=        - apcfg_mesh_eth_bridge: pattern=        - ble_profile: max_length=35 pattern=        - lw_profile: max_length=35 pattern=        - syslog_profile: max_length=35 pattern=        - wan_port_mode: pattern=        - lan: pattern=        - energy_efficient_ethernet: pattern=        - led_state: pattern=        - led_schedules: pattern=        - dtls_policy: pattern=        - dtls_in_kernel: pattern=        - max_clients: min=0 max=4294967295 pattern=        - handoff_rssi: min=20 max=30 pattern=        - handoff_sta_thresh: min=5 max=60 pattern=        - handoff_roaming: pattern=        - deny_mac_list: pattern=        - ap_country: pattern=        - ip_fragment_preventing: pattern=        - tun_mtu_uplink: min=576 max=1500 pattern=        - tun_mtu_downlink: min=576 max=1500 pattern=        - split_tunneling_acl_path: pattern=        - split_tunneling_acl_local_ap_subnet: pattern=        - split_tunneling_acl: pattern=        - allowaccess: pattern=        - login_passwd_change: pattern=        - login_passwd: max_length=128 pattern=        - lldp: pattern=        - poe_mode: pattern=        - usb_port: pattern=        - frequency_handoff: pattern=        - ap_handoff: pattern=        - default_mesh_root: pattern=        - radio_1: pattern=        - radio_2: pattern=        - radio_3: pattern=        - radio_4: pattern=        - lbs: pattern=        - ext_info_enable: pattern=        - indoor_outdoor_deployment: pattern=        - esl_ses_dongle: pattern=        - console_login: pattern=        - wan_port_auth: pattern=        - wan_port_auth_usrname: max_length=63 pattern=        - wan_port_auth_password: max_length=128 pattern=        - wan_port_auth_methods: pattern=        - wan_port_auth_macsec: pattern=        - apcfg_auto_cert: pattern=        - apcfg_auto_cert_enroll_protocol: pattern=        - apcfg_auto_cert_crypto_algo: pattern=        - apcfg_auto_cert_est_server: max_length=255 pattern=        - apcfg_auto_cert_est_ca_id: max_length=255 pattern=        - apcfg_auto_cert_est_http_username: max_length=63 pattern=        - apcfg_auto_cert_est_http_password: max_length=128 pattern=        - apcfg_auto_cert_est_subject: max_length=127 pattern=        - apcfg_auto_cert_est_subject_alt_name: max_length=127 pattern=        - apcfg_auto_cert_auto_regen_days: min=0 max=4294967295 pattern=        - apcfg_auto_cert_est_https_ca: max_length=79 pattern=        - apcfg_auto_cert_scep_keytype: pattern=        - apcfg_auto_cert_scep_keysize: pattern=        - apcfg_auto_cert_scep_ec_name: pattern=        - apcfg_auto_cert_scep_sub_fully_dn: max_length=255 pattern=        - apcfg_auto_cert_scep_url: max_length=255 pattern=        - apcfg_auto_cert_scep_password: max_length=128 pattern=        - apcfg_auto_cert_scep_ca_id: max_length=255 pattern=        - apcfg_auto_cert_scep_subject_alt_name: max_length=127 pattern=        - apcfg_auto_cert_scep_https_ca: max_length=79 pattern=        - unii_4_5ghz_band: pattern=        - admin_auth_tacacs: max_length=35 pattern=        - admin_restrict_local: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=35, default=None, description="WTP (or FortiAP or AP) profile name.")    
    comment: str | None = Field(max_length=255, default=None, description="Comment.")    
    platform: WtpProfilePlatform | None = Field(default=None, description="WTP, FortiAP, or AP platform.")    
    control_message_offload: list[WtpProfileControlMessageOffloadEnum] = Field(default_factory=list, description="Enable/disable CAPWAP control message data channel offload.")    
    bonjour_profile: str | None = Field(max_length=35, default=None, description="Bonjour profile name.")  # datasource: ['wireless-controller.bonjour-profile.name']    
    apcfg_profile: str | None = Field(max_length=35, default=None, description="AP local configuration profile name.")  # datasource: ['wireless-controller.apcfg-profile.name']    
    apcfg_mesh: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable AP local mesh configuration (default = disable).")    
    apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"] | None = Field(default="ethernet", description="Mesh AP Type (default = ethernet).")    
    apcfg_mesh_ssid: str | None = Field(max_length=15, default=None, description=" Mesh SSID (default = none).")  # datasource: ['wireless-controller.vap.name']    
    apcfg_mesh_eth_bridge: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable mesh ethernet bridge (default = disable).")    
    ble_profile: str | None = Field(max_length=35, default=None, description="Bluetooth Low Energy profile name.")  # datasource: ['wireless-controller.ble-profile.name']    
    lw_profile: str | None = Field(max_length=35, default=None, description="LoRaWAN profile name.")  # datasource: ['wireless-controller.lw-profile.name']    
    syslog_profile: str | None = Field(max_length=35, default=None, description="System log server configuration profile name.")  # datasource: ['wireless-controller.syslog-profile.name']    
    wan_port_mode: Literal["wan-lan", "wan-only"] | None = Field(default="wan-only", description="Enable/disable using a WAN port as a LAN port.")    
    lan: WtpProfileLan | None = Field(default=None, description="WTP LAN port mapping.")    
    energy_efficient_ethernet: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable use of energy efficient Ethernet on WTP.")    
    led_state: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable use of LEDs on WTP (default = enable).")    
    led_schedules: list[WtpProfileLedSchedules] = Field(default_factory=list, description="Recurring firewall schedules for illuminating LEDs on the FortiAP. If led-state is enabled, LEDs will be visible when at least one of the schedules is valid. Separate multiple schedule names with a space.")    
    dtls_policy: list[WtpProfileDtlsPolicyEnum] = Field(default_factory=list, description="WTP data channel DTLS policy (default = clear-text).")    
    dtls_in_kernel: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable data channel DTLS in kernel.")    
    max_clients: int | None = Field(ge=0, le=4294967295, default=0, description="Maximum number of stations (STAs) supported by the WTP (default = 0, meaning no client limitation).")    
    handoff_rssi: int | None = Field(ge=20, le=30, default=25, description="Minimum received signal strength indicator (RSSI) value for handoff (20 - 30, default = 25).")    
    handoff_sta_thresh: int | None = Field(ge=5, le=60, default=0, description="Threshold value for AP handoff.")    
    handoff_roaming: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable client load balancing during roaming to avoid roaming delay (default = enable).")    
    deny_mac_list: list[WtpProfileDenyMacList] = Field(default_factory=list, description="List of MAC addresses that are denied access to this WTP, FortiAP, or AP.")    
    ap_country: WtpProfileApCountryEnum | None = Field(default=WtpProfileApCountryEnum.__, description="Country in which this WTP, FortiAP, or AP will operate (default = NA, automatically use the country configured for the current VDOM).")    
    ip_fragment_preventing: list[Literal["tcp-mss-adjust", "icmp-unreachable"]] = Field(default_factory=list, description="Method(s) by which IP fragmentation is prevented for control and data packets through CAPWAP tunnel (default = tcp-mss-adjust).")    
    tun_mtu_uplink: int | None = Field(ge=576, le=1500, default=0, description="The maximum transmission unit (MTU) of uplink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).")    
    tun_mtu_downlink: int | None = Field(ge=576, le=1500, default=0, description="The MTU of downlink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).")    
    split_tunneling_acl_path: Literal["tunnel", "local"] | None = Field(default="local", description="Split tunneling ACL path is local/tunnel.")    
    split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable automatically adding local subnetwork of FortiAP to split-tunneling ACL (default = disable).")    
    split_tunneling_acl: list[WtpProfileSplitTunnelingAcl] = Field(default_factory=list, description="Split tunneling ACL filter list.")    
    allowaccess: list[Literal["https", "ssh", "snmp"]] = Field(default_factory=list, description="Control management access to the managed WTP, FortiAP, or AP. Separate entries with a space.")    
    login_passwd_change: Literal["yes", "default", "no"] | None = Field(default="no", description="Change or reset the administrator password of a managed WTP, FortiAP or AP (yes, default, or no, default = no).")    
    login_passwd: Any = Field(max_length=128, default=None, description="Set the managed WTP, FortiAP, or AP's administrator password.")    
    lldp: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable Link Layer Discovery Protocol (LLDP) for the WTP, FortiAP, or AP (default = enable).")    
    poe_mode: WtpProfilePoeModeEnum | None = Field(default=WtpProfilePoeModeEnum.AUTO, description="Set the WTP, FortiAP, or AP's PoE mode.")    
    usb_port: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable USB port of the WTP (default = enable).")    
    frequency_handoff: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable frequency handoff of clients to other channels (default = disable).")    
    ap_handoff: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable AP handoff of clients to other APs (default = disable).")    
    default_mesh_root: Literal["enable", "disable"] | None = Field(default="disable", description="Configure default mesh root SSID when it is not included by radio's SSID configuration.")    
    radio_1: WtpProfileRadio1 | None = Field(default=None, description="Configuration options for radio 1.")    
    radio_2: WtpProfileRadio2 | None = Field(default=None, description="Configuration options for radio 2.")    
    radio_3: WtpProfileRadio3 | None = Field(default=None, description="Configuration options for radio 3.")    
    radio_4: WtpProfileRadio4 | None = Field(default=None, description="Configuration options for radio 4.")    
    lbs: WtpProfileLbs | None = Field(default=None, description="Set various location based service (LBS) options.")    
    ext_info_enable: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable station/VAP/radio extension information.")    
    indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"] | None = Field(default="platform-determined", description="Set to allow indoor/outdoor-only channels under regulatory rules (default = platform-determined).")    
    esl_ses_dongle: WtpProfileEslSesDongle | None = Field(default=None, description="ESL SES-imagotag dongle configuration.")    
    console_login: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable FortiAP console login access (default = enable).")    
    wan_port_auth: Literal["none", "802.1x"] | None = Field(default="none", description="Set WAN port authentication mode (default = none).")    
    wan_port_auth_usrname: str | None = Field(max_length=63, default=None, description="Set WAN port 802.1x supplicant user name.")    
    wan_port_auth_password: Any = Field(max_length=128, default=None, description="Set WAN port 802.1x supplicant password.")    
    wan_port_auth_methods: WtpProfileWanPortAuthMethodsEnum | None = Field(default=WtpProfileWanPortAuthMethodsEnum.ALL, description="WAN port 802.1x supplicant EAP methods (default = all).")    
    wan_port_auth_macsec: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable WAN port 802.1x supplicant MACsec policy (default = disable).")    
    apcfg_auto_cert: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable AP local auto cert configuration (default = disable).")    
    apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"] | None = Field(default="none", description="Certificate enrollment protocol (default = none)")    
    apcfg_auto_cert_crypto_algo: WtpProfileApcfgAutoCertCryptoAlgoEnum | None = Field(default=WtpProfileApcfgAutoCertCryptoAlgoEnum.EC_SECP256R1, description="Cryptography algorithm: rsa-1024, rsa-1536, rsa-2048, rsa-4096, ec-secp256r1, ec-secp384r1, ec-secp521r1 (default = ec-secp256r1)")    
    apcfg_auto_cert_est_server: str | None = Field(max_length=255, default=None, description="Address and port for EST server (e.g. https://example.com:1234).")    
    apcfg_auto_cert_est_ca_id: str | None = Field(max_length=255, default=None, description="CA identifier of the CA server for signing via EST.")    
    apcfg_auto_cert_est_http_username: str | None = Field(max_length=63, default=None, description="HTTP Authentication username for signing via EST.")    
    apcfg_auto_cert_est_http_password: Any = Field(max_length=128, default=None, description="HTTP Authentication password for signing via EST.")    
    apcfg_auto_cert_est_subject: str | None = Field(max_length=127, default="CN=FortiAP,DC=local,DC=COM", description="Subject e.g. \"CN=User,DC=example,DC=COM\" (default = CN=FortiAP,DC=local,DC=COM)")    
    apcfg_auto_cert_est_subject_alt_name: str | None = Field(max_length=127, default=None, description="Subject alternative name (optional, e.g. \"DNS:dns1.com,IP:192.168.1.99\")")    
    apcfg_auto_cert_auto_regen_days: int | None = Field(ge=0, le=4294967295, default=30, description="Number of days to wait before expiry of an updated local certificate is requested (0 = disabled) (default = 30).")    
    apcfg_auto_cert_est_https_ca: str | None = Field(max_length=79, default=None, description="PEM format https CA Certificate.")  # datasource: ['vpn.certificate.ca.name']    
    apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"] | None = Field(default="rsa", description="Key type (default = rsa)")    
    apcfg_auto_cert_scep_keysize: WtpProfileApcfgAutoCertScepKeysizeEnum | None = Field(default=WtpProfileApcfgAutoCertScepKeysizeEnum.V_2048, description="Key size: 1024, 1536, 2048, 4096 (default 2048).")    
    apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"] | None = Field(default="secp256r1", description="Elliptic curve name: secp256r1, secp384r1 and secp521r1. (default secp256r1).")    
    apcfg_auto_cert_scep_sub_fully_dn: str | None = Field(max_length=255, default=None, description="Full DN of the subject (e.g C=US,ST=CA,L=Sunnyvale,O=Fortinet,OU=Dep1,emailAddress=test@example.com). There should be no space in between the attributes. Supported DN attributes (case-sensitive) are:C,ST,L,O,OU,emailAddress. The CN defaults to the device’s SN and cannot be changed.")    
    apcfg_auto_cert_scep_url: str | None = Field(max_length=255, default=None, description="SCEP server URL.")    
    apcfg_auto_cert_scep_password: Any = Field(max_length=128, default=None, description="SCEP server challenge password for auto-regeneration.")    
    apcfg_auto_cert_scep_ca_id: str | None = Field(max_length=255, default=None, description="CA identifier of the CA server for signing via SCEP.")    
    apcfg_auto_cert_scep_subject_alt_name: str | None = Field(max_length=127, default=None, description="Subject alternative name (optional, e.g. \"DNS:dns1.com,IP:192.168.1.99\")")    
    apcfg_auto_cert_scep_https_ca: str | None = Field(max_length=79, default=None, description="PEM format https CA Certificate.")  # datasource: ['vpn.certificate.ca.name']    
    unii_4_5ghz_band: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable UNII-4 5Ghz band channels (default = disable).")    
    admin_auth_tacacs: str | None = Field(max_length=35, default=None, description="Remote authentication server for admin user.")  # datasource: ['user.tacacs+.name']    
    admin_restrict_local: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable local admin authentication restriction when remote authenticator is up and running (default = disable).")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
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
    @field_validator('apcfg_mesh_ssid')
    @classmethod
    def validate_apcfg_mesh_ssid(cls, v: Any) -> Any:
        """
        Validate apcfg_mesh_ssid field.
        
        Datasource: ['wireless-controller.vap.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('ble_profile')
    @classmethod
    def validate_ble_profile(cls, v: Any) -> Any:
        """
        Validate ble_profile field.
        
        Datasource: ['wireless-controller.ble-profile.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('lw_profile')
    @classmethod
    def validate_lw_profile(cls, v: Any) -> Any:
        """
        Validate lw_profile field.
        
        Datasource: ['wireless-controller.lw-profile.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('syslog_profile')
    @classmethod
    def validate_syslog_profile(cls, v: Any) -> Any:
        """
        Validate syslog_profile field.
        
        Datasource: ['wireless-controller.syslog-profile.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('apcfg_auto_cert_est_https_ca')
    @classmethod
    def validate_apcfg_auto_cert_est_https_ca(cls, v: Any) -> Any:
        """
        Validate apcfg_auto_cert_est_https_ca field.
        
        Datasource: ['vpn.certificate.ca.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('apcfg_auto_cert_scep_https_ca')
    @classmethod
    def validate_apcfg_auto_cert_scep_https_ca(cls, v: Any) -> Any:
        """
        Validate apcfg_auto_cert_scep_https_ca field.
        
        Datasource: ['vpn.certificate.ca.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('admin_auth_tacacs')
    @classmethod
    def validate_admin_auth_tacacs(cls, v: Any) -> Any:
        """
        Validate admin_auth_tacacs field.
        
        Datasource: ['user.tacacs+.name']
        
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "WtpProfileModel":
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
            >>> policy = WtpProfileModel(
            ...     bonjour_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_bonjour_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
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
            >>> policy = WtpProfileModel(
            ...     apcfg_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_apcfg_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
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
    async def validate_apcfg_mesh_ssid_references(self, client: Any) -> list[str]:
        """
        Validate apcfg_mesh_ssid references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/vap        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     apcfg_mesh_ssid="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_apcfg_mesh_ssid_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "apcfg_mesh_ssid", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.wireless_controller.vap.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Apcfg-Mesh-Ssid '{value}' not found in "
                "wireless-controller/vap"
            )        
        return errors    
    async def validate_ble_profile_references(self, client: Any) -> list[str]:
        """
        Validate ble_profile references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/ble-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     ble_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_ble_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "ble_profile", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.wireless_controller.ble_profile.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Ble-Profile '{value}' not found in "
                "wireless-controller/ble-profile"
            )        
        return errors    
    async def validate_lw_profile_references(self, client: Any) -> list[str]:
        """
        Validate lw_profile references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/lw-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     lw_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_lw_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "lw_profile", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.wireless_controller.lw_profile.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Lw-Profile '{value}' not found in "
                "wireless-controller/lw-profile"
            )        
        return errors    
    async def validate_syslog_profile_references(self, client: Any) -> list[str]:
        """
        Validate syslog_profile references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/syslog-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     syslog_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_syslog_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "syslog_profile", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.wireless_controller.syslog_profile.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Syslog-Profile '{value}' not found in "
                "wireless-controller/syslog-profile"
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
            >>> policy = WtpProfileModel(
            ...     lan=[{"port-esl-ssid": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_lan_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
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
    async def validate_led_schedules_references(self, client: Any) -> list[str]:
        """
        Validate led_schedules references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/schedule/group        - firewall/schedule/recurring        - firewall/schedule/onetime        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     led_schedules=[{"name": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_led_schedules_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "led_schedules", [])
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
            if await client.api.cmdb.firewall.schedule.group.exists(value):
                found = True
            elif await client.api.cmdb.firewall.schedule.recurring.exists(value):
                found = True
            elif await client.api.cmdb.firewall.schedule.onetime.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Led-Schedules '{value}' not found in "
                    "firewall/schedule/group or firewall/schedule/recurring or firewall/schedule/onetime"
                )        
        return errors    
    async def validate_radio_1_references(self, client: Any) -> list[str]:
        """
        Validate radio_1 references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/arrp-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     radio_1=[{"arrp-profile": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_radio_1_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "radio_1", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("arrp-profile")
            else:
                value = getattr(item, "arrp-profile", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.wireless_controller.arrp_profile.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Radio-1 '{value}' not found in "
                    "wireless-controller/arrp-profile"
                )        
        return errors    
    async def validate_radio_2_references(self, client: Any) -> list[str]:
        """
        Validate radio_2 references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/arrp-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     radio_2=[{"arrp-profile": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_radio_2_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "radio_2", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("arrp-profile")
            else:
                value = getattr(item, "arrp-profile", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.wireless_controller.arrp_profile.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Radio-2 '{value}' not found in "
                    "wireless-controller/arrp-profile"
                )        
        return errors    
    async def validate_radio_3_references(self, client: Any) -> list[str]:
        """
        Validate radio_3 references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/arrp-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     radio_3=[{"arrp-profile": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_radio_3_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "radio_3", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("arrp-profile")
            else:
                value = getattr(item, "arrp-profile", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.wireless_controller.arrp_profile.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Radio-3 '{value}' not found in "
                    "wireless-controller/arrp-profile"
                )        
        return errors    
    async def validate_radio_4_references(self, client: Any) -> list[str]:
        """
        Validate radio_4 references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - wireless-controller/arrp-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     radio_4=[{"arrp-profile": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_radio_4_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "radio_4", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("arrp-profile")
            else:
                value = getattr(item, "arrp-profile", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.wireless_controller.arrp_profile.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Radio-4 '{value}' not found in "
                    "wireless-controller/arrp-profile"
                )        
        return errors    
    async def validate_lbs_references(self, client: Any) -> list[str]:
        """
        Validate lbs references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/addrgrp        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     lbs=[{"ble-rtls-asset-addrgrp-list": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_lbs_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "lbs", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("ble-rtls-asset-addrgrp-list")
            else:
                value = getattr(item, "ble-rtls-asset-addrgrp-list", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.firewall.addrgrp.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Lbs '{value}' not found in "
                    "firewall/addrgrp"
                )        
        return errors    
    async def validate_apcfg_auto_cert_est_https_ca_references(self, client: Any) -> list[str]:
        """
        Validate apcfg_auto_cert_est_https_ca references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - vpn/certificate/ca        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     apcfg_auto_cert_est_https_ca="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_apcfg_auto_cert_est_https_ca_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "apcfg_auto_cert_est_https_ca", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.vpn.certificate.ca.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Apcfg-Auto-Cert-Est-Https-Ca '{value}' not found in "
                "vpn/certificate/ca"
            )        
        return errors    
    async def validate_apcfg_auto_cert_scep_https_ca_references(self, client: Any) -> list[str]:
        """
        Validate apcfg_auto_cert_scep_https_ca references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - vpn/certificate/ca        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     apcfg_auto_cert_scep_https_ca="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_apcfg_auto_cert_scep_https_ca_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "apcfg_auto_cert_scep_https_ca", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.vpn.certificate.ca.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Apcfg-Auto-Cert-Scep-Https-Ca '{value}' not found in "
                "vpn/certificate/ca"
            )        
        return errors    
    async def validate_admin_auth_tacacs_plus__references(self, client: Any) -> list[str]:
        """
        Validate admin_auth_tacacs_plus_ references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - user/tacacs+        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = WtpProfileModel(
            ...     admin_auth_tacacs_plus_="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_admin_auth_tacacs_plus__references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.wireless_controller.wtp_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "admin_auth_tacacs_plus_", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.user.tacacs_plus_.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Admin-Auth-Tacacs+ '{value}' not found in "
                "user/tacacs+"
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
        
        errors = await self.validate_bonjour_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_apcfg_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_apcfg_mesh_ssid_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_ble_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_lw_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_syslog_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_lan_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_led_schedules_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_radio_1_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_radio_2_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_radio_3_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_radio_4_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_lbs_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_apcfg_auto_cert_est_https_ca_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_apcfg_auto_cert_scep_https_ca_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_admin_auth_tacacs_plus__references(client)
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
    "WtpProfileModel",    "WtpProfilePlatform",    "WtpProfileLan",    "WtpProfileLedSchedules",    "WtpProfileDenyMacList",    "WtpProfileSplitTunnelingAcl",    "WtpProfileRadio1",    "WtpProfileRadio1.Vaps",    "WtpProfileRadio1.Channel",    "WtpProfileRadio2",    "WtpProfileRadio2.Vaps",    "WtpProfileRadio2.Channel",    "WtpProfileRadio3",    "WtpProfileRadio3.Vaps",    "WtpProfileRadio3.Channel",    "WtpProfileRadio4",    "WtpProfileRadio4.Vaps",    "WtpProfileRadio4.Channel",    "WtpProfileLbs",    "WtpProfileEslSesDongle",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:38.752214Z
# ============================================================================