"""Base world class for Plato worlds."""

from __future__ import annotations

import asyncio
import importlib.metadata
import json
import logging
import os
import traceback
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Literal, cast, get_args, get_origin

import httpx
from opentelemetry.trace import StatusCode
from pydantic import BaseModel as PydanticBaseModel
from typing_extensions import TypeVar

from plato.markers import WorkspaceMarker
from plato.otel import aggregate_step_costs, get_tracer
from plato.runtimes.base import RuntimeInfo
from plato.settings import PlatoSettings
from plato.settings import get_settings as get_plato_settings
from plato.utils.versions import get_plato_version
from plato.vm_metrics import instrument_system_metrics
from plato.worlds.chronos_mixin import ChronosSessionMixin
from plato.worlds.config import (
    AgentConfig,
    ChronosConfig,
    DevConfig,
    LLMConfig,
    RunConfig,
)
from plato.worlds.models import (
    Observation,
    StepResult,
)
from plato.worlds.preview_mixin import PreviewMixin
from plato.worlds.runtime_mixin import RuntimeMixin
from plato.worlds.schema import get_world_schema
from plato.worlds.stage_tracking import disable_stage_tracking, enable_stage_tracking
from plato.worlds.testing import run_e2e_tests
from plato.worlds.workspace import Workspace

if TYPE_CHECKING:
    from plato.agents.execution import AgentExecutionManager
    from plato.agents.mounts import AgentWorkspaceMount
    from plato.agents.task import AgentTask
    from plato.agents.warmpool import WarmPool
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
        top_package = cls.__module__.split(".")[0]
        dist_names = importlib.metadata.packages_distributions().get(top_package, [])
        for dist_name in dist_names:
            try:
                return importlib.metadata.version(dist_name)
            except importlib.metadata.PackageNotFoundError:
                continue
        return "0.0.0"

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
                    checkpoint=self.checkpoint,
                    primary_workspace=primary_workspace,
                    primary_mount=primary_mount,
                    total_agents=total_agents,
                    min_warmpool_timeout=self.config.min_warmpool_timeout,
                )
                self._agent_execution_managers[manager_key] = manager
            elif total_agents is not None:
                manager.update_vm_timeout(total_agents)
            runner._execution_manager = manager

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

        await self._connect_plato_session()
        await self._resolve_world_hostname()

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
                await self.close()
                await self._shutdown_agent_execution_managers()
                await self._disconnect_plato_session()

        await self._finalize(run_error)

    async def _init_declared_workspaces(self) -> None:
        """Auto-discover Workspace markers on config and set everything up."""
        annotations = self.config.get_field_annotations()
        state_root = Path(self.config.state.path)

        for field_name, marker in annotations.items():
            if not isinstance(marker, WorkspaceMarker):
                continue

            # Resolve path
            configured_path = getattr(self.config, field_name, None)
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
            )

            await workspace.init()

            self._workspaces[field_name] = workspace
            # workspace.path is the content directory (data/ for tracked, root otherwise)
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
        annotations = self.config.get_field_annotations()

        # Separate workspaces by transport type so git/rsync/sshfs transports can
        # init in parallel while NFS workspaces share a single server
        # (sequential add_export).
        nfs_ws: list[Workspace] = []
        git_ws: list[tuple[Workspace, WorkspaceMarker]] = []
        rsync_ws: list[Workspace] = []
        sshfs_ws: list[Workspace] = []

        for ws in self._workspaces.values():
            marker = annotations.get(ws.name)
            marker_transport = marker.transport if isinstance(marker, WorkspaceMarker) else None
            if marker_transport == "git" and isinstance(marker, WorkspaceMarker):
                git_ws.append((ws, marker))
            elif marker_transport == "rsync":
                rsync_ws.append(ws)
            elif self.config.transport_mode == "sshfs" and marker_transport != "git":
                sshfs_ws.append(ws)
            else:
                nfs_ws.append(ws)

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

        parallel_tasks = [_setup_git(ws, m) for ws, m in git_ws]
        parallel_tasks.extend(_setup_rsync(ws) for ws in rsync_ws)
        parallel_tasks.extend(_setup_sshfs(ws) for ws in sshfs_ws)

        # NFS: first workspace creates server, rest add exports (sequential)
        nfs_server = None
        for i, ws in enumerate(nfs_ws):
            nfs_server = await ws.setup_transport(
                self._runtime_info,
                transport_mode="nfs_kernel",
                nfs_server=nfs_server,
                export_fsid=i,
            )

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
        resumed = await self._try_resume()
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
            # call when result.done was True.
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
