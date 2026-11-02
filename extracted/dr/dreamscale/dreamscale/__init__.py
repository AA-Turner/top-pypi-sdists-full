"""Dreamscale - fast serverless inference for your robots."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("dreamscale")
except PackageNotFoundError:  # Direct source import outside an installed environment.
    __version__ = "0+unknown"

from dreamscale import (
    agents,
    arx5,
    datasets,
    dreamzero,
    dreamzero_yam,
    franka,
    libero,
    robot,
    so101,
    trainings,
    yam,
)
from dreamscale.errors import (
    AuthError,
    CreditsError,
    NoCapacityError,
    ObservationError,
)
from dreamscale.errors import (
    DreamscaleError as Error,
)
from dreamscale.policy import (
    ActionSmoothingMode,
    ActResult,
    AsyncPolicy,
    ChunkEvent,
    DispatchEvent,
    LatencyStats,
    MergeEvent,
    Policy,
    PolicyStepResult,
    ProviderPreference,
    QueueMergeEvent,
    RegionPreference,
    RequestEvent,
    RunHooks,
    RunResult,
    RunStrategy,
    RunTimingSummary,
    SamplingMode,
    SpeedPreference,
    aconnect,
    connect,
)

__all__ = [
    "Error",
    "AuthError",
    "CreditsError",
    "NoCapacityError",
    "ObservationError",
    "Policy",
    "AsyncPolicy",
    "ActResult",
    "ActionSmoothingMode",
    "ChunkEvent",
    "DispatchEvent",
    "MergeEvent",
    "PolicyStepResult",
    "RunHooks",
    "RunResult",
    "RunStrategy",
    "RunTimingSummary",
    "SamplingMode",
    "LatencyStats",
    "RegionPreference",
    "ProviderPreference",
    "SpeedPreference",
    "QueueMergeEvent",
    "RequestEvent",
    "aconnect",
    "agents",
    "arx5",
    "connect",
    "datasets",
    "dreamzero",
    "dreamzero_yam",
    "franka",
    "libero",
    "robot",
    "so101",
    "trainings",
    "yam",
    "__version__",
]
