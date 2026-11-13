"""QueuedSink: an async client's writes are queued in its journal for later delivery, and where
the outbox journal is (the $TMPDIR fallback, the Kubernetes root-disk notice)."""

from __future__ import annotations

import errno
import os
import time
from pathlib import Path
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ...secret_gate import check_upload
from .. import sink as _sink
from ..journal.journal import Journal
from ..status_fields import StatusField
from ..ops.classify import classify as _journal_classify
from ..sender import SendPolicy, is_queue_only
from ..sink import HeldClient, SinkKind
from ... import routes

#: Outbox directories this process has already warned about falling back from.
_FALLBACK_WARNED: set[str] = set()
_K8S_NOTICE_GIVEN = False


def _usable_journal(directory: Path | None) -> Journal:
    """The journal a `Client` should queue in: ``directory`` (default: the machine's
    outbox) when it can take appends, else the ``$TMPDIR`` fallback with ONE warning that
    it does not survive a pod or machine restart (plan 1.5). An unusable queue used to drop
    every write, one warning each; an explicit unusable ``PROBE_OUTBOX_DIR`` falls back too."""
    from ..journal.paths import fallback_dir, private_fallback_root

    primary = Journal(directory)
    try:
        reason = primary.usable()
    except Exception:  # noqa: BLE001 -- cannot tell: keep the configured queue
        return primary
    if reason is None:
        if (
            directory is None
            and not os.environ.get("PROBE_OUTBOX_DIR")
            and _under_private_fallback(primary.dir, private_fallback_root)
        ):
            # No home directory (`journal.default_root`): the default already IS the
            # fallback, which must still be said once.
            _warn_fallback(primary, "there is no home directory", primary)
        elif directory is None:
            # Only the DEFAULT outbox: an explicit `spool_dir` is the caller's choice (review
            # of #2054).
            _kubernetes_notice(primary)
        return primary
    try:
        fallback = Journal(fallback_dir())
        if fallback.dir == primary.dir or fallback.usable() is not None:
            return primary
    except Exception:  # noqa: BLE001
        return primary
    _warn_fallback(primary, reason, fallback)
    return fallback


def _under_private_fallback(path: Path, private_fallback_root) -> bool:
    try:
        return path.is_relative_to(private_fallback_root())
    except Exception:  # noqa: BLE001
        return False


def _warn_fallback(primary: Journal, reason: str, fallback: Journal) -> None:
    if str(primary.dir) in _FALLBACK_WARNED:
        return
    _FALLBACK_WARNED.add(str(primary.dir))
    where = (
        f"queueing in {fallback.dir}"
        if fallback.dir == primary.dir
        else f"the outbox at {primary.dir} cannot be used; queueing in {fallback.dir} instead"
    )
    small = ""
    try:
        import shutil

        free = shutil.disk_usage(fallback.dir if fallback.dir.exists() else fallback.dir.parent).free
        if free < 256 * 1024 * 1024:
            # A small tmpfs: most writes will be sent directly or dropped, and this is the
            # one place that can say why (review of #2054).
            small = f" It has only {free // (1024 * 1024)} MiB free, so writes may be dropped."
    except OSError:
        pass
    _diagnostics.warn(
        f"probe: {reason}: {where}. That directory does NOT survive a pod or machine "
        f"restart: set PROBE_OUTBOX_DIR to a writable, persistent path.{small}"
    )


def _kubernetes_notice(journal: Journal) -> None:
    """Once per process, on Kubernetes with the default outbox: the queue sits on the
    container's disk and the detached worker dies with the pod, so writes still queued when
    the pod is deleted are lost (plan 1.5)."""
    global _K8S_NOTICE_GIVEN
    if (
        _K8S_NOTICE_GIVEN
        or not os.environ.get("KUBERNETES_SERVICE_HOST")
        or os.environ.get("PROBE_OUTBOX_DIR")
        or os.environ.get("PROBE_OUTBOX_WORKER")
        or not _on_container_root_disk(journal.dir)
    ):
        return
    _K8S_NOTICE_GIVEN = True
    _diagnostics.warn(
        f"probe: running on Kubernetes with the outbox on the container's disk "
        f"({journal.dir}); writes still queued when the pod is deleted are lost. Set "
        "PROBE_OUTBOX_DIR to a persistent volume, and PROBE_FINISH_TIMEOUT_SEC=600 with "
        "terminationGracePeriodSeconds at least that long."
    )


def _on_container_root_disk(path: Path) -> bool:
    """Whether ``path`` is on the same filesystem as ``/`` (the container's writable layer).
    A HOME that is a mounted volume (JupyterHub's per-user PV) is another device and the
    notice would be wrong there (review of #2054)."""
    try:
        probe_path = path
        while not probe_path.exists() and probe_path.parent != probe_path:
            probe_path = probe_path.parent
        return os.stat(probe_path).st_dev == os.stat("/").st_dev
    except OSError:
        return False


#: An append that failed for want of space (plan 1.5): ENOSPC, and EDQUOT
#: where the platform has it.
_OUT_OF_SPACE = frozenset(
    code for code in (errno.ENOSPC, getattr(errno, "EDQUOT", None)) if code is not None
)


class QueuedSink:
    """Queues in `client.journal`, for every async client. Holds no state: the client keeps its counters.

    That journal is the live outbox `<outbox>/`, which a background drainer delivers, or an offline
    run's own queue `<outbox>/offline/<creation_key>/`, which only `probe sync` delivers
    (`client._drains_by_hand`). The sink never decides who delivers: it wakes the drainer the client
    picked (`pick_drainer`), and `send_instead_of_queueing` refuses a queue drained by hand."""

    kind = SinkKind.QUEUED
    _client = HeldClient()

    def __init__(self, client: Any) -> None:
        self._client = client

    def queues(self, *, strict: bool, sync: bool) -> bool:
        # strict means "fail loudly, never journal": a demand for the network, so it implies sync.
        return not sync and not strict

    def land(
        self, method: str, path: str, body: dict | None, *, policy: SendPolicy, blocking: bool, admitted: bool,
    ) -> Any:
        """Queue the write, or send it around the queue below the free-space floor; a strict or
        sync write goes out now as a sync client's would."""
        client = self._client
        if not self.queues(strict=policy.strict, sync=policy.sync):
            return client._delivery.sender.land(method, path, body, policy=policy, blocking=blocking, admitted=admitted)
        if client._send_instead_of_queueing(method, path, body):
            return None
        if client._enqueue(
            method,
            path,
            body,
            blocking=blocking,
            prepared=True,
            direct_ok=True,
            admitted=admitted,
        ):
            client._after_enqueue()
        return None

    def enqueue(
        self,
        method: str,
        path: str,
        body: dict | None,
        *,
        blocking: bool = True,
        validation_error: str | None = None,
        prepared: bool = False,
        admitted: bool = False,
        direct_ok: bool = False,
    ) -> bool:
        """Journal one op; returns whether it landed and never raises for a failure of ours (a full or
        read-only disk, `flock` ENOSYS): the gap is recorded and counted on `dropped_writes`.
        KeyboardInterrupt/SystemExit propagate. ``direct_ok``: try a direct send before dropping for
        want of space (plan 1.5). ``prepared``: the body was normalized and checked already."""
        client = self._client
        try:
            options: dict[str, Any] = (
                {"validation_error": validation_error} if validation_error is not None else {}
            )
            if prepared:
                options["_prepared"] = True
            if admitted:
                options["admitted"] = True
            client.journal.append_http(method, path, body, blocking=blocking, **options)
            return True
        except (KeyboardInterrupt, SystemExit):
            # A Ctrl-C (or `sys.exit`) mid-append is the user stopping the process, not a
            # broken outbox: counting it a dropped write let training carry on past the
            # Ctrl-C and closed an interrupted run with a drop notice. Nothing is left
            # half-written: `write_text_atomic` unlinks its temp file, and the op file
            # either landed whole (it delivers) or not at all.
            raise
        except BaseException as enqueue_error:  # noqa: BLE001
            if (
                direct_ok
                and isinstance(enqueue_error, OSError)
                and enqueue_error.errno in _OUT_OF_SPACE
                and client._send_instead_of_queueing(method, path, body, out_of_space=True)
            ):
                return True
            client.dropped_writes += 1
            try:
                # Once per drop: a refusal at the cap was already recorded by the journal
                # (review of #2014: each drop rewrote the producer file twice).
                if not getattr(enqueue_error, "gap_recorded", False):
                    client.journal.note_capture_gap(str(enqueue_error))
            except Exception:  # noqa: BLE001 -- the journal is the thing that broke
                pass
            # One line per kind, then at most one per 5 min with the running count (plan
            # 1.7): a warning per drop was 44 lines for 50 drops.
            client._note_drop(f"{method} {path}: {_diagnostics.describe(enqueue_error)}")
            # The warning reaches the operator's terminal and nothing else. This is DATA
            # LOSS (neither server nor journal got the write): exactly what must not stay local.
            _sink._capture_swallowed(
                enqueue_error,
                site="client.enqueue_dropped",
                base_url=client.settings.base_url,
                spool_dir=str(client.journal.dir),
            )
            return False

    def enqueue_upload(self, **kwargs) -> dict | None:
        """Journal one byte upload; returns the journal's result, or None when it could not be queued, and
        never raises for a failure of ours. Catches ``Exception``, not ``BaseException``, so Ctrl-C still
        interrupts a multi-GB copy. Built-in redaction is off (scanning disabled); a caller's `_redact`
        still runs on ``meta``. ``notes`` is dropped."""
        client = self._client
        check_upload(kwargs.get("src_path"))
        try:
            # INSIDE the try: redaction is arbitrary code (the caller's especially) and one
            # that raises would escape a method that never raises, taking out the caller's
            # synchronous fallback.
            # scanning disabled: from ...redaction import default_scrub, scrub_text

            kwargs.pop("notes", None)
            meta = kwargs.get("meta")
            if isinstance(meta, dict):
                # scanning disabled: scrubbed = default_scrub(meta)
                scrubbed = meta
                if isinstance(scrubbed, dict):
                    # default_scrub caught the sensitive KEYS; scrub_text catches
                    # a secret sitting in prose under an innocent one.
                    scrubbed = {
                        # scanning disabled: k: (scrub_text(v) if isinstance(v, str) else v) for k, v in scrubbed.items()
                        k: v for k, v in scrubbed.items()
                    }
                kwargs["meta"] = scrubbed
            if client._redact is not None and isinstance(kwargs.get("meta"), dict):
                # Only structured values go to a caller redactor (declared dict -> dict):
                # round-tripping a string through a wrapper key DROPPED the value when the
                # redactor returned an allowlisted subset.
                kwargs["meta"] = client._redact(kwargs["meta"])
            # scanning disabled: kwargs = default_scrub(kwargs)
            return client.journal.append_upload(**kwargs)
        except Exception as enqueue_error:  # noqa: BLE001 -- see the docstring
            client.dropped_writes += 1
            try:
                if not getattr(enqueue_error, "gap_recorded", False):
                    client.journal.note_capture_gap(str(enqueue_error))
            except Exception:  # noqa: BLE001 -- the journal is the thing that broke
                pass
            client._note_drop(
                f"upload {kwargs.get('name')!r}: {_diagnostics.describe(enqueue_error)}"
            )
            _sink._capture_swallowed(
                enqueue_error,
                site="client.enqueue_upload_dropped",
                base_url=client.settings.base_url,
                spool_dir=str(client.journal.dir),
            )
            return None

    def send_instead_of_queueing(
        self, method: str, path: str, body: dict | None, *, out_of_space: bool = False
    ) -> bool:
        """Below the outbox's free-space floor, send ``body`` now rather than drop it (plan 1.5); True when
        it landed. Only while the run has nothing queued (the first write of a series and step wins),
        bounded in time, never for an offline queue. ``out_of_space``: the append itself hit ENOSPC."""
        client = self._client
        if getattr(client, "_drains_by_hand", False) or is_queue_only():
            return False
        journal = client.journal
        if not out_of_space:
            try:
                if journal.below_floor() is None:
                    return False
            except Exception:  # noqa: BLE001 -- the journal decides on its own below
                return False
        from ..journal.run_ops import RunOps

        run_ref = routes.run_ref_of(path)
        now = time.monotonic()
        with client._direct_lock:
            if run_ref is None or now < client._direct_closed_until:
                return False
        try:
            # Proving the run clear parses queued op files on first ask (this thread). A
            # deep queue means delivery is behind anyway: no direct send, no seconds-long
            # first scan (review of #2054).
            status = Journal.read_status(journal.dir, include_receipts=False) or {}
            if int(status.get(StatusField.PENDING) or 0) > client.DIRECT_SEND_MAX_QUEUED:
                return False
            with client._direct_lock:
                lane = client._lanes.get(run_ref)
                if lane is None:
                    # Every queue of the outbox: a write of this run queued under another
                    # credential (#2035) is overtaken just the same (#2041 round 4).
                    lane = client._lanes[run_ref] = RunOps(
                        journal, run_ref, blocking_only=False, queues=journal.outbox_queues()
                    )
            if lane.pending():
                # Queued ops hold this write back, and on a full disk it is dropped before
                # queueing, so no enqueue will kick the drainer. Kick it here (throttled), or
                # an op whose worker exited strands and every later write of the run is
                # dropped behind it (7-day soak, 0.200.2).
                client._kick_drainer()
                return False
        except Exception:  # noqa: BLE001 -- cannot prove the run is clear: queue it
            return False
        from ..transport.deadlines import deadline_scope

        try:
            from ..ops.op_handler import gate_samples_body

            with deadline_scope(now + client.DIRECT_SEND_TIMEOUT_SECONDS):
                client.transport.request(method, path, json_body=gate_samples_body(client, method, path, body))
        except Exception as exc:  # noqa: BLE001 -- the write falls back to the queue
            try:
                # Only a failure saying the SERVER is down or refusing everyone opens the
                # breaker. A 422/409 is about this write: closing direct sends for every run
                # dropped every good write under low disk for minutes (review of #2054).
                if _journal_classify(exc) in ("transient", "auth"):
                    with client._direct_lock:
                        client._direct_failures += 1
                        first, ceiling = client.DIRECT_SEND_BACKOFF
                        wait = min(ceiling, first * 2 ** (client._direct_failures - 1))
                        client._direct_closed_until = time.monotonic() + wait
            except Exception:  # noqa: BLE001 -- the breaker may never raise out of write()
                pass
            return False
        with client._direct_lock:
            client._direct_failures = 0
            client.direct_sends += 1
        return True
