"""
This module contains the custom exceptions used in the BEC library.
"""


class ScanAbortion(Exception):
    """Scan abortion exception"""


class ScanInterruption(Exception):
    """Scan interruption exception"""


class ServiceConfigError(Exception):
    """Service config error"""


class DeviceConfigError(Exception):
    """Device config error"""
