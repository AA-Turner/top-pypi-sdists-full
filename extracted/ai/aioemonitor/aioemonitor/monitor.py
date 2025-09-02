"""Monitor for aioemonitor."""

DEFAULT_REQUEST_TIMEOUT = 55
STATUS_ENDPOINT = "/status.xml"

import re
from dataclasses import dataclass

import xmltodict


@dataclass
class EmonitorChannel:
    number: int
    active: int
    label: str
    ct_size: int
    paired_with_channel: int
    input: int
    max_power: float
    avg_power: float
    inst_power: float


@dataclass
class EmonitorHardware:
    serial_number: str
    firmware_version: str


@dataclass
class EmonitorNetwork:
    mac_address: str
    ip_address: str


@dataclass
class EmonitorStatus:
    hardware: EmonitorHardware
    network: EmonitorNetwork
    channels: list


class Emonitor:
    """Async emonitor api."""

    def __init__(self, host, websession, timeout=DEFAULT_REQUEST_TIMEOUT):
        """Create oncue async api object."""
        self._host = host
        self._websession = websession
        self._timeout = timeout

    async def _get(self, endpoint, params=None):
        """Make a get request."""
        response = await self._websession.request(
            "GET",
            f"http://{self._host}{endpoint}",
            timeout=self._timeout,
            params=params,
        )
        data = await response.read()
        return data.decode("utf-8", "ignore")

    async def async_get_status(self):
        """Call api to get latest status."""
        text = await self._get(STATUS_ENDPOINT)
        # Strip the TLA_number because can can have invalid UTF-8
        data = xmltodict.parse(re.sub("<TLA_number>.*?</TLA_number>", "", text.strip()))
        emonitor = data["emonitor"]
        hardware = emonitor["hardware"]
        emonitor_hardware = EmonitorHardware(
            hardware["serial_number"], hardware["firmware_version"]
        )
        network = emonitor["hardware"]["network"]
        emonitor_network = EmonitorNetwork(
            network["MAC_address"], network["IP_address"]
        )
        emonitor_channels = {
            _as_int(channel["@Number"]): EmonitorChannel(
                _as_int(channel["@Number"]),
                _channel_is_active(channel["active"]),
                channel["label"],
                _as_int(channel["CT_size"]),
                _as_int(channel["paired_with_channel"]) or None,
                _as_int(channel["input"]),
                _as_float(channel["max_power"]),
                _as_float(channel["avg_power"]),
                _as_float(channel["inst_power"]),
            )
            for channel in emonitor["channels"]["channel"]
        }
        return EmonitorStatus(emonitor_hardware, emonitor_network, emonitor_channels)


def _channel_is_active(active):
    try:
        return bool(int(active))
    except TypeError:
        return None


def _as_int(str):
    try:
        return int(str)
    except TypeError:
        return None


def _as_float(str):
    try:
        return float(str)
    except TypeError:
        return None
