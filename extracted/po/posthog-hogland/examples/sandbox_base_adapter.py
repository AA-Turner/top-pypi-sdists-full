"""Reference ``SandboxBase`` adapter — vendor this into the PostHog repo.

This file is **not** part of the ``hogland`` runtime package. It imports
from ``products.tasks.backend.services.sandbox`` (PostHog's
``SandboxBase`` and friends), so it won't resolve in this repo's env —
hogland's CI explicitly excludes it from lint and type-check. The
acceptance test is "it imports cleanly once vendored next to
``modal_sandbox.py``".

The point of the file is to give PostHog a thorough mapping showing
every ``SandboxBase`` method routed through the ``hogland`` SDK. Copy
it as ``products/tasks/backend/services/hogbox_sandbox.py``, tweak the
template→snapshot-alias map and the agent-server bootstrap command for
your conventions, and swap the backend in your factory.

Design choices worth flagging up front:

* **Single-credential auth.** Hogland uses one credential per caller
  on the wire as ``Authorization: Bearer <X>`` (see ``docs/AUTH_PLAN.md``
  in the hogland repo). The Django pod authenticates with a *projected*
  K8s ServiceAccount JWT (AUTH_PLAN Path 3) — hogplane verifies the
  JWT cross-account via the issuing cluster's EKS OIDC JWKS, then
  matches ``{iss, namespace, sa_name}`` against a TrustMapping to
  resolve a Principal. The projected volume must be mounted with
  hogland's audience (default ``hogland``) at a hogland-specific path;
  ``INTEGRATION_NOTES.md`` in the hogland SDK has the pod-spec snippet.
  No per-tunnel token is minted, and there's no Modal-style connect-token
  layer. ``get_connect_credentials()`` returns the same credential the
  SDK is already using; the caller hits ``proxy_url`` with it.

* **No 1:1 parity for cosmetic Modal mechanics.** We don't reproduce
  the two-layer auth, the wildcard-subdomain tunnels, or Modal's
  per-create image build with verbose=True. Where Modal's mechanic
  doesn't carry information the consumer relies on, we skip it.

* **What we do match exactly:** the ``SandboxBase`` method
  signatures, the typed exception hierarchy, the ``ExecutionStream``
  protocol shape (``iter_stdout()`` + ``wait() -> ExecutionResult``),
  the ``SandboxStatus`` enum, and the ``SandboxConfig`` defaults
  (4 CPU / 16 GB RAM / 64 GB disk).

* **Known SDK-side gaps** flagged inline with ``# TODO(hogland-NNN):``:

  * ``region`` pinning is not yet on hogland — single-region today.
    Document with PostHog ops if multi-region is needed.
  * ``set_tags`` post-create is not yet on hogland — tags are
    passed at create-time only. ``PatchSandboxRequest`` server-side
    will need a ``tags`` field.
"""

from __future__ import annotations

import logging
import os
import shlex
import time
from pathlib import Path
from typing import TYPE_CHECKING

# These imports resolve in the PostHog repo, not in hogland's. Module
# layout mirrors PostHog's live `products/tasks/backend/services/hogland_sandbox.py`:
# the SandboxBase shape + status enum sit in `services.sandbox`, the
# typed exceptions live in `temporal.exceptions`, and McpServerConfig
# is in `temporal.process_task.utils`.
from products.tasks.backend.services.sandbox import (  # type: ignore[import-not-found]
    AgentServerResult,
    ExecutionResult,
    ExecutionStream,
    SandboxBase,
    SandboxConfig,
    SandboxStatus,
    SandboxTemplate,
)
from products.tasks.backend.temporal.exceptions import (  # type: ignore[import-not-found]
    SandboxCleanupError,
    SandboxExecutionError,
    SandboxNotFoundError,
    SandboxTimeoutError,
    SnapshotCreationError,
)
from products.tasks.backend.temporal.process_task.utils import (  # type: ignore[import-not-found]
    McpServerConfig,
)

from hogland import (
    APIError,
    ExecEvent,
    Hogbox,
    Hogland,
    NotFoundError,
    ValidationError,
)
from hogland import (
    ServerError as HoglandServerError,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants the consumer is most likely to tweak
# ---------------------------------------------------------------------------

ENV_FILE_PATH = "/etc/hogbox-env"
"""Where we drop ``KEY=value`` lines for the agent server to source.

The base image's `start-agent-server.sh` is expected to `source
/etc/hogbox-env` before exec-ing the agent process. Adjust to whatever
contract your base image actually uses.
"""

AGENT_PORT = 8080
"""Port the agent-server listens on inside the box."""

AGENT_HEALTH_PATH = "/health"
"""HTTP path on the agent-server that returns 200 when ready."""

AGENT_HEALTH_TIMEOUT_S = 60
"""How long to wait for the agent-server to come up after start."""

# Template → snapshot-alias map. The aliases need to exist server-side;
# create them with `hogland snapshot alias create posthog-tasks-default
# <snap-id>` after baking the base image.
TEMPLATE_TO_SNAPSHOT_ALIAS: dict[SandboxTemplate, str] = {
    SandboxTemplate.DEFAULT_BASE: "alias:posthog-tasks-default",
    SandboxTemplate.NOTEBOOK_BASE: "alias:posthog-tasks-notebook",
    SandboxTemplate.PI_BASE: "alias:posthog-tasks-pi",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _render_env_file(env: dict[str, str]) -> str:
    """Render an env dict to ``KEY="value"`` lines for `source`-ing."""
    lines = [f"export {k}={shlex.quote(v)}" for k, v in sorted(env.items())]
    return "\n".join(lines) + "\n"


def _resolve_snapshot(config: SandboxConfig) -> str | None:
    """Pick the right snapshot id for ``create()``.

    Precedence: explicit ``snapshot_id`` (Django UUID resolved upstream)
    > Modal-style ``snapshot_external_id`` > template alias > base
    image (None — server picks the default).
    """
    if config.snapshot_id:
        return config.snapshot_id
    if config.snapshot_external_id:
        return config.snapshot_external_id
    return TEMPLATE_TO_SNAPSHOT_ALIAS.get(config.template)


def _translate_error(err: APIError, action: str, sandbox_id: str | None = None) -> Exception:
    """Map a hogland :class:`APIError` to the PostHog exception tree.

    PostHog's `temporal.exceptions` classes all take
    ``(message, context_dict, cause=...)``; constructing them with a
    bare string raises on the missing ``context`` arg. Sandbox id is
    optional (some call sites — e.g. ``create`` — don't have one yet).
    """
    context: dict[str, str] = {"action": action, "error": str(err)}
    if sandbox_id is not None:
        context["sandbox_id"] = sandbox_id
    if isinstance(err, NotFoundError):
        return SandboxNotFoundError(f"hogbox not found during {action}", context, cause=err)
    if isinstance(err, ValidationError):
        return SandboxExecutionError(f"hogbox rejected {action}", context, cause=err)
    if isinstance(err, HoglandServerError):
        return SandboxExecutionError(f"hogbox server error during {action}", context, cause=err)
    return SandboxExecutionError(f"hogbox call failed during {action}", context, cause=err)


# Where the pod spec is expected to mount a *projected* SA token volume
# with hogland's audience configured. The default cluster SA token at
# /var/run/secrets/kubernetes.io/serviceaccount/token is intentionally not
# used — its audience is the cluster API server, which fails hogplane's
# `aud` check. See INTEGRATION_NOTES.md in the hogland SDK for the pod-spec
# snippet and the audience/TrustMapping coordination steps.
HOGLAND_SA_TOKEN_PATH = Path("/var/run/secrets/hogland.posthog.dev/token")


def _hogland_client(region: str | None = None) -> Hogland:
    """Build a ``Hogland`` client wired with the right credential.

    Credential order: explicit ``HOG_TOKEN`` env → projected SA token
    (EKS OIDC, AUTH_PLAN Path 3) → raises.

    The SA token is read **per call**, not cached. K8s rewrites the
    projected file roughly every 50 minutes; reading at use-time picks
    up the fresh token without restart. The read is cheap (kernel page
    cache after the first call).

    ``region`` is reserved for the day hogland runs separate per-region
    deploys; route to a ``REGIONAL_HOSTS[region]`` map here when that
    lands. No-op today.
    """
    del region
    if os.environ.get("HOG_TOKEN"):
        return Hogland()
    try:
        token = HOGLAND_SA_TOKEN_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return Hogland()  # falls through to ConfigurationError
    return Hogland(token=token)


# ---------------------------------------------------------------------------
# ExecutionStream impl
# ---------------------------------------------------------------------------


class _HogboxExecutionStream(ExecutionStream):
    """Wraps hogland's SSE ``exec_stream`` to satisfy PostHog's protocol.

    PostHog's ``ExecutionStream`` exposes ``iter_stdout()`` (stdout-only
    iterator) plus ``wait() -> ExecutionResult`` (final result with
    stderr accumulated and exit code). Our wire format yields stdout,
    stderr, and exit events interleaved on a single SSE stream, so we
    buffer stderr as we go and surface it in ``wait()``.

    HTTP errors from the SSE connection (auth, 404, 5xx) only surface
    when the consumer starts iterating — ``box.exec_stream(...)`` just
    builds a generator. We translate ``APIError`` to PostHog's exception
    tree inside :meth:`_pull` so callers see ``SandboxExecutionError``,
    not raw ``APIError``.
    """

    _STDERR_CAP = 1 << 20  # 1 MiB — mirrors hogland's server-side stderr cap.

    def __init__(self, source: Iterable[ExecEvent], sandbox_id: str) -> None:
        self._source: Iterator[ExecEvent] = iter(source)
        self._sandbox_id = sandbox_id
        self._stderr_buf: list[str] = []
        self._stderr_bytes = 0
        self._exit_code: int | None = None
        self._duration_ms: int | None = None
        self._drained = False

    def _pull(self) -> Iterator[ExecEvent]:
        try:
            yield from self._source
        except APIError as err:
            raise _translate_error(err, "execute_stream", self._sandbox_id) from err

    def _record_stderr(self, chunk: str) -> None:
        remaining = self._STDERR_CAP - self._stderr_bytes
        if remaining <= 0:
            return
        if len(chunk) > remaining:
            chunk = chunk[:remaining]
        self._stderr_buf.append(chunk)
        self._stderr_bytes += len(chunk)

    def iter_stdout(self) -> Iterator[str]:
        """Yield stdout chunks as they arrive.

        On exhaustion, ``self._exit_code`` and ``self._duration_ms``
        are populated. Stderr chunks are buffered up to ``_STDERR_CAP``
        bytes; overflow is dropped (typical exec produces far less
        stderr than stdout, so this rarely matters).
        """
        for event in self._pull():
            if event.kind == "stdout":
                yield event.data
            elif event.kind == "stderr":
                self._record_stderr(event.data)
            elif event.kind == "exit":
                self._exit_code = event.exit_code
                self._duration_ms = event.duration_ms
                break
        self._drained = True

    def wait(self) -> ExecutionResult:
        """Drain any remaining frames and return the final result."""
        if not self._drained:
            for event in self._pull():
                if event.kind == "stderr":
                    self._record_stderr(event.data)
                elif event.kind == "exit":
                    self._exit_code = event.exit_code
                    self._duration_ms = event.duration_ms
                    break
            self._drained = True
        return ExecutionResult(
            stdout="",
            stderr="".join(self._stderr_buf),
            exit_code=self._exit_code if self._exit_code is not None else -1,
            error=None,
        )


# ---------------------------------------------------------------------------
# The adapter
# ---------------------------------------------------------------------------


class HogboxSandbox(SandboxBase):
    """``SandboxBase`` implementation backed by hogland's HTTP API.

    Inheritance is intentional — :class:`SandboxBase` ships a concrete
    ``clone_repository`` and the ``__enter__``/``__exit__`` context
    manager that we want to pick up for free.
    """

    def __init__(self, client: Hogland, box: Hogbox, config: SandboxConfig) -> None:
        self._client = client
        self._box = box
        self._sandbox_url: str | None = None
        self.id = box.id
        self.config = config

    # ---- factory methods -------------------------------------------------

    @staticmethod
    def create(config: SandboxConfig) -> HogboxSandbox:
        client = _hogland_client()
        snapshot_id = _resolve_snapshot(config)

        try:
            box = client.create(
                cpus=config.cpu_cores,
                memory_mib=int(config.memory_gb * 1024),
                disk_gib=config.disk_size_gb,
                snapshot_id=snapshot_id,
                env=config.environment_variables or None,
                ttl_seconds=config.ttl_seconds,
                name=config.name or None,
                tags=[f"{k}={v}" for k, v in (config.metadata or {}).items()] or None,
                kind="posthog-tasks",
            )
        except APIError as err:
            raise _translate_error(err, "create") from err

        return HogboxSandbox(client, box, config)

    @staticmethod
    def get_by_id(sandbox_id: str) -> HogboxSandbox:
        client = _hogland_client()
        try:
            box = client.get(sandbox_id)
        except NotFoundError as err:
            raise SandboxNotFoundError(
                f"hogbox {sandbox_id} not found",
                {"sandbox_id": sandbox_id, "error": str(err)},
                cause=err,
            ) from err
        except APIError as err:
            raise _translate_error(err, "get_by_id", sandbox_id) from err

        # Reconstruct a minimal SandboxConfig from the box view so
        # `self.config` is meaningful after re-attach. Fields we can't
        # recover (template, ttl) stay as their defaults.
        config = SandboxConfig(
            name=box.view.spec.name or "",
            cpu_cores=box.view.spec.cpus,
            memory_gb=box.view.spec.memory_mib / 1024,
            disk_size_gb=box.view.spec.disk_gib,
        )
        return HogboxSandbox(client, box, config)

    @staticmethod
    def delete_snapshot(external_id: str) -> None:
        # No-op — matches Modal's behaviour. Hogland's snapshots are
        # owned by the OwnerID Principal and reaped by their lifecycle,
        # not explicit deletes from the consumer side. If a future
        # version of hogland wants explicit delete, call
        # client.delete_snapshot(external_id) here.
        del external_id

    # ---- lifecycle -------------------------------------------------------

    @property
    def sandbox_url(self) -> str | None:
        """The agent-server URL, cached after ``get_connect_credentials``."""
        return self._sandbox_url

    def destroy(self) -> None:
        try:
            self._box.delete()
        except APIError as err:
            raise SandboxCleanupError(
                f"hogbox delete failed: {err}",
                {"sandbox_id": self.id, "error": str(err)},
                cause=err,
            ) from err
        finally:
            self._client.close()

    def get_status(self) -> SandboxStatus:
        try:
            self._box.refresh()
        except NotFoundError:
            return SandboxStatus.SHUTDOWN
        except APIError as err:
            raise _translate_error(err, "get_status", self.id) from err
        # Hogland statuses: "creating", "running", "paused", "failed",
        # "destroyed". Anything other than "running" maps to SHUTDOWN
        # for the SandboxBase contract.
        return SandboxStatus.RUNNING if self._box.status == "running" else SandboxStatus.SHUTDOWN

    def is_running(self) -> bool:
        return self.get_status() == SandboxStatus.RUNNING

    # ---- exec ------------------------------------------------------------

    def _require_running(self, action: str) -> None:
        if not self.is_running():
            raise SandboxExecutionError(
                "Sandbox not in running state.",
                {"sandbox_id": self.id, "action": action},
                cause=RuntimeError(f"hogbox {self.id} is not running"),
            )

    def execute(self, command: str, timeout_seconds: int | None = None) -> ExecutionResult:
        self._require_running("execute")
        timeout = timeout_seconds if timeout_seconds is not None else self.config.default_execution_timeout_seconds
        try:
            result = self._box.exec(["bash", "-c", command], timeout_seconds=timeout)
        except APIError as err:
            raise _translate_error(err, "execute", self.id) from err

        if result.timed_out:
            raise SandboxTimeoutError(
                f"hogbox exec timed out after {timeout}s",
                {"sandbox_id": self.id, "command": command, "timeout_seconds": str(timeout)},
                cause=TimeoutError(f"exec timed out after {timeout}s"),
            )
        return ExecutionResult(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
            error=None,
        )

    def execute_stream(
        self,
        command: str,
        timeout_seconds: int | None = None,
    ) -> ExecutionStream:
        self._require_running("execute_stream")
        timeout = (
            timeout_seconds
            if timeout_seconds is not None
            else self.config.default_execution_timeout_seconds
        )
        # `box.exec_stream` is a generator — building it doesn't fire the
        # HTTP request, so there's nothing to catch here. The stream
        # wrapper translates APIError to the PostHog exception tree
        # when the consumer actually iterates.
        source = self._box.exec_stream(["bash", "-c", command], timeout_seconds=timeout)
        return _HogboxExecutionStream(source, self.id)

    # ---- files -----------------------------------------------------------

    def write_file(self, path: str, payload: bytes) -> ExecutionResult:
        self._require_running("write_file")
        try:
            self._box.write_file(path, payload, mkdir=True)
        except APIError as err:
            raise _translate_error(err, f"write_file({path})", self.id) from err
        return ExecutionResult(stdout="", stderr="", exit_code=0, error=None)

    # ---- repo / task helpers --------------------------------------------

    def setup_repository(self, repository: str) -> ExecutionResult:
        # No-op like Modal's current impl; the heavy lifting lives in
        # the inherited concrete ``clone_repository`` on SandboxBase.
        del repository
        return ExecutionResult(stdout="", stderr="", exit_code=0, error=None)

    def is_git_clean(self, repository: str) -> tuple[bool, str]:
        self._require_running("is_git_clean")
        result = self.execute(
            f"cd {shlex.quote(repository)} && git status --porcelain",
        )
        is_clean = result.exit_code == 0 and not result.stdout.strip()
        return is_clean, result.stdout

    def execute_task(
        self,
        task_id: str,  # noqa: ARG002 — matches base signature; agent-server owns this now
        run_id: str,  # noqa: ARG002
        repository: str | None = None,  # noqa: ARG002
        create_pr: bool = True,  # noqa: ARG002
    ) -> ExecutionResult:
        # No-op like Modal's current impl — the agent-server pattern
        # replaced this code path.
        return ExecutionResult(stdout="", stderr="", exit_code=0, error=None)

    # ---- agent-server credentials & boot --------------------------------

    def get_connect_credentials(self) -> AgentServerResult:
        """Return the URL + bearer the consumer hits the agent-server with.

        The URL is hogplane's authenticated proxy into the box at
        ``AGENT_PORT``. The token is the same bearer the SDK used to
        talk to hogplane — there is no per-tunnel token (see
        ``docs/AUTH_PLAN.md``).
        """
        url = self._box.proxy_url(AGENT_PORT)
        self._sandbox_url = url
        return AgentServerResult(url=url, token=self._client.token)

    def start_agent_server(
        self,
        repository: str,
        task_id: str,
        run_id: str,
        mode: str = "background",
        create_pr: bool = True,
        interaction_origin: str | None = None,
        branch: str | None = None,
        runtime_adapter: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        reasoning_effort: str | None = None,
        mcp_configs: list[McpServerConfig] | None = None,
        allowed_domains: list[str] | None = None,
        event_ingest_token: str | None = None,
    ) -> None:
        """Boot the agent-server inside the box and wait for it to be healthy."""
        self._require_running("start_agent_server")

        if allowed_domains is not None:
            self._setup_agentsh(allowed_domains)

        if mcp_configs:
            for cfg in mcp_configs:
                self._write_mcp_config(cfg)

        # Build the agent-server command. The exact invocation is
        # base-image-specific — tweak to match your image's entrypoint.
        argv = [
            "agent-server",
            "--repository",
            repository,
            "--task-id",
            task_id,
            "--run-id",
            run_id,
            "--port",
            str(AGENT_PORT),
            "--mode",
            mode,
        ]
        if create_pr:
            argv.append("--create-pr")
        if branch:
            argv.extend(["--branch", branch])
        if runtime_adapter:
            argv.extend(["--runtime-adapter", runtime_adapter])
        if provider:
            argv.extend(["--provider", provider])
        if model:
            argv.extend(["--model", model])
        if reasoning_effort:
            argv.extend(["--reasoning-effort", reasoning_effort])
        if interaction_origin:
            argv.extend(["--interaction-origin", interaction_origin])

        # event_ingest_token is per-run (issued by PostHog backend) and
        # flows to the agent-server via env, never via CLI flag — keeps
        # the secret off `ps`. Materialised as a `source`-able export
        # line right before launch.
        env_inline = ""
        if event_ingest_token:
            env_inline = f"export POSTHOG_EVENT_INGEST_TOKEN={shlex.quote(event_ingest_token)}\n"

        # We launch the agent detached so this method can return; the
        # in-box logs go to journald (or wherever the base image points).
        cmd = " ".join(shlex.quote(a) for a in argv)
        launch_script = (
            f"set -euo pipefail\n"
            f"source {shlex.quote(ENV_FILE_PATH)} 2>/dev/null || true\n"
            f"{env_inline}"
            f"nohup {cmd} >/var/log/agent-server.log 2>&1 &\n"
            f"echo $! > /run/agent-server.pid\n"
        )
        result = self._box.exec(["bash", "-c", launch_script], timeout_seconds=30)
        if result.exit_code != 0:
            raise SandboxExecutionError(
                "agent-server failed to launch",
                {
                    "sandbox_id": self.id,
                    "exit_code": str(result.exit_code),
                    "stderr": result.stderr,
                },
                cause=RuntimeError(f"agent-server exited {result.exit_code}"),
            )

        self._wait_for_agent_health()

    def _wait_for_agent_health(self) -> None:
        """Poll the in-box agent-server until it returns 200 on health.

        Backs off 0.25 → 0.5 → 1 → 2 → 4 s between probes; typical
        healthy paths see 1-2 probes, pathological paths ~10 instead of
        ``AGENT_HEALTH_TIMEOUT_S`` fixed-1s polls.
        """
        deadline = time.monotonic() + AGENT_HEALTH_TIMEOUT_S
        delay = 0.25
        last_err = ""
        while time.monotonic() < deadline:
            probe = self._box.exec(
                [
                    "curl",
                    "-fsS",
                    "-m",
                    "2",
                    f"http://127.0.0.1:{AGENT_PORT}{AGENT_HEALTH_PATH}",
                ],
                timeout_seconds=5,
            )
            if probe.exit_code == 0:
                return
            last_err = probe.stderr or probe.stdout
            time.sleep(delay)
            delay = min(delay * 2, 4.0)
        raise SandboxExecutionError(
            f"agent-server health check failed after {AGENT_HEALTH_TIMEOUT_S}s",
            {"sandbox_id": self.id, "last_stderr": last_err},
            cause=TimeoutError("agent-server health check exhausted retries"),
        )

    def _setup_agentsh(self, allowed_domains: list[str]) -> None:
        """Write ``agentsh`` policy files. Requires the base image to ship ``agentsh``.

        The exact files / paths / daemon-reload commands depend on your
        base image. This is a placeholder showing the shape — fill in
        the real paths once the image is settled. The Modal backend's
        equivalent is in ``modal_sandbox.py`` `_setup_agentsh`.
        """
        # TODO: replace with real `agentsh` config layout.
        policy = "\n".join(allowed_domains) + "\n"
        self._box.write_file("/etc/agentsh/allowed-domains", policy.encode(), mkdir=True)
        restart = self._box.exec(
            ["systemctl", "restart", "agentsh"],
            timeout_seconds=10,
        )
        if restart.exit_code != 0:
            raise SandboxExecutionError(
                "failed to restart agentsh after policy update",
                {"sandbox_id": self.id, "stderr": restart.stderr},
                cause=RuntimeError(f"systemctl restart agentsh exited {restart.exit_code}"),
            )

    def _write_mcp_config(self, cfg: McpServerConfig) -> None:
        """Drop an MCP server config inside the box."""
        # The actual schema depends on PostHog's McpServerConfig shape;
        # adjust this serialisation to match your real type.
        import json as _json

        # The McpServerConfig type may be a dataclass or pydantic model.
        # Handle both shapes defensively.
        if hasattr(cfg, "model_dump"):
            payload = _json.dumps(cfg.model_dump()).encode()
        elif hasattr(cfg, "__dict__"):
            payload = _json.dumps(cfg.__dict__).encode()
        else:
            payload = _json.dumps(dict(cfg)).encode()  # type: ignore[arg-type]
        name = getattr(cfg, "name", "mcp")
        path = f"/etc/mcp/{name}.json"
        self._box.write_file(path, payload, mkdir=True)

    # ---- snapshots -------------------------------------------------------

    def create_snapshot(self) -> str:
        """Pause→sync→resume the box and return the snapshot id.

        Hogland's snapshots include paused VM memory + the rootfs, so a
        restore boots the *same* process tree, not a fresh container —
        intentional. Document this when users compare to Modal.
        """
        self._require_running("create_snapshot")

        # The Modal impl uses `sb.exec("true").wait()` as a sync point
        # before snapshot because Modal reports a sandbox running before
        # the FS snapshot is ready. Hogland's pause-before-snapshot
        # makes that workaround unnecessary, but we keep the sync
        # exec for parity — it's cheap and surfaces "dead process tree"
        # before we burn a snapshot on it.
        sync = self._box.exec(["true"], timeout_seconds=5)
        if sync.exit_code != 0:
            raise SnapshotCreationError(
                "pre-snapshot sync exec failed",
                {
                    "sandbox_id": self.id,
                    "exit_code": str(sync.exit_code),
                    "stderr": sync.stderr,
                },
                cause=RuntimeError(f"sync exec exited {sync.exit_code}"),
            )

        try:
            record = self._box.snapshot()
        except APIError as err:
            raise SnapshotCreationError(
                "hogbox snapshot failed",
                {"sandbox_id": self.id, "error": str(err)},
                cause=err,
            ) from err
        return record.id

    # ---- env-var refresh (for snapshot resume) --------------------------

    def update_environment_variables(self, env: dict[str, str]) -> None:
        """Overwrite the in-box env file used by the agent-server.

        Called by ``inject_fresh_tokens_on_resume``-style flows after a
        snapshot restore — fresh ``GITHUB_TOKEN`` / ``POSTHOG_*`` values
        replace the stale ones baked into the snapshot. The agent-server
        is expected to re-source the file (the base image's launch
        script sources it on startup; if the agent is already running
        you'll need to restart it via :meth:`start_agent_server`).
        """
        self._require_running("update_environment_variables")
        try:
            self._box.write_file(
                ENV_FILE_PATH,
                _render_env_file(env).encode(),
                mode="0600",
                mkdir=False,
            )
        except APIError as err:
            raise _translate_error(err, "update_environment_variables", self.id) from err


# ---------------------------------------------------------------------------
# Open follow-ups (not blocking adoption)
# ---------------------------------------------------------------------------
#
# 1. `set_tags` post-create: `PatchSandboxRequest` only accepts `name`
#    today. Tags are passed at create-time only. If PostHog needs to
#    update tags mid-run (e.g. on state changes), file a feature
#    request on hogland.
#
# 2. `region`: not modelled. If EU vs US data-residency matters, raise
#    with hogland ops — could be a `BoxSpec.region` field or a
#    cluster-per-region deployment.
#
# 3. `agentsh` allowed_domains: this adapter writes one config file
#    and restarts a daemon. The real policy schema depends on the
#    PostHog base image — confirm the path + restart command match.
#
# 4. Provision diagnostics: hogland boots from snapshots rather than
#    building images per-create, so the "first 80 lines of build
#    output" surface doesn't exist. The user-facing "image build may
#    take a few minutes" UX should be replaced with "restoring
#    snapshot" copy.
