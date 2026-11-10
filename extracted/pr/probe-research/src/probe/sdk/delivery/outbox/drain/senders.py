"""DrainSendersMixin: the client each op goes out with (one per credential and route, kept for the
worker's life by `SenderClients`), and sending an op, a batch or an upload window."""

from __future__ import annotations

from collections import OrderedDict
from contextlib import nullcontext
import os
from pathlib import Path
import threading
from typing import Any

from probe.sdk import errors
from probe.sdk.session_marker import SIGN_IN_HINT


#: Ops looked at per parallel window, as a multiple of the worker count. Bounded because a
#: window is read into memory and the serial loop behind it decides everything: a larger
#: window buys nothing once the link is saturated and costs re-work when the pass stops early.
UPLOAD_WINDOW_FACTOR = 4
#: Ops a window may look past to fill itself, as a multiple of its size. A run queue of
#: metric points holds no upload to find; scanning the rest at every window cost a drain of
#: 6,000 such ops 565,504 op reads.
UPLOAD_WINDOW_SCAN_FACTOR = 4


class SenderClients:
    """The clients drain passes send with, one per pinned context, credential and route, kept
    across passes (I13): the worker's next pass reuses an open keep-alive connection instead of a
    TLS handshake per pass (~2,800/s at 10k runs). A client whose credential or base URL changed
    is replaced; a forked child starts empty (the sockets are its parent's, never closed here)."""

    #: Clients kept across passes at most; the least recently used is closed first.
    MAX_CLIENTS = 32

    def __init__(self) -> None:
        self._clients: OrderedDict[tuple, Any] = OrderedDict()
        self._pid = os.getpid()
        self._lock = threading.Lock()

    def take_client(self, key: tuple, settings: Any, client_class: Any) -> Any:
        """The client for ``key``: the kept one while its class and ``settings`` (token, base URL,
        workspace) are unchanged, else a new one."""
        with self._lock:
            if self._pid != os.getpid():
                self._clients = OrderedDict()
                self._pid = os.getpid()
            kept = self._clients.pop(key, None)
            if kept is not None and type(kept) is client_class and getattr(kept, "settings", None) == settings:
                self._clients[key] = kept
                return kept
            if kept is not None:
                _close_quietly(kept)
            # async_writes=False because THIS is the drainer: an async client mints a
            # producer record (`sdk:{host}:{pid}:{uuid4}`) per construction, and a long
            # outage would litter producers/ with single-use entries in the registry that makes
            # capture loss visible. NOT because replay would re-journal: replay never goes
            # through `Client.write`, it uses `transport.request` and `upload_fingerprinted`
            # directly; write mode does not govern the drain path.
            client = client_class(settings=settings, async_writes=False)
            self._clients[key] = client
            return client

    def start_pass(self) -> None:
        """Before a pass (none holds a client then): keep the `MAX_CLIENTS` most recently used,
        and have each re-ask what the server supports, as a client built per pass did, so a
        deploy that adds or rolls back a route is seen by the next pass."""
        with self._lock:
            while len(self._clients) > self.MAX_CLIENTS:
                _close_quietly(self._clients.popitem(last=False)[1])
            for client in self._clients.values():
                forget = getattr(client, "_forget_server_features", None)
                if callable(forget):
                    forget()

    def close(self) -> None:
        """Close every kept client (the worker is exiting, or a pass that built its own ended)."""
        with self._lock:
            clients, self._clients = list(self._clients.values()), OrderedDict()
            if self._pid != os.getpid():
                return  # a forked child's copies: the parent's sockets
        for client in clients:
            _close_quietly(client)


def _close_quietly(client: Any) -> None:
    try:
        client.close()
    except Exception:  # noqa: BLE001 -- a close never stops delivery
        pass


class DrainSendersMixin:
    """Part of DrainPass: its methods run with `self` the DrainPass; fold_parts() copies them into DrainPass."""

    def _start_senders(self) -> None:
        """The client class and the credential state every send of this pass shares."""
        self.client_class = delivery_client()  # loaded here, not at import: enqueue paths must not import httpx

        # Per pass: what each key resolved to (a client, or a `CredentialNotHere` asked once).
        self.clients: dict[tuple, Any] = {}
        # The worker's clients outlive the pass (I13); any other drain's are closed at its end.
        shared = self.options.senders
        self.should_close_senders = shared is None
        self.sender_clients = SenderClients() if shared is None else shared
        if shared is not None:
            shared.start_pass()

        # Credentials the API refused (#2041 review): fingerprint -> when. Earlier passes' come
        # from status.json, so a refused credential is re-tried once per cooldown, not per pass;
        # this pass's refusals apply to every later op of that credential, the writer's own too.
        self.cooling = _cooling_refusals(self.journal)
        self.refused_now: dict[str, str] = {}
        # Fingerprint -> adopted (`probe outbox adopt`), read once per pass.
        self.adoptions: dict[str, bool] = {}
        # Adopted fingerprint -> the fingerprint of the login its writes go out with this pass. A
        # refusal of THAT login is recorded under it too, so the banner names it and its cooldown
        # holds the adopted writes back as well.
        self.adopted_login: dict[str, str] = {}
        self.delivered_fps: set[str] = set()
        # One token is one account: what any of a token's writes recorded vouches for all of them
        # (#2041 re-review). Filled from the queue below.
        self.accounts: dict[str, tuple[str, str]] = {}
        self.learned: set[str] = set()

    # -- senders --------------------------------------------------------------------------------
    def is_adopted(self, fingerprint: str) -> bool:
        if fingerprint not in self.adoptions:
            self.adoptions[fingerprint] = adopted_account(fingerprint) is not None
        return self.adoptions[fingerprint]

    def record_token_account(self, op: dict) -> None:
        """After a stored-login write went out with ITS OWN token: remember which account that
        token is, once per token (`record_account`), so its other writes can follow a
        same-account re-login (a login saved by the setup wizard or an older CLI records none,
        #2041 round 3)."""
        stamp = (op.get("context") or {}).get("principal")
        if not isinstance(stamp, dict) or stamp.get("source") != CredentialSource.CONFIG:
            return
        fp = stamp.get("fingerprint")
        if not fp or op_credential(op)[1] or fp in self.learned or stamp_identity(stamp) or fp in self.accounts:
            return
        self.learned.add(fp)
        try:
            if recorded_account(fp) is not None:
                return
            sender = self.choose_client(op.get("context"))
            settings = getattr(sender, "settings", None)
            if settings is None or credential_fingerprint(settings.token, None) != fp:
                return  # went out with a later login (the account was known): nothing to learn
            record_account(
                fp,
                _identity_of(settings, getattr(sender, "transport", None)),
                login_of=_login_base_of(op.get("context"), settings.base_url),
            )
        except Exception:  # noqa: BLE001 -- evidence for later, never a delivery step
            return

    def choose_client(self, context: dict | None, ingest: bool = False, op: dict | None = None):
        """The client that sends ``op`` (pinned ``context``): one per context, credential and route
        per pass; raises `CredentialNotHere` / `AdoptedRouteRefused` for a write it must not send."""
        stamp = (context or {}).get("principal")
        stamped_fp = None
        if isinstance(stamp, dict):
            stamped_fp = stamp.get("ingest_fingerprint") if ingest else stamp.get("fingerprint")
        key = ((context or {}).get("name"), (context or {}).get("base_url"), stamped_fp, ingest)
        # What a client_factory is told: the route, so it matches the right key.
        asked = {**context, "route": "ingest"} if (ingest and isinstance(context, dict)) else context
        self._refuse_refused_credential(stamped_fp, ingest, asked)
        self._refuse_adopted_route(op, stamped_fp, ingest, asked)
        if isinstance(self.clients.get(key), CredentialNotHere):
            # A fresh instance: re-raising one object grows its traceback per op.
            raise CredentialNotHere(str(self.clients[key]), permanent=self.clients[key].permanent)
        if key not in self.clients:
            self._build_client(context, key, asked, stamp, stamped_fp, ingest)
        return self.clients[key]

    def _refuse_refused_credential(self, stamped_fp, ingest: bool, asked) -> None:
        """Raise `CredentialNotHere` for a credential the API refused, this pass or (cooling) before."""
        client_factory = self.options.client_factory
        refused_at = self.refused_now.get(stamped_fp) if stamped_fp else None
        if (
            refused_at is None
            and stamped_fp in self.cooling
            and (ingest or not self.is_adopted(stamped_fp))
            and (client_factory is None or client_factory(asked) is None)
        ):
            # Refused in an earlier pass. The writer itself (client_factory) may still try: a
            # re-login it picked up is how its writes recover. So may an adopted credential's
            # writes, which go out with the stored login now: the refusal on record is of the
            # dead token, which a job still running with it re-records every cooldown.
            refused_at = self.cooling[stamped_fp]
        if refused_at is not None:
            # Set aside with every other write of that credential: no re-asking the API, no
            # holding anyone else's writes up.
            raise CredentialNotHere(
                f"its credential was refused by the API at {refused_at}; it waits for a "
                f"new sign-in ({SIGN_IN_HINT}), or for the process that holds that credential"
            )

    def _refuse_adopted_route(self, op: dict | None, stamped_fp, ingest: bool, asked) -> None:
        """Raise `AdoptedRouteRefused` for an adopted credential's write the stored login may not send."""
        client_factory = self.options.client_factory
        if (
            op is not None
            and stamped_fp
            and not ingest
            and self.is_adopted(stamped_fp)
            and (client_factory is None or client_factory(asked) is None)
        ):
            refused_here = adopted_route_refuses(op)
            if refused_here is not None:
                raise AdoptedRouteRefused(
                    f"queued with a revoked credential that was adopted, but {refused_here} "
                    "(`probe outbox retry` requeues it if that credential comes back)",
                    status=422,
                )

    def _build_client(self, context, key: tuple, asked, stamp, stamped_fp, ingest: bool) -> None:
        """Make (or take from ``client_factory``) the client for ``key`` and keep it for the pass."""
        client_factory = self.options.client_factory
        supplied = client_factory(asked) if client_factory is not None else None
        if supplied is not None:
            self.clients[key] = supplied
            return
        try:
            if stamped_fp and not ingest and self.is_adopted(stamped_fp):
                # Before `_settings_for_op`, whose account check is the
                # login's first request and may be what is refused.
                login_fp = _stored_login_fingerprint(context)
                if login_fp:
                    self.adopted_login[stamped_fp] = login_fp
                login_refused = self.refused_now.get(login_fp or "") or self.cooling.get(
                    login_fp or ""
                )
                if login_refused:
                    raise CredentialNotHere(
                        f"adopted by the login stored here, which the API refused at "
                        f"{login_refused}; it waits for a new sign-in ({SIGN_IN_HINT})"
                    )
            account = self.accounts.get((stamp or {}).get("fingerprint") or "")
            settings = _settings_for_op(context, ingest=ingest, account=account)
        except CredentialNotHere as absent:
            self.clients[key] = absent  # asked once per pass, not once per op
            raise
        if not settings.token and not settings.ingest_token:
            raise errors.AuthError(
                f"no credentials for context {key[0] or '<default>'} ({SIGN_IN_HINT})"
            )
        self.clients[key] = self.sender_clients.take_client(key, settings, self.client_class)

    def _send_upload_window(self, position: int) -> bool:
        """Send the uploads in the window ahead of ``position`` in parallel. False ends the pass."""
        workers = self.workers
        consumed = self.consumed
        prefetched = self.prefetched
        ahead = self.queued[
            position : position + workers * UPLOAD_WINDOW_FACTOR * UPLOAD_WINDOW_SCAN_FACTOR
        ]
        if self.drain_hold.let_go:
            # Another drain may have sent or changed some of these while this pass was
            # away: only what is still queued may go.
            ahead = [
                item for item in ahead
                if item[0] in consumed or self.drain_hold.fresh(*item)
            ]
        try:
            landed = _prefetch_uploads(
                self.journal,
                ahead,
                self.choose_client,
                workers,
                self.options.run_ref,
                skips=self.should_skip_in_window,
                already=prefetched.keys() | consumed,
                away=self.drain_hold.away,
            )
        except _LockNotBack:
            # Its uploads stay queued (results unrecorded) for the next drain, which
            # sends them again: a file the server holds gets its row back, no bytes move
            # twice.
            self.report.deadline_reached = True
            return False
        if self.drain_hold.yields:
            # Settled NOW, not when the serial pass reaches each: this pass lets go of
            # the drain lock again and another drain would send a landed upload whose op
            # file is still queued a second time (`_DrainHold.away`).
            prefetched.update(self.settle_window(ahead, landed))
        else:
            prefetched.update(landed)
        if landed or not any(
            isinstance(o, dict)
            and o.get("kind") == "upload"
            and p not in prefetched
            and p not in consumed
            for p, o in ahead
        ):
            self.cursor = position + workers * UPLOAD_WINDOW_FACTOR
        else:
            # Uploads ahead, none free to go yet: an op in front of them (a run's
            # metadata, a span) goes first. Look again right after it, not a window
            # later (a run's first 30 uploads went one by one behind its first write).
            self.cursor = position + 1
        return True

    # -- sending --------------------------------------------------------------------------------
    def _send_batch(
        self, path: Path, op: dict, lane: Any, metric_ops: list, step_ops: list, sample_ops: list = ()
    ) -> bool:
        """Plans 1.2 and T4: this op and the telemetry queued behind it in its run: its metric ops
        as ONE `/metrics` POST, its step records as ONE `/steps/batch` POST (one each on an older
        server), head's kind first; or its sample ops as ONE `/samples/batch` POST. False ends
        the pass."""
        sample_ops = list(sample_ops)
        batch = [*metric_ops, *step_ops, *sample_ops]
        # Settled OUTSIDE the per-op `try`: an error while settling must not send the head
        # through `settle_failure` again after it landed (review of #2053).
        try:
            client = self.choose_client(op.get("context"), op=op)
        except OpHeldHere as held:
            # Every op of the batch shares the head's context (it is in
            # `_merge_key`), so none of them is this drainer's to send.
            self.hold(lane, batch, held)
            return True
        except Exception as exc:  # noqa: BLE001 -- the head's failure, as alone
            if self.settle_failure(path, op, exc, lane) == "break":
                return False
            return True
        self.consumed.update(item[0] for item in batch)
        landed, failed, merged = [], [], 0
        parts = [(metric_ops, _send_merged), (step_ops, None)]
        if not metric_ops or metric_ops[0][0] != path:
            parts.reverse()
        parts.append((sample_ops, _send_samples))
        for part, send in parts:
            if not part:
                continue
            if part is step_ops and steps_batch_supported(client):
                send = _send_steps
            with _delivery_scope(part[0][1]):
                got, lost, joined, stopped = _deliver_items(self.journal, client, part, self.run_ids, send)
            landed += got
            failed += lost
            merged += joined
            if stopped:
                break  # the rest stays queued behind the op that stopped it
        self.report.coalesced += merged
        try:
            action = self.settle_batch(batch, landed, failed, lane)
        except Exception as exc:  # noqa: BLE001 -- e.g. ENOSPC recording a failure
            # What landed may be sent again next pass (the insert keeps the first write
            # of a point); nothing is lost or resent now. The run waits for the rest of the
            # pass: an unsettled op of it is still queued and its later ops (its close)
            # must not go ahead of it (review of #2053).
            log.warning("outbox: settling a coalesced batch failed", exc_info=True)
            self.stalled[lane] = LaneStall(_redact(f"{type(exc).__name__}: {exc}"))
            action = "continue"
        if action == "break":
            return False
        return True

    def _send_one(self, path: Path, op: dict, lane: Any) -> bool:
        """Send one op and settle what came back. False ends the pass."""
        went_away = self.drain_hold.let_go  # the count before this op's attempt
        try:
            self._deliver(path, op, lane)
        except OpInProgress as progress:
            self._record_in_progress(progress, lane, op)
            return True
        except OpHeldHere as held:
            self.hold(lane, [(path, op)], held)
            return True
        except Exception as exc:  # noqa: BLE001 -- classified in settle_failure
            if (
                not isinstance(exc, _LockNotBack)
                and self.drain_hold.let_go != went_away
                and not path.exists()
            ):
                # Sent with the lock let go, and meanwhile a drain that knows no run locks (an
                # older release, `probe outbox discard`) delivered it or set it aside: writing
                # the op back would bring it back into the queue (#3618).
                return True
            if self.settle_failure(path, op, exc, lane) == "break":
                return False
            return True
        else:
            self._settle_landed(path, op, lane, went_away)
            return True

    def _deliver(self, path: Path, op: dict, lane: Any) -> None:
        """Send ``op`` (or find its receipt or prefetched upload) and record its receipt."""
        journal = self.journal
        if journal.receipt_enabled and op.get("schema") != DELIVERY_SCHEMA:
            raise errors.ValidationError(
                "unsupported delivery operation schema", status=422
            )
        if op.get("correlation") and journal.receipt(op["correlation"]) is not None:
            # Receipt committed before a crash prevented op deletion.
            result = None
        elif path in self.prefetched:
            # Its bytes already moved, in parallel with its neighbours. The receipt is
            # still written here, in order, on this thread (`_prefetch_uploads`).
            journal._save_delivery_receipt(op, self.prefetched[path])
        else:
            with _delivery_scope(op):
                sender = self.choose_client(op.get("context"), op_credential(op)[1], op=op)
                # An upload's bytes go with the drain lock let go and its run's lock held
                # (#3618): a 30 MiB file no longer holds every other run's close for the
                # length of its PUT.
                sending = (
                    self.drain_hold.away({lane})
                    if op.get("kind") == "upload" and not op.get("correlation")
                    else nullcontext()
                )
                with sending:
                    result = _execute(journal, sender, path, op, self.run_ids)
            journal._save_delivery_receipt(op, result)
        delivered_fp = _stamp_fingerprint(op)
        if delivered_fp is not None:
            self.delivered_fps.add(delivered_fp)
            self.record_token_account(op)
from probe.sdk.delivery.outbox.drain.adoption import AdoptedRouteRefused  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import CredentialNotHere  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import CredentialSource  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import DELIVERY_SCHEMA  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import LaneStall  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import OpHeldHere  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import OpInProgress  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.lock import _LockNotBack  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import _cooling_refusals  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.coalesce import _deliver_items, _send_merged, _send_samples, _send_steps, steps_batch_supported  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import _delivery_scope  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import _execute  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import _identity_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import _login_base_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.upload_windows import _prefetch_uploads  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.classify import _redact  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import _settings_for_op  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import _stamp_fingerprint  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import _stored_login_fingerprint  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import adopted_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import adopted_route_refuses  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import credential_fingerprint  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import delivery_client  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.journal import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import op_credential  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.accounts import record_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.accounts import recorded_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import stamp_identity  # noqa: E402 -- pieces need each other; the front door loads this one first
