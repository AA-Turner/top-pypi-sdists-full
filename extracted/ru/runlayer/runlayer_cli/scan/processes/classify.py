"""AI-relatedness scoring + classification for enumerated processes.

Each :class:`~runlayer_cli.scan.processes.models.ProcessCandidate` is scored by
combining weighted signals; only candidates scoring at or above a threshold are
promoted to a redacted :class:`~runlayer_cli.scan.processes.models.DiscoveredProcess`.
Non-AI candidates are dropped client-side (volume, noise, privacy).

Design principle from the RFC: a bare "listens on a port" is deliberately weak
and must combine with another signal. Clients spawn many non-MCP children, so
parenthood alone is also weak and must combine -- only an exact match to a
configured server, a client executable signature, or an unambiguous MCP/agent
argv marker is strong enough to stand alone. This keeps the false-positive rate
low against the dev-server / browser / database corpus.

Classification correlates back to the filesystem channel: a listening port that
matches a configured MCP server URL, or an argv that matches a configured
stdio server's command, carries that server's ``config_hash``.

Standard-library only so this stays inside the frozen ``aiwatch`` bundle.
"""

from __future__ import annotations

import os
from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass, field
from functools import lru_cache
from urllib.parse import urlsplit

import structlog

from runlayer_cli.scan.agents.install import (
    AgentRuntimeSignature,
    runtime_signatures,
)
from runlayer_cli.scan.agents.redact import sanitize_path
from runlayer_cli.scan.agents.registry import load_registry
from runlayer_cli.scan.processes.models import (
    DiscoveredProcess,
    OverrideConfigRef,
    ProcessCandidate,
    ProcessDiscoveryResult,
    ProcessKind,
    Transport,
)
from runlayer_cli.scan.processes.redact import (
    command_hash,
    redact_argv,
    redact_cwd_project,
    redact_exe,
)
from runlayer_cli.scan.processes.settings_override import (
    SettingsOverrideFlagSpec,
    SettingsOverrideMatch,
    extract_settings_overrides,
    override_config_refs,
    sanitized_settings_overrides,
)

logger = structlog.get_logger(__name__)

# Signal weights. Anything >= DEFAULT_THRESHOLD stands alone; everything below
# must combine. Tuned so bare listeners and bare client-parenthood are dropped,
# while configured-server matches / client executables / unambiguous MCP argv
# markers pass on their own.
W_CLIENT_SIGNATURE = 0.9
W_CONFIG_COMMAND_MATCH = 0.9
W_CONFIG_PORT_MATCH = 0.8
W_MCP_OFFICIAL = 0.7
W_AGENT_PROBE = 0.7
W_AGENT_RUNTIME = 0.6
W_AGENT_FRAMEWORK = 0.5
W_MCP_MARKER = 0.4
W_PARENT_CLIENT = 0.3
W_ELECTRON_MAIN_HELPERS = 0.3
W_AI_CHILD_TREE = 0.3
W_TRANSIENT_MCP_LAUNCHER = 0.6
W_BARE_LOOPBACK = 0.1
W_BARE_ALL_INTERFACES = 0.15

DEFAULT_THRESHOLD = 0.5

# Cap emitted findings so a pathological host can't produce an unbounded list.
MAX_DISCOVERED = 500
ProcessKey = tuple[str | None, int]

# Unambiguous "official MCP server" argv marker (strong on its own).
_MCP_OFFICIAL_MARKERS = ("@modelcontextprotocol/",)

# Weaker MCP launcher markers (must combine).
_MCP_MARKERS = (
    "mcp-server-",
    "mcp_server",
    "modelcontextprotocol",
    "fastmcp",
    "-mcp-proxy",
    "mcp-proxy",
    "mcp-inspector",
)

# Electron/Chromium helper processes carry a --type=<role> flag; the client is
# the single main process without one, so helpers are not classified as clients.
_HELPER_FLAG_PREFIX = "--type="
_PACKAGE_RUNTIME_EXECUTABLES = frozenset(
    {"bun", "bun.exe", "deno", "deno.exe", "node", "node.exe"}
)
_TRANSIENT_LAUNCHERS = frozenset(
    {
        "bunx",
        "bunx.exe",
        "npx",
        "npx.cmd",
        "npx.exe",
        "uvx",
        "uvx.exe",
    }
)
_PNPM_LAUNCHERS = frozenset({"pnpm", "pnpm.cmd", "pnpm.exe"})
_NPX_SCRIPT_LAUNCHERS = frozenset({"npx-cli.js", "npx-cli.cjs"})
_PNPM_SCRIPT_LAUNCHERS = frozenset({"pnpm.cjs", "pnpm.js"})
_BUN_LAUNCHERS = frozenset({"bun", "bun.exe"})
_NPX_BOOLEAN_FLAGS = frozenset({"-y", "--yes", "--no"})
_NPX_PACKAGE_FLAGS = frozenset({"-p", "--package"})
_UVX_BOOLEAN_FLAGS = frozenset(
    {"-h", "--help", "-q", "--quiet", "-v", "--verbose", "--isolated", "--refresh"}
)
_UVX_VALUE_FLAGS = frozenset(
    {"-p", "--python", "-w", "--with", "--from", "--directory", "--project"}
)
_EXTENSION_HOST_MARKERS = ("extensionhost", "extension-host")


@dataclass(frozen=True)
class ResolvedAgentRuntimeSignature:
    """Runtime signature resolved once per scan (not once per candidate)."""

    framework_id: str
    argv_markers: tuple[str, ...]
    gateway_ports: tuple[int, ...]
    agent_fingerprint: str | None = None
    installation_path: str | None = None


@dataclass(frozen=True)
class AgentInstallationCorrelation:
    """One at-rest agent identity available for runtime correlation."""

    location: str
    fingerprint: str


def _resolve_runtime_signatures(
    signatures: tuple[AgentRuntimeSignature, ...],
) -> tuple[ResolvedAgentRuntimeSignature, ...]:
    resolved: list[ResolvedAgentRuntimeSignature] = []
    for signature in signatures:
        try:
            ports = tuple(
                port for port in signature.gateway_ports() if 0 < port <= 65535
            )
        except Exception:
            ports = ()
        try:
            agent_fingerprint = signature.agent_fingerprint()
        except Exception:
            agent_fingerprint = None
        try:
            installation_path = signature.installation_path()
        except Exception:
            installation_path = None
        resolved.append(
            ResolvedAgentRuntimeSignature(
                framework_id=signature.framework_id,
                argv_markers=tuple(marker.lower() for marker in signature.argv_markers),
                gateway_ports=ports,
                agent_fingerprint=agent_fingerprint,
                installation_path=installation_path,
            )
        )
    return tuple(resolved)


def _default_runtime_signatures() -> tuple[ResolvedAgentRuntimeSignature, ...]:
    return _resolve_runtime_signatures(runtime_signatures())


@dataclass
class ClassifierContext:
    """Correlation inputs derived from the filesystem channel + client registry.

    Configured ports and stdio commands are keyed by their host/WSL namespace.
    ``client_signatures`` maps a client name to executable substrings that
    identify its running process; ``client_package_signatures`` identifies npm
    package paths in full argv (derived from each client's
    ``install_probe.npm_packages``).
    """

    configured_ports: dict[
        tuple[str | None, int],
        tuple[str | None, Transport] | None,
    ] = field(default_factory=dict)
    configured_commands: dict[
        tuple[str | None, str, tuple[str, ...]],
        str | None,
    ] = field(default_factory=dict)
    client_signatures: dict[str, tuple[str, ...]] = field(default_factory=dict)
    client_package_signatures: dict[str, tuple[str, ...]] = field(default_factory=dict)
    ai_extension_signatures: tuple[str, ...] = ()
    client_override_flags: dict[str, tuple[SettingsOverrideFlagSpec, ...]] = field(
        default_factory=dict
    )
    agent_runtime_signatures: tuple[ResolvedAgentRuntimeSignature, ...] = field(
        default_factory=_default_runtime_signatures
    )
    agent_installations: dict[str, list[AgentInstallationCorrelation]] = field(
        default_factory=dict
    )
    detect_agents: bool = True


@lru_cache(maxsize=16)
def _agent_framework_markers(excluded_frameworks: tuple[str, ...]) -> tuple[str, ...]:
    """Framework-id markers to match against process argv (best-effort).

    Reuses the static agent-detection registry (``signatures.json``) so the two
    channels share one framework vocabulary. Short ids (< 5 chars) are dropped
    to avoid matching generic argv tokens. Frameworks with dedicated runtime
    signatures are excluded so one argv token fires exactly one signal.
    """
    markers: set[str] = set()
    try:
        registry = load_registry()
    except Exception:  # registry is best-effort here
        return ()
    for framework_id in registry.framework_ids:
        token = framework_id.strip().lower()
        if len(token) >= 5 and token not in excluded_frameworks:
            markers.add(token)
    return tuple(sorted(markers))


def _normalize_command_key(
    command: str, args: list[str] | None
) -> tuple[str, tuple[str, ...]]:
    """Normalize a stdio command + args into a match key (basename + args)."""
    base = os.path.basename(command).lower()
    arg_tuple = tuple(a for a in (args or []))
    return base, arg_tuple


def _wsl_namespace(value: str | None) -> str | None:
    return value.casefold() if value is not None else None


def build_context(
    configurations,
    clients,
    agents=(),
    *,
    detect_agents: bool = True,
) -> ClassifierContext:
    """Build a :class:`ClassifierContext` from scan configs + client registry.

    ``configurations`` is the scan's list of ``MCPClientConfig`` (each with
    ``.servers``); ``clients`` is the ``MCPClientDefinition`` registry. Kept
    duck-typed (attribute access only) so the classifier core stays decoupled
    from those concrete types and unit-testable with plain fixtures.
    """
    context = ClassifierContext(
        agent_runtime_signatures=(
            _default_runtime_signatures() if detect_agents else ()
        ),
        detect_agents=detect_agents,
    )
    for config in configurations:
        namespace = _wsl_namespace(getattr(config, "wsl_distro", None))
        for server in getattr(config, "servers", []):
            config_hash = getattr(server, "config_hash", "") or None
            url = getattr(server, "url", None)
            command = getattr(server, "command", None)
            server_type = (getattr(server, "type", "") or "").lower()
            if url:
                port = _port_from_url(url)
                if port is not None:
                    transport: Transport = "sse" if server_type == "sse" else "http"
                    key = (namespace, port)
                    existing = context.configured_ports.get(key)
                    if key not in context.configured_ports:
                        context.configured_ports[key] = (config_hash, transport)
                    elif existing is None or existing[0] != config_hash:
                        context.configured_ports[key] = None
            if command and config_hash:
                command_key = _normalize_command_key(
                    command,
                    getattr(server, "args", None),
                )
                key = (namespace, *command_key)
                existing_hash = context.configured_commands.get(key)
                if key not in context.configured_commands:
                    context.configured_commands[key] = config_hash
                elif existing_hash != config_hash:
                    context.configured_commands[key] = None

    ai_extension_signatures: set[str] = set()
    for client in clients:
        signatures = getattr(client, "process_signatures", None)
        if signatures:
            context.client_signatures[client.name] = tuple(
                str(signature).lower() for signature in signatures
            )
        install_probe = getattr(client, "install_probe", None)
        ai_extension_signatures.update(
            str(extension_id).lower()
            for extension_id in (
                getattr(install_probe, "vscode_extension_ids", None) or ()
            )
            if extension_id
        )
        npm_packages = getattr(install_probe, "npm_packages", None) or ()
        package_names = tuple(
            str(package.name).lower()
            for package in npm_packages
            if getattr(package, "name", None)
        )
        if package_names:
            context.client_package_signatures[client.name] = package_names
        override_flags = getattr(client, "settings_override_flags", None)
        if override_flags:
            context.client_override_flags[client.name] = tuple(override_flags)
    context.ai_extension_signatures = tuple(sorted(ai_extension_signatures))

    for agent in agents:
        framework_id = getattr(agent, "framework_id", None)
        fingerprint = getattr(agent, "agent_fingerprint", None)
        location = getattr(agent, "location", None)
        if framework_id and fingerprint and location:
            context.agent_installations.setdefault(framework_id, []).append(
                AgentInstallationCorrelation(
                    location=str(location),
                    fingerprint=str(fingerprint),
                )
            )
    return context


def _port_from_url(url: str) -> int | None:
    try:
        return urlsplit(url).port
    except (ValueError, TypeError):
        return None


def _argv_text(candidate: ProcessCandidate) -> str:
    """Lowercased haystack for substring markers (exe + full argv)."""
    parts = list(candidate.argv)
    if candidate.exe:
        parts.append(candidate.exe)
    return " ".join(parts).lower()


def _is_helper_process(candidate: ProcessCandidate) -> bool:
    return any(arg.startswith(_HELPER_FLAG_PREFIX) for arg in candidate.argv)


def _matched_client(
    candidate: ProcessCandidate,
    client_signatures: dict[str, tuple[str, ...]],
    client_package_signatures: dict[str, tuple[str, ...]],
) -> str | None:
    """Client name whose executable signature matches this candidate, if any."""
    candidate_paths = [candidate.exe or ""]
    if candidate.argv:
        candidate_paths.append(candidate.argv[0])

    launcher = next((path for path in candidate_paths if path), "")
    launcher_name = launcher.replace("\\", "/").rsplit("/", 1)[-1].lower()
    is_script_launcher = (
        launcher_name.startswith("python")
        or launcher_name in _PACKAGE_RUNTIME_EXECUTABLES
    )
    signature_paths = candidate_paths
    if is_script_launcher and len(candidate.argv) > 1:
        signature_paths = [*candidate_paths, candidate.argv[1]]

    haystacks = tuple(path.lower() for path in signature_paths if path)
    if not haystacks:
        return None
    for name, signatures in client_signatures.items():
        if any(sig in haystack for sig in signatures for haystack in haystacks):
            return name
    normalized_candidate_paths = [
        normalized
        for value in candidate_paths
        if "://" not in (normalized := value.lower().replace("\\", "/"))
    ]
    runtime_entrypoint = any(
        value.rsplit("/", 1)[-1] in _PACKAGE_RUNTIME_EXECUTABLES
        for value in normalized_candidate_paths
    )
    argv_paths = list(normalized_candidate_paths)
    if runtime_entrypoint:
        argv_paths.extend(
            normalized
            for value in candidate.argv
            if "://" not in (normalized := value.lower().replace("\\", "/"))
        )
    for name, packages in client_package_signatures.items():
        for package in packages:
            marker = f"node_modules/{package}/"
            if any(
                value.startswith(marker) or f"/{marker}" in value
                for value in argv_paths
            ):
                return name
    return None


def _process_key(candidate: ProcessCandidate, *, pid: int | None = None) -> ProcessKey:
    namespace = (
        candidate.wsl_distro.casefold() if candidate.wsl_distro is not None else None
    )
    return namespace, candidate.pid if pid is None else pid


def _client_pid_map(
    candidates: list[ProcessCandidate],
    client_signatures: dict[str, tuple[str, ...]],
    client_package_signatures: dict[str, tuple[str, ...]],
) -> dict[ProcessKey, str | None]:
    """Map namespace + pid to main client processes (helpers excluded)."""
    mapping: dict[ProcessKey, str | None] = {}
    for candidate in candidates:
        if _is_helper_process(candidate):
            continue
        name = _matched_client(
            candidate,
            client_signatures,
            client_package_signatures,
        )
        if name is not None:
            mapping[_process_key(candidate)] = name
    return mapping


def _launcher_name(value: str | None) -> str:
    return (value or "").replace("\\", "/").rsplit("/", 1)[-1].lower()


def _npx_package_operand(arguments: list[str]) -> str | None:
    explicit_package: str | None = None
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument.startswith("--package="):
            explicit_package = argument.partition("=")[2] or None
        elif argument in _NPX_PACKAGE_FLAGS:
            index += 1
            if index >= len(arguments):
                return None
            explicit_package = arguments[index]
        elif argument in {"-c", "--call"} or argument.startswith("--call="):
            return None
        elif (
            argument in _NPX_BOOLEAN_FLAGS
            or argument.startswith("--yes=")
            or argument.startswith("--no-")
        ):
            pass
        elif argument == "--":
            index += 1
            return explicit_package or (
                arguments[index] if index < len(arguments) else None
            )
        elif argument.startswith("-"):
            return None
        else:
            return explicit_package or argument
        index += 1
    return explicit_package


def _uvx_package_operand(arguments: list[str]) -> str | None:
    explicit_package: str | None = None
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        flag, separator, value = argument.partition("=")
        if separator and flag in _UVX_VALUE_FLAGS:
            if not value:
                return None
            if flag == "--from":
                explicit_package = value
        elif argument in _UVX_VALUE_FLAGS:
            index += 1
            if index >= len(arguments):
                return None
            if argument == "--from":
                explicit_package = arguments[index]
        elif argument in _UVX_BOOLEAN_FLAGS:
            pass
        elif argument == "--":
            index += 1
            return explicit_package or (
                arguments[index] if index < len(arguments) else None
            )
        elif argument.startswith("-"):
            return None
        else:
            return explicit_package or argument
        index += 1
    return explicit_package


def _simple_package_operand(
    arguments: list[str],
    *,
    boolean_flags: frozenset[str] = frozenset(),
) -> str | None:
    operand: str | None = None
    for index, argument in enumerate(arguments):
        if argument in boolean_flags:
            continue
        if argument == "--":
            operand = arguments[index + 1] if index + 1 < len(arguments) else None
            break
        if argument.startswith("-"):
            break
        operand = argument
        break
    return operand


def _transient_launcher(
    candidate: ProcessCandidate,
) -> tuple[str, list[str]] | None:
    executable_name = _launcher_name(candidate.exe)
    argv_names = [_launcher_name(value) for value in candidate.argv]
    argv_launcher = argv_names[0] if argv_names else ""
    launcher: tuple[str, list[str]] | None = None
    if argv_launcher in _TRANSIENT_LAUNCHERS:
        launcher = (
            argv_launcher.removesuffix(".exe").removesuffix(".cmd"),
            candidate.argv[1:],
        )
    elif argv_launcher in _PNPM_LAUNCHERS and len(candidate.argv) > 1:
        if candidate.argv[1].casefold() == "dlx":
            launcher = ("pnpm", candidate.argv[2:])
    elif argv_launcher in _BUN_LAUNCHERS and len(candidate.argv) > 1:
        if candidate.argv[1].casefold() == "x":
            launcher = ("bunx", candidate.argv[2:])
    elif (
        executable_name in _PACKAGE_RUNTIME_EXECUTABLES
        and len(argv_names) > 1
        and argv_names[1] in _NPX_SCRIPT_LAUNCHERS
    ):
        launcher = ("npx", candidate.argv[2:])
    elif (
        executable_name in _PACKAGE_RUNTIME_EXECUTABLES
        and len(argv_names) > 2
        and argv_names[1] in _PNPM_SCRIPT_LAUNCHERS
        and candidate.argv[2].casefold() == "dlx"
    ):
        launcher = ("pnpm", candidate.argv[3:])
    return launcher


def _is_mcp_package_operand(value: str | None) -> bool:
    if value is None:
        return False
    normalized = value.strip().casefold()
    if normalized.startswith("@"):
        version_separator = normalized.find("@", 1)
        if version_separator >= 0:
            normalized = normalized[:version_separator]
    else:
        normalized = normalized.partition("@")[0]
    normalized = normalized.partition("==")[0].partition("[")[0].replace("_", "-")
    return normalized.startswith(
        ("@modelcontextprotocol/", "mcp-server-")
    ) or normalized in {"fastmcp", "mcp-inspector", "mcp-proxy"}


def _is_transient_mcp_launcher(candidate: ProcessCandidate) -> bool:
    launcher = _transient_launcher(candidate)
    operand: str | None = None
    if launcher is not None:
        launcher_name, arguments = launcher
        if launcher_name == "npx":
            operand = _npx_package_operand(arguments)
        elif launcher_name == "uvx":
            operand = _uvx_package_operand(arguments)
        elif launcher_name == "pnpm":
            operand = _simple_package_operand(arguments)
        elif launcher_name == "bunx":
            operand = _simple_package_operand(
                arguments,
                boolean_flags=frozenset({"--bun"}),
            )
    return _is_mcp_package_operand(operand)


def _children_by_parent(
    candidates: list[ProcessCandidate],
) -> dict[ProcessKey, list[ProcessCandidate]]:
    children: dict[ProcessKey, list[ProcessCandidate]] = {}
    for candidate in candidates:
        if candidate.ppid is not None:
            children.setdefault(
                _process_key(candidate, pid=candidate.ppid),
                [],
            ).append(candidate)
    return children


def _has_ai_child_tree_signal(
    candidate: ProcessCandidate,
    ai_extension_signatures: tuple[str, ...],
) -> bool:
    haystack = _argv_text(candidate)
    has_ai_extension = any(marker in haystack for marker in ai_extension_signatures)
    return _is_extension_host(candidate) and has_ai_extension


def _is_extension_host(candidate: ProcessCandidate) -> bool:
    haystack = _argv_text(candidate)
    return any(marker in haystack for marker in _EXTENSION_HOST_MARKERS)


@dataclass
class _ElectronSubtreeSignal:
    has_extension_host: bool = False
    has_ai_evidence: bool = False
    matched_client: str | None = None


def _electron_ai_client_pids(
    candidates: list[ProcessCandidate],
    context: ClassifierContext,
) -> dict[ProcessKey, str | None]:
    """Infer renamed Electron clients from helper + AI child-tree topology."""
    children_by_parent = _children_by_parent(candidates)
    ai_evidence_by_pid = {
        _process_key(candidate): _has_ai_child_tree_signal(
            candidate,
            context.ai_extension_signatures,
        )
        for candidate in candidates
    }
    matched_client_by_pid = {
        _process_key(candidate): _matched_client(
            candidate,
            context.client_signatures,
            context.client_package_signatures,
        )
        for candidate in candidates
    }
    candidate_by_pid = {_process_key(candidate): candidate for candidate in candidates}
    subtree_by_pid = {
        _process_key(candidate): _ElectronSubtreeSignal() for candidate in candidates
    }
    remaining_children = {
        _process_key(candidate): sum(
            _process_key(child) in candidate_by_pid
            for child in children_by_parent.get(_process_key(candidate), ())
        )
        for candidate in candidates
    }
    leaves = deque(
        pid for pid, child_count in remaining_children.items() if child_count == 0
    )
    while leaves:
        pid = leaves.popleft()
        candidate = candidate_by_pid[pid]
        parent_pid = (
            _process_key(candidate, pid=candidate.ppid)
            if candidate.ppid is not None
            else None
        )
        if parent_pid is None or parent_pid not in candidate_by_pid:
            continue
        child_subtree = subtree_by_pid[pid]
        parent_subtree = subtree_by_pid[parent_pid]
        child_client = matched_client_by_pid.get(pid)
        parent_subtree.has_extension_host = (
            parent_subtree.has_extension_host
            or _is_extension_host(candidate)
            or child_subtree.has_extension_host
        )
        parent_subtree.has_ai_evidence = (
            parent_subtree.has_ai_evidence
            or ai_evidence_by_pid.get(pid, False)
            or child_client is not None
            or child_subtree.has_ai_evidence
        )
        parent_subtree.matched_client = (
            parent_subtree.matched_client
            or child_client
            or child_subtree.matched_client
        )
        remaining_children[parent_pid] -= 1
        if remaining_children[parent_pid] == 0:
            leaves.append(parent_pid)

    mapping: dict[ProcessKey, str | None] = {}
    for candidate in candidates:
        candidate_key = _process_key(candidate)
        direct_children = children_by_parent.get(candidate_key, ())
        if _is_helper_process(candidate) or not any(
            _is_helper_process(child) for child in direct_children
        ):
            continue
        signal = subtree_by_pid[candidate_key]
        if not signal.has_extension_host or not signal.has_ai_evidence:
            continue
        mapping[candidate_key] = signal.matched_client
    return mapping


@dataclass
class _Score:
    total: float = 0.0
    signals: list[str] = field(default_factory=list)
    kind_votes: dict[ProcessKind, float] = field(default_factory=dict)
    config_hash: str | None = None
    transport: Transport | None = None
    matched_client: str | None = None
    via_client: bool = False
    agent_framework_votes: dict[str, float] = field(default_factory=dict)
    settings_overrides: list[SettingsOverrideMatch] = field(default_factory=list)

    def add(
        self,
        weight: float,
        signal: str,
        *,
        kind: ProcessKind | None = None,
    ) -> None:
        self.total += weight
        self.signals.append(signal)
        if kind is not None:
            self.kind_votes[kind] = self.kind_votes.get(kind, 0.0) + weight

    def add_agent(self, weight: float, signal: str, framework_id: str) -> None:
        self.add(weight, signal, kind="agent")
        self.agent_framework_votes[framework_id] = (
            self.agent_framework_votes.get(framework_id, 0.0) + weight
        )


def _resolve_kind(votes: dict[ProcessKind, float]) -> ProcessKind:
    """Pick the winning kind by summed weight, tie-broken client>mcp_server>agent."""
    if not votes:
        return "mcp_server"
    priority = {"client": 3, "mcp_server": 2, "agent": 1}
    return max(votes.items(), key=lambda kv: (kv[1], priority[kv[0]]))[0]


def _resolve_agent_framework(votes: dict[str, float]) -> str | None:
    if not votes:
        return None
    return sorted(votes, key=lambda framework: (-votes[framework], framework))[0]


def _normalize_path_for_match(value: str) -> str:
    return os.path.normcase(os.path.normpath(value)).replace("\\", "/").rstrip("/")


def _correlated_agent_installation(
    candidate: ProcessCandidate,
    framework_id: str | None,
    context: ClassifierContext,
) -> AgentInstallationCorrelation | None:
    """Match a runtime agent to one at-rest installation on the same scan."""
    if framework_id is None:
        return None
    correlations = context.agent_installations.get(framework_id, [])
    if len(correlations) == 1:
        return correlations[0]
    if candidate.cwd is None:
        return None

    cwd = _normalize_path_for_match(candidate.cwd)
    path_matches: list[tuple[int, AgentInstallationCorrelation]] = []
    for item in correlations:
        root = _normalize_path_for_match(item.location)
        if cwd == root or cwd.startswith(f"{root}/"):
            path_matches.append((len(root), item))
    if not path_matches:
        return None

    longest = max(length for length, _item in path_matches)
    best = {
        (_normalize_path_for_match(item.location), item.fingerprint): item
        for length, item in path_matches
        if length == longest
    }
    return next(iter(best.values())) if len(best) == 1 else None


def _sole_agent_fingerprint(
    framework_id: str | None,
    context: ClassifierContext,
) -> str | None:
    if framework_id is None:
        return None
    fingerprints = {
        item.fingerprint for item in context.agent_installations.get(framework_id, [])
    }
    return next(iter(fingerprints)) if len(fingerprints) == 1 else None


def _runtime_signature_identity(
    framework_id: str | None,
    context: ClassifierContext,
) -> tuple[str | None, str | None]:
    if framework_id is None:
        return None, None
    if context.agent_installations.get(framework_id):
        return None, None
    for signature in context.agent_runtime_signatures:
        if signature.framework_id == framework_id:
            return signature.agent_fingerprint, signature.installation_path
    return None, None


def _is_docker_agent_probe(
    candidate: ProcessCandidate,
    framework_id: str | None,
) -> bool:
    return bool(
        framework_id
        and "docker" in candidate.agent_runtime_signals.get(framework_id, ())
    )


def _resolve_transport(
    score: _Score, candidate: ProcessCandidate, kind: ProcessKind
) -> Transport | None:
    """Decide the transport once the kind is known."""
    if score.transport is not None:
        return score.transport
    if kind != "client" and candidate.listening_ports:
        # A listener we could not correlate to a configured URL; default to http
        # (sse is indistinguishable without an active probe, which v1 defers).
        return "http"
    if kind == "mcp_server":
        return "stdio"
    return None


def _score_candidate(
    candidate: ProcessCandidate,
    context: ClassifierContext,
    client_pids: dict[ProcessKey, str | None],
    topology_client_pids: dict[ProcessKey, str | None],
    framework_markers: tuple[str, ...],
) -> _Score:
    score = _Score()
    haystack = _argv_text(candidate)
    candidate_key = _process_key(candidate)

    # Strong: this process IS a known client executable (main process only).
    if not _is_helper_process(candidate):
        client_name = _matched_client(
            candidate,
            context.client_signatures,
            context.client_package_signatures,
        )
        if client_name is not None:
            score.add(W_CLIENT_SIGNATURE, f"client:{client_name}", kind="client")
            score.matched_client = client_name
    if candidate_key in topology_client_pids:
        score.add(
            W_ELECTRON_MAIN_HELPERS,
            "electron_main_helpers",
            kind="client",
        )
        score.add(W_AI_CHILD_TREE, "ai_child_tree", kind="client")
        score.matched_client = (
            score.matched_client or topology_client_pids[candidate_key]
        )
    if score.matched_client is not None:
        score.settings_overrides = extract_settings_overrides(
            candidate.argv,
            context.client_override_flags.get(score.matched_client, ()),
        )
        for flag in dict.fromkeys(match.flag for match in score.settings_overrides):
            score.add(0.0, f"settings_override:{flag}")

    # Strong: argv matches a configured stdio server's command.
    if candidate.argv:
        command_key = _normalize_command_key(candidate.argv[0], candidate.argv[1:])
        key = (_wsl_namespace(candidate.wsl_distro), *command_key)
        config_hash = context.configured_commands.get(key)
        if config_hash is not None:
            score.add(W_CONFIG_COMMAND_MATCH, "config_command_match", kind="mcp_server")
            score.config_hash = config_hash
            score.transport = "stdio"

    # Strong: a listening port matches a configured MCP server URL.
    for port in candidate.listening_ports:
        configured = context.configured_ports.get(
            (_wsl_namespace(candidate.wsl_distro), port)
        )
        if configured is not None:
            config_hash, transport = configured
            score.add(
                W_CONFIG_PORT_MATCH, f"config_port_match:{port}", kind="mcp_server"
            )
            score.config_hash = score.config_hash or config_hash
            score.transport = transport
            break

    # Strong-ish: unambiguous official MCP server marker in argv.
    if any(marker in haystack for marker in _MCP_OFFICIAL_MARKERS):
        score.add(W_MCP_OFFICIAL, "mcp_official", kind="mcp_server")

    # Medium: declarative framework-specific argv / gateway-port signals.
    for signature in context.agent_runtime_signatures:
        framework_id = signature.framework_id
        if any(marker in haystack for marker in signature.argv_markers):
            score.add_agent(
                W_AGENT_RUNTIME,
                f"agent_runtime:{framework_id}:argv",
                framework_id,
            )
        for port in candidate.listening_ports:
            if port in signature.gateway_ports:
                score.add_agent(
                    W_AGENT_RUNTIME,
                    f"agent_runtime:{framework_id}:port:{port}",
                    framework_id,
                )
                break
        for probe_signal in candidate.agent_runtime_signals.get(framework_id, ()):
            score.add_agent(
                W_AGENT_PROBE,
                f"agent_runtime:{framework_id}:{probe_signal}",
                framework_id,
            )

    # Medium: agent-framework id markers (word-boundary matched).
    matched_framework = _first_framework_marker(haystack, framework_markers)
    if matched_framework is not None:
        score.add_agent(
            W_AGENT_FRAMEWORK,
            f"agent_framework:{matched_framework}",
            matched_framework,
        )

    # Medium: weaker MCP launcher markers.
    if any(marker in haystack for marker in _MCP_MARKERS):
        score.add(W_MCP_MARKER, "mcp_marker", kind="mcp_server")
    if _is_transient_mcp_launcher(candidate):
        score.add(
            W_TRANSIENT_MCP_LAUNCHER,
            "transient_mcp_launcher",
            kind="mcp_server",
        )

    # Weak: parent is a detected client (clients spawn many non-MCP children, so
    # this only boosts -- it must combine with an argv/config signal to pass).
    parent_key = (
        _process_key(candidate, pid=candidate.ppid)
        if candidate.ppid is not None
        else None
    )
    if parent_key is not None and parent_key in client_pids:
        parent_client = client_pids[parent_key]
        parent_label = parent_client or "electron_ai"
        score.add(
            W_PARENT_CLIENT,
            f"parent_client:{parent_label}",
            kind="mcp_server",
        )
        score.via_client = True
        if parent_client is not None:
            score.matched_client = score.matched_client or parent_client

    # Weak: a bare listener (loopback weaker than all-interfaces).
    if candidate.listening_ports and "config_port_match" not in " ".join(score.signals):
        if candidate.bind_scope == "loopback":
            score.add(W_BARE_LOOPBACK, "listening:loopback")
        elif candidate.bind_scope == "all_interfaces":
            score.add(W_BARE_ALL_INTERFACES, "listening:all_interfaces")

    return score


def _first_framework_marker(
    haystack: str, framework_markers: tuple[str, ...]
) -> str | None:
    """Return the first framework marker present as a bounded token in haystack."""
    for marker in framework_markers:
        idx = haystack.find(marker)
        while idx != -1:
            before = haystack[idx - 1] if idx > 0 else ""
            after_idx = idx + len(marker)
            after = haystack[after_idx] if after_idx < len(haystack) else ""
            if not _is_word_char(before) and not _is_word_char(after):
                return marker
            idx = haystack.find(marker, idx + 1)
    return None


def _is_word_char(ch: str) -> bool:
    return ch.isalnum() or ch == "_"


def _discovery_source(candidate: ProcessCandidate, via_client: bool):
    if via_client:
        return "client_child"
    return candidate.discovery_source


def classify_processes(
    candidates: list[ProcessCandidate],
    context: ClassifierContext,
    *,
    usernames=(),
    threshold: float = DEFAULT_THRESHOLD,
) -> list[DiscoveredProcess]:
    """Score candidates and return only the redacted process sightings."""

    return classify_processes_with_overrides(
        candidates,
        context,
        usernames=usernames,
        threshold=threshold,
    ).processes


def classify_processes_with_overrides(
    candidates: list[ProcessCandidate],
    context: ClassifierContext,
    *,
    usernames: Sequence[str] = (),
    threshold: float = DEFAULT_THRESHOLD,
) -> ProcessDiscoveryResult:
    """Score every candidate; return the redacted AI-related ones.

    Candidates below ``threshold`` are dropped (not AI-related, or too weak a
    signal to submit). Surviving candidates are redacted (argv scrubbed, cwd
    reduced to a basename) and sorted by descending confidence. Raw override
    config refs are returned separately for local-only PHASE 12 parsing.
    """
    signature_client_pids = _client_pid_map(
        candidates,
        context.client_signatures,
        context.client_package_signatures,
    )
    topology_client_pids = _electron_ai_client_pids(candidates, context)
    client_pids = {**topology_client_pids, **signature_client_pids}
    excluded_frameworks = tuple(
        sorted(
            {signature.framework_id for signature in context.agent_runtime_signatures}
        )
    )
    framework_markers = (
        _agent_framework_markers(excluded_frameworks) if context.detect_agents else ()
    )

    discovered: list[tuple[DiscoveredProcess, list[OverrideConfigRef]]] = []
    for candidate in candidates:
        score = _score_candidate(
            candidate,
            context,
            client_pids,
            topology_client_pids,
            framework_markers,
        )
        confidence = min(1.0, score.total)
        if confidence < threshold:
            continue
        kind = _resolve_kind(score.kind_votes)
        transport = _resolve_transport(score, candidate, kind)
        agent_framework_id = (
            _resolve_agent_framework(score.agent_framework_votes)
            if kind == "agent"
            else None
        )
        docker_agent_probe = _is_docker_agent_probe(
            candidate,
            agent_framework_id,
        )
        agent_installation = (
            None
            if docker_agent_probe
            else _correlated_agent_installation(
                candidate,
                agent_framework_id,
                context,
            )
        )
        runtime_fingerprint, runtime_root_path = _runtime_signature_identity(
            agent_framework_id,
            context,
        )
        if docker_agent_probe and agent_framework_id is not None:
            runtime_root_path = f"runtime:docker:{agent_framework_id}"
        agent_fingerprint = (
            agent_installation.fingerprint
            if agent_installation is not None
            else (
                _sole_agent_fingerprint(agent_framework_id, context)
                or runtime_fingerprint
            )
        )
        agent_root_path = sanitize_path(
            (
                agent_installation.location
                if agent_installation is not None
                else runtime_root_path
            ),
            usernames=usernames,
        )
        process = DiscoveredProcess(
            pid=candidate.pid if candidate.pid > 0 else None,
            ppid=candidate.ppid,
            kind=kind,
            discovery_source=_discovery_source(candidate, score.via_client),
            matched_client=score.matched_client,
            exe=redact_exe(candidate.exe, usernames=usernames),
            argv_redacted=redact_argv(candidate.argv, usernames=usernames),
            command_hash=command_hash(candidate.argv),
            config_hash=score.config_hash,
            agent_framework_id=agent_framework_id,
            agent_fingerprint=agent_fingerprint,
            agent_root_path=agent_root_path,
            listening_ports=list(candidate.listening_ports),
            bind_scope=candidate.bind_scope,
            transport=transport,
            ai_signals=score.signals,
            confidence=confidence,
            user=candidate.user,
            started_at=candidate.started_at,
            cwd_project=redact_cwd_project(candidate.cwd, usernames=usernames),
            settings_overrides=sanitized_settings_overrides(
                score.settings_overrides,
                usernames=usernames,
            ),
            wsl_distro=candidate.wsl_distro,
        )
        discovered.append(
            (
                process,
                override_config_refs(
                    candidate,
                    score.matched_client,
                    score.settings_overrides,
                ),
            )
        )

    discovered.sort(key=lambda item: item[0].confidence, reverse=True)
    if len(discovered) > MAX_DISCOVERED:
        logger.warning(
            "process_discovery_truncated",
            detected=len(discovered),
            kept=MAX_DISCOVERED,
        )
        discovered = discovered[:MAX_DISCOVERED]
    return ProcessDiscoveryResult(
        processes=[process for process, _refs in discovered],
        override_config_refs=[ref for _process, refs in discovered for ref in refs],
    )
