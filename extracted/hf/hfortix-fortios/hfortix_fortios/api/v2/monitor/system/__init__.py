"""FortiOS CMDB - System category"""

from . import admin
from . import api_user
from . import automation_action
from . import automation_stitch
from . import available_interfaces
from . import botnet
from . import botnet_domains
from . import central_management
from . import certificate
from . import change_password
from . import cluster
from . import com_log
from . import config
from . import config_error_log
from . import config_revision
from . import config_script
from . import config_sync
from . import crash_log
from . import csf
from . import debug
from . import dhcp
from . import dhcp6
from . import disconnect_admins
from . import external_resource
from . import firmware
from . import fortiguard
from . import fortimanager
from . import fsck
from . import ha_peer
from . import hscalefw_license
from . import interface
from . import ipam
from . import logdisk
from . import lte_modem
from . import modem
from . import modem5g
from . import ntp
from . import object
from . import os
from . import password_policy_conform
from . import performance
from . import private_data_encryption
from . import process
from . import resource
from . import sandbox
from . import sdn_connector
from . import time
from . import traffic_history
from . import upgrade_report
from . import usb_device
from . import usb_log
from . import vmlicense
from .acme_certificate_status import AcmeCertificateStatus
from .acquired_dns import AcquiredDns
from .available_certificates import AvailableCertificates
from .check_port_availability import CheckPortAvailability
from .current_admins import CurrentAdmins
from .global_resources import GlobalResources
from .global_search import GlobalSearch
from .ha_backup_hb_used import HaBackupHbUsed
from .ha_checksums import HaChecksums
from .ha_history import HaHistory
from .ha_hw_interface import HaHwInterface
from .ha_nonsync_checksums import HaNonsyncChecksums
from .ha_statistics import HaStatistics
from .ha_table_checksums import HaTableChecksums
from .interface_connected_admins_info import InterfaceConnectedAdminsInfo
from .ipconf import Ipconf
from .link_monitor import LinkMonitor
from .modem3g import Modem3g
from .monitor_sensor import MonitorSensor
from .resolve_fqdn import ResolveFqdn
from .running_processes import RunningProcesses
from .sensor_info import SensorInfo
from .status import Status
from .storage import Storage
from .timezone import Timezone
from .trusted_cert_authorities import TrustedCertAuthorities
from .vdom_link import VdomLink
from .vdom_resource import VdomResource
from .vm_information import VmInformation

__all__ = [
    "AcmeCertificateStatus",
    "AcquiredDns",
    "Admin",
    "ApiUser",
    "AutomationAction",
    "AutomationStitch",
    "AvailableCertificates",
    "AvailableInterfaces",
    "Botnet",
    "BotnetDomains",
    "CentralManagement",
    "Certificate",
    "ChangePassword",
    "CheckPortAvailability",
    "Cluster",
    "ComLog",
    "Config",
    "ConfigErrorLog",
    "ConfigRevision",
    "ConfigScript",
    "ConfigSync",
    "CrashLog",
    "Csf",
    "CurrentAdmins",
    "Debug",
    "Dhcp",
    "Dhcp6",
    "DisconnectAdmins",
    "ExternalResource",
    "Firmware",
    "Fortiguard",
    "Fortimanager",
    "Fsck",
    "GlobalResources",
    "GlobalSearch",
    "HaBackupHbUsed",
    "HaChecksums",
    "HaHistory",
    "HaHwInterface",
    "HaNonsyncChecksums",
    "HaPeer",
    "HaStatistics",
    "HaTableChecksums",
    "HscalefwLicense",
    "Interface",
    "InterfaceConnectedAdminsInfo",
    "Ipam",
    "Ipconf",
    "LinkMonitor",
    "Logdisk",
    "LteModem",
    "Modem",
    "Modem3g",
    "Modem5g",
    "MonitorSensor",
    "Ntp",
    "Object",
    "Os",
    "PasswordPolicyConform",
    "Performance",
    "PrivateDataEncryption",
    "Process",
    "ResolveFqdn",
    "Resource",
    "RunningProcesses",
    "Sandbox",
    "SdnConnector",
    "SensorInfo",
    "Status",
    "Storage",
    "System",
    "Time",
    "Timezone",
    "TrafficHistory",
    "TrustedCertAuthorities",
    "UpgradeReport",
    "UsbDevice",
    "UsbLog",
    "VdomLink",
    "VdomResource",
    "VmInformation",
    "Vmlicense",
]


class System:
    """System endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """System endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.admin = admin.Admin(client)
        self.api_user = api_user.ApiUser(client)
        self.automation_action = automation_action.AutomationAction(client)
        self.automation_stitch = automation_stitch.AutomationStitch(client)
        self.available_interfaces = available_interfaces.AvailableInterfaces(client)
        self.botnet = botnet.Botnet(client)
        self.botnet_domains = botnet_domains.BotnetDomains(client)
        self.central_management = central_management.CentralManagement(client)
        self.certificate = certificate.Certificate(client)
        self.change_password = change_password.ChangePassword(client)
        self.cluster = cluster.Cluster(client)
        self.com_log = com_log.ComLog(client)
        self.config = config.Config(client)
        self.config_error_log = config_error_log.ConfigErrorLog(client)
        self.config_revision = config_revision.ConfigRevision(client)
        self.config_script = config_script.ConfigScript(client)
        self.config_sync = config_sync.ConfigSync(client)
        self.crash_log = crash_log.CrashLog(client)
        self.csf = csf.Csf(client)
        self.debug = debug.Debug(client)
        self.dhcp = dhcp.Dhcp(client)
        self.dhcp6 = dhcp6.Dhcp6(client)
        self.disconnect_admins = disconnect_admins.DisconnectAdmins(client)
        self.external_resource = external_resource.ExternalResource(client)
        self.firmware = firmware.Firmware(client)
        self.fortiguard = fortiguard.Fortiguard(client)
        self.fortimanager = fortimanager.Fortimanager(client)
        self.fsck = fsck.Fsck(client)
        self.ha_peer = ha_peer.HaPeer(client)
        self.hscalefw_license = hscalefw_license.HscalefwLicense(client)
        self.interface = interface.Interface(client)
        self.ipam = ipam.Ipam(client)
        self.logdisk = logdisk.Logdisk(client)
        self.lte_modem = lte_modem.LteModem(client)
        self.modem = modem.Modem(client)
        self.modem5g = modem5g.Modem5g(client)
        self.ntp = ntp.Ntp(client)
        self.object = object.Object(client)
        self.os = os.Os(client)
        self.password_policy_conform = password_policy_conform.PasswordPolicyConform(client)
        self.performance = performance.Performance(client)
        self.private_data_encryption = private_data_encryption.PrivateDataEncryption(client)
        self.process = process.Process(client)
        self.resource = resource.Resource(client)
        self.sandbox = sandbox.Sandbox(client)
        self.sdn_connector = sdn_connector.SdnConnector(client)
        self.time = time.Time(client)
        self.traffic_history = traffic_history.TrafficHistory(client)
        self.upgrade_report = upgrade_report.UpgradeReport(client)
        self.usb_device = usb_device.UsbDevice(client)
        self.usb_log = usb_log.UsbLog(client)
        self.vmlicense = vmlicense.Vmlicense(client)
        self.acme_certificate_status = AcmeCertificateStatus(client)
        self.acquired_dns = AcquiredDns(client)
        self.available_certificates = AvailableCertificates(client)
        self.check_port_availability = CheckPortAvailability(client)
        self.current_admins = CurrentAdmins(client)
        self.global_resources = GlobalResources(client)
        self.global_search = GlobalSearch(client)
        self.ha_backup_hb_used = HaBackupHbUsed(client)
        self.ha_checksums = HaChecksums(client)
        self.ha_history = HaHistory(client)
        self.ha_hw_interface = HaHwInterface(client)
        self.ha_nonsync_checksums = HaNonsyncChecksums(client)
        self.ha_statistics = HaStatistics(client)
        self.ha_table_checksums = HaTableChecksums(client)
        self.interface_connected_admins_info = InterfaceConnectedAdminsInfo(client)
        self.ipconf = Ipconf(client)
        self.link_monitor = LinkMonitor(client)
        self.modem3g = Modem3g(client)
        self.monitor_sensor = MonitorSensor(client)
        self.resolve_fqdn = ResolveFqdn(client)
        self.running_processes = RunningProcesses(client)
        self.sensor_info = SensorInfo(client)
        self.status = Status(client)
        self.storage = Storage(client)
        self.timezone = Timezone(client)
        self.trusted_cert_authorities = TrustedCertAuthorities(client)
        self.vdom_link = VdomLink(client)
        self.vdom_resource = VdomResource(client)
        self.vm_information = VmInformation(client)
