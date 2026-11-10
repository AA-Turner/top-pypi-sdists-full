"""Route: one rollout's way through the proxy (its 128-bit secret, attempt key, upstream and the producer it writes
through), and the table of them. The secret in the URL is the only key: one sandbox cannot reach another's record."""

from __future__ import annotations

import secrets
import threading
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...samples import RunSamples
    from .dialect import Dialect

#: 16 random bytes: a 128-bit secret per rollout.
SECRET_BYTES = 16
#: Routes remembered at once; the oldest ended ones are forgotten first.
ROUTES_REMEMBERED = 100_000
#: A request body kept for a watch's first snapshot at most (a bigger one is forwarded, not kept).
MAX_KEPT_REQUEST_BYTES = 2 * 1024 * 1024
#: Request bodies kept across all routes at most; past it the oldest kept one is let go (memory, never training's).
MAX_KEPT_REQUESTS_BYTES = 256 * 1024 * 1024


@dataclass(eq=False)
class Route:
    """Flags are set from other threads (`is_canceled` by a cancel, `is_ended` by `attempt_end`); `calls` is the
    event loop's; the rest is the observer thread's."""

    secret: str
    attempt_key: str
    upstream: str
    samples: RunSamples
    is_canceled: bool = False
    is_ended: bool = False
    calls: set = field(default_factory=set)
    #: The newest model call's (dialect, request body), for a watch's first snapshot (None when too big to keep).
    last_request: tuple[Dialect, bytes] | None = None
    # -- the observer thread's -------------------------------------------------------------------
    calls_started: int = 0
    calls_done: int = 0
    tokens: int = 0
    #: Request history items already sent as turns while watched; None: no watch is being fed.
    covered: int | None = None
    #: The last finished call's request body and reply turns (its reply joins the next snapshot).
    replied: tuple[bytes, list[dict], int] | None = None

    def make_target(self, api_path: str, query: str) -> str:
        """The upstream URL for a call to ``api_path`` (after our `/r/<secret>`; one or two leading `/v1` are ours:
        the OpenAI SDK adds none to its base URL, the Anthropic SDK one more)."""
        for _ in range(2):
            if api_path == "/v1" or api_path.startswith("/v1/"):
                api_path = api_path[3:]
        return self.upstream.rstrip("/") + api_path + (f"?{query}" if query else "")


class RouteTable:
    """Thread-safe: rollouts open routes from the trainer's threads, the event loop reads them by secret."""

    def __init__(self, limit: int = ROUTES_REMEMBERED) -> None:
        self._by_secret: dict[str, Route] = {}
        self._by_key: dict[str, Route] = {}
        self._limit = limit
        self._lock = threading.Lock()
        #: Routes holding a request body, oldest first, and its size.
        self._kept: OrderedDict[str, int] = OrderedDict()
        self._kept_bytes = 0

    def open(self, samples: RunSamples, attempt_key: str, upstream: str) -> Route:
        """The rollout's route: the same one again for the same key and upstream while it runs, else a new one."""
        with self._lock:
            found = self._by_key.get(attempt_key)
            if found is not None and not found.is_ended and found.upstream == upstream and found.samples is samples:
                return found
            route = Route(secrets.token_urlsafe(SECRET_BYTES), attempt_key, upstream, samples)
            self._by_secret[route.secret] = route
            self._by_key[attempt_key] = route
            self._forget_oldest()
            return route

    def keep_request(self, route: Route, dialect: Dialect, body: bytes) -> None:
        """Keep the route's newest model call for a watch's first snapshot, within the byte budgets."""
        with self._lock:
            self._release_request(route)
            if route.is_ended or len(body) > MAX_KEPT_REQUEST_BYTES:
                return
            route.last_request = (dialect, body)
            self._kept[route.secret] = len(body)
            self._kept_bytes += len(body)
            while self._kept_bytes > MAX_KEPT_REQUESTS_BYTES:
                secret, size = self._kept.popitem(last=False)
                self._kept_bytes -= size
                oldest = self._by_secret.get(secret)
                if oldest is not None:
                    oldest.last_request = None

    def get(self, secret: str) -> Route | None:
        return self._by_secret.get(secret)

    def find(self, attempt_key: str) -> Route | None:
        return self._by_key.get(attempt_key)

    def end(self, attempt_key: str) -> Route | None:
        """The rollout ended: late calls still forward, nothing more is recorded for it."""
        with self._lock:
            route = self._by_key.get(attempt_key)
            if route is not None:
                route.is_ended = True
                self._release_request(route)
        return route

    def get_live(self) -> list[Route]:
        """Routes whose rollout has not ended."""
        with self._lock:
            return [route for route in self._by_key.values() if not route.is_ended]

    def _forget_oldest(self) -> None:
        while len(self._by_secret) > self._limit:
            oldest = next((route for route in self._by_secret.values() if route.is_ended),
                          next(iter(self._by_secret.values())))  # fmt: skip
            self._by_secret.pop(oldest.secret, None)
            self._release_request(oldest)
            if self._by_key.get(oldest.attempt_key) is oldest:
                self._by_key.pop(oldest.attempt_key, None)

    def _release_request(self, route: Route) -> None:
        """Under the lock: the route no longer holds a request body."""
        size = self._kept.pop(route.secret, None)
        if size is not None:
            self._kept_bytes -= size
        route.last_request = None
