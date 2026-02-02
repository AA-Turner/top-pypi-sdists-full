"""FortiOS CMDB - SwitchController category"""

from . import acl
from . import auto_config
from . import initial_config
from . import ptp
from . import qos
from . import security_policy
from .custom_command import CustomCommand
from .dynamic_port_policy import DynamicPortPolicy
from .flow_tracking import FlowTracking
from .fortilink_settings import FortilinkSettings
from .global_ import Global
from .igmp_snooping import IgmpSnooping
from .ip_source_guard_log import IpSourceGuardLog
from .lldp_profile import LldpProfile
from .lldp_settings import LldpSettings
from .location import Location
from .mac_policy import MacPolicy
from .managed_switch import ManagedSwitch
from .network_monitor_settings import NetworkMonitorSettings
from .remote_log import RemoteLog
from .sflow import Sflow
from .snmp_community import SnmpCommunity
from .snmp_sysinfo import SnmpSysinfo
from .snmp_trap_threshold import SnmpTrapThreshold
from .snmp_user import SnmpUser
from .storm_control import StormControl
from .storm_control_policy import StormControlPolicy
from .stp_instance import StpInstance
from .stp_settings import StpSettings
from .switch_group import SwitchGroup
from .switch_interface_tag import SwitchInterfaceTag
from .switch_log import SwitchLog
from .switch_profile import SwitchProfile
from .system import System
from .traffic_policy import TrafficPolicy
from .traffic_sniffer import TrafficSniffer
from .virtual_port_pool import VirtualPortPool
from .vlan_policy import VlanPolicy
from .x802_1x_settings import X8021xSettings

__all__ = [
    "Acl",
    "AutoConfig",
    "CustomCommand",
    "DynamicPortPolicy",
    "FlowTracking",
    "FortilinkSettings",
    "Global",
    "IgmpSnooping",
    "InitialConfig",
    "IpSourceGuardLog",
    "LldpProfile",
    "LldpSettings",
    "Location",
    "MacPolicy",
    "ManagedSwitch",
    "NetworkMonitorSettings",
    "Ptp",
    "Qos",
    "RemoteLog",
    "SecurityPolicy",
    "Sflow",
    "SnmpCommunity",
    "SnmpSysinfo",
    "SnmpTrapThreshold",
    "SnmpUser",
    "StormControl",
    "StormControlPolicy",
    "StpInstance",
    "StpSettings",
    "SwitchController",
    "SwitchGroup",
    "SwitchInterfaceTag",
    "SwitchLog",
    "SwitchProfile",
    "System",
    "TrafficPolicy",
    "TrafficSniffer",
    "VirtualPortPool",
    "VlanPolicy",
    "X8021xSettings",
]


class SwitchController:
    """SwitchController endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """SwitchController endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.acl = acl.Acl(client)
        self.auto_config = auto_config.AutoConfig(client)
        self.initial_config = initial_config.InitialConfig(client)
        self.ptp = ptp.Ptp(client)
        self.qos = qos.Qos(client)
        self.security_policy = security_policy.SecurityPolicy(client)
        self.custom_command = CustomCommand(client)
        self.dynamic_port_policy = DynamicPortPolicy(client)
        self.flow_tracking = FlowTracking(client)
        self.fortilink_settings = FortilinkSettings(client)
        self.global_ = Global(client)
        self.igmp_snooping = IgmpSnooping(client)
        self.ip_source_guard_log = IpSourceGuardLog(client)
        self.lldp_profile = LldpProfile(client)
        self.lldp_settings = LldpSettings(client)
        self.location = Location(client)
        self.mac_policy = MacPolicy(client)
        self.managed_switch = ManagedSwitch(client)
        self.network_monitor_settings = NetworkMonitorSettings(client)
        self.remote_log = RemoteLog(client)
        self.sflow = Sflow(client)
        self.snmp_community = SnmpCommunity(client)
        self.snmp_sysinfo = SnmpSysinfo(client)
        self.snmp_trap_threshold = SnmpTrapThreshold(client)
        self.snmp_user = SnmpUser(client)
        self.storm_control = StormControl(client)
        self.storm_control_policy = StormControlPolicy(client)
        self.stp_instance = StpInstance(client)
        self.stp_settings = StpSettings(client)
        self.switch_group = SwitchGroup(client)
        self.switch_interface_tag = SwitchInterfaceTag(client)
        self.switch_log = SwitchLog(client)
        self.switch_profile = SwitchProfile(client)
        self.system = System(client)
        self.traffic_policy = TrafficPolicy(client)
        self.traffic_sniffer = TrafficSniffer(client)
        self.virtual_port_pool = VirtualPortPool(client)
        self.vlan_policy = VlanPolicy(client)
        self.x802_1x_settings = X8021xSettings(client)
