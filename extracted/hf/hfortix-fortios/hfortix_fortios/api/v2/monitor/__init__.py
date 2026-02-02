"""FortiOS CMDB - Monitor category"""

from . import azure
from . import casb
from . import endpoint_control
from . import extender_controller
from . import extension_controller
from . import firewall
from . import firmware
from . import fortiguard
from . import fortiview
from . import geoip
from . import ips
from . import license
from . import log
from . import monitor
from . import network
from . import registration
from . import router
from . import sdwan
from . import service
from . import switch_controller
from . import system
from . import user
from . import utm
from . import videofilter
from . import virtual_wan
from . import vpn
from . import vpn_certificate
from . import wanopt
from . import web_ui
from . import webcache
from . import webfilter
from . import webproxy
from . import wifi

__all__ = [
    "Azure",
    "Casb",
    "EndpointControl",
    "ExtenderController",
    "ExtensionController",
    "Firewall",
    "Firmware",
    "Fortiguard",
    "Fortiview",
    "Geoip",
    "Ips",
    "License",
    "Log",
    "Monitor",
    "Monitor",
    "Network",
    "Registration",
    "Router",
    "Sdwan",
    "Service",
    "SwitchController",
    "System",
    "User",
    "Utm",
    "Videofilter",
    "VirtualWan",
    "Vpn",
    "VpnCertificate",
    "Wanopt",
    "WebUi",
    "Webcache",
    "Webfilter",
    "Webproxy",
    "Wifi",
]


class Monitor:
    """Monitor endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Monitor endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.azure = azure.Azure(client)
        self.casb = casb.Casb(client)
        self.endpoint_control = endpoint_control.EndpointControl(client)
        self.extender_controller = extender_controller.ExtenderController(client)
        self.extension_controller = extension_controller.ExtensionController(client)
        self.firewall = firewall.Firewall(client)
        self.firmware = firmware.Firmware(client)
        self.fortiguard = fortiguard.Fortiguard(client)
        self.fortiview = fortiview.Fortiview(client)
        self.geoip = geoip.Geoip(client)
        self.ips = ips.Ips(client)
        self.license = license.License(client)
        self.log = log.Log(client)
        self.monitor = monitor.Monitor(client)
        self.network = network.Network(client)
        self.registration = registration.Registration(client)
        self.router = router.Router(client)
        self.sdwan = sdwan.Sdwan(client)
        self.service = service.Service(client)
        self.switch_controller = switch_controller.SwitchController(client)
        self.system = system.System(client)
        self.user = user.User(client)
        self.utm = utm.Utm(client)
        self.videofilter = videofilter.Videofilter(client)
        self.virtual_wan = virtual_wan.VirtualWan(client)
        self.vpn = vpn.Vpn(client)
        self.vpn_certificate = vpn_certificate.VpnCertificate(client)
        self.wanopt = wanopt.Wanopt(client)
        self.web_ui = web_ui.WebUi(client)
        self.webcache = webcache.Webcache(client)
        self.webfilter = webfilter.Webfilter(client)
        self.webproxy = webproxy.Webproxy(client)
        self.wifi = wifi.Wifi(client)
