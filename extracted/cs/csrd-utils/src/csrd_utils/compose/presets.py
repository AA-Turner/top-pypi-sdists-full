"""Preset definitions for compose workspaces.

Each preset declares the infrastructure categories it requires (the user
picks the *specific* type within each category, e.g. postgres vs mariadb)
and a set of starter service templates.

Presets with ``composable_styles`` present a multi-select of service
patterns.  Each selected style contributes its services; auth wiring
is applied automatically based on ``foreground_services``.
"""

from ..models import (
    INFRA_CATEGORIES,
    PresetDefinition,
    ServiceAugment,
    ServiceNode,
    StyleDefinition,
)

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

PRESET_REGISTRY: dict[str, PresetDefinition] = {
    "authenticated-cluster": PresetDefinition(
        name="authenticated-cluster",
        description="Authenticated cluster with composable service styles",
        required_infra_categories=["database"],
        optional_infra_categories=[],
        workspace_augments=["jwt-auth-provider"],
        default_service_augments=["db-config"],
        optional_service_augments=[
            "delegate-config",
            "service-layer",
        ],
        services=[],  # services come from composable_styles
        composable_styles=[
            StyleDefinition(
                name="crud-app",
                label="crud app",
                description="CRUD service with database + auth passthrough",
                required_infra_categories=[],  # database already required by preset
                foreground_services=["app-service"],
                services=[
                    ServiceNode(
                        name="app-service",
                        role="app",
                        port=8080,
                        features=["database"],
                        augments=[
                            ServiceAugment(name="db-config"),
                            ServiceAugment(
                                name="crud-scaffold",
                                options={"entity_name": "item"},
                            ),
                        ],
                    ),
                ],
            ),
            StyleDefinition(
                name="event-driven",
                label="event-driven",
                description="RabbitMQ producer/consumer with auth",
                required_infra_categories=["messaging"],
                foreground_services=["producer-service"],
                services=[
                    ServiceNode(
                        name="producer-service",
                        role="app",
                        port=8080,
                        features=["messaging"],
                        augments=[
                            ServiceAugment(name="rabbit-messaging"),
                        ],
                    ),
                    ServiceNode(
                        name="consumer-service",
                        role="app",
                        port=8081,
                        features=["messaging"],
                        augments=[
                            ServiceAugment(name="rabbit-messaging"),
                        ],
                    ),
                ],
            ),
            StyleDefinition(
                name="worker",
                label="worker",
                description="Celery dispatcher/worker with auth",
                required_infra_categories=["caching"],
                foreground_services=["dispatcher-service"],
                services=[
                    ServiceNode(
                        name="dispatcher-service",
                        role="app",
                        port=8080,
                        features=["caching"],
                        augments=[
                            ServiceAugment(name="celery-dispatcher"),
                        ],
                    ),
                    ServiceNode(
                        name="worker-service",
                        role="worker",
                        port=0,
                        features=["caching"],
                        augments=[
                            ServiceAugment(name="celery-worker"),
                        ],
                    ),
                ],
            ),
        ],
    ),
    "event-driven-cluster": PresetDefinition(
        name="event-driven-cluster",
        description="Services communicating via RabbitMQ messaging",
        required_infra_categories=["messaging"],
        optional_infra_categories=["database", "caching"],
        workspace_augments=[],
        default_service_augments=[],
        optional_service_augments=[
            "crud-scaffold",
            "delegate-config",
            "service-layer",
        ],
        services=[
            ServiceNode(
                name="producer-service",
                role="app",
                port=8080,
                features=["messaging"],
                augments=[
                    ServiceAugment(name="rabbit-messaging"),
                ],
            ),
            ServiceNode(
                name="consumer-service",
                role="app",
                port=8081,
                features=["messaging"],
                augments=[
                    ServiceAugment(name="rabbit-messaging"),
                ],
            ),
        ],
    ),
    "worker-cluster": PresetDefinition(
        name="worker-cluster",
        description="App service with a Celery worker backed by Redis",
        required_infra_categories=["caching"],
        optional_infra_categories=["database", "messaging"],
        workspace_augments=[],
        default_service_augments=[],
        optional_service_augments=[
            "db-config",
            "crud-scaffold",
            "delegate-config",
            "service-layer",
        ],
        services=[
            ServiceNode(
                name="app-service",
                role="app",
                port=8080,
                features=["caching"],
                augments=[
                    ServiceAugment(name="celery-dispatcher"),
                ],
            ),
            ServiceNode(
                name="worker-service",
                role="worker",
                port=0,
                features=["caching"],
                augments=[
                    ServiceAugment(name="celery-worker"),
                ],
            ),
        ],
    ),
}


def list_presets() -> list[PresetDefinition]:
    """Return all registered presets in display order."""

    return list(PRESET_REGISTRY.values())


def members_for_category(category_label: str) -> list[str]:
    """Return sorted member infra types for a category label."""

    for label, members, _single in INFRA_CATEGORIES:
        if label == category_label:
            return sorted(members)
    return []
