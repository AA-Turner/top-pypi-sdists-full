"""Typed spec models for csrd compose."""

from pydantic import ConfigDict, Field, field_validator

from .base import BaseModel
from .types import AugmentOptionsMap, OptionsMap


class WorkspaceAugment(BaseModel):
    """Workspace-scoped augment reference."""

    name: str
    options: AugmentOptionsMap = Field(default_factory=dict)


class ServiceAugment(BaseModel):
    """Service-scoped augment reference with optional configuration."""

    name: str
    options: AugmentOptionsMap = Field(default_factory=dict)


class WorkspaceConfig(BaseModel):
    """Workspace-level metadata for compose rendering."""

    name: str = "workspace"
    git_init: bool = False
    augments: list[WorkspaceAugment] = Field(default_factory=list)


class PresetRef(BaseModel):
    """Preset reference with optional options map."""

    name: str
    options: OptionsMap = Field(default_factory=dict)


class ServiceNode(BaseModel):
    """Single service entry in the compose spec.

    Services declare the infrastructure they need via *features* — a list
    of capability tags such as ``"database"``, ``"caching"``, or
    ``"messaging"``.  The renderer inspects these tags to inject the
    correct ``depends_on``, ``environment``, and ``volumes`` entries,
    wiring each service to the workspace's configured infra.
    """

    name: str
    role: str = "app"
    port: int = 8080
    features: list[str] = Field(default_factory=list)
    augments: list[ServiceAugment] = Field(default_factory=list)
    include_actuator: bool = False


# ---------------------------------------------------------------------------
# Infrastructure
# ---------------------------------------------------------------------------

INFRA_DATABASES = frozenset({"postgres", "mariadb", "sqlite"})
INFRA_MESSAGING = frozenset({"rabbitmq"})
INFRA_CACHING = frozenset({"redis"})
INFRA_ALL_TYPES = INFRA_DATABASES | INFRA_MESSAGING | INFRA_CACHING

# Category definitions: (label, member types, single-select?)
INFRA_CATEGORIES: list[tuple[str, frozenset[str], bool]] = [
    ("database", INFRA_DATABASES, True),
    ("messaging", INFRA_MESSAGING, True),
    ("caching", INFRA_CACHING, True),
]


class InfraNode(BaseModel):
    """Single infrastructure entry in the compose spec."""

    type: str

    @field_validator("type")
    @classmethod
    def _validate_type(cls, value: str) -> str:
        if value not in INFRA_ALL_TYPES:
            raise ValueError(
                f"Unknown infra type '{value}'. "
                f"Must be one of: {', '.join(sorted(INFRA_ALL_TYPES))}"
            )
        return value


class ComposeSpec(BaseModel):
    """Canonical top-level model for `csrd-compose.yaml`."""

    version: int = 1
    workspace: WorkspaceConfig = Field(default_factory=WorkspaceConfig)
    presets: list[PresetRef] = Field(default_factory=list)
    services: list[ServiceNode] = Field(default_factory=list)
    infra: list[InfraNode] = Field(default_factory=list)
    overrides: dict[str, object] = Field(default_factory=dict)

    @field_validator("version")
    @classmethod
    def _validate_version(cls, value: int) -> int:
        if value != 1:
            raise ValueError("Only compose spec version 1 is supported")
        return value


class StyleDefinition(BaseModel):
    """Composable service style within a preset.

    Each style declares a set of services to add when selected.
    The ``foreground`` flag on each service entry controls auth wiring:
    foreground services get ``auth-passthrough``, background services
    get only ``jwt-auth-consumer``.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    label: str
    description: str
    services: list[ServiceNode] = Field(default_factory=list)
    required_infra_categories: list[str] = Field(default_factory=list)
    #: Names of services that are user-facing (get auth-passthrough).
    #: Services not listed here are background (get jwt-auth-consumer only).
    foreground_services: list[str] = Field(default_factory=list)


class PresetDefinition(BaseModel):
    """Declarative workspace preset."""

    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    required_infra_categories: list[str] = Field(default_factory=list)
    optional_infra_categories: list[str] = Field(default_factory=list)
    services: list[ServiceNode] = Field(default_factory=list)
    workspace_augments: list[str] = Field(default_factory=list)
    default_service_augments: list[str] = Field(default_factory=list)
    optional_service_augments: list[str] = Field(default_factory=list)
    composable_styles: list[StyleDefinition] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Spec query helpers
# ---------------------------------------------------------------------------


def find_service_by_role(spec: ComposeSpec, role: str) -> ServiceNode | None:
    """Return the first service with the given role, or ``None``."""
    return next((s for s in spec.services if s.role == role), None)


def find_service_by_name(spec: ComposeSpec, name: str) -> ServiceNode | None:
    """Return the service with the given name, or ``None``."""
    return next((s for s in spec.services if s.name == name), None)
