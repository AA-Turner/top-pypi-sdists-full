"""World-side agent task orchestration."""

from __future__ import annotations

import asyncio
import logging
import os
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from opentelemetry import trace

from plato.agents import vm_setup
from plato.agents.audit import (
    collect_and_store_audit_results,
    prepare_audited_mounts,
    write_audit_context,
)
from plato.agents.browser_tooling import build_agent_browser_sessions_block
from plato.agents.context import AgentContext
from plato.agents.login_backends import resolve_login_backend
from plato.agents.mounts import AgentWorkspaceMount
from plato.runtimes.base import Runtime, RuntimeInfo
from plato.tools.mcp import scoped_mcp_url
from plato.tools.request_context import (
    ToolRequestContext,
    register_client_context,
    unregister_client_context,
)
from plato.utils.subprocess import run_ssh

if TYPE_CHECKING:
    from plato.agents.execution import AgentExecutionManager
    from plato.agents.warmpool import WarmPool
    from plato.v2.async_.session import Session
    from plato.worlds.config import AgentConfig

logger = logging.getLogger(__name__)


def create_agent_runtime(
    agent: AgentConfig,
    session: Session | None = None,
    ssh_key_path: Path | None = None,
) -> Runtime:
    """Create a Runtime for agent execution based on agent config."""
    from plato.runtimes import create_runtime

    # Agent image lives on the AgentConfig, not the runtime config.
    # Copy the runtime config with the agent's image so create_runtime gets it.
    runtime_cfg = agent.runtime.model_copy(update={"image": agent.image})
    return create_runtime(runtime_cfg, session=session, ssh_key_path=ssh_key_path)


class AgentTask:
    """Builder for running agents with optional lifecycle hooks.

    Usage:
        # One-shot (simple)
        await AgentTask(agent_config, runtime).run(instruction)

        # Two-phase with hooks
        await (
            AgentTask(agent_config, runtime)
            .on_prepare(async_login_fn)
            .run(instruction)
        )

    Execution: start runtime → install code → mount workspaces → hooks → execute → cleanup.
    """

    def __init__(
        self,
        agent: AgentConfig,
        runtime: Runtime,
        display_name: str | None = None,
        mounts: list[AgentWorkspaceMount] | None = None,
        agent_containers: list[str] | None = None,
        agent_code_path: Path | None = None,
        warm_pool: WarmPool | None = None,
        session: Session | None = None,
        world_runtime_info: RuntimeInfo | None = None,
        review_exhaustion_policy: Literal["fail", "merge", "raise"] = "fail",
    ):
        self._agent = agent
        self._runtime = runtime
        self._session = session
        self._display_name = display_name
        self._mounts = mounts or []
        self._prepare_hooks: list[Callable[[RuntimeInfo], Awaitable[None]]] = []
        self._post_run_hooks: list[Callable[[RuntimeInfo], Awaitable[None]]] = []
        self._agent_containers = agent_containers
        self._agent_code_path = agent_code_path
        self._warm_pool = warm_pool
        self._world_runtime_info = world_runtime_info
        # Set during _run_on_runtime so exit conditions / hooks can access the agent VM
        self.runtime_info: RuntimeInfo | None = None
        # Continuation loop settings (set via with_continuation())
        self._exit_condition: Callable[[], Awaitable[bool]] | None = None
        self._max_continuations: int = 2
        self._continuation_instruction: str | Callable[[], str] = "Continue. Complete all remaining work."
        self._continuation_exhausted_hook: Callable[[], Awaitable[None]] | None = None
        self._continuation_cap_cost: Callable[[], float] | None = None
        # Optional `/compact <instructions>` message sent to the live session
        # after each execution and before the exit condition runs (see
        # _run_session_compaction). None disables it.
        self._compaction_instruction: str | Callable[[], str] | None = None
        self.continuation_exhausted: bool = False
        # File trigger settings (set via with_file_triggers_from())
        self._file_trigger_patterns: list[str] | None = None
        self._trigger_server_url: str | None = None
        # Populated after run() completes — hex span ID of the agent.execution.output span
        self.last_execution_span_id: str = ""
        # Shared executor — set by BaseWorld.agent() when AgentConfig.max_parallel is set
        self._execution_manager: AgentExecutionManager | None = None
        # Per-task review gate settings (set by BaseWorld.agent())
        self._review_fn: Callable[..., Awaitable[Any]] | None = None
        self._max_review_continuations: int = 2
        self._review_exhaustion_policy: Literal["fail", "merge", "raise"] = review_exhaustion_policy
        # Optional `/compact <instructions>` text run before each review when this
        # task has a review gate (set by BaseWorld.agent()).
        self._review_compaction_instruction: str | Callable[[], str] | None = None
        # Set to True by the execution manager after a successful merge to main
        self.merged: bool = False
        # Set when a review-exhaustion policy force-merges the branch.
        self.review_exhaustion_force_merged: bool = False

    def on_prepare(self, fn: Callable[[RuntimeInfo], Awaitable[None]]) -> AgentTask:
        """Register a hook that runs after the environment is ready but before the agent task.

        The hook receives a RuntimeInfo with hostname for networking
        (e.g., to connect to Chrome CDP at `http://{info.hostname}:9224`).
        """
        self._prepare_hooks.append(fn)
        return self

    def on_post_run(self, fn: Callable[[RuntimeInfo], Awaitable[None]]) -> AgentTask:
        """Register a hook that runs after the agent finishes but before the VM is torn down.

        The hook receives the same RuntimeInfo, so you can still SSH into the
        agent VM (e.g., to collect artifacts, run validation, or read results).
        """
        self._post_run_hooks.append(fn)
        return self

    def with_continuation(
        self,
        exit_condition: Callable[[], Awaitable[bool]],
        max_continuations: int = 2,
        continuation_instruction: str | Callable[[], str] = "Continue. Complete all remaining work.",
        on_exhausted: Callable[[], Awaitable[None]] | None = None,
        continuation_cap_cost: Callable[[], float] | None = None,
        compaction_instruction: str | Callable[[], str] | None = None,
    ) -> AgentTask:
        """Configure a continuation loop for resilient agent execution.

        When configured, the runner will re-invoke the agent (using ``--continue``
        to resume its Claude Code session) up to *max_continuations* additional
        times if *exit_condition* returns ``False`` after an execution.

        The VM is started once and kept alive across all attempts. Transport
        sync-back happens after each execution, so the exit condition
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
        self._continuation_exhausted_hook = on_exhausted
        self._continuation_cap_cost = continuation_cap_cost
        self._compaction_instruction = compaction_instruction
        return self

    async def _run_session_compaction(
        self,
        *,
        info: Any,
        run_agent_config: dict[str, Any],
        runtime_dict: dict[str, Any],
        runner_path: str,
        workdir: str,
        current_display_name: str | None,
    ) -> None:
        """Send a ``/compact <instructions>`` message to the live agent session.

        Invoked right after an execution and before the exit condition (review)
        runs, so it reaches the server while the session's prompt cache is still
        warm. It resumes the session (``continue_session=True``) with the compaction
        text as the only message; the agent compacts and ends the turn. Best-effort:
        any failure is logged and swallowed so the build/review loop keeps going.
        """
        instruction_source = self._compaction_instruction
        if instruction_source is None:
            return
        try:
            # Resolve the (possibly callable) instruction inside the try so a
            # raising callable is swallowed too — compaction is best-effort and
            # must never abort the continuation/review loop.
            compaction_text = instruction_source() if callable(instruction_source) else instruction_source
            if not compaction_text:
                return
            exec_ctx = AgentContext(
                image=self._agent.image,
                package=self._agent.package,
                config={**run_agent_config, "continue_session": True},
                instruction=compaction_text,
                display_name=current_display_name,
                ssh_probe_timeout=self._agent.ssh_probe_timeout,
                ssh_probe_retries=self._agent.ssh_probe_retries,
                runtime=runtime_dict,
                agent_code_path=self._agent_code_path,
            )
            logger.info(
                "Compacting agent session before review (cache-warm) on VM %s",
                info.runtime_id,
            )
            # Deliberately not stored as last_execution_span_id — the build
            # execution span, not this maintenance compaction, is the one
            # downstream review/audit logic cares about.
            await vm_setup.execute_agent(info, exec_ctx, runner_path, workdir)
        except Exception:
            logger.warning(
                "Mid-session compaction failed; continuing without it",
                exc_info=True,
            )

    def with_file_triggers_from(self, ctx: object) -> AgentTask:
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

    def _all_mounts(self) -> list[AgentWorkspaceMount]:
        """Return mounts without duplicates."""
        mounts: list[AgentWorkspaceMount] = []
        seen: set[tuple[str, str, str, str]] = set()
        for mount in self._mounts:
            if mount is None:
                continue
            marker = (
                mount.workspace_name,
                str(mount.world_path),
                mount.agent_path,
                mount.transport_kind,
            )
            if marker in seen:
                continue
            seen.add(marker)
            mounts.append(mount)
        return mounts

    def _build_run_agent_config(
        self,
        info: RuntimeInfo,
        mounts: list[AgentWorkspaceMount],
    ) -> dict[str, object]:
        config: dict[str, object] = dict(self._agent.config or {})
        mcp_server_url = config.get("mcp_server_url")
        if isinstance(mcp_server_url, str) and mcp_server_url:
            config["mcp_server_url"] = scoped_mcp_url(
                mcp_server_url,
                client_id=info.runtime_id,
            )
        config["plato_mounts"] = [mount.to_payload().model_dump() for mount in mounts]
        if self._agent.browser_tooling and resolve_login_backend(self._agent.package) == "agent_browser":
            config.setdefault("browser_tooling", True)
        return config

    async def _run_pre_login(self, info: RuntimeInfo) -> None:
        """Run pre-agent login against each env in ``self._session``.

        Gated on ``AgentConfig.browser_tooling``. The backend (CDP vs.
        agent-browser) is resolved from the agent package — the world
        doesn't need to know which protocol its agent ships.

        Runs after ``on_prepare`` hooks so world-specific groundwork (display
        resize, session recording) can complete before login fires.
        """
        if self._session is None:
            logger.debug("pre-login skipped: no session attached to AgentTask")
            return
        if not self._session.envs:
            logger.debug("pre-login skipped: session has no envs")
            return

        backend = resolve_login_backend(self._agent.package)
        if backend is None:
            raise RuntimeError(
                f"pre-login requested for package {self._agent.package!r} "
                "but no login backend is registered for it. Add it to "
                "plato.agents.login_backends._PACKAGE_LOGIN_BACKENDS."
            )

        flow = self._agent.pre_login_flow
        env_alias = self._agent.pre_login_env_alias

        if backend == "agent_browser":
            if info.ssh_key_path is None:
                raise RuntimeError("agent-browser pre-login needs ssh_key_path on RuntimeInfo")
            await self._session.login_via_agent_browser(
                hostname=info.hostname,
                ssh_key_path=info.ssh_key_path,
                flow=flow,
                env_alias=env_alias,
                retries=3,
                retry_delay_ms=2000,
                log=logger,
            )
            return

        # CDP — connect once, log in, stabilize (reload + stray-tab cleanup)
        # so the downstream agent that shares this Chrome lands on the
        # logged-in page.
        await self._session.login_via_cdp(
            cdp_url=f"http://{info.hostname}:9224",
            flow=flow,
            env_alias=env_alias,
            retries=3,
            retry_delay_ms=2000,
            log=logger,
        )

    def _maybe_append_sessions_block(self, instruction: str) -> str:
        """Append the ``agent-browser`` ``--session`` map when relevant.

        Only fires for packages that use the ``agent_browser`` login backend
        (claude-code / gemini-cli / codex) — other packages don't ship the CLI
        that reads those session names.
        """
        if self._session is None:
            return instruction
        if resolve_login_backend(self._agent.package) != "agent_browser":
            return instruction
        aliases = [env.alias for env in self._session.envs if env.artifact_id]
        return instruction + build_agent_browser_sessions_block(aliases)

    def _register_tool_request_context(
        self,
        info: RuntimeInfo,
        *,
        instruction: str,
        display_name: str | None,
        attempt: int,
    ) -> None:
        register_client_context(
            ToolRequestContext(
                client_id=info.runtime_id,
                hostname=info.hostname,
                display_name=display_name,
                instruction=instruction,
                session_id=os.environ.get("SESSION_ID"),
                image=self._agent.image,
                attempt=attempt,
            )
        )

    async def run(
        self,
        instruction: str,
        display_name: str | None = None,
    ) -> str:
        """Run the agent: start VM → setup → execute (with optional continuation) → cleanup.

        Args:
            instruction: Task instruction for the agent.
            display_name: Optional per-run override for the agent display name.

        Returns the runtime_id (VM alias).
        """
        if self._execution_manager is not None:
            return await self._execution_manager.run(self, instruction, display_name)
        if self._warm_pool is not None:
            return await self._run_with_warm_pool(instruction, display_name)

        return await self._run_impl(instruction, display_name)

    async def _run_with_warm_pool(self, instruction: str, display_name: str | None = None) -> str:
        assert self._warm_pool is not None
        mounts = [mount.clone_for_run() for mount in self._all_mounts()]
        pooled_runtime = await self._warm_pool.acquire()
        try:
            agent_id = await self._run_on_runtime(
                pooled_runtime.runtime_info,
                instruction,
                display_name=display_name,
                mounts=mounts,
            )
        except Exception:
            await self._warm_pool.release(
                pooled_runtime,
                workspace_paths=[mount.agent_path for mount in mounts],
                destroy=True,
            )
            raise

        await self._warm_pool.release(
            pooled_runtime,
            workspace_paths=[mount.agent_path for mount in mounts],
        )
        return agent_id

    async def _run_impl(self, instruction: str, display_name: str | None = None, *, _retries: int = 2) -> str:
        last_error: Exception | None = None
        for attempt in range(1, _retries + 1):
            current_display_name = display_name or self._display_name
            mounts = [mount.clone_for_run() for mount in self._all_mounts()]
            alias = vm_setup.make_agent_alias(current_display_name)
            info = await self._runtime.start(alias=alias)
            try:
                return await self._run_on_runtime(
                    info,
                    instruction,
                    display_name=display_name,
                    mounts=mounts,
                )
            except RuntimeError as exc:
                if "Permission denied (publickey)" in str(exc) and attempt < _retries:
                    logger.warning(
                        "SSH auth failed on %s (attempt %d/%d), retrying with fresh VM",
                        info.runtime_id,
                        attempt,
                        _retries,
                    )
                    last_error = exc
                else:
                    raise
            finally:
                logger.info("Cleaning up agent VM %s", info.runtime_id)
                try:
                    await self._runtime.stop(info.runtime_id)
                except Exception:
                    logger.warning("Failed to clean up agent VM %s", info.runtime_id, exc_info=True)
        raise last_error  # type: ignore[misc]

    async def _run_on_runtime(
        self,
        info: RuntimeInfo,
        instruction: str,
        *,
        display_name: str | None,
        mounts: list[AgentWorkspaceMount],
    ) -> str:
        self.runtime_info = info
        current_display_name = display_name or self._display_name
        mounts, audited_mounts = prepare_audited_mounts(mounts)

        runtime_dict = self._agent.runtime.model_dump()
        run_error: Exception | None = None
        final_error: Exception | None = None

        try:
            # Code sync + env setup are independent SSH operations — run concurrently.
            agent_ctx = AgentContext(
                image=self._agent.image,
                package=self._agent.package,
                config=self._agent.config,
                instruction="",
                display_name=current_display_name,
                ssh_probe_timeout=self._agent.ssh_probe_timeout,
                ssh_probe_retries=self._agent.ssh_probe_retries,
                runtime=runtime_dict,
                agent_code_path=self._agent_code_path,
            )
            await asyncio.gather(
                vm_setup.install_agent_code(info, agent_ctx),
                vm_setup.setup_agent_env(info, self._session, self._world_runtime_info),
            )

            # Resolve runner path (needs agent code installed)
            runner_path = await vm_setup.resolve_runner_path(info)

            # Mount workspaces
            await vm_setup.setup_workspaces(info, mounts)

            # Prepare hooks
            for hook in self._prepare_hooks:
                await hook(info)

            # Declarative pre-agent login — runs after world-specific setup
            # (display resize, recorder) so hooks can finish any groundwork
            # the login backend depends on.
            if self._agent.browser_tooling:
                await self._run_pre_login(info)
                # agent-browser login stores each env's cookies under
                # --session <env.alias>. The model only knows to pass that
                # name if we list it, so append the session map to the
                # task instruction.
                instruction = self._maybe_append_sessions_block(instruction)

            run_agent_config = self._build_run_agent_config(info, mounts)
            workdir = mounts[0].agent_path if mounts else "/workspace"

            self.continuation_exhausted = False

            tracer = trace.get_tracer("plato.agents.task")
            task_attrs = {
                "plato.agent.task_id": info.runtime_id,
                "plato.task.type": "agent",
            }
            if current_display_name:
                task_attrs["plato.task.display_name"] = current_display_name

            with tracer.start_as_current_span("agent.task", attributes=task_attrs) as task_span:
                # Write audit/tool-execution context with `agent.task` as the
                # current span — out-of-band hooks (e.g. claude-code's
                # PostToolUse) load this file and parent their spans to the
                # captured span_id, so writing it inside the agent.task scope
                # keeps those spans nested in the agent subtree.
                await write_audit_context(
                    info,
                    audited_mounts,
                    agent_image=self._agent.image,
                    default_display_name=self._display_name,
                    display_name=current_display_name,
                    watch_paths=list({mount.mount_path for mount in mounts}),
                    file_trigger_patterns=self._file_trigger_patterns,
                    trigger_server_url=self._trigger_server_url,
                )
                attempt = 0
                used_continuation_budget = 0.0
                while True:
                    is_continuation = attempt > 0
                    task_span.set_attribute("plato.agent.attempts", attempt + 1)
                    if is_continuation:
                        ci = self._continuation_instruction
                        current_instruction = ci() if callable(ci) else ci
                    else:
                        current_instruction = instruction
                    self._register_tool_request_context(
                        info,
                        instruction=current_instruction,
                        display_name=current_display_name,
                        attempt=attempt + 1,
                    )

                    # Inject continue_session into agent config for continuation
                    agent_config = dict(run_agent_config)
                    if is_continuation:
                        agent_config = {**agent_config, "continue_session": True}

                    exec_ctx = AgentContext(
                        image=self._agent.image,
                        package=self._agent.package,
                        config=agent_config,
                        instruction=current_instruction,
                        display_name=current_display_name,
                        ssh_probe_timeout=self._agent.ssh_probe_timeout,
                        ssh_probe_retries=self._agent.ssh_probe_retries,
                        runtime=runtime_dict,
                        agent_code_path=self._agent_code_path,
                    )

                    if is_continuation:
                        logger.info(
                            "Continuation attempt %d/%s: exit condition not met, resuming agent",
                            attempt,
                            self._max_continuations,
                        )

                    logger.info("Executing agent on VM %s...", info.runtime_id)
                    span_id = await vm_setup.execute_agent(info, exec_ctx, runner_path, workdir)
                    self.last_execution_span_id = span_id
                    logger.info("Agent execution completed on VM %s", info.runtime_id)

                    # Sync workspaces back after execution
                    await vm_setup.sync_back_workspaces(info, mounts)

                    # If no exit condition configured, one-shot — break immediately
                    if self._exit_condition is None:
                        break

                    # Compact the just-exited session BEFORE the (multi-minute)
                    # review runs, while its prompt cache is still warm on the
                    # server. This keeps the continued session small for the next
                    # attempt and makes the compaction's own summarization call
                    # cheap (it reads cache-hot context). Best-effort — a
                    # compaction failure must not abort the build/review loop.
                    if self._compaction_instruction is not None:
                        await self._run_session_compaction(
                            info=info,
                            run_agent_config=run_agent_config,
                            runtime_dict=runtime_dict,
                            runner_path=runner_path,
                            workdir=workdir,
                            current_display_name=current_display_name,
                        )

                    # Check exit condition (workspace is synced back after execute())
                    if await self._exit_condition():
                        logger.info("Exit condition met after attempt %d", attempt + 1)
                        break

                    cap_cost = 1.0
                    if self._continuation_cap_cost is not None:
                        cap_cost = float(self._continuation_cap_cost())

                    if cap_cost <= 0:
                        logger.info(
                            "Attempt %d did not consume continuation budget (cap_cost=%s); continuing without using review budget",
                            attempt + 1,
                            cap_cost,
                        )
                        attempt += 1
                        continue

                    if used_continuation_budget + cap_cost > float(self._max_continuations):
                        self.continuation_exhausted = True
                        logger.warning(
                            "Exit condition not met after %d attempt(s) (max_continuations=%d, used_budget=%.2f, next_cap_cost=%.2f)",
                            attempt + 1,
                            self._max_continuations,
                            used_continuation_budget,
                            cap_cost,
                        )
                        if self._continuation_exhausted_hook is not None:
                            await self._continuation_exhausted_hook()
                        break

                    used_continuation_budget += cap_cost
                    attempt += 1
        except Exception as exc:
            run_error = exc
            logger.exception("Agent run failed on VM %s", info.runtime_id)
        finally:
            # Kill file watcher sidecar if started
            if self._file_trigger_patterns and self._trigger_server_url:
                try:
                    ssh_key = info.ssh_key_path
                    if ssh_key:
                        await run_ssh(
                            ssh_key,
                            info.hostname,
                            "if [ -f /tmp/plato-file-watcher.pid ]; then "
                            "kill $(cat /tmp/plato-file-watcher.pid) 2>/dev/null; "
                            "rm -f /tmp/plato-file-watcher.pid; fi",
                            timeout=5,
                        )
                except Exception:
                    logger.debug("Failed to stop file watcher sidecar", exc_info=True)

            await collect_and_store_audit_results(
                info,
                audited_mounts,
                agent_image=self._agent.image,
                default_display_name=self._display_name,
                display_name=current_display_name,
            )

            try:
                for hook in self._post_run_hooks:
                    await hook(info)
            except Exception as exc:
                if run_error is None:
                    final_error = exc
                logger.exception("Post-run hook failed on VM %s", info.runtime_id)
            finally:
                unregister_client_context(info.runtime_id)

        if run_error is not None:
            raise run_error.with_traceback(run_error.__traceback__)
        if final_error is not None:
            raise final_error.with_traceback(final_error.__traceback__)

        logger.info("Agent run complete: %s", info.runtime_id)
        return info.runtime_id


async def run_agent(
    agent: AgentConfig,
    instruction: str,
    display_name: str | None = None,
    session: Session | None = None,
    ssh_key_path: Path | None = None,
    local_agent_path: Path | None = None,
) -> str:
    """Run an agent in a VM (one-shot convenience function).

    Args:
        agent: Agent configuration (image, runtime, config)
        instruction: Task instruction for the agent
        session: Plato session (required for VM mode)
        ssh_key_path: SSH key for rsync to VM (vm mode)
        local_agent_path: Path to agent code on world VM for syncing (vm mode)

    Returns:
        VM alias
    """
    rt = create_agent_runtime(agent, session=session, ssh_key_path=ssh_key_path)
    runner = AgentTask(agent, rt, agent_code_path=local_agent_path, display_name=display_name, session=session)
    return await runner.run(instruction)
