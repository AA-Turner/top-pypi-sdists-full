"""SdkMethods: the methods a training process's SDK asks of a Probe service (plan D8-D11, D20, D21):
`outbox.drain`, `box.watch`, `telemetry.send`, `api.call`, `files.hash`, `credentials.hold`. One copy
(plan D28): the delivery service (`service.py`) and the machine service
(`service/server/handlers/background.py`) both serve these."""

from __future__ import annotations

import asyncio
import concurrent.futures
import threading
import time
from collections.abc import Awaitable, Callable

from probe.foundation.service_api.env import CALLER_FENCED_ENV, drop_fence_endpoint_names, is_fence_endpoint_name
from probe.foundation.service_api.params import need_background, need_telemetry
from probe.foundation.service_api.vocabularies import BackgroundRefusal
from probe.foundation.service_api.wire import API_PROGRESS_TOPIC, Method, event

from . import callers
from .background.background import BackgroundHost
from .connection import Connection

#: `outbox.drain` / `box.watch` checks and child starts (a stat, a fork) on their own threads, at
#: most this many taken in at once, and what a caller is answered within.
BACKGROUND_THREADS = 2
MAX_PENDING_BACKGROUND = 8
BACKGROUND_WAIT_S = 2.0
#: `files.hash`: what its answer may take past the job's own deadline (a queue and a child's start).
HASH_ANSWER_MARGIN_S = 30.0
#: The variable whose address the stored login follows (`settings.resolve`, plan D10).
BASE_URL_ENV = "PROBE_BASE_URL"
#: The keys a drain sends with (`settings.resolve`): only these make a request "bring its own".
OWN_KEYS = ("PROBE_TOKEN", "PROBE_INGEST_TOKEN")
#: The methods `SdkMethods` answers.
SDK_METHODS = frozenset({
    Method.OUTBOX_DRAIN, Method.BOX_WATCH, Method.TELEMETRY_SEND, Method.API_CALL, Method.FILES_HASH,
    Method.CREDENTIALS_HOLD,
})


class SdkMethods:
    """The SDK's methods over one service's background host, relay and hashing pool. `is_fenced(pid)`
    decides whether a caller reaches only the API and its storage (plan D25)."""

    def __init__(
        self, *, log: Callable[[str], None], is_fenced: Callable[[int | None], bool] = callers.is_confined,
        incident: Callable[..., None] = lambda *args, **kwargs: None, consent_names: tuple = (),
    ) -> None:
        self.log = log
        self.is_fenced = is_fenced
        #: Drainer and box watcher children, client telemetry (plan Q5).
        self.background = BackgroundHost(log=log, incident=incident, consent_names=consent_names)
        #: `api.call` (plan D10) and `files.hash` (D20, D24): built at their first request.
        self._relay = None
        self._hashing = None
        self._lock = threading.Lock()
        self._starts: concurrent.futures.ThreadPoolExecutor | None = None
        self._slots = threading.BoundedSemaphore(MAX_PENDING_BACKGROUND)
        #: The service is on its way out: no drain or watcher starts.
        self.is_stopping = False

    def get_handlers(self) -> dict[str, Callable[[Connection, dict], Awaitable[dict]]]:
        return {
            Method.OUTBOX_DRAIN: self.drain_outbox,
            Method.BOX_WATCH: self.watch_box,
            Method.TELEMETRY_SEND: self.send_telemetry,
            Method.API_CALL: self.call_api,
            Method.FILES_HASH: self.hash_files,
            Method.CREDENTIALS_HOLD: self.hold_credentials,
        }

    @property
    def relay(self):
        """`api.call`'s HTTP sender, built at the first request (off the service's start path)."""
        with self._lock:
            if self._relay is None:
                from .relay import Relay  # noqa: PLC0415 -- off the start path

                self._relay = Relay(log=self.log)
            return self._relay

    @property
    def hashing(self):
        """`files.hash`'s niced children, built at the first request."""
        with self._lock:
            if self._hashing is None:
                from .hashing import HashPool  # noqa: PLC0415 -- off the start path

                self._hashing = HashPool(log=self.log)
            return self._hashing

    # -- the methods ------------------------------------------------------------------------

    async def drain_outbox(self, connection: Connection, parameters: dict) -> dict:
        """`outbox.drain` (plan D8): this service's own drain of the outbox folder `dir`, as its
        child. `{accepted: true, state}` (started, or a drain of it runs), else `{accepted: false,
        reason}`: the journal waits for the next ask."""
        return await self.start_background(
            connection, _strip_service_marks(need_background(parameters, directory=True)), self.background.drain)

    async def watch_box(self, connection: Connection, parameters: dict) -> dict:
        """`box.watch` (plan Q5): this box's watcher (`probe.sdk.run.watcher`), likewise."""
        return await self.start_background(
            connection, _strip_service_marks(need_background(parameters, directory=False)),
            self.background.watch_box)

    async def send_telemetry(self, connection: Connection, parameters: dict) -> dict:
        """`telemetry.send` (plan D10): one batch the caller built, POSTed from the service's
        telemetry thread, the only way a client's telemetry goes out."""
        entries, batch_id = need_telemetry(parameters)
        return self.background.send_telemetry(entries, batch_id)

    async def hold_credentials(self, connection: Connection, parameters: dict) -> dict:
        """`credentials.hold` (plan D21): an in-code key, held in memory for its queue's drains
        (`{fingerprint, env}`); `{held: true}`. Checked on a thread (the fingerprint's hash)."""
        from .background.credentials import need_credentials

        fingerprint, env = await asyncio.to_thread(need_credentials, parameters)
        url = env.get("PROBE_BASE_URL")
        if url and await asyncio.to_thread(self._check_fenced, connection.peer_pid) \
                and not await asyncio.to_thread(callers.is_known_endpoint, url, {}):
            # A fenced caller's key goes only where this machine's config sends its own (D26, M1): a
            # key it read from that config, held with an address of its own, would leave the fence.
            from probe.foundation.service_api.wire import invalid_params

            raise invalid_params("a sandboxed caller may hold a key only for this machine's Probe server")
        self.background.credentials.hold(fingerprint, env)
        return {"held": True}

    async def call_api(self, connection: Connection, parameters: dict) -> dict:
        """`api.call` (plan D10): send the HTTP request a training process packaged, on the relay's
        own threads, and answer with the response. A fenced caller reaches only the API and its
        storage (D25). While a body streams into the caller's file, `api.progress` events keep it
        waiting; a caller gone stops the stream."""
        from .relay import need_api_call

        call = need_api_call(parameters, connection.take_fds())
        call.is_fenced = await asyncio.to_thread(self._check_fenced, connection.peer_pid)
        if call.is_fenced:
            call.env = {**drop_fence_endpoint_names(call.env), **get_network_env()}  # H-2: this service's own
        loop = asyncio.get_running_loop()
        request_id = connection.request_id

        def report_progress(done: int) -> bool:
            if connection.is_gone():
                return False
            message = event(API_PROGRESS_TOPIC, {"id": request_id, "bytes": done})
            loop.call_soon_threadsafe(connection.send_nowait, message)
            return True

        return await asyncio.wrap_future(self.relay.submit(call, report_progress))

    async def hash_files(self, connection: Connection, parameters: dict) -> dict:
        """`files.hash` (plan D20, D24): hash the files a training process opened, in this service's
        niced hashing children (at most 2 a machine, the rest queued), within the job's own deadline
        and a margin for its answer."""
        from .hashing import need_files_hash

        job = need_files_hash(parameters, connection.take_fds())
        wait = max(0.0, job.deadline - time.monotonic()) + HASH_ANSWER_MARGIN_S
        try:
            return await asyncio.wait_for(asyncio.wrap_future(self.hashing.submit(job)), wait)
        except (asyncio.TimeoutError, TimeoutError):
            return {"expired": True}

    # -- the service's view ---------------------------------------------------------------------

    def public(self) -> dict:
        """`service.status`'s parts: the background host's, the relay's and the hashing pool's."""
        return {
            "background": self.background.public(),
            "relay": self._relay.public() if self._relay is not None else None,
            "hashing": self._hashing.public() if self._hashing is not None else None,
        }

    def count_in_flight(self) -> int:
        """`api.call`s and `files.hash` jobs taken and not answered, and telemetry batches queued."""
        count = self.background.public()["telemetry"]["queued"]
        if self._relay is not None:
            count += self._relay.count_in_flight()
        if self._hashing is not None:
            count += self._hashing.count_in_flight()
        return count

    def close(self, flush_s: float = 0.0) -> None:
        """No new work; the telemetry taken is sent for up to `flush_s`. Blocks: call it on a thread."""
        self.is_stopping = True
        if self._starts is not None:
            self._starts.shutdown(wait=False, cancel_futures=True)
        for part in (self._relay, self._hashing):
            if part is not None:
                try:
                    part.close()
                except Exception:  # noqa: BLE001 -- the callers fail open
                    pass
        self.background.close(flush_s)

    # -- inside ---------------------------------------------------------------------------------

    def _check_fenced(self, pid: int | None) -> bool:
        try:
            return self.is_fenced(pid)
        except Exception:  # noqa: BLE001 -- unknown counts as fenced
            return True

    async def start_background(self, connection: Connection, request: dict, start: Callable[[dict], dict]) -> dict:
        """`start(request)` on a thread. A fenced caller's endpoint settings are dropped first (H-2:
        the child uses this service's own). Refused when its `PROBE_BASE_URL` is one the stored login
        may not go to and it brings no key of its own (D10, D26: the stored login follows that
        variable). An answer not ready within BACKGROUND_WAIT_S reads `busy`; the start still
        completes, and the next ask meets its lease."""
        if self.is_stopping:
            return {"accepted": False, "reason": BackgroundRefusal.STOPPING}
        pid = connection.peer_pid
        if request["env"].get(CALLER_FENCED_ENV) != "1" and await asyncio.to_thread(self._check_fenced, pid):
            # D31: a sandboxed caller's drain or box watch is not served in this release (its journal
            # waits; `finish()` names `probe outbox drain` from an unsandboxed shell). A request the
            # machine service already fenced (`CALLER_FENCED_ENV`, its own) is its own.
            return {"accepted": False, "reason": BackgroundRefusal.SANDBOXED}

        def run_checked() -> dict:
            try:
                checked = request
                if request["env"].get(CALLER_FENCED_ENV) != "1" and self._check_fenced(pid):
                    checked = {**request, "env": {**drop_fence_endpoint_names(request["env"]), **get_network_env()}}
                if not has_own_key(checked["env"]) and not is_base_url_allowed(checked["env"]):
                    return {"accepted": False, "reason": BackgroundRefusal.UNKNOWN_ENDPOINT}
                return start(checked)
            finally:
                self._slots.release()

        if not self._slots.acquire(blocking=False):
            return {"accepted": False, "reason": BackgroundRefusal.BUSY}
        with self._lock:
            if self._starts is None:
                self._starts = concurrent.futures.ThreadPoolExecutor(BACKGROUND_THREADS,
                                                                      thread_name_prefix="probe-background")
        try:
            future = asyncio.get_running_loop().run_in_executor(self._starts, run_checked)
        except RuntimeError:  # shut down meanwhile
            self._slots.release()
            return {"accepted": False, "reason": BackgroundRefusal.STOPPING}
        try:
            return await asyncio.wait_for(asyncio.shield(future), BACKGROUND_WAIT_S)
        except (asyncio.TimeoutError, TimeoutError):
            return {"accepted": False, "reason": BackgroundRefusal.BUSY}


def has_own_key(env: dict) -> bool:
    """The request brings a key of its own, which its drain sends instead of the stored login
    (a stored key never goes to an address it was not stored for, D26)."""
    return any(env.get(name) for name in OWN_KEYS)


def is_base_url_allowed(env: dict) -> bool:
    """May a drainer run with `env`'s PROBE_BASE_URL (plan D10: the stored login follows it)?
    Unset, or https and an endpoint that login may go to (`callers.is_known_endpoint`). Blocking
    (reads the CLI config): a thread."""
    url = env.get(BASE_URL_ENV) or None  # empty is unset, as `config.resolve` reads it
    return url is None or (url.startswith("https://") and callers.is_known_endpoint(url, env))


def get_network_env() -> dict:
    """This service's own proxies, CA files, config path and API (`env.is_fence_endpoint_name`): what
    a fenced caller's call or child uses instead of the caller's (H-2). A delivery service has them
    from the SDK that started it (`handoff.ensure_service`'s starter env); a machine service from
    its own start."""
    import os

    return {name: value for name, value in os.environ.items() if is_fence_endpoint_name(name)}


def _strip_service_marks(request: dict) -> dict:
    """A caller's request with no mark only a service sets (`CALLER_FENCED_ENV`: a request the machine
    service already fenced, handed to `start_background` by its own handler): a caller can never say
    it was fenced already and skip the sandbox refusal or the network-settings rule (#4287 review)."""
    return {**request, "env": {name: value for name, value in request["env"].items() if name != CALLER_FENCED_ENV}}
