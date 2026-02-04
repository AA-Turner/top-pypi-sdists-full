"""FortiOS CMDB - Spectrum category"""

from ..spectrum_base import Spectrum as SpectrumBase
from .keep_alive import KeepAlive
from .start import Start
from .stop import Stop

__all__ = [
    "KeepAlive",
    "Spectrum",
    "Start",
    "Stop",
]


class Spectrum(SpectrumBase):
    """Spectrum endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Spectrum endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.keep_alive = KeepAlive(client)
        self.start = Start(client)
        self.stop = Stop(client)
