"""CoreMixin, Client's constructor: build once what every part shares -- settings, credential,
Transport, journal and sink, delivery mode."""

from __future__ import annotations
import os
import socket
import threading
import uuid
import warnings  # noqa: F401 -- served by the old `probe.sdk.client` door
import weakref
from collections import deque
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any
from ..settings import settings as config_module
from ...foundation.safe_warn import safe_warn as _diagnostics

from .. import errors
from ..settings.settings import Settings, resolve
from ..session_marker import WIZARD_HINT
from ..delivery.outbox.drain.credentials import (
    CredentialSource,
    credential_fingerprint)
from ..delivery.journal.journal import Journal
from ..delivery.status_fields import StatusField
from ..delivery.outbox.drainer import export_interval_from_env, pick_drainer

from ...foundation.request_identity.surface import Surface
from ..delivery.transport.transport import Transport
from ..delivery.delivery import Delivery, _env_async_writes, _usable_journal


#: Old exporter intervals, kept for importers of the old door: on the default transport the detached
#: worker is the only sender now (D1), a token passed in code riding its spawn (R5, #2041).
_DEFAULT_EXPORT_INTERVAL_SECONDS = 2.0
_CODE_TOKEN_EXPORT_INTERVAL_S = 2.0


class CoreMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        token: str | None = None,
        ingest_token: str | None = None,
        hmac_secret: str | None = None,
        settings: Settings | None = None,
        transport: Transport | None = None,
        fail_open: bool = True,
        journal: "Journal | None" = None,
        spool_dir: str | Path | None = None,
        async_writes: bool | None = None,
        auto_drain: bool = True,
        drain_interval: float | None = None,
        redact: "Callable[[dict], dict] | bool | None" = None,
        surface: str = Surface.SDK.value,
        client_headers: Mapping[str, str] | None = None,
        attribution: str | None = None,
        raise_permanent: bool = False,
    ):
        self.settings = settings or resolve(
            base_url=base_url,
            token=token,
            ingest_token=ingest_token,
            hmac_secret=hmac_secret,
        )
        # Plan 2.7: an ambient credential (env or stored login, as `probe.init()` builds) is
        # re-read when the API refuses it; one passed in code never is (`refresh_credentials`).
        self._ambient_credentials = (
            settings is None and token is None and ingest_token is None and transport is None
        )
        #: Where a refresh may look again: "env" re-reads PROBE_TOKEN only (the stored login can be
        #: another account on a shared box), "config" this context's stored token, None never
        #: (passed in code). A PROBE_TOKEN copying the stored login IS the login
        #: (`_is_the_stored_login`), so a job that exported it survives a re-login.
        self._credential_source: str | None = None
        if self._ambient_credentials and self.settings.token:
            self._credential_source = "config"
            if os.environ.get(config_module.TOKEN_ENV) and not self._is_the_login(
                config_module.current_context_name() or None
            ):
                self._credential_source = "env"
        self._credential_lock = threading.Lock()
        self._credential_checked_at = float("-inf")
        self._credential_stale_warned = False
        #: (customer_id, user_id) of the starting credential. Looked up once, in the background,
        #: only when something that may refresh starts (heartbeat, exporter): a revoked token can
        #: no longer be asked, a refresh adopts a token only for the SAME account, and a
        #: one-request CLI command must not pay for it.
        self._credential_identity: tuple[str, str] | None = None
        self._credential_identity_started = False
        self._credential_identity_ready = threading.Event()
        #: A stored login already refused as another account's; not re-asked (`/v1/me` every 30 s) until the config changes.
        self._credential_rejected: str | None = None
        # `surface` tags requests for analytics (cli/sdk/mcp); ignored with a built `transport`, which carries its own.
        if transport is not None and client_headers:
            raise ValueError(
                "client_headers configure the default Transport; pass them to "
                "a custom Transport directly"
            )
        self.transport = transport or Transport(
            self.settings,
            surface=surface,
            client_headers=client_headers,
            attribution=attribution,
        )
        if transport is not None and attribution is not None:
            from ..delivery.transport.headers import resolve_attribution

            transport.attribution = resolve_attribution(attribution)
        self.fail_open = fail_open
        #: Default `write` ``raise_permanent``. The CLI sets it (lineage plan L14): a refusal raises
        #: and exits 1 instead of printing `null`; a failure that may still succeed is queued. Off for the SDK.
        self.raise_permanent = raise_permanent
        #: Called per write whose request failed and fell back to the outbox (``queued``) or was
        #: lost with it: `{"method", "path", "error", "queued"}`. `write()` returns None either way
        #: (as a 204 does), so without this the CLI would print `null` as success. Nothing is
        #: recorded while None (every SDK client): the delivery notices count those.
        self.on_undelivered: Callable[[dict], None] | None = None
        #: With a hook set: the last `UNDELIVERED_KEPT` of those, and the total (the deque drops the oldest).
        self.undelivered_writes: deque[dict] = deque(maxlen=self.UNDELIVERED_KEPT)
        self.undelivered_count = 0
        #: Experiment id -> its project as last placed (`_experiment_home`); a 404/410 re-places it.
        self._experiment_homes: dict[str, str] = {}
        # One queue (eng review 2026-07-29, T1-C): the journal holds async writes and the sync
        # fail-open net that used to be the spool; `spool_dir` is its directory override.
        # Async is the DEFAULT (ProSeCo, 2026-08-19): a sync write puts the network on the training
        # loop's critical path. `None` = "nobody asked", so the credential gate below degrades to
        # sync; an explicit True still raises.
        # `_async_requested` is the ARGUMENT only, captured BEFORE the environment is folded in:
        # otherwise a stray exported `PROBE_ASYNC=1` read as an explicit request, skipped the
        # transport gate and built an async client with no drainer or credential guard, journaling
        # writes nothing would deliver. The environment steers the default, never the invariants.
        async_writes = self._resolve_async_writes(async_writes, transport=transport)
        self.async_writes = async_writes
        # The write pipeline and its sinks; the sink follows `async_writes` (`Delivery.sink`).
        self._delivery_pipeline = Delivery(self)
        #: Writes ACCEPTED then dropped because the outbox could not be written (ENOSPC, read-only
        #: state dir, flock ENOSYS). `_enqueue`'s bool is discarded by `write()`, so without this a
        #: caller cannot tell "queued" from "lost". Monotonic, THIS process only; snapshot around a write.
        self.dropped_writes = 0
        #: Writes sent straight to the server: outbox volume under its free-space floor, nothing queued (plan 1.5). Reported at `finish()`.
        self.direct_sends = 0
        #: Requests set aside by `discard_delivery` before delivery; reported as `discarded`.
        self._discarded_requests = 0
        self._direct_closed_until = float("-inf")
        self._direct_failures = 0
        self._direct_lock = threading.Lock()
        self._lanes: dict[str, Any] = {}
        if journal is not None and spool_dir is not None:
            raise ValueError("pass journal or spool_dir, not both")
        self.journal = journal or _usable_journal(
            Path(spool_dir).expanduser() if spool_dir else None
        )
        self.journal.attribution = str(getattr(self.transport, "attribution", "ambient"))
        #: Fingerprints of every credential this client wrote with; an op stamped otherwise is not its to replay (#2035).
        self._credential_fingerprints: set[str] = set()
        mine = credential_fingerprint(self.settings.token, self.settings.ingest_token)
        if mine:
            self._credential_fingerprints.add(mine)
        #: Same, for the ingest token `/ingest` writes use.
        self._ingest_fingerprints: set[str] = set()
        mine_ingest = credential_fingerprint(None, self.settings.ingest_token)
        if mine_ingest:
            self._ingest_fingerprints.add(mine_ingest)
        stamp = self._bind_journal_context(journal=journal, surface=surface)
        # After the queue is settled (#2041): the notices' baseline reads the queue this client writes to.
        self._init_delivery_notices()
        # Never a run's code, reads or outputs, wherever it is (even an explicit `spool_dir`).
        from ..capture import owndirs

        owndirs.note(self.journal.outbox_root)
        # D1: on the default transport the detached outbox worker is the only sender of queued
        # writes (`miles-parity.md` F1); ``drain_interval`` / PROBE_EXPORT_INTERVAL_SEC only cap its
        # collect window, so a writer that asked for delivery every N seconds gets it (review of
        # #3785, I18). The in-process exporter (F2) stays for an injected transport, which no worker
        # can replay. Never the env for a queue only `probe sync` drains.
        if drain_interval is None and async_writes and not self._drains_by_hand:
            drain_interval = export_interval_from_env()
        named_interval = drain_interval
        self._drain_interval = drain_interval if (async_writes and transport is not None) else None
        if named_interval is not None and async_writes:
            self.journal.window_cap = float(named_interval)
        #: A token passed in code is in no env or config: the worker gets it at spawn, in its own
        #: environment only (R5; #2041: 0 of 5 delivered when nothing could hold it).
        self._worker_credentials: dict | None = None
        if (
            async_writes
            and transport is None
            and isinstance(stamp, dict)
            and stamp.get("source") == CredentialSource.CODE
        ):
            # With its server: the worker matches an env credential only for writes pinned to the
            # server its own env names (`credentials._settings_for_op`).
            self._worker_credentials = {
                name: value
                for name, value in (
                    (config_module.TOKEN_ENV, self.settings.token),
                    ("PROBE_INGEST_TOKEN", self.settings.ingest_token),
                    (config_module.BASE_URL_ENV, self.settings.base_url),
                )
                if value
            }
        self._exporter = None
        self._exporter_lock = threading.Lock()
        # A worker fork suits default-transport clients only, but a FORCED kick (deferred finish, F3) works from sync ones too.
        self._default_transport = transport is None
        auto_drain = self._ensure_async_drainer(
            async_writes=async_writes, auto_drain=auto_drain, transport=transport,
        )
        # Producer accounting (parity F4): long-lived writers get a per-process id; the CLI shares
        # one per-host id, so thousands of `probe --async log` calls are ONE producer line (sequences
        # stay safe: allocation reads the registry under the append lock).
        # Parity F5: scrub payloads at CAPTURE, before the journal (often shared storage) or wire.
        # True = the standard scrubber, a callable = your own, None = untouched.
        if redact is True:
            from ..redaction import default_scrub

            self._redact: Callable | None = default_scrub
        else:
            self._redact = redact or None
        self._seal_producer_on_close = False
        if async_writes:
            host = socket.gethostname()
            if surface == Surface.CLI.value:
                producer_id = f"cli:{host}"
            else:
                producer_id = f"{surface}:{host}:{os.getpid()}:{uuid.uuid4().hex[:8]}"
                self._seal_producer_on_close = True
            # The per-host CLI id suits a training loop but merges concurrent CLI writers (several
            # importers) into one line. Let the caller name them (`PROBE_OUTBOX_PRODUCER_ID=import:shard-3`).
            # Id-only: seal-on-close stays with the SURFACE, so the first process to exit does not
            # close a shared line under live siblings.
            override = (os.environ.get("PROBE_OUTBOX_PRODUCER_ID") or "").strip()
            if override:
                producer_id = override
            try:
                self.journal.register_producer(producer_id, role=surface)
            except Exception:  # noqa: BLE001 -- accounting must never block writes
                pass
        self._auto_drain = (
            async_writes and auto_drain and transport is None and self._drain_interval is None
        )
        # Explicit receipt enqueue is async even when ordinary entity writes are sync.
        self._delivery_auto_drain = auto_drain
        # Who delivers this client's queue, picked ONCE (the service, a thread or none).
        self._drainer = pick_drainer(self)
        # Plan D9: a training process's service starts now, off this thread, so its first drain,
        # relay or hash (a SIGTERM's close included) finds it up. D21: a key passed in code too.
        if self._default_transport and surface == Surface.SDK.value:
            from ...foundation.service_api import handoff

            if not handoff.is_under_service():
                handoff.start_soon(self.settings.base_url)
        self._hand_key_to_service(should_wait=False)
        if (
            async_writes
            and transport is None
            and (auto_drain or self._drain_interval is not None)
            and not (self.settings.token or self.settings.ingest_token)
        ):
            # F7: an op nothing can deliver would fail hours later in the drainer log.
            raise errors.ValidationError(
                f"async_writes needs deliverable credentials: {WIZARD_HINT} "
                "or set PROBE_TOKEN -- or pass auto_drain=False to queue "
                "offline and deliver later via flush()/`probe outbox drain`"
            )
        self._events = None
        # Stop signals for this client's live run-heartbeat threads; weak so finished beats do not pile up.
        self._run_heartbeat_stops: weakref.WeakSet[threading.Event] = weakref.WeakSet()
        # 2.3: a close killed mid-barrier by a relaunch and held aside goes back in the queue now,
        # in any delivery mode (one stat if none); the kick below delivers it.
        try:
            self._restore_abandoned_holds()
        except Exception:  # noqa: BLE001 -- a hold left in place is the old behaviour
            pass
        self._kick_waiting_queues(async_writes=async_writes, auto_drain=auto_drain)

    def _resolve_async_writes(self, async_writes, *, transport):
        """Pick sync or async writes: the argument, then PROBE_ASYNC, then async, degraded where nothing
        could drain. Returns async_writes."""
        self._async_requested = async_writes
        if async_writes is None:
            # PROBE_ASYNC is an SDK knob too: a campaign could not change write mode without editing the training script.
            async_writes = _env_async_writes()
        if async_writes is None:
            async_writes = True
        if async_writes and transport is not None and self._async_requested is not True:
            # Async needs the DEFAULT transport (the detached worker cannot replay an injected one, F1).
            # Injecting callers (hosted MCP, fake-transport tests) stay synchronous; an explicit
            # async_writes=True still opts in via the in-process exporter (F2).
            async_writes = False
        if (
            async_writes
            and self._async_requested is not True
            and transport is None
            and not (self.settings.token or self.settings.ingest_token)
        ):
            # Nothing could drain this journal and async was not asked for: use the path that works. Explicit True still raises (F7).
            async_writes = False
        return async_writes

    def _bind_journal_context(self, *, journal, surface):
        """Bind the journal to the active context when it has none. Returns the context's credential
        stamp."""
        stamp = None
        if self.journal.context is None:
            name = config_module.current_context_name() or None
            self.journal.context = {"name": name, "base_url": self.settings.base_url}
            stamp = self._credential_stamp(name)
            if stamp is not None:
                self.journal.context["principal"] = stamp
                if (
                    self.async_writes
                    and stamp["source"] in (CredentialSource.ENV, CredentialSource.CODE)
                    and not os.environ.get("PROBE_OUTBOX_WORKER")
                    and surface != Surface.CLI.value  # one command: gone in a moment
                ):
                    # Who holds a credential only it can send with, for `probe outbox status`.
                    from ..delivery.outbox.drain.holders import record_holder

                    record_holder(stamp["fingerprint"])
                if (
                    journal is None
                    and stamp["source"] in (CredentialSource.ENV, CredentialSource.CODE)
                    and not self._is_the_stored_login(name)
                ):
                    # Own queue (journal.CREDENTIAL_NAMESPACE): no release before the stamp can send
                    # these as the stored login or stall on them, and this worker never waits behind
                    # another's (#2041). The stored login's writes stay in the shared queue.
                    self.journal = Journal.for_credential(
                        self.journal.dir,
                        self._credential_queue_name(stamp),
                        context=self.journal.context,
                        attribution=self.journal.attribution,
                    )
        return stamp

    def _ensure_async_drainer(self, *, async_writes, auto_drain, transport):
        """Async writes need a drainer: the detached worker or the in-process exporter. Returns
        auto_drain (switched on when async was not asked for)."""
        # Async REQUIRES a drainer, and each of the two (parity F1/F2) has a precondition: the
        # detached worker needs the default transport, the in-process exporter a drain_interval.
        # Three reachable configurations journaled every write with nothing to deliver it, silently
        # (a queued write returns None like a delivered one). Each branch below picks the mechanism
        # that CAN work for its shape.
        if (
            async_writes
            and self._drain_interval is None
            and not (auto_drain and self._default_transport)
        ):
            if transport is not None and self._drains_by_hand:
                pass
            elif transport is not None:
                # F1 is out (the worker cannot replay an injected transport) and F2 needs an
                # interval nobody named. Draining by hand via `flush()`/`finish()` is valid (CLI
                # barrier, fake-transport tests); a forced exporter would race their assertions.
                # So warn once and leave the choice: the silence was the bug, not the setup.
                _diagnostics.warn(
                    "probe: async writes with a custom transport have no "
                    "background drainer — the detached worker cannot replay an "
                    "injected transport. Pass drain_interval=<seconds> for the "
                    "in-process exporter, or call flush()/finish() yourself; "
                    "otherwise queued writes stay on disk."
                )
            elif self._async_requested is None:
                # Async not asked for, auto_drain=False: the detached worker still sends (D1), rather
                # than degrade to sync, which would put the network back on the training loop
                # (before async became the default, auto_drain=False only meant "no auto-drain of
                # the fail-open spool").
                auto_drain = True
            else:
                # Explicit async AND no drainer: warn, do not refuse. Real for hand-draining writers and
                # tests inspecting a journal; the defect was a silent queue looking like delivery.
                _diagnostics.warn(
                    "probe: async writes with auto_drain=False have no "
                    "background drainer. Call flush() yourself, or leave "
                    "auto_drain on for the background worker; otherwise queued "
                    "writes stay on disk."
                )
        return auto_drain

    def _kick_waiting_queues(self, *, async_writes, auto_drain):
        """Deliver a queue an earlier process left behind, in this client's queue and the shared one."""
        if self._auto_drain:
            # A queue left by an earlier process (pod on the same volume, laptop after sleep) drains
            # now, not at the first write (plan 1.5). One status read; only a non-empty queue is kicked.
            try:
                waiting = Journal.read_status(self.journal.dir) or {}
                if int(waiting.get(StatusField.PENDING) or 0) or int(waiting.get(StatusField.WAITING) or 0):
                    self._kick_drainer()
            except Exception:  # noqa: BLE001 -- a kick is latency, never a gate
                pass
        if async_writes and auto_drain and self._default_transport:
            try:
                root = self.journal.outbox_root
                if root != self.journal.dir:
                    # This client queues in its credential's own queue (#2035) and may deliver it
                    # in-process; the shared queue's backlog is the shared worker's, which any process may start.
                    shared = Journal.read_status(root, credential_queues=False) or {}
                    if int(shared.get(StatusField.PENDING) or 0) or int(shared.get(StatusField.WAITING) or 0):
                        from ..delivery import outbox as outbox_worker

                        # Asked on a thread: a start of the service is never the training loop's wait.
                        threading.Thread(
                            target=outbox_worker.maybe_spawn, args=(str(root),), name="probe-outbox-ask", daemon=True,
                        ).start()
            except Exception:  # noqa: BLE001 -- a kick is latency, never a gate
                pass
