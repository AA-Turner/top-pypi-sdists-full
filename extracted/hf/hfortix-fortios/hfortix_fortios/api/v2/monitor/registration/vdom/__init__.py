"""FortiOS CMDB - Vdom category"""

from .add_license import AddLicense

__all__ = [
    "AddLicense",
    "Vdom",
]


class Vdom:
    """Vdom endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Vdom endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.add_license = AddLicense(client)
