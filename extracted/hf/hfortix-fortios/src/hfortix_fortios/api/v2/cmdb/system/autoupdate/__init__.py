"""FortiOS CMDB - Autoupdate category"""

from .schedule import Schedule

__all__ = [
    "Autoupdate",
    "Schedule",
]


class Autoupdate:
    """Autoupdate endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Autoupdate endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.schedule = Schedule(client)
