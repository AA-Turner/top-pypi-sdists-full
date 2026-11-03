"""The tour: right after setup, myOrb shows the demo's made-up day with a guide through it, then
leads to the Get started steps; from then on the user's own data.

While it runs, every page the user opens is served by a second myOrb inside this one: the public
demo, with a database of its own under data_dir/tour. So nothing the user does in the tour
touches their own data, and the demo's pages need no changes to show it. Only ending the tour,
signing out and the files every page loads stay with this myOrb.

It ends only on purpose: with the button of its last step, or by confirming "End the tour"
(tour.js). Closing the page or signing out keeps it for next time.
"""

import asyncio
import logging
from contextlib import AsyncExitStack
from typing import Any

import httpx2
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from myorb.config import Settings
from myorb.connections import store

logger = logging.getLogger(__name__)

router = APIRouter()

PROVIDER = "tour"
# Served by this myOrb during the tour too: the tour's own routes and signing out.
OWN = ("/tour/", "/logout")


class Tour:
    """Whether the tour runs, kept in the database, and the demo that shows it."""

    def __init__(self, settings: Settings, transport: httpx2.AsyncBaseTransport | None) -> None:
        self.settings = settings.model_copy(
            update={
                "data_dir": settings.data_dir / "tour",
                "demo": True,
                "public_demo": True,
                "tour": True,
                "plugins": None,
            }
        )
        self.transport = transport
        self.active = False
        self._demo: ASGIApp | None = None
        self._stack: AsyncExitStack | None = None
        self._lock = asyncio.Lock()

    async def load(self, app: Any) -> None:
        async with app.state.sessionmaker() as db:
            data = await store.get_provider_settings(db, app.state.secret_box, PROVIDER)
        self.active = bool(data and data.get("active"))

    async def set(self, app: Any, active: bool) -> None:
        async with app.state.sessionmaker() as db:
            await store.save_provider_settings(
                db, app.state.secret_box, PROVIDER, {"active": active}
            )
        self.active = active
        if not active:
            await self.close()

    async def demo(self) -> ASGIApp:
        """The demo's app, started the first time it is needed."""
        async with self._lock:
            if self._demo is None:
                from myorb.app import create_app

                demo = create_app(self.settings, http_transport=self.transport)
                stack = AsyncExitStack()
                await stack.enter_async_context(demo.router.lifespan_context(demo))
                self._demo, self._stack = demo, stack
            return self._demo

    async def close(self) -> None:
        async with self._lock:
            if self._stack is not None:
                try:
                    await self._stack.aclose()
                except Exception:
                    logger.exception("Stopping the tour's demo failed")
            self._demo = self._stack = None


class _Served(Response):
    """A response that is another app's answer to the same request."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.background = None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)


async def tour_middleware(request: Request, call_next: Any) -> Response:
    """During the tour, the demo answers the signed-in user. Runs after the sign-in check."""
    tour: Tour | None = getattr(request.app.state, "tour", None)
    if (
        tour is None
        or not tour.active
        or not getattr(request.state, "authenticated", False)
        or request.url.path.startswith(OWN)
    ):
        return await call_next(request)
    return _Served(await tour.demo())


@router.post("/tour/start")
async def start(request: Request) -> Response:
    if request.app.state.tour is not None:
        await request.app.state.tour.set(request.app, True)
    return RedirectResponse("/", status_code=303)


@router.post("/tour/finish")
async def finish(request: Request) -> Response:
    """The tour's end, on purpose: on to the Get started steps, with the user's own data."""
    if request.app.state.tour is not None:
        await request.app.state.tour.set(request.app, False)
    return RedirectResponse("/integrations", status_code=303)
