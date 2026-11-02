"""OfflineClient: an async client over the offline run's own queue, drained only by `probe sync`;
its transport refuses every socket."""

from __future__ import annotations
from typing import Any

import httpx

from ... import errors
from ...client.client import Client
from ...settings.settings import Settings
from ..journal.journal import Journal
from ..transport.transport import Transport
from .lineage import LINEAGE_ROUTES


# -- no network, by construction ----------------------------------------------
class OfflineTransport(Transport):
    """A transport that refuses every request without touching a socket. The run's writes
    are journaled (async client), so only fail-open paths that would go to the network reach
    here (a sync write, a read, a feature probe): each fails at once with a TransportError
    (no retry, no sleep) and its fallback journals or skips. The httpx client is a
    MockTransport that raises too, so even a path bypassing these methods cannot send."""

    def __init__(self, settings: Settings):
        from ....foundation.tls.tls import ssl_context

        http = httpx.Client(
            base_url=settings.base_url or "http://offline.invalid",
            transport=httpx.MockTransport(self._refuse),
            # Never used (nothing is sent), but every client in the package
            # carries the one shared trust (plan item l).
            verify=ssl_context(),
        )
        super().__init__(settings, client=http, max_retries=0)
        #: How many requests were refused -- evidence for tests and doctor.
        self.refused = 0

    @staticmethod
    def _refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("offline mode: no network", request=request)

    def _offline(self, what: str) -> errors.TransportError:
        self.refused += 1
        refused = errors.TransportError(
            f"{what}: not sent -- this run is offline (PROBE_MODE=offline); "
            "`probe sync` delivers it later"
        )
        refused.offline = True
        return refused

    def request(self, method: str, path: str, **_kw: Any) -> httpx.Response:
        raise self._offline(f"{method} {path}")

    def put_url(self, url: str, *_a: Any, **_kw: Any) -> None:
        raise self._offline("PUT <blob>")

    def put_file(self, url: str, *_a: Any, **_kw: Any) -> None:
        raise self._offline("PUT <blob>")

    def put_fileobj(self, url: str, *_a: Any, **_kw: Any) -> None:
        raise self._offline("PUT <blob>")

    def get_url(self, url: str) -> bytes:
        raise self._offline("GET <blob>")

    def download_to(self, url: str, dest: str, **_kw: Any) -> tuple[int, str]:
        raise self._offline("GET <blob>")


class OfflineClient(Client):
    """The client behind an offline run: an async client, so its writes land in `QueuedSink`, whose
    journal is the run's own queue (`<outbox>/offline/<creation_key>/`); no drainer, no worker, no
    feature probes."""

    #: `probe sync` is this client's drainer: no "no background drainer" notice, no delivery
    #: notices or reports, no low-disk send around the queue (each reads this flag). A class
    #: attribute, not a `warnings` filter (process-wide, not thread-safe, hides other threads').
    _drains_by_hand = True

    def __init__(self, settings: Settings, journal: Journal):
        # Nothing drains this queue before `probe sync`, so the stalled-drainer op ceiling
        # would only drop a long run's tail and close (`Journal.op_ceiling`). The free-space
        # floor still applies.
        journal.op_ceiling = 0
        super().__init__(
            settings=settings,
            transport=OfflineTransport(settings),
            journal=journal,
            async_writes=True,
            auto_drain=False,
        )

    #: Features whose writes an offline run QUEUES instead of asking about: the server that
    #: decides is the one `probe sync` delivers to, and `sync_dir` checks it there (and says
    #: so when it lacks one). Asking now would be a request; every other feature reads as
    #: unsupported offline.
    DEFERRED_FEATURES = frozenset({"run_config_merge", *LINEAGE_ROUTES})

    def supports_feature(self, name: str) -> bool:
        return name in self.DEFERRED_FEATURES
