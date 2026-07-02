"""
Capability loader — v1 spec.

Load capabilities from disk, validate against the v1 contract,
and prepare for use.

See specs/capabilities/ for the canonical spec.
"""

from __future__ import annotations

import importlib.util
import os
import re
import sys
import typing as t
from pathlib import Path

import yaml
from loguru import logger

from dreadnode.capabilities.types import (
    AgentDef,
    DependencySpec,
    HealthCheck,
    LoadFailure,
    LoadOptions,
    LoadResult,
    MCPServerAuth,
    MCPServerDef,
    WorkerDef,
)
from dreadnode.core.util import valid_version
from dreadnode.packaging.manifest import CapabilityManifest
from dreadnode.storage.storage import Storage

MANIFEST_FILE = "capability.yaml"
PROJECT_CAPABILITIES_RELATIVE_DIR = Path(".dreadnode") / "capabilities"
CAPABILITY_DIRS_ENV = "DREADNODE_CAPABILITY_DIRS"
PROJECT_ROOT_ENV = "DREADNODE_PROJECT_ROOT"

# CAP-VALID-002: name pattern
_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")

# CAP-WTOP-006 / CAP-WENV-001..002: the runtime injects these keys
# authoritatively for every subprocess worker it spawns. Manifest ``env:``
# entries that set them would be silently overridden, so loader rejects them
# at parse time for clarity.
_RESERVED_WORKER_ENV_KEYS: frozenset[str] = frozenset(
    {
        "DREADNODE_RUNTIME_URL",
        "DREADNODE_RUNTIME_TOKEN",
        "DREADNODE_RUNTIME_ID",
    }
)


# ============================================================================
# Search Path Resolution
# ============================================================================


def get_default_capabilities_dir() -> Path:
    """Get the default user capabilities directory."""
    from dreadnode.app.main import DEFAULT_INSTANCE

    if DEFAULT_INSTANCE._storage is not None:
        return DEFAULT_INSTANCE.storage.capabilities_path

    return Storage(cache=DEFAULT_INSTANCE.cache).capabilities_path


def resolve_search_paths(
    *,
    capability_dirs: list[str | Path] | None = None,
    cwd: Path | None = None,
    user_dir: str | Path | None = None,
) -> list[Path]:
    """
    Resolve capability discovery search paths (CAP-LOAD-001).

    Precedence:
    1. Project-local .dreadnode/capabilities
    2. User-local ~/.dreadnode/capabilities
    3. Explicit dirs (CLI flags)
    4. DREADNODE_CAPABILITY_DIRS env list
    """
    cwd = cwd or Path.cwd()
    project_dir = (_resolve_project_root(cwd) / PROJECT_CAPABILITIES_RELATIVE_DIR).resolve()
    user_dir = (
        Path(user_dir).resolve()
        if user_dir is not None
        else get_default_capabilities_dir().resolve()
    )
    explicit = [Path(d).resolve() for d in (capability_dirs or [])]
    env_dirs = _split_capability_dirs(os.environ.get(CAPABILITY_DIRS_ENV))

    ordered = [project_dir, user_dir, *explicit, *env_dirs]
    return _dedupe_paths(ordered)


def _resolve_project_root(cwd: Path) -> Path:
    root_from_env = os.environ.get(PROJECT_ROOT_ENV, "").strip()
    if root_from_env:
        return (cwd / root_from_env).resolve()

    git_root = _find_git_root(cwd)
    if git_root:
        return git_root

    return cwd.resolve()


def _find_git_root(start: Path) -> Path | None:
    current = start.resolve()
    while True:
        if (current / ".git").exists():
            return current
        parent = current.parent
        if parent == current:
            return None
        current = parent


def _split_capability_dirs(value: str | None) -> list[Path]:
    if not value:
        return []
    return [Path(entry.strip()).resolve() for entry in value.split(os.pathsep) if entry.strip()]


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    deduped: list[Path] = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped


# ============================================================================
# Load Single Capability
# ============================================================================


class _CapabilityResolution(t.NamedTuple):
    path: Path
    manifest: CapabilityManifest
    agents: list[AgentDef]
    tools: list[t.Any] | None
    hooks: list[t.Any] | None
    policies: list[t.Any] | None
    skills_paths: list[Path] | None
    skills_path: Path | None
    mcp_server_defs: list[MCPServerDef]
    component_health: list[dict[str, t.Any]]
    dependencies: DependencySpec = DependencySpec()
    checks: list[HealthCheck] = []  # noqa: RUF012
    worker_defs: list[WorkerDef] = []  # noqa: RUF012


async def load_capability(
    path: str | Path,
    options: LoadOptions | None = None,
    source: t.Literal["runtime", "local"] = "local",
    *,
    bundled: bool = False,
) -> t.Any:
    """Load a capability from a directory.

    ``bundled`` is a loader-gated flag the SDK sets only for the built-in
    platform capability shipped in ``dreadnode/builtin_capabilities``. Authors
    cannot set it; the manifest contract has no corresponding field. Under
    CAP-IDENT-004/005, bundled capabilities are exempt from wire-name
    qualification and keep their bare tool names.
    """
    options = options or LoadOptions()
    base = options.base_dir or Path.cwd()
    capability_path = (base / path).resolve()
    manifest_path = capability_path / MANIFEST_FILE

    if not manifest_path.exists():
        raise FileNotFoundError(f"No {MANIFEST_FILE} found in {capability_path}")

    resolved = _resolve_capability(capability_path)

    from dreadnode.capabilities.capability import Capability

    # Python tools are lazily discovered on first `.tools` access (see
    # `Capability.tools`). Stamping happens at that point using the
    # capability's `bundled` flag — threaded via `_from_resolved` below.
    return Capability._from_resolved(
        path=resolved.path,
        manifest=resolved.manifest,
        agents=resolved.agents,
        tools=resolved.tools,
        hooks=resolved.hooks,
        policies=resolved.policies,
        worker_defs=resolved.worker_defs,
        skills_paths=resolved.skills_paths,
        skills_path=resolved.skills_path,
        mcp_server_defs=resolved.mcp_server_defs,
        source=source,
        component_health=resolved.component_health,
        dependencies=resolved.dependencies,
        checks=resolved.checks,
        bundled=bundled,
    )


def _stamp_tool_identities(
    tools: list[t.Any] | None,
    *,
    cap_name: str,
    bundled: bool,
) -> list[t.Any] | None:
    """Stamp ``namespace`` and ``source`` on each Python-sourced Tool.

    ``_discover_python_tools`` always expands Toolsets into their constituent
    Tools before returning, so this only needs to handle Tool instances.

    MCP tools are stamped later by MCPLifecycleManager once their clients
    connect. Synthetic tools are stamped by their constructor. Bundled
    capabilities stay bare-named (CAP-IDENT-004/005).

    Validates that no two stamped Tools compute the same wire name within
    this capability (CAP-IDENT-013 for the Python-only slice).
    """
    if tools is None:
        return None
    from dreadnode.agents.tools import Tool
    from dreadnode.capabilities.tool_rules import validate_wire_names

    if bundled:
        namespace: tuple[str, ...] = ()
        source = "bundled"
    else:
        namespace = (cap_name,)
        source = "python"

    stamped: list[t.Any] = []
    for item in tools:
        if isinstance(item, Tool):
            stamped.append(item.model_copy(update={"namespace": namespace, "source": source}))
        else:
            stamped.append(item)

    validate_wire_names(item for item in stamped if isinstance(item, Tool))
    return stamped


# ============================================================================
# Load Multiple Capabilities
# ============================================================================


async def load_capabilities(
    directory: str | Path | None = None,
    options: LoadOptions | None = None,
    source: t.Literal["runtime", "local"] = "local",
) -> LoadResult:
    """Load all capabilities from a directory."""
    options = options or LoadOptions()
    cap_dir = (
        Path(directory).resolve()
        if directory is not None
        else get_default_capabilities_dir().resolve()
    )

    if not cap_dir.exists():
        return LoadResult()

    capabilities: list[t.Any] = []
    failures: list[LoadFailure] = []

    for entry in sorted(cap_dir.iterdir()):
        if not entry.is_dir():
            continue
        if not (entry / MANIFEST_FILE).exists():
            logger.debug("Skipping {} — no {}", entry.name, MANIFEST_FILE)
            continue
        try:
            cap = await load_capability(entry, options, source=source)
            capabilities.append(cap)
        except Exception as e:
            failures.append(
                LoadFailure(
                    name=entry.name,
                    path=entry,
                    error=str(e),
                )
            )

    logger.debug(
        "Scanned {} — found {} capabilities, {} failures",
        cap_dir,
        len(capabilities),
        len(failures),
    )

    return LoadResult(capabilities=capabilities, failures=failures)


async def load_capabilities_from_search_paths(
    search_paths: list[Path],
    options: LoadOptions | None = None,
    source: t.Literal["runtime", "local"] = "local",
) -> LoadResult:
    """
    Load capabilities from search paths.

    If the same capability name appears in multiple directories, the first one wins.
    """
    capabilities: list[t.Any] = []
    failures: list[LoadFailure] = []
    seen: set[str] = set()

    for path in search_paths:
        result = await load_capabilities(path, options, source=source)
        for cap in result.capabilities:
            if cap.name not in seen:
                seen.add(cap.name)
                capabilities.append(cap)
        failures.extend(result.failures)

    return LoadResult(capabilities=capabilities, failures=failures)


# ============================================================================
# Capability Discovery
# ============================================================================


async def list_capabilities(
    directory: str | Path | None = None,
) -> list[dict[str, t.Any]]:
    """List available capabilities without fully loading them."""
    cap_dir = (
        Path(directory).resolve()
        if directory is not None
        else get_default_capabilities_dir().resolve()
    )

    if not cap_dir.exists():
        return []

    results: list[dict[str, t.Any]] = []

    for entry in sorted(cap_dir.iterdir()):
        if not entry.is_dir():
            continue

        manifest_path = entry / MANIFEST_FILE
        if not manifest_path.exists():
            continue

        try:
            content = manifest_path.read_text()
            manifest = _parse_capability_file(content, manifest_path)
            results.append(
                {
                    "name": manifest.name,
                    "path": str(entry),
                    "version": manifest.version,
                    "description": manifest.description,
                }
            )
        except Exception:
            results.append({"name": entry.name, "path": str(entry)})

    return results


# ============================================================================
# Capability Resolution
# ============================================================================


def _resolve_capability(capability_path: Path) -> _CapabilityResolution:
    manifest_path = capability_path / MANIFEST_FILE
    content = manifest_path.read_text()
    manifest = _parse_capability_file(content, manifest_path)
    component_health: list[dict[str, t.Any]] = []

    # Parse declared flags for when: validation (CAP-FLAG-001)
    from dreadnode.capabilities.flags import validate_flags_block

    flag_defs = validate_flags_block(manifest.flags, manifest_path)
    declared_flags = {f.name for f in flag_defs}

    agent_refs = _build_export_refs(capability_path, manifest.agents, ["agents/"], "agents")
    agents = _resolve_agent_definitions(
        capability_path, manifest.name, agent_refs, component_health
    )
    mcp_defs = parse_mcp_servers(
        manifest.mcp,
        capability_path,
        component_health,
        declared_flags=declared_flags,
        manifest_path=manifest_path,
    )
    worker_defs = parse_workers(
        manifest.workers,
        capability_path,
        component_health,
        declared_flags=declared_flags,
        manifest_path=manifest_path,
    )
    skills_paths = _resolve_skill_paths(capability_path, manifest.skills, component_health) or None
    skills_path = skills_paths[0] if skills_paths else None
    skill_count = sum(1 for h in component_health if h.get("kind") == "skill")
    exported_count = (
        len(agents)
        + skill_count
        + _count_python_tool_files(capability_path, manifest.tools)
        + _count_python_hook_files(capability_path, manifest.hooks)
        + _count_declared_workers(manifest.workers)
        + len(mcp_defs)
    )
    if exported_count == 0:
        raise ValueError(
            f"Capability '{manifest.name}' must export at least one component "
            f"(agent, tool, hook, skill, worker, or MCP server) [CAP-VALID-008]"
        )

    # Parse dependencies into typed structure
    dep_spec = DependencySpec()
    raw_deps = manifest.dependencies
    if raw_deps and isinstance(raw_deps, dict):
        dep_spec = DependencySpec(
            python=raw_deps.get("python", []),
            packages=raw_deps.get("packages", []),
            scripts=raw_deps.get("scripts", []),
        )

    # Parse checks into typed structures and run pre-flight checks
    health_checks: list[HealthCheck] = []
    raw_checks = manifest.checks
    if raw_checks and isinstance(raw_checks, list):
        health_checks = [HealthCheck(name=c["name"], command=c["command"]) for c in raw_checks]

    for check in health_checks:
        _run_preflight_check(check, component_health, cwd=capability_path)

    return _CapabilityResolution(
        path=capability_path,
        manifest=manifest,
        agents=agents,
        tools=None,
        hooks=None,
        policies=None,
        skills_paths=skills_paths,
        skills_path=skills_path,
        mcp_server_defs=mcp_defs,
        component_health=component_health,
        dependencies=dep_spec,
        checks=health_checks,
        worker_defs=worker_defs,
    )


# ============================================================================
# Manifest Parsing & Validation
# ============================================================================


def _parse_capability_file(content: str, manifest_path: Path) -> CapabilityManifest:
    """Parse and validate a capability.yaml file against v1 spec."""
    parsed = yaml.safe_load(content)
    if not isinstance(parsed, dict):
        raise ValueError(f"Capability manifest must contain a root object: {manifest_path}")  # noqa: TRY004

    _validate_contract(parsed, manifest_path)

    return CapabilityManifest(
        schema_version=parsed["schema"],
        name=parsed["name"],
        version=str(parsed["version"]),
        description=parsed["description"],
        agents=parsed.get("agents"),  # None=omitted (auto-discover), []=disabled
        tools=parsed.get("tools"),
        hooks=parsed.get("hooks"),
        policies=parsed.get("policies"),
        skills=parsed.get("skills"),
        workers=parsed.get("workers"),
        mcp=parsed.get("mcp"),
        author=parsed.get("author"),
        license=parsed.get("license"),
        repository=parsed.get("repository"),
        keywords=parsed.get("keywords", []),
        dependencies=parsed.get("dependencies"),
        checks=parsed.get("checks"),
        flags=parsed.get("flags"),
    )


def _validate_contract(data: dict[str, t.Any], manifest_path: Path) -> None:
    """Validate a capability manifest against v1 spec rules.

    CAP-VALID-005: Unknown top-level keys are ignored.
    Only canonical v1 fields are validated.
    """

    # CAP-VALID-001: required fields
    for required in ("schema", "name", "version", "description"):
        if required not in data:
            raise ValueError(
                f"Required field '{required}' missing in {manifest_path} [CAP-VALID-001]"
            )

    # CAP-VALID-004: schema must be 1
    schema = data["schema"]
    if schema != 1:
        raise ValueError(
            f"Unsupported schema version {schema!r} in {manifest_path}; expected 1 [CAP-VALID-004]"
        )

    # CAP-VALID-002: name format
    name = data["name"]
    if not isinstance(name, str) or not _NAME_PATTERN.match(name):
        raise ValueError(
            f"Capability name {name!r} must match [a-z0-9][a-z0-9-]* "
            f"in {manifest_path} [CAP-VALID-002]"
        )

    # CAP-VALID-003: version uses fixed semver
    version = data["version"]
    if not isinstance(version, (str, int, float)):
        raise ValueError(f"Capability version must be a string in {manifest_path} [CAP-VALID-003]")  # noqa: TRY004
    if not valid_version(str(version)):
        raise ValueError(
            f"Capability version {version!r} must use fixed semver (X.Y.Z) in {manifest_path} [CAP-VALID-003]"
        )

    # CAP-VALID-001: description must be a non-empty string
    description = data["description"]
    if not isinstance(description, str) or not description.strip():
        raise ValueError(
            f"Capability 'description' must be a non-empty string "
            f"in {manifest_path} [CAP-VALID-001]"
        )

    # CAP-VALID-006: export path arrays must contain only non-empty strings
    for field in ("agents", "tools", "hooks", "skills"):
        value = data.get(field)
        if value is None:
            continue
        if not isinstance(value, list):
            raise ValueError(  # noqa: TRY004
                f"Capability field '{field}' must be an array in {manifest_path} [CAP-VALID-006]"
            )
        for item in value:
            if not isinstance(item, str) or not item:
                raise ValueError(
                    f"Capability field '{field}' must contain only non-empty strings "
                    f"in {manifest_path} [CAP-VALID-006]"
                )

    # CAP-WRK-001: workers is a map keyed by worker name
    workers = data.get("workers")
    if workers is not None and not isinstance(workers, dict):
        raise ValueError(
            f"Capability field 'workers' must be a map keyed by worker name "
            f"in {manifest_path} [CAP-WRK-001]"
        )

    # Validate mcp if present
    mcp = data.get("mcp")
    if mcp is not None and not isinstance(mcp, dict):
        raise ValueError(f"Capability field 'mcp' must be an object in {manifest_path}")

    # Validate keywords if present
    keywords = data.get("keywords")
    if keywords is not None:
        if not isinstance(keywords, list):
            raise ValueError(f"Capability field 'keywords' must be an array in {manifest_path}")
        for item in keywords:
            if not isinstance(item, str):
                raise ValueError(  # noqa: TRY004
                    f"Capability field 'keywords' must contain strings in {manifest_path}"
                )

    # CAP-VALID-015: dependencies must be a mapping if present
    dependencies = data.get("dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            raise ValueError(
                f"Capability 'dependencies' must be a mapping in {manifest_path} [CAP-VALID-015]"
            )

        # CAP-VALID-016: known dependency fields must be lists of non-empty strings
        for dep_field in ("python", "packages", "scripts"):
            dep_value = dependencies.get(dep_field)
            if dep_value is None:
                continue
            if not isinstance(dep_value, list):
                raise ValueError(  # noqa: TRY004
                    f"Capability 'dependencies.{dep_field}' must be a list "
                    f"in {manifest_path} [CAP-VALID-016]"
                )
            for item in dep_value:
                if not isinstance(item, str) or not item:
                    raise ValueError(
                        f"Capability 'dependencies.{dep_field}' must contain only non-empty strings "
                        f"in {manifest_path} [CAP-VALID-016]"
                    )

        # CAP-VALID-017: script paths must not escape capability directory
        cap_dir = manifest_path.parent
        for script_path in dependencies.get("scripts", []):
            resolved = (cap_dir / script_path).resolve()
            if not resolved.is_relative_to(cap_dir.resolve()):
                raise ValueError(
                    f"Dependency script path '{script_path}' escapes capability directory "
                    f"in {manifest_path} [CAP-VALID-017]"
                )

    # CAP-VALID-018: checks must be a list of mappings if present
    checks = data.get("checks")
    if checks is not None:
        if not isinstance(checks, list):
            raise ValueError(
                f"Capability 'checks' must be a list in {manifest_path} [CAP-VALID-018]"
            )
        # CAP-VALID-019: each check must have name and command
        for i, check in enumerate(checks):
            if not isinstance(check, dict):
                raise ValueError(  # noqa: TRY004
                    f"Capability 'checks[{i}]' must be a mapping in {manifest_path} [CAP-VALID-018]"
                )
            for req_field in ("name", "command"):
                val = check.get(req_field)
                if not val or not isinstance(val, str):
                    raise ValueError(
                        f"Capability check '{req_field}' is required and must be a non-empty string "
                        f"in {manifest_path} [CAP-VALID-019]"
                    )


# ============================================================================
# Dependency Pre-Loading
# ============================================================================


def preload_dependency_specs(
    workspace_dir: Path,
) -> list[tuple[str, Path, DependencySpec]]:
    """Enumerate dependency specs for capabilities synced into ``workspace_dir``.

    Used by the install pipeline (``dreadnode.capabilities.install``) before
    ``Capability.discover`` runs, so dependency installs land before preflight
    ``checks:`` execute. Parses ``capability.yaml`` only — does not resolve
    agents, tools, hooks, or workers.

    Skips entries that are not directories, hidden, missing a manifest, or
    whose manifest fails to parse — failures are absorbed here and surfaced
    by the loader proper, which records them via the load-failure path.
    """
    if not workspace_dir.exists():
        return []

    specs: list[tuple[str, Path, DependencySpec]] = []
    for entry in sorted(workspace_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        manifest_path = entry / MANIFEST_FILE
        if not manifest_path.is_file():
            continue
        try:
            manifest = _parse_capability_file(
                manifest_path.read_text(encoding="utf-8"), manifest_path
            )
        except Exception:
            logger.debug("Skipping malformed manifest during dependency preload: {}", manifest_path)
            continue
        raw = manifest.dependencies if isinstance(manifest.dependencies, dict) else {}
        spec = DependencySpec(
            python=list(raw.get("python", []) or []),
            packages=list(raw.get("packages", []) or []),
            scripts=list(raw.get("scripts", []) or []),
        )
        specs.append((manifest.name, entry, spec))
    return specs


# ============================================================================
# Pre-flight Checks
# ============================================================================

_CHECK_TIMEOUT_SECONDS = 5


def _run_preflight_check(
    check: HealthCheck,
    component_health: list[dict[str, t.Any]],
    cwd: Path,
) -> None:
    """Run a single pre-flight check and append result to component_health.

    Each check runs with ``cwd`` (the capability root) as its working directory,
    so commands can reference capability-relative paths like ``scripts/foo.py``.
    """
    import subprocess

    try:
        result = subprocess.run(  # noqa: S602
            check.command,
            shell=True,
            capture_output=True,
            timeout=_CHECK_TIMEOUT_SECONDS,
            check=False,
            cwd=str(cwd),
        )
        if result.returncode == 0:
            component_health.append(
                {
                    "kind": "check",
                    "name": check.name,
                    "status": "ok",
                    "error": None,
                }
            )
        else:
            stderr = result.stderr.decode("utf-8", errors="replace").strip()
            component_health.append(
                {
                    "kind": "check",
                    "name": check.name,
                    "status": "error",
                    "error": stderr or f"exit code {result.returncode}",
                }
            )
    except subprocess.TimeoutExpired:
        component_health.append(
            {
                "kind": "check",
                "name": check.name,
                "status": "error",
                "error": f"timed out after {_CHECK_TIMEOUT_SECONDS}s",
            }
        )
    except Exception as exc:
        component_health.append(
            {
                "kind": "check",
                "name": check.name,
                "status": "error",
                "error": str(exc),
            }
        )


# ============================================================================
# Export Path Resolution
# ============================================================================


class _ExportRef(t.NamedTuple):
    path: str
    required: bool
    field: str


def _build_export_refs(
    capability_path: Path,
    configured_paths: list[str] | None,
    default_paths: list[str],
    field: str,
) -> list[_ExportRef]:
    """Build export references from configured + default paths.

    Per contract.md "Omission vs. Empty Behavior":
    - Field omitted (None): auto-discover default dirs
    - Field present with paths: auto-discover defaults PLUS listed paths
    - Field present as []: disabled — no auto-discovery
    """
    # Explicit empty list = disabled
    if configured_paths is not None and len(configured_paths) == 0:
        return []

    refs: list[_ExportRef] = []
    seen: set[Path] = set()

    # Auto-discover default directories
    for default_path in default_paths:
        normalized = default_path.strip()
        if not normalized:
            continue
        absolute = (capability_path / normalized).resolve()
        if not absolute.exists():
            continue
        if absolute in seen:
            continue
        # CAP-VALID-007: path must be within capability directory
        if not _is_contained_within(absolute, capability_path):
            continue
        seen.add(absolute)
        refs.append(_ExportRef(path=normalized, required=False, field=field))

    # Add configured paths
    for configured_path in configured_paths or []:
        normalized = configured_path.strip()
        if not normalized:
            continue
        absolute = (capability_path / normalized).resolve()
        # CAP-VALID-007: path must be within capability directory
        if not _is_contained_within(absolute, capability_path):
            raise ValueError(
                f"Export path '{configured_path}' resolves outside capability "
                f"directory in {capability_path} [CAP-VALID-007]"
            )
        if absolute in seen:
            continue
        seen.add(absolute)
        refs.append(_ExportRef(path=normalized, required=True, field=field))

    return refs


def _is_contained_within(resolved_path: Path, capability_path: Path) -> bool:
    """Check that a path is contained within the capability root (prevent traversal)."""
    try:
        real_root = capability_path.resolve()
        real_path = resolved_path.resolve()
        return real_path == real_root or str(real_path).startswith(str(real_root) + os.sep)
    except (OSError, ValueError):
        return False


def _resolve_export_path(
    capability_path: Path,
    ref: _ExportRef,
) -> Path | None:
    resolved = (capability_path / ref.path).resolve()
    if not resolved.exists():
        return None
    if not _is_contained_within(resolved, capability_path):
        return None
    return resolved


# ============================================================================
# Skill Path Resolution
# ============================================================================


def _resolve_skill_paths(
    capability_path: Path,
    configured_paths: list[str] | None,
    component_health: list[dict[str, t.Any]] | None = None,
) -> list[Path]:
    """Resolve skill export paths."""
    refs = _build_export_refs(capability_path, configured_paths, ["skills/"], "skills")
    paths: list[Path] = []
    for ref in refs:
        resolved = (capability_path / ref.path).resolve()
        if not resolved.exists():
            continue
        if not _is_contained_within(resolved, capability_path):
            continue
        # Record health for each skill subdirectory by attempting to parse its
        # SKILL.md. Mirrors `_load_agent_from_markdown` so frontmatter parse /
        # validation failures surface to `dreadnode capability validate` instead
        # of being silently dropped at runtime by `discover_skills`.
        if component_health is not None and resolved.is_dir():
            # Deferred: agents.skills -> capabilities.capability -> this module.
            from dreadnode.agents.skills import load_skill

            for skill_dir in sorted(resolved.iterdir()):
                if not skill_dir.is_dir():
                    continue
                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    component_health.append(
                        {
                            "kind": "skill",
                            "name": skill_dir.name,
                            "status": "error",
                            "error": f"Missing SKILL.md in {skill_dir}",
                            "detail": "Each skill directory must contain a SKILL.md file",
                        }
                    )
                    continue
                try:
                    skill = load_skill(skill_md)
                except Exception as exc:
                    logger.warning("Failed to load skill from {}: {}", skill_md, exc)
                    component_health.append(
                        {
                            "kind": "skill",
                            "name": skill_dir.name,
                            "status": "error",
                            "error": str(exc),
                            "detail": "Check SKILL.md frontmatter format",
                        }
                    )
                else:
                    component_health.append(
                        {
                            "kind": "skill",
                            "name": skill.name,
                            "status": "ok",
                            "error": None,
                            "detail": None,
                        }
                    )
        paths.append(resolved)
    return paths


# ============================================================================
# Agent Resolution
# ============================================================================


def _resolve_agent_definitions(
    capability_path: Path,
    capability_name: str,
    refs: list[_ExportRef],
    component_health: list[dict[str, t.Any]],
) -> list[AgentDef]:
    agents: list[AgentDef] = []

    for ref in refs:
        resolved = _resolve_export_path(capability_path, ref)
        if not resolved:
            continue

        files: list[Path] = []
        if resolved.is_dir():
            files = [
                f
                for f in _list_files_recursive(resolved)
                if f.suffix.lower() in (".md", ".markdown")
            ]
        elif resolved.suffix.lower() in (".md", ".markdown"):
            files = [resolved]

        for f in files:
            agent, health = _load_agent_from_markdown(f, capability_name)
            component_health.append(health)
            if agent is not None:
                agents.append(agent)

    _assert_unique_names(agents, "agent", capability_path)
    return agents


def _load_agent_from_markdown(
    file_path: Path,
    capability_name: str,
) -> tuple[AgentDef | None, dict[str, t.Any]]:
    try:
        agent = _agent_from_markdown(file_path)
        agent.capability = capability_name
    except Exception as exc:
        logger.warning(f"Failed to load agent from {file_path}: {exc}")
        return (
            None,
            {
                "kind": "agent",
                "name": file_path.stem,
                "status": "error",
                "error": str(exc),
                "detail": "Check agent markdown frontmatter format",
            },
        )
    else:
        return (
            agent,
            {
                "kind": "agent",
                "name": agent.name,
                "status": "ok",
                "error": None,
                "detail": None,
            },
        )


def _agent_from_markdown(file_path: Path) -> AgentDef:
    """Parse an agent definition from a markdown file with YAML frontmatter."""
    content = file_path.read_text()
    fallback_name = file_path.stem

    frontmatter, body = _parse_frontmatter(content)

    # Name: from frontmatter or filename stem
    name = fallback_name
    if frontmatter and isinstance(frontmatter.get("name"), str) and frontmatter["name"].strip():
        name = frontmatter["name"].strip()

    # CAP-VALID-010: agent name format
    if not _NAME_PATTERN.match(name):
        logger.warning(f"Agent name '{name}' in {file_path} does not match [a-z0-9][a-z0-9-]*")

    # CAP-VALID-011: description required
    description = f"Agent '{name}'"
    if frontmatter and isinstance(frontmatter.get("description"), str):
        description = frontmatter["description"]
    elif body.strip():
        description = _extract_markdown_summary(body) or description

    # Model
    model = "inherit"
    if frontmatter and isinstance(frontmatter.get("model"), str) and frontmatter["model"].strip():
        model = frontmatter["model"].strip()

    # Engine (loop owner) — resolves with the same precedence as model
    engine = "inherit"
    if frontmatter and isinstance(frontmatter.get("engine"), str) and frontmatter["engine"].strip():
        engine = frontmatter["engine"].strip()

    # Tool rules: dict[str, bool] with fnmatch patterns
    tools = _read_tools_dict(frontmatter, "tools", file_path)

    # Skills allow-list
    skills = _read_string_list(frontmatter, "skills", file_path)

    # Metadata
    metadata = (
        frontmatter.get("metadata")
        if frontmatter and isinstance(frontmatter.get("metadata"), dict)
        else None
    )

    # CAP-VALID-011: body (system prompt) must be non-empty
    system_prompt = body.strip()
    if not system_prompt:
        logger.warning(f"Agent '{name}' in {file_path} has empty system prompt [CAP-VALID-011]")

    return AgentDef(
        name=name,
        description=description,
        model=model,
        engine=engine,
        system_prompt=system_prompt,
        tools=tools,
        skills=skills,
        metadata=metadata,
    )


# ============================================================================
# Python Tool Discovery
# ============================================================================


def _python_export_paths(
    capability_path: Path,
    configured_paths: list[str] | None,
    default_dir: str,
) -> list[Path]:
    if configured_paths is not None and len(configured_paths) == 0:
        return []

    seen_roots: set[Path] = set()
    roots: list[Path] = []

    for relative in [default_dir, *(configured_paths or [])]:
        resolved = (capability_path / relative).resolve()
        if not resolved.exists() or not _is_contained_within(resolved, capability_path):
            continue
        if resolved in seen_roots:
            continue
        seen_roots.add(resolved)
        roots.append(resolved)

    files: list[Path] = []
    for root in roots:
        if root.is_dir():
            files.extend(file for file in sorted(root.rglob("*.py")) if file.name != "__init__.py")
        elif root.suffix.lower() == ".py" and root.name != "__init__.py":
            files.append(root)
    return files


def _load_python_module(
    file_path: Path,
    capability_path: Path,
    capability_name: str,
    kind: str,
) -> t.Any:
    relative = file_path.resolve().relative_to(capability_path.resolve())
    module_name = (
        f"dreadnode.capabilities.{kind}."
        f"{capability_name.replace('-', '_')}."
        f"{str(relative.with_suffix('')).replace('/', '_').replace('-', '_')}"
    )
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _instantiate_toolset(toolset_cls: type[t.Any]) -> t.Any | None:
    try:
        return toolset_cls()
    except TypeError:
        return None


def _discover_python_tools(
    capability_path: Path,
    manifest: CapabilityManifest,
    component_health: list[dict[str, t.Any]],
) -> list[t.Any]:
    """Discover Python tools from @tool and Toolset classes."""
    from dreadnode.agents.tools import Tool, Toolset

    tools: list[t.Any] = []
    seen: set[str] = set()
    for file_path in _python_export_paths(capability_path, manifest.tools, "tools/"):
        try:
            module = _load_python_module(file_path, capability_path, manifest.name, "tool")
        except Exception as e:
            logger.warning(f"[{manifest.name}] Failed to import {file_path}: {e}")
            component_health.append(
                {
                    "kind": "tool",
                    "name": file_path.stem,
                    "status": "error",
                    "error": str(e),
                    "detail": "Check that all dependencies are installed in the runtime environment",
                }
            )
            continue

        for value in vars(module).values():
            if isinstance(value, Tool):
                if value.name not in seen:
                    tools.append(value)
                    seen.add(value.name)
                    component_health.append(
                        {
                            "kind": "tool",
                            "name": value.name,
                            "status": "ok",
                            "error": None,
                            "detail": None,
                        }
                    )
                continue

            if isinstance(value, Toolset):
                for tool in value.get_tools():
                    if tool.name in seen:
                        continue
                    tools.append(tool)
                    seen.add(tool.name)
                    component_health.append(
                        {
                            "kind": "tool",
                            "name": tool.name,
                            "status": "ok",
                            "error": None,
                            "detail": None,
                        }
                    )
                continue

            if isinstance(value, type) and issubclass(value, Toolset) and value is not Toolset:
                toolset = _instantiate_toolset(value)
                if toolset is None:
                    logger.warning(
                        f"[{manifest.name}] Toolset {value.__name__} requires constructor arguments "
                        "— skipping auto-instantiation"
                    )
                    component_health.append(
                        {
                            "kind": "tool",
                            "name": value.__name__,
                            "status": "error",
                            "error": f"Toolset {value.__name__} requires constructor arguments",
                            "detail": "Provide a no-arg constructor or instantiate the Toolset manually",
                        }
                    )
                    continue
                for tool in toolset.get_tools():
                    if tool.name in seen:
                        continue
                    tools.append(tool)
                    seen.add(tool.name)
                    component_health.append(
                        {
                            "kind": "tool",
                            "name": tool.name,
                            "status": "ok",
                            "error": None,
                            "detail": None,
                        }
                    )
    return tools


def _discover_python_hooks(
    capability_path: Path,
    manifest: CapabilityManifest,
    component_health: list[dict[str, t.Any]],
) -> list[t.Any]:
    """Discover Python hooks from exported hook files."""
    from dreadnode.core.hook import Hook

    hooks: list[t.Any] = []
    seen: set[str] = set()
    for file_path in _python_export_paths(capability_path, manifest.hooks, "hooks/"):
        try:
            module = _load_python_module(file_path, capability_path, manifest.name, "hook")
        except Exception as e:
            logger.warning(f"[{manifest.name}] Failed to import {file_path}: {e}")
            component_health.append(
                {
                    "kind": "hook",
                    "name": file_path.stem,
                    "status": "error",
                    "error": str(e),
                    "detail": "Check that all dependencies are installed in the runtime environment",
                }
            )
            continue

        for value in vars(module).values():
            if not isinstance(value, Hook):
                continue
            name = getattr(value, "__name__", getattr(value, "name", ""))
            if not name or name in seen:
                continue
            hooks.append(value)
            seen.add(name)
            component_health.append(
                {
                    "kind": "hook",
                    "name": name,
                    "status": "ok",
                    "error": None,
                    "detail": None,
                }
            )
    return hooks


def _discover_python_policies(
    capability_path: Path,
    manifest: CapabilityManifest,
    component_health: list[dict[str, t.Any]],
) -> list[t.Any]:
    """Discover session-policy classes shipped by a capability.

    Mirrors :func:`_discover_python_hooks` but scans the ``policies/``
    directory (or any paths configured in ``manifest.policies``) and
    returns a list of classes, not instances — they're registered by
    name into :data:`dreadnode.policies._REGISTRY` at
    :meth:`CapabilityRegistry.register_capability_policies` time so
    the runtime can instantiate them on demand with per-session
    parameters.

    A valid policy class is *any* top-level class that exposes a
    non-empty ``name`` class attribute. We duck-type rather than
    ``isinstance``-check :class:`~dreadnode.policies.SessionPolicy`
    because subclassing isn't required for the loader contract —
    although authors are expected to subclass it for the
    Pydantic-fields and ``@hook`` machinery to work.
    """
    policies: list[t.Any] = []
    seen: set[str] = set()
    configured = manifest.policies if hasattr(manifest, "policies") else None
    for file_path in _python_export_paths(capability_path, configured, "policies/"):
        try:
            module = _load_python_module(file_path, capability_path, manifest.name, "policy")
        except Exception as e:
            logger.warning(f"[{manifest.name}] Failed to import {file_path}: {e}")
            component_health.append(
                {
                    "kind": "policy",
                    "name": file_path.stem,
                    "status": "error",
                    "error": str(e),
                    "detail": "Check that all dependencies are installed in the runtime environment",
                }
            )
            continue

        for attr_name, value in vars(module).items():
            if not isinstance(value, type):
                continue
            # Skip imports from other modules — we only want classes
            # defined *in* this file so that importing SessionPolicy
            # at the top doesn't get re-registered.
            if getattr(value, "__module__", None) != module.__name__:
                continue
            policy_name = getattr(value, "name", None)
            if not isinstance(policy_name, str) or not policy_name:
                continue
            if policy_name in seen:
                continue
            policies.append(value)
            seen.add(policy_name)
            component_health.append(
                {
                    "kind": "policy",
                    "name": f"{attr_name} (policy={policy_name!r})",
                    "status": "ok",
                    "error": None,
                    "detail": None,
                }
            )
    return policies


# ============================================================================
# Component Counting (for CAP-VALID-008)
# ============================================================================


def _count_python_tool_files(
    capability_path: Path,
    configured_paths: list[str] | None,
) -> int:
    """Count Python tool files that would be discovered."""
    refs = _build_export_refs(capability_path, configured_paths, ["tools/"], "tools")
    count = 0
    for ref in refs:
        resolved = _resolve_export_path(capability_path, ref)
        if not resolved:
            continue
        if resolved.is_dir():
            count += sum(1 for f in resolved.rglob("*.py") if f.name != "__init__.py")
        elif resolved.suffix.lower() == ".py" and resolved.name != "__init__.py":
            count += 1
    return count


def _count_python_hook_files(
    capability_path: Path,
    configured_paths: list[str] | None,
) -> int:
    """Count Python hook files that would be discovered."""
    refs = _build_export_refs(capability_path, configured_paths, ["hooks/"], "hooks")
    count = 0
    for ref in refs:
        resolved = _resolve_export_path(capability_path, ref)
        if not resolved:
            continue
        if resolved.is_dir():
            count += sum(1 for f in resolved.rglob("*.py") if f.name != "__init__.py")
        elif resolved.suffix.lower() == ".py" and resolved.name != "__init__.py":
            count += 1
    return count


def load_worker_from_def(
    worker_def: WorkerDef,
    capability_path: Path,
    capability_name: str,
) -> t.Any:
    """Import a worker module on behalf of the lifecycle manager (CAP-WRK-002, CAP-WRK-007).

    Only called when the worker's gate is satisfied. Enforces exactly one
    ``Worker`` instance per file. Assigns the manifest key as the worker's
    name when the constructor omitted it; validates equality when provided.

    Raises ``ImportError`` on module import failure or ``ValueError`` when
    the file exposes zero or multiple ``Worker`` instances, or when the
    constructor name conflicts with the manifest key.
    """
    from dreadnode.capabilities.worker import Worker

    module = _load_python_module(worker_def.path, capability_path, capability_name, "worker")

    instances = [value for value in vars(module).values() if isinstance(value, Worker)]
    if len(instances) == 0:
        raise ValueError(
            f"Worker file '{worker_def.path}' does not expose a Worker instance [CAP-WRK-002]"
        )
    if len(instances) > 1:
        raise ValueError(
            f"Worker file '{worker_def.path}' exposes {len(instances)} Worker instances; "
            f"expected exactly one [CAP-WRK-002]"
        )

    worker = instances[0]
    if worker.name is None:
        worker.name = worker_def.name
    elif worker.name != worker_def.name:
        raise ValueError(
            f"Worker '{worker_def.name}' constructor name {worker.name!r} does not match "
            f"manifest key {worker_def.name!r} in '{worker_def.path}' [CAP-WAPI-001]"
        )
    return worker


def _count_declared_workers(workers: dict[str, t.Any] | None) -> int:
    """Count workers declared in the manifest (CAP-WRK-001, CAP-FLAG-071).

    Counts declared entries regardless of current gate state, so a capability
    whose only worker is gated passes `CAP-VALID-008`.
    """
    if not workers:
        return 0
    return len(workers)


def _count_mcp_servers(
    mcp: dict[str, t.Any] | None,
    capability_path: Path,
) -> int:
    """Count MCP servers from manifest definition.

    Delegates to parse_mcp_servers() for accurate counting of individual
    servers, including those defined within .mcp.json files.
    """
    return len(parse_mcp_servers(mcp, capability_path))


# ============================================================================
# MCP Server Parsing
# ============================================================================


def _interpolate_capability_root(value: str, root: str) -> str:
    """Replace ${CAPABILITY_ROOT} in a string value (CAP-MCP-003)."""
    return value.replace("${CAPABILITY_ROOT}", root)


def _interpolate_server_def(raw: dict[str, t.Any], root: str) -> dict[str, t.Any]:
    """Interpolate ${CAPABILITY_ROOT} in all string values of a server def.

    Only resolves ${CAPABILITY_ROOT} at parse time (structural paths).
    ${VAR} / ${VAR:-default} env placeholders are preserved here and
    resolved later at connect time by MCPServerDef.to_server_config().
    """
    result: dict[str, t.Any] = {}
    for key, value in raw.items():
        if isinstance(value, str):
            result[key] = _interpolate_capability_root(value, root)
        elif isinstance(value, list):
            result[key] = [
                _interpolate_capability_root(v, root) if isinstance(v, str) else v for v in value
            ]
        elif isinstance(value, dict):
            result[key] = {
                k: _interpolate_capability_root(v, root) if isinstance(v, str) else v
                for k, v in value.items()
            }
        else:
            result[key] = value
    return result


def _normalize_headers(raw_headers: dict[str, t.Any], root: str) -> tuple[dict[str, str], set[str]]:
    """Flatten MCP headers, recording which keys are declared optional (CAP-MCP-013).

    A header value is either a string (``"Bearer ${TOKEN}"``) or an object form
    ``{value: str, optional: bool}``. The object form (missing ``value`` is an
    error) lets an author mark a header ``optional: true``, so it is dropped
    when its ``${VAR}`` is unset rather than sent with an empty credential.
    ``${CAPABILITY_ROOT}`` is interpolated here; ``${VAR}`` placeholders are
    preserved until connect time.
    """
    flat: dict[str, str] = {}
    optional: set[str] = set()
    for key, value in raw_headers.items():
        if isinstance(value, dict):
            if "value" not in value:
                raise ValueError(f"MCP header '{key}' object form requires a 'value' field")
            flat[key] = _interpolate_capability_root(str(value["value"]), root)
            if value.get("optional"):
                optional.add(key)
        else:
            flat[key] = _interpolate_capability_root(str(value), root)
    return flat, optional


def _parse_server_entry(
    name: str,
    raw: dict[str, t.Any],
    capability_path: Path,
    *,
    source: t.Literal["inline", "file"] = "inline",
) -> MCPServerDef:
    """Parse a single MCP server entry into an MCPServerDef."""
    # Extract when BEFORE interpolation — it's control flow, not a path (CAP-FLAG-010)
    when = raw.get("when")
    filtered = {k: v for k, v in raw.items() if k != "when"}

    root = str(capability_path.resolve())
    interpolated = _interpolate_server_def(filtered, root)

    # Optional timeout fields
    timeout_kw: dict[str, float] = {}
    if "timeout" in interpolated:
        timeout_kw["timeout"] = float(interpolated["timeout"])
    if "init_timeout" in interpolated:
        timeout_kw["init_timeout"] = float(interpolated["init_timeout"])

    common_kw = {"when": when, "source": source}

    # CAP-MCP-011: parse auth block. Only valid on streamable-HTTP servers;
    # rejecting it on stdio gives manifest authors a clear error rather
    # than silently dropping the field.
    auth_raw = interpolated.get("auth")
    auth: MCPServerAuth | None = None
    if auth_raw is not None:
        if not isinstance(auth_raw, dict):
            raise ValueError(
                f"MCP server '{name}' has invalid 'auth' field — expected a mapping, "
                f"got {type(auth_raw).__name__}"
            )
        auth_type = auth_raw.get("type", "oauth")
        if auth_type != "oauth":
            raise ValueError(
                f"MCP server '{name}' has unsupported auth type '{auth_type}' "
                f"(only 'oauth' is supported)"
            )
        auth = MCPServerAuth(
            type="oauth",
            scope=auth_raw.get("scope"),
            client_name=auth_raw.get("client_name"),
        )

    # CAP-MCP-002: infer transport from fields
    if "command" in interpolated:
        if auth is not None:
            raise ValueError(
                f"MCP server '{name}' declares 'auth' on a stdio transport — "
                f"auth is only supported on streamable-HTTP (url:) servers. "
                f"Stdio subprocesses handle their own auth."
            )
        return MCPServerDef(
            name=name,
            transport="stdio",
            command=interpolated["command"],
            args=interpolated.get("args", []),
            env=interpolated.get("env"),
            cwd=interpolated.get("cwd", root),  # CAP-MCP-005
            **timeout_kw,
            **common_kw,
        )
    if "url" in interpolated:
        raw_headers = interpolated.get("headers")
        headers, optional_headers = (
            _normalize_headers(raw_headers, root) if raw_headers else ({}, set())
        )
        return MCPServerDef(
            name=name,
            transport="streamable-http",
            url=interpolated["url"],
            headers=headers or None,
            optional_headers=optional_headers,
            auth=auth,
            **timeout_kw,
            **common_kw,
        )
    raise ValueError(f"MCP server '{name}' must have either 'command' (stdio) or 'url' (http)")


def _load_mcp_file(path: Path) -> dict[str, dict[str, t.Any]]:
    """Load an .mcp.json file and return its mcpServers dict."""
    import json

    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Failed to read MCP config file {}: {}", path, e)
        return {}

    servers = data.get("mcpServers", {})
    if not isinstance(servers, dict):
        logger.warning("Invalid mcpServers in {}: expected object", path)
        return {}
    return servers


def parse_workers(
    workers: dict[str, t.Any] | None,
    capability_path: Path,
    component_health: list[dict[str, t.Any]] | None = None,
    *,
    declared_flags: set[str] | None = None,
    manifest_path: Path | None = None,
) -> list[WorkerDef]:
    """Parse worker entries from a capability manifest (CAP-WRK-001).

    Returns an empty list when *workers* is None or ``{}``. Validates each
    entry's name, `path`, and optional `when:` predicate. Paths that fail
    validation produce a `component_health` error entry but don't abort
    the rest of the capability load (mirrors `CAP-MCP-007`).
    """
    from dreadnode.capabilities.flags import validate_when

    if not workers:
        return []

    if not isinstance(workers, dict):
        raise ValueError(  # noqa: TRY004
            f"Capability field 'workers' must be a map in "
            f"{manifest_path or capability_path} [CAP-WRK-001]"
        )

    declared_flags = declared_flags or set()
    effective_manifest_path = manifest_path or (capability_path / "capability.yaml")

    defs: list[WorkerDef] = []
    seen_paths: dict[Path, str] = {}
    root = str(capability_path.resolve())
    allowed_fields = {"path", "command", "args", "env", "when"}
    for name, raw in workers.items():
        if not isinstance(name, str) or not _NAME_PATTERN.match(name):
            raise ValueError(
                f"Worker name {name!r} must match [a-z0-9][a-z0-9-]* "
                f"in {effective_manifest_path} [CAP-WRK-001]"
            )
        if not isinstance(raw, dict):
            raise ValueError(  # noqa: TRY004
                f"Worker '{name}' must be a map in {effective_manifest_path} [CAP-WRK-001]"
            )
        unknown = set(raw.keys()) - allowed_fields
        if unknown:
            raise ValueError(
                f"Worker '{name}' has unknown fields {sorted(unknown)} "
                f"in {effective_manifest_path} [CAP-WRK-001]"
            )
        has_path = "path" in raw
        has_command = "command" in raw
        # CAP-WTOP-004: path and command are mutually exclusive; one is required.
        if has_path and has_command:
            raise ValueError(
                f"Worker '{name}' declares both 'path' and 'command'; exactly one is "
                f"allowed in {effective_manifest_path} [CAP-WTOP-004]"
            )
        if not has_path and not has_command:
            raise ValueError(
                f"Worker '{name}' requires either 'path' (in-process) or 'command' "
                f"(subprocess) in {effective_manifest_path} [CAP-WRK-001]"
            )

        try:
            validated_when = validate_when(
                raw.get("when"),
                declared_flags,
                name,
                effective_manifest_path,
                source="inline",
                component_kind="Worker",
            )
        except Exception as e:
            # Flag-layer errors are non-fatal (CAP-WRK-003 spirit); record in health
            # and skip this worker. Structural errors (bad/missing path, command
            # shape, etc.) still raise — they indicate a malformed manifest.
            logger.warning("Failed to parse worker '{}': {}", name, e)
            if component_health is not None:
                component_health.append(
                    {
                        "kind": "worker",
                        "name": name,
                        "status": "error",
                        "error": str(e),
                        "detail": None,
                    }
                )
            continue

        if has_path:
            worker_def = _parse_inprocess_worker_entry(
                name,
                raw,
                capability_path,
                effective_manifest_path=effective_manifest_path,
                seen_paths=seen_paths,
                when=validated_when,
            )
        else:
            worker_def = _parse_subprocess_worker_entry(
                name,
                raw,
                effective_manifest_path=effective_manifest_path,
                capability_root=root,
                when=validated_when,
            )
        defs.append(worker_def)
        if component_health is not None:
            component_health.append(
                {
                    "kind": "worker",
                    "name": name,
                    "status": "stopped",
                    "error": None,
                    "detail": None,
                }
            )

    return defs


def _parse_inprocess_worker_entry(
    name: str,
    raw: dict[str, t.Any],
    capability_path: Path,
    *,
    effective_manifest_path: Path,
    seen_paths: dict[Path, str],
    when: list[str] | None,
) -> WorkerDef:
    """Validate a ``path:``-form worker entry (in-process Python worker)."""
    # Subprocess-only keys make no sense alongside path; reject explicitly so the
    # manifest author hears about it rather than silently ignoring the value.
    for subprocess_key in ("args", "env"):
        if subprocess_key in raw:
            raise ValueError(
                f"Worker '{name}' declares '{subprocess_key}' alongside 'path'; "
                f"that field is only valid for subprocess workers (use 'command') "
                f"in {effective_manifest_path} [CAP-WTOP-004]"
            )

    path_value = raw["path"]
    if not isinstance(path_value, str) or not path_value:
        raise ValueError(
            f"Worker '{name}' requires a non-empty 'path' "
            f"in {effective_manifest_path} [CAP-WRK-001]"
        )
    # CAP-WRK-004: path must resolve inside the capability directory.
    absolute = (capability_path / path_value).resolve()
    if not _is_contained_within(absolute, capability_path):
        raise ValueError(
            f"Worker '{name}' path '{path_value}' resolves outside the capability "
            f"directory in {effective_manifest_path} [CAP-WRK-004]"
        )
    # CAP-WRK-002: two entries may not share a path.
    if absolute in seen_paths:
        raise ValueError(
            f"Worker '{name}' path '{path_value}' is already used by worker "
            f"'{seen_paths[absolute]}' in {effective_manifest_path} [CAP-WRK-002]"
        )
    seen_paths[absolute] = name
    return WorkerDef(name=name, path=absolute, when=when)


def _parse_subprocess_worker_entry(
    name: str,
    raw: dict[str, t.Any],
    *,
    effective_manifest_path: Path,
    capability_root: str,
    when: list[str] | None,
) -> WorkerDef:
    """Validate a ``command:``-form worker entry (subprocess worker, CAP-WTOP-004)."""
    command_value = raw["command"]
    if not isinstance(command_value, str) or not command_value:
        raise ValueError(
            f"Worker '{name}' requires a non-empty 'command' "
            f"in {effective_manifest_path} [CAP-WTOP-004]"
        )

    args_raw = raw.get("args", [])
    if not isinstance(args_raw, list) or not all(isinstance(a, str) for a in args_raw):
        raise ValueError(
            f"Worker '{name}' 'args' must be a list of strings "
            f"in {effective_manifest_path} [CAP-WTOP-004]"
        )

    env_raw = raw.get("env", {})
    if not isinstance(env_raw, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in env_raw.items()
    ):
        raise ValueError(
            f"Worker '{name}' 'env' must be a map of string to string "
            f"in {effective_manifest_path} [CAP-WTOP-004]"
        )

    # CAP-WTOP-006 / CAP-WENV-002: the runtime owns DREADNODE_RUNTIME_{URL,TOKEN,ID}
    # and injects them authoritatively. Setting them in the manifest is a silent
    # no-op at runtime, which is confusing — reject at parse time so the author
    # sees the conflict immediately.
    reserved_env_keys = {key for key in env_raw if key in _RESERVED_WORKER_ENV_KEYS}
    if reserved_env_keys:
        offending = ", ".join(sorted(reserved_env_keys))
        raise ValueError(
            f"Worker '{name}' 'env' must not set runtime-owned keys ({offending}); "
            f"these are injected authoritatively by the runtime "
            f"in {effective_manifest_path} [CAP-WTOP-006]"
        )

    # CAP-WTOP-004: ${CAPABILITY_ROOT} interpolation in command, args, env values.
    command = _interpolate_capability_root(command_value, capability_root)
    args = [_interpolate_capability_root(a, capability_root) for a in args_raw]
    env = {k: _interpolate_capability_root(v, capability_root) for k, v in env_raw.items()}

    return WorkerDef(name=name, command=command, args=args, env=env, when=when)


def parse_mcp_servers(
    mcp: dict[str, t.Any] | None,
    capability_path: Path,
    component_health: list[dict[str, t.Any]] | None = None,
    *,
    declared_flags: set[str] | None = None,
    manifest_path: Path | None = None,
) -> list[MCPServerDef]:
    """Parse MCP server definitions from a capability manifest.

    CAP-MCP-001: files and inline servers are merged, inline wins on name conflict.
    Returns empty list for mcp={} (explicit disable).
    Auto-discovers .mcp.json and mcp.json when mcp is None.
    """
    from dreadnode.capabilities.flags import validate_when

    # mcp={} -> explicit disable
    if isinstance(mcp, dict) and not mcp:
        return []

    declared_flags = declared_flags or set()
    effective_manifest_path = manifest_path or (capability_path / "capability.yaml")

    # Track which servers came from files vs inline
    file_servers: dict[str, dict[str, t.Any]] = {}
    inline_servers: dict[str, dict[str, t.Any]] = {}

    if mcp is None:
        # Auto-discover
        for filename in (".mcp.json", "mcp.json"):
            p = capability_path / filename
            if p.exists():
                file_servers.update(_load_mcp_file(p))
    else:
        # Load from files first
        files = mcp.get("files", [])
        if isinstance(files, list):
            for rel in files:
                p = capability_path / rel
                if p.exists():
                    file_servers.update(_load_mcp_file(p))
                else:
                    logger.warning("MCP config file not found: {}", p)

        # Inline servers override file-loaded (CAP-MCP-001)
        servers = mcp.get("servers", {})
        if isinstance(servers, dict):
            inline_servers.update(servers)

    # Merge: inline wins on name conflict
    merged: dict[str, tuple[dict[str, t.Any], t.Literal["inline", "file"]]] = {
        name: (raw, "file") for name, raw in file_servers.items()
    }
    for name, raw in inline_servers.items():
        merged[name] = (raw, "inline")

    defs: list[MCPServerDef] = []
    for name, (raw, source) in merged.items():
        if not isinstance(raw, dict):
            logger.warning("Skipping MCP server '{}': expected object", name)
            continue
        try:
            server_def = _parse_server_entry(name, raw, capability_path, source=source)
            # CAP-FLAG-010/012: validate when predicate
            if declared_flags or server_def.when is not None:
                server_def.when = validate_when(
                    server_def.when,
                    declared_flags,
                    name,
                    effective_manifest_path,
                    source=source,
                )
            defs.append(server_def)
            if component_health is not None:
                component_health.append(
                    {
                        "kind": "mcp_server",
                        "name": name,
                        "status": "ok",
                        "error": None,
                        "detail": None,
                    }
                )
        except Exception as e:
            # CAP-MCP-007: single server failure doesn't invalidate capability
            logger.warning("Failed to parse MCP server '{}': {}", name, e)
            if component_health is not None:
                component_health.append(
                    {
                        "kind": "mcp_server",
                        "name": name,
                        "status": "error",
                        "error": str(e),
                        "detail": "Check MCP server definition — needs 'command' (stdio) or 'url' (http)",
                    }
                )

    return defs


# ============================================================================
# Merge Capabilities
# ============================================================================


def merge_capabilities(capabilities: list[t.Any]) -> MergedCapabilities:
    """Merge multiple capabilities into one."""

    agents: list[AgentDef] = []
    tools: list[t.Any] = []

    for cap in capabilities:
        agents.extend(cap.agents)
        tools.extend(cap.tools)

    return MergedCapabilities(agents=agents, tools=tools)


# ============================================================================
# Utility Types
# ============================================================================


class MergedCapabilities(t.NamedTuple):
    agents: list[AgentDef]
    tools: list[t.Any]


# ============================================================================
# Helpers
# ============================================================================


def _list_files_recursive(root: Path) -> list[Path]:
    """List all files recursively, sorted. Skips the manifest file."""
    if not root.is_dir():
        return []
    return [
        item
        for item in sorted(root.rglob("*"))
        if item.is_file() and item.name not in {MANIFEST_FILE, "__init__.py"}
    ]


def _assert_unique_names(
    defs: list[t.Any],
    kind: str,
    capability_path: Path,
) -> None:
    seen: set[str] = set()
    for d in defs:
        name = d.name if hasattr(d, "name") else d.get("name", "")
        if name in seen:
            raise ValueError(f"Duplicate {kind} name '{name}' in capability at {capability_path}")
        seen.add(name)


def _parse_frontmatter(content: str) -> tuple[dict[str, t.Any] | None, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content
    try:
        parsed = yaml.safe_load(match.group(1))
        return (parsed if isinstance(parsed, dict) else None), match.group(2)
    except yaml.YAMLError:
        return None, content


def _extract_markdown_summary(content: str) -> str:
    for raw_line in content.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            return re.sub(r"^#+\s*", "", line).strip()
        return line[:117] + "..." if len(line) > 120 else line
    return ""


def _read_string_list(
    obj: dict[str, t.Any] | None,
    field: str,
    source: Path,
) -> list[str]:
    if not obj or field not in obj or obj[field] is None:
        return []

    value = obj[field]
    if not isinstance(value, list):
        raise ValueError(f"Field '{field}' must be an array in {source}")  # noqa: TRY004

    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"Field '{field}' must contain only non-empty strings in {source}")
        result.append(item)
    return result


def _read_tools_dict(
    obj: dict[str, t.Any] | None,
    field: str,
    source: Path,
) -> dict[str, bool]:
    if not obj or field not in obj or obj[field] is None:
        return {}

    value = obj[field]
    if isinstance(value, dict):
        for k, v in value.items():
            if not isinstance(k, str) or not k.strip():
                raise ValueError(f"Field '{field}' keys must be non-empty strings in {source}")
            if not isinstance(v, bool):
                raise ValueError(f"Field '{field}' values must be booleans in {source}")  # noqa: TRY004
        return dict(value)

    raise ValueError(f"Field '{field}' must be a dict in {source}")
