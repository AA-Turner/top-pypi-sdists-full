"""Runtime client with server lifecycle management.

Extends :class:`RuntimeClient` with the ability to start, stop, and
restart the runtime server — either in-process via ASGI or as a
managed subprocess. Also provides transport introspection methods
used by the TUI connection manager.
"""

import asyncio
import contextlib
import os
import secrets
import shlex
import socket
import subprocess
import tempfile
import time
import typing as t
from pathlib import Path

import httpx
import uvicorn
from loguru import logger

from dreadnode.app.client import models
from dreadnode.app.client.runtime_client import (
    DEFAULT_RUNTIME_HOST,
    DEFAULT_RUNTIME_PORT,
    DEFAULT_RUNTIME_URL,
    RuntimeClient,
)
from dreadnode.app.client.transports import StreamingASGITransport
from dreadnode.app.env import read_env_with_deprecation

DEFAULT_START_TIMEOUT_S = 20.0
_INPROC_BIND_RETRIES = 3

if t.TYPE_CHECKING:
    import concurrent.futures

    from dreadnode.app.config import Profile


class ManagedRuntimeClient(RuntimeClient):
    """Runtime client that can start and manage the server process.

    Use this when the client is responsible for ensuring the server
    is running — the TUI, ``dn --print``, and similar launchers.
    Workers and standalone scripts that connect to an already-running
    server should use :class:`RuntimeClient` directly.
    """

    def __init__(
        self,
        server_url: str | None = None,
        auto_start: bool = True,
        transport: httpx.AsyncBaseTransport | None = None,
        capability_dirs: list[str] | None = None,
        enabled_capabilities: list[str] | None = None,
        capability_flag_overrides: list[str] | None = None,
        system_prompt_append: str | None = None,
        auth_token: str | None = None,
    ) -> None:
        super().__init__(
            server_url=server_url or DEFAULT_RUNTIME_URL,
            auth_token=auth_token,
            transport=transport,
        )
        self.auto_start = auto_start
        self._in_process = auto_start and transport is None and server_url is None
        self._owned_process: subprocess.Popen[t.Any] | None = None
        self._owned_log_file: t.Any = None
        self._platform_server: str | None = None
        self._platform_api_key: str | None = None
        self._platform_organization: str | None = None
        self._platform_workspace: str | None = None
        self._platform_project: str | None = None
        # CLI overrides threaded to initialize_app()
        self._capability_dirs = capability_dirs
        self._enabled_capabilities = enabled_capabilities
        self._capability_flag_overrides = capability_flag_overrides
        self._system_prompt_append = system_prompt_append
        self._lifecycle_ctx: t.Any = None
        # In-process loopback HTTP listener — bound only when self._in_process
        # so subprocess workers (and any other capability subprocess that uses
        # RuntimeClient) have a real URL to connect to. The ASGITransport keeps
        # the fast path for in-proc callers; uvicorn here is purely for
        # out-of-process consumers.
        self._uvicorn_server: uvicorn.Server | None = None
        self._uvicorn_serve_future: concurrent.futures.Future[None] | None = None
        self._inproc_bind_host: str | None = None
        self._inproc_bind_port: int | None = None
        self._inproc_minted_token: bool = False
        # Track exactly which env keys we set so close()/restart() can clear
        # only what we own (and not stomp explicit operator values).
        self._inproc_env_keys: set[str] = set()
        # Serialize concurrent start() callers so the slow in-process boot
        # (capability scan + MCP start + litellm warmup) runs once. The
        # event lets passive consumers (e.g. the TUI notify subscriber)
        # wait for the runtime to come up instead of racing start() and
        # kicking off a second boot with empty credentials.
        self._start_lock = asyncio.Lock()
        self._started_event = asyncio.Event()

    # ── Platform profile ──────────────────────────────────────────

    def set_platform_profile(self, profile: "Profile") -> None:
        """Store the active platform profile for local server startup."""
        self._platform_server = profile.url
        self._platform_api_key = profile.api_key
        self._platform_organization = profile.default_organization
        self._platform_workspace = profile.default_workspace
        self._platform_project = profile.default_project

    def clear_platform_profile(self) -> None:
        """Clear any stored platform profile for local-only runtime startup."""
        self._platform_server = None
        self._platform_api_key = None
        self._platform_organization = None
        self._platform_workspace = None
        self._platform_project = None

    # ── Session creation (with platform project default) ──────────

    async def create_session(
        self,
        *,
        capability: str | None = None,
        agent: str | None = None,
        model: str | None = None,
        session_id: str | None = None,
        group_id: str | None = None,
        project: str | None = None,
        generate_params_extra: dict[str, t.Any] | None = None,
        policy: str | dict[str, t.Any] | None = None,
        labels: dict[str, list[str]] | None = None,
        origin: str | None = None,
        project_memory_scope_kind: str | None = None,
        enable_project_memory_preload: bool | None = None,
        project_memory_preload_limit: int | None = None,
    ) -> models.SessionInfo:
        """Create a session, defaulting project from the platform profile."""
        resolved_project = project or self._platform_project
        return await super().create_session(
            capability=capability,
            agent=agent,
            model=model,
            session_id=session_id,
            group_id=group_id,
            project=resolved_project,
            generate_params_extra=generate_params_extra,
            policy=policy,
            labels=labels,
            origin=origin,
            project_memory_scope_kind=project_memory_scope_kind,
            enable_project_memory_preload=enable_project_memory_preload,
            project_memory_preload_limit=project_memory_preload_limit,
        )

    # ── Server lifecycle ──────────────────────────────────────────

    async def start(self) -> None:
        """Ensure the target server is reachable, auto-starting if needed."""
        if self._started:
            return

        async with self._start_lock:
            if self._started:
                return

            if self._in_process:
                logger.info("Server start | mode=in-process | url={}", self.server_url)
                await self._start_in_process()
                self._mark_started()
                return

            if not self.auto_start:
                try:
                    await self._await_ready()
                except RuntimeError as exc:
                    raise RuntimeError(
                        f"{exc}\n\nThe --server flag overrides the local runtime endpoint, "
                        "not the platform API. Omit --server to auto-start the local runtime, "
                        "and use /login --server <url> to set the platform API."
                    ) from exc
                logger.info("Server start | mode=external | url={}", self.server_url)
                self._mark_started()
                return

            if await self._is_healthy():
                await self._await_ready()
                logger.info("Server start | mode=external | url={}", self.server_url)
                self._mark_started()
                return

            logger.info("Server start | mode=spawned | url={}", self.server_url)
            self._spawn_local_server()
            await self._wait_until_healthy()
            self._mark_started()

    async def wait_until_started(self) -> None:
        """Block until ``start()`` has successfully brought the server up."""
        await self._started_event.wait()

    def _mark_started(self) -> None:
        self._started = True
        self._started_event.set()

    def _mark_stopped(self) -> None:
        self._started = False
        self._started_event.clear()

    async def close(self) -> None:
        """Close resources and shut down any managed server."""
        logger.info("Closing runtime client")

        # Exit in-process lifecycle before closing the transport
        # (the httpx client owns the ASGI transport whose loop hosts it).
        if self._in_process and self._lifecycle_ctx is not None:
            transport = self._http_client._transport
            if (
                isinstance(transport, StreamingASGITransport)
                and transport.server_loop is not None
                and transport.server_loop.is_running()
            ):
                server_loop = transport.require_server_loop()
                future = asyncio.run_coroutine_threadsafe(
                    self._lifecycle_ctx.__aexit__(None, None, None),
                    server_loop,
                )
                await asyncio.to_thread(future.result)
            else:
                await self._lifecycle_ctx.__aexit__(None, None, None)
            self._lifecycle_ctx = None

        # Stop uvicorn AFTER lifecycle exit so workers (which stop inside
        # server_lifecycle.__aexit__) finish their final HTTP traffic before
        # the listener goes away.
        if self._in_process:
            await self._stop_uvicorn()

        await super().close()

        if self._in_process:
            from dreadnode.app.server.app import reset_app_state

            reset_app_state()
            self._clear_inproc_env()
            logger.debug("In-process server state reset")
            return

        if self._owned_process is not None and self._owned_process.poll() is None:
            logger.info("Terminating spawned server | pid={}", self._owned_process.pid)
            self._owned_process.terminate()
            with contextlib.suppress(subprocess.TimeoutExpired):
                self._owned_process.wait(timeout=5)
            if self._owned_process.poll() is None:
                logger.warning(
                    "Server did not terminate gracefully, killing | pid={}", self._owned_process.pid
                )
                self._owned_process.kill()
                with contextlib.suppress(subprocess.TimeoutExpired):
                    self._owned_process.wait(timeout=2)

        if self._owned_log_file is not None:
            log_name = self._owned_log_file.name
            self._owned_log_file.close()
            with contextlib.suppress(OSError):
                Path(log_name).unlink()

    async def restart(self) -> None:
        """Restart the server so it picks up fresh platform context."""
        logger.info("Restarting runtime server | in_process={}", self._in_process)
        interactive = self._interactive_transport
        self._interactive_transport = None
        if interactive is not None:
            await interactive.close()
        if self._in_process:
            # Stop uvicorn BEFORE reset_app_state swaps app.state.server out
            # from under any in-flight requests.
            await self._stop_uvicorn()
            await self._http_client.aclose()

            from dreadnode.app.server.app import reset_app_state

            reset_app_state()

            self._mark_stopped()
            # _start_in_process() will reuse self._inproc_bind_port so any
            # subprocess workers that re-spawn get the same loopback URL.
            await self._start_in_process()
            self._mark_started()
            return

        await self.close()
        self._owned_process = None
        self._owned_log_file = None
        self._mark_stopped()
        self._http_client = self._create_http_client()
        await self.start()

    # ── Transport introspection (TUI connection manager) ──────────

    async def probe_interactive_transport(self) -> bool:
        """Check remote liveness through the persistent interactive websocket."""
        transport = self._interactive_transport
        if transport is None:
            return False
        await transport.ping()
        return True

    def latest_session_snapshot(self, session_id: str) -> dict[str, t.Any] | None:
        """Return the last interactive session snapshot seen for a session."""
        transport = self._interactive_transport
        if transport is None:
            return None
        return transport.latest_session_snapshot(session_id)

    def latest_session_resync_required(self, session_id: str) -> dict[str, t.Any] | None:
        """Return the last replay-miss payload seen for a session."""
        transport = self._interactive_transport
        if transport is None:
            return None
        return transport.latest_resync_required(session_id)

    def desired_session_subscriptions(self) -> set[str]:
        """Return the sessions the client intends to keep subscribed."""
        transport = self._interactive_transport
        if transport is None:
            return set()
        return transport.desired_session_ids()

    def subscribed_session_subscriptions(self) -> set[str]:
        """Return the sessions currently subscribed on the websocket."""
        transport = self._interactive_transport
        if transport is None:
            return set()
        return transport.subscribed_session_ids()

    # ── Private server management ─────────────────────────────────

    async def _start_in_process(self) -> None:
        """Initialize the FastAPI app in-process, bind a loopback HTTP server
        for out-of-process workers, and connect in-proc callers via ASGI."""
        logger.info("Starting in-process runtime server")
        from dreadnode.app.server.app import app as server_app
        from dreadnode.app.server.app import get_state, initialize_app, server_lifecycle

        # Pre-bind the loopback socket BEFORE initialize_app/lifespan so the
        # auth middleware sees the token (it reads env at request time) and
        # WorkerLifecycleManager (started inside server_lifecycle) sees the
        # authoritative URL/token on ServerState.
        host, port, sock, token, minted = self._resolve_inproc_bind()
        self._inproc_bind_host = host
        self._inproc_bind_port = port
        self._inproc_minted_token = minted
        self._set_inproc_env(host, port, token if minted else None)
        self.server_url = f"http://{host}:{port}"
        # Update the auth header so in-proc httpx requests carry the token
        # whenever we ourselves required it (auth middleware enforces).
        if token is not None and self._auth_token is None:
            self._auth_token = token

        await asyncio.to_thread(
            initialize_app,
            server=self._platform_server,
            api_key=self._platform_api_key,
            organization=self._platform_organization,
            workspace=self._platform_workspace,
            project=self._platform_project,
            capability_dirs=self._capability_dirs,
            enabled_capabilities=self._enabled_capabilities,
            capability_flag_overrides=self._capability_flag_overrides,
            system_prompt_append=self._system_prompt_append,
        )

        # Stash the runtime contract on ServerState so WorkerLifecycleManager
        # ._runtime_contract_env hands subprocess workers the URL we actually
        # bound — not the stale env default.
        state = get_state()
        state.runtime_url = self.server_url
        state.runtime_token = token
        state.runtime_id = os.environ.get("DREADNODE_RUNTIME_ID")

        # Create the transport — it owns a dedicated server event loop. Both
        # the manual server_lifecycle context AND our embedded uvicorn run on
        # this loop so they share the same MCP/worker state.
        transport = StreamingASGITransport(app=server_app)
        server_loop = transport.require_server_loop()

        # Start uvicorn on the transport's server loop using the pre-bound
        # socket. lifespan="off" because we drive server_lifecycle ourselves
        # below; install_signal_handlers is no-op on non-main threads
        # (uvicorn 0.42 short-circuits in capture_signals), so Ctrl+C in the
        # TUI's main loop is preserved.
        self._uvicorn_server = self._build_uvicorn_server(server_app, host, port)
        self._uvicorn_serve_future = asyncio.run_coroutine_threadsafe(
            self._uvicorn_server.serve(sockets=[sock]),
            server_loop,
        )
        await self._wait_until_uvicorn_started()

        # In-process mode skips FastAPI lifespan events, so we enter the
        # shared server_lifecycle context manually on the transport's server
        # loop. This ensures MCP client tasks, the reload endpoint, workers,
        # and shutdown all share the same event loop — avoiding cross-loop
        # errors. Workers boot here and now have a live loopback URL+token.
        self._lifecycle_ctx = server_lifecycle()
        future = asyncio.run_coroutine_threadsafe(self._lifecycle_ctx.__aenter__(), server_loop)
        await asyncio.to_thread(future.result)

        # `initialize_app` above already configured scope and populated the
        # registry, so this runtime really is ready. Deferred startup — which
        # normally owns this state — never runs here because in-process mode
        # sets `lifespan="off"` and drives `server_lifecycle` itself, so say so
        # explicitly or `/api/health` would report `configuring` forever.
        state.startup.mark_ready()

        self._http_client = self._create_http_client(transport=transport)

    @staticmethod
    def _build_uvicorn_server(app: t.Any, host: str, port: int) -> uvicorn.Server:
        config = uvicorn.Config(
            app,
            host=host,
            port=port,
            log_config=None,
            lifespan="off",
            loop="none",
            access_log=False,
        )
        return uvicorn.Server(config)

    async def _wait_until_uvicorn_started(self) -> None:
        """Poll uvicorn.Server.started until ready (or the serve task fails)."""
        if self._uvicorn_server is None or self._uvicorn_serve_future is None:
            return
        try:
            async with asyncio.timeout(5.0):
                while not self._uvicorn_server.started:
                    if self._uvicorn_serve_future.done():
                        # serve() exited before reporting started — surface its error.
                        self._uvicorn_serve_future.result()
                        raise RuntimeError("uvicorn serve() exited before starting")
                    await asyncio.sleep(0.02)
        except TimeoutError as exc:
            raise RuntimeError(
                f"uvicorn did not start within 5s on http://"
                f"{self._inproc_bind_host}:{self._inproc_bind_port}"
            ) from exc

    def _resolve_inproc_bind(
        self,
    ) -> tuple[str, int, socket.socket, str | None, bool]:
        """Resolve (host, port, bound_socket, token, token_was_minted).

        Precedence:
          - host: ``DREADNODE_RUNTIME_HOST`` env > ``127.0.0.1``. Auto-bind is
            loopback-only by design — operators who need LAN exposure should
            run ``dn serve`` externally.
          - port: ``DREADNODE_RUNTIME_PORT`` env > ephemeral (kernel-assigned).
          - port (restart): the previously-bound port is preferred so
            re-spawned subprocess workers get the same URL.
          - token: ``DREADNODE_RUNTIME_TOKEN`` env > auto-mint (32 bytes
            url-safe).
        """
        explicit_host = read_env_with_deprecation(
            "DREADNODE_RUNTIME_HOST", "DREADNODE_SERVER_HOST", ""
        )
        host = explicit_host or "127.0.0.1"

        port_str = read_env_with_deprecation("DREADNODE_RUNTIME_PORT", "DREADNODE_SERVER_PORT", "")
        if port_str and port_str != "0":
            requested_port = int(port_str)
        elif self._inproc_bind_port is not None:
            requested_port = self._inproc_bind_port
        else:
            requested_port = 0

        sock = self._bind_loopback_socket(host, requested_port)

        explicit_token = read_env_with_deprecation("DREADNODE_RUNTIME_TOKEN", "SANDBOX_AUTH_TOKEN")
        if explicit_token:
            return host, sock.getsockname()[1], sock, explicit_token, False

        minted = secrets.token_urlsafe(32)
        logger.debug("Auto-minted in-process runtime token (loopback bind)")
        return host, sock.getsockname()[1], sock, minted, True

    @staticmethod
    def _bind_loopback_socket(host: str, port: int) -> socket.socket:
        """Bind a TCP socket for uvicorn to take ownership of.

        Returns an unlistened socket — ``loop.create_server(sock=sock)``
        inside uvicorn calls ``listen()`` itself. For ephemeral binds we
        retry on the rare collision; for explicit ports we surface the
        bind error immediately.
        """
        last_exc: OSError | None = None
        attempts = _INPROC_BIND_RETRIES if port == 0 else 1
        for _ in range(attempts):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind((host, port))
            except OSError as exc:
                sock.close()
                last_exc = exc
            else:
                return sock
        assert last_exc is not None
        raise last_exc

    def _set_inproc_env(self, host: str, port: int, minted_token: str | None) -> None:
        """Set DREADNODE_RUNTIME_* env vars and remember which we own.

        Writing HOST/PORT/URL keeps the env consistent with the bound socket
        for any in-process consumer that constructs ``RuntimeClient()`` with
        no args. The TOKEN write is what activates ``SandboxAuthMiddleware``
        (it reads env at request time).
        """
        url = f"http://{host}:{port}"
        for key, value in (
            ("DREADNODE_RUNTIME_HOST", host),
            ("DREADNODE_RUNTIME_PORT", str(port)),
            ("DREADNODE_RUNTIME_URL", url),
        ):
            if os.environ.get(key) != value:
                os.environ[key] = value
                self._inproc_env_keys.add(key)
        if minted_token is not None:
            os.environ["DREADNODE_RUNTIME_TOKEN"] = minted_token
            self._inproc_env_keys.add("DREADNODE_RUNTIME_TOKEN")

    def _clear_inproc_env(self) -> None:
        for key in self._inproc_env_keys:
            os.environ.pop(key, None)
        self._inproc_env_keys.clear()

    async def _stop_uvicorn(self) -> None:
        """Stop the embedded uvicorn server and wait for serve() to return."""
        server = self._uvicorn_server
        future = self._uvicorn_serve_future
        if server is None or future is None:
            return
        server.should_exit = True
        with contextlib.suppress(Exception):
            await asyncio.to_thread(future.result, 5)
        self._uvicorn_server = None
        self._uvicorn_serve_future = None

    def _spawn_local_server(self) -> None:
        """Spawn the agent server as a subprocess."""
        command = [
            "uv",
            "run",
            "dreadnode",
            "serve",
            "--host",
            DEFAULT_RUNTIME_HOST,
            "--port",
            str(DEFAULT_RUNTIME_PORT),
        ]
        if self._platform_server:
            command.extend(["--platform-server", shlex.quote(self._platform_server)])
        if self._platform_api_key:
            command.extend(["--api-key", shlex.quote(self._platform_api_key)])
        if self._platform_organization:
            command.extend(["--organization", shlex.quote(self._platform_organization)])
        if self._platform_workspace:
            command.extend(["--workspace", shlex.quote(self._platform_workspace)])
        if self._platform_project:
            command.extend(["--project", shlex.quote(self._platform_project)])

        self._owned_log_file = tempfile.NamedTemporaryFile(  # noqa: SIM115 - manually owned across subprocess lifecycle
            mode="w+",
            encoding="utf-8",
            prefix="dreadnode-tui-server-",
            suffix=".log",
            delete=False,
        )
        self._owned_process = subprocess.Popen(  # noqa: S603 - command is assembled from fixed local runtime arguments
            command,
            stdout=self._owned_log_file,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
        )
        logger.info(
            "Spawned local server | pid={} | cmd={} | log={}",
            self._owned_process.pid,
            " ".join(command),
            self._owned_log_file.name,
        )

    async def _wait_until_healthy(self, timeout_s: float = DEFAULT_START_TIMEOUT_S) -> None:
        deadline = time.monotonic() + timeout_s
        attempts = 0
        start_time = time.monotonic()
        while time.monotonic() < deadline:
            attempts += 1
            if self._owned_process is not None and self._owned_process.poll() is not None:
                logger.error(
                    "Spawned server exited early | exit_code={} | attempts={}",
                    self._owned_process.returncode,
                    attempts,
                )
                log_tail = self._read_log_tail()
                details = f"\n\n{log_tail}" if log_tail else ""
                raise RuntimeError(
                    f"Local Dreadnode server exited with status {self._owned_process.returncode}.{details}"
                )
            if await self._is_healthy():
                remaining = max(deadline - time.monotonic(), 0.0)
                await self._await_ready(budget=remaining)
                elapsed = time.monotonic() - start_time
                logger.info("Server ready | attempts={} | elapsed={:.1f}s", attempts, elapsed)
                return
            await asyncio.sleep(0.1)

        elapsed = time.monotonic() - start_time
        logger.error(
            "Server health timeout | url={} | attempts={} | elapsed={:.1f}s",
            self.server_url,
            attempts,
            elapsed,
        )
        log_tail = self._read_log_tail()
        details = f"\n\n{log_tail}" if log_tail else ""
        raise RuntimeError(
            f"Timed out waiting for local Dreadnode server at {self.server_url}.{details}"
        )

    def _read_log_tail(self, max_chars: int = 4000) -> str:
        if self._owned_log_file is None:
            return ""
        with contextlib.suppress(OSError):
            return Path(self._owned_log_file.name).read_text(encoding="utf-8")[-max_chars:].strip()
        return ""
