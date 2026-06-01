"""Augment descriptors for application-level service capabilities.

Each augment is described by an ``AugmentDescriptor`` dataclass that
encapsulates everything the renderer and scaffolder need: prerequisite
checks, compose wiring, package dependencies, settings fields, and
template references.  Adding a new augment requires only adding a new
descriptor to ``AUGMENT_REGISTRY``.

Mirrors the ``InfraDescriptor`` pattern in ``infra.py``.
"""

import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

from ..models import (
    ComposeSpec,
    ServiceAugment,
    ServiceNode,
    WorkspaceAugment,
    find_service_by_name,
    find_service_by_role,
)

# ---------------------------------------------------------------------------
# Resolver callback type aliases
# ---------------------------------------------------------------------------

#: Resolves dynamic compose env / settings / template vars from spec.
AugmentResolver = Callable[[ServiceAugment, ServiceNode, ComposeSpec], dict[str, str]]

#: Resolves dynamic env example lines from workspace augment + spec.
EnvExampleResolver = Callable[[WorkspaceAugment, ComposeSpec], list[str]]

#: Resolves dynamic routers from augment options.
#: Returns list of (import_line, alias) tuples.
DynamicRouterResolver = Callable[[ServiceAugment, ServiceNode, ComposeSpec], list[tuple[str, str]]]

#: Resolves dynamic migration imports from augment options.
#: Returns list of (import_line, var_name) tuples.
DynamicMigrationResolver = Callable[
    [ServiceAugment, ServiceNode, ComposeSpec], list[tuple[str, str]]
]

#: Returns multiple variable dicts for multi-instance template rendering.
#: Each dict is used to render the full template set once (e.g. per entity).
MultiScaffoldResolver = Callable[[ServiceAugment, ServiceNode, ComposeSpec], list[dict[str, str]]]


# ---------------------------------------------------------------------------
# Role registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RoleDescriptor:
    """Describes a service role and its auto-wiring behaviour.

    Parameters
    ----------
    name
        Role identifier (e.g. ``"app"``, ``"auth"``, ``"worker"``).
    singleton
        Whether at most one service with this role may exist per workspace.
    implies_workspace_augments
        Workspace-scope augments auto-added when a service selects this
        role (e.g. ``"auth"`` implies ``["jwt-auth-provider"]``).
    implies_service_augments
        Service-scope augments auto-added to the service when it selects
        this role (e.g. ``"worker"`` implies ``["celery-worker"]``).
    requires_infra
        Infra categories that must be present when this role is selected.
        The wizard calls ``_ensure_infra`` for each category.
    name_hints
        Substrings matched against service names to auto-suggest this
        role (e.g. ``["auth"]`` matches ``"auth-service"``).
    """

    name: str
    singleton: bool = False
    implies_workspace_augments: list[str] = field(default_factory=list)
    implies_service_augments: list[str] = field(default_factory=list)
    requires_infra: list[str] = field(default_factory=list)
    name_hints: list[str] = field(default_factory=list)


ROLE_REGISTRY: dict[str, RoleDescriptor] = {
    "app": RoleDescriptor(name="app"),
    "auth": RoleDescriptor(
        name="auth",
        singleton=True,
        implies_workspace_augments=["jwt-auth-provider"],
        requires_infra=["database"],
        name_hints=["auth"],
    ),
    "worker": RoleDescriptor(
        name="worker",
        implies_service_augments=["celery-worker"],
        requires_infra=["caching"],
        name_hints=["worker", "job"],
    ),
    "gateway": RoleDescriptor(
        name="gateway",
        singleton=True,
        implies_service_augments=["gateway-proxy"],
        name_hints=["gateway", "proxy", "bff"],
    ),
}


# ---------------------------------------------------------------------------
# Option prompts — data-driven follow-up questions for augments
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OptionPrompt:
    """Describes a follow-up question the wizard asks when an augment is selected.

    Parameters
    ----------
    key
        Option key stored in ``ServiceAugment.options``.  Keys starting
        with ``_`` are transient (used for control flow, not persisted).
    prompt
        Human-readable prompt text.
    default
        Default value for text prompts.
    kind
        ``"text"`` for free-form input, ``"yes_no"`` for boolean.
    adds_augments
        Service-scope augments auto-added when answered affirmatively
        (non-empty string for text, ``True`` for yes_no).
    follow_ups
        Nested prompts shown only when this prompt is answered
        affirmatively.
    exclude_role
        Skip this prompt when the current service has this role.
    """

    key: str
    prompt: str
    default: str = ""
    kind: Literal["text", "yes_no"] = "text"
    adds_augments: list[str] = field(default_factory=list)
    follow_ups: list["OptionPrompt"] = field(default_factory=list)
    exclude_role: str | None = None


@dataclass(frozen=True)
class RouterDescriptor:
    """Describes a router contributed by an augment.

    Parameters
    ----------
    import_path
        Dot-path relative to the service package, e.g.
        ``".views.auth_passthrough_view"``.
    attr
        Name of the router attribute in the module, e.g. ``"router"``.
    alias
        Import alias used in ``__init__.py``, e.g.
        ``"auth_passthrough_router"``.
    """

    import_path: str
    attr: str = "router"
    alias: str = ""


@dataclass(frozen=True)
class MiddlewareDescriptor:
    """Describes middleware contributed by an augment."""

    import_path: str
    class_name: str


@dataclass(frozen=True)
class ProxySpec:
    """Declares that an augment exposes proxy-able endpoints for gateway discovery.

    When a gateway exists in the workspace, target services' augments with
    a ``proxy_spec`` are auto-registered in ``gateway-routes.yaml``.  The
    gateway then forwards requests matching the prefix to the target service.

    Parameters
    ----------
    prefix
        URL path prefix this augment owns (e.g. ``"/api/tasks"``).
        Can be a list for augments that expose multiple unrelated
        prefixes (e.g. ``["/api/signup", "/api/token"]``).
        For augments with dynamic prefixes (e.g. crud-scaffold where the
        entity name determines the prefix), use ``prefix_template`` instead.
    prefix_template
        Template string for dynamic prefixes, resolved from augment options.
        Uses ``string.Template`` syntax, e.g. ``"/api/${entity_name_plural}"``.
    public
        If ``True``, the gateway skips JWT validation for this prefix.
        Only ``auth-passthrough`` should set this.
    """

    prefix: str | list[str] | None = None
    prefix_template: str | None = None
    public: bool = False


@dataclass(frozen=True)
class ExceptionHandlerDescriptor:
    """Describes an exception handler contributed by an augment."""

    import_path: str
    handler_name: str
    exception_class: str = "Exception"


@dataclass(frozen=True)
class AugmentDescriptor:
    """Complete description of an augment capability.

    Parameters
    ----------
    name
        Unique augment identifier used in specs and registry lookups.
    scope
        ``"workspace"`` for cluster-wide facts, ``"service"`` for
        per-service capabilities.
    description
        Human-readable description shown in menus and docs.
    requires_infra
        Infra feature categories that must be present in the spec
        (e.g. ``["database"]``).
    requires_workspace_augment
        A workspace-scope augment that must exist for this augment to
        be valid (e.g. ``"jwt-auth-provider"``).
    requires_service_in_spec
        A service role that must exist in the spec.
    compose_env
        Static compose environment variables contributed by this augment.
    compose_depends_on
        Static compose ``depends_on`` entries.
    packages
        Python package names added to the service's ``requirements.txt``.
    settings_fields
        Static settings fields (name → default value). Dynamic fields
        are resolved via ``resolve_settings_fields``.
    template_dir
        Relative name under ``templates/augments/`` for scaffolded
        files.  ``None`` for augments that don't scaffold files.
    conflicts_with
        Augment names that cannot coexist with this one.
    needs_target_selection
        Whether the wizard should prompt the user to pick target
        services from the spec (e.g. delegate targets).
    option_prompts
        Data-driven follow-up questions the wizard asks when this
        augment is selected.  Replaces ad-hoc if/elif branching.
    resolve_compose_env
        Optional callback to resolve dynamic compose env/depends_on.
        Returns a dict of env key→value pairs.
    resolve_settings_fields
        Optional callback to resolve dynamic settings fields.
        Returns a dict of field_name→default_value_expr pairs.
    resolve_template_vars
        Optional callback to resolve dynamic template variables.
        Returns a dict of var_name→value pairs.
    resolve_env_example_lines
        Optional callback to resolve dynamic ``.env.example`` lines.
    env_example_lines
        Static ``.env.example`` lines contributed by this augment.
    """

    name: str
    scope: Literal["workspace", "service"]
    description: str

    # Prerequisites
    requires_infra: list[str] = field(default_factory=list)
    requires_workspace_augment: str | None = None
    requires_service_in_spec: str | None = None

    # What it contributes to compose (static values only)
    compose_env: dict[str, str] = field(default_factory=dict)
    compose_depends_on: list[str] = field(default_factory=list)

    # What it contributes to scaffolded code
    packages: list[str] = field(default_factory=list)
    settings_fields: dict[str, str] = field(default_factory=dict)
    template_dir: str | None = None

    # Conflict prevention
    conflicts_with: list[str] = field(default_factory=list)

    # Augment implication: selecting this augment auto-adds implied augments.
    # E.g. crud-scaffold implies db-config.  Resolved transitively.
    implies: list[str] = field(default_factory=list)

    # Does this augment resolve values dynamically from the spec?
    needs_target_selection: bool = False

    # Data-driven follow-up prompts for the wizard
    option_prompts: list[OptionPrompt] = field(default_factory=list)

    # Auto-apply: augments with this flag are silently added to every
    # service without appearing in the capabilities prompt.
    auto_apply: bool = False

    # Hidden: augments that are implementation details auto-wired by
    # higher-level prompts (e.g. db-config is implied by crud-scaffold,
    # jwt-auth-consumer is added by "Protect with token auth?").
    # Hidden augments don't appear in the capabilities prompt but can
    # still be added via direct mode or the add-augment command.
    hidden: bool = False

    # For workspace-scope augments: scaffold template files into the
    # service with this role.  ``None`` means no scaffolding.
    applies_to_role: str | None = None

    # Routers to wire into __init__.py via include_router
    routers: list[RouterDescriptor] = field(default_factory=list)

    # Middleware to add to the app
    middleware: list[MiddlewareDescriptor] = field(default_factory=list)

    # Exception handlers to register on the app
    exception_handlers: list[ExceptionHandlerDescriptor] = field(default_factory=list)

    # Dynamic resolver callbacks (Open-Closed: no if/elif branches needed)
    resolve_compose_env: AugmentResolver | None = None
    resolve_compose_deps: AugmentResolver | None = None
    resolve_compose_volumes: AugmentResolver | None = None
    resolve_settings_fields: AugmentResolver | None = None
    resolve_template_vars: AugmentResolver | None = None

    # Env example lines (static or dynamic)
    env_example_lines: list[str] = field(default_factory=list)
    resolve_env_example_lines: EnvExampleResolver | None = None

    # Dynamic routers resolved from augment options (e.g. entity-named views)
    resolve_dynamic_routers: DynamicRouterResolver | None = None

    # Dynamic migration imports resolved from augment options
    resolve_dynamic_migrations: DynamicMigrationResolver | None = None

    # Multi-instance scaffolding: when set, templates are rendered once
    # per returned variable dict (e.g. one per discovered entity).
    resolve_multi_scaffold_vars: MultiScaffoldResolver | None = None

    # Proxy endpoint registration: when set, the gateway's gateway-proxy
    # augment auto-discovers this augment on target services and generates
    # proxy views/delegates for it.
    proxy_spec: ProxySpec | None = None


# ---------------------------------------------------------------------------
# Resolver functions — dynamic wiring extracted from renderer/scaffolder
# ---------------------------------------------------------------------------


# Lazy import to avoid circular dependency with infra.py
def _detect_db(spec: ComposeSpec) -> str | None:
    from .infra import detect_configured_db

    return detect_configured_db({n.type for n in spec.infra})


def _db_infra_desc(db: str):
    from .infra import INFRA_REGISTRY

    return INFRA_REGISTRY.get(db)


def _plain_default(value: str) -> str:
    """Strip docker-compose ``${VAR:-default}`` syntax to just ``default``."""
    m = re.match(r"^\$\{[A-Z_]+:-(.+)}$", value)
    return m.group(1) if m else value


def _sql_auto_id(spec: ComposeSpec) -> str:
    """Return the SQL auto-increment primary key syntax for the configured DB."""
    db = _detect_db(spec)
    if db == "postgres":
        return "SERIAL PRIMARY KEY"
    elif db == "mariadb":
        return "INTEGER PRIMARY KEY AUTO_INCREMENT"
    else:
        # sqlite or None — both use AUTOINCREMENT
        return "INTEGER PRIMARY KEY AUTOINCREMENT"


# ── jwt-auth-consumer ────────────────────────────────────────────────────


def _jwt_auth_consumer_compose_env(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    env: dict[str, str] = {}
    auth_svc = find_service_by_role(spec, "auth")
    if auth_svc is not None and auth_svc.name != svc.name:
        env["AUTH_JWKS_URL"] = f"http://{auth_svc.name}:{auth_svc.port}/.well-known/jwks.json"
    return env


def _jwt_auth_consumer_settings(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    fields: dict[str, str] = {}
    auth_svc = find_service_by_role(spec, "auth")
    if auth_svc is not None:
        fields["auth_jwks_url"] = f'"http://{auth_svc.name}:{auth_svc.port}/.well-known/jwks.json"'
    fields["jwt_algorithm"] = '"RS256"'
    fields["jwt_issuer"] = '"csrd-auth"'
    fields["jwt_audience"] = f'"{spec.workspace.name}"'
    return fields


def _jwt_auth_consumer_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    variables: dict[str, str] = {}
    auth_svc = find_service_by_role(spec, "auth")
    if auth_svc is not None:
        variables["auth_service_name"] = auth_svc.name
        variables["auth_service_port"] = str(auth_svc.port)
    return variables


# ── auth-passthrough ─────────────────────────────────────────────────────


def _auth_passthrough_compose_env(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    env: dict[str, str] = {}
    auth_svc = find_service_by_role(spec, "auth")
    if auth_svc is not None and auth_svc.name != svc.name:
        env["AUTH_SERVICE_URL"] = f"http://{auth_svc.name}:{auth_svc.port}"
    return env


def _auth_passthrough_settings(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    fields: dict[str, str] = {}
    auth_svc = find_service_by_role(spec, "auth")
    if auth_svc is not None:
        fields["auth_service_url"] = f'"http://{auth_svc.name}:{auth_svc.port}"'
    return fields


def _auth_passthrough_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    variables: dict[str, str] = {}
    auth_svc = find_service_by_role(spec, "auth")
    if auth_svc is not None:
        variables["auth_service_name"] = auth_svc.name
        variables["auth_service_port"] = str(auth_svc.port)
    return variables


# ── delegate-config ──────────────────────────────────────────────────────


def _delegate_compose_env(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    env: dict[str, str] = {}
    targets = augment.options.get("targets", [])
    if isinstance(targets, str):
        targets = [targets]
    for target_name in targets:
        target_svc = find_service_by_name(spec, target_name)
        if target_svc is not None and target_svc.name != svc.name:
            url_key = f"{target_name.upper().replace('-', '_')}_SERVICE_URL"
            env[url_key] = f"http://{target_name}:{target_svc.port}"
    return env


def _delegate_settings(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    fields: dict[str, str] = {}
    targets = augment.options.get("targets", [])
    if isinstance(targets, str):
        targets = [targets]
    for target_name in targets:
        target_svc = find_service_by_name(spec, target_name)
        if target_svc is not None:
            field_name = f"{target_name.replace('-', '_')}_service_url"
            fields[field_name] = f'"http://{target_name}:{target_svc.port}"'
    return fields


def _delegate_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    variables: dict[str, str] = {}
    targets = augment.options.get("targets", [])
    if isinstance(targets, str):
        targets = [targets]
    variables["targets"] = ",".join(targets)
    for target_name in targets:
        target_svc = find_service_by_name(spec, target_name)
        if target_svc is not None:
            key = f"{target_name.replace('-', '_')}_port"
            variables[key] = str(target_svc.port)
    return variables


# ── db-config ────────────────────────────────────────────────────────────


def _db_settings_fields(svc: ServiceNode, spec: ComposeSpec) -> dict[str, str]:
    """Resolve database settings fields based on configured infra.

    Shared by ``_db_config_settings`` and ``_jwt_auth_provider_settings``
    to avoid copy-paste drift.
    """
    fields: dict[str, str] = {}
    db = _detect_db(spec)
    if db == "sqlite" or db is None:
        fields["db_path"] = f'"/app/data/{svc.name}.db"'
    elif db in ("postgres", "mariadb"):
        db_desc = _db_infra_desc(db)
        if db_desc is not None:
            for env_key, env_val in db_desc.service_env.items():
                plain = _plain_default(env_val)
                field_name = env_key.lower()
                # Port fields must be int, not str
                if field_name.endswith("_port") and plain.isdigit():
                    fields[field_name] = plain
                else:
                    fields[field_name] = f'"{plain}"'
    else:
        raise ValueError(f"Unsupported database type: {db!r}")
    return fields


def _db_config_settings(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    return _db_settings_fields(svc, spec)


def _db_compose_env(augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec) -> dict[str, str]:
    """Compose env vars for database connectivity (shared by db-config and jwt-auth-provider)."""
    db = _detect_db(spec)
    if db is None or db == "sqlite":
        return {}
    desc = _db_infra_desc(db)
    return dict(desc.service_env) if desc is not None else {}


def _db_compose_deps(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Compose depends_on for database container (shared by db-config and jwt-auth-provider)."""
    db = _detect_db(spec)
    if db is None or db == "sqlite":
        return {}
    desc = _db_infra_desc(db)
    return dict(desc.depends_on) if desc is not None else {}


def _db_compose_volumes(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Compose volumes for sqlite (per-service data volume)."""
    db = _detect_db(spec)
    if db == "sqlite" or db is None:
        return {f"{svc.name}-data": "/app/data"}
    return {}


def _db_config_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    variables: dict[str, str] = {}
    db = _detect_db(spec)
    if db == "postgres":
        variables["db_adapter_import"] = "from csrd.repository import PGAdapter"
        variables["db_adapter_class"] = "PGAdapter"
        variables["db_adapter_constructor"] = (
            "PGAdapter(\n"
            "        host=settings.db_host,\n"
            "        port=int(settings.db_port),\n"
            "        user=settings.db_user,\n"
            "        password=settings.db_password,\n"
            "        database=settings.db_name,\n"
            "    )"
        )
    elif db == "mariadb":
        variables["db_adapter_import"] = "from csrd.repository import MariaAdapter"
        variables["db_adapter_class"] = "MariaAdapter"
        variables["db_adapter_constructor"] = (
            "MariaAdapter(\n"
            "        host=settings.db_host,\n"
            "        port=int(settings.db_port),\n"
            "        user=settings.db_user,\n"
            "        password=settings.db_password,\n"
            "        database=settings.db_name,\n"
            "    )"
        )
    elif db == "sqlite" or db is None:
        # Default to sqlite for scaffolded code when no db is configured yet.
        # Scaffolded files are created once — the user can edit them later.
        variables["db_adapter_import"] = "from csrd.repository import SQLiteAdapter"
        variables["db_adapter_class"] = "SQLiteAdapter"
        variables["db_adapter_constructor"] = "SQLiteAdapter(db_path=settings.db_path)"
    else:
        raise ValueError(f"Unsupported database type: {db!r}")

    # SQL dialect
    variables["sql_auto_id"] = _sql_auto_id(spec)

    return variables


# ── shared template var helpers ───────────────────────────────────────────


def _auth_guard_vars(svc: ServiceNode) -> dict[str, str]:
    """Return template variables for conditional JWT auth guards.

    Used by crud-scaffold, rabbit-messaging, and celery-dispatcher
    to conditionally include ``Security(auth_dep)`` when the service
    has ``jwt-auth-consumer``.
    """
    has_auth = any(a.name == "jwt-auth-consumer" for a in svc.augments)
    if has_auth:
        return {
            "fastapi_imports": "from fastapi import APIRouter, Security",
            "auth_import": "from ..dependencies.auth import auth_dep",
            "auth_guard": "\n    _claims=Security(auth_dep),",
        }
    return {
        "fastapi_imports": "from fastapi import APIRouter",
        "auth_import": "",
        "auth_guard": "",
    }


# ── crud-scaffold ────────────────────────────────────────────────────────


def _crud_scaffold_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    variables: dict[str, str] = {}
    entity_raw = augment.options.get("entity_name", "item")
    entity = entity_raw if isinstance(entity_raw, str) else entity_raw[0]
    snake = entity.replace("-", "_").lower()
    pascal = "".join(w.capitalize() for w in snake.split("_"))
    plural_raw = augment.options.get("entity_name_plural", snake + "s")
    plural = plural_raw if isinstance(plural_raw, str) else plural_raw[0]
    variables["entity_name"] = entity
    variables["entity_name_snake"] = snake
    variables["entity_name_pascal"] = pascal
    variables["entity_name_plural"] = plural

    # SQL dialect
    variables["sql_auto_id"] = _sql_auto_id(spec)

    variables.update(_auth_guard_vars(svc))

    return variables


def _crud_scaffold_dynamic_routers(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> list[tuple[str, str]]:
    """Resolve entity-named router imports for crud-scaffold."""
    entity_raw = augment.options.get("entity_name", "item")
    entity = entity_raw if isinstance(entity_raw, str) else entity_raw[0]
    snake = entity.replace("-", "_").lower()
    alias = f"{snake}_router"
    import_line = f"from .views.{snake}_view import router as {alias}"
    return [(import_line, alias)]


def _crud_scaffold_dynamic_migrations(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> list[tuple[str, str]]:
    """Resolve entity-named migration imports for crud-scaffold."""
    entity_raw = augment.options.get("entity_name", "item")
    entity = entity_raw if isinstance(entity_raw, str) else entity_raw[0]
    snake = entity.replace("-", "_").lower()
    import_line = f"from .migrations_{snake} import {snake}_migration"
    return [(import_line, f"{snake}_migration")]


# ── gateway-proxy ─────────────────────────────────────────────────────────


def resolve_gateway_routes(spec: ComposeSpec) -> list[dict[str, str | bool]]:
    """Discover all proxy-able routes from target services in the spec.

    Iterates non-gateway, non-worker services and collects ``ProxySpec``
    declarations from their augments.  Also scans the gateway's own
    augments for public prefixes (e.g. auth-passthrough).

    Returns a flat list suitable for rendering ``gateway-routes.yaml``.

    Each entry: ``{"prefix": "/api/...", "target": "http://svc:port", "public": False}``
    """
    from string import Template

    gateway = next((s for s in spec.services if s.role == "gateway"), None)
    if gateway is None:
        return []

    routes: list[dict[str, str | bool]] = []
    seen_prefixes: set[str] = set()

    # Scan gateway's own augments for public prefixes (e.g. auth-passthrough).
    # These are served directly by the gateway, not proxied, but the
    # middleware needs to know they're public (skip JWT guard).
    for aug in gateway.augments:
        desc = AUGMENT_REGISTRY.get(aug.name)
        if desc is None or desc.proxy_spec is None:
            continue
        ps = desc.proxy_spec
        if not ps.public or ps.prefix is None:
            continue
        prefixes = ps.prefix if isinstance(ps.prefix, list) else [ps.prefix]
        for prefix in prefixes:
            if prefix not in seen_prefixes:
                seen_prefixes.add(prefix)
                routes.append(
                    {
                        "prefix": prefix,
                        "target": f"http://{gateway.name}:{gateway.port}",
                        "public": True,
                    }
                )

    # Scan inner services for proxy-able routes.
    for svc in spec.services:
        if svc.role in ("gateway", "worker") or svc.port == 0:
            continue
        target_url = f"http://{svc.name}:{svc.port}"

        # Collect augments from the service itself plus workspace-scope
        # augments that target this service's role (e.g. jwt-auth-provider
        # with applies_to_role="auth" contributes routes for the auth svc).
        augments_to_scan: list[ServiceAugment] = list(svc.augments)
        for wa in spec.workspace.augments:
            desc = AUGMENT_REGISTRY.get(wa.name)
            if desc is not None and desc.applies_to_role == svc.role:
                augments_to_scan.append(ServiceAugment(name=wa.name, options=wa.options))

        for aug in augments_to_scan:
            desc = AUGMENT_REGISTRY.get(aug.name)
            if desc is None or desc.proxy_spec is None:
                continue
            ps = desc.proxy_spec

            # Resolve prefixes (static, list, or template)
            if ps.prefix is not None:
                prefixes = ps.prefix if isinstance(ps.prefix, list) else [ps.prefix]
            elif ps.prefix_template is not None:
                # Build substitution vars: raw options + common derived values
                sub_vars = dict(aug.options)
                # Derive entity_name_plural if not explicitly set
                entity_raw = aug.options.get("entity_name", "")
                if entity_raw and "entity_name_plural" not in sub_vars:
                    entity = entity_raw if isinstance(entity_raw, str) else entity_raw[0]
                    snake = entity.replace("-", "_").lower()
                    sub_vars["entity_name_plural"] = aug.options.get(
                        "entity_name_plural", snake + "s"
                    )
                resolved = Template(ps.prefix_template).safe_substitute(sub_vars)
                # Skip unresolved templates (missing variables)
                if "$" in resolved:
                    continue
                prefixes = [resolved]
            else:
                continue

            for prefix in prefixes:
                if prefix in seen_prefixes:
                    continue
                seen_prefixes.add(prefix)

                routes.append(
                    {
                        "prefix": prefix,
                        "target": target_url,
                        "public": ps.public,
                    }
                )

    return routes


def _gateway_proxy_compose_env(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """No compose env needed — gateway reads routes from config file."""
    return {}


def _base_svc_template_vars(svc: ServiceNode) -> dict[str, str]:
    """Common template variables shared by multiple augment resolvers."""
    return {
        "service_name": svc.name,
        "service_name_snake": svc.name.replace("-", "_"),
        "port": str(svc.port),
    }


def _gateway_proxy_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    return _base_svc_template_vars(svc)


# ── rabbit-messaging ─────────────────────────────────────────────────────


def _caching_compose_env(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Compose env: REDIS_URL from infra descriptor."""
    from .infra import INFRA_REGISTRY

    desc = INFRA_REGISTRY.get("redis")
    if desc is not None:
        return dict(desc.service_env)
    return {}


def _caching_compose_deps(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Compose depends_on: redis container."""
    from .infra import INFRA_REGISTRY

    desc = INFRA_REGISTRY.get("redis")
    if desc is not None:
        return dict(desc.depends_on)
    return {}


def _caching_settings(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Settings field: cache_url."""
    return {
        "cache_url": '"redis://redis:6379/0"',
    }


def _caching_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    return _base_svc_template_vars(svc)


# ── metrics ──────────────────────────────────────────────────────────────


def _metrics_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    return _base_svc_template_vars(svc)


# ── tracing ──────────────────────────────────────────────────────────────


def _tracing_settings(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    return {
        "otel_service_name": f'"{svc.name}"',
        "otel_exporter_otlp_endpoint": '"http://localhost:4318/v1/traces"',
        "otel_enabled": '"false"',
    }


def _tracing_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    return _base_svc_template_vars(svc)


# ── rabbit-messaging ────────────────────────────────────────────────────


def _rabbit_compose_env(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Compose env: RABBITMQ_URL from infra descriptor."""
    from .infra import INFRA_REGISTRY

    desc = INFRA_REGISTRY.get("rabbitmq")
    if desc is not None:
        return dict(desc.service_env)
    return {}


def _rabbit_compose_deps(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Compose depends_on: rabbitmq container."""
    from .infra import INFRA_REGISTRY

    desc = INFRA_REGISTRY.get("rabbitmq")
    if desc is not None:
        return dict(desc.depends_on)
    return {}


def _rabbit_settings(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Settings field: rabbitmq_url."""
    return {
        "rabbitmq_url": '"amqp://service_rabbit:change_me@rabbitmq:5672/"',
    }


def _rabbit_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    return _auth_guard_vars(svc)


# ── jwt-auth-provider ────────────────────────────────────────────────────


def _jwt_auth_provider_settings(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    fields: dict[str, str] = {}
    fields["jwt_algorithm"] = '"RS256"'
    fields["jwt_issuer"] = '"csrd-auth"'
    fields["jwt_audience"] = f'"{spec.workspace.name}"'
    fields["jwt_ttl_seconds"] = "3600"
    fields["jwt_key_size"] = "2048"
    fields["jwt_key_rotation_interval"] = "86400"
    fields["jwt_key_retention_period"] = "90000"

    # Database settings — shared with db-config
    fields.update(_db_settings_fields(svc, spec))
    return fields


def _jwt_auth_provider_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    # Shares db adapter logic with db-config
    return _db_config_template_vars(augment, svc, spec)


def _jwt_auth_provider_env_example(augment: WorkspaceAugment, spec: ComposeSpec) -> list[str]:
    signing = augment.options.get("signing", "jwks")
    lines = [
        "# JWT Authentication",
        "JWT_ISSUER=csrd-auth",
        f"JWT_AUDIENCE={spec.workspace.name}",
        "JWT_TTL_SECONDS=3600",
    ]
    if signing == "shared-secret":
        lines.append("JWT_ALGORITHM=HS256")
        lines.append("JWT_SECRET=changeme-use-a-strong-secret")
    else:
        lines.append("JWT_ALGORITHM=RS256")
        lines.append("JWT_KEY_SIZE=2048")
        lines.append("JWT_KEY_ROTATION_INTERVAL=86400")
        lines.append("JWT_KEY_RETENTION_PERIOD=90000")
    return lines


# ── celery-worker ────────────────────────────────────────────────────────


def _celery_compose_env(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Compose env: BROKER_URL and RESULT_BACKEND from Redis."""
    return {
        "BROKER_URL": "redis://redis:6379/1",
        "RESULT_BACKEND": "redis://redis:6379/2",
    }


def _celery_compose_deps(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Compose depends_on: redis container."""
    from .infra import INFRA_REGISTRY

    desc = INFRA_REGISTRY.get("redis")
    if desc is not None:
        return dict(desc.depends_on)
    return {}


def _celery_settings(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Settings fields for Celery configuration."""
    return {
        "broker_url": '"redis://redis:6379/1"',
        "result_backend": '"redis://redis:6379/2"',
    }


def _celery_worker_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    return {
        "service_name": svc.name,
        "service_name_snake": svc.name.replace("-", "_"),
    }


# ── celery-dispatcher ─────────────────────────────────────────────────────


def _celery_dispatcher_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    # Find the worker service to reference its task names
    worker = find_service_by_role(spec, "worker")
    worker_snake = worker.name.replace("-", "_") if worker else "worker_service"

    variables = _auth_guard_vars(svc)
    variables["worker_name_snake"] = worker_snake
    return variables


def _realtime_websocket_template_vars(
    augment: ServiceAugment, svc: ServiceNode, spec: ComposeSpec
) -> dict[str, str]:
    """Template vars for realtime-websocket scaffold files."""
    ws_path = augment.options.get("realtime_ws_path")
    if not isinstance(ws_path, str) or not ws_path.strip():
        ws_path = "/ws"
    return {
        "realtime_ws_path": ws_path,
    }


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

AUGMENT_REGISTRY: dict[str, AugmentDescriptor] = {
    # ── Workspace-scope ────────────────────────────────────────────
    "jwt-auth-provider": AugmentDescriptor(
        name="jwt-auth-provider",
        scope="workspace",
        description="Cluster provides JWT authentication via an auth service",
        requires_infra=["database"],
        packages=[
            "csrd-auth",
            "csrd-models",
            "csrd-repository",
            "csrd-migration",
            "csrd-lifespan",
            "PyJWT[crypto]",
        ],
        template_dir="jwt-auth-provider",
        applies_to_role="auth",
        routers=[
            RouterDescriptor(
                import_path=".views.auth_view",
                alias="auth_router",
            ),
            RouterDescriptor(
                import_path=".views.users_view",
                alias="users_router",
            ),
            RouterDescriptor(
                import_path=".views.users_admin_view",
                alias="users_admin_router",
            ),
            RouterDescriptor(
                import_path=".views.jwks_view",
                alias="jwks_router",
            ),
        ],
        resolve_settings_fields=_jwt_auth_provider_settings,
        resolve_template_vars=_jwt_auth_provider_template_vars,
        resolve_env_example_lines=_jwt_auth_provider_env_example,
        resolve_compose_env=_db_compose_env,
        resolve_compose_deps=_db_compose_deps,
        resolve_compose_volumes=_db_compose_volumes,
        proxy_spec=ProxySpec(prefix="/api/users"),
    ),
    # ── Service-scope ──────────────────────────────────────────────
    "db-config": AugmentDescriptor(
        name="db-config",
        scope="service",
        description="Database repository with migrations and compose wiring",
        hidden=True,
        requires_infra=["database"],
        packages=["csrd-repository", "csrd-migration", "csrd-lifespan"],
        template_dir="db-config",
        resolve_compose_env=_db_compose_env,
        resolve_compose_deps=_db_compose_deps,
        resolve_compose_volumes=_db_compose_volumes,
        resolve_settings_fields=_db_config_settings,
        resolve_template_vars=_db_config_template_vars,
    ),
    "delegate-config": AugmentDescriptor(
        name="delegate-config",
        scope="service",
        description="Inter-service delegation with delegate classes",
        packages=["csrd-delegate", "csrd-models"],
        needs_target_selection=True,
        resolve_compose_env=_delegate_compose_env,
        resolve_settings_fields=_delegate_settings,
        resolve_template_vars=_delegate_template_vars,
    ),
    "jwt-auth-consumer": AugmentDescriptor(
        name="jwt-auth-consumer",
        scope="service",
        description="JWT token validation using cluster auth service",
        hidden=True,
        requires_workspace_augment="jwt-auth-provider",
        packages=["csrd-auth", "csrd-models"],
        template_dir="jwt-auth-consumer",
        resolve_compose_env=_jwt_auth_consumer_compose_env,
        resolve_settings_fields=_jwt_auth_consumer_settings,
        resolve_template_vars=_jwt_auth_consumer_template_vars,
    ),
    "auth-passthrough": AugmentDescriptor(
        name="auth-passthrough",
        scope="service",
        description="Unguarded signup/login proxy endpoints to the auth service",
        hidden=True,
        requires_workspace_augment="jwt-auth-provider",
        packages=["csrd-delegate", "csrd-models"],
        template_dir="auth-passthrough",
        routers=[
            RouterDescriptor(
                import_path=".views.auth_passthrough_view",
                alias="auth_passthrough_router",
            ),
        ],
        proxy_spec=ProxySpec(prefix=["/api/signup", "/api/token"], public=True),
        resolve_compose_env=_auth_passthrough_compose_env,
        resolve_settings_fields=_auth_passthrough_settings,
        resolve_template_vars=_auth_passthrough_template_vars,
    ),
    "structured-logging": AugmentDescriptor(
        name="structured-logging",
        scope="service",
        description="Request context middleware and structured logging",
        packages=["csrd-logging", "csrd-context"],
        auto_apply=True,
        middleware=[
            MiddlewareDescriptor(
                import_path="csrd.context.middleware",
                class_name="RequestContextMiddleware",
            ),
        ],
    ),
    "service-layer": AugmentDescriptor(
        name="service-layer",
        scope="service",
        description="BaseService + ServiceError hierarchy + exception handler",
        packages=["csrd-service", "csrd-models"],
        exception_handlers=[
            ExceptionHandlerDescriptor(
                import_path="csrd.service",
                handler_name="service_exception_handler",
            ),
        ],
    ),
    "crud-scaffold": AugmentDescriptor(
        name="crud-scaffold",
        scope="service",
        description="CRUD endpoints for a named entity with token-guarded views",
        implies=["db-config"],
        packages=[],  # db-config covers repository/migration dependencies
        template_dir="crud-scaffold",
        routers=[],  # routers are dynamic per entity — wired via resolve_dynamic_routers
        option_prompts=[
            OptionPrompt(
                key="entity_name",
                prompt="Entity name",
                default="item",
            ),
            OptionPrompt(
                key="_token_auth",
                prompt="Protect with token auth?",
                kind="yes_no",
                adds_augments=["jwt-auth-consumer"],
                follow_ups=[
                    OptionPrompt(
                        key="_auth_passthrough",
                        prompt="Expose login/signup endpoints on this service?",
                        kind="yes_no",
                        adds_augments=["auth-passthrough"],
                        exclude_role="auth",
                    ),
                ],
            ),
        ],
        proxy_spec=ProxySpec(prefix_template="/api/${entity_name_plural}"),
        resolve_template_vars=_crud_scaffold_template_vars,
        resolve_dynamic_routers=_crud_scaffold_dynamic_routers,
        resolve_dynamic_migrations=_crud_scaffold_dynamic_migrations,
    ),
    "gateway-proxy": AugmentDescriptor(
        name="gateway-proxy",
        scope="service",
        description="Transparent reverse proxy with JWT guard and route config",
        hidden=True,
        packages=["httpx>=0.27,<1", "pyyaml>=6,<7"],
        template_dir="gateway",
        routers=[
            RouterDescriptor(
                import_path=".views.proxy_view",
                alias="proxy_router",
            ),
        ],
        resolve_template_vars=_gateway_proxy_template_vars,
    ),
    "caching": AugmentDescriptor(
        name="caching",
        scope="service",
        description="Redis cache client with health-check and test endpoints [unverified]",
        requires_infra=["caching"],
        packages=["redis"],
        template_dir="caching",
        routers=[
            RouterDescriptor(
                import_path=".views.cache_view",
                alias="cache_router",
            ),
        ],
        resolve_compose_env=_caching_compose_env,
        resolve_compose_deps=_caching_compose_deps,
        resolve_settings_fields=_caching_settings,
        resolve_template_vars=_caching_template_vars,
    ),
    "metrics": AugmentDescriptor(
        name="metrics",
        scope="service",
        description="Prometheus metrics middleware and /metrics scrape endpoint [unverified]",
        packages=["prometheus-client"],
        template_dir="metrics",
        settings_fields={
            "metrics_enabled": "True",
            "metrics_path": '"/metrics"',
        },
        routers=[
            RouterDescriptor(
                import_path=".views.metrics_view",
                alias="metrics_router",
            ),
        ],
        middleware=[
            MiddlewareDescriptor(
                import_path=".middleware.metrics",
                class_name="MetricsMiddleware",
            ),
        ],
        resolve_template_vars=_metrics_template_vars,
    ),
    "tracing": AugmentDescriptor(
        name="tracing",
        scope="service",
        description="OpenTelemetry distributed tracing with OTLP exporter [unverified]",
        packages=[
            "opentelemetry-sdk",
            "opentelemetry-instrumentation-fastapi",
            "opentelemetry-exporter-otlp-proto-http",
        ],
        template_dir="tracing",
        middleware=[
            MiddlewareDescriptor(
                import_path=".middleware.tracing",
                class_name="TracingMiddleware",
            ),
        ],
        resolve_settings_fields=_tracing_settings,
        resolve_template_vars=_tracing_template_vars,
    ),
    "rabbit-messaging": AugmentDescriptor(
        name="rabbit-messaging",
        scope="service",
        description="RabbitMQ messaging with publisher and consumer support [unverified]",
        requires_infra=["messaging"],
        packages=["csrd-message[rabbit]", "csrd-lifespan"],
        template_dir="rabbit-messaging",
        routers=[
            RouterDescriptor(
                import_path=".views.messaging_view",
                alias="messaging_router",
            ),
        ],
        proxy_spec=ProxySpec(prefix="/api/messages"),
        resolve_compose_env=_rabbit_compose_env,
        resolve_compose_deps=_rabbit_compose_deps,
        resolve_settings_fields=_rabbit_settings,
        resolve_template_vars=_rabbit_template_vars,
    ),
    "celery-worker": AugmentDescriptor(
        name="celery-worker",
        scope="service",
        description="Celery task worker with Redis broker",
        hidden=True,
        requires_infra=["caching"],
        packages=["celery[redis]"],
        template_dir="celery-worker",
        conflicts_with=["celery-dispatcher"],
        env_example_lines=[
            "# Celery broker",
            "BROKER_URL=redis://redis:6379/1",
            "RESULT_BACKEND=redis://redis:6379/2",
        ],
        resolve_compose_env=_celery_compose_env,
        resolve_compose_deps=_celery_compose_deps,
        resolve_settings_fields=_celery_settings,
        resolve_template_vars=_celery_worker_template_vars,
    ),
    "celery-dispatcher": AugmentDescriptor(
        name="celery-dispatcher",
        scope="service",
        description="Task dispatch endpoints for Celery workers",
        hidden=True,
        requires_infra=["caching"],
        packages=["celery[redis]"],
        template_dir="celery-dispatcher",
        conflicts_with=["celery-worker"],
        env_example_lines=[
            "# Celery broker",
            "BROKER_URL=redis://redis:6379/1",
            "RESULT_BACKEND=redis://redis:6379/2",
        ],
        routers=[
            RouterDescriptor(
                import_path=".views.tasks_view",
                alias="tasks_router",
            ),
        ],
        proxy_spec=ProxySpec(prefix="/api/tasks"),
        resolve_compose_env=_celery_compose_env,
        resolve_compose_deps=_celery_compose_deps,
        resolve_settings_fields=_celery_settings,
        resolve_template_vars=_celery_dispatcher_template_vars,
    ),
    "realtime-websocket": AugmentDescriptor(
        name="realtime-websocket",
        scope="service",
        description="WebSocket real-time connection support with csrd-realtime",
        packages=["csrd-realtime"],
        template_dir="realtime-websocket",
        settings_fields={
            "realtime_enabled": "True",
            "realtime_ws_path": '"/ws"',
            "realtime_max_connections": "5000",
        },
        routers=[
            RouterDescriptor(
                import_path=".views.realtime_view",
                alias="realtime_router",
            ),
        ],
        resolve_template_vars=_realtime_websocket_template_vars,
    ),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def augment_for(name: str) -> AugmentDescriptor:
    """Look up an augment descriptor by name.

    Raises ``KeyError`` if the name is not registered.
    """
    return AUGMENT_REGISTRY[name]


def augments_for_scope(scope: Literal["workspace", "service"]) -> list[AugmentDescriptor]:
    """Return all augment descriptors matching the given scope."""
    return [d for d in AUGMENT_REGISTRY.values() if d.scope == scope]
