"""FortiOS CMDB - Casb category"""

from . import saas_application

__all__ = [
    "Casb",
    "SaasApplication",
]


class Casb:
    """Casb endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Casb endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.saas_application = saas_application.SaasApplication(client)
