"""Spec and serialization helpers for runtime-launched world tests."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Protocol, cast

import cloudpickle
from pydantic import BaseModel, Field

from plato.worlds.config import GitTransportConfig

if TYPE_CHECKING:
    from pydantic import BaseModel as PydanticBaseModel

    from plato.agents.task import AgentTask
    from plato.worlds.config import AgentConfig, RunConfig
    from plato.worlds.workspace import Workspace

JsonValue = dict[str, object] | list[object] | None | bool | int | float | str


class WorldTestContext(Protocol):
    """Protocol exposed to injected world test hooks."""

    config: RunConfig
    state: PydanticBaseModel
    lifecycle: list[str]
    test_result: object | None
    _step_count: int

    def workspace(self, name: str) -> Workspace: ...

    def agent(
        self,
        config: AgentConfig,
        display_name: str | None = None,
        workspaces: list[Workspace] | None = None,
        warm_pool: object | None = None,
        agent_code_path: Path | None = None,
        total_agents: int | None = None,
        review_fn: object | None = None,
        max_review_continuations: int = 2,
        review_exhaustion_policy: Literal["fail", "merge", "raise"] = "fail",
    ) -> AgentTask: ...

    async def checkpoint(self, label: str, *, trigger_span_id: str = "") -> None: ...


WorldTestHook = Callable[[WorldTestContext], object]


class WorldWorkspaceSpec(BaseModel):
    """Workspace declaration for the generic test harness world."""

    name: str
    tracked: bool = False
    mount_path: str | None = None
    relative_path: str | None = None
    dvcignore: list[str] = Field(default_factory=list)
    transport: Literal["nfs_kernel", "sshfs", "git", "rsync"] | None = None
    git_config: GitTransportConfig | None = None
    commit_strategy: Literal["manifest", "archive"] = "manifest"
    source_ref: str | None = None
    """Restore workspace from an existing ref before the test runs.

    Format: ``"session_id:step_name"`` — restores from the given session and step.
    """
    source_repo: str | None = None
    """Workspace repo name to resolve S3 credentials for the source ref.

    Only needed when the source repo differs from the test workspace's own repo
    (e.g. restoring from ``"webclone/stripe/code"`` into a test workspace named ``"code"``).
    """


@dataclass(slots=True)
class WorldTestSpec:
    """Host-side spec for a launched world test."""

    name: str
    workspaces: list[WorldWorkspaceSpec] = field(default_factory=list)
    reset: WorldTestHook | None = None
    step: WorldTestHook | None = None
    close: WorldTestHook | None = None


@dataclass(slots=True)
class LoadedWorldTestSpec:
    """Runtime-loaded world test spec with callables resolved."""

    name: str
    workspaces: list[WorldWorkspaceSpec]
    reset: WorldTestHook | None = None
    step: WorldTestHook | None = None
    close: WorldTestHook | None = None


class WorldTestRunResult(BaseModel):
    """Structured result emitted by the generic harness world."""

    name: str
    step_count: int
    lifecycle: list[str] = Field(default_factory=list)
    workspace_repo_names: dict[str, str] = Field(default_factory=dict)
    test_result: JsonValue = None
    final_result: JsonValue = None


class _SerializedWorldTestSpec(BaseModel):
    name: str
    workspaces: list[WorldWorkspaceSpec] = Field(default_factory=list)
    reset_hook_path: str | None = None
    step_hook_path: str | None = None
    close_hook_path: str | None = None


def dump_world_test_spec(spec: WorldTestSpec, destination: Path) -> Path:
    """Write a serialized world test spec bundle and return ``spec.json``."""
    destination.mkdir(parents=True, exist_ok=True)

    serialized = _SerializedWorldTestSpec(
        name=spec.name,
        workspaces=spec.workspaces,
        reset_hook_path=_dump_hook(destination, "reset", spec.reset),
        step_hook_path=_dump_hook(destination, "step", spec.step),
        close_hook_path=_dump_hook(destination, "close", spec.close),
    )
    spec_path = destination / "spec.json"
    spec_path.write_text(serialized.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return spec_path


def load_world_test_spec(spec_path: Path) -> LoadedWorldTestSpec:
    """Load a runtime-side spec bundle and resolve its hook payloads."""
    serialized = _SerializedWorldTestSpec.model_validate_json(spec_path.read_text(encoding="utf-8"))
    parent = spec_path.parent
    return LoadedWorldTestSpec(
        name=serialized.name,
        workspaces=serialized.workspaces,
        reset=_load_hook(parent, serialized.reset_hook_path),
        step=_load_hook(parent, serialized.step_hook_path),
        close=_load_hook(parent, serialized.close_hook_path),
    )


async def call_world_test_hook(hook: WorldTestHook | None, world: object) -> object | None:
    """Call a serialized world test hook and await it when needed."""
    if hook is None:
        return None
    result = hook(cast(WorldTestContext, world))
    if inspect.isawaitable(result):
        return await result
    return result


def _dump_hook(destination: Path, name: str, hook: WorldTestHook | None) -> str | None:
    if hook is None:
        return None
    hook_path = destination / f"{name}.pkl"
    hook_path.write_bytes(cloudpickle.dumps(hook))
    return hook_path.name


def _load_hook(parent: Path, relative_path: str | None) -> WorldTestHook | None:
    if relative_path is None:
        return None
    hook = cloudpickle.loads((parent / relative_path).read_bytes())
    if not callable(hook):
        raise TypeError(f"Serialized hook at {(parent / relative_path)} is not callable")
    return cast(WorldTestHook, hook)
