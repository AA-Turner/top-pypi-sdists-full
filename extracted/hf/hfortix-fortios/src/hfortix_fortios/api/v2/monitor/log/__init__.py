"""FortiOS CMDB - Log category"""

from . import av_archive
from . import device
from . import forticloud
from . import forticloud_report
from . import local_report
from . import policy_archive
from . import stats
from .current_disk_usage import CurrentDiskUsage
from .feature_set import FeatureSet
from .fortianalyzer import Fortianalyzer
from .fortianalyzer_queue import FortianalyzerQueue
from .forticloud_report_list import ForticloudReportList
from .historic_daily_remote_logs import HistoricDailyRemoteLogs
from .hourly_disk_usage import HourlyDiskUsage
from .local_report_list import LocalReportList

__all__ = [
    "AvArchive",
    "CurrentDiskUsage",
    "Device",
    "FeatureSet",
    "Fortianalyzer",
    "FortianalyzerQueue",
    "Forticloud",
    "ForticloudReport",
    "ForticloudReportList",
    "HistoricDailyRemoteLogs",
    "HourlyDiskUsage",
    "LocalReport",
    "LocalReportList",
    "Log",
    "PolicyArchive",
    "Stats",
]


class Log:
    """Log endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Log endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.av_archive = av_archive.AvArchive(client)
        self.device = device.Device(client)
        self.forticloud = forticloud.Forticloud(client)
        self.forticloud_report = forticloud_report.ForticloudReport(client)
        self.local_report = local_report.LocalReport(client)
        self.policy_archive = policy_archive.PolicyArchive(client)
        self.stats = stats.Stats(client)
        self.current_disk_usage = CurrentDiskUsage(client)
        self.feature_set = FeatureSet(client)
        self.fortianalyzer = Fortianalyzer(client)
        self.fortianalyzer_queue = FortianalyzerQueue(client)
        self.forticloud_report_list = ForticloudReportList(client)
        self.historic_daily_remote_logs = HistoricDailyRemoteLogs(client)
        self.hourly_disk_usage = HourlyDiskUsage(client)
        self.local_report_list = LocalReportList(client)
