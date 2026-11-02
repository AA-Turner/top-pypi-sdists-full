"""Async client for the Daikin Onecta cloud API."""

from .air_purification import AirPurificationClient
from .auth import get_account_id
from .client import OnectaClient
from .climate import ClimateControlClient
from .domestic_hot_water import DomesticHotWaterClient
from .exceptions import (
    OnectaAccessTokenError,
    OnectaApiError,
    OnectaAuthenticationError,
    OnectaConnectionError,
    OnectaError,
    OnectaRateLimitError,
    OnectaRequestError,
    OnectaResponseError,
)
from .firmware import FirmwareClient
from .management_point import ManagementPointClient
from .models import (
    AirPurification,
    ClimateControl,
    DomesticHotWater,
    EnergyAggregate,
    EnergyData,
    Firmware,
    FirmwareOffer,
    GatewayDevice,
    Schedule,
    ScheduleDefinition,
    ScheduleMode,
    ScheduleSelection,
    ScheduleState,
    Site,
    SiteLocation,
    SiteUser,
)
from .rate_limit import RateLimit
from .schedule import ScheduleClient

__all__ = [
    "GatewayDevice",
    "AirPurification",
    "AirPurificationClient",
    "ClimateControl",
    "ClimateControlClient",
    "DomesticHotWater",
    "EnergyData",
    "EnergyAggregate",
    "DomesticHotWaterClient",
    "FirmwareClient",
    "Firmware",
    "FirmwareOffer",
    "ManagementPointClient",
    "OnectaAccessTokenError",
    "OnectaApiError",
    "OnectaAuthenticationError",
    "OnectaClient",
    "OnectaConnectionError",
    "OnectaError",
    "OnectaRateLimitError",
    "OnectaRequestError",
    "OnectaResponseError",
    "RateLimit",
    "Schedule",
    "ScheduleClient",
    "ScheduleDefinition",
    "ScheduleMode",
    "ScheduleSelection",
    "ScheduleState",
    "Site",
    "SiteLocation",
    "SiteUser",
    "get_account_id",
]
