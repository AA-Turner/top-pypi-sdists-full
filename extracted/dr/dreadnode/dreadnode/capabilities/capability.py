"""High-level resolved capability object."""

from __future__ import annotations

import asyncio
import json
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

from dreadnode.capabilities.loader import (
    LoadOptions,
    get_default_capabilities_dir,
    load_capabilities_from_search_paths,
    resolve_search_paths,
)
from dreadnode.capabilities.loader import (
    load_capability as load_capability_definition,
)
from dreadnode.capabilities.types import DependencySpec, HealthCheck
from dreadnode.storage.storage import Storage

if t.TYPE_CHECKING:
    import builtins

    from dreadnode.capabilities.flags import FlagDef, ResolvedFlag
    from dreadnode.capabilities.types import MCPServerDef, WorkerDef
    from dreadnode.packaging.manifest import CapabilityManifest


@dataclass
class DiscoverResult:
    """Result of capability discovery for a single host type."""

    capabilities: dict[str, Capability] = field(default_factory=dict)
    disabled: dict[str, Capability] = field(default_factory=dict)
    failures: list[dict[str, t.Any]] = field(default_factory=list)


def read_local_capability_state(path: Path) -> dict[str, bool]:
    """Read persisted local capability state keyed by bare capability name."""
    return {
        key: record.get("enabled", True)
        for key, record in read_local_capability_records(path).items()
    }


def read_local_capability_records(path: Path) -> dict[str, dict[str, t.Any]]:
    """Read persisted local capability records keyed by bare capability name."""
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text())
    except Exception:
        return {}
    if not isinstance(raw, dict):
        return {}

    records: dict[str, dict[str, t.Any]] = {}
    for key, value in raw.items():
        if not isinstance(key, str):
            continue
        if isinstance(value, bool):
            records[key] = {"enabled": value}
            continue
        if not isinstance(value, dict):
            continue
        record = dict(value)
        enabled = record.get("enabled", True)
        if not isinstance(enabled, bool):
            enabled = True
        record["enabled"] = enabled
        records[key] = record
    return records


def write_local_capability_state(path: Path, state: dict[str, bool]) -> None:
    """Persist local capability state keyed by bare capability name."""
    existing = read_local_capability_records(path)
    records: dict[str, dict[str, t.Any]] = {}
    for key, enabled in state.items():
        if not isinstance(key, str):
            continue
        record = dict(existing.get(key, {}))
        record["enabled"] = enabled
        records[key] = record
    write_local_capability_records(path, records)


def write_local_capability_records(path: Path, state: dict[str, dict[str, t.Any]]) -> None:
    """Persist structured local capability records keyed by bare capability name."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True))


class Capability:
    """Resolved capability ready for SDK and runtime use."""

    def __init__(
        self,
        capability: str | Path,
        *,
        cwd: Path | None = None,
        storage: Storage | None = None,
        capability_dirs: builtins.list[str | Path] | None = None,
        bundled: bool = False,
    ) -> None:
        self._ref = capability
        self._cwd = Path(cwd) if cwd is not None else Path.cwd()
        self._storage = storage
        self._capability_dirs = capability_dirs
        self._bundled = bundled

        resolved = self._resolve()
        self._copy_from(resolved)
        # _copy_from inherits _bundled from the resolver's result, but the
        # caller-provided flag takes precedence — the resolver doesn't know
        # it's loading a bundled capability unless the caller tells it.
        self._bundled = bundled

    @classmethod
    def _from_resolved(
        cls,
        *,
        path: Path,
        manifest: CapabilityManifest,
        agents: builtins.list[t.Any] | None = None,
        tools: builtins.list[t.Any] | None = None,
        hooks: builtins.list[t.Any] | None = None,
        policies: builtins.list[t.Any] | None = None,
        worker_defs: builtins.list[WorkerDef] | None = None,
        skills_paths: builtins.list[Path] | None = None,
        skills_path: Path | None = None,
        mcp_server_defs: builtins.list[MCPServerDef] | None = None,
        source: t.Literal["runtime", "local"] = "local",
        component_health: builtins.list[dict[str, t.Any]] | None = None,
        dependencies: DependencySpec | None = None,
        checks: builtins.list[HealthCheck] | None = None,
        ref: str | Path | None = None,
        cwd: Path | None = None,
        storage: Storage | None = None,
        capability_dirs: builtins.list[str | Path] | None = None,
        bundled: bool = False,
    ) -> Capability:
        instance = cls.__new__(cls)
        instance._ref = ref if ref is not None else manifest.name
        instance._cwd = Path(cwd) if cwd is not None else Path.cwd()
        instance._storage = storage
        instance._capability_dirs = capability_dirs
        instance._path = path
        instance._manifest = manifest
        instance._agents = list(agents or [])
        instance._tools = list(tools) if tools is not None else None
        instance._hooks = list(hooks) if hooks is not None else None
        instance._policies = list(policies) if policies is not None else None
        instance._worker_defs = list(worker_defs or [])
        instance._skills_paths = skills_paths
        instance._skills_path = skills_path
        instance._mcp_server_defs = list(mcp_server_defs or [])
        instance._source = source
        instance._component_health = list(component_health or [])
        instance._dependencies = dependencies if dependencies is not None else DependencySpec()
        instance._checks = list(checks or [])
        instance._flag_defs: builtins.list[FlagDef] | None = None
        instance._resolved_flags: builtins.list[ResolvedFlag] = []
        instance._bundled = bundled
        return instance

    @classmethod
    def _with_context(
        cls,
        capability: Capability,
        *,
        cwd: Path | None = None,
        storage: Storage | None = None,
        capability_dirs: builtins.list[str | Path] | None = None,
    ) -> Capability:
        return cls._from_resolved(
            path=capability.path,
            manifest=capability.manifest,
            agents=capability.agents,
            tools=capability._tools,
            hooks=capability._hooks,
            policies=capability._policies,
            worker_defs=capability._worker_defs,
            skills_paths=capability.skills_paths,
            skills_path=capability.skills_path,
            mcp_server_defs=capability.mcp_server_defs,
            source=capability.source,
            component_health=capability.component_health,
            dependencies=capability._dependencies,
            checks=capability._checks,
            ref=capability._ref,
            cwd=cwd,
            storage=storage,
            capability_dirs=capability_dirs,
        )

    @classmethod
    def list(
        cls,
        *,
        cwd: Path | None = None,
        storage: Storage | None = None,
        capability_dirs: builtins.list[str | Path] | None = None,
    ) -> builtins.list[str]:
        """List capability names visible from the configured search paths."""
        search_paths = resolve_search_paths(
            cwd=Path(cwd) if cwd is not None else Path.cwd(),
            user_dir=storage.capabilities_path
            if storage is not None
            else get_default_capabilities_dir(),
            capability_dirs=capability_dirs,
        )
        result = asyncio.run(load_capabilities_from_search_paths(search_paths, LoadOptions()))
        return [cap.name for cap in result.capabilities]

    @classmethod
    def discover(
        cls,
        *,
        cwd: Path | None = None,
        storage: Storage | None = None,
        capability_dirs: builtins.list[str | Path] | None = None,
        workspace_dir: Path | None = None,
        host: str = "local",
    ) -> DiscoverResult:
        """Discover capabilities for a specific host type."""
        resolved_cwd = Path(cwd) if cwd is not None else Path.cwd()
        all_failures: builtins.list[dict[str, t.Any]] = []

        if host == "sandbox":
            effective: dict[str, Capability] = {}
            from loguru import logger

            logger.info(
                "Discovering sandbox capabilities from workspace_dir={}  (exists={})",
                workspace_dir,
                workspace_dir.exists() if workspace_dir else "N/A",
            )
            if workspace_dir and workspace_dir.exists():
                ws_result = asyncio.run(
                    load_capabilities_from_search_paths(
                        [workspace_dir],
                        LoadOptions(),
                        source="runtime",
                    )
                )
                for cap in ws_result.capabilities:
                    effective[cap.name] = cls._with_context(
                        cap,
                        cwd=resolved_cwd,
                        storage=storage,
                        capability_dirs=capability_dirs,
                    )
                for failure in ws_result.failures:
                    all_failures.append(
                        {
                            "name": failure.name,
                            "path": str(failure.path),
                            "error": failure.error,
                            "source": "runtime",
                        }
                    )
            return DiscoverResult(capabilities=effective, failures=all_failures)

        search_paths = resolve_search_paths(
            cwd=resolved_cwd,
            user_dir=storage.capabilities_path
            if storage is not None
            else get_default_capabilities_dir(),
            capability_dirs=capability_dirs,
        )
        local_result = asyncio.run(load_capabilities_from_search_paths(search_paths, LoadOptions()))
        effective: dict[str, Capability] = {}
        for cap in local_result.capabilities:
            effective[cap.name] = cls._with_context(
                cap,
                cwd=resolved_cwd,
                storage=storage,
                capability_dirs=capability_dirs,
            )
        for failure in local_result.failures:
            all_failures.append(
                {
                    "name": failure.name,
                    "path": str(failure.path),
                    "error": failure.error,
                    "source": "local",
                }
            )

        local_state_path = (
            storage.local_capability_state_path
            if storage is not None
            else Storage().local_capability_state_path
        )
        local_state = read_local_capability_state(local_state_path)
        disabled: dict[str, Capability] = {}
        for name in list(effective.keys()):
            if local_state.get(name, True) is False:
                disabled[name] = effective.pop(name)

        return DiscoverResult(capabilities=effective, disabled=disabled, failures=all_failures)

    @property
    def name(self) -> str:
        return self._manifest.name

    @property
    def version(self) -> str:
        return self._manifest.version

    @property
    def description(self) -> str:
        return self._manifest.description

    @property
    def path(self) -> Path:
        return self._path

    @property
    def source(self) -> str:
        return self._source

    @property
    def bundled(self) -> bool:
        """Whether this capability is the SDK-internal bundled platform capability.

        Set by the loader (via ``load_capability(path, bundled=True)``) for
        exactly the capability shipped in ``dreadnode/builtin_capabilities``.
        Not a manifest field; not author-settable (CAP-IDENT-004/005).
        """
        return getattr(self, "_bundled", False)

    @property
    def component_health(self) -> builtins.list[dict[str, t.Any]]:
        return self._component_health

    @property
    def manifest(self) -> CapabilityManifest:
        return self._manifest

    @property
    def tools(self) -> builtins.list[t.Any]:
        if self._tools is None:
            from dreadnode.capabilities.loader import (
                _discover_python_tools,
                _stamp_tool_identities,
            )

            raw = _discover_python_tools(self._path, self._manifest, self._component_health)
            self._tools = _stamp_tool_identities(
                raw, cap_name=self._manifest.name, bundled=self.bundled
            )
        return self._tools or []

    @property
    def hooks(self) -> builtins.list[t.Any]:
        if self._hooks is None:
            from dreadnode.capabilities.loader import _discover_python_hooks

            self._hooks = _discover_python_hooks(self._path, self._manifest, self._component_health)
        return self._hooks

    @property
    def policies(self) -> builtins.list[t.Any]:
        if self._policies is None:
            from dreadnode.capabilities.loader import _discover_python_policies

            self._policies = _discover_python_policies(
                self._path, self._manifest, self._component_health
            )
        return self._policies

    @property
    def worker_defs(self) -> builtins.list[WorkerDef]:
        """Parsed worker entries from capability.yaml (CAP-WRK-001).

        Module import is deferred to the `WorkerLifecycleManager`, which
        evaluates the gate (CAP-WRK-007) before importing.
        """
        return self._worker_defs

    @property
    def agents(self) -> builtins.list[t.Any]:
        return self._agents

    @property
    def skills_path(self) -> Path | None:
        return self._skills_path

    @property
    def mcp_server_defs(self) -> builtins.list[MCPServerDef]:
        return self._mcp_server_defs

    @property
    def skills_paths(self) -> builtins.list[Path] | None:
        return self._skills_paths

    @property
    def dependencies(self) -> DependencySpec:
        return self._dependencies

    @property
    def checks(self) -> builtins.list[HealthCheck]:
        return self._checks

    @property
    def flag_defs(self) -> builtins.list[FlagDef]:
        if self._flag_defs is None:
            from dreadnode.capabilities.flags import validate_flags_block

            self._flag_defs = validate_flags_block(
                self._manifest.flags, self._path / "capability.yaml"
            )
        return self._flag_defs

    @property
    def resolved_flags(self) -> builtins.list[ResolvedFlag]:
        return self._resolved_flags

    def resolve_flags(
        self,
        persisted: dict[str, bool] | None = None,
        env_overrides: dict[str, bool] | None = None,
        cli_overrides: dict[str, bool] | None = None,
    ) -> None:
        """Resolve effective flag state from the four-layer override stack."""
        from dreadnode.capabilities.flags import resolve_flags

        self._resolved_flags = resolve_flags(
            self.flag_defs,
            persisted=persisted,
            env_overrides=env_overrides,
            cli_overrides=cli_overrides,
        )

    def flag_env_vars(self) -> dict[str, str]:
        """Build CAPABILITY_FLAG__* env vars from resolved flags (CAP-FLAG-020)."""
        from dreadnode.capabilities.flags import flag_to_env_name

        return {
            flag_to_env_name(self.name, f.name): "1" if f.effective else "0"
            for f in self._resolved_flags
        }

    def _copy_from(self, other: Capability) -> None:
        self._ref = other._ref
        self._cwd = other._cwd
        self._storage = other._storage
        self._capability_dirs = other._capability_dirs
        self._path = other._path
        self._manifest = other._manifest
        self._agents = other._agents
        self._tools = other._tools
        self._hooks = other._hooks
        self._policies = other._policies
        self._worker_defs = other._worker_defs
        self._skills_paths = other._skills_paths
        self._skills_path = other._skills_path
        self._mcp_server_defs = other._mcp_server_defs
        self._source = other._source
        self._component_health = other._component_health
        self._dependencies = other._dependencies
        self._checks = other._checks
        self._flag_defs = getattr(other, "_flag_defs", None)
        self._resolved_flags = getattr(other, "_resolved_flags", [])
        self._bundled = getattr(other, "_bundled", False)

    def _resolve(self) -> Capability:
        load_options = LoadOptions()
        capability_path = Path(self._ref)

        if capability_path.exists():
            return self._with_context(
                asyncio.run(
                    load_capability_definition(capability_path, load_options, bundled=self._bundled)
                ),
                cwd=self._cwd,
                storage=self._storage,
                capability_dirs=self._capability_dirs,
            )

        search_paths = resolve_search_paths(
            cwd=self._cwd,
            user_dir=(
                self._storage.capabilities_path
                if self._storage is not None
                else get_default_capabilities_dir()
            ),
            capability_dirs=self._capability_dirs,
        )
        result = asyncio.run(load_capabilities_from_search_paths(search_paths, load_options))

        target_name = str(self._ref)
        for capability in result.capabilities:
            if capability.name == target_name:
                return self._with_context(
                    capability,
                    cwd=self._cwd,
                    storage=self._storage,
                    capability_dirs=self._capability_dirs,
                )

        searched = ", ".join(str(path) for path in search_paths)
        raise FileNotFoundError(f"Capability not found: {target_name}. Searched: {searched}")

    def __repr__(self) -> str:
        return f"Capability(name={self.name!r}, path={str(self.path)!r})"
