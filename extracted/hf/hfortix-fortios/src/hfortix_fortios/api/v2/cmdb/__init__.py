"""FortiOS CMDB - CMDB category"""

from . import alertemail
from . import antivirus
from . import application
from . import authentication
from . import automation
from . import casb
from . import certificate
from . import diameter_filter
from . import dlp
from . import dnsfilter
from . import emailfilter
from . import endpoint_control
from . import ethernet_oam
from . import extension_controller
from . import file_filter
from . import firewall
from . import ftp_proxy
from . import icap
from . import ips
from . import log
from . import monitoring
from . import report
from . import router
from . import rule
from . import sctp_filter
from . import switch_controller
from . import system
from . import user
from . import videofilter
from . import virtual_patch
from . import voip
from . import vpn
from . import waf
from . import web_proxy
from . import webfilter
from . import wireless_controller
from . import ztna

__all__ = [
    "Alertemail",
    "Antivirus",
    "Application",
    "Authentication",
    "Automation",
    "CMDB",
    "Casb",
    "Certificate",
    "DiameterFilter",
    "Dlp",
    "Dnsfilter",
    "Emailfilter",
    "EndpointControl",
    "EthernetOam",
    "ExtensionController",
    "FileFilter",
    "Firewall",
    "FtpProxy",
    "Icap",
    "Ips",
    "Log",
    "Monitoring",
    "Report",
    "Router",
    "Rule",
    "SctpFilter",
    "SwitchController",
    "System",
    "User",
    "Videofilter",
    "VirtualPatch",
    "Voip",
    "Vpn",
    "Waf",
    "WebProxy",
    "Webfilter",
    "WirelessController",
    "Ztna",
]


class CMDB:
    """CMDB endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """CMDB endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.alertemail = alertemail.Alertemail(client)
        self.antivirus = antivirus.Antivirus(client)
        self.application = application.Application(client)
        self.authentication = authentication.Authentication(client)
        self.automation = automation.Automation(client)
        self.casb = casb.Casb(client)
        self.certificate = certificate.Certificate(client)
        self.diameter_filter = diameter_filter.DiameterFilter(client)
        self.dlp = dlp.Dlp(client)
        self.dnsfilter = dnsfilter.Dnsfilter(client)
        self.emailfilter = emailfilter.Emailfilter(client)
        self.endpoint_control = endpoint_control.EndpointControl(client)
        self.ethernet_oam = ethernet_oam.EthernetOam(client)
        self.extension_controller = extension_controller.ExtensionController(client)
        self.file_filter = file_filter.FileFilter(client)
        self.firewall = firewall.Firewall(client)
        self.ftp_proxy = ftp_proxy.FtpProxy(client)
        self.icap = icap.Icap(client)
        self.ips = ips.Ips(client)
        self.log = log.Log(client)
        self.monitoring = monitoring.Monitoring(client)
        self.report = report.Report(client)
        self.router = router.Router(client)
        self.rule = rule.Rule(client)
        self.sctp_filter = sctp_filter.SctpFilter(client)
        self.switch_controller = switch_controller.SwitchController(client)
        self.system = system.System(client)
        self.user = user.User(client)
        self.videofilter = videofilter.Videofilter(client)
        self.virtual_patch = virtual_patch.VirtualPatch(client)
        self.voip = voip.Voip(client)
        self.vpn = vpn.Vpn(client)
        self.waf = waf.Waf(client)
        self.web_proxy = web_proxy.WebProxy(client)
        self.webfilter = webfilter.Webfilter(client)
        self.wireless_controller = wireless_controller.WirelessController(client)
        self.ztna = ztna.Ztna(client)
