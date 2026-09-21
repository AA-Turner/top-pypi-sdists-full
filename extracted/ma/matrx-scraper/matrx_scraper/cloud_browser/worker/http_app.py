"""Authenticated HTTP transport for the persistent browser worker."""

from __future__ import annotations

import asyncio
import contextlib
import logging
import signal

from fastapi import FastAPI, Header

from matrx_scraper.cloud_browser.worker import models as M
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

        installed = False
        try:
            loop.add_signal_handler(signal.SIGTERM, on_sigterm)
            installed = True
        except (NotImplementedError, RuntimeError, ValueError):
            _logger.warning("SIGTERM handler not installed; Chromium may be killed mid-write")
        try:
            yield
        finally:
            if installed:
                with contextlib.suppress(Exception):
                    loop.remove_signal_handler(signal.SIGTERM)
            if termination_task is not None:
                # The lifespan is the explicit error owner: retrieving and
                # propagating this result makes a failed profile close fail the
                # worker process instead of becoming an unobserved task error.
                await termination_task

    return lifespan


def create_worker_app(worker: BrowserWorker, *, stream: StreamSupervisor | None = None) -> FastAPI:
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

    @app.get("/health")
    async def health() -> dict[str, object]:
        return {
            "status": worker.health,
            "worker_id": worker.worker_id,
            "stream_rtc_config": stream is not None,
        }

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
        if stream is not None and response.ok and not response.human_input_enabled:
            # The runtime disabled input synchronously before media stops.
            stream.stop()
            stream.clear_rtc()
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
