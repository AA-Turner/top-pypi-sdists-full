"""Workspace mutation and orchestration operations.

These functions load, mutate, and persist the compose spec.  They are
the canonical way to change a workspace's ``csrd-compose.yaml`` from
library code or CLI handlers.

``render_workspace`` is the top-level orchestration function that loads
the spec, renders all workspace files, scaffolds services, and optionally
initializes a git repository.
"""

import re
from pathlib import Path

from ..models import (
    INFRA_ALL_TYPES,
    INFRA_DATABASES,
    ComposeSpec,
    InfraNode,
    ServiceAugment,
    ServiceNode,
    WorkspaceAugment,
)
from .augments import AUGMENT_REGISTRY, augment_for
from .infra import INFRA_REGISTRY
from .loader import default_spec, load_spec, save_spec, spec_file_path

# ---------------------------------------------------------------------------
# Workspace rendering (orchestration)
# ---------------------------------------------------------------------------

_ENV_KEY_RE = re.compile(r"^([A-Z][A-Z0-9_]*)=", re.MULTILINE)


def _merge_new_env_vars(env_path: Path, env_example_content: str) -> None:
    """Append env vars from .env.example that are missing in .env.

    Preserves all existing user values.  Only adds new keys with their
    default values so services don't crash after adding augments.
    """
    existing = env_path.read_text(encoding="utf-8")
    existing_keys = set(_ENV_KEY_RE.findall(existing))

    new_lines: list[str] = []
    for line in env_example_content.splitlines():
        m = _ENV_KEY_RE.match(line)
        if m and m.group(1) not in existing_keys:
            new_lines.append(line)

    if new_lines:
        # Ensure trailing newline before appending
        if existing and not existing.endswith("\n"):
            existing += "\n"
        existing += "\n# Added by csrd (new augment vars)\n"
        existing += "\n".join(new_lines) + "\n"
        env_path.write_text(existing, encoding="utf-8")


def render_workspace(output_dir: Path, *, git_init: bool = False) -> Path:
    """Render deterministic workspace files from the current spec.

    Orchestrates: load spec → mutate → save → render files → scaffold →
    git init.  Pure render functions live in ``renderer.py``.

    If a ``csrd-compose.yaml`` already exists the spec is loaded from disk
    so that previously-added services and infra are reflected in the
    rendered ``docker-compose.yml`` and ``.env.example``.
    """
    from .git import maybe_git_init
    from .renderer import (
        WORKSPACE_MARKER_FILENAME,
        _render_agents_md,
        _render_compose,
        _render_compose_override_example,
        _render_dockerignore,
        _render_env_example,
        _render_gateway_routes,
        _render_gitignore,
        _render_pyproject,
        _render_readme,
        _render_workspace_marker,
    )
    from .scaffolder import scaffold_services
    from .service_renderers import (
        render_init,
        render_migrations,
        render_requirements,
        render_settings,
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path) if spec_path.is_file() else default_spec(output_dir)

    spec.workspace.git_init = git_init
    save_spec(spec, spec_path)

    (output_dir / "docker-compose.yml").write_text(_render_compose(spec), encoding="utf-8")
    env_example_content = _render_env_example(spec)
    (output_dir / ".env.example").write_text(env_example_content, encoding="utf-8")

    # Seed .env from .env.example only on first render so services can
    # start immediately.  On subsequent renders the user may have set
    # strong passwords or API keys — never overwrite existing values.
    # However, new keys added by augments/services must be appended.
    env_path = output_dir / ".env"
    if not env_path.exists():
        env_path.write_text(env_example_content, encoding="utf-8")
    else:
        _merge_new_env_vars(env_path, env_example_content)
    (output_dir / "README.md").write_text(_render_readme(spec), encoding="utf-8")

    # .gitignore is scaffolded (created once, never overwritten) so user-added
    # ignore patterns (node_modules/, .idea/, etc.) survive re-renders.
    gitignore_path = output_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(_render_gitignore(), encoding="utf-8")

    (output_dir / ".dockerignore").write_text(_render_dockerignore(), encoding="utf-8")

    # docker-compose.override.yml.example is scaffolded (created once, never
    # overwritten) so users can copy it to docker-compose.override.yml and
    # customise host-side ports, extra env vars, etc.  Docker Compose auto-
    # merges the override file.
    override_example = output_dir / "docker-compose.override.yml.example"
    if not override_example.exists():
        override_example.write_text(_render_compose_override_example(spec), encoding="utf-8")

    (output_dir / "pyproject.toml").write_text(_render_pyproject(spec), encoding="utf-8")
    (output_dir / WORKSPACE_MARKER_FILENAME).write_text(
        _render_workspace_marker(),
        encoding="utf-8",
    )

    # AGENTS.md is scaffolded (created once, never overwritten) so user
    # edits are preserved.
    agents_path = output_dir / "AGENTS.md"
    if not agents_path.exists():
        agents_path.write_text(_render_agents_md(spec), encoding="utf-8")

    # Scaffold service source trees from the cookiecutter template.
    # Returns the set of service names that were newly scaffolded so we
    # know which spec-rendered files need to be written for the first time.
    newly_scaffolded = scaffold_services(spec, output_dir)

    # Gateway routes config (rendered into gateway service src dir for self-containment).
    # Must run AFTER scaffold_services so the service dir already exists (the scaffolder
    # skips services whose src dir is already present).
    # Gateway routes config — scaffolded once, never overwritten so that
    # user-added custom routes survive re-renders.
    gateway_routes_content = _render_gateway_routes(spec)
    if gateway_routes_content is not None:
        gateway_svc = next((s for s in spec.services if s.role == "gateway"), None)
        if gateway_svc is not None:
            gw_dir = output_dir / "src" / gateway_svc.name.replace("-", "_")
            gw_dir.mkdir(parents=True, exist_ok=True)
            gw_routes_path = gw_dir / "gateway-routes.yaml"
            if not gw_routes_path.exists():
                gw_routes_path.write_text(gateway_routes_content, encoding="utf-8")

    # Spec-rendered service files (settings.py, __init__.py, requirements.txt,
    # migrations.py) are written on first scaffold only — they overwrite the
    # cookiecutter stubs with augment-aware versions.  On subsequent renders
    # the files are user-owned and never overwritten, so manually added
    # routers, settings fields, and dependencies survive re-renders.
    for svc in spec.services:
        # Frontend services are not Python — skip spec-rendered Python files
        if svc.role == "frontend":
            continue
        svc_dir = output_dir / "src" / svc.name.replace("-", "_")
        if not svc_dir.exists():
            continue

        # Only write spec-rendered files for newly scaffolded services
        if svc.name not in newly_scaffolded:
            continue

        svc_dir.mkdir(parents=True, exist_ok=True)
        (svc_dir / "settings.py").write_text(render_settings(svc, spec), encoding="utf-8")
        (svc_dir / "__init__.py").write_text(render_init(svc, spec), encoding="utf-8")
        (svc_dir / "requirements.txt").write_text(render_requirements(svc, spec), encoding="utf-8")

        migrations_content = render_migrations(svc, spec)
        if migrations_content is not None:
            (svc_dir / "migrations.py").write_text(migrations_content, encoding="utf-8")

    if spec.workspace.git_init:
        maybe_git_init(output_dir)

    return output_dir


def apply(output_dir: Path, *, git_init: bool = False) -> Path:
    """Apply baseline empty-workspace rendering into *output_dir*."""

    return render_workspace(output_dir, git_init=git_init)


def validate(output_dir: Path) -> ComposeSpec:
    """Validate and return the canonical compose spec for a workspace."""

    return load_spec(spec_file_path(output_dir))


def add_service(output_dir: Path, service: ServiceNode) -> ComposeSpec:
    """Append a service to the workspace spec and persist to disk.

    Raises ``ValueError`` if *service.name* already exists.
    Returns the updated spec.
    """

    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    existing_names = {s.name for s in spec.services}
    if service.name in existing_names:
        raise ValueError(f"Service '{service.name}' already exists in workspace spec")

    spec.services.append(service)
    save_spec(spec, spec_path)
    return spec


def add_infra(output_dir: Path, infra: InfraNode) -> ComposeSpec:
    """Add or replace an infrastructure entry in the workspace spec.

    Database types are mutually exclusive — adding one replaces any existing
    database entry.  Other infra types (redis, rabbitmq) are singletons that
    cannot be duplicated.

    Returns the updated spec.
    """

    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    existing_types = {i.type for i in spec.infra}

    if infra.type in INFRA_DATABASES:
        # Remove any existing database entry (mutually exclusive)
        spec.infra = [i for i in spec.infra if i.type not in INFRA_DATABASES]
    elif infra.type in existing_types:
        raise ValueError(f"Infra '{infra.type}' already exists in workspace spec")

    spec.infra.append(infra)
    save_spec(spec, spec_path)
    return spec


def remove_infra(output_dir: Path, infra_type: str) -> ComposeSpec:
    """Remove an infrastructure entry from the workspace spec.

    Raises ``ValueError`` if *infra_type* is not currently configured.
    Returns the updated spec.
    """

    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    existing_types = {i.type for i in spec.infra}
    if infra_type not in existing_types:
        raise ValueError(f"Infra '{infra_type}' is not configured in workspace spec")

    spec.infra = [i for i in spec.infra if i.type != infra_type]
    save_spec(spec, spec_path)
    return spec


def available_infra(workspace_dir: Path) -> list[str]:
    """Return infra types not yet present in the workspace spec.

    Database types are mutually exclusive — if any database is already
    configured, all database options are excluded.
    """

    spec_path = spec_file_path(workspace_dir)
    if not spec_path.is_file():
        return sorted(INFRA_ALL_TYPES)

    spec = load_spec(spec_path)
    existing = {i.type for i in spec.infra}

    available: list[str] = []
    has_db = bool(existing & INFRA_DATABASES)
    for infra_type in sorted(INFRA_ALL_TYPES):
        if infra_type in existing:
            continue
        if has_db and infra_type in INFRA_DATABASES:
            continue
        available.append(infra_type)
    return available


def configured_infra(workspace_dir: Path) -> list[str]:
    """Return infra types currently configured in the workspace spec."""

    spec_path = spec_file_path(workspace_dir)
    if not spec_path.is_file():
        return []

    spec = load_spec(spec_path)
    return sorted(i.type for i in spec.infra)


# ---------------------------------------------------------------------------
# Augment operations
# ---------------------------------------------------------------------------


def _infra_features_in_spec(spec: ComposeSpec) -> set[str]:
    """Return the set of infra feature categories present in the spec."""
    features: set[str] = set()
    for infra_node in spec.infra:
        desc = INFRA_REGISTRY.get(infra_node.type)
        if desc is not None:
            features.add(desc.feature)
    return features


def _validate_augment_prerequisites(
    augment_name: str,
    spec: ComposeSpec,
    *,
    service_name: str | None = None,
) -> None:
    """Validate that all prerequisites for an augment are met.

    Raises ``ValueError`` with a descriptive message on failure.
    """
    desc = augment_for(augment_name)

    # Check required infra features
    if desc.requires_infra:
        spec_features = _infra_features_in_spec(spec)
        missing = set(desc.requires_infra) - spec_features
        if missing:
            raise ValueError(
                f"Augment '{augment_name}' requires infra features "
                f"{sorted(missing)}, but they are not configured. "
                f"Add the required infra first."
            )

    # Check required workspace augment
    if desc.requires_workspace_augment:
        ws_augment_names = {a.name for a in spec.workspace.augments}
        if desc.requires_workspace_augment not in ws_augment_names:
            raise ValueError(
                f"Augment '{augment_name}' requires workspace augment "
                f"'{desc.requires_workspace_augment}', but it is not present. "
                f"Add the workspace augment first."
            )

    # Check required service role in spec
    if desc.requires_service_in_spec:
        roles = {s.role for s in spec.services}
        if desc.requires_service_in_spec not in roles:
            raise ValueError(
                f"Augment '{augment_name}' requires a service with role "
                f"'{desc.requires_service_in_spec}' in the spec."
            )

    # Check conflicts (only relevant for service-scope augments)
    if service_name is not None and desc.conflicts_with:
        svc = next((s for s in spec.services if s.name == service_name), None)
        if svc is not None:
            existing = {a.name for a in svc.augments}
            conflicts = set(desc.conflicts_with) & existing
            if conflicts:
                raise ValueError(
                    f"Augment '{augment_name}' conflicts with "
                    f"{sorted(conflicts)} on service '{service_name}'."
                )

    # Role compatibility checks for service-scope augments
    if service_name is not None:
        svc = next((s for s in spec.services if s.name == service_name), None)
        if (
            svc is not None
            and augment_name == "realtime-websocket"
            and svc.role
            in (
                "frontend",
                "worker",
            )
        ):
            raise ValueError(
                f"Augment 'realtime-websocket' is not compatible with role '{svc.role}'. "
                "Realtime WebSocket is only supported on 'app', 'auth', and 'gateway' roles."
            )


def add_workspace_augment(
    output_dir: Path,
    augment_name: str,
    options: dict[str, str | list[str]] | None = None,
) -> ComposeSpec:
    """Add a workspace-scoped augment to the spec.

    Validates that the augment exists in the registry and has scope
    ``"workspace"``.  Raises ``ValueError`` on validation failure.
    Returns the updated spec.
    """
    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    # Validate augment exists and has correct scope
    try:
        desc = augment_for(augment_name)
    except KeyError:
        raise ValueError(f"Unknown augment '{augment_name}'") from None

    if desc.scope != "workspace":
        raise ValueError(
            f"Augment '{augment_name}' has scope '{desc.scope}', "
            f"not 'workspace'. Use add_service_augment() instead."
        )

    # Check for duplicates
    existing = {a.name for a in spec.workspace.augments}
    if augment_name in existing:
        raise ValueError(f"Workspace augment '{augment_name}' is already present.")

    _validate_augment_prerequisites(augment_name, spec)

    spec.workspace.augments.append(WorkspaceAugment(name=augment_name, options=options or {}))
    save_spec(spec, spec_path)
    return spec


def add_service_augment(
    output_dir: Path,
    service_name: str,
    augment_name: str,
    options: dict[str, str | list[str]] | None = None,
) -> ComposeSpec:
    """Add a service-scoped augment to a specific service in the spec.

    Validates prerequisites, scope, duplicates, and conflicts.
    Raises ``ValueError`` on validation failure.
    Returns the updated spec.
    """
    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    # Validate augment exists and has correct scope
    try:
        desc = augment_for(augment_name)
    except KeyError:
        raise ValueError(f"Unknown augment '{augment_name}'") from None

    if desc.scope != "service":
        raise ValueError(
            f"Augment '{augment_name}' has scope '{desc.scope}', "
            f"not 'service'. Use add_workspace_augment() instead."
        )

    # Find the target service
    svc = next((s for s in spec.services if s.name == service_name), None)
    if svc is None:
        raise ValueError(f"Service '{service_name}' not found in workspace spec.")

    # Check for duplicates
    existing = {a.name for a in svc.augments}
    if augment_name in existing:
        raise ValueError(
            f"Augment '{augment_name}' is already present on service '{service_name}'."
        )

    # Validate target selection requirement
    if desc.needs_target_selection:
        targets = (options or {}).get("targets", [])
        if not targets:
            raise ValueError(
                f"Augment '{augment_name}' requires target selection. "
                f'Pass options={{"targets": [...]}}.'
            )

    _validate_augment_prerequisites(augment_name, spec, service_name=service_name)

    svc.augments.append(ServiceAugment(name=augment_name, options=options or {}))
    save_spec(spec, spec_path)
    return spec


def remove_service_augment(
    output_dir: Path,
    service_name: str,
    augment_name: str,
) -> ComposeSpec:
    """Remove a service-scoped augment from a service.

    Only updates the spec — scaffolded files are NOT removed (they may
    contain user edits).  Returns the updated spec.
    Raises ``ValueError`` if the augment is not present.
    """
    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    svc = next((s for s in spec.services if s.name == service_name), None)
    if svc is None:
        raise ValueError(f"Service '{service_name}' not found in workspace spec.")

    original_count = len(svc.augments)
    svc.augments = [a for a in svc.augments if a.name != augment_name]

    if len(svc.augments) == original_count:
        raise ValueError(f"Augment '{augment_name}' is not present on service '{service_name}'.")

    save_spec(spec, spec_path)
    return spec


def remove_service(output_dir: Path, service_name: str) -> ComposeSpec:
    """Remove a service from the workspace spec by name.

    Only updates the spec — scaffolded files are NOT removed (they may
    contain user edits).  Returns the updated spec.
    Raises ``ValueError`` if the service is not found.
    """

    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    existing_names = {s.name for s in spec.services}
    if service_name not in existing_names:
        raise ValueError(f"Service '{service_name}' not found in workspace spec.")

    spec.services = [s for s in spec.services if s.name != service_name]
    save_spec(spec, spec_path)
    return spec


def rename_service(output_dir: Path, old_name: str, new_name: str) -> ComposeSpec:
    """Rename a service in the workspace spec.

    Updates the service name and any cross-service augment ``targets``
    options that reference the old name.  Only updates the spec —
    filesystem renames are the caller's responsibility.

    Raises ``ValueError`` if *old_name* is not found or *new_name*
    already exists.
    """

    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    existing_names = {s.name for s in spec.services}
    if old_name not in existing_names:
        raise ValueError(f"Service '{old_name}' not found in workspace spec.")
    if new_name in existing_names:
        raise ValueError(f"Service '{new_name}' already exists in workspace spec.")

    # Rename the service itself
    svc = next(s for s in spec.services if s.name == old_name)
    svc.name = new_name

    # Update cross-service augment target references
    for other_svc in spec.services:
        for aug in other_svc.augments:
            targets = aug.options.get("targets")
            if targets is None:
                continue
            if isinstance(targets, str) and targets == old_name:
                aug.options["targets"] = new_name
            elif isinstance(targets, list):
                aug.options["targets"] = [new_name if t == old_name else t for t in targets]

    save_spec(spec, spec_path)
    return spec


def next_available_port(spec: ComposeSpec, default: int = 8080) -> int:
    """Return the next unused port for a new service.

    Uses ``max(existing service ports) + 1``, or *default* when no
    services exist.
    """
    if not spec.services:
        return default
    return max(s.port for s in spec.services) + 1


def available_workspace_augments(output_dir: Path) -> list[str]:
    """Return workspace-scope augment names that can be added.

    Filters out augments already present and those with unmet
    prerequisites.
    """
    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    existing = {a.name for a in spec.workspace.augments}
    available: list[str] = []

    for name, desc in sorted(AUGMENT_REGISTRY.items()):
        if desc.scope != "workspace":
            continue
        if name in existing:
            continue
        try:
            _validate_augment_prerequisites(name, spec)
        except ValueError:
            continue
        available.append(name)

    return available


def available_service_augments(
    output_dir: Path,
    service_name: str,
) -> list[str]:
    """Return augment names that can be added to a service.

    Filters out augments already present, those with unmet prerequisites,
    and those with conflicts.
    """
    spec_path = spec_file_path(output_dir)
    spec = load_spec(spec_path)

    svc = next((s for s in spec.services if s.name == service_name), None)
    if svc is None:
        return []

    existing = {a.name for a in svc.augments}
    available: list[str] = []

    for name, desc in sorted(AUGMENT_REGISTRY.items()):
        if desc.scope != "service":
            continue
        if name in existing:
            continue
        try:
            _validate_augment_prerequisites(name, spec, service_name=service_name)
        except ValueError:
            continue
        available.append(name)

    return available
