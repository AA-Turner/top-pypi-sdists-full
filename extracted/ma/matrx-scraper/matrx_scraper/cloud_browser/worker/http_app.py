"""Authenticated HTTP transport for the persistent browser worker."""

from __future__ import annotations

import asyncio
import contextlib
import logging
import signal
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Query, Request

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.cloud_computer_launch import CloudComputerLaunch
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

from typing import Protocol


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

        async def terminate() -> None:
            try:
                await worker.terminate_gracefully(reason="sigterm")
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
            # Chrome older than the profile's last Chrome (ruling 16), else null.
            "chrome_downgrade": worker.chrome_downgrade,
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
        return await asyncio.to_thread(read_machine_activity, agent_pid=agent_pid, work=work)

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
    from .machine_agent import AGENT_OP, AgentDaemon, home_dir, hydrate_for_request, run_exec

    #: The op of the token AI Dream mints for a person's "delete held files" click.
    RESOLVE_OP = "machine_files_resolve"

    home = home_dir()
    built = start_sync(token=launch.files_token, url=launch.files_url, home=Path(home))
    sync, session = built if built else (None, None)
    daemon = AgentDaemon(home, launch_env=launch.process_env)
    tasks: list[asyncio.Task[None]] = []

    def _start_machine_services() -> None:
        tasks.append(asyncio.create_task(daemon.run_forever(), name="cloud-computer-agent-daemon"))
        if sync is not None and session is not None:
            tasks.append(
                asyncio.create_task(sync.run_forever(renew=session.renew), name="cloud-computer-files")
            )

    app.state.background_starters = [_start_machine_services]

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
        return {
            "sync": sync.status() if sync is not None else {"enabled": False},
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
            verifier = getattr(worker, "_verifier", None)
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

    @app.api_route("/agent/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    async def agent_door(path: str, request: Request) -> Response:
        """The sandbox agent API (fs, exec, search, git) of THIS machine, for agent tools.
        Every call is counted while it runs (``/machine/activity``), so a long agent
        command is work the build move waits for."""
        from .machine_activity import AGENT_CALLS

        with AGENT_CALLS:
            return await _agent_call(path, request)

    async def _agent_call(path: str, request: Request) -> Response:
        verifier = getattr(worker, "_verifier", None)
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
        timeout = 70.0
        if isinstance(body, dict) and isinstance(body.get("timeout"), (int, float)):
            timeout = float(body["timeout"]) + 15.0
        if path == "exec" and request.method == "POST" and isinstance(body, dict):
            try:
                return Response(
                    content=json.dumps(await run_exec(daemon, body, timeout=timeout)),
                    media_type="application/json",
                )
            except httpx.HTTPError as exc:
                raise HTTPException(status_code=503, detail=f"agent daemon exec failed: {exc}") from exc
        headers = {"x-matrx-agent-token": daemon.token}
        if request.headers.get("content-type"):
            headers["content-type"] = request.headers["content-type"]
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
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
