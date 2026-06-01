"""Per-service file renderers: settings.py, __init__.py, requirements.txt.

These files are rendered on **first scaffold only** — once they exist they
are user-owned and will not be overwritten on re-render.  This ensures
manually added routers, settings fields, and dependencies survive when
augments are added later.
"""

from ..models import ComposeSpec, ServiceAugment, ServiceNode
from .augments import AUGMENT_REGISTRY, AugmentDescriptor
from .infra import detect_configured_db

# ---------------------------------------------------------------------------
# Base packages always included in every service
# ---------------------------------------------------------------------------

_BASE_PACKAGES: list[str] = [
    "fastapi>=0.115,<1",
    "uvicorn[standard]>=0.30,<1",
    "pydantic-settings>=2.6,<3",
    "csrd-models>=0.3,<1",
    "csrd-versioning>=0.1.36,<1",
]

# Worker services don't need FastAPI/uvicorn/versioning
_WORKER_BASE_PACKAGES: list[str] = [
    "pydantic-settings>=2.6,<3",
]


# ---------------------------------------------------------------------------
# requirements.txt
# ---------------------------------------------------------------------------


def render_requirements(svc: ServiceNode, spec: ComposeSpec) -> str:
    """Render ``requirements.txt`` from base deps + augment packages.

    Packages are deduplicated and sorted for deterministic output.
    """
    packages = list(_WORKER_BASE_PACKAGES if svc.role == "worker" else _BASE_PACKAGES)

    # Gateway doesn't need versioning — it's a plain proxy
    if svc.role == "gateway":
        packages = [p for p in packages if "csrd-versioning" not in p]

    for augment in svc.augments:
        desc = AUGMENT_REGISTRY.get(augment.name)
        if desc is not None:
            packages.extend(desc.packages)

    # Workspace augments that apply to this service's role
    for ws_aug in spec.workspace.augments:
        desc = AUGMENT_REGISTRY.get(ws_aug.name)
        if desc is not None and desc.applies_to_role == svc.role:
            packages.extend(desc.packages)

    # Deduplicate by package name (before version specifier)
    seen: dict[str, str] = {}
    for pkg in packages:
        name = pkg.split(">=")[0].split("[")[0].strip().lower()
        if name not in seen:
            seen[name] = pkg

    # Add DB driver based on configured infra (needed by adapter at runtime)
    _svc_augment_names = {a.name for a in svc.augments}
    _ws_augment_names = {a.name for a in spec.workspace.augments}
    _has_db_augment = bool(
        {"db-config", "jwt-auth-provider"} & (_svc_augment_names | _ws_augment_names)
    )
    if _has_db_augment:
        db = detect_configured_db({n.type for n in spec.infra})
        if db == "postgres" and "psycopg" not in seen:
            seen["psycopg"] = "psycopg[binary]"
        elif db == "mariadb" and "pymysql" not in seen:
            seen["pymysql"] = "pymysql"

    return "\n".join(sorted(seen.values())) + "\n"


# ---------------------------------------------------------------------------
# settings.py
# ---------------------------------------------------------------------------


def _augment_settings_fields(
    svc: ServiceNode,
    spec: ComposeSpec,
) -> dict[str, str]:
    """Collect settings fields contributed by all augments on a service.

    Returns a dict of ``{field_name: default_value_expr}``.  Static fields
    come from the descriptor's ``settings_fields``; dynamic fields are
    resolved via the ``resolve_settings_fields`` callback.

    Raises ``ValueError`` on field name collisions between augments.
    """
    fields: dict[str, str] = {}
    field_owners: dict[str, str] = {}  # field_name → augment_name

    def _merge(augment_fields: dict[str, str], owner_name: str) -> None:
        for field_name in augment_fields:
            if field_name in field_owners:
                raise ValueError(
                    f"Settings field '{field_name}' on service '{svc.name}' "
                    f"is contributed by both '{field_owners[field_name]}' and "
                    f"'{owner_name}'. Augments must not declare the same "
                    f"settings field."
                )
            field_owners[field_name] = owner_name
        fields.update(augment_fields)

    # Workspace augments that apply to this service's role
    for ws_aug in spec.workspace.augments:
        desc = AUGMENT_REGISTRY.get(ws_aug.name)
        if desc is None or desc.applies_to_role != svc.role:
            continue

        ws_fields: dict[str, str] = dict(desc.settings_fields)
        if desc.resolve_settings_fields is not None:
            # Create a synthetic ServiceAugment for the resolver interface
            sa = ServiceAugment(name=ws_aug.name, options=ws_aug.options)
            ws_fields.update(desc.resolve_settings_fields(sa, svc, spec))
        _merge(ws_fields, ws_aug.name)

    for augment in svc.augments:
        desc = AUGMENT_REGISTRY.get(augment.name)
        if desc is None:
            continue

        augment_fields: dict[str, str] = dict(desc.settings_fields)
        if desc.resolve_settings_fields is not None:
            augment_fields.update(desc.resolve_settings_fields(augment, svc, spec))
        _merge(augment_fields, augment.name)

    return fields


def render_settings(svc: ServiceNode, spec: ComposeSpec) -> str:
    """Render ``settings.py`` from base fields + augment contributions."""
    augment_fields = _augment_settings_fields(svc, spec)

    lines = [
        "from csrd.models import BaseSettings",
        "",
        "",
        "class Settings(BaseSettings):",
        "",
        f'    app_name: str = "{svc.name}"',
    ]

    # Worker services don't expose HTTP, so no port or actuator fields
    if svc.role != "worker":
        lines.append(f"    port: int = {svc.port}")
        actuator_default = "True" if svc.include_actuator else "False"
        lines.append(f"    include_actuator_endpoints: bool = {actuator_default}")

    if augment_fields:
        lines.append("")
        lines.append("    # Augment-contributed fields")
        for field_name, default in sorted(augment_fields.items()):
            # Infer type from default value syntax
            if default.startswith('"') or default.startswith("'"):
                field_type = "str"
            elif default in ("True", "False"):
                field_type = "bool"
            elif default.isdigit():
                field_type = "int"
            else:
                field_type = "str"
            lines.append(f"    {field_name}: {field_type} = {default}")

    lines.extend(
        [
            "",
            "",
            "settings = Settings()",
            "",
        ]
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# __init__.py
# ---------------------------------------------------------------------------


def render_init(svc: ServiceNode, spec: ComposeSpec) -> str:
    """Render ``__init__.py`` with ``build_app()`` + augment middleware/handlers."""

    # Worker services get a minimal __init__.py that re-exports celery_app
    if svc.role == "worker":
        return (
            '"""Worker service — Celery task processor."""\n'
            "\n"
            "from .celery_app import app as celery_app\n"
            "\n"
            '__all__ = ("celery_app",)\n'
        )

    # Gateway services get a plain FastAPI app — no versioning middleware.
    # The proxy catches all paths as-is; versioning would mangle URLs
    # before the proxy view can match them against the route table.
    if svc.role == "gateway":
        return _render_gateway_init(svc, spec)

    # Collect all augment descriptors that apply to this service
    descriptors: list[tuple[str, AugmentDescriptor]] = []

    # Workspace augments targeting this service's role
    for ws_aug in spec.workspace.augments:
        desc = AUGMENT_REGISTRY.get(ws_aug.name)
        if desc is not None and desc.applies_to_role == svc.role:
            descriptors.append((ws_aug.name, desc))

    # Service-scope augments
    for augment in svc.augments:
        desc = AUGMENT_REGISTRY.get(augment.name)
        if desc is not None:
            descriptors.append((augment.name, desc))

    # Check whether this service needs a database lifespan (connect, migrate, close).
    # Both db-config and jwt-auth-provider use the same lifespan pattern.
    has_db = any(name in ("db-config", "jwt-auth-provider") for name, _ in descriptors)
    has_rabbit = any(name == "rabbit-messaging" for name, _ in descriptors)
    has_caching = any(name == "caching" for name, _ in descriptors)
    has_tracing = any(name == "tracing" for name, _ in descriptors)
    needs_lifespan = has_db or has_rabbit or has_caching

    # Collect imports
    imports = [
        "from fastapi import FastAPI",
        "",
        "from csrd.versioning import (",
        "    UNVERSIONED,",
        "    VersionedApiConfig,",
        "    VersionedAppComposeConfig,",
        "    compose_versioned_apps,",
        ")",
        "",
        "from .settings import settings",
        "from .views import app as unversioned_app",
    ]

    # Migration startup imports (lifespan pattern)
    if needs_lifespan:
        imports.append("")
        imports.append("from contextlib import asynccontextmanager")
        imports.append("from collections.abc import AsyncIterator")
        imports.append("")
        imports.append("from csrd.lifespan import lifespan_stack")

    if has_db:
        imports.append("from csrd.migration import MigrationRunner")
        imports.append("from .dependencies.db import create_adapter")
        imports.append("from .migrations import migrations")

    if has_rabbit:
        imports.append("from .dependencies.rabbit import create_rabbit_lifespan")

    if has_caching:
        imports.append("")
        imports.append("import redis")

    if has_tracing:
        imports.append("")
        imports.append("from .middleware.tracing import configure_tracing")

    # Router imports (from descriptors)
    router_aliases: list[str] = []
    for _name, desc in descriptors:
        for r in desc.routers:
            alias = r.alias or r.import_path.rsplit(".", 1)[-1] + "_router"
            imports.append(f"from {r.import_path} import {r.attr} as {alias}")
            router_aliases.append(alias)

    # Dynamic routers from descriptor callbacks (e.g. entity-named views)
    for augment in svc.augments:
        desc = AUGMENT_REGISTRY.get(augment.name)
        if desc is not None and desc.resolve_dynamic_routers is not None:
            for import_line, alias in desc.resolve_dynamic_routers(augment, svc, spec):
                imports.append(import_line)
                router_aliases.append(alias)

    # Middleware imports
    middleware_classes: list[str] = []
    for _name, desc in descriptors:
        for m in desc.middleware:
            imports.append("")
            imports.append(f"from {m.import_path} import {m.class_name}")
            middleware_classes.append(m.class_name)

    # Gateway auth middleware (only when gateway has jwt-auth-consumer)
    has_gateway_proxy = any(name == "gateway-proxy" for name, _ in descriptors)
    has_jwt_consumer = any(name == "jwt-auth-consumer" for name, _ in descriptors)
    if has_gateway_proxy and has_jwt_consumer:
        imports.append("")
        imports.append("from .middleware.auth_guard import GatewayAuthMiddleware")
        middleware_classes.append("GatewayAuthMiddleware")

    # Exception handler imports
    handler_pairs: list[tuple[str, str]] = []  # (exception_class, handler_name)
    for _name, desc in descriptors:
        for eh in desc.exception_handlers:
            imports.append("")
            imports.append(f"from {eh.import_path} import {eh.handler_name}")
            handler_pairs.append((eh.exception_class, eh.handler_name))

    # Build app body
    body = [
        "",
        "",
    ]

    # Generate lifespan function for database services
    if has_db:
        body.extend(
            [
                "@asynccontextmanager",
                "async def _db_lifespan(app: FastAPI) -> AsyncIterator[dict[str, object]]:",
                '    """Connect database, run migrations, and close on shutdown."""',
                "    adapter = create_adapter(settings)",
                "    await adapter.connect()",
                "    runner = MigrationRunner()",
                "    await runner.apply_all(adapter, migrations)",
                '    yield {"db_adapter": adapter}',
                "    await adapter.close()",
                "",
                "",
            ]
        )

    # Generate rabbit lifespan reference
    if has_rabbit:
        body.extend(
            [
                "_rabbit_lifespan = create_rabbit_lifespan(settings)",
                "",
                "",
            ]
        )

    # Generate cache lifespan (connect on startup, close on shutdown)
    if has_caching:
        body.extend(
            [
                "@asynccontextmanager",
                "async def _cache_lifespan(app: FastAPI) -> AsyncIterator[dict[str, object]]:",
                '    """Connect Redis cache on startup, close on shutdown."""',
                "    client = redis.from_url(settings.cache_url, decode_responses=True)",
                '    yield {"cache": client}',
                "    client.close()",
                "",
                "",
            ]
        )

    body.append("def build_app() -> FastAPI:")

    # Wire routers
    if router_aliases:
        for alias in router_aliases:
            body.append(f"    unversioned_app.include_router({alias})")
        body.append("")

    body.extend(
        [
            "    app = compose_versioned_apps(",
            "        version_mapping={UNVERSIONED: unversioned_app},",
            "        config=VersionedAppComposeConfig(",
            f'            title="{svc.name}",',
            '            app_state={"settings": settings},',
            "            api=VersionedApiConfig(",
            '                prefix="/",',
            "                app_name=settings.app_name,",
            "                include_actuator_endpoints=settings.include_actuator_endpoints,",
            "            ),",
        ]
    )

    if needs_lifespan:
        lifespan_args: list[str] = []
        if has_db:
            lifespan_args.append("_db_lifespan")
        if has_rabbit:
            lifespan_args.append("_rabbit_lifespan")
        if has_caching:
            lifespan_args.append("_cache_lifespan")
        body.append(f"            lifespan=lifespan_stack({', '.join(lifespan_args)}),")

    body.append("        ),")
    body.append("    )")

    # Wire middleware
    for cls in middleware_classes:
        body.append("")
        body.append(f"    app.add_middleware({cls})")

    # Wire exception handlers
    for exc_cls, handler in handler_pairs:
        body.append("")
        body.append(f"    app.add_exception_handler({exc_cls}, {handler})")

    # Tracing startup
    if has_tracing:
        body.append("")
        body.append("    configure_tracing()")

    body.extend(
        [
            "",
            "    return app",
            "",
            "",
            '__all__ = ("build_app",)',
            "",
        ]
    )

    return "\n".join(imports + body)


def _render_gateway_init(svc: ServiceNode, spec: ComposeSpec) -> str:
    """Render a gateway ``__init__.py`` with plain FastAPI (no versioning)."""

    # Collect all augment descriptors for this service
    descriptors: list[tuple[str, AugmentDescriptor]] = []
    for ws_aug in spec.workspace.augments:
        desc = AUGMENT_REGISTRY.get(ws_aug.name)
        if desc is not None and desc.applies_to_role == svc.role:
            descriptors.append((ws_aug.name, desc))
    for augment in svc.augments:
        desc = AUGMENT_REGISTRY.get(augment.name)
        if desc is not None:
            descriptors.append((augment.name, desc))

    imports = [
        '"""Gateway service — transparent reverse proxy with JWT guard."""',
        "",
        "from fastapi import FastAPI",
        "",
        "from .settings import settings",
    ]

    # Router imports
    router_aliases: list[str] = []
    for _name, desc in descriptors:
        for r in desc.routers:
            alias = r.alias or r.import_path.rsplit(".", 1)[-1] + "_router"
            imports.append(f"from {r.import_path} import {r.attr} as {alias}")
            router_aliases.append(alias)

    # Middleware imports
    middleware_classes: list[str] = []
    for _name, desc in descriptors:
        for m in desc.middleware:
            imports.append("")
            imports.append(f"from {m.import_path} import {m.class_name}")
            middleware_classes.append(m.class_name)

    # Gateway auth middleware
    has_gateway_proxy = any(name == "gateway-proxy" for name, _ in descriptors)
    has_jwt_consumer = any(name == "jwt-auth-consumer" for name, _ in descriptors)
    if has_gateway_proxy and has_jwt_consumer:
        imports.append("")
        imports.append("from .middleware.auth_guard import GatewayAuthMiddleware")
        middleware_classes.append("GatewayAuthMiddleware")

    body = [
        "",
        "",
        "def build_app() -> FastAPI:",
        f'    app = FastAPI(title="{svc.name}")',
        "    app.state.settings = settings",
        "",
        "    # Health endpoint — registered before the catch-all proxy route",
        '    @app.get("/_info/health", include_in_schema=False)',
        "    async def health() -> dict[str, str]:",
        '        return {"status": "UP"}',
        "",
    ]

    # Wire routers — the proxy catch-all must come AFTER /_info/health
    if router_aliases:
        for alias in router_aliases:
            body.append(f"    app.include_router({alias})")
        body.append("")

    # Wire middleware
    for cls in middleware_classes:
        body.append("")
        body.append(f"    app.add_middleware({cls})")

    body.extend(
        [
            "",
            "    return app",
            "",
            "",
            '__all__ = ("build_app",)',
            "",
        ]
    )

    return "\n".join(imports + body)


# ---------------------------------------------------------------------------
# migrations.py
# ---------------------------------------------------------------------------


def render_migrations(svc: ServiceNode, spec: ComposeSpec) -> str | None:
    """Render ``migrations.py`` with auto-imported crud-scaffold migrations.

    Returns ``None`` when the service has no ``db-config`` augment.

    The rendered file is designed to work both ways:

    * **With the generator** — crud-scaffold entity migrations are
      auto-imported on each render.  Re-running the generator picks up
      new entities.
    * **Without the generator** — users can add migrations directly
      to the list or import from their own ``migrations_*.py`` files.
      The file is plain Python; no special tooling required.
    """
    augment_names: set[str] = set()
    for ws_aug in spec.workspace.augments:
        desc = AUGMENT_REGISTRY.get(ws_aug.name)
        if desc is not None and desc.applies_to_role == svc.role:
            augment_names.add(ws_aug.name)
    for augment in svc.augments:
        augment_names.add(augment.name)

    if "db-config" not in augment_names:
        return None

    # Collect entity names from augments with dynamic migration resolvers
    migration_imports: list[tuple[str, str]] = []  # (import_line, var_name)
    for augment in svc.augments:
        desc = AUGMENT_REGISTRY.get(augment.name)
        if desc is not None and desc.resolve_dynamic_migrations is not None:
            migration_imports.extend(desc.resolve_dynamic_migrations(augment, svc, spec))

    lines = [
        '"""Database migrations for this service.',
        "",
        "This file is rendered by the generator but is safe to edit directly.",
        "If you stop using the generator, just add Migration entries to the list.",
        '"""',
        "",
        "from csrd.migration import Migration",
    ]

    if migration_imports:
        lines.append("")
        for import_line, _var_name in migration_imports:
            lines.append(import_line)

    lines.append("")
    lines.append("")
    lines.append("migrations: list[Migration] = [")

    if migration_imports:
        for _import_line, var_name in migration_imports:
            lines.append(f"    {var_name},")
        lines.append("    # Add custom migrations below this line")
    else:
        lines.append("    # Migration(")
        lines.append('    #     version="001",')
        lines.append('    #     description="Initial schema",')
        lines.append('    #     up="CREATE TABLE ...",')
        lines.append('    #     down="DROP TABLE ...",')
        lines.append("    # ),")

    lines.append("]")
    lines.append("")
    lines.append('__all__ = ("migrations",)')
    lines.append("")

    return "\n".join(lines)
