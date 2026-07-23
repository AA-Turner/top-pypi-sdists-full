"""Agent execution environments.

``Environment`` is the abstract base class; ``TaskEnvironment`` is the
platform-backed implementation for running hosted Dreadnode tasks, and
``LocalComposeEnvironment`` is the self-hosted variant for users who
already have a ``docker-compose.yaml`` describing the services their
agent needs to reach.
"""

import asyncio
import contextlib
import contextvars
import inspect
import subprocess
import typing as t
from abc import ABC, abstractmethod
from pathlib import Path

from dreadnode.core.templating import render_task_instruction

if t.TYPE_CHECKING:
    from dreadnode.app.api.client import ApiClient

T = t.TypeVar("T")

EnvironmentContext = dict[str, t.Any]
EnvironmentExecution = t.Awaitable[T] | t.Callable[[EnvironmentContext], t.Awaitable[T]]

current_task_environment: contextvars.ContextVar["TaskEnvironment | None"] = contextvars.ContextVar(
    "current_task_environment", default=None
)
"""The provisioned ``TaskEnvironment`` for the current async scope, if any.

Set automatically by ``TaskEnvironment.setup()`` and cleared by
``TaskEnvironment.teardown()``. Scorers, objectives, and other downstream code
can read this to reach the live sandbox (e.g. to run ``env.execute()``) without
plumbing the env through every call signature."""


# Polling contract for the async provision path. The server returns
# ``state="building"`` or ``"provisioning"`` before the sandbox is reachable
# and the SDK polls ``/status`` until ``ready``. These defaults handle cold
# provisions of compose-heavy tasks (image pull + container boot + health
# checks) without saturating the polling endpoint.
_POLLABLE_ENV_STATES: frozenset[str] = frozenset({"building", "provisioning"})
_POLL_MAX_INTERVAL_SEC: float = 5.0
_POLL_DEADLINE_SEC: float = 900.0


class Environment(ABC):
    """Base class for agent execution environments.

    An environment manages the lifecycle of an external system
    (container, kernel, API connection, etc.).

    Example::

        env = DockerEnvironment(image="python:3.11")
        agent = Agent(name="runner", tools=[bash_tool])
        result = await env.run(agent.run("Run the tests"))
    """

    @abstractmethod
    async def setup(self) -> EnvironmentContext:
        """Initialize the environment and return its context dict."""
        ...

    @abstractmethod
    async def teardown(self) -> None:
        """Clean up the environment."""
        ...

    async def reset(self) -> EnvironmentContext:
        """Reset for a new attempt. Default: teardown + setup."""
        await self.teardown()
        return await self.setup()

    async def get_state(self) -> EnvironmentContext:
        """Return current state (for debugging/logging). Default: empty."""
        return {}

    async def __aenter__(self) -> "Environment":
        await self.setup()
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.teardown()

    @t.overload
    async def run(self, execution: t.Awaitable[T]) -> T: ...

    @t.overload
    async def run(
        self,
        execution: t.Callable[[EnvironmentContext], t.Awaitable[T]],
    ) -> T: ...

    async def run(self, execution: EnvironmentExecution[T]) -> T:
        """Run work within this environment.

        Sets up the environment, awaits the work, and tears down afterward.

        Args:
            execution: Either an awaitable to run directly (for example
                ``agent.run("goal")``) or a callable that receives the setup
                context dict and returns an awaitable.

        Returns:
            The execution result.
        """
        try:
            context = await self.setup()
            if callable(execution):
                fn = t.cast("t.Callable[[EnvironmentContext], t.Awaitable[T]]", execution)
                awaitable: t.Awaitable[T] = fn(context)
            else:
                awaitable = execution
            if not inspect.isawaitable(awaitable):
                raise TypeError("Environment.run() expected an awaitable result")
            return await awaitable
        finally:
            await self.teardown()


class TaskEnvironment(Environment):
    """API-backed task environment for running an SDK agent against a hosted task."""

    def __init__(
        self,
        api_client: "ApiClient",
        *,
        org: str,
        workspace: str,
        task_ref: str,
        project_id: str | None = None,
        inputs: dict[str, t.Any] | None = None,
        secret_ids: list[str] | None = None,
        model_overrides: dict[str, str] | None = None,
        timeout_sec: int | None = None,
    ) -> None:
        self.api_client = api_client
        self.org = org
        self.workspace = workspace
        self._task_ref = task_ref
        self.project_id = project_id
        self._inputs = inputs
        self.secret_ids = secret_ids
        self._model_overrides = model_overrides
        self._timeout_sec = timeout_sec
        self._context: EnvironmentContext | None = None
        self._execute_token: str | None = None
        self._contextvar_token: contextvars.Token[TaskEnvironment | None] | None = None

    async def setup(self) -> EnvironmentContext:
        if self._context is not None:
            return dict(self._context)

        request: dict[str, t.Any] = {"task_ref": self._task_ref}
        if self.project_id is not None:
            request["project_id"] = self.project_id
        if self._inputs is not None:
            request["inputs"] = self._inputs
        if self.secret_ids is not None:
            request["secret_ids"] = self.secret_ids
        if self._model_overrides is not None:
            request["model_overrides"] = self._model_overrides
        if self._timeout_sec is not None:
            request["timeout_sec"] = self._timeout_sec

        context = await asyncio.to_thread(
            self.api_client.create_environment,
            self.org,
            self.workspace,
            request,
        )
        # Async provision contract: ``execute_token`` is delivered in this
        # POST response — stash it now before polling can clobber it (polls
        # never carry the token; only the POST does). When ``state`` is
        # ``building``/``provisioning``, ``service_urls`` aren't populated
        # yet; poll ``/status`` until the env is ``ready`` (or ``failed``,
        # which raises), then fold the polled service-side fields back into
        # context so downstream code sees a fully populated environment.
        token = context.get("execute_token")
        if isinstance(token, str) and token:
            self._execute_token = token
        state = context.get("state")
        if state in _POLLABLE_ENV_STATES:
            environment_id = context.get("id")
            if not isinstance(environment_id, str):
                raise RuntimeError("Environment response missing id; cannot poll for provision")
            # Caller's ``timeout_sec`` doubles as the client-side poll budget
            # when set — a request asking for a 600s env shouldn't wait 900s
            # just to discover it can't be provisioned. Unset falls back to
            # the module default.
            deadline = (
                float(self._timeout_sec)
                if isinstance(self._timeout_sec, int) and self._timeout_sec > 0
                else _POLL_DEADLINE_SEC
            )
            status = await self._poll_until_ready(environment_id, deadline_sec=deadline)
            for key in ("state", "service_urls", "instruction", "expires_at"):
                value = status.get(key)
                if value is not None:
                    context[key] = value
        self._context = context
        self._contextvar_token = current_task_environment.set(self)
        return dict(context)

    async def _poll_until_ready(
        self, environment_id: str, *, deadline_sec: float = _POLL_DEADLINE_SEC
    ) -> dict[str, t.Any]:
        """Poll ``GET /environments/{id}/status`` until terminal state.

        Exponential backoff from 1s → ``_POLL_MAX_INTERVAL_SEC`` capped. Total
        wait bounded by ``deadline_sec`` (caller's ``timeout_sec`` when set,
        otherwise the module default). A ``failed`` status raises with the
        server-provided error message.

        A just-created environment's status can 404 for the first few polls: the
        platform tracks the pending env in per-replica memory until the sandbox
        row is persisted, so a status poll routed to a different API replica than
        the one that handled the POST sees neither the tracker entry nor the row
        yet. Treat that 404 as "still provisioning" and keep polling until the
        deadline instead of aborting a provision that will succeed.
        """
        from dreadnode.app.api.client import NotFoundError

        interval = 1.0
        deadline = asyncio.get_event_loop().time() + deadline_sec
        while True:
            try:
                status = await asyncio.to_thread(
                    self.api_client.get_environment_status,
                    self.org,
                    self.workspace,
                    environment_id,
                )
            except NotFoundError:
                if asyncio.get_event_loop().time() >= deadline:
                    raise
                await asyncio.sleep(interval)
                interval = min(interval * 1.5, _POLL_MAX_INTERVAL_SEC)
                continue
            state = status.get("state")
            if state == "ready":
                return status
            if state == "failed":
                raise RuntimeError(
                    f"Environment {environment_id} failed to provision: "
                    f"{status.get('error') or 'unknown error'}"
                )
            if asyncio.get_event_loop().time() >= deadline:
                raise TimeoutError(
                    f"Environment {environment_id} did not reach ready within "
                    f"{deadline_sec}s (last state={state})"
                )
            await asyncio.sleep(interval)
            interval = min(interval * 1.5, _POLL_MAX_INTERVAL_SEC)

    async def teardown(self) -> None:
        if self._contextvar_token is not None:
            # The token may have been created in a different asyncio Context (for
            # example setup() and teardown() ran in separate Jupyter cells). A
            # failed reset must not block the actual environment deletion below.
            with contextlib.suppress(ValueError):
                current_task_environment.reset(self._contextvar_token)
            self._contextvar_token = None

        if self._context is None:
            return

        environment_id = self.id
        if environment_id is None:
            self._context = None
            self._execute_token = None
            return

        await asyncio.to_thread(
            self.api_client.delete_environment,
            self.org,
            self.workspace,
            environment_id,
        )
        self._context = None
        self._execute_token = None

    async def get_state(self) -> EnvironmentContext:
        return self.context

    def render_instruction(self, *, inputs: dict[str, t.Any] | None = None) -> str | None:
        """Render the task's instruction template using this environment's ``service_urls``.

        Merges the environment's ``service_urls`` with caller-provided
        ``inputs`` (inputs win on conflict). Unknown placeholders are left
        in place so the caller can inspect what was not resolved.
        """
        merged_inputs: dict[str, t.Any] = {}
        if self._inputs:
            merged_inputs.update(self._inputs)
        if inputs:
            merged_inputs.update(inputs)
        return render_task_instruction(
            self.instruction,
            service_urls=self.service_urls,
            inputs=merged_inputs or None,
        )

    async def execute(self, command: str, *, timeout_sec: int = 30) -> tuple[int, str]:
        """Execute a shell command inside the environment's sandbox.

        Returns ``(exit_code, output)``. Combined stdout/stderr.
        """
        environment_id = self.id
        token = self._execute_token
        if environment_id is None or token is None:
            raise RuntimeError(
                "TaskEnvironment is not provisioned — call setup() (or use "
                "as an async context manager) before execute()."
            )
        payload = await asyncio.to_thread(
            self.api_client.execute_in_environment,
            self.org,
            self.workspace,
            environment_id,
            command=command,
            timeout_sec=timeout_sec,
            execute_token=token,
        )
        return int(payload["exit_code"]), str(payload["output"])

    async def logs(self) -> str:
        """Return the tail of the sandbox server log for this environment."""
        environment_id = self.id
        if environment_id is None:
            raise RuntimeError(
                "TaskEnvironment is not provisioned — call setup() (or use "
                "as an async context manager) before logs()."
            )
        payload = await asyncio.to_thread(
            self.api_client.get_environment_logs,
            self.org,
            self.workspace,
            environment_id,
        )
        value = payload.get("logs")
        return value if isinstance(value, str) else ""

    @property
    def context(self) -> EnvironmentContext:
        return dict(self._context or {})

    @property
    def instruction(self) -> str | None:
        value = self.context.get("instruction")
        return value if isinstance(value, str) else None

    @property
    def id(self) -> str | None:
        value = self.context.get("id")
        return str(value) if value is not None else None

    @property
    def task_ref(self) -> str | None:
        value = self.context.get("task_ref")
        return value if isinstance(value, str) else None

    @property
    def service_urls(self) -> dict[str, dict[str, t.Any]] | None:
        value = self.context.get("service_urls")
        if isinstance(value, dict):
            return t.cast("dict[str, dict[str, t.Any]]", value)
        return None

    @property
    def inputs(self) -> dict[str, t.Any] | None:
        """Template-substitution inputs passed at construction time.

        Read-only — returns a fresh copy so callers can't mutate internal
        state. ``None`` when no inputs were supplied.
        """
        return dict(self._inputs) if self._inputs else None

    @property
    def task_verification(self) -> dict[str, t.Any] | None:
        """Snapshot of the task's ``verification`` config as of provision time.

        Training rollouts, optimization trials, and ad-hoc grading code read
        this to dispatch ``env_flag`` / ``env_script`` / ``llm_judge`` style
        verification without a separate ``GET /tasks/{ref}`` round-trip. The
        value is a copy — callers can't mutate it.

        Returns ``None`` when the task has no verification config or when the
        environment hasn't been set up yet.
        """
        value = self.context.get("task_verification")
        if isinstance(value, dict):
            return t.cast("dict[str, t.Any]", dict(value))
        return None


class LocalComposeEnvironment(Environment):
    """Environment backed by a local ``docker compose`` stack.

    Drop-in replacement for ``TaskEnvironment`` when the target services are
    a local compose file you manage yourself — no platform task registry,
    no ``POST /environments`` round-trip, just ``docker compose up --wait``
    and a context dict the agent's scorer can read.

    Example::

        from pathlib import Path

        env = LocalComposeEnvironment(
            compose_file=Path("./fixtures/juiceshop/docker-compose.yaml"),
            project_name="juiceshop-opt",
            instruction="Find the access log endpoint exposing user data.",
            service_urls={"juiceshop": {"url": "http://localhost:3000", "port": 3000}},
        )
        async with env:
            output = await agent.run(env.instruction)

    ``service_urls`` is a manually-declared map — the agent reads it from the
    context to know where services live. If your compose file uses dynamic
    host port mappings, override ``_resolve_service_urls`` on a subclass
    to read them from ``docker compose ps --format json``.
    """

    def __init__(
        self,
        compose_file: "Path | str",
        *,
        project_name: str | None = None,
        instruction: str | None = None,
        service_urls: dict[str, dict[str, t.Any]] | None = None,
        wait_timeout_sec: int = 120,
        env_vars: dict[str, str] | None = None,
    ) -> None:
        self.compose_file = Path(compose_file).resolve()
        # ``docker compose -p`` prefixes container / network names. Default to
        # the parent directory name — matches the behavior of running
        # ``docker compose up`` from the file's directory without ``-p``.
        self.project_name = project_name or self.compose_file.parent.name
        self._instruction = instruction
        self._service_urls = service_urls or {}
        self._wait_timeout_sec = wait_timeout_sec
        self._env_vars = env_vars
        self._context: EnvironmentContext | None = None

    async def setup(self) -> EnvironmentContext:
        if self._context is not None:
            return dict(self._context)

        # ``--wait`` blocks until healthchecks pass; honors Compose's
        # ``healthcheck:`` directives. Without it, we'd race the agent
        # against a service that hasn't bound its port yet.
        await asyncio.to_thread(
            self._compose,
            "up",
            "-d",
            "--wait",
            "--wait-timeout",
            str(self._wait_timeout_sec),
        )

        self._context = {
            "id": self.project_name,
            "state": "ready",
            "task_ref": None,
            "instruction": self._instruction,
            "service_urls": self._service_urls,
        }
        return dict(self._context)

    async def teardown(self) -> None:
        if self._context is None:
            return
        # ``--volumes`` drops compose-managed volumes — the run is
        # disposable; next setup starts clean. Omit if you want to persist
        # state across trials (useful for long-lived reference data).
        await asyncio.to_thread(self._compose, "down", "--volumes", "--remove-orphans")
        self._context = None

    async def execute(
        self,
        command: str,
        *,
        service: str,
        timeout_sec: int = 30,
    ) -> tuple[int, str]:
        """Run ``command`` inside one of the compose services.

        Unlike ``TaskEnvironment.execute`` (which targets a single
        sandbox), compose stacks have N services; pick one by name via
        ``service=`` — it must match a key in the compose file.
        """
        if self._context is None:
            raise RuntimeError(
                "LocalComposeEnvironment is not provisioned — call setup() "
                "(or use as an async context manager) before execute()."
            )
        result = await asyncio.to_thread(
            self._compose_capture,
            "exec",
            "-T",  # no TTY — keeps stdout/stderr clean for capture
            service,
            "sh",
            "-c",
            command,
            timeout_sec=timeout_sec,
        )
        return result.returncode, (result.stdout or "") + (result.stderr or "")

    # ── internal helpers ──

    def _compose(self, *args: str) -> None:
        subprocess.run(  # noqa: S603
            self._base_cmd() + list(args),
            check=True,
            capture_output=True,
            text=True,
            env={**(self._env_vars or {}), **_inherit_env()},
        )

    def _compose_capture(self, *args: str, timeout_sec: int) -> "subprocess.CompletedProcess[str]":
        return subprocess.run(  # noqa: S603
            self._base_cmd() + list(args),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env={**(self._env_vars or {}), **_inherit_env()},
            check=False,
        )

    def _base_cmd(self) -> list[str]:
        return [
            "docker",
            "compose",
            "-p",
            self.project_name,
            "-f",
            str(self.compose_file),
        ]


def _inherit_env() -> dict[str, str]:
    """Inherit PATH and HOME so the subprocess finds ``docker``."""
    import os

    return {k: os.environ[k] for k in ("PATH", "HOME") if k in os.environ}
