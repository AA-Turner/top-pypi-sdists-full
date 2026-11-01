"""Delivery: the write pipeline Client and Run write through (normalize, drop what the server
cannot store, NUL check, redact), into the sink chosen once from the client's mode."""

from __future__ import annotations

import importlib
import os
import warnings
from typing import Any

from .. import errors
from ...foundation.safe_warn import safe_warn as _diagnostics
from . import sink as _sink
from .ops.ops import run_ref_for_path
from .sink import HeldClient, Sink
from .sinks.direct import DirectSink
from .sinks.fanout import FanOutSink
from .sinks.journaled import JournalSink, _usable_journal  # noqa: F401 -- Client picks its journal here

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


#: The offline sink and client, by name: their module holds OfflineClient, a Client subclass,
#: so it loads with the client (which imports this module) and is only looked up when needed.
OFFLINE_SINK = "probe.sdk.delivery.sinks.offline:OfflineSink"
OFFLINE_CLIENT = "probe.sdk.delivery.sinks.offline:OfflineClient"


def _by_name(target: str) -> Any:
    module, _, name = target.partition(":")
    return getattr(importlib.import_module(module), name)


def is_offline_client(client: Any) -> bool:
    """Whether ``client`` writes an offline run's queue (an `OfflineClient`)."""
    return isinstance(client, _by_name(OFFLINE_CLIENT))


class Delivery:
    """One client's write pipeline and its sinks. The sink is chosen once from the client's
    mode (async or sync, drained by hand or not), and again only if that mode is reassigned."""

    _client = HeldClient()

    def __init__(self, client: Any) -> None:
        self._client = client
        self.direct = DirectSink(client)
        self.journaled = JournalSink(client)
        self.fanout = FanOutSink(client)
        #: (mode, sink) as ONE value: two threads choosing at once never pair a mode with the other's sink.
        self._chosen: tuple[tuple[bool, bool], Sink] | None = None

    @property
    def sink(self) -> Sink:
        client = self._client
        mode = (bool(client.async_writes), bool(getattr(client, "_drains_by_hand", False)))
        chosen = self._chosen
        if chosen is None or chosen[0] != mode:
            if not mode[0]:
                sink = self.direct
            elif mode[1]:
                sink = _by_name(OFFLINE_SINK)(client)
            else:
                sink = self.journaled
            chosen = self._chosen = (mode, sink)
        return chosen[1]

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
        if raise_permanent is None:
            raise_permanent = bool(getattr(client, "raise_permanent", False))
        strict = (not client.fail_open) if strict is None else strict
        validation_error = None
        try:
            unstorable.validate_nuls(body, path=path, method=method)
        except errors.ValidationError as exc:
            if strict or raise_permanent or not durable:
                raise
            validation_error = str(exc)
        if client._redact is not None and body is not None:
            body = client._redact(body)
        # The runs this process writes: the delivery notices name only
        # trouble of these (plan 1.7).
        run_ref = run_ref_for_path(path)
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
        if not durable:
            resp = client.transport.request(method, path, json_body=body)
            return resp.json() if resp.content else None
        # Resolve `strict` BEFORE the async branch. Read after, async mode downgraded a
        # strict write to a queued replay: a data-loss bug once async became the default
        # (Miles passes strict=True, then `queue.acknowledge()` DELETES its durable record
        # on seeing no exception, so a queued write erased the only copy).
        # strict = "fail loudly, never journal" = a demand for the network, so it implies
        # sync and an explicit strict=True beats async mode.
        strict = (not client.fail_open) if strict is None else strict
        return self.sink.land(
            method, path, body, strict=strict, sync=sync, blocking=blocking,
            raise_permanent=raise_permanent, admitted=admitted,
        )

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
