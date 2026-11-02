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
from ..delivery.outbox.drainer import export_interval_from_env, pick_drainer

from ...foundation.request_identity.surface import Surface
from ..delivery.transport.transport import Transport
from ..delivery.delivery import Delivery, _env_async_writes, _usable_journal


#: Fallback poll interval for the in-process exporter (F2), seconds. An enqueue wakes the
#: exporter anyway: this is the idle re-check, not a write's delivery delay.
_DEFAULT_EXPORT_INTERVAL_SECONDS = 2.0


#: Exporter interval (s) for a token passed in code, which the detached worker cannot hold (#2041).
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
        # After the queue is settled (#2041): the notices' baseline reads the queue this client writes to.
        self._init_delivery_notices()
        # Never a run's code, reads or outputs, wherever it is (even an explicit `spool_dir`).
        from ..capture import owndirs

        owndirs.note(self.journal.outbox_root)
        # Parity F1/F2 (docs/2026-08-04-outbox-miles-parity.md): an async enqueue wakes a drainer.
        # Default (F1): the detached outbox worker, default-transport clients only (it resolves its
        # own transport). With ``drain_interval`` or PROBE_EXPORT_INTERVAL_SEC (F2): an in-process
        # exporter delivers through THIS client: fork-free, works with any transport. Never the env
        # for a queue only `probe sync` drains: its exporter would send through a transport that
        # refuses everything, and each refusal counts toward dead-lettering the run's writes.
        if drain_interval is None and async_writes and not self._drains_by_hand:
            drain_interval = export_interval_from_env()
        # Named by the caller (argument or env), not a default below: it caps the collect window,
        # so a writer that asked for delivery every N seconds gets it (review of #3785, I18).
        named_interval = drain_interval
        if (
            drain_interval is None
            and async_writes
            and auto_drain
            and transport is None
            and isinstance(stamp, dict)
            and stamp.get("source") == CredentialSource.CODE
        ):
            # A code token is in no env or config, so the detached worker cannot hold it: deliver
            # in-process or writes wait for flush()/finish() (#2041: 0 of 5 delivered, stranded at exit).
            drain_interval = _CODE_TOKEN_EXPORT_INTERVAL_S
        self._drain_interval = drain_interval if async_writes else None
        if named_interval is not None and self._drain_interval is not None:
            self.journal.window_cap = float(named_interval)
        self._exporter = None
        self._exporter_lock = threading.Lock()
        # A worker fork suits default-transport clients only, but a FORCED kick (deferred finish, F3) works from sync ones too.
        self._default_transport = transport is None
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
                # Async not asked for and auto_drain=False rules out the worker, but the DEFAULT
                # transport allows F2. Take it rather than degrade to sync, which would silently put
                # the network back on the training loop (before async became the default,
                # auto_drain=False only meant "no auto-drain of the fail-open spool"). Delivery
                # stays guaranteed; only the crash-surviving subprocess is lost.
                self._drain_interval = _DEFAULT_EXPORT_INTERVAL_SECONDS
            else:
                # Explicit async AND no drainer: warn, do not refuse. Real for hand-draining writers and
                # tests inspecting a journal; the defect was a silent queue looking like delivery.
                _diagnostics.warn(
                    "probe: async writes with auto_drain=False have no "
                    "background drainer. Pass drain_interval=<seconds> for the "
                    "in-process exporter, or call flush()/finish() yourself; "
                    "otherwise queued writes stay on disk."
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
        # Who delivers this client's queue, picked ONCE (worker, thread or none).
        self._drainer = pick_drainer(self)
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
        if self._auto_drain:
            # A queue left by an earlier process (pod on the same volume, laptop after sleep) drains
            # now, not at the first write (plan 1.5). One status read; only a non-empty queue is kicked.
            try:
                waiting = Journal.read_status(self.journal.dir) or {}
                if int(waiting.get("pending") or 0) or int(waiting.get("waiting") or 0):
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
                    if int(shared.get("pending") or 0) or int(shared.get("waiting") or 0):
                        from ..delivery import outbox as outbox_worker

                        outbox_worker.maybe_spawn(str(root))
            except Exception:  # noqa: BLE001 -- a kick is latency, never a gate
                pass
