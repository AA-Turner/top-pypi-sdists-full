import asyncio
import os
import time
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from dreadnode.app.api.models import (
    CapabilityAgentInfo,
    CapabilityInfo,
    ComponentStatusInfo,
    FlagInfo,
    RuntimeInfoResponse,
)
from dreadnode.app.paths import mcp_log_path
from dreadnode.core.types.common import UNSET, Unset

if t.TYPE_CHECKING:
    from dreadnode.app.server.runtime_events import EventBus
    from dreadnode.app.server.worker_manager import WorkerLifecycleManager
    from dreadnode.capabilities.capability import Capability
    from dreadnode.capabilities.types import AgentDef


def _tool_name(tool: t.Any) -> str:
    """Get the name of a tool object."""
    return getattr(tool, "name", "")


@dataclass(slots=True)
class CapabilityRegistry:
    """Registry of capabilities available to the local server."""

    capabilities: dict[str, "Capability"] = field(default_factory=dict)
    disabled_local: dict[str, "Capability"] = field(default_factory=dict)
    default_capability_name: str | None = None
    mcp_manager: "MCPLifecycleManager | None" = None
    worker_manager: "WorkerLifecycleManager | None" = None
    runtime_bindings: list[dict[str, t.Any]] = field(default_factory=list)
    load_failures: list[dict[str, t.Any]] = field(default_factory=list)
    local_capability_records: dict[str, dict[str, t.Any]] = field(default_factory=dict)
    update_info: dict[str, str] = field(default_factory=dict)
    _skills_cache: list[t.Any] | None = field(default=None, init=False, repr=False)

    def get(self, name: str | None) -> "Capability | None":
        if not name:
            return None
        return self.capabilities.get(name)

    def default(self) -> "Capability | None":
        if self.default_capability_name:
            return self.capabilities.get(self.default_capability_name)
        if self.capabilities:
            return next(iter(self.capabilities.values()))
        return None

    def resolve(
        self,
        *,
        capability_name: str | None = None,
        agent_name: str | None = None,
    ) -> tuple[str | None, "Capability | None", "AgentDef | None"]:
        """Resolve a capability + agent pair for a new session."""
        if capability_name:
            capability = self.get(capability_name)
            if capability is None:
                raise ValueError(f"Unknown capability: {capability_name}")

            if agent_name:
                agent_def = next(
                    (agent for agent in capability.agents if agent.name == agent_name), None
                )
                if agent_def is None:
                    raise ValueError(
                        f"Agent '{agent_name}' is not defined in capability '{capability_name}'"
                    )
                return capability_name, capability, agent_def

            agent_def = capability.agents[0] if capability.agents else None
            return capability_name, capability, agent_def

        if agent_name:
            matches = [
                (loaded_capability_name, capability, agent_def)
                for loaded_capability_name, capability in self.capabilities.items()
                for agent_def in capability.agents
                if agent_def.name == agent_name
            ]
            if len(matches) == 1:
                return matches[0]
            if len(matches) > 1:
                matched_capabilities = ", ".join(
                    sorted(capability_name for capability_name, _, _ in matches)
                )
                raise ValueError(
                    f"Agent '{agent_name}' is defined in multiple capabilities: "
                    f"{matched_capabilities}. Choose a capability explicitly."
                )
            logger.warning(
                "Requested agent '{}' was not found in loaded capabilities; "
                "falling back to the default capability",
                agent_name,
            )

        capability = self.default()
        if capability is None:
            return None, None, None
        capability_name = self.default_capability_name
        if capability_name is None and self.capabilities:
            capability_name = next(iter(self.capabilities))
        agent_def = capability.agents[0] if capability.agents else None
        return capability_name, capability, agent_def

    def all_tools(self) -> list[t.Any]:
        """All tools from all capabilities + MCP servers, deduped by name."""
        seen: set[str] = set()
        tools: list[t.Any] = []
        for cap in self.capabilities.values():
            for tool in cap.tools:
                name = _tool_name(tool)
                if name and name not in seen:
                    tools.append(tool)
                    seen.add(name)
                elif name in seen:
                    logger.debug(
                        "Tool '{}' already registered, skipping duplicate",
                        name,
                    )
        if self.mcp_manager:
            for tool in self.mcp_manager.all_tools():
                name = _tool_name(tool)
                if name and name not in seen:
                    tools.append(tool)
                    seen.add(name)
                elif name in seen:
                    logger.debug("Tool '{}' already registered (MCP), skipping", name)
        return tools

    def all_hooks(self) -> list[t.Any]:
        """All hooks contributed by loaded capabilities, in registration order.

        Hooks are session-global middleware — unlike tools, they aren't
        filtered by per-agent rules. A capability that ships a
        ``@hook(GenerationStep)`` participates in every turn as long as
        the capability is loaded.
        """
        hooks: list[t.Any] = []
        for cap in self.capabilities.values():
            cap_hooks = getattr(cap, "hooks", None) or []
            hooks.extend(cap_hooks)
        return hooks

    def register_capability_policies(self) -> list[str]:
        """Register all policy classes contributed by loaded capabilities.

        Walks every capability's ``.policies`` list and inserts each
        class into the global :data:`dreadnode.policies._REGISTRY` via
        :func:`~dreadnode.policies.register_policy`. Idempotent:
        re-registering a capability's policies is a no-op unless the
        class object itself changed.

        Returns the list of registered policy names for telemetry
        and CLI ``/policies`` listing. Called at end of
        capability-load so policies become available before the
        first session is created.
        """
        from dreadnode.policies import register_policy

        registered: list[str] = []
        for cap in self.capabilities.values():
            cap_policies = getattr(cap, "policies", None) or []
            for policy_cls in cap_policies:
                try:
                    register_policy(policy_cls)
                    name = getattr(policy_cls, "name", None)
                    if isinstance(name, str) and name:
                        registered.append(name)
                except ValueError as exc:
                    logger.warning(
                        "Capability '{}' policy {} rejected: {}",
                        getattr(cap, "name", "?"),
                        getattr(policy_cls, "__name__", repr(policy_cls)),
                        exc,
                    )
        return registered

    def all_skills(self) -> list[t.Any]:
        """Discover skills from all capabilities and stamp structural identity.

        Each skill is stamped with its `source` (`python` for capability
        skills, `bundled` for the bundled capability) and `namespace` tuple
        (`(cap_name,)` for capability skills, `()` for bundled). Two
        capabilities shipping the same bare name both survive as distinct
        qualified identifiers — there is no shadow/override behavior
        (CAP-IDENT-012, CAP-IDENT-016).
        """
        if self._skills_cache is not None:
            return self._skills_cache

        from dataclasses import replace

        from dreadnode.agents.skills import discover_skills

        skills: list[t.Any] = []
        for cap_name, cap in self.capabilities.items():
            bundled = bool(getattr(cap, "bundled", False))
            if bundled:
                source: t.Literal["bundled", "python"] = "bundled"
                namespace: tuple[str, ...] = ()
            else:
                source = "python"
                namespace = (cap_name,)
            for skills_path in cap.skills_paths or []:
                for skill in discover_skills(skills_path):
                    skills.append(replace(skill, source=source, namespace=namespace))

        self._skills_cache = skills
        return self._skills_cache

    def find_agent(self, agent_name: str) -> tuple[str, t.Any, "AgentDef"] | None:
        """Find an agent by name across all capabilities."""
        for cap_name, cap in self.capabilities.items():
            for agent_def in cap.agents:
                if agent_def.name == agent_name:
                    return (cap_name, cap, agent_def)
        return None

    def to_runtime_info(self, *, working_dir: Path) -> RuntimeInfoResponse:
        """Serialize registry state for CLI/runtime introspection."""
        from dreadnode.capabilities.sync import bare_capability_name

        def _provenance_for(
            *, bare_name: str, source: str
        ) -> t.Literal["local", "org", "public"] | None:
            if source == "runtime":
                return None
            record = self.local_capability_records.get(bare_name, {})
            persisted = record.get("source")
            if persisted == "org":
                return "org"
            if persisted == "public":
                return "public"
            return "local"

        def _display_identity(
            *,
            bare_name: str,
            source: str,
            binding: dict[str, t.Any] | None = None,
        ) -> tuple[str, str | None]:
            canonical_name = None
            if binding is not None:
                binding_name = binding.get("capability_name")
                if isinstance(binding_name, str) and binding_name.strip():
                    canonical_name = binding_name
            if canonical_name is not None:
                return canonical_name, canonical_name
            if source in {"local", "package"}:
                record = self.local_capability_records.get(bare_name, {})
                artifact_identity = record.get("artifact_identity")
                if isinstance(artifact_identity, str) and artifact_identity.strip():
                    return bare_name, artifact_identity
                return bare_name, None
            return f"{source}/{bare_name}", None

        def _capability_metadata(
            capability: t.Any,
        ) -> tuple[str | None, dict[str, t.Any] | None, str | None, dict[str, t.Any] | None]:
            contract = getattr(capability, "contract", None)
            description = getattr(capability, "description", None)
            if description is None and contract is not None:
                description = getattr(contract, "description", None)

            author = getattr(capability, "author", None)
            if author is None and contract is not None:
                author = getattr(contract, "author", None)

            license_name = getattr(capability, "license", None)
            if license_name is None and contract is not None:
                license_name = getattr(contract, "license", None)

            origin = getattr(capability, "origin", None)
            if origin is None and contract is not None:
                repository = getattr(contract, "repository", None)
                if isinstance(repository, str) and repository.strip():
                    origin = {"type": "repository", "url": repository}

            return description, author, license_name, origin

        def _local_path(value: t.Any) -> str | None:
            if value is None:
                return None
            raw_path = getattr(value, "path", value)
            if not isinstance(raw_path, (str, Path)):
                return None
            return str(Path(raw_path))

        capabilities_out: list[CapabilityInfo] = []
        binding_by_bare: dict[str, dict[str, t.Any]] = {}
        for binding in self.runtime_bindings:
            bare = bare_capability_name(binding.get("capability_name", ""))
            binding_by_bare[bare] = binding

        for name, capability in self.capabilities.items():
            source = getattr(capability, "source", "local")
            version = getattr(capability, "version", None)
            health = getattr(capability, "component_health", [])
            binding = binding_by_bare.pop(name, None)
            binding_id = binding.get("id") if binding else None
            display_name, canonical_name = _display_identity(
                bare_name=name,
                source=source,
                binding=binding,
            )
            cap_update = self.update_info.get(canonical_name) if canonical_name else None
            description, author, license_name, origin = _capability_metadata(capability)

            capabilities_out.append(
                CapabilityInfo(
                    name=name,
                    display_name=display_name,
                    canonical_name=canonical_name,
                    local_path=_local_path(capability),
                    source=source,
                    provenance=_provenance_for(bare_name=name, source=source),
                    version=version,
                    description=description,
                    author=author,
                    license=license_name,
                    origin=origin,
                    enabled=True,
                    binding_id=binding_id,
                    update_available=cap_update,
                    flags=[
                        FlagInfo(
                            name=f.name,
                            description=f.description,
                            default=f.default,
                            effective=f.effective,
                            source=f.source,
                        )
                        for f in getattr(capability, "resolved_flags", [])
                    ],
                    components=[ComponentStatusInfo(**entry) for entry in health],
                    dependencies=(
                        {
                            "python": _cap_deps.python,
                            "packages": _cap_deps.packages,
                            "scripts": _cap_deps.scripts,
                        }
                        if (
                            (_cap_deps := getattr(capability, "dependencies", None))
                            and (_cap_deps.python or _cap_deps.packages or _cap_deps.scripts)
                        )
                        else None
                    ),
                    checks=(
                        [{"name": c.name, "command": c.command} for c in _cap_checks]
                        if (_cap_checks := getattr(capability, "checks", None))
                        else None
                    ),
                    entry_agent=None,
                    skills_paths=[
                        str(p)
                        for p in (
                            capability.skills_paths
                            or ([] if capability.skills_path is None else [capability.skills_path])
                        )
                    ],
                    agents=[
                        CapabilityAgentInfo(
                            name=a.name,
                            description=a.description,
                            model=a.model,
                            capability=name,
                        )
                        for a in capability.agents
                    ],
                )
            )

        for bare, binding in binding_by_bare.items():
            if not binding.get("enabled", True):
                display_name, canonical_name = _display_identity(
                    bare_name=bare,
                    source="runtime",
                    binding=binding,
                )
                cap_update = self.update_info.get(canonical_name) if canonical_name else None
                capabilities_out.append(
                    CapabilityInfo(
                        name=bare,
                        display_name=display_name,
                        canonical_name=canonical_name,
                        local_path=None,
                        source="runtime",
                        provenance=None,
                        version=binding.get("version"),
                        enabled=False,
                        binding_id=binding.get("id"),
                        update_available=cap_update,
                        components=[],
                    )
                )

        for name, capability in self.disabled_local.items():
            source = getattr(capability, "source", "local")
            version = getattr(capability, "version", None)
            display_name, canonical_name = _display_identity(
                bare_name=name,
                source=source,
                binding=None,
            )
            cap_update = self.update_info.get(canonical_name) if canonical_name else None
            description, author, license_name, origin = _capability_metadata(capability)
            capabilities_out.append(
                CapabilityInfo(
                    name=name,
                    display_name=display_name,
                    canonical_name=canonical_name,
                    local_path=_local_path(capability),
                    source=source,
                    provenance=_provenance_for(bare_name=name, source=source),
                    version=version,
                    description=description,
                    author=author,
                    license=license_name,
                    origin=origin,
                    enabled=False,
                    update_available=cap_update,
                    components=[],
                )
            )

        for failure in self.load_failures:
            name = failure.get("name", "unknown")
            display_name, canonical_name = _display_identity(
                bare_name=name,
                source="local",
                binding=None,
            )
            cap_update = self.update_info.get(canonical_name) if canonical_name else None
            capabilities_out.append(
                CapabilityInfo(
                    name=name,
                    display_name=display_name,
                    canonical_name=canonical_name,
                    local_path=_local_path(failure.get("path")),
                    source="local",
                    provenance=_provenance_for(bare_name=name, source="local"),
                    enabled=True,
                    update_available=cap_update,
                    components=[
                        ComponentStatusInfo(
                            kind="capability",
                            name=name,
                            status="error",
                            error=failure.get("error"),
                            detail="Check capability.yaml format and directory structure",
                        )
                    ],
                )
            )

        runtime_id = os.environ.get("DREADNODE_RUNTIME_ID", "").strip() or None
        host = "sandbox" if runtime_id else "local"
        from dreadnode.version import VERSION

        return RuntimeInfoResponse(
            runtime_id=runtime_id,
            host_type=host,
            version=VERSION,
            working_dir=str(working_dir),
            default_capability=self.default_capability_name,
            capabilities=capabilities_out,
        )


def _stamp_mcp_tools(client: t.Any, *, cap_name: str, server_name: str) -> None:
    """Stamp MCP-sourced identity on each tool an MCP client reports (CAP-IDENT-007).

    Mutates ``client.tools`` in place — each entry is replaced with a
    ``model_copy`` carrying ``source='mcp'`` and ``namespace=(cap, server)``.
    Non-Tool entries are left alone defensively; MCPClient is expected to
    expose ``Tool`` instances but we don't depend on it.
    """
    from dreadnode.agents.tools import Tool

    stamped: list[t.Any] = []
    for item in getattr(client, "tools", []) or []:
        if isinstance(item, Tool):
            stamped.append(
                item.model_copy(update={"source": "mcp", "namespace": (cap_name, server_name)})
            )
        else:
            stamped.append(item)
    client.tools = stamped


@dataclass
class MCPLifecycleManager:
    """Manages MCP server connections for all capabilities.

    Connection is non-blocking with respect to runtime startup
    (CAP-MCP-009): ``start()`` registers every server as ``connecting``
    in component health, schedules per-server connects as background
    tasks, and returns. Tools become available on the per-turn
    ``all_tools()`` snapshot as each server reaches ``connected``.
    ``wait_for_connects()`` is provided for tests (and any caller that
    legitimately needs the settled state) but production never awaits.
    """

    event_bus: "EventBus | None" = None
    _clients: dict[str, tuple[t.Any, t.Any]] = field(default_factory=dict)
    _registry: t.Any = field(default=None)
    _connect_tasks: set[asyncio.Task[None]] = field(default_factory=set)
    _supervisor_task: asyncio.Task[None] | None = field(default=None)
    _connects_done: asyncio.Event = field(default_factory=asyncio.Event)

    def iter_qualified_tools(self) -> t.Iterator[tuple[str, str, t.Any]]:
        """Yield ``(capability, server, tool)`` for every connected client.

        Snapshots ``_clients`` before iterating so concurrent reconnect
        mutations don't raise ``RuntimeError: dictionary changed size during
        iteration`` (Will's Gap #11).
        """
        for qualified, (_server_def, client) in list(self._clients.items()):
            if client is None:
                continue
            cap_name, _, server_name = qualified.partition(":")
            for tool in list(getattr(client, "tools", []) or []):
                yield cap_name, server_name, tool

    async def start(self, registry: CapabilityRegistry) -> None:
        """Register MCP servers and schedule connects in the background.

        Returns once every server has a placeholder entry in ``_clients``
        and component_health (status ``connecting`` for active servers,
        ``gated_off`` for gated ones). Per-server ``connect()`` calls run
        as background tasks so runtime startup is never blocked by a
        slow or interactive MCP server (CAP-MCP-009, CAP-WLIF-002).

        Use ``wait_for_connects()`` to await the settled state (tests
        and the rare caller that legitimately needs every connect to
        have completed).
        """
        from dreadnode.capabilities.flags import evaluate_when

        self._registry = registry
        self._connects_done = asyncio.Event()
        started_at = time.perf_counter()
        gated_count = 0

        # Phase 1 — synchronous registration. Stamp every server into
        # ``_clients`` and component_health with metadata + initial status
        # before returning, so the UI sees a complete picture immediately
        # and the per-turn ``all_tools()`` snapshot is stable.
        pending: list[tuple[t.Any, t.Any, dict[str, str]]] = []
        for cap in registry.capabilities.values():
            resolved = cap.resolved_flags
            flag_env = cap.flag_env_vars()
            cap_health = getattr(cap, "component_health", None)
            for server_def in cap.mcp_server_defs:
                qualified = f"{cap.name}:{server_def.name}"
                # CAP-FLAG-014: gate evaluation happens once, synchronously.
                if not evaluate_when(server_def.when, resolved):
                    gated_count += 1
                    logger.debug("MCP server gated off: {}", qualified)
                    self._clients[qualified] = (server_def, None)
                    when_names = ", ".join(server_def.when or [])
                    self._stamp_initial_health(
                        cap_health,
                        server_def=server_def,
                        qualified=qualified,
                        capability=cap.name,
                        status="gated_off",
                        detail=f"Requires flag: {when_names}",
                        extra={"when": list(server_def.when or [])},
                    )
                    self._publish_state_changed(
                        capability=cap.name,
                        name=server_def.name,
                        status="gated_off",
                        error=None,
                        detail=f"Requires flag: {when_names}",
                        tool_count=0,
                    )
                    continue

                # Non-gated: register pending and schedule the connect.
                self._clients[qualified] = (server_def, None)
                self._stamp_initial_health(
                    cap_health,
                    server_def=server_def,
                    qualified=qualified,
                    capability=cap.name,
                    status="connecting",
                    detail=None,
                )
                self._publish_state_changed(
                    capability=cap.name,
                    name=server_def.name,
                    status="connecting",
                    error=None,
                    detail=None,
                    tool_count=0,
                )
                pending.append((cap, server_def, flag_env))

        if not pending:
            self._connects_done.set()
            logger.info(
                "MCP start | no servers to connect | gated_off={} | total_ms={}",
                gated_count,
                round((time.perf_counter() - started_at) * 1000),
            )
            return

        # Phase 2 — background. Per-server connect tasks plus a single
        # supervisor that logs the aggregate summary once everything has
        # settled and signals ``_connects_done`` for any waiters.
        for cap, server_def, flag_env in pending:
            task = asyncio.create_task(
                self._start_server(cap, server_def, flag_env),
                name=f"mcp-connect:{cap.name}:{server_def.name}",
            )
            self._connect_tasks.add(task)
            task.add_done_callback(self._connect_tasks.discard)

        self._supervisor_task = asyncio.create_task(
            self._supervise_connects(started_at, len(pending), gated_count),
            name="mcp-connect-supervisor",
        )

    def _stamp_initial_health(
        self,
        cap_health: list[dict[str, t.Any]] | None,
        *,
        server_def: t.Any,
        qualified: str,
        capability: str,
        status: str,
        detail: str | None,
        extra: dict[str, t.Any] | None = None,
    ) -> None:
        """Stamp the static metadata + initial status onto an MCP server's
        health entry. Subsequent transitions go through
        ``_update_component_health`` which only touches dynamic fields.
        """
        if cap_health is None:
            return
        for entry in cap_health:
            if entry.get("kind") == "mcp_server" and entry.get("name") == server_def.name:
                entry["qualified_name"] = qualified
                entry["capability"] = capability
                entry["transport"] = server_def.transport
                entry["status"] = status
                entry["error"] = None
                entry["detail"] = detail
                entry["tool_count"] = 0
                if extra:
                    entry.update(extra)
                break

    async def _supervise_connects(
        self,
        started_at: float,
        total: int,
        gated_count: int,
    ) -> None:
        """Wait for every per-server connect task to settle, then log + signal."""
        try:
            # Per-server tasks swallow their own exceptions; return_exceptions
            # is belt-and-braces so a programmer error here doesn't deadlock
            # ``_connects_done``.
            if self._connect_tasks:
                await asyncio.gather(*list(self._connect_tasks), return_exceptions=True)
        finally:
            self._connects_done.set()
            connected = sum(
                1 for _server_def, client in self._clients.values() if client is not None
            )
            failed = total - connected
            logger.info(
                "MCP start complete | connected={} | failed={} | gated_off={} | total_ms={}",
                connected,
                failed,
                gated_count,
                round((time.perf_counter() - started_at) * 1000),
            )

    async def wait_for_connects(self) -> None:
        """Await every scheduled MCP connect to settle. For tests."""
        await self._connects_done.wait()

    async def _start_server(self, cap: t.Any, server_def: t.Any, flag_env: dict[str, str]) -> None:
        """Connect one MCP server in the background.

        Always swallows its own exceptions — failure is recorded in
        component_health and published over the event bus. The
        synchronous registration in ``start()`` has already stamped
        metadata; this updates dynamic fields only.
        """
        from dreadnode.agents.mcp.client import MCPClient
        from dreadnode.agents.mcp.config import StdioServerConfig

        qualified = f"{cap.name}:{server_def.name}"
        server_started_at = time.perf_counter()
        client: t.Any = None
        try:
            config = server_def.to_server_config()
            # CAP-FLAG-020: inject CAPABILITY_FLAG__* env vars into subprocess
            if isinstance(config, StdioServerConfig) and flag_env:
                config.env = {**(config.env or {}), **flag_env}
            log_path = (
                mcp_log_path(cap.name, server_def.name)
                if isinstance(config, StdioServerConfig)
                else None
            )
            client = MCPClient.from_config(config, log_path=log_path)
            # Background startup connect: never open a browser. An OAuth server
            # with no stored token settles into needs_auth (CAP-MCP-010); the
            # user authenticates explicitly via the Services screen.
            await client.connect(interactive=False)
            _stamp_mcp_tools(client, cap_name=cap.name, server_name=server_def.name)
            self._clients[qualified] = (server_def, client)
            logger.info("MCP server connected: {}", qualified)
            logger.debug(
                "MCP start | server={} | status=connected | elapsed_ms={}",
                qualified,
                round((time.perf_counter() - server_started_at) * 1000),
            )
            self._update_component_health(cap.name, server_def.name, "ok", None, len(client.tools))
        except asyncio.CancelledError:
            # Shutdown (stop()) cancelled this connect mid-flight. The client
            # runs its connection in a separate owner task that this
            # cancellation does NOT reach, and the client was never stored in
            # ``_clients`` (so stop()'s disconnect loop won't see it). Tear it
            # down explicitly so the transport/subprocess doesn't leak, then
            # propagate the cancellation.
            if client is not None:
                try:
                    await client.disconnect()
                except Exception:
                    logger.opt(exception=True).debug(
                        "Error disconnecting in-flight MCP connect '{}' during cancel",
                        qualified,
                    )
            raise
        except Exception as exc:
            logger.opt(exception=True).warning(
                "MCP server '{}' failed to start — skipping",
                qualified,
            )
            logger.debug(
                "MCP start | server={} | status=failed | elapsed_ms={} | error={}",
                qualified,
                round((time.perf_counter() - server_started_at) * 1000),
                exc,
            )
            self._clients[qualified] = (server_def, None)
            self._record_connect_failure(cap.name, server_def, client, exc)

    def _record_connect_failure(
        self, capability: str, server_def: t.Any, client: t.Any, exc: Exception
    ) -> None:
        """Stamp a failed MCP connect into component_health.

        Preserves the client's ``NEEDS_AUTH`` classification rather than
        flattening every failure to a generic error (the bug ENG-6989
        verified). The client computes its own status in ``_set_error_status``;
        the lifecycle manager reads it. Shared by the background
        ``_start_server`` and the user-initiated ``reconnect_server`` so both
        paths classify failures identically.
        """
        from dreadnode.agents.mcp.config import MCPStatus

        client_status = getattr(client, "status", None) if client is not None else None
        if client_status == MCPStatus.NEEDS_AUTH:
            self._update_component_health(
                capability,
                server_def.name,
                "needs_auth",
                str(exc),
                0,
                detail="Server requires authentication — use Authenticate in Services to connect",
            )
        else:
            # CAP-FLAG-015: distinguish enabled-failed from generic error.
            status = "enabled_failed" if server_def.when else "error"
            self._update_component_health(
                capability,
                server_def.name,
                status,
                str(exc),
                0,
                detail="Check server command/URL and authentication credentials",
            )

    async def stop(self) -> None:
        """Cancel any in-flight connects, then disconnect every live MCP server."""
        started_at = time.perf_counter()

        # Cancel pending background connects first so a slow/hanging
        # ``connect()`` doesn't keep us in shutdown. Each task's
        # ``except CancelledError`` block disconnects an in-flight client
        # (the connection's owner task is separate and isn't reached by
        # cancelling the wrapper, so it must be torn down explicitly).
        cancelled = 0
        for task in list(self._connect_tasks):
            if not task.done():
                task.cancel()
                cancelled += 1
        pending_tasks = list(self._connect_tasks)
        if pending_tasks:
            await asyncio.gather(*pending_tasks, return_exceptions=True)
        if self._supervisor_task is not None and not self._supervisor_task.done():
            # The supervisor was awaiting gather() on the connect tasks;
            # cancelling them lets it run to completion (setting the
            # done event) — just await it.
            await asyncio.gather(self._supervisor_task, return_exceptions=True)
        self._connect_tasks.clear()
        self._supervisor_task = None

        disconnect_targets = [
            (name, client)
            for name, (_server_def, client) in self._clients.items()
            if client is not None
        ]
        async with asyncio.TaskGroup() as tg:
            for name, client in disconnect_targets:
                tg.create_task(self._disconnect_client(name, client))
        logger.info(
            "MCP stop complete | cancelled_connects={} | disconnected={} | total_ms={}",
            cancelled,
            len(disconnect_targets),
            round((time.perf_counter() - started_at) * 1000),
        )
        self._clients.clear()

    async def _disconnect_client(self, name: str, client: t.Any) -> None:
        """Disconnect one MCP client without interrupting the rest."""
        started_at = time.perf_counter()
        try:
            await client.disconnect()
            logger.debug(
                "MCP stop | server={} | status=disconnected | elapsed_ms={}",
                name,
                round((time.perf_counter() - started_at) * 1000),
            )
        except Exception:
            logger.opt(exception=True).warning("Error disconnecting MCP server '{}'", name)
            logger.debug(
                "MCP stop | server={} | status=error | elapsed_ms={}",
                name,
                round((time.perf_counter() - started_at) * 1000),
            )

    def all_tools(self) -> list[t.Any]:
        """Collect tools from all connected MCP servers."""
        tools: list[t.Any] = []
        for _server_def, client in self._clients.values():
            if client is not None:
                tools.extend(client.tools)
        return tools

    def get_server_detail(self, capability: str, server_name: str) -> dict[str, t.Any] | None:
        """Return full detail dict for an MCP server, or None if not found."""
        qualified = f"{capability}:{server_name}"
        entry = self._clients.get(qualified)
        if entry is None:
            return None

        server_def, client = entry
        # Single health-entry lookup, reused for both the client-absent status
        # fallback and the canonical ``detail`` passthrough below.
        health_entry = self._lookup_health_entry(capability, server_def.name)

        if client is not None:
            status_val = (
                client.status.value if hasattr(client.status, "value") else str(client.status)
            )
            error_val = getattr(client, "_error", None)
            raw_log_path = getattr(client, "log_path", None)
            # Only trust a real Path — test doubles may return a stand-in.
            client_log_path = raw_log_path if isinstance(raw_log_path, Path) else None
            raw_recent = getattr(client, "recent_stderr", [])
            recent_stderr = list(raw_recent) if isinstance(raw_recent, list) else []
            tools = []
            for tool in client.tools:
                tool_info: dict[str, t.Any] = {
                    "name": tool.name,
                    "description": getattr(tool, "description", ""),
                }
                params = getattr(tool, "parameters_schema", None) or getattr(
                    tool, "parameters", None
                )
                if params:
                    tool_info["input_schema"] = params
                tools.append(tool_info)
        else:
            # Prefer the canonical component_health status when the client
            # object isn't stored yet. Under non-blocking startup
            # (CAP-MCP-009) ``_clients[q] = (server_def, None)`` is set
            # synchronously while ``_start_server`` runs in the background,
            # so a ``connecting`` or ``needs_auth`` health entry must
            # surface here — not the legacy "disconnected/Server failed to
            # connect" default that pre-dated background connects.
            if health_entry is not None and health_entry.get("status"):
                status_val = str(health_entry["status"])
                error_val = health_entry.get("error")
                if error_val is None and status_val in ("connecting", "needs_auth"):
                    # connecting has no error; needs_auth's detail carries
                    # the user-facing hint, error stays None until/unless
                    # the underlying connect raises.
                    error_val = None
                elif error_val is None:
                    error_val = "Server failed to connect"
            else:
                status_val = "disconnected"
                error_val = "Server failed to connect"
            client_log_path = None
            recent_stderr = []
            tools = []

        # Stdio servers always get a log path (even when the client failed to
        # spawn) so operators can see where captured stderr *would* land.
        if client_log_path is None and server_def.transport == "stdio":
            client_log_path = mcp_log_path(capability, server_def.name)

        # Carry the canonical ``detail`` field through to the detail view
        # so the ``needs_auth`` user-facing hint (and any future per-status
        # guidance) renders without forcing the TUI to fall back to its
        # cached list-level snapshot. Reuses the single lookup from above.
        detail_text = health_entry.get("detail") if health_entry else None
        # Surface the manifest-declared auth type so the TUI can offer the
        # Re-authenticate action for OAuth servers without round-tripping
        # the manifest schema.
        auth_def = getattr(server_def, "auth", None)
        auth_type = auth_def.type if auth_def is not None else None
        return {
            "name": server_def.name,
            "qualified_name": qualified,
            "capability": capability,
            "status": status_val,
            "error": error_val,
            "detail": detail_text,
            "transport": server_def.transport,
            "command": server_def.command,
            "args": list(server_def.args),
            "url": server_def.url,
            "auth_type": auth_type,
            "log_path": str(client_log_path) if client_log_path is not None else None,
            "recent_stderr": recent_stderr,
            "tool_count": len(tools),
            "tools": tools,
        }

    def _lookup_health_entry(self, capability: str, server_name: str) -> dict[str, t.Any] | None:
        """Return the component_health entry for an MCP server, or None.

        Used by ``get_server_detail`` and any other code that needs the
        canonical lifecycle-manager-owned status (``connecting``,
        ``needs_auth``, etc.) when the client object itself is absent.
        """
        if self._registry is None:
            return None
        cap = self._registry.capabilities.get(capability)
        if cap is None:
            return None
        for entry in getattr(cap, "component_health", []) or []:
            if entry.get("kind") == "mcp_server" and entry.get("name") == server_name:
                return entry
        return None

    async def reconnect_server(self, capability: str, server_name: str) -> dict[str, t.Any] | None:
        """Disconnect and reconnect an MCP server."""
        from dreadnode.agents.mcp.client import MCPClient
        from dreadnode.agents.mcp.config import StdioServerConfig
        from dreadnode.capabilities.flags import evaluate_when

        qualified = f"{capability}:{server_name}"
        entry = self._clients.get(qualified)
        if entry is None:
            return None

        server_def, client = entry

        # CAP-FLAG-014: re-evaluate when: predicate before reconnecting
        if self._registry is not None:
            cap = self._registry.capabilities.get(capability)
            if cap is not None and not evaluate_when(server_def.when, cap.resolved_flags):
                self._update_component_health(capability, server_def.name, "gated_off", None, 0)
                detail = self.get_server_detail(capability, server_name) or {}
                detail["gated_off"] = True
                detail["when"] = list(server_def.when or [])
                return detail

        if client is not None:
            try:
                await client.disconnect()
            except Exception:
                logger.debug(
                    "Error during disconnect of '{}' — proceeding with reconnect", qualified
                )

        new_client: t.Any = None
        try:
            config = server_def.to_server_config()
            # CAP-FLAG-020: inject flag env vars on reconnect too
            if self._registry is not None and isinstance(config, StdioServerConfig):
                cap = self._registry.capabilities.get(capability)
                if cap is not None:
                    flag_env = cap.flag_env_vars()
                    if flag_env:
                        config.env = {**(config.env or {}), **flag_env}
            log_path = (
                mcp_log_path(capability, server_def.name)
                if isinstance(config, StdioServerConfig)
                else None
            )
            new_client = MCPClient.from_config(config, log_path=log_path)
            # User-initiated reconnect: this IS the moment the runtime owns the
            # browser-open. An OAuth server with no token drives the full
            # interactive flow (discovery → browser → callback → tokens).
            await new_client.connect(interactive=True)
            _stamp_mcp_tools(new_client, cap_name=capability, server_name=server_def.name)
            self._clients[qualified] = (server_def, new_client)
            self._update_component_health(
                capability, server_def.name, "ok", None, len(new_client.tools)
            )
        except Exception as exc:
            logger.warning("Reconnect failed for '{}': {}", qualified, exc)
            # Preserve a needs_auth classification (e.g. the user cancelled or
            # timed out the browser flow) rather than flattening to a generic
            # error — shared with _start_server's handling.
            self._clients[qualified] = (server_def, None)
            self._record_connect_failure(capability, server_def, new_client, exc)

        return self.get_server_detail(capability, server_name)

    async def reauthenticate_server(
        self, capability: str, server_name: str
    ) -> dict[str, t.Any] | None:
        """Clear stored OAuth credentials for a server, then reconnect.

        Targeted: only this server's entry in the on-disk token store is
        removed (per :meth:`FileTokenStorage.clear`). Other authenticated
        capabilities keep their tokens. The subsequent ``reconnect_server``
        call will see no stored tokens and trigger a fresh OAuth round-trip
        (browser open, callback server, token exchange).

        Returns the same detail dict shape as :meth:`reconnect_server`.
        Returns ``None`` only if the server is unknown or is a stdio server
        (stdio manages its own credentials — use :meth:`reconnect_server`).
        Every streamable-http server is OAuth-capable now that OAuth is
        reactive-by-default (CAP-MCP-011), so no ``auth:`` declaration is
        required for re-authentication to apply.
        """
        from dreadnode.agents.mcp.auth import FileTokenStorage

        qualified = f"{capability}:{server_name}"
        entry = self._clients.get(qualified)
        if entry is None:
            return None
        server_def, _ = entry

        # Meaningful for any streamable-http server: OAuth is reactive-by-
        # default (CAP-MCP-011), so every HTTP server is OAuth-capable — a
        # declared auth: block is not required. Stdio servers manage their own
        # credentials; reject cleanly so the caller uses reconnect_server.
        if server_def.transport != "streamable-http":
            return None

        url = server_def.url
        if url:
            try:
                from dreadnode.capabilities.types import _expand_env_vars

                storage = FileTokenStorage(_expand_env_vars(url))
                await storage.clear()
                logger.info("Cleared OAuth credentials for {}", qualified)
            except Exception as exc:
                logger.warning("Failed to clear OAuth credentials for {}: {}", qualified, exc)

        return await self.reconnect_server(capability, server_name)

    def _update_component_health(
        self,
        capability: str,
        server_name: str,
        status: str,
        error: str | None,
        tool_count: int,
        *,
        detail: str | None | Unset = UNSET,
    ) -> None:
        """Update the component_health entry for an MCP server in the registry.

        Also publishes a ``component.state_changed`` runtime event so the
        TUI (and any other subscribers) can patch their cached
        ``runtime_info`` snapshots in place without polling. Publish is
        fire-and-forget; the registry mutation has already happened
        regardless of whether the bus delivers.

        ``detail`` defaults to preserving the existing detail field. Pass
        an explicit value (including ``None``) to overwrite it — used by
        ``_start_server`` to attach an auth-prompt hint on
        ``needs_auth`` transitions.
        """
        if self._registry is None:
            return
        cap = self._registry.capabilities.get(capability)
        if cap is None:
            return
        effective_detail: str | None = None
        for entry in getattr(cap, "component_health", []):
            if entry.get("kind") == "mcp_server" and entry.get("name") == server_name:
                entry["status"] = status
                entry["error"] = error
                entry["tool_count"] = tool_count
                if detail is not UNSET:
                    entry["detail"] = detail
                effective_detail = entry.get("detail")
                break
        self._publish_state_changed(
            capability=capability,
            name=server_name,
            status=status,
            error=error,
            detail=effective_detail,
            tool_count=tool_count,
        )

    def _publish_state_changed(
        self,
        *,
        capability: str,
        name: str,
        status: str,
        error: str | None,
        detail: str | None,
        tool_count: int,
    ) -> None:
        """Schedule a ``component.state_changed`` publish on the bus."""
        if self.event_bus is None:
            return
        from dreadnode.app.server import runtime_events

        try:
            asyncio.create_task(  # noqa: RUF006
                self.event_bus.publish(
                    kind=runtime_events.EVENT_COMPONENT_STATE_CHANGED,
                    payload={
                        "capability": capability,
                        "name": name,
                        "kind": "mcp_server",
                        "status": status,
                        "error": error,
                        "detail": detail,
                        "tool_count": tool_count,
                    },
                ),
                name=f"component-state-publish:{capability}:{name}",
            )
        except RuntimeError:
            logger.debug(
                "component.state_changed: no running loop, skipping publish | {}:{}",
                capability,
                name,
            )
