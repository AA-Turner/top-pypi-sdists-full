"""Base world class for Plato worlds."""

from __future__ import annotations

import asyncio
import importlib.metadata
import json
import logging
import os
import time
import traceback
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Literal, NoReturn, cast, get_args, get_origin

import httpx
from opentelemetry.trace import StatusCode
from pydantic import BaseModel as PydanticBaseModel
from typing_extensions import TypeVar

from plato.markers import WorkspaceMarker
from plato.otel import aggregate_step_costs, force_flush_tracing, get_tracer
from plato.runtimes.base import RuntimeInfo
from plato.settings import PlatoSettings
from plato.settings import get_settings as get_plato_settings
from plato.utils.versions import get_plato_version
from plato.vm_metrics import instrument_system_metrics
from plato.worlds import handover
from plato.worlds.chronos_mixin import ChronosSessionMixin
from plato.worlds.config import (
    AgentConfig,
    ChronosConfig,
    DecisionConfig,
    DevConfig,
    LLMConfig,
    RunConfig,
)
from plato.worlds.handover import Handoff, HandoffAgent, HandoffRefused, HandoffWorkspace
from plato.worlds.models import (
    Observation,
    StepResult,
)
from plato.worlds.preview_mixin import PreviewMixin
from plato.worlds.runtime_mixin import RuntimeMixin
from plato.worlds.schema import get_world_schema
from plato.worlds.stage_tracking import disable_stage_tracking, enable_stage_tracking
from plato.worlds.tailscale import (
    LocalCommandRunner,
    SshCommandRunner,
    TailscaleError,
    TailscaleNode,
    build_join_plan,
    join_tailnet,
    leave_tailnet,
    resolve_auth_key,
)
from plato.worlds.testing import run_e2e_tests
from plato.worlds.workspace import Workspace

if TYPE_CHECKING:
    from plato.agents.execution import AgentExecutionManager
    from plato.agents.mounts import AgentWorkspaceMount
    from plato.agents.task import AgentTask
    from plato.agents.warmpool import AgentVMBudget, WarmPool
    from plato.decision import DecisionClient
    from plato.llm import LLMClient
    from plato.worlds.result_store import ResultStore

logger = logging.getLogger(__name__)


@dataclass
class ResolvedWorkspaceRepo:
    """Result of resolving a workspace repo via Chronos."""

    s3_bucket: str
    s3_prefix: str
    repo_id: str
    commit_ref: str
    repo_name: str
    chronos_url: str
    api_key: str


class AgentTailnetMember(PydanticBaseModel):
    """An agent VM that joined the tailnet. It logs out after its task (or at world close as a fallback)."""

    info: RuntimeInfo
    node: TailscaleNode
    leave_failed: bool = False
    """True after a failed post-run logout. The leave already removed the managed blocks,
    so the next task on this VM (warm pool) joins again instead of reusing the member."""


WORLD_TAILNET_ROLE = "world"
AGENT_TAILNET_ROLE_PREFIX = "agent-"
# Chars of the agent VM alias (its random suffix) kept in the node hostname.
AGENT_TAILNET_ID_CHARS = 8


# Global registry of worlds
_WORLD_REGISTRY: dict[str, type[BaseWorld]] = {}

# Type variable for config
ConfigT = TypeVar("ConfigT", bound=RunConfig)

# Type variable for typed state (optional, defaults to PydanticBaseModel)
StateT = TypeVar("StateT", bound=PydanticBaseModel, default=PydanticBaseModel)
WorldT = TypeVar("WorldT", bound="BaseWorld")


def register_world(name: str):
    """Decorator to register a world class."""

    def decorator(cls: type[WorldT]) -> type[WorldT]:
        _WORLD_REGISTRY[name] = cls
        logger.debug(f"Registered world: {name} -> {cls.__name__}")
        return cls

    return decorator


def get_registered_worlds() -> dict[str, type[BaseWorld]]:
    """Get all registered worlds."""
    return _WORLD_REGISTRY.copy()


def get_world(name: str) -> type[BaseWorld] | None:
    """Get a world by name."""
    return _WORLD_REGISTRY.get(name)


@cache
def _version_for_top_package(top_package: str) -> str:
    """Version of the distribution that provides ``top_package``, or "0.0.0".

    ``importlib.metadata.packages_distributions()`` walks the file list of every
    installed distribution (~0.3s in a full env) and is re-scanned on every call.
    The installed set cannot change inside a running interpreter, so cache it —
    ``BaseWorld.get_version()`` is called three times per ``run()``.
    """
    for dist_name in importlib.metadata.packages_distributions().get(top_package, []):
        try:
            return importlib.metadata.version(dist_name)
        except importlib.metadata.PackageNotFoundError:
            continue
    return "0.0.0"


def _distribution_for_top_package(top_package: str) -> str | None:
    """The installed distribution that provides ``top_package`` (what Chronos installs), or None."""
    names = importlib.metadata.packages_distributions().get(top_package, [])
    return names[0] if names else None


class BaseWorld(PreviewMixin, RuntimeMixin, ChronosSessionMixin, ABC, Generic[ConfigT, StateT]):
    """Base class for Plato worlds.

    Subclass with a config type parameter for fully typed config access.
    Optionally pass a second type parameter for typed state:

        class CodeWorldConfig(RunConfig):
            repository_url: str
            prompt: str
            coder: Annotated[AgentConfig, Agent(description="Coding agent")]
            git_token: Annotated[str | None, Secret(description="GitHub token")] = None

        @register_world("code")
        class CodeWorld(BaseWorld[CodeWorldConfig]):
            name = "code"
            description = "Run coding agents"

            async def reset(self) -> Observation:
                url = self.config.repository_url  # typed as str
                agent = self.config.coder          # typed as AgentConfig
                token = self.config.git_token      # typed as str | None

    For typed state, define a Pydantic model and pass it as the second generic:

        class MyState(BaseModel):
            current_step: int = 0

        class MyWorld(BaseWorld[MyConfig, MyState]):
            async def reset(self) -> Observation:
                self.state.current_step = 0  # fully typed
    """

    handoff: Handoff | None = None
    """Set when this process took the world over from a previous one in the same session (handover.py): its agents
    to re-attach and its state. None for a world that started fresh."""

    # Class attributes
    name: ClassVar[str] = "base"
    description: ClassVar[str] = ""
    world_type: ClassVar[str] = "world"
    review_models: ClassVar[list[type]] = []  # Set to DEFAULT_REVIEW_MODELS below after class definition
    _state_class: ClassVar[type[PydanticBaseModel] | None] = None

    # Instance attributes
    config: ConfigT  # Typed via generic parameter

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Extract StateT from Generic args
        for base in getattr(cls, "__orig_bases__", []):
            args = get_args(base)
            if len(args) >= 2 and args[1] is not type(None):
                if isinstance(args[1], type) and issubclass(args[1], PydanticBaseModel):
                    cls._state_class = args[1]

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(f"plato.worlds.{self.name}")
        self.config: ConfigT = cast(ConfigT, RunConfig())
        self._step_count: int = 0
        self._session_id: str | None = None
        self._chronos_completed: bool = False
        self._agent_containers: list[str] = []
        self._state: StateT | None = None
        self._workspaces: dict[str, Workspace] = {}
        self._agent_execution_managers: dict[str, AgentExecutionManager] = {}
        # Optional session-wide cap on live agent VMs shared by EVERY execution
        # manager/warm pool this world creates. Per-manager max_parallel bounds
        # each pool individually, but managers are keyed per config/mount shape,
        # so without a shared budget the SUM of retained idle VMs across pools
        # can exceed the session env limit. Worlds that fan out across multiple
        # shapes (e.g. the workflow world) set this in reset().
        self._agent_vm_budget: AgentVMBudget | None = None
        # request_checkpoint() coalescer: one background task per world runs
        # the newest pending label, so a burst of merges gets one checkpoint.
        self._pending_checkpoint_label: str | None = None
        self._requested_checkpoint_task: asyncio.Task[None] | None = None
        # Raised once by flush_requested_checkpoints: the merged tree is not in a checkpoint yet.
        self._requested_checkpoint_error: Exception | None = None
        self._tailscale_world_node: TailscaleNode | None = None
        self._tailscale_agent_members: dict[str, AgentTailnetMember] = {}

    @property
    def state(self) -> StateT:
        """Access the typed state. Lazily initialized on first access."""
        if self._state is None and self._state_class:
            self._state = cast(StateT, self._state_class())
        return self._state  # type: ignore[return-value]

    @classmethod
    def get_config_class(cls) -> type[RunConfig]:
        """Get the config class from the generic parameter."""
        for base in getattr(cls, "__orig_bases__", ()):
            origin = get_origin(base)
            if origin is not None and issubclass(origin, BaseWorld):
                args = get_args(base)
                if args and isinstance(args[0], type) and issubclass(args[0], RunConfig):
                    return args[0]
        return RunConfig

    @classmethod
    def get_version(cls) -> str:
        """Get version from package metadata."""
        return _version_for_top_package(cls.__module__.split(".")[0])

    @classmethod
    def get_schema(cls) -> dict:
        """Get full schema including world config, agents, secrets, and envs."""
        return get_world_schema(cls)

    @abstractmethod
    async def reset(self) -> Observation:
        """Setup the world and return initial observation."""
        pass

    @abstractmethod
    async def step(self) -> StepResult:
        """Execute one step of the world."""
        pass

    async def preview(self) -> Observation:
        """Run the world in preview mode.

        Override this to provide custom preview behavior. The default
        raises NotImplementedError so preview-only launches don't
        silently run the normal reset/step loop.
        """
        raise NotImplementedError(f"World '{self.name}' does not implement preview mode")

    async def close(self) -> None:
        """Cleanup resources. Called after run completes."""
        pass

    def llm(self, config: LLMConfig, store: ResultStore | None = None) -> LLMClient:
        """Get an LLM client for the given config, with optional ResultStore caching."""
        from plato.llm import LLMClient

        return LLMClient(
            config,
            store=store,
            tracer_name=f"plato.worlds.{self.name}.llm",
            atif_source="world",
        )

    def decision(self, config: DecisionConfig | None = None) -> DecisionClient:
        """Get a TypeSafe System One (Jev) client for typed choice/noul/score decisions.

        Without a config the key comes from ``JEV_API_KEY`` / ``TYPESAFE_API_KEY``.
        See ``plato.decision`` for usage.
        """
        from plato.decision import DecisionClient

        return DecisionClient(
            config,
            tracer_name=f"plato.worlds.{self.name}.decision",
            atif_source="world",
        )

    def agent(
        self,
        config: AgentConfig,
        display_name: str | None = None,
        workspaces: list[Workspace] | None = None,
        mounts: list[AgentWorkspaceMount] | None = None,
        warm_pool: WarmPool | None = None,
        use_warm_pool: bool = True,
        agent_code_path: Path | None = None,
        total_agents: int | None = None,
        review_fn: Any | None = None,
        max_review_continuations: int = 2,
        review_exhaustion_policy: Literal["fail", "merge", "raise"] = "fail",
        review_compaction_instruction: str | Callable[[], str] | None = None,
    ) -> AgentTask:
        """Get an agent runner for the given config.

        Args:
            config: Agent configuration.
            display_name: Optional logical name to surface in VM aliases and OTel traces.
            workspaces: Workspaces to mount on the agent.
                The first workspace becomes the primary workspace.
                Each workspace's mount_path (from WorkspaceMarker) determines
                where it appears on the agent VM.
            total_agents: Total number of agents that will run through the pool.
                Scales the VM sandbox timeout to ``runtime.vm.timeout * total_agents``
                so pooled VMs stay alive long enough for all sequential reuse.
            use_warm_pool: Whether to use the config-backed shared warm pool.
                Set to ``False`` for one-shot agents whose VM must be destroyed
                immediately after the run.
            review_fn: Optional async review function. When set, each agent
                execution is followed by a review; merge happens only on pass,
                otherwise the agent is continued with feedback. The function
                receives the agent hostname and must return a
                :class:`~plato.agents.review_gate.ReviewGateResult`.
            max_review_continuations: Max agent retries after review failure.
            review_exhaustion_policy: Behavior when review continuations are
                exhausted. ``"fail"`` leaves the branch unmerged,
                ``"merge"`` force-merges, and ``"raise"`` aborts the task.
        """
        from plato.agents.execution import AgentExecutionManager
        from plato.agents.mounts import AgentWorkspaceMount
        from plato.agents.task import AgentTask, create_agent_runtime

        if warm_pool is not None and not use_warm_pool:
            raise ValueError("Pass either warm_pool=... or use_warm_pool=False, not both")

        ssh_key_path = self._runtime_info.ssh_key_path if self._runtime_info else None

        agent_runtime = create_agent_runtime(
            config,
            session=self._plato_session,
            ssh_key_path=ssh_key_path,
        )

        if workspaces and mounts:
            raise ValueError("Pass either workspaces=[...] or mounts=[...], not both")
        resolved_mounts = mounts or [workspace.mount() for workspace in workspaces or []]
        for mount in resolved_mounts:
            if not isinstance(mount, AgentWorkspaceMount):
                raise TypeError(f"Expected AgentWorkspaceMount, got {type(mount).__name__}")

        # Auto-resolve dev agent code path from /agents/<name> if not explicitly provided.
        # The test runner syncs dev.agents entries to /agents/<name> on the world VM;
        # pass the path through so AgentTask rsyncs it to the agent VM.
        if agent_code_path is None:
            pkg = config.package or ""
            agent_name = pkg.split(":")[0] if ":" in pkg else pkg
            if agent_name:
                candidate = Path(f"/agents/{agent_name}")
                if candidate.exists():
                    agent_code_path = candidate

        runner = AgentTask(
            config,
            agent_runtime,
            display_name=display_name,
            mounts=resolved_mounts,
            agent_containers=self._agent_containers,
            agent_code_path=agent_code_path,
            warm_pool=warm_pool,
            session=self._plato_session,
            world_runtime_info=self._runtime_info,
            review_exhaustion_policy=review_exhaustion_policy,
        )

        if warm_pool is None and use_warm_pool:
            primary_mount = resolved_mounts[0] if resolved_mounts else None
            primary_workspace = workspaces[0] if workspaces else self._resolve_primary_workspace(primary_mount)
            manager_key = self._agent_execution_manager_key(config, primary_mount)
            manager = self._agent_execution_managers.get(manager_key)
            if manager is None:
                manager = AgentExecutionManager(
                    agent_config=config,
                    runtime_factory=lambda: create_agent_runtime(
                        config,
                        session=self._plato_session,
                        ssh_key_path=ssh_key_path,
                    ),
                    world_runtime_info=self._runtime_info,
                    request_checkpoint=self.request_checkpoint,
                    primary_workspace=primary_workspace,
                    primary_mount=primary_mount,
                    total_agents=total_agents,
                    min_warmpool_timeout=self.config.min_warmpool_timeout,
                    vm_budget=self._agent_vm_budget,
                    warmpool_idle_timeout=self.config.warmpool_idle_timeout,
                )
                self._agent_execution_managers[manager_key] = manager
            elif total_agents is not None:
                manager.update_vm_timeout(total_agents)
            runner._execution_manager = manager

        # The logout runs in on_post_run, before the VM is released or stopped.
        if self.config.tailscale.joins_agents:
            runner.on_prepare(self._join_tailnet_agent)
            runner.on_post_run(self._leave_tailnet_agent)

        # Review gate is per-task, not per-manager — set on the runner
        if review_fn is not None:
            runner._review_fn = review_fn
            runner._max_review_continuations = max_review_continuations
            runner._review_exhaustion_policy = review_exhaustion_policy
            runner._review_compaction_instruction = review_compaction_instruction

        return runner

    def _resolve_primary_workspace(self, primary_mount: AgentWorkspaceMount | None) -> Workspace | None:
        if primary_mount is None:
            return None
        workspace = self._workspaces.get(primary_mount.workspace_name)
        if workspace is None:
            return None
        if workspace.path != primary_mount.world_path:
            return None
        return workspace

    def _agent_execution_manager_key(
        self,
        config: AgentConfig,
        primary_mount: AgentWorkspaceMount | None,
    ) -> str:
        config_sig = json.dumps(config.model_dump(mode="json", exclude_none=True), sort_keys=True)
        if primary_mount is None:
            mount_sig = "nomount"
        else:
            mount_sig = json.dumps(
                {
                    "workspace_name": primary_mount.workspace_name,
                    "world_path": str(primary_mount.world_path),
                    "agent_path": primary_mount.agent_path,
                    "transport_kind": primary_mount.transport_kind,
                    "git_sync_mode": primary_mount.git_sync.mode if primary_mount.git_sync else None,
                },
                sort_keys=True,
            )
        return f"{config_sig}:{mount_sig}"

    async def _shutdown_agent_execution_managers(self) -> None:
        managers = list(self._agent_execution_managers.values())
        self._agent_execution_managers.clear()
        if managers:
            await asyncio.gather(*(manager.shutdown() for manager in managers), return_exceptions=True)

    # ------------------------------------------------------------------
    # Workspace access
    # ------------------------------------------------------------------

    def workspace(self, name: str) -> Workspace:
        """Get a declared workspace by name.

        The returned Workspace exposes two key path properties:

        - ``ws.path`` — content directory on the **world VM**.
          Use this for reading/writing files from world code.
          For tracked workspaces this is ``<root>/data``; for untracked it's ``<root>``.

        - ``ws.mount_path`` — path where this workspace appears on **agent VMs**.
          Use this when building agent instructions or any path the agent will see.
          Defaults to ``str(ws.path)`` unless overridden via
          ``WorkspaceMarker(mount_path="/workspace/code")``.

        Always use these properties — never hardcode raw paths.

        Usage::

            ws = self.workspace("code")
            ws.path                           # world VM content dir
            ws.mount_path                    # agent VM mount path
            await ws.commit("step_1")         # DVC commit (tracked)
            await ws.restore("step_1")        # DVC restore

            # Pass to agent:
            runner = self.agent(config, workspaces=[ws])
            instruction = f"Edit files in {ws.mount_path}"
        """
        if name not in self._workspaces:
            raise KeyError(f"No workspace '{name}'. Available: {list(self._workspaces.keys())}")
        return self._workspaces[name]

    def create_workspace(
        self,
        *,
        name: str,
        path: Path,
        mount_path: str,
        parent: Workspace | str,
        tracked: bool = False,
    ) -> Workspace:
        """Create an ad-hoc workspace as a child of an existing workspace.

        Args:
            name: Logical name for the workspace.
            path: Absolute path on the world VM.
            mount_path: Where this workspace appears on agent VMs.
            parent: Parent workspace (name or Workspace).
                The path must be under the parent workspace's path.
            tracked: Whether to DVC-track this workspace.

        Returns:
            A new Workspace. Transport must be set up externally.

        Raises:
            ValueError: If path is not under the parent workspace's path.
        """
        parent_ws = self.workspace(parent) if isinstance(parent, str) else parent

        resolved_parent = parent_ws.path.resolve()
        resolved_child = path.resolve()
        if not (str(resolved_child).startswith(str(resolved_parent) + "/") or resolved_child == resolved_parent):
            raise ValueError(
                f"Workspace path {resolved_child} is not under parent workspace "
                f"path {resolved_parent}. Ad-hoc workspaces must be subdirectories "
                f"of their parent."
            )

        ws = Workspace(
            name=name,
            path=path,
            tracked=tracked,
            mount_path=mount_path,
            # An ad-hoc child of a pinned workspace lives on the same VM.
            pin_to_agent_vm=parent_ws.pin_to_agent_vm,
        )

        # Derive transport from parent if available
        if parent_ws.transport is not None:
            transport = parent_ws.transport.with_path(str(ws.path))
            transport.mount_path = mount_path
            ws.transport = transport

        return ws

    async def checkpoint(self, label: str, *, trigger_span_id: str = "") -> None:
        """Save state and commit all tracked workspaces."""
        for workspace in self._workspaces.values():
            if workspace.tracked:
                await workspace.commit(label, trigger_span_id=trigger_span_id)
        await self.save_state()

    def request_checkpoint(self, label: str) -> None:
        """Ask for a checkpoint without waiting for it.

        Requests made while one runs coalesce to the newest label. A world
        with its own checkpoint loop overrides this to wake that loop.
        """
        self._pending_checkpoint_label = label
        task = self._requested_checkpoint_task
        if task is None or task.done():
            self._requested_checkpoint_task = asyncio.create_task(self._run_requested_checkpoints())

    async def _run_requested_checkpoints(self) -> None:
        while self._pending_checkpoint_label is not None:
            label = self._pending_checkpoint_label
            self._pending_checkpoint_label = None
            try:
                await self.checkpoint(label)
            except Exception as exc:
                self.logger.warning("Requested checkpoint '%s' failed", label, exc_info=True)
                self._requested_checkpoint_error = exc
                if self._pending_checkpoint_label is None:
                    # Keep it pending: the next request must still commit the merged tree.
                    self._pending_checkpoint_label = label
                    return
                # A newer request commits every workspace, so it covers this merge too.
                continue
            # This checkpoint committed every workspace, so it covers earlier failures.
            self._requested_checkpoint_error = None

    async def flush_requested_checkpoints(self) -> None:
        """Wait for the requested checkpoints (running and pending) to finish.

        Raises the error of a failed requested checkpoint, one time. The failed
        label stays pending, so the next ``request_checkpoint`` runs it again.
        """
        task = self._requested_checkpoint_task
        if task is not None:
            await asyncio.shield(task)
        error = self._requested_checkpoint_error
        if error is not None:
            self._requested_checkpoint_error = None
            raise error

    def workspace_repo_name(self, field_name: str) -> str:
        """Return the Chronos repo name for a workspace field.

        Override this in subclasses to customize workspace repo naming.
        The default is ``{world.name}/{field_name}``::

            class MyWorld(BaseWorld):
                def workspace_repo_name(self, field_name: str) -> str:
                    return f"{self.name}/{self.config.project}/{field_name}"
        """
        return f"{self.name}/{field_name}"

    async def _resolve_workspace_repo_by_name(self, repo_name: str) -> ResolvedWorkspaceRepo:
        """Resolve a workspace repo by exact name."""
        chronos_url = self._get_chronos_base_url()
        api_key = self._get_chronos_api_key()
        logger.info("Resolving workspace repo %r via %s (auth=%s)", repo_name, chronos_url, self._chronos_auth_source())
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{chronos_url}/api/workspace-repos/resolve",
                json={"name": repo_name},
                headers={"X-API-Key": api_key},
            )
            if resp.status_code >= 400:
                logger.error(
                    "workspace-repos/resolve %r failed: HTTP %s (auth=%s): %s",
                    repo_name,
                    resp.status_code,
                    self._chronos_auth_source(),
                    resp.text,
                )
            resp.raise_for_status()
            data = resp.json()
        return ResolvedWorkspaceRepo(
            s3_bucket=data["s3_bucket"],
            s3_prefix=data["s3_prefix"],
            repo_id=data["repo_id"],
            commit_ref="",
            repo_name=repo_name,
            chronos_url=chronos_url,
            api_key=api_key,
        )

    async def _resolve_workspace_repo(self, field_name: str) -> ResolvedWorkspaceRepo:
        """Resolve workspace repo via Chronos."""
        repo_name = self.workspace_repo_name(field_name)

        chronos_url = self._get_chronos_base_url()
        api_key = self._get_chronos_api_key()

        if not chronos_url:
            raise RuntimeError(
                f"Cannot resolve workspace repo '{repo_name}': no chronos_url configured. "
                "Set session.chronos_url or session.otel_url."
            )

        logger.info("Resolving workspace repo %r via %s (auth=%s)", repo_name, chronos_url, self._chronos_auth_source())
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{chronos_url}/api/workspace-repos/resolve",
                json={"name": repo_name},
                headers={"X-API-Key": api_key},
            )
            if resp.status_code >= 400:
                logger.error(
                    "workspace-repos/resolve %r failed: HTTP %s (auth=%s): %s",
                    repo_name,
                    resp.status_code,
                    self._chronos_auth_source(),
                    resp.text,
                )
            resp.raise_for_status()
            data = resp.json()

        return ResolvedWorkspaceRepo(
            s3_bucket=data["s3_bucket"],
            s3_prefix=data["s3_prefix"],
            repo_id=data["repo_id"],
            commit_ref="",
            repo_name=repo_name,
            chronos_url=chronos_url,
            api_key=api_key,
        )

    # ------------------------------------------------------------------
    # run() and helpers
    # ------------------------------------------------------------------

    def _handed_over_workspace(self, name: str) -> HandoffWorkspace | None:
        if self.handoff is None:
            return None
        return next((ws for ws in self.handoff.workspaces if ws.name == name), None)

    async def check_handoff(self, handoff: Handoff) -> None:
        """Override to check a handoff this process is about to take over, while the previous process is still in
        charge: raise ``HandoffRefused`` (the state it can't read, an agent it doesn't know) and the previous process
        stops this one and carries on. Nothing may be touched here (agents, workspaces): only read and check."""

    async def hand_over(
        self,
        version: str,
        *,
        agents: dict[str, AgentTask],
        state: dict[str, Any] | None = None,
        package: str | None = None,
        upgrade_sdk: bool = True,
    ) -> NoReturn:
        """Hand this world over to ``version`` of its package, in place: same VM, same session (handover.py).

        ``agents`` are the running agents to hand over, by the world's name for each: each must be running a daemon
        job now (``AgentTask.agent_job_id``) or be between turns (``AgentTask.between_turns``), and stay so until this
        process exits: the world holds back their next turns meanwhile. ``state`` goes to the new process as ``self.handoff.state``. The new
        process is installed and started the way Chronos started this one, with the package pinned to ``version`` (and
        the SDK installed as for a fresh start, unless ``upgrade_sdk`` is False); this one stops its
        heartbeat and exits without stopping any agent, unmounting any workspace or completing the session.

        Raises ``HandoffRefused`` (and hands nothing over; this process carries on) when it can't: an agent without a
        running job, a workspace on a transport other than NFS, a start script it can't read, or a failed install.
        """

        package = package or _distribution_for_top_package(type(self).__module__.split(".")[0])
        if not package:
            raise HandoffRefused("can't tell which package this world was installed from")
        handed: list[HandoffAgent] = []
        for name, task in agents.items():
            info = task.current_runtime_info
            if info is None or (task.agent_job_id is None and not task.between_turns):
                raise HandoffRefused(f"agent {name} is neither running a daemon job nor between turns")
            runtime = info.model_dump(mode="json", exclude={"env"})
            handed.append(HandoffAgent(name=name, agent_job_id=task.agent_job_id, runtime=runtime))
        workspaces: list[HandoffWorkspace] = []
        annotations = {**self.config.get_field_annotations(), **self.extra_workspace_markers()}
        for name, ws in self._workspaces.items():
            marker = annotations.get(name)
            transport = marker.transport if isinstance(marker, WorkspaceMarker) else None
            if (transport or self.config.transport_mode) not in ("nfs_kernel", None):
                raise HandoffRefused(f"workspace '{name}' uses the {transport} transport: only NFS can be handed over")
            mount = ws.live_mount()
            workspaces.append(
                HandoffWorkspace(
                    name=name,
                    mountpoint=str(mount.mountpoint if mount is not None else ws.path),
                    cache_dir=str(mount.cache_dir) if mount is not None else None,
                    worker_pid=getattr(mount.worker_proc, "pid", None) if mount is not None else None,
                )
            )
        nxt = handover.next_process(handover.START_SCRIPT.read_text(), package, version)
        commands = nxt.install if upgrade_sdk else [c for c in nxt.install if "plato-sdk-v2" not in c]

        async def put_back() -> None:
            back = handover.next_process(handover.START_SCRIPT.read_text(), package, self.get_version())
            await asyncio.to_thread(handover.install, [c for c in back.install if "plato-sdk-v2" not in c])

        async def put_back_after(installing: asyncio.Future[None]) -> None:
            (outcome,) = await asyncio.gather(installing, return_exceptions=True)
            if outcome is not None:
                self.logger.warning("Installing %s==%s failed while cancelled: %r", package, version, outcome)
            await put_back()

        installing = asyncio.ensure_future(asyncio.to_thread(handover.install, commands))
        try:
            await asyncio.shield(installing)
        except asyncio.CancelledError:
            # The install's thread can't be stopped: let it finish, then put this version back, before cancelling.
            await asyncio.shield(put_back_after(installing))
            raise

        previous = self.handoff.generation if self.handoff is not None else 0
        handoff = Handoff(
            generation=previous + 1,
            old_pid=os.getpid(),
            handed_at=time.time(),
            package_spec=f"{package}=={version}",
            chronos_session_id=self.chronos.session_id,
            plato_session_id=self._plato_session.session_id if self._plato_session is not None else None,
            agents=handed,
            workspaces=workspaces,
            state=state or {},
        )
        try:
            path = handover.write(handoff)
            pid = handover.start_next(nxt.runner, path)
        except BaseException as error:
            # Nothing was started: this process stays in charge, on its own version.
            await asyncio.shield(put_back())
            if isinstance(error, Exception):
                raise HandoffRefused(f"starting {handoff.package_spec} failed: {error}") from error
            raise

        async def roll_back() -> None:
            # The new version won't take over: stop it, and put this version back.
            handover.abort(pid)
            await put_back()

        try:
            ready = await asyncio.to_thread(handover.wait_ready, path, pid)
        except BaseException:
            # Cancelled (or failed) while waiting: this process stays in charge, so the successor must not.
            await asyncio.shield(roll_back())
            raise
        if not ready:
            await roll_back()
            raise HandoffRefused(f"{handoff.package_spec} didn't get ready to take over (see /tmp/world.log)")
        self.logger.info(
            "Handed over to %s (pid %d): %d agent(s), %d workspace(s); this process exits now",
            handoff.package_spec,
            pid,
            len(handed),
            len(workspaces),
        )
        await self._disconnect_plato_session()
        await asyncio.to_thread(force_flush_tracing, 5000)
        logging.shutdown()
        os._exit(0)

    async def run(
        self,
        config: ConfigT,
        chronos: ChronosConfig,
        dev: DevConfig | None = None,
        runtime_info: RuntimeInfo | None = None,
    ) -> None:
        """Run the world: reset -> step until done -> close."""
        self.config = config
        self.chronos = chronos
        self.dev = dev or DevConfig()
        self._runtime_info = runtime_info
        self._ssh_key_path = runtime_info.ssh_key_path if runtime_info else None
        self._step_count = 0
        self._slack_notify_token = None

        self.logger.info(f"Starting world '{self.name}'")

        if self.config.state.enabled:
            Path(self.config.state.path).mkdir(parents=True, exist_ok=True)

        self._setup_session()

        if self.config.slack_notifications_enabled:
            self._slack_notify_token = enable_stage_tracking(
                session_id=self.chronos.session_id,
                base_url=self._get_chronos_base_url(),
            )

        plato_version = get_plato_version()
        world_version = self.get_version()
        self.logger.debug(f"World version: {world_version}, Plato SDK version: {plato_version}")

        handoff_path = os.environ.get(handover.HANDOFF_ENV)
        handoff = handover.read(Path(handoff_path)) if handoff_path else None
        await self._connect_plato_session()
        await self._resolve_world_hostname()
        if handoff_path and handoff is not None:
            # Taking over from a previous process. Check everything that can be checked while it's still in charge,
            # say so, and touch nothing (agents, workspaces) until it has exited: one world process at a time.
            async with self._chronos_client() as chronos:
                await handover.verify(
                    handoff,
                    session_id=self.chronos.session_id,
                    plato_session=self._plato_session,
                    get_session=chronos.get_session,
                )
            declared = {
                name
                for name, marker in {**self.config.get_field_annotations(), **self.extra_workspace_markers()}.items()
                if isinstance(marker, WorkspaceMarker)
            }
            if declared != {ws.name for ws in handoff.workspaces}:
                raise HandoffRefused(f"this version's workspaces {sorted(declared)} aren't the ones handed over")
            await self.check_handoff(handoff)
            handover.ready_path(Path(handoff_path)).touch()
            await asyncio.to_thread(handover.wait_for_exit, handoff.old_pid)
            handover.taken_path(Path(handoff_path)).touch()
            self.handoff = handoff
            self.logger.info(
                "Took over from world process %d (handoff %d, %.1f s ago): %d agent(s), %d workspace(s)",
                handoff.old_pid,
                handoff.generation,
                time.time() - handoff.handed_at,
                len(handoff.agents),
                len(handoff.workspaces),
            )

        tracer = get_tracer("plato.world")

        run_error: Exception | None = None
        with (
            tracer.start_as_current_span("world") as root_span,
            aggregate_step_costs(root_span, tracer, name=self.name, version=self.get_version()),
        ):
            root_span.set_attribute("plato.world.name", self.name)
            root_span.set_attribute("plato.world.version", self.get_version())
            root_span.set_attribute("plato.session.id", self.chronos.session_id)
            root_span.set_attribute("plato.phase", "world_start")

            try:
                await self._join_tailnet_world()
                plato_settings = get_plato_settings()
                if self.config.preview.enabled:
                    await self._run_preview_loop(tracer)
                elif plato_settings.e2e_test_dir:
                    await self._run_e2e_loop(tracer, plato_settings)
                else:
                    await self._run_loop(tracer)
            except Exception as e:
                run_error = e
                root_span.set_status(StatusCode.ERROR, str(e))
                root_span.record_exception(e)

                with tracer.start_as_current_span("world_error") as err_span:
                    err_span.set_status(StatusCode.ERROR, str(e))
                    err_span.set_attribute("error.type", type(e).__name__)
                    err_span.set_attribute("error.message", str(e))
                    err_span.set_attribute("error.traceback", traceback.format_exc())
                    err_span.record_exception(e)
            finally:
                if self._slack_notify_token is not None:
                    disable_stage_tracking(self._slack_notify_token)
                # A merge near the end must not lose its requested checkpoint.
                # A failed one is logged, so that the shutdown steps still run.
                try:
                    await self.flush_requested_checkpoints()
                except Exception:
                    self.logger.warning("A requested checkpoint failed before shutdown", exc_info=True)
                # Each step runs even when an earlier one raises, so a failed close() keeps no VM alive.
                try:
                    await self.close()
                finally:
                    try:
                        # Before the agent VMs go away, so each one can still log out over SSH.
                        await self._leave_tailnet()
                    finally:
                        try:
                            await self._shutdown_agent_execution_managers()
                        finally:
                            await self._disconnect_plato_session()

        await self._finalize(run_error)

    def _tailscale_session_id(self) -> str:
        chronos = getattr(self, "chronos", None)
        return chronos.session_id if chronos is not None else ""

    async def _join_tailnet_world(self) -> None:
        """Join the world VM to the tailnet. A failed join raises only when ``tailscale.required`` is true."""
        ts = self.config.tailscale
        if not ts.joins_world:
            return
        try:
            auth_key = await resolve_auth_key(ts, log=self.logger)
            plan = build_join_plan(
                ts, session_id=self._tailscale_session_id(), role=WORLD_TAILNET_ROLE, auth_key=auth_key
            )
            node = await join_tailnet(LocalCommandRunner(), plan, persist_proxy_env=False, log=self.logger)
        except TailscaleError as exc:
            if ts.required:
                raise
            self.logger.warning("World VM did not join the tailnet (tailscale.required is false): %s", exc)
            return
        self._tailscale_world_node = node

    @property
    def tailscale_proxy_env(self) -> dict[str, str]:
        """Proxy environment to tailnet peers (userspace mode only, else empty).

        Not in ``os.environ``, so Chronos, LLM and S3 stay direct. Pass it only to code that talks to peers.
        """
        node = self._tailscale_world_node
        return dict(node.proxy_env) if node is not None else {}

    async def _join_tailnet_agent(self, info: RuntimeInfo) -> None:
        """``on_prepare`` hook: join one agent VM over SSH. Raises only when ``tailscale.required`` is true."""
        ts = self.config.tailscale
        member = self._tailscale_agent_members.get(info.runtime_id)
        if member is not None and not member.leave_failed:
            return
        role = f"{AGENT_TAILNET_ROLE_PREFIX}{info.runtime_id[-AGENT_TAILNET_ID_CHARS:]}"
        try:
            # Minted on the world VM (here), so only the one-off key crosses SSH to the agent VM.
            auth_key = await resolve_auth_key(ts, log=self.logger)
            plan = build_join_plan(ts, session_id=self._tailscale_session_id(), role=role, auth_key=auth_key)
            node = await join_tailnet(SshCommandRunner(info), plan, persist_proxy_env=True, log=self.logger)
        except TailscaleError as exc:
            if ts.required:
                raise
            self.logger.warning(
                "Agent VM %s did not join the tailnet (tailscale.required is false): %s", info.runtime_id, exc
            )
            return
        self._tailscale_agent_members[info.runtime_id] = AgentTailnetMember(info=info, node=node)

    async def _leave_tailnet_agent(self, info: RuntimeInfo) -> None:
        """``on_post_run`` hook: log one agent VM out. Never raises.

        After a failed logout the member stays, so the sweep in :meth:`_leave_tailnet` tries again.
        """
        member = self._tailscale_agent_members.get(info.runtime_id)
        if member is None:
            return
        try:
            left = await leave_tailnet(
                SshCommandRunner(member.info),
                member.node,
                timeout_s=self.config.tailscale.leave_timeout_s,
                log=self.logger,
            )
        except Exception as exc:
            self.logger.warning("Tailscale leave failed on agent VM %s: %s", info.runtime_id, exc)
            left = False
        if left:
            self._tailscale_agent_members.pop(info.runtime_id, None)
        else:
            member.leave_failed = True

    async def _leave_tailnet(self) -> None:
        """Log out every tailnet node this session still has. Best effort: never raises."""
        ts = self.config.tailscale
        members = list(self._tailscale_agent_members.values())
        self._tailscale_agent_members.clear()
        world_node, self._tailscale_world_node = self._tailscale_world_node, None
        if not members and world_node is None:
            return
        try:
            leaves = [
                leave_tailnet(SshCommandRunner(m.info), m.node, timeout_s=ts.leave_timeout_s, log=self.logger)
                for m in members
            ]
            if world_node is not None:
                leaves.append(
                    leave_tailnet(LocalCommandRunner(), world_node, timeout_s=ts.leave_timeout_s, log=self.logger)
                )
            await asyncio.gather(*leaves, return_exceptions=True)
        except Exception as exc:
            self.logger.warning("Tailscale cleanup failed: %s", exc)

    def extra_workspace_markers(self) -> dict[str, WorkspaceMarker]:
        """Dynamic workspaces to register alongside the config's marker fields.

        Override to contribute config-driven workspaces (e.g. a dict of named
        datasets) that cannot be declared as static ``Annotated`` fields. Each
        entry rides the exact same pipeline as a marker field: repo resolve,
        ``state.workspaces`` restore (key ``<world>/<name>``), FUSE mount, and
        transport setup (including per-export NFS ``readonly``). Names must not
        collide with marker field names; there is no ``config.<name>`` attribute
        for dynamic workspaces — use ``self.workspace(name).path``.
        """
        return {}

    async def _init_declared_workspaces(self) -> None:
        """Auto-discover Workspace markers on config and set everything up."""
        annotations: dict[str, Any] = dict(self.config.get_field_annotations())
        for extra_name, extra_marker in self.extra_workspace_markers().items():
            if extra_name in annotations:
                raise ValueError(f"extra_workspace_markers(): '{extra_name}' collides with a config marker field")
            annotations[extra_name] = extra_marker
        state_root = Path(self.config.state.path)
        config_fields = set(type(self.config).model_fields)

        for field_name, marker in annotations.items():
            if not isinstance(marker, WorkspaceMarker):
                continue

            # Resolve path (dynamic workspaces have no config attribute)
            configured_path = getattr(self.config, field_name, None) if field_name in config_fields else None
            if configured_path and str(configured_path) not in (".", ""):
                ws_path = Path(configured_path)
            else:
                ws_path = state_root / field_name

            ws_path.mkdir(parents=True, exist_ok=True)

            # Resolve workspace repo via Chronos
            if marker.tracked:
                repo_info = await self._resolve_workspace_repo(field_name)
            else:
                repo_info = ResolvedWorkspaceRepo(
                    s3_bucket="",
                    s3_prefix="",
                    repo_id="",
                    commit_ref="",
                    repo_name="",
                    chronos_url="",
                    api_key="",
                )

            workspace = Workspace(
                name=field_name,
                path=ws_path,
                tracked=marker.tracked,
                mount_path=marker.mount_path,
                dvcignore=marker.dvcignore,
                s3_bucket=repo_info.s3_bucket,
                s3_prefix=repo_info.s3_prefix,
                repo_id=repo_info.repo_id,
                repo_name=repo_info.repo_name,
                chronos_url=repo_info.chronos_url,
                api_key=repo_info.api_key,
                session_id=self.chronos.session_id if self.chronos else "",
                commit_strategy=getattr(marker, "commit_strategy", "manifest"),
                nfs_mount_options=getattr(marker, "nfs_mount_options", ""),
                pin_to_agent_vm=getattr(marker, "pin_to_agent_vm", False),
            )

            if self.handoff is not None:
                # Every workspace was handed over live. A new one can't be set up beside them: the NFS server's
                # exports would be written again under the agents. That release needs a full restart.
                adopted = self._handed_over_workspace(field_name)
                if adopted is None:
                    raise HandoffRefused(f"workspace '{field_name}' is new in this version: it needs a full restart")
                if adopted.cache_dir:
                    workspace.adopt_mount(Path(adopted.mountpoint), Path(adopted.cache_dir), adopted.worker_pid)
                else:
                    await workspace.init()  # untracked: a plain directory, nothing mounted to keep
            else:
                await workspace.init()

            self._workspaces[field_name] = workspace
            # workspace.path is the content directory (data/ for tracked, root otherwise)
            if field_name in config_fields:
                object.__setattr__(self.config, field_name, workspace.path)
            self.logger.info(
                f"Workspace '{field_name}' at {ws_path} "
                f"(tracked={marker.tracked}, mount_path={workspace._mount_path}, repo={repo_info.repo_name})"
            )

    async def _setup_workspaces(self) -> None:
        """Mount FUSE overlays and initialize transports for all workspaces."""
        if not self._workspaces:
            return

        # 1. Mount FUSE for all workspaces in parallel.
        #    Must happen before transport setup so NFS exports the FUSE mountpoint.
        await asyncio.gather(*(ws.ensure_fuse_mount() for ws in self._workspaces.values()))

        # 2. Setup transports (NFS/SSHFS/Git).
        #    Skip if no runtime info (e.g., unit tests without real runtime).
        if self._runtime_info is None:
            return

        runtime_info = self._runtime_info
        annotations = {**self.config.get_field_annotations(), **self.extra_workspace_markers()}

        # Separate workspaces by transport type so git/rsync/sshfs transports can
        # init in parallel while NFS workspaces share a single server
        # (sequential add_export).
        nfs_ws: list[tuple[Workspace, WorkspaceMarker | None]] = []
        git_ws: list[tuple[Workspace, WorkspaceMarker]] = []
        rsync_ws: list[Workspace] = []
        sshfs_ws: list[Workspace] = []
        fuse_ws: list[tuple[Workspace, WorkspaceMarker]] = []

        for ws in self._workspaces.values():
            marker = annotations.get(ws.name)
            marker_transport = marker.transport if isinstance(marker, WorkspaceMarker) else None
            if marker_transport == "git" and isinstance(marker, WorkspaceMarker):
                git_ws.append((ws, marker))
            elif marker_transport == "rsync":
                rsync_ws.append(ws)
            elif marker_transport == "fuse" and isinstance(marker, WorkspaceMarker):
                fuse_ws.append((ws, marker))
            elif marker_transport == "sshfs" or (marker_transport is None and self.config.transport_mode == "sshfs"):
                # An EXPLICIT per-workspace transport always wins: a marker
                # pinned to "nfs_kernel" must not be silently rerouted to
                # sshfs by the world-level transport_mode (read-only datasets
                # opt out of fuse INTO NFS specifically).
                sshfs_ws.append(ws)
            else:
                nfs_ws.append((ws, marker if isinstance(marker, WorkspaceMarker) else None))

        # Git transports init in parallel (each has its own bare repo)
        async def _setup_git(ws: Workspace, marker: WorkspaceMarker) -> None:
            await ws.setup_transport(
                runtime_info,
                marker_transport="git",
                git_config=marker.git_config,
            )

        # SSHFS transports init in parallel (each is independent)
        async def _setup_sshfs(ws: Workspace) -> None:
            await ws.setup_transport(
                runtime_info,
                transport_mode="sshfs",
            )

        async def _setup_rsync(ws: Workspace) -> None:
            await ws.setup_transport(
                runtime_info,
                marker_transport="rsync",
            )

        # Direct per-agent-VM fuse mounts (read-only datasets): no world-side
        # server, so these init in parallel like git/rsync/sshfs.
        async def _setup_fuse(ws: Workspace, marker: WorkspaceMarker) -> None:
            await ws.setup_transport(
                runtime_info,
                marker_transport="fuse",
                readonly=marker.readonly,
            )

        parallel_tasks = [_setup_git(ws, m) for ws, m in git_ws]
        parallel_tasks.extend(_setup_rsync(ws) for ws in rsync_ws)
        parallel_tasks.extend(_setup_sshfs(ws) for ws in sshfs_ws)
        parallel_tasks.extend(_setup_fuse(ws, m) for ws, m in fuse_ws)

        # NFS: first workspace creates server, rest add exports (sequential)
        nfs_server = None
        nfs_fresh = False
        for i, (ws, ws_marker) in enumerate(nfs_ws):
            readonly = ws_marker.readonly if ws_marker is not None else False
            if self._handed_over_workspace(ws.name) is not None:
                # The previous process's NFS server is still serving this export: only the handle is new.
                nfs_server = ws.adopt_nfs_transport(runtime_info, nfs_server, readonly=readonly)
                continue
            nfs_server = await ws.setup_transport(
                self._runtime_info,
                transport_mode="nfs_kernel",
                nfs_server=nfs_server,
                export_fsid=i,
                readonly=readonly,
            )
            nfs_fresh = True
        if not nfs_fresh:
            nfs_server = None  # nothing new to export: leave the running server alone

        # Run NFS refresh + git/sshfs inits in parallel
        if parallel_tasks and nfs_server is not None:
            await asyncio.gather(nfs_server.refresh_exports(), *parallel_tasks)
        elif nfs_server is not None:
            await nfs_server.refresh_exports()
        elif parallel_tasks:
            await asyncio.gather(*parallel_tasks)

    async def _init_world(self, tracer: Any) -> Observation:
        """Common world initialization: metrics, workspaces, state resume, reset.

        Called by all execution modes (run loop, preview, e2e) before their
        mode-specific logic.
        """
        if self.chronos.otel_url and self.chronos.session_id:
            instrument_system_metrics(
                otlp_endpoint=self.chronos.otel_url,
                session_id=self.chronos.session_id,
                env_alias="world",
                job_id=os.environ.get("JOB_ID", ""),
            )

        await self._init_declared_workspaces()

        # Resume state BEFORE setting up workspaces so restored .git-bare
        # isn't nuked by _init_bare_repo during transport setup.
        # A world taking over keeps the live workspaces: restoring a checkpoint over them would roll back the
        # agents' writes since it.
        resumed = await self._try_resume() if self.handoff is None else False
        if resumed:
            self.logger.info("Resumed from saved state")

        await self._setup_workspaces()

        with tracer.start_as_current_span("reset") as reset_span:
            reset_span.set_attribute("plato.phase", "reset")
            reset_span.set_attribute("plato.world.name", self.name)
            obs = await self.reset()
            obs_data = obs.model_dump()
            reset_span.set_attribute("plato.observation", json.dumps(obs_data, default=str))

        self.logger.info(f"World reset complete: {obs}")
        return obs

    async def _run_loop(self, tracer: Any) -> None:
        """Execute the reset → step → checkpoint loop."""
        await self._init_world(tracer)

        while True:
            self._step_count += 1

            with tracer.start_as_current_span(f"step_{self._step_count}") as step_span:
                step_span.set_attribute("plato.phase", "step")
                step_span.set_attribute("plato.world.name", self.name)
                step_span.set_attribute("plato.step.number", self._step_count)
                result = await self.step()
                step_span.set_attribute("plato.step.done", result.done)
                if result.observation is not None:
                    obs_data = result.observation.model_dump()
                    step_span.set_attribute("plato.step.observation", json.dumps(obs_data, default=str))

            self.logger.info(f"Step {self._step_count}: done={result.done}")

            # Checkpoint unconditionally — the final step's outputs would
            # otherwise be dropped because the previous gate skipped this
            # call when result.done was True. Requested checkpoints finish
            # first, so two checkpoints never commit the workspaces at once.
            # A failed one is logged; step.N commits every workspace.
            try:
                await self.flush_requested_checkpoints()
            except Exception:
                self.logger.warning(
                    "A requested checkpoint failed; step.%d commits all workspaces", self._step_count, exc_info=True
                )
            await self.checkpoint(f"step.{self._step_count}")

            if result.done:
                break

        # Capture the final observation for session completion
        self._final_result: dict | None = None
        if result.observation is not None:
            try:
                self._final_result = result.observation.model_dump()
            except Exception as e:
                self.logger.warning(f"Failed to serialize final observation: {e}")

    async def _run_e2e_loop(self, tracer: Any, settings: PlatoSettings) -> None:
        """Execute e2e tests after reset() instead of the step() loop."""
        await self._init_world(tracer)

        try:
            await run_e2e_tests(
                self,
                tracer,
                test_dir=settings.e2e_test_dir,
                test_filter=settings.e2e_test_filter,
            )
        finally:
            try:
                try:
                    await self.flush_requested_checkpoints()
                except Exception:
                    self.logger.warning(
                        "A requested checkpoint failed; e2e_tests commits all workspaces", exc_info=True
                    )
                await self.checkpoint("e2e_tests")
                tracked = [n for n, ws in self._workspaces.items() if ws.tracked]
                if tracked:
                    self.logger.info(
                        "Checkpointed workspaces: %s (use `plato chronos workspace-refs <session-id>` to list, "
                        "`plato chronos download <session-id> --repo <name>` to download)",
                        ", ".join(tracked),
                    )
            except Exception:
                self.logger.warning("Failed to checkpoint after e2e tests", exc_info=True)


# Set default review models on BaseWorld after class definition to avoid circular imports.
# Subclasses that don't override review_models will inherit these.
from plato.worlds.session_review_models import DEFAULT_REVIEW_MODELS  # noqa: E402

BaseWorld.review_models = DEFAULT_REVIEW_MODELS
