"""FortiOS CMDB - Spectrum category (stub)"""

from typing import Any
from ..spectrum_base import Spectrum as SpectrumBase
from .keep_alive import KeepAlive
from .start import Start
from .stop import Stop

class Spectrum(SpectrumBase):
    """Spectrum endpoints wrapper for CMDB API."""

    keep_alive: KeepAlive
    start: Start
    stop: Stop

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
