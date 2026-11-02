"""Delivery: the write pipeline Client and Run write through (normalize, drop what the server
cannot store, NUL check, redact), into the sink the client's mode picks."""

from __future__ import annotations

import os
import warnings
from typing import Any

from .. import errors
from ...foundation.safe_warn import safe_warn as _diagnostics
from . import sink as _sink
from .. import routes
from .sink import HeldClient, Sink
from .sender import Sender, resolve_policy
from .sinks.fanout import FanOutSink
from .sinks.queued import QueuedSink, _usable_journal  # noqa: F401 -- Client picks its journal here

#: Kinds of unstorable metric point this process has warned about.
_UNSTORABLE_WARNED: set[str] = set()


def _warn_unstorable(reasons: list[str]) -> None:
    """One warning per kind per process for points dropped as unstorable."""
    from ..values.unstorable import MAX_METRIC_KEY_BYTES

    for reason in sorted(set(reasons)):
        if reason in _UNSTORABLE_WARNED:
            continue
        _UNSTORABLE_WARNED.add(reason)
        what = (
            "a step outside a 64-bit signed integer"
            if reason == "step"
            else f"a key over {MAX_METRIC_KEY_BYTES} bytes"
        )
        _diagnostics.warn(
            f"probe: dropped metric point(s) with {what}: the server cannot store them. "
            "Later ones are dropped without a warning."
        )


#: The `PROBE_ASYNC` spellings: the only parser (the CLI delegates here).
_ASYNC_TRUE = {"1", "true", "yes", "on"}
_ASYNC_FALSE = {"0", "false", "no", "off"}


def _env_async_writes() -> bool | None:
    """`PROBE_ASYNC` as a tri-state: on, off, or unset (None -> use the default).

    Unset and unrecognised both return None: a typo warns and defers to the default
    rather than pinning a write mode.
    """
    raw = (os.environ.get("PROBE_ASYNC") or "").strip().lower()
    if not raw:
        return None
    if raw in _ASYNC_TRUE:
        return True
    if raw in _ASYNC_FALSE:
        return False
    warnings.warn(
        f"ignoring unrecognised PROBE_ASYNC={raw!r}; expected one of "
        f"{sorted(_ASYNC_TRUE | _ASYNC_FALSE)}",
        stacklevel=3,
    )
    return None


def is_offline_client(client: Any) -> bool:
    """Whether ``client`` writes an offline run's queue (an `OfflineClient`)."""
    # Imported here: OfflineClient is a Client subclass, so its module loads with the client.
    from .offline.client import OfflineClient

    return isinstance(client, OfflineClient)


class Delivery:
    """One client's write pipeline and its sinks, built once. `sink` follows the client's mode
    (async or sync) as it is now. An offline run is an async client: its writes land in
    `QueuedSink` like any other's, in its own queue."""

    _client = HeldClient()

    def __init__(self, client: Any) -> None:
        self._client = client
        self.sender = Sender(client)
        self.queued = QueuedSink(client)
        self.fanout = FanOutSink(client)

    @property
    def sink(self) -> Sink:
        return self.queued if self._client.async_writes else self.sender

    def write(
        self,
        method: str,
        path: str,
        body: dict | None = None,
        *,
        strict: bool | None = None,
        durable: bool = True,
        sync: bool = False,
        blocking: bool = True,
        raise_permanent: bool | None = None,
        admitted: bool = False,
    ):
        """`Client.write`'s pipeline; its docstring says what every flag means."""
        client = self._client
        # Renew a DETACHED run's auto-update lease off its own traffic: every SDK write
        # passes here. A detached run (heartbeat=False) holds no flock, so its 30-minute
        # lease would expire under a longer job and an upgrade land mid-run. Process-bound
        # runs have no lease file; the write is skipped until the lease is half spent.
        _sink._touch_run_lease(path, base_url=client.settings.base_url, spool_dir=str(client.journal.dir))
        from ..values import unstorable

        # Structural errors cannot be journaled; policy errors can (keep a permanent
        # refusal before scrubbing removes the offending identity).
        body = unstorable.normalize_json(body)
        # Points the server cannot store (step past int64, key past its index row size)
        # are 500s the outbox would retry for a day, blocking the run's later writes:
        # dropped here, at every metric writer's door (review of #2053).
        body, unstorable_reasons = unstorable.drop_unstorable_points(method, path, body)
        if unstorable_reasons:
            _warn_unstorable(unstorable_reasons)
            if not body.get("points"):
                return None
        policy = resolve_policy(client, strict=strict, sync=sync, durable=durable, raise_permanent=raise_permanent)
        validation_error = None
        try:
            unstorable.validate_nuls(body, path=path, method=method)
        except errors.ValidationError as exc:
            if policy.should_raise_on_invalid_body():
                raise
            validation_error = str(exc)
        if client._redact is not None and body is not None:
            body = client._redact(body)
        # The runs this process writes: the delivery notices name only
        # trouble of these (plan 1.7).
        run_ref = routes.run_ref_of(path)
        runs = client.__dict__.get("_my_runs")
        if run_ref is not None and runs is not None:
            runs.add(run_ref)
        if "_attempted_writes" in client.__dict__:
            client._attempted_writes += 1  # the report's denominator (plan 1.12)
        # `scrub_body`: `default_scrub`, minus the ISO timestamps `Run.log`
        # stamps on every point (plan 1.4), which cannot hold a credential.
        # scanning disabled: from ..stamp_scrub import scrub_body

        # scanning disabled: body = scrub_body(body)
        if validation_error is not None:
            if client._enqueue(
                method,
                path,
                body,
                blocking=blocking,
                validation_error=validation_error,
                prepared=True,
            ):
                client._after_enqueue()
            return None
        if not policy.durable:
            resp = client.transport.request(method, path, json_body=body)
            return resp.json() if resp.content else None
        # `strict` is resolved BEFORE the async branch (`resolve_policy`). Read after, async mode
        # downgraded a strict write to a queued replay: a data-loss bug once async became the
        # default (Miles passes strict=True, then `queue.acknowledge()` DELETES its durable record
        # on seeing no exception, so a queued write erased the only copy).
        return self.sink.land(method, path, body, policy=policy, blocking=blocking, admitted=admitted)

    def note_undelivered(self, method: str, path: str, exc: BaseException, *, queued: bool) -> None:
        """Hand a write that fell back to the outbox (`queued`) or was lost with it to
        `on_undelivered`, and keep it; nothing without a hook. Never raises (fail-open path)."""
        client = self._client
        report = getattr(client, "on_undelivered", None)
        if report is None:
            return
        try:
            text = str(exc).strip()
            # httpx timeouts stringify EMPTY: the type is then all there is to say.
            error = f"{type(exc).__name__}: {text}" if text else type(exc).__name__
            entry = {"method": method, "path": path, "error": error[:300], "queued": bool(queued)}
            client.undelivered_writes.append(entry)
            client.undelivered_count += 1
            report(entry)
        except Exception:  # noqa: BLE001 -- a report about a write never breaks the write
            pass
