"""Authenticated HTTP transport for the persistent browser worker."""

from __future__ import annotations

from matrx_utils.http_client import shared_client
from matrx_utils.task_pumps import run_pumps_then_cleanup
import asyncio
import contextlib
import logging
import os
import signal
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Query, Request, WebSocket
from fastapi.responses import StreamingResponse

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.cloud_computer_launch import CloudComputerLaunch
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

from typing import Any, Protocol


class StreamSupervisor(Protocol):
    def configure_rtc(self, rtc_config: M.RtcConfig) -> None: ...
    def clear_rtc(self) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...


def _bearer(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, separator, value = authorization.partition(" ")
    if separator and scheme.lower() == "bearer" and value:
        return value
    return None


_logger = logging.getLogger(__name__)


def _end_idle_stream(stream: StreamSupervisor) -> None:
    """Nobody drives or watches: end the picture. A kept-warm Cloud Computer
    stream (``keep_warm``) stays up, so no control change ever drops it."""
    if getattr(stream, "keep_warm", False):
        return
    stream.stop()
    stream.clear_rtc()


def _termination_lifespan(worker: BrowserWorker, stream: StreamSupervisor | None):  # noqa: ANN202
    """Own SIGTERM: close Chromium cleanly BEFORE the server shuts down.

    ECS stops a task with SIGTERM and gives it ``stopTimeout`` (120 s). Uvicorn's
    own handler would begin refusing connections at once and exit within
    seconds, with Chromium killed mid-write. Ours runs first: the worker stops
    taking commands, Chromium closes so the profile on the shared volume is
    consistent (the next worker adopts it), the video stream stops, and only
    then does the signal reach uvicorn's handler. SIGINT is left to uvicorn.
    """

    @contextlib.asynccontextmanager
    async def lifespan(_app: FastAPI):  # noqa: ANN202
        loop = asyncio.get_running_loop()
        previous = signal.getsignal(signal.SIGTERM)
        termination_task: asyncio.Task[None] | None = None

        async def final_flush() -> None:
            # The Cloud folder's last uploads run beside Chrome's clean close: both
            # fit the 120 s stop timeout, and neither waits for the other.
            for flush in getattr(_app.state, "background_flushers", []):
                try:
                    _logger.info("cloud files final flush on SIGTERM: %s", await flush())
                except Exception:
                    _logger.exception("cloud files final flush on SIGTERM failed")

        async def terminate() -> None:
            try:
                closed, _ = await asyncio.gather(
                    worker.terminate_gracefully(reason="sigterm"), final_flush(),
                    return_exceptions=True,
                )
                if isinstance(closed, BaseException):
                    raise closed
            finally:
                if stream is not None:
                    with contextlib.suppress(Exception):
                        stream.stop()
                if callable(previous) and previous not in (signal.SIG_DFL, signal.SIG_IGN):
                    previous(signal.SIGTERM, None)  # type: ignore[operator]
                else:
                    loop.stop()

        def on_sigterm() -> None:
            nonlocal termination_task
            if termination_task is None:
                termination_task = loop.create_task(terminate(), name="cloud-browser-sigterm")

        warm_task: asyncio.Task[None] | None = None
        if stream is not None and getattr(stream, "keep_warm", False):

            async def start_warm() -> None:
                # Off the event loop (Selkies' listener wait blocks) and never
                # in the way of the worker answering its first request.
                try:
                    await asyncio.to_thread(stream.start_warm)  # type: ignore[attr-defined]
                    _logger.info("cloud computer stream started warm")
                except Exception:
                    _logger.exception("warm stream did not start; it starts on the first view")

            warm_task = loop.create_task(start_warm(), name="cloud-computer-warm-stream")
        # Cloud Computer background services (files sync, agent daemon).
        for start in getattr(_app.state, "background_starters", []):
            start()
        installed = False
        try:
            loop.add_signal_handler(signal.SIGTERM, on_sigterm)
            installed = True
        except (NotImplementedError, RuntimeError, ValueError):
            _logger.warning("SIGTERM handler not installed; Chromium may be killed mid-write")
        try:
            yield
        finally:
            if warm_task is not None and not warm_task.done():
                warm_task.cancel()
            if installed:
                with contextlib.suppress(Exception):
                    loop.remove_signal_handler(signal.SIGTERM)
            # Cloud Computer supervised processes end with the worker (the machine stopping).
            for stop in getattr(_app.state, "background_stoppers", []):
                with contextlib.suppress(Exception):
                    await stop()
            if termination_task is not None:
                # The lifespan is the explicit error owner: retrieving and
                # propagating this result makes a failed profile close fail the
                # worker process instead of becoming an unobserved task error.
                await termination_task

    return lifespan


def create_worker_app(
    worker: BrowserWorker,
    *,
    stream: StreamSupervisor | None = None,
    cloud_computer: CloudComputerLaunch | None = None,
) -> FastAPI:
    """Expose one worker's eight operations without adding another state owner."""
    app = FastAPI(
        title="Matrx persistent browser worker",
        docs_url=None,
        redoc_url=None,
        lifespan=_termination_lifespan(worker, stream),
    )
    if stream is not None:

        def prepare_human_control(rtc_config: M.RtcConfig) -> None:
            try:
                stream.configure_rtc(rtc_config)
                stream.start()
            except Exception:
                # Configuration/start never leaves a half-live default stream behind.
                stream.stop()
                stream.clear_rtc()
                raise

        worker.set_human_control_preparer(
            prepare_human_control,
            lambda: (stream.stop(), stream.clear_rtc()),
        )

    @app.post("/desktop/open-browser")
    async def desktop_open_browser(request: Request) -> dict[str, object]:
        """The desktop's Chrome icon: open the agent's Chrome (same profile)
        when a person had closed it. Answers only the machine itself."""
        client = request.client.host if request.client else ""
        if client not in {"127.0.0.1", "::1"}:
            raise HTTPException(status_code=403, detail="desktop only")
        reopened = await worker.ensure_desktop_browser()
        return {"reopened": reopened, "open": worker.context is not None}

    @app.get("/health")
    async def health() -> dict[str, object]:
        return {
            "status": worker.health,
            "worker_id": worker.worker_id,
            "stream_rtc_config": stream is not None,
            # Keeps a watched stream up while the agent drives (view mode).
            "stream_view": stream is not None,
            # Heartbeats may ask for a liveness probe (``liveness_probe_timeout_ms``).
            "browser_liveness": True,
            # Heartbeats may carry the control plane's tuning (lease_watchdog_grace_seconds, leftover_chrome_grace_seconds).
            "worker_tuning": True,
            # Each agent (CommandRequest.agent_ref) drives its own tab.
            "tab_per_agent": True,
            # Chrome older than the profile's last Chrome (ruling 16), else null.
            "chrome_downgrade": worker.chrome_downgrade,
            # What this build can do for AI Dream's save path (a Cloud Computer worker sets them;
            # a server asking for one not listed words "not on this build", never a 404 error).
            "capabilities": sorted(getattr(app.state, "capabilities", ())),
            # A Cloud Computer hosts several named browsers routed by run_id
            # (machine_browsers.py); a fleet worker hosts one.
            "multi_browser": bool(worker.multi_browser),
            "max_browsers": int(worker.max_browsers),
            "browsers": worker.browsers(),
        }

    @app.post("/machine/record-software")
    async def machine_record_software() -> dict[str, object]:
        """Cloud Computer save-before-stop: record the person's system installs
        into their home so the next task (any build) replays them. Facts only."""
        from .machine_software import record_software

        return await record_software()

    @app.get("/machine/software-status")
    async def machine_software_status() -> dict[str, object]:
        """Progress of the wake-time replay of the person's system installs."""
        from .machine_software import software_status

        return software_status()

    @app.get("/machine/carryover-snapshot")
    async def machine_carryover_snapshot(auth_domain: list[str] = Query(default=[])) -> dict[str, object]:
        """The release carry-over check's snapshot (ruling 16): counts, names and
        hashes of what the person would miss; never cookie values or contents."""
        from .machine_software import carryover_snapshot

        return await carryover_snapshot(auth_domain)

    _install_machine_files_and_agent(app, worker, cloud_computer)

    @app.get("/machine/activity")
    async def machine_activity() -> dict[str, object]:
        """Cloud Computer idle evidence: CPU the person's OWN programs used.

        Facts only, no verdict: the cumulative CPU ticks of every process that is
        not part of the platform's own desktop/browser/stream stack (a shell job,
        a build, an editor), and how many of them are running right now. The
        control plane compares two readings; any growth is activity. Unreadable
        ``/proc`` answers ``available: false`` and never a guessed zero.
        """
        from .machine_activity import read_machine_activity

        source = getattr(app.state, "machine_work", None)
        agent_pid, work = source() if source is not None else (None, None)
        # The supervised host app (an idle server) is the platform's, never the person working:
        # its process tree is left out; only real calls through /app count (AGENT_CALLS).
        hosted = getattr(app.state, "machine_app", None)
        quiet = {hosted.pid} if hosted is not None and hosted.pid is not None else set()
        return await asyncio.to_thread(
            read_machine_activity, agent_pid=agent_pid, work=work, platform_roots=quiet
        )

    @app.post("/bootstrap", response_model=M.BootstrapResponse)
    async def bootstrap(
        request: M.BootstrapRequest, authorization: str | None = Header(default=None)
    ) -> M.BootstrapResponse:
        response = await worker.bootstrap(request, bearer=_bearer(authorization))
        return response

    @app.post("/heartbeat", response_model=M.HeartbeatResponse)
    async def heartbeat(
        request: M.HeartbeatRequest, authorization: str | None = Header(default=None)
    ) -> M.HeartbeatResponse:
        response = await worker.heartbeat(request, bearer=_bearer(authorization))
        if stream is not None and response.ok:
            if not request.access_still_valid:
                stream.stop()
                stream.clear_rtc()
            elif (
                getattr(stream, "running", False)
                and response.controller.state != "human_control"
                and not worker.view_stream_live
                # Another browser on this machine under a person's control keeps it.
                and not worker.human_control_live
            ):
                # Nobody drives and nobody watches any more: end the picture
                # (a kept-warm Cloud Computer stream stays up).
                _end_idle_stream(stream)
        return response

    @app.post("/command", response_model=M.CommandResponse)
    async def command(
        request: M.CommandRequest, authorization: str | None = Header(default=None)
    ) -> M.CommandResponse:
        return await worker.command(request, bearer=_bearer(authorization))

    @app.post("/observe", response_model=M.ObserveResponse)
    async def observe(
        request: M.ObserveRequest, authorization: str | None = Header(default=None)
    ) -> M.ObserveResponse:
        return await worker.observe(request, bearer=_bearer(authorization))

    @app.post("/capture", response_model=M.CaptureResponse)
    async def capture(
        request: M.CaptureRequest, authorization: str | None = Header(default=None)
    ) -> M.CaptureResponse:
        return await worker.capture(request, bearer=_bearer(authorization))

    @app.post("/controller-transition", response_model=M.ControllerTransitionResponse)
    async def controller_transition(
        request: M.ControllerTransitionRequest, authorization: str | None = Header(default=None)
    ) -> M.ControllerTransitionResponse:
        response = await worker.controller_transition(request, bearer=_bearer(authorization))
        if (
            stream is not None
            and response.ok
            and not response.human_input_enabled
            and not worker.view_stream_live
            and not worker.human_control_live
        ):
            # The runtime disabled input synchronously before media stops. A
            # person still watching keeps the picture (control → view), and a
            # kept-warm Cloud Computer stream never drops on a control change.
            _end_idle_stream(stream)
        return response

    @app.post("/checkpoint", response_model=M.CheckpointResponse)
    async def checkpoint(
        request: M.CheckpointRequest, authorization: str | None = Header(default=None)
    ) -> M.CheckpointResponse:
        return await worker.checkpoint(request, bearer=_bearer(authorization))

    @app.post("/shutdown", response_model=M.ShutdownResponse)
    async def shutdown(
        request: M.ShutdownRequest, authorization: str | None = Header(default=None)
    ) -> M.ShutdownResponse:
        response = await worker.shutdown(request, bearer=_bearer(authorization))
        if stream is not None:
            stream.stop()
        return response

    return app


#: What a Cloud Computer worker of this build answers for AI Dream's save path (``/health``).
MACHINE_CAPABILITIES = (
    "cloud_files_flush", "cloud_files_sync_feed", "git_safety_branches", "git_safety_timings", "person_memory",
    "port_preview",
)


def _install_machine_files_and_agent(
    app: FastAPI, worker: BrowserWorker, launch: CloudComputerLaunch | None
) -> None:
    """Cloud Computer only (``launch`` given, i.e. ``MATRX_CLOUD_COMPUTER=1`` read by
    server.py): the ``Cloud`` folder sync (``cloud_files_sync``) and the agent shell/fs
    door to the sandbox daemon (``machine_agent``). Both start in the background;
    neither delays boot."""
    if launch is None:
        return
    import httpx
    from fastapi import Response

    from .cloud_files_sync import start_sync
    from .errors import WorkerProtocolError
    from .machine_app import MachineApp, parse_spec
    from .machine_agent import (
        AGENT_OP,
        AgentDaemon,
        apply_vault_env,
        daemon_refusal,
        home_dir,
        hydrate_for_request,
        run_exec,
    )

    #: The op of the token AI Dream mints for a person's "delete held files" click.
    RESOLVE_OP = "machine_files_resolve"

    home = home_dir()
    app.state.capabilities = MACHINE_CAPABILITIES
    built = start_sync(token=launch.files_token, url=launch.files_url, home=Path(home))
    sync, session = built if built else (None, None)
    daemon = AgentDaemon(home, launch_env=launch.process_env)
    machine_app = MachineApp(home)
    app.state.machine_app = machine_app
    app.state.background_stoppers = [machine_app.stop]
    tasks: list[asyncio.Task[None]] = []

    def _start_machine_services() -> None:
        tasks.append(asyncio.create_task(daemon.run_forever(), name="cloud-computer-agent-daemon"))
        if sync is not None and session is not None:
            tasks.append(
                asyncio.create_task(sync.run_forever(renew=session.renew), name="cloud-computer-files")
            )

    app.state.background_starters = [_start_machine_services]
    if sync is not None:
        app.state.background_flushers = [sync.flush]

    def _machine_work() -> tuple[int | None, dict[str, object] | None]:
        """What the build move must never interrupt: the agent daemon's pid (its
        child processes are agent shell work) and the Cloud folder's transfers."""
        proc = daemon._proc
        pid = proc.pid if proc is not None and proc.returncode is None else None
        return pid, (sync.work_signals() if sync is not None else None)

    app.state.machine_work = _machine_work

    def _local_only(request: Request) -> None:
        client = request.client.host if request.client else ""
        if client not in {"127.0.0.1", "::1"}:
            raise HTTPException(status_code=403, detail="machine only")

    @app.get("/machine/cloud-files/status")
    async def cloud_files_status() -> dict[str, object]:
        """The Cloud folder's sync state (counts, cursor, knobs, last error) and the agent daemon."""
        sync_status = sync.status() if sync is not None else {"enabled": False}
        if sync is not None and sync_status["work"]["clean_since_flush_request"]:
            # Clean at the moment of answering: nothing changed since the qualifying pass's scan.
            sync_status["work"]["clean_since_flush_request"] = await sync.clean_now()
        return {
            "sync": sync_status,
            "session": {
                "expires_at": session.expires_at, "renew_error": session.renew_error,
            } if session is not None else None,
            "agent_daemon": daemon.status(),
        }

    @app.post("/machine/cloud-files/fetch")
    async def cloud_files_fetch(request: Request, path: str = Query(...)) -> dict[str, object]:
        """``cloud-files fetch <path>`` on the machine: download a stub's real file."""
        _local_only(request)
        if sync is None:
            raise HTTPException(status_code=409, detail="cloud files sync is off on this machine")
        rel = sync.rel_for(path)
        if rel is None or rel not in sync.entries:
            raise HTTPException(status_code=404, detail="not a file in the Cloud folder")
        return {"path": rel, "fetched": await sync.hydrate(rel)}

    @app.post("/machine/cloud-files/sync-now")
    async def cloud_files_sync_now(request: Request) -> dict[str, object]:
        _local_only(request)
        if sync is None:
            raise HTTPException(status_code=409, detail="cloud files sync is off on this machine")
        await sync.pull_once()
        await sync.push_once()
        return sync.status()

    @app.post("/machine/cloud-files/flush")
    async def cloud_files_flush(timeout_seconds: float | None = Query(default=None)) -> dict[str, object]:
        """Save-before-stop: one final sync pass that waits (bounded by the knob AI Dream
        sends, else ``final_flush_seconds``) until every local Cloud change is uploaded
        and every conflict copy written. Answers what was left; never silent."""
        if sync is None:
            return {"flushed": False, "reason": "cloud files sync is off on this machine", "enabled": False}
        return await sync.flush(timeout_seconds)

    @app.post("/machine/git/safety-branches")
    async def machine_git_safety_branches(
        machine_id: str = Query(...), git_timeout_seconds: float = Query(..., gt=0),
        deadline_seconds: float | None = Query(default=None, gt=0),
    ) -> dict[str, object]:
        """Save-before-stop, ruling 19: every repository under the home with unsaved work is
        pushed to ``safety/<machine-id>-<date>`` with the owner's GitHub credential (the token
        file the daemon's git helper reads). Answers each repository: pushed, or why not."""
        from .machine_git_safety import push_safety_branches

        return await push_safety_branches(
            Path(home), machine_id=machine_id, base_env=daemon._env(),
            git_timeout_seconds=git_timeout_seconds, token_file=daemon.git_token_path,
            deadline_seconds=deadline_seconds,
        )

    @app.post("/machine/cloud-files/resolve-held")
    async def cloud_files_resolve_held(request: Request) -> dict[str, object]:
        """The person's answer to held deletes: ``{"hold_id", "action": "delete"|"restore"}``.

        ``restore`` is always safe (the files come back from the cloud), so the
        loopback CLI may ask for it. ``delete`` needs the short-lived token AI Dream
        mints only for the person's own signed-in click in the app (``mtx_op=
        machine_files_resolve``, header ``X-Matrx-Resolve-Token``): an agent on this
        machine holds no such token, so it can never confirm its own mass delete
        (review 2 N5)."""
        from .cloud_files_sync import RESOLVE_ACTIONS, HoldChanged

        body = await request.json()
        hold_id = str((body or {}).get("hold_id") or "")
        action = str((body or {}).get("action") or "")
        if action not in RESOLVE_ACTIONS:
            raise HTTPException(status_code=422, detail="action must be delete or restore")
        token = request.headers.get("x-matrx-resolve-token", "")
        if token:
            verifier = worker.token_verifier
            if verifier is None:
                raise HTTPException(status_code=503, detail="no token verifier")
            try:
                verifier.verify(token, worker_id=worker.worker_id, op=RESOLVE_OP, session=True)
            except WorkerProtocolError as exc:
                raise HTTPException(status_code=401, detail=exc.code) from exc
        elif action == "delete":
            raise HTTPException(
                status_code=403,
                detail="deleting held files is confirmed in the AI Matrx app (Computer tab)",
            )
        else:
            _local_only(request)
        if sync is None:
            raise HTTPException(status_code=409, detail="cloud files sync is off on this machine")
        try:
            answer = await sync.resolve_held(hold_id, action)
        except HoldChanged as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return {**answer, "status": sync.status()}

    @app.post("/machine/vault-env")
    async def machine_vault_env(request: Request) -> dict[str, object]:
        """AI Dream pushes the owner's Vault env at binding (machine agent token
        only). The values stay in this process's memory and ride every agent
        ``exec``; the answer names what changed — names only, never a value."""
        verifier = worker.token_verifier
        if verifier is None:
            raise HTTPException(status_code=503, detail="no token verifier")
        try:
            verifier.verify(
                request.headers.get("x-sandbox-access-token", ""),
                worker_id=worker.worker_id, op=AGENT_OP, session=True,
            )
        except WorkerProtocolError as exc:
            raise HTTPException(status_code=401, detail=exc.code) from exc
        try:
            payload = await request.json()
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="body must be JSON") from exc
        env = payload.get("env") if isinstance(payload, dict) else None
        if not isinstance(env, dict):
            raise HTTPException(status_code=422, detail="env must be an object of name -> value")
        return apply_vault_env(daemon, env)

    def _verify_agent_token(token: str) -> None:
        _verify_agent({"x-sandbox-access-token": token})

    # The person's memory, a read-only rendering AI Dream pushes at wake and binding.
    from .machine_memory import install_memory_route

    install_memory_route(app, home=home, verify=_verify_agent_token)

    def _verify_agent(headers: Any) -> None:
        verifier = worker.token_verifier
        if verifier is None:
            raise HTTPException(status_code=503, detail="no token verifier")
        try:
            verifier.verify(
                headers.get("x-sandbox-access-token", ""),
                worker_id=worker.worker_id, op=AGENT_OP, session=True,
            )
        except WorkerProtocolError as exc:
            raise HTTPException(status_code=401, detail=exc.code) from exc

    @app.get("/machine/app")
    async def machine_app_status(request: Request) -> dict[str, object]:
        """The supervised app's state (names only, never an env value)."""
        _verify_agent(request.headers)
        return machine_app.status()

    @app.put("/machine/app")
    async def machine_app_apply(request: Request) -> dict[str, object]:
        """The host names the one app this machine supervises (machines plan 4b part 2
        item 3): argv, folder in the home, loopback port, exact env. Same spec again is a
        no-op; a new one replaces the old process. Machine agent token only."""
        _verify_agent(request.headers)
        try:
            spec = parse_spec(await request.json(), home=home)
        except ValueError as exc:  # AppSpecError and bad JSON alike
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return await machine_app.apply(spec)

    @app.delete("/machine/app")
    async def machine_app_stop(request: Request) -> dict[str, object]:
        _verify_agent(request.headers)
        await machine_app.stop()
        return machine_app.status()

    #: Request headers never relayed into the app: the worker's own credential (consumed
    #: here, like the old orchestrator proxy) and hop-by-hop framing.
    _APP_DROP_REQUEST = frozenset({
        "x-sandbox-access-token", "host", "content-length", "connection", "keep-alive",
        "transfer-encoding", "upgrade", "te", "trailer", "proxy-authorization",
    })
    _APP_DROP_RESPONSE = frozenset({"content-length", "connection", "keep-alive", "transfer-encoding"})

    @app.api_route("/app/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    async def app_door(path: str, request: Request) -> Response:
        """The supervised app's HTTP, relayed byte for byte (streams included, no read
        deadline). Authenticated like ``/agent``; the caller's ``Authorization`` (the
        PERSON's JWT) passes through untouched — the app's own owner check reads it."""
        from .machine_activity import AGENT_CALLS

        _verify_agent(request.headers)
        port = machine_app.port
        if port is None:
            raise HTTPException(status_code=409, detail="no app is configured on this machine")
        if not await machine_app.wait_listening(2.0):
            raise HTTPException(status_code=503, detail="the machine's app is not listening yet")
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _APP_DROP_REQUEST}
        raw = await request.body()
        client = shared_client(resend=False, timeout=httpx.Timeout(30.0, read=None))
        # A live app call (a coding turn's stream) is work the build move waits for.
        AGENT_CALLS.count += 1
        try:
            upstream = await client.send(
                client.build_request(
                    request.method, f"http://127.0.0.1:{port}/{path}",
                    params=list(request.query_params.multi_items()),
                    content=raw or None, headers=headers,
                ),
                stream=True,
            )
        except httpx.HTTPError as exc:
            await client.aclose()
            AGENT_CALLS.count -= 1
            raise HTTPException(status_code=503, detail=f"the machine's app did not answer: {exc}") from exc

        async def relay():  # noqa: ANN202
            try:
                async for chunk in upstream.aiter_raw():
                    yield chunk
            finally:
                await upstream.aclose()
                await client.aclose()
                AGENT_CALLS.count -= 1

        return StreamingResponse(
            relay(), status_code=upstream.status_code,
            headers={k: v for k, v in upstream.headers.items() if k.lower() not in _APP_DROP_RESPONSE},
        )

    # ── port previews (a dev server on this machine, for a person AI Dream admitted) ──
    from .machine_agent import MACHINE_SERVICE_PORTS

    _preview_reserved = MACHINE_SERVICE_PORTS | {daemon.port}
    with contextlib.suppress(ValueError):
        _preview_reserved |= {int(os.environ.get("BROWSER_WORKER_PORT") or 8002)}

    def _preview_port(port: int) -> None:
        if not 1 <= port <= 65535 or port in _preview_reserved:
            raise HTTPException(status_code=403, detail=f"port {port} cannot be previewed")

    @app.api_route(
        "/agent/preview/{port}/{path:path}",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
        include_in_schema=False,
    )
    async def preview_door(port: int, path: str, request: Request) -> Response:
        """A dev server on this machine's loopback, relayed byte for byte (streams included).
        Only AI Dream reaches this (private address + the machine agent token); AI Dream already
        checked the person may use this machine. ``localhost`` so an app bound to ``::1`` only
        (Node's default for ``localhost``) answers too; the Host header is ``localhost:<port>``,
        which dev servers' host checks accept."""
        _verify_agent(request.headers)
        _preview_port(port)
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _APP_DROP_REQUEST}
        raw = await request.body()
        client = shared_client(resend=False, timeout=httpx.Timeout(30.0, read=None), follow_redirects=False)
        try:
            upstream = await client.send(
                client.build_request(
                    request.method, f"http://localhost:{port}/{path}",
                    params=list(request.query_params.multi_items()),
                    content=raw or None, headers=headers,
                ),
                stream=True,
            )
        except httpx.HTTPError as exc:
            await client.aclose()
            raise HTTPException(
                status_code=502, detail=f"nothing answered on port {port} of this machine: {exc}"
            ) from exc

        async def relay():  # noqa: ANN202
            try:
                async for chunk in upstream.aiter_raw():
                    yield chunk
            finally:
                await upstream.aclose()
                await client.aclose()

        return StreamingResponse(
            relay(), status_code=upstream.status_code,
            headers={k: v for k, v in upstream.headers.items() if k.lower() not in _APP_DROP_RESPONSE},
        )

    @app.websocket("/agent/preview/{port}/{path:path}")
    async def preview_socket(websocket: WebSocket, port: int, path: str) -> None:
        """A dev server's WebSocket (hot reload) on this machine's loopback; the offered
        subprotocols (``vite-hmr``) pass through."""
        from websockets.asyncio.client import connect as ws_connect
        from websockets.exceptions import WebSocketException

        try:
            _verify_agent(websocket.headers)
            _preview_port(port)
        except HTTPException as exc:
            await websocket.close(code=4000 + exc.status_code, reason=str(exc.detail)[:120])
            return
        offered = [p.strip() for p in (websocket.headers.get("sec-websocket-protocol") or "").split(",") if p.strip()]
        query = websocket.url.query
        extra = {"Cookie": websocket.headers["cookie"]} if websocket.headers.get("cookie") else None
        try:
            async with ws_connect(
                f"ws://localhost:{port}/{path}" + (f"?{query}" if query else ""),
                subprotocols=offered or None, additional_headers=extra, max_size=None,
            ) as upstream:
                await websocket.accept(subprotocol=upstream.subprotocol)

                async def to_client() -> None:
                    async for message in upstream:
                        if isinstance(message, bytes):
                            await websocket.send_bytes(message)
                        else:
                            await websocket.send_text(message)

                async def to_app() -> None:
                    while True:
                        message = await websocket.receive()
                        if message.get("type") == "websocket.disconnect":
                            return
                        if message.get("text") is not None:
                            await upstream.send(message["text"])
                        elif message.get("bytes") is not None:
                            await upstream.send(message["bytes"])

                await run_pumps_then_cleanup([to_client(), to_app()])
        except (OSError, WebSocketException) as exc:
            _logger.warning("[machine-agent] preview socket on port %s ended: %s", port, exc)
            with contextlib.suppress(Exception):
                await websocket.close(code=1011, reason="the app is not reachable")
            return
        with contextlib.suppress(Exception):
            await websocket.close()

    @app.websocket("/agent/pty")
    async def agent_pty(websocket: WebSocket) -> None:
        """The person's interactive terminal on THIS machine: the daemon's ``/pty``
        relayed byte-for-byte (machines plan 4b). Same agent token as every ``/agent``
        call, in the ``X-Sandbox-Access-Token`` header AI Dream's relay sends. An open
        terminal counts as agent work, so the build move never cuts it."""
        from websockets.asyncio.client import connect as ws_connect
        from websockets.exceptions import ConnectionClosed

        from .machine_activity import AGENT_CALLS

        verifier = worker.token_verifier
        if verifier is None:
            await websocket.close(code=1011, reason="no token verifier")
            return
        try:
            verifier.verify(
                websocket.headers.get("x-sandbox-access-token", ""),
                worker_id=worker.worker_id, op=AGENT_OP, session=True,
            )
        except WorkerProtocolError as exc:
            await websocket.close(code=4401, reason=exc.code)
            return
        params = {k: v for k, v in websocket.query_params.items() if k in ("cols", "rows")}
        params["agent_token"] = daemon.token
        query = "&".join(f"{k}={v}" for k, v in params.items())
        await websocket.accept()
        with AGENT_CALLS:
            try:
                async with ws_connect(f"ws://127.0.0.1:{daemon.port}/pty?{query}", max_size=None) as upstream:

                    async def to_client() -> None:
                        async for message in upstream:
                            if isinstance(message, bytes):
                                await websocket.send_bytes(message)
                            else:
                                await websocket.send_text(message)

                    async def to_daemon() -> None:
                        while True:
                            message = await websocket.receive()
                            if message.get("type") == "websocket.disconnect":
                                return
                            if message.get("text") is not None:
                                await upstream.send(message["text"])
                            elif message.get("bytes") is not None:
                                await upstream.send(message["bytes"])

                    await run_pumps_then_cleanup([to_client(), to_daemon()])
            except (OSError, ConnectionClosed) as exc:
                _logger.warning("[machine-agent] terminal relay ended: %s", exc)
        with contextlib.suppress(Exception):
            await websocket.close()

    @app.api_route("/agent/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    async def agent_door(path: str, request: Request) -> Response:
        """The sandbox agent API (fs, exec, search, git) of THIS machine, for agent tools.
        Every call is counted while it runs (``/machine/activity``), so a long agent
        command is work the build move waits for."""
        from .machine_activity import AGENT_CALLS

        with AGENT_CALLS:
            return await _agent_call(path, request)

    async def _agent_call(path: str, request: Request) -> Response:
        verifier = worker.token_verifier
        if verifier is None:
            raise HTTPException(status_code=503, detail="no token verifier")
        try:
            verifier.verify(
                request.headers.get("x-sandbox-access-token", ""),
                worker_id=worker.worker_id, op=AGENT_OP, session=True,
            )
        except WorkerProtocolError as exc:
            raise HTTPException(status_code=401, detail=exc.code) from exc
        import json

        raw = await request.body()
        body: object = None
        if raw and "json" in (request.headers.get("content-type") or ""):
            try:
                body = json.loads(raw)
            except ValueError:
                body = None
        params = dict(request.query_params)
        await hydrate_for_request(request.method, path, params, body, sync)
        # A clone or push outlasts a file read; the app's git routes allow 120 s.
        timeout = 150.0 if path.startswith("git/") else 70.0
        if isinstance(body, dict) and isinstance(body.get("timeout"), (int, float)):
            timeout = float(body["timeout"]) + 15.0
        # A wake's first call can arrive before the daemon binds (/health answers
        # first); it waits for the bind within the call's own deadline.
        if daemon.available and not await daemon.wait_listening(timeout):
            raise HTTPException(status_code=503, detail="agent daemon is not listening yet")
        if path == "exec" and request.method == "POST" and isinstance(body, dict):
            try:
                return Response(
                    content=json.dumps(await run_exec(daemon, body, timeout=timeout)),
                    media_type="application/json",
                )
            except httpx.HTTPStatusError as exc:
                # The daemon refused the command (a folder that is not there, a bad body): its
                # own status and sentence, never a 503 that reads as the machine being down.
                if 400 <= exc.response.status_code < 500:
                    raise HTTPException(
                        status_code=exc.response.status_code, detail=daemon_refusal(exc.response)
                    ) from exc
                raise HTTPException(status_code=503, detail=f"agent daemon exec failed: {exc}") from exc
            except httpx.HTTPError as exc:
                raise HTTPException(status_code=503, detail=f"agent daemon exec failed: {exc}") from exc
        headers = {"x-matrx-agent-token": daemon.token}
        if request.headers.get("content-type"):
            headers["content-type"] = request.headers["content-type"]
        if path == "exec/stream":
            # A live command stream: relay each chunk as it comes, with no read deadline
            # (a long build is quiet between lines); buffering here showed nothing until the end.
            client = shared_client(resend=False, timeout=httpx.Timeout(timeout, read=None))
            try:
                upstream = await client.send(
                    client.build_request(
                        request.method, f"{daemon.base_url}/{path}", params=params,
                        content=raw, headers=headers,
                    ),
                    stream=True,
                )
            except httpx.HTTPError as exc:
                await client.aclose()
                raise HTTPException(status_code=503, detail=f"agent daemon unreachable: {exc}") from exc

            async def relay():
                try:
                    async for chunk in upstream.aiter_raw():
                        yield chunk
                finally:
                    await upstream.aclose()
                    await client.aclose()

            return StreamingResponse(
                relay(), status_code=upstream.status_code,
                headers={
                    k: v for k, v in upstream.headers.items()
                    if k.lower().startswith("x-matrx-") or k.lower() == "content-type"
                },
            )
        try:
            async with shared_client(resend=False, timeout=timeout) as client:
                upstream = await client.request(
                    request.method, f"{daemon.base_url}/{path}", params=params,
                    content=raw, headers=headers,
                )
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=503, detail=f"agent daemon unreachable: {exc}") from exc
        passthrough = {
            k: v for k, v in upstream.headers.items()
            if k.lower().startswith("x-matrx-") or k.lower() == "content-type"
        }
        return Response(content=upstream.content, status_code=upstream.status_code, headers=passthrough)
