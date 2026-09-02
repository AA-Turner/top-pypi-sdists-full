"""Authenticated HTTP transport for the persistent browser worker."""

from __future__ import annotations

from fastapi import FastAPI, Header

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

from typing import Protocol


class StreamSupervisor(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...


def _bearer(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, separator, value = authorization.partition(" ")
    if separator and scheme.lower() == "bearer" and value:
        return value
    return None


def create_worker_app(worker: BrowserWorker, *, stream: StreamSupervisor | None = None) -> FastAPI:
    """Expose one worker's eight operations without adding another state owner."""
    app = FastAPI(title="Matrx persistent browser worker", docs_url=None, redoc_url=None)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": worker.health, "worker_id": worker.worker_id}

    @app.post("/bootstrap", response_model=M.BootstrapResponse)
    async def bootstrap(
        request: M.BootstrapRequest, authorization: str | None = Header(default=None)
    ) -> M.BootstrapResponse:
        response = await worker.bootstrap(request, bearer=_bearer(authorization))
        if (
            response.ok
            and request.policy.reopened_controller_state == "human_control"
            and request.policy.reopened_human_input_enabled
            and stream is not None
        ):
            stream.start()
        return response

    @app.post("/heartbeat", response_model=M.HeartbeatResponse)
    async def heartbeat(
        request: M.HeartbeatRequest, authorization: str | None = Header(default=None)
    ) -> M.HeartbeatResponse:
        return await worker.heartbeat(request, bearer=_bearer(authorization))

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
        starting_human_control = request.to_state == "human_control" and request.enable_human_input
        if starting_human_control and stream is not None:
            stream.start()
        response = await worker.controller_transition(request, bearer=_bearer(authorization))
        if stream is not None:
            if not response.ok and starting_human_control:
                stream.stop()
            elif response.ok and not response.human_input_enabled:
                # The runtime disabled input synchronously before media stops.
                stream.stop()
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
