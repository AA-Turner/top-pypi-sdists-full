"""FortiOS CMDB - AutomationStitch category"""

from .stats import Stats
from .test import Test
from .webhook import Webhook

__all__ = [
    "AutomationStitch",
    "Stats",
    "Test",
    "Webhook",
]


class AutomationStitch:
    """AutomationStitch endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """AutomationStitch endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.stats = Stats(client)
        self.test = Test(client)
        self.webhook = Webhook(client)
