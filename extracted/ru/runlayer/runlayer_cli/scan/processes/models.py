"""Data models for the runtime process-discovery channel (scan PHASE 12).

Two shapes:

* :class:`ProcessCandidate` -- the raw enumeration record (unredacted argv/cwd),
  internal to the channel. Source A (process table) and Source B (listening
  sockets) both produce these, unioned by pid.
* :class:`DiscoveredProcess` -- the scored, classified, and *redacted* outcome
  for one AI-related process. This is what dry-runs display and scan submissions
  send to the backend. Mirrors the RFC's ``DiscoveredProcess``.

Standard-library only so this stays inside the frozen ``aiwatch`` bundle import
closure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, TypedDict

ProcessKind = Literal["client", "mcp_server", "agent"]
DiscoverySource = Literal[
    "proc_table", "listening_port", "client_child", "runtime_probe"
]
BindScope = Literal["loopback", "all_interfaces", "none"]
Transport = Literal["stdio", "http", "sse"]
MCPConfigOverrideKind = Literal["file", "user_data_dir"]

MAX_SETTINGS_OVERRIDES_PER_PROCESS = 32
MAX_SETTINGS_OVERRIDE_VALUE_LENGTH = 2048


class SettingsOverridePayload(TypedDict):
    """Sanitized settings-override evidence sent with a process sighting."""

    flag: str
    value: str | None


@dataclass(frozen=True)
class OverrideConfigRef:
    """Raw local-only path reference used to parse an override MCP config."""

    client: str
    flag: str
    value: str
    mcp_config: MCPConfigOverrideKind
    pid: int | None
    user: str | None
    cwd: str | None = None
    wsl_distro: str | None = None


@dataclass
class ProcessCandidate:
    """A single enumerated process, pre-scoring and pre-redaction.

    ``argv`` and ``cwd`` are raw (unredacted) here; they are scrubbed only when a
    candidate is promoted to a :class:`DiscoveredProcess`. Nothing derived from
    these leaves the device before that redaction pass.
    """

    pid: int
    ppid: int | None = None
    exe: str | None = None
    argv: list[str] = field(default_factory=list)
    user: str | None = None
    started_at: str | None = None
    cwd: str | None = None
    listening_ports: list[int] = field(default_factory=list)
    bind_scope: BindScope = "none"
    discovery_source: DiscoverySource = "proc_table"
    # Shared service/container probes annotate candidates here. Keys are agent
    # framework ids; values are non-sensitive signal labels (service/docker).
    agent_runtime_signals: dict[str, list[str]] = field(default_factory=dict)
    wsl_distro: str | None = None


@dataclass
class DiscoveredProcess:
    """A scored, classified, redacted AI-related process (the RFC shape).

    ``command_hash`` is a stable hash of the full argv used only for correlation
    (never surfaced as readable text). ``config_hash`` is set when the process
    correlates to a configured MCP server from the filesystem channel. Evidence
    tokens in ``ai_signals`` explain the classification so an analyst can trust
    (or dismiss) the finding.
    """

    pid: int | None
    ppid: int | None
    kind: ProcessKind
    discovery_source: DiscoverySource
    matched_client: str | None
    exe: str | None
    argv_redacted: list[str]
    command_hash: str
    config_hash: str | None
    agent_framework_id: str | None
    agent_fingerprint: str | None
    agent_root_path: str | None
    listening_ports: list[int]
    bind_scope: BindScope
    transport: Transport | None
    ai_signals: list[str]
    confidence: float
    user: str | None
    started_at: str | None
    cwd_project: str | None
    settings_overrides: list[SettingsOverridePayload] = field(default_factory=list)
    wsl_distro: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serializable view for display and scan submission.

        It carries only redacted argv + correlation hashes, never raw cwd/env.
        """
        payload = {
            "pid": self.pid,
            "ppid": self.ppid,
            "kind": self.kind,
            "discovery_source": self.discovery_source,
            "matched_client": self.matched_client,
            "exe": self.exe,
            "argv_redacted": self.argv_redacted,
            "command_hash": self.command_hash,
            "config_hash": self.config_hash,
            "agent_framework_id": self.agent_framework_id,
            "agent_fingerprint": self.agent_fingerprint,
            "agent_root_path": self.agent_root_path,
            "listening_ports": self.listening_ports,
            "bind_scope": self.bind_scope,
            "transport": self.transport,
            "ai_signals": self.ai_signals,
            "confidence": round(self.confidence, 3),
            "user": self.user,
            "started_at": self.started_at,
            "cwd_project": self.cwd_project,
            "settings_overrides": self.settings_overrides,
        }
        if self.wsl_distro is not None:
            payload["wsl_distro"] = self.wsl_distro
        return payload

    def to_api_payload(self) -> dict[str, Any]:
        """Version-tolerant wire view for backend scan submission.

        Older backends reject the newer ``runtime_probe`` Literal with a 422
        for the whole scan. The field is optional and unused for correlation,
        so omit only that new value while retaining it in the local display.
        """
        payload = self.to_dict()
        if self.discovery_source == "runtime_probe":
            payload.pop("discovery_source")
        return payload


@dataclass
class ProcessDiscoveryResult:
    """Process sightings and local config refs discovered at runtime."""

    processes: list[DiscoveredProcess] = field(default_factory=list)
    override_config_refs: list[OverrideConfigRef] = field(default_factory=list)
