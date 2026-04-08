"""World-side agent task orchestration."""

from __future__ import annotations

import asyncio
import logging
import os
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TYPE_CHECKING

from plato.agents import vm_setup
from plato.agents.audit import (
    collect_and_store_audit_results,
    prepare_audited_mounts,
    write_audit_context,
)
from plato.agents.context import AgentContext
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
        # File trigger settings (set via with_file_triggers_from())
        self._file_trigger_patterns: list[str] | None = None
        self._trigger_server_url: str | None = None
        # Populated after run() completes — hex span ID of the agent.execution.output span
        self.last_execution_span_id: str = ""
        # Shared executor — set by BaseWorld.agent() when AgentConfig.max_parallel is set
        self._execution_manager: AgentExecutionManager | None = None

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
        return self

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
        return config

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

            run_agent_config = self._build_run_agent_config(info, mounts)
            workdir = mounts[0].agent_path if mounts else "/workspace"

            total_attempts = 1 + (self._max_continuations if self._exit_condition else 0)

            for attempt in range(total_attempts):
                is_continuation = attempt > 0
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
                    runtime=runtime_dict,
                    agent_code_path=self._agent_code_path,
                )

                if is_continuation:
                    logger.info(
                        "Continuation attempt %d/%d: exit condition not met, resuming agent",
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
