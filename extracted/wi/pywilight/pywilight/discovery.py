"""Module to discover WiLight devices."""
import logging
import requests

from . import ssdp
from .wilight_device.api.xsd import device as deviceParser
from .wilight_device import PyWiLightDevice

_LOGGER = logging.getLogger(__name__)


MANUFACTURER = 'All Automacao Ltda'


def discover_devices(ssdp_st=None, max_devices=None,
                     match_serial=None,
                     rediscovery_enabled=True):
    """Find WiLight devices on the local network."""
    ssdp_st = ssdp_st or ssdp.ST
    ssdp_entries = ssdp.scan(ssdp_st, max_entries=max_devices,
                             match_serial=match_serial)

    wilights = []

    for entry in ssdp_entries:
        if entry.match_device_description(
                {'manufacturer': MANUFACTURER}):
            serialNumber = entry.description.get('device').get('serialNumber')
            device = device_from_description(
                description_url=entry.location, serialNumber=serialNumber,
                rediscovery_enabled=rediscovery_enabled)

            if device is not None:
                wilights.append(device)

    return wilights

def device_from_host(host):
    url = f"http://{host}:45995/wilight.xml"
    return device_from_description(url, None)

def device_from_description(description_url, serialNumber, rediscovery_enabled=True):
    """Return object representing WiLight device running at host, else None."""
    xml = requests.get(description_url, timeout=10)
    mac = deviceParser.parseString(xml.content).device.macAddress
    model_in = deviceParser.parseString(xml.content).device.modelName
    serial_number = serialNumber or deviceParser.parseString(xml.content).device.serialNumber
    key = deviceParser.parseString(xml.content).device.modelNumber

    if serial_number is None:
        _LOGGER.debug(
            'No serial number was supplied or found in setup xml at: %s.',
            description_url)

    return wilight_from_discovery(
        description_url, mac, model_in, serial_number, key,
        rediscovery_enabled=rediscovery_enabled)

def wilight_from_discovery(location, mac, model_in, serial_number, key,
                                  rediscovery_enabled=True):
    """Create device class based on the device input data."""
    if mac is None:
        return None
    if model_in is None:
        return None
    if len(mac) < 17:
        return None
    if len(model_in) < 15:
        return None
    if serial_number is None:
        return None
    if len(serial_number) != 12:
        return None
    if location is None:
        return None
    host = location.split('/', 3)[2].split(':', 1)[0]
    model_config = model_in.split(' ', 1)[1].split('-', 1)
    model = model_config[0][0:4]
    swversion = model_config[0][4:16]
    config = model_config[1]

    return PyWiLightDevice(host=host, mac=mac, serial_number=serial_number,
                    model=model, swversion=swversion, config=config,
                    key=key, rediscovery_enabled=rediscovery_enabled)
