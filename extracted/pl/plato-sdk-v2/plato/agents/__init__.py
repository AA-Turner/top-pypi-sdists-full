"""Plato agent framework.

Provides base classes and utilities for building and running agents.

Base Classes:
    - BaseAgent: Abstract base class for agents
    - AgentConfig: Base configuration class
    - Secret: Annotation marker for secrets

Registry:
    - register_agent: Decorator to register an agent
    - get_agent: Get an agent by name
    - get_registered_agents: Get all registered agents

Runner:
    - run_agent: Run agents in Plato VMs

OTel Tracing:
    - instrument: Initialize OTel tracing from environment
    - get_tracer: Get a tracer for creating spans

Example (direct execution):
    from plato.agents import BaseAgent, AgentConfig, Secret, register_agent
    from typing import Annotated

    class MyAgentConfig(AgentConfig):
        model_name: str = "anthropic/claude-sonnet-4"
        api_key: Annotated[str, Secret(description="API key")]

    @register_agent("my-agent")
    class MyAgent(BaseAgent[MyAgentConfig]):
        name = "my-agent"
        description = "My custom agent"

        async def run(self, instruction: str) -> None:
            # Agent implementation
            ...

Example (VM execution):
    from plato.agents import run_agent

    job_id = await run_agent(
        image="my-agent:latest",
        config={"model_name": "anthropic/claude-sonnet-4", "api_key": "sk-..."},
        instruction="Fix the bug",
    )
"""

from __future__ import annotations

__all__ = [
    # Config
    "AgentConfig",
    "Runtime",
    "RuntimeConfig",
    "Secret",
    "VMResources",
    "VMRuntimeConfig",
    # Base
    "BaseAgent",
    "ConfigT",
    "register_agent",
    "get_agent",
    "get_registered_agents",
    # Runner
    "run_agent",
    "AgentRunner",
    "ParallelAgentOrchestrator",
    "ParallelAgentResult",
    "WarmPool",
    "PooledVM",
    # OTel tracing
    "init_tracing",
    "instrument",
    "shutdown_tracing",
    "get_tracer",
    "is_initialized",
]

from plato.agents.base import (
    BaseAgent,
    ConfigT,
    get_agent,
    get_registered_agents,
    register_agent,
)
from plato.agents.config import AgentConfig
from plato.agents.parallel import ParallelAgentOrchestrator, ParallelAgentResult
from plato.agents.runner import AgentRunner, run_agent
from plato.agents.runtime import PooledVM, WarmPool
from plato.markers import Secret
from plato.otel import (
    get_tracer,
    init_tracing,
    instrument,
    is_initialized,
    shutdown_tracing,
)
from plato.runtime import (
    Runtime,
    RuntimeConfig,
    VMResources,
    VMRuntimeConfig,
)
