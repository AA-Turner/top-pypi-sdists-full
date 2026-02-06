"""
Pydantic Models for CMDB - switch_controller/managed_switch

Runtime validation models for switch_controller/managed_switch configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class ManagedSwitchSystemInterfaceAllowaccessEnum(str, Enum):
    """Allowed values for allowaccess field in system-interface."""
    PING = "ping"
    HTTPS = "https"
    HTTP = "http"
    SSH = "ssh"
    SNMP = "snmp"
    TELNET = "telnet"
    RADIUS_ACCT = "radius-acct"

class ManagedSwitchSystemDhcpServerOptionsTypeEnum(str, Enum):
    """Allowed values for type_ field in system-dhcp-server.options."""
    HEX = "hex"
    STRING = "string"
    IP = "ip"
    FQDN = "fqdn"

class ManagedSwitchSwitchLogSeverityEnum(str, Enum):
    """Allowed values for severity field in switch-log."""
    EMERGENCY = "emergency"
    ALERT = "alert"
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    NOTIFICATION = "notification"
    INFORMATION = "information"
    DEBUG = "debug"

class ManagedSwitchStpInstancePriorityEnum(str, Enum):
    """Allowed values for priority field in stp-instance."""
    V_0 = "0"
    V_4096 = "4096"
    V_8192 = "8192"
    V_12288 = "12288"
    V_16384 = "16384"
    V_20480 = "20480"
    V_24576 = "24576"
    V_28672 = "28672"
    V_32768 = "32768"
    V_36864 = "36864"
    V_40960 = "40960"
    V_45056 = "45056"
    V_49152 = "49152"
    V_53248 = "53248"
    V_57344 = "57344"
    V_61440 = "61440"

class ManagedSwitchSnmpUserAuthProtoEnum(str, Enum):
    """Allowed values for auth_proto field in snmp-user."""
    MD5 = "md5"
    SHA1 = "sha1"
    SHA224 = "sha224"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"

class ManagedSwitchSnmpUserPrivProtoEnum(str, Enum):
    """Allowed values for priv_proto field in snmp-user."""
    AES128 = "aes128"
    AES192 = "aes192"
    AES192C = "aes192c"
    AES256 = "aes256"
    AES256C = "aes256c"
    DES = "des"

class ManagedSwitchSnmpCommunityEventsEnum(str, Enum):
    """Allowed values for events field in snmp-community."""
    CPU_HIGH = "cpu-high"
    MEM_LOW = "mem-low"
    LOG_FULL = "log-full"
    INTF_IP = "intf-ip"
    ENT_CONF_CHANGE = "ent-conf-change"
    L2MAC = "l2mac"

class ManagedSwitchRemoteLogSeverityEnum(str, Enum):
    """Allowed values for severity field in remote-log."""
    EMERGENCY = "emergency"
    ALERT = "alert"
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    NOTIFICATION = "notification"
    INFORMATION = "information"
    DEBUG = "debug"

class ManagedSwitchRemoteLogFacilityEnum(str, Enum):
    """Allowed values for facility field in remote-log."""
    KERNEL = "kernel"
    USER = "user"
    MAIL = "mail"
    DAEMON = "daemon"
    AUTH = "auth"
    SYSLOG = "syslog"
    LPR = "lpr"
    NEWS = "news"
    UUCP = "uucp"
    CRON = "cron"
    AUTHPRIV = "authpriv"
    FTP = "ftp"
    NTP = "ntp"
    AUDIT = "audit"
    ALERT = "alert"
    CLOCK = "clock"
    LOCAL0 = "local0"
    LOCAL1 = "local1"
    LOCAL2 = "local2"
    LOCAL3 = "local3"
    LOCAL4 = "local4"
    LOCAL5 = "local5"
    LOCAL6 = "local6"
    LOCAL7 = "local7"

class ManagedSwitchPortsSpeedEnum(str, Enum):
    """Allowed values for speed field in ports."""
    V_10HALF = "10half"
    V_10FULL = "10full"
    V_100HALF = "100half"
    V_100FULL = "100full"
    V_1000FULL = "1000full"
    V_10000FULL = "10000full"
    AUTO = "auto"
    V_1000AUTO = "1000auto"
    V_1000FULL_FIBER = "1000full-fiber"
    V_40000FULL = "40000full"
    AUTO_MODULE = "auto-module"
    V_100FX_HALF = "100FX-half"
    V_100FX_FULL = "100FX-full"
    V_100000FULL = "100000full"
    V_2500AUTO = "2500auto"
    V_2500FULL = "2500full"
    V_25000FULL = "25000full"
    V_50000FULL = "50000full"
    V_10000CR = "10000cr"
    V_10000SR = "10000sr"
    V_100000SR4 = "100000sr4"
    V_100000CR4 = "100000cr4"
    V_40000SR4 = "40000sr4"
    V_40000CR4 = "40000cr4"
    V_40000AUTO = "40000auto"
    V_25000CR = "25000cr"
    V_25000SR = "25000sr"
    V_50000CR = "50000cr"
    V_50000SR = "50000sr"
    V_5000AUTO = "5000auto"
    SGMII_AUTO = "sgmii-auto"

class ManagedSwitchPortsPoePortPriorityEnum(str, Enum):
    """Allowed values for poe_port_priority field in ports."""
    CRITICAL_PRIORITY = "critical-priority"
    HIGH_PRIORITY = "high-priority"
    LOW_PRIORITY = "low-priority"
    MEDIUM_PRIORITY = "medium-priority"

class ManagedSwitchPortsFecStateEnum(str, Enum):
    """Allowed values for fec_state field in ports."""
    DISABLED = "disabled"
    CL74 = "cl74"
    CL91 = "cl91"
    DETECT_BY_MODULE = "detect-by-module"

class ManagedSwitchPortsFlowControlEnum(str, Enum):
    """Allowed values for flow_control field in ports."""
    DISABLE = "disable"
    TX = "tx"
    RX = "rx"
    BOTH = "both"

class ManagedSwitchPortsLldpStatusEnum(str, Enum):
    """Allowed values for lldp_status field in ports."""
    DISABLE = "disable"
    RX_ONLY = "rx-only"
    TX_ONLY = "tx-only"
    TX_RX = "tx-rx"

class ManagedSwitchPortsPortSelectionCriteriaEnum(str, Enum):
    """Allowed values for port_selection_criteria field in ports."""
    SRC_MAC = "src-mac"
    DST_MAC = "dst-mac"
    SRC_DST_MAC = "src-dst-mac"
    SRC_IP = "src-ip"
    DST_IP = "dst-ip"
    SRC_DST_IP = "src-dst-ip"

class ManagedSwitch8021XSettingsMacUsernameDelimiterEnum(str, Enum):
    """Allowed values for mac_username_delimiter field in 802-1X-settings."""
    COLON = "colon"
    HYPHEN = "hyphen"
    NONE = "none"
    SINGLE_HYPHEN = "single-hyphen"

class ManagedSwitch8021XSettingsMacPasswordDelimiterEnum(str, Enum):
    """Allowed values for mac_password_delimiter field in 802-1X-settings."""
    COLON = "colon"
    HYPHEN = "hyphen"
    NONE = "none"
    SINGLE_HYPHEN = "single-hyphen"

class ManagedSwitch8021XSettingsMacCallingStationDelimiterEnum(str, Enum):
    """Allowed values for mac_calling_station_delimiter field in 802-1X-settings."""
    COLON = "colon"
    HYPHEN = "hyphen"
    NONE = "none"
    SINGLE_HYPHEN = "single-hyphen"

class ManagedSwitch8021XSettingsMacCalledStationDelimiterEnum(str, Enum):
    """Allowed values for mac_called_station_delimiter field in 802-1X-settings."""
    COLON = "colon"
    HYPHEN = "hyphen"
    NONE = "none"
    SINGLE_HYPHEN = "single-hyphen"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class ManagedSwitchVlan(BaseModel):
    """
    Child table model for vlan.
    
    Configure VLAN assignment priority.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vlan_name: str | None = Field(max_length=15, default=None, description="VLAN name.")  # datasource: ['system.interface.name']    
    assignment_priority: int = Field(ge=1, le=255, default=128, description="802.1x Radius (Tunnel-Private-Group-Id) VLANID assign-by-name priority. A smaller value has a higher priority.")
class ManagedSwitchSystemInterface(BaseModel):
    """
    Child table model for system-interface.
    
    Configure system interface on FortiSwitch.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=15, default=None, description="Interface name.")    
    switch_id: str | None = Field(max_length=35, default=None, description="Switch ID.")  # datasource: ['switch-controller.managed-switch.switch-id']    
    mode: Literal["static", "dhcp"] | None = Field(default="static", description="Interface addressing mode.")    
    ip: Any = Field(default="0.0.0.0 0.0.0.0", description="IP and mask for this interface.")    
    status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable interface status.")    
    allowaccess: list[ManagedSwitchSystemInterfaceAllowaccessEnum] = Field(default_factory=list, description="Permitted types of management access to this interface.")    
    vlan: str = Field(max_length=15, description="VLAN name.")  # datasource: ['system.interface.name']    
    type_: Literal["vlan", "physical"] | None = Field(default="vlan", serialization_alias="type", description="Interface type.")    
    interface: str = Field(max_length=63, description="Interface name.")  # datasource: ['switch-controller.managed-switch.ports.port-name']    
    vrf: str | None = Field(max_length=63, default=None, description="VRF for this route.")  # datasource: ['switch-controller.managed-switch.router-vrf.name']
class ManagedSwitchSystemDhcpServerOptions(BaseModel):
    """
    Child table model for system-dhcp-server.options.
    
    DHCP options.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    code: int = Field(ge=0, le=255, default=0, description="DHCP option code.")    
    type_: ManagedSwitchSystemDhcpServerOptionsTypeEnum | None = Field(default=ManagedSwitchSystemDhcpServerOptionsTypeEnum.HEX, serialization_alias="type", description="DHCP option type.")    
    value: str | None = Field(max_length=312, default=None, description="DHCP option value.")    
    ip: list[str] = Field(default_factory=list, description="DHCP option IPs.")
class ManagedSwitchSystemDhcpServerIpRange(BaseModel):
    """
    Child table model for system-dhcp-server.ip-range.
    
    DHCP IP range configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    start_ip: str = Field(default="0.0.0.0", description="Start of IP range.")    
    end_ip: str = Field(default="0.0.0.0", description="End of IP range.")
class ManagedSwitchSystemDhcpServer(BaseModel):
    """
    Child table model for system-dhcp-server.
    
    Configure DHCP servers.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    switch_id: str | None = Field(max_length=35, default=None, description="Switch ID.")  # datasource: ['switch-controller.managed-switch.switch-id']    
    status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable this DHCP configuration.")    
    lease_time: int | None = Field(ge=0, le=4294967295, default=604800, description="Lease time in seconds, 0 means unlimited.")    
    dns_service: Literal["local", "default", "specify"] | None = Field(default="specify", description="Options for assigning DNS servers to DHCP clients.")    
    dns_server1: str | None = Field(default="0.0.0.0", description="DNS server 1.")    
    dns_server2: str | None = Field(default="0.0.0.0", description="DNS server 2.")    
    dns_server3: str | None = Field(default="0.0.0.0", description="DNS server 3.")    
    ntp_service: Literal["local", "default", "specify"] | None = Field(default="specify", description="Options for assigning Network Time Protocol (NTP) servers to DHCP clients.")    
    ntp_server1: str | None = Field(default="0.0.0.0", description="NTP server 1.")    
    ntp_server2: str | None = Field(default="0.0.0.0", description="NTP server 2.")    
    ntp_server3: str | None = Field(default="0.0.0.0", description="NTP server 3.")    
    default_gateway: str | None = Field(default="0.0.0.0", description="Default gateway IP address assigned by the DHCP server.")    
    netmask: str = Field(default="0.0.0.0", description="Netmask assigned by the DHCP server.")    
    interface: str = Field(max_length=15, description="DHCP server can assign IP configurations to clients connected to this interface.")  # datasource: ['switch-controller.managed-switch.system-interface.name']    
    ip_range: list[ManagedSwitchSystemDhcpServerIpRange] = Field(default_factory=list, description="DHCP IP range configuration.")    
    options: list[ManagedSwitchSystemDhcpServerOptions] = Field(default_factory=list, description="DHCP options.")
class ManagedSwitchSwitchLog(BaseModel):
    """
    Child table model for switch-log.
    
    Configuration method to edit FortiSwitch logging settings (logs are transferred to and inserted into the FortiGate event log).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    local_override: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to configure local logging settings that override global logging settings.")    
    status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable adding FortiSwitch logs to the FortiGate event log.")    
    severity: ManagedSwitchSwitchLogSeverityEnum | None = Field(default=ManagedSwitchSwitchLogSeverityEnum.NOTIFICATION, description="Severity of FortiSwitch logs that are added to the FortiGate event log.")
class ManagedSwitchStpSettings(BaseModel):
    """
    Child table model for stp-settings.
    
    Configuration method to edit Spanning Tree Protocol (STP) settings used to prevent bridge loops.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    local_override: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to configure local STP settings that override global STP settings.")    
    name: str | None = Field(max_length=31, default=None, description="Name of local STP settings configuration.")    
    revision: int | None = Field(ge=0, le=65535, default=0, description="STP revision number (0 - 65535).")    
    hello_time: int | None = Field(ge=1, le=10, default=2, description="Period of time between successive STP frame Bridge Protocol Data Units (BPDUs) sent on a port (1 - 10 sec, default = 2).")    
    forward_time: int | None = Field(ge=4, le=30, default=15, description="Period of time a port is in listening and learning state (4 - 30 sec, default = 15).")    
    max_age: int | None = Field(ge=6, le=40, default=20, description="Maximum time before a bridge port saves its configuration BPDU information (6 - 40 sec, default = 20).")    
    max_hops: int | None = Field(ge=1, le=40, default=20, description="Maximum number of hops between the root bridge and the furthest bridge (1- 40, default = 20).")    
    pending_timer: int | None = Field(ge=1, le=15, default=4, description="Pending time (1 - 15 sec, default = 4).")
class ManagedSwitchStpInstance(BaseModel):
    """
    Child table model for stp-instance.
    
    Configuration method to edit Spanning Tree Protocol (STP) instances.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: str | None = Field(max_length=2, default=None, serialization_alias="id", description="Instance ID.")    
    priority: ManagedSwitchStpInstancePriorityEnum | None = Field(default=ManagedSwitchStpInstancePriorityEnum.V_32768, description="Priority.")
class ManagedSwitchStormControl(BaseModel):
    """
    Child table model for storm-control.
    
    Configuration method to edit FortiSwitch storm control for measuring traffic activity using data rates to prevent traffic disruption.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    local_override: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override global FortiSwitch storm control settings for this FortiSwitch.")    
    rate: int | None = Field(ge=0, le=10000000, default=500, description="Rate in packets per second at which storm control drops excess traffic(0-10000000, default=500, drop-all=0).")    
    burst_size_level: int | None = Field(ge=0, le=4, default=0, description="Increase level to handle bursty traffic (0 - 4, default = 0).")    
    unknown_unicast: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable storm control to drop unknown unicast traffic.")    
    unknown_multicast: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable storm control to drop unknown multicast traffic.")    
    broadcast: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable storm control to drop broadcast traffic.")
class ManagedSwitchStaticMac(BaseModel):
    """
    Child table model for static-mac.
    
    Configuration method to edit FortiSwitch Static and Sticky MAC.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    type_: Literal["static", "sticky"] | None = Field(default="static", serialization_alias="type", description="Type.")    
    vlan: str | None = Field(max_length=15, default=None, description="Vlan.")  # datasource: ['system.interface.name']    
    mac: str | None = Field(default="00:00:00:00:00:00", description="MAC address.")    
    interface: str | None = Field(max_length=35, default=None, description="Interface name.")    
    description: str | None = Field(max_length=63, default=None, description="Description.")
class ManagedSwitchSnmpUser(BaseModel):
    """
    Child table model for snmp-user.
    
    Configuration method to edit Simple Network Management Protocol (SNMP) users.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=32, default=None, description="SNMP user name.")    
    queries: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable SNMP queries for this user.")    
    query_port: int | None = Field(ge=0, le=65535, default=161, description="SNMPv3 query port (default = 161).")    
    security_level: Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"] | None = Field(default="no-auth-no-priv", description="Security level for message authentication and encryption.")    
    auth_proto: ManagedSwitchSnmpUserAuthProtoEnum | None = Field(default=ManagedSwitchSnmpUserAuthProtoEnum.SHA256, description="Authentication protocol.")    
    auth_pwd: Any = Field(max_length=128, description="Password for authentication protocol.")    
    priv_proto: ManagedSwitchSnmpUserPrivProtoEnum | None = Field(default=ManagedSwitchSnmpUserPrivProtoEnum.AES128, description="Privacy (encryption) protocol.")    
    priv_pwd: Any = Field(max_length=128, description="Password for privacy (encryption) protocol.")
class ManagedSwitchSnmpTrapThreshold(BaseModel):
    """
    Child table model for snmp-trap-threshold.
    
    Configuration method to edit Simple Network Management Protocol (SNMP) trap threshold values.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    trap_high_cpu_threshold: int | None = Field(ge=0, le=4294967295, default=80, description="CPU usage when trap is sent.")    
    trap_low_memory_threshold: int | None = Field(ge=0, le=4294967295, default=80, description="Memory usage when trap is sent.")    
    trap_log_full_threshold: int | None = Field(ge=0, le=4294967295, default=90, description="Log disk usage when trap is sent.")
class ManagedSwitchSnmpSysinfo(BaseModel):
    """
    Child table model for snmp-sysinfo.
    
    Configuration method to edit Simple Network Management Protocol (SNMP) system info.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    status: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable SNMP.")    
    engine_id: str | None = Field(max_length=24, default=None, description="Local SNMP engine ID string (max 24 char).")    
    description: str | None = Field(max_length=35, default=None, description="System description.")    
    contact_info: str | None = Field(max_length=35, default=None, description="Contact information.")    
    location: str | None = Field(max_length=35, default=None, description="System location.")
class ManagedSwitchSnmpCommunityHosts(BaseModel):
    """
    Child table model for snmp-community.hosts.
    
    Configure IPv4 SNMP managers (hosts).
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Host entry ID.")    
    ip: str = Field(description="IPv4 address of the SNMP manager (host).")
class ManagedSwitchSnmpCommunity(BaseModel):
    """
    Child table model for snmp-community.
    
    Configuration method to edit Simple Network Management Protocol (SNMP) communities.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="SNMP community ID.")    
    name: str = Field(max_length=35, description="SNMP community name.")    
    status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable this SNMP community.")    
    hosts: list[ManagedSwitchSnmpCommunityHosts] = Field(default_factory=list, description="Configure IPv4 SNMP managers (hosts).")    
    query_v1_status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable SNMP v1 queries.")    
    query_v1_port: int | None = Field(ge=0, le=65535, default=161, description="SNMP v1 query port (default = 161).")    
    query_v2c_status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable SNMP v2c queries.")    
    query_v2c_port: int | None = Field(ge=0, le=65535, default=161, description="SNMP v2c query port (default = 161).")    
    trap_v1_status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable SNMP v1 traps.")    
    trap_v1_lport: int | None = Field(ge=0, le=65535, default=162, description="SNMP v2c trap local port (default = 162).")    
    trap_v1_rport: int | None = Field(ge=0, le=65535, default=162, description="SNMP v2c trap remote port (default = 162).")    
    trap_v2c_status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable SNMP v2c traps.")    
    trap_v2c_lport: int | None = Field(ge=0, le=65535, default=162, description="SNMP v2c trap local port (default = 162).")    
    trap_v2c_rport: int | None = Field(ge=0, le=65535, default=162, description="SNMP v2c trap remote port (default = 162).")    
    events: list[ManagedSwitchSnmpCommunityEventsEnum] = Field(default_factory=list, description="SNMP notifications (traps) to send.")
class ManagedSwitchRouterVrf(BaseModel):
    """
    Child table model for router-vrf.
    
    Configure VRF.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="VRF entry name.")    
    switch_id: str | None = Field(max_length=35, default=None, description="Switch ID.")  # datasource: ['switch-controller.managed-switch.switch-id']    
    vrfid: int = Field(ge=0, le=1023, default=0, description="VRF ID.")
class ManagedSwitchRouterStatic(BaseModel):
    """
    Child table model for router-static.
    
    Configure static routes.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Entry sequence number.")    
    switch_id: str | None = Field(max_length=35, default=None, description="Switch ID.")  # datasource: ['switch-controller.managed-switch.switch-id']    
    blackhole: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable blackhole on this route.")    
    comment: str | None = Field(max_length=63, default=None, description="Comment.")    
    device: str | None = Field(max_length=35, default=None, description="Gateway out interface.")  # datasource: ['switch-controller.managed-switch.system-interface.name']    
    distance: int | None = Field(ge=1, le=255, default=10, description="Administrative distance for the route (1 - 255, default = 10).")    
    dst: str = Field(default="0.0.0.0 0.0.0.0", description="Destination ip and mask for this route.")    
    dynamic_gateway: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable dynamic gateway.")    
    gateway: str = Field(default="0.0.0.0", description="Gateway ip for this route.")    
    status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable route status.")    
    vrf: str | None = Field(max_length=35, default=None, description="VRF for this route.")  # datasource: ['switch-controller.managed-switch.router-vrf.name']
class ManagedSwitchRouteOffloadRouter(BaseModel):
    """
    Child table model for route-offload-router.
    
    Configure route offload MCLAG IP address.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vlan_name: str | None = Field(max_length=15, default=None, description="VLAN name.")  # datasource: ['system.interface.name']    
    router_ip: str = Field(default="0.0.0.0", description="Router IP address.")
class ManagedSwitchRemoteLog(BaseModel):
    """
    Child table model for remote-log.
    
    Configure logging by FortiSwitch device to a remote syslog server.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=35, description="Remote log name.")    
    status: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable logging by FortiSwitch device to a remote syslog server.")    
    server: str = Field(max_length=63, description="IPv4 address of the remote syslog server.")    
    port: int | None = Field(ge=0, le=65535, default=514, description="Remote syslog server listening port.")    
    severity: ManagedSwitchRemoteLogSeverityEnum | None = Field(default=ManagedSwitchRemoteLogSeverityEnum.INFORMATION, description="Severity of logs to be transferred to remote log server.")    
    csv: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable comma-separated value (CSV) strings.")    
    facility: ManagedSwitchRemoteLogFacilityEnum | None = Field(default=ManagedSwitchRemoteLogFacilityEnum.LOCAL7, description="Facility to log to remote syslog server.")
class ManagedSwitchPortsUntaggedVlans(BaseModel):
    """
    Child table model for ports.untagged-vlans.
    
    Configure switch port untagged VLANs.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vlan_name: str = Field(max_length=79, description="VLAN name.")  # datasource: ['system.interface.name']
class ManagedSwitchPortsMembers(BaseModel):
    """
    Child table model for ports.members.
    
    Aggregated LAG bundle interfaces.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    member_name: str = Field(max_length=79, description="Interface name from available options.")
class ManagedSwitchPortsInterfaceTags(BaseModel):
    """
    Child table model for ports.interface-tags.
    
    Tag(s) associated with the interface for various features including virtual port pool, dynamic port policy.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    tag_name: str | None = Field(max_length=63, default=None, description="FortiSwitch port tag name when exported to a virtual port pool or matched to dynamic port policy.")  # datasource: ['switch-controller.switch-interface-tag.name']
class ManagedSwitchPortsFortiswitchAcls(BaseModel):
    """
    Child table model for ports.fortiswitch-acls.
    
    ACLs on this port.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ACL ID.")
class ManagedSwitchPortsDhcpSnoopOption82Override(BaseModel):
    """
    Child table model for ports.dhcp-snoop-option82-override.
    
    Configure DHCP snooping option 82 override.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vlan_name: str | None = Field(max_length=15, default=None, description="DHCP snooping option 82 VLAN.")  # datasource: ['system.interface.name']    
    circuit_id: str | None = Field(max_length=254, default=None, description="Circuit ID string.")    
    remote_id: str | None = Field(max_length=254, default=None, description="Remote ID string.")
class ManagedSwitchPortsAllowedVlans(BaseModel):
    """
    Child table model for ports.allowed-vlans.
    
    Configure switch port tagged VLANs.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vlan_name: str = Field(max_length=79, description="VLAN name.")  # datasource: ['system.interface.name']
class ManagedSwitchPortsAclGroup(BaseModel):
    """
    Child table model for ports.acl-group.
    
    ACL groups on this port.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="ACL group name.")  # datasource: ['switch-controller.acl.group.name']
class ManagedSwitchPorts(BaseModel):
    """
    Child table model for ports.
    
    Managed-switch port list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    port_name: str = Field(max_length=15, description="Switch port name.")    
    port_owner: str | None = Field(max_length=15, default=None, description="Switch port name.")    
    switch_id: str | None = Field(max_length=35, default=None, description="Switch id.")    
    speed: ManagedSwitchPortsSpeedEnum | None = Field(default=ManagedSwitchPortsSpeedEnum.AUTO, description="Switch port speed; default and available settings depend on hardware.")    
    status: Literal["up", "down"] | None = Field(default="up", description="Switch port admin status: up or down.")    
    poe_status: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable PoE status.")    
    ip_source_guard: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable IP source guard.")    
    ptp_status: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable PTP policy on this FortiSwitch port.")    
    ptp_policy: str | None = Field(max_length=63, default="default", description="PTP policy configuration.")  # datasource: ['switch-controller.ptp.interface-policy.name']    
    aggregator_mode: Literal["bandwidth", "count"] | None = Field(default="bandwidth", description="LACP member select mode.")    
    flapguard: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable flap guard.")    
    flap_rate: int | None = Field(ge=1, le=30, default=5, description="Number of stage change events needed within flap-duration.")    
    flap_duration: int | None = Field(ge=5, le=300, default=30, description="Period over which flap events are calculated (seconds).")    
    flap_timeout: int | None = Field(ge=0, le=120, default=0, description="Flap guard disabling protection (min).")    
    rpvst_port: Literal["disabled", "enabled"] | None = Field(default="disabled", description="Enable/disable inter-operability with rapid PVST on this interface.")    
    poe_pre_standard_detection: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable PoE pre-standard detection.")    
    port_number: int | None = Field(ge=1, le=64, default=0, description="Port number.")    
    port_prefix_type: int | None = Field(ge=0, le=1, default=0, description="Port prefix type.")    
    fortilink_port: int | None = Field(ge=0, le=1, default=0, description="FortiLink uplink port.")    
    poe_capable: int | None = Field(ge=0, le=1, default=0, description="PoE capable.")    
    pd_capable: int | None = Field(ge=0, le=1, default=0, description="Powered device capable.")    
    stacking_port: int | None = Field(ge=0, le=1, default=0, description="Stacking port.")    
    p2p_port: int | None = Field(ge=0, le=1, default=0, description="General peer to peer tunnel port.")    
    mclag_icl_port: int | None = Field(ge=0, le=1, default=0, description="MCLAG-ICL port.")    
    authenticated_port: int | None = Field(ge=0, le=1, default=0, description="Peer to Peer Authenticated port.")    
    restricted_auth_port: int | None = Field(ge=0, le=1, default=0, description="Peer to Peer Restricted Authenticated port.")    
    encrypted_port: int | None = Field(ge=0, le=1, default=0, description="Peer to Peer Encrypted port.")    
    fiber_port: int | None = Field(ge=0, le=1, default=0, description="Fiber-port.")    
    media_type: str | None = Field(max_length=31, default=None, description="Media type.")    
    poe_standard: str | None = Field(max_length=63, default=None, description="PoE standard supported.")    
    poe_max_power: str | None = Field(max_length=35, default=None, description="PoE maximum power.")    
    poe_mode_bt_cabable: int | None = Field(ge=0, le=1, default=0, description="PoE mode IEEE 802.3BT capable.")    
    poe_port_mode: Literal["ieee802-3af", "ieee802-3at", "ieee802-3bt"] | None = Field(default="ieee802-3at", description="Configure PoE port mode.")    
    poe_port_priority: ManagedSwitchPortsPoePortPriorityEnum | None = Field(default=ManagedSwitchPortsPoePortPriorityEnum.LOW_PRIORITY, description="Configure PoE port priority.")    
    poe_port_power: Literal["normal", "perpetual", "perpetual-fast"] | None = Field(default="normal", description="Configure PoE port power.")    
    flags: int | None = Field(ge=0, le=4294967295, default=0, description="Port properties flags.")    
    isl_local_trunk_name: str | None = Field(max_length=15, default=None, description="ISL local trunk name.")    
    isl_peer_port_name: str | None = Field(max_length=15, default=None, description="ISL peer port name.")    
    isl_peer_device_name: str | None = Field(max_length=35, default=None, description="ISL peer device name.")    
    isl_peer_device_sn: str | None = Field(max_length=16, default=None, description="ISL peer device serial number.")    
    fgt_peer_port_name: str | None = Field(max_length=15, default=None, description="FGT peer port name.")    
    fgt_peer_device_name: str | None = Field(max_length=35, default=None, description="FGT peer device name.")    
    vlan: str | None = Field(max_length=15, default=None, description="Assign switch ports to a VLAN.")  # datasource: ['system.interface.name']    
    allowed_vlans_all: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable all defined vlans on this port.")    
    allowed_vlans: list[ManagedSwitchPortsAllowedVlans] = Field(default_factory=list, description="Configure switch port tagged VLANs.")    
    untagged_vlans: list[ManagedSwitchPortsUntaggedVlans] = Field(default_factory=list, description="Configure switch port untagged VLANs.")    
    type_: Literal["physical", "trunk"] | None = Field(default="physical", serialization_alias="type", description="Interface type: physical or trunk port.")    
    access_mode: Literal["dynamic", "nac", "static"] | None = Field(default="static", description="Access mode of the port.")    
    matched_dpp_policy: str | None = Field(max_length=63, default=None, description="Matched child policy in the dynamic port policy.")    
    matched_dpp_intf_tags: str | None = Field(max_length=63, default=None, description="Matched interface tags in the dynamic port policy.")    
    acl_group: list[ManagedSwitchPortsAclGroup] = Field(default_factory=list, description="ACL groups on this port.")    
    fortiswitch_acls: list[ManagedSwitchPortsFortiswitchAcls] = Field(default_factory=list, description="ACLs on this port.")    
    dhcp_snooping: Literal["untrusted", "trusted"] | None = Field(default="untrusted", description="Trusted or untrusted DHCP-snooping interface.")    
    dhcp_snoop_option82_trust: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable allowance of DHCP with option-82 on untrusted interface.")    
    dhcp_snoop_option82_override: list[ManagedSwitchPortsDhcpSnoopOption82Override] = Field(default_factory=list, description="Configure DHCP snooping option 82 override.")    
    arp_inspection_trust: Literal["untrusted", "trusted"] | None = Field(default="untrusted", description="Trusted or untrusted dynamic ARP inspection.")    
    igmp_snooping_flood_reports: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable flooding of IGMP reports to this interface when igmp-snooping enabled.")    
    mcast_snooping_flood_traffic: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable flooding of IGMP snooping traffic to this interface.")    
    stp_state: Literal["enabled", "disabled"] | None = Field(default="enabled", description="Enable/disable Spanning Tree Protocol (STP) on this interface.")    
    stp_root_guard: Literal["enabled", "disabled"] | None = Field(default="disabled", description="Enable/disable STP root guard on this interface.")    
    stp_bpdu_guard: Literal["enabled", "disabled"] | None = Field(default="disabled", description="Enable/disable STP BPDU guard on this interface.")    
    stp_bpdu_guard_timeout: int | None = Field(ge=0, le=120, default=5, description="BPDU Guard disabling protection (0 - 120 min).")    
    edge_port: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable this interface as an edge port, bridging connections between workstations and/or computers.")    
    discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = Field(default="none", description="Configure discard mode for port.")    
    packet_sampler: Literal["enabled", "disabled"] | None = Field(default="disabled", description="Enable/disable packet sampling on this interface.")    
    packet_sample_rate: int | None = Field(ge=0, le=99999, default=512, description="Packet sampling rate (0 - 99999 p/sec).")    
    sflow_counter_interval: int | None = Field(ge=0, le=255, default=0, description="sFlow sampling counter polling interval in seconds (0 - 255).")    
    sample_direction: Literal["tx", "rx", "both"] | None = Field(default="both", description="Packet sampling direction.")    
    fec_capable: int | None = Field(ge=0, le=1, default=0, description="FEC capable.")    
    fec_state: ManagedSwitchPortsFecStateEnum | None = Field(default=ManagedSwitchPortsFecStateEnum.DETECT_BY_MODULE, description="State of forward error correction.")    
    flow_control: ManagedSwitchPortsFlowControlEnum | None = Field(default=ManagedSwitchPortsFlowControlEnum.DISABLE, description="Flow control direction.")    
    pause_meter: int | None = Field(ge=128, le=2147483647, default=0, description="Configure ingress pause metering rate, in kbps (default = 0, disabled).")    
    pause_meter_resume: Literal["75%", "50%", "25%"] | None = Field(default="50%", description="Resume threshold for resuming traffic on ingress port.")    
    loop_guard: Literal["enabled", "disabled"] | None = Field(default="disabled", description="Enable/disable loop-guard on this interface, an STP optimization used to prevent network loops.")    
    loop_guard_timeout: int | None = Field(ge=0, le=120, default=45, description="Loop-guard timeout (0 - 120 min, default = 45).")    
    port_policy: str | None = Field(max_length=63, default=None, description="Switch controller dynamic port policy from available options.")  # datasource: ['switch-controller.dynamic-port-policy.name']    
    qos_policy: str | None = Field(max_length=63, default="default", description="Switch controller QoS policy from available options.")  # datasource: ['switch-controller.qos.qos-policy.name']    
    storm_control_policy: str | None = Field(max_length=63, default="default", description="Switch controller storm control policy from available options.")  # datasource: ['switch-controller.storm-control-policy.name']    
    port_security_policy: str | None = Field(max_length=31, default=None, description="Switch controller authentication policy to apply to this managed switch from available options.")  # datasource: ['switch-controller.security-policy.802-1X.name']    
    export_to_pool: str | None = Field(max_length=35, default=None, description="Switch controller export port to pool-list.")  # datasource: ['switch-controller.virtual-port-pool.name']    
    interface_tags: list[ManagedSwitchPortsInterfaceTags] = Field(default_factory=list, description="Tag(s) associated with the interface for various features including virtual port pool, dynamic port policy.")    
    learning_limit: int | None = Field(ge=0, le=128, default=0, description="Limit the number of dynamic MAC addresses on this Port (1 - 128, 0 = no limit, default).")    
    sticky_mac: Literal["enable", "disable"] | None = Field(default="disable", description="Enable or disable sticky-mac on the interface.")    
    lldp_status: ManagedSwitchPortsLldpStatusEnum | None = Field(default=ManagedSwitchPortsLldpStatusEnum.TX_RX, description="LLDP transmit and receive status.")    
    lldp_profile: str | None = Field(max_length=63, default="default-auto-isl", description="LLDP port TLV profile.")  # datasource: ['switch-controller.lldp-profile.name']    
    export_to: str | None = Field(max_length=31, default=None, description="Export managed-switch port to a tenant VDOM.")  # datasource: ['system.vdom.name']    
    mac_addr: str | None = Field(default="00:00:00:00:00:00", description="Port/Trunk MAC.")    
    allow_arp_monitor: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/Disable allow ARP monitor.")    
    qnq: str | None = Field(max_length=15, default=None, description="802.1AD VLANs in the VDom.")  # datasource: ['system.interface.name']    
    log_mac_event: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable logging for dynamic MAC address events.")    
    port_selection_criteria: ManagedSwitchPortsPortSelectionCriteriaEnum | None = Field(default=ManagedSwitchPortsPortSelectionCriteriaEnum.SRC_DST_IP, description="Algorithm for aggregate port selection.")    
    description: str | None = Field(max_length=63, default=None, description="Description for port.")    
    lacp_speed: Literal["slow", "fast"] | None = Field(default="slow", description="End Link Aggregation Control Protocol (LACP) messages every 30 seconds (slow) or every second (fast).")    
    mode: Literal["static", "lacp-passive", "lacp-active"] | None = Field(default="static", description="LACP mode: ignore and do not send control messages, or negotiate 802.3ad aggregation passively or actively.")    
    bundle: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable Link Aggregation Group (LAG) bundling for non-FortiLink interfaces.")    
    member_withdrawal_behavior: Literal["forward", "block"] | None = Field(default="block", description="Port behavior after it withdraws because of loss of control packets.")    
    mclag: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable multi-chassis link aggregation (MCLAG).")    
    min_bundle: int | None = Field(ge=1, le=24, default=1, description="Minimum size of LAG bundle (1 - 24, default = 1).")    
    max_bundle: int | None = Field(ge=1, le=24, default=24, description="Maximum size of LAG bundle (1 - 24, default = 24).")    
    members: list[ManagedSwitchPortsMembers] = Field(default_factory=list, description="Aggregated LAG bundle interfaces.")    
    fallback_port: str | None = Field(max_length=79, default=None, description="LACP fallback port.")
class ManagedSwitchMirrorSrcIngress(BaseModel):
    """
    Child table model for mirror.src-ingress.
    
    Source ingress interfaces.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="Interface name.")
class ManagedSwitchMirrorSrcEgress(BaseModel):
    """
    Child table model for mirror.src-egress.
    
    Source egress interfaces.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=79, description="Interface name.")
class ManagedSwitchMirror(BaseModel):
    """
    Child table model for mirror.
    
    Configuration method to edit FortiSwitch packet mirror.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=63, default=None, description="Mirror name.")    
    status: Literal["active", "inactive"] | None = Field(default="inactive", description="Active/inactive mirror configuration.")    
    switching_packet: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable switching functionality when mirroring.")    
    dst: str | None = Field(max_length=63, default=None, description="Destination port.")    
    src_ingress: list[ManagedSwitchMirrorSrcIngress] = Field(default_factory=list, description="Source ingress interfaces.")    
    src_egress: list[ManagedSwitchMirrorSrcEgress] = Field(default_factory=list, description="Source egress interfaces.")
class ManagedSwitchIpSourceGuardBindingEntry(BaseModel):
    """
    Child table model for ip-source-guard.binding-entry.
    
    IP and MAC address configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    entry_name: str = Field(max_length=16, description="Configure binding pair.")    
    ip: str = Field(default="0.0.0.0", description="Source IP for this rule.")    
    mac: str = Field(default="00:00:00:00:00:00", description="MAC address for this rule.")
class ManagedSwitchIpSourceGuard(BaseModel):
    """
    Child table model for ip-source-guard.
    
    IP source guard.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    port: str | None = Field(max_length=15, default=None, description="Ingress interface to which source guard is bound.")    
    description: str | None = Field(max_length=63, default=None, description="Description.")    
    binding_entry: list[ManagedSwitchIpSourceGuardBindingEntry] = Field(description="IP and MAC address configuration.")
class ManagedSwitchIgmpSnoopingVlans(BaseModel):
    """
    Child table model for igmp-snooping.vlans.
    
    Configure IGMP snooping VLAN.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    vlan_name: str | None = Field(max_length=15, default="default", description="List of FortiSwitch VLANs.")  # datasource: ['system.interface.name']    
    proxy: Literal["disable", "enable", "global"] | None = Field(default="global", description="IGMP snooping proxy for the VLAN interface.")    
    querier: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable IGMP snooping querier for the VLAN interface.")    
    querier_addr: str | None = Field(default="0.0.0.0", description="IGMP snooping querier address.")    
    version: int | None = Field(ge=2, le=3, default=2, description="IGMP snooping querying version.")
class ManagedSwitchIgmpSnooping(BaseModel):
    """
    Child table model for igmp-snooping.
    
    Configure FortiSwitch IGMP snooping global settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    local_override: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable overriding the global IGMP snooping configuration.")    
    aging_time: int | None = Field(ge=15, le=3600, default=300, description="Maximum time to retain a multicast snooping entry for which no packets have been seen (15 - 3600 sec, default = 300).")    
    flood_unknown_multicast: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable unknown multicast flooding.")    
    vlans: list[ManagedSwitchIgmpSnoopingVlans] = Field(default_factory=list, description="Configure IGMP snooping VLAN.")
class ManagedSwitchDhcpSnoopingStaticClient(BaseModel):
    """
    Child table model for dhcp-snooping-static-client.
    
    Configure FortiSwitch DHCP snooping static clients.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=35, default=None, description="Client name.")    
    vlan: str = Field(max_length=15, description="VLAN name.")  # datasource: ['system.interface.name']    
    ip: str = Field(default="0.0.0.0", description="Client static IP address.")    
    mac: str = Field(default="00:00:00:00:00:00", description="Client MAC address.")    
    port: str = Field(max_length=15, description="Interface name.")
class ManagedSwitchCustomCommand(BaseModel):
    """
    Child table model for custom-command.
    
    Configuration method to edit FortiSwitch commands to be pushed to this FortiSwitch device upon rebooting the FortiGate switch controller or the FortiSwitch.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    command_entry: str | None = Field(max_length=35, default=None, description="List of FortiSwitch commands.")    
    command_name: str = Field(max_length=35, description="Names of commands to be pushed to this FortiSwitch device, as configured under config switch-controller custom-command.")  # datasource: ['switch-controller.custom-command.command-name']
class ManagedSwitch8021XSettings(BaseModel):
    """
    Child table model for 802-1X-settings.
    
    Configuration method to edit FortiSwitch 802.1X global settings.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    local_override: Literal["enable", "disable"] | None = Field(default="disable", description="Enable to override global 802.1X settings on individual FortiSwitches.")    
    link_down_auth: Literal["set-unauth", "no-action"] | None = Field(default="set-unauth", description="Authentication state to set if a link is down.")    
    reauth_period: int | None = Field(ge=0, le=1440, default=60, description="Reauthentication time interval (1 - 1440 min, default = 60, 0 = disable).")    
    max_reauth_attempt: int | None = Field(ge=0, le=15, default=3, description="Maximum number of authentication attempts (0 - 15, default = 3).")    
    tx_period: int | None = Field(ge=12, le=60, default=30, description="802.1X Tx period (seconds, default=30).")    
    mab_reauth: Literal["disable", "enable"] | None = Field(default="disable", description="Enable or disable MAB reauthentication settings.")    
    mac_username_delimiter: ManagedSwitch8021XSettingsMacUsernameDelimiterEnum | None = Field(default=ManagedSwitch8021XSettingsMacUsernameDelimiterEnum.HYPHEN, description="MAC authentication username delimiter (default = hyphen).")    
    mac_password_delimiter: ManagedSwitch8021XSettingsMacPasswordDelimiterEnum | None = Field(default=ManagedSwitch8021XSettingsMacPasswordDelimiterEnum.HYPHEN, description="MAC authentication password delimiter (default = hyphen).")    
    mac_calling_station_delimiter: ManagedSwitch8021XSettingsMacCallingStationDelimiterEnum | None = Field(default=ManagedSwitch8021XSettingsMacCallingStationDelimiterEnum.HYPHEN, description="MAC calling station delimiter (default = hyphen).")    
    mac_called_station_delimiter: ManagedSwitch8021XSettingsMacCalledStationDelimiterEnum | None = Field(default=ManagedSwitch8021XSettingsMacCalledStationDelimiterEnum.HYPHEN, description="MAC called station delimiter (default = hyphen).")    
    mac_case: Literal["lowercase", "uppercase"] | None = Field(default="lowercase", description="MAC case (default = lowercase).")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class ManagedSwitchPurdueLevelEnum(str, Enum):
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

class ManagedSwitchModel(BaseModel):
    """
    Pydantic model for switch_controller/managed_switch configuration.
    
    Configure FortiSwitch devices that are managed by this FortiGate.
    
    Validation Rules:        - switch_id: max_length=35 pattern=        - sn: max_length=16 pattern=        - description: max_length=63 pattern=        - switch_profile: max_length=35 pattern=        - access_profile: max_length=31 pattern=        - purdue_level: pattern=        - fsw_wan1_peer: max_length=35 pattern=        - fsw_wan1_admin: pattern=        - poe_pre_standard_detection: pattern=        - dhcp_server_access_list: pattern=        - poe_detection_type: min=0 max=255 pattern=        - max_poe_budget: min=0 max=65535 pattern=        - directly_connected: min=0 max=1 pattern=        - version: min=0 max=255 pattern=        - max_allowed_trunk_members: min=0 max=255 pattern=        - pre_provisioned: min=0 max=255 pattern=        - l3_discovered: min=0 max=1 pattern=        - mgmt_mode: min=0 max=255 pattern=        - tunnel_discovered: min=0 max=1 pattern=        - tdr_supported: max_length=31 pattern=        - dynamic_capability: pattern=        - switch_device_tag: max_length=32 pattern=        - switch_dhcp_opt43_key: max_length=63 pattern=        - mclag_igmp_snooping_aware: pattern=        - dynamically_discovered: min=0 max=1 pattern=        - ptp_status: pattern=        - ptp_profile: max_length=63 pattern=        - radius_nas_ip_override: pattern=        - radius_nas_ip: pattern=        - route_offload: pattern=        - route_offload_mclag: pattern=        - route_offload_router: pattern=        - vlan: pattern=        - type_: pattern=        - owner_vdom: max_length=31 pattern=        - flow_identity: pattern=        - staged_image_version: max_length=127 pattern=        - delayed_restart_trigger: min=0 max=255 pattern=        - firmware_provision: pattern=        - firmware_provision_version: max_length=35 pattern=        - firmware_provision_latest: pattern=        - ports: pattern=        - ip_source_guard: pattern=        - stp_settings: pattern=        - stp_instance: pattern=        - override_snmp_sysinfo: pattern=        - snmp_sysinfo: pattern=        - override_snmp_trap_threshold: pattern=        - snmp_trap_threshold: pattern=        - override_snmp_community: pattern=        - snmp_community: pattern=        - override_snmp_user: pattern=        - snmp_user: pattern=        - qos_drop_policy: pattern=        - qos_red_probability: min=0 max=100 pattern=        - switch_log: pattern=        - remote_log: pattern=        - storm_control: pattern=        - mirror: pattern=        - static_mac: pattern=        - custom_command: pattern=        - dhcp_snooping_static_client: pattern=        - igmp_snooping: pattern=        - _802_1X_settings: pattern=        - router_vrf: pattern=        - system_interface: pattern=        - router_static: pattern=        - system_dhcp_server: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    switch_id: str = Field(max_length=35, description="Managed-switch name.")    
    sn: str = Field(max_length=16, description="Managed-switch serial number.")    
    description: str | None = Field(max_length=63, default=None, description="Description.")    
    switch_profile: str | None = Field(max_length=35, default="default", description="FortiSwitch profile.")  # datasource: ['switch-controller.switch-profile.name']    
    access_profile: str | None = Field(max_length=31, default="default", description="FortiSwitch access profile.")  # datasource: ['switch-controller.security-policy.local-access.name']    
    purdue_level: ManagedSwitchPurdueLevelEnum | None = Field(default=ManagedSwitchPurdueLevelEnum.V_3, description="Purdue Level of this FortiSwitch.")    
    fsw_wan1_peer: str = Field(max_length=35, description="FortiSwitch WAN1 peer port.")  # datasource: ['system.interface.name']    
    fsw_wan1_admin: Literal["discovered", "disable", "enable"] | None = Field(default="discovered", description="FortiSwitch WAN1 admin status; enable to authorize the FortiSwitch as a managed switch.")    
    poe_pre_standard_detection: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable PoE pre-standard detection.")    
    dhcp_server_access_list: Literal["global", "enable", "disable"] | None = Field(default="global", description="DHCP snooping server access list.")    
    poe_detection_type: int | None = Field(ge=0, le=255, default=0, description="PoE detection type for FortiSwitch.")    
    max_poe_budget: int | None = Field(ge=0, le=65535, default=0, description="Max PoE budget for FortiSwitch.")    
    directly_connected: int | None = Field(ge=0, le=1, default=0, description="Directly connected FortiSwitch.")    
    version: int | None = Field(ge=0, le=255, default=0, description="FortiSwitch version.")    
    max_allowed_trunk_members: int | None = Field(ge=0, le=255, default=0, description="FortiSwitch maximum allowed trunk members.")    
    pre_provisioned: int | None = Field(ge=0, le=255, default=0, description="Pre-provisioned managed switch.")    
    l3_discovered: int | None = Field(ge=0, le=1, default=0, description="Layer 3 management discovered.")    
    mgmt_mode: int | None = Field(ge=0, le=255, default=0, description="FortiLink management mode.")    
    tunnel_discovered: int | None = Field(ge=0, le=1, default=0, description="SOCKS tunnel management discovered.")    
    tdr_supported: str | None = Field(max_length=31, default=None, description="TDR supported.")    
    dynamic_capability: str | None = Field(default="0x00000000000000000000000000000000", description="List of features this FortiSwitch supports (not configurable) that is sent to the FortiGate device for subsequent configuration initiated by the FortiGate device.")    
    switch_device_tag: str | None = Field(max_length=32, default=None, description="User definable label/tag.")    
    switch_dhcp_opt43_key: str | None = Field(max_length=63, default=None, description="DHCP option43 key.")    
    mclag_igmp_snooping_aware: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable MCLAG IGMP-snooping awareness.")    
    dynamically_discovered: int | None = Field(ge=0, le=1, default=0, description="Dynamically discovered FortiSwitch.")    
    ptp_status: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable PTP profile on this FortiSwitch.")    
    ptp_profile: str | None = Field(max_length=63, default="default", description="PTP profile configuration.")  # datasource: ['switch-controller.ptp.profile.name']    
    radius_nas_ip_override: Literal["disable", "enable"] | None = Field(default="disable", description="Use locally defined NAS-IP.")    
    radius_nas_ip: str = Field(default="0.0.0.0", description="NAS-IP address.")    
    route_offload: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable route offload on this FortiSwitch.")    
    route_offload_mclag: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable route offload MCLAG on this FortiSwitch.")    
    route_offload_router: list[ManagedSwitchRouteOffloadRouter] = Field(default_factory=list, description="Configure route offload MCLAG IP address.")    
    vlan: list[ManagedSwitchVlan] = Field(default_factory=list, description="Configure VLAN assignment priority.")    
    type_: Literal["virtual", "physical"] | None = Field(default="physical", serialization_alias="type", description="Indication of switch type, physical or virtual.")    
    owner_vdom: str | None = Field(max_length=31, default=None, description="VDOM which owner of port belongs to.")    
    flow_identity: str | None = Field(default="00000000", description="Flow-tracking netflow ipfix switch identity in hex format(00000000-FFFFFFFF default=0).")    
    staged_image_version: str | None = Field(max_length=127, default=None, description="Staged image version for FortiSwitch.")    
    delayed_restart_trigger: int | None = Field(ge=0, le=255, default=0, description="Delayed restart triggered for this FortiSwitch.")    
    firmware_provision: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable provisioning of firmware to FortiSwitches on join connection.")    
    firmware_provision_version: str | None = Field(max_length=35, default=None, description="Firmware version to provision to this FortiSwitch on bootup (major.minor.build, i.e. 6.2.1234).")    
    firmware_provision_latest: Literal["disable", "once"] | None = Field(default="disable", description="Enable/disable one-time automatic provisioning of the latest firmware version.")    
    ports: list[ManagedSwitchPorts] = Field(default_factory=list, description="Managed-switch port list.")    
    ip_source_guard: list[ManagedSwitchIpSourceGuard] = Field(default_factory=list, description="IP source guard.")    
    stp_settings: ManagedSwitchStpSettings | None = Field(default=None, description="Configuration method to edit Spanning Tree Protocol (STP) settings used to prevent bridge loops.")    
    stp_instance: list[ManagedSwitchStpInstance] = Field(default_factory=list, description="Configuration method to edit Spanning Tree Protocol (STP) instances.")    
    override_snmp_sysinfo: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable overriding the global SNMP system information.")    
    snmp_sysinfo: ManagedSwitchSnmpSysinfo | None = Field(default=None, description="Configuration method to edit Simple Network Management Protocol (SNMP) system info.")    
    override_snmp_trap_threshold: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable overriding the global SNMP trap threshold values.")    
    snmp_trap_threshold: ManagedSwitchSnmpTrapThreshold | None = Field(default=None, description="Configuration method to edit Simple Network Management Protocol (SNMP) trap threshold values.")    
    override_snmp_community: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable overriding the global SNMP communities.")    
    snmp_community: list[ManagedSwitchSnmpCommunity] = Field(default_factory=list, description="Configuration method to edit Simple Network Management Protocol (SNMP) communities.")    
    override_snmp_user: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable overriding the global SNMP users.")    
    snmp_user: list[ManagedSwitchSnmpUser] = Field(default_factory=list, description="Configuration method to edit Simple Network Management Protocol (SNMP) users.")    
    qos_drop_policy: Literal["taildrop", "random-early-detection"] | None = Field(default="taildrop", description="Set QoS drop-policy.")    
    qos_red_probability: int | None = Field(ge=0, le=100, default=12, description="Set QoS RED/WRED drop probability.")    
    switch_log: ManagedSwitchSwitchLog | None = Field(default=None, description="Configuration method to edit FortiSwitch logging settings (logs are transferred to and inserted into the FortiGate event log).")    
    remote_log: list[ManagedSwitchRemoteLog] = Field(default_factory=list, description="Configure logging by FortiSwitch device to a remote syslog server.")    
    storm_control: ManagedSwitchStormControl | None = Field(default=None, description="Configuration method to edit FortiSwitch storm control for measuring traffic activity using data rates to prevent traffic disruption.")    
    mirror: list[ManagedSwitchMirror] = Field(default_factory=list, description="Configuration method to edit FortiSwitch packet mirror.")    
    static_mac: list[ManagedSwitchStaticMac] = Field(default_factory=list, description="Configuration method to edit FortiSwitch Static and Sticky MAC.")    
    custom_command: list[ManagedSwitchCustomCommand] = Field(default_factory=list, description="Configuration method to edit FortiSwitch commands to be pushed to this FortiSwitch device upon rebooting the FortiGate switch controller or the FortiSwitch.")    
    dhcp_snooping_static_client: list[ManagedSwitchDhcpSnoopingStaticClient] = Field(default_factory=list, description="Configure FortiSwitch DHCP snooping static clients.")    
    igmp_snooping: ManagedSwitchIgmpSnooping | None = Field(default=None, description="Configure FortiSwitch IGMP snooping global settings.")    
    _802_1X_settings: ManagedSwitch8021XSettings | None = Field(default=None, serialization_alias="802-1X-settings", description="Configuration method to edit FortiSwitch 802.1X global settings.")    
    router_vrf: list[ManagedSwitchRouterVrf] = Field(default_factory=list, description="Configure VRF.")    
    system_interface: list[ManagedSwitchSystemInterface] = Field(default_factory=list, description="Configure system interface on FortiSwitch.")    
    router_static: list[ManagedSwitchRouterStatic] = Field(default_factory=list, description="Configure static routes.")    
    system_dhcp_server: list[ManagedSwitchSystemDhcpServer] = Field(default_factory=list, description="Configure DHCP servers.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('switch_profile')
    @classmethod
    def validate_switch_profile(cls, v: Any) -> Any:
        """
        Validate switch_profile field.
        
        Datasource: ['switch-controller.switch-profile.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('access_profile')
    @classmethod
    def validate_access_profile(cls, v: Any) -> Any:
        """
        Validate access_profile field.
        
        Datasource: ['switch-controller.security-policy.local-access.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('fsw_wan1_peer')
    @classmethod
    def validate_fsw_wan1_peer(cls, v: Any) -> Any:
        """
        Validate fsw_wan1_peer field.
        
        Datasource: ['system.interface.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('ptp_profile')
    @classmethod
    def validate_ptp_profile(cls, v: Any) -> Any:
        """
        Validate ptp_profile field.
        
        Datasource: ['switch-controller.ptp.profile.name']
        
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "ManagedSwitchModel":
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
    async def validate_switch_profile_references(self, client: Any) -> list[str]:
        """
        Validate switch_profile references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - switch-controller/switch-profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ManagedSwitchModel(
            ...     switch_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_switch_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "switch_profile", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.switch_controller.switch_profile.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Switch-Profile '{value}' not found in "
                "switch-controller/switch-profile"
            )        
        return errors    
    async def validate_access_profile_references(self, client: Any) -> list[str]:
        """
        Validate access_profile references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - switch-controller/security-policy/local-access        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ManagedSwitchModel(
            ...     access_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_access_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "access_profile", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.switch_controller.security_policy.local_access.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Access-Profile '{value}' not found in "
                "switch-controller/security-policy/local-access"
            )        
        return errors    
    async def validate_fsw_wan1_peer_references(self, client: Any) -> list[str]:
        """
        Validate fsw_wan1_peer references exist in FortiGate.
        
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
            >>> policy = ManagedSwitchModel(
            ...     fsw_wan1_peer="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_fsw_wan1_peer_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "fsw_wan1_peer", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.system.interface.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Fsw-Wan1-Peer '{value}' not found in "
                "system/interface"
            )        
        return errors    
    async def validate_ptp_profile_references(self, client: Any) -> list[str]:
        """
        Validate ptp_profile references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - switch-controller/ptp/profile        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ManagedSwitchModel(
            ...     ptp_profile="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_ptp_profile_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "ptp_profile", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.switch_controller.ptp.profile.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Ptp-Profile '{value}' not found in "
                "switch-controller/ptp/profile"
            )        
        return errors    
    async def validate_route_offload_router_references(self, client: Any) -> list[str]:
        """
        Validate route_offload_router references exist in FortiGate.
        
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
            >>> policy = ManagedSwitchModel(
            ...     route_offload_router=[{"vlan-name": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_route_offload_router_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "route_offload_router", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("vlan-name")
            else:
                value = getattr(item, "vlan-name", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.system.interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Route-Offload-Router '{value}' not found in "
                    "system/interface"
                )        
        return errors    
    async def validate_vlan_references(self, client: Any) -> list[str]:
        """
        Validate vlan references exist in FortiGate.
        
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
            >>> policy = ManagedSwitchModel(
            ...     vlan=[{"vlan-name": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_vlan_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "vlan", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("vlan-name")
            else:
                value = getattr(item, "vlan-name", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.system.interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Vlan '{value}' not found in "
                    "system/interface"
                )        
        return errors    
    async def validate_ports_references(self, client: Any) -> list[str]:
        """
        Validate ports references exist in FortiGate.
        
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
            >>> policy = ManagedSwitchModel(
            ...     ports=[{"qnq": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_ports_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "ports", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("qnq")
            else:
                value = getattr(item, "qnq", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.system.interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Ports '{value}' not found in "
                    "system/interface"
                )        
        return errors    
    async def validate_static_mac_references(self, client: Any) -> list[str]:
        """
        Validate static_mac references exist in FortiGate.
        
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
            >>> policy = ManagedSwitchModel(
            ...     static_mac=[{"vlan": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_static_mac_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "static_mac", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("vlan")
            else:
                value = getattr(item, "vlan", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.system.interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Static-Mac '{value}' not found in "
                    "system/interface"
                )        
        return errors    
    async def validate_custom_command_references(self, client: Any) -> list[str]:
        """
        Validate custom_command references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - switch-controller/custom-command        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ManagedSwitchModel(
            ...     custom_command=[{"command-name": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_custom_command_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "custom_command", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("command-name")
            else:
                value = getattr(item, "command-name", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.switch_controller.custom_command.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Custom-Command '{value}' not found in "
                    "switch-controller/custom-command"
                )        
        return errors    
    async def validate_dhcp_snooping_static_client_references(self, client: Any) -> list[str]:
        """
        Validate dhcp_snooping_static_client references exist in FortiGate.
        
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
            >>> policy = ManagedSwitchModel(
            ...     dhcp_snooping_static_client=[{"vlan": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_dhcp_snooping_static_client_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "dhcp_snooping_static_client", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("vlan")
            else:
                value = getattr(item, "vlan", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.system.interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Dhcp-Snooping-Static-Client '{value}' not found in "
                    "system/interface"
                )        
        return errors    
    async def validate_router_vrf_references(self, client: Any) -> list[str]:
        """
        Validate router_vrf references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - switch-controller/managed-switch        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ManagedSwitchModel(
            ...     router_vrf=[{"switch-id": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_router_vrf_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "router_vrf", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("switch-id")
            else:
                value = getattr(item, "switch-id", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.switch_controller.managed_switch.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Router-Vrf '{value}' not found in "
                    "switch-controller/managed-switch"
                )        
        return errors    
    async def validate_system_interface_references(self, client: Any) -> list[str]:
        """
        Validate system_interface references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - switch-controller/managed-switch/router-vrf        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ManagedSwitchModel(
            ...     system_interface=[{"vrf": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_system_interface_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "system_interface", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("vrf")
            else:
                value = getattr(item, "vrf", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.switch_controller.managed_switch.router_vrf.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"System-Interface '{value}' not found in "
                    "switch-controller/managed-switch/router-vrf"
                )        
        return errors    
    async def validate_router_static_references(self, client: Any) -> list[str]:
        """
        Validate router_static references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - switch-controller/managed-switch/router-vrf        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ManagedSwitchModel(
            ...     router_static=[{"vrf": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_router_static_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "router_static", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("vrf")
            else:
                value = getattr(item, "vrf", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.switch_controller.managed_switch.router_vrf.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Router-Static '{value}' not found in "
                    "switch-controller/managed-switch/router-vrf"
                )        
        return errors    
    async def validate_system_dhcp_server_references(self, client: Any) -> list[str]:
        """
        Validate system_dhcp_server references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - switch-controller/managed-switch/system-interface        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = ManagedSwitchModel(
            ...     system_dhcp_server=[{"interface": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_system_dhcp_server_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.switch_controller.managed_switch.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "system_dhcp_server", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("interface")
            else:
                value = getattr(item, "interface", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.switch_controller.managed_switch.system_interface.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"System-Dhcp-Server '{value}' not found in "
                    "switch-controller/managed-switch/system-interface"
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
        
        errors = await self.validate_switch_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_access_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_fsw_wan1_peer_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_ptp_profile_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_route_offload_router_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_vlan_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_ports_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_static_mac_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_custom_command_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_dhcp_snooping_static_client_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_router_vrf_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_system_interface_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_router_static_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_system_dhcp_server_references(client)
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
    "ManagedSwitchModel",    "ManagedSwitchRouteOffloadRouter",    "ManagedSwitchVlan",    "ManagedSwitchPorts",    "ManagedSwitchPorts.AllowedVlans",    "ManagedSwitchPorts.UntaggedVlans",    "ManagedSwitchPorts.AclGroup",    "ManagedSwitchPorts.FortiswitchAcls",    "ManagedSwitchPorts.DhcpSnoopOption82Override",    "ManagedSwitchPorts.InterfaceTags",    "ManagedSwitchPorts.Members",    "ManagedSwitchIpSourceGuard",    "ManagedSwitchIpSourceGuard.BindingEntry",    "ManagedSwitchStpSettings",    "ManagedSwitchStpInstance",    "ManagedSwitchSnmpSysinfo",    "ManagedSwitchSnmpTrapThreshold",    "ManagedSwitchSnmpCommunity",    "ManagedSwitchSnmpCommunity.Hosts",    "ManagedSwitchSnmpUser",    "ManagedSwitchSwitchLog",    "ManagedSwitchRemoteLog",    "ManagedSwitchStormControl",    "ManagedSwitchMirror",    "ManagedSwitchMirror.SrcIngress",    "ManagedSwitchMirror.SrcEgress",    "ManagedSwitchStaticMac",    "ManagedSwitchCustomCommand",    "ManagedSwitchDhcpSnoopingStaticClient",    "ManagedSwitchIgmpSnooping",    "ManagedSwitchIgmpSnooping.Vlans",    "ManagedSwitch8021XSettings",    "ManagedSwitchRouterVrf",    "ManagedSwitchSystemInterface",    "ManagedSwitchRouterStatic",    "ManagedSwitchSystemDhcpServer",    "ManagedSwitchSystemDhcpServer.IpRange",    "ManagedSwitchSystemDhcpServer.Options",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:29.217383Z
# ============================================================================