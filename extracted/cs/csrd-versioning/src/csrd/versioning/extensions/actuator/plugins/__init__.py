from collections.abc import Sequence

from .base import ActuatorLink, ActuatorPlugin, BaseActuatorPlugin
from .env import (
    EnvActuatorPlugin,
    PropertySourceProvider,
    PropertySourceRegistry,
    SanitizationConfig,
    ShowValues,
    create_property_source_registry,
)
from .health import (
    AppStateHealthIndicator,
    BaseHealthIndicator,
    DatabaseHealthIndicator,
    DiskSpaceHealthIndicator,
    HealthActuatorPlugin,
    HealthIndicator,
    KafkaHealthIndicator,
    LaunchDarklyHealthIndicator,
    LivenessIndicator,
    MongoHealthIndicator,
    PingHealthIndicator,
    RabbitHealthIndicator,
    ReadinessIndicator,
    ShowDetails,
    Status,
    discover_indicators,
)
from .info import InfoActuatorPlugin


def default_actuator_plugins() -> Sequence[ActuatorPlugin]:
    """Return the built-in actuator plugins auto-wired by default."""

    return (InfoActuatorPlugin(), EnvActuatorPlugin(), HealthActuatorPlugin())


__all__ = (
    "ActuatorLink",
    "ActuatorPlugin",
    "AppStateHealthIndicator",
    "BaseActuatorPlugin",
    "BaseHealthIndicator",
    "DatabaseHealthIndicator",
    "DiskSpaceHealthIndicator",
    "EnvActuatorPlugin",
    "HealthActuatorPlugin",
    "HealthIndicator",
    "InfoActuatorPlugin",
    "KafkaHealthIndicator",
    "LaunchDarklyHealthIndicator",
    "LivenessIndicator",
    "MongoHealthIndicator",
    "PingHealthIndicator",
    "PropertySourceProvider",
    "PropertySourceRegistry",
    "RabbitHealthIndicator",
    "ReadinessIndicator",
    "SanitizationConfig",
    "ShowDetails",
    "ShowValues",
    "Status",
    "create_property_source_registry",
    "default_actuator_plugins",
    "discover_indicators",
)
