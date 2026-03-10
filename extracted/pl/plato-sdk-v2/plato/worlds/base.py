"""Base world class for Plato worlds."""

from __future__ import annotations

import asyncio
import importlib.metadata
import json
import logging
import os
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Generic, get_args, get_origin

import httpx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from opentelemetry.trace import StatusCode
from pydantic import BaseModel as PydanticBaseModel
from typing_extensions import TypeVar

from plato.agents.runner import AgentRunner, create_runtime
from plato.agents.runtime.transport import NFSTransport, Transport
from plato.llm import LLMClient
from plato.markers import WorkspaceMarker
from plato.otel import get_tracer, init_tracing, shutdown_tracing
from plato.runtime import RuntimeConfig, VMRuntimeConfig
from plato.v2.async_.session import Session
from plato.vm_metrics import instrument_system_metrics, shutdown_metrics
from plato.worlds.config import AgentConfig, DevConfig, LLMConfig, RunConfig, SessionConfig
from plato.worlds.human_annotation import RequiresHumanAnnotation
from plato.worlds.models import Observation, StateHistoryEntry, StepResult, WorkspaceSnapshot
from plato.worlds.schema import get_world_schema
from plato.worlds.workspace import Workspace

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment
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


def _generate_ssh_key() -> Path:
    """Generate an Ed25519 SSH key pair for VM access."""
    key_path = Path("/tmp/agent_ssh_key")
    if key_path.exists():
        key_path.unlink()
    pub_path = key_path.with_suffix(".pub")
    if pub_path.exists():
        pub_path.unlink()

    private_key = Ed25519PrivateKey.generate()

    key_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.OpenSSH,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    key_path.chmod(0o600)

    pub_path.write_bytes(
        private_key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH,
        )
        + b"\n"
    )

    return key_path


def _get_plato_version() -> str:
    """Get the installed plato SDK version."""
    try:
        return importlib.metadata.version("plato-sdk-v2")
    except Exception:
        return "unknown"


def register_world(name: str):
    """Decorator to register a world class."""

    def decorator(cls: type[BaseWorld]) -> type[BaseWorld]:
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


class BaseWorld(ABC, Generic[ConfigT, StateT]):
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
    _state_class: ClassVar[type[PydanticBaseModel] | None] = None

    # Instance attributes
    config: ConfigT  # Typed via generic parameter
    plato_session: Session | None = None  # Connected Plato session (if running on managed VM)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Extract StateT from Generic args
        for base in getattr(cls, "__orig_bases__", []):
            args = get_args(base)
            if len(args) >= 2 and args[1] is not type(None):
                if isinstance(args[1], type) and issubclass(args[1], PydanticBaseModel):
                    cls._state_class = args[1]

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"plato.worlds.{self.name}")
        self._step_count: int = 0
        self.plato_session = None
        self._current_step_id: str | None = None
        self._session_id: str | None = None
        self._agent_containers: list[str] = []  # Track spawned agent containers for cleanup
        self._state: StateT | None = None
        self._transport: Transport | None = None  # NFS/rsync transport (set during session connect)
        self._nfs_mesh_ip: str | None = None
        self._ssh_key_path: Path | None = None
        self._workspaces: dict[str, Workspace] = {}  # declared workspaces
        self._tailscaled_proc: asyncio.subprocess.Process | None = None

    @property
    def state(self) -> StateT:
        """Access the typed state. Lazily initialized on first access."""
        if self._state is None and self._state_class:
            self._state = self._state_class()
        return self._state  # type: ignore[return-value]

    @classmethod
    def get_config_class(cls) -> type[RunConfig]:
        """Get the config class from the generic parameter."""
        for base in getattr(cls, "__orig_bases__", []):
            origin = get_origin(base)
            if origin is BaseWorld:
                args = get_args(base)
                if args and isinstance(args[0], type) and issubclass(args[0], RunConfig):
                    return args[0]
        return RunConfig

    @classmethod
    def get_version(cls) -> str:
        """Get version from package metadata."""
        for pkg_name in [cls.__module__.split(".")[0], f"plato-world-{cls.name}"]:
            try:
                return importlib.metadata.version(pkg_name)
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

    async def close(self) -> None:
        """Cleanup resources. Called after run completes."""
        await self._cleanup_tailscale()
        await self._cleanup_agent_containers()
        await self._cleanup_agent_envs()

    async def _cleanup_tailscale(self) -> None:
        """Terminate tailscaled if this world started it."""
        proc = self._tailscaled_proc
        self._tailscaled_proc = None
        if proc is None:
            return

        try:
            if proc.returncode is None:
                proc.terminate()
                try:
                    await asyncio.wait_for(proc.wait(), timeout=5)
                except TimeoutError:
                    self.logger.warning("tailscaled did not exit after SIGTERM, sending SIGKILL")
                    proc.kill()
                    await proc.wait()
            else:
                await proc.wait()
        except ProcessLookupError:
            # Process already exited.
            return
        except Exception as e:
            self.logger.warning(f"Failed to cleanup tailscaled process: {e}")

    async def _cleanup_agent_containers(self) -> None:
        """Stop any agent containers spawned by this world."""
        if not self._agent_containers:
            return

        self.logger.info(f"Stopping {len(self._agent_containers)} agent container(s)...")
        for container_name in self._agent_containers:
            try:
                proc = await asyncio.create_subprocess_exec(
                    "docker",
                    "stop",
                    container_name,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                await proc.wait()
                self.logger.debug(f"Stopped container: {container_name}")
            except Exception as e:
                self.logger.warning(f"Failed to stop container {container_name}: {e}")
        self._agent_containers.clear()
        self.logger.info("Agent containers stopped")

    async def _cleanup_agent_envs(self) -> None:
        """Remove all non-runtime environments (agent VMs) from the session."""
        if not self.plato_session:
            return

        try:
            envs = self.plato_session.envs
        except Exception as e:
            self.logger.warning(f"Failed to list agent envs for cleanup: {e}")
            return

        for env in envs:
            if env.alias == "runtime":
                continue
            try:
                self.logger.info(f"Removing agent env: {env.alias} (job={env.job_id})")
                await self.plato_session.remove_env(env)
            except Exception as e:
                self.logger.warning(f"Failed to remove env {env.alias}: {e}")

    def llm(self, config: LLMConfig, store: ResultStore | None = None):
        """Get an LLM client for the given config, with optional ResultStore caching."""
        return LLMClient(config, store=store)

    def agent(
        self,
        config: AgentConfig,
        display_name: str | None = None,
        workspaces: list[Workspace] | None = None,
    ) -> AgentRunner:
        """Get an agent runner for the given config.

        Args:
            config: Agent configuration.
            display_name: Optional logical name to surface in VM aliases and OTel traces.
            workspaces: Workspaces to mount on the agent.
                The first workspace becomes the primary workspace.
                Each workspace's mount_path (from WorkspaceMarker) determines
                where it appears on the agent VM.
        """
        resolved: list[Transport] = []
        if workspaces:
            for ws in workspaces:
                if ws.transport is None:
                    raise RuntimeError(
                        f"Workspace '{ws.name}' has no transport (NFS/rsync). Is the Plato session connected?"
                    )
                resolved.append(ws.transport)

        primary = resolved[0] if resolved else self._transport
        extra = resolved[1:] if len(resolved) > 1 else None

        runtime = create_runtime(
            config,
            session=self.plato_session,
            ssh_key_path=self._ssh_key_path,
        )
        return AgentRunner(
            config,
            runtime,
            display_name=display_name,
            workspace=primary,
            workspaces=extra,
            agent_containers=self._agent_containers,
        )

    async def _connect_plato_session(self) -> None:
        """Connect to Plato session from config."""
        if not self.session.plato_session:
            return

        try:
            self.logger.info("Restoring Plato session from serialized data")
            self.plato_session = await Session.load(self.session.plato_session, start_heartbeat=True)
            self.logger.info(f"Plato session {self.plato_session.session_id} restored, heartbeat started")
        except Exception as e:
            self.logger.warning(f"Failed to restore Plato session: {e}")
            return

        await self._setup_ssh_key()
        await self._create_transport()

    async def _setup_ssh_key(self) -> None:
        """Generate or reuse SSH key and add it to the Plato session."""
        if self.dev.ssh_key_path:
            self._ssh_key_path = self.dev.ssh_key_path
        else:
            self._ssh_key_path = _generate_ssh_key()

        pub_key = Path(str(self._ssh_key_path) + ".pub").read_text().strip()
        assert self.plato_session is not None
        await self.plato_session.add_ssh_key(pub_key)
        self.logger.debug("SSH key added to session")

    async def _create_transport(self) -> None:
        """Create the transport object (does NOT start the NFS server).

        The server is started later by ``_start_transport()`` so that FUSE
        mounts from workspace restore are already in place when NFS begins
        exporting with ``crossmnt``.
        """
        assert self._ssh_key_path is not None, "SSH key must be set before creating transport"

        mesh_ip = None
        if self.plato_session:
            for env in self.plato_session.envs:
                if env.alias == "runtime":
                    try:
                        mesh_ip = await env.get_mesh_ip()
                    except Exception as e:
                        self.logger.warning(f"Failed to get mesh IP from runtime env: {e}")
                    break
        if not mesh_ip or not self.plato_session:
            raise RuntimeError("NFS transport requires mesh IP from Plato session")

        self._nfs_mesh_ip = mesh_ip
        self._transport = None
        self.logger.info(f"Transport: nfs_kernel (mesh_ip={mesh_ip})")

    async def _start_transport(self) -> None:
        """Start the NFS server after workspaces (and any FUSE mounts) are ready."""
        if not self._nfs_mesh_ip or not self._workspaces:
            return
        assert self._ssh_key_path is not None

        # Ensure all workspaces have FUSE mounts (overlayfs can't be NFS-exported)
        for ws in self._workspaces.values():
            await ws.ensure_fuse_mount()

        # Each workspace gets its own NFSTransport and NFS export.
        ws_list = list(self._workspaces.values())
        first = ws_list[0]
        first_path = str(first.path)

        self._transport = NFSTransport(first_path, self._nfs_mesh_ip, self._ssh_key_path)
        await self._transport.initialize()

        for i, ws in enumerate(ws_list[1:], start=1):
            await self._transport.add_export(str(ws.path), fsid=i)

        await self._transport.refresh_exports()

        # Assign per-workspace transports
        for ws in ws_list:
            t = NFSTransport(str(ws.path), self._nfs_mesh_ip, self._ssh_key_path)
            t.mount_path = ws.mount_path
            ws.transport = t

    async def _disconnect_plato_session(self) -> None:
        """Stop heartbeat for the Plato session (does not close the session)."""
        if self.plato_session:
            try:
                await self.plato_session.stop_heartbeat()
                self.logger.info("Plato session heartbeat stopped")
            except Exception as e:
                self.logger.warning(f"Error stopping Plato heartbeat: {e}")

    async def _complete_chronos_session(
        self,
        status: str,
        exit_code: int = 0,
        error_message: str | None = None,
        result: dict | None = None,
    ) -> None:
        """Report session completion to Chronos.

        Args:
            status: Final status ('completed' or 'failed').
            exit_code: Exit code from world runner.
            error_message: Error message if failed.
            result: Final observation/result data from the world. Persisted on the
                session record so consumers can access it via get_details() without
                needing to query the trajectory endpoint separately.
        """
        if not self.session.otel_url or not self.session.session_id:
            return

        base_url = self.session.otel_url.removesuffix("/api/otel")
        url = f"{base_url}/api/sessions/{self.session.session_id}/complete"
        api_key = os.environ.get("PLATO_API_KEY", "")

        payload: dict = {"status": status, "exit_code": exit_code, "error_message": error_message}
        if result is not None:
            payload["result"] = result

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    url,
                    json=payload,
                    headers={"X-API-Key": api_key, "Content-Type": "application/json"},
                )
                if resp.status_code < 300:
                    self.logger.info(f"Reported session {status} to Chronos")
                else:
                    self.logger.warning(f"Chronos complete returned {resp.status_code}: {resp.text}")
        except Exception as e:
            self.logger.warning(f"Failed to report session completion to Chronos: {e}")

    async def save_state(self) -> None:
        """Persist world state to Chronos DB."""
        if not self.config.state.enabled or self._state is None:
            return

        ws_snapshots: dict[str, WorkspaceSnapshot] = {}
        if self._workspaces:
            for name, ws in self._workspaces.items():
                ws_dict = await ws.to_state_dict()
                ws_snapshots[name] = WorkspaceSnapshot(**ws_dict)
            self._state.workspaces = ws_snapshots

        # Append to state history
        self._state.state_history.append(
            StateHistoryEntry(
                step=self._step_count,
                timestamp=datetime.now(UTC).isoformat(),
                workspaces=ws_snapshots,
            )
        )

        await self._upload_state(self._state.model_dump())

    async def load_state(self, session_id: str | None = None) -> bool:
        """Load world state from Chronos DB and restore tracked workspaces.

        Args:
            session_id: Session to load state from. Defaults to the current session.
        """
        if not self.config.state.enabled:
            return False

        workspace_specs = self.config.state.workspaces
        use_workspace_specs_mode = bool(workspace_specs)
        sid = session_id or self.session.session_id
        if not sid and not use_workspace_specs_mode:
            return False

        state_applied = False
        if sid:
            data = await self._download_state(sid)
            if data is None:
                if not use_workspace_specs_mode:
                    return False
            elif not data:
                self.logger.info("State payload for session %s is empty; starting fresh", sid)
                if not use_workspace_specs_mode:
                    return False
            else:
                if not self._apply_state(data):
                    return False
                state_applied = True

        # Restore tracked workspaces from the exact checkpoint recorded in state.
        # When resuming cross-session, the source session may have used
        # different workspace repo names. Use resume_workspaces config
        # to override, or fall back to the saved snapshot repo name.
        resume_repos = self.config.state.resume_workspaces
        saved_snapshots = self._state.workspaces if self._state else {}
        restored_any = False
        for name, workspace in self._workspaces.items():
            if workspace.tracked:
                snap = saved_snapshots.get(name)
                if use_workspace_specs_mode:
                    spec = (workspace_specs.get(name) or "").strip()
                    if not spec:
                        self.logger.info(
                            "State workspaces has no entry for tracked workspace '%s'; treating as empty workspace",
                            name,
                        )
                        continue
                    if ":" in spec:
                        source_session_id, exact_step = spec.split(":", 1)
                        source_session_id = source_session_id.strip()
                        exact_step = exact_step.strip()
                    else:
                        source_session_id = (session_id or self.config.state.resume_from or "").strip()
                        exact_step = spec
                    if not source_session_id:
                        raise RuntimeError(
                            f"Workspace resume spec for '{name}' must include session_id:step (got '{spec}')"
                        )
                    if not exact_step:
                        raise RuntimeError(f"Workspace resume spec for '{name}' is missing step name (got '{spec}')")
                    should_record_resume_input = source_session_id != (self.session.session_id or "")
                else:
                    if not snap:
                        self.logger.info(
                            "State has no snapshot for tracked workspace '%s'; treating as empty workspace",
                            name,
                        )
                        continue
                    if not snap.steps:
                        self.logger.info(
                            "State snapshot for tracked workspace '%s' has no saved step; treating as empty workspace",
                            name,
                        )
                        continue
                    exact_step = snap.steps[-1]
                    source_session_id = (session_id or "").strip()
                    should_record_resume_input = bool(session_id)

                original = {
                    "session_id": workspace.session_id,
                    "repo_name": workspace.repo_name,
                    "repo_id": workspace.repo_id,
                    "s3_bucket": workspace.s3_bucket,
                    "s3_prefix": workspace.s3_prefix,
                }
                source_session_public_id: str | None = None
                source_repo_name: str | None = None
                source_ref_public_id: str | None = None
                try:
                    if source_session_id:
                        workspace.session_id = source_session_id

                    # Override repo config for cross-session resume
                    override_repo = resume_repos.get(name)
                    if (
                        not override_repo
                        and not use_workspace_specs_mode
                        and source_session_id
                        and snap
                        and snap.repo_name
                    ):
                        override_repo = snap.repo_name
                    if override_repo and source_session_id:
                        resolved = await self._resolve_workspace_repo_by_name(override_repo)
                        workspace.repo_name = override_repo
                        workspace.repo_id = resolved.repo_id
                        workspace.s3_bucket = resolved.s3_bucket
                        workspace.s3_prefix = resolved.s3_prefix
                        # Force credential refresh for the new repo
                        workspace._sts_credentials = {}
                        workspace._sts_expires_at = 0

                    self.logger.info(
                        f"Restoring workspace '{name}' from session '{workspace.session_id}' "
                        f"(repo={workspace.repo_name}, step={exact_step})"
                    )
                    restored = await workspace.restore(exact_step)
                    if not restored:
                        raise RuntimeError(
                            f"Workspace '{name}' step '{exact_step}' has no DVC files "
                            f"(session={workspace.session_id}, repo={workspace.repo_name})"
                        )
                    self.logger.info(f"Restored workspace '{name}' from step '{exact_step}'")
                    restored_any = True
                    if self._state and name in self._state.workspaces:
                        self._state.workspaces[name].steps = [exact_step]
                    source_session_public_id = workspace.session_id
                    source_repo_name = workspace.repo_name
                    source_ref_public_id = getattr(workspace, "_last_restored_source_ref_public_id", "") or None
                except Exception as e:
                    self.logger.exception(
                        "Failed to restore workspace '%s' from session '%s' (repo=%s, step=%s)",
                        name,
                        workspace.session_id,
                        workspace.repo_name,
                        exact_step,
                    )
                    raise RuntimeError(
                        f"Failed to restore workspace '{name}' from session '{workspace.session_id}' "
                        f"(repo={workspace.repo_name}, step={exact_step}): {e}"
                    ) from e
                finally:
                    workspace.session_id = original["session_id"]
                    workspace.repo_name = original["repo_name"]
                    workspace.repo_id = original["repo_id"]
                    workspace.s3_bucket = original["s3_bucket"]
                    workspace.s3_prefix = original["s3_prefix"]
                    # Force credential refresh back to current repo
                    workspace._sts_credentials = {}
                    workspace._sts_expires_at = 0

                if should_record_resume_input:
                    if source_ref_public_id:
                        await workspace._record_workspace_ref(
                            exact_step,
                            "input",
                            {},
                            source_ref_public_id=source_ref_public_id,
                        )
                    elif source_session_public_id and source_repo_name:
                        await workspace._record_workspace_ref(
                            exact_step,
                            "input",
                            {},
                            source_session_public_id=source_session_public_id,
                            source_repo_name=source_repo_name,
                            source_step_name=exact_step,
                        )
                    else:
                        raise RuntimeError(
                            f"Failed to record resume lineage for workspace '{name}' "
                            f"(repo={workspace.repo_name}, step={exact_step}): missing source metadata"
                        )

        return restored_any or state_applied

    def _apply_state(self, data: dict) -> bool:
        """Apply a state dict to the world's in-memory state."""
        if not self._state_class:
            return False
        self._state = self._state_class.model_validate(data)  # type: ignore[assignment]
        return True

    async def _try_resume(self) -> bool:
        """Try to resume from saved state. Returns True if resumed.

        Loads state and workspace data from Chronos so we pick up
        where we left off.
        """
        if not self.config.state.enabled:
            return False

        resume_sid = self.config.state.resume_from or None
        if not resume_sid and not self.config.state.workspaces:
            return False
        restored = await self.load_state(session_id=resume_sid)
        return restored

    def _get_chronos_base_url(self) -> str:
        """Get the Chronos API base URL from session config."""
        if self.session.chronos_url:
            return self.session.chronos_url.rstrip("/")
        if self.session.otel_url:
            return self.session.otel_url.removesuffix("/api/otel")
        return ""

    async def _upload_state(self, state_data: dict) -> bool:
        """Upload world state dict to Chronos DB."""
        session_id = self.session.session_id
        if not session_id:
            self.logger.warning("Cannot upload state: no session_id")
            return False

        base_url = self._get_chronos_base_url()
        if not base_url:
            self.logger.warning("Cannot upload state: no chronos_url")
            return False

        try:
            api_key = os.environ.get("PLATO_API_KEY", "")
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.put(
                    f"{base_url}/api/sessions/{session_id}/state",
                    json=state_data,
                    headers={"X-API-Key": api_key},
                )
                if resp.status_code == 200:
                    return True
                self.logger.warning(f"State upload failed: {resp.status_code}")
                return False
        except Exception as e:
            self.logger.warning(f"Failed to upload state: {e}")
            return False

    async def _download_state(self, session_id: str) -> dict | None:
        """Download world state dict from Chronos DB. Returns None if not found."""
        base_url = self._get_chronos_base_url()
        if not base_url:
            self.logger.warning("Cannot download state: no chronos_url")
            return None

        try:
            api_key = os.environ.get("PLATO_API_KEY", "")
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(
                    f"{base_url}/api/sessions/{session_id}/state",
                    headers={"X-API-Key": api_key},
                )
                if resp.status_code == 404:
                    self.logger.info(f"No state found for session {session_id}")
                    return None
                resp.raise_for_status()
                self.logger.info(f"Downloaded state from session {session_id}")
                return resp.json()
        except Exception as e:
            self.logger.warning(f"Failed to download state: {e}")
            return None

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

    async def checkpoint(self, label: str) -> None:
        """Save state and commit all tracked workspaces."""
        for name, workspace in self._workspaces.items():
            if workspace.tracked:
                self.logger.info(f"Checkpoint workspace '{name}' at '{label}'")
                await workspace.commit(label)
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
        api_key = os.environ.get("PLATO_API_KEY", "")
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{chronos_url}/api/workspace-repos/resolve",
                json={"name": repo_name},
                headers={"X-API-Key": api_key},
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
        api_key = os.environ.get("PLATO_API_KEY", "")

        if not chronos_url:
            raise RuntimeError(
                f"Cannot resolve workspace repo '{repo_name}': no chronos_url configured. "
                "Set session.chronos_url or session.otel_url."
            )

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{chronos_url}/api/workspace-repos/resolve",
                json={"name": repo_name},
                headers={"X-API-Key": api_key},
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

    def get_env(self, alias: str) -> Environment | None:
        """Get an environment by alias."""
        if not self.plato_session:
            self.logger.warning("Cannot get env: Plato session not connected")
            return None
        return self.plato_session.get_env(alias)

    @property
    def envs(self) -> list[Environment]:
        """Get all environments in the Plato session."""
        if not self.plato_session:
            return []
        return self.plato_session.envs

    # ------------------------------------------------------------------
    # run() and helpers
    # ------------------------------------------------------------------

    async def run(
        self,
        config: ConfigT,
        session: SessionConfig | None = None,
        dev: DevConfig | None = None,
        runtime: RuntimeConfig | None = None,
    ) -> None:
        """Run the world: reset -> step until done -> close."""
        self.config = config
        self.session = session or SessionConfig()
        self.dev = dev or DevConfig()
        self.runtime = runtime or VMRuntimeConfig()
        self._step_count = 0

        self.logger.info(f"Starting world '{self.name}'")

        if self.config.state.enabled:
            Path(self.config.state.path).mkdir(parents=True, exist_ok=True)

        self._setup_session()

        plato_version = _get_plato_version()
        world_version = self.get_version()
        self.logger.info(f"World version: {world_version}, Plato SDK version: {plato_version}")

        await self._connect_plato_session()

        tracer = get_tracer("plato.world")

        run_error: Exception | None = None
        with tracer.start_as_current_span("world") as root_span:
            root_span.set_attribute("plato.world.name", self.name)
            root_span.set_attribute("plato.world.version", self.get_version())
            root_span.set_attribute("plato.session.id", self.session.session_id)
            root_span.set_attribute("plato.phase", "world_start")

            try:
                await self._run_loop(tracer)
            except Exception as e:
                run_error = e
                if isinstance(e, RequiresHumanAnnotation):
                    self.logger.warning(
                        "RAISING REQUIRES_HUMAN_ANNOTATION: title=%s items=%d message=%s",
                        e.request.title,
                        len(e.request.items),
                        str(e),
                    )
                    root_span.set_attribute("plato.requires_human_annotation", True)
                    root_span.set_attribute("plato.human_annotation.title", e.request.title)
                    root_span.add_event(
                        "requires_human_annotation",
                        {
                            "message": str(e),
                            "items": len(e.request.items),
                        },
                    )
                else:
                    root_span.set_status(StatusCode.ERROR, str(e))
                    root_span.record_exception(e)

                    # Log error as a dedicated span so it's clearly visible in traces
                    import traceback

                    with tracer.start_as_current_span("world_error") as err_span:
                        err_span.set_status(StatusCode.ERROR, str(e))
                        err_span.set_attribute("error.type", type(e).__name__)
                        err_span.set_attribute("error.message", str(e))
                        err_span.set_attribute("error.traceback", traceback.format_exc())
                        err_span.record_exception(e)
            finally:
                await self.close()
                await self._disconnect_plato_session()

        await self._finalize(run_error)

    def _setup_session(self) -> None:
        """Initialize OTel tracing and session info.

        Parent trace context is resolved in this order:
        1. ``SessionConfig.parent_trace_id`` / ``parent_span_id`` (set by
           Chronos when it has trace context for the parent session).
        2. World config extra fields ``parent_trace_id`` / ``parent_span_id``
           (set by a parent world that passes its trace context in world_config).
        3. Environment variables ``OTEL_TRACE_ID`` / ``OTEL_PARENT_SPAN_ID``
           (fallback for manual propagation).
        """
        if not self.session.session_id:
            return

        self._session_id = self.session.session_id
        os.environ["SESSION_ID"] = self.session.session_id

        if self.session.otel_url:
            agent_otel_url = self.session.otel_url
            if "localhost" in agent_otel_url or "127.0.0.1" in agent_otel_url:
                agent_otel_url = agent_otel_url.replace("localhost", "host.docker.internal")
                agent_otel_url = agent_otel_url.replace("127.0.0.1", "host.docker.internal")
            os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = agent_otel_url
            os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http/protobuf"

        if self.session.otel_url:
            # Resolve parent trace context (SessionConfig > config extras > env vars)
            parent_trace_id = (
                getattr(self.session, "parent_trace_id", None)
                or (self.config.model_extra or {}).get("parent_trace_id")
                or os.environ.get("OTEL_TRACE_ID")
            )
            parent_span_id = (
                getattr(self.session, "parent_span_id", None)
                or (self.config.model_extra or {}).get("parent_span_id")
                or os.environ.get("OTEL_PARENT_SPAN_ID")
            )

            if parent_trace_id and parent_span_id:
                logger.debug(f"Linking to parent trace: trace_id={parent_trace_id}, span_id={parent_span_id}")

            logger.debug(f"Initializing OTel tracing with endpoint: {self.session.otel_url}")
            init_tracing(
                service_name=f"world-{self.name}",
                session_id=self.session.session_id,
                otlp_endpoint=self.session.otel_url,
                parent_trace_id=parent_trace_id,
                parent_span_id=parent_span_id,
            )
        else:
            logger.debug("No otel_url in session - OTel tracing disabled")

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
                backup=marker.tracked,
                dvcignore=marker.dvcignore,
                s3_bucket=repo_info.s3_bucket,
                s3_prefix=repo_info.s3_prefix,
                repo_id=repo_info.repo_id,
                repo_name=repo_info.repo_name,
                chronos_url=repo_info.chronos_url,
                api_key=repo_info.api_key,
                session_id=self.session.session_id if self.session else "",
            )

            await workspace.init()

            self._workspaces[field_name] = workspace
            # workspace.path is the content directory (data/ for tracked, root otherwise)
            object.__setattr__(self.config, field_name, workspace.path)
            self.logger.info(
                f"Workspace '{field_name}' at {ws_path} "
                f"(tracked={marker.tracked}, mount_path={workspace._mount_path}, repo={repo_info.repo_name})"
            )

    async def _generate_tailscale_auth_key(self, api_key: str) -> str:
        """Generate a short-lived, single-use auth key via the Tailscale API."""
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.tailscale.com/api/v2/tailnet/-/keys",
                auth=("", api_key),
                json={
                    "capabilities": {
                        "devices": {
                            "create": {
                                "reusable": False,
                                "ephemeral": True,
                                "preauthorized": True,
                            }
                        }
                    },
                    "expirySeconds": 300,
                },
            )
            if resp.status_code != 200:
                raise RuntimeError(f"Tailscale API key generation failed (HTTP {resp.status_code}): {resp.text}")
            return resp.json()["key"]

    async def _setup_tailscale(self) -> None:
        """Join a Tailscale tailnet using the API key to generate an auth key.

        Raises RuntimeError if any step fails.
        """
        ts = self.config.tailscale
        if not ts.enabled:
            return

        if shutil.which("tailscale") is None or shutil.which("tailscaled") is None:
            self.logger.info("Installing Tailscale...")
            proc = await asyncio.create_subprocess_shell(
                "curl -fsSL https://tailscale.com/install.sh | sh",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                raise RuntimeError(f"Tailscale install failed (rc={proc.returncode}): {stderr.decode().strip()}")
        else:
            self.logger.info("Tailscale already installed, skipping install")

        async def _tailscale_status() -> dict[str, Any] | None:
            proc = await asyncio.create_subprocess_exec(
                "sudo",
                "tailscale",
                "status",
                "--json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _stderr = await proc.communicate()
            if proc.returncode != 0:
                return None
            return json.loads(stdout.decode())

        status = await _tailscale_status()
        is_online = bool(status and status.get("Self", {}).get("Online"))

        if not is_online:
            # Containers don't have systemd, so start tailscaled manually if needed.
            self.logger.info("Starting tailscaled daemon...")
            self._tailscaled_proc = await asyncio.create_subprocess_exec(
                "sudo",
                "tailscaled",
                "--state=/var/lib/tailscale/tailscaled.state",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await asyncio.sleep(2)

            if not ts.api_key:
                raise RuntimeError(
                    "tailscale.enabled is True but tailscale.api_key is not set "
                    "and no existing tailnet connection was found"
                )

            # Generate a short-lived auth key via the Tailscale API only when reconnecting.
            self.logger.info("Generating Tailscale auth key...")
            auth_key = await self._generate_tailscale_auth_key(ts.api_key)

            self.logger.info("Connecting to tailnet...")
            proc = await asyncio.create_subprocess_exec(
                "sudo",
                "tailscale",
                "up",
                f"--auth-key={auth_key}",
                "--accept-dns=false",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                raise RuntimeError(f"'tailscale up' failed (rc={proc.returncode}): {stderr.decode().strip()}")

            status = await _tailscale_status()
            if status is None:
                raise RuntimeError("'tailscale status' failed after connect")
        else:
            self.logger.info("Tailscale already connected, skipping auth/up")

        assert status is not None
        self_name = status.get("Self", {}).get("HostName", "unknown")
        peers = status.get("Peer", {})
        peer_names = [p.get("HostName", "?") for p in peers.values()]
        self.logger.info("Tailscale connected as '%s', %d peer(s) visible", self_name, len(peer_names))
        self.logger.debug("Tailscale peers: %s", ", ".join(peer_names) or "(none)")

        # MagicDNS doesn't reliably configure the system resolver in
        # containers, so write /etc/hosts entries for all tailscale peers.
        hosts_lines = []
        for peer in peers.values():
            # DNSName is the tailscale MagicDNS name (e.g. "plato-a100.tail1234.ts.net.")
            # HostName is the OS hostname (e.g. "instance-20260226-193911")
            dns_name = peer.get("DNSName", "").rstrip(".")
            os_hostname = peer.get("HostName", "")
            # Extract short name from DNS (e.g. "plato-a100" from "plato-a100.tail1234.ts.net")
            short_name = dns_name.split(".")[0] if dns_name else ""
            addrs = peer.get("TailscaleIPs", [])
            if addrs:
                ipv4 = next((a for a in addrs if "." in a), None)
                if ipv4:
                    names = []
                    if short_name:
                        names.append(short_name)
                    if os_hostname and os_hostname != short_name:
                        names.append(os_hostname)
                    if names:
                        hosts_lines.append(f"{ipv4}\t{' '.join(names)}")
        if hosts_lines:
            try:
                hosts_block = "\n# Tailscale peers\n" + "\n".join(hosts_lines) + "\n"
                hosts_path = Path("/etc/hosts")
                existing = hosts_path.read_text()
                hosts_path.write_text(existing + hosts_block)
                self.logger.info("Added %d tailscale peer(s) to /etc/hosts", len(hosts_lines))
                self.logger.debug("Tailscale /etc/hosts entries: %s", ", ".join(hosts_lines))
            except Exception as e:
                self.logger.warning(f"Failed to update /etc/hosts: {e}")

    async def _run_loop(self, tracer: Any) -> None:
        """Execute the reset → step → checkpoint loop."""
        # Start VM system metrics collection
        if self.session.otel_url and self.session.session_id:
            instrument_system_metrics(
                otlp_endpoint=self.session.otel_url,
                session_id=self.session.session_id,
                env_alias="world",
                job_id=os.environ.get("JOB_ID", ""),
            )

        # Auto-discover and initialize declared workspaces (Workspace markers on config)
        await self._init_declared_workspaces()

        # Optional Tailscale VPN setup
        await self._setup_tailscale()

        # Resume from saved state if available (before reset so state is populated)
        resumed = await self._try_resume()
        if resumed:
            self.logger.info("Resumed from saved state")

        # Start NFS server AFTER workspaces are restored (FUSE mounts must exist
        # before NFS begins exporting with crossmnt).
        await self._start_transport()

        # Reset phase — world-specific initialization
        with tracer.start_as_current_span("reset") as reset_span:
            reset_span.set_attribute("plato.phase", "reset")
            reset_span.set_attribute("plato.world.name", self.name)
            obs = await self.reset()
            obs_data = obs.model_dump()
            reset_span.set_attribute("plato.observation", json.dumps(obs_data, default=str))

        self.logger.info(f"World reset complete: {obs}")

        while True:
            self._step_count += 1

            with tracer.start_as_current_span(f"step_{self._step_count}") as step_span:
                step_span.set_attribute("plato.phase", "step")
                step_span.set_attribute("plato.world.name", self.name)
                step_span.set_attribute("plato.step.number", self._step_count)
                self._current_step_id = format(step_span.get_span_context().span_id, "016x")
                result = await self.step()
                step_span.set_attribute("plato.step.done", result.done)
                if result.observation is not None:
                    obs_data = result.observation.model_dump()
                    step_span.set_attribute("plato.step.observation", json.dumps(obs_data, default=str))

            self.logger.info(f"Step {self._step_count}: done={result.done}")

            if not result.done:
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

    async def _finalize(self, run_error: Exception | None) -> None:
        """Report completion/failure to Chronos and shutdown tracing."""
        await shutdown_metrics()

        is_dev = bool(self.dev and self.dev.world)
        final_result = getattr(self, "_final_result", None)
        if run_error and isinstance(run_error, RequiresHumanAnnotation):
            payload: dict[str, Any] = {}
            if isinstance(final_result, dict):
                payload.update(final_result)
            payload.update(run_error.result_payload())
            self.logger.warning(
                "Completing session as needs_human_annotation: title=%s items=%d",
                run_error.request.title,
                len(run_error.request.items),
            )
            await self._complete_chronos_session(
                "needs_human_annotation",
                exit_code=0,
                error_message=str(run_error),
                result=payload,
            )
        elif not is_dev:
            if run_error:
                error_msg = f"{type(run_error).__name__}: {run_error}"
                await self._complete_chronos_session(
                    "failed",
                    exit_code=1,
                    error_message=error_msg,
                    result=final_result,
                )
            else:
                await self._complete_chronos_session("completed", exit_code=0, result=final_result)
        else:
            self.logger.info(
                "Skipping Chronos completion in dev-world mode (run_error=%s)",
                type(run_error).__name__ if run_error else "None",
            )

        shutdown_tracing()
        self._session_id = None

        if run_error and not isinstance(run_error, RequiresHumanAnnotation):
            raise run_error

        if isinstance(run_error, RequiresHumanAnnotation):
            self.logger.info(
                "World '%s' ended: requires human annotation (%s)",
                self.name,
                run_error.request.title,
            )
            return

        self.logger.info(f"World '{self.name}' completed after {self._step_count} steps")
