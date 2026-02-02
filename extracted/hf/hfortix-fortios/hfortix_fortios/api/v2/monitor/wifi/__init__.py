"""FortiOS CMDB - Wifi category"""

from . import ap_profile
from . import client as client_ns
from . import euclid
from . import firmware
from . import managed_ap
from . import nac_device
from . import network
from . import region_image
from . import rogue_ap
from . import spectrum
from . import ssid
from . import vlan_probe
from .ap_channels import ApChannels
from .ap_names import ApNames
from .ap_status import ApStatus
from .interfering_ap import InterferingAp
from .matched_devices import MatchedDevices
from .meta import Meta
from .station_capability import StationCapability
from .statistics import Statistics
from .unassociated_devices import UnassociatedDevices

__all__ = [
    "ApChannels",
    "ApNames",
    "ApProfile",
    "ApStatus",
    "Client",
    "Euclid",
    "Firmware",
    "InterferingAp",
    "ManagedAp",
    "MatchedDevices",
    "Meta",
    "NacDevice",
    "Network",
    "RegionImage",
    "RogueAp",
    "Spectrum",
    "Ssid",
    "StationCapability",
    "Statistics",
    "UnassociatedDevices",
    "VlanProbe",
    "Wifi",
]


class Wifi:
    """Wifi endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Wifi endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.ap_profile = ap_profile.ApProfile(client)
        self.client = client_ns.Client(client)
        self.euclid = euclid.Euclid(client)
        self.firmware = firmware.Firmware(client)
        self.managed_ap = managed_ap.ManagedAp(client)
        self.nac_device = nac_device.NacDevice(client)
        self.network = network.Network(client)
        self.region_image = region_image.RegionImage(client)
        self.rogue_ap = rogue_ap.RogueAp(client)
        self.spectrum = spectrum.Spectrum(client)
        self.ssid = ssid.Ssid(client)
        self.vlan_probe = vlan_probe.VlanProbe(client)
        self.ap_channels = ApChannels(client)
        self.ap_names = ApNames(client)
        self.ap_status = ApStatus(client)
        self.interfering_ap = InterferingAp(client)
        self.matched_devices = MatchedDevices(client)
        self.meta = Meta(client)
        self.station_capability = StationCapability(client)
        self.statistics = Statistics(client)
        self.unassociated_devices = UnassociatedDevices(client)
