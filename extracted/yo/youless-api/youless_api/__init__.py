"""
This file contains a helper class to easily obtain data from the YouLess sensor.
"""
import logging
from datetime import datetime
from typing import Optional

from youless_api.const import SensorType
from youless_api.device import ls110, ls120
from youless_api.gateway import fetch_device_info, fetch_enologic_api
from youless_api.youless_sensor import YoulessSensor, PowerMeter, ExtraMeter, DeliveryMeter, Phase

name = "youless_api"
logger = logging.getLogger(__name__)


class YoulessAPI:
    """A helper class to obtain data from the YouLess Sensor."""

    _cache_data: Optional[dict] = None

    def __init__(self, host, username=None, password=None):
        """Initialize the data bridge."""
        self._host = host
        if username is None:
            self._authentication = None
        else:
            self._authentication = (username, password)
        self._model = None
        self._mac_address = None
        self._firmware_version = None
        self._fetcher = None

    def initialize(self):
        """Establish a connection to the remote device"""
        device_info = fetch_device_info(self._host, self._authentication)

        if device_info is None:
            logger.debug("No device information discovered, assuming LS110 device.")
            self._model = "LS110"
            self._fetcher = ls110(self._host, self._authentication)
        else:
            self._mac_address = device_info["mac"]
            self._firmware_version = device_info["fw"] if "fw" in device_info else None

            enologic_data = fetch_enologic_api(self._host, self._authentication)
            if enologic_data is None:
                logger.debug("Incorrect enologic response, assuming LS120 with PVOutput firmware.")
                self._model = "LS120 - PVOutput"
                self._fetcher = ls110(self._host, self._authentication)
            else:
                logger.debug("Enologic output detected, LS120 device found.")
                self._model = "LS120"
                self._fetcher = ls120(self._host, self._authentication, device_info)

    def update(self):
        """Fetch the latest settings from the Youless Sensor."""
        if self._fetcher:
            self._cache_data = self._fetcher()
        else:
            logger.warning("No fetch algorithm is chosen, setup failed.")

    @property
    def mac_address(self) -> Optional[str]:
        """Get the MAC address of the connected device."""
        return self._mac_address

    @property
    def model(self) -> Optional[str]:
        """Return the model of the connected device."""
        return self._model

    @property
    def firmware_version(self) -> Optional[str]:
        """Get the firmware version of the connected device."""
        return self._firmware_version

    @property
    def current_tariff(self) -> Optional[int]:
        """Get the current tariff, is either 0 or 1 and only present if phase information is present."""
        return self._cache_data[SensorType.TARIFF] if SensorType.TARIFF in self._cache_data else None

    @property
    def water_meter(self) -> Optional[YoulessSensor]:
        """Get the water data available."""
        return self._cache_data[SensorType.WATER] if SensorType.WATER in self._cache_data else None

    @property
    def gas_meter(self) -> Optional[YoulessSensor]:
        """"Get the gas data available."""
        return self._cache_data[SensorType.GAS] if SensorType.GAS in self._cache_data else None

    @property
    def current_power_usage(self) -> Optional[YoulessSensor]:
        """Get the current power usage."""
        return self._cache_data[SensorType.POWER_USAGE] if SensorType.POWER_USAGE in self._cache_data else None

    @property
    def average_power(self) -> Optional[YoulessSensor]:
        """Get the average power usage of active Tarif."""
        return self._cache_data[SensorType.POWER_AVERAGE] if SensorType.POWER_AVERAGE in self._cache_data else None

    @property
    def power_meter(self) -> Optional[PowerMeter]:
        """Get the power meter values."""
        return self._cache_data[SensorType.POWER_METER] if SensorType.POWER_METER in self._cache_data else None

    @property
    def delivery_meter(self) -> Optional[DeliveryMeter]:
        """Get the power delivered values."""
        return self._cache_data[SensorType.DELIVERY_METER] if SensorType.DELIVERY_METER in self._cache_data else None

    @property
    def extra_meter(self) -> Optional[ExtraMeter]:
        """Get the meter values of an attached meter."""
        return self._cache_data[SensorType.EXTRA_METER] if SensorType.EXTRA_METER in self._cache_data else None

    @property
    def phase1(self) -> Optional[Phase]:
        """Get the phase 1 information"""
        return self._cache_data[SensorType.PHASE1] if SensorType.PHASE1 in self._cache_data else None

    @property
    def phase2(self) -> Optional[Phase]:
        """Get the phase 1 information"""
        return self._cache_data[SensorType.PHASE2] if SensorType.PHASE2 in self._cache_data else None

    @property
    def phase3(self) -> Optional[Phase]:
        """Get the phase 1 information"""
        return self._cache_data[SensorType.PHASE3] if SensorType.PHASE3 in self._cache_data else None

    @property
    def peak_power(self) -> Optional[YoulessSensor]:
        """Get the peak power of the month."""
        return self._cache_data[SensorType.MONTH_PEAK] if SensorType.MONTH_PEAK in self._cache_data else None

    @property
    def peak_power_time(self) -> Optional[datetime]:
        """Get the date time of the peak time."""
        return self._cache_data[SensorType.MONTH_PEAK_TIME] if SensorType.MONTH_PEAK_TIME in self._cache_data else None

    @property
    def secured(self) -> bool:
        """Flag indicating if the API has authentication or not."""
        return self._authentication is not None
