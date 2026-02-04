"""FortiOS CMDB - Monitoring category"""

from .npu_hpe import NpuHpe

__all__ = [
    "Monitoring",
    "NpuHpe",
]


class Monitoring:
    """Monitoring endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Monitoring endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.npu_hpe = NpuHpe(client)
