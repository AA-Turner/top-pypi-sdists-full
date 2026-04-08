"""Agent runner CLI — entrypoint for plato-agent-runner on agent VMs."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plato.agents.base import BaseAgent

logger = logging.getLogger(__name__)


def discover_agents() -> None:
    """Discover and load installed agent packages via entry points."""
    from plato.utils.discovery import discover_plugins

    discover_plugins("plato.agents")


async def _run_agent_cli(instruction: str, agent_name: str | None = None) -> None:
    """Run an agent with config from environment."""
    from plato.agents.base import get_registered_agents
    from plato.otel import instrument, shutdown_tracing

    otel_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    session_id = os.environ.get("SESSION_ID")
    print(f"[agent-runner] OTEL_EXPORTER_OTLP_ENDPOINT={otel_endpoint}", flush=True)
    print(f"[agent-runner] SESSION_ID={session_id}", flush=True)

    instrument("agent")

    job_id = os.environ.get("JOB_ID", "")
    if otel_endpoint and session_id:
        from plato.vm_metrics import instrument_system_metrics

        instrument_system_metrics(
            otlp_endpoint=otel_endpoint,
            session_id=session_id,
            env_alias="agent",
            job_id=job_id,
        )

    config_b64 = os.environ.get("AGENT_CONFIG_B64")
    if not config_b64:
        raise ValueError("AGENT_CONFIG_B64 environment variable required")

    from plato.utils.encoding import decode_b64_json

    config_dict = decode_b64_json(config_b64)
    discover_agents()
    agent_cls = _load_registered_agent_cls(get_registered_agents(), agent_name)

    agent = agent_cls()
    config_class = agent_cls.get_config_class()
    agent.config = config_class(**config_dict)
    try:
        await agent.run(instruction)
    finally:
        from plato.vm_metrics import shutdown_metrics

        await shutdown_metrics()
        shutdown_tracing()


def _load_registered_agent_cls(
    registered_agents: dict[str, type[BaseAgent]],
    agent_name: str | None = None,
) -> type[BaseAgent]:
    """Return the requested registered agent class."""
    if not registered_agents:
        raise ValueError("No agents registered")

    if agent_name:
        agent_cls = registered_agents.get(agent_name)
        if not agent_cls:
            available = ", ".join(sorted(registered_agents))
            raise ValueError(f"Agent '{agent_name}' not found. Registered agents: {available or '(none)'}")
        return agent_cls

    if len(registered_agents) != 1:
        available = ", ".join(sorted(registered_agents))
        raise ValueError(
            f"Multiple agents registered but no agent package was specified. Registered agents: {available}"
        )

    agent_name = next(iter(registered_agents))
    agent_cls = registered_agents.get(agent_name)
    if not agent_cls:
        raise ValueError(f"Agent '{agent_name}' not found")
    return agent_cls


def _reset_commands_cli(workspace_paths: list[str], agent_name: str | None = None) -> None:
    """Print pooled-VM reset commands for the installed agent package."""
    from plato.agents.base import get_registered_agents

    discover_agents()
    agent_cls = _load_registered_agent_cls(get_registered_agents(), agent_name)
    commands = agent_cls.reset_commands(workspace_paths)
    print(json.dumps(commands))


def main() -> None:
    """CLI entry point for plato-agent-runner."""
    import argparse

    parser = argparse.ArgumentParser(description="Run Plato agents")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run an agent")
    run_parser.add_argument("--agent-package", help="Registered agent package/name to run")
    run_parser.add_argument("--instruction", "-i", help="Task instruction")
    run_parser.add_argument("--instruction-b64", help="Base64 encoded instruction")
    run_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")

    reset_parser = subparsers.add_parser("reset-commands", help="Print pooled VM reset commands as JSON")
    reset_parser.add_argument("--agent-package", help="Registered agent package/name to inspect")
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
        logging.getLogger("httpx").setLevel(logging.WARNING)

        if args.instruction_b64:
            from plato.utils.encoding import decode_b64

            instruction = decode_b64(args.instruction_b64)
        elif args.instruction:
            instruction = args.instruction
        else:
            parser.error("--instruction or --instruction-b64 required")

        asyncio.run(_run_agent_cli(instruction, args.agent_package))
    elif args.command == "reset-commands":
        try:
            _reset_commands_cli(args.workspace_paths, args.agent_package)
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            raise SystemExit(1) from exc
    else:
        parser.print_help()
