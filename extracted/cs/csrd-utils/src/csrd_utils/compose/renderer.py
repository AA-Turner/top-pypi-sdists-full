"""Pure spec-to-content renderers for workspace artifacts.

Every function in this module is a **pure transform** from ``ComposeSpec``
(or no input) to a string.  No filesystem I/O, no spec mutations, no
side effects.  Orchestration lives in ``operations.py``.
"""

from typing import Any

from ..models import ComposeSpec, ServiceAugment, ServiceNode
from .augments import AUGMENT_REGISTRY
from .infra import (
    INFRA_REGISTRY,
    render_infra,
)
from .yaml_editor import dumps_yaml

WORKSPACE_MARKER_FILENAME = ".csrd-workspace"


# ---------------------------------------------------------------------------
# docker-compose.yml rendering
# ---------------------------------------------------------------------------


def _wire_feature(
    feature: str,
    *,
    infra_types: set[str],
    deps: dict[str, Any],
    env: dict[str, str],
    volumes: dict[str, None],
    spec: ComposeSpec,
) -> None:
    """Wire a single feature tag into deps/env/volumes via the infra registry.

    Database features are handled by augments (db-config, jwt-auth-provider)
    and skipped in ``_render_service`` before reaching this function.
    """

    # Generic feature wiring (caching, messaging, …)
    for desc in INFRA_REGISTRY.values():
        if desc.feature == feature and desc.name in infra_types:
            deps.update(desc.depends_on)
            env.update(desc.service_env)


def _wire_augment(
    augment: ServiceAugment,
    *,
    svc: ServiceNode,
    spec: ComposeSpec,
    deps: dict[str, Any],
    env: dict[str, str],
    volumes: dict[str, None],
) -> None:
    """Wire a single service augment into deps/env/volumes via the augment registry.

    Static ``compose_env`` and ``compose_depends_on`` from the descriptor
    are applied unconditionally.  Dynamic values are resolved via the
    descriptor's resolver callbacks.  Wiring is idempotent — duplicate
    keys are silently deduplicated.
    """
    desc = AUGMENT_REGISTRY.get(augment.name)
    if desc is None:
        return

    # Static env/depends_on from descriptor
    env.update(desc.compose_env)
    for dep_name in desc.compose_depends_on:
        if dep_name != svc.name:
            deps[dep_name] = {"condition": "service_started"}

    # Dynamic env from resolver callback
    if desc.resolve_compose_env is not None:
        dynamic_env = desc.resolve_compose_env(augment, svc, spec)
        env.update(dynamic_env)
        # Auto-wire depends_on for services referenced in dynamic env
        for _key, value in dynamic_env.items():
            if value.startswith("http://"):
                host = value.split("://", 1)[1].split(":", 1)[0].split("/", 1)[0]
                if host != svc.name:
                    deps[host] = {"condition": "service_started"}

    # Dynamic depends_on from resolver (e.g. database container)
    if desc.resolve_compose_deps is not None:
        dynamic_deps = desc.resolve_compose_deps(augment, svc, spec)
        for dep_name, condition in dynamic_deps.items():
            if dep_name != svc.name:
                deps[dep_name] = (
                    condition if isinstance(condition, dict) else {"condition": condition}
                )

    # Dynamic volumes from resolver (e.g. sqlite per-service volume)
    if desc.resolve_compose_volumes is not None:
        dynamic_vols = desc.resolve_compose_volumes(augment, svc, spec)
        for vol_name in dynamic_vols:
            volumes[vol_name] = None


def _render_service(
    svc: ServiceNode,
    *,
    spec: ComposeSpec,
    base_port_offset: int,
) -> tuple[dict[str, Any], dict[str, None]]:
    """Build a compose service dict and its volumes for a single ServiceNode.

    Wiring is driven by the service's *features* list.  Each feature
    (``database``, ``caching``, ``messaging``) contributes ``depends_on``,
    ``environment``, and/or ``volumes`` entries sourced from the workspace
    infra configuration.

    Returns ``(service_dict, volumes_dict)``.
    """

    svc_def: dict[str, Any] = {
        "build": {
            "context": ".",
            "dockerfile": f"Dockerfile.{svc.name}",
        },
        "ports": [f"{svc.port + base_port_offset}:{svc.port + base_port_offset}"],
        "env_file": ".env",
    }

    # Frontend services: no Python wiring, just volume mount for hot reload
    if svc.role == "frontend":
        svc_snake = svc.name.replace("-", "_")
        svc_def["volumes"] = [
            f"./src/{svc_snake}/src:/app/src/{svc_snake}/src",
            f"./src/{svc_snake}/index.html:/app/src/{svc_snake}/index.html",
        ]
        # Sensible container defaults for Vite-based frontends.  The app
        # inside the container must bind to the container port (not the
        # host-side port which may differ via override).
        gateway = next((s for s in spec.services if s.role == "gateway"), None)
        gateway_target = (
            f"http://{gateway.name}:{gateway.port}" if gateway else "http://localhost:8000"
        )
        svc_def["environment"] = {
            "VITE_PORT": str(svc.port),
            "VITE_HOST": "0.0.0.0",
            "VITE_API_TARGET": gateway_target,
        }
        return svc_def, {}

    deps: dict[str, Any] = {}
    env: dict[str, str] = {}
    volumes: dict[str, None] = {}
    infra_types = {n.type for n in spec.infra}

    for feature in svc.features:
        # Database wiring is now handled by augments (db-config, jwt-auth-provider)
        if feature == "database":
            continue
        _wire_feature(
            feature,
            infra_types=infra_types,
            deps=deps,
            env=env,
            volumes=volumes,
            spec=spec,
        )

    # Augment wiring (application-level concerns)
    env_owners: dict[str, str] = {}  # env_key → augment_name (collision detection)
    for augment in svc.augments:
        env_before = set(env.keys())
        _wire_augment(
            augment,
            svc=svc,
            spec=spec,
            deps=deps,
            env=env,
            volumes=volumes,
        )
        # Check for env key collisions between augments
        new_keys = set(env.keys()) - env_before
        for key in new_keys:
            if key in env_owners:
                raise ValueError(
                    f"Environment variable '{key}' on service '{svc.name}' "
                    f"is contributed by both '{env_owners[key]}' and "
                    f"'{augment.name}'. This is a conflict — augments must "
                    f"not write the same environment variable."
                )
            env_owners[key] = augment.name

    # Workspace augment wiring (e.g. jwt-auth-provider → auth-service)
    for ws_aug in spec.workspace.augments:
        desc = AUGMENT_REGISTRY.get(ws_aug.name)
        if desc is None or desc.applies_to_role != svc.role:
            continue
        synthetic = ServiceAugment(name=ws_aug.name, options=dict(ws_aug.options))
        env_before = set(env.keys())
        _wire_augment(
            synthetic,
            svc=svc,
            spec=spec,
            deps=deps,
            env=env,
            volumes=volumes,
        )
        new_keys = set(env.keys()) - env_before
        for key in new_keys:
            if key in env_owners:
                raise ValueError(
                    f"Environment variable '{key}' on service '{svc.name}' "
                    f"is contributed by both '{env_owners[key]}' and "
                    f"'{ws_aug.name}'. This is a conflict."
                )
            env_owners[key] = ws_aug.name

    # sqlite per-service volume
    if volumes:
        svc_def["volumes"] = [f"{vol}:/app/data" for vol in volumes]

    if deps:
        svc_def["depends_on"] = deps
    if env:
        svc_def["environment"] = env

    # Worker services: no ports, celery command instead of uvicorn
    if svc.role == "worker":
        svc_def.pop("ports", None)
        svc_snake = svc.name.replace("-", "_")
        svc_def["command"] = f"celery -A {svc_snake}.celery_app worker --loglevel=info"

    # Gateway services: mount route config file
    if svc.role == "gateway":
        svc_snake = svc.name.replace("-", "_")
        svc_volumes = svc_def.get("volumes", [])
        svc_volumes.append(f"./src/{svc_snake}/gateway-routes.yaml:/app/gateway-routes.yaml:ro")
        svc_def["volumes"] = svc_volumes

    return svc_def, volumes


def _render_compose(spec: ComposeSpec) -> str:
    """Build the full ``docker-compose.yml`` content from the spec."""

    services: dict[str, Any] = {}
    volumes: dict[str, None] = {}

    # --- Infra containers first ---
    for infra_node in spec.infra:
        desc = INFRA_REGISTRY.get(infra_node.type)
        if desc is None or not desc.has_container:
            continue
        name, svc_def, vol_defs = render_infra(infra_node.type)
        services[name] = svc_def
        volumes.update(vol_defs)

    # --- Application services ---
    for svc in spec.services:
        svc_def, svc_volumes = _render_service(svc, spec=spec, base_port_offset=0)
        services[svc.name] = svc_def
        volumes.update(svc_volumes)

    payload: dict[str, Any] = {"services": services}
    if volumes:
        payload["volumes"] = volumes

    return dumps_yaml(payload)


# ---------------------------------------------------------------------------
# Env example rendering
# ---------------------------------------------------------------------------


def _render_env_example(spec: ComposeSpec) -> str:
    """Build ``.env.example`` with sensible defaults for configured infra."""

    lines = ["# Workspace defaults\n"]

    seen_features: set[str] = set()
    for infra_node in spec.infra:
        desc = INFRA_REGISTRY.get(infra_node.type)
        if desc is None or not desc.env_example_lines:
            continue
        # Avoid duplicate sections for the same feature (e.g. two DB types)
        if desc.feature in seen_features:
            continue
        seen_features.add(desc.feature)
        lines.extend(desc.env_example_lines)
        lines.append("")

    # Workspace augment env example lines (data-driven)
    for ws_aug in spec.workspace.augments:
        aug_desc = AUGMENT_REGISTRY.get(ws_aug.name)
        if aug_desc is None:
            continue

        # Dynamic resolver takes priority
        if aug_desc.resolve_env_example_lines is not None:
            example_lines = aug_desc.resolve_env_example_lines(ws_aug, spec)
            if example_lines:
                lines.extend(example_lines)
                lines.append("")
        elif aug_desc.env_example_lines:
            lines.extend(aug_desc.env_example_lines)
            lines.append("")

    # Service augment env example lines
    seen_augments: set[str] = set()
    seen_env_blocks: set[tuple[str, ...]] = set()
    for svc in spec.services:
        for augment in svc.augments:
            if augment.name in seen_augments:
                continue
            aug_desc = AUGMENT_REGISTRY.get(augment.name)
            if aug_desc is None:
                continue
            if aug_desc.env_example_lines:
                block = tuple(aug_desc.env_example_lines)
                if block in seen_env_blocks:
                    seen_augments.add(augment.name)
                    continue
                seen_augments.add(augment.name)
                seen_env_blocks.add(block)
                lines.extend(aug_desc.env_example_lines)
                lines.append("")

    return "\n".join(lines) + "\n"


def _render_readme(spec: ComposeSpec) -> str:
    """Build a starter ``README.md`` for the workspace."""

    svc_lines = ""
    if spec.services:
        svc_list = ", ".join(f"`{s.name}` (:{s.port})" for s in spec.services)
        svc_lines = f"\n## Services\n\n{svc_list}\n"

    return (
        f"# {spec.workspace.name}\n\n"
        "Generated by [csrd](https://github.com/csrd-api/fastapi-common).\n"
        f"{svc_lines}\n"
        "## Quick start\n\n"
        "```bash\n"
        "docker compose up --build\n"
        "```\n\n"
        "## Workspace commands\n\n"
        "```bash\n"
        "csrd generate                # interactive menu\n"
        "csrd generate add-service    # add a service\n"
        "csrd generate rename-service # rename a service\n"
        "csrd doctor                  # validate service layout\n"
        "csrd audit                   # scan for insecure defaults\n"
        "csrd compose validate        # validate csrd-compose.yaml\n"
        "```\n\n"
        "Edit `csrd-compose.yaml` then run `csrd compose apply` to re-render.\n"
    )


def _render_gitignore() -> str:
    """Build a default ``.gitignore`` for the workspace."""

    return (
        "# Runtime env files\n"
        ".env\n"
        "\n"
        "# Docker Compose local overrides (user-specific port mappings, etc.)\n"
        "docker-compose.override.yml\n"
        "\n"
        "# Python cache\n"
        "__pycache__/\n"
        "*.py[cod]\n"
        "\n"
        "# Test and tooling cache\n"
        ".pytest_cache/\n"
        ".mypy_cache/\n"
        ".ruff_cache/\n"
    )


def _render_pyproject(spec: ComposeSpec) -> str:
    """Build a workspace-level ``pyproject.toml`` with pytest config."""

    service_src_paths = [f"src/{svc.name.replace('-', '_')}" for svc in spec.services]

    lines = [
        "[project]",
        f'name = "{spec.workspace.name}"',
        'version = "0.1.0"',
        'requires-python = ">=3.12"',
        "",
        "[tool.pytest.ini_options]",
        'testpaths = ["tests"]',
        'python_files = ["test_*.py"]',
        'python_classes = ["Test*"]',
        'python_functions = ["test_*"]',
    ]

    if service_src_paths:
        lines.append("pythonpath = [")
        for p in service_src_paths:
            lines.append(f'    "{p}",')
        lines.append("]")

    lines.append("")
    return "\n".join(lines) + "\n"


def _render_workspace_marker() -> str:
    """Build the ``.csrd-workspace`` marker file content."""

    return "workspace: csrd\n"


def _render_agents_md(spec: ComposeSpec) -> str:
    """Build an ``AGENTS.md`` describing the csrd framework for workspace developers."""

    ws_name = spec.workspace.name

    return f"""\
# {ws_name} — Agent & Developer Guide

This workspace was generated by **csrd compose**.  The services in this
workspace are built on the `csrd-*` library stack — a set of independent
PyPI packages that provide reusable FastAPI building blocks.

> **Before implementing logic**, check the library index below.  If a
> capability exists in a `csrd-*` package, use the library import — do
> not reimplement it in service code.

---

## Workspace structure

| Path | Purpose |
|---|---|
| `csrd-compose.yaml` | **Source of truth** — declarative workspace spec |
| `docker-compose.yml` | Rendered from spec (regenerated on apply) |
| `.env.example` | Environment variable template |
| `src/<service>/` | Service source trees |
| `src/<service>/settings.py` | Initially generated — yours to modify |
| `src/<service>/__init__.py` | Initially generated — yours to modify |
| `src/<service>/requirements.txt` | Initially generated — yours to modify |
| `src/<service>/views/` | User-owned — add endpoints here |
| `src/<service>/repositories/` | User-owned — add data access here |
| `src/<service>/services/` | User-owned — add business logic here |
| `src/<service>/dependencies/` | User-owned — add FastAPI dependencies here |

**File ownership**: All files listed above are yours after initial generation.
The generator will not overwrite files that already exist unless you explicitly
run `csrd compose apply --force`. Once you start building features, treat every
file as fully owned — modify settings.py, __init__.py, requirements.txt, etc.
freely as your implementation requires.

---

## csrd-* library packages

### csrd-models
`pip install csrd-models` · `from csrd.models import ...`

Pydantic v2 `BaseModel` (camelCase aliases), `BaseSettings` (.env loading),
`UserClaims` dataclass, `APIErrorResponse`, error models, `model_parser`
for DB row → model conversion.

### csrd-context
`pip install csrd-context` · `from csrd.context import ...`

Request-scoped context via `contextvars`.  `RequestContextMiddleware`
extracts hit ID, app ID, path/query params.  Context variables:
`user_info_context`, `hit_id_context`, `app_id_context`.

### csrd-auth
`pip install csrd-auth` · `from csrd.auth import ...`

Pluggable JWT authentication.  Authenticators: `JWTAuthenticator`,
`RemoteAuthenticator`, `CallbackAuthenticator`, `ChainedAuthenticator`,
`StaticAuthenticator`.  Key providers: `StaticKeyProvider`,
`EnvKeyProvider`, `JWKSKeyProvider`, `MultiKeyProvider`,
`CallbackKeyProvider`.  Guards: `require_authorities()`,
`require_any_authority()`.  Factory: `create_jwt_bearer()`,
`create_bearer_dependency()`.  Key ring: `KeyRingManager` for RSA key
lifecycle.

### csrd-repository
`pip install csrd-repository` · `from csrd.repository import ...`

Repository pattern with async database adapters.  `SQLiteAdapter` (aiosqlite),
`PGAdapter` (psycopg), `MariaAdapter` (pymysql).  `BaseRepository` with
`fetch_one`, `fetch_all`, `require_one`, `insert`, `update`, `upsert`,
`delete`.

### csrd-migration
`pip install csrd-migration` · `from csrd.migration import ...`

`Migration` dataclass (`version`, `description`, `up` SQL, `down` SQL).
`MigrationRunner` applies/rollbacks migrations using any adapter, tracks
versions in `_csrd_migrations` table.

### csrd-service
`pip install csrd-service` · `from csrd.service import ...`

`BaseService` base class.  Domain errors: `ServiceError` (500),
`NotFoundError` (404), `ConflictError` (409), `ValidationError` (422),
`AuthorizationError` (403), `DownstreamError` (502).
`service_exception_handler` maps errors to `APIErrorResponse` JSON.

### csrd-delegate
`pip install csrd-delegate` · `from csrd.delegate import ...`

`BaseDelegate` for inter-service HTTP calls with auth header forwarding.
`RetryProfile` for retry config.

### csrd-logging
`pip install csrd-logging` · `from csrd.logging import ...`

`ContextLogger` (stdlib wrapper with request context enrichment),
`LoggingMixin` (optional auto-instrumentation), `RequestContextFilter`.

### csrd-lifespan
`pip install csrd-lifespan` · `from csrd.lifespan import ...`

`lifespan_stack(*lifespans)` — compose multiple async context manager
lifespans into one for FastAPI.

### csrd-versioning
`pip install csrd-versioning` · `from csrd.versioning import ...`

`compose_versioned_apps(version_mapping, config)` — API version dispatch,
OpenAPI docs, actuator endpoints (`/health`, `/info`).

### csrd-message
`pip install csrd-message` · `from csrd.message import ...`

Transport-agnostic `MessagePublisher` / `MessageConsumer` protocols.
RabbitMQ adapter (`csrd-message[rabbit]`): `RabbitPublisher`,
`RabbitConsumer`, `RabbitMessageHandler`, `RabbitLifespan`, dead-letter
exchange wiring.

---

## Common patterns

### Auth flow (provider → consumer)
```
KeyRingManager → signs JWT → /.well-known/jwks.json
                                    ↓
JWKSKeyProvider → fetches keys → JWTAuthenticator → UserClaims
                                                        ↓
                                              user_info_context.set()
                                                        ↓
                                              require_authorities()
```

### Database flow
```
SQLiteAdapter / PGAdapter / MariaAdapter
        ↓
BaseRepository (fetch_one, insert, upsert, ...)
        ↓
MigrationRunner.apply_all(adapter, migrations)
```

### Error handling flow
```
Business logic raises ServiceError (NotFoundError, ConflictError, ...)
        ↓
service_exception_handler → APIErrorResponse JSON
```

---

## Dependency tiers

```
Tier 3:  csrd.versioning  ──→  csrd.context, csrd.models
Tier 2:  csrd.delegate    ──→  csrd.models
         csrd.repository  ──→  csrd.models
         csrd.service     ──→  csrd.context, csrd.models
Tier 1.5: csrd.auth       ──→  csrd.context, csrd.models
          csrd.logging     ──→  csrd.context
Tier 1:  csrd.context     ──→  csrd.models
         csrd.models       (standalone)
         csrd.message      (standalone)
         csrd.lifespan     (standalone)
```

Higher-tier packages may depend on lower tiers.  Same-tier and reverse
dependencies are forbidden.

---

## Re-rendering this workspace

```bash
# Edit csrd-compose.yaml, then:
csrd compose apply

# Or use the interactive menu:
csrd generate

# Rename a service (updates spec, directories, code references):
csrd generate rename-service

# Install tab completion (one-time):
csrd completion install
```

`docker-compose.yml` is always regenerated from the spec.  Scaffolded files
(views, repositories, services, dependencies) are never overwritten — your
custom code is safe.  Files like `settings.py`, `__init__.py`, and
`pyproject.toml` (per-service) are only written on first scaffold; once they
exist they are yours.

Set `CSRD_NO_TTY=1` to force numbered-fallback prompts instead of the
arrow-key TUI (useful for scripting or CI).

---

## Workflow — Feature Development Lifecycle

Features are developed in three phases.  Each phase is a separate
conversation turn — do NOT proceed to the next phase without user
confirmation.

### Phase 1: Design Dialog

Triggered by: "let's plan the next feature" / "let's design X"

1. Discuss requirements, propose options, hash out tradeoffs.
2. Document decisions in DESIGN.md (or relevant design doc).
3. STOP.  Summarize and wait for confirmation.

### Phase 2: Implementation Plan

Triggered by: "let's build the plan" / "plan this out"

1. Read finalized design from DESIGN.md.
2. Break into milestones with checklists in IMPLEMENTATION_PLAN.md.
3. STOP.  Present plan summary and wait for approval.

### Phase 3: Execution (one milestone at a time)

Triggered by: "start M0" / "do the next milestone" / "go"

1. Execute one milestone only.
2. Commit with clear message.
3. Mark milestone complete in IMPLEMENTATION_PLAN.md.
4. STOP.  Report what was done and wait for "continue."

### Workflow rules

- Never execute more than one milestone without checking in.
- If something unexpected happens, stop and report.
- User may say "finish M2 then check back in" — do that milestone, then stop.

---

## Handling csrd-* library gaps

> **Sync note**: This section is the *sender/writer* side of the gap report
> workflow.  The *receiver/consumer* side — how the csrd-* maintainer handles
> an incoming report — lives in the root `AGENTS.md` of the csrd-* repo
> (`## Handling downstream gap reports`).  Lifecycle state names and
> migration-guide format requirements must stay in sync across both sides.

If you discover a missing, broken, or painful behavior in a csrd-* package
during implementation, write a gap report and paste it into the csrd-* repo's
agentic chat.

#### Report types

Every report must declare its type on the first line: `TYPE: DEFICIT` or
`TYPE: FRICTION`.

**DEFICIT** — An articulable technical defect.  Something is missing or
broken: an API does not exist, output is wrong, a required feature has no
implementation.  A workaround is in place while waiting for the fix.

**FRICTION** — A discovered pain point.  The behavior works but is awkward,
tedious, or rough.  No workaround required.  Does not block downstream work.

#### Report format

Gap reports are plain-text documents designed to be pasted directly into
an agentic chat session with the csrd-* maintainer.  They must:

- **Not use nested markdown** (no fenced code blocks inside fenced blocks,
  no deep heading hierarchies) — keep it flat so it renders cleanly when
  pasted into a chat input.
- **State clearly** that this is a gap report generated during usage of a
  csrd-* library in a downstream project.
- **Declare the type** (`TYPE: DEFICIT` or `TYPE: FRICTION`) on the first line.

Structure for DEFICIT reports:
1. TYPE: DEFICIT — one-line summary
2. What was expected vs what happened
3. Workaround currently in place (with inline code, not fenced blocks)
4. Proposed fix for the csrd-* package
5. Request for a migration guide — ask the csrd-* agent to return a
   document describing: what changed in the library, the new API/behavior,
   and what the downstream repo should update (imports, removed overrides,
   config changes) so this repo can be adjusted when the fix ships
6. Acceptance criteria for closure — specific, verifiable checks that
   must all pass before the report is deleted (e.g. "installed version
   includes X", "workaround removed from file Y", "tests pass").
   These may be refined after the csrd-* agent responds with its
   migration guide — update the criteria based on what the fix actually changed.

Structure for FRICTION reports:
1. TYPE: FRICTION — one-line summary
2. What currently happens and why it is painful
3. What a better experience would look like
4. No workaround section required — note "no workaround needed" explicitly
5. No acceptance criteria required at filing time

Response formatting rules (include in every DEFICIT report):
- Ask the csrd-* agent to return its migration guide as a **single
  plain-text code block** with no nested markdown inside.
- The response must be directly pasteable into this repo's agentic
  chat session without requiring reformatting.
- The response must identify itself as a migration guide in reply to
  the specific gap report (by name/number) so the receiving agent
  knows which workaround to remove and which report to close.
- State this explicitly in the "REQUESTED RESPONSE" section of the report.

#### Gap report lifecycle

- **Open:** Report exists in `docs/csrd-gaps/`, workaround in place
  (DEFICIT) or pain point noted (FRICTION).
- **Resolved:** The csrd-* agent ships the fix and returns a migration
  guide (DEFICIT), or the friction is addressed in a polish release
  (FRICTION).  Apply changes, verify tests pass, then **delete the report**.
- **Partial:** Fix only partially addresses the report — keep the file
  but update it to reflect what remains open.
- A DEFICIT report is deleted when ALL of these are true:
  1. The csrd-* package has shipped the fix (version bumped in pyproject.toml)
  2. The workaround code has been removed from this repo
  3. Tests pass without the workaround
- A FRICTION report is deleted when the pain point is gone and no
  follow-up work remains.
"""


def _render_dockerignore() -> str:
    """Build a ``.dockerignore`` for the workspace."""

    return (
        "__pycache__/\n"
        "*.pyc\n"
        "*.pyo\n"
        "*.pyd\n"
        ".venv/\n"
        ".env\n"
        ".git\n"
        ".pytest_cache/\n"
        ".mypy_cache/\n"
        ".ruff_cache/\n"
        "tests/\n"
    )


def _render_compose_override_example(spec: ComposeSpec) -> str:
    """Build ``docker-compose.override.yml.example`` with port customization hints.

    Users copy this to ``docker-compose.override.yml`` and adjust host-side
    ports.  Docker Compose automatically merges the override file.  The
    actual ``docker-compose.override.yml`` is never regenerated so user
    changes are safe.
    """
    lines = [
        "# Copy this file to docker-compose.override.yml and adjust as needed.",
        "# Docker Compose merges this automatically with docker-compose.yml.",
        "# This file is NEVER overwritten by `csrd compose apply`.",
        "#",
        "# Common use: remap host-side ports to avoid collisions.",
        "",
        "services:",
    ]
    for svc in spec.services:
        lines.append(f"  # {svc.name}:")
        lines.append("  #   ports:")
        lines.append(f'  #     - "{svc.port}:{svc.port}"  # host:container')
    lines.append("")
    return "\n".join(lines)


def _render_gateway_routes(spec: ComposeSpec) -> str | None:
    """Render ``gateway-routes.yaml`` from discovered ProxySpec prefixes.

    Returns ``None`` if no gateway exists in the spec.
    """
    from .augments import resolve_gateway_routes

    routes = resolve_gateway_routes(spec)
    if not routes:
        return None

    gateway = next(s for s in spec.services if s.role == "gateway")

    lines = ["# Gateway route table — auto-generated, but safe to edit manually.", "routes:"]

    # Health probe must bypass the JWT guard so Docker HEALTHCHECK and
    # external load balancers can reach it without credentials.
    lines.append('  - prefix: "/_info/health"')
    lines.append(f'    target: "http://{gateway.name}:{gateway.port}"')
    lines.append("    public: true")

    for route in routes:
        lines.append(f'  - prefix: "{route["prefix"]}"')
        lines.append(f'    target: "{route["target"]}"')
        if route.get("public"):
            lines.append("    public: true")
    lines.append("")
    return "\n".join(lines)
