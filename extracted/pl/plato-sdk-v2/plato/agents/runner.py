"""Agent runner - run agents in Docker containers or VMs."""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TYPE_CHECKING

from plato.agents.runtime import DockerRuntime, PlatoVMRuntime
from plato.agents.runtime.base import AgentContext, PreparedAgent, Runtime
from plato.agents.runtime.transport import Transport
from plato.agents.runtime.vm import VMConfig
from plato.runtime import VMRuntimeConfig

if TYPE_CHECKING:
    from plato.v2.async_.session import Session
    from plato.worlds.config import AgentConfig

logger = logging.getLogger(__name__)


def create_runtime(
    agent: AgentConfig,
    session: Session | None = None,
    ssh_key_path: Path | None = None,
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
        workspace: Transport | None = None,
        workspaces: list[Transport] | None = None,
        agent_containers: list[str] | None = None,
        agent_code_path: Path | None = None,
    ):
        self._agent = agent
        self._runtime = runtime
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

    async def run(
        self,
        instruction: str,
        workspace: Transport | str | None = None,
        mount_path: str | None = None,
        workspaces: list[Transport] | None = None,
    ) -> str:
        """Run the agent: prepare → hooks → execute (with optional continuation loop) → cleanup.

        Args:
            instruction: Task instruction for the agent.
            workspace: Primary workspace. Accepts a Transport object or a host path string.
            mount_path: Where to mount the primary workspace on the agent VM.
                Defaults to the same path as on the host.
            workspaces: Additional workspaces to mount on the agent VM.
                Each workspace's mount_path determines where it appears on the agent.

        Returns the agent_id (container name or VM job ID).
        """
        ws = self._workspace
        if workspace is not None:
            if isinstance(workspace, str):
                if self._workspace is not None:
                    ws = self._workspace.with_path(workspace)
                else:
                    raise RuntimeError("No transport configured — cannot create workspace from path string")
            else:
                ws = workspace
        if mount_path and ws:
            ws.mount_path = mount_path

        # Set workspaces on VM runtime
        all_workspaces = workspaces or self._default_workspaces
        if isinstance(self._runtime, PlatoVMRuntime):
            self._runtime.workspace = ws
            self._runtime.workspaces = all_workspaces

        # Derive string path for ctx.workspace (used by DockerRuntime)
        workspace_path = ws.path if ws else None

        runtime_dict = self._agent.runtime.model_dump()
        prep_ctx = AgentContext(
            image=self._agent.image,
            config=self._agent.config,
            instruction="",
            workspace=workspace_path,
            runtime=runtime_dict,
            agent_code_path=self._agent_code_path,
        )
        prepared = await self._runtime.prepare(prep_ctx)

        try:
            for hook in self._prepare_hooks:
                await hook(prepared)

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

            for hook in self._post_run_hooks:
                await hook(prepared)
        except Exception:
            logger.exception("Agent run failed on VM %s", prepared.agent_id)
            await self._runtime.cleanup(prepared.agent_id, error=True)
            raise
        else:
            logger.info("Cleaning up agent VM %s", prepared.agent_id)
            await self._runtime.cleanup(prepared.agent_id)

        logger.info("Agent run complete: %s", prepared.agent_id)
        return prepared.agent_id


async def run_agent(
    agent: AgentConfig,
    instruction: str,
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
    from plato.agents.base import get_agent, get_registered_agents
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

    # Discover agents
    discover_agents()

    # Get agent class
    agents = get_registered_agents()
    if not agents:
        raise ValueError("No agents registered")

    # Use first registered agent (typically only one per package)
    agent_name = list(agents.keys())[0]
    agent_cls = get_agent(agent_name)
    if not agent_cls:
        raise ValueError(f"Agent '{agent_name}' not found")

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
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
