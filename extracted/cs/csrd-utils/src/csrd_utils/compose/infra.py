"""Infrastructure container definitions for docker-compose rendering.

Each infra type is described by an ``InfraDescriptor`` dataclass that
encapsulates everything the renderer needs: container definition,
volumes, service environment wiring, depends_on entries, and
``.env.example`` lines.  Adding a new infra type requires only adding
a new descriptor to ``INFRA_REGISTRY``.
"""

from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Healthcheck presets
# ---------------------------------------------------------------------------


def _healthcheck(
    test: list[str], interval: str = "5s", timeout: str = "3s", retries: int = 3
) -> dict[str, Any]:
    return {
        "test": test,
        "interval": interval,
        "timeout": timeout,
        "retries": retries,
        "start_period": "10s",
    }


# ---------------------------------------------------------------------------
# Descriptor
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class InfraDescriptor:
    """Complete description of an infrastructure component.

    Fields
    ------
    name
        Identifier used as compose service name and spec type key.
    feature
        The capability feature tag this infra satisfies (e.g. ``"database"``).
    has_container
        ``False`` for infra like sqlite that need no container.
    service_def
        Docker-compose service dict (image, healthcheck, …).
    volumes
        Named volumes required by the container.
    service_env
        Environment variables injected into *application* services
        that declare the matching feature.
    depends_on
        ``depends_on`` entries injected into application services.
    env_example_lines
        Lines contributed to ``.env.example``.
    """

    name: str
    feature: str
    has_container: bool = True
    service_def: dict[str, Any] = field(default_factory=dict)
    volumes: dict[str, None] = field(default_factory=dict)
    service_env: dict[str, str] = field(default_factory=dict)
    depends_on: dict[str, Any] = field(default_factory=dict)
    env_example_lines: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_DB_ENV_EXAMPLE_BASE = [
    "# Database",
    "DB_NAME=service_db",
    "DB_USER=service_user",
    "DB_PASSWORD=change_me",
]

_DB_SERVICE_ENV_BASE: dict[str, str] = {
    "DB_NAME": "${DB_NAME:-service_db}",
    "DB_USER": "${DB_USER:-service_user}",
    "DB_PASSWORD": "${DB_PASSWORD:-change_me}",
}


INFRA_REGISTRY: dict[str, InfraDescriptor] = {
    "postgres": InfraDescriptor(
        name="postgres",
        feature="database",
        service_def={
            "image": "postgres:16-alpine",
            "restart": "unless-stopped",
            "environment": {
                "POSTGRES_DB": "${DB_NAME:-service_db}",
                "POSTGRES_USER": "${DB_USER:-service_user}",
                "POSTGRES_PASSWORD": "${DB_PASSWORD:-change_me}",
            },
            "ports": ["5432:5432"],
            "volumes": ["postgres-data:/var/lib/postgresql/data"],
            "healthcheck": _healthcheck(
                [
                    "CMD-SHELL",
                    "pg_isready -U ${DB_USER:-service_user} -d ${DB_NAME:-service_db}",
                ],
            ),
        },
        volumes={"postgres-data": None},
        service_env={
            **_DB_SERVICE_ENV_BASE,
            "DB_HOST": "postgres",
            "DB_PORT": "5432",
        },
        depends_on={"postgres": {"condition": "service_healthy"}},
        env_example_lines=[
            *_DB_ENV_EXAMPLE_BASE,
            "DB_HOST=postgres",
            "DB_PORT=5432",
        ],
    ),
    "mariadb": InfraDescriptor(
        name="mariadb",
        feature="database",
        service_def={
            "image": "mariadb:11",
            "restart": "unless-stopped",
            "environment": {
                "MYSQL_ROOT_PASSWORD": "${MYSQL_ROOT_PASSWORD:-change_me_root}",
                "MYSQL_DATABASE": "${DB_NAME:-service_db}",
                "MYSQL_USER": "${DB_USER:-service_user}",
                "MYSQL_PASSWORD": "${DB_PASSWORD:-change_me}",
            },
            "ports": ["3306:3306"],
            "volumes": ["mariadb-data:/var/lib/mysql"],
            "healthcheck": _healthcheck(
                ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"],
            ),
        },
        volumes={"mariadb-data": None},
        service_env={
            **_DB_SERVICE_ENV_BASE,
            "DB_HOST": "mariadb",
            "DB_PORT": "3306",
        },
        depends_on={"mariadb": {"condition": "service_healthy"}},
        env_example_lines=[
            *_DB_ENV_EXAMPLE_BASE,
            "DB_HOST=mariadb",
            "DB_PORT=3306",
            "MYSQL_ROOT_PASSWORD=change_me_root",
        ],
    ),
    "sqlite": InfraDescriptor(
        name="sqlite",
        feature="database",
        has_container=False,
        # sqlite needs no container, no depends_on, no service_env
        # (DB_PATH is set per-service in the renderer)
    ),
    "redis": InfraDescriptor(
        name="redis",
        feature="caching",
        service_def={
            "image": "redis:7-alpine",
            "restart": "unless-stopped",
            "ports": ["6379:6379"],
            "healthcheck": _healthcheck(
                ["CMD", "redis-cli", "ping"],
            ),
        },
        service_env={"REDIS_URL": "redis://redis:6379/0"},
        depends_on={"redis": {"condition": "service_healthy"}},
        env_example_lines=[
            "# Redis",
            "REDIS_URL=redis://redis:6379/0",
        ],
    ),
    "rabbitmq": InfraDescriptor(
        name="rabbitmq",
        feature="messaging",
        service_def={
            "image": "rabbitmq:3-management-alpine",
            "restart": "unless-stopped",
            "environment": {
                "RABBITMQ_DEFAULT_USER": "${RABBITMQ_USER:-service_rabbit}",
                "RABBITMQ_DEFAULT_PASS": "${RABBITMQ_PASSWORD:-change_me}",
            },
            "ports": ["5672:5672", "15672:15672"],
            "healthcheck": _healthcheck(
                ["CMD", "rabbitmq-diagnostics", "-q", "ping"],
            ),
        },
        service_env={
            "RABBITMQ_URL": (
                "amqp://${RABBITMQ_USER:-service_rabbit}"
                ":${RABBITMQ_PASSWORD:-change_me}@rabbitmq:5672/"
            ),
        },
        depends_on={"rabbitmq": {"condition": "service_healthy"}},
        env_example_lines=[
            "# RabbitMQ",
            "RABBITMQ_USER=service_rabbit",
            "RABBITMQ_PASSWORD=change_me",
            "RABBITMQ_URL=amqp://service_rabbit:change_me@rabbitmq:5672/",
        ],
    ),
}
"""Map infra type name → descriptor with all rendering data."""

# Subset of registry entries that have containers (used by compose renderer)
INFRA_RENDERERS = {k: v for k, v in INFRA_REGISTRY.items() if v.has_container}


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def render_infra(infra_type: str) -> tuple[str, dict[str, Any], dict[str, None]]:
    """Render an infra type into its compose service name, service dict, and volumes.

    Raises ``KeyError`` if *infra_type* has no container (e.g. ``sqlite``).
    """
    desc = INFRA_REGISTRY[infra_type]
    if not desc.has_container:
        raise KeyError(f"Infra type '{infra_type}' has no container to render")
    return desc.name, dict(desc.service_def), dict(desc.volumes)


def descriptor_for(infra_type: str) -> InfraDescriptor:
    """Look up the descriptor for an infra type.

    Raises ``KeyError`` if the type is unknown.
    """
    return INFRA_REGISTRY[infra_type]


def descriptors_for_feature(feature: str, spec_infra_types: set[str]) -> list[InfraDescriptor]:
    """Return descriptors whose feature matches and whose type is configured."""
    return [
        desc
        for desc in INFRA_REGISTRY.values()
        if desc.feature == feature and desc.name in spec_infra_types
    ]


def detect_configured_db(infra_types: set[str] | list[str]) -> str | None:
    """Return the database type from a collection of infra types, or ``None``."""
    from ..models import INFRA_DATABASES

    for t in infra_types:
        if t in INFRA_DATABASES:
            return t
    return None
