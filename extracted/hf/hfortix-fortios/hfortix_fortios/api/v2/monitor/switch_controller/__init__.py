"""FortiOS CMDB - SwitchController category"""

from . import fsw_firmware
from . import isl_lockdown
from . import managed_switch
from . import mclag_icl
from . import nac_device
from . import recommendation
from .detected_device import DetectedDevice
from .known_nac_device_criteria_list import KnownNacDeviceCriteriaList
from .matched_devices import MatchedDevices

__all__ = [
    "DetectedDevice",
    "FswFirmware",
    "IslLockdown",
    "KnownNacDeviceCriteriaList",
    "ManagedSwitch",
    "MatchedDevices",
    "MclagIcl",
    "NacDevice",
    "Recommendation",
    "SwitchController",
]


class SwitchController:
    """SwitchController endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """SwitchController endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.fsw_firmware = fsw_firmware.FswFirmware(client)
        self.isl_lockdown = isl_lockdown.IslLockdown(client)
        self.managed_switch = managed_switch.ManagedSwitch(client)
        self.mclag_icl = mclag_icl.MclagIcl(client)
        self.nac_device = nac_device.NacDevice(client)
        self.recommendation = recommendation.Recommendation(client)
        self.detected_device = DetectedDevice(client)
        self.known_nac_device_criteria_list = KnownNacDeviceCriteriaList(client)
        self.matched_devices = MatchedDevices(client)
