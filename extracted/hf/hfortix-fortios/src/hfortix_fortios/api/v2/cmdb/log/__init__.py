"""FortiOS CMDB - Log category"""

from . import disk
from . import fortianalyzer
from . import fortianalyzer2
from . import fortianalyzer3
from . import fortianalyzer_cloud
from . import fortiguard
from . import memory
from . import null_device
from . import syslogd
from . import syslogd2
from . import syslogd3
from . import syslogd4
from . import tacacs_plus_accounting
from . import tacacs_plus_accounting2
from . import tacacs_plus_accounting3
from . import webtrends
from .custom_field import CustomField
from .eventfilter import Eventfilter
from .gui_display import GuiDisplay
from .setting import Setting
from .threat_weight import ThreatWeight

__all__ = [
    "CustomField",
    "Disk",
    "Eventfilter",
    "Fortianalyzer",
    "Fortianalyzer2",
    "Fortianalyzer3",
    "FortianalyzerCloud",
    "Fortiguard",
    "GuiDisplay",
    "Log",
    "Memory",
    "NullDevice",
    "Setting",
    "Syslogd",
    "Syslogd2",
    "Syslogd3",
    "Syslogd4",
    "TacacsPlusAccounting",
    "TacacsPlusAccounting2",
    "TacacsPlusAccounting3",
    "ThreatWeight",
    "Webtrends",
]


class Log:
    """Log endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Log endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.disk = disk.Disk(client)
        self.fortianalyzer = fortianalyzer.Fortianalyzer(client)
        self.fortianalyzer2 = fortianalyzer2.Fortianalyzer2(client)
        self.fortianalyzer3 = fortianalyzer3.Fortianalyzer3(client)
        self.fortianalyzer_cloud = fortianalyzer_cloud.FortianalyzerCloud(client)
        self.fortiguard = fortiguard.Fortiguard(client)
        self.memory = memory.Memory(client)
        self.null_device = null_device.NullDevice(client)
        self.syslogd = syslogd.Syslogd(client)
        self.syslogd2 = syslogd2.Syslogd2(client)
        self.syslogd3 = syslogd3.Syslogd3(client)
        self.syslogd4 = syslogd4.Syslogd4(client)
        self.tacacs_plus_accounting = tacacs_plus_accounting.TacacsPlusAccounting(client)
        self.tacacs_plus_accounting2 = tacacs_plus_accounting2.TacacsPlusAccounting2(client)
        self.tacacs_plus_accounting3 = tacacs_plus_accounting3.TacacsPlusAccounting3(client)
        self.webtrends = webtrends.Webtrends(client)
        self.custom_field = CustomField(client)
        self.eventfilter = Eventfilter(client)
        self.gui_display = GuiDisplay(client)
        self.setting = Setting(client)
        self.threat_weight = ThreatWeight(client)
