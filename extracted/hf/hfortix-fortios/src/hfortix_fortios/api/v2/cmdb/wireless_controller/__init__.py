"""FortiOS CMDB - WirelessController category"""

from . import hotspot20
from .access_control_list import AccessControlList
from .ap_status import ApStatus
from .apcfg_profile import ApcfgProfile
from .arrp_profile import ArrpProfile
from .ble_profile import BleProfile
from .bonjour_profile import BonjourProfile
from .global_ import Global
from .inter_controller import InterController
from .log import Log
from .lw_profile import LwProfile
from .mpsk_profile import MpskProfile
from .nac_profile import NacProfile
from .qos_profile import QosProfile
from .region import Region
from .setting import Setting
from .snmp import Snmp
from .ssid_policy import SsidPolicy
from .syslog_profile import SyslogProfile
from .timers import Timers
from .utm_profile import UtmProfile
from .vap import Vap
from .vap_group import VapGroup
from .wag_profile import WagProfile
from .wids_profile import WidsProfile
from .wtp import Wtp
from .wtp_group import WtpGroup
from .wtp_profile import WtpProfile

__all__ = [
    "AccessControlList",
    "ApStatus",
    "ApcfgProfile",
    "ArrpProfile",
    "BleProfile",
    "BonjourProfile",
    "Global",
    "Hotspot20",
    "InterController",
    "Log",
    "LwProfile",
    "MpskProfile",
    "NacProfile",
    "QosProfile",
    "Region",
    "Setting",
    "Snmp",
    "SsidPolicy",
    "SyslogProfile",
    "Timers",
    "UtmProfile",
    "Vap",
    "VapGroup",
    "WagProfile",
    "WidsProfile",
    "WirelessController",
    "Wtp",
    "WtpGroup",
    "WtpProfile",
]


class WirelessController:
    """WirelessController endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """WirelessController endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.hotspot20 = hotspot20.Hotspot20(client)
        self.access_control_list = AccessControlList(client)
        self.ap_status = ApStatus(client)
        self.apcfg_profile = ApcfgProfile(client)
        self.arrp_profile = ArrpProfile(client)
        self.ble_profile = BleProfile(client)
        self.bonjour_profile = BonjourProfile(client)
        self.global_ = Global(client)
        self.inter_controller = InterController(client)
        self.log = Log(client)
        self.lw_profile = LwProfile(client)
        self.mpsk_profile = MpskProfile(client)
        self.nac_profile = NacProfile(client)
        self.qos_profile = QosProfile(client)
        self.region = Region(client)
        self.setting = Setting(client)
        self.snmp = Snmp(client)
        self.ssid_policy = SsidPolicy(client)
        self.syslog_profile = SyslogProfile(client)
        self.timers = Timers(client)
        self.utm_profile = UtmProfile(client)
        self.vap = Vap(client)
        self.vap_group = VapGroup(client)
        self.wag_profile = WagProfile(client)
        self.wids_profile = WidsProfile(client)
        self.wtp = Wtp(client)
        self.wtp_group = WtpGroup(client)
        self.wtp_profile = WtpProfile(client)
