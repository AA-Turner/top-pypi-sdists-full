"""
Pydantic Models for CMDB - extension_controller/extender_profile

Runtime validation models for extension_controller/extender_profile configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class ExtenderProfileWifiRadio2OperatingStandardEnum(str, Enum):
    """Allowed values for operating_standard field in wifi.radio-2."""
    AUTO = "auto"
    V_11A_N_AC_AX = "11A-N-AC-AX"
    V_11A_N_AC = "11A-N-AC"
    V_11A_N = "11A-N"
    V_11A = "11A"
    V_11N_AC_AX = "11N-AC-AX"
    V_11AC_AX = "11AC-AX"
    V_11AC = "11AC"
    V_11N_AC = "11N-AC"
    V_11B_G_N_AX = "11B-G-N-AX"
    V_11B_G_N = "11B-G-N"
    V_11B_G = "11B-G"
    V_11B = "11B"
    V_11G_N_AX = "11G-N-AX"
    V_11N_AX = "11N-AX"
    V_11AX = "11AX"
    V_11G_N = "11G-N"
    V_11N = "11N"
    V_11G = "11G"

class ExtenderProfileWifiRadio2ChannelEnum(str, Enum):
    """Allowed values for channel field in wifi.radio-2."""
    CH36 = "CH36"
    CH40 = "CH40"
    CH44 = "CH44"
    CH48 = "CH48"
    CH52 = "CH52"
    CH56 = "CH56"
    CH60 = "CH60"
    CH64 = "CH64"
    CH100 = "CH100"
    CH104 = "CH104"
    CH108 = "CH108"
    CH112 = "CH112"
    CH116 = "CH116"
    CH120 = "CH120"
    CH124 = "CH124"
    CH128 = "CH128"
    CH132 = "CH132"
    CH136 = "CH136"
    CH140 = "CH140"
    CH144 = "CH144"
    CH149 = "CH149"
    CH153 = "CH153"
    CH157 = "CH157"
    CH161 = "CH161"
    CH165 = "CH165"

class ExtenderProfileWifiRadio2BandwidthEnum(str, Enum):
    """Allowed values for bandwidth field in wifi.radio-2."""
    AUTO = "auto"
    V_20MHZ = "20MHz"
    V_40MHZ = "40MHz"
    V_80MHZ = "80MHz"

class ExtenderProfileWifiRadio1OperatingStandardEnum(str, Enum):
    """Allowed values for operating_standard field in wifi.radio-1."""
    AUTO = "auto"
    V_11A_N_AC_AX = "11A-N-AC-AX"
    V_11A_N_AC = "11A-N-AC"
    V_11A_N = "11A-N"
    V_11A = "11A"
    V_11N_AC_AX = "11N-AC-AX"
    V_11AC_AX = "11AC-AX"
    V_11AC = "11AC"
    V_11N_AC = "11N-AC"
    V_11B_G_N_AX = "11B-G-N-AX"
    V_11B_G_N = "11B-G-N"
    V_11B_G = "11B-G"
    V_11B = "11B"
    V_11G_N_AX = "11G-N-AX"
    V_11N_AX = "11N-AX"
    V_11AX = "11AX"
    V_11G_N = "11G-N"
    V_11N = "11N"
    V_11G = "11G"

class ExtenderProfileWifiRadio1ChannelEnum(str, Enum):
    """Allowed values for channel field in wifi.radio-1."""
    CH1 = "CH1"
    CH2 = "CH2"
    CH3 = "CH3"
    CH4 = "CH4"
    CH5 = "CH5"
    CH6 = "CH6"
    CH7 = "CH7"
    CH8 = "CH8"
    CH9 = "CH9"
    CH10 = "CH10"
    CH11 = "CH11"

class ExtenderProfileWifiRadio1BandwidthEnum(str, Enum):
    """Allowed values for bandwidth field in wifi.radio-1."""
    AUTO = "auto"
    V_20MHZ = "20MHz"
    V_40MHZ = "40MHz"
    V_80MHZ = "80MHz"

class ExtenderProfileWifiCountryEnum(str, Enum):
    """Allowed values for country field in wifi."""
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

class ExtenderProfileLanExtensionDownlinksPortEnum(str, Enum):
    """Allowed values for port field in lan-extension.downlinks."""
    PORT1 = "port1"
    PORT2 = "port2"
    PORT3 = "port3"
    PORT4 = "port4"
    PORT5 = "port5"
    LAN1 = "lan1"
    LAN2 = "lan2"
    LAN = "lan"

class ExtenderProfileLanExtensionBackhaulPortEnum(str, Enum):
    """Allowed values for port field in lan-extension.backhaul."""
    WAN = "wan"
    LTE1 = "lte1"
    LTE2 = "lte2"
    PORT1 = "port1"
    PORT2 = "port2"
    PORT3 = "port3"
    PORT4 = "port4"
    PORT5 = "port5"
    SFP = "sfp"

class ExtenderProfileCellularSmsNotificationReceiverAlertEnum(str, Enum):
    """Allowed values for alert field in cellular.sms-notification.receiver."""
    SYSTEM_REBOOT = "system-reboot"
    DATA_EXHAUSTED = "data-exhausted"
    SESSION_DISCONNECT = "session-disconnect"
    LOW_SIGNAL_STRENGTH = "low-signal-strength"
    MODE_SWITCH = "mode-switch"
    OS_IMAGE_FALLBACK = "os-image-fallback"
    FGT_BACKUP_MODE_SWITCH = "fgt-backup-mode-switch"

class ExtenderProfileCellularModem2DefaultSimEnum(str, Enum):
    """Allowed values for default_sim field in cellular.modem2."""
    SIM1 = "sim1"
    SIM2 = "sim2"
    CARRIER = "carrier"
    COST = "cost"

class ExtenderProfileCellularModem1DefaultSimEnum(str, Enum):
    """Allowed values for default_sim field in cellular.modem1."""
    SIM1 = "sim1"
    SIM2 = "sim2"
    CARRIER = "carrier"
    COST = "cost"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ExtenderProfileWifiRadio2LocalVaps(BaseModel):
    """
    Child table model for wifi.radio-2.local-vaps.
    
    Wi-Fi local VAP. Select up to three VAPs.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Wi-Fi local VAP name.")  # datasource: ['extension-controller.extender-vap.name']
class ExtenderProfileWifiRadio2(BaseModel):
    """
    Child table model for wifi.radio-2.
    
    Radio-2 config for Wi-Fi 5GHz
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    mode: Literal["AP", "Client"] | None = Field(default="AP", description="Wi-Fi radio mode AP(LAN mode) / Client(WAN mode).")    
    band: Literal["5GHz"] | None = Field(default="5GHz", description="Wi-Fi band selection 2.4GHz / 5GHz.")    
    status: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable Wi-Fi radio.")    
    operating_standard: ExtenderProfileWifiRadio2OperatingStandardEnum | None = Field(default=ExtenderProfileWifiRadio2OperatingStandardEnum.AUTO, description="Wi-Fi operating standard.")    
    guard_interval: Literal["auto", "400ns", "800ns"] | None = Field(default="auto", description="Wi-Fi guard interval.")    
    channel: list[ExtenderProfileWifiRadio2ChannelEnum] = Field(default_factory=list, description="Wi-Fi channels.")    
    bandwidth: ExtenderProfileWifiRadio2BandwidthEnum | None = Field(default=ExtenderProfileWifiRadio2BandwidthEnum.AUTO, description="Wi-Fi channel bandwidth.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Wi-Fi power level in percent (0 - 100, 0 = auto, default = 100).")    
    beacon_interval: int | None = Field(ge=100, le=3500, default=100, description="Wi-Fi beacon interval in miliseconds (100 - 3500, default = 100).")    
    _80211d: Literal["disable", "enable"] | None = Field(default="enable", serialization_alias="80211d", description="Enable/disable Wi-Fi 802.11d.")    
    max_clients: int | None = Field(ge=0, le=512, default=0, description="Maximum number of Wi-Fi radio clients (0 - 512, 0 = unlimited, default = 0).")    
    extension_channel: Literal["auto", "higher", "lower"] | None = Field(default="auto", description="Wi-Fi extension channel.")    
    bss_color_mode: Literal["auto", "static"] | None = Field(default="auto", description="Wi-Fi 802.11AX BSS color mode.")    
    bss_color: int | None = Field(ge=0, le=63, default=0, description="Wi-Fi 802.11AX BSS color value (0 - 63, 0 = disable, default = 0).")    
    lan_ext_vap: str | None = Field(max_length=31, default=None, description="Wi-Fi LAN-Extention VAP. Select only one VAP.")  # datasource: ['extension-controller.extender-vap.name']    
    local_vaps: list[ExtenderProfileWifiRadio2LocalVaps] = Field(default_factory=list, description="Wi-Fi local VAP. Select up to three VAPs.")
class ExtenderProfileWifiRadio1LocalVaps(BaseModel):
    """
    Child table model for wifi.radio-1.local-vaps.
    
    Wi-Fi local VAP. Select up to three VAPs.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Wi-Fi local VAP name.")  # datasource: ['extension-controller.extender-vap.name']
class ExtenderProfileWifiRadio1(BaseModel):
    """
    Child table model for wifi.radio-1.
    
    Radio-1 config for Wi-Fi 2.4GHz
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    mode: Literal["AP", "Client"] | None = Field(default="AP", description="Wi-Fi radio mode AP(LAN mode) / Client(WAN mode).")    
    band: Literal["2.4GHz"] | None = Field(default="2.4GHz", description="Wi-Fi band selection 2.4GHz / 5GHz.")    
    status: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable Wi-Fi radio.")    
    operating_standard: ExtenderProfileWifiRadio1OperatingStandardEnum | None = Field(default=ExtenderProfileWifiRadio1OperatingStandardEnum.AUTO, description="Wi-Fi operating standard.")    
    guard_interval: Literal["auto", "400ns", "800ns"] | None = Field(default="auto", description="Wi-Fi guard interval.")    
    channel: list[ExtenderProfileWifiRadio1ChannelEnum] = Field(default_factory=list, description="Wi-Fi channels.")    
    bandwidth: ExtenderProfileWifiRadio1BandwidthEnum | None = Field(default=ExtenderProfileWifiRadio1BandwidthEnum.AUTO, description="Wi-Fi channel bandwidth.")    
    power_level: int | None = Field(ge=0, le=100, default=100, description="Wi-Fi power level in percent (0 - 100, 0 = auto, default = 100).")    
    beacon_interval: int | None = Field(ge=100, le=3500, default=100, description="Wi-Fi beacon interval in miliseconds (100 - 3500, default = 100).")    
    _80211d: Literal["disable", "enable"] | None = Field(default="enable", serialization_alias="80211d", description="Enable/disable Wi-Fi 802.11d.")    
    max_clients: int | None = Field(ge=0, le=512, default=0, description="Maximum number of Wi-Fi radio clients (0 - 512, 0 = unlimited, default = 0).")    
    extension_channel: Literal["auto", "higher", "lower"] | None = Field(default="auto", description="Wi-Fi extension channel.")    
    bss_color_mode: Literal["auto", "static"] | None = Field(default="auto", description="Wi-Fi 802.11AX BSS color mode.")    
    bss_color: int | None = Field(ge=0, le=63, default=0, description="Wi-Fi 802.11AX BSS color value (0 - 63, 0 = disable, default = 0).")    
    lan_ext_vap: str | None = Field(max_length=31, default=None, description="Wi-Fi LAN-Extention VAP. Select only one VAP.")  # datasource: ['extension-controller.extender-vap.name']    
    local_vaps: list[ExtenderProfileWifiRadio1LocalVaps] = Field(default_factory=list, description="Wi-Fi local VAP. Select up to three VAPs.")
class ExtenderProfileWifi(BaseModel):
    """
    Child table model for wifi.
    
    FortiExtender Wi-Fi configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    country: ExtenderProfileWifiCountryEnum | None = Field(default=ExtenderProfileWifiCountryEnum.__, description="Country in which this FEX will operate (default = NA).")    
    radio_1: ExtenderProfileWifiRadio1 | None = Field(default=None, description="Radio-1 config for Wi-Fi 2.4GHz")    
    radio_2: ExtenderProfileWifiRadio2 | None = Field(default=None, description="Radio-2 config for Wi-Fi 5GHz")
class ExtenderProfileLanExtensionTrafficSplitServices(BaseModel):
    """
    Child table model for lan-extension.traffic-split-services.
    
    Config FortiExtender traffic split interface for LAN extension.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=31, default=None, description="FortiExtender LAN extension tunnel split entry name.")    
    vsdb: Literal["disable", "enable"] | None = Field(default="disable", description="Set video streaming traffic goes through local WAN [enable/disable].")    
    address: str = Field(max_length=79, description="Address selection.")  # datasource: ['firewall.address.name']    
    service: str = Field(max_length=79, default="ALL", description="Service selection.")  # datasource: ['firewall.service.custom.name']
class ExtenderProfileLanExtensionDownlinksVids(BaseModel):
    """
    Child table model for lan-extension.downlinks.vids.
    
    FortiExtender LAN extension downlink VIDs.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vid: int | None = Field(ge=1, le=4089, default=0, description="Please enter VID numbers (1 - 4089) with space separated. Up to 50 VIDs are accepted.")
class ExtenderProfileLanExtensionDownlinks(BaseModel):
    """
    Child table model for lan-extension.downlinks.
    
    Config FortiExtender downlink interface for LAN extension.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=31, default=None, description="FortiExtender LAN extension downlink config entry name.")    
    type_: Literal["port", "vap"] = Field(default="port", serialization_alias="type", description="FortiExtender LAN extension downlink type [port/vap].")    
    port: ExtenderProfileLanExtensionDownlinksPortEnum = Field(description="FortiExtender LAN extension downlink port.")    
    vap: str = Field(max_length=31, description="FortiExtender LAN extension downlink vap.")  # datasource: ['extension-controller.extender-vap.name']    
    pvid: int = Field(ge=1, le=4089, default=1, description="FortiExtender LAN extension downlink PVID (1 - 4089).")    
    vids: list[ExtenderProfileLanExtensionDownlinksVids] = Field(default_factory=list, description="FortiExtender LAN extension downlink VIDs.")
class ExtenderProfileLanExtensionBackhaul(BaseModel):
    """
    Child table model for lan-extension.backhaul.
    
    LAN extension backhaul tunnel configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=31, default=None, description="FortiExtender LAN extension backhaul name.")    
    port: ExtenderProfileLanExtensionBackhaulPortEnum = Field(default=ExtenderProfileLanExtensionBackhaulPortEnum.WAN, description="FortiExtender uplink port.")    
    role: Literal["primary", "secondary"] = Field(default="primary", description="FortiExtender uplink port.")    
    weight: int = Field(ge=1, le=256, default=1, description="WRR weight parameter.")    
    health_check_interval: int | None = Field(ge=1, le=3600, default=5, description="Health monitoring interval in seconds (1 - 3600, default = 5).")    
    health_check_probe_cnt: int | None = Field(ge=1, le=10, default=1, description="Number of health monitoring probes to send within an interval (1 - 10, default = 1).")    
    health_check_probe_tm: int | None = Field(ge=1, le=10, default=2, description="Health monitoring probe timeout in seconds (1 - 10, default = 2).")    
    health_check_fail_cnt: int | None = Field(ge=1, le=10, default=5, description="Number of failures before the link is considered dead (1 - 10, default = 5).")    
    health_check_recovery_cnt: int | None = Field(ge=1, le=10, default=5, description="Number of successful checks before the link is considered alive (1 - 10, default = 5).")
class ExtenderProfileLanExtension(BaseModel):
    """
    Child table model for lan-extension.
    
    FortiExtender LAN extension configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    link_loadbalance: Literal["activebackup", "loadbalance"] = Field(default="activebackup", description="LAN extension link load balance strategy.")    
    ipsec_tunnel: str | None = Field(max_length=15, default=None, description="IPsec tunnel name.")    
    backhaul_interface: str | None = Field(max_length=15, default=None, description="IPsec phase1 interface.")  # datasource: ['system.interface.name']    
    backhaul_ip: str | None = Field(max_length=63, default=None, description="IPsec phase1 IPv4/FQDN. Used to specify the external IP/FQDN when the FortiGate unit is behind a NAT device.")    
    backhaul: list[ExtenderProfileLanExtensionBackhaul] = Field(default_factory=list, description="LAN extension backhaul tunnel configuration.")    
    downlinks: list[ExtenderProfileLanExtensionDownlinks] = Field(default_factory=list, description="Config FortiExtender downlink interface for LAN extension.")    
    traffic_split_services: list[ExtenderProfileLanExtensionTrafficSplitServices] = Field(default_factory=list, description="Config FortiExtender traffic split interface for LAN extension.")
class ExtenderProfileCellularSmsNotificationReceiver(BaseModel):
    """
    Child table model for cellular.sms-notification.receiver.
    
    SMS notification receiver list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=31, default=None, description="FortiExtender SMS notification receiver name.")    
    status: Literal["disable", "enable"] | None = Field(default="disable", description="SMS notification receiver status.")    
    phone_number: str = Field(max_length=31, description="Receiver phone number. Format: [+][country code][area code][local phone number]. For example, +16501234567.")    
    alert: list[ExtenderProfileCellularSmsNotificationReceiverAlertEnum] = Field(default_factory=list, description="Alert multi-options.")
class ExtenderProfileCellularSmsNotificationAlert(BaseModel):
    """
    Child table model for cellular.sms-notification.alert.
    
    SMS alert list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    system_reboot: str = Field(max_length=63, default="system will reboot", description="Display string when system rebooted.")    
    data_exhausted: str = Field(max_length=63, default="data plan is exhausted", description="Display string when data exhausted.")    
    session_disconnect: str = Field(max_length=63, default="LTE data session is disconnected", description="Display string when session disconnected.")    
    low_signal_strength: str = Field(max_length=63, default="LTE signal strength is too low", description="Display string when signal strength is low.")    
    os_image_fallback: str = Field(max_length=63, default="system start to fallback OS image", description="Display string when falling back to a previous OS image.")    
    mode_switch: str = Field(max_length=63, default="system networking mode switched", description="Display string when mode is switched.")    
    fgt_backup_mode_switch: str = Field(max_length=63, default="FortiGate backup work mode switched", description="Display string when FortiGate backup mode switched.")
class ExtenderProfileCellularSmsNotification(BaseModel):
    """
    Child table model for cellular.sms-notification.
    
    FortiExtender cellular SMS notification configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["disable", "enable"] = Field(default="disable", description="FortiExtender SMS notification status.")    
    alert: ExtenderProfileCellularSmsNotificationAlert | None = Field(default=None, description="SMS alert list.")    
    receiver: list[ExtenderProfileCellularSmsNotificationReceiver] = Field(default_factory=list, description="SMS notification receiver list.")
class ExtenderProfileCellularModem2AutoSwitch(BaseModel):
    """
    Child table model for cellular.modem2.auto-switch.
    
    FortiExtender auto switch configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    disconnect: Literal["disable", "enable"] = Field(default="disable", description="Auto switch by disconnect.")    
    disconnect_threshold: int = Field(ge=1, le=100, default=3, description="Automatically switch based on disconnect threshold.")    
    disconnect_period: int = Field(ge=600, le=18000, default=600, description="Automatically switch based on disconnect period.")    
    signal: Literal["disable", "enable"] = Field(default="disable", description="Automatically switch based on signal strength.")    
    dataplan: Literal["disable", "enable"] = Field(default="disable", description="Automatically switch based on data usage.")    
    switch_back: list[Literal["time", "timer"]] = Field(default_factory=list, description="Auto switch with switch back multi-options.")    
    switch_back_time: str | None = Field(max_length=31, default="00:01", description="Automatically switch over to preferred SIM/carrier at a specified time in UTC (HH:MM).")    
    switch_back_timer: int | None = Field(ge=3600, le=2147483647, default=86400, description="Automatically switch over to preferred SIM/carrier after the given time (3600 - 2147483647 sec).")
class ExtenderProfileCellularModem2(BaseModel):
    """
    Child table model for cellular.modem2.
    
    Configuration options for modem 2.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    redundant_mode: Literal["disable", "enable"] = Field(default="disable", description="FortiExtender mode.")    
    redundant_intf: str = Field(max_length=15, description="Redundant interface.")    
    conn_status: int | None = Field(ge=0, le=4294967295, default=0, description="Connection status.")    
    default_sim: ExtenderProfileCellularModem2DefaultSimEnum = Field(default=ExtenderProfileCellularModem2DefaultSimEnum.SIM1, description="Default SIM selection.")    
    gps: Literal["disable", "enable"] | None = Field(default="enable", description="FortiExtender GPS enable/disable.")    
    sim1_pin: Literal["disable", "enable"] | None = Field(default="disable", description="SIM #1 PIN status.")    
    sim2_pin: Literal["disable", "enable"] | None = Field(default="disable", description="SIM #2 PIN status.")    
    sim1_pin_code: Any = Field(max_length=27, default=None, description="SIM #1 PIN password.")    
    sim2_pin_code: Any = Field(max_length=27, default=None, description="SIM #2 PIN password.")    
    preferred_carrier: str | None = Field(max_length=31, default=None, description="Preferred carrier.")    
    auto_switch: ExtenderProfileCellularModem2AutoSwitch | None = Field(default=None, description="FortiExtender auto switch configuration.")    
    multiple_PDN: Literal["disable", "enable"] | None = Field(default="disable", description="Multiple-PDN enable/disable.")    
    pdn1_dataplan: str | None = Field(max_length=31, default=None, description="PDN1-dataplan.")  # datasource: ['extension-controller.dataplan.name']    
    pdn2_dataplan: str | None = Field(max_length=31, default=None, description="PDN2-dataplan.")  # datasource: ['extension-controller.dataplan.name']    
    pdn3_dataplan: str | None = Field(max_length=31, default=None, description="PDN3-dataplan.")  # datasource: ['extension-controller.dataplan.name']    
    pdn4_dataplan: str | None = Field(max_length=31, default=None, description="PDN4-dataplan.")  # datasource: ['extension-controller.dataplan.name']
class ExtenderProfileCellularModem1AutoSwitch(BaseModel):
    """
    Child table model for cellular.modem1.auto-switch.
    
    FortiExtender auto switch configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    disconnect: Literal["disable", "enable"] = Field(default="disable", description="Auto switch by disconnect.")    
    disconnect_threshold: int = Field(ge=1, le=100, default=3, description="Automatically switch based on disconnect threshold.")    
    disconnect_period: int = Field(ge=600, le=18000, default=600, description="Automatically switch based on disconnect period.")    
    signal: Literal["disable", "enable"] = Field(default="disable", description="Automatically switch based on signal strength.")    
    dataplan: Literal["disable", "enable"] = Field(default="disable", description="Automatically switch based on data usage.")    
    switch_back: list[Literal["time", "timer"]] = Field(default_factory=list, description="Auto switch with switch back multi-options.")    
    switch_back_time: str | None = Field(max_length=31, default="00:01", description="Automatically switch over to preferred SIM/carrier at a specified time in UTC (HH:MM).")    
    switch_back_timer: int | None = Field(ge=3600, le=2147483647, default=86400, description="Automatically switch over to preferred SIM/carrier after the given time (3600 - 2147483647 sec).")
class ExtenderProfileCellularModem1(BaseModel):
    """
    Child table model for cellular.modem1.
    
    Configuration options for modem 1.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    redundant_mode: Literal["disable", "enable"] = Field(default="disable", description="FortiExtender mode.")    
    redundant_intf: str = Field(max_length=15, description="Redundant interface.")    
    conn_status: int | None = Field(ge=0, le=4294967295, default=0, description="Connection status.")    
    default_sim: ExtenderProfileCellularModem1DefaultSimEnum = Field(default=ExtenderProfileCellularModem1DefaultSimEnum.SIM1, description="Default SIM selection.")    
    gps: Literal["disable", "enable"] | None = Field(default="enable", description="FortiExtender GPS enable/disable.")    
    sim1_pin: Literal["disable", "enable"] | None = Field(default="disable", description="SIM #1 PIN status.")    
    sim2_pin: Literal["disable", "enable"] | None = Field(default="disable", description="SIM #2 PIN status.")    
    sim1_pin_code: Any = Field(max_length=27, default=None, description="SIM #1 PIN password.")    
    sim2_pin_code: Any = Field(max_length=27, default=None, description="SIM #2 PIN password.")    
    preferred_carrier: str | None = Field(max_length=31, default=None, description="Preferred carrier.")    
    auto_switch: ExtenderProfileCellularModem1AutoSwitch | None = Field(default=None, description="FortiExtender auto switch configuration.")    
    multiple_PDN: Literal["disable", "enable"] | None = Field(default="disable", description="Multiple-PDN enable/disable.")    
    pdn1_dataplan: str | None = Field(max_length=31, default=None, description="PDN1-dataplan.")  # datasource: ['extension-controller.dataplan.name']    
    pdn2_dataplan: str | None = Field(max_length=31, default=None, description="PDN2-dataplan.")  # datasource: ['extension-controller.dataplan.name']    
    pdn3_dataplan: str | None = Field(max_length=31, default=None, description="PDN3-dataplan.")  # datasource: ['extension-controller.dataplan.name']    
    pdn4_dataplan: str | None = Field(max_length=31, default=None, description="PDN4-dataplan.")  # datasource: ['extension-controller.dataplan.name']
class ExtenderProfileCellularDataplan(BaseModel):
    """
    Child table model for cellular.dataplan.
    
    Dataplan names.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Dataplan name.")  # datasource: ['extension-controller.dataplan.name']
class ExtenderProfileCellularControllerReport(BaseModel):
    """
    Child table model for cellular.controller-report.
    
    FortiExtender controller report configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["disable", "enable"] = Field(default="disable", description="FortiExtender controller report status.")    
    interval: int = Field(ge=0, le=4294967295, default=300, description="Controller report interval.")    
    signal_threshold: int = Field(ge=10, le=50, default=10, description="Controller report signal threshold.")
class ExtenderProfileCellular(BaseModel):
    """
    Child table model for cellular.
    
    FortiExtender cellular configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    dataplan: list[ExtenderProfileCellularDataplan] = Field(default_factory=list, description="Dataplan names.")    
    controller_report: ExtenderProfileCellularControllerReport | None = Field(default=None, description="FortiExtender controller report configuration.")    
    sms_notification: ExtenderProfileCellularSmsNotification | None = Field(default=None, description="FortiExtender cellular SMS notification configuration.")    
    modem1: ExtenderProfileCellularModem1 | None = Field(default=None, description="Configuration options for modem 1.")    
    modem2: ExtenderProfileCellularModem2 | None = Field(default=None, description="Configuration options for modem 2.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class ExtenderProfileModelEnum(str, Enum):
    """Allowed values for model field."""
    FX201E = "FX201E"
    FX211E = "FX211E"
    FX200F = "FX200F"
    FXA11F = "FXA11F"
    FXE11F = "FXE11F"
    FXA21F = "FXA21F"
    FXE21F = "FXE21F"
    FXA22F = "FXA22F"
    FXE22F = "FXE22F"
    FX212F = "FX212F"
    FX311F = "FX311F"
    FX312F = "FX312F"
    FX511F = "FX511F"
    FXR51G = "FXR51G"
    FXN51G = "FXN51G"
    FXW51G = "FXW51G"
    FVG21F = "FVG21F"
    FVA21F = "FVA21F"
    FVG22F = "FVG22F"
    FVA22F = "FVA22F"
    FX04DA = "FX04DA"
    FG = "FG"
    BS10FW = "BS10FW"
    BS20GW = "BS20GW"
    BS20GN = "BS20GN"
    FVG51G = "FVG51G"
    FXE11G = "FXE11G"
    FX211G = "FX211G"

class ExtenderProfileAllowaccessEnum(str, Enum):
    """Allowed values for allowaccess field."""
    PING = "ping"
    TELNET = "telnet"
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"
    SNMP = "snmp"


# ============================================================================
# Main Model
# ============================================================================

class ExtenderProfileModel(BaseModel):
    """
    Pydantic model for extension_controller/extender_profile configuration.
    
    FortiExtender extender profile configuration.
    
    Validation Rules:        - name: max_length=31 pattern=        - id_: min=0 max=102400000 pattern=        - model: pattern=        - extension: pattern=        - allowaccess: pattern=        - login_password_change: pattern=        - login_password: max_length=27 pattern=        - enforce_bandwidth: pattern=        - bandwidth_limit: min=1 max=16776000 pattern=        - cellular: pattern=        - wifi: pattern=        - lan_extension: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=31, default=None, description="FortiExtender profile name.")    
    id_: int | None = Field(ge=0, le=102400000, default=32, serialization_alias="id", description="ID.")    
    model: ExtenderProfileModelEnum = Field(default=ExtenderProfileModelEnum.FX201E, description="Model.")    
    extension: Literal["wan-extension", "lan-extension"] = Field(default="wan-extension", description="Extension option.")    
    allowaccess: list[ExtenderProfileAllowaccessEnum] = Field(default_factory=list, description="Control management access to the managed extender. Separate entries with a space.")    
    login_password_change: Literal["yes", "default", "no"] | None = Field(default="no", description="Change or reset the administrator password of a managed extender (yes, default, or no, default = no).")    
    login_password: Any = Field(max_length=27, description="Set the managed extender's administrator password.")    
    enforce_bandwidth: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable enforcement of bandwidth on LAN extension interface.")    
    bandwidth_limit: int = Field(ge=1, le=16776000, default=1024, description="FortiExtender LAN extension bandwidth limit (Mbps).")    
    cellular: ExtenderProfileCellular | None = Field(description="FortiExtender cellular configuration.")    
    wifi: ExtenderProfileWifi | None = Field(default=None, description="FortiExtender Wi-Fi configuration.")    
    lan_extension: ExtenderProfileLanExtension | None = Field(description="FortiExtender LAN extension configuration.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "ExtenderProfileModel":
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
    async def validate_lan_extension_references(self, client: Any) -> list[str]:
        """
        Validate lan_extension references exist in FortiGate.
        
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
            >>> policy = ExtenderProfileModel(
            ...     lan_extension=[{"backhaul-interface": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_lan_extension_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.extension_controller.extender_profile.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "lan_extension", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("backhaul-interface")
            else:
                value = getattr(item, "backhaul-interface", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.system.interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Lan-Extension '{value}' not found in "
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
        
        errors = await self.validate_lan_extension_references(client)
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
    "ExtenderProfileModel",    "ExtenderProfileCellular",    "ExtenderProfileCellular.Dataplan",    "ExtenderProfileCellular.ControllerReport",    "ExtenderProfileCellular.SmsNotification",    "ExtenderProfileCellular.SmsNotification.Alert",    "ExtenderProfileCellular.SmsNotification.Receiver",    "ExtenderProfileCellular.Modem1",    "ExtenderProfileCellular.Modem1.AutoSwitch",    "ExtenderProfileCellular.Modem2",    "ExtenderProfileCellular.Modem2.AutoSwitch",    "ExtenderProfileWifi",    "ExtenderProfileWifi.Radio1",    "ExtenderProfileWifi.Radio1.LocalVaps",    "ExtenderProfileWifi.Radio2",    "ExtenderProfileWifi.Radio2.LocalVaps",    "ExtenderProfileLanExtension",    "ExtenderProfileLanExtension.Backhaul",    "ExtenderProfileLanExtension.Downlinks",    "ExtenderProfileLanExtension.Downlinks.Vids",    "ExtenderProfileLanExtension.TrafficSplitServices",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-04T03:46:38.892569Z
# ============================================================================