"""MachineBrowsers — several named browsers on one Cloud Computer.

A fleet worker is "one process, one Chromium profile, one run" (``runtime.py``).
A Cloud Computer is the person's own machine and runs as many of their browsers
as its owner allows (Arman 2026-11-01: every browser runs on the person's or
organization's machine, each agent in its own tab or window). This host keeps that one-run runtime UNCHANGED and holds one
``BrowserWorker`` per live run:

* every S2 envelope already carries ``run_id``, so ``/bootstrap /heartbeat
  /command /observe /capture /controller-transition /checkpoint /shutdown``
  route to the run's own worker — its own profile directory, host lock,
  Chromium singleton and ordered command queue (the three fences are per
  profile already);
* a bootstrap for a NEW run takes a free worker (a stopped one is reused) or a
  new one up to ``max_browsers``; the same profile while it is live goes to its
  own worker, which answers ``already_bootstrapped`` exactly as before (the
  manager then attaches or fences); a full host answers
  ``machine_browsers_full`` and launches nothing;
* each browser opens its own window (window class per profile, ``runtime.py``)
  and opening its view or taking control raises that window on the one
  desktop the stream shows.

How many browsers a machine runs is the control plane's knob
(``cloud_computer.browsers.max_live_per_machine``; the manager closes the idle
one or refuses before it bootstraps). ``max_browsers`` here is only the host's
own safety ceiling so a confused caller can never exhaust the machine.

The HTTP layer (``http_app.create_worker_app``) takes this object in place of
one ``BrowserWorker``: it answers the same attributes and operations.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from collections.abc import Callable
from typing import Any

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.errors import WorkerProtocolError
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

logger = logging.getLogger(__name__)

#: The host's own safety ceiling, equal to the top of the control plane's setting
#: ``cloud_computer.browsers.max_live_per_machine`` (16), which is what actually decides how many
#: run. No environment variable: the setting lowers it, a confused caller cannot exceed it.
DEFAULT_MAX_BROWSERS = 16

#: Health values that mean "this browser is up and serving its run".
_SERVING = frozenset({"healthy", "ready", "degraded"})


class MachineBrowsers:
    """``run_id`` → its own ``BrowserWorker``; one desktop, several windows."""

    multi_browser = True

    def __init__(
        self,
        primary: BrowserWorker,
        *,
        factory: Callable[[], BrowserWorker],
        max_browsers: int = DEFAULT_MAX_BROWSERS,
    ) -> None:
        self._primary = primary
        self._factory = factory
        self.max_browsers = max(1, int(max_browsers))
        self._workers: list[BrowserWorker] = [primary]
        self._by_run: dict[str, BrowserWorker] = {}
        self._placement_gate = asyncio.Lock()
        self._preparer: tuple[Any, Any] | None = None
        # Answers a run this host does not hold ("not_bootstrapped"): the
        # manager's own recovery for a worker that lost its session.
        self._nobody: BrowserWorker | None = None
        self._watched: dict[int, bool] = {}

    # ── the attributes the HTTP layer reads ────────────────────────────────

    @property
    def worker_id(self) -> str:
        return self._primary.worker_id

    @property
    def token_verifier(self) -> Any:
        """Every browser on the machine shares the one verifier ``server.py`` built;
        the ``/agent`` door, terminal and ``/machine/*`` routes verify through it
        (missing here, every agent door answered 503 on image 297821e6)."""
        return self._primary.token_verifier

    @property
    def chrome_downgrade(self) -> dict[str, str | None] | None:
        for worker in self._workers:
            if worker.chrome_downgrade is not None:
                return worker.chrome_downgrade
        return None

    @property
    def health(self) -> str:
        for worker in self._workers:
            if worker.health in _SERVING:
                return worker.health
        return self._primary.health

    @property
    def view_stream_live(self) -> bool:
        return any(worker.view_stream_live for worker in self._workers)

    @property
    def human_control_live(self) -> bool:
        """A person controls one of this machine's browsers right now."""
        return any(worker.controller_state == "human_control" for worker in self._workers)

    @property
    def context(self) -> Any:
        for worker in self._workers:
            if worker.context is not None:
                return worker.context
        return None

    @property
    def workers(self) -> tuple[BrowserWorker, ...]:
        return tuple(self._workers)

    def browsers(self) -> list[dict[str, object]]:
        """The open browsers, for ``/health`` and the desktop launcher."""
        return [
            {
                "run_id": worker.run_id,
                "profile_id": worker.profile_id,
                "health": worker.health,
                "window_class": worker.window_class,
            }
            for worker in self._workers
            if worker.run_id and not worker.free_for_new_run
        ]

    def set_human_control_preparer(self, prepare: Any, clear: Any = None) -> None:
        self._preparer = (prepare, clear)
        for worker in self._workers:
            worker.set_human_control_preparer(prepare, clear)

    # ── placement ──────────────────────────────────────────────────────────

    def _new_worker(self) -> BrowserWorker:
        worker = self._factory()
        if self._preparer is not None:
            worker.set_human_control_preparer(*self._preparer)
        return worker

    def _holding(self, run_id: str) -> BrowserWorker | None:
        worker = self._by_run.get(run_id)
        if worker is not None:
            return worker
        for candidate in self._workers:
            if candidate.run_id == run_id and run_id:
                return candidate
        return None

    def _place(self, request: M.BootstrapRequest) -> BrowserWorker | None:
        held = self._holding(request.run_id)
        if held is not None:
            return held
        for worker in self._workers:
            if worker.profile_id == request.profile_id and not worker.free_for_new_run:
                # The same profile live here: its own worker answers
                # ``already_bootstrapped`` (never a second Chromium on it).
                return worker
        free = next((w for w in self._workers if w.free_for_new_run), None)
        if free is None and len(self._workers) < self.max_browsers:
            free = self._new_worker()
            self._workers.append(free)
        if free is None:
            return None
        for stale in [key for key, worker in self._by_run.items() if worker is free]:
            del self._by_run[stale]
        self._by_run[request.run_id] = free
        return free

    def _route(self, run_id: str) -> BrowserWorker:
        held = self._holding(run_id)
        if held is not None:
            return held
        if self._nobody is None:
            self._nobody = self._new_worker()
        return self._nobody

    # ── the eight operations ───────────────────────────────────────────────

    async def bootstrap(
        self, request: M.BootstrapRequest, *, bearer: str | None = None
    ) -> M.BootstrapResponse:
        async with self._placement_gate:
            worker = self._place(request)
        if worker is None:
            logger.warning(
                "machine browsers full (%d): run %s not started", self.max_browsers, request.run_id
            )
            return self._primary._error_reply(  # noqa: SLF001 - same reply shape
                M.BootstrapResponse,
                WorkerProtocolError(
                    "machine_browsers_full",
                    message=f"this machine already runs {self.max_browsers} browsers",
                ),
                accepted=False,
                host_lock_acquired=False,
            )
        return await worker.bootstrap(request, bearer=bearer)

    async def heartbeat(
        self, request: M.HeartbeatRequest, *, bearer: str | None = None
    ) -> M.HeartbeatResponse:
        worker = self._route(request.run_id)
        response = await worker.heartbeat(request, bearer=bearer)
        await self._raise_when_newly_watched(worker)
        return response

    async def command(
        self, request: M.CommandRequest, *, bearer: str | None = None
    ) -> M.CommandResponse:
        return await self._route(request.run_id).command(request, bearer=bearer)

    async def observe(
        self, request: M.ObserveRequest, *, bearer: str | None = None
    ) -> M.ObserveResponse:
        return await self._route(request.run_id).observe(request, bearer=bearer)

    async def capture(
        self, request: M.CaptureRequest, *, bearer: str | None = None
    ) -> M.CaptureResponse:
        return await self._route(request.run_id).capture(request, bearer=bearer)

    async def controller_transition(
        self, request: M.ControllerTransitionRequest, *, bearer: str | None = None
    ) -> M.ControllerTransitionResponse:
        worker = self._route(request.run_id)
        response = await worker.controller_transition(request, bearer=bearer)
        if response.ok and getattr(response, "human_input_enabled", False):
            # Take control of THIS browser: its window comes to the front.
            await worker.raise_window()
        return response

    async def checkpoint(
        self, request: M.CheckpointRequest, *, bearer: str | None = None
    ) -> M.CheckpointResponse:
        return await self._route(request.run_id).checkpoint(request, bearer=bearer)

    async def shutdown(
        self, request: M.ShutdownRequest, *, bearer: str | None = None
    ) -> M.ShutdownResponse:
        return await self._route(request.run_id).shutdown(request, bearer=bearer)

    async def _raise_when_newly_watched(self, worker: BrowserWorker) -> None:
        """A view stream opened on this run (heartbeat ``stream_view_seconds``):
        raise its window so the picture shows THIS browser."""
        watched = worker.view_stream_live
        was = self._watched.get(id(worker), False)
        self._watched[id(worker)] = watched
        if watched and not was:
            await worker.raise_window()

    # ── the desktop and the process ────────────────────────────────────────

    async def ensure_desktop_browser(self) -> bool:
        """The desktop's Chrome icon: reopen every browser a person closed."""
        reopened = False
        for worker in self._workers:
            with contextlib.suppress(Exception):
                reopened = await worker.ensure_desktop_browser() or reopened
        return reopened

    async def terminate_gracefully(self, *, reason: str) -> None:
        await asyncio.gather(
            *(worker.terminate_gracefully(reason=reason) for worker in self._workers),
            return_exceptions=True,
        )


__all__ = ["DEFAULT_MAX_BROWSERS", "MachineBrowsers"]
