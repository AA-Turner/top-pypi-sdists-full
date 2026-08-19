"""Device outlet implementation."""

import enum

from .api import ApiItem
from .device import TypedDeviceOutletTable


class OutletCapability(enum.IntFlag):
    """Outlet capabilities."""

    RELAY = 1
    METERING = 2


class Outlet(ApiItem):
    """Represents an outlet."""

    raw: TypedDeviceOutletTable

    @property
    def name(self) -> str:
        """Name of outlet."""
        return self.raw["name"]

    @property
    def index(self) -> int:
        """Outlet index."""
        return self.raw["index"]

    @property
    def has_relay(self) -> bool | None:
        """Is the outlet controllable.

        Not reported by USP-PDU-Pro, see caps.
        """
        if (has_relay := self.raw.get("has_relay")) is not None:
            return has_relay
        if (caps := self.caps) is not None:
            return bool(caps & OutletCapability.RELAY)
        return None

    @property
    def relay_state(self) -> bool:
        """Is outlet power on."""
        return self.raw["relay_state"]

    @property
    def cycle_enabled(self) -> bool | None:
        """Modem Power Cycle."""
        return self.raw.get("cycle_enabled")

    # Metering capabilities of outlet

    @property
    def has_metering(self) -> bool | None:
        """Is metering supported.

        Reported false by UP1 and UP6 which does not have power metering.
        Not reported by by USP-PDU-Pro, see caps.
        """
        if (has_metering := self.raw.get("has_metering")) is not None:
            return has_metering
        if (caps := self.caps) is not None:
            return bool(caps & OutletCapability.METERING)
        return None

    @property
    def caps(self) -> int | None:
        """Outlet capabilities.

        1: Outlet supports relay (switching)
        3: Outlet supports relay and metering
        """
        return self.raw.get("outlet_caps")

    @property
    def voltage(self) -> str | float | None:
        """Voltage draw of outlet."""
        return self.raw.get("outlet_voltage")

    @property
    def current(self) -> str | float | None:
        """Usage of outlet."""
        return self.raw.get("outlet_current")

    @property
    def power(self) -> str | float | None:
        """Power consumption of the outlet."""
        return self.raw.get("outlet_power")

    @property
    def power_factor(self) -> str | float | None:
        """Power factor."""
        return self.raw.get("outlet_power_factor")

    def __repr__(self) -> str:
        """Return the representation."""
        return f"<{self.name}: relay state {self.relay_state}>"
