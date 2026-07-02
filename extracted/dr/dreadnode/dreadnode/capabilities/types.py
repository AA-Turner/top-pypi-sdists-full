"""
Capability type definitions — v1 spec.

See specs/capabilities/contract.md for the canonical schema.
"""

from __future__ import annotations

import os
import re
import typing as t
from dataclasses import dataclass, field

if t.TYPE_CHECKING:
    from pathlib import Path

    from dreadnode.capabilities.capability import Capability

# ============================================================================
# Environment Variable Interpolation (CAP-MCP-003)
# ============================================================================

_ENV_VAR_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-(.*?))?\}")


def _expand_env_vars(value: str) -> str:
    """Expand ${VAR} and ${VAR:-default} placeholders from os.environ.

    Called at connect time (not parse time) so that capabilities can be
    loaded, packaged, and inspected without requiring every referenced
    env var to be set in the current shell.
    """

    def _replace(match: re.Match[str]) -> str:
        name = match.group(1)
        default = match.group(2)
        env_value = os.environ.get(name)
        if env_value is not None:
            return env_value
        if default is not None:
            return default
        raise ValueError(
            f"MCP server references unset env var '{name}' "
            f"(use ${{{name}:-default}} to provide a fallback)"
        )

    return _ENV_VAR_PATTERN.sub(_replace, value)


def _expand_optional_env_vars(value: str) -> str | None:
    """Expand env vars for an *optional* header value (CAP-MCP-013).

    Identical to :func:`_expand_env_vars`, except an unset ``${VAR}`` without
    a default does not raise — instead the whole value resolves to ``None``,
    signalling the caller to omit the header entirely rather than send it with
    an empty credential (e.g. a bare ``Authorization: Bearer``). A ``${VAR:-x}``
    default still applies, so an optional header with a fallback keeps its key.
    """
    missing = False

    def _replace(match: re.Match[str]) -> str:
        nonlocal missing
        name = match.group(1)
        default = match.group(2)
        env_value = os.environ.get(name)
        if env_value is not None:
            return env_value
        if default is not None:
            return default
        missing = True
        return ""

    result = _ENV_VAR_PATTERN.sub(_replace, value)
    return None if missing else result


def _expand_env_in_dict(d: dict[str, str]) -> dict[str, str]:
    """Expand env vars in all values of a string dict."""
    return {k: _expand_env_vars(v) for k, v in d.items()}


def _expand_env_in_list(lst: list[str]) -> list[str]:
    """Expand env vars in all items of a string list."""
    return [_expand_env_vars(v) for v in lst]


# ============================================================================
# Component Definitions
# ============================================================================


@dataclass
class AgentDef:
    """Agent definition resolved from markdown frontmatter."""

    name: str
    description: str
    model: str = "inherit"
    engine: str = "inherit"
    """Loop owner: ``inherit`` (→ runtime default → ``native``), a built-in engine
    name (e.g. ``claude-code``), or a ``mod:attr`` reference. Resolves with the
    same precedence as ``model``."""
    system_prompt: str = ""
    tools: dict[str, bool] = field(default_factory=dict)
    skills: list[str] = field(default_factory=list)
    metadata: dict[str, t.Any] | None = None
    capability: str | None = None


@dataclass
class AgentLinkDef:
    """Synthetic capability link between agents."""

    kind: t.Literal["delegate", "subagent", "handoff"]
    source: str
    target: str


@dataclass
class MCPServerAuth:
    """Parsed ``auth:`` block from an MCP server manifest entry.

    Only OAuth is supported today; ``type`` is reserved for future
    auth schemes (e.g. ``api_key``, ``mTLS``). Bound to streamable-HTTP
    transports — declaring ``auth:`` on a stdio server is rejected at
    load time (stdio servers handle their own auth in the subprocess).
    """

    type: t.Literal["oauth"] = "oauth"
    scope: str | None = None
    client_name: str | None = None


@dataclass
class MCPServerDef:
    """Parsed MCP server definition from a capability manifest.

    CAP-MCP-002: transport is inferred from fields (command -> stdio, url -> streamable-http).
    """

    name: str
    transport: t.Literal["stdio", "streamable-http"]
    # stdio fields
    command: str | None = None
    args: list[str] = field(default_factory=list)
    env: dict[str, str] | None = None
    cwd: str | Path | None = None
    # streamable-http fields
    url: str | None = None
    headers: dict[str, str] | None = None
    # header keys declared `optional: true` — dropped when their ${VAR} is unset (CAP-MCP-013)
    optional_headers: set[str] = field(default_factory=set)
    # auth (streamable-http only, CAP-MCP-011)
    auth: MCPServerAuth | None = None
    # timeout fields (capability.yaml → server config)
    timeout: float | None = None
    init_timeout: float | None = None
    # flag gating (CAP-FLAG-010)
    when: list[str] | None = None
    source: t.Literal["inline", "file"] | None = None

    def _resolve_init_timeout(self) -> dict[str, float]:
        """Resolve init_timeout: explicit init_timeout > timeout > default."""
        if self.init_timeout is not None:
            return {"init_timeout": self.init_timeout}
        if self.timeout is not None:
            return {"init_timeout": self.timeout}
        return {}

    def _expand_headers(self) -> dict[str, str] | None:
        """Resolve header env placeholders, omitting unset optional headers.

        Non-optional headers follow CAP-MCP-003 (raise on unset, no default).
        Optional headers (CAP-MCP-013) whose ``${VAR}`` is unset and has no
        default are dropped from the wire entirely, leaving reactive OAuth
        (CAP-MCP-011) as the clean default instead of sending an empty
        ``Authorization`` header.
        """
        if not self.headers:
            return None
        resolved: dict[str, str] = {}
        for key, value in self.headers.items():
            if key in self.optional_headers:
                expanded = _expand_optional_env_vars(value)
                if expanded is None:
                    continue
                resolved[key] = expanded
            else:
                resolved[key] = _expand_env_vars(value)
        return resolved or None

    def to_server_config(self) -> t.Any:
        """Convert to an MCPClient-compatible ServerConfig.

        Resolves ${VAR} and ${VAR:-default} env placeholders at this point
        (connect time), not at capability load time, so that capabilities
        can be loaded/packaged without every secret being present.
        """
        from dreadnode.agents.mcp.config import HttpServerConfig, OAuthConfig, StdioServerConfig

        timeout_kw = self._resolve_init_timeout()
        if self.transport == "stdio":
            return StdioServerConfig(
                command=_expand_env_vars(self.command or ""),
                args=_expand_env_in_list(self.args),
                env=_expand_env_in_dict(self.env) if self.env else None,
                cwd=_expand_env_vars(str(self.cwd)) if self.cwd else None,
                **timeout_kw,
            )
        oauth_config: OAuthConfig | None = None
        if self.auth is not None and self.auth.type == "oauth":
            oauth_config = OAuthConfig(
                client_name=self.auth.client_name or "dreadnode",
                scope=self.auth.scope,
            )
        return HttpServerConfig(
            url=_expand_env_vars(self.url or ""),
            headers=self._expand_headers(),
            oauth=oauth_config,
            **timeout_kw,
        )


@dataclass
class WorkerDef:
    """Parsed worker entry from a capability manifest.

    Two kinds, mutually exclusive (CAP-WTOP-004):

    * In-process Python worker — populates :attr:`path`; the runtime imports
      the module and drives the :class:`Worker` instance via ``WorkerRunner``.
    * Subprocess worker — populates :attr:`command` (with optional
      :attr:`args` / :attr:`env`); the runtime spawns and supervises it,
      injecting the ``DREADNODE_RUNTIME_*`` env contract (CAP-WENV-001..003).

    See CAP-WRK-001/002/007 and CAP-WTOP-004..009 in specs/capabilities/workers.md.
    """

    name: str
    path: Path | None = None
    command: str | None = None
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    when: list[str] | None = None

    @property
    def is_subprocess(self) -> bool:
        """True when this worker is a runtime-spawned subprocess (CAP-WTOP-004)."""
        return self.command is not None


@dataclass
class DependencySpec:
    """Declared runtime dependencies from capability.yaml.

    These fields are sandbox-specific — they describe what a managed
    sandbox (E2B/Docker) needs. Ignored for local installs.
    """

    python: list[str] = field(default_factory=list)
    packages: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)


@dataclass
class HealthCheck:
    """Pre-flight check definition from capability.yaml.

    Runs on load for enabled capabilities. Exit code 0 = pass, non-zero = fail.
    Failed checks produce a component_health entry with kind="check".
    """

    name: str
    command: str


@dataclass
class LoadFailure:
    """A capability that failed to load."""

    name: str
    path: Path
    error: str


@dataclass
class LoadResult:
    """Result of loading capabilities from search paths."""

    capabilities: list[Capability] = field(default_factory=list)
    failures: list[LoadFailure] = field(default_factory=list)


@dataclass
class LoadOptions:
    """Options for loading a capability."""

    base_dir: Path | None = None
