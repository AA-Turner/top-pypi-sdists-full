"""DTOs and the inheritance resolver for agent runtime environments.

A runtime environment is a reusable, org-scoped toolchain layer (language packages, CLIs via
brew, setup scripts, non-secret config) an agent's fleet turns run inside. Environments inherit:
``parent_environment_id`` points at a base whose layers a child extends and overrides. The
resolver flattens the chain root->...->env into one effective spec and content-hashes it; that
hash is the fleet's cache key for the materialized layer. Secrets never live here - workspace
secrets are injected at turn time and always win.

Mirror of ``xpander_dev_utils.models.runtime_environments`` in xpander-mono; the SDK cannot import
that package, so this copy is kept identical by hand (like the orchestration models mirror).
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Literal, Mapping, Optional

from pydantic import Field, field_validator

from xpander_sdk.models.shared import XPanderSharedModel

__all__ = [
    "PACKAGE_MANAGERS",
    "RuntimeEnvironmentCycleError",
    "RuntimePackages",
    "RuntimeScript",
    "RuntimeConfigFile",
    "RuntimeEnvironment",
    "RuntimeEnvironmentPublicItem",
    "RuntimeEnvironmentCreateRequest",
    "RuntimeEnvironmentUpdateRequest",
    "ResolvedRuntimeEnvironment",
    "resolve_runtime_environment",
]

PACKAGE_MANAGERS = ("pip", "npm", "pnpm", "brew")


class RuntimeEnvironmentCycleError(ValueError):
    """Raised when an environment's parent chain loops back on itself."""


class RuntimePackages(XPanderSharedModel):
    """Package lists per manager; each entry is a manager-native spec (e.g. 'httpx==0.27')."""

    pip: List[str] = Field(default_factory=list)
    npm: List[str] = Field(default_factory=list)
    pnpm: List[str] = Field(default_factory=list)
    brew: List[str] = Field(default_factory=list)


class RuntimeScript(XPanderSharedModel):
    """One setup step, run after install; steps run in order, base before child."""

    name: str = Field(..., description="Short label for the step.")
    body: str = Field(..., description="Shell body executed in the layer at build time.")


class RuntimeConfigFile(XPanderSharedModel):
    """A non-secret config file seeded into the layer (kube context, cloud profile, etc.)."""

    path: str = Field(..., description="Destination path, relative to the layer home.")
    contents: str = Field(
        ...,
        description="Plain file contents - non-secret config only; workspace secrets are injected "
        "separately at turn time and take precedence.",
    )

    @field_validator("path")
    @classmethod
    def _path_stays_in_layer(cls, value: str) -> str:
        """A config path is a relative, forward-slash path inside the layer home - reject escapes."""
        if not value or "\x00" in value or "\\" in value:
            raise ValueError("config path must be non-empty and contain no NUL or backslash")
        if value.startswith("/") or value.startswith("~"):
            raise ValueError("config path must be relative to the layer home")
        if any(segment == ".." for segment in value.split("/")):
            raise ValueError("config path must not contain '..'")
        return value


class RuntimeEnvironment(XPanderSharedModel):
    """A runtime environment row - this layer's own definition (unresolved)."""

    id: Optional[str] = None
    organization_id: Optional[str] = None
    name: str = Field(..., description="Environment name, unique per org among live rows.")
    icon: Optional[str] = None
    description: Optional[str] = None
    parent_environment_id: Optional[str] = Field(
        default=None, description="The base this environment extends; None = a root."
    )
    packages: RuntimePackages = Field(default_factory=RuntimePackages)
    setup_scripts: List[RuntimeScript] = Field(default_factory=list)
    config: List[RuntimeConfigFile] = Field(default_factory=list)
    access_scope: Literal["organizational", "personal"] = Field(default="organizational")
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RuntimeEnvironmentPublicItem(XPanderSharedModel):
    """The metadata projection the list endpoints return (no heavy body)."""

    id: str
    organization_id: str
    name: str
    icon: Optional[str] = None
    description: Optional[str] = None
    parent_environment_id: Optional[str] = None
    access_scope: Literal["organizational", "personal"] = "organizational"
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RuntimeEnvironmentCreateRequest(XPanderSharedModel):
    name: str
    icon: Optional[str] = None
    description: Optional[str] = None
    parent_environment_id: Optional[str] = None
    packages: RuntimePackages = Field(default_factory=RuntimePackages)
    setup_scripts: List[RuntimeScript] = Field(default_factory=list)
    config: List[RuntimeConfigFile] = Field(default_factory=list)
    access_scope: Literal["organizational", "personal"] = "organizational"


class RuntimeEnvironmentUpdateRequest(XPanderSharedModel):
    """A partial update - only the provided fields change."""

    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    parent_environment_id: Optional[str] = None
    packages: Optional[RuntimePackages] = None
    setup_scripts: Optional[List[RuntimeScript]] = None
    config: Optional[List[RuntimeConfigFile]] = None
    access_scope: Optional[Literal["organizational", "personal"]] = None


class ResolvedRuntimeEnvironment(XPanderSharedModel):
    """The inheritance chain flattened into one effective spec, plus its content hash."""

    environment_id: str = Field(..., description="The leaf environment this was resolved for.")
    chain: List[str] = Field(default_factory=list, description="Env ids root-first, leaf last.")
    packages: RuntimePackages = Field(default_factory=RuntimePackages)
    setup_scripts: List[RuntimeScript] = Field(default_factory=list)
    config: List[RuntimeConfigFile] = Field(default_factory=list)
    hash: str = Field(..., description="sha256 of the effective spec - the fleet layer cache key.")


def _package_identity(manager: str, spec: str) -> str:
    """The name a package spec pins, so a child can override a parent's version of it."""
    text = spec.strip()
    if manager in ("npm", "pnpm"):
        # scoped '@scope/name@ver' -> split on the LAST '@'; unscoped 'name@ver' -> first '@'
        if text.startswith("@"):
            at = text.rfind("@")
            return text[:at] if at > 0 else text
        return text.split("@", 1)[0]
    # pip / brew: the name ends at the first version operator or space
    for i, ch in enumerate(text):
        if ch in "=<>!~ @[;":
            return text[:i]
    return text


def _merge_packages(chain_packages: List[RuntimePackages]) -> RuntimePackages:
    """Merge base->child: keep first-seen order, a later (child) spec replaces the same name."""
    out: Dict[str, List[str]] = {m: [] for m in PACKAGE_MANAGERS}
    order: Dict[str, List[str]] = {m: [] for m in PACKAGE_MANAGERS}
    by_name: Dict[str, Dict[str, str]] = {m: {} for m in PACKAGE_MANAGERS}
    for pkgs in chain_packages:
        for manager in PACKAGE_MANAGERS:
            for spec in getattr(pkgs, manager) or []:
                name = _package_identity(manager, spec)
                if name not in by_name[manager]:
                    order[manager].append(name)
                by_name[manager][name] = spec  # child spec wins for the same name
    for manager in PACKAGE_MANAGERS:
        out[manager] = [by_name[manager][name] for name in order[manager]]
    return RuntimePackages(**out)


def resolve_runtime_environment(
    environment_id: str,
    by_id: Mapping[str, RuntimeEnvironment],
) -> Optional[ResolvedRuntimeEnvironment]:
    """Flatten the parent chain of ``environment_id`` into one effective, content-hashed spec.

    ``by_id`` maps env id -> its own (unresolved) definition, built from LIVE rows. Returns None
    when the requested leaf is absent (unknown or soft-deleted) - distinct from a present-but-empty
    environment - so the caller falls back to the platform default rather than a valid-looking empty
    layer. Packages merge with child-overrides keyed on package name; scripts run base->child in
    order; config files merge by path with child-overrides. A missing *ancestor* ends the walk
    (treated as a root); a chain that loops raises ``RuntimeEnvironmentCycleError``.
    """
    if environment_id not in by_id:
        return None
    chain: List[RuntimeEnvironment] = []
    seen: set = set()
    cursor: Optional[str] = environment_id
    while cursor is not None:
        if cursor in seen:
            raise RuntimeEnvironmentCycleError(
                f"runtime environment inheritance cycle at {cursor}"
            )
        seen.add(cursor)
        env = by_id.get(cursor)
        if env is None:
            break
        chain.append(env)
        cursor = env.parent_environment_id
    chain.reverse()  # root first, leaf last

    packages = _merge_packages([e.packages for e in chain])

    scripts: List[RuntimeScript] = []
    for env in chain:
        scripts.extend(env.setup_scripts or [])

    config_by_path: Dict[str, RuntimeConfigFile] = {}
    for env in chain:
        for cfg in env.config or []:
            config_by_path[cfg.path] = cfg  # child overrides the same path
    config = [config_by_path[path] for path in sorted(config_by_path)]

    canonical = json.dumps(
        {
            "packages": {m: getattr(packages, m) for m in PACKAGE_MANAGERS},
            "setup_scripts": [{"name": s.name, "body": s.body} for s in scripts],
            "config": [{"path": c.path, "contents": c.contents} for c in config],
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    return ResolvedRuntimeEnvironment(
        environment_id=environment_id,
        chain=[e.id for e in chain if e.id],
        packages=packages,
        setup_scripts=scripts,
        config=config,
        hash=digest,
    )
