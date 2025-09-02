"""Custom Exceptions of pyEGPS."""


class EgpsException(Exception):
    """General EGPS exception."""


class MissingLibrary(EgpsException):
    """System is a missing a library."""


class UsbError(EgpsException):
    """Can't access the usb device."""


class UnsupportedProducId(UsbError):
    """Device has an unsupported product id."""


class MaximumConnectionTriesReached(UsbError):
    """Couldn't connect to device."""


class InvalidSocketNumber(EgpsException):
    """Device has no such socket."""
