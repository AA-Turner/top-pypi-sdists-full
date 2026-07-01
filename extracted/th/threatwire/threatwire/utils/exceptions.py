"""
threatwire.utils.exceptions
============================
Library-specific exceptions for clear error handling.
"""


class ThreatWireError(Exception):
    """Base exception for all threatwire errors."""


class CaptureError(ThreatWireError):
    """Raised when packet capture fails."""


class InterfaceError(CaptureError):
    """Raised when the network interface cannot be opened (permissions, not found, etc.)."""


class PcapReadError(CaptureError):
    """Raised when a PCAP file cannot be read or is malformed."""


class RuleLoadError(ThreatWireError):
    """Raised when rule files cannot be loaded or parsed."""


class DecoderError(ThreatWireError):
    """Raised when a protocol decoder encounters an unrecoverable error."""


class BusError(ThreatWireError):
    """Raised when the ThreatEventBus encounters a fatal error."""
