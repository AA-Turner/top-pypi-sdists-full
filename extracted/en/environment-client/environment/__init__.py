from .flood_monitoring import FloodClient
from .bathing_waters import BathingWatersClient
from .asset_management import AssetManagementClient
from .catchment_data import CatchmentDataClient
from .public_register import PublicRegisterClient

__all__ = [
    "FloodClient",
    "BathingWatersClient",
    "AssetManagementClient",
    "CatchmentDataClient",
    "PublicRegisterClient",
]
