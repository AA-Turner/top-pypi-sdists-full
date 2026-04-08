"""Spec and serialization helpers for runtime-launched agent tests."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, cast

import cloudpickle
from pydantic import BaseModel

from plato.agents.mounts import AgentWorkspaceMountPayload

if TYPE_CHECKING:
    from plato.agents.config import AgentConfig


class AgentTestContext(Protocol):
    """Protocol exposed to injected agent test hooks."""

    config: AgentConfig
    workspace: Path
    workspace_dir: Path
    instruction: str
    mounts: list[AgentWorkspaceMountPayload]
    call_mcp_tool: Callable[..., object] | None


AgentTestHook = Callable[[AgentTestContext], object]


@dataclass(slots=True)
class AgentTestSpec:
    """Host-side spec for a launched agent test."""

    name: str
    run: AgentTestHook


class _SerializedAgentTestSpec(BaseModel):
    name: str
    run_hook_path: str


def dump_agent_test_spec(spec: AgentTestSpec, destination: Path) -> Path:
    """Write a serialized agent test spec bundle and return ``spec.json``."""
    destination.mkdir(parents=True, exist_ok=True)
    run_hook_path = destination / "run.pkl"
    run_hook_path.write_bytes(cloudpickle.dumps(spec.run))

    serialized = _SerializedAgentTestSpec(
        name=spec.name,
        run_hook_path=run_hook_path.name,
    )
    spec_path = destination / "spec.json"
    spec_path.write_text(serialized.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return spec_path


def load_agent_test_spec(spec_path: Path) -> AgentTestSpec:
    """Load a runtime-side agent spec bundle and resolve its hook payload."""
    serialized = _SerializedAgentTestSpec.model_validate_json(spec_path.read_text(encoding="utf-8"))
    hook = cloudpickle.loads((spec_path.parent / serialized.run_hook_path).read_bytes())
    if not callable(hook):
        raise TypeError(f"Serialized hook at {(spec_path.parent / serialized.run_hook_path)} is not callable")

    return AgentTestSpec(
        name=serialized.name,
        run=cast(AgentTestHook, hook),
    )


async def call_agent_test_hook(hook: AgentTestHook, agent: object) -> object | None:
    """Call a serialized agent test hook and await it when needed."""
    result = hook(cast(AgentTestContext, agent))
    if inspect.isawaitable(result):
        return await result
    return result
