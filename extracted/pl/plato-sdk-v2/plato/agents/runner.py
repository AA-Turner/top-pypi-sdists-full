"""Agent runner - run agents in Docker containers or VMs."""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import sys
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from opentelemetry import trace

from plato.agents.runtime import DockerRuntime, PlatoVMRuntime
from plato.agents.runtime.base import AgentContext, PreparedAgent, Runtime
from plato.agents.runtime.transport import NFSTransport, SSHFSTransport, Transport
from plato.agents.runtime.vm import VMConfig
from plato.chronos.models import AuditEventInput, Operation
from plato.runtime import VMRuntimeConfig
from plato.utils.audit import (
    AuditScopeContext,
    audit_ignore_filter,
    build_audit_key,
    load_audit_ignore,
    new_audit_run_id,
    parse_audit_raw,
    write_audit_jsonl,
)
from plato.utils.audit_resolution import resolve_audit_events_for_scope
from plato.utils.subprocess import run_ssh
from plato.utils.tool_execution import (
    DEFAULT_TOOL_EXECUTION_CONTEXT_PATH,
    DEFAULT_TOOL_EXECUTION_SPOOL_PATH,
    DEFAULT_TOOL_START_SPOOL_PATH,
    ToolExecutionContext,
    ToolExecutionRecord,
    ToolExecutionScope,
    parse_tool_execution_records,
    tool_execution_spool_path,
    write_tool_execution_records,
)

if TYPE_CHECKING:
    from plato.agents.base import BaseAgent
    from plato.agents.runtime.warmpool import WarmPool
    from plato.v2.async_.session import Session
    from plato.worlds.config import AgentConfig

logger = logging.getLogger(__name__)


@dataclass
class AuditScope:
    """Per-workspace audit collection scope for a single agent run."""

    transport: NFSTransport | SSHFSTransport
    workspace_name: str
    repo_root: Path
    mount_path: str
    audit_run_id: str
    audit_key: str

    @property
    def spool_path(self) -> Path:
        return self.repo_root / ".plato" / "audit" / self.workspace_name / f"{self.audit_run_id}.jsonl"

    @property
    def tool_spool_path(self) -> Path:
        return tool_execution_spool_path(
            self.repo_root / ".plato",
            workspace_name=self.workspace_name,
            audit_run_id=self.audit_run_id,
        )


def create_runtime(
    agent: AgentConfig,
    session: Session | None = None,
    ssh_key_path: Path | None = None,
    warm_pool: WarmPool | None = None,
) -> Runtime:
    """Create a runtime instance based on agent config."""
    runtime_cfg = agent.runtime
    if runtime_cfg.type == "vm":
        if session is None:
            raise ValueError("session is required for VM mode")
        if not isinstance(runtime_cfg, VMRuntimeConfig):
            raise ValueError("VMRuntimeConfig required for VM mode")
        return PlatoVMRuntime(
            session=session,
            ssh_key_path=ssh_key_path,
            vm_config=VMConfig(
                cpus=runtime_cfg.vm.cpus or 2,
                memory=runtime_cfg.vm.memory or 4096,
                disk=runtime_cfg.vm.disk or 10240,
                timeout=runtime_cfg.vm.timeout or 7200,
            ),
            warm_pool=warm_pool,
        )
    else:
        return DockerRuntime()


class AgentRunner:
    """Builder for running agents with optional lifecycle hooks.

    Usage:
        # One-shot (simple)
        await AgentRunner(agent_config, runtime).run(instruction)

        # Two-phase with hooks
        await (
            AgentRunner(agent_config, runtime)
            .on_prepare(async_login_fn)
            .run(instruction, workspace="/workspace")
        )

    Execution: prepare() → on_prepare hooks → execute() → on_post_run hooks → cleanup.
    """

    def __init__(
        self,
        agent: AgentConfig,
        runtime: Runtime,
        display_name: str | None = None,
        workspace: Transport | None = None,
        workspaces: list[Transport] | None = None,
        agent_containers: list[str] | None = None,
        agent_code_path: Path | None = None,
    ):
        self._agent = agent
        self._runtime = runtime
        self._display_name = display_name
        self._workspace = workspace
        self._default_workspaces = workspaces or []
        self._prepare_hooks: list[Callable[[PreparedAgent], Awaitable[None]]] = []
        self._post_run_hooks: list[Callable[[PreparedAgent], Awaitable[None]]] = []
        self._agent_containers = agent_containers
        self._agent_code_path = agent_code_path
        # Continuation loop settings (set via with_continuation())
        self._exit_condition: Callable[[], Awaitable[bool]] | None = None
        self._max_continuations: int = 2
        self._continuation_instruction: str = "Continue. Complete all remaining work."
        # File trigger settings (set via with_file_triggers())
        self._file_trigger_patterns: list[str] | None = None
        self._trigger_server_url: str | None = None
        # Populated after run() completes — hex span ID of the agent.execution.output span
        self.last_execution_span_id: str = ""
        # Concurrency semaphore — set by BaseWorld.agent() when AgentConfig.max_parallel is set
        self._concurrency_semaphore: asyncio.Semaphore | None = None

    def on_prepare(self, fn: Callable[[PreparedAgent], Awaitable[None]]) -> AgentRunner:
        """Register a hook that runs after the environment is ready but before the agent task.

        The hook receives a PreparedAgent with hostname for networking
        (e.g., to connect to Chrome CDP at `http://{prepared.hostname}:9224`).
        """
        self._prepare_hooks.append(fn)
        return self

    def on_post_run(self, fn: Callable[[PreparedAgent], Awaitable[None]]) -> AgentRunner:
        """Register a hook that runs after the agent finishes but before the VM is torn down.

        The hook receives the same PreparedAgent, so you can still SSH into the
        agent VM (e.g., to collect artifacts, run validation, or read results).
        """
        self._post_run_hooks.append(fn)
        return self

    def with_continuation(
        self,
        exit_condition: Callable[[], Awaitable[bool]],
        max_continuations: int = 2,
        continuation_instruction: str = "Continue. Complete all remaining work.",
    ) -> AgentRunner:
        """Configure a continuation loop for resilient agent execution.

        When configured, the runner will re-invoke the agent (using ``--continue``
        to resume its Claude Code session) up to *max_continuations* additional
        times if *exit_condition* returns ``False`` after an execution.

        The VM is prepared once and kept alive across all attempts.  Transport
        sync-back happens after each ``execute()`` call, so the exit condition
        can inspect files on the shared workspace / NFS mount.

        Args:
            exit_condition: Async callable returning ``True`` when the agent's
                work is complete (e.g. ``completion.json`` exists).
            max_continuations: Maximum number of extra attempts after the
                initial run (default 2, so up to 3 total executions).
            continuation_instruction: Prompt sent on continuation runs.
        """
        self._exit_condition = exit_condition
        self._max_continuations = max_continuations
        self._continuation_instruction = continuation_instruction
        return self

    def with_file_triggers(
        self,
        patterns: list[str],
        trigger_server_url: str,
    ) -> AgentRunner:
        """Configure file-pattern checkpoint triggers.

        Starts a file watcher sidecar on the agent VM that monitors workspace
        directories for files matching *patterns* and pushes trigger events
        (with span context) to the world VM's trigger server.

        Args:
            patterns: Glob patterns to watch, e.g. ``["**/progress.json"]``.
            trigger_server_url: TCP address of the world's trigger server,
                e.g. ``"10.0.0.1:8765"``.
        """
        self._file_trigger_patterns = patterns
        self._trigger_server_url = trigger_server_url
        return self

    def with_file_triggers_from(self, ctx: object) -> AgentRunner:
        """Configure file triggers from a :class:`CheckpointContext`.

        This is the recommended way to wire file triggers — the patterns
        and trigger server URL are read directly from the context yielded
        by :func:`~plato.worlds.checkpoint.checkpoint`.
        """
        trigger_url = getattr(ctx, "trigger_url", None)
        trigger_patterns = getattr(ctx, "trigger_patterns", None)
        if trigger_url and trigger_patterns:
            self._file_trigger_patterns = trigger_patterns
            self._trigger_server_url = trigger_url
        return self

    def _all_transports(self) -> list[Transport]:
        """Return the primary and extra transports without duplicates."""
        transports: list[Transport] = []
        seen: set[int] = set()
        for transport in [self._workspace, *self._default_workspaces]:
            if transport is None:
                continue
            marker = id(transport)
            if marker in seen:
                continue
            seen.add(marker)
            transports.append(transport)
        return transports

    def _default_agent_name(self) -> str:
        return self._agent.image.split("/")[-1].split(":")[0]

    def _audit_workspace_name(self, transport: Transport) -> str:
        workspace_name = getattr(transport, "workspace_name", None)
        if workspace_name:
            return workspace_name
        mount_path = transport.agent_mount_path
        fallback = Path(mount_path).name or "workspace"
        return fallback

    def _configure_audit_scopes(self, display_name: str | None = None) -> list[AuditScope]:
        """Create one audit scope per tracked NFS/SSHFS-mounted workspace.

        Each scope gets its own *copy* of the transport so that parallel
        ``AgentRunner`` instances don't overwrite each other's ``audit_key``
        on a shared ``Transport`` object.
        """
        del display_name
        scopes: list[AuditScope] = []

        for transport in self._all_transports():
            if not isinstance(transport, (NFSTransport, SSHFSTransport)):
                continue
            if not getattr(transport, "workspace_tracked", False):
                continue

            repo_root = getattr(transport, "workspace_repo_root", None)
            if not repo_root:
                logger.debug(
                    "Skipping audit scope for tracked transport without repo root: %s",
                    transport.path,
                )
                continue

            # Create a per-runner copy so we don't mutate the shared transport.
            transport_copy = transport.with_path(transport.path)
            transport_copy.mount_path = transport.mount_path

            workspace_name = self._audit_workspace_name(transport_copy)
            audit_run_id = new_audit_run_id()
            audit_key = build_audit_key(audit_run_id)
            transport_copy.configure_audit_scope(
                audit_run_id=audit_run_id,
                audit_key=audit_key,
            )

            # Replace the shared transport reference with our copy so that
            # setup_agent() (called later during execute) reads the correct
            # audit_key for this runner, not whichever runner wrote last.
            self._replace_transport(transport, transport_copy)

            scopes.append(
                AuditScope(
                    transport=transport_copy,
                    workspace_name=workspace_name,
                    repo_root=Path(repo_root),
                    mount_path=transport_copy.agent_mount_path,
                    audit_run_id=audit_run_id,
                    audit_key=audit_key,
                )
            )

        return scopes

    def _replace_transport(self, old: Transport, new: Transport) -> None:
        """Swap a transport reference in workspace slots so downstream code uses the copy."""
        if self._workspace is old:
            self._workspace = new
        for i, ws in enumerate(self._default_workspaces):
            if ws is old:
                self._default_workspaces[i] = new

    def _audit_context_payload(
        self,
        prepared: PreparedAgent,
        scopes: list[AuditScope],
        *,
        display_name: str | None,
    ) -> dict[str, object]:
        span = trace.get_current_span()
        ctx = span.get_span_context()
        trace_id = format(ctx.trace_id, "032x") if ctx.is_valid else ""
        span_id = format(ctx.span_id, "016x") if ctx.is_valid else ""

        agent_name = display_name or self._display_name or self._default_agent_name()
        return {
            "session_id": os.environ.get("SESSION_ID", ""),
            "agent_id": prepared.agent_id,
            "agent_name": agent_name,
            "display_name": display_name or self._display_name or agent_name,
            "trace_id": trace_id,
            "span_id": span_id,
            "scopes": [
                {
                    "workspace_name": scope.workspace_name,
                    "mount_path": scope.mount_path,
                    "audit_run_id": scope.audit_run_id,
                    "audit_key": scope.audit_key,
                }
                for scope in scopes
            ],
        }

    def _tool_execution_context_payload(
        self,
        prepared: PreparedAgent,
        scopes: list[AuditScope],
        *,
        display_name: str | None,
    ) -> ToolExecutionContext:
        audit_context = self._audit_context_payload(
            prepared,
            scopes,
            display_name=display_name,
        )
        return ToolExecutionContext(
            session_id=str(audit_context.get("session_id", "")),
            agent_id=prepared.agent_id,
            agent_name=str(audit_context.get("agent_name", "")),
            display_name=str(audit_context.get("display_name", "")),
            trace_id=str(audit_context.get("trace_id", "")),
            span_id=str(audit_context.get("span_id", "")),
            spool_path=str(DEFAULT_TOOL_EXECUTION_SPOOL_PATH),
            hook_spool_path=str(DEFAULT_TOOL_START_SPOOL_PATH),
            scopes=[
                ToolExecutionScope(
                    workspace_name=scope.workspace_name,
                    mount_path=scope.mount_path,
                    audit_run_id=scope.audit_run_id,
                    audit_key=scope.audit_key,
                )
                for scope in scopes
            ],
        )

    async def _write_audit_context(
        self,
        prepared: PreparedAgent,
        scopes: list[AuditScope],
        *,
        display_name: str | None,
    ) -> None:
        """Write audit context JSON to the agent VM before agent launch."""
        try:
            context_json = json.dumps(
                self._audit_context_payload(
                    prepared,
                    scopes,
                    display_name=display_name,
                )
            )
            tool_context_json = self._tool_execution_context_payload(
                prepared,
                scopes,
                display_name=display_name,
            ).model_dump_json()

            if isinstance(self._runtime, PlatoVMRuntime) and self._runtime.ssh_key_path:
                await run_ssh(
                    self._runtime.ssh_key_path,
                    prepared.hostname,
                    (
                        "cat > /tmp/plato-audit-context.json << 'AUDIT_EOF'\n"
                        f"{context_json}\n"
                        "AUDIT_EOF\n"
                        f"cat > {DEFAULT_TOOL_EXECUTION_CONTEXT_PATH} << 'TOOL_EOF'\n"
                        f"{tool_context_json}\n"
                        "TOOL_EOF\n"
                        f": > {DEFAULT_TOOL_EXECUTION_SPOOL_PATH}\n"
                        f": > {DEFAULT_TOOL_START_SPOOL_PATH}"
                    ),
                    timeout=10,
                )
                logger.debug("Wrote audit and tool execution context to agent VM")

                # Start file watcher sidecar if triggers configured
                if self._file_trigger_patterns and self._trigger_server_url:
                    watch_paths = list({scope.mount_path for scope in scopes})
                    watcher_config = json.dumps(
                        {
                            "server_url": self._trigger_server_url,
                            "patterns": self._file_trigger_patterns,
                            "watch_paths": watch_paths,
                            "poll_interval_s": 2.0,
                        }
                    )
                    await run_ssh(
                        self._runtime.ssh_key_path,
                        prepared.hostname,
                        (
                            f"cat > /tmp/plato-file-watcher-config.json << 'WATCHER_EOF'\n"
                            f"{watcher_config}\n"
                            "WATCHER_EOF\n"
                            "nohup python3 -m plato.utils.file_watcher "
                            "/tmp/plato-file-watcher-config.json "
                            "> /tmp/plato-file-watcher.log 2>&1 &\n"
                            "echo $! > /tmp/plato-file-watcher.pid"
                        ),
                        timeout=10,
                    )
                    logger.info(
                        "Started file watcher sidecar on %s (patterns=%s, server=%s)",
                        prepared.hostname,
                        self._file_trigger_patterns,
                        self._trigger_server_url,
                    )
        except Exception:
            logger.warning("Failed to write audit context to agent VM", exc_info=True)

    async def _read_tool_execution_records(
        self,
        prepared: PreparedAgent,
    ) -> list[ToolExecutionRecord]:
        if not isinstance(self._runtime, PlatoVMRuntime) or self._runtime.ssh_key_path is None:
            return []

        context_exit_code, context_stdout, context_stderr = await run_ssh(
            self._runtime.ssh_key_path,
            prepared.hostname,
            (
                f"echo '=== context ==='; "
                f"if [ -f {DEFAULT_TOOL_EXECUTION_CONTEXT_PATH} ]; then cat {DEFAULT_TOOL_EXECUTION_CONTEXT_PATH}; else echo '<missing>'; fi; "
                f"echo; echo '=== spool-meta ==='; "
                f"if [ -f {DEFAULT_TOOL_EXECUTION_SPOOL_PATH} ]; then ls -l {DEFAULT_TOOL_EXECUTION_SPOOL_PATH}; wc -l {DEFAULT_TOOL_EXECUTION_SPOOL_PATH}; else echo '<missing>'; fi"
            ),
            timeout=10,
        )
        if context_exit_code == 0:
            logger.debug(
                "Tool execution VM state for agent %s:%s%s",
                prepared.agent_id,
                "\n",
                context_stdout,
            )
        else:
            logger.warning(
                "Failed to inspect tool execution VM state for agent %s: %s",
                prepared.agent_id,
                context_stderr,
            )

        exit_code, stdout, stderr = await run_ssh(
            self._runtime.ssh_key_path,
            prepared.hostname,
            (f"if [ -f {DEFAULT_TOOL_EXECUTION_SPOOL_PATH} ]; then cat {DEFAULT_TOOL_EXECUTION_SPOOL_PATH}; fi"),
            timeout=10,
        )
        if exit_code != 0:
            logger.warning(
                "Failed to read tool execution spool from agent VM %s: %s",
                prepared.agent_id,
                stderr,
            )
            return []

        records = parse_tool_execution_records(stdout)
        from collections import Counter

        tool_counts = Counter(r.tool_name for r in records)
        logger.info(
            "Read %d tool execution records from agent VM %s: %s",
            len(records),
            prepared.agent_id,
            dict(tool_counts),
        )
        for record in records:
            logger.info(
                "  spool record: tool=%s span=%s started=%s ended=%s delta_ms=%.1f",
                record.tool_name,
                record.span_id,
                record.started_at.isoformat(),
                record.ended_at.isoformat(),
                (record.ended_at - record.started_at).total_seconds() * 1000,
            )
        return records

    async def _collect_and_store_audit(
        self,
        prepared: PreparedAgent,
        scopes: list[AuditScope],
        *,
        display_name: str | None,
    ) -> None:
        """Collect audit logs from tracked workspace scopes into scoped JSONL spools."""
        try:
            if not isinstance(self._runtime, PlatoVMRuntime):
                return

            if not scopes:
                return

            context = self._audit_context_payload(
                prepared,
                scopes,
                display_name=display_name,
            )
            tool_records = await self._read_tool_execution_records(prepared)
            if tool_records:
                logger.debug(
                    "Read %d tool execution records from agent VM %s: %s",
                    len(tool_records),
                    prepared.agent_id,
                    [
                        {
                            "tool_name": record.tool_name,
                            "trace_id": record.trace_id,
                            "span_id": record.span_id,
                            "started_at": record.started_at.isoformat(),
                            "ended_at": record.ended_at.isoformat(),
                            "path_hints": record.path_hints,
                            "working_directory": record.working_directory,
                            "pid": record.pid,
                            "child_pids": record.child_pids,
                        }
                        for record in tool_records
                    ],
                )
            else:
                logger.debug(
                    "No tool execution records were collected from agent VM %s",
                    prepared.agent_id,
                )
            for scope in scopes:
                await asyncio.to_thread(write_tool_execution_records, scope.tool_spool_path, tool_records)
                logger.debug(
                    "Stored %d tool execution records in %s",
                    len(tool_records),
                    scope.tool_spool_path,
                )
                raw_log = await scope.transport.collect_audit_log(
                    prepared.hostname,
                    audit_key=scope.audit_key,
                )
                if not raw_log:
                    logger.debug(
                        "No audit log data collected from agent VM for scope %s",
                        scope.audit_key,
                    )
                    continue

                # Parse → filter pipeline runs in a thread to avoid blocking
                # the event loop (auparse is C code, pathspec is CPU-bound).
                ignore_spec = await asyncio.to_thread(load_audit_ignore, scope.transport.path)

                def _parse_and_filter(raw: str) -> list[AuditEventInput]:
                    """Parse raw audit log, apply auditignore + mount-root filters.

                    Returns a materialised list because downstream resolution
                    needs random access for time-window attribution.
                    """
                    parsed = parse_audit_raw(raw)
                    filtered = audit_ignore_filter(parsed, ignore_spec, workspace_prefix=scope.mount_path)
                    return [
                        e
                        for e in filtered
                        if not (
                            e.path in (scope.mount_path, scope.mount_path + "/.")
                            and e.operation == Operation.opened_file
                        )
                    ]

                events = await asyncio.to_thread(_parse_and_filter, raw_log)
                if not events:
                    logger.debug(
                        "No audit events after parsing and filtering for scope %s",
                        scope.audit_key,
                    )
                    continue
                logger.info(
                    "Parsed %d audit events for scope %s (agent=%s), time range: %s .. %s",
                    len(events),
                    scope.audit_key,
                    prepared.agent_id,
                    min(e.timestamp for e in events).isoformat(),
                    max(e.timestamp for e in events).isoformat(),
                )

                scope_context = AuditScopeContext(
                    session_id=str(context.get("session_id", "")),
                    agent_id=prepared.agent_id,
                    agent_name=str(context.get("agent_name", "")),
                    display_name=str(context.get("display_name", "")),
                    workspace_name=scope.workspace_name,
                    audit_run_id=scope.audit_run_id,
                    audit_key=scope.audit_key,
                    trace_id=str(context.get("trace_id", "")),
                    span_id=str(context.get("span_id", "")),
                )
                resolved_events = await asyncio.to_thread(
                    resolve_audit_events_for_scope,
                    events,
                    scope_context=scope_context,
                    tool_records=tool_records,
                )
                from collections import Counter as _ResolvedCounter

                _resolved_tools = _ResolvedCounter(e.tool_name for e in resolved_events)
                logger.info(
                    "Resolved %d audit events for scope %s (agent=%s): tool_attribution=%s",
                    len(resolved_events),
                    scope.audit_key,
                    prepared.agent_id,
                    dict(_resolved_tools),
                )
                await asyncio.to_thread(write_audit_jsonl, scope.spool_path, resolved_events, scope_context)
                logger.debug(
                    "Stored %d audit events in %s",
                    len(resolved_events),
                    scope.spool_path,
                )
        except Exception:
            logger.warning("Failed to collect and store audit log", exc_info=True)

    async def run(
        self,
        instruction: str,
        display_name: str | None = None,
    ) -> str:
        """Run the agent: prepare → hooks → execute (with optional continuation loop) → cleanup.

        Args:
            instruction: Task instruction for the agent.
            display_name: Optional per-run override for the agent display name.

        Returns the agent_id (container name or VM job ID).
        """
        if self._concurrency_semaphore is not None:
            return await self._run_with_semaphore(instruction, display_name)

        return await self._run_impl(instruction, display_name)

    async def _run_with_semaphore(self, instruction: str, display_name: str | None = None) -> str:
        assert self._concurrency_semaphore is not None
        async with self._concurrency_semaphore:
            return await self._run_impl(instruction, display_name)

    async def _run_impl(self, instruction: str, display_name: str | None = None) -> str:
        current_display_name = display_name or self._display_name
        audit_scopes = self._configure_audit_scopes(current_display_name)

        # Read workspace references AFTER _configure_audit_scopes, which may
        # replace them with per-runner copies carrying the correct audit_key.
        ws = self._workspace

        # Set workspaces on VM runtime
        if isinstance(self._runtime, PlatoVMRuntime):
            self._runtime.workspace = ws
            self._runtime.workspaces = self._default_workspaces

        # Derive string path for ctx.workspace (used by DockerRuntime)
        workspace_path = ws.path if ws else None

        runtime_dict = self._agent.runtime.model_dump()
        prep_ctx = AgentContext(
            image=self._agent.image,
            config=self._agent.config,
            instruction="",
            display_name=current_display_name,
            workspace=workspace_path,
            runtime=runtime_dict,
            agent_code_path=self._agent_code_path,
        )
        prepared = await self._runtime.prepare(prep_ctx)
        run_error: Exception | None = None
        final_error: Exception | None = None

        try:
            for hook in self._prepare_hooks:
                await hook(prepared)

            await self._write_audit_context(
                prepared,
                audit_scopes,
                display_name=current_display_name,
            )

            total_attempts = 1 + (self._max_continuations if self._exit_condition else 0)

            for attempt in range(total_attempts):
                is_continuation = attempt > 0
                current_instruction = self._continuation_instruction if is_continuation else instruction

                # Inject continue_session into agent config for continuation
                # runs so the agent can use --continue on the CLI.
                agent_config = self._agent.config
                if is_continuation:
                    agent_config = {**agent_config, "continue_session": True}

                exec_ctx = AgentContext(
                    image=self._agent.image,
                    config=agent_config,
                    instruction=current_instruction,
                    display_name=current_display_name,
                    workspace=workspace_path,
                    runtime=runtime_dict,
                    agent_code_path=self._agent_code_path,
                )

                if is_continuation:
                    logger.info(
                        "Continuation attempt %d/%d: exit condition not met, resuming agent",
                        attempt,
                        self._max_continuations,
                    )

                logger.info("Executing agent on VM %s...", prepared.agent_id)
                await self._runtime.execute(prepared, exec_ctx)
                logger.info("Agent execution completed on VM %s", prepared.agent_id)

                # Capture the execution span ID if the runtime exposes it
                if hasattr(self._runtime, "last_execution_span_id"):
                    self.last_execution_span_id = str(self._runtime.last_execution_span_id)

                # If no exit condition configured, one-shot — break immediately
                if self._exit_condition is None:
                    break

                # Check exit condition (workspace is synced back after execute())
                if await self._exit_condition():
                    logger.info("Exit condition met after attempt %d", attempt + 1)
                    break

                if attempt == total_attempts - 1:
                    logger.warning(
                        "Exit condition not met after %d attempt(s) (max_continuations=%d)",
                        total_attempts,
                        self._max_continuations,
                    )
        except Exception as exc:
            run_error = exc
            logger.exception("Agent run failed on VM %s", prepared.agent_id)
        finally:
            # Kill file watcher sidecar if started
            if self._file_trigger_patterns and self._trigger_server_url:
                try:
                    if isinstance(self._runtime, PlatoVMRuntime) and self._runtime.ssh_key_path:
                        await run_ssh(
                            self._runtime.ssh_key_path,
                            prepared.hostname,
                            "if [ -f /tmp/plato-file-watcher.pid ]; then "
                            "kill $(cat /tmp/plato-file-watcher.pid) 2>/dev/null; "
                            "rm -f /tmp/plato-file-watcher.pid; fi",
                            timeout=5,
                        )
                except Exception:
                    logger.debug("Failed to stop file watcher sidecar", exc_info=True)

            await self._collect_and_store_audit(
                prepared,
                audit_scopes,
                display_name=current_display_name,
            )

            try:
                for hook in self._post_run_hooks:
                    await hook(prepared)
            except Exception as exc:
                if run_error is None:
                    final_error = exc
                logger.exception("Post-run hook failed on VM %s", prepared.agent_id)

            logger.info("Cleaning up agent VM %s", prepared.agent_id)
            try:
                await self._runtime.cleanup(
                    prepared.agent_id,
                    error=run_error is not None or final_error is not None,
                )
            except Exception as exc:
                if run_error is not None or final_error is not None:
                    logger.warning(
                        "Agent VM cleanup failed while handling a prior error for %s",
                        prepared.agent_id,
                        exc_info=True,
                    )
                else:
                    final_error = exc

        if run_error is not None:
            raise run_error.with_traceback(run_error.__traceback__)
        if final_error is not None:
            raise final_error.with_traceback(final_error.__traceback__)

        logger.info("Agent run complete: %s", prepared.agent_id)
        return prepared.agent_id


async def run_agent(
    agent: AgentConfig,
    instruction: str,
    display_name: str | None = None,
    workspace: str | None = None,
    session: Session | None = None,
    ssh_key_path: Path | None = None,
    local_agent_path: Path | None = None,
) -> str:
    """Run an agent in a Docker container or VM (one-shot convenience function).

    Args:
        agent: Agent configuration (image, runtime, config)
        instruction: Task instruction for the agent
        workspace: Docker volume name (docker) or path to sync (vm)
        session: Plato session (required for VM mode)
        ssh_key_path: SSH key for rsync to VM (vm mode)
        local_agent_path: Path to agent code on world VM for syncing (vm mode)

    Returns:
        Container name (docker) or job ID (vm)
    """
    ctx = AgentContext(
        image=agent.image,
        config=agent.config,
        instruction=instruction,
        display_name=display_name,
        workspace=workspace,
        agent_code_path=local_agent_path,
    )
    runtime = create_runtime(agent, session=session, ssh_key_path=ssh_key_path)
    return await runtime.run(ctx)


# =============================================================================
# CLI for running agents inside VMs
# =============================================================================


def discover_agents() -> None:
    """Discover and load installed agent packages via entry points."""
    from plato.utils.discovery import discover_plugins

    discover_plugins("plato.agents")


async def _run_agent_cli(instruction: str, tools_path: str | None = None) -> None:
    """Run an agent with config from environment."""
    from plato.agents.base import get_registered_agents
    from plato.otel import instrument, shutdown_tracing

    # Debug: show OTEL config
    otel_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    session_id = os.environ.get("SESSION_ID")
    print(f"[agent-runner] OTEL_EXPORTER_OTLP_ENDPOINT={otel_endpoint}", flush=True)
    print(f"[agent-runner] SESSION_ID={session_id}", flush=True)

    # Initialize OTEL tracing if configured
    instrument("agent")

    # Instrument VM system metrics (CPU/memory) if OTEL is configured
    job_id = os.environ.get("JOB_ID", "")
    if otel_endpoint and session_id:
        from plato.vm_metrics import instrument_system_metrics

        instrument_system_metrics(
            otlp_endpoint=otel_endpoint,
            session_id=session_id,
            env_alias="agent",
            job_id=job_id,
        )

    # Load config from env
    config_b64 = os.environ.get("AGENT_CONFIG_B64")
    if not config_b64:
        raise ValueError("AGENT_CONFIG_B64 environment variable required")

    config_dict = json.loads(base64.b64decode(config_b64).decode())

    discover_agents()
    agent_cls = _load_registered_agent_cls(get_registered_agents())

    # Create agent and set config
    agent = agent_cls()
    config_class = agent_cls.get_config_class()
    agent.config = config_class(**config_dict)

    try:
        await agent.run(instruction, tools_path=tools_path)
    finally:
        from plato.vm_metrics import shutdown_metrics

        await shutdown_metrics()
        shutdown_tracing()


def _load_registered_agent_cls(
    registered_agents: dict[str, type[BaseAgent]],
) -> type[BaseAgent]:
    """Return the single agent class exposed by the current agent package."""
    if not registered_agents:
        raise ValueError("No agents registered")

    agent_name = list(registered_agents.keys())[0]
    agent_cls = registered_agents.get(agent_name)
    if not agent_cls:
        raise ValueError(f"Agent '{agent_name}' not found")
    return agent_cls


def _reset_commands_cli(workspace_paths: list[str]) -> None:
    """Print pooled-VM reset commands for the installed agent package."""
    from plato.agents.base import get_registered_agents

    discover_agents()
    agent_cls = _load_registered_agent_cls(get_registered_agents())
    commands = agent_cls.reset_commands(workspace_paths)
    print(json.dumps(commands))


def main() -> None:
    """CLI entry point for plato-agent-runner."""
    import argparse

    parser = argparse.ArgumentParser(description="Run Plato agents")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run an agent")
    run_parser.add_argument("--instruction", "-i", help="Task instruction")
    run_parser.add_argument("--instruction-b64", help="Base64 encoded instruction")
    run_parser.add_argument("--tools-path", help="Path to pickled plato tools (.pkl)")
    run_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")

    reset_parser = subparsers.add_parser("reset-commands", help="Print pooled VM reset commands as JSON")
    reset_parser.add_argument(
        "--workspace-paths",
        nargs="*",
        default=[],
        help="Workspace mount paths to clean before reusing the VM",
    )

    args = parser.parse_args()

    if args.command == "run":
        log_level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )
        # Silence noisy httpx logs
        logging.getLogger("httpx").setLevel(logging.WARNING)

        # Get instruction (b64 takes precedence)
        if args.instruction_b64:
            instruction = base64.b64decode(args.instruction_b64).decode()
        elif args.instruction:
            instruction = args.instruction
        else:
            parser.error("--instruction or --instruction-b64 required")

        asyncio.run(_run_agent_cli(instruction, tools_path=args.tools_path))
    elif args.command == "reset-commands":
        try:
            _reset_commands_cli(args.workspace_paths)
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            raise SystemExit(1) from exc
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
