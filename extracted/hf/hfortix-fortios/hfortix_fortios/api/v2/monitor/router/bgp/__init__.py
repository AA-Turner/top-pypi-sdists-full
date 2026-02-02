"""FortiOS CMDB - Bgp category"""

from .clear_soft_in import ClearSoftIn
from .clear_soft_out import ClearSoftOut
from .neighbors import Neighbors
from .neighbors6 import Neighbors6
from .neighbors_statistics import NeighborsStatistics
from .paths import Paths
from .paths6 import Paths6
from .paths_statistics import PathsStatistics
from .soft_reset_neighbor import SoftResetNeighbor

__all__ = [
    "Bgp",
    "ClearSoftIn",
    "ClearSoftOut",
    "Neighbors",
    "Neighbors6",
    "NeighborsStatistics",
    "Paths",
    "Paths6",
    "PathsStatistics",
    "SoftResetNeighbor",
]


class Bgp:
    """Bgp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Bgp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.clear_soft_in = ClearSoftIn(client)
        self.clear_soft_out = ClearSoftOut(client)
        self.neighbors = Neighbors(client)
        self.neighbors6 = Neighbors6(client)
        self.neighbors_statistics = NeighborsStatistics(client)
        self.paths = Paths(client)
        self.paths6 = Paths6(client)
        self.paths_statistics = PathsStatistics(client)
        self.soft_reset_neighbor = SoftResetNeighbor(client)
