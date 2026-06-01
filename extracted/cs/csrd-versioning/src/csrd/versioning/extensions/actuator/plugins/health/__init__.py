"""Spring Boot-style health actuator with composable indicators."""

from .auto import (
    AppStateHealthIndicator,
    DatabaseHealthIndicator,
    KafkaHealthIndicator,
    LaunchDarklyHealthIndicator,
    MongoHealthIndicator,
    RabbitHealthIndicator,
    discover_indicators,
)
from .indicators import (
    BaseHealthIndicator,
    DiskSpaceHealthIndicator,
    HealthIndicator,
    LivenessIndicator,
    PingHealthIndicator,
    ReadinessIndicator,
)
from .plugin import HealthActuatorPlugin, ShowDetails, Status

__all__ = (
    "AppStateHealthIndicator",
    "BaseHealthIndicator",
    "DatabaseHealthIndicator",
    "DiskSpaceHealthIndicator",
    "HealthActuatorPlugin",
    "HealthIndicator",
    "KafkaHealthIndicator",
    "LaunchDarklyHealthIndicator",
    "LivenessIndicator",
    "MongoHealthIndicator",
    "PingHealthIndicator",
    "RabbitHealthIndicator",
    "ReadinessIndicator",
    "ShowDetails",
    "Status",
    "discover_indicators",
)
