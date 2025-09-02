"""

This file contains the sensor class for the youless API

"""


class YoulessSensor:
    """A wrapper class to contain the Youless Sensor values."""

    def __init__(self, value, uom):
        """Initialize the value wrapper."""
        self._value = value
        self._uom = uom

    @property
    def unit_of_measurement(self):
        """Get the unit of measurement for this value."""
        return self._uom

    @property
    def value(self):
        """Get the current value"""
        return self._value


class PowerMeter:

    def __init__(self, low: YoulessSensor, high: YoulessSensor,
                 total: YoulessSensor):
        self._low = low
        self._high = high
        self._total = total

    @property
    def low(self) -> YoulessSensor:
        return self._low

    @property
    def high(self) -> YoulessSensor:
        return self._high

    @property
    def total(self):
        return self._total


class DeliveryMeter:

    def __init__(self, low: YoulessSensor, high: YoulessSensor):
        self._low = low
        self._high = high

    @property
    def low(self) -> YoulessSensor:
        return self._low

    @property
    def high(self) -> YoulessSensor:
        return self._high


class ExtraMeter:

    def __init__(self, total: YoulessSensor, usage: YoulessSensor):
        self._total = total
        self._usage = usage

    @property
    def usage(self) -> YoulessSensor:
        return self._usage

    @property
    def total(self) -> YoulessSensor:
        return self._total


class Phase:
    def __init__(self, current: YoulessSensor, voltage: YoulessSensor, power: YoulessSensor):
        self._current = current
        self._voltage = voltage
        self._power = power

    @property
    def current(self) -> YoulessSensor:
        return self._current

    @property
    def voltage(self) -> YoulessSensor:
        return self._voltage

    @property
    def power(self) -> YoulessSensor:
        return self._power
