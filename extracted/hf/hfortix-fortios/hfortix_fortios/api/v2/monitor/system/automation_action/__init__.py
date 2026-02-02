"""FortiOS CMDB - AutomationAction category"""

from .stats import Stats

__all__ = [
    "AutomationAction",
    "Stats",
]


class AutomationAction:
    """AutomationAction endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """AutomationAction endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.stats = Stats(client)
