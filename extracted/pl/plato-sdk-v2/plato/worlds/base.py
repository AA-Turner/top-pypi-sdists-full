"""Base world class for Plato worlds."""

from __future__ import annotations

import asyncio
import importlib.metadata
import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Generic, get_args, get_origin

import httpx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from pydantic import BaseModel as PydanticBaseModel
from typing_extensions import TypeVar

from plato.agents.runner import AgentRunner, create_runtime
from plato.agents.runtime.workspace import NFSWorkspace, RsyncWorkspace, Workspace
from plato.llm import LLMClient
from plato.otel import get_tracer, init_tracing, shutdown_tracing
from plato.runtime import RuntimeConfig, VMRuntimeConfig
from plato.v2.async_.session import Session
from plato.vm_metrics import instrument_system_metrics, shutdown_metrics
from plato.worlds.config import AgentConfig, DevConfig, LLMConfig, RunConfig, SessionConfig, WorkspaceMode
from plato.worlds.models import Observation, StepResult
from plato.worlds.restic import ResticCheckpointMixin
from plato.worlds.s3 import download_from_s3, upload_to_s3
from plato.worlds.schema import get_world_schema

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment
    from plato.worlds.result_store import ResultStore

logger = logging.getLogger(__name__)

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


class BaseWorld(ResticCheckpointMixin, ABC, Generic[ConfigT, StateT]):
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
        self._workspace: Workspace | None = None
        self._ssh_key_path: Path | None = None
        self.__init_restic__()

    @property
    def state(self) -> StateT:
        """Access the typed state. Lazily initialized on first access."""
        if self._state is None and self._state_class:
            self._state = self._state_class()
        return self._state  # type: ignore[return-value]

    def reset_state(self) -> None:
        """Reset state to defaults."""
        if self._state_class:
            self._state = self._state_class()

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
        await self._cleanup_agent_containers()
        await self._cleanup_agent_envs()

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
        except Exception:
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

    def agent(self, config: AgentConfig, workspace: Workspace | None = None) -> AgentRunner:
        """Get an agent runner for the given config."""
        ws = self._workspace if workspace is None else workspace
        runtime = create_runtime(
            config,
            session=self.plato_session,
            ssh_key_path=self._ssh_key_path,
        )
        return AgentRunner(config, runtime, workspace=ws, agent_containers=self._agent_containers)

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
        await self._create_workspace()

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

    async def _create_workspace(self) -> None:
        """Create the workspace instance from config after session is connected."""
        assert self._ssh_key_path is not None, "SSH key must be set before creating workspace"
        ssh_key_path = self._ssh_key_path
        ws_config = self.config.workspace

        if ws_config.mode == WorkspaceMode.nfs:
            mesh_ip = None
            if self.plato_session:
                for env in self.plato_session.envs:
                    if env.alias == "runtime":
                        try:
                            mesh_ip = await env.get_mesh_ip()
                        except Exception:
                            pass
                        break
            if not mesh_ip or not self.plato_session:
                raise RuntimeError("NFS mode requested but mesh IP not available")
            self._workspace = NFSWorkspace(ws_config.path, mesh_ip, ssh_key_path)
        else:
            self._workspace = RsyncWorkspace(ws_config.path, ssh_key_path)

        self.logger.info(f"Workspace mode: {type(self._workspace).__name__} (path={self._workspace.path})")
        await self._workspace.initialize()

        # Register the default workspace for restic checkpointing
        self.register_workspace("workspace", ws_config.path, backup=True)

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

    async def _create_checkpoint(self) -> dict[str, str] | None:
        """Create a checkpoint snapshot of all environments (excluding configured envs)."""
        if not self.plato_session:
            self.logger.warning("Cannot create checkpoint: Plato session not connected")
            return None

        exclude_envs = set(self.config.checkpoint.exclude_envs)
        envs_to_snapshot = [env for env in self.plato_session.envs if env.alias not in exclude_envs]

        if not envs_to_snapshot:
            self.logger.info("No environments to checkpoint (all excluded)")
            return {}

        self.logger.info(
            f"Creating checkpoint for {len(envs_to_snapshot)} environment(s): {[e.alias for e in envs_to_snapshot]}"
        )

        results: dict[str, str] = {}
        for env in envs_to_snapshot:
            try:
                result = await env.snapshot_store()
                artifact_id = result.artifact_id
                results[env.alias] = artifact_id

                if not result.success or result.error:
                    self.logger.error(
                        f"Checkpoint failed for '{env.alias}': {result.error or 'unknown error'} (job_id={env.job_id})"
                    )
                elif artifact_id:
                    self.logger.info(f"Checkpoint created for '{env.alias}': {artifact_id}")
                else:
                    self.logger.warning(
                        f"Checkpoint for '{env.alias}' returned empty artifact_id (job_id={env.job_id})"
                    )
            except Exception as e:
                self.logger.error(f"Failed to checkpoint '{env.alias}': {e}")

        return results

    async def save_state(self) -> None:
        """Persist world state locally and upload to S3."""
        if not self.config.state.enabled or self._state is None:
            return
        data = self._state.model_dump()
        workspaces = self._serialize_workspaces()
        if workspaces:
            data["_workspaces"] = workspaces
        state_file = Path(self.config.state.path) / "world_state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(data, default=str))
        await self._upload_state()

    def load_state(self) -> bool:
        """Load world state from the state directory."""
        if not self.config.state.enabled or not self.config.state.resume:
            return False
        state_file = Path(self.config.state.path) / "world_state.json"
        if not state_file.exists():
            return False
        try:
            data = json.loads(state_file.read_text())
        except (json.JSONDecodeError, OSError):
            return False
        if "_workspaces" in data:
            self._deserialize_workspaces(data.pop("_workspaces"))
        if self._state_class:
            self._state = self._state_class.model_validate(data)  # type: ignore[assignment]
        return True

    def _get_chronos_base_url(self) -> str:
        """Get the Chronos API base URL from session config."""
        if self.session.chronos_url:
            return self.session.chronos_url.rstrip("/")
        if self.session.otel_url:
            return self.session.otel_url.removesuffix("/api/otel")
        return ""

    async def _restore_session_state(self) -> bool:
        """Download state from a previous session via Chronos presigned URL."""
        resume_session = self.config.state.resume_session
        if not resume_session:
            return False

        self.logger.info(f"Restoring state from session {resume_session}")
        return await self._download_state(resume_session)

    async def _upload_state(self) -> bool:
        """Upload world_state.json to S3 via Chronos presigned PUT URL."""
        if not self.config.state.enabled:
            return True

        session_id = self.session.session_id
        if not session_id:
            self.logger.warning("Cannot upload state: no session_id")
            return False

        state_file = Path(self.config.state.path) / "world_state.json"
        if not state_file.exists():
            self.logger.debug("No state file to upload")
            return True

        base_url = self._get_chronos_base_url()
        if not base_url:
            self.logger.warning("Cannot upload state: no chronos_url")
            return False

        return await upload_to_s3(base_url, session_id, "state", state_file.read_bytes(), "application/json")

    async def _download_state(self, resume_session_id: str) -> bool:
        """Download state.json from a previous session via Chronos presigned URL."""
        base_url = self._get_chronos_base_url()
        if not base_url:
            self.logger.warning("Cannot download state: no chronos_url")
            return False

        data = await download_from_s3(base_url, resume_session_id, "state")
        if data is None:
            return False

        state_path = Path(self.config.state.path)
        state_path.mkdir(parents=True, exist_ok=True)
        (state_path / "world_state.json").write_bytes(data)
        self.logger.info(f"Downloaded state from session {resume_session_id}")
        return True

    async def _create_and_upload_checkpoint(self) -> tuple[dict[str, str], bool]:
        """Create a full checkpoint including env snapshots and state upload."""
        env_snapshots = await self._create_checkpoint()
        if env_snapshots is None:
            env_snapshots = {}

        await self._checkpoint_workspaces()

        state_uploaded = True
        if self.config.state.enabled:
            state_uploaded = await self._upload_state()
            if state_uploaded:
                self.logger.info(f"Uploaded state at step {self._step_count}")
            else:
                self.logger.warning(f"Failed to upload state at step {self._step_count}")

        return env_snapshots, state_uploaded

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

        # Try to restore state from a previous session
        resumed = False
        self.logger.info(
            f"State config: resume={self.config.state.resume}, resume_session={self.config.state.resume_session!r}, resume_step={self.config.state.resume_step}"
        )
        if self.config.state.resume:
            if self.config.state.resume_session:
                await self._restore_session_state()
            resumed = self.load_state()
            self.logger.info(f"load_state returned: {resumed}")
        if resumed:
            self.logger.info("Resumed from saved state — skipping full reset")
            if self.config.state.resume_step is not None:
                self._step_count = self.config.state.resume_step

        # Reset phase — sets up workspaces (NFS bind mounts, etc.)
        with tracer.start_as_current_span("reset") as reset_span:
            reset_span.set_attribute("plato.phase", "reset")
            reset_span.set_attribute("plato.world.name", self.name)
            reset_span.set_attribute("plato.world.resumed", resumed)
            obs = await self.reset()
            obs_data = obs.model_dump()
            reset_span.set_attribute("plato.observation", json.dumps(obs_data, default=str))

        # Restore workspace backups AFTER reset (so NFS bind mounts are set up first)
        if resumed and self.config.state.resume_session and self._workspace_paths:
            await self._download_workspace_backup(self.config.state.resume_session)
            resume_step = self.config.state.resume_step
            await self._restore_workspaces(step=resume_step)
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
                await self.save_state()
                if self.config.state.enabled:
                    await self._checkpoint_workspaces()

            if result.done:
                break

        # Capture the final observation for session completion
        self._final_result: dict | None = None
        if result.observation is not None:
            try:
                self._final_result = result.observation.model_dump()
            except Exception:
                pass

    async def _finalize(self, run_error: Exception | None) -> None:
        """Report completion/failure to Chronos and shutdown tracing."""
        await shutdown_metrics()

        is_dev = bool(self.dev and self.dev.world)
        if not is_dev:
            final_result = getattr(self, "_final_result", None)
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

        shutdown_tracing()
        self._session_id = None

        if run_error:
            raise run_error

        self.logger.info(f"World '{self.name}' completed after {self._step_count} steps")
